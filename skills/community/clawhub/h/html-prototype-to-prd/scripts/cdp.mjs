const BASE = 'http://127.0.0.1:9222';

export async function openSession() {
  const targets = await (await fetch(BASE + '/json/list')).json();
  const page = targets.find(t => t.type === 'page');
  if (!page) throw new Error('no page target');
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  let id = 0;
  const pending = new Map();
  ws.onmessage = e => {
    const m = JSON.parse(e.data);
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
  };
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });

  function send(method, params = {}) {
    const i = ++id;
    return new Promise(r => { pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  }

  await send('Page.enable');
  await send('Runtime.enable');
  await send('Log.enable').catch(() => {});

  async function go(url) {
    const loaded = new Promise(r => { ws.onmessage2 = r; });
    await send('Page.navigate', { url });
    for (let i = 0; i < 60; i++) {
      const s = await evalJs('document.readyState');
      if (s === 'complete') break;
      await sleep(150);
    }
    await sleep(600);
  }

  async function evalJs(expression) {
    const r = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
    if (r.result && r.result.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails).slice(0, 800));
    return r.result && r.result.result ? r.result.result.value : undefined;
  }

  async function shot(file, clip) {
    const params = { format: 'png', captureBeyondViewport: !!clip };
    if (clip) Object.assign(params, { clip: { ...clip, scale: 1 } });
    const r = await send('Page.captureScreenshot', params);
    if (!r.result || !r.result.data) throw new Error('screenshot failed: ' + JSON.stringify(r).slice(0, 400));
    const fs = await import('node:fs');
    fs.writeFileSync(file, Buffer.from(r.result.data, 'base64'));
    return file;
  }

  function close() { try { ws.close(); } catch (e) {} }
  return { ws, send, go, evalJs, shot, close };
}

export const sleep = ms => new Promise(r => setTimeout(r, ms));
