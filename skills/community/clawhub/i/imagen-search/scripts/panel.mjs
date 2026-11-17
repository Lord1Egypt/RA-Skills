import http from 'node:http';
import { randomBytes, timingSafeEqual } from 'node:crypto';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { readKey, saveKey, removeKey } from './client.mjs';

export async function startPanel({ client, manifest = { items: [] }, selectionFile = path.resolve('imagen-selection.json'), ttl = 30 * 60 * 1000 } = {}) {
  const token = randomBytes(32).toString('hex');
  let selected = [], revision = 0;
  const assets = new Map((manifest.items || []).map(item => [item.public_id, item]));
  const html = await readFile(fileURLToPath(new URL('../assets/panel.html', import.meta.url)));
  let origin;
  const json = (res, status, body) => { res.writeHead(status, { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' }); res.end(JSON.stringify(body)); };
  const server = http.createServer(async (req, res) => {
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('Referrer-Policy', 'no-referrer');
    res.setHeader('Content-Security-Policy', "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src https://cdn.imagen.chat; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'");
    if (req.headers.host !== new URL(origin).host || (req.headers.origin && req.headers.origin !== origin)) return json(res, 403, { error: 'local_origin_required' });
    const route = new URL(req.url, origin).pathname;
    if (req.method === 'GET' && route === '/') { res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' }); res.end(html); return; }
    const provided = Buffer.from(req.headers['x-imagen-session'] || '');
    if (provided.length !== token.length || !timingSafeEqual(provided, Buffer.from(token))) return json(res, 403, { error: 'local_session_required' });
    let body = {};
    try {
      if (req.method === 'POST') {
        if (req.headers['content-type'] !== 'application/json') return json(res, 415, { error: 'json_required' });
        let content = '';
        for await (const chunk of req) { content += chunk; if (content.length > 16384) throw new Error('Request too large.'); }
        body = JSON.parse(content || '{}');
      }
      if (req.method === 'GET' && route === '/state') return json(res, 200, { connected: Boolean(await readKey(client.keyFile)), items: [...assets.values()], selected, revision });
      if (req.method === 'GET' && route === '/credits') return json(res, 200, await client.credits());
      if (req.method === 'POST' && route === '/key') {
        if (!/^img_live_[a-f0-9]{64}$/.test(body.key || '')) throw new Error('Enter an Imagen creator key, not a model-provider key.');
        await client.credits(body.key); // Validate before replacing the saved credential.
        await saveKey(body.key, client.keyFile);
        return json(res, 200, { connected: true });
      }
      if (req.method === 'POST' && route === '/disconnect') { await removeKey(client.keyFile); return json(res, 200, { connected: false }); }
      if (req.method === 'POST' && route === '/search') {
        const result = await client.search({ query: String(body.query || '').slice(0,120), orientation: body.orientation || '', page_size: 12 });
        for (const item of result.items) assets.set(item.public_id, item);
        return json(res, 200, result);
      }
      if (req.method === 'POST' && route === '/selection') {
        if (!Array.isArray(body.ids) || body.ids.some(id => !assets.has(id))) throw new Error('Select images from the displayed results.');
        selected = [...new Set(body.ids)]; revision++;
        const file = path.resolve(selectionFile);
        await mkdir(path.dirname(file), { recursive: true });
        // Selection files contain only public metadata, never credentials or signed URLs.
        await writeFile(file, JSON.stringify({ revision, selected: selected.map(id => assets.get(id)), saved_at: new Date().toISOString() }, null, 2), { mode: 0o600 });
        return json(res, 200, { saved: true, count: selected.length });
      }
      if (req.method === 'POST' && route === '/close') { json(res, 200, { closed: true }); setImmediate(close); return; }
      json(res, 404, { error: 'not_found' });
    } catch (error) { json(res, 400, { error: error.message }); }
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  origin = `http://127.0.0.1:${server.address().port}`;
  const timer = setTimeout(() => close(), ttl);
  function close() { clearTimeout(timer); server.closeAllConnections(); server.close(); }
  return { url: `${origin}/#${token}`, selectionFile: path.resolve(selectionFile), close };
}
