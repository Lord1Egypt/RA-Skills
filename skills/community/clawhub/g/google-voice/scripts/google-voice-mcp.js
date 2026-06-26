#!/usr/bin/env node
/* Minimal Google Voice MCP server, no external deps.
 * Auth modes:
 *  - browser (default): uses Chrome DevTools Protocol at GV_CDP_URL or http://127.0.0.1:19222
 *    and runs fetch inside an existing/new Google Voice/clients6 tab so browser cookies are used.
 *  - header: set GV_COOKIE or GV_AUTHORIZATION to call clients6.google.com directly.
 * This server does not store credentials. It stops at API calls requested by MCP tools.
 */
const GV_API_KEY = process.env.GV_API_KEY;
if (!GV_API_KEY) throw new Error('Set GV_API_KEY from a local Google Voice web session/HAR before calling Google Voice endpoints. Do not commit it.');
const GV_CLIENT_VERSION = process.env.GV_CLIENT_VERSION || '906554935';
const CDP_HTTP = process.env.GV_CDP_URL || 'http://127.0.0.1:19222';
const MODE = process.env.GV_AUTH_MODE || (process.env.GV_COOKIE || process.env.GV_AUTHORIZATION ? 'header' : 'browser');
let GWS_TOKEN_CACHE = null;

function decodeMaybeBase64(text) {
  if (!text) return text;
  const t = text.trim();
  if (t.startsWith('[') || t.startsWith('{')) return t;
  try {
    const d = Buffer.from(t, 'base64').toString('utf8');
    if (d.trim().startsWith('[') || d.trim().startsWith('{')) return d;
  } catch {}
  return text;
}
function endpoint(path) { return `https://clients6.google.com${path}?alt=protojson&key=${GV_API_KEY}`; }
function baseHeaders() { return {
  'content-type': 'application/json+protobuf',
  'x-client-version': GV_CLIENT_VERSION,
  'x-goog-authuser': process.env.GV_AUTHUSER || '0',
  'x-goog-encode-response-if-executable': 'base64',
  'origin': 'https://clients6.google.com',
  'referer': 'https://clients6.google.com/static/proxy.html?usegapi=1',
}; }
async function getGwsAccessToken() {
  const now = Math.floor(Date.now() / 1000);
  if (GWS_TOKEN_CACHE && GWS_TOKEN_CACHE.exp > now + 60) return GWS_TOKEN_CACHE.token;
  const { execFileSync } = require('child_process');
  const exported = execFileSync(process.env.GWS_BIN || 'gws', ['auth', 'export'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
  const creds = JSON.parse(exported);
  if (!creds.refresh_token || !creds.client_id || !creds.client_secret) throw new Error('gws auth export did not return OAuth refresh credentials');
  const params = new URLSearchParams({
    client_id: creds.client_id,
    client_secret: creds.client_secret,
    refresh_token: creds.refresh_token,
    grant_type: 'refresh_token',
  });
  const res = await fetch('https://oauth2.googleapis.com/token', { method: 'POST', headers: { 'content-type': 'application/x-www-form-urlencoded' }, body: params });
  const j = await res.json();
  if (!res.ok || !j.access_token) throw new Error('gws token refresh failed: ' + JSON.stringify({ error: j.error, error_description: j.error_description }));
  GWS_TOKEN_CACHE = { token: j.access_token, exp: now + (j.expires_in || 3000) };
  return GWS_TOKEN_CACHE.token;
}
async function directFetch(path, body) {
  const headers = baseHeaders();
  if (MODE === 'gws') headers.authorization = 'Bearer ' + await getGwsAccessToken();
  if (process.env.GV_COOKIE) headers.cookie = process.env.GV_COOKIE;
  if (process.env.GV_AUTHORIZATION) headers.authorization = process.env.GV_AUTHORIZATION;
  const res = await fetch(endpoint(path), { method: 'POST', headers, body: JSON.stringify(body) });
  const text = decodeMaybeBase64(await res.text());
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${text.slice(0,500)}`);
  return JSON.parse(text);
}
async function cdpEval(tabId, expression, timeout=30000) {
  const wsUrl = `ws://127.0.0.1:19222/devtools/page/${tabId}`;
  const ws = new WebSocket(wsUrl);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
  const p = new Promise((res, rej) => { ws.onmessage = e => res(JSON.parse(e.data)); ws.onerror = rej; });
  ws.send(JSON.stringify({ id: 1, method: 'Runtime.evaluate', params: { expression, awaitPromise: true, returnByValue: true, timeout } }));
  const msg = await p; ws.close();
  if (msg.result?.exceptionDetails) throw new Error(msg.result.exceptionDetails.exception?.description || msg.result.exceptionDetails.text);
  if (msg.error) throw new Error(msg.error.message);
  return msg.result.result.value;
}
async function getBrowserTab() {
  const tabs = await (await fetch(`${CDP_HTTP}/json/list`)).json();
  const existing = tabs.find(t => /clients6\.google\.com|voice\.google\.com/.test(t.url || ''));
  if (existing) return existing.id;
  const j = await (await fetch(`${CDP_HTTP}/json/new?` + encodeURIComponent('https://voice.google.com/'), { method: 'PUT' })).json();
  await new Promise(r => setTimeout(r, 2500));
  return j.id;
}
async function browserFetch(path, body) {
  const tab = await getBrowserTab();
  const expr = `(async()=>{const res=await fetch(${JSON.stringify(endpoint(path))},{method:'POST',credentials:'include',headers:${JSON.stringify(baseHeaders())},body:${JSON.stringify(JSON.stringify(body))}}); const text=await res.text(); return {ok:res.ok,status:res.status,text};})()`;
  const out = await cdpEval(tab, expr, 45000);
  const text = decodeMaybeBase64(out.text || '');
  if (!out.ok) throw new Error(`HTTP ${out.status}: ${text.slice(0,500)}`);
  return JSON.parse(text);
}
async function gvFetch(path, body) { return (MODE === 'header' || MODE === 'gws') ? directFetch(path, body) : browserFetch(path, body); }

function summarizeThreadList(raw, limit=20) {
  const rows = Array.isArray(raw?.[0]) ? raw[0] : Array.isArray(raw) ? raw : [];
  return rows.slice(0, limit).map(row => ({
    threadId: row?.[0],
    timestampMs: row?.[2]?.[0]?.[1] || row?.[1] || null,
    snippet: row?.[2]?.[0]?.[9] || row?.[9] || null,
    participants: row?.[2]?.[0]?.[15] || row?.[15] || null,
    raw: process.env.GV_INCLUDE_RAW === '1' ? row : undefined,
  }));
}
function summarizeThread(raw) {
  const arr = Array.isArray(raw?.[0]) ? raw[0] : raw;
  const events = Array.isArray(arr?.[2]) ? arr[2] : [];
  return { threadId: arr?.[0], events: events.map(e => ({ id:e?.[0], timestampMs:e?.[1], from:e?.[2], text:e?.[9], type:e?.[4], raw:process.env.GV_INCLUDE_RAW==='1'?e:undefined })) };
}
const tools = [
  { name: 'gv_list_threads', description: 'List Google Voice SMS/thread summaries using HAR-derived /api2thread/list. Requires an authenticated browser session or GV_COOKIE/GV_AUTHORIZATION.', inputSchema: { type:'object', properties:{ pageSize:{type:'number', default:20}, raw:{type:'boolean', default:false} } } },
  { name: 'gv_get_thread', description: 'Get messages for a Google Voice thread id (for example t.22395).', inputSchema: { type:'object', required:['threadId'], properties:{ threadId:{type:'string'}, limit:{type:'number', default:100}, context:{type:['string','null'], description:'Optional third positional value observed in HAR, usually phone/group context.'}, raw:{type:'boolean', default:false} } } },
  { name: 'gv_send_sms', description: 'Experimental send SMS via HAR-derived /api2thread/sendsms. Use only with explicit user approval. May require anti-abuse token/context from browser.', inputSchema: { type:'object', required:['text','recipients'], properties:{ text:{type:'string'}, recipients:{type:'array', items:{type:'string'}}, threadId:{type:['string','null']}, token:{type:['string','null']} } } },
  { name: 'gv_raw_call', description: 'Advanced: call a HAR-derived Google Voice endpoint with a JSON/protobuf body. For debugging only.', inputSchema: { type:'object', required:['path','body'], properties:{ path:{type:'string'}, body:{} } } },
];
async function callTool(name, args={}) {
  if (args.raw) process.env.GV_INCLUDE_RAW='1'; else delete process.env.GV_INCLUDE_RAW;
  if (name === 'gv_list_threads') {
    const body = [1, args.pageSize || 20, 15, null, null, [null,1,1,1]];
    const raw = await gvFetch('/voice/v1/voiceclient/api2thread/list', body);
    return args.raw ? raw : summarizeThreadList(raw, args.pageSize || 20);
  }
  if (name === 'gv_get_thread') {
    const raw = await gvFetch('/voice/v1/voiceclient/api2thread/get', [args.threadId, args.limit || 100, args.context || null, [null,1,1]]);
    return args.raw ? raw : summarizeThread(raw);
  }
  if (name === 'gv_send_sms') {
    const body = [null,null,null,null,args.text,args.threadId || null,null,null,args.recipients,null,args.token ? [args.token] : []];
    return await gvFetch('/voice/v1/voiceclient/api2thread/sendsms', body);
  }
  if (name === 'gv_raw_call') return await gvFetch(args.path, args.body);
  throw new Error(`unknown tool ${name}`);
}
function send(obj) { process.stdout.write(JSON.stringify(obj) + '\n'); }
async function handle(msg) {
  if (msg.method === 'initialize') return send({ jsonrpc:'2.0', id:msg.id, result:{ protocolVersion:'2024-11-05', capabilities:{ tools:{} }, serverInfo:{ name:'google-voice-har', version:'0.1.0' } } });
  if (msg.method === 'notifications/initialized') return;
  if (msg.method === 'tools/list') return send({ jsonrpc:'2.0', id:msg.id, result:{ tools } });
  if (msg.method === 'tools/call') {
    try { const result = await callTool(msg.params.name, msg.params.arguments || {}); return send({ jsonrpc:'2.0', id:msg.id, result:{ content:[{ type:'text', text: JSON.stringify(result, null, 2) }] } }); }
    catch (e) { return send({ jsonrpc:'2.0', id:msg.id, error:{ code:-32000, message:String(e.message || e) } }); }
  }
  send({ jsonrpc:'2.0', id:msg.id, error:{ code:-32601, message:'method not found' } });
}
let buf=''; process.stdin.setEncoding('utf8'); process.stdin.on('data', chunk => { buf += chunk; for (;;) { const i=buf.indexOf('\n'); if (i<0) break; const line=buf.slice(0,i).trim(); buf=buf.slice(i+1); if (!line) continue; Promise.resolve().then(()=>handle(JSON.parse(line))).catch(e=>send({jsonrpc:'2.0', id:null, error:{code:-32000, message:String(e)}})); } });
