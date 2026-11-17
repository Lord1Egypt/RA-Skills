import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createTestHarness, type TestHarness } from '@chrischall/mcp-utils/test';
import { rawTextResult, errorResult } from '@chrischall/mcp-utils';
import { blobStoreFromEnv, mintUploadSlot } from '@chrischall/mcp-utils/export';
import * as lib from '../../../gogcli-mcp/src/lib.js';
import type { GogArg, GogFileArg } from '../../../gogcli-mcp/src/lib.js';
import { registerExtraGmailTools } from '../../src/tools/gmail-extra.js';
import { installFakeBlobStore, type FakeBlobStore } from '../../../gogcli-mcp/tests/support/fake-blob-store.js';

vi.mock('../../../gogcli-mcp/src/lib.js', async (importOriginal) => {
  const actual = await importOriginal<typeof lib>();
  return { ...actual, runOrDiagnose: vi.fn() };
});

// blobKeys on the draft tools and gog_gmail_import: nothing here sends mail,
// so there is no gate — the blob is read, handed to gog as a temp file, and
// deleted only once gog succeeded.

const ORIGINAL_ENV = { ...process.env };
let fake: FakeBlobStore;
let harness: TestHarness;

beforeEach(async () => {
  vi.clearAllMocks();
  process.env = { ...ORIGINAL_ENV };
  delete process.env.MCP_DATA_DIR;
  process.env.GOG_FILE_ROOTS = mkdtempSync(join(tmpdir(), 'gmail-blobkeys-'));
  fake = installFakeBlobStore();
  vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult('{"draftId":"d1"}'));
  harness = await createTestHarness(registerExtraGmailTools);
});

afterEach(() => {
  process.env = ORIGINAL_ENV;
  vi.unstubAllGlobals();
});

function upload(filename: string, bytes: string): string {
  const key = mintUploadSlot(blobStoreFromEnv()!, { filename }).blobKey;
  fake.put(key, bytes);
  return key;
}

const lastArgs = () => vi.mocked(lib.runOrDiagnose).mock.calls.at(-1)![0] as GogArg[];
const fileArgs = (args: GogArg[]) => args.filter((a): a is GogFileArg => typeof a === 'object' && a.kind === 'file' && a.encoding === 'base64');

describe('draft tools + blobKeys', () => {
  it.each([
    ['gog_gmail_drafts_create', { subject: 'S', body: 'B' }],
    ['gog_gmail_drafts_update', { draftId: 'd1', subject: 'S', body: 'B' }],
    ['gog_gmail_drafts_reply', { messageId: 'm1', body: 'B' }],
    ['gog_gmail_drafts_reply_all', { messageId: 'm1', body: 'B' }],
  ] as const)('%s attaches the uploaded file and deletes it once the draft holds it', async (tool, args) => {
    const key = upload('photo.jpg', 'JPEGBYTES');
    const result = await harness.callTool(tool, { ...args, blobKeys: [key] });
    expect(result.isError).toBeFalsy();
    expect(fileArgs(lastArgs())).toEqual([expect.objectContaining({ flag: 'attach', filename: 'photo.jpg', contents: Buffer.from('JPEGBYTES').toString('base64') })]);
    expect(fake.deleted).toEqual([key]);
  });

  it('keeps the blob when the draft write fails', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(errorResult('Error: quota'));
    const key = upload('photo.jpg', 'JPEGBYTES');
    const result = await harness.callTool('gog_gmail_drafts_create', { subject: 'S', body: 'B', blobKeys: [key] });
    expect(result.isError).toBe(true);
    expect(fake.deleted).toEqual([]);
    expect(fake.blobs.has(key)).toBe(true);
  });

  it('refuses a foreign key before anything runs', async () => {
    const result = await harness.callTool('gog_gmail_drafts_create', { subject: 'S', body: 'B', blobKeys: ['other/k'] });
    expect(result.isError).toBe(true);
    expect(result.content[0]!.text).toMatch(/not an upload key/);
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
  });

  it('on a hosted deployment, an attach path is refused with the slot route', async () => {
    process.env.MCP_DATA_DIR = '/data';
    const result = await harness.callTool('gog_gmail_drafts_create', { subject: 'S', body: 'B', attach: ['/Users/someone/a.pdf'] });
    expect(result.isError).toBe(true);
    expect(result.content[0]!.text).toMatch(/server is remote.*gog_upload_slots/s);
  });
});

describe('gog_gmail_import + blobKeys', () => {
  it('imports the uploaded .eml as gog\'s positional file and deletes it after', async () => {
    vi.mocked(lib.runOrDiagnose).mockResolvedValue(rawTextResult('{"id":"i1"}'));
    const key = upload('message.eml', 'From: pat@example.com\r\n\r\nhi');
    const result = await harness.callTool('gog_gmail_import', { blobKeys: [key], labels: ['Archive'] });
    expect(result.isError).toBeFalsy();
    const args = lastArgs();
    expect(args.slice(0, 2)).toEqual(['gmail', 'import']);
    expect(args[2]).toMatchObject({ kind: 'file', positional: true, filename: 'message.eml' });
    expect(args).toContain('--label=Archive');
    expect(fake.deleted).toEqual([key]);
  });

  // The fake store makes this a hosted deployment, so a path must really exist
  // on the server (as one gog downloaded there would).
  const serverFile = () => {
    const path = join(process.env.GOG_FILE_ROOTS!, 'm.eml');
    writeFileSync(path, 'From: a');
    return path;
  };

  it('still takes a server path', async () => {
    const path = serverFile();
    await harness.callTool('gog_gmail_import', { file: path });
    expect(lastArgs()).toEqual(['gmail', 'import', lib.pos(path)]);
  });

  it('wants exactly one of file or blobKeys', async () => {
    const none = await harness.callTool('gog_gmail_import', {});
    expect(none.content[0]!.text).toMatch(/exactly one of file or blobKeys/);
    const key = upload('m.eml', 'x');
    const both = await harness.callTool('gog_gmail_import', { file: serverFile(), blobKeys: [key] });
    expect(both.content[0]!.text).toMatch(/exactly one/);
    expect(lib.runOrDiagnose).not.toHaveBeenCalled();
  });

  it('accepts at most one key', async () => {
    const result = await harness.callTool('gog_gmail_import', { blobKeys: [upload('a.eml', 'x'), upload('b.eml', 'y')] });
    expect(result.isError).toBe(true);
  });
});
