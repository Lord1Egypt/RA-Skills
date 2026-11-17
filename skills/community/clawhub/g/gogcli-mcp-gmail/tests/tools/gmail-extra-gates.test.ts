import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { registerExtraGmailTools, BATCH_DELETE_PREVIEW_MAX } from '../../src/tools/gmail-extra.js';
import * as lib from '../../../gogcli-mcp/src/lib.js';
import { createTestHarness } from '@chrischall/mcp-utils/test';
import { rawTextResult } from '@chrischall/mcp-utils';
import type { ElicitRequest, ElicitResult } from '@modelcontextprotocol/server';
import { pos } from '../../../gogcli-mcp/src/argv.js';
import { resetConfirmTokenState } from '../../../gogcli-mcp/src/send-confirm-token.js';

vi.mock('../../../gogcli-mcp/src/lib.js', async (importOriginal) => {
  const actual = await importOriginal<typeof lib>();
  return { ...actual, runOrDiagnose: vi.fn() };
});

// ============================================================================
// Fleet audit 2026-09-24 SEC-6: a forced batch delete bypasses the Trash (and
// `force` is only the model's say-so), an enabled vacation responder replies to
// every sender, and a send-as alias makes Google email the address — each asks.
// ============================================================================

const ORIGINAL_ENV = { ...process.env };
beforeEach(() => {
  vi.clearAllMocks();
  process.env = { ...ORIGINAL_ENV };
  delete process.env.MCP_CONFIRM_MODE;
  process.env.GOG_ACCOUNT = 'me@example.com';
  resetConfirmTokenState();
});
afterEach(() => { process.env = ORIGINAL_ENV; });

const json = (r: { content: Array<{ text?: string }> }) => JSON.parse(r.content[0]!.text as string);
async function prompted(answer: ElicitResult = { action: 'accept', content: { confirmed: true } }) {
  const seen: ElicitRequest[] = [];
  const harness = await createTestHarness(registerExtraGmailTools, { elicitation: async (r) => { seen.push(r); return answer; } });
  const details = () => JSON.parse(seen[0]!.params.message.split('\n').slice(1).join('\n')).details;
  return { harness, seen, details };
}
const unprompted = () => createTestHarness(registerExtraGmailTools);

const META = (n: number) => JSON.stringify({ headers: { from: `sender${n}@example.com`, subject: `Invoice ${n}`, date: 'Mon, 21 Sep 2026 10:00:00 -0400' } });
function stub(failing?: string) {
  vi.mocked(lib.runOrDiagnose).mockImplementation(async (args) => {
    if (args[0] === 'gmail' && args[1] === 'get') {
      const id = String((args[2] as { value?: unknown }).value ?? args[2]);
      if (failing === id) return { content: [{ type: 'text', text: 'Error: not found' }], isError: true };
      return rawTextResult(id === 'bare' ? '{}' : META(Number(id.slice(1))));
    }
    return rawTextResult('{"ok":true}');
  });
}
const callsTo = (...words: string[]) => vi.mocked(lib.runOrDiagnose).mock.calls.filter(([args]) =>
  words.every((w, i) => args[i] === w));

describe('gog_gmail_batch_delete', () => {
  it('without force, neither reads nor asks — gog refuses on its own', async () => {
    stub();
    const { harness, seen } = await prompted();
    await harness.callTool('gog_gmail_batch_delete', { messageIds: ['m1'] });
    expect(seen).toHaveLength(0);
    expect(callsTo('gmail', 'get')).toHaveLength(0);
    expect(callsTo('gmail', 'batch', 'delete')[0]![0]).toEqual(['gmail', 'batch', 'delete', pos('m1')]);
  });

  it('reads each message and asks listing sender, subject and date', async () => {
    stub();
    const { harness, details, seen } = await prompted();
    await harness.callTool('gog_gmail_batch_delete', { messageIds: ['m1', 'bare'], force: true });
    expect(seen[0]!.params.message).toMatch(/PERMANENTLY deleting 2 message/);
    expect(details()).toEqual({
      count: 2,
      messages: [
        { id: 'm1', from: 'sender1@example.com', subject: 'Invoice 1', date: 'Mon, 21 Sep 2026 10:00:00 -0400' },
        { id: 'bare' },
      ],
    });
    expect(callsTo('gmail', 'batch', 'delete')[0]![0]).toEqual(['gmail', 'batch', 'delete', pos('m1'), pos('bare'), '--force']);
  });

  it(`names the first ${BATCH_DELETE_PREVIEW_MAX} and counts the rest`, async () => {
    stub();
    const ids = Array.from({ length: BATCH_DELETE_PREVIEW_MAX + 3 }, (_, i) => `m${i}`);
    const { harness, details } = await prompted({ action: 'decline' });
    await harness.callTool('gog_gmail_batch_delete', { messageIds: ids, force: true });
    expect(details().messages).toHaveLength(BATCH_DELETE_PREVIEW_MAX);
    expect(details().notShown).toBe(3);
    // Only the named ones are read (the rail may re-run the handler after the prompt, so count distinct ids).
    expect(new Set(callsTo('gmail', 'get').map(([args]) => JSON.stringify(args[2]))).size).toBe(BATCH_DELETE_PREVIEW_MAX);
    expect(callsTo('gmail', 'batch', 'delete')).toHaveLength(0);
  });

  it('returns a failed read without asking or deleting', async () => {
    stub('m2');
    const { harness, seen } = await prompted();
    expect((await harness.callTool('gog_gmail_batch_delete', { messageIds: ['m1', 'm2'], force: true })).isError).toBe(true);
    expect(seen).toHaveLength(0);
    expect(callsTo('gmail', 'batch', 'delete')).toHaveLength(0);
  });

  it('refuses a client that cannot be prompted, pointing at the Trash', async () => {
    process.env.MCP_CONFIRM_MODE = 'refuse';
    stub();
    const r = json(await (await unprompted()).callTool('gog_gmail_batch_delete', { messageIds: ['m1'], force: true }));
    expect(r).toMatchObject({ reason: 'confirmation-unsupported', action: 'gmail.batch-delete' });
    expect(r.note).toMatch(/gog_gmail_trash/);
  });

  it('token fallback: binds every id — a different set is refused, the same set deletes', async () => {
    process.env.MCP_CONFIRM_MODE = 'ask-user';
    stub();
    const harness = await unprompted();
    const args = { messageIds: ['m1', 'm2'], force: true };
    const p1 = json(await harness.callTool('gog_gmail_batch_delete', args));
    expect(p1.preview.count).toBe(2);
    const swapped = json(await harness.callTool('gog_gmail_batch_delete', { ...args, messageIds: ['m1', 'm3'], confirmToken: p1.confirmToken }));
    expect(swapped.error).toMatch(/DRAFT_CHANGED|TOKEN_INVALID/);
    await harness.callTool('gog_gmail_batch_delete', { ...args, confirmToken: p1.confirmToken });
    expect(callsTo('gmail', 'batch', 'delete')).toHaveLength(1);
  });
});

describe('gog_gmail_vacation_update', () => {
  const ON = { enable: true, subject: 'Away', body: '<p>Back Monday</p>', start: '2026-10-01T00:00:00Z', end: '2026-10-05T00:00:00Z' };

  it.each([
    [{ disable: true }, ['gmail', 'settings', 'vacation', 'update', '--disable']],
    [{ subject: 'Edited' }, ['gmail', 'settings', 'vacation', 'update', '--subject=Edited']],
  ])('does not ask for %j', async (args, argv) => {
    stub();
    const { harness, seen } = await prompted();
    await harness.callTool('gog_gmail_vacation_update', args);
    expect(seen).toHaveLength(0);
    expect(callsTo('gmail', 'settings', 'vacation')[0]![0]).toEqual(argv);
  });

  it('asks before turning it on, with the text, the window and who gets it', async () => {
    stub();
    const { harness, details } = await prompted();
    await harness.callTool('gog_gmail_vacation_update', ON);
    expect(details()).toEqual({
      from: 'me@example.com', subject: 'Away', start: ON.start, end: ON.end, repliesTo: 'every sender', bodyPreview: '<p>Back Monday</p>',
    });
    expect(callsTo('gmail', 'settings', 'vacation')).toHaveLength(1);
  });

  it.each([
    [{ contactsOnly: true }, 'your contacts'],
    [{ domainOnly: true }, 'senders in your domain'],
  ])('names the narrower audience for %j', async (scope, repliesTo) => {
    stub();
    const { harness, details } = await prompted({ action: 'decline' });
    expect(json(await harness.callTool('gog_gmail_vacation_update', { ...ON, ...scope })))
      .toMatchObject({ cancelled: true, action: 'gmail.vacation-enable' });
    expect(details().repliesTo).toBe(repliesTo);
    expect(callsTo('gmail', 'settings', 'vacation')).toHaveLength(0);
  });

  it('refuses a client that cannot be prompted', async () => {
    process.env.MCP_CONFIRM_MODE = 'refuse';
    const r = json(await (await unprompted()).callTool('gog_gmail_vacation_update', ON));
    expect(r).toMatchObject({ reason: 'confirmation-unsupported', action: 'gmail.vacation-enable' });
    expect(r.note).toMatch(/Gmail settings/);
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
  });

  it('token fallback: previews the full body, refuses a changed one', async () => {
    process.env.MCP_CONFIRM_MODE = 'ask-user';
    stub();
    const harness = await unprompted();
    const p1 = json(await harness.callTool('gog_gmail_vacation_update', ON));
    expect(p1.preview.body).toBe('<p>Back Monday</p>');
    expect(json(await harness.callTool('gog_gmail_vacation_update', { ...ON, body: 'x', confirmToken: p1.confirmToken })))
      .toMatchObject({ error: 'DRAFT_CHANGED' });
    await harness.callTool('gog_gmail_vacation_update', { ...ON, confirmToken: p1.confirmToken });
    expect(callsTo('gmail', 'settings', 'vacation')).toHaveLength(1);
  });
});

describe('gog_gmail_sendas_create', () => {
  const ARGS = { email: 'alias@example.com', displayName: 'Support', replyTo: 'help@example.com', signature: '<b>Support</b>' };

  it('asks with the address, name, reply-to and signature', async () => {
    stub();
    const { harness, details } = await prompted();
    await harness.callTool('gog_gmail_sendas_create', ARGS);
    expect(details()).toEqual({
      account: 'me@example.com', email: 'alias@example.com', displayName: 'Support', replyTo: 'help@example.com',
      treatAsAlias: false, signaturePreview: '<b>Support</b>',
    });
    expect(callsTo('gmail', 'settings', 'sendas', 'create')[0]![0]).toEqual([
      'gmail', 'settings', 'sendas', 'create', pos('alias@example.com'),
      '--display-name=Support', '--reply-to=help@example.com', '--signature=<b>Support</b>',
    ]);
  });

  it('creates nothing when the user declines', async () => {
    stub();
    const r = json(await (await prompted({ action: 'decline' })).harness.callTool('gog_gmail_sendas_create', { email: 'a@example.com' }));
    expect(r).toMatchObject({ cancelled: true, action: 'gmail.sendas-create' });
    expect(callsTo('gmail', 'settings', 'sendas', 'create')).toHaveLength(0);
  });

  it('refuses a client that cannot be prompted', async () => {
    process.env.MCP_CONFIRM_MODE = 'refuse';
    const r = json(await (await unprompted()).callTool('gog_gmail_sendas_create', ARGS));
    expect(r).toMatchObject({ reason: 'confirmation-unsupported', action: 'gmail.sendas-create' });
    expect(r.note).toMatch(/Send mail as/);
  });

  it('token fallback: a different address is refused, the same call creates', async () => {
    process.env.MCP_CONFIRM_MODE = 'ask-user';
    stub();
    const harness = await unprompted();
    const p1 = json(await harness.callTool('gog_gmail_sendas_create', ARGS));
    expect(p1.preview).toMatchObject({ email: 'alias@example.com', signature: '<b>Support</b>' });
    const other = json(await harness.callTool('gog_gmail_sendas_create', { ...ARGS, email: 'x@example.com', confirmToken: p1.confirmToken }));
    expect(other.error).toMatch(/DRAFT_CHANGED|TOKEN_INVALID/);
    await harness.callTool('gog_gmail_sendas_create', { ...ARGS, treatAsAlias: false, confirmToken: p1.confirmToken });
    expect(callsTo('gmail', 'settings', 'sendas', 'create')).toHaveLength(1);
  });
});
