import { McpServer } from '@modelcontextprotocol/server';
import type { CallToolResult } from '@modelcontextprotocol/server';
import { z } from 'zod';
import { rawTextResult, textResult, errorResult, redactSecrets } from '@chrischall/mcp-utils';
import { accountParam, runOrDiagnose, run, diagnose, payloadArg, normalizeTimestamps, finalizeGmailSearch, fetchGmailPages, pageTokenParam, pageAliasParam, resolvePageToken, attachInlineParam, inlineAttachmentArgs, assertNotBoth, replySchema, appendReplyFlags, signatureSchema, appendSignatureFlags, confineSignatureFile, signaturePreview, attachmentDetails, blobStoreFromEnv, createBlobUrlMinter, uploadToBlobStore, ATTACHMENT_DOWNLOAD_ROOT, ATTACH_INLINE_ALTERNATIVE, assertOneFileSource, blobKeysParam, confineUploadPath, confineUploadPaths, readBlobFiles, releaseBlobs, singleBlobKeyParam, extractEmails, logGmailDispatch, requireGmailDispatchConfirmation, bodyPreview, attachmentNames, CONFIRM_FALLBACK_DESCRIPTION, confirmTokenParam, senderPreview, requireDispatchConfirmation, parseMetadataHeaders, pos, confinePath, prepareDownloadRoot, removeDownload } from '../../../gogcli-mcp/src/lib.js';
import type { BlobFile, GogArg, InlineAttachmentInput, BlobUrlMinter, BlobUploadOutcome, SignatureFlags } from '../../../gogcli-mcp/src/lib.js';
import { readDecodedMessage, escapeHtml, markdownToHtml, parseHeaders, headerValue, partMimeType, decodePartText, bestBodyText, firstInlineBody, applyTextPatch, composeBodyParts, storedBodyText, bodySha256, readerHeaders, confirmationSkippedFor, withConfirmSkippedNote, CONFIRM_SKIP_TO_ENV } from '../../../gogcli-mcp/src/lib.js';
import type { GmailHeader, GmailPayloadPart, GmailDraftMessage, GmailStoredMessage } from '../../../gogcli-mcp/src/lib.js';

// Body extraction moved to gogcli-mcp's src/gmail-mime.ts; re-exported so this
// package's callers (and its tests) keep their import path.
export { parseHeaders, headerValue, decodeTextBytes, partMimeType, decodePartText, decodeBase64UrlText, bestBodyText } from '../../../gogcli-mcp/src/lib.js';
export type { HeaderMap, GmailPayloadPart, GmailDraftMessage } from '../../../gogcli-mcp/src/lib.js';

// How many messages a forced batch delete names in its prompt; every id is still bound.
export const BATCH_DELETE_PREVIEW_MAX = 25;

// Pull the text out of a single-text-block tool result; undefined for any
// other shape (an error result is still a text block, so it parses below).
function resultText(result: CallToolResult): string | undefined {
  const first = result.content[0];
  return first?.type === 'text' ? first.text : undefined;
}

type GmailMessage = {
  id?: string;
  threadId?: string;
  internalDate?: string;
  labelIds?: string[];
  snippet?: string;
  payload?: { headers?: GmailHeader[] };
};

// Headers worth keeping in a snippets-only thread view.
const SNIPPET_HEADERS = ['From', 'To', 'Cc', 'Subject', 'Date'];

// Reduce a full Gmail message to a lightweight overview: id/labels/snippet plus
// the key envelope headers, dropping the raw MIME payload that dominates the
// size of a thread fetch.
function summarizeMessage(m: GmailMessage): Record<string, unknown> {
  const rawHeaders = m.payload?.headers;
  const headers: Record<string, string | undefined> = {};
  if (Array.isArray(rawHeaders)) {
    for (const h of rawHeaders) {
      if (h.name && SNIPPET_HEADERS.includes(h.name)) headers[h.name] = h.value;
    }
  }
  return {
    id: m.id,
    threadId: m.threadId,
    internalDate: m.internalDate,
    labelIds: m.labelIds,
    snippet: m.snippet,
    headers,
  };
}

// Wrapper-side trim of a `gog gmail thread get` JSON result: keep only the last
// `latestN` messages and/or reduce each to a snippet view. gog has no native
// message-limit flag, so this is done by post-processing its output. Any
// non-JSON output (an error, an unexpected shape) is passed through untouched.
function trimThread(
  result: CallToolResult,
  latestN: number | undefined,
  snippetsOnly: boolean | undefined,
): CallToolResult {
  try {
    const parsed = JSON.parse(resultText(result) ?? '') as { thread?: { messages?: unknown[] } };
    const messages = parsed.thread?.messages;
    if (!Array.isArray(messages)) return result;
    let trimmed: unknown[] = messages;
    if (latestN !== undefined) trimmed = trimmed.slice(-latestN);
    if (snippetsOnly) trimmed = trimmed.map((m) => summarizeMessage(m as GmailMessage));
    return rawTextResult(JSON.stringify({ ...parsed, thread: { ...parsed.thread, messages: trimmed } }));
  } catch {
    return result;
  }
}

// gog's own default for --inline-max-bytes (gmail_attachment.go:27,
// `default:"3145728"` at upstream-v0.35.0). Restated here so the wrapper can pin
// the flag on every call rather than let GOG_GMAIL_INLINE_MAX_BYTES decide.
const GOG_DEFAULT_INLINE_MAX_BYTES = 3145728;

// The most a caller may raise inlineMaxBytes to: 10 MiB of raw attachment bytes.
// mcp-host (the hosted runtime that runs this server for claude.ai) caps any
// single child result at 14 MiB of serialized JSON-RPC (CHILD_RESULT_MAX_BYTES,
// chrischall/mcp-host#952) and replaces anything larger with a generic "result
// too large" tool error; before #952 an oversized result killed the child
// process outright. 10 MiB raw is ~13.3 MiB as base64, which with the JSON-RPC
// envelope still fits under 14 MiB — so this bound applies first and the caller
// gets this tool's own too-large-to-inline answer instead of the host's.
// claude.ai itself accepts images up to 10 MB each (measured 2026-09-27).
//
// A larger request is CLAMPED, not rejected: above the ceiling gog already falls
// back to writing the file without inline bytes (auto → a file path, inline → a
// "too large to return inline" error pointing at url/drive), so clamping keeps
// that behaviour and never fails a drive/url/off call that merely passed a big
// number. The result carries a note saying the value was clamped.
export const MAX_INLINE_MAX_BYTES = 10 * 1024 * 1024;

// `gog gmail attachment --inline --json` emits base64 content when the attachment
// is within gog's inline cap (3 MiB by default, --inline-max-bytes), otherwise
// just the on-disk path plus a `reason` explaining the size fallback.
//
// `filename`/`mimeType` come from gog's own part lookup and are present whenever
// that lookup resolved the part — always in indexed mode, and by single-attachment
// fallback otherwise. They are absent when the opaque id missed against a message
// with several attachments, which is exactly the case resolveBySize exists for.
type InlineAttachment = {
  path?: string;
  bytes?: number;
  cached?: boolean;
  contentBase64?: string;
  reason?: string;
  filename?: string;
  mimeType?: string;
};

// One entry from `gog gmail get --json` `.attachments[]`: the message part
// metadata, carrying the TRUE filename and MIME type. `size` is the key the
// legacy path matches on — Gmail's `attachmentId` is NOT stable across calls
// (see resolveBySize); `attachmentIndex` is, which is why resolveByIndex exists.
// The two ids are mutually exclusive in gog's output: indexed mode emits the
// index INSTEAD of the id (`attachmentId,omitempty`).
type AttachmentMeta = {
  filename?: string;
  mimeType?: string;
  attachmentId?: string;
  attachmentIndex?: number;
  size?: number;
};

// MIME type by file extension — the download endpoint reports none, and the
// client needs it to render an inline image or label an embedded resource. Part
// metadata (authoritative) and a magic-byte sniff (below) backstop this.
const MIME_BY_EXT: Record<string, string> = {
  pdf: 'application/pdf',
  png: 'image/png',
  jpg: 'image/jpeg',
  jpeg: 'image/jpeg',
  gif: 'image/gif',
  webp: 'image/webp',
  svg: 'image/svg+xml',
  bmp: 'image/bmp',
  tiff: 'image/tiff',
  heic: 'image/heic',
  txt: 'text/plain',
  csv: 'text/csv',
  md: 'text/markdown',
  json: 'application/json',
  xml: 'application/xml',
  html: 'text/html',
  htm: 'text/html',
  ics: 'text/calendar',
  zip: 'application/zip',
  doc: 'application/msword',
  docx: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  xls: 'application/vnd.ms-excel',
  xlsx: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  ppt: 'application/vnd.ms-powerpoint',
  pptx: 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
};

// Reverse map for naming a part that carried no filename: MIME type → a canonical
// extension. Deliberate: a known type must never be saved as `*.bin`. Later
// entries win, so image/jpeg resolves to `jpeg` and text/html to `htm` — both fine.
const EXT_BY_MIME: Record<string, string> = Object.fromEntries(
  Object.entries(MIME_BY_EXT).map(([ext, mime]) => [mime, ext]),
);

// Lowercased extension of a filename, or '' if it has none.
function extOf(name: string): string {
  const dot = name.lastIndexOf('.');
  return dot >= 0 ? name.slice(dot + 1).toLowerCase() : '';
}

// Make a caller- or part-supplied name safe as a SINGLE path segment: no
// directory separators or traversal (it is interpolated into an --out path gog
// creates server-side), no control chars, bounded length.
//
// ORDER IS LOAD-BEARING, and it was wrong: the dot strip ran BEFORE the trim,
// so a leading space carried the dots past it and ' ..' came out as a literal
// '..'. (A leading TAB did not, only because it is a control char and is
// removed on the line above — which is precisely the kind of accident that
// makes the gap look closed.) A '.' or '..' segment is the one shape the
// gateway refuses outright rather than normalising, and the same string is
// gog's `--out`, so it also asks the upload to read a file outside the only
// root it will read from. Trim, THEN strip, then trim again so stripping the
// dots cannot expose whitespace of its own.
function sanitizeFilename(name: string): string {
  const base = name
    .replace(/[/\\]+/g, '_')
    // eslint-disable-next-line no-control-regex
    .replace(/[\x00-\x1f]/g, '')
    .trim()
    .replace(/^\.+/, '')
    .trim()
    .slice(0, 200);
  return base || 'attachment';
}

// Leading magic bytes → MIME type, for the common binary attachments.
const MAGIC_SIGNATURES: ReadonlyArray<readonly [string, string]> = [
  ['%PDF', 'application/pdf'],
  ['\x89PNG', 'image/png'],
  ['\xFF\xD8\xFF', 'image/jpeg'],
  ['GIF8', 'image/gif'],
];

// Does this string survive a base64 decode/re-encode round trip unchanged?
//
// The MCP SDK validates an image block's `data` and a resource block's `blob`
// against its own base64 schema, and a failure there is a PROTOCOL error
// (-32602 "Invalid Base64 string") — thrown past this tool's try/catch, so the
// caller gets a wire-level fault with no clue which attachment caused it and no
// suggestion of what to do instead. Checking here converts that into an ordinary
// tool result that can name the file and offer a working alternative.
//
// No try/catch: `Buffer.from(…, 'base64')` is total — it SKIPS characters it
// does not recognise rather than throwing, which is precisely why a bare decode
// cannot be used as the check and the re-encode comparison is required.
function isValidBase64(value: string): boolean {
  return Buffer.from(value, 'base64').toString('base64') === value;
}

// Sniff a MIME type from the leading bytes of standard base64; returns undefined
// for anything unrecognised.
//
// `atob` cannot throw here, and that is now ENFORCED rather than assumed: the
// caller drops `contentBase64` outright when isValidBase64 rejects it, so this
// only ever runs on a payload that round-trips — and any 4-aligned prefix of
// valid base64 is itself valid.
function sniffMime(base64: string): string | undefined {
  const head = atob(base64.slice(0, 16)); // 4-aligned slice; decodes to ~12 bytes
  for (const [signature, mimeType] of MAGIC_SIGNATURES) {
    if (head.startsWith(signature)) return mimeType;
  }
  return undefined;
}

// Resolve the real filename + MIME type from the message part metadata
// (`gog gmail get` `.attachments[]`), which the download endpoint doesn't return.
// A lightweight metadata read — no body bytes.
//
// The match is by SIZE, not attachmentId: Gmail's attachmentId is not stable
// across API calls (a fresh `get` re-issues a different id for the same part, as
// verified live), so the caller's id can't be matched against a fresh listing.
// The downloaded byte count is stable and, in practice, unique per message — so
// it identifies the part. An ambiguous (repeated) size yields undefined, and the
// caller falls back to a magic-byte sniff + a MIME-derived name.
async function resolveBySize(
  messageId: string,
  sizeBytes: number | undefined,
  account: string | undefined,
): Promise<AttachmentMeta | undefined> {
  if (sizeBytes === undefined) return undefined;
  try {
    const parsed = JSON.parse(await run(['gmail', 'get', pos(messageId)], { account })) as {
      attachments?: AttachmentMeta[];
    };
    const matches = (parsed.attachments ?? []).filter((a) => a.size === sizeBytes);
    return matches.length === 1 ? matches[0] : undefined;
  } catch {
    return undefined;
  }
}

// Resolve the part metadata for a 0-based attachment INDEX (gog >= 0.35.0). Unlike
// resolveBySize this is deterministic and needs no guessing: each part carries the
// index gog assigned it, so the lookup matches that DECLARED field rather than the
// array slot it happens to occupy. `collectAttachments` sets AttachmentIndex = i,
// so the two agree today — but they are different promises, and resolving by
// position would name the download after the wrong part on the day they diverge
// (#252).
//
// It also runs BEFORE the download rather than after, so the real filename can be
// handed to gog as --name/--out instead of the provisional `attachment` basename.
// Same one extra call as resolveBySize — it replaces it, it does not add to it.
async function resolveByIndex(
  messageId: string,
  index: number,
  account: string | undefined,
): Promise<AttachmentMeta | undefined> {
  try {
    const parsed = JSON.parse(
      await run(['gmail', 'get', pos(messageId), '--use-indexed-attachment-ids'], { account }),
    ) as { attachments?: AttachmentMeta[] };
    const attachments = parsed.attachments;
    if (!attachments) return undefined;
    // Match the DECLARED index, not the array slot. gog assigns
    // AttachmentIndex = i over the collected parts (gmail_attachments.go), so
    // the two agree today — but they are different promises, and resolveBySize
    // above already matches on a field rather than a position. If a listing
    // ever arrives filtered or reordered, position resolution does not fail, it
    // names the download after the WRONG part, which is worse than an error.
    const declared = attachments.find((a) => a.attachmentIndex === index);
    if (declared) return declared;
    // Nothing declared an index — an older gog, or a listing fetched without
    // --use-indexed-attachment-ids. Position is then the only reading of the
    // caller's number, and it is the one gog itself would apply.
    if (attachments.every((a) => a.attachmentIndex === undefined)) return attachments[index];
    // Some parts declared an index and none matched: the caller asked for an
    // index that is not in this message. Guessing by position here would be the
    // exact silent mis-naming this function exists to avoid.
    return undefined;
  } catch {
    return undefined;
  }
}

// A writable, ephemeral server-side output path, under `relDir` — one or more
// path segments naming this download. gog MkdirAll's the tree, and /tmp is
// writable everywhere this runs — unlike gog's default (the gogcli config dir),
// which on a hosted deployment's persistent data volume would accumulate
// downloaded attachments indefinitely.
//
// `ATTACHMENT_DOWNLOAD_ROOT` is ALSO the only directory `uploadToBlobStore` will
// read a file back from. That is load-bearing for deliver="url" and for nothing
// else — see blobOutPath.
//
// `relDir` is ALREADY-SANITIZED segments and this function does not re-sanitize:
// it is handed several of them for deliver="url" (`<messageId>/<attachmentRef>`),
// so collapsing separators here would weld the key's two segments into one and
// the path signed would stop matching the path written. Every caller owes it
// `sanitizeFilename` per segment — see `messageOutPath` and `blobOutPath`, which
// are the only two.
function defaultOutPath(relDir: string, filename: string): string {
  return `${ATTACHMENT_DOWNLOAD_ROOT}/${relDir}/${filename}`;
}

// Where every delivery mode OTHER than "url" lands its download: the message id
// as one sanitized segment.
//
// The id is the caller's string and gog MkdirAll's whatever it is told, so a raw
// `../../x` walked the write out of the attachment root — on a hosted deployment
// potentially into the data directory that holds gog's keyring and refresh token. deliver="url" was
// held to one segment from the start because its path and its object key have to
// be the same string, so the gap was visible there as a refused upload and
// invisible in the four modes that only write; the rule is the SAME rule
// (`sanitizeFilename`, once per segment) rather than a second one, because two
// spellings of "safe segment" is how the next mode gets missed.
function messageOutPath(messageId: string, fileName: string): string {
  return defaultOutPath(sanitizeFilename(messageId), fileName);
}

// Strip the command echo and any message/attachment ids from a gog failure before
// it reaches the caller. An execFile-style error message is
// `Command failed: gog gmail attachment <msg> <token> ...\n<stderr>` — leaking the
// full command line (opaque attachment token included) and a raw shell error such
// as `mkdir /home/claude: permission denied`. Keep only the stderr
// tail, with the ids redacted.
//
// `attachmentId` is undefined in indexed mode: the reference is then a small
// integer, which is neither secret nor safely substitutable — blind-replacing "0"
// would corrupt every number in the message.
function sanitizeAttachmentError(err: unknown, messageId: string, attachmentId: string | undefined): string {
  let msg = err instanceof Error ? err.message : String(err);
  msg = msg.replace(/^Command failed:.*(\n|$)/, ''); // drop the command echo line
  if (attachmentId) msg = msg.split(attachmentId).join('<attachment>');
  msg = msg.split(messageId).join('<message>');
  return msg.trim() || 'the download failed on the server';
}

// The attachment bytes as a native image block (so clients render them). A
// leading text block summarises the attachment for the model.
function inlineImageResult(summary: string, base64: string, mimeType: string): CallToolResult {
  return { content: [{ type: 'text', text: summary }, { type: 'image', data: base64, mimeType }] };
}

// The attachment bytes as an MCP embedded-resource blob. Only some hosts render
// or accept non-image resources (claude.ai currently rejects application/pdf),
// so this is reserved for the explicit deliver="inline" escape hatch — deliver
// "auto" never routes bytes the host would silently drop through here.
function inlineResourceResult(
  messageId: string,
  filename: string,
  summary: string,
  base64: string,
  mimeType: string,
): CallToolResult {
  return {
    content: [
      { type: 'text', text: summary },
      {
        type: 'resource',
        resource: { uri: `gmail-attachment://${messageId}/${filename}`, mimeType, blob: base64 },
      },
    ],
  };
}

// A file-path delivery: the bytes were written server-side and the caller reads
// them from `path`. Useful where the caller shares the filesystem (local stdio);
// a hosted caller asks for deliver="url" or "drive" instead.
function fileResult(
  path: string,
  fileName: string,
  mimeType: string,
  bytes: number | undefined,
): CallToolResult {
  return textResult({
    delivery: 'file',
    path,
    fileName,
    mimeType,
    bytes,
    note: 'Saved on the server filesystem — read it from `path`.',
  });
}

// Prepend an advisory note (e.g. why a caller-supplied `out` was ignored) to a
// result's content, or return it unchanged when there is nothing to say.
function withNote(result: CallToolResult, notes: string[]): CallToolResult {
  if (notes.length === 0) return result;
  return { ...result, content: [{ type: 'text', text: notes.join(' ') }, ...result.content] };
}

// Upload the file gog wrote (server-side, on the same box that ran the download)
// to Google Drive and return its metadata + shareable link. This is how a large
// or non-renderable attachment — one that can't come back inline —
// reaches the caller.
async function deliverViaDrive(
  path: string,
  name: string,
  driveFolder: string | undefined,
  account: string | undefined,
): Promise<CallToolResult> {
  const args: GogArg[] = ['drive', 'upload', pos(path), '--json'];
  if (driveFolder) args.push(`--parent=${driveFolder}`);
  args.push(`--name=${name}`); // callers always resolve a filename first
  // `gog drive upload --json` wraps the created file under a `file` key.
  const parsed = JSON.parse(await run(args, { account })) as {
    file?: { id?: string; name?: string; mimeType?: string; size?: number | string; webViewLink?: string };
  };
  const file = parsed.file ?? {};
  return textResult({
    deliveredVia: 'drive',
    note: 'Attachment delivered via Google Drive; open or download it at webViewLink.',
    id: file.id,
    name: file.name,
    mimeType: file.mimeType,
    size: file.size,
    webViewLink: file.webViewLink,
  });
}

// ===========================================================================
// deliver="url" — the attachment as a link anything can fetch.
//
// A hosted MCP has no HTTP surface of its own, which is why Drive delivery
// exists at all: it borrows Google's. The borrowed surface is a poor fit —
// a `webViewLink` needs a Google session, so an agent holding `curl` cannot
// spend it; a file lands in the user's Drive as a side effect of READING mail;
// and GOG_READONLY refuses the upload outright. mcp-host lends the surface
// directly instead: a per-registration blob store at `/b/<registrationId>/…`
// sitting OUTSIDE OAuth, where a signed URL is the entire access control.
//
// gog runs in this process tree, so `gog gmail attachment --out` wrote the file
// to this machine's disk and `uploadToBlobStore` streams it from there — the
// bytes never pass through this process's memory as a whole.
// ===========================================================================

// A thrown value as text. `String()` rather than the message alone on the other
// branch, because a rejected promise is not obliged to carry an Error — and the
// two call sites below are both reporting somebody else's failure.
function failureText(err: unknown): string {
  return err instanceof Error ? err.message : String(err);
}

// The two caller-supplied strings that address one attachment, as path
// segments — `<messageId>/<attachmentRef>`.
//
// `sanitizeFilename` is applied to both, because they are the CALLER's strings
// and the gateway REFUSES an empty, '.' or '..' segment rather than normalising
// it ("the bytes signed and the bytes used would be different strings") — a link
// minted for one could never be spent. One segment each, always.
//
// The REFERENCE is in it because a filename does not identify an attachment: two
// parts of one message routinely share one (two scans named IMG_0001.jpg, two
// invoice.pdf parts), so a key of message + name has the second call overwrite
// the first — and a link already handed to the agent for the first then serves
// the other's bytes, under the name and type the earlier answer reported. It is
// the reference and not the resolved index because that is what the caller
// named; an opaque attachmentId is not stable across Gmail API calls, so the
// legacy path mints a fresh key per call rather than a colliding one.
function attachmentKeySegments(messageId: string, attachmentRef: string): string {
  return `${sanitizeFilename(messageId)}/${sanitizeFilename(attachmentRef)}`;
}

// The object key for one attachment, under the registration's own prefix.
function blobObjectPath(messageId: string, attachmentRef: string, fileName: string): string {
  return `gmail/${attachmentKeySegments(messageId, attachmentRef)}/${fileName}`;
}

// Where a deliver="url" download must land on the server.
//
// This is the one delivery mode that reads the file back, and `uploadToBlobStore`
// confines `path` to `ATTACHMENT_DOWNLOAD_ROOT` — so the path is not the
// caller's to choose here, and an `out` is ignored (with a note).
//
// The segments are the SAME ones the object key is minted from, sanitized the
// same way, so the string gog is told to write and the string the upload is
// handed to read are one string. They were not: `defaultOutPath` interpolated
// the raw messageId while the key sanitized it, so a messageId of `../../x`
// minted a perfectly good key while asking the upload to read
// `/tmp/gog-attachments/../../x/attachment`, which it refuses.
function blobOutPath(messageId: string, attachmentRef: string, fileName: string): string {
  return defaultOutPath(attachmentKeySegments(messageId, attachmentRef), fileName);
}

// Resolve the minter for this registration's blob store, or the refusal to
// answer with instead. Called BEFORE the download: a `deliver="url"` that
// discovers its own impossibility afterwards has paid for a Gmail fetch, left a
// file on disk, and still has nothing to hand back.
function resolveBlobMinter(): BlobUrlMinter | CallToolResult {
  const store = blobStoreFromEnv();
  if (!store) {
    return errorResult(
      'deliver="url" needs the blob store an MCP host lends its child, and MCP_BLOB_BASE_URL is not set — ' +
      'this is a local (stdio) install, where nothing is serving HTTP on your behalf and so there is no link to ' +
      'hand you. Use deliver="auto" (a server-side file path you can read directly), deliver="inline" for the ' +
      'bytes themselves, or deliver="drive" for a Google Drive copy.',
    );
  }
  try {
    return createBlobUrlMinter(store);
  } catch (err) {
    // A configuration fault, named here rather than discovered as a 404 at the
    // gateway with nothing to point at. Neither message echoes the signing key.
    return errorResult(
      `deliver="url" cannot be served: ${failureText(err)}. ` +
      'MCP_BLOB_BASE_URL should be the `https://<host>/b/<registrationId>` this registration was handed at spawn.',
    );
  }
}

// Mint a write URL, stream the downloaded file to it, and hand back a read URL.
//
// GOG_READONLY does not reach this path, deliberately: that switch is the
// wrapper adding `--readonly` to a gog invocation, and it exists to stop writes
// to the USER'S Google account. Nothing here asks gog to write — the download
// is a read, and the bytes then move over HTTP into the host's own store — so
// this is the delivery mode that still works where deliver="drive" is blocked.
async function deliverViaBlobUrl(
  minter: BlobUrlMinter,
  messageId: string,
  attachmentRef: string,
  path: string,
  fileName: string,
  mimeType: string,
): Promise<CallToolResult> {
  const rest = blobObjectPath(messageId, attachmentRef, fileName);
  // The URL and the content type its signature COMMITS TO, together: the
  // gateway rebuilds the write payload from the PUT's own `Content-Type`
  // header, so a header that is dropped, defaulted or re-cased produces a
  // signature that does not verify — and the refusal reads as a missing object
  // rather than a wrong header.
  const target = minter.putUrl(rest, mimeType);
  let outcome: BlobUploadOutcome;
  try {
    outcome = await uploadToBlobStore({ path, url: target.url, contentType: target.contentType });
  } catch (err) {
    // The message comes from the upload client, which scrubs the URL and its
    // bare signature out of everything it throws. Nothing here puts them back.
    return errorResult(
      `The attachment downloaded, but storing it for download failed: ${failureText(err)}. ` +
      'Nothing was half-delivered — call this tool again for a fresh link, or use deliver="drive" to receive it ' +
      'through Google Drive instead.',
    );
  }
  // Minted AFTER the upload, so the link's lifetime starts when the bytes are
  // actually there — and the expiry is READ BACK off the URL rather than
  // recomputed, so what is reported is the instant the signature commits to.
  const url = minter.getUrl(rest);
  const expiresAt = new Date(Number(new URL(url).searchParams.get('exp'))).toISOString();
  return textResult({
    deliveredVia: 'url',
    note:
      'Fetch it with `curl` or any HTTP client — the link carries its own signature, so it needs no credential, ' +
      `no session and no Google account. It expires at ${expiresAt}; call this tool again for a fresh one.`,
    url,
    fileName,
    mimeType,
    // What was actually streamed: the size of the object now at that URL.
    bytes: outcome.bytes,
    expiresAt,
  });
}

// ===========================================================================
// APPLE MAIL DRAFT FORKS — shared signal primitives and the pairing verdict.
//
// A draft created by gog_gmail_drafts_create and then edited in a real mail
// client is not updated in place: Apple Mail writes a NEW draft and abandons
// the original. The id changes (a later update 404s), the reply headers are
// usually gone (sending starts a NEW conversation in front of every Cc'd
// recipient), and the two bodies diverge with NEITHER being a superset.
//
// Everything below is PURE — no gog invocation, no I/O. Cost decisions live
// with the callers; these functions only turn already-fetched fields into
// signals, so the N+1 budget is decided once, at the call site.
//
// THE HAZARD THIS CODE EXISTS FOR: telling a caller "draft X replaced draft Y"
// when it did not causes two unrelated messages to be merged, in
// legal-adjacent co-parenting correspondence with a parenting coordinator on
// Cc. A missed fork costs a re-check; a WRONG fork sends the wrong text to the
// wrong thread. So the verdict is deliberately biased toward precision, and it
// returns the evidence as a list the caller can judge rather than a bare
// boolean.
// ===========================================================================

/**
 * `api` = created through the Gmail API (what this server does).
 * `non-api` = arrived over IMAP/sync.
 *
 * NOT `apple-mail`. An `s:` prefix means "some IMAP/sync client wrote this" —
 * Thunderbird, Outlook-over-IMAP and Gmail offline all produce it too.
 * Upgrading `non-api` to `apple-mail` requires an actual Apple identity header
 * (see appleIdentitySignals), which costs a per-draft header fetch.
 *
 * Draft ids can be NEGATIVE (`r-457330811034304502` is a real API draft), so
 * this tests the `s:` prefix rather than matching `/^r\d/`.
 */
export type DraftOrigin = 'api' | 'non-api';

export function originFromDraftId(id: string): DraftOrigin {
  return id.startsWith('s:') ? 'non-api' : 'api';
}

/** The three fields `gog gmail drafts list` actually returns. That is all. */
export type DraftListEntry = { id?: string; messageId?: string; threadId?: string };

/**
 * True when the draft's threadId is its own messageId — i.e. it is the ROOT of
 * a new thread, so sending it starts a new conversation instead of replying.
 *
 * This is free (both fields are in the listing) and it is the CONSEQUENCE the
 * owner cares about. It is NOT a fork discriminator: the live probe measured
 * P(Apple | roots-own-thread) = 4/8 = 0.50, a coin flip.
 *
 * Absent fields yield `false`, not `true` — `undefined === undefined` would
 * otherwise report every field-less draft as rooting its own thread.
 */
export function rootsOwnThread(d: DraftListEntry): boolean {
  if (!d.messageId || !d.threadId) return false;
  return d.messageId === d.threadId;
}

/**
 * Apple identity headers found on a message, reported as `Name: value` strings
 * so the caller can read the evidence rather than trust a boolean.
 *
 * Proves only that APPLE WROTE THIS DRAFT. It says nothing about WHICH draft
 * it replaced — on its own it can never establish a pairing.
 *
 * `X-Uniform-Type-Identifier` counts only when it names an Apple type; the
 * header name alone is not evidence of the value it carries.
 */
export function appleIdentitySignals(headers: GmailHeader[] | undefined): string[] {
  const out: string[] = [];
  for (const h of headers ?? []) {
    const name = h.name ?? '';
    const lower = name.toLowerCase();
    const value = h.value ?? '';
    if (lower === 'x-uniform-type-identifier') {
      if (value.toLowerCase().startsWith('com.apple.')) out.push(`${name}: ${value}`);
      continue;
    }
    if (lower === 'x-universally-unique-identifier' || lower.startsWith('x-apple-')) {
      out.push(`${name}: ${value}`);
    }
  }
  return out;
}

/** `<ABC@gmail.com>` -> `ABC@gmail.com`. Case is preserved: RFC822 Message-Ids
 *  are case-sensitive, and lowercasing them would merge distinct ids. */
export function normalizeMessageId(v: string | undefined): string | undefined {
  const trimmed = v?.trim();
  if (!trimmed) return undefined;
  const stripped = trimmed.replace(/^</, '').replace(/>$/, '').trim();
  return stripped.length > 0 ? stripped : undefined;
}

/**
 * Every bracketed id in a References / In-Reply-To chain, bracket-stripped.
 * Bare unbracketed ids are deliberately ignored: an unparseable chain must
 * yield NO lineage rather than a guessed one.
 */
export function messageIdsIn(references: string | undefined): string[] {
  const matches = references?.match(/<[^<>\s]+>/g) ?? [];
  return matches.map((m) => m.slice(1, -1));
}

/** Whitespace-normalized, blank-stripped body lines. This is the unit of the
 *  DIVERGENCE report (what each copy would lose), where quoted lines are real
 *  content and must be kept: a merge that drops the quote block loses it.
 *
 *  It is NOT the unit of the lineage judgement — see authoredBodyLines. */
export function normalizeBodyLines(text: string | undefined): string[] {
  return (text ?? '')
    .replace(/\r\n?/g, '\n')
    .split('\n')
    .map((l) => l.replace(/\s+/g, ' ').trim())
    .filter((l) => l.length > 0);
}

/**
 * Jaccard overlap of ALL normalized body lines, 0..1 — quoted lines included.
 * Reported by the divergence and content-loss paths, which are asking "how
 * much of this text would I lose", a question the quote block is part of.
 *
 * NEVER use it as a lineage signal: two replies into the same thread quote the
 * same original, so this scores them high while proving nothing. measureBody-
 * Agreement is the lineage metric.
 *
 * An empty body on either side scores 0 — absence of content is absence of
 * evidence, never a match.
 */
export function bodySimilarity(a: string | undefined, b: string | undefined): number {
  const left = new Set(normalizeBodyLines(a));
  const right = new Set(normalizeBodyLines(b));
  if (left.size === 0 || right.size === 0) return 0;
  let shared = 0;
  for (const line of left) if (right.has(line)) shared += 1;
  return shared / (left.size + right.size - shared);
}

// ---------------------------------------------------------------------------
// AUTHORED TEXT vs QUOTING APPARATUS.
//
// Apple Mail quotes the original on reply BY DEFAULT, and writes an
// attribution line above the quote. Two unrelated replies into the same thread
// therefore share a large, byte-identical block — measured on a real pair, a
// 30-line quote under a 5-line reply scores 0.79 on whole-line Jaccard, well
// past the 0.60 threshold. Counting that as evidence pairs every two replies
// in a thread, which is the default shape of the mailbox this feature serves.
//
// So the lineage metric looks ONLY at lines neither draft quoted. The
// attribution line counts as apparatus, not authorship: it is generated from
// the quoted message, identically, by every client on every reply.
// ---------------------------------------------------------------------------

/** `On <anything> wrote:` — the attribution line Apple Mail and Gmail write
 *  above a quote. Anchored at both ends so ordinary prose ("On the whole I
 *  agree", "She wrote: bring the seat") is not swallowed. */
const QUOTE_ATTRIBUTION_LINE = /^On\b.*\bwrote:$/i;

/** `-----Original Message-----`, `---------- Forwarded message ---------`. */
const QUOTE_SEPARATOR_LINE = /^-{2,}\s*(original message|forwarded message)/i;

export function isQuotedBodyLine(line: string): boolean {
  return line.startsWith('>') || QUOTE_ATTRIBUTION_LINE.test(line) || QUOTE_SEPARATOR_LINE.test(line);
}

// ---------------------------------------------------------------------------
// CLIENT BOILERPLATE IS APPARATUS TOO.
//
// The property that disqualified quoted text — a mail client reproduces it
// identically on every message, whatever the message says — is just as true of
// the salutation, the closing formula, the name under it and the signature
// block. `Sent from my iPhone` is Apple Mail's OWN DEFAULT signature.
//
// Measured: `Hi Jennifer,` + `Thanks,` + `Chris` + `Sent from my iPhone` is 4
// lines and 43 characters, which cleared the 2-line and 40-character minimums
// on its own; and for two symmetric n-line drafts the similarity gate reduces
// to `shared >= 0.75n`, which 4-of-6 lines clears. So two genuinely unrelated
// one-sentence notes — different subjects, different threads, no shared reply
// root — paired as `confirmed`. Short confirmation plus a signature is the
// DOMINANT shape of the co-parenting mailbox this feature serves, so that was
// the default case, not a corner.
//
// Everything here is DELIBERATELY position-independent where it can be. A rule
// that strips `Best, Chris` only when it is the last line removes it from one
// copy of a message and keeps it in the other the moment one copy has a
// sentence after it — manufacturing divergence as readily as agreement. Only
// the two things that genuinely ARE positional stay positional: the salutation
// (first line) and a bare name (directly under a closing formula).
// ---------------------------------------------------------------------------

/** RFC 3676's `-- ` signature delimiter. normalizeBodyLines has already
 *  trimmed the trailing space by the time this runs. */
const SIGNATURE_DELIMITER_LINE = /^--$/;

/** The signature a mail CLIENT appends by itself, not the author. */
const CLIENT_SIGNATURE_LINE = /^(sent from my\b|sent from (mail|outlook|yahoo|windows)\b|sent via\b|get outlook for\b)/i;

/** A salutation. Consulted for the FIRST line only, so ordinary prose that
 *  happens to open with one of these words mid-body is left alone. Sentence
 *  punctuation rules it out: `Hi Jennifer,` is a greeting, `Hi — I paid the
 *  invoice. Details below.` is content. */
const GREETING_LINE = /^(hi|hello|hey|dear|good (morning|afternoon|evening)|greetings)\b[^.!?]{0,48}$/i;

/** A closing formula alone on its line: `Thanks,` `Best regards!` `Sincerely`. */
const SIGN_OFF_ALONE =
  /^(thanks|thanks again|thanks so much|thank you|thank you so much|many thanks|best|best regards|all the best|regards|kind regards|warmly|warm regards|sincerely|cheers|talk soon|speak soon|love|take care|appreciate it|respectfully|yours|yours truly|yours sincerely)[,.!]*$/i;

/** The same formula with the name on the SAME line — `Best, Chris`. The tail
 *  must still look like a name; `Thanks, I will send the invoice tomorrow` is a
 *  sentence and stays. */
const SIGN_OFF_WITH_NAME =
  /^(thanks|thank you|many thanks|best|best regards|all the best|regards|kind regards|warmly|warm regards|sincerely|cheers|love|take care|respectfully|yours)\s*[,\u2014\u2013-]\s*(.+)$/i;

/** A person's name on a line of its own: at most three words, no sentence
 *  punctuation. Deliberately narrow, and only ever consulted for the lines
 *  directly beneath a closing formula. */
const NAME_LINE = /^-{0,2}\s*\p{L}[\p{L}'\u2019.-]*(?:\s+\p{L}[\p{L}'\u2019.-]*){0,2}$/u;

/** A CONTACT line in a personal signature block: phone, email, URL, handle, or
 *  a short title/org line. Only ever consulted for the run directly beneath a
 *  closing formula, for the same reason NAME_LINE is.
 *
 *  This exists because a user-configured signature is not the client default.
 *  `boilerplateLineFlags` stripped the RFC 3676 `-- ` block and the client's own
 *  `Sent from my iPhone`, and it stripped the NAME under a sign-off — but the run
 *  stopped at the first line that was not name-shaped, so everything below the
 *  name survived as authored prose:
 *
 *      Thanks,                     -> stripped (sign-off)
 *      Chris Hall                  -> stripped (name-shaped)
 *      (704) 555-0142              -> NOT name-shaped, run stops here
 *      chris.c.hall@gmail.com      -> survived
 *      https://example.com/chris   -> survived
 *
 *  Those three lines are identical on every message this account composes, so
 *  two entirely unrelated drafts shared 3 authored lines / 61 chars and scored
 *  similarity 0.60 against a 0.60 threshold — `meetsThreshold: true` on a plumber
 *  note and a soccer note. Measured, not hypothesised. */
const CONTACT_LINE =
  /^(?:[+(]?\d[\d\s().-]{6,}|[^\s@]+@[^\s@]+\.[^\s@]+|(?:https?:\/\/|www\.)\S+|@[\w.]+)$/i;

function isNameLine(line: string): boolean {
  return !/[.!?:;]$/.test(line) && NAME_LINE.test(line);
}

function isSignOffLine(line: string): boolean {
  if (SIGN_OFF_ALONE.test(line)) return true;
  const withName = line.match(SIGN_OFF_WITH_NAME);
  return withName !== null && isNameLine(withName[2]!);
}

/** Which of these (already unquoted) lines are client boilerplate. */
function boilerplateLineFlags(lines: readonly string[]): boolean[] {
  const flags = lines.map(() => false);

  // The `-- ` delimiter and EVERYTHING under it is the signature block.
  const delimiter = lines.findIndex((l) => SIGNATURE_DELIMITER_LINE.test(l));
  if (delimiter !== -1) for (let i = delimiter; i < lines.length; i += 1) flags[i] = true;

  // Closing formulas and client signatures, wherever they sit.
  lines.forEach((line, i) => {
    if (isSignOffLine(line) || CLIENT_SIGNATURE_LINE.test(line)) flags[i] = true;
  });

  // The salutation — first line only.
  if (lines.length > 0 && GREETING_LINE.test(lines[0]!)) flags[0] = true;

  // The signature block directly under a closing formula, and only there:
  // `Thanks,` / `Chris Hall` / `(704) 555-0142` / `chris@example.com`.
  //
  // The run continues through NAME-shaped AND CONTACT-shaped lines. It used to
  // stop at the first non-name-shaped line, which meant a user-configured
  // signature (phone, email, URL under the name) survived as authored content —
  // identical on every message the account sends, and enough on its own to push
  // two unrelated drafts to `meetsThreshold: true`.
  //
  // It still stops at genuine prose, so a postscript under the sign-off is kept:
  // neither shape matches a sentence.
  lines.forEach((line, i) => {
    if (!isSignOffLine(line)) return;
    for (let j = i + 1; j < lines.length; j += 1) {
      const next = lines[j]!;
      if (!isNameLine(next) && !CONTACT_LINE.test(next)) break;
      flags[j] = true;
    }
  });

  return flags;
}

/** The normalized lines a draft actually WROTE: quoting apparatus AND client
 *  boilerplate removed. This is the unit of the LINEAGE judgement only — the
 *  divergence report still counts every line, because a merge that drops the
 *  signature really did drop it. */
export function authoredBodyLines(text: string | undefined): string[] {
  const unquoted = normalizeBodyLines(text).filter((l) => !isQuotedBodyLine(l));
  const flags = boilerplateLineFlags(unquoted);
  return unquoted.filter((_, i) => !flags[i]);
}

/** How many lines each filter removed, reported so the caller can redo the
 *  arithmetic rather than trust the verdict. */
function apparatusCounts(text: string | undefined): { quoted: number; boilerplate: number } {
  const all = normalizeBodyLines(text);
  const unquoted = all.filter((l) => !isQuotedBodyLine(l));
  return {
    quoted: all.length - unquoted.length,
    boilerplate: unquoted.length - authoredBodyLines(text).length,
  };
}

/** Overlap at or above this fraction of AUTHORED lines is one of the three
 *  conditions of the body-agreement lineage signal. */
export const FORK_BODY_SIMILARITY_THRESHOLD = 0.6;

/** ...and the agreement must rest on at least this many shared AUTHORED lines
 *  — after quoting AND client boilerplate are removed, so this is a count of
 *  substance. Kept at 2 deliberately: the comparison is line-based, and a
 *  single shared line can be a stock sentence two unrelated notes both use
 *  ("Let me know if that works for you."). Requiring two makes the agreement
 *  structural rather than coincidental. The cost is a real one — a genuine
 *  fork of a ONE-SENTENCE note comes back `candidate`, not `confirmed` — and
 *  that is the intended direction: a missed fork costs a re-check, a wrong one
 *  sends the wrong text to the wrong thread. `missing` names the shortfall in
 *  words so the caller can see exactly what was and was not found. */
export const FORK_MIN_SHARED_AUTHORED_LINES = 2;

/** ...totalling at least this many characters. `Ok.` + `Thanks.` is two lines
 *  and 10 characters: identical, and evidence of nothing. Real correspondence
 *  clears this on a single sentence. */
export const FORK_MIN_SHARED_AUTHORED_CHARS = 40;

const BODY_AGREEMENT_BASIS_NOTE =
  'Measured over lines NEITHER draft quotes AND that neither draft\'s mail client generated. Excluded as apparatus: quoted (`>`) ' +
  'lines, the `On ... wrote:` attribution, forward separators, the opening salutation, the closing formula, the name under it, ' +
  'and the signature block (an RFC 3676 `-- ` block, or a line like `Sent from my iPhone` — Apple Mail\'s own default). All of ' +
  'those are reproduced IDENTICALLY on every message a client composes, whatever the message says, so counting them pairs two ' +
  'unrelated short notes from one account: `Hi Jennifer,` + `Thanks,` + `Chris` + `Sent from my iPhone` alone is 4 lines and 43 ' +
  'characters. Lines are compared after collapsing runs of whitespace and dropping blanks, so a client that RE-WRAPPED a ' +
  'paragraph at a different width, or swapped straight quotes for curly ones, produces lines that no longer match and drives ' +
  'this number DOWN — a low score is weak evidence of absence.';

export type BodyAgreement = {
  /** Jaccard overlap of the two authored-line sets, 0..1. */
  similarity: number;
  similarityThreshold: number;
  sharedAuthoredLines: number;
  minSharedAuthoredLines: number;
  sharedAuthoredChars: number;
  minSharedAuthoredChars: number;
  /** How many lines were excluded as quoting apparatus on each side. */
  quotedLinesIgnored: { original: number; candidate: number };
  /** ...and how many as client boilerplate (salutation, closing formula, name,
   *  signature block). Reported separately from quoting so the caller can see
   *  which filter did the work. */
  boilerplateLinesIgnored: { original: number; candidate: number };
  /** True only when all three minimums are met. */
  meetsThreshold: boolean;
  basisNote: string;
};

/**
 * How much of what the two drafts actually WROTE (as opposed to quoted) is the
 * same text. Every input to the judgement is returned, not just the verdict,
 * so a caller can re-do the arithmetic.
 */
export function measureBodyAgreement(
  originalBody: string | undefined,
  candidateBody: string | undefined,
): BodyAgreement {
  const left = new Set(authoredBodyLines(originalBody));
  const right = new Set(authoredBodyLines(candidateBody));
  const shared = [...left].filter((line) => right.has(line));
  const similarity = left.size === 0 || right.size === 0
    ? 0
    : shared.length / (left.size + right.size - shared.length);
  const sharedAuthoredChars = shared.reduce((n, line) => n + line.length, 0);
  const originalApparatus = apparatusCounts(originalBody);
  const candidateApparatus = apparatusCounts(candidateBody);
  return {
    similarity,
    similarityThreshold: FORK_BODY_SIMILARITY_THRESHOLD,
    sharedAuthoredLines: shared.length,
    minSharedAuthoredLines: FORK_MIN_SHARED_AUTHORED_LINES,
    sharedAuthoredChars,
    minSharedAuthoredChars: FORK_MIN_SHARED_AUTHORED_CHARS,
    quotedLinesIgnored: { original: originalApparatus.quoted, candidate: candidateApparatus.quoted },
    boilerplateLinesIgnored: { original: originalApparatus.boilerplate, candidate: candidateApparatus.boilerplate },
    meetsThreshold: similarity >= FORK_BODY_SIMILARITY_THRESHOLD
      && shared.length >= FORK_MIN_SHARED_AUTHORED_LINES
      && sharedAuthoredChars >= FORK_MIN_SHARED_AUTHORED_CHARS,
    basisNote: BODY_AGREEMENT_BASIS_NOTE,
  };
}

/** `Chris Hall <Chris.C.Hall@Gmail.com>` -> `chris.c.hall@gmail.com`. */
export function normalizeFrom(v: string | undefined): string | undefined {
  const angled = v?.match(/<([^<>\s]+)>/);
  const addr = angled ? angled[1] : v?.trim();
  return addr ? addr.toLowerCase() : undefined;
}

/** `run()` + the timestamp repair `runOrDiagnose` would have applied.
 *
 *  These paths read gog JSON through bare `run()` because they parse it rather
 *  than hand it back verbatim — but the values they lift out (internalDate,
 *  internalDateIso) are then re-emitted to the caller, and skipping the seam
 *  meant they arrived without the explicit offset and without the `<field>Display`
 *  sibling every other tool in this repo returns. Two shapes of timestamp in one
 *  response, with nothing marking which is which, is the exact defect
 *  docs/timestamps.md exists to prevent. */
async function runNormalized(args: GogArg[], opts: { account?: string }): Promise<string> {
  return normalizeTimestamps(await run(args, opts));
}

/** Gmail's `internalDate` is epoch millis as a string. Anything else — absent,
 *  blank, non-numeric — is `undefined`, so ordering is reported as UNKNOWN
 *  rather than silently coerced (Number('') is 0, which would date a draft to
 *  1970 and make every other draft look newer). */
export function parseInternalDateMs(v: string | undefined): number | undefined {
  if (v === undefined || v.trim() === '') return undefined;
  const n = Number(v);
  return Number.isFinite(n) ? n : undefined;
}

/**
 * Signals that MUST NEVER establish a pairing on their own. Exported so tool
 * descriptions quote one canonical list instead of drifting copies — this is
 * caller-facing copy, not an internal comment.
 */
export const FORK_SIGNALS_THAT_NEVER_SUFFICE: readonly string[] = [
  'A draft id beginning `s:` means non-API (IMAP/sync) origin — Thunderbird, Outlook-over-IMAP and Gmail offline produce it too. It is not "Apple", and it is not "a fork".',
  'threadId === messageId means the draft roots its own thread. Measured on a live mailbox, P(Apple | roots-own-thread) was 4/8 = 0.50 — a coin flip. Report it as a consequence, never use it as a discriminator.',
  'An identical subject, even minutes apart. Same-subject same-sender drafts are routinely created deliberately; a subject+recency rule fires on all of them and is wrong every time. Subject can also be absent entirely.',
  'Any single X-Apple-* header. It proves Apple wrote THIS draft; it says nothing about WHICH draft it replaced.',
  'A UUID-shaped Message-Id, or `Mime-Version: 1.0 (1.0)`. The doubled form is iOS-only — macOS Mail writes `Mime-Version: 1.0 (Mac OS X Mail 16.0 ...)`, so its absence is not counter-evidence.',
  'Recency alone.',
  'A SHARED REPLY ROOT. Two drafts replying into the same conversation share one by construction, and in a mailbox whose threads are all with the same person that is nearly every pair of drafts. It links each draft to a common ANCESTOR — never the candidate to the original — so it is reported as corroboration and can never establish a pairing on its own.',
  'QUOTED TEXT. Body agreement is measured only over lines NEITHER draft quotes, because Apple Mail quotes the original on every reply: two unrelated replies into one thread carry the same 30-line block, which scores 0.79 on a whole-body line metric while proving nothing.',
  'GREETINGS, SIGN-OFFS AND SIGNATURE BLOCKS, for exactly the same reason as quoted text: a mail client reproduces them identically on every message whatever the message says. `Hi Jennifer,` + `Thanks,` + `Chris` + `Sent from my iPhone` is 4 lines and 43 characters of pure apparatus — enough, on its own, to clear a naive line-and-character threshold — and `Sent from my iPhone` is Apple Mail\'s own default signature. They are excluded from the lineage metric alongside quoting; the divergence report still counts them, because a merge that drops the signature really did drop it.',
  'THE COMPOSITE TRAP: `s:` prefix AND threadId === messageId together are still insufficient. Both are consequences of the same single fact (non-API origin) and neither references the supposed original. No pairing verdict without a lineage signal.',
  'Note the converse error too: a fork does NOT always lose its reply headers. A live Apple-authored draft was found carrying a full 5-deep References chain, so "Apple fork means threading is gone" must not be asserted anywhere.',
];

/** Which cost tier the facts were gathered at. 0 = fields already in
 *  `drafts list` (no extra spawn); 1 = one `messages search` fan-out; 2 = a
 *  per-draft header fetch, hard-capped at a named pair. */
export type ForkPairingTier = 0 | 1 | 2;

export type ForkPairingVerdict = 'confirmed' | 'candidate' | 'none';

/** Everything the verdict may look at. Fields are optional because which of
 *  them exist depends on the tier the caller paid for. */
export type DraftFacts = {
  draftId?: string;
  messageIdHeader?: string;
  inReplyTo?: string;
  references?: string;
  from?: string;
  subject?: string;
  internalDate?: string;
  bodyText?: string;
  /** From appleIdentitySignals — TIER 2 ONLY. */
  appleSignals?: string[];
};

export type ForkPairing = {
  verdict: ForkPairingVerdict;
  tier: ForkPairingTier;
  evidence: string[];
  missing: string[];
  /** Every number the LINEAGE decision rests on, so the threshold can be
   *  judged rather than trusted. */
  bodyAgreement: BodyAgreement;
  note: string;
};

function replyRoots(d: DraftFacts): string[] {
  const roots = messageIdsIn(d.references);
  const inReplyTo = normalizeMessageId(d.inReplyTo);
  if (inReplyTo) roots.push(inReplyTo);
  return roots;
}

function firstSharedRoot(a: DraftFacts, b: DraftFacts): string | undefined {
  const bRoots = new Set(replyRoots(b));
  for (const root of replyRoots(a)) if (bRoots.has(root)) return root;
  return undefined;
}

function label(d: DraftFacts): string {
  return d.draftId ?? '(unknown id)';
}

/**
 * Decide whether `candidate` replaced `original`, and SHOW THE WORK.
 *
 * Four independent requirements; `confirmed` needs all four:
 *   1. IDENTITY  — the candidate carries an Apple identity header (tier 2).
 *   2. LINEAGE   — a link from THE CANDIDATE to THE ORIGINAL. Exactly two
 *                  things qualify, and both point at the original itself:
 *                    (a) BACK-LINK: the original draft's own Message-Id appears
 *                        in the candidate's In-Reply-To/References; or
 *                    (b) BODY AGREEMENT: the text the two drafts WROTE (quoting
 *                        excluded) meets all three printed minimums.
 *                  A SHARED REPLY ROOT IS NOT LINEAGE. It links both drafts to
 *                  a common ancestor — the co-parent's message — which every
 *                  reply in the thread does. It is reported as corroboration
 *                  and can raise the answer no higher than a weak `candidate`.
 *   3. ORDERING  — the candidate is strictly newer.
 *   4. SAME FROM — both drafts are from the same address.
 *
 * Without LINEAGE the verdict can never be `confirmed`, no matter how many
 * other signals fire. That rule is what defeats the composite trap: origin,
 * thread-rooting, recency, Apple headers and a shared reply root are all
 * consequences of "Apple wrote this reply", and none of them mentions the
 * original. With lineage but not all four, the verdict is `candidate` and
 * `missing` names each absent signal in words.
 *
 * STRUCTURAL GUARANTEE: `confirmed` requires IDENTITY, identity signals can
 * only come from a tier-2 header fetch, and supplying them below tier 2 throws.
 * Therefore no tier-0/tier-1-only path can ever emit `confirmed`.
 */
export function evaluateForkPairing(
  original: DraftFacts,
  candidate: DraftFacts,
  tier: ForkPairingTier,
): ForkPairing {
  const signals = candidate.appleSignals ?? [];
  if (tier < 2 && signals.length > 0) {
    throw new Error(
      `evaluateForkPairing was given Apple identity signals at tier ${tier}, but identity headers ` +
      'can only come from a tier 2 per-draft header fetch. This is a wiring bug: a cheap listing path ' +
      'must never be able to produce a "confirmed" fork pairing.',
    );
  }

  const evidence: string[] = [];
  const missing: string[] = [];

  // ---- 2. LINEAGE (required for `confirmed`) ----
  const agreement = measureBodyAgreement(original.bodyText, candidate.bodyText);
  const originalMessageId = normalizeMessageId(original.messageIdHeader);
  let lineage = false;

  // (a) BACK-LINK. In-Reply-To as well as References: a client that re-threads
  //     onto the original draft writes the id into either one.
  if (originalMessageId !== undefined && replyRoots(candidate).includes(originalMessageId)) {
    evidence.push(
      `LINEAGE: the candidate's In-Reply-To/References cites the ORIGINAL DRAFT's own Message-Id <${originalMessageId}> — ` +
      'a link to the original itself, not to a shared ancestor',
    );
    lineage = true;
  }
  // (b) BODY AGREEMENT, on text neither draft quoted.
  if (agreement.meetsThreshold) {
    evidence.push(
      `LINEAGE: the two drafts agree on text NEITHER of them quotes — authored body line similarity ` +
      `${agreement.similarity.toFixed(2)} meets the ${FORK_BODY_SIMILARITY_THRESHOLD.toFixed(2)} threshold over ` +
      `${agreement.sharedAuthoredLines} shared line(s) / ${agreement.sharedAuthoredChars} characters`,
    );
    lineage = true;
  }
  // CORROBORATION ONLY. Reported because it is true and worth seeing, labelled
  // because on its own it is the mailbox's default state, not evidence.
  const sharedRoot = firstSharedRoot(original, candidate);
  if (sharedRoot) {
    evidence.push(
      `CORROBORATING ONLY (never a pairing on its own): both drafts reply into the same conversation — shared reply root ` +
      `<${sharedRoot}>. That links each draft to a common ANCESTOR, not the candidate to the original, and EVERY reply in ` +
      'that thread has it.',
    );
  }
  if (!lineage) {
    missing.push(
      `no lineage signal: the candidate's In-Reply-To/References does not cite the original draft's Message-Id, and the text ` +
      `the two drafts wrote rather than quoted does not agree (similarity ${agreement.similarity.toFixed(2)} vs the ` +
      `${FORK_BODY_SIMILARITY_THRESHOLD.toFixed(2)} threshold, ${agreement.sharedAuthoredLines} shared line(s) of ` +
      `${agreement.sharedAuthoredChars} characters vs the ${FORK_MIN_SHARED_AUTHORED_LINES}/${FORK_MIN_SHARED_AUTHORED_CHARS} ` +
      `minimums)${sharedRoot ? '. A shared reply root is corroboration, not lineage' : ''}`,
    );
  }

  // ---- 1. IDENTITY ----
  const identity = signals.length > 0;
  if (identity) evidence.push(`the candidate carries Apple identity header(s): ${signals.join('; ')}`);
  else missing.push('no Apple identity header on the candidate (X-Apple-*, X-Universally-Unique-Identifier, X-Uniform-Type-Identifier)');

  // ---- 3. ORDERING ----
  const originalMs = parseInternalDateMs(original.internalDate);
  const candidateMs = parseInternalDateMs(candidate.internalDate);
  let ordering = false;
  if (originalMs === undefined || candidateMs === undefined) {
    missing.push('internalDate is missing on one or both drafts, so it cannot be shown that the candidate is newer');
  } else if (candidateMs > originalMs) {
    ordering = true;
    evidence.push(`the candidate is newer (internalDate ${candidateMs} > ${originalMs})`);
  } else {
    missing.push(`the candidate is not newer than the original (internalDate ${candidateMs} <= ${originalMs})`);
  }

  // ---- 4. SAME FROM ----
  const originalFrom = normalizeFrom(original.from);
  const candidateFrom = normalizeFrom(candidate.from);
  let sameFrom = false;
  if (originalFrom === undefined || candidateFrom === undefined) {
    missing.push('From missing on one or both drafts');
  } else if (originalFrom === candidateFrom) {
    sameFrom = true;
    evidence.push(`same From (${originalFrom})`);
  } else {
    missing.push(`different From (${originalFrom} vs ${candidateFrom})`);
  }

  let verdict: ForkPairingVerdict;
  if (lineage) verdict = identity && ordering && sameFrom ? 'confirmed' : 'candidate';
  else if (sharedRoot !== undefined) verdict = 'candidate';
  else verdict = 'none';

  // Phrasing is load-bearing: `candidate` must read as a question, never as a
  // statement of fact, because a caller acting on it merges two messages.
  let note: string;
  if (verdict === 'confirmed') {
    note = `Draft ${label(candidate)} replaced draft ${label(original)}. All four signals are present — see evidence. Reconcile the bodies before sending: neither copy is guaranteed to be a superset of the other.`;
  } else if (verdict === 'candidate' && !lineage) {
    note = `Unconfirmed and WEAK: could draft ${label(candidate)} be a rewrite of draft ${label(original)}? The ONLY thing connecting them is that both reply into the same conversation, which every reply in that thread does — it places them under a common ancestor and says nothing about one coming from the other. Nothing here is a link back to draft ${label(original)}, and the text they did not quote does not agree. Read both bodies yourself; do not merge or send on the strength of this.`;
  } else if (verdict === 'candidate') {
    note = `Unconfirmed: could draft ${label(candidate)} be a rewrite of draft ${label(original)}? Something links them, but not everything a pairing needs — read "missing" and decide yourself. Do not merge or send on the strength of this alone.`;
  } else {
    note = `No lineage signal was found between draft ${label(candidate)} and draft ${label(original)}: neither cites the other and the text they did not quote does not agree. That is a failure to FIND evidence, not proof that they are unrelated — the comparison is line-based, so a client that re-wrapped the paragraphs or swapped in smart quotes can hide a real link. Read both bodies before concluding either way.`;
  }

  return {
    verdict,
    tier,
    evidence,
    missing,
    bodyAgreement: agreement,
    note,
  };
}


// BODY EXTRACTION lives in gogcli-mcp's src/gmail-mime.ts (shared with
// gog_gmail_get); the names are re-exported below for this package's callers.

// ---------------------------------------------------------------------------
// THE DIVERGENCE REPORT.
//
// In the observed fork a whole paragraph had been deleted in the mail client
// while the Gmail copy had later additions: NEITHER copy was a superset, and
// recreating from either alone lost work. That fact is the single most useful
// thing this feature can tell a caller, so it is a named field rather than
// something to be inferred from two lists.
// ---------------------------------------------------------------------------

/** Whether there was anything to compare. A body this server could not decode
 *  normalizes to zero lines, which is INDISTINGUISHABLE from an empty draft —
 *  so neither is allowed to produce a containment claim. */
export type BodyDiffComparability = 'compared' | 'a-unreadable' | 'b-unreadable' | 'both-unreadable';

export type BodySupersetClaim = 'a-superset-of-b' | 'b-superset-of-a' | 'identical' | 'neither' | 'not-assessed';

export type BodyDiff = {
  onlyInA: string[];
  onlyInB: string[];
  /** How many lines diverged IN TOTAL on each side, before the per-side cap.
   *  Without these, `truncated: true` and 200 printed lines cannot be told
   *  apart from 200-of-201 and 200-of-500 — and the whole point of the diff is
   *  deciding what to merge before an overwrite. Mirrors
   *  ContentLossCheck.linesOnlyInSiblingCount. */
  onlyInACount: number;
  onlyInBCount: number;
  sharedLineCount: number;
  similarity: number;
  comparability: BodyDiffComparability;
  supersetClaim: BodySupersetClaim;
  /** null when comparability !== 'compared': with one side unread, "neither is
   *  a superset" and "one is" are both unsupported, and `false` would read as
   *  the latter. */
  neitherIsSuperset: boolean | null;
  truncated: boolean;
  note: string;
};

/** Default cap on the per-side line lists. A diff is for a human to read; an
 *  uncapped one on a quoted 200-message thread is not. */
export const DRAFT_DIFF_MAX_LINES = 200;

export function diffBodyLines(a: string, b: string, maxLines: number): BodyDiff {
  const left = new Set(normalizeBodyLines(a));
  const right = new Set(normalizeBodyLines(b));
  const onlyInA = [...left].filter((line) => !right.has(line));
  const onlyInB = [...right].filter((line) => !left.has(line));
  const sharedLineCount = left.size - onlyInA.length;
  const truncated = onlyInA.length > maxLines || onlyInB.length > maxLines;

  // A side that yielded no lines was not READ, as far as anything here can
  // tell. Saying "every line of A is present in B" about it invites deleting
  // or overwriting A on the strength of a body this server never saw.
  let comparability: BodyDiffComparability = 'compared';
  if (left.size === 0) comparability = right.size === 0 ? 'both-unreadable' : 'a-unreadable';
  else if (right.size === 0) comparability = 'b-unreadable';

  let supersetClaim: BodySupersetClaim;
  let base: string;
  if (comparability !== 'compared') {
    supersetClaim = 'not-assessed';
    const which = comparability === 'both-unreadable' ? 'NEITHER draft yielded any body text'
      : comparability === 'a-unreadable' ? 'Draft A yielded no body text' : 'Draft B yielded no body text';
    base =
      `${which} (it normalized to zero lines), so NOTHING WAS COMPARED and no containment claim is ` +
      'made in either direction — in particular this does NOT say one draft\'s text is safely present in the other. The ' +
      'draft may genuinely be empty, or its text may sit in a MIME part this server could not decode; read it with ' +
      'gog_gmail_drafts_get before overwriting or deleting either copy.';
  } else if (onlyInA.length > 0 && onlyInB.length > 0) {
    supersetClaim = 'neither';
    base = 'NEITHER copy is a superset: each draft holds lines the other does not. Recreating from either one alone LOSES WORK — merge the two bodies by hand, then write the merged text back with gog_gmail_drafts_update.';
  } else if (onlyInA.length > 0) {
    supersetClaim = 'a-superset-of-b';
    base = 'Draft A is a superset of draft B: every line of B is present in A, and A has more.';
  } else if (onlyInB.length > 0) {
    supersetClaim = 'b-superset-of-a';
    base = 'Draft B is a superset of draft A: every line of A is present in B, and B has more.';
  } else {
    supersetClaim = 'identical';
    base = 'The two bodies are identical once whitespace and blank lines are normalized.';
  }

  return {
    onlyInA: onlyInA.slice(0, maxLines),
    onlyInB: onlyInB.slice(0, maxLines),
    onlyInACount: onlyInA.length,
    onlyInBCount: onlyInB.length,
    sharedLineCount,
    similarity: bodySimilarity(a, b),
    comparability,
    supersetClaim,
    neitherIsSuperset: comparability === 'compared' ? supersetClaim === 'neither' : null,
    truncated,
    note: truncated
      ? `${base} (Line lists truncated to ${maxLines} per side; ${onlyInA.length} line(s) diverged only in A and ` +
        `${onlyInB.length} only in B — onlyInACount/onlyInBCount are the true totals.)`
      : base,
  };
}

// ---------------------------------------------------------------------------
// TIER 0 — what a listing can say for FREE.
//
// `gog gmail drafts list` returns id, messageId and threadId. That is all. Both
// fields below are computed from those three, so enriching a 20-draft listing
// costs ZERO extra gog spawns. Anything that needs a
// header or a body needs a per-draft fetch and lives behind an explicit opt-in.
// ---------------------------------------------------------------------------

/** gog's own default for `gmail drafts list --max` (gmail_drafts.go,
 *  `GmailDraftsListCmd.Max`, `default:"20"` at upstream-v0.35.0). Restated so
 *  the enrichment search can be told to cover exactly the same window — its own
 *  default is 10, which would silently under-cover the listing. */
const GOG_DRAFTS_LIST_DEFAULT_MAX = 20;

export const DRAFT_LIST_ORIGIN_NOTE =
  '`origin` is derived from the draft id alone and costs nothing: `api` = created through the Gmail API (what this server does); ' +
  '`non-api` = the id begins `s:`, meaning the draft arrived over IMAP/sync. `non-api` is NOT a claim of "Apple Mail" — ' +
  'Thunderbird, Outlook-over-IMAP and Gmail offline produce `s:` ids too, and confirming Apple authorship needs an actual ' +
  'identity header, which only a per-draft fetch can see (gog_gmail_drafts_diff). `rootsOwnThread` is likewise a CONSEQUENCE, ' +
  'not a fork test: on a live mailbox P(Apple | rootsOwnThread) measured 4/8 = 0.50, a coin flip. Neither field, alone or together, ' +
  'establishes that one draft replaced another.';

// One of exactly TWO constants, so they ride along ONCE per result and the
// per-row `rootsOwnThread` boolean selects between them. Attaching the text to
// every row cost 8.9x the payload on a 20-draft listing (942 -> 8428 bytes) on
// the free path every caller takes, for zero extra information.
const DRAFT_ROOTS_OWN_THREAD_NOTE =
  'threadId equals this draft\'s own messageId, so the draft is the ROOT of a new thread: sending it starts a NEW conversation ' +
  'rather than replying, in front of every recipient including anyone on Cc. Normal for a draft composed from scratch — and also ' +
  'what a mail client\'s replacement of a previously threaded draft looks like.';

const DRAFT_IN_THREAD_NOTE =
  'threadId differs from this draft\'s messageId, so the draft sits inside an existing thread and sending it continues that ' +
  'conversation. (Whether it also carries In-Reply-To/References is not visible from a listing — that needs a per-draft fetch.)';

const DRAFT_ENRICH_COST_NOTE =
  'enrich spent ONE extra gog invocation (`gmail messages search in:drafts`), so the spawn cost is flat in the number of drafts. ' +
  'It is not free on the other axis: gog fans that one command out to one Gmail messages.get per matching draft at concurrency 10, ' +
  'so Google reads and wall-clock are linear in the result count. Narrow `max` before turning it on.';

/** One row of `gog gmail messages search --json`; only the fields the join needs. */
type EnrichedDraftMessage = {
  id?: string;
  from?: string;
  subject?: string;
  internalDateIso?: string;
  to?: string;
  cc?: string;
  bcc?: string;
  headers?: Record<string, string>;
};

/**
 * The addressing facts an enriched listing row carries: the recipient fields
 * as stored (omitted when empty), how many addresses they hold, whether there
 * are any, and whether the draft is a reply (In-Reply-To present). Answers
 * "is this draft still unaddressed?" for the whole listing in one call.
 */
export function draftRecipientFacts(m: EnrichedDraftMessage): Record<string, unknown> {
  const recipientCount = extractEmails(m.to, m.cc, m.bcc).length;
  return {
    ...(m.to ? { to: m.to } : {}),
    ...(m.cc ? { cc: m.cc } : {}),
    ...(m.bcc ? { bcc: m.bcc } : {}),
    recipientCount,
    hasRecipients: Boolean(m.to || m.cc || m.bcc),
    isReply: Boolean(m.headers?.['In-Reply-To']),
  };
}

// ---------------------------------------------------------------------------
// TIER 2 — a NAMED PAIR only, never a scan.
// ---------------------------------------------------------------------------

/** The per-draft facts the diff reports back. Deliberately excludes the body
 *  text itself: the body is reported once, as a diff, not twice verbatim. */
type DraftDiffSide = {
  draftId: string;
  messageId?: string;
  threadId?: string;
  origin: DraftOrigin;
  rootsOwnThread: boolean;
  subject?: string;
  from?: string;
  to?: string;
  cc?: string;
  internalDate?: string;
  messageIdHeader?: string;
  inReplyTo?: string;
  references?: string;
  appleIdentitySignals: string[];
  bodyLineCount: number;
};

function describeDraftSide(draftId: string, msg: GmailDraftMessage): { side: DraftDiffSide; facts: DraftFacts } {
  const headers = parseHeaders(msg.payload);
  const bodyText = bestBodyText(msg.payload);
  const side: DraftDiffSide = {
    draftId,
    messageId: msg.id,
    threadId: msg.threadId,
    origin: originFromDraftId(draftId),
    rootsOwnThread: rootsOwnThread({ id: draftId, messageId: msg.id, threadId: msg.threadId }),
    subject: headerValue(headers, 'Subject'),
    from: headerValue(headers, 'From'),
    to: headerValue(headers, 'To'),
    cc: headerValue(headers, 'Cc'),
    internalDate: msg.internalDate,
    messageIdHeader: headerValue(headers, 'Message-Id'),
    inReplyTo: headerValue(headers, 'In-Reply-To'),
    references: headerValue(headers, 'References'),
    appleIdentitySignals: appleIdentitySignals(msg.payload?.headers),
    // The DE-DUPLICATED count, matching diffBodyLines/evaluateContentLoss, which
    // compare Set members. Counting raw lines here broke the arithmetic a reader
    // naturally checks: onlyInACount + sharedLineCount === bodyLineCount only
    // holds when both sides count the same unit, and a body that repeats a line
    // (a divider, a blank-ish separator) made it not hold.
    bodyLineCount: new Set(normalizeBodyLines(bodyText)).size,
  };
  return {
    side,
    facts: {
      draftId,
      messageIdHeader: side.messageIdHeader,
      inReplyTo: side.inReplyTo,
      references: side.references,
      from: side.from,
      subject: side.subject,
      internalDate: side.internalDate,
      bodyText,
      appleSignals: side.appleIdentitySignals,
    },
  };
}

/**
 * The threading consequences, stated as sentences rather than left for the
 * caller to infer from two threadIds. This is the part of a fork that actually
 * hurts: the replacement sits on its own thread with no reply headers, so
 * sending it arrives as a new conversation in front of every Cc'd recipient.
 */
function threadingDifferences(a: DraftDiffSide, b: DraftDiffSide): string[] {
  const out: string[] = [];
  if (a.threadId !== b.threadId) {
    out.push(
      `The two drafts sit on different threadIds (${a.threadId ?? '(none)'} vs ${b.threadId ?? '(none)'}), so they are not the ` +
      'same conversation. Sending the one that roots its own thread starts a NEW conversation in front of every recipient, ' +
      'including anyone on Cc.',
    );
  }
  const aReplies = Boolean(a.inReplyTo ?? a.references);
  const bReplies = Boolean(b.inReplyTo ?? b.references);
  if (aReplies !== bReplies) {
    const withHeaders = aReplies ? a.draftId : b.draftId;
    const without = aReplies ? b.draftId : a.draftId;
    out.push(
      `Draft ${withHeaders} carries reply headers (In-Reply-To/References) and draft ${without} does not: only the first will ` +
      'arrive as a reply. gog_gmail_drafts_update with replyToThreadId re-threads a draft in place, keeping its id — but it ' +
      'also requires a full body, so reconcile the bodies below first.',
    );
  }
  if (out.length === 0) {
    out.push('No threading difference: the two drafts share a threadId and agree on whether they carry reply headers.');
  }
  return out;
}

// ---------------------------------------------------------------------------
// REQUIREMENT 4 — VERIFY THE THREADING gog ACTUALLY WROTE.
//
// The REPAIR already exists upstream and is not rebuilt here. On
// `gmail drafts update`, `--thread-id` sets replyToThreadID, so buildDraftMessage
// RESOLVES In-Reply-To/References from the thread's latest non-draft message,
// `Users.Drafts.Update("me", draftID, ...)` KEEPS the draft id, and
// writeDraftResult reports threadId/inReplyTo/references/replyContextSource
// (internal/cmd/gmail_drafts.go, upstream-v0.35.0). Adopting a mail client's
// replacement onto the original thread is therefore ONE call of an existing
// tool. What was missing is that nobody read gog's report back.
//
// THE SILENT CASE THIS CATCHES. fetchReplyInfo's thread branch has no "target
// has no Message-ID header" guard — the message-id branch does
// (internal/cmd/gmail_reply.go:79 vs :105) — so a thread whose latest non-draft
// message carries no Message-Id resolves NO lineage. And because an explicit
// reply target suppresses the carry-forward branch (gmail_drafts.go:967), the
// draft is MOVED onto the new thread and ends up with no reply headers at all:
// worse off than before the call, reported as a plain success.
//
// Zero extra gog invocations: every field read here is already in the write's
// own acknowledgement.
// ---------------------------------------------------------------------------

/** What the caller asked to happen to the draft's reply context. Mirrors
 *  appendDraftFlags' own precedence — replyToMessageId wins over
 *  replyToThreadId — so the verification can never describe a target gog was
 *  not given. */
export type ThreadingIntent =
  | { requested: 'set'; via: 'replyToMessageId' | 'replyToThreadId'; target: string }
  | { requested: 'clear' };

export function threadingIntentOf(f: {
  replyToMessageId?: string;
  replyToThreadId?: string;
  clearReplyContext?: boolean;
}): ThreadingIntent | undefined {
  if (f.replyToMessageId) return { requested: 'set', via: 'replyToMessageId', target: f.replyToMessageId };
  if (f.replyToThreadId) return { requested: 'set', via: 'replyToThreadId', target: f.replyToThreadId };
  if (f.clearReplyContext) return { requested: 'clear' };
  return undefined;
}

export type ThreadingVerification = {
  requested: 'set' | 'clear';
  via?: 'replyToMessageId' | 'replyToThreadId';
  target?: string;
  ok: boolean;
  effective: {
    threadId?: string;
    inReplyTo?: string;
    references?: string;
    replyContextSource?: string;
  };
  note: string;
};

// gog requires --body on EVERY update (draftComposeInput.validate,
// gmail_drafts.go:322: "required: --body, --body-file, --body-html, or
// --body-html-file"). There is no header-only edit, so re-threading and
// overwriting the body are the same operation — which is exactly the operation
// that can drop the paragraph living only in the sibling copy.
const BODY_OVERWRITE_CAVEAT =
  'gog requires a body on every update, so there is no header-only edit: this call REWROTE the whole body. If a sibling ' +
  'draft holds text this body does not, that text now exists only there — compare them with gog_gmail_drafts_diff before ' +
  'the next write.';

const VERIFICATION_PROVENANCE =
  'These are gog\'s own report of what it wrote, not an independent re-fetch, and they cost no extra gog invocation. ' +
  'To read the stored headers back from Gmail, use gog_gmail_raw with format=metadata on the draft\'s messageId.';

/**
 * Read gog's write acknowledgement back against what the caller asked for.
 *
 * `ok` is deliberately narrow: for a `set` it means gog reported an actual
 * In-Reply-To, and for a `clear` it means gog reported none. Everything else
 * the ack said is passed through under `effective` so the caller can judge the
 * claim rather than trust the boolean.
 */
export function verifyThreading(intent: ThreadingIntent, ack: Record<string, unknown>): ThreadingVerification {
  // gog writes an explicit JSON null for "no reply context" (nilIfEmpty,
  // gmail_drafts.go:551), so anything that is not a non-blank string is absent.
  const str = (name: string): string | undefined => {
    const v = ack[name];
    return typeof v === 'string' && v.trim() !== '' ? v : undefined;
  };
  const effective = {
    threadId: str('threadId'),
    inReplyTo: str('inReplyTo'),
    references: str('references'),
    replyContextSource: str('replyContextSource'),
  };
  const hasLineage = effective.inReplyTo !== undefined;
  const threadLabel = effective.threadId ?? '(none reported)';

  if (intent.requested === 'clear') {
    return {
      requested: 'clear',
      ok: !hasLineage,
      effective,
      note: hasLineage
        ? `WARNING: clearReplyContext was requested, but gog reports the draft STILL carries In-Reply-To ${effective.inReplyTo}. ` +
          `It has NOT been turned back into a standalone message. Re-read it before sending. ${VERIFICATION_PROVENANCE}`
        : `Reply context cleared: gog reports no In-Reply-To/References, so this draft will arrive as a standalone message. ` +
          `Its draft id and its threadId (${threadLabel}) are unchanged — dropping the headers does not move the draft out of ` +
          `the thread in Gmail's own UI, it only stops recipients' clients threading it. ${BODY_OVERWRITE_CAVEAT} ${VERIFICATION_PROVENANCE}`,
    };
  }

  return {
    requested: 'set',
    via: intent.via,
    target: intent.target,
    ok: hasLineage,
    effective,
    note: hasLineage
      ? `Threading applied and verified: gog reports the draft now replies to ${effective.inReplyTo}, on thread ${threadLabel}, ` +
        `with the draft id unchanged — it was updated in place, not recreated. See effective.references and ` +
        `effective.replyContextSource for the rest ("caller" means the lineage was resolved from the target you named, ` +
        `"carried" that it came from the draft's own stored headers). ${BODY_OVERWRITE_CAVEAT} ${VERIFICATION_PROVENANCE}`
      : `WARNING: ${intent.via} ${intent.target} was accepted, but gog reports NO reply headers at all (inReplyTo is null). ` +
        `The draft HAS been moved onto thread ${threadLabel}, so this was not a no-op — it simply will not arrive as a reply, ` +
        `because recipients' mail clients thread on In-Reply-To/References, not on Gmail's threadId. And an explicit reply ` +
        `target REPLACES the draft's own stored reply context rather than carrying it forward, so any lineage the draft had ` +
        `before this call is gone. Do not send it as a reply on this evidence. ${VERIFICATION_PROVENANCE}`,
  };
}

// Hang the verification off the result the caller is getting anyway. Additive,
// exactly like gog_gmail_drafts_list: gog's own fields are never removed or
// renamed. A result that is not JSON (gog's human table output, an error) keeps
// its text and gets the note prepended instead of being reshaped.
function withThreadingVerification(result: CallToolResult, verification: ThreadingVerification): CallToolResult {
  try {
    // String() rather than a nullish guard: a non-text result stringifies to
    // 'undefined', which is not valid JSON and lands in the same catch.
    const parsed = JSON.parse(String(resultText(result))) as Record<string, unknown>;
    return rawTextResult(JSON.stringify({ ...parsed, threadingVerification: verification }));
  } catch {
    return withNote(result, [`threadingVerification: ${verification.note}`]);
  }
}

// ---------------------------------------------------------------------------
// REQUIREMENT 5 — AN ADOPTION MUST NOT SILENTLY DROP THE OTHER COPY'S TEXT.
//
// `draftComposeInput.validate()` hard-requires a body on every update
// ("required: --body, --body-file, --body-html, or --body-html-file",
// internal/cmd/gmail_drafts.go:321 at upstream-v0.35.0). There is NO
// header-only edit. So re-threading a mail client's replacement back onto the
// original conversation is also a full body overwrite — precisely the
// operation that destroys the paragraph living only in the other copy. In the
// observed case NEITHER copy was a superset: the client copy had lost a
// paragraph, the Gmail copy had gained sentences, and writing either one over
// the other lost work.
//
// HAZARD B — COST. Opt-in, and exactly ONE extra gog invocation: a `drafts
// get` on the sibling the CALLER named. It never scans for a sibling, never
// grows with the mailbox, and with `forkSiblingDraftId` absent it spends
// nothing and changes no argv.
//
// HAZARD A — CLAIMS. This compares two bodies. That is the whole of it. Two
// unrelated drafts produce a total-divergence report, which is the same shape
// a genuine fork produces, so nothing here may read as "this replaced that" —
// only gog_gmail_drafts_diff weighs identity, lineage and ordering.
//
// FAIL CLOSED. A caller who names a sibling asked for a guard, so an
// un-runnable check (sibling unfetchable, unparseable, or carrying no readable
// body) refuses the write exactly as a detected loss does. An unrun check is
// not a passed check. `acceptContentLoss` is the single, explicit override for
// both.
// ---------------------------------------------------------------------------

export type ContentLossStatus = 'clean' | 'would-lose' | 'unchecked';

export type ContentLossCheck = {
  siblingDraftId: string;
  status: ContentLossStatus;
  siblingBodyLineCount: number;
  newBodyLineCount: number;
  linesOnlyInSibling: string[];
  linesOnlyInSiblingCount: number;
  truncated: boolean;
  similarity: number;
  /** Always null. Present so the absence of a pairing verdict is explicit in
   *  the payload rather than something the caller has to notice is missing. */
  forkClaim: null;
  forkClaimNote: string;
  note: string;
  /** Set only when the caller overrode a non-clean check with acceptContentLoss. */
  acknowledged?: boolean;
  /** ...and whether the write it authorised ACTUALLY SUCCEEDED. Only ever set
   *  alongside `acknowledged`, and only after the write has returned, because
   *  the one thing this field must never do is report a save that did not
   *  happen: a caller who believes the merged body is stored may delete or
   *  overwrite the sibling that now holds the only copy of the listed lines. */
  written?: boolean;
};

const CONTENT_LOSS_NO_CLAIM_NOTE =
  'This check compares two bodies and nothing else. It does not say that either draft replaced the other, and it cannot: YOU ' +
  'named this sibling, nothing here searched for it. Identical bodies would not prove a pairing and divergent bodies would not ' +
  'disprove one — a pairing verdict needs an identity header, a lineage link back to the original and an ordering, which is ' +
  'what gog_gmail_drafts_diff weighs and reports with its evidence.';

const CONTENT_LOSS_COMPARISON_NOTE =
  'Lines are compared after collapsing runs of whitespace and dropping blank lines, and only against the plain-text `body` you ' +
  'passed — a bodyHtml is not compared, and neither are attachments, recipients or the subject. The comparison is LINE-BASED: ' +
  'a copy whose paragraphs were re-wrapped at a different width, or whose straight quotes became curly ones, no longer matches ' +
  'line for line, so it can be reported as loss even though no words were dropped. Read the listed lines before deciding.';

/**
 * Which lines of the sibling draft the body about to be written does not
 * contain — i.e. what this update would leave existing only in the sibling.
 *
 * A sibling with no readable body is `unchecked`, never `clean`: reporting
 * "nothing would be lost" because nothing could be read is the one answer this
 * guard must never give.
 */
export function evaluateContentLoss(
  siblingDraftId: string,
  siblingBody: string,
  newBody: string,
  maxLines: number,
): ContentLossCheck {
  const siblingLines = new Set(normalizeBodyLines(siblingBody));
  const newLines = new Set(normalizeBodyLines(newBody));
  const missing = [...siblingLines].filter((line) => !newLines.has(line));
  const truncated = missing.length > maxLines;
  const base = {
    siblingDraftId,
    siblingBodyLineCount: siblingLines.size,
    newBodyLineCount: newLines.size,
    linesOnlyInSibling: missing.slice(0, maxLines),
    linesOnlyInSiblingCount: missing.length,
    truncated,
    similarity: bodySimilarity(siblingBody, newBody),
    forkClaim: null,
    forkClaimNote: CONTENT_LOSS_NO_CLAIM_NOTE,
  };

  if (siblingLines.size === 0) {
    return {
      ...base,
      status: 'unchecked',
      note:
        `No body text could be read from draft ${siblingDraftId}, so NOTHING WAS COMPARED and nothing is proven. The draft may ` +
        'genuinely be empty, or its text may sit in a MIME part this server could not decode. Read it with gog_gmail_drafts_get ' +
        `before overwriting draft text you cannot see. ${CONTENT_LOSS_COMPARISON_NOTE}`,
    };
  }

  if (missing.length === 0) {
    return {
      ...base,
      status: 'clean',
      note:
        `Every line of draft ${siblingDraftId} is already present in the body you passed, so this update leaves nothing behind ` +
        `in that copy. It says nothing about the reverse direction: lines of the draft being UPDATED that your body omits are ` +
        `overwritten regardless — this check cannot see them, because gog's write acknowledgement never returns the previous ` +
        `body. ${CONTENT_LOSS_COMPARISON_NOTE}`,
    };
  }

  return {
    ...base,
    status: 'would-lose',
    note:
      `WARNING: ${missing.length} line(s) of draft ${siblingDraftId} are NOT in the body you passed. gog requires a body on ` +
      'every update, so this call rewrites the WHOLE body — afterwards those lines exist only in that sibling draft. Merge them ' +
      'into the body and retry, or pass acceptContentLoss:true to write anyway.' +
      (truncated ? ` (Line list truncated to ${maxLines}; linesOnlyInSiblingCount is the true total.)` : '') +
      ` ${CONTENT_LOSS_COMPARISON_NOTE}`,
  };
}

/** The check could not be RUN — the sibling was unfetchable or unreadable.
 *  Deliberately the same shape and the same gate as a detected loss. */
export function unreadableSiblingCheck(siblingDraftId: string, reason: string): ContentLossCheck {
  return {
    siblingDraftId,
    status: 'unchecked',
    siblingBodyLineCount: 0,
    newBodyLineCount: 0,
    linesOnlyInSibling: [],
    linesOnlyInSiblingCount: 0,
    truncated: false,
    similarity: 0,
    forkClaim: null,
    forkClaimNote: CONTENT_LOSS_NO_CLAIM_NOTE,
    note:
      `Could not read draft ${siblingDraftId} to check what this update would overwrite: ${reason}. NOTHING WAS COMPARED, so ` +
      'nothing is proven. A draft id that has stopped resolving is itself worth noting — that is what a mail client leaves ' +
      'behind when it rewrites a draft instead of updating it.',
  };
}

/** ONE gog invocation, on the id the caller named. No scan, no fallback search. */
async function checkSiblingContentLoss(
  siblingDraftId: string,
  newBody: string,
  account: string | undefined,
): Promise<ContentLossCheck> {
  let raw: string;
  try {
    raw = await runNormalized(['gmail', 'drafts', 'get', pos(siblingDraftId), '--use-indexed-attachment-ids=false'], { account });
  } catch (err) {
    return unreadableSiblingCheck(siblingDraftId, String(err));
  }
  let message: GmailDraftMessage | undefined;
  try {
    message = (JSON.parse(raw) as { draft?: { message?: GmailDraftMessage } }).draft?.message;
  } catch {
    message = undefined;
  }
  if (!message) {
    return unreadableSiblingCheck(siblingDraftId, '`gog gmail drafts get` returned no `draft.message` object to read a body from');
  }
  return evaluateContentLoss(siblingDraftId, bestBodyText(message.payload), newBody, DRAFT_DIFF_MAX_LINES);
}

const CONTENT_LOSS_HOW_TO_PROCEED: readonly string[] = [
  'Merge the missing lines into your body and call gog_gmail_drafts_update again. The check re-runs, so a complete merge passes it.',
  'Run gog_gmail_drafts_diff on the two ids first if you want the full picture — it reports both directions of divergence, ' +
    'whether either body is a superset, how the threading differs, and (separately, with its evidence) whether there is enough ' +
    'to say one draft replaced the other.',
  'Pass acceptContentLoss:true to write this body as-is. The sibling draft is not touched either way, so the listed lines are ' +
    'still recoverable from it afterwards — but the draft you are updating loses whatever your body omits, permanently.',
  'Drop forkSiblingDraftId to skip the check entirely (and the one gog call it costs).',
];

function contentLossRefusal(draftId: string, check: ContentLossCheck): CallToolResult {
  const code = check.status === 'unchecked' ? 'DRAFT_CONTENT_LOSS_UNCHECKED' : 'DRAFT_CONTENT_LOSS';
  const headline =
    check.status === 'unchecked'
      ? `the content-loss check you asked for could not be run against draft ${check.siblingDraftId}`
      : `${check.linesOnlyInSiblingCount} line(s) of draft ${check.siblingDraftId} are missing from the body you passed`;
  const payload = {
    code,
    codeMeaning:
      check.status === 'unchecked'
        ? 'The named sibling could not be read, so the guard could not run. An unrun check is not a passed check, so the write was refused.'
        : 'The body passed would have dropped text the named sibling still holds, and gog rewrites the whole body on every update.',
    tool: 'gog_gmail_drafts_update',
    draftId,
    forkSiblingDraftId: check.siblingDraftId,
    whatHappened:
      `NOTHING WAS WRITTEN. Draft ${draftId} is byte-for-byte as it was: no body, subject, recipient, attachment or reply-header ` +
      `change was applied, and no gog write ran at all. ${headline}.`,
    contentLossCheck: check,
    howToProceed: CONTENT_LOSS_HOW_TO_PROCEED,
  };
  return errorResult(
    `${code}: nothing was written — ${headline}. gog requires a body on every draft update, so there is no header-only edit ` +
    'and the update would have rewritten the whole body.\n\n' +
    JSON.stringify(payload, null, 2),
  );
}

// Additive, like every other block this file hangs off a result: gog's own
// fields are never removed or renamed, and a non-JSON result keeps its text and
// gets the note prepended instead of being reshaped.
function withContentLossCheck(result: CallToolResult, check: ContentLossCheck): CallToolResult {
  try {
    const parsed = JSON.parse(String(resultText(result))) as Record<string, unknown>;
    return rawTextResult(JSON.stringify({ ...parsed, contentLossCheck: check }));
  } catch {
    return withNote(result, [`contentLossCheck: ${check.note}`]);
  }
}

// ---------------------------------------------------------------------------
// REQUIREMENT 1 — A 404 ON A DRAFT ID IS A REPORT, NOT A BARE notFound.
//
// A draft created here and then edited in a mail client is not updated in
// place: the client writes a NEW draft and abandons the original, so the id
// stops resolving and the next write returns `Google API error (404 notFound)`
// — which reads exactly like "your draft was deleted" and leaves the caller to
// rebuild the state by hand.
//
// HAZARD A DECIDES THE SHAPE. The 404'd draft cannot be fetched, so there is
// nothing left to establish LINEAGE against, and without lineage no pairing
// verdict is possible at any tier. This report therefore names NO replacement,
// ever. It reports what exists and hands over the one tool that can decide.
//
// HAZARD B DECIDES THE COST. At most 2 extra gog invocations, CONSTANT in the
// number of drafts, and only on a call that has already failed. A non-404
// failure spends nothing. Both are asserted by tests.
// ---------------------------------------------------------------------------

/** gog renders a Google 404 as `Google API error (404 notFound): ...`, or
 *  `Google API error (404): ...` when the error carries no reason
 *  (internal/errfmt/googleapi.go:63-66 at upstream-v0.35.0). The second
 *  alternative catches a 404 that reached us through some other rendering.
 *  Both require the literal 404: the word "notFound" alone never triggers it. */
const DRAFT_NOT_FOUND_PATTERN = /Google API error \(404\b|\b404\b[^\n]{0,40}not\s?found/i;

/** Hard cap on the fork report's candidate window. Constant by construction —
 *  this is a failure path and must not grow with the mailbox. */
const DRAFT_FORK_MAX_CANDIDATES = 20;

const DRAFT_FORK_CLAIM_NOTE =
  'This report names NO replacement, and cannot. The 404\'d draft can no longer be fetched, so there is nothing left to ' +
  'establish lineage against — no References citing it, no shared reply root, no body to compare — and without a lineage ' +
  'signal no pairing verdict is possible at any cost tier. The drafts below are simply the drafts that exist right now; ' +
  'ordering is presentation, not evidence. To decide whether one draft replaced another, name a PAIR and run ' +
  'gog_gmail_drafts_diff, which reads both sides\' headers and bodies.';

const DRAFT_FORK_OTHER_EXPLANATIONS: readonly string[] = [
  'The draft was deleted — by you, by a mail client, or by an earlier gog_gmail_drafts_delete. A deleted draft 404s identically.',
  'The draft was already sent. Sending consumes the draft, so its id stops resolving; check Sent before recreating anything.',
  'A mail client rewrote the draft instead of updating it in place, writing a NEW draft and abandoning this id. This is the ' +
    'only one of the three that strands text in two places, and the reason this report exists.',
];

/** The explanation that belongs FIRST whenever the caller passed a reply
 *  target: `gmail drafts update` resolves the draft, the thread behind
 *  --thread-id and the message behind --reply-to-message-id, and gog renders
 *  all three 404s with the identical string. GOOGLE_404_NOT_THE_DRAFT already
 *  treats this as the leading alternative when the draft IS listed; the branch
 *  that could NOT find the draft has strictly less evidence, so it must not be
 *  the one that stays silent about it. */
function replyTargetExplanation(replyTarget: ReplyTarget): string {
  return `The 404 may have been about your REPLY TARGET rather than the draft. You passed ${replyTarget.via}=${replyTarget.target}, ` +
    'and `gog gmail drafts update` resolves up to three different Google entities — the draft (Users.Drafts.Get/Update), the ' +
    'thread behind --thread-id and the message behind --reply-to-message-id — which gog renders with the IDENTICAL 404 string ' +
    '(internal/errfmt/googleapi.go). Thread ids and message ids are both 16-hex strings and are routinely confused, and a ' +
    'thread id copied from a stale record may simply no longer exist. Fetch it — gog_gmail_thread_get for a thread id, ' +
    'gog_gmail_get for a message id — before concluding anything about the draft.';
}

/** What the post-failure listing is actually able to say about the draft id.
 *  `absence of evidence` and `evidence of absence` are different answers, and
 *  only one of them is a fork story. */
type DraftListingBasis = 'complete-listing' | 'capped-listing' | 'listing-unavailable';

const DRAFT_LISTING_BASIS_NOTE: Record<DraftListingBasis, (draftId: string, listed: number) => string> = {
  'complete-listing': (draftId, listed) =>
    `The listing returned ${listed} draft(s) — FEWER than the ${DRAFT_FORK_MAX_CANDIDATES}-draft window it asked for, so it ` +
    `covers the whole Drafts folder. Draft ${draftId} really is not in the mailbox.`,
  'capped-listing': (draftId) =>
    `The listing came back FULL: ${DRAFT_FORK_MAX_CANDIDATES} drafts, which is the entire window it asked for, so it is ` +
    `TRUNCATED and draft ${draftId} could still exist beyond it. "Not listed here" is NOT evidence that the draft is gone — ` +
    'the window is capped by construction, because this is a failure path and must not grow with the size of the mailbox. ' +
    `Run gog_gmail_drafts_list with a larger max (or all:true) before concluding the draft forked.`,
  'listing-unavailable': (draftId) =>
    `The listing FAILED, so nothing here shows whether draft ${draftId} still exists. The 404 is the only evidence there is, ` +
    'and gog renders the draft, thread and message 404s identically. Run gog_gmail_drafts_list yourself before acting.',
};

const DRAFT_FORK_NEXT_STEPS: readonly string[] = [
  'Run gog_gmail_drafts_list — origin and rootsOwnThread cost nothing there — and look for a draft you did not create through this server.',
  'Name a PAIR and run gog_gmail_drafts_diff: it is the only path in this server that can issue a fork verdict, because it is ' +
    'the only one that reads both sides\' identity headers, reply lineage and bodies. It cannot be pointed at THIS id — a 404\'d ' +
    'draft cannot be fetched at all — so diff the survivor against another draft you still have.',
  'If a replacement lost its reply threading, re-thread it IN PLACE with gog_gmail_drafts_update replyToThreadId=<the original ' +
    'thread id>: the draft keeps its id and gog resolves In-Reply-To/References from that thread\'s latest message, reporting ' +
    'them back under threadingVerification. It requires a full body, so merge the two bodies FIRST — whatever you do not pass is lost.',
  'If the draft was deleted or already sent, nothing forked and there is nothing to reconcile.',
];

/** Tier-0 + tier-1 facts about the drafts that DO exist, for the fork report.
 *  Never more than 2 gog invocations, and it degrades rather than throwing: a
 *  failed lookup must not replace the explanation the caller came for. */
async function currentDraftsForForkReport(account: string | undefined): Promise<Record<string, unknown>> {
  let entries: DraftListEntry[];
  try {
    const listed = JSON.parse(
      await run(['gmail', 'drafts', 'list', `--max=${DRAFT_FORK_MAX_CANDIDATES}`], { account }),
    ) as { drafts?: unknown };
    if (!Array.isArray(listed.drafts)) throw new Error('`gog gmail drafts list` returned no drafts array');
    entries = listed.drafts as DraftListEntry[];
  } catch (err) {
    return {
      extraGogCalls: 1,
      listingBasis: 'listing-unavailable' satisfies DraftListingBasis,
      currentDraftsUnavailable:
        `Could not list the surviving drafts (${String(err)}), so this report names none. Run gog_gmail_drafts_list yourself — ` +
        'origin and rootsOwnThread are free there.',
    };
  }

  // Tier 1: ONE more invocation buys subject/from/date for every draft. Worth
  // it here because "which of these is mine" is unanswerable from three opaque
  // ids — but it is still one command that makes gog fetch each matching draft
  // server-side, so the cap above is what keeps that bounded.
  const byMessageId = new Map<string | undefined, EnrichedDraftMessage>();
  let enrichmentNote: string;
  try {
    const searched = JSON.parse(await runNormalized([
      'gmail', 'messages', 'search', 'in:drafts', `--max=${DRAFT_FORK_MAX_CANDIDATES}`,
      '--include-attachments=false', '--use-indexed-attachment-ids=false',
    ], { account })) as { messages?: EnrichedDraftMessage[] };
    if (!Array.isArray(searched.messages)) throw new Error('`gog gmail messages search in:drafts` returned no messages array');
    for (const m of searched.messages) {
      if (m.id) byMessageId.set(m.id, m);
    }
    enrichmentNote = DRAFT_ENRICH_COST_NOTE;
  } catch (err) {
    enrichmentNote =
      `subject, from and internalDateIso are missing: the single enrichment call failed (${String(err)}). The free fields ` +
      '(origin, rootsOwnThread) are unaffected.';
  }

  const currentDrafts = entries.map((d) => {
    const extra = byMessageId.get(d.messageId);
    return {
      ...d,
      origin: originFromDraftId(d.id ?? ''),
      rootsOwnThread: rootsOwnThread(d),
      subject: extra?.subject,
      from: extra?.from,
      internalDateIso: extra?.internalDateIso,
    };
  });
  // Newest first WHERE A DATE WAS AVAILABLE, and nowhere else: ISO strings sort
  // chronologically, and a missing date sorts last rather than winning by
  // accident. This is presentation only — forkClaimNote says so in words,
  // because "listed first" is exactly the kind of thing a caller reads as a
  // verdict.
  currentDrafts.sort((x, y) => (y.internalDateIso ?? '').localeCompare(x.internalDateIso ?? ''));

  // A window that came back FULL may have cut the mailbox off; one that came
  // back short covered all of it. That difference is the whole difference
  // between "the draft is gone" and "I did not see the draft".
  const listingBasis: DraftListingBasis =
    entries.length >= DRAFT_FORK_MAX_CANDIDATES ? 'capped-listing' : 'complete-listing';
  return { extraGogCalls: 2, listingBasis, currentDrafts, enrichmentNote };
}

/** Split the listing's self-assessment out of the rows it returned, so the
 *  basis can be reported as its own block rather than as a loose field. */
function splitListingBasis(report: Record<string, unknown>): { basis: DraftListingBasis; rest: Record<string, unknown> } {
  const { listingBasis, ...rest } = report;
  return { basis: listingBasis as DraftListingBasis, rest };
}

function draftForkedResult(
  tool: string,
  draftId: string,
  gogError: string,
  report: Record<string, unknown>,
  replyTarget: ReplyTarget | undefined,
): CallToolResult {
  const { basis, rest } = splitListingBasis(report);
  const listed = Array.isArray(rest.currentDrafts) ? rest.currentDrafts.length : 0;
  // ONLY a listing that covered the whole folder is entitled to the sentence
  // "the draft no longer resolves". A capped window that came back full, or a
  // listing that failed outright, has not looked everywhere — and treating
  // absence of evidence as the fork story sends the caller hunting for a
  // replacement that does not exist, and possibly recreating correspondence
  // that is already in the mailbox.
  const proven = basis === 'complete-listing';
  const whatHappened = proven
    ? `${tool} could not act on draft ${draftId}: Gmail no longer has a draft with that id, and a listing that covered the ` +
      'whole Drafts folder does not contain it either. Editing a draft in a real mail client does not update it in place — the ' +
      'client writes a NEW draft and abandons the original — so the id you were given stops resolving, the replacement usually ' +
      'sits on its OWN threadId with no In-Reply-To/References (sending it would start a new conversation in front of every ' +
      'recipient, including anyone on Cc), and each copy can hold text the other lost. Gmail has no draft under this id, so ' +
      'nothing this call carried — subject, body, recipients — is saved under it.'
    : `${tool} did not run and NOTHING WAS WRITTEN: Gmail returned 404 notFound. Whether draft ${draftId} itself still exists ` +
      `is NOT established here — ${DRAFT_LISTING_BASIS_NOTE[basis](draftId, listed)} A mail client rewriting a draft instead of ` +
      'updating it in place is one explanation for a 404 like this, and the reason this report exists, but on this evidence it ' +
      'is only one of several — read otherExplanations before acting on any of them.';
  const payload = {
    code: 'DRAFT_FORKED',
    codeMeaning:
      'Gmail returned 404 notFound for this draft id. DRAFT_FORKED names the most common CAUSE — a mail client rewriting the ' +
      'draft instead of updating it in place — not a proven one: deletion and sending produce the same 404, and so does a ' +
      'stale reply target. See otherExplanations, and see listingEvidence for what the post-failure listing could actually show.',
    tool,
    draftId,
    gogError,
    whatHappened,
    replyTarget: replyTarget ?? null,
    listingEvidence: {
      basis,
      windowSize: DRAFT_FORK_MAX_CANDIDATES,
      draftsListed: basis === 'listing-unavailable' ? null : listed,
      draftFoundInListing: false,
      establishesTheDraftIsGone: proven,
      note: DRAFT_LISTING_BASIS_NOTE[basis](draftId, listed),
    },
    forkClaim: null,
    forkClaimNote: DRAFT_FORK_CLAIM_NOTE,
    ...rest,
    otherExplanations: replyTarget
      ? [replyTargetExplanation(replyTarget), ...DRAFT_FORK_OTHER_EXPLANATIONS]
      : DRAFT_FORK_OTHER_EXPLANATIONS,
    nextSteps: DRAFT_FORK_NEXT_STEPS,
    signalsThatNeverSuffice: FORK_SIGNALS_THAT_NEVER_SUFFICE,
  };
  const headline = proven
    ? `DRAFT_FORKED: draft ${draftId} no longer resolves — Gmail 404'd it and a listing that covered the whole Drafts folder ` +
      `does not contain it — so ${tool} did not run. The usual cause is a mail client rewriting the draft under a new id ` +
      'rather than updating it; deletion and sending look identical from here.'
    : `DRAFT_FORKED: Gmail returned 404 notFound for draft ${draftId}, so ${tool} did not run and nothing was written. ` +
      `Whether that draft still exists is NOT established: ${DRAFT_LISTING_BASIS_NOTE[basis](draftId, listed)}`;
  return errorResult(
    `${headline} No replacement is named below — that judgement needs a named pair and gog_gmail_drafts_diff.\n\n` +
    JSON.stringify(payload, null, 2),
  );
}

/** What the caller asked the draft to reply to, if anything. `gmail drafts
 *  update` resolves this SEPARATELY from the draft, and a miss 404s
 *  identically. */
type ReplyTarget = { via: 'replyToMessageId' | 'replyToThreadId'; target: string };

/** Did the listing we just took still contain the id we failed on? An id-less
 *  row (every field is `omitempty` in gog) can never match. */
function draftIsStillListed(report: Record<string, unknown>, draftId: string): boolean {
  const listed = report.currentDrafts;
  return Array.isArray(listed) && listed.some((d) => (d as { id?: string }).id === draftId);
}

const NOT_THE_DRAFT_RACE_NOTE =
  'The listing was taken AFTER the failure, so it is evidence about now, not about the instant the call ran. If something ' +
  'recreated a draft under this id in between — vanishingly unlikely, but not impossible — the listed draft could be a ' +
  'different one from the draft you addressed.';

const NOT_THE_DRAFT_WHY_404 =
  '`gog gmail drafts update` resolves up to THREE different Google entities, and gog renders all three 404s with the same ' +
  'string (`Google API error (404 notFound): Requested entity was not found.`, internal/errfmt/googleapi.go): the DRAFT itself ' +
  '(Users.Drafts.Get/Update), the THREAD behind --thread-id (Users.Threads.Get, i.e. replyToThreadId) and the MESSAGE behind ' +
  '--reply-to-message-id (Users.Messages.Get). The error text alone cannot tell them apart — the draft listing can.';

function notTheDraftResult(
  tool: string,
  draftId: string,
  gogError: string,
  report: Record<string, unknown>,
  replyTarget: ReplyTarget | undefined,
): CallToolResult {
  const targetClause = replyTarget
    ? `You passed ${replyTarget.via}=${replyTarget.target}; since the draft resolves, THAT id is the one that did not, and it ` +
      'is the first thing to check. Thread ids and message ids are both 16-hex strings and are routinely confused, and a ' +
      'thread id copied from a stale record may simply no longer exist.'
    : 'This call named no reply target, so the 404 came from somewhere else in it. Whatever it was, it was not this draft id.';
  const { rest } = splitListingBasis(report);
  const payload = {
    code: 'GOOGLE_404_NOT_THE_DRAFT',
    codeMeaning:
      `Google returned 404 notFound, but draft ${draftId} is STILL LISTED in the mailbox, so the 404 was not about the draft ` +
      'id. It is deliberately NOT reported as a fork: nothing here suggests a mail client replaced anything.',
    tool,
    draftId,
    gogError,
    whatHappened:
      `${tool} did not run and NOTHING WAS WRITTEN — but draft ${draftId} still exists: it is still listed below, in a ` +
      `listing taken after the failure. ${NOT_THE_DRAFT_WHY_404} ${targetClause}`,
    replyTarget: replyTarget ?? null,
    forkClaim: null,
    forkClaimNote:
      'No fork is claimed and none is implied. The draft you addressed still resolves, which is the opposite of what a mail ' +
      'client rewriting a draft leaves behind.',
    ...rest,
    raceNote: NOT_THE_DRAFT_RACE_NOTE,
    nextSteps: [
      'Check the reply target, not the draft: a thread id belongs in replyToThreadId and a message id in replyToMessageId, ' +
        'and both are 16-hex strings. Fetch it — gog_gmail_thread_get for a thread id, gog_gmail_get for a message id — and a ' +
        '404 there confirms the target is what is missing.',
      'If the thread id came from a stale record (an old fork report, an earlier note), re-find the conversation with ' +
        'gog_gmail_search and take the thread id from a message that still exists.',
      'Re-run the call without the reply target to confirm the draft itself writes fine. Remember it rewrites the WHOLE body, ' +
        'so pass the body you actually want.',
      'Do NOT go hunting for a replacement draft. Nothing here says this draft forked.',
    ],
  };
  return errorResult(
    `GOOGLE_404_NOT_THE_DRAFT: Google said 404 notFound, but draft ${draftId} is still listed, so the 404 was not about the ` +
    `draft id — ${replyTarget ? `the reply target ${replyTarget.via}=${replyTarget.target} is the remaining explanation` : 'something else in the call is the explanation'}. ` +
    `${tool} did not run and nothing was written. This is NOT a fork.\n\n` +
    JSON.stringify(payload, null, 2),
  );
}

/**
 * Turn a draft-not-found failure into the report above; pass everything else
 * through untouched, having spent nothing.
 *
 * The 404 is only attributed to the DRAFT ID once the listing has failed to
 * find it. When the draft is still there, the same (already-paid-for) listing
 * refutes the fork story, and the report says so instead of sending the caller
 * after a replacement that does not exist.
 */
async function forkAwareDraftFailure(
  result: CallToolResult,
  tool: string,
  draftId: string,
  account: string | undefined,
  replyTarget?: ReplyTarget,
): Promise<CallToolResult> {
  // A success is never inspected: a body that happens to quote "404 not found"
  // must not trigger this. String() rather than a nullish guard because an
  // error result always carries a text block, and the literal 'undefined'
  // matches no 404 pattern anyway.
  if (result.isError !== true) return result;
  const text = String(resultText(result));
  if (!DRAFT_NOT_FOUND_PATTERN.test(text)) return result;
  const report = await currentDraftsForForkReport(account);
  return draftIsStillListed(report, draftId)
    ? notTheDraftResult(tool, draftId, text, report, replyTarget)
    : draftForkedResult(tool, draftId, text, report, replyTarget);
}

// autoreply is bulk and query-driven — there is no single "the message" to
// fetch headers from, so the preview instead runs the SAME search (bounded by
// the same max) to show which messages would actually be matched, rather
// than just echoing the query text back.
function parseSearchSenders(raw: string): string[] {
  try {
    const parsed = JSON.parse(raw) as { threads?: Array<{ from?: string }> };
    return Array.isArray(parsed.threads) ? parsed.threads.map((t) => t.from).filter((v): v is string => Boolean(v)) : [];
  } catch {
    return [];
  }
}

// The token fallback binds the matched set itself, not just the senders: the
// same people in different threads is a different send.
function parseSearchMatches(raw: string): Array<{ id?: string; from?: string; subject?: string }> {
  try {
    const parsed = JSON.parse(raw) as { threads?: Array<{ id?: string; from?: string; subject?: string }> };
    return Array.isArray(parsed.threads) ? parsed.threads.map(({ id, from, subject }) => ({ id, from, subject })) : [];
  } catch {
    return [];
  }
}

/** What `gog gmail get --format=metadata --json` says about a message being forwarded. */
export function parseForwardMetadata(raw: string): {
  from?: string;
  subject?: string;
  date?: string;
  messageIdHeader?: string;
  threadId?: string;
  attachments: Array<{ name: string; size: number | null }>;
} {
  let parsed: {
    headers?: Record<string, unknown>;
    message?: { threadId?: unknown };
    attachments?: Array<{ filename?: unknown; size?: unknown }>;
  } | null = null;
  try {
    parsed = JSON.parse(raw);
  } catch {
    parsed = null;
  }
  const header = (k: string) => (typeof parsed?.headers?.[k] === 'string' ? parsed.headers[k] as string : undefined);
  const threadId = parsed?.message?.threadId;
  return {
    from: header('from'),
    subject: header('subject'),
    date: header('date'),
    messageIdHeader: header('message_id'),
    threadId: typeof threadId === 'string' ? threadId : undefined,
    attachments: (Array.isArray(parsed?.attachments) ? parsed.attachments : []).map((a) => ({
      name: typeof a.filename === 'string' ? a.filename : '',
      size: typeof a.size === 'number' ? a.size : null,
    })),
  };
}

// After confirmation, the send needs no extra recipient lookup: gog's own
// autoreply response already reports the resolved reply target per matched
// message (internal/cmd/gmail_autoreply.go's gmailAutoReplyResult.ReplyTo,
// serialized as `replyTo`) — skipped messages simply omit it.
function parseAutoReplyRecipients(raw: string): string[] {
  try {
    const parsed = JSON.parse(raw) as { autoReply?: { results?: Array<{ replyTo?: string }> } };
    const results = parsed.autoReply?.results ?? [];
    return results.map((r) => r.replyTo).filter((v): v is string => Boolean(v));
  } catch {
    return [];
  }
}

/** Every named attachment part of a stored message, in order. */
function attachmentFilenames(payload: GmailPayloadPart | undefined): string[] {
  const names: string[] = [];
  const walk = (part: GmailPayloadPart | undefined): void => {
    if (!part) return;
    if (part.filename) names.push(part.filename);
    for (const child of part.parts ?? []) walk(child);
  };
  walk(payload);
  return names;
}

/**
 * The confirmation preview for sending a stored draft: who it goes to, its
 * subject, a bounded body preview and every attachment name — read off the
 * draft itself. Unreadable output degrades to an empty preview rather than
 * skipping the prompt: the user is still asked, just with less to go on.
 */
export function previewStoredDraft(raw: string): {
  recipients: string[];
  to?: string;
  cc?: string;
  bcc?: string;
  subject?: string;
  bodyPreview?: string;
  attachments: string[];
} {
  let message: GmailDraftMessage | undefined;
  try {
    message = (JSON.parse(raw) as { draft?: { message?: GmailDraftMessage } }).draft?.message;
  } catch {
    message = undefined;
  }
  const headers = parseHeaders(message?.payload);
  const to = headerValue(headers, 'To');
  const cc = headerValue(headers, 'Cc');
  const bcc = headerValue(headers, 'Bcc');
  return {
    recipients: extractEmails(to, cc, bcc),
    to,
    cc,
    bcc,
    subject: headerValue(headers, 'Subject'),
    bodyPreview: bodyPreview(bestBodyText(message?.payload)),
    attachments: attachmentFilenames(message?.payload),
  };
}

/** Every named attachment part with its byte size, in order. */
function attachmentSizes(payload: GmailPayloadPart | undefined): Array<{ name: string; size: number | null }> {
  const out: Array<{ name: string; size: number | null }> = [];
  const walk = (part: GmailPayloadPart | undefined): void => {
    if (!part) return;
    if (part.filename) out.push({ name: part.filename, size: part.body?.size ?? null });
    for (const child of part.parts ?? []) walk(child);
  };
  walk(payload);
  return out;
}

/**
 * The token fallback's subject for sending a stored draft: the COMPLETE draft
 * as it would go out, bound to its draftId and — as the revision — its current
 * messageId, which Gmail rotates whenever the draft is re-saved (Apple Mail does
 * so on every save). Attachment ids are left out of the hash: they are not
 * stable across reads of the same unchanged message.
 */
export function storedDraftTokenSubject(raw: string, draftId: string, account: string | undefined) {
  let message: GmailDraftMessage | undefined;
  try {
    message = (JSON.parse(raw) as { draft?: { message?: GmailDraftMessage } }).draft?.message;
  } catch {
    message = undefined;
  }
  const headers = parseHeaders(message?.payload);
  const h = (name: string) => headerValue(headers, name);
  const bodyText = firstInlineBody(message?.payload, 'text/plain');
  const bodyHtml = firstInlineBody(message?.payload, 'text/html');
  const attachments = attachmentSizes(message?.payload);
  const fields = {
    from: h('From') ?? senderPreview(account),
    to: h('To'),
    cc: h('Cc'),
    bcc: h('Bcc'),
    subject: h('Subject'),
    attachments,
    threadId: message?.threadId,
    inReplyTo: h('In-Reply-To'),
    references: h('References'),
  };
  return {
    target: draftId,
    revision: message?.id,
    payload: { ...fields, bodyText, bodyHtml },
    preview: {
      draftId,
      messageId: message?.id,
      ...fields,
      // The plain-text part when there is one; an HTML-only draft shows its
      // HTML, since that is what the recipient reads.
      body: bodyText || bodyHtml,
    },
  };
}

/** How much of a copied body the copy_to confirmation shows. */
export const COPY_TO_PREVIEW_CHARS = 300;

/** The separator line above a quoted message in a review copy. */
export const COPY_TO_QUOTE_SEPARATOR = '-------- Message being answered --------';

/**
 * The review copy of a stored draft: its subject behind `subjectPrefix`, its
 * plain body (an HTML-only draft converted to text) and — only when the draft
 * HAS one — its HTML part, each with the optional note and quoted message
 * below. Recipients, threading and attachments are deliberately not part of it.
 */
export function buildDraftCopy(
  draft: GmailStoredMessage,
  opts: { subjectPrefix: string; appendText?: string; quoted?: GmailStoredMessage },
): { subject: string; text: string; html?: string } {
  const subject = `${opts.subjectPrefix}${headerValue(parseHeaders(draft.payload), 'Subject') ?? ''}`;
  let text = storedBodyText(draft.payload).text;
  const storedHtml = firstInlineBody(draft.payload, 'text/html');
  let html = storedHtml === '' ? undefined : storedHtml;
  const addBlock = (blockText: string, blockHtml: string): void => {
    text = text === '' ? blockText : `${text}\n\n${blockText}`;
    if (html !== undefined) html = `${html}\n${blockHtml}`;
  };
  if (opts.appendText) addBlock(opts.appendText, markdownToHtml(opts.appendText));
  if (opts.quoted) {
    const h = readerHeaders(opts.quoted.payload);
    const meta = [h.from && `From: ${h.from}`, h.date && `Date: ${h.date}`, h.subject && `Subject: ${h.subject}`].filter((l): l is string => Boolean(l));
    const quotedText = storedBodyText(opts.quoted.payload).text;
    const block = [COPY_TO_QUOTE_SEPARATOR, ...meta, '', quotedText].join('\n');
    const quotedHtml = `<hr><p>${[COPY_TO_QUOTE_SEPARATOR, ...meta].map(escapeHtml).join('<br>')}</p>`
      + `<blockquote style="margin:0 0 0 .8ex;border-left:1px #ccc solid;padding-left:1ex">${escapeHtml(quotedText).replace(/\n/g, '<br>')}</blockquote>`;
    addBlock(block, quotedHtml);
  }
  return { subject, text, ...(html !== undefined ? { html } : {}) };
}

const BODY_FORMAT_DESCRIPTION =
  'How `body` is written. text (default): the plain part is sent exactly as given. markdown: the plain part drops the ' +
  '**bold**/*italic* markers, and when no bodyHtml is passed the HTML part is rendered from the markdown (paragraphs, "- " ' +
  'and "1. " lists, **bold**, *italic*, "> " quotes) — one input, both parts. On gog_gmail_drafts_update the HTML part ' +
  'is generated from the body in either format unless htmlFromText is false.';

export function registerExtraGmailTools(server: McpServer): void {
  server.registerTool('gog_gmail_raw', {
    description: 'Dump the raw Gmail API response as JSON (lossless; for scripting and LLM consumption).',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      messageId: z.string().describe('Gmail message ID'),
      format: z.enum(['full', 'metadata', 'minimal', 'raw']).optional().describe('Gmail format (default: full)'),
      pretty: z.boolean().optional().describe('Pretty-print JSON (default: compact single-line)'),
      account: accountParam,
    }),
  }, async ({ messageId, format, pretty, account }) => {
    const args: GogArg[] = ['gmail', 'raw', pos(messageId)];
    if (format) args.push(`--format=${format}`);
    if (pretty) args.push('--pretty');
    // Verbatim by contract: see the `lossless` note on runOrDiagnose.
    return runOrDiagnose(args, { account, lossless: true });
  });

  server.registerTool('gog_gmail_attachment', {
    description:
      'Download a Gmail attachment and deliver its contents so you can actually read them. Identify the ' +
      'attachment by attachmentIndex (preferred: the 0-based position from a listing fetched with ' +
      'useIndexedAttachmentIds — stable, and it resolves the real name before the download) or by the legacy ' +
      'opaque attachmentId. The real filename and MIME type are resolved from the message part metadata, so ' +
      'the saved file and response are named correctly (e.g. Guest_Copy.pdf), never a generic *.bin. ' +
      'deliver="auto" (default): ' +
      'images always come back as a native image block; anything else is written server-side and returned as a ' +
      'file PATH, readable only when this server runs on your machine (local stdio). On a hosted deployment ' +
      '(e.g. mcp-host) you cannot read that filesystem, so use deliver="url" or deliver="drive" there. ' +
      'deliver="inline" forces the bytes inline as an image or embedded ' +
      'resource blob (use only if your client consumes resource blobs; errors if over inlineMaxBytes — 3 MiB by default, at most 10 MiB). ' +
      'deliver="drive" always uploads to Drive; deliver="off" writes the file server-side and returns ' +
      '{path, fileName, mimeType, bytes}. Drive delivery creates a file in your Drive (blocked when GOG_READONLY is set). ' +
      'deliver="url" returns {url, fileName, mimeType, bytes, expiresAt}: a signed download link you can fetch with ' +
      'curl or any HTTP client with NO credential, no session and no Google account, valid for one hour. It writes ' +
      'nothing to your Drive and is NOT blocked by GOG_READONLY — it is the right choice when you need the bytes ' +
      'themselves and they are too large or the wrong type to come back inline. It works only where this server is ' +
      'hosted with a blob store (e.g. mcp-host); on a local stdio install it errors and tells you so.',
    // Writes the file on the gog host (a caller `out` can overwrite one) and
    // deliver="drive" creates a Drive file: not read-only (audit SEC-4).
    annotations: { readOnlyHint: false, destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      messageId: z.string().describe('Gmail message ID'),
      attachmentId: z.string().optional().describe('The opaque attachment ID from a listing. Legacy addressing: Gmail re-issues a DIFFERENT id for the same part on every API call, so an id copied from an older listing can be stale. Prefer attachmentIndex. Exactly one of attachmentId / attachmentIndex is required.'),
      attachmentIndex: z.number().int().nonnegative().optional().describe('The attachment\'s 0-based position in its message — the `attachmentIndex` field of a listing fetched with useIndexedAttachmentIds. Stable (a message\'s MIME structure does not change), so this is the reliable way to name an attachment. Exactly one of attachmentId / attachmentIndex is required. NOTE: it is per-MESSAGE — in gog_gmail_thread_attachments the array is flattened across the whole thread, so use each row\'s messageId + attachmentIndex, never its position in that flat list.'),
      inlineMaxBytes: z.number().int().nonnegative().optional().describe('Byte ceiling under which gog embeds the attachment bytes rather than only writing the file. Defaults to gog\'s own 3145728, which this server pins explicitly on every call so an ambient GOG_GMAIL_INLINE_MAX_BYTES cannot change the answer. Raise it to inline something larger (at most 10485760 = 10 MiB — a larger value is clamped to that, because the hosted runtime cannot return a bigger result), lower it to force the file/Drive path.'),
      deliver: z
        .enum(['auto', 'inline', 'drive', 'url', 'off'])
        .optional()
        .describe('How to return the contents: auto (image inline; else a server-side file path), inline (force bytes as image/resource blob), drive (always a Drive link), url (a signed download link you can fetch with curl — hosted deployments only), or off (server-side download only). Default: auto.'),
      out: z.string().optional().describe('Server-side path where gog writes the file; must be inside the server\'s GOG_FILE_ROOTS directories. NOTE: this resolves on the gog server\'s filesystem, not your machine — on a hosted deployment you cannot read it. deliver="url" ignores it (the server has to read the file back to upload it, and only does that from its own download directory); every other delivery mode honors it. Omit it to use an ephemeral temp path.'),
      name: z.string().optional().describe('Filename override. Defaults to the attachment\'s real filename from the message metadata; pass this to skip that lookup or force a name.'),
      driveFolder: z.string().optional().describe('Destination Google Drive folder ID for the uploaded copy (deliver="drive").'),
      account: accountParam,
    }),
  }, async ({ messageId, attachmentId, attachmentIndex, deliver = 'auto', out, name, inlineMaxBytes, driveFolder, account }) => {
    // gog reads the id and the index from the SAME positional argument and is told
    // which shape it got by --use-indexed-attachment-ids, so the wrapper has to
    // pick exactly one. Rejected here rather than by zod so the message can say
    // which one to prefer and why.
    if ((attachmentId === undefined) === (attachmentIndex === undefined)) {
      return errorResult(
        'Pass exactly one of attachmentId or attachmentIndex. Prefer attachmentIndex — the 0-based ' +
        '`attachmentIndex` from a listing fetched with useIndexedAttachmentIds — because Gmail\'s opaque ' +
        'attachmentId is not stable across API calls and a copied one may no longer resolve.',
      );
    }
    // A caller `out` is a write to the gog host's filesystem with attacker-
    // chosen bytes: it must sit inside GOG_FILE_ROOTS (SEC-4).
    if (out) confinePath(out, 'out');
    const indexed = attachmentIndex !== undefined;
    const attachmentRef = indexed ? String(attachmentIndex) : attachmentId as string;
    // deliver="url" needs the host's blob store, and the answer to "is there
    // one" is a fact about this deployment that no download changes. Settled
    // FIRST so a local stdio install is told why it cannot have a link before a
    // byte is fetched, rather than half-way through. Set for that mode and no
    // other, which is what makes it the delivery branch's own condition below.
    let blobMinter: BlobUrlMinter | undefined;
    if (deliver === 'url') {
      const resolved = resolveBlobMinter();
      if ('content' in resolved) return resolved;
      blobMinter = resolved;
    }
    try {
      // 1. Start from the caller's `name` (the recommended path — the caller got
      //    the attachmentId from a listing that also carried the filename). The
      //    download endpoint reports neither name nor MIME; when `name` is absent
      //    we resolve them AFTER downloading, by matching the byte count against
      //    the part metadata (attachmentIds aren't stable enough to match on).
      let filename = name ? sanitizeFilename(name) : undefined;
      let mimeType: string | undefined = filename ? MIME_BY_EXT[extOf(filename)] : undefined;

      // 1b. Indexed mode resolves the part metadata BEFORE the download, because
      //     an index identifies the part outright. The file is then written under
      //     its real name and the post-download size heuristic never runs.
      if (indexed && !filename) {
        const meta = await resolveByIndex(messageId, attachmentIndex, account);
        if (meta?.filename) filename = sanitizeFilename(meta.filename);
        if (meta?.mimeType) mimeType = meta.mimeType;
      }

      // 2. Choose the server-side output path. The on-disk basename is
      //    provisional when `name` is absent; the response still reports the
      //    resolved filename. deliver="url" ignores a caller `out`:
      //    `uploadToBlobStore` will only read a file back from the attachment
      //    download root.
      const notes: string[] = [];
      let outPath = out;
      if (out && deliver === 'url') {
        notes.push(
          '`out` was ignored: deliver="url" has the server read the file back to upload it, and it will only ' +
          'read from its own download directory.',
        );
        outPath = undefined;
      }
      // Our own private download root, not a caller path: made owner-only and
      // swept of expired downloads before gog writes into it (SEC-6).
      const ownPath = !outPath;
      if (!outPath) {
        await prepareDownloadRoot();
        outPath = deliver === 'url'
          ? blobOutPath(messageId, attachmentRef, filename ?? 'attachment')
          : messageOutPath(messageId, filename ?? 'attachment');
      }
      // A staging copy the caller will never be pointed at again is deleted
      // once delivered; one returned BY PATH is left for the TTL sweep.
      const discard = async (result: CallToolResult, file: string): Promise<CallToolResult> => {
        if (ownPath) await removeDownload(file);
        return result;
      };

      // 3. Download. --inline returns the bytes for the image/resource cases;
      //    skip it when delivery is by path, Drive or URL (don't ship base64 only
      //    to discard it).
      const needInline = deliver === 'auto' || deliver === 'inline';
      const args: GogArg[] = ['gmail', 'attachment', pos(messageId), pos(attachmentRef)];
      // PIN the id-vs-index mode on every call. GOG_GMAIL_USE_INDEXED_ATTACHMENT_IDS
      // in the host env would otherwise make gog parse an opaque attachmentId as an
      // integer and hard-fail ("the attachment argument must be a 0-based index",
      // reproduced against a v0.35.0 build). runner.ts strips only credential-shaped
      // vars, and a hosted deployment's env is not the caller's to control — an
      // explicit flag is the only setting authoritative everywhere.
      args.push(indexed ? '--use-indexed-attachment-ids' : '--use-indexed-attachment-ids=false');
      if (needInline) args.push('--inline');
      // PINNED for the same reason as --use-indexed-attachment-ids above: gog declares
      // this flag env:"GOG_GMAIL_INLINE_MAX_BYTES" (gmail_attachment.go:27), so an ambient
      // value in the host env would silently decide whether contentBase64 comes back at
      // all. Restating gog's own default keeps the arg array the single authority.
      // BOUNDED at MAX_INLINE_MAX_BYTES (see its comment): clamped, with a note.
      const inlineCeiling = Math.min(inlineMaxBytes ?? GOG_DEFAULT_INLINE_MAX_BYTES, MAX_INLINE_MAX_BYTES);
      if (inlineMaxBytes !== undefined && inlineMaxBytes > MAX_INLINE_MAX_BYTES) {
        notes.push(
          `inlineMaxBytes ${inlineMaxBytes} was clamped to ${MAX_INLINE_MAX_BYTES} (10 MiB), the most this tool ` +
          'returns inline: a larger result would exceed the hosted runtime\'s 14 MiB result limit.',
        );
      }
      args.push(`--inline-max-bytes=${inlineCeiling}`);
      args.push(`--out=${outPath}`, `--name=${filename ?? 'attachment'}`);
      // `contentBase64` is exempt from redaction: it is the attachment's own
      // bytes, and a base64 blob large enough will eventually spell a token
      // shape by chance — which used to delete a slab out of the middle of it
      // and hand the client an "Invalid Base64 string" protocol error. See
      // RunOptions.opaqueFields.
      const info = JSON.parse(await run(args, { account, opaqueFields: ['contentBase64'] })) as InlineAttachment;
      const path = info.path ?? outPath;

      // BACKSTOP, not the fix — the redaction exemption above is. Bytes that
      // cannot round-trip as base64 must never be handed to the SDK, which
      // rejects them as a -32602 protocol error the caller cannot act on. The
      // file itself was still written server-side, so dropping the inline copy
      // degrades to the path/Drive channel rather than losing the attachment.
      const inlineUnusable = info.contentBase64 !== undefined && !isValidBase64(info.contentBase64);
      if (inlineUnusable) {
        delete info.contentBase64;
        notes.push(
          'The inline copy of this attachment was dropped: the bytes returned by the server were not ' +
          'valid base64, so returning them would have failed as a protocol error. The file itself was ' +
          'downloaded successfully and is delivered below.',
        );
      }

      // 4. Resolve the real filename/MIME when it is still unknown. gog's own
      //    --inline response carries the part metadata whenever its lookup hit, so
      //    prefer that; the size heuristic is the last resort and applies only to
      //    the legacy id path (an index already resolved above).
      if (!filename && info.filename) filename = sanitizeFilename(info.filename);
      if (!mimeType && info.mimeType) mimeType = info.mimeType;
      if (!filename && !indexed) {
        const meta = await resolveBySize(messageId, info.bytes, account);
        if (meta?.filename) filename = sanitizeFilename(meta.filename);
        if (!mimeType && meta?.mimeType) mimeType = meta.mimeType;
      }
      if (!mimeType && info.contentBase64) mimeType = sniffMime(info.contentBase64);
      mimeType = mimeType ?? 'application/octet-stream';
      // Still no filename → derive one from the MIME type; never leave it *.bin.
      if (!filename) {
        const ext = EXT_BY_MIME[mimeType];
        filename = ext ? `attachment.${ext}` : 'attachment';
      }
      const isImage = mimeType.startsWith('image/');
      const summary = `${filename} — ${info.bytes ?? '?'} bytes, ${mimeType}, returned inline.`;

      // 5. Deliver by the requested channel. Every delivery is wrapped with
      //    `notes` so an ignored-`out` explanation is never silently dropped,
      //    whatever the mode or type.
      if (deliver === 'off') {
        return withNote(textResult({ delivery: 'file', path, cached: info.cached, bytes: info.bytes, fileName: filename, mimeType }), notes);
      }
      if (deliver === 'drive') {
        return discard(withNote(await deliverViaDrive(path, filename, driveFolder, account), notes), path);
      }
      // deliver === 'url'. The minter is set for that mode and no other, and it
      // was resolved before the download — so this branch cannot be reached
      // without one, and no other mode can fall into it.
      if (blobMinter) {
        return discard(withNote(await deliverViaBlobUrl(blobMinter, messageId, attachmentRef, path, filename, mimeType), notes), path);
      }
      if (deliver === 'inline') {
        if (info.contentBase64) {
          return discard(withNote(isImage
            ? inlineImageResult(summary, info.contentBase64, mimeType)
            : inlineResourceResult(messageId, filename, summary, info.contentBase64, mimeType), notes), path);
        }
        if (inlineUnusable) {
          return errorResult(
            `The bytes returned for ${filename} were not valid base64, so they cannot be delivered inline ` +
            '(the MCP transport would reject them as a protocol error). The file WAS downloaded and is ' +
            `readable server-side at ${path}. Use deliver="url" or deliver="drive" to receive it.`,
          );
        }
        return errorResult(
          `Attachment is too large to return inline (${info.reason ?? "exceeds gog's inline size limit, 3 MiB by default — raise inlineMaxBytes"}; ` +
          `inlineMaxBytes allows at most 10 MiB, and this request used ${inlineCeiling} bytes). ` +
          'Use deliver="url" for a signed download link (hosted) or deliver="drive" for a Google Drive link.',
        );
      }
      // deliver === 'auto': images render everywhere; everything else is a
      // server-side file path.
      if (isImage && info.contentBase64) {
        return discard(withNote(inlineImageResult(summary, info.contentBase64, mimeType), notes), path);
      }
      return withNote(fileResult(path, filename, mimeType, info.bytes), notes);
    } catch (err) {
      // Never surface gog's raw error (it echoes the full command line + attachment
      // token on the backend); redact the ids and let diagnose classify the rest.
      return diagnose(new Error(sanitizeAttachmentError(err, messageId, attachmentId))); // opaque id only; an index needs no redaction
    }
  });

  server.registerTool('gog_gmail_url', {
    description: 'Print Gmail web URLs for one or more threads.',
    annotations: { readOnlyHint: true, openWorldHint: false },
    inputSchema: z.object({
      threadIds: z.array(z.string()).min(1).describe('One or more thread IDs'),
      account: accountParam,
    }),
  }, async ({ threadIds, account }) => {
    return runOrDiagnose(['gmail', 'url', ...threadIds.map(pos)], { account });
  });

  server.registerTool('gog_gmail_history', {
    description: 'List Gmail history events since a given historyId (for syncing).',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      since: z.string().optional().describe('Start history ID'),
      max: z.number().optional().describe('Max results (default: 100)'),
      pageToken: pageTokenParam,
      page: pageAliasParam,
      all: z.boolean().optional().describe('Fetch all pages'),
      account: accountParam,
    }),
  }, async ({ since, max, pageToken, page, all, account }) => {
    const args: GogArg[] = ['gmail', 'history'];
    if (since) args.push(`--since=${since}`);
    if (max !== undefined) args.push(`--max=${max}`);
    const token = resolvePageToken({ pageToken, page });
    if (token) args.push(`--page=${token}`);
    if (all) args.push('--all');
    return runOrDiagnose(args, { account });
  });

  const bulkActions: Array<{ tool: string; cmd: string; description: string; supportsThread?: boolean }> = [
    {
      tool: 'gog_gmail_archive',
      cmd: 'archive',
      description: 'Archive messages (remove from inbox). Pass either messageIds or a Gmail search query. Set thread=true to treat the ids as THREAD ids and archive every message in each thread (the right mode for ids that came from thread search).',
      supportsThread: true,
    },
    {
      tool: 'gog_gmail_mark_read',
      cmd: 'mark-read',
      description: 'Mark messages as read. Pass either messageIds or a Gmail search query.',
    },
    {
      tool: 'gog_gmail_mark_unread',
      cmd: 'unread',
      description: 'Mark messages as unread. Pass either messageIds or a Gmail search query.',
    },
    {
      tool: 'gog_gmail_trash',
      cmd: 'trash',
      description: 'Move messages to trash. Pass either messageIds or a Gmail search query.',
    },
  ];

  for (const { tool, cmd, description, supportsThread } of bulkActions) {
    const inputSchema: Record<string, z.ZodTypeAny> = {
      messageIds: z.array(z.string()).optional().describe('Specific message IDs to act on'),
      query: z.string().optional().describe('Gmail search query (alternative to messageIds; acts on all matching)'),
      max: z.number().optional().describe('Max messages when using --query (default: 100)'),
      account: accountParam,
    };
    if (supportsThread) {
      inputSchema.thread = z.boolean().optional().describe('Treat messageIds as THREAD ids and act on every message in each thread');
    }
    server.registerTool(tool, {
      description,
      annotations: { destructiveHint: true, openWorldHint: true },
      inputSchema: z.object(inputSchema),
    }, async (rawArgs) => {
      const { messageIds, query, max, thread, account } = rawArgs as {
        messageIds?: string[]; query?: string; max?: number; thread?: boolean; account?: string;
      };
      const args: GogArg[] = ['gmail', cmd];
      if (messageIds) args.push(...messageIds.map(pos));
      if (query) args.push(`--query=${query}`);
      if (max !== undefined) args.push(`--max=${max}`);
      if (supportsThread && thread) args.push('--thread');
      return runOrDiagnose(args, { account });
    });
  }

  server.registerTool('gog_gmail_message_modify', {
    description: 'Modify labels on a single message (add and/or remove labels).',
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      messageId: z.string().describe('Gmail message ID'),
      add: z.string().optional().describe('Labels to add (comma-separated, name or ID)'),
      remove: z.string().optional().describe('Labels to remove (comma-separated, name or ID)'),
      account: accountParam,
    }),
  }, async ({ messageId, add, remove, account }) => {
    const args: GogArg[] = ['gmail', 'messages', 'modify', pos(messageId)];
    if (add) args.push(`--add=${add}`);
    if (remove) args.push(`--remove=${remove}`);
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_gmail_batch_delete', {
    description: 'Permanently delete multiple messages (requires the broader Gmail scope; not reversible — messages bypass Trash). Requires force:true to delete non-interactively. Use gog_gmail_trash for normal deletes. '
      + 'Because `force` is only the model\'s say-so, a forced delete also reads each message and asks the MCP host to '
      + `show the user a confirmation prompt listing them (sender, subject, date; the first ${BATCH_DELETE_PREVIEW_MAX} by name) `
      + 'first; nothing is deleted unless they accept.' + CONFIRM_FALLBACK_DESCRIPTION,
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      messageIds: z.array(z.string()).min(1).describe('Message IDs to permanently delete'),
      force: z.boolean().optional().describe('Required to delete in this non-interactive context — without it the delete is refused as a safety guard.'),
      account: accountParam,
      confirmToken: confirmTokenParam,
    }),
  }, async ({ messageIds, force, account, confirmToken }, ctx) => {
    const args: GogArg[] = ['gmail', 'batch', 'delete', ...messageIds.map(pos)];
    // Without --force gog refuses on its own (the runner injects --no-input),
    // so only a forced delete can destroy anything and only it asks.
    if (force) {
      const messages: Array<Record<string, string>> = [];
      for (const id of messageIds.slice(0, BATCH_DELETE_PREVIEW_MAX)) {
        const got = await runOrDiagnose(['gmail', 'get', pos(id), '--format=metadata'], { account });
        if (got.isError) return got;
        const { from, subject, date } = parseMetadataHeaders(String(resultText(got)));
        messages.push({ id, ...(from ? { from } : {}), ...(subject ? { subject } : {}), ...(date ? { date } : {}) });
      }
      const more = messageIds.length - messages.length;
      const view = { count: messageIds.length, messages, ...(more > 0 ? { notShown: more } : {}) };
      const confirmation = await requireDispatchConfirmation(ctx, {
        action: 'gmail.batch-delete',
        message: `Review and confirm PERMANENTLY deleting ${messageIds.length} message(s) — they skip the Trash and cannot be recovered:`,
        confirmationLabel: 'Confirm that these messages should be permanently deleted now.',
        details: view,
        unsupportedNote: 'Move them to the Trash with gog_gmail_trash instead; the user can empty it from Gmail.',
        fallback: {
          args: { messageIds, force, account },
          tool: 'gog_gmail_batch_delete',
          account,
          confirmToken,
          // Every id is bound, not only the ones shown by name.
          subject: () => ({ target: messageIds.join(','), payload: { ...view, messageIds }, preview: view }),
        },
      });
      if (confirmation) return confirmation;
      args.push('--force');
    }
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_gmail_batch_modify', {
    description: 'Modify labels on multiple messages in one call (add and/or remove labels).',
    annotations: { destructiveHint: false, openWorldHint: true },
    inputSchema: z.object({
      messageIds: z.array(z.string()).min(1).describe('Message IDs to modify'),
      add: z.string().optional().describe('Labels to add (comma-separated, name or ID)'),
      remove: z.string().optional().describe('Labels to remove (comma-separated, name or ID)'),
      account: accountParam,
    }),
  }, async ({ messageIds, add, remove, account }) => {
    const args: GogArg[] = ['gmail', 'batch', 'modify', ...messageIds.map(pos)];
    if (add) args.push(`--add=${add}`);
    if (remove) args.push(`--remove=${remove}`);
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_gmail_thread_get', {
    description: 'Get a Gmail thread with all messages. THIS IS THE CORRECT TOOL WHEN YOU ALREADY KNOW THE threadId — it returns the thread in full, so unlike a search it can never be truncated, mis-ranked, or come back empty because the query missed. Never re-discover a known thread with gog_gmail_search; read it here. For long threads that overflow context, use latestN to fetch only the most recent messages and/or snippetsOnly for a lightweight per-message headers+snippet view; sanitizeContent strips raw payloads/HTML and is the biggest size reducer when you do need bodies. Note each message carries two distinct id concepts: the top-level `id` (the Gmail short hex message id — pass THIS as replyToMessageId to reply) and the `Message-Id` header (the RFC822 `<…@host>` value used in In-Reply-To/References) — don\'t confuse either with the `threadId`. To reply to the thread itself, pass the thread\'s id as replyToThreadId on gog_gmail_drafts_create. Read-only: it lists attachments but never downloads them — fetch each one with gog_gmail_attachment.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      threadId: z.string().describe('Gmail thread ID'),
      full: z.boolean().optional().describe('Show full message bodies'),
      sanitizeContent: z.boolean().optional().describe('Strip HTML, remove URLs, omit raw payloads from JSON (largest payload-size reduction)'),
      latestN: z.number().int().positive().optional().describe('Return only the most recent N messages in the thread (wrapper-side trim; avoids overflowing context on long threads)'),
      snippetsOnly: z.boolean().optional().describe('Reduce each message to its id, labels, snippet, and key headers (From/To/Cc/Subject/Date), dropping full bodies'),
      useIndexedAttachmentIds: z.boolean().optional().describe('Report each attachment as a 0-based `attachmentIndex` within its message instead of an opaque `attachmentId`. The index is stable across calls (a message\'s MIME structure does not change) while the id is not, so this is what you want before calling gog_gmail_attachment.'),
      account: accountParam,
    }),
  }, async ({ threadId, full, sanitizeContent, latestN, snippetsOnly, useIndexedAttachmentIds, account }) => {
    const args: GogArg[] = ['gmail', 'thread', 'get', pos(threadId)];
    if (full) args.push('--full');
    if (sanitizeContent) args.push('--sanitize-content');
    // PINNED, not conditional: GOG_GMAIL_USE_INDEXED_ATTACHMENT_IDS in the host env
    // swaps `attachmentId` for `attachmentIndex` in every attachments[] entry. Only
    // an explicit flag makes the response shape the same on both transports.
    args.push(useIndexedAttachmentIds ? '--use-indexed-attachment-ids' : '--use-indexed-attachment-ids=false');
    const result = await runOrDiagnose(args, { account });
    if (latestN === undefined && !snippetsOnly) return result;
    return trimThread(result, latestN, snippetsOnly);
  });

  server.registerTool('gog_gmail_thread_modify', {
    description: 'Modify labels on all messages in a thread (add and/or remove labels).',
    annotations: { destructiveHint: false, openWorldHint: true },
    inputSchema: z.object({
      threadId: z.string().describe('Gmail thread ID'),
      add: z.string().optional().describe('Labels to add (comma-separated, name or ID)'),
      remove: z.string().optional().describe('Labels to remove (comma-separated, name or ID)'),
      account: accountParam,
    }),
  }, async ({ threadId, add, remove, account }) => {
    const args: GogArg[] = ['gmail', 'thread', 'modify', pos(threadId)];
    if (add) args.push(`--add=${add}`);
    if (remove) args.push(`--remove=${remove}`);
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_gmail_thread_attachments', {
    description: 'List all attachments in a Gmail thread (filenames, ids, sizes). Read-only: to receive the bytes, fetch each one with gog_gmail_attachment (image inline, or deliver="url"/"drive"/"off").',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      threadId: z.string().describe('Gmail thread ID'),
      useIndexedAttachmentIds: z.boolean().optional().describe('Report each attachment as a 0-based `attachmentIndex` instead of an opaque `attachmentId`. Set this before calling gog_gmail_attachment: the index is stable across calls, the id is not. The index counts WITHIN each message, and this listing flattens every message\'s attachments into one array — so pair each row\'s `messageId` with its own `attachmentIndex`; a row\'s position in the flat array is NOT the index.'),
      account: accountParam,
    }),
  }, async ({ threadId, useIndexedAttachmentIds, account }) => {
    const args: GogArg[] = ['gmail', 'thread', 'attachments', pos(threadId)];
    // PINNED — see gog_gmail_thread_get. This listing is the one place the index is
    // load-bearing: gog concatenates every message's attachments into a single
    // array, so array position is NOT the per-message index the download expects.
    args.push(useIndexedAttachmentIds ? '--use-indexed-attachment-ids' : '--use-indexed-attachment-ids=false');
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_gmail_labels_list', {
    description: 'List all Gmail labels for the account.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      account: accountParam,
    }),
  }, async ({ account }) => {
    return runOrDiagnose(['gmail', 'labels', 'list'], { account });
  });

  server.registerTool('gog_gmail_labels_get', {
    description: 'Get label details, including message and thread counts.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      labelIdOrName: z.string().describe('Label ID or name (e.g. INBOX, STARRED, or a user-created label)'),
      account: accountParam,
    }),
  }, async ({ labelIdOrName, account }) => {
    return runOrDiagnose(['gmail', 'labels', 'get', pos(labelIdOrName)], { account });
  });

  server.registerTool('gog_gmail_labels_create', {
    description: 'Create a new Gmail label.',
    annotations: { destructiveHint: false, openWorldHint: true },
    inputSchema: z.object({
      name: z.string().describe('Label name'),
      account: accountParam,
    }),
  }, async ({ name, account }) => {
    return runOrDiagnose(['gmail', 'labels', 'create', pos(name)], { account });
  });

  server.registerTool('gog_gmail_labels_rename', {
    description: 'Rename a Gmail label.',
    annotations: { destructiveHint: false, openWorldHint: true },
    inputSchema: z.object({
      labelIdOrName: z.string().describe('Current label ID or name'),
      newName: z.string().describe('New label name'),
      account: accountParam,
    }),
  }, async ({ labelIdOrName, newName, account }) => {
    return runOrDiagnose(['gmail', 'labels', 'rename', pos(labelIdOrName), pos(newName)], { account });
  });

  server.registerTool('gog_gmail_labels_delete', {
    description: 'Delete a Gmail label.',
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      labelIdOrName: z.string().describe('Label ID or name to delete'),
      account: accountParam,
    }),
  }, async ({ labelIdOrName, account }) => {
    return runOrDiagnose(['gmail', 'labels', 'delete', pos(labelIdOrName), '--force'], { account }); // gog gates this op; without --force the runner's --no-input makes it refuse
  });

  server.registerTool('gog_gmail_labels_modify', {
    description: 'Modify labels on one or more threads (add and/or remove labels).',
    annotations: { destructiveHint: false, openWorldHint: true },
    inputSchema: z.object({
      threadIds: z.array(z.string()).min(1).describe('One or more thread IDs'),
      add: z.string().optional().describe('Labels to add (comma-separated, name or ID)'),
      remove: z.string().optional().describe('Labels to remove (comma-separated, name or ID)'),
      account: accountParam,
    }),
  }, async ({ threadIds, add, remove, account }) => {
    const args: GogArg[] = ['gmail', 'labels', 'modify', ...threadIds.map(pos)];
    if (add) args.push(`--add=${add}`);
    if (remove) args.push(`--remove=${remove}`);
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_gmail_drafts_list', {
    description:
      'List Gmail drafts. Each entry is annotated FOR FREE — no extra gog invocation, whatever the number of drafts — with ' +
      '`origin` (`api` = created through the Gmail API; `non-api` = the id begins `s:`, i.e. it arrived over IMAP/sync) and ' +
      '`rootsOwnThread` (threadId equals the draft\'s own messageId, so sending it starts a NEW conversation instead of replying). ' +
      'Read those two as facts about the draft, NOT as a fork verdict: `non-api` is not "Apple Mail" (Thunderbird, Outlook-over-IMAP ' +
      'and Gmail offline all produce `s:` ids), and rootsOwnThread was a 4/8 = 0.50 coin flip for Apple authorship on a live mailbox. ' +
      'The prose behind rootsOwnThread is one of exactly two constants, so it rides along ONCE per result under `threadingNotes` ' +
      '(`rootsOwnThread` / `inThread`) and the per-row boolean selects between them. ' +
      'To decide whether one draft actually replaced another, diff the named pair with gog_gmail_drafts_diff.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      max: z.number().optional().describe('Max results (default: 20)'),
      pageToken: pageTokenParam,
      page: pageAliasParam,
      all: z.boolean().optional().describe('Fetch all pages'),
      enrich: z.boolean().optional().describe(
        'Add subject, from, internalDateIso, to/cc/bcc, recipientCount, hasRecipients and isReply (In-Reply-To present) to each draft. Costs ONE extra gog invocation (`gmail messages search in:drafts`) ' +
        'regardless of how many drafts there are — but that single command makes gog fetch every matching draft server-side at ' +
        'concurrency 10, so Google reads and wall-clock are linear in the result count even though gog spawns are not. Narrow `max` ' +
        'before enabling it. If the search fails the listing silently degrades to the free fields rather than erroring.',
      ),
      account: accountParam,
    }),
  }, async ({ max, pageToken, page, all, enrich, account }) => {
    const args: GogArg[] = ['gmail', 'drafts', 'list'];
    if (max !== undefined) args.push(`--max=${max}`);
    const token = resolvePageToken({ pageToken, page });
    if (token) args.push(`--page=${token}`);
    if (all) args.push('--all');
    const result = await runOrDiagnose(args, { account });

    // Post-process gog's own JSON, exactly as trimThread does: anything that is
    // not a drafts listing (an error, a "No drafts" line, an unexpected shape)
    // passes through untouched, and gog's fields are only ever ADDED to.
    let parsed: Record<string, unknown>;
    let entries: DraftListEntry[];
    try {
      parsed = JSON.parse(resultText(result) ?? '') as Record<string, unknown>;
      const rawDrafts = parsed.drafts;
      if (!Array.isArray(rawDrafts)) return result;
      entries = rawDrafts as DraftListEntry[];
    } catch {
      return result;
    }

    // Tier 1 is opt-in and capped at ONE extra invocation. It is deliberately
    // spent only AFTER the listing parsed, so an unparseable listing never
    // costs a second spawn. The key type allows `undefined` so the join below
    // needs no branch; `undefined` is never inserted.
    const byMessageId = new Map<string | undefined, EnrichedDraftMessage>();
    let enrichment: Record<string, unknown> | undefined;
    if (enrich) {
      const searchArgs = ['gmail', 'messages', 'search', 'in:drafts', `--max=${max ?? GOG_DRAFTS_LIST_DEFAULT_MAX}`];
      if (all) searchArgs.push('--all');
      // The caller's page token, or enrichment silently searches page 1 while the
      // list is on page N: an extra gog spawn that joins ZERO rows and still
      // reported applied:true. The token is a drafts-list cursor, so it is only
      // meaningful to the paged search.
      if (token) searchArgs.push(`--page=${token}`);
      // Both PINNED for the same reason as gog_gmail_messages_search: the env
      // vars behind them change the result shape (and the per-message cost).
      searchArgs.push('--include-attachments=false', '--use-indexed-attachment-ids=false');
      // Recipients and In-Reply-To ride the SAME metadata read gog already makes
      // per draft (gog >= 0.48: no extra API call), so "is this draft addressed
      // yet / is it a reply" never needs a per-draft fetch.
      searchArgs.push('--include-recipients', '--headers=In-Reply-To');
      try {
        const messages = (JSON.parse(await runNormalized(searchArgs, { account })) as { messages?: EnrichedDraftMessage[] }).messages;
        if (!Array.isArray(messages)) throw new Error('`gog gmail messages search in:drafts` returned no messages array');
        for (const m of messages) {
          if (m.id) byMessageId.set(m.id, m);
        }
        enrichment = { requested: true, applied: true, extraGogCalls: 1, matched: 0, unmatched: 0, costNote: DRAFT_ENRICH_COST_NOTE };
      } catch (err) {
        // Never an error: the caller asked for a listing and gets one, with the
        // free tier-0 fields intact and an explicit reason the rest is missing.
        enrichment = {
          requested: true,
          applied: false,
          extraGogCalls: 1,
          reason: `Enrichment failed, so the listing degraded to the free tier-0 fields (origin, rootsOwnThread): ${String(err)}`,
        };
      }
    }

    let matched = 0;
    const drafts = entries.map((d) => {
      const roots = rootsOwnThread(d);
      const extra = byMessageId.get(d.messageId);
      if (extra) matched += 1;
      return {
        ...d,
        origin: originFromDraftId(d.id ?? ''),
        rootsOwnThread: roots,
        ...(extra ? { subject: extra.subject, from: extra.from, internalDateIso: extra.internalDateIso, ...draftRecipientFacts(extra) } : {}),
      };
    });
    if (enrichment?.applied === true) {
      enrichment.matched = matched;
      enrichment.unmatched = entries.length - matched;
    }

    return rawTextResult(JSON.stringify({
      ...parsed,
      drafts,
      originNote: DRAFT_LIST_ORIGIN_NOTE,
      threadingNotes: { rootsOwnThread: DRAFT_ROOTS_OWN_THREAD_NOTE, inThread: DRAFT_IN_THREAD_NOTE },
      ...(enrichment ? { enrichment } : {}),
    }));
  });

  server.registerTool('gog_gmail_drafts_diff', {
    description:
      'Compare TWO NAMED DRAFTS and report exactly how they diverged: which body lines exist only in one, whether either is a ' +
      'superset of the other, how their threading differs, and — kept deliberately separate from all of that — whether there is ' +
      'enough evidence to say one REPLACED the other. Use it when a draft you created stopped resolving (`gog_gmail_drafts_update` ' +
      'returning `Google API error (404 notFound)` is the usual first symptom) and a newer draft has appeared: editing a draft in a ' +
      'real mail client does not update it in place, it writes a new draft and abandons the original, so both copies can hold text ' +
      'the other lost. COST: exactly 2 gog invocations, one `gmail drafts get` per named draft. It never scans the mailbox and never ' +
      'grows with the number of drafts. ' +
      'THE PAIRING VERDICT IS `confirmed` ONLY when all four of these hold: an Apple identity header on the candidate, a real ' +
      'LINEAGE link FROM THE CANDIDATE TO THE ORIGINAL, a strictly newer candidate, and the same From. Exactly two things count ' +
      'as lineage, and both point at the original itself: (a) the ORIGINAL DRAFT\'s own Message-Id appearing in the candidate\'s ' +
      'In-Reply-To/References, or (b) agreement on text NEITHER draft quoted AND NEITHER CLIENT GENERATED — the salutation, the ' +
      'closing formula, the name under it and the signature block are excluded alongside quoting, because a mail client ' +
      'reproduces all of them identically on every message it composes — meeting all three printed minimums (similarity, ' +
      'shared lines, shared characters — all reported under bodyAgreement, alongside quotedLinesIgnored and ' +
      'boilerplateLinesIgnored so you can see what each filter removed). A SHARED REPLY ROOT IS NOT LINEAGE: it links both ' +
      'drafts to a common ANCESTOR, which every reply in a thread has, so it is reported as corroboration and can raise the ' +
      'answer no higher than an explicitly WEAK `candidate`. Anything less than all four is `candidate` and names every missing ' +
      'signal; with neither lineage nor corroboration it is `none` — which means no evidence was FOUND, not that the drafts are ' +
      'proven unrelated (the comparison is line-based, so re-wrapping and smart quotes can hide a real link). NONE OF THE ' +
      'FOLLOWING EVER SUFFICES, alone or combined: ' +
      FORK_SIGNALS_THAT_NEVER_SUFFICE.join(' ') +
      ' Act on `confirmed` only after reading the evidence list; treat `candidate` as a question to verify by hand. Merging the ' +
      'wrong pair sends the wrong text to the wrong thread, in front of everyone on Cc.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      draftIdA: z.string().describe('First draft id — conventionally the ORIGINAL (the one you created). Direction is decided by internalDate, not by this order, and the answer says which it treated as the original.'),
      draftIdB: z.string().describe('Second draft id — conventionally the SUSPECTED REPLACEMENT.'),
      maxDiffLines: z.number().int().positive().optional().describe(`Cap on the per-side line lists (default ${DRAFT_DIFF_MAX_LINES}); must be a positive integer. The counts and the verdict are computed on the FULL bodies; only the printed lists are capped, \`truncated\` says when they were, and onlyInACount/onlyInBCount give the untruncated totals.`),
      account: accountParam,
    }),
  }, async ({ draftIdA, draftIdB, maxDiffLines, account }) => {
    const fetchArgs = (id: string): GogArg[] => ['gmail', 'drafts', 'get', pos(id), '--use-indexed-attachment-ids=false'];
    let rawA: string;
    let rawB: string;
    try {
      rawA = await runNormalized(fetchArgs(draftIdA), { account });
      rawB = await runNormalized(fetchArgs(draftIdB), { account });
    } catch (err) {
      return diagnose(new Error(
        `gog_gmail_drafts_diff could not fetch both drafts (${draftIdA}, ${draftIdB}): ${String(err)}. ` +
        'A draft id that has stopped resolving is exactly what a mail client leaves behind when it rewrites a draft instead of ' +
        'updating it — the old id 404s and a new draft holds the edited text. Run gog_gmail_drafts_list (origin and rootsOwnThread ' +
        'are free there), pick the surviving id, and diff it against the one that still resolves.',
      ));
    }

    const parseDraft = (raw: string): GmailDraftMessage | undefined => {
      try {
        return (JSON.parse(raw) as { draft?: { message?: GmailDraftMessage } }).draft?.message;
      } catch {
        return undefined;
      }
    };
    const msgA = parseDraft(rawA);
    const msgB = parseDraft(rawB);
    if (!msgA || !msgB) {
      return errorResult(
        `Could not read the stored message for draft ${msgA ? draftIdB : draftIdA} — \`gog gmail drafts get\` returned no ` +
        '`draft.message` object. Nothing is reported rather than diffing half a pair and letting the missing side read as "empty".',
      );
    }

    const a = describeDraftSide(draftIdA, msgA);
    const b = describeDraftSide(draftIdB, msgB);

    // Which one is the possible REPLACEMENT? Time decides, not argument order.
    // B is treated as the candidate unless it is strictly older than A; when
    // either internalDate is unreadable the caller's own order stands, and the
    // answer names both roles so the choice is never implicit.
    const aMs = parseInternalDateMs(msgA.internalDate);
    const bMs = parseInternalDateMs(msgB.internalDate);
    const bIsCandidate = !(aMs !== undefined && bMs !== undefined && bMs < aMs);
    const original = bIsCandidate ? a : b;
    const candidate = bIsCandidate ? b : a;

    return textResult({
      drafts: { a: a.side, b: b.side },
      bodyDiff: diffBodyLines(
        bestBodyText(msgA.payload),
        bestBodyText(msgB.payload),
        maxDiffLines ?? DRAFT_DIFF_MAX_LINES,
      ),
      threadingDifferences: threadingDifferences(a.side, b.side),
      forkPairing: {
        originalDraftId: original.side.draftId,
        candidateDraftId: candidate.side.draftId,
        ...evaluateForkPairing(original.facts, candidate.facts, 2),
      },
      costNote: 'This call made exactly 2 gog invocations, one `gmail drafts get` per named draft, and is capped there by construction.',
    });
  });

  server.registerTool('gog_gmail_drafts_get', {
    description:
      'Get a Gmail draft by ID, DECODED by default (format "text"): draftId, messageId, threadId, the headers that matter ' +
      '(from, to, cc, bcc, replyTo, subject, date, messageId, inReplyTo, references), isReply, the plain-text body (an ' +
      'HTML-only draft is converted to text; `textSource` says which) and the attachments by name. "html" returns the HTML ' +
      'part instead, "both" returns both, and "raw" returns gog\'s complete JSON (raw MIME payload with base64 parts and ' +
      'attachment ids) as before. Read-only: it lists attachments but never downloads them — fetch each one with gog_gmail_attachment.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      draftId: z.string().describe('Draft ID'),
      format: z.enum(['text', 'html', 'both', 'raw']).optional().describe('text (default): decoded plain-text body + key headers. html: decoded HTML part. both: text and html. raw: gog\'s full JSON with base64 MIME parts (the previous behaviour).'),
      useIndexedAttachmentIds: z.boolean().optional().describe('format raw only: report each attachment as a 0-based `attachmentIndex` instead of an opaque `attachmentId` (stable across calls, unlike the id).'),
      account: accountParam,
    }),
  }, async ({ draftId, format = 'text', useIndexedAttachmentIds, account }) => {
    const args: GogArg[] = ['gmail', 'drafts', 'get', pos(draftId)];
    args.push(useIndexedAttachmentIds ? '--use-indexed-attachment-ids' : '--use-indexed-attachment-ids=false'); // PINNED — see gog_gmail_thread_get
    if (format === 'raw') return runOrDiagnose(args, { account });
    return readDecodedMessage(args, account, format, (out) => (out as { draft?: { message?: GmailStoredMessage } }).draft?.message, { draftId }, run);
  });

  /** Read a stored draft for a read-modify-write: unredacted (it is written
   *  back) with its base64 parts kept out of redaction. A failed read comes
   *  back as the diagnosed result so the caller's fork-aware path applies. */
  async function readStoredDraft(
    draftId: string,
    account: string | undefined,
  ): Promise<{ message: GmailStoredMessage } | { result: CallToolResult }> {
    let raw: string;
    try {
      raw = await run(['gmail', 'drafts', 'get', pos(draftId), '--use-indexed-attachment-ids=false'], { account, opaqueFields: ['data', 'attachmentId'] });
    } catch (err) {
      return { result: await diagnose(err) };
    }
    let message: GmailStoredMessage | undefined;
    try {
      message = (JSON.parse(raw) as { draft?: { message?: GmailStoredMessage } }).draft?.message;
    } catch {
      message = undefined;
    }
    if (!message) {
      return { result: errorResult(`Could not read draft ${draftId}: \`gog gmail drafts get\` returned no \`draft.message\` object. Nothing was written or sent.`) };
    }
    return { message };
  }

  /** A patch whose `old` matched zero or several times: nothing is written,
   *  and the caller gets the text it has to match against (redacted, like any
   *  output — it is shown, never written back). */
  function patchRefusal(draftId: string, reason: string, current: { text: string; source: string }): CallToolResult {
    return errorResult(JSON.stringify({
      error: 'PATCH_NO_MATCH',
      draftId,
      reason,
      note: 'NOTHING WAS WRITTEN. Each replace[].old must occur exactly once in the stored plain-text body below; widen it with surrounding text to make it unique.',
      textSource: current.source,
      currentText: redactSecrets(current.text),
    }));
  }

  /** Settle the plain and HTML parts before the flags are built. With
   *  `autoHtml` and no caller HTML, the HTML part is generated from the body. */
  function resolveBodyParts<T extends { body: string; bodyFormat?: 'text' | 'markdown'; bodyHtml?: string; bodyHtmlFile?: string }>(
    flags: T,
    autoHtml: boolean,
  ): T {
    const parts = composeBodyParts(flags.body, flags.bodyFormat ?? 'text');
    const generate = autoHtml && !flags.bodyHtml && !flags.bodyHtmlFile && flags.body.trim() !== '';
    return { ...flags, body: parts.text, ...(generate ? { bodyHtml: parts.html } : {}) };
  }

  const draftWriteSchema = {
    to: z.string().optional().describe('Recipients (comma-separated). On gog_gmail_drafts_update: omit to keep the draft\'s current To, pass "" to clear it.'),
    cc: z.string().optional().describe('CC recipients (comma-separated). On gog_gmail_drafts_update: omit to keep the draft\'s current Cc, pass "" to clear it.'),
    bcc: z.string().optional().describe('BCC recipients (comma-separated). On gog_gmail_drafts_update: omit to keep the draft\'s current Bcc, pass "" to clear it.'),
    subject: z.string().describe('Subject'),
    body: z.string().describe('Body (plain text). Any size — a large body is written to a temp file on the gog server rather than inlined into the command line. Note gog strips trailing newlines from a file-delivered body.'),
    bodyFormat: z.enum(['text', 'markdown']).optional().describe(BODY_FORMAT_DESCRIPTION),
    bodyHtml: z.string().optional().describe('Body (HTML; optional). Pass the HTML itself at any size — a large body is written to a temp file on the gog server rather than inlined into the command line. Mutually exclusive with bodyHtmlFile.'),
    bodyHtmlFile: z.string().optional().describe('Path to an HTML file that ALREADY EXISTS on the gog server to use as the HTML body. gog also accepts "-" for stdin, but this server never writes to gog\'s stdin, so "-" would hang until the call times out. Mutually exclusive with bodyHtml — supplying both is rejected. You rarely need this: bodyHtml handles large bodies on its own.'),
    replyToMessageId: z.string().optional().describe('Reply to a specific Gmail MESSAGE id — the short hex `id` field from gog_gmail_get / _search / _thread_get (e.g. 19e7593d77fd9636), NOT a thread id and NOT the RFC822 `<…@host>` Message-Id header. Anchors In-Reply-To/References to that exact message. To reply to a thread when you don\'t know the latest message, use replyToThreadId instead. If both are given, replyToMessageId wins.'),
    replyToThreadId: z.string().optional().describe('Reply to a Gmail THREAD id — passed to gog as --thread-id, which threads the draft using the thread\'s latest-message headers (In-Reply-To/References). This is what "reply to this thread" almost always means. Mutually exclusive with replyToMessageId (which wins if both are set). Thread ids and message ids are both 16-hex strings and easy to confuse — use this param, not replyToMessageId, when the id came from a thread.'),
    replyTo: z.string().optional().describe('Reply-To header address'),
    quote: z.boolean().optional().describe('Include the original message quoted below the body. Requires replyToMessageId or replyToThreadId. DEFAULTS OFF: a draft created with a reply target but without this threads correctly and still reads as a brand-new message, because gog only quotes by default on its reply subcommands. For a real reply draft prefer gog_gmail_drafts_reply / gog_gmail_drafts_reply_all, which also inherit the recipients and the "Re:" subject that this tool leaves to you.'),
    replyAll: z.boolean().optional().describe('Auto-populate recipients from the original message (reply-all), inferring To/Cc from it. Requires replyToMessageId or replyToThreadId. Explicit to/cc/bcc still apply on top; omitRecipients still suppresses them.'),
    attach: z.array(z.string()).optional().describe('File paths to attach (repeatable), resolved ON THE GOG SERVER\'s filesystem — NOT this client\'s. Only usable when gog runs on the same machine you do (local stdio); on a hosted deployment (e.g. mcp-host) these paths do not exist and the call fails with "no such file or directory" — use blobKeys (gog_upload_slots) or, for a small file, attachInline there. Read on the server, base64-encoded with a MIME type inferred from the extension. The JSON result echoes attached filenames and byte sizes — check it to confirm the files were found and embedded. On gog_gmail_drafts_update, supplying attach / attachInline / blobKeys REPLACES the draft\'s existing attachments; omitting all three preserves them (use clearAttachments to remove all). Must be inside the server\'s GOG_FILE_ROOTS directories (default ~/gogcli-mcp-files).'),
    attachInline: attachInlineParam,
    blobKeys: blobKeysParam,
    from: z.string().optional().describe('Send from this email address (must be a verified send-as alias)'),
    autoFromAddressedAlias: z.boolean().optional().describe('When from is omitted, send from the verified send-as alias the original message was addressed TO, instead of the account\'s primary address — so a reply to mail sent to an alias goes back out from that alias. Ignored when from is set.'),
    omitRecipients: z.boolean().optional().describe('Create the draft with no recipients even if to/cc/bcc are supplied — an accidental-send guard. Populate recipients in a later update before sending.'),
    ...signatureSchema,
    returnFull: z.boolean().optional().describe('After writing, re-fetch and return the full stored draft (subject, body, recipients) instead of just the write acknowledgement. Costs one extra read.'),
    account: accountParam,
  };

  type DraftFlags = {
    to?: string;
    cc?: string;
    bcc?: string;
    subject: string;
    body: string;
    bodyFormat?: 'text' | 'markdown';
    bodyHtml?: string;
    bodyHtmlFile?: string;
    replyToMessageId?: string;
    replyToThreadId?: string;
    replyTo?: string;
    quote?: boolean;
    replyAll?: boolean;
    attach?: string[];
    attachInline?: InlineAttachmentInput[];
    blobKeys?: string[];
    from?: string;
    autoFromAddressedAlias?: boolean;
    omitRecipients?: boolean;
  } & SignatureFlags;

  // `blobs` are the files f.blobKeys named, already read by readBlobFiles (async,
  // so the caller does it). REQUIRED, not defaulted: a caller that forgot to
  // read them would save the draft without the files and report success.
  function appendDraftFlags(args: GogArg[], f: DraftFlags, blobs: readonly BlobFile[]): void {
    assertNotBoth('bodyHtml', 'bodyHtmlFile', f.bodyHtml, f.bodyHtmlFile);
    // Server paths are read on the gog host and mailed out: confined (SEC-3).
    // On a hosted deployment a path that is not there says so, and names blobKeys.
    confineUploadPaths(f.attach, 'attach', { alternative: ATTACH_INLINE_ALTERNATIVE });
    if (f.bodyHtmlFile) confinePath(f.bodyHtmlFile, 'bodyHtmlFile');
    confineSignatureFile(f);
    // `!== undefined`, not truthiness: since gog 0.44 `drafts update` keeps an
    // OMITTED recipient field and clears one passed EMPTY, so '' is a request
    // that must reach gog. On create an empty flag is simply no recipients.
    if (!f.omitRecipients) {
      if (f.to !== undefined) args.push(`--to=${f.to}`);
      if (f.cc !== undefined) args.push(`--cc=${f.cc}`);
      if (f.bcc !== undefined) args.push(`--bcc=${f.bcc}`);
    }
    args.push(`--subject=${f.subject}`);
    // body is required, so this is an either/or swap rather than an extra push:
    // --body and --body-file together are a hard error in gog.
    args.push(payloadArg('body', 'body-file', f.body));
    if (f.bodyHtml) args.push(payloadArg('body-html', 'body-html-file', f.bodyHtml, 'html'));
    else if (f.bodyHtmlFile) args.push(`--body-html-file=${f.bodyHtmlFile}`);
    // A draft can reply to a specific message (--reply-to-message-id) or thread
    // off the latest message in a thread (--thread-id, which gog resolves
    // server-side). replyToMessageId wins when both are supplied.
    if (f.replyToMessageId) args.push(`--reply-to-message-id=${f.replyToMessageId}`);
    else if (f.replyToThreadId) args.push(`--thread-id=${f.replyToThreadId}`);
    // --reply-all infers original recipients; gog requires a reply target above.
    if (f.replyAll) args.push('--reply-all');
    if (f.replyTo) args.push(`--reply-to=${f.replyTo}`);
    if (f.quote) args.push('--quote');
    if (f.attach) for (const path of f.attach) args.push(`--attach=${path}`);
    // Same repeatable --attach flag, but the bytes travel with the call: the
    // runner writes each one to a temp file beside gog and passes that path.
    // This is the only attachment route that works when the caller and gog do
    // not share a filesystem (a hosted deployment such as mcp-host).
    // `args` is passed so the size check sees the body, which shares the budget.
    args.push(...inlineAttachmentArgs('attach', f.attachInline, args));
    // Uploaded files (blobKeys): same flag, bytes from the upload store, outside
    // the request budget the inline check enforces.
    for (const blob of blobs) args.push(blob.arg);
    if (f.from) args.push(`--from=${f.from}`);
    appendSignatureFlags(args, f);
    // PINNED, not conditional: GOG_GMAIL_AUTO_FROM_ADDRESSED_ALIAS in the host env
    // silently changes which address the mail goes out FROM, with nothing in the arg
    // array to show for it — and a hosted deployment's env is not the caller's to set.
    // An explicit flag is the only value authoritative everywhere.
    args.push(f.autoFromAddressedAlias ? '--auto-from-addressed-alias' : '--auto-from-addressed-alias=false');
  }

  // Run a draft write, then — when returnFull is set — re-fetch the stored
  // draft so the caller can verify subject/body/recipients persisted without a
  // separate gog_gmail_drafts_get round trip. For updates the id is known up
  // front; for creates it's read from the write response's draftId. Degrades to
  // the raw write result if the id can't be determined.
  /** The write succeeded; only the `returnFull` re-read did not. Hand back the
   *  acknowledgement, and say plainly which half failed — a caller that cannot
   *  tell those apart will either re-send or delete the wrong copy.
   *
   *  A missing id and any OTHER read failure are different stories and get
   *  different text. Gating on DRAFT_NOT_FOUND_PATTERN — the same test
   *  forkAwareDraftFailure uses — keeps the fork explanation for the case that
   *  actually looks like one; a permission error, a timeout or a transport fault
   *  keeps its own message instead of being retold as a fork, which would both
   *  mislead and discard the only text saying what really went wrong. */
  function withRefetchNote(written: CallToolResult, draftId: string, refetch: CallToolResult): CallToolResult {
    const detail = resultText(refetch)?.trim();
    const looksForked = detail !== undefined && DRAFT_NOT_FOUND_PATTERN.test(detail);
    const because = looksForked
      ? 'the id did not resolve, which on this mailbox usually means the draft was forked by a mail client ' +
        'between the write and the read. Run gog_gmail_drafts_list to find the current id'
      : `the read failed for a different reason, reported verbatim here: ${detail ?? '(no detail supplied)'}. ` +
        'That is a failure of the READ ONLY';
    return {
      ...written,
      content: [
        ...written.content,
        {
          type: 'text' as const,
          text:
            `Note: the write to draft ${draftId} SUCCEEDED and is acknowledged above. The follow-up ` +
            `read-back requested by returnFull could not be performed — ${because}. Nothing was lost; ` +
            `run gog_gmail_drafts_get on ${draftId} to confirm the saved content.`,
        },
      ],
    };
  }

  async function writeDraft(
    args: GogArg[],
    account: string | undefined,
    returnFull: boolean | undefined,
    knownDraftId?: string,
    intent?: ThreadingIntent,
  ): Promise<CallToolResult> {
    const result = await runOrDiagnose(args, { account });
    // The write must have returned a JSON acknowledgement before anything is
    // read from it. A failed write (an error result, not JSON) is surfaced
    // as-is rather than masked by re-fetching the unchanged draft — this
    // matters for the update path, where a known draftId would otherwise
    // re-fetch a stale draft — and there is nothing to verify threading
    // against either.
    let ack: Record<string, unknown>;
    let ackDraftId: string | undefined;
    try {
      ack = JSON.parse(resultText(result) ?? '') as Record<string, unknown>;
      ackDraftId = typeof ack.draftId === 'string' ? ack.draftId : undefined;
    } catch {
      return result;
    }
    // Threading is read from the WRITE ack: inReplyTo/references/
    // replyContextSource are reported only there, and the returnFull re-fetch
    // below does not carry them. Costs no extra gog invocation.
    const verification = intent ? verifyThreading(intent, ack) : undefined;
    let final = result;
    if (returnFull) {
      const draftId = knownDraftId ?? ackDraftId;
      // Same PIN as gog_gmail_drafts_get — this re-fetch is handed to the caller
      // verbatim, so its attachments[] shape must not depend on the host env.
      if (draftId) {
        const refetched = await runOrDiagnose(['gmail', 'drafts', 'get', pos(draftId), '--use-indexed-attachment-ids=false'], { account });
        // ONLY adopt the re-fetch when it worked. `returnFull` is a convenience
        // read AFTER an acknowledged write; a 404 here means the draft moved (an
        // Apple Mail fork between write and read is exactly the case this file
        // exists for), NOT that the write failed.
        //
        // Returning the failed read in place of the successful write made every
        // downstream consumer read the write as failed: forkAwareDraftFailure
        // diagnosed DRAFT_FORKED, and the content-loss note told the caller
        // "NOTHING WAS SAVED" about content that had just been saved. That is the
        // most destructive thing this tool can say to someone about to tidy up
        // the sibling copy.
        if (refetched.isError !== true) final = refetched;
        else final = withRefetchNote(result, draftId, refetched);
      }
    }
    if (!verification) return final;
    return withThreadingVerification(final, verification);
  }

  server.registerTool('gog_gmail_drafts_create', {
    description: 'SAVES ONLY. DOES NOT SEND. Create a new Gmail draft. Recipients (to/cc/bcc) are optional; omit them (or set omitRecipients) to create a recipient-less draft as an accidental-send guard. For replies, prefer replyToThreadId (anchors to the thread\'s latest message) or replyToMessageId (a specific message) — don\'t pass a thread id into replyToMessageId, which mis-threads silently.',
    annotations: { destructiveHint: false, openWorldHint: true },
    inputSchema: z.object(draftWriteSchema),
  }, async ({ account, returnFull, ...input }) => {
    // Only bodyFormat markdown adds an HTML part on create; plain text stays
    // plain, exactly as before.
    const flags = resolveBodyParts(input, input.bodyFormat === 'markdown');
    const blobs = await readBlobFiles(flags.blobKeys, 'attach');
    const args: GogArg[] = ['gmail', 'drafts', 'create'];
    appendDraftFlags(args, flags, blobs);
    // Uploaded files are deleted only once the draft holds them.
    return releaseBlobs(await writeDraft(args, account, returnFull), blobs);
  });

  server.registerTool('gog_gmail_drafts_update', {
    description:
      'Update an existing Gmail draft. For replies, prefer replyToThreadId (threads off the thread\'s latest message) or ' +
      'replyToMessageId (a specific message) over passing a thread id into replyToMessageId. An update preserves the draft\'s ' +
      'existing reply context (In-Reply-To/References) and its threadId; it never invents reply headers for a draft that is not ' +
      'a reply. Attachment semantics: supplying attach REPLACES the draft\'s existing attachments; omitting it preserves them; ' +
      'set clearAttachments to remove all. ' +
      'REPAIRING THREADING IN PLACE: passing replyToThreadId re-anchors the draft onto that thread and lets gog resolve ' +
      'In-Reply-To/References from the thread\'s latest sent-or-received message, KEEPING THE SAME DRAFT ID — so a draft that ' +
      'lost its reply headers (typically one a mail client rewrote from scratch) is adopted back onto the conversation in a ' +
      'single call. Whenever you change reply context (replyToThreadId, replyToMessageId or clearReplyContext) the result gains ' +
      'a `threadingVerification` block reporting the effective threadId/inReplyTo/references/replyContextSource, an `ok` flag ' +
      'and a plain-English note, so you can confirm the repair WITHOUT a raw-header fetch and without a second call. Read it: an ' +
      'explicit reply target REPLACES the draft\'s stored lineage rather than merging with it, and if the target thread yields ' +
      'no reply headers the draft is still MOVED onto that thread — it would arrive inside the conversation but not as a reply. ' +
      'TWO WAYS TO CHANGE THE BODY. (1) Whole body: pass `body` and it replaces the stored text. (2) Patch: pass `replace` ' +
      '([{old, new}], each `old` must occur EXACTLY once in the stored text), `append` and/or `prepend` INSTEAD of `body`; ' +
      'the tool reads the stored plain text, applies the edits and writes the result, so an edit to one paragraph never resends ' +
      'the rest. Zero or several matches is an error that writes NOTHING and returns the current text. In both modes, when ' +
      'bodyHtml/bodyHtmlFile are omitted the HTML part is GENERATED from the plain text (minimal markdown: paragraphs, "- " ' +
      'and "1. " lists, **bold**, *italic*, "> " quotes), so the two parts cannot drift; set htmlFromText false to send plain ' +
      'text only. `subject` may be omitted: the stored subject is kept. If a sibling copy ' +
      'of this draft exists, diff them with gog_gmail_drafts_diff and merge BEFORE updating, or whatever text the new body ' +
      'does not hold is lost. A 404 comes back diagnosed rather than as a bare notFound, and the diagnosis is checked against a draft ' +
      'listing first: GOOGLE_404_NOT_THE_DRAFT when the draft is still listed — because replyToThreadId and replyToMessageId ' +
      'resolve their own Google entities and a miss on either 404s with the identical message — and DRAFT_FORKED otherwise. ' +
      'That listing is capped at 20 drafts, so DRAFT_FORKED reports under `listingEvidence` whether its own evidence actually ' +
      'covers the mailbox: only `complete-listing` (the window came back short of 20, so it saw the whole Drafts folder) says ' +
      'the draft is gone. `capped-listing` and `listing-unavailable` say in words that they establish nothing about the draft, ' +
      'and any reply target you passed is echoed there with its explanation listed first.',
    annotations: { destructiveHint: false, openWorldHint: true },
    inputSchema: z.object({
      draftId: z.string().describe('Draft ID'),
      ...draftWriteSchema,
      subject: z.string().optional().describe('Subject. Omit to keep the draft\'s stored subject (costs one read of the draft).'),
      body: z.string().optional().describe('The WHOLE new body (plain text). Any size — a large body is written to a temp file on the gog server. Omit it when patching with replace/append/prepend; exactly one of the two modes must be used.'),
      replace: z.array(z.object({
        old: z.string().describe('Exact text to find in the draft\'s stored plain-text body. Must occur exactly once.'),
        new: z.string().describe('Text to put in its place ("" deletes it).'),
      })).optional().describe('Exact-match edits applied in order to the stored plain text, each against the text as the earlier ones left it. Every `old` must occur EXACTLY once; otherwise nothing is written and the error returns the current text.'),
      append: z.string().optional().describe('Text added at the end of the stored body (after a blank line). Patch mode.'),
      prepend: z.string().optional().describe('Text added at the start of the stored body (before a blank line). Patch mode.'),
      htmlFromText: z.boolean().optional().describe('Default true: when bodyHtml/bodyHtmlFile are omitted, generate the HTML part from the plain text so both parts match. false sends plain text only (gog then drops any stored HTML part).'),
      clearAttachments: z.boolean().optional().describe('Remove all attachments from the draft. By default, omitting attach preserves the draft\'s existing attachments; this intentionally clears them. Ignored if attach is also supplied (attach replaces).'),
      clearReplyContext: z.boolean().optional().describe('Strip In-Reply-To/References from the draft, turning a reply back into a standalone message while keeping the same draft id and threadId. Use this to repair a mis-threaded draft in place instead of deleting and recreating it. Mutually exclusive with replyToMessageId, replyToThreadId and quote — gog rejects the call if any of them is combined with this.'),
      forkSiblingDraftId: z.string().optional().describe('Id of the OTHER copy of this draft — the one a mail client left behind, or the one you are merging from. Because gog requires a body on every update, this call rewrites the WHOLE body; naming a sibling makes the tool read that draft FIRST (one extra gog call, on this id only — it never scans) and refuse to write if your body omits any line the sibling still holds, naming the exact lines. Set acceptContentLoss to write anyway. Omit this param and nothing extra is spent. It is purely a text comparison and makes NO claim that either draft replaced the other — for that verdict use gog_gmail_drafts_diff.'),
      acceptContentLoss: z.boolean().optional().describe('Write even though the forkSiblingDraftId check found lines your body drops — or could not be run at all (sibling unfetchable/unreadable). Without it either outcome refuses the write and changes nothing. The lines are still reported on the result under contentLossCheck. Ignored when forkSiblingDraftId is not set.'),
    }),
  }, async ({ draftId, account, returnFull, clearAttachments, clearReplyContext, forkSiblingDraftId, acceptContentLoss, replace, append, prepend, htmlFromText, ...input }) => {
    const patching = (replace?.length ?? 0) > 0 || append !== undefined || prepend !== undefined;
    if (patching && input.body !== undefined) {
      return errorResult('Pass EITHER body (replace the whole body) OR replace/append/prepend (patch the stored body), not both. Nothing was written.');
    }
    if (!patching && input.body === undefined) {
      return errorResult('body is required unless you patch the stored body with replace, append or prepend. Nothing was written.');
    }
    // Patching, or keeping the stored subject, needs the draft as it is now:
    // ONE read, before anything is written. Whole-body with a subject reads nothing.
    let body = input.body ?? '';
    let subject = input.subject;
    if (patching || subject === undefined) {
      const stored = await readStoredDraft(draftId, account);
      if ('result' in stored) return forkAwareDraftFailure(stored.result, 'gog_gmail_drafts_update', draftId, account);
      subject ??= headerValue(parseHeaders(stored.message.payload), 'Subject') ?? '';
      if (patching) {
        const current = storedBodyText(stored.message.payload);
        const outcome = applyTextPatch(current.text, { replace, append, prepend });
        if (!outcome.ok) return patchRefusal(draftId, outcome.reason, current);
        body = outcome.text;
      }
    }
    const flags = resolveBodyParts({ ...input, subject, body }, htmlFromText !== false);
    // BEFORE the write, never after: a report on an overwrite that already
    // happened is not a guard. Skipped entirely — zero extra invocations — when
    // no sibling was named.
    let check: ContentLossCheck | undefined;
    let overridden = false;
    if (forkSiblingDraftId) {
      check = await checkSiblingContentLoss(forkSiblingDraftId, flags.body, account);
      if (check.status !== 'clean' && !acceptContentLoss) return contentLossRefusal(draftId, check);
      overridden = check.status !== 'clean';
    }
    const blobs = await readBlobFiles(flags.blobKeys, 'attach');
    const args: GogArg[] = ['gmail', 'drafts', 'update', pos(draftId)];
    appendDraftFlags(args, flags, blobs);
    if (clearAttachments) args.push('--clear-attachments');
    if (clearReplyContext) args.push('--clear-reply-context');
    const intent = threadingIntentOf({ ...flags, clearReplyContext });
    const result = await writeDraft(args, account, returnFull, draftId, intent);
    const reported = await forkAwareDraftFailure(
      result, 'gog_gmail_drafts_update', draftId, account,
      intent?.requested === 'set' ? { via: intent.via, target: intent.target } : undefined,
    );
    // The acknowledgement is derived from the OUTCOME, never predicted before
    // it. Appending "the update WAS written" ahead of the write meant every
    // failed write — a 404, a permission error — came back `isError: true`
    // carrying that sentence, which is the single most destructive thing this
    // tool could tell a caller who is about to tidy up the sibling copy.
    if (check !== undefined && overridden) {
      check = reported.isError === true
        ? {
          ...check,
          acknowledged: true,
          written: false,
          note: `${check.note} acceptContentLoss was set, so the write was ATTEMPTED — but it FAILED and NOTHING WAS SAVED. ` +
            `Draft ${draftId} is unchanged and the lines listed above still exist in draft ${check.siblingDraftId}; nothing was ` +
            'lost by this call. Read the error above before retrying.',
        }
        : {
          ...check,
          acknowledged: true,
          written: true,
          note: `${check.note} acceptContentLoss was set, so the update WAS written despite this: draft ${draftId} now holds ` +
            `only the body you passed, and the lines listed above exist only in draft ${check.siblingDraftId}.`,
        };
    }
    return releaseBlobs(check ? withContentLossCheck(reported, check) : reported, blobs);
  });

  server.registerTool('gog_gmail_drafts_delete', {
    description: 'Permanently delete a Gmail draft (not reversible — drafts do not go to Trash). Requires force:true to delete non-interactively.',
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      draftId: z.string().describe('Draft ID'),
      force: z.boolean().optional().describe('Required to delete in this non-interactive context — without it the delete is refused as a safety guard.'),
      account: accountParam,
    }),
  }, async ({ draftId, account, force }) => {
    const args: GogArg[] = ['gmail', 'drafts', 'delete', pos(draftId)];
    if (force) args.push('--force');
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_gmail_drafts_send', {
    description:
      'SENDS MAIL — reads the stored draft and asks the MCP host to show a confirmation prompt with its recipients, subject, a preview of the body and the attachment names; the draft is sent only after the user accepts. ' +
      'Send an existing Gmail draft. If the id no longer resolves, the 404 comes back as a DRAFT_FORKED report — what happened, ' +
      'the drafts that do exist (with their free origin/rootsOwnThread fields) and what to do next — rather than a bare ' +
      'notFound. It names no replacement: that judgement needs a named pair and gog_gmail_drafts_diff. If the draft turns out ' +
      'to be still listed, the answer is GOOGLE_404_NOT_THE_DRAFT instead and claims no fork at all.' +
      CONFIRM_FALLBACK_DESCRIPTION +
      ' The token is bound to the draft\'s current messageId, so a draft edited or re-saved between the two calls (a mail ' +
      'client rotates the messageId on every save) is DRAFT_CHANGED, never sent unseen.',
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      draftId: z.string().describe('Draft ID to send'),
      account: accountParam,
      confirmToken: confirmTokenParam,
    }),
  }, async ({ draftId, account, confirmToken }, ctx) => {
    // Sending a staged draft dispatches mail as irreversibly as gog_gmail_send,
    // so it goes through the same confirmation rail (audit SEC-2) — otherwise
    // drafts_create + drafts_send is an unconfirmed route around it. The prompt
    // is built from the STORED draft, since that, not anything the caller says,
    // is what will go out. A draft that no longer resolves takes the same
    // fork-aware path a failed send always has.
    const got = await runOrDiagnose(['gmail', 'drafts', 'get', pos(draftId)], { account });
    if (got.isError) return forkAwareDraftFailure(got, 'gog_gmail_drafts_send', draftId, account);
    const raw = resultText(got) ?? '';
    const preview = previewStoredDraft(raw);
    // The drafts get above runs on EVERY call, so on phase 2 of the token
    // fallback it is the re-read the token is checked against.
    const skipped = confirmationSkippedFor('gmail.drafts-send', { to: preview.to, cc: preview.cc, bcc: preview.bcc });
    const confirmation = skipped ? undefined : await requireGmailDispatchConfirmation(ctx, 'gmail.drafts-send', { draftId, ...preview }, {
      tool: 'gog_gmail_drafts_send',
      account,
      args: { draftId, account },
      confirmToken,
      subject: () => storedDraftTokenSubject(raw, draftId, account),
    });
    if (confirmation) return confirmation;
    const result = await runOrDiagnose(['gmail', 'drafts', 'send', pos(draftId)], { account });
    if (!result.isError) logGmailDispatch('gog_gmail_drafts_send', preview.recipients, account);
    const reported = await forkAwareDraftFailure(result, 'gog_gmail_drafts_send', draftId, account);
    return skipped ? withConfirmSkippedNote(reported) : reported;
  });

  server.registerTool('gog_gmail_drafts_copy_to', {
    description:
      'SENDS MAIL — sends a COPY of a stored draft (its current subject and body, text and HTML parts) to the addresses you ' +
      'name, for review: the classic "DRAFT: <subject>" copy to someone who should read it before it goes out. The draft ' +
      'itself is NOT touched, and nothing of its addressing comes along: not its recipients, not its threading, not its ' +
      'attachments. You never pass the body — the tool reads it from the draft — so a review copy costs no more than its ' +
      'arguments. The confirmation prompt shows the recipients, the subject, the first ' + COPY_TO_PREVIEW_CHARS + ' ' +
      'characters of the body, its length and its SHA-256 — NOT the whole body. `appendText` adds a note below the body; ' +
      '`includeQuotedFrom` appends the text of another message (e.g. the one the draft answers) below a separator. ' +
      `If the server sets ${CONFIRM_SKIP_TO_ENV} and EVERY To/Cc/Bcc address is on it, no confirmation is asked and the result says so.` +
      CONFIRM_FALLBACK_DESCRIPTION +
      ' The token is bound to the draft\'s current messageId, so a draft edited between the two calls is DRAFT_CHANGED, never sent unseen.',
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      draftId: z.string().describe('The draft to copy. It is read, never modified.'),
      to: z.string().describe('Who receives the copy (comma-separated).'),
      cc: z.string().optional().describe('CC for the copy (comma-separated).'),
      bcc: z.string().optional().describe('BCC for the copy (comma-separated).'),
      subjectPrefix: z.string().optional().describe('Prefix for the copy\'s subject (default "DRAFT: "; "" for none).'),
      appendText: z.string().optional().describe('A note added below the draft\'s body in the copy (plain text; rendered into the HTML part too).'),
      includeQuotedFrom: z.string().optional().describe('A Gmail message id whose text is appended below a separator — typically the message the draft replies to, so the reviewer sees what is being answered. Costs one extra read.'),
      account: accountParam,
      confirmToken: confirmTokenParam,
    }),
  }, async ({ draftId, to, cc, bcc, subjectPrefix, appendText, includeQuotedFrom, account, confirmToken }, ctx) => {
    // Read on EVERY call: on phase 2 of the token fallback this is the re-read
    // the token is checked against.
    const stored = await readStoredDraft(draftId, account);
    if ('result' in stored) return forkAwareDraftFailure(stored.result, 'gog_gmail_drafts_copy_to', draftId, account);
    let quoted: GmailStoredMessage | undefined;
    if (includeQuotedFrom) {
      try {
        quoted = (JSON.parse(await run(['gmail', 'get', pos(includeQuotedFrom), '--format=full'], { account, opaqueFields: ['data', 'attachmentId'] })) as { message?: GmailStoredMessage }).message;
      } catch (err) {
        return diagnose(err);
      }
      if (!quoted) return errorResult(`Could not read message ${includeQuotedFrom} to quote: gog returned no \`message\` object. Nothing was sent.`);
    }
    const copy = buildDraftCopy(stored.message, { subjectPrefix: subjectPrefix ?? 'DRAFT: ', appendText, quoted });
    if (copy.text === '' && copy.html === undefined) {
      return errorResult(`Draft ${draftId} has no body to copy. Nothing was sent.`);
    }
    const args: GogArg[] = ['gmail', 'send', `--to=${to}`, `--subject=${copy.subject}`, payloadArg('body', 'body-file', copy.text)];
    if (cc) args.push(`--cc=${cc}`);
    if (bcc) args.push(`--bcc=${bcc}`);
    if (copy.html !== undefined) args.push(payloadArg('body-html', 'body-html-file', copy.html, 'html'));

    const recipients = extractEmails(to, cc, bcc);
    const sha256 = bodySha256(copy.text);
    const summary = {
      draftId,
      to,
      ...(cc ? { cc } : {}),
      ...(bcc ? { bcc } : {}),
      recipients,
      subject: copy.subject,
      bodyLength: copy.text.length,
      bodySha256: sha256,
      bodyStart: copy.text.length > COPY_TO_PREVIEW_CHARS ? `${copy.text.slice(0, COPY_TO_PREVIEW_CHARS)}…` : copy.text,
      hasHtmlPart: copy.html !== undefined,
      ...(appendText ? { appendedNoteLength: appendText.length } : {}),
      ...(includeQuotedFrom ? { quotesMessageId: includeQuotedFrom } : {}),
      draftUnchanged: true,
    };
    const skipped = confirmationSkippedFor('gmail.drafts-copy-to', { to, cc, bcc });
    const confirmation = skipped ? undefined : await requireGmailDispatchConfirmation(ctx, 'gmail.drafts-copy-to', summary, {
      tool: 'gog_gmail_drafts_copy_to',
      account,
      args: { draftId, to, cc, bcc, subjectPrefix, appendText, includeQuotedFrom, account },
      confirmToken,
      // The WHOLE copy is hashed into the token; only the summary is shown.
      subject: () => ({
        target: draftId,
        revision: stored.message.id,
        payload: { to, cc, bcc, subject: copy.subject, text: copy.text, html: copy.html },
        preview: summary,
      }),
    });
    if (confirmation) return confirmation;
    const result = await runOrDiagnose(args, { account });
    if (!result.isError) logGmailDispatch('gog_gmail_drafts_copy_to', recipients, account);
    return skipped ? withConfirmSkippedNote(result) : result;
  });

  server.registerTool('gog_gmail_import', {
    description:
      'Import an existing RFC822/EML message INTO the mailbox. This is Gmail\'s import path, not a send: nothing ' +
      'leaves the account, and the message keeps its own From/Date/Message-Id headers so it files where it ' +
      'belongs chronologically. Use it to restore an exported message or to file a .eml under a label; to ' +
      'actually send mail use gog_gmail_send, and to stage one use gog_gmail_drafts_create. The file is read on ' +
      'the gog SERVER, not your machine — on a hosted deployment upload it with gog_upload_slots and pass blobKeys instead.',
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      file: z.string().optional().describe('Path to an RFC822/EML file that ALREADY EXISTS on the gog server (exactly one of file or blobKeys). gog also accepts "-" for stdin, but this server never writes to gog\'s stdin, so "-" would hang until the call times out.'),
      blobKeys: singleBlobKeyParam,
      labels: z.array(z.string()).optional().describe('Labels to apply to the imported message (repeatable). Each may be a label ID or a label name — names are resolved server-side. A name containing a COMMA cannot be passed here: gog declares --label as a Kong slice with no separator override, so Kong splits each value on commas and "Clients, Inc" is looked up as two labels ("Clients" and "Inc") and fails. Use that label\'s ID instead — ids never contain a comma; gog_gmail_labels_list gives you one.'),
      internalDateSource: z.enum(['dateHeader', 'receivedTime']).optional().describe('Which clock sets Gmail\'s internal date: dateHeader (gog default — the message\'s own Date header, so it sorts into the mailbox at its original time) or receivedTime (now).'),
      neverMarkSpam: z.boolean().optional().describe('Never classify the imported message as spam.'),
      processForCalendar: z.boolean().optional().describe('Process calendar invitations inside the imported message — this can ADD EVENTS to your calendar.'),
      account: accountParam,
    }),
  }, async ({ file, blobKeys, labels, internalDateSource, neverMarkSpam, processForCalendar, account }) => {
    if (file !== undefined) confineUploadPath(file, 'file');
    assertOneFileSource({ file, blobKeys });
    const blobs = await readBlobFiles(blobKeys, 'file', { positional: true });
    // Not gated: gogcli's internal/cmd/gmail_import.go has no confirmDestructive /
    // dryRunAndConfirmDestructive call site (checked at upstream v0.35.0, and a live
    // `--dry-run` against a v0.35.0 build proceeds), so no --force is appended.
    const args: GogArg[] = ['gmail', 'import', file !== undefined ? pos(file) : blobs[0]!.arg];
    if (labels) for (const label of labels) args.push(`--label=${label}`);
    if (internalDateSource) args.push(`--internal-date-source=${internalDateSource}`);
    if (neverMarkSpam) args.push('--never-mark-spam');
    if (processForCalendar) args.push('--process-for-calendar');
    return releaseBlobs(await runOrDiagnose(args, { account }), blobs);
  });

  server.registerTool('gog_gmail_forward', {
    description:
      'SENDS MAIL — asks the MCP host to show a confirmation prompt with the recipients, the note text, and attachment handling. '
      + 'Mail is sent only after the user accepts that prompt. To STAGE a forward instead of sending it, use '
      + 'gog_gmail_drafts_forward, which never needs confirmation. '
      + 'Forward an existing Gmail message to new recipients.'
      + CONFIRM_FALLBACK_DESCRIPTION,
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      messageId: z.string().describe('Gmail message ID to forward'),
      to: z.string().describe('Recipients (comma-separated; required)'),
      cc: z.string().optional().describe('CC recipients (comma-separated)'),
      bcc: z.string().optional().describe('BCC recipients (comma-separated)'),
      note: z.string().optional().describe('Introductory text above the forwarded message'),
      noteHtml: z.string().optional().describe('Introductory HTML above the forwarded message (gog >= 0.46). Combine with note to give the plain-text part its own wording; any size — a large note is written to a temp file on the gog server rather than inlined into the command line.'),
      from: z.string().optional().describe('Send from this email address (must be a verified send-as alias)'),
      skipAttachments: z.boolean().optional().describe('Do not include original attachments'),
      ...signatureSchema,
      account: accountParam,
      confirmToken: confirmTokenParam,
    }),
  }, async ({ messageId, to, cc, bcc, note, noteHtml, from, skipAttachments, signature, signatureFrom, signatureFile, account, confirmToken }, ctx) => {
    const sig = { signature, signatureFrom, signatureFile };
    confineSignatureFile(sig);
    const recipients = extractEmails(to, cc, bcc);
    const confirmation = await requireGmailDispatchConfirmation(ctx, 'gmail.forward', {
      messageId, to, cc, bcc, recipients, recipientCount: recipients.length,
      noteLength: (note ?? noteHtml ?? '').length,
      notePreview: bodyPreview(note ?? noteHtml),
      // With both, notePreview shows only the plain part; the HTML part can say
      // something else and must not leave unseen.
      ...(note && noteHtml ? { noteHtmlLength: noteHtml.length, noteHtmlPreview: bodyPreview(noteHtml) } : {}),
      skipAttachments: Boolean(skipAttachments),
      attachmentsIncluded: !skipAttachments,
      ...(signaturePreview(sig) ? { signature: signaturePreview(sig) } : {}),
    }, {
      tool: 'gog_gmail_forward',
      account,
      args: { messageId, to, cc, bcc, note, noteHtml, from, skipAttachments, signature, signatureFrom, signatureFile, account },
      confirmToken,
      // Fallback only: read what is being forwarded, so the user sees whose
      // message and which attachments leave, and phase 2 re-reads it.
      subject: async () => {
        const meta = await runOrDiagnose(['gmail', 'get', pos(messageId), '--format=metadata'], { account });
        if (meta.isError) return meta;
        const original = parseForwardMetadata(resultText(meta) ?? '');
        const attachments = skipAttachments ? [] : original.attachments;
        const sender = senderPreview(account, from);
        const subject = original.subject ? `Fwd: ${original.subject}` : undefined;
        // Hashed by content, so an edited signature file is a changed send.
        const localFiles = attachmentDetails(signatureFile ? [signatureFile] : undefined, undefined);
        return {
          target: messageId,
          payload: { from: sender, to, cc, bcc, subject, note, noteHtml, attachments, original, signature: Boolean(signature), signatureFrom, localFiles },
          preview: {
            from: sender, to, cc, bcc, subject,
            body: note,
            ...(noteHtml ? { noteHtml } : {}),
            ...(signaturePreview(sig) ? { signature: signaturePreview(sig) } : {}),
            forwarding: { messageId, from: original.from, subject: original.subject, date: original.date, messageIdHeader: original.messageIdHeader },
            attachments,
            threadId: original.threadId,
          },
        };
      },
    });
    if (confirmation) return confirmation;
    const args: GogArg[] = ['gmail', 'forward', pos(messageId), `--to=${to}`];
    if (cc) args.push(`--cc=${cc}`);
    if (bcc) args.push(`--bcc=${bcc}`);
    if (note) args.push(payloadArg('note', 'note-file', note));
    if (noteHtml) args.push(payloadArg('note-html', 'note-html-file', noteHtml, 'html'));
    if (from) args.push(`--from=${from}`);
    if (skipAttachments) args.push('--skip-attachments');
    appendSignatureFlags(args, sig);
    const result = await runOrDiagnose(args, { account });
    if (!result.isError) logGmailDispatch('gog_gmail_forward', recipients, account);
    return result;
  });

  // gog >= 0.36.0: the draft-side twins of reply / reply-all / forward. They
  // take the SAME flag set as the send-side commands and share the composition
  // path with them, so replySchema/appendReplyFlags are imported from the base
  // package (where gog_gmail_reply itself now lives) rather than re-declared —
  // the only difference is the subcommand and that NOTHING IS SENT.
  //
  // These exist because staging a reply used to mean gog_gmail_drafts_create
  // with replyToMessageId/replyToThreadId, which threads the draft but does NOT
  // inherit the original's recipients or quote its body — the caller had to
  // rebuild both by hand, and a missed Cc is invisible until the draft goes
  // out. Here the inheritance is gog's, identical to what the send path would
  // have produced.
  const draftReplyNote =
    ' Composes exactly what gog_gmail_reply%s would send — inherited recipients, "Re:" subject and quoted ' +
    'original — but SAVES IT AS A DRAFT instead of sending. Nothing leaves the mailbox; send it later with ' +
    'gog_gmail_drafts_send, or edit it first with gog_gmail_drafts_update (which overwrites the whole body, ' +
    'quote included — read the draft back before editing).';

  server.registerTool('gog_gmail_drafts_reply', {
    description:
      'SAVES ONLY. DOES NOT SEND. Save a reply to a Gmail message as a draft (to the original sender only).' + draftReplyNote.replace('%s', '') +
      ' Prefer this over gog_gmail_drafts_create + replyToMessageId when the draft is a real reply: that route threads ' +
      'the draft but leaves recipients and quoting for you to reconstruct.',
    annotations: { destructiveHint: false, openWorldHint: true },
    inputSchema: z.object({ ...replySchema, returnFull: draftWriteSchema.returnFull }),
  }, async ({ messageId, account, returnFull, ...flags }) => {
    const blobs = await readBlobFiles(flags.blobKeys, 'attach');
    const args: GogArg[] = ['gmail', 'drafts', 'reply', pos(messageId)];
    appendReplyFlags(args, flags, blobs);
    return releaseBlobs(await writeDraft(args, account, returnFull), blobs);
  });

  server.registerTool('gog_gmail_drafts_reply_all', {
    description:
      'SAVES ONLY. DOES NOT SEND. Save a reply-all to a Gmail message as a draft (sender plus every To/Cc recipient).' +
      draftReplyNote.replace('%s', '_all') +
      ' Use the remove flag to drop recipients BEFORE the draft exists, rather than editing them out afterwards.',
    annotations: { destructiveHint: false, openWorldHint: true },
    inputSchema: z.object({ ...replySchema, returnFull: draftWriteSchema.returnFull }),
  }, async ({ messageId, account, returnFull, ...flags }) => {
    const blobs = await readBlobFiles(flags.blobKeys, 'attach');
    const args: GogArg[] = ['gmail', 'drafts', 'reply-all', pos(messageId)];
    appendReplyFlags(args, flags, blobs);
    return releaseBlobs(await writeDraft(args, account, returnFull), blobs);
  });

  server.registerTool('gog_gmail_drafts_forward', {
    description:
      'SAVES ONLY. DOES NOT SEND. Save a forward of a Gmail message as a draft. Same composition as gog_gmail_forward — the original ' +
      'message quoted below an optional note, with its attachments carried over — but nothing is sent. ' +
      'Unlike gog_gmail_forward, `to` is OPTIONAL here: omit it to stage a recipient-less forward as an ' +
      'accidental-send guard, then add recipients with gog_gmail_drafts_update before gog_gmail_drafts_send.',
    annotations: { destructiveHint: false, openWorldHint: true },
    inputSchema: z.object({
      messageId: z.string().describe('Gmail message ID to forward'),
      to: z.string().optional().describe('Recipients (comma-separated). Optional for a draft — omit to stage the forward without recipients.'),
      cc: z.string().optional().describe('CC recipients (comma-separated)'),
      bcc: z.string().optional().describe('BCC recipients (comma-separated)'),
      note: z.string().optional().describe('Introductory text above the forwarded message'),
      noteHtml: z.string().optional().describe('Introductory HTML above the forwarded message (gog >= 0.46). Combine with note to give the plain-text part its own wording; any size — a large note is written to a temp file on the gog server rather than inlined into the command line.'),
      from: z.string().optional().describe('Send from this email address (must be a verified send-as alias)'),
      skipAttachments: z.boolean().optional().describe('Do not include original attachments'),
      ...signatureSchema,
      returnFull: draftWriteSchema.returnFull,
      account: accountParam,
    }),
  }, async ({ messageId, to, cc, bcc, note, noteHtml, from, skipAttachments, signature, signatureFrom, signatureFile, returnFull, account }) => {
    const sig = { signature, signatureFrom, signatureFile };
    confineSignatureFile(sig);
    const args: GogArg[] = ['gmail', 'drafts', 'forward', pos(messageId)];
    if (to) args.push(`--to=${to}`);
    if (cc) args.push(`--cc=${cc}`);
    if (bcc) args.push(`--bcc=${bcc}`);
    if (note) args.push(payloadArg('note', 'note-file', note));
    if (noteHtml) args.push(payloadArg('note-html', 'note-html-file', noteHtml, 'html'));
    if (from) args.push(`--from=${from}`);
    if (skipAttachments) args.push('--skip-attachments');
    appendSignatureFlags(args, sig);
    return writeDraft(args, account, returnFull);
  });

  server.registerTool('gog_gmail_autoreply', {
    description:
      'SENDS MAIL to every message matching the query — asks the MCP host to show a confirmation prompt containing '
      + 'a bounded search against the same query, including how many messages match and who sent them. Mail is sent '
      + 'only after the user accepts that prompt. There is no draft-only counterpart for this one: it acts across a query-defined '
      + 'set of messages rather than a single reply target, so gog has no "stage all of these as drafts" command to '
      + 'stand in for it — the confirmation prompt is this tool\'s only pre-send check. '
      + 'Reply once to all messages matching a Gmail search query. Use the label flag to dedupe across runs.'
      + CONFIRM_FALLBACK_DESCRIPTION,
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      query: z.string().describe('Gmail search query'),
      max: z.number().optional().describe('Max matching messages to inspect (default: 20)'),
      subject: z.string().optional().describe('Override reply subject (default: Re: original subject)'),
      body: z.string().optional().describe('Reply body (plain text; required unless bodyHtml is set)'),
      bodyHtml: z.string().optional().describe('Reply body HTML'),
      from: z.string().optional().describe('Send from this email address (must be a verified send-as alias)'),
      replyTo: z.string().optional().describe('Reply-To header address'),
      label: z.string().optional().describe('Label to add after replying (used for dedupe; default: AutoReplied)'),
      archive: z.boolean().optional().describe('Archive threads after auto-replying'),
      markRead: z.boolean().optional().describe('Mark threads as read after auto-replying'),
      skipBulk: z.boolean().optional().describe('Skip auto-generated/list mail'),
      allowSelf: z.boolean().optional().describe('Allow replying to messages sent by your own address'),
      account: accountParam,
      confirmToken: confirmTokenParam,
    }),
  }, async ({ query, max, subject, body, bodyHtml, from, replyTo, label, archive, markRead, skipBulk, allowSelf, account, confirmToken }, ctx) => {
    const searchResult = await runOrDiagnose(['gmail', 'search', pos(query), `--max=${max ?? 20}`], { account });
    if (searchResult.isError) return searchResult;
    const senders = parseSearchSenders(resultText(searchResult) ?? '{}');
    const sampleSenders = extractEmails(...senders);
    const confirmation = await requireGmailDispatchConfirmation(ctx, 'gmail.autoreply', {
      query,
      matchCount: senders.length,
      sampleSenders,
      subject: subject || undefined,
      bodyLength: (body ?? bodyHtml ?? '').length,
      bodyPreview: bodyPreview(body ?? bodyHtml),
      max: max ?? 20,
      label: label || 'AutoReplied',
      archive: Boolean(archive),
      markRead: Boolean(markRead),
    }, {
      tool: 'gog_gmail_autoreply',
      account,
      args: { query, max, subject, body, bodyHtml, from, replyTo, label, archive, markRead, skipBulk, allowSelf, account },
      confirmToken,
      // The search above runs on every call; binding its matches means a
      // different set of messages on phase 2 is DRAFT_CHANGED, not a surprise.
      subject: () => {
        const matches = parseSearchMatches(resultText(searchResult) ?? '{}');
        const sender = senderPreview(account, from);
        const options = {
          max: max ?? 20, label: label || 'AutoReplied', archive: Boolean(archive), markRead: Boolean(markRead),
          skipBulk: Boolean(skipBulk), allowSelf: Boolean(allowSelf),
        };
        return {
          target: query,
          payload: { from: sender, replyTo, subject, body, bodyHtml, matches, ...options },
          preview: {
            from: sender,
            to: sampleSenders,
            subject: subject || 'Re: <each original subject>',
            body: body ?? bodyHtml,
            ...(replyTo ? { replyTo } : {}),
            query,
            matchCount: matches.length,
            matches,
            ...options,
          },
        };
      },
    });
    if (confirmation) return confirmation;
    const args: GogArg[] = ['gmail', 'autoreply', pos(query)];
    if (max !== undefined) args.push(`--max=${max}`);
    if (subject) args.push(`--subject=${subject}`);
    if (body) args.push(payloadArg('body', 'body-file', body));
    // `gmail autoreply` has --body-file but NO --body-html-file (verified against
    // gog 0.34.1), so an HTML autoreply body stays inline and is still bounded by
    // the runner's per-arg cap. Route it through payloadArg if gog ever adds one.
    if (bodyHtml) args.push(`--body-html=${bodyHtml}`);
    if (from) args.push(`--from=${from}`);
    if (replyTo) args.push(`--reply-to=${replyTo}`);
    if (label) args.push(`--label=${label}`);
    if (archive) args.push('--archive');
    if (markRead) args.push('--mark-read');
    if (skipBulk) args.push('--skip-bulk');
    if (allowSelf) args.push('--allow-self');
    const result = await runOrDiagnose(args, { account });
    if (!result.isError) {
      const recipients = extractEmails(...parseAutoReplyRecipients(resultText(result) ?? '{}'));
      logGmailDispatch('gog_gmail_autoreply', recipients, account);
    }
    return result;
  });

  server.registerTool('gog_gmail_messages_search', {
    description: 'Search individual messages (not threads) using Gmail query syntax. Returns one result per matching message. '
      + 'Results are ALWAYS newest-first by Gmail\'s internalDate — the wrapper sorts them, so the first result is the most recent match. '
      + 'IMPORTANT — a response carrying "truncated": true is an INCOMPLETE view of the matches: NEVER report that a message does not exist on the strength of one. Page through it (pass nextPageToken back as `pageToken`), set maxPages to walk several pages in one call, or narrow the query first. '
      + 'If you already know the thread, read it with gog_gmail_thread_get instead of searching for it.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      query: z.string().describe('Gmail search query (e.g. "from:alice is:unread has:attachment")'),
      max: z.number().optional().describe('Max results'),
      pageToken: pageTokenParam,
      page: pageAliasParam,
      maxPages: z.number().int().positive().max(20).optional().describe('Walk up to this many pages in ONE call and merge the results, instead of returning a single page. Use it for existence questions (\"is there any mail matching X?\"), which a single page cannot answer. Stops early at the last page; if pages remain when the cap is hit the response is still marked truncated. Prefer this over all=true, which is unbounded.'),
      all: z.boolean().optional().describe('Fetch all pages'),
      includeBody: z.boolean().optional().describe('Include the decoded message body in each result'),
      full: z.boolean().optional().describe('Show full message bodies without truncation (implies includeBody)'),
      bodyFormat: z.enum(['text', 'html']).optional().describe('Body format preference when includeBody is set'),
      includeAttachments: z.boolean().optional().describe('Include each message\'s attachment metadata (filename, size, mimeType, id or index). NOT a cheap add-on: like includeBody it makes gog fetch every matching message at format=full, so it costs a full per-message read — narrow the query or lower max before turning it on.'),
      useIndexedAttachmentIds: z.boolean().optional().describe('Report each attachment as a 0-based `attachmentIndex` within its message instead of an opaque `attachmentId` (stable across calls, unlike the id). Only has an effect alongside includeAttachments or includeBody.'),
      includeRecipients: z.boolean().optional().describe('Include each message\'s To, Cc and Bcc in the results. Free: read from headers the search already fetches, no extra API calls.'),
      sanitizeContent: z.boolean().optional().describe('Return agent-oriented sanitized content, as gog_gmail_get does: HTML stripped, HTTP(S) URLs removed, header text sanitized. Shrinks includeBody results; the URL removal is lossy, so omit it when you need to follow a link.'),
      account: accountParam,
    }),
  }, async ({ query, max, pageToken, page, maxPages, all, includeBody, full, bodyFormat, includeAttachments, useIndexedAttachmentIds, includeRecipients, sanitizeContent, account }) => {
    const args: GogArg[] = ['gmail', 'messages', 'search', pos(query)];
    if (max !== undefined) args.push(`--max=${max}`);
    if (all) args.push('--all');
    if (includeBody) args.push('--include-body');
    if (full) args.push('--full');
    if (bodyFormat) args.push(`--body-format=${bodyFormat}`);
    if (includeRecipients) args.push('--include-recipients');
    if (sanitizeContent) args.push('--sanitize-content');
    // Both PINNED: GOG_GMAIL_INCLUDE_ATTACHMENTS and GOG_GMAIL_USE_INDEXED_ATTACHMENT_IDS
    // each change the result shape (and the first also the per-message API cost) with
    // nothing in the arg array to show for it. See gog_gmail_thread_get.
    args.push(includeAttachments ? '--include-attachments' : '--include-attachments=false');
    args.push(useIndexedAttachmentIds ? '--use-indexed-attachment-ids' : '--use-indexed-attachment-ids=false');
    // See gog_gmail_search: the cursor rides per page so the walk can advance it.
    const runPage = (tok: string | undefined) =>
      runOrDiagnose(tok ? [...args, `--page=${tok}`] : args, { account });
    const token = resolvePageToken({ pageToken, page });
    const result = maxPages !== undefined
      ? await fetchGmailPages(runPage, 'messages', maxPages, token)
      : await runPage(token);
    return finalizeGmailSearch(result, {
      itemsKey: 'messages',
      method: 'users.messages.list',
      query,
      account,
    });
  });

  server.registerTool('gog_gmail_labels_style', {
    description: "Change a user label's color or visibility (background/text color from Gmail's palette, label-list and message-list visibility).",
    annotations: { destructiveHint: false, openWorldHint: true },
    inputSchema: z.object({
      labelIdOrName: z.string().describe('Label ID or name to restyle'),
      backgroundColor: z.string().optional().describe("Background color from Gmail's label palette as #RRGGBB"),
      textColor: z.string().optional().describe("Text color from Gmail's label palette as #RRGGBB"),
      labelListVisibility: z.enum(['labelShow', 'labelShowIfUnread', 'labelHide']).optional().describe('Label-list visibility'),
      messageListVisibility: z.enum(['show', 'hide']).optional().describe('Message-list visibility'),
      account: accountParam,
    }),
  }, async ({ labelIdOrName, backgroundColor, textColor, labelListVisibility, messageListVisibility, account }) => {
    const args: GogArg[] = ['gmail', 'labels', 'style', pos(labelIdOrName)];
    if (backgroundColor) args.push(`--background-color=${backgroundColor}`);
    if (textColor) args.push(`--text-color=${textColor}`);
    if (labelListVisibility) args.push(`--label-list-visibility=${labelListVisibility}`);
    if (messageListVisibility) args.push(`--message-list-visibility=${messageListVisibility}`);
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_gmail_vacation_get', {
    description: 'Get the current vacation responder (auto-reply) settings.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      account: accountParam,
    }),
  }, async ({ account }) => {
    return runOrDiagnose(['gmail', 'settings', 'vacation', 'get'], { account });
  });

  server.registerTool('gog_gmail_vacation_update', {
    description: 'Update the vacation responder. Pass enable (with subject/body) to turn it on, or disable to turn it off; optional start/end RFC3339 times and contactsOnly/domainOnly scoping. '
      + 'An enabled responder auto-replies to every sender in scope, so enable asks the MCP host to show the user a '
      + 'confirmation prompt with the subject, the text, the window and who gets it first; disabling does not ask.'
      + CONFIRM_FALLBACK_DESCRIPTION,
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      enable: z.boolean().optional().describe('Enable the vacation responder (asks the user first)'),
      disable: z.boolean().optional().describe('Disable the vacation responder'),
      subject: z.string().optional().describe('Subject line for the auto-reply'),
      body: z.string().optional().describe('HTML body of the auto-reply message'),
      start: z.string().optional().describe('Start time in RFC3339 format (e.g. 2024-12-20T00:00:00Z)'),
      end: z.string().optional().describe('End time in RFC3339 format (e.g. 2024-12-31T23:59:59Z)'),
      contactsOnly: z.boolean().optional().describe('Only respond to contacts'),
      domainOnly: z.boolean().optional().describe('Only respond to senders in the same domain'),
      account: accountParam,
      confirmToken: confirmTokenParam,
    }),
  }, async ({ enable, disable, subject, body, start, end, contactsOnly, domainOnly, account, confirmToken }, ctx) => {
    const args: GogArg[] = ['gmail', 'settings', 'vacation', 'update'];
    if (enable) args.push('--enable');
    if (disable) args.push('--disable');
    if (subject) args.push(`--subject=${subject}`);
    // `gmail settings vacation update` exposes only --body — there is no
    // --body-file variant (verified against gog 0.34.1), so this stays inline.
    if (body) args.push(`--body=${body}`);
    if (start) args.push(`--start=${start}`);
    if (end) args.push(`--end=${end}`);
    if (contactsOnly) args.push('--contacts-only');
    if (domainOnly) args.push('--domain-only');
    if (enable) {
      const responder = {
        from: senderPreview(account),
        subject,
        start,
        end,
        repliesTo: contactsOnly ? 'your contacts' : domainOnly ? 'senders in your domain' : 'every sender',
      };
      const confirmation = await requireDispatchConfirmation(ctx, {
        action: 'gmail.vacation-enable',
        message: 'Review and confirm turning on this auto-reply:',
        confirmationLabel: 'Confirm that this auto-reply should be switched on now.',
        details: { ...responder, bodyPreview: bodyPreview(body) },
        unsupportedNote: 'Ask the user to turn on the vacation responder from Gmail settings.',
        fallback: {
          args: { enable, disable, subject, body, start, end, contactsOnly, domainOnly, account },
          tool: 'gog_gmail_vacation_update',
          account,
          confirmToken,
          subject: () => {
            const view = { ...responder, body };
            return { target: responder.from, payload: view, preview: view };
          },
        },
      });
      if (confirmation) return confirmation;
    }
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_gmail_filters_list', {
    description: 'List all Gmail filters for the account.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      account: accountParam,
    }),
  }, async ({ account }) => {
    return runOrDiagnose(['gmail', 'settings', 'filters', 'list'], { account });
  });

  server.registerTool('gog_gmail_filters_get', {
    description: 'Get the criteria and actions of a single Gmail filter by ID.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      filterId: z.string().describe('Filter ID'),
      account: accountParam,
    }),
  }, async ({ filterId, account }) => {
    return runOrDiagnose(['gmail', 'settings', 'filters', 'get', pos(filterId)], { account });
  });

  server.registerTool('gog_gmail_filters_create', {
    description: 'Create a Gmail filter. Specify match criteria (from/to/subject/query/hasAttachment) and one or more actions (label, archive, mark-read, star, important, trash, forward, never-spam). A filter with forward asks the MCP host to show a confirmation prompt first, since it sends every future matching message to that address.',
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      from: z.string().optional().describe('Match messages from this sender'),
      to: z.string().optional().describe('Match messages to this recipient'),
      subject: z.string().optional().describe('Match messages with this subject'),
      query: z.string().optional().describe('Advanced Gmail search query for matching'),
      hasAttachment: z.boolean().optional().describe('Match messages with attachments'),
      addLabel: z.string().optional().describe('Label(s) to add to matching messages (comma-separated, name or ID)'),
      removeLabel: z.string().optional().describe('Label(s) to remove from matching messages (comma-separated, name or ID)'),
      archive: z.boolean().optional().describe('Archive matching messages (skip inbox)'),
      markRead: z.boolean().optional().describe('Mark matching messages as read'),
      star: z.boolean().optional().describe('Star matching messages'),
      important: z.boolean().optional().describe('Mark as important'),
      trash: z.boolean().optional().describe('Move matching messages to trash'),
      neverSpam: z.boolean().optional().describe('Never mark as spam'),
      forward: z.string().optional().describe('Forward to this email address (must be a verified forwarding address)'),
      account: accountParam,
    }),
  }, async ({ from, to, subject, query, hasAttachment, addLabel, removeLabel, archive, markRead, star, important, trash, neverSpam, forward, account }, ctx) => {
    // A forward action routes every FUTURE matching message to another
    // address — persistent exfiltration if a prompt-injected agent sets it up —
    // so it needs the user's confirmation like any other send (audit SEC-2).
    if (forward) {
      const criteria = Object.fromEntries(
        Object.entries({ from, to, subject, query, hasAttachment }).filter(([, v]) => v !== undefined),
      );
      const confirmation = await requireGmailDispatchConfirmation(ctx, 'gmail.filter-forward', {
        forwardTo: forward,
        criteria,
        alsoArchive: Boolean(archive),
        alsoTrash: Boolean(trash),
        alsoMarkRead: Boolean(markRead),
      });
      if (confirmation) return confirmation;
    }
    const args: GogArg[] = ['gmail', 'settings', 'filters', 'create'];
    if (from) args.push(`--from=${from}`);
    if (to) args.push(`--to=${to}`);
    if (subject) args.push(`--subject=${subject}`);
    if (query) args.push(`--query=${query}`);
    if (hasAttachment) args.push('--has-attachment');
    if (addLabel) args.push(`--add-label=${addLabel}`);
    if (removeLabel) args.push(`--remove-label=${removeLabel}`);
    if (archive) args.push('--archive');
    if (markRead) args.push('--mark-read');
    if (star) args.push('--star');
    if (important) args.push('--important');
    if (trash) args.push('--trash');
    if (neverSpam) args.push('--never-spam');
    if (forward) args.push(`--forward=${forward}`, '--force'); // gog gates this op; without --force the runner's --no-input makes it refuse (forwarding filters only)
    const result = await runOrDiagnose(args, { account });
    if (forward && !result.isError) logGmailDispatch('gog_gmail_filters_create', extractEmails(forward), account);
    return result;
  });

  server.registerTool('gog_gmail_filters_delete', {
    description: 'Delete a Gmail filter by ID.',
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      filterId: z.string().describe('Filter ID to delete'),
      account: accountParam,
    }),
  }, async ({ filterId, account }) => {
    return runOrDiagnose(['gmail', 'settings', 'filters', 'delete', pos(filterId), '--force'], { account }); // gog gates this op; without --force the runner's --no-input makes it refuse
  });

  server.registerTool('gog_gmail_sendas_list', {
    description: 'List all send-as aliases configured for the account.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      account: accountParam,
    }),
  }, async ({ account }) => {
    return runOrDiagnose(['gmail', 'settings', 'sendas', 'list'], { account });
  });

  server.registerTool('gog_gmail_sendas_get', {
    description: 'Get details of a single send-as alias by its email address.',
    annotations: { readOnlyHint: true, openWorldHint: true },
    inputSchema: z.object({
      email: z.string().describe('Send-as alias email address'),
      account: accountParam,
    }),
  }, async ({ email, account }) => {
    return runOrDiagnose(['gmail', 'settings', 'sendas', 'get', pos(email)], { account });
  });

  server.registerTool('gog_gmail_sendas_create', {
    description: 'Create a send-as alias. Newly added aliases generally require email verification before they can be used (see gog_gmail_sendas_verify). '
      + 'Google emails the address and the account gains a new identity to send as, so this asks the MCP host to show '
      + 'the user a confirmation prompt with the address, name and reply-to first; nothing is created unless they accept.'
      + CONFIRM_FALLBACK_DESCRIPTION,
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      email: z.string().describe('Email address of the new send-as alias'),
      displayName: z.string().optional().describe('Name that appears in the From field'),
      replyTo: z.string().optional().describe('Reply-to address'),
      signature: z.string().optional().describe('HTML signature for emails sent from this alias'),
      treatAsAlias: z.boolean().optional().describe('Treat as alias (replies sent from Gmail web)'),
      account: accountParam,
      confirmToken: confirmTokenParam,
    }),
  }, async ({ email, displayName, replyTo, signature, treatAsAlias, account, confirmToken }, ctx) => {
    const args: GogArg[] = ['gmail', 'settings', 'sendas', 'create', pos(email)];
    if (displayName) args.push(`--display-name=${displayName}`);
    if (replyTo) args.push(`--reply-to=${replyTo}`);
    if (signature) args.push(`--signature=${signature}`);
    if (treatAsAlias) args.push('--treat-as-alias');
    const alias = { account: senderPreview(account), email, displayName, replyTo, treatAsAlias: Boolean(treatAsAlias) };
    const confirmation = await requireDispatchConfirmation(ctx, {
      action: 'gmail.sendas-create',
      message: 'Review and confirm adding this send-as address — Google emails it a verification request:',
      confirmationLabel: 'Confirm that this address should be added as a sending identity now.',
      details: { ...alias, signaturePreview: bodyPreview(signature) },
      unsupportedNote: 'Ask the user to add it from Gmail settings (Accounts > Send mail as).',
      fallback: {
        // treatAsAlias as the call means it: an omitted flag and false are the same alias.
        args: { email, displayName, replyTo, signature, treatAsAlias: Boolean(treatAsAlias), account },
        tool: 'gog_gmail_sendas_create',
        account,
        confirmToken,
        subject: () => {
          const view = { ...alias, signature };
          return { target: email, payload: view, preview: view };
        },
      },
    });
    if (confirmation) return confirmation;
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_gmail_sendas_update', {
    description: 'Update a send-as alias (display name, reply-to, signature, alias handling, or make it the default).',
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      email: z.string().describe('Send-as alias email address to update'),
      displayName: z.string().optional().describe('Name that appears in the From field'),
      replyTo: z.string().optional().describe('Reply-to address'),
      signature: z.string().optional().describe('HTML signature'),
      treatAsAlias: z.boolean().optional().describe('Treat as alias'),
      makeDefault: z.boolean().optional().describe('Make this the default send-as address'),
      account: accountParam,
    }),
  }, async ({ email, displayName, replyTo, signature, treatAsAlias, makeDefault, account }) => {
    const args: GogArg[] = ['gmail', 'settings', 'sendas', 'update', pos(email)];
    if (displayName) args.push(`--display-name=${displayName}`);
    if (replyTo) args.push(`--reply-to=${replyTo}`);
    if (signature) args.push(`--signature=${signature}`);
    if (treatAsAlias) args.push('--treat-as-alias');
    if (makeDefault) args.push('--make-default');
    return runOrDiagnose(args, { account });
  });

  server.registerTool('gog_gmail_sendas_delete', {
    description: 'Delete a send-as alias by its email address.',
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      email: z.string().describe('Send-as alias email address to delete'),
      account: accountParam,
    }),
  }, async ({ email, account }) => {
    return runOrDiagnose(['gmail', 'settings', 'sendas', 'delete', pos(email), '--force'], { account }); // gog gates this op; without --force the runner's --no-input makes it refuse
  });

  server.registerTool('gog_gmail_sendas_verify', {
    description: 'Resend the verification email for a send-as alias that is pending verification.',
    annotations: { destructiveHint: true, openWorldHint: true },
    inputSchema: z.object({
      email: z.string().describe('Send-as alias email address to verify'),
      account: accountParam,
    }),
  }, async ({ email, account }) => {
    return runOrDiagnose(['gmail', 'settings', 'sendas', 'verify', pos(email)], { account });
  });
}
