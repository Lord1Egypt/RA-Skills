import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { registerExtraGmailTools, buildDraftCopy, draftRecipientFacts, COPY_TO_PREVIEW_CHARS, COPY_TO_QUOTE_SEPARATOR } from '../../src/tools/gmail-extra.js';
import * as lib from '../../../gogcli-mcp/src/lib.js';
import { resetConfirmTokenState } from '../../../gogcli-mcp/src/send-confirm-token.js';
import { createTestHarness, type TestHarness } from '@chrischall/mcp-utils/test';
import { rawTextResult, errorResult } from '@chrischall/mcp-utils';
import type { ElicitRequest, ElicitResult } from '@modelcontextprotocol/server';
import { pos, isGogPositional } from '../../../gogcli-mcp/src/argv.js';

// ============================================================================
// Decoded draft reads, review copies (gog_gmail_drafts_copy_to), patch-style
// draft edits, generated HTML parts, enriched listings and the
// MCP_CONFIRM_SKIP_TO allowlist — the workflow of reviewing drafts before
// they go out, without moving the body back and forth through the model.
// ============================================================================

vi.mock('../../../gogcli-mcp/src/lib.js', async (importOriginal) => {
  const actual = await importOriginal<typeof lib>();
  return { ...actual, run: vi.fn(), runOrDiagnose: vi.fn(), diagnose: vi.fn() };
});

const ORIGINAL_ENV = { ...process.env };
const b64url = (t: string) => Buffer.from(t, 'utf8').toString('base64url');
const plain = (args: unknown): unknown[] => (args as unknown[]).map((a) => (isGogPositional(a) ? a.value : a));
const text = (r: { content: Array<{ text?: string }> }) => r.content.map((c) => c.text ?? '').join('\n');

const HEADERS = [
  { name: 'From', value: 'Chris <chris@example.com>' },
  { name: 'To', value: 'Coordinator <pc@example.org>' },
  { name: 'Subject', value: 'Thanksgiving schedule' },
  { name: 'In-Reply-To', value: '<their@example.org>' },
];

const TAIL = 'UNIQUE-TAIL: the part past the preview, which the prompt must never echo.';
const LONG_BODY = `Hi,\n\n${'This paragraph explains the proposed holiday schedule in full detail. '.repeat(6)}\n\n${TAIL}\n\nThanks,\nChris`;

type Part = Record<string, unknown>;
const draftJson = (payload: Part, messageId = 'm1') => JSON.stringify({ draft: { id: 'd1', message: { id: messageId, threadId: 't1', payload } } });
const textOnly = (body = 'Plain body') => ({ mimeType: 'text/plain', headers: HEADERS, body: { data: b64url(body) } });
const htmlOnly = (html = '<p>Para one</p><p>Para <b>two</b></p>') => ({ mimeType: 'text/html', headers: HEADERS, body: { data: b64url(html) } });
const multipart = (body = LONG_BODY, html = `<div>${body}</div>`) => ({
  mimeType: 'multipart/mixed',
  headers: HEADERS,
  parts: [
    { mimeType: 'multipart/alternative', parts: [
      { mimeType: 'text/plain', body: { data: b64url(body) } },
      { mimeType: 'text/html', body: { data: b64url(html) } },
    ] },
    { mimeType: 'application/pdf', filename: 'calendar.pdf', body: { attachmentId: 'att1', size: 99 } },
  ],
});

let harness: TestHarness;
let elicit: ReturnType<typeof vi.fn<(r: ElicitRequest) => Promise<ElicitResult>>>;

beforeEach(async () => {
  vi.clearAllMocks();
  process.env = { ...ORIGINAL_ENV };
  delete process.env.MCP_CONFIRM_SKIP_TO;
  resetConfirmTokenState();
  vi.spyOn(process.stderr, 'write').mockImplementation(() => true);
  vi.mocked(lib.run).mockResolvedValue('{}');
  vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult('{"id":"sent1"}'));
  vi.mocked(lib.diagnose).mockResolvedValue(errorResult('diagnosed'));
  elicit = vi.fn(async () => ({ action: 'accept', content: { confirmed: true } }) as ElicitResult);
  harness = await createTestHarness(registerExtraGmailTools, { elicitation: (r) => elicit(r) });
});

afterEach(() => {
  process.env = ORIGINAL_ENV;
  vi.restoreAllMocks();
});

const runCalls = () => vi.mocked(lib.run).mock.calls.map(([args]) => plain(args));
const writes = () => vi.mocked(lib.runOrDiagnose).mock.calls.map(([args]) => plain(args));

// ---------------------------------------------------------------------------
describe('gog_gmail_drafts_get — decoded by default', () => {
  it('returns the decoded text of a text-only draft, with its headers, and no base64', async () => {
    vi.mocked(lib.run).mockResolvedValueOnce(draftJson(textOnly('Plain body')));
    const result = await harness.callTool('gog_gmail_drafts_get', { draftId: 'd1' });
    expect(vi.mocked(lib.run)).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'get', pos('d1'), '--use-indexed-attachment-ids=false'],
      { account: undefined, opaqueFields: ['data', 'attachmentId'] },
    );
    const view = JSON.parse(text(result));
    expect(view).toMatchObject({
      draftId: 'd1', id: 'm1', threadId: 't1', format: 'text', text: 'Plain body', textSource: 'text/plain', isReply: true,
      headers: { from: 'Chris <chris@example.com>', to: 'Coordinator <pc@example.org>', subject: 'Thanksgiving schedule', inReplyTo: '<their@example.org>' },
    });
    expect(text(result)).not.toContain(b64url('Plain body'));
  });

  it('converts an HTML-only draft to text', async () => {
    vi.mocked(lib.run).mockResolvedValueOnce(draftJson(htmlOnly()));
    const view = JSON.parse(text(await harness.callTool('gog_gmail_drafts_get', { draftId: 'd1' })));
    expect(view).toMatchObject({ text: 'Para one\n\nPara two', textSource: 'converted-from-html' });
  });

  it('reads the plain part of a multipart draft and lists its attachment; html and both on request', async () => {
    vi.mocked(lib.run).mockResolvedValue(draftJson(multipart('plain', '<p>rich</p>')));
    const view = JSON.parse(text(await harness.callTool('gog_gmail_drafts_get', { draftId: 'd1' })));
    expect(view.text).toBe('plain');
    expect(view.attachments).toEqual([{ filename: 'calendar.pdf', mimeType: 'application/pdf', size: 99, attachmentId: 'att1' }]);
    expect(JSON.parse(text(await harness.callTool('gog_gmail_drafts_get', { draftId: 'd1', format: 'html' })))).toMatchObject({ html: '<p>rich</p>' });
    expect(JSON.parse(text(await harness.callTool('gog_gmail_drafts_get', { draftId: 'd1', format: 'both' })))).toMatchObject({ text: 'plain', html: '<p>rich</p>' });
  });

  it('diagnoses a failed read, and passes unexpected output through', async () => {
    vi.mocked(lib.run).mockRejectedValueOnce(new Error('404'));
    const failed = await harness.callTool('gog_gmail_drafts_get', { draftId: 'd1' });
    expect(failed.isError).toBe(true);
    expect(text(failed)).toContain('404');
    vi.mocked(lib.run).mockResolvedValueOnce('{"draft":{}}');
    expect(text(await harness.callTool('gog_gmail_drafts_get', { draftId: 'd1' }))).toBe('{"draft":{}}');
  });
});

// ---------------------------------------------------------------------------
describe('gog_gmail_drafts_list — enrichment carries recipients and reply status', () => {
  it('returns to/cc/bcc, recipientCount, hasRecipients and isReply from the one batched search', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(JSON.stringify({ drafts: [
      { id: 'r1', messageId: 'm1', threadId: 't1' },
      { id: 'r2', messageId: 'm2', threadId: 'm2' },
    ] })));
    vi.mocked(lib.run).mockResolvedValueOnce(JSON.stringify({ messages: [
      { id: 'm1', subject: 'Re: x', to: 'pc@example.org', cc: 'a@x.com, b@x.com', headers: { 'In-Reply-To': '<p@x>' } },
      { id: 'm2', subject: 'unaddressed', headers: { 'In-Reply-To': '' } },
    ] }));
    const parsed = JSON.parse(text(await harness.callTool('gog_gmail_drafts_list', { enrich: true })));
    expect(runCalls()).toHaveLength(1);
    expect(runCalls()[0]).toEqual(expect.arrayContaining(['--include-recipients', '--headers=In-Reply-To']));
    expect(parsed.drafts[0]).toMatchObject({ to: 'pc@example.org', cc: 'a@x.com, b@x.com', recipientCount: 3, hasRecipients: true, isReply: true });
    expect(parsed.drafts[1]).toMatchObject({ recipientCount: 0, hasRecipients: false, isReply: false });
    expect(parsed.drafts[1]).not.toHaveProperty('to');
  });

  it('draftRecipientFacts reports a Bcc-only draft as addressed', () => {
    expect(draftRecipientFacts({ bcc: 'x@y.com' })).toEqual({ bcc: 'x@y.com', recipientCount: 1, hasRecipients: true, isReply: false });
  });
});

// ---------------------------------------------------------------------------
describe('gog_gmail_drafts_update — patch edits', () => {
  const STORED = 'Hi Pat,\n\nPickup is at 5pm on Friday.\n\nThanks,\nChris';

  it('applies replace/append/prepend to the STORED text, keeps the stored subject, and generates matching HTML', async () => {
    vi.mocked(lib.run).mockResolvedValueOnce(draftJson(textOnly(STORED)));
    await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1',
      replace: [{ old: 'at 5pm', new: 'at **6pm**' }],
      append: '- bring the car seat',
    });
    expect(runCalls()).toEqual([['gmail', 'drafts', 'get', 'd1', '--use-indexed-attachment-ids=false']]);
    const newBody = 'Hi Pat,\n\nPickup is at **6pm** on Friday.\n\nThanks,\nChris\n\n- bring the car seat';
    expect(writes()).toEqual([[
      'gmail', 'drafts', 'update', 'd1', '--subject=Thanksgiving schedule', `--body=${newBody}`,
      '--body-html=<p>Hi Pat,</p>\n<p>Pickup is at <strong>6pm</strong> on Friday.</p>\n<p>Thanks,<br>Chris</p>\n<ul><li>bring the car seat</li></ul>',
      '--auto-from-addressed-alias=false',
    ]]);
  });

  it('a stored draft with no Subject header is written with an empty subject', async () => {
    vi.mocked(lib.run).mockResolvedValueOnce(draftJson({ mimeType: 'text/plain', body: { data: b64url('x') } }));
    await harness.callTool('gog_gmail_drafts_update', { draftId: 'd1', append: 'y' });
    expect(writes()[0]).toEqual(expect.arrayContaining(['--subject=', '--body=x\n\ny']));
  });

  it('an explicit subject wins over the stored one', async () => {
    vi.mocked(lib.run).mockResolvedValueOnce(draftJson(textOnly(STORED)));
    await harness.callTool('gog_gmail_drafts_update', { draftId: 'd1', subject: 'New', prepend: 'Updated:' });
    expect(writes()[0]).toEqual(expect.arrayContaining(['--subject=New', `--body=Updated:\n\n${STORED}`]));
  });

  it.each([
    ['zero matches', [{ old: 'at 7pm', new: 'x' }], 'does not occur'],
    ['several matches', [{ old: '\n\n', new: ' ' }], 'occurs more than once'],
  ])('%s is an error that writes NOTHING and returns the current text', async (_n, replace, why) => {
    vi.mocked(lib.run).mockResolvedValueOnce(draftJson(textOnly(STORED)));
    const result = await harness.callTool('gog_gmail_drafts_update', { draftId: 'd1', replace });
    expect(result.isError).toBe(true);
    const body = JSON.parse(text(result).replace(/^Error: /, ''));
    expect(body).toMatchObject({ error: 'PATCH_NO_MATCH', draftId: 'd1', textSource: 'text/plain', currentText: STORED });
    expect(body.reason).toContain(why);
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
  });

  it('patches the converted text of an HTML-only draft', async () => {
    vi.mocked(lib.run).mockResolvedValueOnce(draftJson(htmlOnly()));
    await harness.callTool('gog_gmail_drafts_update', { draftId: 'd1', replace: [{ old: 'Para two', new: 'Para 2' }] });
    expect(writes()[0]).toEqual(expect.arrayContaining(['--body=Para one\n\nPara 2', '--body-html=<p>Para one</p>\n<p>Para 2</p>']));
  });

  it('refuses body together with a patch, and neither, before reading anything', async () => {
    const both = await harness.callTool('gog_gmail_drafts_update', { draftId: 'd1', body: 'x', append: 'y' });
    expect(both.isError).toBe(true);
    expect(text(both)).toContain('EITHER body');
    const neither = await harness.callTool('gog_gmail_drafts_update', { draftId: 'd1', subject: 'S' });
    expect(neither.isError).toBe(true);
    expect(text(neither)).toContain('body is required');
    expect(lib.run).not.toHaveBeenCalled();
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
  });

  it('a failed or unreadable read of the stored draft writes nothing', async () => {
    vi.mocked(lib.run).mockRejectedValueOnce(new Error('boom'));
    vi.mocked(lib.diagnose).mockResolvedValueOnce(errorResult('read failed'));
    const failed = await harness.callTool('gog_gmail_drafts_update', { draftId: 'd1', append: 'x' });
    expect(failed.isError).toBe(true);
    vi.mocked(lib.run).mockResolvedValueOnce('not json');
    const unreadable = await harness.callTool('gog_gmail_drafts_update', { draftId: 'd1', append: 'x' });
    expect(text(unreadable)).toContain('returned no `draft.message`');
    expect(writes().filter((a) => a.includes('update'))).toEqual([]);
  });
});

describe('gog_gmail_drafts_update / _create — generated HTML and bodyFormat', () => {
  it('whole-body mode with a subject reads nothing and renders the markdown HTML part', async () => {
    await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', bodyFormat: 'markdown',
      body: 'Hi,\n\n- **one**\n- two\n\n1. first\n\n> quoted *line*',
    });
    expect(lib.run).not.toHaveBeenCalled();
    expect(writes()[0]).toEqual([
      'gmail', 'drafts', 'update', 'd1', '--subject=S',
      '--body=Hi,\n\n- one\n- two\n\n1. first\n\n> quoted line',
      '--body-html=<p>Hi,</p>\n<ul><li><strong>one</strong></li><li>two</li></ul>\n<ol><li>first</li></ol>\n'
        + '<blockquote style="margin:0 0 0 .8ex;border-left:1px #ccc solid;padding-left:1ex"><p>quoted <em>line</em></p></blockquote>',
      '--auto-from-addressed-alias=false',
    ]);
  });

  it('keeps a caller-supplied bodyHtml, and htmlFromText false sends plain text only', async () => {
    await harness.callTool('gog_gmail_drafts_update', { draftId: 'd1', subject: 'S', body: 'B', bodyHtml: '<b>mine</b>' });
    await harness.callTool('gog_gmail_drafts_update', { draftId: 'd1', subject: 'S', body: 'B', htmlFromText: false });
    expect(writes()[0]).toContain('--body-html=<b>mine</b>');
    expect(writes()[1]!.some((a) => String(a).startsWith('--body-html'))).toBe(false);
  });

  it('create stays plain unless bodyFormat is markdown', async () => {
    await harness.callTool('gog_gmail_drafts_create', { subject: 'S', body: '**B**' });
    await harness.callTool('gog_gmail_drafts_create', { subject: 'S', body: '**B**', bodyFormat: 'markdown' });
    expect(writes()[0]).toEqual(['gmail', 'drafts', 'create', '--subject=S', '--body=**B**', '--auto-from-addressed-alias=false']);
    expect(writes()[1]).toEqual(['gmail', 'drafts', 'create', '--subject=S', '--body=B', '--body-html=<p><strong>B</strong></p>', '--auto-from-addressed-alias=false']);
  });
});

// ---------------------------------------------------------------------------
describe('gog_gmail_drafts_copy_to', () => {
  const sends = () => writes().filter((a) => a[1] === 'send');
  // An accepted prompt RE-RUNS the handler (the protocol retry), so each read
  // is stubbed by its argv rather than by call order.
  const reads = (draft: string, quoted?: string | Error) => vi.mocked(lib.run).mockImplementation(async (args) => {
    if (plain(args)[1] === 'drafts') return draft;
    if (quoted instanceof Error) throw quoted;
    return quoted ?? '{}';
  });

  it('sends the stored subject and both body parts to the named address, and never writes the draft', async () => {
    reads(draftJson(multipart()));
    const result = await harness.callTool('gog_gmail_drafts_copy_to', { draftId: 'd1', to: 'wife@example.com' });
    expect(result.isError).toBeFalsy();
    expect(sends()).toEqual([[
      'gmail', 'send', '--to=wife@example.com', '--subject=DRAFT: Thanksgiving schedule', `--body=${LONG_BODY}`, `--body-html=<div>${LONG_BODY}</div>`,
    ]]);
    // Nothing of the draft's own addressing, threading or attachments rides along.
    expect(sends()[0]!.join(' ')).not.toMatch(/pc@example\.org|--thread-id|--reply-to-message-id|--attach/);
    expect(writes().filter((a) => a[1] === 'drafts')).toEqual([]);
  });

  it('the confirmation shows recipients, subject, the first 300 characters, length and hash — NOT the whole body', async () => {
    reads(draftJson(multipart()));
    await harness.callTool('gog_gmail_drafts_copy_to', { draftId: 'd1', to: 'wife@example.com', cc: 'me@example.com', bcc: 'x@example.com', subjectPrefix: 'REVIEW: ' });
    expect(elicit).toHaveBeenCalledTimes(1);
    const prompt = JSON.stringify(elicit.mock.calls[0]![0]);
    expect(LONG_BODY.indexOf(TAIL)).toBeGreaterThan(COPY_TO_PREVIEW_CHARS);
    expect(prompt).not.toContain('UNIQUE-TAIL');
    expect(prompt).toContain(LONG_BODY.slice(5, 60)); // past the newlines, which the prompt escapes
    expect(prompt).toContain('REVIEW: Thanksgiving schedule');
    expect(prompt).toContain(String(LONG_BODY.length));
    expect(prompt).toMatch(/[0-9a-f]{64}/);
    expect(sends()[0]).toEqual(expect.arrayContaining(['--cc=me@example.com', '--bcc=x@example.com']));
  });

  it('a failed send is returned as-is and not logged as a dispatch', async () => {
    process.env.MCP_CONFIRM_SKIP_TO = 'wife@example.com';
    reads(draftJson(textOnly()));
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(errorResult('send failed'));
    const result = await harness.callTool('gog_gmail_drafts_copy_to', { draftId: 'd1', to: 'wife@example.com' });
    expect(result.isError).toBe(true);
    expect(text(result)).not.toContain('WITHOUT a confirmation prompt');
    const logged = vi.mocked(process.stderr.write).mock.calls.map(([line]) => String(line));
    expect(logged.some((l) => l.includes('gmail_dispatch'))).toBe(false);
  });

  it('a declined prompt sends nothing', async () => {
    elicit.mockResolvedValueOnce({ action: 'decline' });
    reads(draftJson(textOnly()));
    await harness.callTool('gog_gmail_drafts_copy_to', { draftId: 'd1', to: 'wife@example.com' });
    expect(sends()).toEqual([]);
  });

  it('appends a note and the quoted message below the body; a plain-only draft stays plain', async () => {
    reads(draftJson(textOnly('My reply')), JSON.stringify({ message: { id: 'q1', payload: {
      mimeType: 'text/plain',
      headers: [{ name: 'From', value: 'Co-parent <cp@example.com>' }, { name: 'Date', value: 'Fri, 7 Nov 2026' }],
      body: { data: b64url('Their message') },
    } } }));
    await harness.callTool('gog_gmail_drafts_copy_to', { draftId: 'd1', to: 'wife@example.com', appendText: 'Thoughts?', includeQuotedFrom: 'q1' });
    expect(runCalls()[1]).toEqual(['gmail', 'get', 'q1', '--format=full']);
    expect(sends()[0]).toEqual([
      'gmail', 'send', '--to=wife@example.com', '--subject=DRAFT: Thanksgiving schedule',
      `--body=My reply\n\nThoughts?\n\n${COPY_TO_QUOTE_SEPARATOR}\nFrom: Co-parent <cp@example.com>\nDate: Fri, 7 Nov 2026\n\nTheir message`,
    ]);
  });

  it('reports a quoted message it cannot read, and a draft with no body, without sending', async () => {
    reads(draftJson(textOnly()), new Error('404'));
    expect(text(await harness.callTool('gog_gmail_drafts_copy_to', { draftId: 'd1', to: 'a@b.com', includeQuotedFrom: 'q1' }))).toBe('diagnosed');
    reads(draftJson(textOnly()), '{}');
    expect(text(await harness.callTool('gog_gmail_drafts_copy_to', { draftId: 'd1', to: 'a@b.com', includeQuotedFrom: 'q1' }))).toContain('Could not read message q1');
    reads(draftJson({ mimeType: 'multipart/mixed', headers: HEADERS }));
    expect(text(await harness.callTool('gog_gmail_drafts_copy_to', { draftId: 'd1', to: 'a@b.com' }))).toContain('has no body to copy');
    vi.mocked(lib.run).mockReset().mockRejectedValue(new Error('gone'));
    vi.mocked(lib.diagnose).mockResolvedValueOnce(errorResult('read failed'));
    expect((await harness.callTool('gog_gmail_drafts_copy_to', { draftId: 'd1', to: 'a@b.com' })).isError).toBe(true);
    expect(sends()).toEqual([]);
  });

  it('buildDraftCopy appends to the HTML part too, with an empty prefix and a subject-less draft', () => {
    const copy = buildDraftCopy(
      { payload: { mimeType: 'text/html', body: { data: b64url('<p>x</p>') } } },
      { subjectPrefix: '', appendText: '**note**', quoted: { payload: { mimeType: 'text/plain', headers: [{ name: 'Subject', value: 'Q & A' }], body: { data: b64url('a <b>\nc') } } } },
    );
    expect(copy.subject).toBe('');
    expect(copy.text).toBe(`x\n\n**note**\n\n${COPY_TO_QUOTE_SEPARATOR}\nSubject: Q & A\n\na <b>\nc`);
    expect(copy.html).toBe(`<p>x</p>\n<p><strong>note</strong></p>\n<hr><p>${COPY_TO_QUOTE_SEPARATOR}<br>Subject: Q &amp; A</p>`
      + '<blockquote style="margin:0 0 0 .8ex;border-left:1px #ccc solid;padding-left:1ex">a &lt;b&gt;<br>c</blockquote>');
    expect(buildDraftCopy({ payload: { mimeType: 'multipart/mixed' } }, { subjectPrefix: 'D: ', appendText: 'only' }))
      .toEqual({ subject: 'D: ', text: 'only' });
  });
});

// ---------------------------------------------------------------------------
describe('MCP_CONFIRM_SKIP_TO on the drafts dispatches', () => {
  it('copy_to to allowlisted addresses only: sent with no prompt, and the result says so', async () => {
    process.env.MCP_CONFIRM_SKIP_TO = 'wife@example.com,chris@example.com';
    vi.mocked(lib.run).mockResolvedValue(draftJson(textOnly()));
    const result = await harness.callTool('gog_gmail_drafts_copy_to', { draftId: 'd1', to: 'wife@example.com', cc: 'chris@example.com' });
    expect(elicit).not.toHaveBeenCalled();
    expect(writes().filter((a) => a[1] === 'send')).toHaveLength(1);
    expect(text(result)).toContain('WITHOUT a confirmation prompt');
  });

  it('copy_to with one address off the list still asks', async () => {
    process.env.MCP_CONFIRM_SKIP_TO = 'wife@example.com';
    vi.mocked(lib.run).mockResolvedValue(draftJson(textOnly()));
    const result = await harness.callTool('gog_gmail_drafts_copy_to', { draftId: 'd1', to: 'wife@example.com', bcc: 'pc@example.org' });
    expect(elicit).toHaveBeenCalledTimes(1);
    expect(text(result)).not.toContain('WITHOUT a confirmation prompt');
  });

  it('drafts_send skips only when the STORED draft\'s recipients are all allowlisted', async () => {
    process.env.MCP_CONFIRM_SKIP_TO = 'pc@example.org';
    vi.mocked(lib.runOrDiagnose).mockImplementation(async (args) =>
      rawTextResult(plain(args).includes('get') ? draftJson(textOnly()) : '{"id":"sent"}'));
    const skipped = await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1' });
    expect(elicit).not.toHaveBeenCalled();
    expect(text(skipped)).toContain('WITHOUT a confirmation prompt');

    process.env.MCP_CONFIRM_SKIP_TO = 'someone-else@example.org';
    const asked = await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1' });
    expect(elicit).toHaveBeenCalledTimes(1);
    expect(text(asked)).not.toContain('WITHOUT a confirmation prompt');
  });
});

// ---------------------------------------------------------------------------
describe('gog_gmail_drafts_copy_to — token fallback (no elicitation)', () => {
  it('phase 1 previews the summary only; phase 2 with the token sends', async () => {
    process.env.MCP_CONFIRM_MODE = 'ask-user';
    process.env.GOG_ACCOUNT = 'chris@example.com';
    const noPrompt = await createTestHarness(registerExtraGmailTools);
    vi.mocked(lib.run).mockResolvedValue(draftJson(multipart()));
    const phase1 = await noPrompt.callTool('gog_gmail_drafts_copy_to', { draftId: 'd1', to: 'wife@example.com' });
    const body = JSON.parse(text(phase1));
    expect(body.status).toBe('confirmation-required');
    expect(text(phase1)).not.toContain('UNIQUE-TAIL');
    expect(writes().filter((a) => a[1] === 'send')).toEqual([]);
    await noPrompt.callTool('gog_gmail_drafts_copy_to', { draftId: 'd1', to: 'wife@example.com', confirmToken: body.confirmToken });
    expect(writes().filter((a) => a[1] === 'send')).toHaveLength(1);
  });
});
