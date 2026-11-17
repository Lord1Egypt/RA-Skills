import { describe, it, expect, vi, beforeEach } from 'vitest';
import { registerExtraGmailTools } from '../../src/tools/gmail-extra.js';
import * as lib from '../../../gogcli-mcp/src/lib.js';
import { createTestHarness, type TestHarness } from '@chrischall/mcp-utils/test';
import { rawTextResult, errorResult } from '@chrischall/mcp-utils';

vi.mock('../../../gogcli-mcp/src/lib.js', async (o) => ({ ...(await o<typeof lib>()), run: vi.fn(), runOrDiagnose: vi.fn(), diagnose: vi.fn() }));

let harness: TestHarness;
beforeEach(async () => {
  vi.clearAllMocks();
  vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult('{}'));
  vi.mocked(lib.diagnose).mockResolvedValue(errorResult('diagnosed'));
  harness = await createTestHarness(registerExtraGmailTools);
});

const b64 = (t: string) => Buffer.from(t, 'utf8').toString('base64url');
const draft = (id: string, body: string) => JSON.stringify({
  draft: {
    id,
    message: { id: `m${id}`, threadId: `t${id}`, payload: { mimeType: 'text/plain', headers: [{ name: 'Subject', value: 'S' }], body: { data: b64(body) } } },
  },
});

/**
 * #264: bodyLineCount counted RAW normalized lines while diffBodyLines compares
 * Set members, so onlyInACount + sharedLineCount === bodyLineCount stopped
 * holding the moment a body repeated a line. Dividers repeat constantly in real
 * mail, so this is the ordinary case, not an edge one.
 *
 * Asserted through the TOOL, against the emitted payload, because
 * describeDraftSide is module-private — and because the payload is what a
 * caller actually does arithmetic on.
 */
const A = ['Intro paragraph.', '---', 'Middle paragraph.', '---', 'Closing paragraph.'].join('\n');
const B = ['Intro paragraph.', '---', 'A different middle.', '---', 'Closing paragraph.'].join('\n');

describe('gog_gmail_drafts_diff count arithmetic', () => {
  it('onlyInACount + sharedLineCount === bodyLineCount when a body repeats a line', async () => {
    vi.mocked(lib.run).mockImplementation(async (args: readonly string[]) =>
      draft(String(args[3]), String(args[3]) === 'a1' ? A : B));

    const res = await harness.callTool('gog_gmail_drafts_diff', { draftIdA: 'a1', draftIdB: 'b1' });
    const raw = res.content.map((c: any) => c.text).join('\n');
    const payload = JSON.parse(raw);

    const sideA = payload.drafts.a;
    const diff = payload.bodyDiff;

    expect(sideA.bodyLineCount).toBeDefined();
    expect(diff.onlyInACount).toBeDefined();
    expect(diff.sharedLineCount).toBeDefined();
    // The body has 5 raw lines but only 4 distinct ones — that gap is the bug.
    expect(sideA.bodyLineCount).toBe(4);
    expect(diff.onlyInACount + diff.sharedLineCount).toBe(sideA.bodyLineCount);
  });
});
