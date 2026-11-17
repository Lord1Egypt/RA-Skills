import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { registerExtraGmailTools, parseForwardMetadata, storedDraftTokenSubject } from '../../src/tools/gmail-extra.js';
import * as lib from '../../../gogcli-mcp/src/lib.js';
import { resetConfirmTokenState } from '../../../gogcli-mcp/src/send-confirm-token.js';
import { createTestHarness, type TestHarness } from '@chrischall/mcp-utils/test';
import { rawTextResult, errorResult } from '@chrischall/mcp-utils';
import { pos } from '../../../gogcli-mcp/src/argv.js';

vi.mock('../../../gogcli-mcp/src/lib.js', async (importOriginal) => {
  const actual = await importOriginal<typeof lib>();
  return { ...actual, run: vi.fn(), runOrDiagnose: vi.fn(), diagnose: vi.fn() };
});

// ============================================================================
// The confirmToken fallback on the gmail sub-package's dispatch tools. The
// harness registers no elicitation handler: a client that cannot be prompted.
// ============================================================================

const ORIGINAL_ENV = { ...process.env };
let harness: TestHarness;

beforeEach(async () => {
  vi.clearAllMocks();
  process.env = { ...ORIGINAL_ENV };
  process.env.MCP_CONFIRM_MODE = 'ask-user';
  process.env.GOG_ACCOUNT = 'me@example.com';
  delete process.env.MCP_CONFIRM_TTL_SECONDS;
  delete process.env.MCP_CONFIRM_SECRET;
  resetConfirmTokenState();
  vi.mocked(lib.diagnose).mockResolvedValue(errorResult('diagnosed'));
  vi.spyOn(process.stderr, 'write').mockImplementation(() => true);
  harness = await createTestHarness(registerExtraGmailTools);
});

afterEach(() => {
  process.env = ORIGINAL_ENV;
  vi.restoreAllMocks();
  vi.useRealTimers();
});

const json = (r: { content: Array<{ text?: string }> }) => JSON.parse(r.content[0]!.text as string);
const calls = (sub: string) => vi.mocked(lib.runOrDiagnose).mock.calls.filter(([args]) => (args as unknown[]).includes(sub));

describe('gog_gmail_drafts_send — token fallback', () => {
  const b64url = (t: string) => Buffer.from(t, 'utf8').toString('base64url');
  const draft = ({ messageId = 'm1', body = 'Please find the export attached.' } = {}) => JSON.stringify({
    draft: {
      id: 'd1',
      message: {
        id: messageId,
        threadId: 't1',
        payload: {
          mimeType: 'multipart/mixed',
          headers: [
            { name: 'From', value: 'Me <me@example.com>' },
            { name: 'To', value: 'Alice <alice@example.com>' },
            { name: 'Cc', value: 'carol@example.com' },
            { name: 'Bcc', value: 'hidden@example.com' },
            { name: 'Subject', value: 'Re: Quarterly numbers' },
            { name: 'In-Reply-To', value: '<orig@mail.example.com>' },
            { name: 'References', value: '<orig@mail.example.com>' },
          ],
          parts: [
            {
              mimeType: 'multipart/alternative',
              parts: [
                { mimeType: 'text/plain', body: { data: b64url(body) } },
                { mimeType: 'text/html', body: { data: b64url(`<p>${body}</p>`) } },
              ],
            },
            { mimeType: 'application/json', filename: 't.json', body: { attachmentId: 'a1', size: 1234 } },
          ],
        },
      },
    },
  });

  const stub = (...responses: string[]) => {
    const m = vi.mocked(lib.runOrDiagnose);
    for (const r of responses) m.mockResolvedValueOnce(rawTextResult(r));
  };

  it('unsupported + MCP_CONFIRM_MODE=refuse: keeps the refusal, naming the switch', async () => {

    process.env.MCP_CONFIRM_MODE = 'refuse';
    stub(draft());
    const body = json(await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1' }));
    expect(body.reason).toBe('confirmation-unsupported');
    expect(body.note).toContain('MCP_CONFIRM_MODE=ask-user');
    expect(calls('send')).toHaveLength(0);
  });

  it('phase 1 previews the whole stored draft — Bcc, full body, sizes, ids — and sends nothing', async () => {
    stub(draft());
    const body = json(await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1' }));
    expect(body.status).toBe('confirmation-required');
    expect(body.preview).toEqual({
      draftId: 'd1',
      messageId: 'm1',
      threadId: 't1',
      from: 'Me <me@example.com>',
      to: 'Alice <alice@example.com>',
      cc: 'carol@example.com',
      bcc: 'hidden@example.com',
      subject: 'Re: Quarterly numbers',
      body: 'Please find the export attached.',
      attachments: [{ name: 't.json', size: 1234 }],
      inReplyTo: '<orig@mail.example.com>',
      references: '<orig@mail.example.com>',
    });
    expect(calls('send')).toHaveLength(0);
  });

  it('phase 2 re-reads the draft and sends it with a valid token', async () => {
    stub(draft());
    const { confirmToken } = json(await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1' }));
    stub(draft(), '{"id":"sent"}');
    const result = await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1', confirmToken });
    expect(result.isError).toBeFalsy();
    expect(lib.runOrDiagnose).toHaveBeenLastCalledWith(['gmail', 'drafts', 'send', pos('d1')], { account: undefined });
    expect(calls('send')).toHaveLength(1);
  });

  // Apple Mail re-saves a draft as a new message on every save: same draftId,
  // new messageId. What the user approved is no longer what would go out.
  it('draft re-saved between phases (messageId rotated): DRAFT_CHANGED, nothing sent', async () => {
    stub(draft());
    const { confirmToken } = json(await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1' }));
    stub(draft({ messageId: 'm2', body: 'Please find the export attached. P.S. one more thing' }));
    const result = await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1', confirmToken });
    expect(result.isError).toBe(true);
    const body = json(result);
    expect(body).toMatchObject({ error: 'DRAFT_CHANGED', reason: 'revision-changed', dispatched: false });
    expect(body.preview).toMatchObject({ messageId: 'm2', body: 'Please find the export attached. P.S. one more thing' });
    expect(body.confirmToken).toMatch(/^mcpu\.token\.v1\./);
    expect(calls('send')).toHaveLength(0);

    // The fresh token re-approves the new content.
    stub(draft({ messageId: 'm2', body: 'Please find the export attached. P.S. one more thing' }), '{"id":"sent"}');
    await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1', confirmToken: body.confirmToken });
    expect(calls('send')).toHaveLength(1);
  });

  it('body edited under the same messageId: DRAFT_CHANGED (payload-changed)', async () => {
    stub(draft());
    const { confirmToken } = json(await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1' }));
    stub(draft({ body: 'Different text' }));
    expect(json(await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1', confirmToken })))
      .toMatchObject({ error: 'DRAFT_CHANGED', reason: 'payload-changed' });
    expect(calls('send')).toHaveLength(0);
  });

  it('rejects a token issued for a different draft', async () => {
    stub(draft());
    const { confirmToken } = json(await harness.callTool('gog_gmail_drafts_send', { draftId: 'd-other' }));
    stub(draft());
    expect(json(await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1', confirmToken }))).toMatchObject({ error: 'TOKEN_INVALID' });
    expect(calls('send')).toHaveLength(0);
  });

  it('rejects reused, expired and tampered tokens', async () => {
    vi.useFakeTimers({ toFake: ['Date'] });
    vi.setSystemTime(new Date('2026-09-24T10:00:00Z'));
    stub(draft());
    const { confirmToken } = json(await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1' }));
    stub(draft());
    expect(json(await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1', confirmToken: confirmToken.replace(/.$/, '!') })))
      .toMatchObject({ error: 'TOKEN_INVALID' });
    stub(draft(), '{"id":"sent"}');
    await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1', confirmToken });
    stub(draft());
    expect(json(await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1', confirmToken }))).toMatchObject({ error: 'TOKEN_REUSED' });

    stub(draft());
    const second = json(await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1' })).confirmToken;
    vi.setSystemTime(new Date('2026-09-24T10:10:01Z'));
    stub(draft());
    expect(json(await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1', confirmToken: second }))).toMatchObject({ error: 'TOKEN_EXPIRED' });
    expect(calls('send')).toHaveLength(1);
  });

  it('a draft that no longer resolves still takes the fork-aware path', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(errorResult('Error: notFound'));
    const result = await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1', confirmToken: 'not-a-real-token' });
    expect(result.isError).toBe(true);
    expect(calls('send')).toHaveLength(0);
  });
});

describe('storedDraftTokenSubject', () => {
  it('degrades on unreadable output to an empty preview that still names the draft', () => {
    const s = storedDraftTokenSubject('not json', 'd9', undefined);
    expect(s).toMatchObject({ target: 'd9', revision: undefined, preview: { draftId: 'd9', from: 'me@example.com', body: '', attachments: [] } });
  });

  it('shows an HTML-only draft\'s HTML as its body, and an unsized attachment as null', () => {
    const raw = JSON.stringify({ draft: { message: { id: 'm', payload: { mimeType: 'multipart/mixed', parts: [
      { mimeType: 'text/html', body: { data: Buffer.from('<b>hi</b>').toString('base64url') } },
      { filename: 'x.bin', body: {} },
    ] } } } });
    expect(storedDraftTokenSubject(raw, 'd', 'a@example.com').preview).toMatchObject({ body: '<b>hi</b>', attachments: [{ name: 'x.bin', size: null }] });
  });
});

describe('gog_gmail_forward — token fallback', () => {
  const META = JSON.stringify({
    message: { id: 'm1', threadId: 't1' },
    headers: { from: 'Bob <bob@example.com>', subject: 'Invoice', date: 'Mon, 1 Sep 2026', message_id: '<inv@example.com>' },
    attachments: [{ filename: 'invoice.pdf', size: 2048 }],
  });
  const ARGS = { messageId: 'm1', to: 'accounts@example.com', bcc: 'me-too@example.com', note: 'FYI — see attached.' };

  it('phase 1 reads the forwarded message and previews it; nothing sent', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult(META));
    const body = json(await harness.callTool('gog_gmail_forward', ARGS));
    expect(body.status).toBe('confirmation-required');
    expect(body.preview).toEqual({
      from: 'me@example.com',
      to: 'accounts@example.com',
      bcc: 'me-too@example.com',
      subject: 'Fwd: Invoice',
      body: 'FYI — see attached.',
      forwarding: { messageId: 'm1', from: 'Bob <bob@example.com>', subject: 'Invoice', date: 'Mon, 1 Sep 2026', messageIdHeader: '<inv@example.com>' },
      attachments: [{ name: 'invoice.pdf', size: 2048 }],
      threadId: 't1',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['gmail', 'get', pos('m1'), '--format=metadata'], { account: undefined });
    expect(calls('forward')).toHaveLength(0);
  });

  it('phase 2 with a valid token forwards; skipAttachments empties the attachment list', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult(META));
    const first = json(await harness.callTool('gog_gmail_forward', { ...ARGS, skipAttachments: true, from: 'alias@example.com' }));
    expect(first.preview).toMatchObject({ attachments: [], from: 'alias@example.com' });
    await harness.callTool('gog_gmail_forward', { ...ARGS, skipAttachments: true, from: 'alias@example.com', confirmToken: first.confirmToken });
    expect(calls('forward')).toHaveLength(1);
    expect(calls('forward')[0]![0]).toContain('--bcc=me-too@example.com');
  });

  it('a changed note on phase 2 is DRAFT_CHANGED', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult(META));
    const { confirmToken } = json(await harness.callTool('gog_gmail_forward', ARGS));
    expect(json(await harness.callTool('gog_gmail_forward', { ...ARGS, note: 'changed', confirmToken }))).toMatchObject({ error: 'DRAFT_CHANGED' });
    expect(calls('forward')).toHaveLength(0);
  });

  it('previews an HTML note and binds it: changing it on phase 2 is DRAFT_CHANGED', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult(META));
    const first = json(await harness.callTool('gog_gmail_forward', { ...ARGS, noteHtml: '<b>FYI</b>' }));
    expect(first.preview).toMatchObject({ body: 'FYI — see attached.', noteHtml: '<b>FYI</b>' });
    expect(json(await harness.callTool('gog_gmail_forward', { ...ARGS, noteHtml: '<b>changed</b>', confirmToken: first.confirmToken }))).toMatchObject({ error: 'DRAFT_CHANGED' });
    expect(calls('forward')).toHaveLength(0);
  });

  it('previews the signature and binds it: adding one on phase 2 is DRAFT_CHANGED', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult(META));
    const first = json(await harness.callTool('gog_gmail_forward', { ...ARGS, signatureFrom: 'alias@example.com' }));
    expect(first.preview.signature).toBe('alias@example.com');
    const body = json(await harness.callTool('gog_gmail_forward', { ...ARGS, signatureFrom: 'alias@example.com', signature: true, confirmToken: first.confirmToken }));
    expect(body).toMatchObject({ error: 'DRAFT_CHANGED' });
    expect(calls('forward')).toHaveLength(0);
  });

  it('binds a signatureFile by content: an edited file is DRAFT_CHANGED', async () => {
    const root = mkdtempSync(join(tmpdir(), 'fwd-sig-'));
    const prev = process.env.GOG_FILE_ROOTS;
    process.env.GOG_FILE_ROOTS = root;
    try {
      const path = join(root, 'sig.txt');
      writeFileSync(path, 'v1');
      vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult(META));
      const first = json(await harness.callTool('gog_gmail_forward', { ...ARGS, signatureFile: path }));
      expect(first.preview.signature).toBe(path);
      writeFileSync(path, 'v2');
      const body = json(await harness.callTool('gog_gmail_forward', { ...ARGS, signatureFile: path, confirmToken: first.confirmToken }));
      expect(body).toMatchObject({ error: 'DRAFT_CHANGED' });
      expect(calls('forward')).toHaveLength(0);
    } finally {
      process.env.GOG_FILE_ROOTS = prev;
    }
  });

  it('a failed read of the original is returned as-is and nothing is sent', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(errorResult('Error: notFound'));
    const result = await harness.callTool('gog_gmail_forward', ARGS);
    expect(result.isError).toBe(true);
    expect(calls('forward')).toHaveLength(0);
  });

  it('a read with no text block previews an unknown original rather than failing', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue({ content: [] });
    const body = json(await harness.callTool('gog_gmail_forward', ARGS));
    expect(body.preview).toMatchObject({ attachments: [], forwarding: { messageId: 'm1' } });
    expect(body.preview).not.toHaveProperty('subject');
  });

  it('parseForwardMetadata tolerates unreadable and partial output', () => {
    expect(parseForwardMetadata('nope')).toEqual({ attachments: [] });
    expect(parseForwardMetadata('{"headers":{"from":5},"attachments":[{}]}')).toMatchObject({ from: undefined, attachments: [{ name: '', size: null }] });
  });
});

describe('gog_gmail_autoreply — token fallback', () => {
  const SEARCH = (ids = ['th1', 'th2']) => JSON.stringify({
    threads: ids.map((id, i) => ({ id, from: `Sender ${i} <s${i}@example.com>`, subject: `Topic ${i}` })),
  });
  const ARGS = { query: 'label:inbox is:unread', body: 'Out until Monday.' };

  it('phase 1 previews the matched set and full body; nothing sent', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult(SEARCH()));
    const body = json(await harness.callTool('gog_gmail_autoreply', { ...ARGS, replyTo: 'desk@example.com' }));
    expect(body.status).toBe('confirmation-required');
    expect(body.preview).toMatchObject({
      from: 'me@example.com',
      to: ['s0@example.com', 's1@example.com'],
      subject: 'Re: <each original subject>',
      body: 'Out until Monday.',
      replyTo: 'desk@example.com',
      matchCount: 2,
      matches: [{ id: 'th1', from: 'Sender 0 <s0@example.com>', subject: 'Topic 0' }, { id: 'th2', from: 'Sender 1 <s1@example.com>', subject: 'Topic 1' }],
      label: 'AutoReplied',
    });
    expect(calls('autoreply')).toHaveLength(0);
  });

  it('phase 2 with a valid token sends', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult(SEARCH()));
    const { confirmToken } = json(await harness.callTool('gog_gmail_autoreply', ARGS));
    await harness.callTool('gog_gmail_autoreply', { ...ARGS, confirmToken });
    expect(calls('autoreply')).toHaveLength(1);
  });

  it('a different matched set on phase 2 is DRAFT_CHANGED', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult(SEARCH()));
    const { confirmToken } = json(await harness.callTool('gog_gmail_autoreply', ARGS));
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult(SEARCH(['th1', 'th2', 'th3'])));
    expect(json(await harness.callTool('gog_gmail_autoreply', { ...ARGS, confirmToken }))).toMatchObject({ error: 'DRAFT_CHANGED' });
    expect(calls('autoreply')).toHaveLength(0);
  });

  it('a search with no threads array, or no text block, matches nothing', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult('{}'));
    expect(json(await harness.callTool('gog_gmail_autoreply', ARGS)).preview.matches).toEqual([]);
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce({ content: [] });
    expect(json(await harness.callTool('gog_gmail_autoreply', ARGS)).preview.matches).toEqual([]);
  });

  it('an explicit subject and an HTML body are what the preview shows; unreadable search output matches nothing', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult('not json'));
    const body = json(await harness.callTool('gog_gmail_autoreply', { query: 'x', subject: 'Away', bodyHtml: '<p>Away</p>' }));
    expect(body.preview).toMatchObject({ subject: 'Away', body: '<p>Away</p>', matchCount: 0, matches: [] });
  });
});
