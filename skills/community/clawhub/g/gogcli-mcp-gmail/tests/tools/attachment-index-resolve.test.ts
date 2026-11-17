import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createTestHarness, type TestHarness } from '@chrischall/mcp-utils/test';

vi.mock('../../../gogcli-mcp/src/lib.js', async (orig) => {
  const actual = await orig<Record<string, unknown>>();
  return { ...actual, run: vi.fn() };
});
const { run } = await import('../../../gogcli-mcp/src/lib.js');
const { registerExtraGmailTools } = await import('../../src/tools/gmail-extra.js');

/**
 * #252: resolveByIndex took `attachments[index]` — array POSITION — while
 * resolveBySize matches on a declared field. gog assigns AttachmentIndex = i
 * today, so position happens to agree; the moment it does not (a filtered or
 * reordered listing) the download is silently named after the WRONG part, which
 * is worse than failing.
 *
 * The declared `attachmentIndex` is the contract. Match it.
 */
describe('resolveByIndex matches the declared attachmentIndex', () => {
  let h: TestHarness;
  beforeEach(async () => { vi.clearAllMocks(); h = await createTestHarness(registerExtraGmailTools); });

  it('picks the part whose attachmentIndex equals the request, not its array slot', async () => {
    (run as any).mockImplementation(async (args: string[]) => {
      if (args[1] === 'get') {
        // Declared indexes deliberately NOT in array order.
        return JSON.stringify({ attachments: [
          { filename: 'second.pdf', attachmentIndex: 1, size: 100, mimeType: 'application/pdf' },
          { filename: 'first.pdf',  attachmentIndex: 0, size: 200, mimeType: 'application/pdf' },
        ] });
      }
      return JSON.stringify({ path: '/tmp/x', size: 200 });
    });
    await h.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentIndex: 0 });
    const dl = (run as any).mock.calls.map((c: any[]) => c[0]).find((a: string[]) => a[1] === 'attachment');
    // index 0 is declared by the SECOND array element (first.pdf)
    expect(dl.join(' ')).toContain('first.pdf');
    expect(dl.join(' ')).not.toContain('second.pdf');
  });

  it('still resolves when gog omits attachmentIndex, by position', async () => {
    (run as any).mockImplementation(async (args: string[]) => {
      if (args[1] === 'get') {
        return JSON.stringify({ attachments: [
          { filename: 'a.pdf', size: 100, mimeType: 'application/pdf' },
          { filename: 'b.pdf', size: 200, mimeType: 'application/pdf' },
        ] });
      }
      return JSON.stringify({ path: '/tmp/x', size: 200 });
    });
    await h.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentIndex: 1 });
    const dl = (run as any).mock.calls.map((c: any[]) => c[0]).find((a: string[]) => a[1] === 'attachment');
    expect(dl.join(' ')).toContain('b.pdf');
  });

  it('refuses to guess when indexes are declared but none matches', async () => {
    // The caller asked for an index this message does not have. Falling back to
    // position here would hand back a real-but-wrong attachment, which is the
    // silent mis-naming this resolver exists to prevent — so it resolves to
    // nothing and the download keeps its provisional name instead.
    (run as any).mockImplementation(async (args: string[]) => {
      if (args[1] === 'get') {
        return JSON.stringify({ attachments: [
          { filename: 'a.pdf', attachmentIndex: 0, size: 100, mimeType: 'application/pdf' },
          { filename: 'b.pdf', attachmentIndex: 1, size: 200, mimeType: 'application/pdf' },
        ] });
      }
      return JSON.stringify({ path: '/tmp/x', size: 200 });
    });
    await h.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentIndex: 7 });
    const dl = (run as any).mock.calls.map((c: any[]) => c[0]).find((a: string[]) => a[1] === 'attachment');
    expect(dl.join(' ')).not.toContain('a.pdf');
    expect(dl.join(' ')).not.toContain('b.pdf');
  });
});
