#!/usr/bin/env node

import { createHash } from "node:crypto";
import { constants, lstatSync, openSync, readFileSync, closeSync, writeFileSync } from "node:fs";
import { isAbsolute } from "node:path";
import { isDeepStrictEqual } from "node:util";
import { fileURLToPath } from "node:url";

const uuid = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const maxUploadBytes = 4 * 1024 * 1024;

function fail(message) { throw new Error(message); }
function hash(value) { return createHash("sha256").update(value).digest("hex"); }
function readPrivateFile(path) {
  if (!isAbsolute(path)) fail("Use an absolute file path.");
  const info = lstatSync(path);
  if (!info.isFile() || info.isSymbolicLink()) fail("Input must be a regular file, not a symlink.");
  const descriptor = openSync(path, constants.O_RDONLY | constants.O_NOFOLLOW);
  try { return readFileSync(descriptor); } finally { closeSync(descriptor); }
}
function jsonFile(path) {
  try { return JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(readPrivateFile(path))); }
  catch { fail("Input JSON file is invalid UTF-8 or JSON."); }
}
function report(value) { process.stdout.write(`${JSON.stringify(value)}\n`); }

function pageParts(htmlPath, manifestPath) {
  let html;
  try { html = new TextDecoder("utf-8", { fatal: true }).decode(readPrivateFile(htmlPath)); }
  catch { fail("HTML file is invalid UTF-8."); }
  if (!/^\s*<!doctype html>/i.test(html) || !/<\/html\s*>\s*$/i.test(html))
    fail("Page source must be a complete HTML document.");
  const manifest = jsonFile(manifestPath);
  if (manifest?.protocolVersion !== 1 || manifest?.kind !== "page" || !manifest?.data ||
      !["local", "controlled-cloud"].includes(manifest.data.mode))
    fail("Manifest must be a Page protocol v1 manifest with an explicit data mode.");
  if (manifest.data.mode === "controlled-cloud" && !/\bid\s*=\s*["']onimi-artifact["']/i.test(html))
    fail("Controlled-cloud Page requires its embedded artifact manifest.");
  const source = { kind: "page", html };
  return { source, manifest };
}

function slidesParts(authorPath) {
  const author = jsonFile(authorPath);
  if (author?.kind !== "slides" || author?.document?.format !== "bento/slides" ||
      !Array.isArray(author.document.slides) || author.document.slides.length === 0 ||
      author?.manifest?.protocolVersion !== 1 || author.manifest.kind !== "slides" ||
      !["local", "controlled-cloud"].includes(author.manifest?.data?.mode))
    fail("Slides author file needs a complete document and protocol v1 manifest; run validate-slides first.");
  return { source: { kind: "slides", document: author.document }, manifest: author.manifest };
}

function completeUploadPayload(payload) {
  if (!payload || typeof payload !== "object" || Array.isArray(payload) ||
      Object.keys(payload).sort().join(",") !== "manifest,source" ||
      payload?.manifest?.protocolVersion !== 1 ||
      payload.source?.kind !== payload.manifest.kind ||
      !["local", "controlled-cloud"].includes(payload.manifest?.data?.mode)) return false;
  if (payload.source.kind === "page")
    return Object.keys(payload.source).sort().join(",") === "html,kind" &&
      typeof payload.source.html === "string" && /^\s*<!doctype html>/i.test(payload.source.html) &&
      /<\/html\s*>\s*$/i.test(payload.source.html);
  return payload.source.kind === "slides" &&
    Object.keys(payload.source).sort().join(",") === "document,kind" &&
    payload.source.document?.format === "bento/slides" &&
    Array.isArray(payload.source.document.slides) && payload.source.document.slides.length > 0;
}

function writePayload(outputPath, payload, inline = false) {
  const bytes = Buffer.from(JSON.stringify(payload), "utf8");
  if (!isAbsolute(outputPath)) fail("Output must use an absolute file path.");
  const descriptor = openSync(outputPath, constants.O_WRONLY | constants.O_CREAT | constants.O_EXCL | constants.O_NOFOLLOW, 0o600);
  try { writeFileSync(descriptor, bytes); } finally { closeSync(descriptor); }
  report({ outputPath, sourceKind: payload.source.kind,
    ...(payload.source.kind === "page" ? { htmlBytes: Buffer.byteLength(payload.source.html) } :
      { slideCount: payload.source.document.slides.length }),
    sourceSha256: hash(JSON.stringify(payload.source)), manifestSha256: hash(JSON.stringify(payload.manifest)),
    bytes: bytes.length, sha256: hash(bytes), ...(inline ? { requestSha256: hash(bytes) } : {}) });
}

function preparePage([htmlPath, manifestPath, projectId, revisionText, idempotencyKey, outputPath]) {
  if (!htmlPath || !manifestPath || !projectId || revisionText === undefined || !idempotencyKey || !outputPath)
    fail("Usage: draft-payload.mjs prepare-page <absolute-html> <absolute-manifest-json> <project-uuid> <expected-revision> <mutation-uuid> <absolute-output-json>");
  if (!uuid.test(projectId) || !uuid.test(idempotencyKey)) fail("Project and mutation IDs must be UUIDs.");
  const expectedRevision = Number(revisionText);
  if (!/^(0|[1-9][0-9]*)$/.test(revisionText) || !Number.isSafeInteger(expectedRevision))
    fail("Expected revision must be a nonnegative integer.");
  const { source, manifest } = pageParts(htmlPath, manifestPath);
  const request = { projectId, expectedRevision, idempotencyKey, source, manifest };
  writePayload(outputPath, request, true);
}

function prepareUploadPage([htmlPath, manifestPath, outputPath]) {
  if (!htmlPath || !manifestPath || !outputPath)
    fail("Usage: draft-payload.mjs prepare-upload-page <absolute-html> <absolute-manifest-json> <absolute-output-json>");
  const payload = pageParts(htmlPath, manifestPath);
  if (Buffer.byteLength(JSON.stringify(payload)) > maxUploadBytes)
    fail("Upload body exceeds the 4 MiB staged-draft limit.");
  writePayload(outputPath, payload);
}

function prepareUploadSlides([authorPath, outputPath]) {
  if (!authorPath || !outputPath)
    fail("Usage: draft-payload.mjs prepare-upload-slides <absolute-author-json> <absolute-output-json>");
  const payload = slidesParts(authorPath);
  if (Buffer.byteLength(JSON.stringify(payload)) > maxUploadBytes)
    fail("Upload body exceeds the 4 MiB staged-draft limit.");
  writePayload(outputPath, payload);
}

function prepareBegin([payloadPath, projectId, revisionText, idempotencyKey, outputPath]) {
  if (!payloadPath || !projectId || revisionText === undefined || !idempotencyKey || !outputPath)
    fail("Usage: draft-payload.mjs prepare-begin <absolute-payload-json> <project-uuid> <expected-revision> <mutation-uuid> <absolute-output-json>");
  if (!uuid.test(projectId) || !uuid.test(idempotencyKey) || !/^(0|[1-9][0-9]*)$/.test(revisionText))
    fail("Begin request needs exact UUIDs and nonnegative revision.");
  const expectedRevision = Number(revisionText);
  if (!Number.isSafeInteger(expectedRevision)) fail("Expected revision is too large.");
  const body = readPrivateFile(payloadPath);
  if (body.length > maxUploadBytes) fail("Upload body exceeds the 4 MiB staged-draft limit.");
  let payload;
  try { payload = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(body)); }
  catch { fail("Upload body is invalid UTF-8 or JSON."); }
  if (!completeUploadPayload(payload))
    fail("Upload body must contain a complete Page or Slides source and manifest.");
  const begin = { projectId, expectedRevision, idempotencyKey, sha256: hash(body), bytes: body.length };
  if (!isAbsolute(outputPath)) fail("Output must use an absolute file path.");
  const serialized = JSON.stringify(begin);
  const descriptor = openSync(outputPath, constants.O_WRONLY | constants.O_CREAT | constants.O_EXCL | constants.O_NOFOLLOW, 0o600);
  try { writeFileSync(descriptor, serialized); } finally { closeSync(descriptor); }
  report({ outputPath, requestSha256: hash(serialized), sha256: begin.sha256, bytes: begin.bytes });
}

export async function sendUpload([payloadPath, beginRequestPath, beginResponsePath, resourceUrl, receiptPath], transport = fetch) {
  if (!payloadPath || !beginRequestPath || !beginResponsePath || !resourceUrl || !receiptPath)
    fail("Usage: draft-payload.mjs send-upload <absolute-payload-json> <absolute-begin-request-json> <absolute-begin-response-json> <confirmed-mcp-resource-url> <absolute-receipt-json>");
  const bytes = readPrivateFile(payloadPath);
  if (bytes.length > maxUploadBytes) fail("Upload body exceeds the 4 MiB staged-draft limit.");
  const beginRequest = jsonFile(beginRequestPath);
  if (bytes.length !== beginRequest.bytes || hash(bytes) !== beginRequest.sha256)
    fail("Upload body changed after preparation; start a new save plan.");
  const payload = jsonFile(payloadPath);
  if (!completeUploadPayload(payload))
    fail("Upload body is not a complete Page or Slides source and manifest.");
  const responseFile = jsonFile(beginResponsePath);
  const begin = responseFile?.structuredContent ?? responseFile;
  let url, resource;
  try { url = new URL(begin?.uploadUrl ?? ""); resource = new URL(resourceUrl); }
  catch { fail("Upload URL or confirmed MCP resource URL is invalid."); }
  if (resource.protocol !== "https:" || resource.pathname !== "/mcp" || resource.username ||
      resource.password || resource.search || resource.hash ||
      url.origin !== resource.origin || url.protocol !== "https:" || url.username || url.password || url.search || url.hash ||
      url.pathname !== "/api/v1/onimi/draft-uploads" ||
      begin?.method !== "PUT" || begin?.contentType !== "application/json" ||
      typeof begin?.uploadToken !== "string" || !/^[A-Za-z0-9._~-]{20,2048}$/.test(begin.uploadToken) ||
      !Number.isFinite(Date.parse(begin?.expiresAt)) || Date.parse(begin.expiresAt) <= Date.now())
    fail("Begin-upload response is invalid or expired.");
  let upload;
  try {
    upload = await transport(url, {
      method: "PUT", redirect: "error", signal: AbortSignal.timeout(30_000),
      headers: { "Content-Type": "application/json", Authorization: `OnimiUpload ${begin.uploadToken}` },
      body: bytes,
    });
  } catch {
    fail("Upload outcome is uncertain; read the current draft before retrying the same request.");
  }
  if (!upload.ok) fail(`Upload returned HTTP ${upload.status}; read the current draft before retrying.`);
  let receipt;
  try { receipt = await upload.json(); } catch { fail("Upload response is unreadable; read the current draft before retrying."); }
  const sourceSha256 = hash(JSON.stringify(payload.source));
  if (!uuid.test(receipt?.revisionId ?? "") || receipt?.revision !== beginRequest.expectedRevision + 1 ||
      !/^[0-9a-f]{64}$/.test(receipt?.sourceSha256 ?? "") ||
      (payload.source.kind === "page" && receipt.sourceSha256 !== sourceSha256))
    fail("Upload receipt is incomplete; read the current draft before retrying.");
  if (!isAbsolute(receiptPath)) fail("Receipt must use an absolute file path.");
  const descriptor = openSync(receiptPath, constants.O_WRONLY | constants.O_CREAT | constants.O_EXCL | constants.O_NOFOLLOW, 0o600);
  try { writeFileSync(descriptor, JSON.stringify(receipt)); } finally { closeSync(descriptor); }
  report({ revisionId: receipt.revisionId, revision: receipt.revision, sourceSha256: receipt.sourceSha256,
    sourceReadbackRequired: payload.source.kind === "slides" || receipt.sourceSha256 !== sourceSha256 });
}

function verifyPage([requestPath, readbackPath, uploadProjectId, uploadRevision]) {
  if (!requestPath || !readbackPath)
    fail("Usage: draft-payload.mjs verify-page <absolute-request-json> <absolute-get-draft-json> [<upload-project-uuid> <expected-revision>]");
  const request = jsonFile(requestPath);
  const upload = uploadProjectId !== undefined || uploadRevision !== undefined;
  const projectId = upload ? uploadProjectId : request.projectId;
  const expectedRevision = upload ? Number(uploadRevision) : request.expectedRevision;
  if (upload && (!uuid.test(projectId ?? "") || !/^(0|[1-9][0-9]*)$/.test(uploadRevision ?? "") ||
      !Number.isSafeInteger(expectedRevision))) fail("Upload verification needs an exact project UUID and revision.");
  const response = jsonFile(readbackPath);
  const readback = response?.structuredContent ?? response;
  if (request?.source?.kind !== "page" || typeof request.source.html !== "string" ||
      !request?.manifest || request.manifest.kind !== "page")
    fail("Request file is not a complete Page save request.");
  const expectedSourceSha256 = hash(JSON.stringify(request.source));
  if (readback?.projectId !== projectId || readback?.revision !== expectedRevision + 1 ||
      !uuid.test(readback?.revisionId ?? "") || readback?.sourceSha256 !== expectedSourceSha256 ||
      !isDeepStrictEqual(readback?.source, request.source) ||
      !isDeepStrictEqual(readback?.manifest, request.manifest))
    fail("Saved draft does not match the exact local request; do not finish the journal or publish.");
  report({ projectId: readback.projectId, revisionId: readback.revisionId,
    revision: readback.revision, sourceSha256: expectedSourceSha256 });
}

function verifyHistory([payloadPath, beginRequestPath, receiptPath, historyPath]) {
  if (!payloadPath || !beginRequestPath || !receiptPath || !historyPath)
    fail("Usage: draft-payload.mjs verify-history <absolute-payload-json> <absolute-begin-request-json> <absolute-upload-receipt-json> <absolute-list-revisions-json>");
  const body = readPrivateFile(payloadPath);
  const payload = jsonFile(payloadPath);
  const begin = jsonFile(beginRequestPath);
  const receipt = jsonFile(receiptPath);
  const historyFile = jsonFile(historyPath);
  const history = historyFile?.structuredContent ?? historyFile;
  const revision = history?.revisions?.find((item) => item.revisionId === receipt?.revisionId);
  if (payload?.source?.kind !== "page" || typeof payload.source.html !== "string" ||
      payload?.manifest?.kind !== "page") fail("Upload body is not a complete Page source and manifest.");
  const expectedSourceSha256 = hash(JSON.stringify(payload?.source));
  if (!uuid.test(begin?.projectId ?? "") || !uuid.test(begin?.idempotencyKey ?? "") ||
      !uuid.test(receipt?.revisionId ?? "") || body.length > maxUploadBytes ||
      begin?.sha256 !== hash(body) || begin?.bytes !== body.length ||
      receipt?.revision !== begin.expectedRevision + 1 || receipt?.sourceSha256 !== expectedSourceSha256 ||
      revision?.revision !== receipt.revision || revision?.sourceSha256 !== expectedSourceSha256 ||
      !isDeepStrictEqual(revision?.manifest, payload.manifest))
    fail("Revision history does not match the exact local upload; do not finish the journal or publish.");
  report({ projectId: begin.projectId, revisionId: receipt.revisionId,
    revision: receipt.revision, sourceSha256: expectedSourceSha256 });
}

async function main() {
  const [command, ...arguments_] = process.argv.slice(2);
  if (command === "prepare-page") preparePage(arguments_);
  else if (command === "prepare-upload-page") prepareUploadPage(arguments_);
  else if (command === "prepare-upload-slides") prepareUploadSlides(arguments_);
  else if (command === "prepare-begin") prepareBegin(arguments_);
  else if (command === "send-upload") await sendUpload(arguments_);
  else if (command === "verify-page") verifyPage(arguments_);
  else if (command === "verify-history") verifyHistory(arguments_);
  else fail("Usage: draft-payload.mjs <prepare-page|prepare-upload-page|prepare-upload-slides|prepare-begin|send-upload|verify-page|verify-history> ...");
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main().catch((error) => {
    process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
    process.exitCode = 1;
  });
}
