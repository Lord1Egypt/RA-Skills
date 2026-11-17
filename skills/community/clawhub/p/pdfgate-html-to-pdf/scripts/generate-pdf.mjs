#!/usr/bin/env node
/**
 * PDFGate HTML-to-PDF skill helper.
 * Node.js 18+, no npm dependencies.
 * Calls POST /v1/generate/pdf, streams the PDF to disk and prints a JSON summary.
 * The API key is read from PDFGATE_API_KEY and is never printed.
 */
import { createWriteStream } from 'node:fs';
import { readFile, open, rename, rm, mkdir, stat } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { randomUUID } from 'node:crypto';
import { pipeline } from 'node:stream/promises';
import { Readable } from 'node:stream';

const PRODUCTION_URL = 'https://api.pdfgate.com';
const SANDBOX_URL = 'https://api-sandbox.pdfgate.com';
const ENDPOINT = '/v1/generate/pdf';
const MAX_HTML_BYTES = 10 * 1024 * 1024;
const MAX_SERVER_TIMEOUT_MS = 900000; // PDFGate page-load timeout limit (15 minutes)
const PAGE_SIZES = ['a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'letter', 'legal', 'tabloid', 'ledger'];

const HELP = `PDFGate HTML-to-PDF generator

Usage:
  node generate-pdf.mjs --html-file invoice.html --output invoice.pdf [options]
  node generate-pdf.mjs --url https://example.com --output site.pdf [options]

Required:
  Exactly one of --html-file PATH (use - for stdin) or --url PUBLIC_URL
  --output PATH                     Where to save the resulting PDF (.pdf)
  PDFGATE_API_KEY                   Environment variable (test_ sandbox or live_ production key)

Layout options:
  --page-size SIZE                  a0..a6, letter, legal, tabloid, ledger (default a4)
  --orientation portrait|landscape  (default portrait)
  --margin CSS_LENGTH               Set all four page margins, e.g. 12mm
  --scale N                         Render scale 0.1..2 (default 1)
  --no-background                   Do not print CSS backgrounds
  --media screen|print              CSS media type (PDFGate defaults: screen for --url, print for HTML)
  --header-file PATH                HTML template for the page header (requires --margin)
  --footer-file PATH                HTML template for the page footer (requires --margin)
  --page-ranges RANGES              e.g. 1-3,5

Content options:
  --fillable                        Turn HTML inputs into interactive PDF form fields
  --wait-for-selector CSS           Wait until a CSS selector appears (max 30 s on the server)
  --wait-for-network-idle           Wait until the page has no open network connections
  --delay-ms N                      Wait N ms before rendering, 0..20000

Other:
  --timeout-seconds N               Request timeout, 15..960 (default 120)
  --overwrite                       Replace an existing output file
  --help                            Show this message
`;

const FLAGS = new Set(['--fillable', '--overwrite', '--wait-for-network-idle', '--no-background']);
const VALUES = new Set([
  '--html-file', '--url', '--output', '--page-size', '--orientation', '--media', '--margin',
  '--scale', '--header-file', '--footer-file', '--page-ranges', '--wait-for-selector',
  '--delay-ms', '--timeout-seconds',
]);

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const key = argv[i];
    if (key === '--help' || key === '-h') return { help: true };
    if (key in args) throw new Error(`Repeated option ${key}`);
    if (FLAGS.has(key)) { args[key] = true; continue; }
    if (!VALUES.has(key)) throw new Error(`Unknown option: ${key}`);
    const val = argv[++i];
    if (val === undefined || val === '' || val.startsWith('--')) {
      throw new Error(`Missing value for ${key}`);
    }
    args[key] = val;
  }
  return args;
}

function getBaseUrl(key) {
  if (key.startsWith('test_') && key.length > 5) return { url: SANDBOX_URL, environment: 'sandbox' };
  if (key.startsWith('live_') && key.length > 5) return { url: PRODUCTION_URL, environment: 'production' };
  throw new Error('PDFGATE_API_KEY must be a test_ (sandbox) or live_ (production) PDFGate API key.');
}

function publicUrl(s) {
  let u;
  try { u = new URL(s); } catch { throw new Error('--url must be a valid public http(s) URL.'); }
  if (u.protocol !== 'https:' && u.protocol !== 'http:') throw new Error('--url must use http or https.');
  if (u.username || u.password) throw new Error('Do not put credentials in a URL.');
  const host = u.hostname.toLowerCase().replace(/\.$/, '');
  const privateSuffix = ['.localhost', '.local', '.internal', '.test', '.invalid', '.example', '.home.arpa'];
  if (host === 'localhost' || privateSuffix.some((s) => host.endsWith(s))) {
    throw new Error('--url must refer to a public website, not a local or internal host.');
  }
  if (/^\d+\.\d+\.\d+\.\d+$/.test(host) || host.startsWith('[') || host.includes(':') || !host.includes('.')) {
    throw new Error('--url requires a public domain name, not an IP address or a bare hostname.');
  }
  return u.toString();
}

function parseNumber(name, raw, { min, max, integer }) {
  const n = Number(raw);
  if (!Number.isFinite(n) || (integer && !Number.isInteger(n)) || n < min || n > max) {
    throw new Error(`${name} must be ${integer ? 'an integer' : 'a number'} from ${min} to ${max}.`);
  }
  return n;
}

async function readTextFile(flag, file, { allowStdin = false } = {}) {
  if (allowStdin && file === '-') {
    const chunks = [];
    let size = 0;
    for await (const chunk of process.stdin) {
      size += chunk.length;
      if (size > MAX_HTML_BYTES) throw new Error(`${flag} input exceeds the 10 MiB safety limit.`);
      chunks.push(chunk);
    }
    return Buffer.concat(chunks).toString('utf8');
  }
  let info;
  try { info = await stat(file); } catch { throw new Error(`${flag}: cannot read ${file}`); }
  if (!info.isFile()) throw new Error(`${flag} must point to a regular file.`);
  if (info.size > MAX_HTML_BYTES) throw new Error(`${flag} input exceeds the 10 MiB safety limit.`);
  const text = await readFile(file, 'utf8');
  if (!text.trim()) throw new Error(`${flag}: the file is empty.`);
  return text;
}

async function assertNotExists(path, overwrite) {
  if (overwrite) return;
  let exists = false;
  try { await stat(path); exists = true; } catch (err) { if (err.code !== 'ENOENT') throw err; }
  if (exists) throw new Error(`Output already exists: ${path}. Use --overwrite to replace it.`);
}

function buildBody(args) {
  const size = (args['--page-size'] || 'a4').toLowerCase();
  if (!PAGE_SIZES.includes(size)) throw new Error(`--page-size must be one of: ${PAGE_SIZES.join(', ')}.`);
  const orientation = (args['--orientation'] || 'portrait').toLowerCase();
  if (!['portrait', 'landscape'].includes(orientation)) throw new Error('--orientation must be portrait or landscape.');
  const body = { pageSizeType: size, orientation, jsonResponse: false };

  const media = args['--media']?.toLowerCase();
  if (media !== undefined) {
    if (!['screen', 'print'].includes(media)) throw new Error('--media must be screen or print.');
    body.emulateMediaType = media;
  }
  const margin = args['--margin'];
  if (margin !== undefined) {
    if (!/^\d+(?:\.\d+)?(?:px|mm|cm|in|pt)$/.test(margin)) throw new Error('--margin must be a CSS length such as 12mm.');
    body.margin = { top: margin, bottom: margin, left: margin, right: margin };
  }
  if (args['--scale'] !== undefined) body.scale = parseNumber('--scale', args['--scale'], { min: 0.1, max: 2 });
  if (args['--no-background']) body.printBackground = false;
  const ranges = args['--page-ranges'];
  if (ranges !== undefined) {
    if (!/^\d+(?:-\d+)?(?:,\d+(?:-\d+)?)*$/.test(ranges)) throw new Error('--page-ranges must look like 1-3,5.');
    body.pageRanges = ranges;
  }
  if (args['--fillable']) body.enableFormFields = true;
  if (args['--wait-for-selector'] !== undefined) body.waitForSelector = args['--wait-for-selector'];
  if (args['--wait-for-network-idle']) body.waitForNetworkIdle = true;
  if (args['--delay-ms'] !== undefined) body.delay = parseNumber('--delay-ms', args['--delay-ms'], { min: 0, max: 20000, integer: true });
  if ((args['--header-file'] || args['--footer-file']) && !margin) {
    throw new Error('--header-file and --footer-file require --margin so the template has room on the page.');
  }
  return body;
}

async function requestPdf(baseUrl, key, body, signal) {
  let response;
  try {
    response = await fetch(`${baseUrl}${ENDPOINT}`, {
      method: 'POST',
      headers: { 'X-API-KEY': key, 'Content-Type': 'application/json', 'Accept': 'application/pdf' },
      body: JSON.stringify(body),
      signal,
    });
  } catch (err) {
    if (err?.name === 'TimeoutError' || err?.name === 'AbortError') {
      throw new Error(`PDFGate request timed out after ${signal.reason?.timeoutSeconds ?? '?'} seconds.`);
    }
    throw new Error(`Unable to reach the PDFGate API: ${err?.cause?.message || err.message}`);
  }
  if (!response.ok) {
    let detail = '';
    try {
      const data = JSON.parse(await response.text());
      const message = Array.isArray(data.message) ? data.message.join('; ') : data.message;
      if (typeof message === 'string') detail = message.slice(0, 300);
      else if (typeof data.error === 'string') detail = data.error.slice(0, 300);
    } catch { /* Non-JSON error bodies are not echoed. */ }
    const hint = response.status === 401 ? ' Check that PDFGATE_API_KEY is valid.' :
      response.status === 429 ? ' Too many concurrent requests; retry shortly.' : '';
    throw new Error(`PDFGate returned HTTP ${response.status}${detail ? `: ${detail}` : ''}.${hint}`);
  }
  if (!response.body) throw new Error('PDFGate returned an empty response.');
  return response;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) { process.stdout.write(HELP); return; }
  if (Boolean(args['--html-file']) === Boolean(args['--url'])) throw new Error('Provide exactly one of --html-file or --url.');
  if (!args['--output']) throw new Error('--output is required.');
  const key = process.env.PDFGATE_API_KEY;
  if (!key) throw new Error('PDFGATE_API_KEY environment variable is required.');
  const { url: baseUrl, environment } = getBaseUrl(key);

  const timeout = args['--timeout-seconds'] === undefined ? 120
    : parseNumber('--timeout-seconds', args['--timeout-seconds'], { min: 15, max: 960, integer: true });
  const output = resolve(args['--output']);
  if (!output.toLowerCase().endsWith('.pdf')) throw new Error('--output must have a .pdf extension.');
  await assertNotExists(output, args['--overwrite']);

  const body = buildBody(args);
  body.timeout = Math.min(timeout * 1000, MAX_SERVER_TIMEOUT_MS);
  if (args['--html-file']) body.html = await readTextFile('--html-file', args['--html-file'], { allowStdin: true });
  else body.url = publicUrl(args['--url']);
  if (args['--header-file']) body.header = await readTextFile('--header-file', args['--header-file']);
  if (args['--footer-file']) body.footer = await readTextFile('--footer-file', args['--footer-file']);

  // One deadline for the whole request, download included. A ref'd timer keeps
  // the process alive until the deadline even if the connection goes idle.
  const controller = new AbortController();
  const deadline = Object.assign(new Error('timeout'), { name: 'TimeoutError', timeoutSeconds: timeout });
  const timer = setTimeout(() => controller.abort(deadline), timeout * 1000);
  const response = await requestPdf(baseUrl, key, body, controller.signal).catch((err) => { clearTimeout(timer); throw err; });

  await mkdir(dirname(output), { recursive: true });
  const tmp = `${output}.${randomUUID()}.tmp`;
  try {
    try {
      await pipeline(Readable.fromWeb(response.body), createWriteStream(tmp, { flags: 'wx', mode: 0o600 }), { signal: controller.signal });
    } catch (err) {
      if (controller.signal.aborted) throw new Error(`PDFGate request timed out after ${timeout} seconds while downloading the PDF.`);
      throw new Error(`Failed to save the PDF: ${err.message}`);
    } finally { clearTimeout(timer); }
    const handle = await open(tmp, 'r');
    let isPdf;
    let info;
    try {
      const buffer = Buffer.alloc(5);
      const result = await handle.read(buffer, 0, 5, 0);
      isPdf = result.bytesRead === 5 && buffer.toString('ascii') === '%PDF-';
      info = await handle.stat();
    } finally { await handle.close(); }
    if (!isPdf) throw new Error('PDFGate did not return a PDF file (unexpected response format).');
    // Re-check so a file created while the request was running is not clobbered.
    await assertNotExists(output, args['--overwrite']);
    await rename(tmp, output);
    process.stdout.write(`${JSON.stringify({ success: true, path: output, bytes: info.size, environment })}\n`);
  } finally {
    await rm(tmp, { force: true });
  }
}

main().catch((err) => {
  process.stderr.write(`PDFGate skill error: ${err.message}\n`);
  process.exitCode = 1;
});
