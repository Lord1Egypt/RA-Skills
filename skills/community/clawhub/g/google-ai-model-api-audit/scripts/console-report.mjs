#!/usr/bin/env node
/**
 * console-report.mjs — read a Google Cloud Billing "Reports" page as text via Chrome DevTools Protocol.
 *
 * Why: the billing console holds 30+ days of cost history that the BigQuery billing export
 * cannot backfill, and has no public API. This drives a Chrome that is already signed in.
 *
 * Requires: a Chrome started with --remote-debugging-port=<port> and the target Google account
 * signed in. Pick the right account with --authuser (0-based index in the account switcher).
 *
 * Usage:
 *   node console-report.mjs --account <BILLING_ACCOUNT_ID> --from 2026-11-16 --to 2026-11-22
 *   node console-report.mjs --account ... --from ... --to ... --authuser 1 --json
 *   node console-report.mjs --url "<full reports url>" --json
 *
 * Output: JSON { url, account, from, to, spent, saved, table, raw } on stdout.
 * Nothing is written to disk. The tab is closed afterwards.
 */
import http from 'node:http';

function arg(name, def) {
  const i = process.argv.indexOf('--' + name);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : def;
}
const flag = (name) => process.argv.includes('--' + name);

const PORT = Number(arg('port', '18800'));
const ACCOUNT = arg('account', '');
const FROM = arg('from', '');
const TO = arg('to', '');
const AUTHUSER = arg('authuser', '');
const WAIT_S = Number(arg('wait', '25'));
const TABLE_CHARS = Number(arg('chars', '2500'));

function buildUrl() {
  const explicit = arg('url', '');
  if (explicit) return explicit;
  if (!ACCOUNT || !FROM || !TO) {
    console.error('ERROR: need --account/--from/--to, or --url');
    process.exit(2);
  }
  const p = '/billing/' + ACCOUNT + '/reports;timeRange=CUSTOM_RANGE;from=' + FROM +
            ';to=' + TO + ';timeGrouping=GROUP_BY_DAY';
  return 'https://console.cloud.google.com' + p + (AUTHUSER ? '?authuser=' + AUTHUSER : '');
}

function httpJson(path, method) {
  return new Promise((res, rej) => {
    const req = http.request({ host: '127.0.0.1', port: PORT, path, method: method || 'GET' }, r => {
      let d = '';
      r.on('data', c => (d += c));
      r.on('end', () => { try { res(JSON.parse(d)); } catch (e) { rej(new Error('bad CDP response on ' + path + ': ' + d.slice(0, 200))); } });
    });
    req.on('error', e => rej(new Error('cannot reach Chrome CDP on port ' + PORT + ' (' + e.message + '). Start Chrome with --remote-debugging-port=' + PORT)));
    req.end();
  });
}

class CDP {
  constructor(wsUrl) { this.wsUrl = wsUrl; this.id = 0; this.pending = new Map(); }
  connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.wsUrl);
      this.ws.onopen = () => resolve();
      this.ws.onerror = () => reject(new Error('CDP websocket failed'));
      this.ws.onmessage = ev => {
        const m = JSON.parse(ev.data);
        if (m.id && this.pending.has(m.id)) {
          const p = this.pending.get(m.id);
          this.pending.delete(m.id);
          m.error ? p.reject(new Error(JSON.stringify(m.error))) : p.resolve(m.result);
        }
      };
    });
  }
  send(method, params = {}) {
    const id = ++this.id;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
      setTimeout(() => {
        if (this.pending.has(id)) { this.pending.delete(id); reject(new Error('CDP timeout: ' + method)); }
      }, 45000);
    });
  }
  async js(expression) {
    const r = await this.send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) throw new Error('page JS error: ' + JSON.stringify(r.exceptionDetails).slice(0, 300));
    return r.result && r.result.value;
  }
}

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

(async () => {
  const url = buildUrl();
  const target = await httpJson('/json/new?' + encodeURIComponent(url), 'PUT');
  const cdp = new CDP(target.webSocketDebuggerUrl);
  await cdp.connect();
  await cdp.send('Page.enable');

  // Wait for the cost summary rather than guessing at a fixed delay.
  const deadline = Date.now() + WAIT_S * 1000;
  let text = '';
  while (Date.now() < deadline) {
    await sleep(2000);
    text = await cdp.js('document.body.innerText.replace(/\\n{2,}/g,"\\n")').catch(() => '');
    const summaryReady = /You spent/.test(text) && !text.includes('Loading contents');
    const tableReady = text.includes('Download CSV') && !/Loading contents/.test(text) && /\$[0-9]/.test(text.slice(text.indexOf('Download CSV')));
    if (summaryReady && tableReady) break;
    if (/Verify it.s you|signin\/confirmidentifier/.test(text)) break;
  }

  const href = await cdp.js('location.href').catch(() => url);
  const signedOut = /accounts\.google\.com/.test(href);
  const spent = (text.match(/You spent[^\n]*/) || [''])[0];
  const saved = (text.match(/You saved[^\n]*/) || [''])[0];
  let table = '';
  const anchors = ['Download CSV', 'Date › SKU', 'Date › Service', 'Date › Project'];
  for (const a of anchors) {
    const i = text.indexOf(a);
    if (i >= 0) { table = text.slice(i, i + TABLE_CHARS); break; }
  }
  const out = {
    ok: !signedOut && (spent !== '' || saved !== '' || table !== ''),
    url: href,
    account: ACCOUNT,
    from: FROM,
    to: TO,
    authuser: AUTHUSER || '(default)',
    spent,
    saved,
    table,
    hint: signedOut
      ? 'Signed out: Chrome is not authenticated for this URL. Pick the right account with --authuser, or sign in in that browser profile.'
      : (spent === '' && saved === ''
          ? 'No cost summary found. The page may still be loading (raise --wait), the account may lack billing.viewer, or the billing account id is wrong.'
          : ''),
    raw: flag('raw') ? text.slice(0, 8000) : undefined
  };
  if (flag('json')) console.log(JSON.stringify(out, null, 2));
  else {
    console.log('URL: ' + out.url);
    console.log(spent || '(no spent line)');
    console.log(saved || '(no saved line)');
    if (table) { console.log('--- table ---'); console.log(table); }
    if (out.hint) console.log('\nHINT: ' + out.hint);
  }
  await cdp.send('Target.closeTarget', { targetId: target.id }).catch(() => {});
  cdp.ws.close();
  process.exit(out.ok ? 0 : 1);
})().catch(e => { console.error('ERROR: ' + e.message); process.exit(1); });
