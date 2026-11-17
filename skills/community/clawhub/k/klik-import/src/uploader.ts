import https from 'node:https';
import http from 'node:http';
import zlib from 'node:zlib';
import type { ImportPayload } from './types.ts';

export const KLIK_BASE_URL = process.env.KLIK_BASE_URL ?? 'https://hiklik.ai';
const KLIK_AUTH_URL = process.env.KLIK_AUTH_URL ?? KLIK_BASE_URL;
const KLIK_MEMORY_URL = process.env.KLIK_MEMORY_URL ?? KLIK_BASE_URL;

export interface UploaderOptions {
  baseUrl?: string;
}

export interface VerifyResult {
  user_id: string;
  import_token: string;
  ttl_seconds: number;
}

export interface UploadResult {
  import_id: string;
  accepted: Array<{ collector: string; item_count: number }>;
  server_timestamp: string;
}

function request(
  method: string,
  url: string,
  body: string | Buffer,
  headers: Record<string, string>
): Promise<{ status: number; body: string }> {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const transport = parsed.protocol === 'https:' ? https : http;
    const req = transport.request(
      { method, hostname: parsed.hostname, port: parsed.port || undefined,
        path: parsed.pathname + parsed.search, headers },
      (res) => {
        let data = '';
        res.on('data', (chunk: Buffer) => (data += chunk.toString()));
        res.on('end', () => resolve({ status: res.statusCode ?? 0, body: data }));
      }
    );
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

export async function verifyCode(code: string, opts: UploaderOptions = {}): Promise<VerifyResult> {
  const base = opts.baseUrl ?? KLIK_AUTH_URL;
  const body = JSON.stringify({ code });
  const { status, body: respBody } = await request(
    'POST',
    `${base}/api/v1/auth/import-code/verify`,
    body,
    { 'Content-Type': 'application/json', 'Content-Length': String(Buffer.byteLength(body)) }
  );
  const json = JSON.parse(respBody);
  if (status !== 200) {
    throw new Error(json.error ?? `HTTP ${status}`);
  }
  return json as VerifyResult;
}

export async function uploadPayload(
  payload: ImportPayload,
  importToken: string,
  opts: UploaderOptions = {}
): Promise<UploadResult> {
  const base = opts.baseUrl ?? KLIK_MEMORY_URL;
  const raw = Buffer.from(JSON.stringify(payload), 'utf8');
  const shouldGzip = raw.byteLength > 256 * 1024;
  const body = shouldGzip ? zlib.gzipSync(raw) : raw;

  const headers: Record<string, string> = {
    'X-Import-Token': importToken,
    'Content-Type': 'application/json',
    'Content-Length': String(body.byteLength),
  };
  if (shouldGzip) headers['Content-Encoding'] = 'gzip';

  const { status, body: respBody } = await request(
    'POST',
    `${base}/api/v1/memory/import/upload`,
    body,
    headers
  );
  const json = JSON.parse(respBody);
  if (status !== 200) {
    throw new Error(json.error ?? JSON.stringify(json));
  }
  return json as UploadResult;
}
