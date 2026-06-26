import { createServer as createHttpServer, IncomingMessage, ServerResponse } from "node:http";
import { Socket } from "node:net";
import { randomUUID } from "node:crypto";
import { RawData, WebSocketServer, WebSocket } from "ws";
import { CdpClient } from "./cdp.js";
import { MaskRegion } from "./mask.js";

export type HclConfig = {
  mode: "vnc" | "cdp";
  port: number;
  vncHost?: string;
  vncPort?: number;
  cdpHost?: string;
  cdpPort?: number;
  timeout: number;
  password?: string;
  maskRegions?: MaskRegion[];
};

export type HclServer = {
  onDone: (cb: () => void) => void;
  onFail: (cb: (reason: string) => void) => void;
  onLoginRequired: (cb: (reason: string) => void) => void;
  onTimeout: (cb: (closed: Promise<void>) => void) => void;
  stop: () => Promise<void>;
  setPublicUrl: (url: string) => void;
  getTarget: () => string | null;
};

const HELP_HTML = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>HumanCanHelp</title>
<link rel="icon" href="data:,">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#111;color:#eee;font-family:-apple-system,BlinkMacSystemFont,sans-serif;display:flex;flex-direction:column;height:100vh}
.hdr{background:#1a1a1a;padding:12px 20px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #333;gap:12px;flex-wrap:wrap}
.hdr .logo{font-weight:700;font-size:16px}
.hdr .timer{background:#444;padding:4px 10px;border-radius:4px;font-family:monospace;font-size:13px}
.main{flex:1;display:flex;align-items:center;justify-content:center;padding:16px;overflow:hidden}
.canvas-wrap{position:relative;display:inline-block;max-width:100%;max-height:100%}
.main canvas{border-radius:8px;background:#000;max-width:100%;max-height:100%;display:none}
.mask-layer{position:absolute;inset:0;display:none;pointer-events:none}
.mask-box{position:absolute;background:#000;border:1px solid rgba(255,255,255,0.18)}
.acts{background:#1a1a1a;padding:12px 20px;display:flex;gap:12px;border-top:1px solid #333}
.acts button{flex:1;padding:10px;border:none;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer}
.bd{background:#16a34a;color:#fff}.bd:hover{background:#15803d}
.bl{background:#2563eb;color:#fff}.bl:hover{background:#1d4ed8}
.bf{background:#dc2626;color:#fff}.bf:hover{background:#b91c1c}
.overlay{position:fixed;inset:0;display:none;align-items:center;justify-content:center;z-index:100}
.overlay.show{display:flex}
.pw-box{background:#222;border-radius:12px;padding:32px;width:320px;text-align:center}
.pw-box h2{margin-bottom:8px;font-size:18px}
.pw-box p{font-size:13px;color:#999;margin-bottom:16px}
.pw-box input{width:100%;padding:10px;border:1px solid #444;border-radius:6px;background:#333;color:#eee;font-size:14px;margin-bottom:12px}
.pw-box button{width:100%;padding:10px;background:#2563eb;color:#fff;border:none;border-radius:6px;font-size:14px;cursor:pointer}
.done-box{text-align:center}
.done-box h2{font-size:24px;color:#16a34a;margin-bottom:8px}
.done-box p{color:#999;font-size:14px}
.info{color:#666;font-size:13px}
.connecting{color:#666;font-size:14px}
.expired-msg{color:#f59e0b;font-size:18px;font-weight:600}
</style>
</head>
<body>

<div id="pw" class="overlay">
  <form class="pw-box" onsubmit="checkPw(event)">
    <h2>Password Required</h2>
    <p id="pw-msg">This session is password protected</p>
    <input type="password" id="pwi" placeholder="Enter password" autofocus>
    <button type="submit">Access</button>
  </form>
</div>

<div id="done" class="overlay">
  <div class="done-box">
    <h2 id="done-title">Session Complete</h2>
    <p>You can close this page.</p>
  </div>
</div>

<div class="hdr">
  <span class="logo">HumanCanHelp</span>
  <span class="info" id="inst"></span>
  <span class="info" id="mode-label"></span>
  <span class="timer" id="tmr"></span>
</div>

<div class="main">
  <div class="connecting" id="conn">Connecting to screen...</div>
  <div class="canvas-wrap" id="canvas-wrap">
    <canvas id="cv" tabindex="0"></canvas>
    <div class="mask-layer" id="mask-layer"></div>
  </div>
</div>

<div class="acts">
  <button class="bd" onclick="markDone()">Done - I solved it</button>
  <button class="bl" onclick="markLoginRequired()">Owner action required</button>
  <button class="bf" onclick="markFail()">Cannot solve</button>
</div>

<script>
const cv = document.getElementById('cv');
const ctx = cv.getContext('2d');
const maskLayer = document.getElementById('mask-layer');
let ws = null;
let fbW = 0;
let fbH = 0;
let connected = false;
let mode = 'vnc';
let mouseDown = false;
let maskRegions = [];

function setMaskRegions(regions) {
  maskRegions = Array.isArray(regions) ? regions : [];
  renderMaskRegions();
}

function isMaskedPoint(x, y) {
  return maskRegions.some((region) => x >= region.x && x < region.x + region.w && y >= region.y && y < region.y + region.h);
}

function renderMaskRegions() {
  if (!maskLayer) {
    return;
  }

  maskLayer.innerHTML = '';
  if (!maskRegions.length || !fbW || !fbH) {
    maskLayer.style.display = 'none';
    return;
  }

  maskLayer.style.display = 'block';
  for (const region of maskRegions) {
    const node = document.createElement('div');
    node.className = 'mask-box';
    node.style.left = ((region.x / fbW) * 100) + '%';
    node.style.top = ((region.y / fbH) * 100) + '%';
    node.style.width = ((region.w / fbW) * 100) + '%';
    node.style.height = ((region.h / fbH) * 100) + '%';
    maskLayer.appendChild(node);
  }
}

function getScreenPoint(event) {
  const rect = cv.getBoundingClientRect();
  const scaleX = fbW / rect.width;
  const scaleY = fbH / rect.height;
  return {
    x: Math.floor((event.clientX - rect.left) * scaleX),
    y: Math.floor((event.clientY - rect.top) * scaleY)
  };
}

function showConnected() {
  document.getElementById('conn').style.display = 'none';
  cv.style.display = 'block';
  connected = true;
  renderMaskRegions();
}

function drawDisconnected() {
  if (!connected) return;
  ctx.fillStyle = '#333';
  ctx.fillRect(0, 0, cv.width, cv.height);
  ctx.fillStyle = '#999';
  ctx.font = '16px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('Disconnected', cv.width / 2, cv.height / 2);
}

function showConnectionProblem(message) {
  closeSessionTransport();
  const el = document.getElementById('conn');
  el.style.display = 'block';
  el.className = 'expired-msg';
  el.textContent = message;
  cv.style.display = 'none';
}

function connectVNC() {
  const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
  ws = new WebSocket(proto + '//' + location.host + '/vnc');
  ws.binaryType = 'arraybuffer';

  ws.onopen = () => {
    showConnected();
  };

  ws.onmessage = (event) => {
    const data = event.data;
    if (typeof data === 'string') {
      const msg = JSON.parse(data);
      if (msg.type === 'init') {
        fbW = msg.width;
        fbH = msg.height;
        cv.width = fbW;
        cv.height = fbH;
        renderMaskRegions();
      }
      return;
    }
    handleVncFrame(data);
  };

  ws.onclose = () => {
    if (!connected) {
      showConnectionProblem('Unable to connect to the VNC backend for this session.');
      return;
    }
    drawDisconnected();
  };

  ws.onerror = () => {};
}

function handleVncFrame(buf) {
  const dv = new DataView(buf);
  const msgType = dv.getUint8(0);

  if (msgType !== 0) {
    return;
  }

  const x = dv.getUint16(2);
  const y = dv.getUint16(4);
  const w = dv.getUint16(6);
  const h = dv.getUint16(8);
  const pixelData = new Uint8Array(buf, 12);
  const imgData = ctx.createImageData(w, h);

  for (let i = 0, j = 0; i < pixelData.length && j < imgData.data.length; i += 4, j += 4) {
    imgData.data[j] = pixelData[i + 2];
    imgData.data[j + 1] = pixelData[i + 1];
    imgData.data[j + 2] = pixelData[i];
    imgData.data[j + 3] = 255;
  }

  ctx.putImageData(imgData, x, y);
}

function connectCDP() {
  const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
  ws = new WebSocket(proto + '//' + location.host + '/screen');

  ws.onopen = () => {
    showConnected();
    cv.focus();
  };

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.type === 'init') {
      fbW = msg.width;
      fbH = msg.height;
      cv.width = fbW;
      cv.height = fbH;
      renderMaskRegions();
      return;
    }
    if (msg.type === 'frame') {
      const img = new Image();
      img.onload = () => {
        if (cv.width !== fbW || cv.height !== fbH) {
          cv.width = fbW;
          cv.height = fbH;
        }
        ctx.drawImage(img, 0, 0, fbW, fbH);
      };
      img.src = 'data:image/jpeg;base64,' + msg.data;
    }
  };

  ws.onclose = () => {
    if (!connected) {
      showConnectionProblem('Unable to connect to the browser tab for this session.');
      return;
    }
    drawDisconnected();
  };

  ws.onerror = () => {};
}

function connectScreen() {
  if (mode === 'cdp') {
    connectCDP();
  } else {
    connectVNC();
  }
}

cv.addEventListener('mousedown', (event) => {
  if (!ws || ws.readyState !== 1) return;
  const point = getScreenPoint(event);
  if (isMaskedPoint(point.x, point.y)) return;
  if (mode === 'cdp') {
    mouseDown = true;
    ws.send(JSON.stringify({ type: 'mouseDown', x: point.x, y: point.y }));
    cv.focus();
    return;
  }
  const buf = new ArrayBuffer(6);
  const dv = new DataView(buf);
  dv.setUint8(0, 5);
  dv.setUint8(1, 1);
  dv.setUint16(2, point.x);
  dv.setUint16(4, point.y);
  ws.send(buf);
});

cv.addEventListener('mouseup', (event) => {
  if (!ws || ws.readyState !== 1) return;
  const point = getScreenPoint(event);
  if (isMaskedPoint(point.x, point.y)) return;
  if (mode === 'cdp') {
    mouseDown = false;
    ws.send(JSON.stringify({ type: 'mouseUp', x: point.x, y: point.y }));
    return;
  }
  const buf = new ArrayBuffer(6);
  const dv = new DataView(buf);
  dv.setUint8(0, 5);
  dv.setUint8(1, 0);
  dv.setUint16(2, point.x);
  dv.setUint16(4, point.y);
  ws.send(buf);
});

cv.addEventListener('mousemove', (event) => {
  if (!ws || ws.readyState !== 1 || mode !== 'cdp') return;
  const point = getScreenPoint(event);
  if (isMaskedPoint(point.x, point.y)) return;
  ws.send(JSON.stringify({ type: 'mouseMove', x: point.x, y: point.y, dragging: mouseDown }));
});

cv.addEventListener('mouseleave', () => {
  if (mode === 'cdp') {
    mouseDown = false;
  }
});

document.addEventListener('keydown', (event) => {
  if (!ws || ws.readyState !== 1) return;
  if (mode === 'cdp') {
    ws.send(JSON.stringify({ type: 'keyDown', key: event.key, code: event.code }));
    return;
  }
  const buf = new ArrayBuffer(8);
  const dv = new DataView(buf);
  dv.setUint8(0, 4);
  dv.setUint8(1, 1);
  dv.setUint32(4, event.key.charCodeAt(0));
  ws.send(buf);
});

document.addEventListener('keyup', (event) => {
  if (!ws || ws.readyState !== 1) return;
  if (mode === 'cdp') {
    ws.send(JSON.stringify({ type: 'keyUp', key: event.key, code: event.code }));
    return;
  }
  const buf = new ArrayBuffer(8);
  const dv = new DataView(buf);
  dv.setUint8(0, 4);
  dv.setUint8(1, 0);
  dv.setUint32(4, event.key.charCodeAt(0));
  ws.send(buf);
});

let es = null;

function closeEventStream() {
  if (es) {
    es.close();
    es = null;
  }
}

function closeSessionTransport() {
  closeEventStream();
  if (ws) {
    ws.close();
    ws = null;
  }
}

function connectEvents() {
  closeEventStream();
  es = new EventSource('/api/events');
  es.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.event === 'expired') {
      showExpired();
    }
    if (data.event === 'done') {
      showDoneState('Session Complete');
    }
    if (data.event === 'fail') {
      showDoneState('Session Failed');
    }
    if (data.event === 'login-required') {
      showDoneState('Owner Action Required');
    }
  };
}

function applyStatus(data) {
  mode = data.mode || 'vnc';
  document.getElementById('mode-label').textContent = mode === 'cdp' ? 'CDP mode' : 'VNC mode';
  if (data.instruction) document.getElementById('inst').textContent = data.instruction;
  setMaskRegions(data.maskRegions || []);
  if (data.timeout) startTimer(data.timeout);
}

async function loadStatusAndConnect() {
  const response = await fetch('/api/status');
  if (!response.ok) {
    throw new Error('Failed to load session status');
  }
  const data = await response.json();
  applyStatus(data);
  connectEvents();
  connectScreen();
}

async function checkPw(event) {
  if (event) {
    event.preventDefault();
  }
  const pw = document.getElementById('pwi').value;
  const msg = document.getElementById('pw-msg');
  const response = await fetch('/api/auth', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ password: pw })
  });
  const data = await response.json();
  if (data.ok) {
    msg.textContent = 'Checking session...';
    try {
      await loadStatusAndConnect();
      document.getElementById('pw').classList.remove('show');
      msg.textContent = 'This session is password protected';
    } catch {
      msg.textContent = 'Authenticated, but failed to load the session. Please try again.';
    }
  } else {
    msg.textContent = 'Wrong password. Please try again.';
  }
}

async function markDone() {
  await fetch('/api/done', { method: 'POST' });
  showDoneState('Session Complete');
}

async function markFail() {
  await fetch('/api/fail', { method: 'POST' });
  showDoneState('Session Failed');
}

async function markLoginRequired() {
  await fetch('/api/login-required', { method: 'POST' });
  showDoneState('Owner Action Required');
}

async function bootstrap() {
  try {
    const response = await fetch('/api/status');
    if (!response.ok) {
      throw new Error('Failed to load session status');
    }
    const data = await response.json();
    if (data.password) {
      document.getElementById('pw').classList.add('show');
      document.getElementById('pwi').focus();
    } else {
      applyStatus(data);
      connectEvents();
      connectScreen();
    }
  } catch {
    const el = document.getElementById('conn');
    el.style.display = 'block';
    el.className = 'expired-msg';
    el.textContent = 'Failed to load the session. Refresh to try again.';
  }
}

function showDoneState(title) {
  closeSessionTransport();
  document.getElementById('done-title').textContent = title;
  document.getElementById('done').classList.add('show');
}

function showExpired() {
  closeSessionTransport();
  const el = document.getElementById('conn');
  el.style.display = 'block';
  el.className = 'expired-msg';
  el.textContent = 'This session has expired.';
  cv.style.display = 'none';
  const acts = document.querySelector('.acts');
  if (acts) acts.remove();
}

bootstrap();

function startTimer(seconds) {
  let rem = seconds;
  const el = document.getElementById('tmr');
  const iv = setInterval(() => {
    el.textContent = Math.floor(rem / 60) + ':' + String(rem % 60).padStart(2, '0');
    rem--;
    if (rem < 0) {
      clearInterval(iv);
      showExpired();
    }
  }, 1000);
}

setInterval(async () => {
  try {
    const response = await fetch('/api/status');
    if (!response.ok) {
      return;
    }
    const data = await response.json();
    if (data.status === 'done' || data.status === 'fail' || data.status === 'timeout' || data.status === 'login-required') {
      if (data.status === 'done') {
        showDoneState('Session Complete');
      } else if (data.status === 'login-required') {
        showDoneState('Owner Action Required');
      } else {
        showDoneState('Session Ended');
      }
    }
  } catch {
    // Ignore transient polling failures and wait for the next interval.
  }
}, 3000);
</script>
</body>
</html>`;

type HclStatus = "waiting" | "active" | "done" | "fail" | "timeout" | "login-required";

type CdpWsMessage =
  | { type: "mouseDown"; x: number; y: number }
  | { type: "mouseUp"; x: number; y: number }
  | { type: "mouseMove"; x: number; y: number; dragging?: boolean }
  | { type: "keyDown"; key: string; code: string }
  | { type: "keyUp"; key: string; code: string };

function isObjectRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function isCdpWsMessage(value: unknown): value is CdpWsMessage {
  if (!isObjectRecord(value) || typeof value.type !== "string") {
    return false;
  }

  if (value.type === "mouseDown" || value.type === "mouseUp") {
    return typeof value.x === "number" && typeof value.y === "number";
  }

  if (value.type === "mouseMove") {
    return typeof value.x === "number" && typeof value.y === "number" && (value.dragging === undefined || typeof value.dragging === "boolean");
  }

  if (value.type === "keyDown" || value.type === "keyUp") {
    return typeof value.key === "string" && typeof value.code === "string";
  }

  return false;
}

function keyToText(key: string): string | undefined {
  return key.length === 1 ? key : undefined;
}

function getTokenFromCookie(req: IncomingMessage): string | null {
  const cookieHeader = req.headers.cookie;
  if (!cookieHeader) {
    return null;
  }

  for (const part of cookieHeader.split(";")) {
    const [rawName, ...rawValueParts] = part.trim().split("=");
    if (rawName === "hcl_token") {
      return decodeURIComponent(rawValueParts.join("="));
    }
  }

  return null;
}

export async function createServer(config: HclConfig): Promise<HclServer> {
  let status: HclStatus = "waiting";
  let doneCallback: (() => void) | null = null;
  let failCallback: ((reason: string) => void) | null = null;
  let loginRequiredCallback: ((reason: string) => void) | null = null;
  let timeoutCallback: ((closed: Promise<void>) => void) | null = null;
  let vncSocket: Socket | null = null;
  let publicUrl: string | null = null;
  let cdpTargetUrl: string | null = null;
  const validTokens = new Set<string>();
  const sseClients: ServerResponse[] = [];
  const activeCdpClients = new Set<CdpClient>();
  const activeSockets = new Set<WebSocket>();
  let cleanupPromise: Promise<void> | null = null;

  function isAuthorized(req: IncomingMessage): boolean {
    if (!config.password) {
      return true;
    }

    const headerToken = req.headers["x-hcl-token"];
    if (typeof headerToken === "string" && validTokens.has(headerToken)) {
      return true;
    }

    const cookieToken = getTokenFromCookie(req);
    return cookieToken !== null && validTokens.has(cookieToken);
  }

  function isLocalRequest(req: IncomingMessage): boolean {
    const remote = req.socket.remoteAddress;
    return remote === "127.0.0.1" || remote === "::1" || remote === "::ffff:127.0.0.1";
  }

  function broadcastSSE(event: string, data: Record<string, unknown>) {
    const payload = `data: ${JSON.stringify({ event, ...data })}\n\n`;
    for (const res of sseClients) {
      res.write(payload);
    }
  }

  function cleanup(): Promise<void> {
    if (cleanupPromise) {
      return cleanupPromise;
    }

    if (vncSocket && !vncSocket.destroyed) {
      vncSocket.destroy();
    }

    for (const ws of activeSockets) {
      if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
        ws.close();
      }
    }

    for (const client of activeCdpClients) {
      client.disconnect();
    }

    vncWss.close();
    screenWss.close();
    cleanupPromise = new Promise((resolve) => {
      httpServer.close(() => {
        resolve();
      });
    });
    return cleanupPromise;
  }

  const timeoutTimer = setTimeout(() => {
    status = "timeout";
    broadcastSSE("expired", {});
    const closed = cleanup();
    if (timeoutCallback) timeoutCallback(closed);
  }, config.timeout * 1000);

  const httpServer = createHttpServer((req: IncomingMessage, res: ServerResponse) => {
    if (req.method === "OPTIONS") {
      res.writeHead(200, {
        "Access-Control-Allow-Methods": "GET,POST",
        "Access-Control-Allow-Headers": "Content-Type",
      });
      res.end();
      return;
    }

    const url = new URL(req.url || "/", `http://${req.headers.host}`);

    if (url.pathname === "/" || url.pathname === "/index.html") {
      res.writeHead(200, { "Content-Type": "text/html" });
      res.end(HELP_HTML);
      return;
    }

    if (url.pathname === "/api/status") {
      const canViewFullStatus = !config.password || isAuthorized(req) || isLocalRequest(req);
      res.writeHead(200, { "Content-Type": "application/json" });
      if (!canViewFullStatus) {
        res.end(JSON.stringify({
          password: true,
        }));
        return;
      }
      res.end(JSON.stringify({
        status,
        mode: config.mode,
        password: !!config.password,
        instruction: "Use Login Required only when the real account owner must continue personally; ordinary login steps can still be completed through remote help.",
        timeout: config.timeout,
        publicUrl,
        maskRegions: config.maskRegions ?? [],
      }));
      return;
    }

    if (url.pathname === "/api/events") {
      if (config.password && !isAuthorized(req)) {
        res.writeHead(403, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ ok: false }));
        return;
      }
      res.writeHead(200, {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        Connection: "keep-alive",
      });
      res.write(`data: ${JSON.stringify({ event: "connected" })}\n\n`);
      sseClients.push(res);
      req.on("close", () => {
        const idx = sseClients.indexOf(res);
        if (idx >= 0) {
          sseClients.splice(idx, 1);
        }
      });
      return;
    }

    if (url.pathname === "/api/auth" && req.method === "POST") {
      let body = "";
      req.on("data", (chunk) => {
        body += chunk;
      });
      req.on("end", () => {
        try {
          const data = JSON.parse(body) as { password?: string };
          if (config.password && data.password === config.password) {
            const token = randomUUID();
            validTokens.add(token);
            res.writeHead(200, {
              "Content-Type": "application/json",
              "Set-Cookie": `hcl_token=${encodeURIComponent(token)}; HttpOnly; SameSite=Strict; Path=/`,
            });
            res.end(JSON.stringify({ ok: true }));
          } else {
            res.writeHead(403, { "Content-Type": "application/json" });
            res.end(JSON.stringify({ ok: false }));
          }
        } catch {
          res.writeHead(400, { "Content-Type": "application/json" });
          res.end(JSON.stringify({ ok: false }));
        }
      });
      return;
    }

    if (url.pathname === "/api/done" && req.method === "POST") {
      if (!isAuthorized(req)) {
        res.writeHead(403, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ ok: false }));
        return;
      }
      clearTimeout(timeoutTimer);
      status = "done";
      broadcastSSE("done", {});
      void cleanup();
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ ok: true }));
      if (doneCallback) {
        doneCallback();
      }
      return;
    }

    if (url.pathname === "/api/fail" && req.method === "POST") {
      if (!isAuthorized(req)) {
        res.writeHead(403, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ ok: false }));
        return;
      }
      clearTimeout(timeoutTimer);
      status = "fail";
      broadcastSSE("fail", {});
      void cleanup();
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ ok: true }));
      if (failCallback) {
        failCallback("Helper reported failure");
      }
      return;
    }

    if (url.pathname === "/api/login-required" && req.method === "POST") {
      if (!isAuthorized(req)) {
        res.writeHead(403, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ ok: false }));
        return;
      }
      clearTimeout(timeoutTimer);
      status = "login-required";
      broadcastSSE("login-required", {});
      void cleanup();
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ ok: true }));
      if (loginRequiredCallback) {
        loginRequiredCallback("Helper requested account-owner login or approval");
      }
      return;
    }

    if (url.pathname === "/api/stop" && req.method === "POST") {
      if (!isLocalRequest(req)) {
        res.writeHead(403, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ ok: false }));
        return;
      }
      clearTimeout(timeoutTimer);
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ ok: true }));
      res.once("finish", () => {
        void cleanup();
      });
      return;
    }

    res.writeHead(404);
    res.end("Not found");
  });

  const vncWss = new WebSocketServer({ server: httpServer, path: "/vnc" });
  const screenWss = new WebSocketServer({ server: httpServer, path: "/screen" });

  vncWss.on("connection", (ws: WebSocket, req: IncomingMessage) => {
    activeSockets.add(ws);

    if (config.mode !== "vnc") {
      ws.close(4004, "VNC mode disabled");
      activeSockets.delete(ws);
      return;
    }

    const token = getTokenFromCookie(req);
    if (config.password && (!token || !validTokens.has(token))) {
      ws.close(4001, "Not authenticated");
      activeSockets.delete(ws);
      return;
    }

    status = "active";

    const tcp = new Socket();
    tcp.connect(config.vncPort || 5900, config.vncHost || "localhost", () => {
      vncSocket = tcp;
    });

    tcp.on("data", (data: Buffer) => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(data);
      }
    });

    ws.on("message", (data: Buffer) => {
      if (!tcp.destroyed) {
        tcp.write(data);
      }
    });

    tcp.on("close", () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    });

    ws.on("close", () => {
      activeSockets.delete(ws);
      tcp.destroy();
    });

    tcp.on("error", () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    });
  });

  screenWss.on("connection", async (ws: WebSocket, req: IncomingMessage) => {
    activeSockets.add(ws);

    if (config.mode !== "cdp") {
      ws.close(4004, "CDP mode disabled");
      activeSockets.delete(ws);
      return;
    }

    const token = getTokenFromCookie(req);
    if (config.password && (!token || !validTokens.has(token))) {
      ws.close(4001, "Not authenticated");
      activeSockets.delete(ws);
      return;
    }

    status = "active";

    const cdp = new CdpClient({
      host: config.cdpHost || "localhost",
      port: config.cdpPort || 9222,
    });
    activeCdpClients.add(cdp);

    try {
      await cdp.connect();
      cdpTargetUrl = cdp.getTargetWebSocketUrl();
      ws.send(JSON.stringify({ type: "init", width: 1280, height: 720 }));
      await cdp.startScreencast((data, metadata) => {
        fbSendInit(ws, metadata.deviceWidth, metadata.deviceHeight);
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: "frame", data }));
        }
      });
    } catch {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close(1011, "Failed to connect to CDP target");
      }
      activeCdpClients.delete(cdp);
      cdp.disconnect();
      activeSockets.delete(ws);
      return;
    }

    ws.on("message", async (raw: RawData) => {
      try {
        const parsed = JSON.parse(raw.toString()) as unknown;
        if (!isCdpWsMessage(parsed)) {
          return;
        }

        if (parsed.type === "mouseDown") {
          await cdp.dispatchMouse("mousePressed", parsed.x, parsed.y, "left", 1);
          return;
        }

        if (parsed.type === "mouseUp") {
          await cdp.dispatchMouse("mouseReleased", parsed.x, parsed.y, "left", 0);
          return;
        }

        if (parsed.type === "mouseMove") {
          await cdp.dispatchMouse(
            "mouseMoved",
            parsed.x,
            parsed.y,
            parsed.dragging ? "left" : "none",
            parsed.dragging ? 1 : 0,
          );
          return;
        }

        if (parsed.type === "keyDown") {
          await cdp.dispatchKey("keyDown", parsed.key, parsed.code, keyToText(parsed.key));
          if (keyToText(parsed.key)) {
            await cdp.dispatchKey("char", parsed.key, parsed.code, parsed.key);
          }
          return;
        }

        if (parsed.type === "keyUp") {
          await cdp.dispatchKey("keyUp", parsed.key, parsed.code, keyToText(parsed.key));
        }
      } catch {
        if (ws.readyState === WebSocket.OPEN) {
          ws.close(1003, "Invalid input event");
        }
      }
    });

    ws.on("close", () => {
      activeSockets.delete(ws);
      activeCdpClients.delete(cdp);
      void cdp.stopScreencast().catch(() => {});
      cdp.disconnect();
    });
  });

  function fbSendInit(ws: WebSocket, width: number, height: number) {
    if (width > 0 && height > 0 && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: "init", width, height }));
    }
  }

  return await new Promise((resolve, reject) => {
    httpServer.on("error", reject);
    httpServer.listen(config.port, "0.0.0.0", () => {
      resolve({
        onDone: (cb) => {
          doneCallback = cb;
        },
        onFail: (cb) => {
          failCallback = cb;
        },
        onLoginRequired: (cb) => {
          loginRequiredCallback = cb;
        },
        onTimeout: (cb) => {
          timeoutCallback = cb;
        },
        stop: cleanup,
        setPublicUrl: (url: string) => {
          publicUrl = url;
        },
        getTarget: () => {
          if (config.mode === "cdp") {
            return cdpTargetUrl;
          }
          return `${config.vncHost || "localhost"}:${config.vncPort || 5900}`;
        },
      });
    });
  });
}
