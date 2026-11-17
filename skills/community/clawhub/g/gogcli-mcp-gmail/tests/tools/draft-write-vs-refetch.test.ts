import { describe, it, expect, vi, beforeEach } from 'vitest';
import { registerExtraGmailTools } from '../../src/tools/gmail-extra.js';
import * as lib from '../../../gogcli-mcp/src/lib.js';
import { createTestHarness, type TestHarness } from '@chrischall/mcp-utils/test';
import { rawTextResult, errorResult } from '@chrischall/mcp-utils';

vi.mock('../../../gogcli-mcp/src/lib.js', async (importOriginal) => {
  const actual = await importOriginal<typeof lib>();
  return { ...actual, run: vi.fn(), runOrDiagnose: vi.fn(), diagnose: vi.fn() };
});

let harness: TestHarness;
beforeEach(async () => {
  vi.clearAllMocks();
  vi.mocked(lib.run).mockResolvedValue('{}');
  vi.mocked(lib.diagnose).mockResolvedValue(errorResult('diagnosed'));
  harness = await createTestHarness(registerExtraGmailTools);
});

/**
 * #261: `returnFull` is a convenience READ performed after an acknowledged
 * write. When that read 404s — an Apple Mail fork between the write and the
 * read is exactly the case this file exists for — the write has still happened.
 *
 * The failed read used to REPLACE the successful write result, so every
 * downstream consumer read the write as failed: the fork diagnosis fired, and
 * the content-loss note told the caller "NOTHING WAS SAVED" about content that
 * had just been saved. For someone about to tidy up the sibling copy, that is
 * the most destructive thing this tool could say.
 */
describe('a failed returnFull re-read does not erase a successful write', () => {
  const ack = JSON.stringify({ draftId: 'r123', id: 'r123', message: { id: 'm1', threadId: 't1' } });

  it('reports the write as succeeded, and says which half failed', async () => {
    vi.mocked(lib.runOrDiagnose).mockImplementation(async (args: readonly string[]) =>
      args[2] === 'update' ? rawTextResult(ack) : errorResult('Google API error (404 notFound)'));

    const res = await harness.callTool('gog_gmail_drafts_update', { draftId: 'r123', subject: 'S', body: 'x', returnFull: true });
    const text = res.content.map((c: any) => c.text).join('\n');

    expect(res.isError).not.toBe(true);
    expect(text).toContain('SUCCEEDED');
    expect(text).toMatch(/read-back requested by returnFull could not be performed/i);
    expect(text).not.toMatch(/NOTHING WAS SAVED/);
  });

  it('still adopts the re-read when it works', async () => {
    const full = JSON.stringify({ id: 'r123', payload: { headers: [] } });
    vi.mocked(lib.runOrDiagnose).mockImplementation(async (args: readonly string[]) =>
      rawTextResult(args[2] === 'update' ? ack : full));

    const res = await harness.callTool('gog_gmail_drafts_update', { draftId: 'r123', subject: 'S', body: 'x', returnFull: true });
    expect(res.content.map((c: any) => c.text).join('\n')).toContain('payload');
  });

  it('does NOT retell a non-404 read failure as a fork, and keeps its text', async () => {
    // #264: any refetch failure used to get the fork explanation, discarding the
    // only text saying what actually went wrong. A permission error is not a fork.
    vi.mocked(lib.runOrDiagnose).mockImplementation(async (args: readonly string[]) =>
      args[2] === 'update' ? rawTextResult(ack) : errorResult('Google API error (403 forbidden): insufficient permission'));

    const res = await harness.callTool('gog_gmail_drafts_update', { draftId: 'r123', subject: 'S', body: 'x', returnFull: true });
    const text = res.content.map((c: any) => c.text).join('\n');

    expect(res.isError).not.toBe(true);
    expect(text).toContain('SUCCEEDED');
    expect(text).toContain('403 forbidden');            // the real cause survives
    expect(text).not.toMatch(/forked by a mail client/); // and is not retold as a fork
  });

  it('still gives the fork explanation on a genuine 404', async () => {
    vi.mocked(lib.runOrDiagnose).mockImplementation(async (args: readonly string[]) =>
      args[2] === 'update' ? rawTextResult(ack) : errorResult('Google API error (404 notFound)'));
    const res = await harness.callTool('gog_gmail_drafts_update', { draftId: 'r123', subject: 'S', body: 'x', returnFull: true });
    expect(res.content.map((c: any) => c.text).join('\n')).toMatch(/forked by a mail client/);
  });

  it('still says the write succeeded when the read failure carries no text', async () => {
    // An error result with no content at all: the note must not interpolate
    // `undefined` into the sentence a caller reads to decide what to do next.
    vi.mocked(lib.runOrDiagnose).mockImplementation(async (args: readonly string[]) =>
      args[2] === 'update' ? rawTextResult(ack) : ({ isError: true, content: [] } as any));

    const res = await harness.callTool('gog_gmail_drafts_update', { draftId: 'r123', subject: 'S', body: 'x', returnFull: true });
    const text = res.content.map((c: any) => c.text).join('\n');

    expect(res.isError).not.toBe(true);
    expect(text).toContain('SUCCEEDED');
    expect(text).toContain('(no detail supplied)');
    expect(text).not.toContain('undefined');
  });

  it('still reports a genuinely failed WRITE as an error', async () => {
    // The guard must not swallow a real failure: here the update itself fails.
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(errorResult('Google API error (404 notFound)'));
    const res = await harness.callTool('gog_gmail_drafts_update', { draftId: 'r123', subject: 'S', body: 'x', returnFull: true });
    expect(res.isError).toBe(true);
    expect(res.content.map((c: any) => c.text).join('\n')).not.toContain('SUCCEEDED');
  });
});

/**
 * #261: `enrich` built its `messages search in:drafts` without the caller's
 * `page` token, so enrich+page searched page 1 while the list was on page N —
 * an extra gog spawn that joined ZERO rows and still reported applied:true.
 */
describe('drafts_list enrich honours the caller page token', () => {
  it('passes page through to the enrichment search', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult(JSON.stringify({ drafts: [{ id: 'r1', messageId: 'm1' }] })));
    vi.mocked(lib.run).mockResolvedValue(JSON.stringify({ messages: [{ id: 'm1', subject: 'S' }] }));

    await harness.callTool('gog_gmail_drafts_list', { enrich: true, page: 'TOKEN123' });

    const search = vi.mocked(lib.run).mock.calls.map((c) => c[0] as string[]).find((a) => a[2] === 'search');
    expect(search).toBeDefined();
    expect(search).toContain('--page=TOKEN123');
  });
});
