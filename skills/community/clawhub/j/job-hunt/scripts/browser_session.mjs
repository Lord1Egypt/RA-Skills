#!/usr/bin/env node
/** One consented Chrome connection, isolated CDP clients, no automatic reconnect. */
import {createServer} from 'node:http';
import {randomBytes} from 'node:crypto';
import {createRequire} from 'node:module';
import {readFile, writeFile, mkdir, unlink, open} from 'node:fs/promises';
import {join, resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';
import {dailyEndpoint} from './browser_cdp.mjs';

const alive = pid => {try {process.kill(pid, 0);return true;} catch {return false;}};
const send = (ws, value) => {if (ws?.readyState === 1) ws.send(JSON.stringify(value));};
const failed = state => ['disconnected', 'consent_timeout'].includes(state);
const connectionHelp = browser => `Cannot connect to the selected daily ${browser}. Keep it open and ${browser === 'chrome' ? 'enable remote debugging at chrome://inspect/#remote-debugging' : 'enable its supported remote-debugging endpoint'}, then start one session and accept the browser's connection prompt.`;

export async function createSession({endpoint, WebSocket, WebSocketServer,
  idleMs = 30 * 60 * 1000, consentMs = 120000, changed = () => {}}) {
  const token = randomBytes(24).toString('hex');
  const socketPath = `/devtools/browser/${token}`;
  const pending = new Map(), owners = new Map(), sessionTargets = new Map(), targets = new Map(), clients = new Set();
  let sequence = 0, state = 'waiting_for_consent', lastUse = Date.now(), closing = false;
  const server = createServer((req, res) => {
    if (!req.headers.origin && req.url === socketPath + '/status' && req.method === 'GET') {
      res.setHeader('Content-Type','application/json');
      res.end(JSON.stringify({pid:process.pid,state,clients:clients.size,owned_tabs:targets.size,upstream_connections:1}));return;
    }
    if (!req.headers.origin && req.url === socketPath + '/stop' && req.method === 'POST') {
      if (clients.size) {res.writeHead(409);res.end('Active clients still use this session');return;}
      res.end('stopping');void close();return;
    }
    res.writeHead(404);res.end();
  });
  const downstream = new WebSocketServer({noServer:true, maxPayload:8 * 1024 * 1024});
  const upstream = new WebSocket(endpoint);
  const publish = () => changed({state, clients:clients.size, owned_tabs:targets.size});
  function forward(client, command, cleanup = false) {
    const id = ++sequence;
    pending.set(id, {client, original:command.id, command, cleanup});
    upstream.send(JSON.stringify({...command, id}));
  }
  function closeTarget(targetId) {
    if (upstream.readyState === 1) forward(null, {method:'Target.closeTarget',params:{targetId}}, true);
  }
  function allowed(client, command) {
    const {method, params = {}, sessionId} = command;
    if (sessionId && owners.get(sessionId) !== client) return false;
    if (method === 'Target.createTarget') {
      if (sessionId || params.browserContextId) return false;
      try {
        const u = new URL(params.url);
        return (params.url === 'about:blank' || ['http:', 'https:'].includes(u.protocol)) && !u.username && !u.password;
      } catch {return false;}
    }
    if (method === 'JobHunt.handoffTarget') return !sessionId && targets.get(params.targetId) === client;
    if (['Target.attachToTarget','Target.closeTarget','Target.getTargetInfo','Target.activateTarget'].includes(method)) {
      return targets.get(params.targetId) === client;
    }
    if (method === 'Target.detachFromTarget') return owners.get(params.sessionId) === client;
    if (method.startsWith('Target.') || method.startsWith('Browser.')) return method === 'Browser.getVersion';
    return Boolean(sessionId);
  }
  server.on('upgrade', (req, socket, head) => {
    // Only a local tool holding this session's random path can connect. Web
    // pages with an Origin are not clients of this local transport.
    if (req.url !== socketPath || req.headers.origin || state !== 'connected') {
      socket.end('HTTP/1.1 403 Forbidden\r\nConnection: close\r\n\r\n');return;
    }
    downstream.handleUpgrade(req, socket, head, ws => downstream.emit('connection', ws));
  });
  downstream.on('connection', client => {
    clients.add(client);lastUse = Date.now();publish();
    client.on('error', () => {});
    client.on('message', raw => {
      let command;
      try {command = JSON.parse(raw.toString());} catch {client.close(1007);return;}
      if (!Number.isInteger(command?.id) || typeof command.method !== 'string') {client.close(1007);return;}
      if (!allowed(client, command)) {
        send(client, {id:command.id,error:{code:-32000,message:'CDP operation is outside this client-owned tab/session'}});return;
      }
      if (command.method === 'JobHunt.handoffTarget') {
        // A login/verification page now belongs to the user. Release it before
        // acknowledging, so disconnect/idle/stop cleanup cannot close it and
        // this client cannot keep operating its formerly attached session.
        const targetId = command.params.targetId;
        targets.delete(targetId);
        for (const [id, target] of sessionTargets) if (target === targetId) {
          owners.delete(id);sessionTargets.delete(id);
          forward(null, {method:'Target.detachFromTarget',params:{sessionId:id}}, true);
        }
        lastUse = Date.now();
        forward(client, {id:command.id,method:'Target.activateTarget',params:{targetId}});
        publish();return;
      }
      lastUse = Date.now();forward(client, command);
    });
    client.on('close', () => {
      clients.delete(client);lastUse = Date.now();
      for (const [targetId, owner] of targets) if (owner === client) closeTarget(targetId);
      publish();
    });
  });
  upstream.on('open', () => {state = 'connected';clearTimeout(consentTimer);publish();});
  upstream.on('error', () => {});
  upstream.on('message', raw => {
    let message;try {message = JSON.parse(raw.toString());} catch {return;}
    const item = pending.get(message.id);
    if (item) {
      pending.delete(message.id);
      const {client, command} = item;
      if (!message.error) {
        if (command.method === 'Target.createTarget' && message.result?.targetId) {
          targets.set(message.result.targetId, client);
          // A client can disappear before its creation response arrives.
          if (!clients.has(client)) closeTarget(message.result.targetId);
        }
        if (command.method === 'Target.attachToTarget' && message.result?.sessionId) {
          if (targets.get(command.params.targetId) === client && clients.has(client)) {
            owners.set(message.result.sessionId, client);
            sessionTargets.set(message.result.sessionId, command.params.targetId);
          } else {
            // An attach can finish after handoff or client disconnect. Never
            // restore access to a page that was already released to the user.
            forward(null, {method:'Target.detachFromTarget',params:{sessionId:message.result.sessionId}}, true);
          }
        }
        if (command.method === 'Target.closeTarget' && message.result?.success) targets.delete(command.params.targetId);
        if (command.method === 'Target.detachFromTarget') {owners.delete(command.params.sessionId);sessionTargets.delete(command.params.sessionId);}
      }
      send(client, {...message,id:item.original});publish();return;
    }
    if (message.method === 'Target.detachedFromTarget') {owners.delete(message.params?.sessionId);sessionTargets.delete(message.params?.sessionId);}
    if (message.method === 'Target.targetDestroyed') targets.delete(message.params?.targetId);
    // Never broadcast another client's events or pre-existing browser tabs.
    const owner = owners.get(message.sessionId) || targets.get(message.params?.targetId);
    if (owner) send(owner, message);
  });
  const close = async (finalState = 'closed') => {
    if (closing) return;
    closing = true;state = finalState;publish();clearTimeout(consentTimer);clearInterval(idleTimer);
    for (const targetId of targets.keys()) closeTarget(targetId);
    for (const client of clients) client.close(1001);
    if (upstream.readyState === 1) await new Promise(r => setTimeout(r, 100));
    upstream.close();downstream.close();server.close();publish();
  };
  upstream.on('close', () => {
    if (closing) return;
    clearTimeout(consentTimer);
    for (const client of clients) client.close(1011, 'Browser connection ended; explicitly start a new session');
    pending.clear();void close('disconnected');
  });
  const consentTimer = setTimeout(() => {void close('consent_timeout');}, consentMs);
  const idleTimer = setInterval(() => {if (!clients.size && Date.now() - lastUse > idleMs) void close();}, Math.min(idleMs, 30000));
  await new Promise((ok, fail) => {server.once('error', fail);server.listen(0, '127.0.0.1', ok);});
  return {endpoint:`ws://127.0.0.1:${server.address().port}${socketPath}`, close,
    status:() => ({state,clients:clients.size,owned_tabs:targets.size})};
}

export async function main(argv) {
  const options = {};
  const action = argv.shift();
  for (let i=0;i<argv.length;i+=2) {
    if (!['--root','--browser'].includes(argv[i]) || !argv[i+1]) throw Error('Use start|status|stop --root PATH --browser chrome|edge');
    options[argv[i].slice(2)] = argv[i+1];
  }
  if (!options.root || !['chrome','edge'].includes(options.browser)) throw Error('--root and --browser are required');
  const root = resolve(options.root), browser = options.browser;
  await mkdir(root, {recursive:true});
  const stateFile = join(root, `browser-session-${browser}.json`), lockFile = stateFile + '.lock';
  let previous;try {previous = JSON.parse(await readFile(stateFile,'utf8'));} catch {}
  async function contact(suffix, method = 'GET') {
    if (!previous?.endpoint || !alive(previous.pid)) throw Error('No running browser session; start one session first');
    const url = new URL(previous.endpoint);url.protocol = 'http:';url.pathname += suffix;
    const response = await fetch(url,{method,signal:AbortSignal.timeout(2000)});
    if (!response.ok) throw Error(await response.text());
    return response;
  }
  if (action === 'status') {
    if (!previous || !alive(previous.pid)) {
      if (failed(previous?.state)) throw Error(connectionHelp(browser));
      console.log(JSON.stringify({state:'stopped',browser}));return;
    }
    const status = await (await contact('/status')).json();
    if (failed(status.state)) throw Error(connectionHelp(browser));
    console.log(JSON.stringify({...status,browser}));return;
  }
  if (action === 'endpoint') {
    if (failed(previous?.state)) throw Error(connectionHelp(browser));
    const status = await (await contact('/status')).json();
    if (status.state !== 'connected') throw Error(`Browser session is ${status.state}; wait for user consent instead of opening another connection`);
    if (previous.source_endpoint !== await dailyEndpoint(browser)) throw Error('Selected daily browser restarted; start a new consented session');
    console.log(previous.endpoint);return;
  }
  if (action === 'stop') {
    if (previous && alive(previous.pid)) await contact('/stop','POST');
    console.log(JSON.stringify({state:'stopping',browser}));return;
  }
  if (!['start','serve'].includes(action)) throw Error('Use start, status or stop');
  if (action === 'start') {
    if (previous && alive(previous.pid)) {
      if (previous.source_endpoint !== await dailyEndpoint(browser)) throw Error('Browser changed; stop the old session before starting a new one');
      const status = await (await contact('/status')).json();
      if (failed(status.state)) throw Error(connectionHelp(browser));
      console.log(JSON.stringify({...status,browser,reused:true}));return;
    }
    // Fail before spawning when first-run setup has no endpoint at all.
    try {await dailyEndpoint(browser);} catch (err) {throw Error(`${err.message}. ${connectionHelp(browser)}`);}
    let lock;
    try {lock = await open(lockFile,'wx',0o600);} catch (err) {
      if (err.code === 'EEXIST') throw Error('A session start is already in progress; check status instead of reconnecting');
      throw err;
    }
    try {
      const log = await open(join(root,`browser-session-${browser}.log`),'a',0o600);
      const child = spawn(process.execPath,[process.argv[1],'serve','--root',root,'--browser',browser],
        {detached:true,stdio:['ignore',log.fd,log.fd],windowsHide:true});
      child.unref();await log.close();
      // Do not launch another process in the gap before serve writes its state.
      let firstState = null;
      for (let i=0;i<100;i++) {
        let s;
        try {s=JSON.parse(await readFile(stateFile,'utf8'));} catch {}
        if (s?.pid===child.pid) {
          // The handshake grace below counts from HERE, not from loop entry.
          // Sharing one counter meant a slow spawn spent the window meant for
          // the socket, so an already authorized browser reported
          // waiting_for_consent and sent the user to accept a prompt that was
          // never going to appear.
          if (firstState === null) firstState = i;
          if (failed(s.state) || s.state === 'closed') throw Error(connectionHelp(browser));
          // An already authorized browser commonly opens the socket just
          // after serve writes its first state. Allow that handshake to finish
          // before telling the user that a consent prompt needs attention.
          if (s.state === 'waiting_for_consent' && i - firstState < 20) {
            await new Promise(r=>setTimeout(r,50));
            continue;
          }
          console.log(JSON.stringify({state:s.state,browser,pid:s.pid,reused:false}));return;
        }
        await new Promise(r=>setTimeout(r,50));
      }
      throw Error('Browser session did not start; inspect its local log');
    } finally {await lock.close();await unlink(lockFile);}
  }
  const runtime = JSON.parse(await readFile(join(root,'runtime.json'),'utf8'));
  const {WebSocket,WebSocketServer} = createRequire(runtime.opencli)('ws');
  const source_endpoint = await dailyEndpoint(browser);
  let localEndpoint, writes = Promise.resolve();
  const save = status => {
    writes = writes.then(() => writeFile(stateFile,JSON.stringify({pid:process.pid,browser,
      source_endpoint,endpoint:localEndpoint,...status}),{mode:0o600}));
  };
  save({state:'waiting_for_consent'});
  const session = await createSession({endpoint:source_endpoint,WebSocket,WebSocketServer,changed:save});
  localEndpoint = session.endpoint;save(session.status());
  process.once('SIGTERM',()=>{void session.close();});
  process.once('SIGINT',()=>{void session.close();});
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  main(process.argv.slice(2)).catch(err=>{console.error(err.message);process.exitCode=1;});
}
