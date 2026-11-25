import { readAnalytics, ANALYTICS_CONFIG } from './analytics.mjs';
import { mkdir, readFile, writeFile, rename, unlink, open, lstat } from 'node:fs/promises';
import { homedir } from 'node:os';
import path from 'node:path';
import { randomUUID } from 'node:crypto';

export const API = 'https://imagen.chat/api/v1';
export const CONFIG = path.join(homedir(), '.config', 'imagen-chat', 'creator.json');
export async function readKey(file = CONFIG) {
  try { return JSON.parse(await readFile(file, 'utf8')).api_key || ''; }
  catch (e) { if (e.code === 'ENOENT') return ''; throw new Error('Cannot read Imagen credentials. Reconfigure using the local page.'); }
}
export async function saveKey(key, file = CONFIG) {
  if (!/^img_live_[a-f0-9]{64}$/.test(key)) throw new Error('Enter an Imagen creator key, not a model-provider key.');
  await mkdir(path.dirname(file), { recursive: true, mode: 0o700 });
  const temporary = `${file}.${randomUUID()}.tmp`;
  await writeFile(temporary, JSON.stringify({ api_key: key }), { mode: 0o600, flag: 'wx' });
  await rename(temporary, file);
}
export async function removeKey(file = CONFIG) { await unlink(file).catch(e => { if (e.code !== 'ENOENT') throw e; }); }
export class ImagenClient {
  constructor({ api = API, keyFile = CONFIG, analyticsFile = ANALYTICS_CONFIG, fetcher = fetch } = {}) { this.api = api; this.keyFile = keyFile; this.fetcher = fetcher; this.analyticsFile = analyticsFile; }
  async request(route, { method = 'GET', body, authenticated = false, key } = {}) {
    const headers = { Accept: 'application/json' };
    if (authenticated || key) {
      const secret = key || await readKey(this.keyFile);
      if (!secret) throw new Error('Connect your Imagen account using the local configuration page first.');
      headers.Authorization = `Bearer ${secret}`;
    }
    if (body) headers['Content-Type'] = 'application/json';
    let response;
    try { response = await this.fetcher(this.api + route, { method, headers, body: body ? JSON.stringify(body) : undefined, redirect: 'error', signal: AbortSignal.timeout(25000) }); }
    catch { throw new Error('Imagen connection failed. Check your connection and retry.'); }
    let data;
    try { data = await response.json(); } catch { throw new Error(`Imagen returned an unexpected response (${response.status}).`); }
    if (!response.ok) {
      const code = data.error?.code || `http_${response.status}`;
      // Stable error codes only: never echo remote strings that could contain secrets.
      throw new Error(`Imagen: ${/^[a-z0-9_]+$/i.test(code) ? code : response.status}`);
    }
    return data;
  }
  async search(filters) {
    const allowed = ['query', 'orientation', 'style', 'topic', 'use_case', 'composition', 'page', 'page_size', 'sort'];
    const body = Object.fromEntries(Object.entries(filters).filter(([k,v]) => allowed.includes(k) && v !== undefined && v !== ''));
    for (const name of ['page', 'page_size']) if (body[name] !== undefined) body[name] = Number(body[name]);
    const release = JSON.parse(await readFile(new URL('../release.json', import.meta.url), 'utf8'));
    body.query ??= ''; body.version = release.version; body.record_keywords = await readAnalytics(this.analyticsFile);
    console.error(body.record_keywords ? 'Imagen search: anonymous operational counters; opted-in short query terms retained up to 30 days. analytics --keywords off stops future keyword retention.' : 'Imagen search: anonymous operational counters; keyword retention is OFF. Do not send secrets or article content.');
    const result = await this.request('/gallery/skill/search', { method: 'POST', body });
    return { ...result, items: result.items.map(asset => ({ ...asset, detail_url: `https://imagen.chat/en/images/${asset.slug}--${asset.public_id}`, watermarked: true })) };
  }
  credits(key) { return this.request('/gallery/me/credits', { authenticated: true, key }); }
  detail(id) { validateID(id); return this.request(`/gallery/assets/${id}`); }
  validateMediaURL(url, original) {
    const target = new URL(url), api = new URL(this.api);
    const loopback = hostname => ['127.0.0.1', 'localhost', '[::1]'].includes(hostname);
    const localDevelopment = loopback(api.hostname) && loopback(target.hostname) && api.protocol === 'http:';
    if ((target.protocol !== 'https:' && !(localDevelopment && target.protocol === 'http:')) || target.username || target.password || (!original && target.hostname !== 'cdn.imagen.chat' && !localDevelopment)) throw new Error('Unexpected image delivery URL.');
  }
  async originalLink(id, { maxCredits = 0, operationID = randomUUID() } = {}) {
    validateID(id);
    if (!Number.isSafeInteger(maxCredits) || maxCredits < 0) throw new Error('max-credits must be a non-negative integer.');
    if (typeof operationID !== 'string' || !/^[a-zA-Z0-9_-]{8,100}$/.test(operationID)) throw new Error('Use an operation ID of 8–100 letters, digits, underscores or hyphens.');
    const entitlement = await this.request(`/gallery/assets/${id}/entitlement`, { authenticated: true });
    let spent = 0;
    if (!entitlement.unlocked) {
      if (maxCredits < 1) throw new Error('Original needs 1 credit. Obtain a user budget before passing --max-credits 1.');
      const result = await this.request(`/gallery/assets/${id}/unlock`, { authenticated: true, method: 'POST', body: { idempotency_key: `${operationID}:unlock` } });
      spent = result.newly_unlocked ? 1 : 0;
    }
    const grant = await this.request(`/gallery/assets/${id}/download`, { authenticated: true, method: 'POST', body: { idempotency_key: `${operationID}:download` } });
    this.validateMediaURL(grant.url, true);
    return { ...grant, asset_public_id: id, watermarked: false, temporary: true, credits_spent: spent, operation_id: operationID, notice: 'Temporary original link. Anyone holding it can download until expiry. Do not use as a permanent image-hosting URL.' };
  }
  async download(id, output, { original = false, maxCredits = 0, operationID = randomUUID() } = {}) {
    validateID(id);
    await lstat(path.resolve(output)).then(() => { throw new Error('Destination already exists (EEXIST). Choose a new filename.'); }, error => { if (error.code !== 'ENOENT') throw error; });
    if (!Number.isSafeInteger(maxCredits) || maxCredits < 0) throw new Error('max-credits must be a non-negative integer.');
    let url, grant;
    if (original) {
      grant = await this.originalLink(id, { maxCredits, operationID });
      url = grant.url;
    } else {
      const detail = await this.detail(id);
      url = detail.asset.preview.url;
    }
    this.validateMediaURL(url, original);
    let response;
    try { response = await this.fetcher(url, { redirect: 'error', signal: AbortSignal.timeout(60000) }); }
    catch { throw new Error('Image download failed. Retry with the same operation ID; the original stays unlocked.'); }
    if (!response.ok || !/^image\//i.test(response.headers.get('content-type') || '')) throw new Error('Image download failed or returned non-image content.');
    const limit = 100 * 1024 * 1024;
    if (Number(response.headers.get('content-length')) > limit) throw new Error('Image exceeds the 100 MB download limit.');
    const absolute = path.resolve(output);
    await mkdir(path.dirname(absolute), { recursive: true });
    const temporary = `${absolute}.${randomUUID()}.part`;
    const file = await open(temporary, 'wx', 0o600);
    try {
      let total = 0;
      for await (const chunk of response.body) {
        total += chunk.length;
        if (total > limit) throw new Error('Image exceeds the 100 MB download limit.');
        await file.writeFile(chunk);
      }
      await file.close();
      // Hard link makes the final create exclusive: existing user files are preserved.
      const { link } = await import('node:fs/promises');
      await link(temporary, absolute);
    } finally { await file.close().catch(() => {}); await unlink(temporary).catch(() => {}); }
    return { path: absolute, asset_public_id: id, watermarked: !original, content_type: response.headers.get('content-type'), credits_spent: grant?.credits_spent || 0, ...(original ? { download_expires_at: grant.expires_at } : { public_url: url }), operation_id: operationID };
  }
}
export function validateID(id) { if (!/^[a-f0-9]{32}$/.test(id || '')) throw new Error('Use a valid Imagen public ID.'); }
