import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { registerExtraGmailTools } from '../../src/tools/gmail-extra.js';
import * as lib from '../../../gogcli-mcp/src/lib.js';
import * as runner from '../../../gogcli-mcp/src/runner.js';
import { createTestHarness, type TestHarness } from '@chrischall/mcp-utils/test';
import { rawTextResult, errorResult } from '@chrischall/mcp-utils';
import type { ElicitRequest, ElicitResult } from '@modelcontextprotocol/server';
import { pos, isGogPositional } from '../../../gogcli-mcp/src/argv.js';

// The argv as gog would read it, positional markers unwrapped — for stubs that
// dispatch on an ID. Assertions about marking use pos() directly instead.
// The per-user private download root (was a shared /tmp/gog-attachments).
const ROOT = lib.ATTACHMENT_DOWNLOAD_ROOT;

const plain = (args: unknown): string[] =>
  (args as unknown[]).map((a) => (isGogPositional(a) ? a.value : a)) as string[];

vi.mock('../../../gogcli-mcp/src/lib.js', async (importOriginal) => {
  const actual = await importOriginal<typeof lib>();
  return {
    ...actual,
    run: vi.fn(),
    runOrDiagnose: vi.fn(),
    diagnose: vi.fn(),
    // The one network call on the deliver="url" path. `blobStoreFromEnv` and
    // `createBlobUrlMinter` are deliberately NOT mocked: the signing is the part
    // the gateway judges, so these tests assert the real minter's URLs.
    uploadToBlobStore: vi.fn(),
    // Real filesystem effects on the download root (create 0700, sweep,
    // delete-after-delivery) are covered in gogcli-mcp's attachment-root tests;
    // here they are observed, not performed.
    prepareDownloadRoot: vi.fn(),
    removeDownload: vi.fn(),
  };
});

// finalizeGmailSearch reaches for runner.run DIRECTLY (not the lib re-export
// the mock above replaces) to count matches behind a truncated result set.
// Without this the probe would spawn the real `gog` and hit the live Gmail API
// from a unit test. Only `run` is replaced.
vi.mock('../../../gogcli-mcp/src/runner.js', async (importOriginal) => {
  const actual = await importOriginal<typeof runner>();
  return { ...actual, run: vi.fn() };
});

let harness: TestHarness;
let elicitation: (request: ElicitRequest) => ElicitResult | Promise<ElicitResult>;

beforeEach(async () => {
  vi.clearAllMocks();
  vi.mocked(lib.run).mockResolvedValue('{}');
  vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult('{}'));
  vi.mocked(lib.diagnose).mockResolvedValue(errorResult('diagnosed'));
  // Default: the match-count probe finds nothing to report, so no test depends
  // on a live call. Tests that care stub it explicitly.
  vi.mocked(runner.run).mockRejectedValue(new Error('no count probe stubbed'));
  vi.mocked(lib.uploadToBlobStore).mockRejectedValue(new Error('no blob upload stubbed'));
  elicitation = async () => ({ action: 'accept', content: { confirmed: true } });
  harness = await createTestHarness(registerExtraGmailTools, {
    elicitation: (request) => elicitation(request),
  });
});

describe('gog_gmail_raw', () => {
  it('calls runOrDiagnose with messageId', async () => {
    await harness.callTool('gog_gmail_raw', { messageId: 'm1' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['gmail', 'raw', pos('m1')], { account: undefined, lossless: true });
  });

  it('passes --format and --pretty when provided', async () => {
    await harness.callTool('gog_gmail_raw', { messageId: 'm1', format: 'metadata', pretty: true });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'raw', pos('m1'), '--format=metadata', '--pretty'],
      { account: undefined, lossless: true },
    );
  });

  it('omits --pretty when false', async () => {
    await harness.callTool('gog_gmail_raw', { messageId: 'm1', pretty: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['gmail', 'raw', pos('m1')], { account: undefined, lossless: true });
  });
});

describe('gog_gmail_attachment', () => {
  // base64 whose first 16 chars decode to the given ASCII/binary prefix.
  const PNG_B64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB'; // "\x89PNG\r\n\x1a\n..."
  const PDF_B64 = 'JVBERi0xLjUKJVBFRgo='; // "%PDF-1.5\n%PEF\n"
  const OCTET_B64 = 'AAAAAAAAAAAAAAAA'; // decodes to NUL bytes — no magic match

  // Route the mocked `run` by subcommand: the metadata lookup (`gmail get`), the
  // download (`gmail attachment`), and the Drive upload (`drive upload`).
  function stubGog(opts: {
    meta?: unknown;
    metaError?: Error;
    download?: unknown;
    drive?: unknown;
    downloadError?: unknown;
  }): void {
    vi.mocked(lib.run).mockImplementation(async (args) => {
      const a = plain(args);
      if (a[0] === 'gmail' && a[1] === 'get') {
        if (opts.metaError) throw opts.metaError;
        return JSON.stringify(opts.meta ?? { attachments: [] });
      }
      if (a[0] === 'gmail' && a[1] === 'attachment') {
        if (opts.downloadError) throw opts.downloadError;
        // A FUNCTION download is handed the arg array, so a stub can answer
        // with the `--out` it was actually told to write to — which is what gog
        // does, and the only way a test can see the tool choosing a path other
        // than the one it later hands somebody else to read.
        const answer = typeof opts.download === 'function'
          ? (opts.download as (args: string[]) => unknown)(a)
          : opts.download;
        return JSON.stringify(answer ?? {});
      }
      if (a[0] === 'drive' && a[1] === 'upload') return JSON.stringify(opts.drive ?? { file: {} });
      return '{}';
    });
  }

  // The part metadata (`gmail get` `.attachments[]`) is matched by SIZE — Gmail's
  // attachmentId isn't stable across calls — so every list entry carries a `size`
  // that the download's `bytes` must equal for the filename/MIME to resolve.
  const PDF_LIST = { attachments: [{ filename: 'Guest_Copy.pdf', mimeType: 'application/pdf', size: 99723 }] };
  const PNG_LIST = { attachments: [{ filename: 'photo.png', mimeType: 'image/png', size: 24 }] };

  const call = (args: Record<string, unknown>) =>
    harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentId: 'a1', ...args });
  const textOf = (res: Awaited<ReturnType<typeof call>>) => (res.content[0] as { text: string }).text;
  const gotGet = () => vi.mocked(lib.run).mock.calls.some((c) => (c[0] as string[])[1] === 'get');
  const dlArgs = () => vi.mocked(lib.run).mock.calls.find((c) => (c[0] as string[])[1] === 'attachment')![0] as string[];
  // The path gog was told to write to. Read out of the args rather than restated
  // as a literal, so an assertion about where the file IS cannot quietly become
  // an assertion about where a test thinks it is.
  const outOf = (args: string[]) => args.find((a) => typeof a === 'string' && a.startsWith('--out='))!.slice('--out='.length);

  it('the repro: a no-name PDF on stdio comes back as a readable file path, named correctly', async () => {
    // download writes to a provisional temp path; the real name resolves by size.
    stubGog({ meta: PDF_LIST, download: { path: `${ROOT}/m1/attachment`, bytes: 99723, contentBase64: PDF_B64 } });
    const res = await call({});
    // download to the temp path first, then the metadata read to resolve the name.
    expect(dlArgs()).toEqual(['gmail', 'attachment', pos('m1'), pos('a1'), '--use-indexed-attachment-ids=false', '--inline', '--inline-max-bytes=3145728', `--out=${ROOT}/m1/attachment`, '--name=attachment']);
    expect(gotGet()).toBe(true);
    const payload = JSON.parse(textOf(res));
    expect(payload).toMatchObject({
      delivery: 'file', path: `${ROOT}/m1/attachment`, fileName: 'Guest_Copy.pdf', mimeType: 'application/pdf', bytes: 99723,
    });
    // never an embedded-resource blob on auto (the claude.ai host rejects those for PDF).
    expect(res.content.some((c) => c.type === 'resource')).toBe(false);
  });

  it('an image renders inline (image block)', async () => {
    stubGog({ meta: PNG_LIST, download: { path: `${ROOT}/m1/attachment`, bytes: 24, contentBase64: PNG_B64 } });
    const local = await call({});
    expect(local.content[1]).toEqual({ type: 'image', data: PNG_B64, mimeType: 'image/png' });
    expect(textOf(local)).toContain('photo.png');
    expect(lib.run).not.toHaveBeenCalledWith(expect.arrayContaining(['drive', 'upload']), expect.anything());
  });

  it('a caller-supplied name skips the metadata lookup and names the file directly', async () => {
    stubGog({ download: { path: `${ROOT}/m1/report.pdf`, bytes: 12, contentBase64: PDF_B64 } });
    await call({ name: 'report.pdf' });
    expect(gotGet()).toBe(false);
    expect(dlArgs()).toEqual(['gmail', 'attachment', pos('m1'), pos('a1'), '--use-indexed-attachment-ids=false', '--inline', '--inline-max-bytes=3145728', `--out=${ROOT}/m1/report.pdf`, '--name=report.pdf']);
  });

  it('resolves the real filename by size and sanitizes path separators (no traversal)', async () => {
    stubGog({
      meta: { attachments: [{ filename: '../../etc/evil.pdf', mimeType: 'application/pdf', size: 10 }] },
      download: { path: `${ROOT}/m1/attachment`, bytes: 10, contentBase64: PDF_B64 },
    });
    const res = await call({});
    const fileName = JSON.parse(textOf(res)).fileName as string;
    expect(fileName).not.toMatch(/[/\\]/); // single safe segment, no traversal
    expect(fileName).toContain('evil.pdf');
  });

  it('derives an extension from the MIME type when the part has no filename (never *.bin)', async () => {
    stubGog({
      meta: { attachments: [{ mimeType: 'application/pdf', size: 10 }] },
      download: { path: `${ROOT}/m1/attachment`, bytes: 10, contentBase64: PDF_B64 },
    });
    const res = await call({});
    expect(JSON.parse(textOf(res)).fileName).toBe('attachment.pdf');
  });

  it('falls back to a magic-byte sniff when the size is ambiguous (repeated)', async () => {
    stubGog({
      meta: { attachments: [
        { filename: 'a.pdf', mimeType: 'application/pdf', size: 10 },
        { filename: 'b.pdf', mimeType: 'application/pdf', size: 10 },
      ] },
      download: { path: `${ROOT}/m1/attachment`, bytes: 10, contentBase64: PDF_B64 },
    });
    const res = await call({});
    // two parts share the size → no unique match → sniff + derived name.
    expect(JSON.parse(textOf(res))).toMatchObject({ fileName: 'attachment.pdf', mimeType: 'application/pdf' });
  });

  it('survives a metadata-lookup failure and still delivers, sniffing the MIME', async () => {
    stubGog({ metaError: new Error('get failed'), download: { path: `${ROOT}/m1/attachment`, bytes: 24, contentBase64: PNG_B64 } });
    const res = await call({});
    // resolveBySize catches the failure → sniff → image/png.
    expect(res.content[1]).toEqual({ type: 'image', data: PNG_B64, mimeType: 'image/png' });
  });

  it('summarizes with "? bytes" when the download reports no size (skips the size lookup)', async () => {
    stubGog({ download: { path: `${ROOT}/m1/x.png`, contentBase64: PNG_B64 }, meta: PNG_LIST });
    const res = await call({ name: 'x.png' });
    expect(gotGet()).toBe(false); // no bytes → no size match needed; name given anyway
    expect(res.content[1]).toEqual({ type: 'image', data: PNG_B64, mimeType: 'image/png' });
    expect(textOf(res)).toContain('? bytes');
  });

  it('skips the size lookup entirely when the download reports no bytes and no name', async () => {
    stubGog({ download: { path: `${ROOT}/m1/attachment`, contentBase64: OCTET_B64 } });
    const res = await call({});
    // info.bytes undefined → resolveBySize short-circuits (no `gmail get`).
    expect(gotGet()).toBe(false);
    expect(JSON.parse(textOf(res))).toMatchObject({ delivery: 'file', fileName: 'attachment', mimeType: 'application/octet-stream' });
  });

  it('falls back to application/octet-stream when the message has no attachments array', async () => {
    // meta with no `attachments` key exercises the `?? []` guard in resolveBySize.
    stubGog({ meta: {}, download: { path: `${ROOT}/m1/attachment`, bytes: 12, contentBase64: OCTET_B64 } });
    const res = await call({});
    expect(JSON.parse(textOf(res))).toMatchObject({ delivery: 'file', fileName: 'attachment', mimeType: 'application/octet-stream' });
  });

  it('deliver=inline returns a native image block for an image', async () => {
    stubGog({ meta: PNG_LIST, download: { path: `${ROOT}/m1/attachment`, bytes: 24, contentBase64: PNG_B64 } });
    const res = await call({ deliver: 'inline' });
    expect(res.content[1]).toEqual({ type: 'image', data: PNG_B64, mimeType: 'image/png' });
  });

  it('deliver=inline forces an embedded resource blob for a non-image', async () => {
    stubGog({ download: { path: `${ROOT}/m1/doc.pdf`, bytes: 12, contentBase64: PDF_B64 } });
    const res = await call({ deliver: 'inline', name: 'doc.pdf' });
    expect(res.content[1]).toEqual({
      type: 'resource',
      resource: { uri: 'gmail-attachment://m1/doc.pdf', mimeType: 'application/pdf', blob: PDF_B64 },
    });
  });

  it('deliver=inline errors when the attachment is too large (no reason field)', async () => {
    // no `path` either → exercises the `info.path ?? outPath` fallback.
    stubGog({ download: { bytes: 9_000_000 } });
    const res = await call({ deliver: 'inline', name: 'big.pdf' });
    expect(res.isError).toBe(true);
    expect(textOf(res)).toContain('too large');
    expect(lib.run).not.toHaveBeenCalledWith(expect.arrayContaining(['drive', 'upload']), expect.anything());
  });

  it('deliver=drive skips --inline and uploads, honoring driveFolder and name', async () => {
    stubGog({ download: { path: `${ROOT}/m1/renamed.png`, bytes: 24 }, drive: { file: { id: 'F2', webViewLink: 'https://drive.google.com/file/d/F2/view' } } });
    const res = await call({ deliver: 'drive', driveFolder: 'DIR9', name: 'renamed.png', account: 'me@x.com' });
    expect(dlArgs()).toEqual(['gmail', 'attachment', pos('m1'), pos('a1'), '--use-indexed-attachment-ids=false', '--inline-max-bytes=3145728', `--out=${ROOT}/m1/renamed.png`, '--name=renamed.png']);
    expect(lib.run).toHaveBeenCalledWith(
      ['drive', 'upload', pos(`${ROOT}/m1/renamed.png`), '--json', '--parent=DIR9', '--name=renamed.png'], { account: 'me@x.com' });
    expect(JSON.parse(textOf(res))).toMatchObject({ deliveredVia: 'drive', id: 'F2' });
  });

  it('deliver=off returns a structured record with the size-resolved filename + mime', async () => {
    stubGog({ meta: PDF_LIST, download: { path: `${ROOT}/m1/attachment`, bytes: 99723, cached: true } });
    const res = await call({ deliver: 'off' });
    expect(JSON.parse(textOf(res))).toMatchObject({
      delivery: 'file', path: `${ROOT}/m1/attachment`, fileName: 'Guest_Copy.pdf', mimeType: 'application/pdf', bytes: 99723, cached: true,
    });
  });

  it('still reports drive delivery when the upload output lacks a file envelope', async () => {
    stubGog({ meta: PDF_LIST, download: { path: `${ROOT}/m1/attachment`, bytes: 99723 }, drive: {} });
    const res = await call({ deliver: 'drive' });
    const payload = JSON.parse(textOf(res));
    expect(payload).toMatchObject({ deliveredVia: 'drive' });
    expect(payload.id).toBeUndefined();
  });

  it('honors a caller out on stdio', async () => {
    stubGog({ download: { path: '/home/me/x.png', bytes: 24, contentBase64: PNG_B64 } });
    await call({ out: '/home/me/x.png', name: 'x.png' });
    expect(dlArgs()).toEqual(['gmail', 'attachment', pos('m1'), pos('a1'), '--use-indexed-attachment-ids=false', '--inline', '--inline-max-bytes=3145728', '--out=/home/me/x.png', '--name=x.png']);
  });

  it('a caller name that sanitizes to empty falls back to "attachment"', async () => {
    stubGog({ download: { path: `${ROOT}/m1/attachment`, bytes: 10 } });
    await call({ name: '...' }); // only dots → sanitizes to '' → 'attachment'
    expect(dlArgs()).toEqual(expect.arrayContaining(['--name=attachment', `--out=${ROOT}/m1/attachment`]));
  });

  it('wraps a download failure without leaking the command line or the attachment token', async () => {
    stubGog({ downloadError: new Error('Command failed: gog gmail attachment m1 a1 --out=/home/claude/x.pdf\nmkdir /home/claude: permission denied') });
    const res = await call({});
    expect(lib.diagnose).toHaveBeenCalled();
    const passed = (vi.mocked(lib.diagnose).mock.calls[0][0] as Error).message;
    expect(passed).not.toContain('Command failed');
    expect(passed).not.toContain('a1');
    expect(passed).not.toContain('m1');
    expect(passed).toContain('permission denied');
    expect(res.isError).toBe(true);
  });

  it('wraps a non-Error rejection', async () => {
    stubGog({ downloadError: 'weird string failure' });
    await call({});
    expect((vi.mocked(lib.diagnose).mock.calls[0][0] as Error).message).toBe('weird string failure');
  });

  it('falls back to a generic message when the error is nothing but the command echo', async () => {
    stubGog({ downloadError: new Error('Command failed: gog gmail attachment m1 a1\n') });
    await call({});
    expect((vi.mocked(lib.diagnose).mock.calls[0][0] as Error).message).toBe('the download failed on the server');
  });

  // ==========================================================================
  // FILENAME INDEPENDENCE — the defect reported as "inline delivery fails on
  // filenames containing spaces".
  //
  // It was never the filename. The runner spawns an argv ARRAY (never a shell),
  // so a space has nothing to split; the real variable was the base64 content
  // colliding with a redaction pattern. These lock in that names with spaces,
  // non-ASCII and punctuation all deliver inline, and that the download args
  // carry each name as ONE element.
  // ==========================================================================
  describe('filename independence', () => {
    const NAMES = [
      'image.png',
      'Screenshot 2026-06-13 152500.png',
      'Reçu — étude, final (v2).png',
      "quote'and\"double.png",
      'ファイル 名前.png',
    ];

    for (const filename of NAMES) {
      it(`delivers ${JSON.stringify(filename)} inline as an image`, async () => {
        // Indexed mode resolves the real name BEFORE the download, so the name
        // is what gets handed to gog — the strongest form of this assertion.
        stubGog({
          meta: { attachments: [{ filename, mimeType: 'image/png', size: 24, attachmentIndex: 0 }] },
          download: { path: `${ROOT}/m1/${filename}`, bytes: 24, contentBase64: PNG_B64, filename, mimeType: 'image/png' },
        });
        const res = await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentIndex: 0 });
        const image = res.content.find((c) => c.type === 'image') as { data: string; mimeType: string };
        expect(image).toBeDefined();
        expect(image.data).toBe(PNG_B64);
        // The name reaches gog as a SINGLE argv element, spaces and all.
        expect(dlArgs()).toContain(`--name=${filename}`);
        expect(dlArgs()).toContain(`--out=${ROOT}/m1/${filename}`);
        expect((res.content[0] as { text: string }).text).toContain(filename);
      });
    }

    it('passes a spaced --out path as one argv element, never split on whitespace', async () => {
      const filename = 'Screenshot 2026-06-13 152500.png';
      stubGog({ download: { bytes: 24, contentBase64: PNG_B64, filename, mimeType: 'image/png' } });
      await call({ name: filename });
      const args = dlArgs();
      expect(args).toContain(`--out=${ROOT}/m1/${filename}`);
      // If anything had split on spaces these would appear as separate elements.
      expect(args).not.toContain('2026-06-13');
      expect(args).not.toContain('152500.png');
    });
  });

  // The bytes are exempted from redaction at the runner seam; this asserts the
  // tool actually asks for that exemption, which is the thing that keeps a
  // `1//`-containing PNG from arriving corrupt.
  it('requests the contentBase64 redaction exemption on the download', async () => {
    stubGog({ download: { bytes: 24, contentBase64: PNG_B64, filename: 'a.png', mimeType: 'image/png' } });
    await call({});
    const call0 = vi.mocked(lib.run).mock.calls.find((c) => (c[0] as string[])[1] === 'attachment')!;
    expect(call0[1]).toMatchObject({ opaqueFields: ['contentBase64'] });
  });

  // Belt-and-braces: if bytes ever do arrive unusable, the caller must get a
  // readable tool result, not an MCP -32602 protocol fault they cannot act on.
  it('degrades to the file path when the returned bytes are not valid base64', async () => {
    stubGog({
      meta: PNG_LIST,
      download: { path: `${ROOT}/m1/photo.png`, bytes: 24, contentBase64: 'not!valid!base64!', filename: 'photo.png', mimeType: 'image/png' },
    });
    const res = await call({});
    expect(res.content.some((c) => c.type === 'image')).toBe(false);
    expect(textOf(res)).toContain('not valid base64');
    expect(JSON.stringify(res)).toContain(`${ROOT}/m1/photo.png`);
  });

  // The MIME sniff decodes the leading bytes. On an unusable payload that decode
  // is the FIRST thing to fail, and it must not be what surfaces — the caller's
  // problem is the payload, not the sniff.
  it('survives a MIME sniff of unusable bytes instead of throwing out of the sniff', async () => {
    stubGog({
      meta: { attachments: [] }, // nothing to resolve a MIME type from
      download: { path: `${ROOT}/m1/attachment`, bytes: 4, contentBase64: '!!!!' },
    });
    const res = await call({});
    expect(res.isError).toBeUndefined();
    // content[0] is the dropped-inline note; the delivery payload follows it.
    const payload = JSON.parse((res.content.at(-1) as { text: string }).text);
    expect(payload.mimeType).toBe('application/octet-stream');
    expect(payload.fileName).toBe('attachment');
  });

  it('explains itself rather than throwing when deliver=inline gets unusable bytes', async () => {
    stubGog({
      meta: PNG_LIST,
      download: { path: `${ROOT}/m1/photo.png`, bytes: 24, contentBase64: '!!!!', filename: 'photo.png', mimeType: 'image/png' },
    });
    const res = await call({ deliver: 'inline' });
    expect(res.isError).toBe(true);
    expect(textOf(res)).toContain('not valid base64');
    expect(textOf(res)).toContain(`${ROOT}/m1/photo.png`);
  });

  // The messageId is the CALLER's string and it is interpolated into gog's
  // `--out`, a path gog MkdirAll's and writes to server-side. deliver="url"
  // held it to one segment (there the path and the object key have to be the
  // same string, so the gap showed up as a refused upload); every OTHER mode
  // interpolated it raw. Asserted per DELIVERY MODE rather than once, because
  // the shape of the defect was that the careful path was the new one and the
  // four older ones were never revisited.
  describe('a hostile messageId never leaves the attachment root', () => {
    // Each expectation is one path segment: separators collapse to '_', a
    // leading run of dots is stripped, and a segment that sanitizes to nothing
    // falls back to 'attachment'.
    const IDS: ReadonlyArray<readonly [string, string]> = [
      ['../../etc/passwd', '_.._etc_passwd'],
      ['..', 'attachment'],
      ['a/b', 'a_b'],
      ['.hidden', 'hidden'],
      [' ..', 'attachment'], // the leading-space shape: the trim must precede the dot strip
    ];

    for (const deliver of ['auto', 'inline', 'drive', 'off'] as const) {
      for (const [messageId, segment] of IDS) {
        it(`deliver="${deliver}" keeps ${JSON.stringify(messageId)} in one segment`, async () => {
          stubGog({
            meta: PNG_LIST,
            // Echo the `--out` gog was told to write to, so the assertion is
            // about the path the tool CHOSE rather than one the stub invented.
            download: (args: string[]) => ({ path: outOf(args), bytes: 24, contentBase64: PNG_B64 }),
            drive: { file: { id: 'F1', webViewLink: 'https://drive.google.com/file/d/F1/view' } },
          });

          // `name` is passed so the basename is settled BEFORE the download and
          // the assertion is about the directory segment alone.
          await harness.callTool('gog_gmail_attachment', {
            messageId, attachmentId: 'a1', deliver, name: 'photo.png',
          });

          expect(outOf(dlArgs())).toBe(`${ROOT}/${segment}/photo.png`);
        });
      }
    }
  });

  // ==========================================================================
  // deliver="url" — the attachment as a link an agent can actually fetch.
  //
  // A hosted MCP has no HTTP surface, so `deliver:"drive"` was the only way to
  // hand back a large or non-renderable attachment — and a `webViewLink` needs
  // a Google session, so `curl` cannot spend it; it writes a file into the
  // user's Drive as a side effect of READING mail; and GOG_READONLY blocks it
  // outright. mcp-host lends the missing surface: a per-registration blob store
  // where a signed URL is the whole access control.
  //
  // The upload happens in this process, which is where the bytes are — gog
  // runs in the same process tree and `gog gmail attachment --out` wrote the
  // file to this machine's disk. `uploadToBlobStore` is the only thing mocked
  // here; the SIGNING is the real minter, so these
  // tests see the URLs the gateway would be asked to verify.
  // ==========================================================================
  describe('deliver="url"', () => {
    const BLOB_BASE = 'https://blob.example/b/reg_7';
    // message, then the attachment REFERENCE, then the name. Two attachments of
    // one message can share a filename; keyed on the message alone the second
    // upload overwrites the first.
    const KEY_PATH = `${BLOB_BASE}/gmail/m1/a1/Guest_Copy.pdf?exp=`;

    // Both variables, exactly as mcp-host hands them to a child at spawn.
    const withBlobStore = (): void => {
      vi.stubEnv('MCP_BLOB_BASE_URL', BLOB_BASE);
      vi.stubEnv('MCP_BLOB_SIGNING_KEY', 'signing-key');
    };
    // '' rather than a delete: `readEnvVar` treats a blank as unset and vitest's
    // stubEnv cannot remove a key. This is a LOCAL stdio install.
    const withoutBlobStore = (): void => {
      vi.stubEnv('MCP_BLOB_BASE_URL', '');
      vi.stubEnv('MCP_BLOB_SIGNING_KEY', '');
    };
    const uploaded = () => vi.mocked(lib.uploadToBlobStore).mock.calls[0][0];
    // gog writes where it was TOLD to write and reports that path back, so the
    // stub echoes the tool's own `--out`. A fixed literal cannot see the defect
    // this mode is most exposed to: the path handed to the upload and the key
    // the link is minted under are built from the same two caller strings, and a
    // stub answering the same path whatever it was asked hides them drifting.
    const PDF_DOWNLOAD = (args: string[]) => ({ path: outOf(args), bytes: 99723 });
    // The last text block. `withNote` PREPENDS its note, so content[0] is the
    // note whenever there is one and the payload is always the tail.
    const payloadOf = (res: Awaited<ReturnType<typeof call>>) =>
      JSON.parse((res.content[res.content.length - 1] as { text: string }).text);

    afterEach(() => {
      vi.unstubAllEnvs();
    });

    it('uploads the downloaded file and answers with a link, its name, type, size and expiry', async () => {
      withBlobStore();
      stubGog({ meta: PDF_LIST, download: PDF_DOWNLOAD });
      // DELIBERATELY not gog's 99723: the object now sitting at that URL is what
      // the upload streamed, and that is the number the caller is told.
      vi.mocked(lib.uploadToBlobStore).mockResolvedValue({ bytes: 99730, status: 200 });

      const res = await call({ deliver: 'url' });

      // The upload is asked to send the file gog wrote, to the URL we signed,
      // under the content type that signature commits to — byte for byte, or
      // the gateway answers the PUT as an object that does not exist.
      expect(uploaded().path).toBe(outOf(dlArgs()));
      expect(uploaded().path).toBe(`${ROOT}/m1/a1/attachment`);
      expect(uploaded().contentType).toBe('application/pdf');
      expect(uploaded().url).toContain(KEY_PATH);
      expect(uploaded().url).toMatch(/&sig=[\w-]+$/);

      const payload = payloadOf(res);
      expect(payload).toMatchObject({
        deliveredVia: 'url',
        fileName: 'Guest_Copy.pdf',
        mimeType: 'application/pdf',
        bytes: 99730,
      });
      expect(payload.url).toContain(KEY_PATH);
      // The DELIVERED link still carries its signature. `?exp=` alone is not
      // fetchable — the gateway verifies the signature before it reads a
      // registration row at all — so a response path that dropped or mangled
      // `sig=` would hand the agent a permanently-404ing link. Not hypothetical:
      // `errorResult` redacts exactly this query value (proven by the leak test
      // below), so building the payload with one instead of `textResult` would
      // do it silently.
      expect(payload.url).toMatch(/\?exp=\d+&sig=[\w-]+$/);
      // A READ signature, over a different payload shape — never the write URL
      // handed back, which would let whoever holds it overwrite the object.
      expect(payload.url).not.toBe(uploaded().url);
      // ONE HOUR, which is what the tool description, the note, the README and
      // SKILL.md all promise in prose. Asserted as a window rather than "in the
      // future", which a ten-second link also satisfies.
      const ttlMs = Date.parse(payload.expiresAt) - Date.now();
      expect(ttlMs).toBeGreaterThan(55 * 60_000);
      expect(ttlMs).toBeLessThanOrEqual(60 * 60_000);
      // The agent has to know it can just fetch this, and that it stops working.
      expect(payload.note).toMatch(/curl/);
      expect(payload.note).toMatch(/expires/i);
    });

    it('links an image too when deliver="url" is explicit', async () => {
      withBlobStore();
      // An image, and still a link: deliver is explicit, so it outranks the
      // "images render everywhere" rule that `auto` applies.
      stubGog({ meta: PNG_LIST, download: (args: string[]) => ({ path: outOf(args), bytes: 24, contentBase64: PNG_B64 }) });
      vi.mocked(lib.uploadToBlobStore).mockResolvedValue({ bytes: 24, status: 200 });

      const res = await call({ deliver: 'url' });

      expect(res.content.some((c) => c.type === 'image')).toBe(false);
      expect(payloadOf(res)).toMatchObject({ deliveredVia: 'url', bytes: 24, mimeType: 'image/png' });
    });

    // THE DEPLOYMENT THIS MODE ACTUALLY RUNS ON. mcp-host's child spawns gog
    // itself, so a caller `out` would otherwise be honoured, and `uploadToBlobStore` refuses any
    // path outside the attachment download root: honouring it means a refusal
    // and no link. The path is not the caller's to choose for this mode.
    it('ignores a caller `out` and downloads where the upload will read it back', async () => {
      withBlobStore();
      stubGog({ meta: PDF_LIST, download: PDF_DOWNLOAD });
      vi.mocked(lib.uploadToBlobStore).mockResolvedValue({ bytes: 99723, status: 200 });

      const res = await call({ deliver: 'url', out: '/home/claude/mine.pdf' });

      expect(outOf(dlArgs())).toBe(`${ROOT}/m1/a1/attachment`);
      expect(uploaded().path).toBe(outOf(dlArgs()));
      expect(textOf(res)).toContain('`out` was ignored');
      expect(payloadOf(res)).toMatchObject({ deliveredVia: 'url' });
    });

    // Two attachments of one message can share a filename — two scans named
    // IMG_0001.jpg, two invoice.pdf parts. Keyed on the message alone the second
    // upload OVERWRITES the first, and a link already handed to the agent for
    // the first silently starts serving the other's bytes, under the name and
    // type the earlier answer reported.
    it('keys each attachment separately, so a shared filename cannot overwrite', async () => {
      withBlobStore();
      stubGog({
        meta: { attachments: [
          { filename: 'invoice.pdf', mimeType: 'application/pdf', size: 99723, attachmentIndex: 0 },
          { filename: 'invoice.pdf', mimeType: 'application/pdf', size: 99723, attachmentIndex: 1 },
        ] },
        download: PDF_DOWNLOAD,
      });
      vi.mocked(lib.uploadToBlobStore).mockResolvedValue({ bytes: 99723, status: 200 });

      const first = await harness.callTool('gog_gmail_attachment', {
        messageId: 'm1', attachmentIndex: 0, deliver: 'url',
      });
      const second = await harness.callTool('gog_gmail_attachment', {
        messageId: 'm1', attachmentIndex: 1, deliver: 'url',
      });

      expect(new URL(payloadOf(first).url).pathname).toBe('/b/reg_7/gmail/m1/0/invoice.pdf');
      expect(new URL(payloadOf(second).url).pathname).toBe('/b/reg_7/gmail/m1/1/invoice.pdf');
    });

    // The blob store's own rule for a child that does not find it: fail, say
    // why, and name what does work here. Half-working would be worse — a
    // download paid for and nothing to show for it.
    it('refuses on a local stdio install, before anything is downloaded', async () => {
      withoutBlobStore();
      stubGog({ meta: PDF_LIST, download: PDF_DOWNLOAD });

      const res = await call({ deliver: 'url' });

      expect(res.isError).toBe(true);
      expect(textOf(res)).toContain('MCP_BLOB_BASE_URL');
      expect(textOf(res)).toMatch(/deliver="auto"/);
      expect(lib.run).not.toHaveBeenCalled();
      expect(lib.uploadToBlobStore).not.toHaveBeenCalled();
    });

    it('names a misconfigured blob store instead of minting links that 404', async () => {
      vi.stubEnv('MCP_BLOB_BASE_URL', 'https://blob.example/b'); // the mount, with no registration id
      vi.stubEnv('MCP_BLOB_SIGNING_KEY', 'signing-key');

      const res = await call({ deliver: 'url' });

      expect(res.isError).toBe(true);
      expect(textOf(res)).toContain('MCP_BLOB_BASE_URL');
      expect(lib.run).not.toHaveBeenCalled();
    });

    // A signed URL is a credential with up to 24 h of anybody-who-holds-it
    // access, and an error result is read by a model and written to logs.
    it('explains a failed upload without leaking the signed URL or its signature', async () => {
      withBlobStore();
      stubGog({ meta: PDF_LIST, download: PDF_DOWNLOAD });
      vi.mocked(lib.uploadToBlobStore).mockRejectedValue(
        new Error('the blob store refused the upload with 403: <signed url>'),
      );

      const res = await call({ deliver: 'url' });

      expect(res.isError).toBe(true);
      expect(textOf(res)).toContain('refused the upload with 403');
      expect(textOf(res)).toContain('deliver="drive"'); // a route that still works
      expect(textOf(res)).not.toContain(uploaded().url);
      expect(textOf(res)).not.toContain(new URL(uploaded().url).searchParams.get('sig'));
      // Those two assertions alone cannot fail for the reason this test is
      // named after: `errorResult` runs mcp-utils' `redactSecrets`, which
      // rewrites a `sig=` query value to `[REDACTED]` on its own — so a message
      // that DID interpolate the whole write URL still passes both. mcp-utils
      // is the second layer, not the property; what this tool owes is that the
      // URL never enters the text. Assert on the part redaction leaves behind —
      // the prefix identifying the registration and the object — which is
      // present iff the URL was written and absent iff it was not.
      expect(textOf(res)).not.toContain('/b/reg_7/');
      expect(textOf(res)).not.toContain('Guest_Copy.pdf?exp=');
    });

    it('reports an upload that rejected with something other than an Error', async () => {
      withBlobStore();
      stubGog({ meta: PDF_LIST, download: PDF_DOWNLOAD });
      vi.mocked(lib.uploadToBlobStore).mockRejectedValue('the socket hung up');

      const res = await call({ deliver: 'url' });

      expect(res.isError).toBe(true);
      expect(textOf(res)).toContain('the socket hung up');
    });

    // GOG_READONLY is `runner.ts` adding `--readonly` to a gog invocation, to
    // stop writes to the USER'S Google account. This path never asks gog to
    // write anything: it reads the attachment, and the bytes are then copied
    // into the host's own store over HTTP. That is exactly what makes it usable
    // where deliver="drive" is refused.
    it('runs no mutating gog command, which is why GOG_READONLY cannot block it', async () => {
      withBlobStore();
      stubGog({ meta: PDF_LIST, download: PDF_DOWNLOAD });
      vi.mocked(lib.uploadToBlobStore).mockResolvedValue({ bytes: 99723, status: 200 });

      await call({ deliver: 'url' });

      const commands = vi.mocked(lib.run).mock.calls.map((c) => (c[0] as string[]).slice(0, 2).join(' '));
      expect(commands).not.toContain('drive upload');
      expect(commands.every((c) => c === 'gmail get' || c === 'gmail attachment')).toBe(true);
    });

    // The messageId is the caller's, and it is interpolated into the object
    // key. The gateway REFUSES an empty, '.' or '..' segment rather than
    // normalising it — such a link could never be spent — so the id is held to
    // one segment here, where the message names the call site.
    it('keeps a hostile messageId and attachmentId inside one key segment each, on disk and in the key', async () => {
      withBlobStore();
      stubGog({ meta: PDF_LIST, download: PDF_DOWNLOAD });
      vi.mocked(lib.uploadToBlobStore).mockResolvedValue({ bytes: 99723, status: 200 });

      // BOTH are the caller's strings, and both are now segments of the key.
      await harness.callTool('gog_gmail_attachment', {
        messageId: '../../x', attachmentId: '../b', deliver: 'url',
      });

      expect(new URL(uploaded().url).pathname).toBe('/b/reg_7/gmail/_.._x/_b/Guest_Copy.pdf');
      // The SAME segments on disk. The string signed and the string read have to
      // be one string: `${ROOT}/../../x/attachment` is outside the
      // only root the upload will read from, so a raw id here is a refusal rather
      // than a link even though the key itself was minted correctly.
      expect(outOf(dlArgs())).toBe(`${ROOT}/_.._x/_b/attachment`);
      expect(uploaded().path).toBe(outOf(dlArgs()));

      // A LEADING SPACE is the shape that got through: the dot strip ran before
      // the trim, so ' ..' arrived at the key as a literal '..' and '  . ' as
      // '.' — the two segments the gateway refuses outright, and the two that
      // walk gog's `--out` off the only root the upload reads from. A tab works
      // (it is a control char, stripped first); a space is not one.
      vi.mocked(lib.run).mockClear();
      vi.mocked(lib.uploadToBlobStore).mockClear();
      await harness.callTool('gog_gmail_attachment', {
        messageId: ' ..', attachmentId: '  . ', deliver: 'url',
      });

      expect(new URL(uploaded().url).pathname).toBe('/b/reg_7/gmail/attachment/attachment/Guest_Copy.pdf');
      expect(outOf(dlArgs())).toBe(`${ROOT}/attachment/attachment/attachment`);
    });

    // THE OPERATOR'S DECISION, pinned rather than remembered: the blob store
    // being available does not make it the `auto` default — flipping that is a
    // one-line change somebody decides, never a side effect of configuration.
    it('leaves deliver="auto" off the blob store even when it is configured', async () => {
      withBlobStore();
      stubGog({
        meta: PDF_LIST,
        download: (args: string[]) => ({ path: outOf(args), bytes: 99723, contentBase64: PDF_B64 }),
      });

      const res = await call({});

      expect(JSON.parse(textOf(res))).toMatchObject({ delivery: 'file', fileName: 'Guest_Copy.pdf' });
      expect(lib.uploadToBlobStore).not.toHaveBeenCalled();
    });
  });
});

describe('gog_gmail_url', () => {
  it('calls runOrDiagnose with a single threadId', async () => {
    await harness.callTool('gog_gmail_url', { threadIds: ['t1'] });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['gmail', 'url', pos('t1')], { account: undefined });
  });

  it('calls runOrDiagnose with multiple threadIds', async () => {
    await harness.callTool('gog_gmail_url', { threadIds: ['t1', 't2', 't3'] });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'url', pos('t1'), pos('t2'), pos('t3')],
      { account: undefined },
    );
  });
});

describe('gog_gmail_history', () => {
  it('calls runOrDiagnose with no flags', async () => {
    await harness.callTool('gog_gmail_history', {});
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['gmail', 'history'], { account: undefined });
  });

  it('passes all history flags', async () => {
    await harness.callTool('gog_gmail_history', { since: '12345', max: 50, page: 'tok', all: true });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'history', '--since=12345', '--max=50', '--page=tok', '--all'],
      { account: undefined },
    );
  });

  it('omits --all when false', async () => {
    await harness.callTool('gog_gmail_history', { all: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['gmail', 'history'], { account: undefined });
  });
});

describe('bulk action tools (archive, mark_read, mark_unread, trash)', () => {
  const bulkTools = [
    { tool: 'gog_gmail_archive', cmd: 'archive' },
    { tool: 'gog_gmail_mark_read', cmd: 'mark-read' },
    { tool: 'gog_gmail_mark_unread', cmd: 'unread' },
    { tool: 'gog_gmail_trash', cmd: 'trash' },
  ];

  for (const { tool, cmd } of bulkTools) {
    describe(tool, () => {
      it('passes messageIds as positional args', async () => {
        await harness.callTool(tool, { messageIds: ['m1', 'm2'] });
        expect(lib.runOrDiagnose).toHaveBeenCalledWith(
          ['gmail', cmd, pos('m1'), pos('m2')],
          { account: undefined },
        );
      });

      it('passes --query and --max', async () => {
        await harness.callTool(tool, { query: 'is:unread older_than:7d', max: 50 });
        expect(lib.runOrDiagnose).toHaveBeenCalledWith(
          ['gmail', cmd, '--query=is:unread older_than:7d', '--max=50'],
          { account: undefined },
        );
      });

      it('passes both positional ids and flags together', async () => {
        await harness.callTool(tool, { messageIds: ['m1'], max: 10 });
        expect(lib.runOrDiagnose).toHaveBeenCalledWith(
          ['gmail', cmd, pos('m1'), '--max=10'],
          { account: undefined },
        );
      });
    });
  }

  // gog 0.25.0 — --thread is archive-only
  it('gog_gmail_archive passes --thread to archive whole threads by id', async () => {
    await harness.callTool('gog_gmail_archive', { messageIds: ['t1', 't2'], thread: true });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'archive', pos('t1'), pos('t2'), '--thread'],
      { account: undefined },
    );
  });

  it('other bulk tools do not expose a thread param', async () => {
    await harness.callTool('gog_gmail_trash', { messageIds: ['m1'], thread: true });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'trash', pos('m1')],
      { account: undefined },
    );
  });
});

describe('gog_gmail_message_modify', () => {
  it('calls runOrDiagnose with messageId and label changes', async () => {
    await harness.callTool('gog_gmail_message_modify', {
      messageId: 'm1',
      add: 'STARRED,IMPORTANT',
      remove: 'INBOX',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'messages', 'modify', pos('m1'), '--add=STARRED,IMPORTANT', '--remove=INBOX'],
      { account: undefined },
    );
  });

  it('omits flags when not provided', async () => {
    await harness.callTool('gog_gmail_message_modify', { messageId: 'm1' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'messages', 'modify', pos('m1')],
      { account: undefined },
    );
  });
});

describe('gog_gmail_batch_delete', () => {
  it('calls runOrDiagnose with messageIds as positional args', async () => {
    await harness.callTool('gog_gmail_batch_delete', { messageIds: ['m1', 'm2', 'm3'] });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'batch', 'delete', pos('m1'), pos('m2'), pos('m3')],
      { account: undefined },
    );
  });

  it('appends --force when force is true', async () => {
    await harness.callTool('gog_gmail_batch_delete', { messageIds: ['m1'], force: true });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'batch', 'delete', pos('m1'), '--force'],
      { account: undefined },
    );
  });

  it('omits --force when force is false', async () => {
    await harness.callTool('gog_gmail_batch_delete', { messageIds: ['m1'], force: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'batch', 'delete', pos('m1')],
      { account: undefined },
    );
  });
});

describe('gog_gmail_batch_modify', () => {
  it('calls runOrDiagnose with messageIds and label flags', async () => {
    await harness.callTool('gog_gmail_batch_modify', {
      messageIds: ['m1', 'm2'],
      add: 'STARRED',
      remove: 'INBOX',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'batch', 'modify', pos('m1'), pos('m2'), '--add=STARRED', '--remove=INBOX'],
      { account: undefined },
    );
  });

  it('omits label flags when not provided', async () => {
    await harness.callTool('gog_gmail_batch_modify', { messageIds: ['m1'] });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'batch', 'modify', pos('m1')],
      { account: undefined },
    );
  });
});

describe('gog_gmail_thread_get', () => {
  it('calls runOrDiagnose with threadId', async () => {
    await harness.callTool('gog_gmail_thread_get', { threadId: 't1' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'thread', 'get', pos('t1'), '--use-indexed-attachment-ids=false'],
      { account: undefined },
    );
  });

  it('passes all flags', async () => {
    await harness.callTool('gog_gmail_thread_get', {
      threadId: 't1',
      full: true,
      sanitizeContent: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'thread', 'get', pos('t1'), '--full', '--sanitize-content', '--use-indexed-attachment-ids=false'],
      { account: undefined },
    );
  });

  it('omits boolean flags when false', async () => {
    await harness.callTool('gog_gmail_thread_get', {
      threadId: 't1',
      download: false,
      full: false,
      sanitizeContent: false,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'thread', 'get', pos('t1'), '--use-indexed-attachment-ids=false'],
      { account: undefined },
    );
  });

  const THREAD = JSON.stringify({
    downloaded: false,
    thread: {
      id: 't1',
      messages: [
        { id: 'm1', threadId: 't1', internalDate: '1', labelIds: ['INBOX'], snippet: 'first', payload: { headers: [{ name: 'From', value: 'a@x.com' }, { name: 'Subject', value: 'Hi' }, { name: 'X-Spam', value: 'no' }, { value: 'orphan-no-name' }], body: { data: 'AAAA' } } },
        { id: 'm2', threadId: 't1', internalDate: '2', labelIds: ['INBOX'], snippet: 'second', payload: { headers: [{ name: 'From', value: 'b@x.com' }] } },
        { id: 'm3', threadId: 't1', internalDate: '3', labelIds: ['SENT'], snippet: 'third' },
      ],
    },
  });

  it('does not transform the output when no paging params are given', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(THREAD));
    const result = await harness.callTool('gog_gmail_thread_get', { threadId: 't1' });
    expect(result.content[0].text).toBe(THREAD);
  });

  it('latestN returns only the last N messages', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(THREAD));
    const result = await harness.callTool('gog_gmail_thread_get', { threadId: 't1', latestN: 2 });
    // latestN is wrapper-side; no CLI flag is added
    expect(vi.mocked(lib.runOrDiagnose).mock.calls[0]![0]).toEqual(['gmail', 'thread', 'get', pos('t1'), '--use-indexed-attachment-ids=false']);
    const parsed = JSON.parse(result.content[0].text);
    expect(parsed.thread.messages.map((m: { id: string }) => m.id)).toEqual(['m2', 'm3']);
  });

  it('snippetsOnly returns per-message headers and snippet without bodies', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(THREAD));
    const result = await harness.callTool('gog_gmail_thread_get', { threadId: 't1', snippetsOnly: true });
    const parsed = JSON.parse(result.content[0].text);
    expect(parsed.thread.messages).toHaveLength(3);
    const m1 = parsed.thread.messages[0];
    expect(m1.snippet).toBe('first');
    expect(m1.headers).toEqual({ From: 'a@x.com', Subject: 'Hi' }); // X-Spam dropped
    expect(m1.payload).toBeUndefined();
    // a message with no payload yields empty headers without throwing
    expect(parsed.thread.messages[2].headers).toEqual({});
  });

  it('combines latestN and snippetsOnly', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(THREAD));
    const result = await harness.callTool('gog_gmail_thread_get', { threadId: 't1', latestN: 1, snippetsOnly: true });
    const parsed = JSON.parse(result.content[0].text);
    expect(parsed.thread.messages).toHaveLength(1);
    expect(parsed.thread.messages[0].id).toBe('m3');
  });

  it('returns the raw result when the payload is not JSON', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult('not json'));
    const result = await harness.callTool('gog_gmail_thread_get', { threadId: 't1', latestN: 2 });
    expect(result.content[0].text).toBe('not json');
  });

  it('returns the raw result when there is no messages array', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult('{"thread":{}}'));
    const result = await harness.callTool('gog_gmail_thread_get', { threadId: 't1', snippetsOnly: true });
    expect(result.content[0].text).toBe('{"thread":{}}');
  });

  it('returns the raw result when there is no thread object', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult('{}'));
    const result = await harness.callTool('gog_gmail_thread_get', { threadId: 't1', latestN: 1 });
    expect(result.content[0].text).toBe('{}');
  });
});

describe('gog_gmail_thread_modify', () => {
  it('calls runOrDiagnose with threadId and label flags', async () => {
    await harness.callTool('gog_gmail_thread_modify', {
      threadId: 't1',
      add: 'IMPORTANT',
      remove: 'INBOX',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'thread', 'modify', pos('t1'), '--add=IMPORTANT', '--remove=INBOX'],
      { account: undefined },
    );
  });

  it('omits label flags when not provided', async () => {
    await harness.callTool('gog_gmail_thread_modify', { threadId: 't1' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'thread', 'modify', pos('t1')],
      { account: undefined },
    );
  });
});

describe('gog_gmail_thread_attachments', () => {
  it('calls runOrDiagnose with threadId', async () => {
    await harness.callTool('gog_gmail_thread_attachments', { threadId: 't1' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'thread', 'attachments', pos('t1'), '--use-indexed-attachment-ids=false'],
      { account: undefined },
    );
  });

  // SEC-4: a read-only listing used to write every attachment in the thread to
  // a caller-chosen server directory. Downloads go through gog_gmail_attachment,
  // which is confined and honestly annotated; the listing stays read-only.
  // The dead download/outDir inputs are gone from the schema (QUAL-2); a stale
  // caller that still sends them gets the plain read-only listing, never a write.
  it('ignores a stale download/outDir and only lists', async () => {
    for (const args of [{ download: true }, { outDir: '/tmp/atts' }]) {
      vi.mocked(lib.runOrDiagnose).mockClear();
      await harness.callTool('gog_gmail_thread_attachments', { threadId: 't1', ...args });
      expect(lib.runOrDiagnose).toHaveBeenCalledWith(
        ['gmail', 'thread', 'attachments', pos('t1'), '--use-indexed-attachment-ids=false'],
        { account: undefined },
      );
    }
  });
});

describe('gog_gmail_labels_list', () => {
  it('calls runOrDiagnose with no args', async () => {
    await harness.callTool('gog_gmail_labels_list', {});
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'labels', 'list'],
      { account: undefined },
    );
  });

  it('forwards account', async () => {
    await harness.callTool('gog_gmail_labels_list', { account: 'a@b.com' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'labels', 'list'],
      { account: 'a@b.com' },
    );
  });
});

describe('gog_gmail_labels_get', () => {
  it('calls runOrDiagnose with labelIdOrName', async () => {
    await harness.callTool('gog_gmail_labels_get', { labelIdOrName: 'INBOX' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'labels', 'get', pos('INBOX')],
      { account: undefined },
    );
  });
});

describe('gog_gmail_labels_create', () => {
  it('calls runOrDiagnose with name', async () => {
    await harness.callTool('gog_gmail_labels_create', { name: 'Newsletter' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'labels', 'create', pos('Newsletter')],
      { account: undefined },
    );
  });
});

describe('gog_gmail_labels_rename', () => {
  it('calls runOrDiagnose with old and new names', async () => {
    await harness.callTool('gog_gmail_labels_rename', { labelIdOrName: 'Old', newName: 'New' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'labels', 'rename', pos('Old'), pos('New')],
      { account: undefined },
    );
  });
});

describe('gog_gmail_labels_delete', () => {
  it('calls runOrDiagnose with labelIdOrName', async () => {
    await harness.callTool('gog_gmail_labels_delete', { labelIdOrName: 'Trash-Me' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'labels', 'delete', pos('Trash-Me'), '--force'],
      { account: undefined },
    );
  });
});

describe('gog_gmail_labels_modify', () => {
  it('calls runOrDiagnose with threadIds and label flags', async () => {
    await harness.callTool('gog_gmail_labels_modify', {
      threadIds: ['t1', 't2'],
      add: 'Newsletter',
      remove: 'INBOX',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'labels', 'modify', pos('t1'), pos('t2'), '--add=Newsletter', '--remove=INBOX'],
      { account: undefined },
    );
  });

  it('omits label flags when not provided', async () => {
    await harness.callTool('gog_gmail_labels_modify', { threadIds: ['t1'] });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'labels', 'modify', pos('t1')],
      { account: undefined },
    );
  });
});

describe('gog_gmail_drafts_list', () => {
  it('calls runOrDiagnose with no flags', async () => {
    await harness.callTool('gog_gmail_drafts_list', {});
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'list'],
      { account: undefined },
    );
  });

  it('passes pagination flags', async () => {
    await harness.callTool('gog_gmail_drafts_list', { max: 50, page: 'tok', all: true });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'list', '--max=50', '--page=tok', '--all'],
      { account: undefined },
    );
  });
});

// ===========================================================================
// REQUIREMENT 2 — the listing must say where each draft came from and whether
// sending it would start a NEW conversation, and TIER 0 MUST COST NOTHING.
//
// Hazard B (N+1) is enforced here by assertion, not by intention: the argv has
// to stay byte-identical to today's and `run` must never be touched. A 20-draft
// listing that quietly became 20 gog spawns on one hosted machine is the
// regression these tests exist to make impossible.
// ===========================================================================
describe('gog_gmail_drafts_list — tier 0 origin and threading', () => {
  const LIST = JSON.stringify({
    drafts: [
      // API-created reply: sits inside the co-parent's thread.
      { id: 'r4303011157206680397', messageId: '19f856becba0661d', threadId: '19f856b0000thread' },
      // The Apple Mail replacement: non-API id, roots its own thread.
      { id: 's:14092347734530621658', messageId: '19fe8a673d1e5f21', threadId: '19fe8a673d1e5f21' },
      // Draft ids can be NEGATIVE and still be plain API drafts.
      { id: 'r-457330811034304502', messageId: 'aaa', threadId: 'bbb' },
    ],
    nextPageToken: 'next-tok',
  });

  it('adds origin and rootsOwnThread without spending a single extra gog call', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(LIST));
    const result = await harness.callTool('gog_gmail_drafts_list', {});

    // Hazard B: exactly one invocation, and the argv is what it always was.
    expect(vi.mocked(lib.runOrDiagnose).mock.calls).toHaveLength(1);
    expect(vi.mocked(lib.runOrDiagnose).mock.calls[0]![0]).toEqual(['gmail', 'drafts', 'list']);
    expect(lib.run).not.toHaveBeenCalled();

    const parsed = JSON.parse(result.content[0].text);
    expect(parsed.drafts.map((d: { id: string; origin: string; rootsOwnThread: boolean }) => [d.id, d.origin, d.rootsOwnThread])).toEqual([
      ['r4303011157206680397', 'api', false],
      ['s:14092347734530621658', 'non-api', true],
      ['r-457330811034304502', 'api', false],
    ]);
    // Additive only: gog's own fields survive untouched.
    expect(parsed.drafts[0].messageId).toBe('19f856becba0661d');
    expect(parsed.nextPageToken).toBe('next-tok');
  });

  it('never labels a draft apple-mail from the listing alone', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(LIST));
    const result = await harness.callTool('gog_gmail_drafts_list', {});
    // Hazard A: an `s:` prefix means IMAP/sync — Thunderbird and Outlook produce
    // it too. Claiming "apple-mail" here would be a free false positive.
    expect(JSON.parse(result.content[0].text).drafts[1].origin).toBe('non-api');
    expect(result.content[0].text).not.toContain('apple-mail');
  });

  it('explains rootsOwnThread as the consequence the caller cares about', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(LIST));
    const parsed = JSON.parse((await harness.callTool('gog_gmail_drafts_list', {})).content[0].text);
    // Emitted ONCE for the whole result and selected by the per-row boolean —
    // it is one of exactly two constants, so a copy per row was ~300 chars of
    // duplicated text carrying no extra information.
    expect(parsed.threadingNotes.rootsOwnThread).toContain('NEW conversation');
    expect(parsed.threadingNotes.inThread).toContain('existing thread');
    expect(parsed.drafts[1].rootsOwnThread).toBe(true);
    expect(parsed.drafts[0].rootsOwnThread).toBe(false);
    // The `non-api` != Apple caveat and the measured coin-flip figure ride along once.
    expect(parsed.originNote).toContain('non-api');
    expect(parsed.originNote).toContain('0.50');
  });

  it('passes non-JSON output through untouched', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult('No drafts'));
    const result = await harness.callTool('gog_gmail_drafts_list', {});
    expect(result.content[0].text).toBe('No drafts');
  });

  it('passes JSON without a drafts array through untouched', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult('{"error":"nope"}'));
    const result = await harness.callTool('gog_gmail_drafts_list', {});
    expect(result.content[0].text).toBe('{"error":"nope"}');
  });

  it('passes a non-text result through untouched', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce({ content: [{ type: 'image', data: 'AAAA', mimeType: 'image/png' }] });
    const result = await harness.callTool('gog_gmail_drafts_list', {});
    expect(result.content[0].type).toBe('image');
  });
});

describe('gog_gmail_drafts_list — tier 1 enrich', () => {
  const LIST = JSON.stringify({
    drafts: [
      { id: 'r1', messageId: 'm1', threadId: 't1' },
      { id: 's:2', messageId: 'm2', threadId: 'm2' },
    ],
    nextPageToken: '',
  });
  const SEARCH = JSON.stringify({
    messages: [
      { id: 'm1', threadId: 't1', from: 'Chris <chris@x.com>', subject: 'Re: August schedule', internalDateIso: '2026-08-09T10:00:00-04:00' },
    ],
    nextPageToken: '',
  });

  it('is off by default — no enrichment fields and no second call', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(LIST));
    const parsed = JSON.parse((await harness.callTool('gog_gmail_drafts_list', {})).content[0].text);
    expect(lib.run).not.toHaveBeenCalled();
    expect(parsed.enrichment).toBeUndefined();
    expect(parsed.drafts[0].subject).toBeUndefined();
  });

  it('spends exactly one extra gog call and joins on messageId', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(LIST));
    vi.mocked(lib.run).mockResolvedValueOnce(SEARCH);
    const parsed = JSON.parse((await harness.callTool('gog_gmail_drafts_list', { enrich: true })).content[0].text);

    expect(vi.mocked(lib.run).mock.calls).toHaveLength(1);
    expect(vi.mocked(lib.run).mock.calls[0]![0]).toEqual([
      'gmail', 'messages', 'search', 'in:drafts', '--max=20',
      '--include-attachments=false', '--use-indexed-attachment-ids=false', '--include-recipients', '--headers=In-Reply-To',
    ]);
    expect(parsed.drafts[0]).toMatchObject({
      id: 'r1', origin: 'api', subject: 'Re: August schedule', from: 'Chris <chris@x.com>', internalDateIso: '2026-08-09T10:00:00-04:00',
    });
    // The unjoined draft keeps its tier-0 fields and gains nothing else.
    expect(parsed.drafts[1].subject).toBeUndefined();
    expect(parsed.drafts[1].origin).toBe('non-api');
    expect(parsed.enrichment).toMatchObject({ requested: true, applied: true, extraGogCalls: 1, matched: 1, unmatched: 1 });
  });

  it('mirrors max and --all onto the enrichment search', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(LIST));
    vi.mocked(lib.run).mockResolvedValueOnce(SEARCH);
    await harness.callTool('gog_gmail_drafts_list', { enrich: true, max: 50, all: true, account: 'a@b.com' });
    expect(vi.mocked(lib.run).mock.calls[0]![0]).toEqual([
      'gmail', 'messages', 'search', 'in:drafts', '--max=50', '--all',
      '--include-attachments=false', '--use-indexed-attachment-ids=false', '--include-recipients', '--headers=In-Reply-To',
    ]);
    expect(vi.mocked(lib.run).mock.calls[0]![1]).toEqual({ account: 'a@b.com' });
  });

  it('degrades to tier 0 instead of erroring when the search fails', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(LIST));
    vi.mocked(lib.run).mockRejectedValueOnce(new Error('gog exploded'));
    const result = await harness.callTool('gog_gmail_drafts_list', { enrich: true });
    const parsed = JSON.parse(result.content[0].text);
    expect(result.isError).toBeFalsy();
    expect(parsed.drafts[0].origin).toBe('api'); // tier 0 survives
    expect(parsed.enrichment).toMatchObject({ requested: true, applied: false, extraGogCalls: 1 });
    expect(parsed.enrichment.reason).toContain('gog exploded');
  });

  it('degrades to tier 0 when the search output is not JSON at all', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(LIST));
    vi.mocked(lib.run).mockResolvedValueOnce('not json at all');
    const parsed = JSON.parse((await harness.callTool('gog_gmail_drafts_list', { enrich: true })).content[0].text);
    expect(parsed.enrichment.applied).toBe(false);
    expect(parsed.drafts[0].rootsOwnThread).toBe(false);
  });

  it('degrades to tier 0 when the search output is JSON without a messages array', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(LIST));
    vi.mocked(lib.run).mockResolvedValueOnce('{"error":"quota"}');
    const parsed = JSON.parse((await harness.callTool('gog_gmail_drafts_list', { enrich: true })).content[0].text);
    expect(parsed.enrichment.applied).toBe(false);
    expect(parsed.enrichment.reason).toContain('no messages array');
    expect(parsed.drafts[1].origin).toBe('non-api');
  });

  it('skips messages with no id when joining', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(LIST));
    vi.mocked(lib.run).mockResolvedValueOnce(JSON.stringify({ messages: [{ subject: 'orphan' }] }));
    const parsed = JSON.parse((await harness.callTool('gog_gmail_drafts_list', { enrich: true })).content[0].text);
    expect(parsed.enrichment).toMatchObject({ applied: true, matched: 0, unmatched: 2 });
  });

  it('does not spend the enrichment call when the listing is unparseable', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult('No drafts'));
    const result = await harness.callTool('gog_gmail_drafts_list', { enrich: true });
    expect(lib.run).not.toHaveBeenCalled();
    expect(result.content[0].text).toBe('No drafts');
  });

  it('tolerates a draft entry with no id', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(JSON.stringify({ drafts: [{ messageId: 'm9', threadId: 'm9' }] })));
    const parsed = JSON.parse((await harness.callTool('gog_gmail_drafts_list', {})).content[0].text);
    expect(parsed.drafts[0].origin).toBe('api');
    expect(parsed.drafts[0].rootsOwnThread).toBe(true);
  });
});

// ===========================================================================
// REQUIREMENT 3 — gog_gmail_drafts_diff.
//
// Two named drafts, two gog spawns, never a scan. It answers the question the
// owner actually has in front of a fork: WHAT diverged, WHAT threading was
// lost, and — separately and conservatively — whether one plausibly replaced
// the other.
// ===========================================================================
describe('gog_gmail_drafts_diff', () => {
  const b64 = (s: string) => Buffer.from(s, 'utf8').toString('base64url');

  function draftGetJson(o: {
    draftId: string; messageId: string; threadId: string; internalDate: string;
    headers: Array<{ name: string; value: string }>; body: string;
  }): string {
    return JSON.stringify({
      draft: {
        id: o.draftId,
        message: {
          id: o.messageId,
          threadId: o.threadId,
          internalDate: o.internalDate,
          payload: { mimeType: 'text/plain', headers: o.headers, body: { data: b64(o.body) } },
        },
      },
    });
  }

  // The observed case: an API-created reply threaded onto the co-parent's
  // message, and the Apple Mail replacement that dropped a paragraph, added a
  // sentence, and landed on its own thread.
  const ORIGINAL = draftGetJson({
    draftId: 'r4303011157206680397',
    messageId: '19f856becba0661d',
    threadId: '19f856b0000thread',
    internalDate: '1000',
    headers: [
      { name: 'From', value: 'Chris Hall <chris@x.com>' },
      { name: 'To', value: 'coparent@y.com' },
      { name: 'Cc', value: 'coordinator@pc.com' },
      { name: 'Subject', value: 'Re: August schedule' },
      { name: 'Message-Id', value: '<orig@mail.gmail.com>' },
      { name: 'In-Reply-To', value: '<coparent@mail.gmail.com>' },
      { name: 'References', value: '<coparent@mail.gmail.com>' },
      { name: 'MIME-Version', value: '1.0' },
    ],
    body: 'Thanks for the note.\nI can do the 14th.\nPickup at six.\nTHE PARAGRAPH ONLY GMAIL HAS.\nBest, Chris',
  });
  const APPLE_FORK = draftGetJson({
    draftId: 's:14092347734530621658',
    messageId: '19fe8a673d1e5f21',
    threadId: '19fe8a673d1e5f21',
    internalDate: '2000',
    headers: [
      { name: 'From', value: 'chris@x.com' },
      { name: 'To', value: 'coparent@y.com' },
      { name: 'Subject', value: 'Re: August schedule' },
      { name: 'Message-Id', value: '<8F3C1B0A-1111-2222-3333-AABBCCDDEEFF@gmail.com>' },
      { name: 'Mime-Version', value: '1.0 (1.0)' },
      { name: 'X-Universally-Unique-Identifier', value: '8F3C1B0A-1111-2222-3333-AABBCCDDEEFF' },
      { name: 'X-Apple-Notify-Thread', value: 'yes' },
    ],
    body: 'Thanks for the note.\nI can do the 14th.\nPickup at six.\nBest, Chris\nTHE SENTENCE ONLY APPLE HAS.',
  });

  function stub(map: Record<string, string>): void {
    vi.mocked(lib.run).mockImplementation(async (args) => {
      const id = plain(args)[3]!;
      const payload = map[id];
      if (payload === undefined) throw new Error(`Google API error (404 notFound): ${id}`);
      return payload;
    });
  }

  const call = (extra: Record<string, unknown> = {}) => harness.callTool('gog_gmail_drafts_diff', {
    draftIdA: 'r4303011157206680397', draftIdB: 's:14092347734530621658', ...extra,
  });

  it('costs exactly two gog calls, one per named draft', async () => {
    stub({ 'r4303011157206680397': ORIGINAL, 's:14092347734530621658': APPLE_FORK });
    await call();
    expect(vi.mocked(lib.run).mock.calls).toHaveLength(2);
    expect(vi.mocked(lib.run).mock.calls[0]![0]).toEqual(['gmail', 'drafts', 'get', pos('r4303011157206680397'), '--use-indexed-attachment-ids=false']);
    expect(vi.mocked(lib.run).mock.calls[1]![0]).toEqual(['gmail', 'drafts', 'get', pos('s:14092347734530621658'), '--use-indexed-attachment-ids=false']);
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
  });

  it('shows what each copy alone would lose', async () => {
    stub({ 'r4303011157206680397': ORIGINAL, 's:14092347734530621658': APPLE_FORK });
    const parsed = JSON.parse((await call()).content[0].text);
    expect(parsed.bodyDiff.onlyInA).toEqual(['THE PARAGRAPH ONLY GMAIL HAS.']);
    expect(parsed.bodyDiff.onlyInB).toEqual(['THE SENTENCE ONLY APPLE HAS.']);
    expect(parsed.bodyDiff.sharedLineCount).toBe(4);
    expect(parsed.bodyDiff.neitherIsSuperset).toBe(true);
    expect(parsed.bodyDiff.note).toContain('NEITHER');
  });

  it('names the threading that would be lost by sending the fork', async () => {
    stub({ 'r4303011157206680397': ORIGINAL, 's:14092347734530621658': APPLE_FORK });
    const parsed = JSON.parse((await call()).content[0].text);
    expect(parsed.drafts.a).toMatchObject({ origin: 'api', rootsOwnThread: false, inReplyTo: '<coparent@mail.gmail.com>' });
    expect(parsed.drafts.b).toMatchObject({ origin: 'non-api', rootsOwnThread: true });
    expect(parsed.drafts.b.inReplyTo).toBeUndefined();
    expect(parsed.drafts.b.appleIdentitySignals).toEqual([
      'X-Universally-Unique-Identifier: 8F3C1B0A-1111-2222-3333-AABBCCDDEEFF',
      'X-Apple-Notify-Thread: yes',
    ]);
    expect(parsed.threadingDifferences.join(' ')).toContain('different threadIds');
    expect(parsed.threadingDifferences.join(' ')).toContain('reply headers');
  });

  it('confirms the pairing only with an Apple identity header plus real lineage', async () => {
    stub({ 'r4303011157206680397': ORIGINAL, 's:14092347734530621658': APPLE_FORK });
    const parsed = JSON.parse((await call()).content[0].text);
    expect(parsed.forkPairing.verdict).toBe('confirmed');
    expect(parsed.forkPairing.tier).toBe(2);
    expect(parsed.forkPairing.originalDraftId).toBe('r4303011157206680397');
    expect(parsed.forkPairing.candidateDraftId).toBe('s:14092347734530621658');
    expect(parsed.forkPairing.evidence.join(' ')).toContain('body line similarity');
  });

  // ---- HAZARD A: the test that matters most. ----
  it('returns "none" for two unrelated drafts that share every cheap signal', async () => {
    // Both non-API, both rooting their own thread, both Apple-authored, same
    // From, same subject, minutes apart — the live mailbox really does hold
    // deliberate [VERSION A]/[VERSION B] pairs like this. Only LINEAGE is
    // missing, and without it the answer must be "unrelated".
    const common = {
      threadId: 'self', internalDate: '1000',
      headers: [
        { name: 'From', value: 'chris@x.com' },
        { name: 'Subject', value: 'Re: August schedule' },
        { name: 'X-Universally-Unique-Identifier', value: 'AAAA-1111' },
      ],
    };
    const A = draftGetJson({ ...common, draftId: 's:aaa', messageId: 'self', body: '[VERSION A] I would prefer the 14th and a six oclock pickup.' });
    const B = draftGetJson({
      ...common, draftId: 's:bbb', messageId: 'self2', internalDate: '1180',
      headers: [...common.headers, { name: 'X-Apple-Notify-Thread', value: 'yes' }],
      body: '[VERSION B] Let us keep the current arrangement through September.',
    });
    stub({ 's:aaa': A, 's:bbb': B });
    const result = await harness.callTool('gog_gmail_drafts_diff', { draftIdA: 's:aaa', draftIdB: 's:bbb' });
    const parsed = JSON.parse(result.content[0].text);
    expect(parsed.forkPairing.verdict).toBe('none');
    expect(parsed.forkPairing.missing.join(' ')).toContain('no lineage signal');
    // Nothing in the payload may read as an assertion that one replaced the other.
    expect(result.content[0].text).not.toContain('replaced draft');
  });

  // The default shape of a co-parenting mailbox: two drafts replying into the
  // SAME co-parent message, about different things. Shared root, Apple
  // headers, newer, same From — everything but a link from one to the other.
  it('returns "none" for two independent replies to the same co-parent message', async () => {
    const handoff = draftGetJson({
      draftId: 'r4303011157206680397', messageId: 'm1', threadId: 't1', internalDate: '1000',
      headers: [
        { name: 'From', value: 'Chris Hall <chris@x.com>' },
        { name: 'Message-Id', value: '<orig@mail.gmail.com>' },
        { name: 'In-Reply-To', value: '<coparent-2026-05-01@mail.gmail.com>' },
        { name: 'References', value: '<coparent-2026-05-01@mail.gmail.com>' },
      ],
      body: 'Confirming the July handoff at six on the 14th.\nI will bring the booster seat.',
    });
    const orthodontist = draftGetJson({
      draftId: 's:14092347734530621658', messageId: 'm2', threadId: 't1', internalDate: '2000',
      headers: [
        { name: 'From', value: 'chris@x.com' },
        { name: 'Message-Id', value: '<9F3A@gmail.com>' },
        { name: 'In-Reply-To', value: '<coparent-2026-05-01@mail.gmail.com>' },
        { name: 'References', value: '<coparent-2026-05-01@mail.gmail.com>' },
        { name: 'X-Universally-Unique-Identifier', value: '9F3A' },
      ],
      body: 'The orthodontist invoice came to 240 dollars.\nI am splitting it per the parenting plan.',
    });
    stub({ 'r4303011157206680397': handoff, 's:14092347734530621658': orthodontist });
    const result = await call();
    const parsed = JSON.parse(result.content[0].text);
    expect(parsed.forkPairing.verdict).not.toBe('confirmed');
    expect(result.content[0].text).not.toContain('replaced draft');
    expect(parsed.forkPairing.evidence.join(' ')).toContain('CORROBORATING ONLY');
    expect(parsed.forkPairing.missing.join(' ')).toContain('no lineage signal');
    expect(parsed.forkPairing.bodyAgreement.similarity).toBe(0);
  });

  // Apple quotes the original on reply, so two unrelated replies into one
  // thread share a big identical block. It must not read as agreement.
  it('ignores the quoted block shared by two unrelated replies', async () => {
    const quote = Array.from({ length: 20 }, (_, i) => `> quoted line ${i}`).join('\n');
    const attribution = 'On 1 May 2026, at 09:14, Co Parent <co@x.com> wrote:';
    const mk = (id: string, msgId: string, date: string, body: string, extra: Array<{ name: string; value: string }>) => draftGetJson({
      draftId: id, messageId: msgId, threadId: msgId, internalDate: date,
      headers: [{ name: 'From', value: 'chris@x.com' }, ...extra],
      body: `${body}\n${attribution}\n${quote}`,
    });
    stub({
      r1: mk('r1', 'm1', '1000', 'Tuition is due on the 5th.\nI paid the deposit already.', []),
      's:2': mk('s:2', 'm2', '2000', 'The passport renewal needs both signatures.\nI booked the 3rd.', [{ name: 'X-Apple-Notify-Thread', value: 'yes' }]),
    });
    const parsed = JSON.parse((await harness.callTool('gog_gmail_drafts_diff', { draftIdA: 'r1', draftIdB: 's:2' })).content[0].text);
    expect(parsed.forkPairing.verdict).toBe('none');
    expect(parsed.forkPairing.bodyAgreement.similarity).toBe(0);
    expect(parsed.forkPairing.bodyAgreement.quotedLinesIgnored).toEqual({ original: 21, candidate: 21 });
    // The whole-body diff still shows the quoted block as shared — that is a
    // different question (what would be lost), and it stays honest.
    expect(parsed.bodyDiff.sharedLineCount).toBe(21);
  });

  it('downgrades to "candidate" when lineage exists but the candidate is not newer', async () => {
    const older = draftGetJson({
      draftId: 's:old', messageId: 'x1', threadId: 'x1', internalDate: '500',
      headers: [{ name: 'From', value: 'chris@x.com' }, { name: 'X-Apple-Notify-Thread', value: 'yes' }],
      body: 'Thanks for the note.\nI can do the 14th.\nPickup at six.\nBest, Chris',
    });
    stub({ 'r4303011157206680397': ORIGINAL, 's:old': older });
    const parsed = JSON.parse((await harness.callTool('gog_gmail_drafts_diff', { draftIdA: 'r4303011157206680397', draftIdB: 's:old' })).content[0].text);
    // Draft B is older, so it is treated as the ORIGINAL and A as the candidate.
    expect(parsed.forkPairing.originalDraftId).toBe('s:old');
    expect(parsed.forkPairing.candidateDraftId).toBe('r4303011157206680397');
    expect(parsed.forkPairing.verdict).toBe('candidate');
    expect(parsed.forkPairing.note).toContain('Unconfirmed');
  });

  it('reports identical bodies and no threading difference', async () => {
    const same = (id: string) => draftGetJson({
      draftId: id, messageId: 'same', threadId: 'thr', internalDate: '1000',
      headers: [{ name: 'From', value: 'chris@x.com' }, { name: 'In-Reply-To', value: '<z@y>' }],
      body: 'one\ntwo',
    });
    stub({ 'r1': same('r1'), 'r2': same('r2') });
    const parsed = JSON.parse((await harness.callTool('gog_gmail_drafts_diff', { draftIdA: 'r1', draftIdB: 'r2' })).content[0].text);
    expect(parsed.bodyDiff.note).toContain('identical');
    expect(parsed.threadingDifferences).toEqual(['No threading difference: the two drafts share a threadId and agree on whether they carry reply headers.']);
  });

  it('names a one-sided superset in each direction', async () => {
    const short = draftGetJson({ draftId: 'r1', messageId: 'm', threadId: 'm', internalDate: '1', headers: [], body: 'one\ntwo' });
    const long = draftGetJson({ draftId: 'r2', messageId: 'm', threadId: 'm', internalDate: '2', headers: [], body: 'one\ntwo\nthree' });
    stub({ 'r1': short, 'r2': long });
    expect(JSON.parse((await harness.callTool('gog_gmail_drafts_diff', { draftIdA: 'r1', draftIdB: 'r2' })).content[0].text).bodyDiff.note)
      .toContain('Draft B is a superset');
    stub({ 'r3': long, 'r4': short });
    expect(JSON.parse((await harness.callTool('gog_gmail_drafts_diff', { draftIdA: 'r3', draftIdB: 'r4' })).content[0].text).bodyDiff.note)
      .toContain('Draft A is a superset');
  });

  it('makes no containment claim when one draft’s body could not be read', async () => {
    const empty = JSON.stringify({
      draft: { id: 'r1', message: { id: 'm1', threadId: 'm1', internalDate: '1', payload: { mimeType: 'application/octet-stream', headers: [], body: {} } } },
    });
    const full = draftGetJson({ draftId: 'r2', messageId: 'm2', threadId: 'm2', internalDate: '2', headers: [], body: 'one\ntwo' });
    stub({ r1: empty, r2: full });
    const parsed = JSON.parse((await harness.callTool('gog_gmail_drafts_diff', { draftIdA: 'r1', draftIdB: 'r2' })).content[0].text);
    expect(parsed.bodyDiff.comparability).toBe('a-unreadable');
    expect(parsed.bodyDiff.supersetClaim).toBe('not-assessed');
    expect(parsed.bodyDiff.neitherIsSuperset).toBeNull();
    expect(parsed.bodyDiff.note).not.toMatch(/superset/i);
    expect(parsed.drafts.a.bodyLineCount).toBe(0);
  });

  it('caps the reported diff lines and says so', async () => {
    const many = (n: number, tag: string) => Array.from({ length: n }, (_, i) => `${tag}-${i}`).join('\n');
    stub({
      'r1': draftGetJson({ draftId: 'r1', messageId: 'm', threadId: 'm', internalDate: '1', headers: [], body: many(5, 'a') }),
      'r2': draftGetJson({ draftId: 'r2', messageId: 'm', threadId: 'm', internalDate: '2', headers: [], body: many(5, 'b') }),
    });
    const parsed = JSON.parse((await harness.callTool('gog_gmail_drafts_diff', { draftIdA: 'r1', draftIdB: 'r2', maxDiffLines: 2 })).content[0].text);
    expect(parsed.bodyDiff.onlyInA).toHaveLength(2);
    expect(parsed.bodyDiff.onlyInB).toHaveLength(2);
    expect(parsed.bodyDiff.truncated).toBe(true);
    expect(parsed.bodyDiff.note).toContain('truncated');
  });

  it('reports threading differences when one side has no threadId, in both directions', async () => {
    const noThread = JSON.stringify({
      draft: { id: 'x', message: { id: 'm1', internalDate: '1', payload: { mimeType: 'text/plain', headers: [], body: { data: b64('x') } } } },
    });
    const threaded = draftGetJson({
      draftId: 'r2', messageId: 'm2', threadId: 'thr', internalDate: '2',
      headers: [{ name: 'References', value: '<z@y>' }], body: 'y',
    });
    // A has no threadId and no reply headers; B has both.
    stub({ r1: noThread, r2: threaded });
    const first = JSON.parse((await harness.callTool('gog_gmail_drafts_diff', { draftIdA: 'r1', draftIdB: 'r2' })).content[0].text);
    expect(first.threadingDifferences[0]).toContain('((none) vs thr)');
    expect(first.threadingDifferences[1]).toContain('Draft r2 carries reply headers');
    expect(first.threadingDifferences[1]).toContain('draft r1 does not');
    // Mirror image: now it is B that has no threadId.
    stub({ r3: threaded, r4: noThread });
    const second = JSON.parse((await harness.callTool('gog_gmail_drafts_diff', { draftIdA: 'r3', draftIdB: 'r4' })).content[0].text);
    expect(second.threadingDifferences[0]).toContain('(thr vs (none))');
  });

  it('diagnoses a draft id that no longer resolves, spending only the calls it made', async () => {
    stub({ 'r4303011157206680397': ORIGINAL });
    const result = await call();
    expect(vi.mocked(lib.run).mock.calls).toHaveLength(2);
    expect(lib.diagnose).toHaveBeenCalled();
    expect(String(vi.mocked(lib.diagnose).mock.calls[0]![0])).toContain('s:14092347734530621658');
    expect(result.content[0].text).toBe('diagnosed');
  });

  it('errors clearly when either draft payload is unreadable', async () => {
    stub({ 'r4303011157206680397': 'not json', 's:14092347734530621658': APPLE_FORK });
    expect((await call()).content[0].text).toContain('r4303011157206680397');
    stub({ 'r4303011157206680397': ORIGINAL, 's:14092347734530621658': '{"draft":{}}' });
    expect((await call()).content[0].text).toContain('s:14092347734530621658');
  });
});

describe('gog_gmail_drafts_get', () => {
  it('format raw calls runOrDiagnose with draftId (the previous behaviour)', async () => {
    await harness.callTool('gog_gmail_drafts_get', { draftId: 'd1', format: 'raw' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'get', pos('d1'), '--use-indexed-attachment-ids=false'],
      { account: undefined },
    );
  });

  it('ignores a stale download and only reads the draft', async () => {
    await harness.callTool('gog_gmail_drafts_get', { draftId: 'd1', format: 'raw', download: true });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'get', pos('d1'), '--use-indexed-attachment-ids=false'],
      { account: undefined },
    );
  });
});

describe('gog_gmail_drafts_create', () => {
  it('passes the signature flags after from (gog >= 0.44)', async () => {
    await harness.callTool('gog_gmail_drafts_create', {
      subject: 'Hi', body: 'Hello', from: 'alias@x.com', signature: true, signatureFrom: 'alias@x.com',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'create', '--subject=Hi', '--body=Hello', '--from=alias@x.com', '--signature', '--signature-from=alias@x.com', '--auto-from-addressed-alias=false'],
      { account: undefined },
    );
  });

  // The draft-side tools never mutate the mailbox irreversibly on their own —
  // saving a draft is always reversible — so unlike gog_gmail_reply/send/
  // forward/autoreply they do not request MCP elicitation and write on the
  // first call.
  it('requires no confirmation — writes the draft on the first call', async () => {
    await harness.callTool('gog_gmail_drafts_create', { subject: 'Hi', body: 'Hello' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'create', '--subject=Hi', '--body=Hello', '--auto-from-addressed-alias=false'],
      { account: undefined },
    );
  });

  it('calls runOrDiagnose with minimal required flags', async () => {
    await harness.callTool('gog_gmail_drafts_create', {
      subject: 'Hi',
      body: 'Hello',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'create', '--subject=Hi', '--body=Hello', '--auto-from-addressed-alias=false'],
      { account: undefined },
    );
  });

  it('passes all flags including attachments', async () => {
    await harness.callTool('gog_gmail_drafts_create', {
      to: 'a@b.com,c@d.com',
      cc: 'cc@x.com',
      bcc: 'bcc@x.com',
      subject: 'Hi',
      body: 'Hello',
      bodyHtml: '<p>Hi</p>',
      replyToMessageId: 'm1',
      replyTo: 'rt@x.com',
      quote: true,
      attach: ['/tmp/a.pdf', '/tmp/b.pdf'],
      from: 'me@x.com',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      [
        'gmail', 'drafts', 'create',
        '--to=a@b.com,c@d.com',
        '--cc=cc@x.com',
        '--bcc=bcc@x.com',
        '--subject=Hi',
        '--body=Hello',
        '--body-html=<p>Hi</p>',
        '--reply-to-message-id=m1',
        '--reply-to=rt@x.com',
        '--quote',
        '--attach=/tmp/a.pdf',
        '--attach=/tmp/b.pdf',
        '--from=me@x.com', '--auto-from-addressed-alias=false'
      ],
      { account: undefined },
    );
  });

  // ==========================================================================
  // INLINE ATTACHMENT BYTES on drafts — the outbound half of the "no shared
  // filesystem" defect. `attach` paths resolve on the gog server and are
  // unreachable from a remote caller; attachInline carries the bytes instead.
  // ==========================================================================
  it('turns attachInline into repeatable --attach file args on drafts_create', async () => {
    const png = Buffer.from([0x89, 0x50, 0x4e, 0x47]).toString('base64');
    await harness.callTool('gog_gmail_drafts_create', {
      subject: 'Layouts',
      body: 'See attached',
      attachInline: [{ filename: 'pendant-layouts.png', contentBase64: png }],
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      [
        'gmail', 'drafts', 'create', '--subject=Layouts', '--body=See attached',
        { kind: 'file', flag: 'attach', contents: png, encoding: 'base64', filename: 'pendant-layouts.png' },
        '--auto-from-addressed-alias=false',
      ],
      { account: undefined },
    );
  });

  it('keeps attach paths and attachInline bytes side by side, in that order', async () => {
    const bytes = Buffer.from('hello').toString('base64');
    await harness.callTool('gog_gmail_drafts_create', {
      subject: 'S', body: 'B',
      attach: ['/tmp/on-server.pdf'],
      attachInline: [{ filename: 'from-client.txt', contentBase64: bytes }],
    });
    const args = vi.mocked(lib.runOrDiagnose).mock.calls[0][0];
    expect(args).toContain('--attach=/tmp/on-server.pdf');
    expect(args).toContainEqual({ kind: 'file', flag: 'attach', contents: bytes, encoding: 'base64', filename: 'from-client.txt' });
  });

  it('supports attachInline on drafts_update too', async () => {
    const bytes = Buffer.from('v2').toString('base64');
    await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'B',
      attachInline: [{ filename: 'revised.pdf', contentBase64: bytes }],
    });
    const args = vi.mocked(lib.runOrDiagnose).mock.calls[0][0];
    expect(args).toContainEqual({ kind: 'file', flag: 'attach', contents: bytes, encoding: 'base64', filename: 'revised.pdf' });
  });

  it('preserves a filename with spaces on the way to gog', async () => {
    await harness.callTool('gog_gmail_drafts_create', {
      subject: 'S', body: 'B',
      attachInline: [{ filename: 'Screenshot 2026-06-13 152500.png', contentBase64: Buffer.from('x').toString('base64') }],
    });
    const args = vi.mocked(lib.runOrDiagnose).mock.calls[0][0];
    expect(args.find((a) => typeof a !== 'string')).toMatchObject({ filename: 'Screenshot 2026-06-13 152500.png' });
  });

  it('rejects an invalid inline attachment without writing a draft', async () => {
    const res = await harness.callTool('gog_gmail_drafts_create', {
      subject: 'S', body: 'B',
      attachInline: [{ filename: '../escape.png', contentBase64: Buffer.from('x').toString('base64') }],
    });
    expect(res.isError).toBe(true);
    expect((res.content[0] as { text: string }).text).toMatch(/must be a bare filename, not a path/);
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
  });

  it('passes --body-html-file when bodyHtmlFile is supplied', async () => {
    await harness.callTool('gog_gmail_drafts_create', {
      subject: 'Hi',
      body: 'Hello',
      bodyHtmlFile: '/tmp/body.html',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'create', '--subject=Hi', '--body=Hello', '--body-html-file=/tmp/body.html', '--auto-from-addressed-alias=false'],
      { account: undefined },
    );
  });

  it('passes --reply-all when replyAll is set', async () => {
    await harness.callTool('gog_gmail_drafts_create', {
      subject: 'Re: Hi',
      body: 'Hello all',
      replyToThreadId: 't1',
      replyAll: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'create', '--subject=Re: Hi', '--body=Hello all', '--thread-id=t1', '--reply-all', '--auto-from-addressed-alias=false'],
      { account: undefined },
    );
  });

  it('skips recipient flags when omitRecipients is true, even if to/cc/bcc are supplied', async () => {
    await harness.callTool('gog_gmail_drafts_create', {
      to: 'a@b.com', cc: 'cc@x.com', bcc: 'bcc@x.com',
      subject: 'Hi', body: 'Hello', omitRecipients: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'create', '--subject=Hi', '--body=Hello', '--auto-from-addressed-alias=false'],
      { account: undefined },
    );
  });

  it('returnFull re-fetches and returns the full stored draft', async () => {
    vi.mocked(lib.runOrDiagnose)
      .mockResolvedValueOnce(rawTextResult('{"draftId":"d9","message":{"id":"m9"}}'))
      .mockResolvedValueOnce(rawTextResult('{"id":"d9","message":{"subject":"Hi","body":"Hello"}}'));
    const result = await harness.callTool('gog_gmail_drafts_create', {
      subject: 'Hi', body: 'Hello', returnFull: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenNthCalledWith(1,
      ['gmail', 'drafts', 'create', '--subject=Hi', '--body=Hello', '--auto-from-addressed-alias=false'], { account: undefined });
    expect(lib.runOrDiagnose).toHaveBeenNthCalledWith(2,
      ['gmail', 'drafts', 'get', pos('d9'), '--use-indexed-attachment-ids=false'], { account: undefined });
    expect(result.content[0].text).toContain('"subject":"Hi"');
  });

  it('returnFull does not push --return-full to the CLI', async () => {
    vi.mocked(lib.runOrDiagnose)
      .mockResolvedValueOnce(rawTextResult('{"draftId":"d9"}'))
      .mockResolvedValueOnce(rawTextResult('{}'));
    await harness.callTool('gog_gmail_drafts_create', { subject: 'Hi', body: 'Hello', returnFull: true });
    expect(vi.mocked(lib.runOrDiagnose).mock.calls[0]![0]).not.toContain('--return-full');
  });

  it('returnFull returns the write result when output is not parseable JSON', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult('not json'));
    const result = await harness.callTool('gog_gmail_drafts_create', { subject: 'Hi', body: 'Hello', returnFull: true });
    expect(lib.runOrDiagnose).toHaveBeenCalledTimes(1);
    expect(result.content[0].text).toBe('not json');
  });

  it('returnFull returns the write result when no draftId is present', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult('{"message":{"id":"m9"}}'));
    const result = await harness.callTool('gog_gmail_drafts_create', { subject: 'Hi', body: 'Hello', returnFull: true });
    expect(lib.runOrDiagnose).toHaveBeenCalledTimes(1);
    expect(result.content[0].text).toBe('{"message":{"id":"m9"}}');
  });
});

describe('gmail draft reply threading (native --thread-id)', () => {
  it('passes replyToThreadId straight through as --thread-id on create (no thread fetch)', async () => {
    await harness.callTool('gog_gmail_drafts_create', {
      subject: 'Re: roof', body: 'Sounds good', replyToThreadId: '19dffe06f9668b28', account: 'me@x.com',
    });
    // gog resolves the thread's latest-message headers itself — no extra fetch.
    expect(lib.runOrDiagnose).toHaveBeenCalledTimes(1);
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'create', '--subject=Re: roof', '--body=Sounds good', '--thread-id=19dffe06f9668b28', '--auto-from-addressed-alias=false'],
      { account: 'me@x.com' },
    );
  });

  it('passes replyToThreadId as --thread-id on update', async () => {
    await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'B', replyToThreadId: 't1',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'update', pos('d1'), '--subject=S', '--body=B', '--body-html=<p>B</p>', '--thread-id=t1', '--auto-from-addressed-alias=false'],
      { account: undefined },
    );
  });

  it('replyToMessageId wins when both ids are supplied (no --thread-id)', async () => {
    await harness.callTool('gog_gmail_drafts_create', {
      subject: 'S', body: 'B', replyToMessageId: 'mExplicit', replyToThreadId: 't1',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledTimes(1);
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'create', '--subject=S', '--body=B', '--reply-to-message-id=mExplicit', '--auto-from-addressed-alias=false'],
      { account: undefined },
    );
  });
});

describe('gog_gmail_drafts_update', () => {
  // gog >= 0.44 keeps an omitted To/Cc/Bcc and clears one passed empty, so an
  // explicit '' must reach gog rather than be dropped as falsy.
  it('forwards an explicitly empty to/cc/bcc so gog clears that field', async () => {
    await harness.callTool('gog_gmail_drafts_update', { draftId: 'd1', subject: 'S', body: 'B', to: 'a@b.com', cc: '', bcc: '' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'update', pos('d1'), '--to=a@b.com', '--cc=', '--bcc=', '--subject=S', '--body=B', '--body-html=<p>B</p>', '--auto-from-addressed-alias=false'],
      { account: undefined },
    );
  });

  it('passes signatureFile through after confining it', async () => {
    await harness.callTool('gog_gmail_drafts_update', { draftId: 'd1', subject: 'S', body: 'B', signatureFile: '/tmp/sig.html' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'update', pos('d1'), '--subject=S', '--body=B', '--body-html=<p>B</p>', '--signature-file=/tmp/sig.html', '--auto-from-addressed-alias=false'],
      { account: undefined },
    );
  });

  it('calls runOrDiagnose with draftId and updated fields', async () => {
    await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1',
      subject: 'New subject',
      body: 'New body',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'update', pos('d1'), '--subject=New subject', '--body=New body', '--body-html=<p>New body</p>', '--auto-from-addressed-alias=false'],
      { account: undefined },
    );
  });

  it('passes attachments as repeatable flags', async () => {
    await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1',
      subject: 'S',
      body: 'B',
      attach: ['/tmp/x.pdf'],
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'update', pos('d1'), '--subject=S', '--body=B', '--body-html=<p>B</p>', '--attach=/tmp/x.pdf', '--auto-from-addressed-alias=false'],
      { account: undefined },
    );
  });

  it('skips recipient flags when omitRecipients is true', async () => {
    await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', to: 'a@b.com', subject: 'S', body: 'B', omitRecipients: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'update', pos('d1'), '--subject=S', '--body=B', '--body-html=<p>B</p>', '--auto-from-addressed-alias=false'],
      { account: undefined },
    );
  });

  it('passes --clear-attachments when clearAttachments is true', async () => {
    await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'B', clearAttachments: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'update', pos('d1'), '--subject=S', '--body=B', '--body-html=<p>B</p>', '--auto-from-addressed-alias=false', '--clear-attachments'],
      { account: undefined },
    );
  });

  it('passes --clear-reply-context when clearReplyContext is true', async () => {
    await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'B', clearReplyContext: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'update', pos('d1'), '--subject=S', '--body=B', '--body-html=<p>B</p>', '--auto-from-addressed-alias=false', '--clear-reply-context'],
      { account: undefined },
    );
  });

  // A plain update carries no reply flags at all: gog preserves the draft's own
  // reply context and threadId. Passing a reply target here would re-anchor the
  // draft, so the wrapper must stay silent when the caller says nothing.
  it('sends no reply or thread flags when no reply target is supplied', async () => {
    await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'B',
    });
    const args = vi.mocked(lib.runOrDiagnose).mock.calls[0]?.[0] as string[];
    expect(args.some((a) => typeof a === 'string' && a.startsWith('--reply-to-message-id'))).toBe(false);
    expect(args.some((a) => typeof a === 'string' && a.startsWith('--thread-id'))).toBe(false);
    expect(args).not.toContain('--clear-reply-context');
  });

  it('combines clearAttachments and clearReplyContext', async () => {
    await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'B', clearAttachments: true, clearReplyContext: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'update', pos('d1'), '--subject=S', '--body=B', '--body-html=<p>B</p>',
        '--auto-from-addressed-alias=false', '--clear-attachments', '--clear-reply-context'],
      { account: undefined },
    );
  });

  it('returnFull re-fetches the draft by its known id', async () => {
    vi.mocked(lib.runOrDiagnose)
      .mockResolvedValueOnce(rawTextResult('{"draftId":"d1"}'))
      .mockResolvedValueOnce(rawTextResult('{"id":"d1","message":{"subject":"S"}}'));
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'B', returnFull: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenNthCalledWith(2,
      ['gmail', 'drafts', 'get', pos('d1'), '--use-indexed-attachment-ids=false'], { account: undefined });
    expect(result.content[0].text).toContain('"subject":"S"');
  });

  it('returnFull surfaces a failed update instead of re-fetching a stale draft', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult('Error: update failed'));
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'B', returnFull: true,
    });
    // write failed (non-JSON) → no re-fetch; the error is surfaced
    expect(lib.runOrDiagnose).toHaveBeenCalledTimes(1);
    expect(result.content[0].text).toBe('Error: update failed');
  });
});

describe('gog_gmail_drafts_delete', () => {
  it('calls runOrDiagnose with draftId', async () => {
    await harness.callTool('gog_gmail_drafts_delete', { draftId: 'd1' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'delete', pos('d1')],
      { account: undefined },
    );
  });

  it('appends --force when force is true', async () => {
    await harness.callTool('gog_gmail_drafts_delete', { draftId: 'd1', force: true });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'delete', pos('d1'), '--force'],
      { account: undefined },
    );
  });

  it('omits --force when force is false', async () => {
    await harness.callTool('gog_gmail_drafts_delete', { draftId: 'd1', force: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'delete', pos('d1')],
      { account: undefined },
    );
  });
});

describe('gog_gmail_drafts_send', () => {
  const b64url = (t: string) => Buffer.from(t, 'utf8').toString('base64url');
  const DRAFT = JSON.stringify({
    draft: {
      id: 'd1',
      message: {
        id: 'm1',
        payload: {
          mimeType: 'multipart/mixed',
          headers: [
            { name: 'To', value: 'Mallory <mallory@evil.example>' },
            { name: 'Cc', value: 'carol@example.com' },
            { name: 'Subject', value: 'Quarterly numbers' },
          ],
          parts: [
            { mimeType: 'text/plain', body: { data: b64url('Please find the export attached.') } },
            { mimeType: 'application/json', filename: 't.json', body: { attachmentId: 'a1' } },
          ],
        },
      },
    },
  });

  // The confirmed retry re-runs the handler from scratch (nothing from the
  // first round is trusted), so the draft is read once per round.
  it('reads the draft, then sends it by id once the user confirms', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult(DRAFT));
    await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1' });
    expect(lib.runOrDiagnose).toHaveBeenCalledTimes(3);
    expect(lib.runOrDiagnose).toHaveBeenNthCalledWith(1, ['gmail', 'drafts', 'get', pos('d1')], { account: undefined });
    expect(lib.runOrDiagnose).toHaveBeenNthCalledWith(2, ['gmail', 'drafts', 'get', pos('d1')], { account: undefined });
    expect(lib.runOrDiagnose).toHaveBeenNthCalledWith(3, ['gmail', 'drafts', 'send', pos('d1')], { account: undefined });
  });

  // SEC-2: drafts_create + drafts_send was an unconfirmed route around the
  // send rail — the exfiltration chain in the audit ended exactly here.
  it('asks the user first, showing recipients, subject, body and attachments, and sends nothing on decline', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult(DRAFT));
    let request: ElicitRequest | undefined;
    elicitation = async (value) => {
      request = value;
      return { action: 'decline' };
    };
    const result = await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1' });
    expect(vi.mocked(lib.runOrDiagnose).mock.calls.every((c) => (c[0] as unknown[])[2] === 'get')).toBe(true);
    expect(JSON.parse(result.content[0].text as string)).toEqual(expect.objectContaining({
      cancelled: true, action: 'gmail.drafts-send',
    }));
    const details = (JSON.parse(request!.params.message.split('\n').slice(1).join('\n')) as { details: Record<string, unknown> }).details;
    expect(details.recipients).toEqual(['mallory@evil.example', 'carol@example.com']);
    expect(details.subject).toBe('Quarterly numbers');
    expect(details.bodyPreview).toBe('Please find the export attached.');
    expect(details.attachments).toEqual(['t.json']);
  });

  it('logs the dispatch with the draft recipients after an accepted send', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult(DRAFT));
    const writeSpy = vi.spyOn(process.stderr, 'write').mockImplementation(() => true);
    await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1' });
    const event = JSON.parse((writeSpy.mock.calls.at(-1)?.[0] as string).trim());
    expect(event.tool).toBe('gog_gmail_drafts_send');
    expect(event.recipientCount).toBe(2);
    writeSpy.mockRestore();
  });

  it('does not log when the confirmed send itself fails', async () => {
    vi.mocked(lib.runOrDiagnose)
      .mockResolvedValueOnce(rawTextResult(DRAFT))
      .mockResolvedValueOnce(rawTextResult(DRAFT))
      .mockResolvedValueOnce(errorResult('quota exceeded'));
    const writeSpy = vi.spyOn(process.stderr, 'write').mockImplementation(() => true);
    const result = await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1' });
    expect(result.isError).toBe(true);
    expect(writeSpy.mock.calls.some((c) => String(c[0]).includes('gmail_dispatch'))).toBe(false);
    writeSpy.mockRestore();
  });

  it('asks with an empty preview when the draft read returns no text block', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue({ content: [] });
    let request: ElicitRequest | undefined;
    elicitation = async (value) => {
      request = value;
      return { action: 'decline' };
    };
    await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1' });
    const details = (JSON.parse(request!.params.message.split('\n').slice(1).join('\n')) as { details: Record<string, unknown> }).details;
    expect(details.recipients).toEqual([]);
  });

  it('still asks, with only the id, when the stored draft cannot be read', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult('not json'));
    let request: ElicitRequest | undefined;
    elicitation = async (value) => {
      request = value;
      return { action: 'decline' };
    };
    await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1' });
    const details = (JSON.parse(request!.params.message.split('\n').slice(1).join('\n')) as { details: Record<string, unknown> }).details;
    expect(details.draftId).toBe('d1');
    expect(details.recipients).toEqual([]);
    expect(vi.mocked(lib.runOrDiagnose).mock.calls.some((c) => (c[0] as unknown[])[2] === 'send')).toBe(false);
  });
});

describe('gog_gmail_forward', () => {
  it('appends the signature flags (gog >= 0.44)', async () => {
    await harness.callTool('gog_gmail_forward', { messageId: 'm1', to: 'a@b.com', note: 'FYI', signature: true });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'forward', pos('m1'), '--to=a@b.com', '--note=FYI', '--signature'],
      { account: undefined },
    );
  });

  it('calls runOrDiagnose with messageId and required --to', async () => {
    await harness.callTool('gog_gmail_forward', { messageId: 'm1', to: 'a@b.com' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'forward', pos('m1'), '--to=a@b.com'],
      { account: undefined },
    );
  });

  it('passes all forward flags', async () => {
    await harness.callTool('gog_gmail_forward', {
      messageId: 'm1',
      to: 'a@b.com',
      cc: 'cc@x.com',
      bcc: 'bcc@x.com',
      note: 'FYI',
      from: 'me@x.com',
      skipAttachments: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      [
        'gmail', 'forward', pos('m1'),
        '--to=a@b.com',
        '--cc=cc@x.com',
        '--bcc=bcc@x.com',
        '--note=FYI',
        '--from=me@x.com',
        '--skip-attachments',
      ],
      { account: undefined },
    );
  });

  it('passes an HTML note beside the plain one (gog >= 0.46)', async () => {
    await harness.callTool('gog_gmail_forward', { messageId: 'm1', to: 'a@b.com', note: 'FYI', noteHtml: '<b>FYI</b>' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'forward', pos('m1'), '--to=a@b.com', '--note=FYI', '--note-html=<b>FYI</b>'],
      { account: undefined },
    );
  });

  it('delivers a large HTML note as a --note-html-file temp file', async () => {
    const noteHtml = `<p>${'x'.repeat(lib.PAYLOAD_INLINE_MAX)}</p>`;
    await harness.callTool('gog_gmail_forward', { messageId: 'm1', to: 'a@b.com', noteHtml });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'forward', pos('m1'), '--to=a@b.com', { kind: 'file', flag: 'note-html-file', contents: noteHtml, ext: 'html' }],
      { account: undefined },
    );
  });

  it('previews an HTML-only note in the prompt', async () => {
    let request: ElicitRequest | undefined;
    elicitation = async (value) => {
      request = value;
      return { action: 'decline' };
    };
    await harness.callTool('gog_gmail_forward', { messageId: 'm1', to: 'a@b.com', noteHtml: '<b>FYI</b>' });
    const details = (JSON.parse(request!.params.message.split('\n').slice(1).join('\n')) as { details: Record<string, unknown> }).details;
    expect(details.notePreview).toBe('<b>FYI</b>');
    expect(details.noteLength).toBe(10);
  });

  it('omits --skip-attachments when false', async () => {
    await harness.callTool('gog_gmail_forward', {
      messageId: 'm1', to: 'a@b.com', skipAttachments: false,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'forward', pos('m1'), '--to=a@b.com'],
      { account: undefined },
    );
  });

  // ==========================================================================
  // THE CONFIRMATION GATE. The MCP host owns the user interaction; the tool
  // supplies the review details through input_required and only dispatches
  // after an accepted elicitation response.
  // ==========================================================================
  it('elicits the recipients and sends nothing when the user declines', async () => {
    let request: ElicitRequest | undefined;
    elicitation = async (value) => {
      request = value;
      return { action: 'decline' };
    };
    const result = await harness.callTool('gog_gmail_forward', { messageId: 'm1', to: 'a@b.com, b@c.com' });
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
    expect(request?.params.message).toContain('a@b.com');
    expect(request?.params.message).toContain('b@c.com');
    expect(JSON.parse(result.content[0].text as string)).toEqual(expect.objectContaining({
      confirmed: false,
      cancelled: true,
      action: 'gmail.forward',
    }));
  });

  it('shows the forward note itself in the prompt (SEC-5)', async () => {
    let request: ElicitRequest | undefined;
    elicitation = async (value) => {
      request = value;
      return { action: 'decline' };
    };
    await harness.callTool('gog_gmail_forward', { messageId: 'm1', to: 'a@b.com', note: 'FYI see below' });
    const details = (JSON.parse(request!.params.message.split('\n').slice(1).join('\n')) as { details: Record<string, unknown> }).details;
    expect(details.notePreview).toBe('FYI see below');
    expect(details.attachmentsIncluded).toBe(true);
  });

  it('shows an HTML note beside a plain one in the prompt, so neither is sent unseen', async () => {
    let request: ElicitRequest | undefined;
    elicitation = async (value) => {
      request = value;
      return { action: 'decline' };
    };
    await harness.callTool('gog_gmail_forward', { messageId: 'm1', to: 'a@b.com', note: 'FYI', noteHtml: '<b>Different</b>' });
    const details = (JSON.parse(request!.params.message.split('\n').slice(1).join('\n')) as { details: Record<string, unknown> }).details;
    expect(details.notePreview).toBe('FYI');
    expect(details.noteHtmlPreview).toBe('<b>Different</b>');
    expect(details.noteHtmlLength).toBe(16);
  });

  it('omits the HTML note fields from the prompt when there is no HTML note', async () => {
    let request: ElicitRequest | undefined;
    elicitation = async (value) => {
      request = value;
      return { action: 'decline' };
    };
    await harness.callTool('gog_gmail_forward', { messageId: 'm1', to: 'a@b.com', note: 'FYI' });
    const details = (JSON.parse(request!.params.message.split('\n').slice(1).join('\n')) as { details: Record<string, unknown> }).details;
    expect(details).not.toHaveProperty('noteHtmlPreview');
  });

  it('sends nothing when the user accepts but leaves confirmation false', async () => {
    elicitation = async () => ({ action: 'accept', content: { confirmed: false } });
    const result = await harness.callTool('gog_gmail_forward', { messageId: 'm1', to: 'a@b.com' });
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
    expect(JSON.parse(result.content[0].text as string).cancelled).toBe(true);
  });

  it('logs a gmail_dispatch event with the recipients after an accepted send', async () => {
    const writeSpy = vi.spyOn(process.stderr, 'write').mockImplementation(() => true);
    await harness.callTool('gog_gmail_forward', { messageId: 'm1', to: 'a@b.com' });
    const event = JSON.parse((writeSpy.mock.calls.at(-1)?.[0] as string).trim());
    expect(event.event).toBe('gmail_dispatch');
    expect(event.tool).toBe('gog_gmail_forward');
    expect(event.recipientCount).toBe(1);
    writeSpy.mockRestore();
  });

  it('does not log when the accepted send fails', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(errorResult('boom'));
    const writeSpy = vi.spyOn(process.stderr, 'write').mockImplementation(() => true);
    await harness.callTool('gog_gmail_forward', { messageId: 'm1', to: 'a@b.com' });
    expect(writeSpy).not.toHaveBeenCalled();
    writeSpy.mockRestore();
  });
});

// gog 0.36.0 (openclaw/gogcli#977) added the draft-side twins of reply /
// reply-all / forward. The point of these tests is the SUBCOMMAND: the flag
// handling is the send path's, shared verbatim, and a copy of it here would
// only re-assert what the reply tests above already pin. What is new — and what
// a regression would silently break — is that these route to `drafts <verb>`
// and therefore never send.
describe('gog_gmail_drafts_reply', () => {
  // No confirmation gate here — it reuses replySchema verbatim (not the
  // send-side's sendReplySchema), and staging a draft is reversible.
  it('requires no confirmation, unlike gog_gmail_reply', async () => {
    await harness.callTool('gog_gmail_drafts_reply', { messageId: 'm1', body: 'Thanks' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'reply', pos('m1'), '--body=Thanks', '--auto-from-addressed-alias=false'],
      { account: undefined },
    );
  });

  it('routes to gmail drafts reply, not the sending reply', async () => {
    await harness.callTool('gog_gmail_drafts_reply', { messageId: 'm1', body: 'Thanks' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'reply', pos('m1'), '--body=Thanks', '--auto-from-addressed-alias=false'],
      { account: undefined },
    );
  });

  it('passes the shared reply flag set through unchanged', async () => {
    await harness.callTool('gog_gmail_drafts_reply', {
      messageId: 'm1',
      body: 'Hi',
      to: ['a@b.com'],
      cc: ['cc@x.com'],
      remove: ['old@x.com'],
      subject: 'New subject',
      noQuote: true,
      attach: ['/tmp/a.pdf'],
      from: 'me@x.com',
      signature: true,
      account: 'me@gmail.com',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      [
        'gmail', 'drafts', 'reply', pos('m1'),
        '--body=Hi',
        '--to=a@b.com',
        '--cc=cc@x.com',
        '--remove=old@x.com',
        '--subject=New subject',
        '--no-quote',
        '--attach=/tmp/a.pdf',
        '--from=me@x.com',
        '--signature',
        '--auto-from-addressed-alias=false',
      ],
      { account: 'me@gmail.com' },
    );
  });

  it('returnFull re-fetches the saved draft and never reaches the CLI as a flag', async () => {
    vi.mocked(lib.runOrDiagnose)
      .mockResolvedValueOnce(rawTextResult('{"draftId":"d9"}'))
      .mockResolvedValueOnce(rawTextResult('{"id":"d9","message":{"subject":"Re: Hi"}}'));
    const result = await harness.callTool('gog_gmail_drafts_reply', {
      messageId: 'm1', body: 'Hi', returnFull: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenNthCalledWith(1,
      ['gmail', 'drafts', 'reply', pos('m1'), '--body=Hi', '--auto-from-addressed-alias=false'], { account: undefined });
    expect(lib.runOrDiagnose).toHaveBeenNthCalledWith(2,
      ['gmail', 'drafts', 'get', pos('d9'), '--use-indexed-attachment-ids=false'], { account: undefined });
    expect(result.content[0].text).toContain('"subject":"Re: Hi"');
  });
});

describe('gog_gmail_drafts_reply_all', () => {
  it('requires no confirmation, unlike gog_gmail_reply_all', async () => {
    await harness.callTool('gog_gmail_drafts_reply_all', { messageId: 'm1', body: 'Thanks all' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'reply-all', pos('m1'), '--body=Thanks all', '--auto-from-addressed-alias=false'],
      { account: undefined },
    );
  });

  it('routes to gmail drafts reply-all', async () => {
    await harness.callTool('gog_gmail_drafts_reply_all', { messageId: 'm1', body: 'Thanks all' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'reply-all', pos('m1'), '--body=Thanks all', '--auto-from-addressed-alias=false'],
      { account: undefined },
    );
  });

  it('carries repeatable recipient removals onto the draft', async () => {
    await harness.callTool('gog_gmail_drafts_reply_all', {
      messageId: 'm1', body: 'Hi', remove: ['drop@y.com', 'also@y.com'],
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      [
        'gmail', 'drafts', 'reply-all', pos('m1'),
        '--body=Hi',
        '--remove=drop@y.com',
        '--remove=also@y.com',
        '--auto-from-addressed-alias=false',
      ],
      { account: undefined },
    );
  });
});

describe('gog_gmail_drafts_forward', () => {
  it('appends the signature flags (gog >= 0.44)', async () => {
    await harness.callTool('gog_gmail_drafts_forward', { messageId: 'm1', signatureFrom: 'alias@x.com' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'forward', pos('m1'), '--signature-from=alias@x.com'],
      { account: undefined },
    );
  });

  it('requires no confirmation, unlike gog_gmail_forward', async () => {
    await harness.callTool('gog_gmail_drafts_forward', { messageId: 'm1', to: 'a@b.com' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'forward', pos('m1'), '--to=a@b.com'],
      { account: undefined },
    );
  });

  it('passes an HTML note (gog >= 0.46)', async () => {
    await harness.callTool('gog_gmail_drafts_forward', { messageId: 'm1', noteHtml: '<i>see below</i>' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'forward', pos('m1'), '--note-html=<i>see below</i>'],
      { account: undefined },
    );
  });

  it('omits --to entirely when no recipients are given', async () => {
    await harness.callTool('gog_gmail_drafts_forward', { messageId: 'm1' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'forward', pos('m1')],
      { account: undefined },
    );
  });

  it('passes every forward flag', async () => {
    await harness.callTool('gog_gmail_drafts_forward', {
      messageId: 'm1',
      to: 'a@b.com,c@d.com',
      cc: 'cc@x.com',
      bcc: 'bcc@x.com',
      note: 'FYI',
      from: 'me@x.com',
      skipAttachments: true,
      account: 'me@gmail.com',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      [
        'gmail', 'drafts', 'forward', pos('m1'),
        '--to=a@b.com,c@d.com',
        '--cc=cc@x.com',
        '--bcc=bcc@x.com',
        '--note=FYI',
        '--from=me@x.com',
        '--skip-attachments',
      ],
      { account: 'me@gmail.com' },
    );
  });

  it('returnFull re-fetches the saved forward draft', async () => {
    vi.mocked(lib.runOrDiagnose)
      .mockResolvedValueOnce(rawTextResult('{"draftId":"d7"}'))
      .mockResolvedValueOnce(rawTextResult('{"id":"d7","message":{"subject":"Fwd: Hi"}}'));
    const result = await harness.callTool('gog_gmail_drafts_forward', { messageId: 'm1', returnFull: true });
    expect(lib.runOrDiagnose).toHaveBeenNthCalledWith(2,
      ['gmail', 'drafts', 'get', pos('d7'), '--use-indexed-attachment-ids=false'], { account: undefined });
    expect(result.content[0].text).toContain('"subject":"Fwd: Hi"');
  });
});

describe('gog_gmail_autoreply', () => {
  it('calls runOrDiagnose with query and --body', async () => {
    await harness.callTool('gog_gmail_autoreply', { query: 'is:unread', body: 'Thanks' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'autoreply', pos('is:unread'), '--body=Thanks'],
      { account: undefined },
    );
  });

  it('passes all autoreply flags', async () => {
    await harness.callTool('gog_gmail_autoreply', {
      query: 'is:unread',
      max: 50,
      subject: 'Re: out of office',
      body: 'I am out',
      bodyHtml: '<p>OOO</p>',
      from: 'me@x.com',
      replyTo: 'rt@x.com',
      label: 'OOO-Replied',
      archive: true,
      markRead: true,
      skipBulk: true,
      allowSelf: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      [
        'gmail', 'autoreply', pos('is:unread'),
        '--max=50',
        '--subject=Re: out of office',
        '--body=I am out',
        '--body-html=<p>OOO</p>',
        '--from=me@x.com',
        '--reply-to=rt@x.com',
        '--label=OOO-Replied',
        '--archive',
        '--mark-read',
        '--skip-bulk',
        '--allow-self',
      ],
      { account: undefined },
    );
  });

  it('omits boolean flags when false', async () => {
    await harness.callTool('gog_gmail_autoreply', {
      query: 'is:unread',
      body: 'Thanks',
      archive: false,
      markRead: false,
      skipBulk: false,
      allowSelf: false,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'autoreply', pos('is:unread'), '--body=Thanks'],
      { account: undefined },
    );
  });

  it('supports HTML-only body (no plain --body)', async () => {
    await harness.callTool('gog_gmail_autoreply', { query: 'is:unread', bodyHtml: '<p>Hi</p>' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'autoreply', pos('is:unread'), '--body-html=<p>Hi</p>'],
      { account: undefined },
    );
  });

  // ==========================================================================
  // THE CONFIRMATION GATE. autoreply is the highest-blast-radius tool here — it
  // dispatches across every message a query matches, not just one — so its
  // prompt runs a bounded search instead of just echoing the query back.
  // ==========================================================================
  const autoreplyPrompt = async (
    args: Record<string, unknown>,
    searchResult = rawTextResult('{}'),
  ) => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(searchResult);
    let request: ElicitRequest | undefined;
    elicitation = async (value) => {
      request = value;
      return { action: 'decline' };
    };
    const result = await harness.callTool('gog_gmail_autoreply', { query: 'is:unread', ...args });
    return {
      result,
      details: (JSON.parse(request?.params.message.split('\n').slice(1).join('\n') ?? '{}') as {
        details?: Record<string, unknown>;
      }).details ?? {},
    };
  };

  it('sends nothing and elicits the matching senders when the user declines', async () => {
    const { result, details } = await autoreplyPrompt({ body: 'Thanks' }, rawTextResult(JSON.stringify({
      threads: [{ from: 'Alice <alice@example.com>' }, { from: 'Bob <bob@example.com>' }],
    })));
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['gmail', 'search', pos('is:unread'), '--max=20'], { account: undefined });
    expect(JSON.parse(result.content[0].text as string).cancelled).toBe(true);
    expect(details.matchCount).toBe(2);
    expect(details.sampleSenders).toEqual(['alice@example.com', 'bob@example.com']);
  });

  it('shows the reply text itself in the prompt (SEC-5)', async () => {
    const { details } = await autoreplyPrompt({ body: 'Out until Monday' });
    expect(details.bodyPreview).toBe('Out until Monday');
  });

  it('measures bodyLength from bodyHtml when no plain body is given', async () => {
    const { details } = await autoreplyPrompt({ bodyHtml: '<p>Hi</p>' });
    expect(details.bodyLength).toBe('<p>Hi</p>'.length);
  });

  it('measures bodyLength as zero when neither body nor bodyHtml is given', async () => {
    const { details } = await autoreplyPrompt({});
    expect(details.bodyLength).toBe(0);
  });

  it('treats a valid-JSON search response with no threads array as zero matches', async () => {
    const { details } = await autoreplyPrompt({ body: 'Thanks' });
    expect(details.matchCount).toBe(0);
  });

  it('treats a non-text search result as zero matches', async () => {
    const { details } = await autoreplyPrompt(
      { body: 'Thanks' },
      { content: [{ type: 'image', data: Buffer.from('x').toString('base64'), mimeType: 'image/png' }] },
    );
    expect(details.matchCount).toBe(0);
  });

  it('treats an unparseable search response as zero matches rather than crashing', async () => {
    const { details } = await autoreplyPrompt({ body: 'Thanks' }, rawTextResult('not json at all'));
    expect(details.matchCount).toBe(0);
    expect(details.sampleSenders).toEqual([]);
  });

  it('surfaces a search failure at preview time instead of a false-looking preview', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(errorResult('search failed'));
    const result = await harness.callTool('gog_gmail_autoreply', { query: 'is:unread', body: 'Thanks' });
    expect(result.isError).toBe(true);
  });

  it('logs a gmail_dispatch event with the actually-replied-to senders after an accepted send', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult(JSON.stringify({
      autoReply: {
        results: [
          { action: 'replied', messageId: 'm1', replyTo: 'alice@example.com' },
          { action: 'skipped', messageId: 'm2', reason: 'no_reply_recipient' },
        ],
      },
    })));
    const writeSpy = vi.spyOn(process.stderr, 'write').mockImplementation(() => true);
    await harness.callTool('gog_gmail_autoreply', { query: 'is:unread', body: 'Thanks' });
    const event = JSON.parse((writeSpy.mock.calls.at(-1)?.[0] as string).trim());
    expect(event.tool).toBe('gog_gmail_autoreply');
    expect(event.recipientCount).toBe(1);
    writeSpy.mockRestore();
  });

  it('does not log when the accepted autoreply itself fails', async () => {
    vi.mocked(lib.runOrDiagnose)
      .mockResolvedValueOnce(rawTextResult('{}'))
      .mockResolvedValueOnce(rawTextResult('{}'))
      .mockResolvedValueOnce(errorResult('boom'));
    const writeSpy = vi.spyOn(process.stderr, 'write').mockImplementation(() => true);
    await harness.callTool('gog_gmail_autoreply', { query: 'is:unread', body: 'Thanks' });
    expect(writeSpy).not.toHaveBeenCalled();
    writeSpy.mockRestore();
  });

  it('logs zero recipients for a non-text send response rather than crashing', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue({ content: [{ type: 'image', data: Buffer.from('x').toString('base64'), mimeType: 'image/png' }] });
    const writeSpy = vi.spyOn(process.stderr, 'write').mockImplementation(() => true);
    await harness.callTool('gog_gmail_autoreply', { query: 'is:unread', body: 'Thanks' });
    const event = JSON.parse((writeSpy.mock.calls.at(-1)?.[0] as string).trim());
    expect(event.recipientCount).toBe(0);
    writeSpy.mockRestore();
  });

  it('logs zero recipients rather than crashing on an unparseable send response', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult('not json at all'));
    const writeSpy = vi.spyOn(process.stderr, 'write').mockImplementation(() => true);
    await harness.callTool('gog_gmail_autoreply', { query: 'is:unread', body: 'Thanks' });
    const event = JSON.parse((writeSpy.mock.calls.at(-1)?.[0] as string).trim());
    expect(event.recipientCount).toBe(0);
    writeSpy.mockRestore();
  });
});

describe('gog_gmail_messages_search', () => {
  it('passes --include-recipients and --sanitize-content (gog >= 0.44)', async () => {
    await harness.callTool('gog_gmail_messages_search', { query: 'x', includeRecipients: true, sanitizeContent: true });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'messages', 'search', pos('x'), '--include-recipients', '--sanitize-content', '--include-attachments=false', '--use-indexed-attachment-ids=false'],
      { account: undefined },
    );
  });

  it('calls runOrDiagnose with just the query', async () => {
    await harness.callTool('gog_gmail_messages_search', { query: 'from:alice' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'messages', 'search', pos('from:alice'), '--include-attachments=false', '--use-indexed-attachment-ids=false'],
      { account: undefined },
    );
  });

  it('passes all flags when provided', async () => {
    await harness.callTool('gog_gmail_messages_search', {
      query: 'is:unread',
      max: 10,
      pageToken: 'tok',
      all: true,
      includeBody: true,
      full: true,
      bodyFormat: 'html',
      account: 'me@x.com',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'messages', 'search', pos('is:unread'), '--max=10', '--all', '--include-body', '--full', '--body-format=html', '--include-attachments=false', '--use-indexed-attachment-ids=false', '--page=tok'],
      { account: 'me@x.com' },
    );
  });

  it('omits flags when false/absent', async () => {
    await harness.callTool('gog_gmail_messages_search', { query: 'x', all: false, includeBody: false, full: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'messages', 'search', pos('x'), '--include-attachments=false', '--use-indexed-attachment-ids=false'],
      { account: undefined },
    );
  });
});

describe('page-cursor contract', () => {
  it('never steers a caller to the deprecated `page` alias', async () => {
    const { tools } = await harness.client.listTools();
    const offenders = (tools as { name: string; description?: string }[])
      .filter((t) => /`page`|\bas page\b/i.test(t.description ?? ''))
      .map((t) => t.name);
    expect(offenders).toEqual([]);
  });

  it('offers the alias wherever pageToken is accepted', async () => {
    const { tools } = await harness.client.listTools();
    const withCursor = (tools as { name: string; inputSchema?: { properties?: Record<string, unknown> } }[])
      .filter((t) => 'pageToken' in (t.inputSchema?.properties ?? {}));
    expect(withCursor.length).toBeGreaterThan(0);
    expect(withCursor.filter((t) => !('page' in (t.inputSchema?.properties ?? {}))).map((t) => t.name)).toEqual([]);
  });
});

describe('gog_gmail_messages_search — the page cursor reaches the API', () => {
  it('threads a pageToken through to the gog invocation', async () => {
    await harness.callTool('gog_gmail_messages_search', { query: 'x', pageToken: 'CURSOR' });
    const args = vi.mocked(lib.runOrDiagnose).mock.calls[0][0] as string[];
    expect(args).toContain('--page=CURSOR');
  });

  it('still accepts the deprecated page alias, and pageToken wins over it', async () => {
    await harness.callTool('gog_gmail_messages_search', { query: 'x', page: 'OLD' });
    expect(vi.mocked(lib.runOrDiagnose).mock.calls[0][0]).toContain('--page=OLD');
    vi.mocked(lib.runOrDiagnose).mockClear();
    await harness.callTool('gog_gmail_messages_search', { query: 'x', pageToken: 'NEW', page: 'OLD' });
    expect(vi.mocked(lib.runOrDiagnose).mock.calls[0][0]).toContain('--page=NEW');
  });

  it('walks and merges pages under maxPages', async () => {
    vi.mocked(lib.runOrDiagnose)
      .mockResolvedValueOnce(rawTextResult(JSON.stringify({ messages: [{ id: 'a' }], nextPageToken: 'T1' })))
      .mockResolvedValueOnce(rawTextResult(JSON.stringify({ messages: [{ id: 'b' }] })));
    const result = await harness.callTool('gog_gmail_messages_search', { query: 'x', maxPages: 4 });
    const out = JSON.parse(result.content[0].text as string);
    expect(out.messages.map((m: { id: string }) => m.id)).toEqual(['a', 'b']);
    expect(out).not.toHaveProperty('nextPageToken');
    expect(vi.mocked(lib.runOrDiagnose).mock.calls[1][0]).toContain('--page=T1');
  });
});

describe('gog_gmail_messages_search — result finalization', () => {
  it('sorts results newest-first', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult(JSON.stringify({
      messages: [
        { id: 'old', internalDateIso: '2026-08-01T09:00:00-04:00' },
        { id: 'new', internalDateIso: '2026-08-12T12:36:00-04:00' },
        { id: 'mid', internalDateIso: '2026-08-05T09:00:00-04:00' },
      ],
      nextPageToken: '',
    })));
    const result = await harness.callTool('gog_gmail_messages_search', { query: 'x' });
    const out = JSON.parse(result.content[0].text as string);
    expect(out.messages.map((m: { id: string }) => m.id)).toEqual(['new', 'mid', 'old']);
    expect(out).not.toHaveProperty('truncated');
  });

  it('marks a capped result set truncated and counts the real total', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult(JSON.stringify({
      messages: [{ id: 'a' }, { id: 'b' }],
      nextPageToken: 'tok',
    })));
    vi.mocked(runner.run).mockResolvedValue(JSON.stringify({
      messages: [{ id: 'a' }, { id: 'b' }, { id: 'c' }, { id: 'd' }, { id: 'e' }],
    }));
    const result = await harness.callTool('gog_gmail_messages_search', { query: 'x', max: 2 });
    const out = JSON.parse(result.content[0].text as string);
    expect(out.truncated).toBe(true);
    expect(out.returned).toBe(2);
    expect(out.totalMatches).toBe(5);
    expect(out.warning).toBe(
      'INCOMPLETE RESULT SET: returned 2 of 5 matches. Do not report an absence of results ' +
      'based on this response. Page with nextPageToken or narrow the query.',
    );
    expect(runner.run).toHaveBeenCalledWith(
      ['api', 'call', 'gmail', 'v1', pos('users.messages.list'),
        '--params={"userId":"me","q":"x","maxResults":500,"fields":"messages/id,nextPageToken"}'],
      { account: undefined },
    );
  });

  it('leaves output it does not recognise untouched', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult('No results'));
    const result = await harness.callTool('gog_gmail_messages_search', { query: 'x' });
    expect(result.content[0].text).toBe('No results');
  });
});

describe('gog_gmail_labels_style', () => {
  it('calls runOrDiagnose with just the label', async () => {
    await harness.callTool('gog_gmail_labels_style', { labelIdOrName: 'Work' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'labels', 'style', pos('Work')],
      { account: undefined },
    );
  });

  it('passes all style flags when provided', async () => {
    await harness.callTool('gog_gmail_labels_style', {
      labelIdOrName: 'Work',
      backgroundColor: '#000000',
      textColor: '#ffffff',
      labelListVisibility: 'labelHide',
      messageListVisibility: 'hide',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'labels', 'style', pos('Work'), '--background-color=#000000', '--text-color=#ffffff', '--label-list-visibility=labelHide', '--message-list-visibility=hide'],
      { account: undefined },
    );
  });
});

describe('gog_gmail_vacation_get', () => {
  it('calls runOrDiagnose', async () => {
    await harness.callTool('gog_gmail_vacation_get', { account: 'me@x.com' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'vacation', 'get'],
      { account: 'me@x.com' },
    );
  });
});

describe('gog_gmail_vacation_update', () => {
  it('calls runOrDiagnose with no flags', async () => {
    await harness.callTool('gog_gmail_vacation_update', {});
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'vacation', 'update'],
      { account: undefined },
    );
  });

  it('enables with subject/body/start/end and scoping', async () => {
    await harness.callTool('gog_gmail_vacation_update', {
      enable: true,
      subject: 'Away',
      body: '<p>OOO</p>',
      start: '2024-12-20T00:00:00Z',
      end: '2024-12-31T23:59:59Z',
      contactsOnly: true,
      domainOnly: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'vacation', 'update', '--enable', '--subject=Away', '--body=<p>OOO</p>', '--start=2024-12-20T00:00:00Z', '--end=2024-12-31T23:59:59Z', '--contacts-only', '--domain-only'],
      { account: undefined },
    );
  });

  it('disables the responder', async () => {
    await harness.callTool('gog_gmail_vacation_update', { disable: true, enable: false, contactsOnly: false, domainOnly: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'vacation', 'update', '--disable'],
      { account: undefined },
    );
  });
});

describe('gog_gmail_filters_list', () => {
  it('calls runOrDiagnose', async () => {
    await harness.callTool('gog_gmail_filters_list', {});
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'filters', 'list'],
      { account: undefined },
    );
  });
});

describe('gog_gmail_filters_get', () => {
  it('calls runOrDiagnose with the filter ID', async () => {
    await harness.callTool('gog_gmail_filters_get', { filterId: 'f1' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'filters', 'get', pos('f1')],
      { account: undefined },
    );
  });
});

describe('gog_gmail_filters_create — forwarding needs confirmation', () => {
  // SEC-2: a forward action sends every FUTURE matching message elsewhere.
  it('asks before creating a forwarding filter and creates nothing on decline', async () => {
    let request: ElicitRequest | undefined;
    elicitation = async (value) => {
      request = value;
      return { action: 'decline' };
    };
    const result = await harness.callTool('gog_gmail_filters_create', { query: 'from:bank', forward: 'x@evil.example' });
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
    expect(JSON.parse(result.content[0].text as string).action).toBe('gmail.filter-forward');
    const details = (JSON.parse(request!.params.message.split('\n').slice(1).join('\n')) as { details: Record<string, unknown> }).details;
    expect(details.forwardTo).toBe('x@evil.example');
    expect(details.criteria).toEqual({ query: 'from:bank' });
  });

  it('creates it and logs the forward target once the user confirms', async () => {
    const writeSpy = vi.spyOn(process.stderr, 'write').mockImplementation(() => true);
    await harness.callTool('gog_gmail_filters_create', { from: 'a@x.com', forward: 'x@evil.example' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'filters', 'create', '--from=a@x.com', '--forward=x@evil.example', '--force'],
      { account: undefined },
    );
    const event = JSON.parse((writeSpy.mock.calls.at(-1)?.[0] as string).trim());
    expect(event.tool).toBe('gog_gmail_filters_create');
    expect(event.externalDomains).toEqual(['evil.example']);
    expect(JSON.stringify(event)).not.toContain('x@evil.example');
    writeSpy.mockRestore();
  });

  it('does not log when creating the filter fails', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(errorResult('boom'));
    const writeSpy = vi.spyOn(process.stderr, 'write').mockImplementation(() => true);
    await harness.callTool('gog_gmail_filters_create', { forward: 'x@evil.example' });
    expect(writeSpy).not.toHaveBeenCalled();
    writeSpy.mockRestore();
  });

  it('asks nothing for a filter that does not forward', async () => {
    let asked = false;
    elicitation = async () => {
      asked = true;
      return { action: 'decline' };
    };
    await harness.callTool('gog_gmail_filters_create', { from: 'a@x.com', archive: true });
    expect(asked).toBe(false);
    expect(lib.runOrDiagnose).toHaveBeenCalledTimes(1);
  });
});

describe('gog_gmail_filters_create', () => {
  it('calls runOrDiagnose with no flags', async () => {
    await harness.callTool('gog_gmail_filters_create', {});
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'filters', 'create'],
      { account: undefined },
    );
  });

  it('passes all criteria and actions when provided', async () => {
    await harness.callTool('gog_gmail_filters_create', {
      from: 'alice@x.com',
      to: 'me@x.com',
      subject: 'Report',
      query: 'has:attachment',
      hasAttachment: true,
      addLabel: 'Reports',
      removeLabel: 'INBOX',
      archive: true,
      markRead: true,
      star: true,
      important: true,
      trash: true,
      neverSpam: true,
      forward: 'fwd@x.com',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'filters', 'create', '--from=alice@x.com', '--to=me@x.com', '--subject=Report', '--query=has:attachment', '--has-attachment', '--add-label=Reports', '--remove-label=INBOX', '--archive', '--mark-read', '--star', '--important', '--trash', '--never-spam', '--forward=fwd@x.com', '--force'],
      { account: undefined },
    );
  });

  it('omits boolean flags when false', async () => {
    await harness.callTool('gog_gmail_filters_create', {
      from: 'a@x.com',
      hasAttachment: false,
      archive: false,
      markRead: false,
      star: false,
      important: false,
      trash: false,
      neverSpam: false,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'filters', 'create', '--from=a@x.com'],
      { account: undefined },
    );
  });
});

describe('gog_gmail_filters_delete', () => {
  it('calls runOrDiagnose with the filter ID', async () => {
    await harness.callTool('gog_gmail_filters_delete', { filterId: 'f1' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'filters', 'delete', pos('f1'), '--force'],
      { account: undefined },
    );
  });
});

describe('gog_gmail_sendas_list', () => {
  it('calls runOrDiagnose', async () => {
    await harness.callTool('gog_gmail_sendas_list', {});
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'sendas', 'list'],
      { account: undefined },
    );
  });
});

describe('gog_gmail_sendas_get', () => {
  it('calls runOrDiagnose with the email', async () => {
    await harness.callTool('gog_gmail_sendas_get', { email: 'alias@x.com' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'sendas', 'get', pos('alias@x.com')],
      { account: undefined },
    );
  });
});

describe('gog_gmail_sendas_create', () => {
  it('calls runOrDiagnose with just the email', async () => {
    await harness.callTool('gog_gmail_sendas_create', { email: 'alias@x.com' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'sendas', 'create', pos('alias@x.com')],
      { account: undefined },
    );
  });

  it('passes all flags when provided', async () => {
    await harness.callTool('gog_gmail_sendas_create', {
      email: 'alias@x.com',
      displayName: 'Alias',
      replyTo: 'reply@x.com',
      signature: '<p>sig</p>',
      treatAsAlias: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'sendas', 'create', pos('alias@x.com'), '--display-name=Alias', '--reply-to=reply@x.com', '--signature=<p>sig</p>', '--treat-as-alias'],
      { account: undefined },
    );
  });

  it('omits treatAsAlias when false', async () => {
    await harness.callTool('gog_gmail_sendas_create', { email: 'alias@x.com', treatAsAlias: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'sendas', 'create', pos('alias@x.com')],
      { account: undefined },
    );
  });
});

describe('gog_gmail_sendas_update', () => {
  it('calls runOrDiagnose with just the email', async () => {
    await harness.callTool('gog_gmail_sendas_update', { email: 'alias@x.com' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'sendas', 'update', pos('alias@x.com')],
      { account: undefined },
    );
  });

  it('passes all flags when provided', async () => {
    await harness.callTool('gog_gmail_sendas_update', {
      email: 'alias@x.com',
      displayName: 'Alias',
      replyTo: 'reply@x.com',
      signature: '<p>sig</p>',
      treatAsAlias: true,
      makeDefault: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'sendas', 'update', pos('alias@x.com'), '--display-name=Alias', '--reply-to=reply@x.com', '--signature=<p>sig</p>', '--treat-as-alias', '--make-default'],
      { account: undefined },
    );
  });

  it('omits boolean flags when false', async () => {
    await harness.callTool('gog_gmail_sendas_update', { email: 'alias@x.com', treatAsAlias: false, makeDefault: false });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'sendas', 'update', pos('alias@x.com')],
      { account: undefined },
    );
  });
});

describe('gog_gmail_sendas_delete', () => {
  it('calls runOrDiagnose with the email', async () => {
    await harness.callTool('gog_gmail_sendas_delete', { email: 'alias@x.com' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'sendas', 'delete', pos('alias@x.com'), '--force'],
      { account: undefined },
    );
  });
});

describe('gog_gmail_sendas_verify', () => {
  it('calls runOrDiagnose with the email', async () => {
    await harness.callTool('gog_gmail_sendas_verify', { email: 'alias@x.com' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'settings', 'sendas', 'verify', pos('alias@x.com')],
      { account: undefined },
    );
  });
});

// resultText degradations: a non-text tool result (never produced by
// runOrDiagnose today, but allowed by the MCP result shape) is passed
// through untouched instead of being post-processed.
describe('non-text result passthrough', () => {
  it('gog_gmail_thread_get returns a non-text result untouched when trimming', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue({ content: [] });
    const result = await harness.callTool('gog_gmail_thread_get', { threadId: 't1', latestN: 1 });
    expect(result.content).toEqual([]);
  });

  it('returnFull surfaces a non-text write result without re-fetching', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce({ content: [] });
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'B', returnFull: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledTimes(1);
    expect(result.content).toEqual([]);
  });
});

// Large message bodies cannot travel in argv: the Linux kernel caps
// MAX_ARG_STRLEN at 128 KiB. payloadArg swaps an oversize value for a
// GogFileArg that the runner materializes as a temp file. These tests pin the boundary behavior at the
// tool surface: small bodies stay inline, large ones become file args, and the
// rest of the flag set is unaffected either way.
describe('large payloads route to file args', () => {
  const big = 'x'.repeat(lib.PAYLOAD_INLINE_MAX + 1);
  const bigHtml = `<table>${'<tr><td>cell</td></tr>'.repeat(600)}</table>`;

  // Pull the args array out of the single runOrDiagnose call under test.
  function args(): lib.GogArg[] {
    return vi.mocked(lib.runOrDiagnose).mock.calls[0]![0];
  }

  it('keeps a body at exactly the threshold inline', async () => {
    const atLimit = 'x'.repeat(lib.PAYLOAD_INLINE_MAX);
    await harness.callTool('gog_gmail_drafts_create', { subject: 'S', body: atLimit });
    expect(args()).toEqual(['gmail', 'drafts', 'create', '--subject=S', `--body=${atLimit}`, '--auto-from-addressed-alias=false']);
  });

  it('measures bytes, not characters, so a multibyte body crosses earlier', async () => {
    // Each emoji is 2 UTF-16 units but 4 UTF-8 bytes, so this sits comfortably
    // under the threshold by .length yet well over it by byte count.
    const emoji = '😀'.repeat(1500);
    expect(emoji.length).toBeLessThan(lib.PAYLOAD_INLINE_MAX);
    expect(Buffer.byteLength(emoji, 'utf8')).toBeGreaterThan(lib.PAYLOAD_INLINE_MAX);
    await harness.callTool('gog_gmail_drafts_create', { subject: 'S', body: emoji });
    expect(args()[4]).toEqual({ kind: 'file', flag: 'body-file', contents: emoji, ext: undefined });
  });

  it('gog_gmail_drafts_create routes a large body to --body-file', async () => {
    await harness.callTool('gog_gmail_drafts_create', { subject: 'S', body: big });
    expect(args()).toEqual([
      'gmail', 'drafts', 'create',
      '--subject=S',
      { kind: 'file', flag: 'body-file', contents: big, ext: undefined }, '--auto-from-addressed-alias=false'
    ]);
  });

  it('gog_gmail_drafts_create routes a large bodyHtml to --body-html-file with an html ext', async () => {
    expect(Buffer.byteLength(bigHtml)).toBeGreaterThan(12_000);
    await harness.callTool('gog_gmail_drafts_create', { subject: 'S', body: 'plain', bodyHtml: bigHtml });
    expect(args()).toEqual([
      'gmail', 'drafts', 'create',
      '--subject=S',
      '--body=plain',
      { kind: 'file', flag: 'body-html-file', contents: bigHtml, ext: 'html' }, '--auto-from-addressed-alias=false'
    ]);
  });

  it('gog_gmail_drafts_update routes a large body to --body-file', async () => {
    await harness.callTool('gog_gmail_drafts_update', { draftId: 'd1', subject: 'S', body: big });
    expect(args()).toEqual([
      'gmail', 'drafts', 'update', pos('d1'),
      '--subject=S',
      { kind: 'file', flag: 'body-file', contents: big, ext: undefined },
      // The generated HTML part is as large as the body, so it rides as a file too.
      expect.objectContaining({ kind: 'file', flag: 'body-html-file', ext: 'html' }),
      '--auto-from-addressed-alias=false',
    ]);
  });

  it('omitRecipients still suppresses to/cc/bcc alongside a large body', async () => {
    await harness.callTool('gog_gmail_drafts_create', {
      subject: 'S', body: big, to: 'a@b.com', cc: 'c@d.com', bcc: 'e@f.com', omitRecipients: true,
    });
    expect(args()).toEqual([
      'gmail', 'drafts', 'create',
      '--subject=S',
      { kind: 'file', flag: 'body-file', contents: big, ext: undefined }, '--auto-from-addressed-alias=false'
    ]);
  });

  it('threading and attachments still apply alongside a large body', async () => {
    await harness.callTool('gog_gmail_drafts_create', {
      subject: 'S', body: big, replyToThreadId: 't1', attach: ['/tmp/a.pdf'],
    });
    expect(args()).toEqual([
      'gmail', 'drafts', 'create',
      '--subject=S',
      { kind: 'file', flag: 'body-file', contents: big, ext: undefined },
      '--thread-id=t1',
      '--attach=/tmp/a.pdf', '--auto-from-addressed-alias=false'
    ]);
  });

  it('replyToMessageId still wins over replyToThreadId alongside a large body', async () => {
    await harness.callTool('gog_gmail_drafts_create', {
      subject: 'S', body: big, replyToMessageId: 'm1', replyToThreadId: 't1',
    });
    expect(args()).toContain('--reply-to-message-id=m1');
    expect(args()).not.toContain('--thread-id=t1');
  });

  it('gog_gmail_forward routes a large note to --note-file', async () => {
    await harness.callTool('gog_gmail_forward', { messageId: 'm1', to: 'a@b.com', note: big });
    expect(args()).toEqual([
      'gmail', 'forward', pos('m1'), '--to=a@b.com',
      { kind: 'file', flag: 'note-file', contents: big, ext: undefined },
    ]);
  });

  it('gog_gmail_autoreply routes a large body to --body-file but keeps bodyHtml inline', async () => {
    // gog 0.34.1 gives `gmail autoreply` a --body-file but no --body-html-file.
    await harness.callTool('gog_gmail_autoreply', { query: 'is:unread', body: big, bodyHtml: '<p>Hi</p>' });
    expect(vi.mocked(lib.runOrDiagnose).mock.calls.at(-1)?.[0]).toEqual([
      'gmail', 'autoreply', pos('is:unread'),
      { kind: 'file', flag: 'body-file', contents: big, ext: undefined },
      '--body-html=<p>Hi</p>',
    ]);
  });

  it('gog_gmail_vacation_update keeps a large body inline (gog has no --body-file there)', async () => {
    await harness.callTool('gog_gmail_vacation_update', { enable: true, body: big });
    expect(args()).toEqual(['gmail', 'settings', 'vacation', 'update', '--enable', `--body=${big}`]);
  });
});

// gog hard-errors when an inline flag and its --*-file twin are both present
// ("use only one of --body-html or --body-html-file"). The tools reject the
// combination up front so the caller sees which PARAMS collided.
describe('inline/file param conflicts are rejected before gog runs', () => {
  it('gog_gmail_drafts_create rejects bodyHtml plus bodyHtmlFile', async () => {
    const res = await harness.callTool('gog_gmail_drafts_create', {
      subject: 'S', body: 'B', bodyHtml: '<p>Hi</p>', bodyHtmlFile: '/tmp/b.html',
    });
    expect(res.isError).toBe(true);
    expect((res.content[0] as { text: string }).text).toContain('bodyHtml and bodyHtmlFile are mutually exclusive');
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
  });

  it('gog_gmail_drafts_update rejects bodyHtml plus bodyHtmlFile', async () => {
    const res = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'B', bodyHtml: '<p>Hi</p>', bodyHtmlFile: '/tmp/b.html',
    });
    expect(res.isError).toBe(true);
    expect((res.content[0] as { text: string }).text).toContain('mutually exclusive');
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
  });
});

// ---------------------------------------------------------------------------
// gog 0.35.0 capabilities (MIN_GOG_VERSION floor).
//
// Every flag below is env-bound in gog, so an ambient GOG_GMAIL_* var on the
// host silently changes the SHAPE of the output (or, for the attachment
// download, makes gog reject the caller's own argument). runner.ts strips only
// *_TOKEN/*_SECRET/*_KEY/*_CREDENTIALS, and on a hosted deployment the child
// env belongs to a host this wrapper does not control — so the tests below
// assert the flag is PINNED on every call, not merely pushed when true.
// ---------------------------------------------------------------------------

describe('gog 0.35.0 — indexed attachment ids (gog_gmail_attachment)', () => {
  const PDF_B64 = 'JVBERi0xLjUKJVBFRgo=';
  const INDEXED_LIST = {
    attachments: [
      { filename: 'cover.png', mimeType: 'image/png', attachmentIndex: 0, size: 11 },
      { filename: 'Guest_Copy.pdf', mimeType: 'application/pdf', attachmentIndex: 1, size: 99723 },
    ],
  };

  function stub(opts: { meta?: unknown; metaError?: Error; download?: unknown; downloadError?: unknown }): void {
    vi.mocked(lib.run).mockImplementation(async (args) => {
      const a = plain(args);
      if (a[0] === 'gmail' && a[1] === 'get') {
        if (opts.metaError) throw opts.metaError;
        return JSON.stringify(opts.meta ?? { attachments: [] });
      }
      if (a[0] === 'gmail' && a[1] === 'attachment') {
        if (opts.downloadError) throw opts.downloadError;
        return JSON.stringify(opts.download ?? {});
      }
      return '{}';
    });
  }
  const runArgs = () => vi.mocked(lib.run).mock.calls.map((c) => c[0] as string[]);
  const dlArgs = () => runArgs().find((a) => a[1] === 'attachment')!;
  const textOf = (res: { content: unknown[] }) => (res.content[0] as { text: string }).text;

  it('resolves the real filename BEFORE the download and never runs the size heuristic', async () => {
    stub({ meta: INDEXED_LIST, download: { path: `${ROOT}/m1/Guest_Copy.pdf`, bytes: 99723, contentBase64: PDF_B64 } });
    const res = await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentIndex: 1 });
    // exactly one metadata read, and it happens BEFORE the download.
    expect(runArgs().map((a) => a.slice(0, 2))).toEqual([['gmail', 'get'], ['gmail', 'attachment']]);
    expect(runArgs()[0]).toEqual(['gmail', 'get', pos('m1'), '--use-indexed-attachment-ids']);
    // the index rides in the positional slot, and gog is told to read it as one.
    expect(dlArgs()).toEqual([
      'gmail', 'attachment', pos('m1'), pos('1'), '--use-indexed-attachment-ids', '--inline', '--inline-max-bytes=3145728',
      `--out=${ROOT}/m1/Guest_Copy.pdf`, '--name=Guest_Copy.pdf',
    ]);
    expect(JSON.parse(textOf(res))).toMatchObject({ fileName: 'Guest_Copy.pdf', mimeType: 'application/pdf' });
  });

  it('pins the mode OFF on the legacy attachmentId path', async () => {
    stub({ download: { path: `${ROOT}/m1/x.pdf`, bytes: 12, contentBase64: PDF_B64 } });
    await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentId: 'OPAQUE1', name: 'x.pdf' });
    expect(dlArgs()).toEqual([
      'gmail', 'attachment', pos('m1'), pos('OPAQUE1'), '--use-indexed-attachment-ids=false', '--inline', '--inline-max-bytes=3145728',
      `--out=${ROOT}/m1/x.pdf`, '--name=x.pdf',
    ]);
  });

  it('rejects both attachmentId and attachmentIndex', async () => {
    const res = await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentId: 'a1', attachmentIndex: 0 });
    expect(res.isError).toBe(true);
    expect(textOf(res)).toContain('exactly one');
    expect(lib.run).not.toHaveBeenCalled();
  });

  it('rejects neither attachmentId nor attachmentIndex', async () => {
    const res = await harness.callTool('gog_gmail_attachment', { messageId: 'm1' });
    expect(res.isError).toBe(true);
    expect(textOf(res)).toContain('exactly one');
    expect(lib.run).not.toHaveBeenCalled();
  });

  it('a caller-supplied name skips the index lookup', async () => {
    stub({ meta: INDEXED_LIST, download: { path: `${ROOT}/m1/mine.pdf`, bytes: 5, contentBase64: PDF_B64 } });
    await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentIndex: 1, name: 'mine.pdf' });
    expect(runArgs().some((a) => a[1] === 'get')).toBe(false);
  });

  it('survives an index lookup failure without falling back to the size heuristic', async () => {
    stub({ metaError: new Error('get failed'), download: { path: `${ROOT}/m1/attachment`, bytes: 12, contentBase64: PDF_B64 } });
    const res = await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentIndex: 0 });
    // only the (failed) pre-download lookup — resolveBySize must not run after it.
    expect(runArgs().filter((a) => a[1] === 'get')).toHaveLength(1);
    expect(JSON.parse(textOf(res))).toMatchObject({ fileName: 'attachment.pdf', mimeType: 'application/pdf' });
  });

  it('tolerates a message whose listing carries no attachments array', async () => {
    stub({ meta: {}, download: { path: `${ROOT}/m1/attachment`, bytes: 12, contentBase64: PDF_B64 } });
    const res = await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentIndex: 3 });
    expect(JSON.parse(textOf(res))).toMatchObject({ fileName: 'attachment.pdf' });
  });

  it('uses the filename/mimeType gog itself reports on an --inline download', async () => {
    // gog >= 0.34 returns the part metadata alongside the bytes; prefer it over
    // any wrapper-side guess.
    stub({ meta: { attachments: [{}] }, download: {
      path: `${ROOT}/m1/attachment`, bytes: 12, contentBase64: PDF_B64,
      filename: 'From_Gog.pdf', mimeType: 'application/pdf',
    } });
    const res = await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentIndex: 0 });
    expect(JSON.parse(textOf(res))).toMatchObject({ fileName: 'From_Gog.pdf', mimeType: 'application/pdf' });
  });

  it('prefers a caller name over the one gog reports', async () => {
    stub({ download: {
      path: `${ROOT}/m1/mine.pdf`, bytes: 12, contentBase64: PDF_B64,
      filename: 'From_Gog.pdf', mimeType: 'application/pdf',
    } });
    const res = await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentIndex: 0, name: 'mine.pdf' });
    expect(JSON.parse(textOf(res))).toMatchObject({ fileName: 'mine.pdf', mimeType: 'application/pdf' });
  });

  it('passes inlineMaxBytes through as --inline-max-bytes', async () => {
    stub({ meta: INDEXED_LIST, download: { path: `${ROOT}/m1/cover.png`, bytes: 11 } });
    await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentIndex: 0, inlineMaxBytes: 1048576 });
    expect(dlArgs()).toEqual([
      'gmail', 'attachment', pos('m1'), pos('0'), '--use-indexed-attachment-ids', '--inline', '--inline-max-bytes=1048576',
      `--out=${ROOT}/m1/cover.png`, '--name=cover.png',
    ]);
  });

  it('does not mangle an indexed failure message while redacting (no bare-digit substitution)', async () => {
    stub({ downloadError: new Error('Command failed: gog gmail attachment m1 0\nquota exceeded: 1000 requests') });
    await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentIndex: 0 });
    const passed = (vi.mocked(lib.diagnose).mock.calls[0]![0] as Error).message;
    expect(passed).toBe('quota exceeded: 1000 requests');
  });
});

describe('gog 0.35.0 — indexed ids are pinned on every listing that emits attachments', () => {
  const args = () => vi.mocked(lib.runOrDiagnose).mock.calls[0]![0] as string[];

  it('gog_gmail_thread_get pins the mode off by default and on when asked', async () => {
    await harness.callTool('gog_gmail_thread_get', { threadId: 't1' });
    expect(args()).toEqual(['gmail', 'thread', 'get', pos('t1'), '--use-indexed-attachment-ids=false']);
    vi.clearAllMocks();
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult('{}'));
    await harness.callTool('gog_gmail_thread_get', { threadId: 't1', useIndexedAttachmentIds: true });
    expect(args()).toEqual(['gmail', 'thread', 'get', pos('t1'), '--use-indexed-attachment-ids']);
  });

  it('gog_gmail_thread_attachments pins the mode — a flat list needs per-message indexes', async () => {
    await harness.callTool('gog_gmail_thread_attachments', { threadId: 't1' });
    expect(args()).toEqual(['gmail', 'thread', 'attachments', pos('t1'), '--use-indexed-attachment-ids=false']);
    vi.clearAllMocks();
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult('{}'));
    await harness.callTool('gog_gmail_thread_attachments', { threadId: 't1', useIndexedAttachmentIds: true });
    expect(args()).toEqual(['gmail', 'thread', 'attachments', pos('t1'), '--use-indexed-attachment-ids']);
  });

  it('gog_gmail_drafts_get pins the mode', async () => {
    await harness.callTool('gog_gmail_drafts_get', { draftId: 'd1', format: 'raw' });
    expect(args()).toEqual(['gmail', 'drafts', 'get', pos('d1'), '--use-indexed-attachment-ids=false']);
    vi.clearAllMocks();
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult('{}'));
    await harness.callTool('gog_gmail_drafts_get', { draftId: 'd1', format: 'raw', useIndexedAttachmentIds: true });
    expect(args()).toEqual(['gmail', 'drafts', 'get', pos('d1'), '--use-indexed-attachment-ids']);
  });

  it('gog_gmail_messages_search pins BOTH attachment-shaping flags', async () => {
    await harness.callTool('gog_gmail_messages_search', { query: 'x' });
    expect(args()).toEqual([
      'gmail', 'messages', 'search', pos('x'), '--include-attachments=false', '--use-indexed-attachment-ids=false',
    ]);
    vi.clearAllMocks();
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult('{}'));
    await harness.callTool('gog_gmail_messages_search', { query: 'x', includeAttachments: true, useIndexedAttachmentIds: true });
    expect(args()).toEqual([
      'gmail', 'messages', 'search', pos('x'), '--include-attachments', '--use-indexed-attachment-ids',
    ]);
  });
});

describe('gog 0.35.0 — --auto-from-addressed-alias is pinned on every send-shaped write', () => {
  const args = () => vi.mocked(lib.runOrDiagnose).mock.calls[0]![0] as string[];

  it('gog_gmail_drafts_create pins it off, and sets it when asked', async () => {
    await harness.callTool('gog_gmail_drafts_create', { subject: 'S', body: 'B' });
    expect(args()).toEqual(['gmail', 'drafts', 'create', '--subject=S', '--body=B', '--auto-from-addressed-alias=false']);
    vi.clearAllMocks();
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult('{}'));
    await harness.callTool('gog_gmail_drafts_create', { subject: 'S', body: 'B', autoFromAddressedAlias: true });
    expect(args()).toEqual(['gmail', 'drafts', 'create', '--subject=S', '--body=B', '--auto-from-addressed-alias']);
  });

  it('gog_gmail_drafts_update pins it', async () => {
    await harness.callTool('gog_gmail_drafts_update', { draftId: 'd1', subject: 'S', body: 'B', autoFromAddressedAlias: true });
    expect(args()).toEqual(['gmail', 'drafts', 'update', pos('d1'), '--subject=S', '--body=B', '--body-html=<p>B</p>', '--auto-from-addressed-alias']);
  });
});

describe('gog 0.35.0 — gog_gmail_import', () => {
  const args = () => vi.mocked(lib.runOrDiagnose).mock.calls[0]![0] as string[];

  it('imports a file with no options', async () => {
    await harness.callTool('gog_gmail_import', { file: '/tmp/msg.eml' });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(['gmail', 'import', pos('/tmp/msg.eml')], { account: undefined });
  });

  it('passes every option, repeating --label', async () => {
    await harness.callTool('gog_gmail_import', {
      file: '/srv/exports/archived.eml',
      labels: ['INBOX', 'Archive/2026'],
      internalDateSource: 'receivedTime',
      neverMarkSpam: true,
      processForCalendar: true,
      account: 'me@x.com',
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'import', pos('/srv/exports/archived.eml'), '--label=INBOX', '--label=Archive/2026', '--internal-date-source=receivedTime', '--never-mark-spam', '--process-for-calendar'],
      { account: 'me@x.com' },
    );
  });

  it('omits flags that are false or absent', async () => {
    await harness.callTool('gog_gmail_import', { file: '/tmp/m.eml', neverMarkSpam: false, processForCalendar: false });
    expect(args()).toEqual(['gmail', 'import', pos('/tmp/m.eml')]);
  });

  it('rejects an internalDateSource outside gog\'s enum', async () => {
    const res = await harness.callTool('gog_gmail_import', { file: '/tmp/m.eml', internalDateSource: 'yesterday' });
    expect(res.isError).toBe(true);
  });

  it('never appends --force — gog gates no confirmation on import', async () => {
    await harness.callTool('gog_gmail_import', { file: '/tmp/m.eml' });
    expect(args()).not.toContain('--force');
  });
});

// gog reads a "-" path argument with io.ReadAll(stdinReader(ctx)) — os.Stdin,
// unaffected by --no-input (gmail_import.go:102, gmail_body_input.go:45 at
// upstream-v0.35.0). runner.ts's spawnGog spawns with default stdio and never
// writes to or ends child.stdin, so gog blocks forever on a read that never
// EOFs: `spawn('gog', ['gmail','import','-','--dry-run','--json','--no-input'])`
// was still running with no output after 5s. Under run() that burns the whole
// 30s timeout and returns "gog timed out after 30s". No description may offer
// it as a usable option.
describe('server-side file params never advertise stdin as usable', () => {
  const STDIN_PARAMS: Array<[tool: string, param: string]> = [
    ['gog_gmail_import', 'file'],
    ['gog_gmail_drafts_create', 'bodyHtmlFile'],
    ['gog_gmail_drafts_update', 'bodyHtmlFile'],
  ];

  async function paramDescriptions(): Promise<Map<string, Record<string, { description?: string }>>> {
    const configs = new Map<string, Record<string, { description?: string }>>();
    const { tools } = await harness.client.listTools();
    for (const tool of tools) {
      configs.set(tool.name, tool.inputSchema.properties as Record<string, { description?: string }>);
    }
    return configs;
  }

  it.each(STDIN_PARAMS)('%s.%s warns that stdin hangs instead of offering it', async (tool, param) => {
    const schema = (await paramDescriptions()).get(tool);
    const desc = schema?.[param]?.description ?? '';
    expect(desc).not.toBe('');
    expect(desc).not.toMatch(/(?:or|use)\s+"?-"?\s+(?:for|to read)/i);
    expect(desc).toMatch(/stdin/i);
    expect(desc).toMatch(/hang|never writes/i);
  });
});

// Every env-bound gog flag this tool depends on is pinned on the call, because
// the child env on a hosted deployment belongs to a host we do not control.
// --inline-max-bytes is declared env:"GOG_GMAIL_INLINE_MAX_BYTES"
// (gmail_attachment.go:27 at upstream-v0.35.0), so an ambient value would
// silently decide whether contentBase64 comes back at all.
describe('gog_gmail_attachment pins --inline-max-bytes', () => {
  const args = () => vi.mocked(lib.run).mock.calls[0]![0] as string[];

  it('pins gog\'s default when the caller supplies nothing', async () => {
    vi.mocked(lib.run).mockResolvedValue(JSON.stringify({ bytes: 10, contentBase64: 'AAAA', mimeType: 'image/png', filename: 'a.png' }));
    await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentId: 'a1', deliver: 'inline' });
    expect(args()).toContain('--inline-max-bytes=3145728');
  });

  it('pins the caller\'s value when supplied', async () => {
    vi.mocked(lib.run).mockResolvedValue(JSON.stringify({ bytes: 10, contentBase64: 'AAAA', mimeType: 'image/png', filename: 'a.png' }));
    await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentId: 'a1', deliver: 'inline', inlineMaxBytes: 99 });
    expect(args()).toContain('--inline-max-bytes=99');
  });
});

// mcp-host caps one child result at 14 MiB of serialized JSON-RPC
// (CHILD_RESULT_MAX_BYTES, chrischall/mcp-host#952). 10 MiB raw is ~13.3 MiB
// base64, which fits with the envelope — so a caller's inlineMaxBytes is
// CLAMPED to 10 MiB (gog then falls back to the file path exactly as it does
// for any attachment over the ceiling) and the result says so.
describe('gog_gmail_attachment bounds inlineMaxBytes at 10 MiB', () => {
  const TEN_MIB = 10 * 1024 * 1024;
  const args = () => vi.mocked(lib.run).mock.calls[0]![0] as string[];
  const texts = (res: { content: unknown[] }) =>
    res.content.map((c) => (c as { text?: string }).text ?? '').join('\n');

  it('allows exactly 10 MiB, unchanged and without a note', async () => {
    vi.mocked(lib.run).mockResolvedValue(JSON.stringify({ bytes: 10, contentBase64: 'AAAA', mimeType: 'image/png', filename: 'a.png' }));
    const res = await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentId: 'a1', deliver: 'inline', inlineMaxBytes: TEN_MIB });
    expect(args()).toContain(`--inline-max-bytes=${TEN_MIB}`);
    expect(texts(res)).not.toMatch(/clamped/i);
  });

  it('clamps a larger request to 10 MiB and notes it in the result', async () => {
    vi.mocked(lib.run).mockResolvedValue(JSON.stringify({ bytes: 10, contentBase64: 'AAAA', mimeType: 'image/png', filename: 'a.png' }));
    const res = await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentId: 'a1', deliver: 'inline', inlineMaxBytes: 50 * 1024 * 1024 });
    expect(args()).toContain(`--inline-max-bytes=${TEN_MIB}`);
    expect(res.isError).toBeFalsy();
    expect(texts(res)).toMatch(/inlineMaxBytes .*clamped to 10485760/i);
  });

  it('names the 10 MiB maximum when a clamped inline request is still too large', async () => {
    vi.mocked(lib.run).mockResolvedValue(JSON.stringify({ path: '/tmp/x.pdf', bytes: 12 * 1024 * 1024, reason: 'exceeds inline max bytes' }));
    const res = await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentId: 'a1', deliver: 'inline', name: 'x.pdf', inlineMaxBytes: 50 * 1024 * 1024 });
    expect(res.isError).toBe(true);
    expect(texts(res)).toMatch(/10 MiB/);
    expect(texts(res)).toMatch(/deliver="url"/);
  });

  it('tells the model about the bound in the schema description', async () => {
    const { tools } = await harness.client.listTools();
    const props = tools.find((t) => t.name === 'gog_gmail_attachment')!.inputSchema.properties as Record<string, { description?: string }>;
    expect(props.inlineMaxBytes!.description).toMatch(/10 MiB/);
    expect(props.inlineMaxBytes!.description).toMatch(/10485760/);
  });
});

// ===========================================================================
// REQUIREMENT 4 — VERIFY (and repair) THREADING ON AN UPDATE.
//
// gog already does the repair: `--thread-id` on `gmail drafts update` sets
// replyToThreadID, so buildDraftMessage RESOLVES In-Reply-To/References from
// the thread's latest non-draft message, and Users.Drafts.Update keeps the
// draft id (internal/cmd/gmail_drafts.go, upstream-v0.35.0). What was missing
// is the VERIFICATION: gog reports inReplyTo/references/replyContextSource in
// its own ack, and nothing was reading them back to the caller.
//
// The silent failure this catches: the thread branch of fetchReplyInfo has no
// "target has no Message-ID header" guard (the message branch does), so a
// thread whose latest message lacks a Message-Id resolves NO lineage — and
// because an explicit reply target suppresses the carry-forward branch, the
// draft is MOVED to the new thread and ends up with NO reply headers at all.
// ===========================================================================
describe('gog_gmail_drafts_update — threading verification', () => {
  const ACK = (over: Record<string, unknown> = {}): string => JSON.stringify({
    draftId: 'r4303011157206680397',
    threadId: '19f856becba0661d',
    inReplyTo: '<CAO@mail.gmail.com>',
    references: '<CAO@mail.gmail.com>',
    replyContextSource: 'caller',
    ...over,
  });

  it('adopts a draft onto a thread in one call, keeps its id, and reports the effective headers', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(ACK()));
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'r4303011157206680397',
      subject: 'Re: pickup schedule',
      body: 'merged text',
      replyToThreadId: '19f856becba0661d',
    });

    // One gog invocation: gog resolves the thread's reply headers server-side.
    expect(lib.runOrDiagnose).toHaveBeenCalledTimes(1);
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'update', pos('r4303011157206680397'), '--subject=Re: pickup schedule',
        '--body=merged text', '--body-html=<p>merged text</p>', '--thread-id=19f856becba0661d', '--auto-from-addressed-alias=false'],
      { account: undefined },
    );

    const parsed = JSON.parse(result.content[0].text);
    // The id survives the adoption — that is the whole point of updating in place.
    expect(parsed.draftId).toBe('r4303011157206680397');
    expect(parsed.threadingVerification).toMatchObject({
      requested: 'set',
      via: 'replyToThreadId',
      target: '19f856becba0661d',
      ok: true,
      effective: {
        threadId: '19f856becba0661d',
        inReplyTo: '<CAO@mail.gmail.com>',
        references: '<CAO@mail.gmail.com>',
        replyContextSource: 'caller',
      },
    });
    // Every update rewrites the body — gog requires --body. Say so.
    expect(parsed.threadingVerification.note).toMatch(/body/i);
  });

  it('WARNS when the re-thread moved the draft but produced no reply headers', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(
      ACK({ inReplyTo: null, references: null, replyContextSource: null }),
    ));
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'r4303011157206680397', subject: 'S', body: 'B', replyToThreadId: '19f856becba0661d',
    });
    const v = JSON.parse(result.content[0].text).threadingVerification;
    expect(v.ok).toBe(false);
    expect(v.note).toMatch(/WARNING/);
    expect(v.note).toMatch(/not arrive as a reply/i);
    // The dangerous half: it DID move threads, so it is not a no-op to ignore.
    expect(v.note).toContain('19f856becba0661d');
  });

  it('anchors to a message id when both reply targets are given, and says which it used', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(ACK()));
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'B', replyToMessageId: 'mExplicit', replyToThreadId: 't1',
    });
    const args = vi.mocked(lib.runOrDiagnose).mock.calls[0]![0] as string[];
    expect(args).toContain('--reply-to-message-id=mExplicit');
    expect(args.some((a) => typeof a === 'string' && a.startsWith('--thread-id'))).toBe(false);
    expect(JSON.parse(result.content[0].text).threadingVerification).toMatchObject({
      requested: 'set', via: 'replyToMessageId', target: 'mExplicit', ok: true,
    });
  });

  it('confirms clearReplyContext actually dropped the lineage, and that the threadId stayed', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(
      ACK({ inReplyTo: null, references: null, replyContextSource: null }),
    ));
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'B', clearReplyContext: true,
    });
    const v = JSON.parse(result.content[0].text).threadingVerification;
    expect(v).toMatchObject({ requested: 'clear', ok: true });
    expect(v.note).not.toMatch(/WARNING/);
    expect(v.effective.threadId).toBe('19f856becba0661d');
  });

  it('WARNS when clearReplyContext left reply headers in place', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(ACK()));
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'B', clearReplyContext: true,
    });
    const v = JSON.parse(result.content[0].text).threadingVerification;
    expect(v.ok).toBe(false);
    expect(v.note).toMatch(/WARNING/);
    expect(v.note).toContain('<CAO@mail.gmail.com>');
  });

  it('adds nothing at all when no reply-context change was requested', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(ACK()));
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'B',
    });
    // Byte-identical passthrough: an update that changes no threading must not
    // acquire a new output shape.
    expect(result.content[0].text).toBe(ACK());
  });

  it('carries the verification onto the returnFull re-fetch', async () => {
    vi.mocked(lib.runOrDiagnose)
      .mockResolvedValueOnce(rawTextResult(ACK()))
      .mockResolvedValueOnce(rawTextResult('{"draft":{"id":"r4303011157206680397"}}'));
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'r4303011157206680397', subject: 'S', body: 'B', replyToThreadId: '19f856becba0661d', returnFull: true,
    });
    expect(lib.runOrDiagnose).toHaveBeenCalledTimes(2);
    const parsed = JSON.parse(result.content[0].text);
    expect(parsed.draft.id).toBe('r4303011157206680397');
    expect(parsed.threadingVerification.ok).toBe(true);
  });

  it('degrades to a prose note when the final result is not a JSON object', async () => {
    vi.mocked(lib.runOrDiagnose)
      .mockResolvedValueOnce(rawTextResult(ACK()))
      .mockResolvedValueOnce(rawTextResult('draft_id\tr4303011157206680397'));
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'r4303011157206680397', subject: 'S', body: 'B', replyToThreadId: '19f856becba0661d', returnFull: true,
    });
    expect(result.content[0].text).toMatch(/threadingVerification/);
    expect(result.content[1].text).toBe('draft_id\tr4303011157206680397');
  });

  it('labels an unreported threadId rather than interpolating undefined', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(JSON.stringify({
      draftId: 'd1', inReplyTo: null, references: null, replyContextSource: null,
    })));
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'B', replyToThreadId: 't1',
    });
    const v = JSON.parse(result.content[0].text).threadingVerification;
    expect(v.effective.threadId).toBeUndefined();
    expect(v.note).toContain('(none reported)');
    expect(v.note).not.toContain('undefined');
  });

  it('says nothing when the write itself failed (no JSON ack to verify against)', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(errorResult('Error: usage: --subject required'));
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'B', replyToThreadId: 't1',
    });
    expect(result.content[0].text).toContain('usage: --subject required');
    expect(result.content[0].text).not.toContain('threadingVerification');
  });
});

// ===========================================================================
// REQUIREMENT 1 — a 404 on a draft id is a FORK REPORT, not a bare notFound.
//
// A draft created here and then edited in a mail client is not updated in
// place: the client writes a NEW draft and abandons the original, so the
// original id stops resolving and `gog gmail drafts update` returns
// `Google API error (404 notFound)` with nothing to say it was replaced.
//
// HAZARD A governs the shape of the answer: with the original unfetchable
// there is nothing left to establish LINEAGE against, so this report may never
// name a replacement. It lists what exists and hands the caller the tool that
// can decide (gog_gmail_drafts_diff, on a named pair).
// HAZARD B governs its cost: at most 2 extra gog invocations, constant, and
// only on a call that has ALREADY failed.
// ===========================================================================
describe('gog_gmail_drafts_update — DRAFT_FORKED on 404', () => {
  const NOT_FOUND = 'Error: Google API error (404 notFound): Requested entity was not found.';
  const LIST = JSON.stringify({
    drafts: [
      { id: 's:14092347734530621658', messageId: '19fe8a673d1e5f21', threadId: '19fe8a673d1e5f21' },
      { id: 'r-457330811034304502', messageId: 'aaa', threadId: 'bbb' },
      // gog declares every field `omitempty`, so a draft can arrive with none
      // of them. It must still be listed, not crash the report.
      {},
    ],
  });
  const SEARCH = JSON.stringify({
    messages: [
      { id: '19fe8a673d1e5f21', subject: 'Re: pickup schedule', from: 'me@x.com', internalDateIso: '2026-08-09T10:00:00Z' },
      { id: 'aaa', subject: 'Unrelated note to the plumber', from: 'me@x.com', internalDateIso: '2026-08-01T09:00:00Z' },
      { subject: 'a search hit with no id joins to nothing' },
    ],
  });

  function stub404(): void {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(errorResult(NOT_FOUND));
    vi.mocked(lib.run).mockImplementation(async (args) => {
      const argv = plain(args);
      if (argv[1] === 'drafts' && argv[2] === 'list') return LIST;
      if (argv[1] === 'messages' && argv[2] === 'search') return SEARCH;
      throw new Error(`unexpected gog call: ${argv.join(' ')}`);
    });
  }

  it('explains the 404 as a possible client-side fork and keeps gog\'s own error', async () => {
    stub404();
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'r4303011157206680397', subject: 'S', body: 'B',
    });
    expect(result.isError).toBe(true);
    const text = result.content[0].text as string;
    expect(text).toContain('DRAFT_FORKED');
    expect(text).toContain('r4303011157206680397');
    // gog's own words survive verbatim — the diagnosis is added, never swapped in.
    expect(text).toContain('Google API error (404 notFound)');
    const parsed = JSON.parse(text.slice(text.indexOf('{')));
    expect(parsed.code).toBe('DRAFT_FORKED');
    expect(parsed.currentDrafts.map((d: { id?: string; origin: string; subject?: string }) => [d.id, d.origin, d.subject])).toEqual([
      ['s:14092347734530621658', 'non-api', 'Re: pickup schedule'],
      ['r-457330811034304502', 'api', 'Unrelated note to the plumber'],
      // An id-less draft is reported as `api` — the ONLY thing `non-api` may
      // ever mean is a literal `s:` prefix, so an absent id must not claim one.
      [undefined, 'api', undefined],
    ]);
    expect(parsed.nextSteps.join(' ')).toContain('gog_gmail_drafts_diff');
  });

  it('names NO replacement, even when a newer non-api draft is sitting right there', async () => {
    stub404();
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'r4303011157206680397', subject: 'S', body: 'B',
    });
    const text = result.content[0].text as string;
    const parsed = JSON.parse(text.slice(text.indexOf('{')));
    // Hazard A: the 404'd draft cannot be fetched, so no lineage signal can
    // exist and no pairing verdict is possible. Not "candidate" — none.
    expect(parsed.forkClaim).toBeNull();
    expect(text).not.toContain('confirmed');
    expect(text).not.toContain('apple-mail');
    for (const d of parsed.currentDrafts) expect(d).not.toHaveProperty('verdict');
    // The list is ordering, not evidence, and it says so.
    expect(parsed.forkClaimNote).toMatch(/ordering is presentation, not evidence/i);
    // And the 404 has innocent explanations too.
    expect(parsed.otherExplanations.join(' ')).toMatch(/deleted|sent/i);
  });

  it('spends at most two extra gog invocations, both constant in the number of drafts', async () => {
    stub404();
    await harness.callTool('gog_gmail_drafts_update', { draftId: 'r43', subject: 'S', body: 'B' });
    expect(vi.mocked(lib.run).mock.calls.map((c) => (c[0] as string[]).slice(0, 3))).toEqual([
      ['gmail', 'drafts', 'list'],
      ['gmail', 'messages', 'search'],
    ]);
    expect(vi.mocked(lib.run)).toHaveBeenCalledTimes(2);
  });

  it('leaves a non-404 failure completely alone, and spends nothing', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(errorResult('Error: Google API error (403 forbidden): insufficient scope'));
    const result = await harness.callTool('gog_gmail_drafts_update', { draftId: 'd1', subject: 'S', body: 'B' });
    expect(result.content[0].text).toBe('Error: Google API error (403 forbidden): insufficient scope');
    expect(lib.run).not.toHaveBeenCalled();
  });

  it('does not fire on a SUCCESSFUL result that merely mentions 404', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult('{"draftId":"d1","message":{"snippet":"the 404 not found page"}}'));
    const result = await harness.callTool('gog_gmail_drafts_update', { draftId: 'd1', subject: 'S', body: 'B' });
    expect(result.content[0].text).toContain('the 404 not found page');
    expect(result.content[0].text).not.toContain('DRAFT_FORKED');
    expect(lib.run).not.toHaveBeenCalled();
  });

  it('still reports the fork explanation when the draft listing itself fails', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(errorResult(NOT_FOUND));
    vi.mocked(lib.run).mockRejectedValue(new Error('gog timed out after 30s'));
    const result = await harness.callTool('gog_gmail_drafts_update', { draftId: 'd1', subject: 'S', body: 'B' });
    const text = result.content[0].text as string;
    expect(text).toContain('DRAFT_FORKED');
    const parsed = JSON.parse(text.slice(text.indexOf('{')));
    expect(parsed.currentDrafts).toBeUndefined();
    expect(parsed.currentDraftsUnavailable).toContain('gog timed out');
    expect(vi.mocked(lib.run)).toHaveBeenCalledTimes(1);
  });

  it('keeps the free tier-0 fields when only the enrichment search fails', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(errorResult(NOT_FOUND));
    vi.mocked(lib.run).mockImplementation(async (args) => {
      if (plain(args)[2] === 'list') return LIST;
      throw new Error('search exploded');
    });
    const result = await harness.callTool('gog_gmail_drafts_update', { draftId: 'd1', subject: 'S', body: 'B' });
    const text = result.content[0].text as string;
    const parsed = JSON.parse(text.slice(text.indexOf('{')));
    expect(parsed.currentDrafts).toHaveLength(3);
    expect(parsed.currentDrafts[0].origin).toBe('non-api');
    expect(parsed.currentDrafts[0].subject).toBeUndefined();
    expect(parsed.enrichmentNote).toContain('search exploded');
  });

  it('treats a listing without a drafts array as unavailable rather than empty', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(errorResult(NOT_FOUND));
    // Parses as JSON, but carries no drafts array — a different failure from
    // gog's plain-text "No drafts", and it must not read as "you have none".
    vi.mocked(lib.run).mockResolvedValue('{"nextPageToken":"tok"}');
    const result = await harness.callTool('gog_gmail_drafts_update', { draftId: 'd1', subject: 'S', body: 'B' });
    const parsed = JSON.parse((result.content[0].text as string).slice((result.content[0].text as string).indexOf('{')));
    expect(parsed.currentDraftsUnavailable).toContain('no drafts array');
  });

  it('fires for gog_gmail_drafts_send too — the draft you meant to send is gone', async () => {
    stub404();
    const result = await harness.callTool('gog_gmail_drafts_send', { draftId: 'r4303011157206680397' });
    expect(result.isError).toBe(true);
    const text = result.content[0].text as string;
    expect(text).toContain('DRAFT_FORKED');
    expect(text).toContain('gog_gmail_drafts_send');
    expect(vi.mocked(lib.run)).toHaveBeenCalledTimes(2);
  });

  // `gmail drafts update` resolves THREE Google entities and gog renders all
  // three 404s identically: the draft (Users.Drafts.Get/Update), the thread
  // behind --thread-id (Users.Threads.Get) and the message behind
  // --reply-to-message-id (Users.Messages.Get). Claiming DRAFT_FORKED on a
  // stale THREAD id — while listing that same draft id under currentDrafts —
  // sends the caller hunting for a replacement draft that does not exist.
  it('does not call it a fork when the draft is still listed: the 404 came from the reply target', async () => {
    stub404();
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'r-457330811034304502', subject: 'S', body: 'B',
      replyToThreadId: 'THREAD-THAT-DOES-NOT-EXIST',
    });
    expect(result.isError).toBe(true);
    const text = result.content[0].text as string;
    expect(text).not.toContain('DRAFT_FORKED');
    const parsed = JSON.parse(text.slice(text.indexOf('{')));
    expect(parsed.code).toBe('GOOGLE_404_NOT_THE_DRAFT');
    expect(parsed.replyTarget).toEqual({ via: 'replyToThreadId', target: 'THREAD-THAT-DOES-NOT-EXIST' });
    // The payload may not contradict itself: it lists the draft AND says it is gone.
    expect(parsed.currentDrafts.map((d: { id?: string }) => d.id)).toContain('r-457330811034304502');
    expect(parsed.whatHappened).not.toMatch(/no longer has a draft|has no draft under this id/i);
    expect(parsed.whatHappened).toMatch(/still exists|still listed/i);
    expect(parsed.nextSteps.join(' ')).toMatch(/thread id/i);
    // gog's own words survive, and the cost cap is unchanged.
    expect(text).toContain('Google API error (404 notFound)');
    expect(vi.mocked(lib.run)).toHaveBeenCalledTimes(2);
  });

  it('says the same for a send whose 404 cannot be about the draft id either', async () => {
    stub404();
    const result = await harness.callTool('gog_gmail_drafts_send', { draftId: 's:14092347734530621658' });
    const text = result.content[0].text as string;
    expect(text).not.toContain('DRAFT_FORKED');
    const parsed = JSON.parse(text.slice(text.indexOf('{')));
    expect(parsed.code).toBe('GOOGLE_404_NOT_THE_DRAFT');
    expect(parsed.replyTarget).toBeNull();
    expect(parsed.raceNote).toMatch(/AFTER the failure/i);
  });

  it('recognises a 404 that gog reported without a reason word', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(errorResult('Error: Google API error (404): Requested entity was not found.'));
    vi.mocked(lib.run).mockResolvedValue(LIST);
    const result = await harness.callTool('gog_gmail_drafts_send', { draftId: 'd1' });
    expect(result.content[0].text).toContain('DRAFT_FORKED');
  });
});

// ===========================================================================
// REQUIREMENT 5 — DO NOT LET AN ADOPTION SILENTLY DROP THE OTHER COPY'S TEXT.
//
// `draftComposeInput.validate()` (gmail_drafts.go:321) hard-requires a body on
// every update: "required: --body, --body-file, --body-html, or
// --body-html-file". There is no header-only edit, so re-threading a mail
// client's replacement back onto the original conversation ALWAYS rewrites the
// whole body — the exact operation that drops the paragraph living only in the
// sibling copy. In the observed case neither copy was a superset.
//
// COST (hazard B): the check is opt-in and costs exactly ONE extra gog
// invocation, on a NAMED sibling. It never scans, and with the param absent it
// spends nothing and changes no argv.
//
// CLAIMS (hazard A): it compares two bodies. It never says one draft replaced
// the other — that verdict needs gog_gmail_drafts_diff.
// ===========================================================================
describe('gog_gmail_drafts_update — content-loss check', () => {
  const b64 = (s: string) => Buffer.from(s, 'utf8').toString('base64url');
  const siblingGet = (body: string): string => JSON.stringify({
    draft: { id: 's:14092347734530621658', message: { id: 'm2', threadId: 'm2', payload: { mimeType: 'text/plain', body: { data: b64(body) } } } },
  });
  const ACK = '{"draftId":"r4303011157206680397","threadId":"19f856becba0661d","inReplyTo":"<orig@mail.gmail.com>"}';

  // The observed divergence: the mail-client copy kept a paragraph the merged
  // body forgot.
  const SIBLING_BODY = 'Thanks for the note.\nI can do the 14th.\nTHE PARAGRAPH ONLY APPLE HAS.\nBest, Chris';

  it('spends nothing and changes no argv when no sibling is named', async () => {
    await harness.callTool('gog_gmail_drafts_update', { draftId: 'd1', subject: 'S', body: 'B' });
    expect(lib.run).not.toHaveBeenCalled();
    expect(lib.runOrDiagnose).toHaveBeenCalledTimes(1);
    expect(lib.runOrDiagnose).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'update', pos('d1'), '--subject=S', '--body=B', '--body-html=<p>B</p>', '--auto-from-addressed-alias=false'],
      { account: undefined },
    );
  });

  it('costs exactly one extra invocation, and reads the sibling BEFORE writing', async () => {
    vi.mocked(lib.run).mockResolvedValue(siblingGet(SIBLING_BODY));
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(ACK));
    await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'r4303011157206680397', subject: 'S', body: SIBLING_BODY,
      forkSiblingDraftId: 's:14092347734530621658',
    });
    expect(lib.run).toHaveBeenCalledTimes(1);
    expect(lib.run).toHaveBeenCalledWith(
      ['gmail', 'drafts', 'get', pos('s:14092347734530621658'), '--use-indexed-attachment-ids=false'],
      { account: undefined },
    );
    expect(lib.runOrDiagnose).toHaveBeenCalledTimes(1);
    // Reading after the write would be a report on damage already done.
    expect(vi.mocked(lib.run).mock.invocationCallOrder[0])
      .toBeLessThan(vi.mocked(lib.runOrDiagnose).mock.invocationCallOrder[0]!);
  });

  it('writes, and reports the check, when the new body keeps every sibling line', async () => {
    vi.mocked(lib.run).mockResolvedValue(siblingGet(SIBLING_BODY));
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(ACK));
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'r4303011157206680397', subject: 'S', body: `${SIBLING_BODY}\nplus a line the Gmail copy added`,
      forkSiblingDraftId: 's:14092347734530621658', replyToThreadId: '19f856becba0661d',
    });
    expect(result.isError).toBeFalsy();
    const parsed = JSON.parse(result.content[0].text as string);
    expect(parsed.draftId).toBe('r4303011157206680397');
    expect(parsed.contentLossCheck).toMatchObject({
      siblingDraftId: 's:14092347734530621658', status: 'clean', linesOnlyInSibling: [],
    });
    // The adoption still reports what it actually threaded.
    expect(parsed.threadingVerification.ok).toBe(true);
  });

  it('REFUSES the write when the body would drop a line the sibling holds — and writes nothing', async () => {
    vi.mocked(lib.run).mockResolvedValue(siblingGet(SIBLING_BODY));
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'r4303011157206680397', subject: 'S',
      body: 'Thanks for the note.\nI can do the 14th.\nBest, Chris',
      forkSiblingDraftId: 's:14092347734530621658', replyToThreadId: '19f856becba0661d',
    });
    expect(result.isError).toBe(true);
    // THE point: the draft is untouched.
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
    const text = result.content[0].text as string;
    expect(text).toContain('DRAFT_CONTENT_LOSS');
    expect(text).toContain('THE PARAGRAPH ONLY APPLE HAS.');
    expect(text).toMatch(/nothing was written/i);
    const parsed = JSON.parse(text.slice(text.indexOf('{')));
    expect(parsed.contentLossCheck.status).toBe('would-lose');
    expect(parsed.contentLossCheck.linesOnlyInSiblingCount).toBe(1);
  });

  it('writes anyway, with the loss spelled out, when acceptContentLoss is set', async () => {
    vi.mocked(lib.run).mockResolvedValue(siblingGet(SIBLING_BODY));
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(ACK));
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'r4303011157206680397', subject: 'S', body: 'Thanks for the note.\nBest, Chris',
      forkSiblingDraftId: 's:14092347734530621658', acceptContentLoss: true,
    });
    expect(result.isError).toBeFalsy();
    expect(lib.runOrDiagnose).toHaveBeenCalledTimes(1);
    const check = JSON.parse(result.content[0].text as string).contentLossCheck;
    expect(check.status).toBe('would-lose');
    expect(check.acknowledged).toBe(true);
    expect(check.linesOnlyInSibling).toContain('THE PARAGRAPH ONLY APPLE HAS.');
  });

  it('refuses when the sibling cannot be fetched — an unrun check is not a passed check', async () => {
    vi.mocked(lib.run).mockRejectedValue(new Error('Google API error (404 notFound): Requested entity was not found.'));
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'B', forkSiblingDraftId: 's:gone',
    });
    expect(result.isError).toBe(true);
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
    const text = result.content[0].text as string;
    expect(text).toContain('DRAFT_CONTENT_LOSS_UNCHECKED');
    expect(text).toContain('404 notFound');
  });

  it('refuses when the sibling fetch returned something with no readable body', async () => {
    vi.mocked(lib.run).mockResolvedValue('not json at all');
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'B', forkSiblingDraftId: 's:weird',
    });
    expect(result.content[0].text).toContain('DRAFT_CONTENT_LOSS_UNCHECKED');
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
  });

  it('refuses when the sibling parsed but carried no body text', async () => {
    vi.mocked(lib.run).mockResolvedValue(JSON.stringify({ draft: { message: { payload: { mimeType: 'text/plain' } } } }));
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'B', forkSiblingDraftId: 's:empty',
    });
    expect(result.content[0].text).toContain('DRAFT_CONTENT_LOSS_UNCHECKED');
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
  });

  it('lets acceptContentLoss override an unrunnable check too', async () => {
    vi.mocked(lib.run).mockRejectedValue(new Error('boom'));
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(ACK));
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'B', forkSiblingDraftId: 's:gone', acceptContentLoss: true,
    });
    expect(result.isError).toBeFalsy();
    expect(JSON.parse(result.content[0].text as string).contentLossCheck.status).toBe('unchecked');
  });

  it('degrades to a prose note when the write result is not a JSON object', async () => {
    vi.mocked(lib.run).mockResolvedValue(siblingGet('kept'));
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult('Draft updated.'));
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'd1', subject: 'S', body: 'kept', forkSiblingDraftId: 's:1',
    });
    // The note is prepended; gog's own output is kept verbatim beneath it.
    expect(result.content[0].text).toContain('contentLossCheck:');
    expect(result.content[1].text).toBe('Draft updated.');
  });

  // HAZARD A. The caller names the sibling; this server does not decide the
  // pair. Two unrelated drafts produce a total-divergence report, which is the
  // same shape a real fork produces — so the answer must never read as a
  // pairing verdict, and must point at the one tool that can issue one.
  it('never claims the sibling is a fork, however the bodies compare', async () => {
    vi.mocked(lib.run).mockResolvedValue(siblingGet('dentist appointment friday\ninsurance card is in the drawer'));
    const result = await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'r4303011157206680397', subject: 'Re: August schedule', body: 'Entirely unrelated invoice text.',
      forkSiblingDraftId: 's:unrelated',
    });
    const text = result.content[0].text as string;
    const parsed = JSON.parse(text.slice(text.indexOf('{')));
    expect(parsed.contentLossCheck.forkClaim).toBeNull();
    expect(parsed.contentLossCheck.forkClaimNote).toContain('gog_gmail_drafts_diff');
    expect(text).not.toMatch(/\bconfirmed\b/);
    expect(text).not.toMatch(/replaced draft|is a fork of/i);
  });

  it('is not offered on drafts_create — there is no earlier body to lose', async () => {
    const { tools } = await harness.client.listTools();
    const create = tools.find((t) => t.name === 'gog_gmail_drafts_create');
    const update = tools.find((t) => t.name === 'gog_gmail_drafts_update');
    expect(Object.keys(create!.inputSchema.properties ?? {})).not.toContain('forkSiblingDraftId');
    expect(Object.keys(update!.inputSchema.properties ?? {})).toContain('forkSiblingDraftId');
  });
});

// ===========================================================================
// CLAIMS CORRECTNESS — three things the reports asserted on evidence they did
// not have. Each of these is a sentence a caller acts on: "the update WAS
// written", "draft X no longer resolves", "these two drafts are the same
// message". Getting any of them wrong costs real text in a legal-adjacent
// correspondence, so each is pinned to the evidence that actually exists.
// ===========================================================================

// HAZARD A, through the real RPC path: two genuinely unrelated Apple Mail
// drafts — different subjects, different threadIds, no shared reply root — that
// agree on nothing but `Hi Jennifer,` / `Thanks,` / `Chris` /
// `Sent from my iPhone`. That is 4 lines and 43 characters of pure apparatus,
// and it used to clear all three lineage minimums and come back `confirmed`.
describe('gog_gmail_drafts_diff — boilerplate is never lineage', () => {
  const b64 = (s: string) => Buffer.from(s, 'utf8').toString('base64url');
  const appleDraft = (o: { draftId: string; messageId: string; subject: string; date: string; sentence: string }) =>
    JSON.stringify({
      draft: {
        id: o.draftId,
        message: {
          id: o.messageId, threadId: o.messageId, internalDate: o.date,
          payload: {
            mimeType: 'text/plain',
            headers: [
              { name: 'From', value: 'Chris Hall <chris@x.com>' },
              { name: 'Subject', value: o.subject },
              { name: 'Message-Id', value: `<${o.messageId}@apple.com>` },
              { name: 'X-Universally-Unique-Identifier', value: o.messageId.toUpperCase() },
            ],
            body: { data: b64(`Hi Jennifer,\n\n${o.sentence}\n\nThanks,\nChris\n\nSent from my iPhone`) },
          },
        },
      },
    });

  it('does not pair two unrelated notes that share only the greeting and the signature', async () => {
    const A = appleDraft({ draftId: 'rOLD', messageId: 'aaa1', subject: 'Tuesday pickup', date: '1000', sentence: 'Tuesday pickup at 5 works for me.' });
    const B = appleDraft({ draftId: 's:NEW', messageId: 'bbb2', subject: 'Orthodontist invoice', date: '2000', sentence: 'I paid the orthodontist invoice today.' });
    vi.mocked(lib.run).mockImplementation(async (args) => ({ rOLD: A, 's:NEW': B }[plain(args)[3]!]!));
    const result = await harness.callTool('gog_gmail_drafts_diff', { draftIdA: 'rOLD', draftIdB: 's:NEW' });
    const text = result.content[0].text as string;
    const parsed = JSON.parse(text);
    expect(parsed.forkPairing.verdict).toBe('none');
    expect(parsed.forkPairing.bodyAgreement.meetsThreshold).toBe(false);
    expect(parsed.forkPairing.bodyAgreement.sharedAuthoredLines).toBe(0);
    expect(parsed.forkPairing.bodyAgreement.sharedAuthoredChars).toBe(0);
    expect(parsed.forkPairing.bodyAgreement.boilerplateLinesIgnored).toEqual({ original: 4, candidate: 4 });
    expect(text).not.toContain('replaced draft');
    expect(text).not.toContain('All four signals are present');
    // The divergence report is a DIFFERENT question and stays honest: the
    // apparatus really is text both copies hold.
    expect(parsed.bodyDiff.sharedLineCount).toBe(4);
  });
});

describe('gog_gmail_drafts_diff — truncation reports its magnitude, and the cap is validated', () => {
  const b64 = (s: string) => Buffer.from(s, 'utf8').toString('base64url');
  const body = (tag: string, n: number) => JSON.stringify({
    draft: { id: tag, message: { id: tag, threadId: tag, internalDate: '1', payload: { mimeType: 'text/plain', headers: [], body: { data: b64(Array.from({ length: n }, (_, i) => `${tag}-${i}`).join('\n')) } } } },
  });

  beforeEach(() => {
    vi.mocked(lib.run).mockImplementation(async (args) => body(plain(args)[3]!, 500));
  });

  it('says how many lines each side actually held, not just that it truncated', async () => {
    const parsed = JSON.parse((await harness.callTool('gog_gmail_drafts_diff', { draftIdA: 'a', draftIdB: 'b' })).content[0].text);
    expect(parsed.bodyDiff.onlyInA).toHaveLength(200);
    expect(parsed.bodyDiff.truncated).toBe(true);
    // Without these the caller cannot tell 200-of-201 from 200-of-500, and the
    // whole point of the diff is deciding what to merge before an overwrite.
    expect(parsed.bodyDiff.onlyInACount).toBe(500);
    expect(parsed.bodyDiff.onlyInBCount).toBe(500);
    expect(parsed.bodyDiff.note).toContain('500');
  });

  it('rejects maxDiffLines 0 and negatives instead of printing an empty divergence report', async () => {
    const zero = await harness.callTool('gog_gmail_drafts_diff', { draftIdA: 'a', draftIdB: 'b', maxDiffLines: 0 });
    expect(zero.isError).toBe(true);
    const negative = await harness.callTool('gog_gmail_drafts_diff', { draftIdA: 'a', draftIdB: 'b', maxDiffLines: -1 });
    expect(negative.isError).toBe(true);
    const fractional = await harness.callTool('gog_gmail_drafts_diff', { draftIdA: 'a', draftIdB: 'b', maxDiffLines: 1.5 });
    expect(fractional.isError).toBe(true);
  });
});

describe('gog_gmail_drafts_list — the threading note is emitted once, not per row', () => {
  const rows = (n: number) => JSON.stringify({
    drafts: Array.from({ length: n }, (_, i) => ({ id: `r${i}`, messageId: `m${i}`, threadId: i % 2 === 0 ? `m${i}` : `t${i}` })),
  });

  it('carries both note variants at the top level and none on the rows', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult(rows(20)));
    const text = (await harness.callTool('gog_gmail_drafts_list', {})).content[0].text as string;
    const parsed = JSON.parse(text);
    for (const d of parsed.drafts) expect(d).not.toHaveProperty('threadingNote');
    expect(parsed.threadingNotes.rootsOwnThread).toContain('NEW conversation');
    expect(parsed.threadingNotes.inThread).toContain('existing thread');
    // The selector stays on the row, so the note still resolves per draft.
    expect(parsed.drafts[0].rootsOwnThread).toBe(true);
    expect(parsed.drafts[1].rootsOwnThread).toBe(false);
    // ~300 chars x 20 rows of a constant is a per-call token cost that carries
    // no information. Still exactly one gog spawn — hazard B was never the
    // issue here.
    expect(text.length).toBeLessThan(3000);
    expect(lib.run).not.toHaveBeenCalled();
  });
});

// A caller who believes "the update WAS written" may delete or overwrite the
// sibling that now holds the only copy of the lines the check just listed.
describe('gog_gmail_drafts_update — acceptContentLoss reports the write that ACTUALLY happened', () => {
  const b64 = (s: string) => Buffer.from(s, 'utf8').toString('base64url');
  const SIBLING = JSON.stringify({
    draft: { id: 's:sib', message: { id: 'm2', threadId: 'm2', payload: { mimeType: 'text/plain', body: { data: b64('kept line\nTHE PARAGRAPH ONLY THE SIBLING HAS.') } } } },
  });
  const call = () => harness.callTool('gog_gmail_drafts_update', {
    draftId: 'r43', subject: 'S', body: 'kept line', forkSiblingDraftId: 's:sib', acceptContentLoss: true,
  });

  it('says the write was ATTEMPTED AND FAILED when gog returned a plain error', async () => {
    vi.mocked(lib.run).mockResolvedValue(SIBLING);
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(errorResult('Error: gog: permission denied'));
    const result = await call();
    expect(result.isError).toBe(true);
    const text = result.content.map((c: { text?: string }) => c.text).join('\n');
    expect(text).not.toContain('WAS written');
    expect(text).toMatch(/FAILED/);
    expect(text).toMatch(/nothing was saved/i);
  });

  it('does not claim a write on the 404 path, where it also says the draft is gone', async () => {
    vi.mocked(lib.run).mockImplementation(async (args) => {
      const a = plain(args);
      if (a[2] === 'get') return SIBLING;
      if (a[2] === 'list') return JSON.stringify({ drafts: [{ id: 's:sib', messageId: 'm2', threadId: 'm2' }] });
      return JSON.stringify({ messages: [] });
    });
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(errorResult('Error: Google API error (404 notFound): Requested entity was not found.'));
    const result = await call();
    // A result that says the draft no longer exists AND that the update was
    // written is self-contradictory, and the caller acts on the second half.
    const text = result.content.map((c: { text?: string }) => c.text).join('\n');
    expect(text).toContain('DRAFT_FORKED');
    expect(text).not.toContain('WAS written');
    expect(text).toMatch(/FAILED/);
    expect(text).toMatch(/NOTHING WAS SAVED/i);
  });

  it('still says the update WAS written when the write succeeded', async () => {
    vi.mocked(lib.run).mockResolvedValue(SIBLING);
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(rawTextResult('{"draftId":"r43"}'));
    const result = await call();
    expect(result.isError).toBeFalsy();
    const parsed = JSON.parse(result.content[0].text as string);
    expect(parsed.contentLossCheck.written).toBe(true);
    expect(parsed.contentLossCheck.acknowledged).toBe(true);
    expect(parsed.contentLossCheck.note).toContain('WAS written');
  });
});

// `not listed` is not `does not exist`. The fork report's listing is capped at
// 20 by construction (it is a failure path and must not grow with the mailbox),
// so on a mailbox with more drafts than that, absence of evidence was becoming
// the fork story by default — and sending the caller hunting for a replacement
// that does not exist is exactly the cost this report was built to avoid.
describe('gog_gmail_drafts_update — DRAFT_FORKED states what its listing can and cannot show', () => {
  const NOT_FOUND = 'Error: Google API error (404 notFound): Requested entity was not found.';
  const fullWindow = JSON.stringify({
    drafts: Array.from({ length: 20 }, (_, i) => ({ id: `r${i}`, messageId: `m${i}`, threadId: `t${i}` })),
  });
  const shortWindow = JSON.stringify({ drafts: [{ id: 'r1', messageId: 'm1', threadId: 't1' }] });

  function stub(list: string): void {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(errorResult(NOT_FOUND));
    vi.mocked(lib.run).mockImplementation(async (args) => {
      const a = plain(args);
      if (a[2] === 'list') return list;
      return JSON.stringify({ messages: [] });
    });
  }
  const parse = (result: { content: Array<{ text?: string }> }) => {
    const text = result.content[0].text as string;
    return { text, parsed: JSON.parse(text.slice(text.indexOf('{'))) };
  };

  it('does not assert the draft is gone when the 20-draft window came back FULL', async () => {
    stub(fullWindow);
    const { text, parsed } = parse(await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'rSTILL_EXISTS_BUT_RANK_25', subject: 'S', body: 'B',
    }));
    expect(text).not.toMatch(/no longer resolves/);
    expect(parsed.listingEvidence.basis).toBe('capped-listing');
    expect(parsed.listingEvidence.windowSize).toBe(20);
    expect(parsed.listingEvidence.draftsListed).toBe(20);
    expect(parsed.listingEvidence.note).toMatch(/not evidence|does not establish/i);
    expect(parsed.listingEvidence.note).toContain('gog_gmail_drafts_list');
  });

  it('does assert it when the listing came back SHORT of the window, so it covered the folder', async () => {
    stub(shortWindow);
    const { text, parsed } = parse(await harness.callTool('gog_gmail_drafts_update', { draftId: 'rGONE', subject: 'S', body: 'B' }));
    expect(text).toMatch(/no longer resolves/);
    expect(parsed.listingEvidence.basis).toBe('complete-listing');
    expect(parsed.listingEvidence.draftsListed).toBe(1);
  });

  it('claims nothing about the draft when the listing itself failed', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValueOnce(errorResult(NOT_FOUND));
    vi.mocked(lib.run).mockRejectedValue(new Error('gog timed out after 30s'));
    const { text, parsed } = parse(await harness.callTool('gog_gmail_drafts_update', { draftId: 'rUNKNOWN', subject: 'S', body: 'B' }));
    expect(text).not.toMatch(/no longer resolves/);
    expect(parsed.listingEvidence.basis).toBe('listing-unavailable');
    expect(parsed.listingEvidence.note).toMatch(/failed/i);
  });

  // The branch that CANNOT confirm the fork story was also the one whose
  // explanations omitted the leading alternative the caller literally handed it.
  it('carries the reply target and names it as an explanation', async () => {
    stub(fullWindow);
    const { parsed } = parse(await harness.callTool('gog_gmail_drafts_update', {
      draftId: 'rUNSEEN', subject: 'S', body: 'B', replyToThreadId: 'STALE-THREAD',
    }));
    expect(parsed.replyTarget).toEqual({ via: 'replyToThreadId', target: 'STALE-THREAD' });
    expect(parsed.otherExplanations.join(' ')).toMatch(/replyToThreadId=STALE-THREAD/);
    expect(parsed.otherExplanations.join(' ')).toMatch(/not the draft|reply target/i);
  });

  it('omits the reply-target explanation when the call named no target', async () => {
    stub(shortWindow);
    const { parsed } = parse(await harness.callTool('gog_gmail_drafts_send', { draftId: 'rGONE' }));
    expect(parsed.replyTarget).toBeNull();
    expect(parsed.otherExplanations.join(' ')).not.toMatch(/reply target/i);
  });
});

// SEC-3/SEC-4: every model-supplied server path must resolve inside an
// operator-configured root (GOG_FILE_ROOTS). The suite runs with '/' so the
// arg-shape tests can use any path; these narrow it.
async function withFileRoots<T>(roots: string, fn: () => Promise<T>): Promise<T> {
  const prev = process.env.GOG_FILE_ROOTS;
  process.env.GOG_FILE_ROOTS = roots;
  try {
    return await fn();
  } finally {
    process.env.GOG_FILE_ROOTS = prev;
  }
}

describe('server paths and disk writes (SEC-3/SEC-4/SEC-6)', () => {
  it.each([
    ['gog_gmail_attachment', { messageId: 'm1', attachmentIndex: 0, name: 'a.pdf', deliver: 'off', out: '/Users/me/Library/LaunchAgents/x.plist' }, 'out'],
    ['gog_gmail_drafts_create', { subject: 's', body: 'b', attach: ['/Users/me/.config/gogcli/credentials.json'] }, 'attach'],
    ['gog_gmail_drafts_create', { subject: 's', body: 'b', bodyHtmlFile: '/etc/passwd' }, 'bodyHtmlFile'],
    ['gog_gmail_drafts_reply', { messageId: 'm1', body: 'b', attach: ['/etc/passwd'] }, 'attach'],
    // gog splits drafts create|update --attach on ',' (#1190): every segment is confined.
    ['gog_gmail_drafts_create', { subject: 's', body: 'b', attach: ['/srv/gog-files/decoy.txt,/Users/me/.ssh/id_rsa'] }, 'attach'],
    ['gog_gmail_drafts_update', { draftId: 'd1', subject: 's', body: 'b', attach: ['/srv/gog-files/a,/proc/self/environ'] }, 'attach'],
    ['gog_gmail_import', { file: '/etc/passwd' }, 'file'],
    ['gog_gmail_drafts_create', { subject: 's', body: 'b', signatureFile: '/etc/passwd' }, 'signatureFile'],
    ['gog_gmail_drafts_update', { draftId: 'd1', subject: 's', body: 'b', signatureFile: '/etc/passwd' }, 'signatureFile'],
    ['gog_gmail_drafts_forward', { messageId: 'm1', signatureFile: '/etc/passwd' }, 'signatureFile'],
    ['gog_gmail_forward', { messageId: 'm1', to: 'a@b.com', signatureFile: '/etc/passwd' }, 'signatureFile'],
  ] as Array<[string, Record<string, unknown>, string]>)('%s refuses %j outside the roots', async (tool, args, param) => {
    const result = await withFileRoots('/srv/gog-files', () => harness.callTool(tool, args));
    expect(result.isError).toBe(true);
    expect(result.content[0].text).toMatch(new RegExp(`${param} ".*" is outside the directories`));
    expect(lib.run).not.toHaveBeenCalled();
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
  });

  it('gog_gmail_drafts_reply keeps a comma inside one attach path (gog reply does not split --attach)', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue({ content: [{ type: 'text', text: '{}' }] });
    const result = await withFileRoots('/srv/gog-files', () => harness.callTool('gog_gmail_drafts_reply', {
      messageId: 'm1', body: 'b', attach: ['/srv/gog-files/Report, final.pdf'],
    }));
    expect(result.content[0].text).not.toMatch(/is outside the directories/);
    expect(lib.runOrDiagnose).toHaveBeenCalled();
  });

  it('gog_gmail_attachment is not advertised as read-only, and is marked destructive', async () => {
    const { tools } = await harness.client.listTools();
    const tool = tools.find((t) => t.name === 'gog_gmail_attachment')!;
    expect(tool.annotations?.readOnlyHint).not.toBe(true);
    expect(tool.annotations?.destructiveHint).toBe(true);
  });

  it.each(['gog_gmail_thread_get', 'gog_gmail_thread_attachments', 'gog_gmail_drafts_get'])(
    '%s stays read-only now that it no longer downloads',
    async (name) => {
      const { tools } = await harness.client.listTools();
      expect(tools.find((t) => t.name === name)!.annotations?.readOnlyHint).toBe(true);
    },
  );

  it('gog_gmail_thread_get ignores a stale download/outDir and only reads', async () => {
    for (const args of [{ download: true }, { outDir: '/tmp/x' }]) {
      vi.mocked(lib.runOrDiagnose).mockClear();
      await harness.callTool('gog_gmail_thread_get', { threadId: 't1', ...args });
      expect(lib.runOrDiagnose).toHaveBeenCalledWith(
        ['gmail', 'thread', 'get', pos('t1'), '--use-indexed-attachment-ids=false'],
        { account: undefined },
      );
    }
  });

  // QUAL-2: always-refused inputs cost schema tokens on every listing and
  // invite the model to try them.
  it.each(['gog_gmail_thread_get', 'gog_gmail_thread_attachments', 'gog_gmail_drafts_get'])(
    '%s advertises no dead download/outDir inputs',
    async (name) => {
      const { tools } = await harness.client.listTools();
      const props = (tools.find((t) => t.name === name)!.inputSchema as { properties?: Record<string, unknown> }).properties ?? {};
      expect(Object.keys(props)).not.toContain('download');
      expect(Object.keys(props)).not.toContain('outDir');
    },
  );

  // SEC-6: the default download directory is private and swept, and a staging
  // copy nobody will read again is deleted once delivered.
  describe('download root hygiene', () => {
    const PNG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]).toString('base64');
    const stubDownload = (download: Record<string, unknown>) => {
      vi.mocked(lib.run).mockImplementation(async (args) => {
        if (plain(args)[1] === 'attachment') return JSON.stringify(download);
        if (plain(args)[1] === 'upload') return JSON.stringify({ file: { id: 'F', webViewLink: 'https://drive/x' } });
        return JSON.stringify({ attachments: [{ filename: 'p.png', mimeType: 'image/png', size: 8 }] });
      });
    };
    const defaultPath = `${lib.ATTACHMENT_DOWNLOAD_ROOT}/m1/p.png`;

    it('prepares (0700 + sweep) the private root before a default-path download', async () => {
      stubDownload({ path: defaultPath, bytes: 8, contentBase64: PNG });
      await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentIndex: 0, deliver: 'off' });
      expect(lib.prepareDownloadRoot).toHaveBeenCalledTimes(1);
    });

    it.each(['inline', 'drive'] as const)('deletes the staging copy after deliver="%s"', async (deliver) => {
      stubDownload({ path: defaultPath, bytes: 8, contentBase64: PNG });
      await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentIndex: 0, deliver });
      expect(lib.removeDownload).toHaveBeenCalledWith(defaultPath);
    });

    it('deletes an inline-rendered image under deliver="auto"', async () => {
      stubDownload({ path: defaultPath, bytes: 8, contentBase64: PNG });
      await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentIndex: 0 });
      expect(lib.removeDownload).toHaveBeenCalledWith(defaultPath);
    });

    it('keeps a file it returns BY PATH (deliver="off"), leaving it to the TTL sweep', async () => {
      stubDownload({ path: defaultPath, bytes: 8 });
      await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentIndex: 0, deliver: 'off' });
      expect(lib.removeDownload).not.toHaveBeenCalled();
    });

    it('never deletes or prepares anything for a caller-chosen out path', async () => {
      stubDownload({ path: '/srv/gog-files/p.png', bytes: 8, contentBase64: PNG });
      await harness.callTool('gog_gmail_attachment', { messageId: 'm1', attachmentIndex: 0, deliver: 'inline', out: '/srv/gog-files/p.png' });
      expect(lib.removeDownload).not.toHaveBeenCalled();
      expect(lib.prepareDownloadRoot).not.toHaveBeenCalled();
    });
  });
});
