#!/usr/bin/env node
import { createHash, randomUUID } from 'node:crypto';
import { open, readFile, mkdir, lstat, rename, unlink, link } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

export const API_BASE_URL = 'https://api.apisrouter.com/v1';
const VIDEO_SPECS = {
  'seedance-2.0-fast': { seconds: 4, resolution: '480p', ratio: '16:9' },
  'seedance-2.5': { seconds: 4, resolution: '480p', ratio: '16:9' },
  'seedance-2.0-mini': { seconds: 5, resolution: '720p', ratio: '9:16' },
};
const IMAGE_SIZES = ['1:1', '3:2', '2:3', '4:3', '3:4', '5:4', '4:5', '16:9', '9:16', '2:1', '1:2', '3:1', '1:3', '21:9', '9:21'];
const MAX_API_BYTES = 64 * 1024 * 1024;
const MAX_ASSET_BYTES = 256 * 1024 * 1024;
const STATES = ['unknown', 'processing', 'completed', 'failed', 'rejected'];
const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
const isObject = value => value !== null && typeof value === 'object' && !Array.isArray(value);

export class GenerationError extends Error {
  constructor(code, status) {
    super(code);
    this.name = 'GenerationError';
    this.code = code;
    if (Number.isInteger(status)) this.status = status;
  }
}
const fail = (code, status) => { throw new GenerationError(code, status); };
const protect = fn => async (...args) => {
  try { return await fn(...args); }
  catch (error) { throw error instanceof GenerationError ? error : new GenerationError('local_operation_failed'); }
};
function pathFor(value) {
  if (typeof value !== 'string' || !value || value.includes('\0')) fail('invalid_path');
  return resolve(value);
}
async function syncDirectory(path) {
  const handle = await open(path, 'r');
  try { await handle.sync(); } finally { await handle.close(); }
}
async function writePrivate(path, value, exclusive = false) {
  await mkdir(dirname(path), { recursive: true, mode: 0o700 });
  const destination = exclusive ? path : `${path}.${randomUUID()}.tmp`;
  let handle;
  try {
    handle = await open(destination, 'wx', 0o600);
    await handle.writeFile(`${JSON.stringify(value, null, 2)}\n`);
    await handle.sync();
    await handle.close();
    handle = undefined;
    if (!exclusive) await rename(destination, path);
    await syncDirectory(dirname(path));
  } catch (error) {
    if (handle) await handle.close().catch(() => {});
    if (!exclusive) await unlink(destination).catch(() => {});
    if (exclusive && error.code === 'EEXIST') fail('job_exists');
    // Keep an exclusive receipt even after a disk error: this path must never POST twice.
    fail('receipt_write_failed');
  }
}
async function readJson(path, maxBytes, code) {
  try {
    const info = await lstat(path);
    if (!info.isFile() || info.size > maxBytes) fail(code);
    return JSON.parse(await readFile(path, 'utf8'));
  } catch { fail(code); }
}
function validateRequest(request) {
  if (!isObject(request) || !['image', 'video'].includes(request.kind)) fail('invalid_request');
  const allowed = request.kind === 'video'
    ? ['kind', 'model', 'prompt', 'seconds', 'resolution', 'ratio']
    : ['kind', 'model', 'prompt', 'resolution', 'size', 'images'];
  if (Object.keys(request).some(key => !allowed.includes(key))) fail('invalid_request');
  if (typeof request.prompt !== 'string' || !request.prompt.trim() || Buffer.byteLength(request.prompt) > 32000) fail('invalid_request');
  if (request.kind === 'video') {
    const spec = Object.hasOwn(VIDEO_SPECS, request.model) ? VIDEO_SPECS[request.model] : undefined;
    if (!spec || Object.entries(spec).some(([key, value]) => request[key] !== value)) fail('invalid_request');
  } else {
    if (request.model !== 'gpt-image-2' || !['1k', '2k', '4k'].includes(request.resolution) || !IMAGE_SIZES.includes(request.size)) fail('invalid_request');
    if (Object.hasOwn(request, 'images') && (!Array.isArray(request.images) || request.images.length < 1 || request.images.length > 8 || request.images.some(file => typeof file !== 'string' || !file || file.includes('\0')))) fail('invalid_request');
  }
}
function imageType(bytes) {
  if (bytes.subarray(0, 8).equals(Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]))) return { mime: 'image/png', extension: 'png' };
  if (bytes[0] === 255 && bytes[1] === 216 && bytes[2] === 255) return { mime: 'image/jpeg', extension: 'jpg' };
  if (bytes.toString('ascii', 0, 4) === 'RIFF' && bytes.toString('ascii', 8, 12) === 'WEBP') return { mime: 'image/webp', extension: 'webp' };
  fail('invalid_image');
}
async function prepareRequest(requestFile) {
  const request = await readJson(requestFile, 65536, 'invalid_request');
  validateRequest(request);
  const { kind, images, ...payload } = request;
  if (kind === 'image') payload.n = 1;
  const hash = createHash('sha256').update(JSON.stringify(request));
  let body = JSON.stringify(payload);
  let headers = { 'content-type': 'application/json' };
  let endpoint = kind === 'video' ? '/videos/generations' : '/images/generations';
  if (images) {
    body = new FormData();
    for (const [key, value] of Object.entries(payload)) body.append(key, String(value));
    for (const [index, path] of images.entries()) {
      const file = resolve(dirname(requestFile), path);
      const info = await lstat(file).catch(() => fail('invalid_image'));
      if (!info.isFile() || info.size > 20 * 1024 * 1024) fail('invalid_image');
      const bytes = await readFile(file);
      const type = imageType(bytes);
      hash.update(sha256(bytes));
      body.append(images.length === 1 ? 'image' : 'image[]', new Blob([bytes], { type: type.mime }), `input-${index + 1}.${type.extension}`);
    }
    headers = {};
    endpoint = '/images/edits';
  }
  return { request, body, headers, endpoint, requestHash: hash.digest('hex') };
}
async function boundedBody(response, maxBytes) {
  const chunks = [];
  let size = 0;
  for await (const chunk of response.body) {
    size += chunk.length;
    if (size > maxBytes) fail('response_too_large');
    chunks.push(chunk);
  }
  return Buffer.concat(chunks);
}
function loopback(url) { return ['127.0.0.1', '[::1]', 'localhost'].includes(url.hostname); }

// Only imported callers can inject a loopback test server. The CLI always uses API_BASE_URL.
export function createClient({ apiKey = process.env.APISROUTER_API_KEY, baseUrl = API_BASE_URL, timeoutMs = 180000, allowLoopbackDownloads = false } = {}) {
  let base;
  try { base = new URL(baseUrl); } catch { fail('invalid_api_origin'); }
  if (base.href.replace(/\/$/, '') !== API_BASE_URL && !(base.protocol === 'http:' && loopback(base) && base.pathname === '/v1')) fail('invalid_api_origin');
  if (base.username || base.password || base.search || base.hash) fail('invalid_api_origin');
  if (!Number.isInteger(timeoutMs) || timeoutMs < 1 || timeoutMs > 600000) fail('invalid_timeout');
  const endpointBase = base.href.replace(/\/$/, '');
  const safeText = value => typeof value === 'string' && (!apiKey || !value.includes(apiKey));
  const identity = value => safeText(value) && /^[A-Za-z0-9][A-Za-z0-9._-]{0,191}$/.test(value);
  function requireKey() {
    if (typeof apiKey !== 'string' || !apiKey.trim() || /[\r\n]/.test(apiKey)) fail('api_key_required');
  }
  function resultURL(value) {
    if (!safeText(value)) fail('invalid_result');
    let url;
    try { url = new URL(value); } catch { fail('invalid_result'); }
    if (url.username || url.password || url.hash || !(url.protocol === 'https:' || (allowLoopbackDownloads && url.protocol === 'http:' && loopback(url)))) fail('invalid_result');
    return url.href;
  }
  async function api(path, options = {}) {
    requireKey();
    let response;
    try {
      response = await fetch(`${endpointBase}${path}`, { ...options, headers: { ...options.headers, authorization: `Bearer ${apiKey}` }, redirect: 'manual', credentials: 'omit', signal: AbortSignal.timeout(timeoutMs) });
      if (!response.ok) { await response.body?.cancel(); fail('api_http_error', response.status); }
      const bytes = await boundedBody(response, MAX_API_BYTES);
      try { return JSON.parse(bytes.toString('utf8')); } catch { fail('invalid_api_response'); }
    } catch (error) {
      if (error instanceof GenerationError) throw error;
      fail('api_transport_error');
    }
  }
  function publicReceipt(receipt, jobFile) {
    return {
      job_file: jobFile, kind: receipt.kind, model: receipt.model, status: receipt.status,
      ...(receipt.task_id ? { task_id: receipt.task_id } : {}),
      request_sha256: receipt.request_sha256, has_result: Boolean(receipt.result),
      reconciliation_required: receipt.status === 'unknown' && !receipt.task_id,
    };
  }
  async function loadReceipt(jobFile) {
    const receipt = await readJson(jobFile, MAX_API_BYTES, 'invalid_receipt');
    const info = await lstat(jobFile);
    if ((info.mode & 0o077) !== 0) fail('receipt_permissions');
    if (!isObject(receipt) || receipt.version !== 1 || receipt.api_base_url !== endpointBase || !STATES.includes(receipt.status)
      || !['video', 'image'].includes(receipt.kind) || !/^[a-f0-9]{64}$/.test(receipt.request_sha256)
      || !(receipt.kind === 'video' ? Object.hasOwn(VIDEO_SPECS, receipt.model) : receipt.model === 'gpt-image-2')
      || (receipt.task_id !== undefined && !identity(receipt.task_id))) fail('invalid_receipt');
    return receipt;
  }
  function applyVideo(receipt, data) {
    if (!isObject(data) || !identity(data.task_id) || (receipt.task_id && data.task_id !== receipt.task_id)) fail('invalid_api_response');
    receipt.task_id = data.task_id;
    if (!['processing', 'completed', 'failed'].includes(data.status)) fail('invalid_api_response');
    if (data.status === 'completed') receipt.result = { url: resultURL(data.result?.url) };
    receipt.status = data.status;
    if (data.status === 'failed') receipt.error_code = 'generation_failed';
  }
  function applyImage(receipt, data) {
    if (!isObject(data) || !Array.isArray(data.data) || data.data.length !== 1 || !isObject(data.data[0])) fail('invalid_api_response');
    const result = data.data[0];
    if (result.url) receipt.result = { url: resultURL(result.url) };
    else if (typeof result.b64_json === 'string' && /^[A-Za-z0-9+/]+={0,2}$/.test(result.b64_json) && result.b64_json.length % 4 === 0) {
      const bytes = Buffer.from(result.b64_json, 'base64');
      imageType(bytes);
      receipt.result = { b64_json: result.b64_json };
    } else fail('invalid_api_response');
    receipt.status = 'completed';
  }
  return {
    baseUrl: endpointBase,
    models: protect(async () => {
      const data = await api('/models');
      if (!isObject(data) || !Array.isArray(data.data)) fail('invalid_api_response');
      const ids = data.data.map(item => item?.id);
      if (ids.some(id => !safeText(id) || !/^[A-Za-z0-9][A-Za-z0-9._:/-]{0,191}$/.test(id))) fail('invalid_api_response');
      return { models: [...new Set(ids)] };
    }),
    submit: protect(async ({ requestFile, jobFile, confirmCost } = {}) => {
      if (confirmCost !== true) fail('cost_confirmation_required');
      requireKey();
      const requestPath = pathFor(requestFile);
      const jobPath = pathFor(jobFile);
      const prepared = await prepareRequest(requestPath);
      const receipt = {
        version: 1, api_base_url: endpointBase, kind: prepared.request.kind, model: prepared.request.model,
        request_sha256: prepared.requestHash, status: 'unknown', created_at: new Date().toISOString(),
        requested: prepared.request.kind === 'video' ? VIDEO_SPECS[prepared.request.model] : { resolution: prepared.request.resolution, size: prepared.request.size },
      };
      await writePrivate(jobPath, receipt, true);
      try {
        const data = await api(prepared.endpoint, { method: 'POST', headers: prepared.headers, body: prepared.body });
        if (receipt.kind === 'video') applyVideo(receipt, data); else applyImage(receipt, data);
      } catch (error) {
        const rejected = error.code === 'api_http_error' && error.status >= 400 && error.status < 500 && error.status !== 408;
        receipt.status = rejected ? 'rejected' : 'unknown';
        receipt.error_code = rejected ? 'submission_rejected' : 'submission_unknown';
        if (error.status) receipt.http_status = error.status;
        await writePrivate(jobPath, receipt);
        fail(receipt.error_code, error.status);
      }
      await writePrivate(jobPath, receipt);
      return publicReceipt(receipt, jobPath);
    }),
    poll: protect(async ({ jobFile } = {}) => {
      const jobPath = pathFor(jobFile);
      const receipt = await loadReceipt(jobPath);
      if (receipt.kind === 'video' && receipt.task_id) {
        const data = await api(`/videos/tasks/${encodeURIComponent(receipt.task_id)}`);
        applyVideo(receipt, data);
        receipt.updated_at = new Date().toISOString();
        await writePrivate(jobPath, receipt);
      }
      return publicReceipt(receipt, jobPath);
    }),
    collect: protect(async ({ jobFile, outputFile } = {}) => {
      const jobPath = pathFor(jobFile);
      const outputPath = pathFor(outputFile);
      const receipt = await loadReceipt(jobPath);
      if (receipt.status !== 'completed' || !isObject(receipt.result)) fail('job_not_ready');
      try { await lstat(outputPath); fail('output_exists'); } catch (error) { if (error.code !== 'ENOENT') throw error; }
      await mkdir(dirname(outputPath), { recursive: true, mode: 0o700 });
      const temporary = `${outputPath}.${randomUUID()}.partial`;
      let handle;
      let bytes = 0;
      const hash = createHash('sha256');
      try {
        handle = await open(temporary, 'wx', 0o600);
        let source;
        if (receipt.result.url) {
          const url = resultURL(receipt.result.url);
          const response = await fetch(url, { headers: { accept: '*/*' }, redirect: 'manual', credentials: 'omit', signal: AbortSignal.timeout(timeoutMs) });
          if (!response.ok) { await response.body?.cancel(); fail('download_failed'); }
          source = response.body;
        } else if (typeof receipt.result.b64_json === 'string') source = [Buffer.from(receipt.result.b64_json, 'base64')];
        else fail('invalid_result');
        for await (const chunk of source) {
          bytes += chunk.length;
          if (bytes > MAX_ASSET_BYTES) fail('download_failed');
          hash.update(chunk);
          await handle.writeFile(chunk);
        }
        if (!bytes) fail('download_failed');
        await handle.sync();
        await handle.close();
        handle = undefined;
        // A hard link publishes atomically and fails if any file already occupies the output path.
        await link(temporary, outputPath);
        await syncDirectory(dirname(outputPath));
      } catch (error) {
        if (error.code === 'EEXIST') fail('output_exists');
        fail('download_failed');
      } finally {
        if (handle) await handle.close().catch(() => {});
        await unlink(temporary).catch(() => {});
      }
      return { ...publicReceipt(receipt, jobPath), output: { file: outputPath, bytes, sha256: hash.digest('hex') } };
    }),
  };
}

export async function main(argv = process.argv.slice(2)) {
  const [command, ...args] = argv;
  const accepted = { models: [], submit: ['--request', '--job', '--confirm-cost'], poll: ['--job'], collect: ['--job', '--output'] };
  if (!Object.hasOwn(accepted, command)) fail('invalid_command');
  const values = {};
  for (let index = 0; index < args.length; index++) {
    const flag = args[index];
    if (!accepted[command].includes(flag) || Object.hasOwn(values, flag)) fail('invalid_arguments');
    if (flag === '--confirm-cost') values[flag] = true;
    else {
      const value = args[++index];
      if (!value || value.startsWith('--')) fail('invalid_arguments');
      values[flag] = value;
    }
  }
  for (const flag of accepted[command]) if (flag !== '--confirm-cost' && !values[flag]) fail('invalid_arguments');
  const client = createClient();
  if (command === 'models') return client.models();
  return client[command]({ requestFile: values['--request'], jobFile: values['--job'], outputFile: values['--output'], confirmCost: values['--confirm-cost'] });
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  main().then(result => process.stdout.write(`${JSON.stringify(result, null, 2)}\n`)).catch(error => {
    const safe = error instanceof GenerationError ? error : new GenerationError('local_operation_failed');
    process.stderr.write(`${JSON.stringify({ error: { code: safe.code, ...(safe.status ? { status: safe.status } : {}) } })}\n`);
    process.exitCode = 1;
  });
}
