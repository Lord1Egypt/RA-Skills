#!/usr/bin/env node
import http from 'node:http';
import { spawn } from 'node:child_process';
import { randomBytes } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import fs from 'node:fs/promises';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const HOST = process.env.HOST || '127.0.0.1';
const PORT = Number.parseInt(process.env.PORT || '0', 10);
const TTL_SECONDS = Math.max(1, Number.parseInt(process.env.TTL_SECONDS || '600', 10));
const TOKEN = process.env.TOKEN || randomBytes(24).toString('hex');
const SYNC_AFTER_UNLOCK = /^(1|true|yes)$/i.test(process.env.SYNC_AFTER_UNLOCK || '0');
const RBW_BIN = process.env.RBW_BIN || 'rbw';
const PINENTRY_PATH = process.env.PINENTRY_PATH || path.join(__dirname, 'pinentry.sh');
const PASSWORD_FIFO = process.env.PASSWORD_FIFO || '/tmp/rbw-remote-unlock-password.fifo';
const RBW_CONFIG_PATH = process.env.RBW_CONFIG_PATH || path.join(
  process.env.XDG_CONFIG_HOME || path.join(process.env.HOME || '', '.config'),
  'rbw',
  'config.json'
);
const READY_PREFIX = 'RBW_REMOTE_UNLOCK_READY ';
const MAX_BODY_BYTES = 16 * 1024;
// Default to a relatively short timeout so retries don't get stuck behind a long-running unlock.
const UNLOCK_TIMEOUT_MS = Math.max(5_000, Number.parseInt(process.env.UNLOCK_TIMEOUT_MS || '30000', 10));
// rbw config file writes should be fast; this timeout guards our own I/O.
const CONFIG_IO_TIMEOUT_MS = Math.max(500, Number.parseInt(process.env.CONFIG_IO_TIMEOUT_MS || '2000', 10));

let busy = false;
let shuttingDown = false;
let ttlTimer;

function htmlEscape(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function send(res, statusCode, body, contentType = 'text/plain; charset=utf-8', extraHeaders = {}) {
  if (res.headersSent) return;
  res.writeHead(statusCode, {
    'Content-Type': contentType,
    'Cache-Control': 'no-store, no-cache, must-revalidate, private, max-age=0',
    Pragma: 'no-cache',
    Expires: '0',
    'Referrer-Policy': 'no-referrer',
    'X-Content-Type-Options': 'nosniff',
    ...extraHeaders,
  });
  res.end(body);
}

function pageTemplate({ title, body }) {
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${htmlEscape(title)}</title>
  <style>
    :root { color-scheme: dark; }
    body { font-family: ui-sans-serif, system-ui, sans-serif; max-width: 32rem; margin: 3rem auto; padding: 0 1rem; background: #0b1020; color: #e5e7eb; }
    h1 { font-size: 1.6rem; margin-bottom: .5rem; }
    p { line-height: 1.5; }
    form { margin-top: 1.25rem; display: grid; gap: .75rem; }
    input[type=password] { font-size: 1rem; padding: .8rem .9rem; border-radius: .65rem; border: 1px solid #334155; background: #111827; color: #f9fafb; }
    button { font-size: 1rem; padding: .85rem 1rem; border: 0; border-radius: .65rem; cursor: pointer; background: #2563eb; color: white; }
    .hint { color: #94a3b8; font-size: .95rem; }
    .message { border-radius: .75rem; padding: .9rem 1rem; margin: 1rem 0; }
    .success { background: rgba(34,197,94,.18); border: 1px solid rgba(34,197,94,.35); }
    .error { background: rgba(239,68,68,.16); border: 1px solid rgba(239,68,68,.35); }
    code { background: rgba(148,163,184,.16); padding: .12rem .35rem; border-radius: .3rem; }
  </style>
</head>
<body>
  ${body}
</body>
</html>`;
}

function unlockFormPage(basePath, errorMessage = '') {
  const message = errorMessage
    ? `<div class="message error"><strong>Unlock failed.</strong><br>${htmlEscape(errorMessage)}</div>`
    : '';
  return pageTemplate({
    title: 'rbw remote unlock',
    body: `
      <h1>Unlock rbw</h1>
      <p class="hint">This short-lived page sends your master password directly to the local unlock helper over HTTPS (if tunneled). The password is kept in memory only and is discarded immediately after the unlock attempt.</p>
      ${message}
      <form method="post" action="${htmlEscape(basePath)}/unlock" autocomplete="off">
        <label>
          <span class="hint">Master password</span>
          <input type="password" name="rbw_password" autofocus required autocomplete="off" autocapitalize="none" autocorrect="off" spellcheck="false" data-bwignore data-1p-ignore>
        </label>
        <button type="submit">Unlock</button>
      </form>
    `,
  });
}

function successPage() {
  return pageTemplate({
    title: 'rbw unlocked',
    body: `
      <h1>rbw unlocked</h1>
      <div class="message success">Vault unlock completed.</div>
      <p class="hint">This helper will finalize and then shut down automatically.</p>
    `,
  });
}

function notFoundPage() {
  return pageTemplate({
    title: 'Not found',
    body: `<h1>Not found</h1><p class="hint">This helper expects the secret token in the URL path.</p>`,
  });
}

function methodNotAllowedPage() {
  return pageTemplate({
    title: 'Method not allowed',
    body: `<h1>Method not allowed</h1>`,
  });
}

function collectRequestBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let total = 0;
    req.on('data', (chunk) => {
      total += chunk.length;
      if (total > MAX_BODY_BYTES) {
        reject(new Error('Request body too large'));
        req.destroy();
        return;
      }
      chunks.push(chunk);
    });
    req.on('end', () => resolve(Buffer.concat(chunks)));
    req.on('error', reject);
  });
}

function parsePassword(req, bodyBuffer) {
  const contentType = (req.headers['content-type'] || '').split(';', 1)[0].trim().toLowerCase();
  const bodyText = bodyBuffer.toString('utf8');
  if (contentType === 'application/json') {
    const parsed = JSON.parse(bodyText || '{}');
    return typeof parsed.password === 'string' ? parsed.password : '';
  }
  const params = new URLSearchParams(bodyText);
  return params.get('rbw_password') || params.get('password') || '';
}

function runCommand(command, args, options = {}) {
  return new Promise((resolve) => {
    const child = spawn(command, args, {
      ...options,
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    let stdout = '';
    let stderr = '';
    let killedForTimeout = false;
    let settled = false;

    const finish = (result) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      resolve({ ...result, stdout, stderr, killedForTimeout });
    };

    const timer = setTimeout(() => {
      killedForTimeout = true;
      child.kill('SIGTERM');
      setTimeout(() => child.kill('SIGKILL'), 3_000).unref();
    }, options.timeoutMs || UNLOCK_TIMEOUT_MS);

    child.stdout.on('data', (chunk) => {
      stdout += chunk.toString('utf8');
    });
    child.stderr.on('data', (chunk) => {
      stderr += chunk.toString('utf8');
    });
    child.on('exit', (code, signal) => {
      finish({ code, signal });
    });
    child.on('error', (error) => {
      finish({ code: null, signal: null, error });
    });
  });
}

function summarizeCommandFailure(result, fallback = 'Command failed') {
  if (result?.error?.message) return result.error.message;
  if (result?.killedForTimeout) return 'Command timed out';
  const candidates = `${result?.stderr || ''}\n${result?.stdout || ''}`
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
  return candidates.at(-1) || fallback;
}

async function withTimeout(promise, ms, label) {
  let t;
  const timeout = new Promise((_, reject) => {
    t = setTimeout(() => reject(new Error(`${label} timed out`)), ms);
  });
  try {
    return await Promise.race([promise, timeout]);
  } finally {
    clearTimeout(t);
  }
}

async function readRbwConfig() {
  const raw = await withTimeout(fs.readFile(RBW_CONFIG_PATH, 'utf8'), CONFIG_IO_TIMEOUT_MS, 'read rbw config');
  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch {
    throw new Error(`Unable to parse rbw config JSON at ${RBW_CONFIG_PATH}`);
  }
  return parsed;
}

async function writeRbwConfig(nextConfig) {
  const dir = path.dirname(RBW_CONFIG_PATH);
  const tmp = path.join(dir, `config.json.tmp.${process.pid}.${Date.now()}`);
  const content = `${JSON.stringify(nextConfig)}\n`;
  await withTimeout(fs.writeFile(tmp, content, { mode: 0o600 }), CONFIG_IO_TIMEOUT_MS, 'write rbw config tmp');
  await withTimeout(fs.rename(tmp, RBW_CONFIG_PATH), CONFIG_IO_TIMEOUT_MS, 'rename rbw config');
}

async function setPinentryInConfig(pinentryValue) {
  const cfg = await readRbwConfig();
  const original = Object.prototype.hasOwnProperty.call(cfg, 'pinentry') ? cfg.pinentry : null;
  cfg.pinentry = pinentryValue;
  await writeRbwConfig(cfg);
  return original;
}

async function restorePinentryInConfig(originalPinentry) {
  const cfg = await readRbwConfig();
  if (originalPinentry === null || originalPinentry === undefined) {
    delete cfg.pinentry;
  } else {
    cfg.pinentry = originalPinentry;
  }
  await writeRbwConfig(cfg);
}

async function attemptUnlock(password) {
  console.error('rbw remote unlock: unlock attempt started');

  await fs.rm(PASSWORD_FIFO, { force: true }).catch(() => {});
  const mkfifoResult = await runCommand('mkfifo', ['-m', '600', PASSWORD_FIFO], {
    env: process.env,
    timeoutMs: 5_000,
  });
  if (mkfifoResult.code !== 0) {
    throw new Error(summarizeCommandFailure(mkfifoResult, 'mkfifo failed'));
  }

  const fifoWriter = spawn('bash', ['-lc', 'for _ in 1 2 3; do printf "%s\\n" "$RBW_REMOTE_UNLOCK_PASSWORD" > "$PASSWORD_FIFO" || break; done'], {
    env: {
      ...process.env,
      RBW_REMOTE_UNLOCK_PASSWORD: password,
      PASSWORD_FIFO,
    },
    stdio: 'ignore',
  });

  try {
    const childEnv = {
      ...process.env,
      PASSWORD_FIFO,
    };
    const unlockResult = await runCommand(RBW_BIN, ['unlock'], { env: childEnv });
    if (unlockResult.code !== 0) {
      const msg = summarizeCommandFailure(unlockResult, 'rbw unlock failed');
      console.error(`rbw remote unlock: unlock attempt failed: ${msg}`);
      throw new Error(msg);
    }
    console.error('rbw remote unlock: unlock attempt succeeded');
  } finally {
    fifoWriter.kill('SIGTERM');
    await fs.rm(PASSWORD_FIFO, { force: true }).catch(() => {});
  }
}

function scheduleShutdown(reason, exitCode = 0) {
  if (shuttingDown) return;
  shuttingDown = true;
  clearTimeout(ttlTimer);
  setTimeout(() => {
    server.close(() => {
      if (reason) {
        console.error(`rbw remote unlock helper exiting: ${reason}`);
      }
      process.exit(exitCode);
    });
  }, 50).unref();
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url || '/', `http://${req.headers.host || `${HOST}:${PORT || 0}`}`);
    const pathname = url.pathname.replace(/\/+$/u, '') || '/';
    const basePath = `/${TOKEN}`;

    if (pathname !== basePath && pathname !== `${basePath}/unlock`) {
      send(res, 404, notFoundPage(), 'text/html; charset=utf-8', {
        'Content-Security-Policy': "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'",
      });
      return;
    }

    if (pathname === basePath) {
      if (req.method !== 'GET' && req.method !== 'HEAD') {
        send(res, 405, methodNotAllowedPage(), 'text/html; charset=utf-8', { Allow: 'GET, HEAD' });
        return;
      }
      if (req.method === 'HEAD') {
        send(res, 200, '', 'text/html; charset=utf-8', {
          'Content-Security-Policy': "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'",
        });
        return;
      }
      send(res, 200, unlockFormPage(basePath), 'text/html; charset=utf-8', {
        'Content-Security-Policy': "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'",
      });
      return;
    }

    if (req.method !== 'POST') {
      send(res, 405, methodNotAllowedPage(), 'text/html; charset=utf-8', { Allow: 'POST' });
      return;
    }

    if (busy) {
      send(res, 409, unlockFormPage(basePath, `An unlock attempt is already in progress. Please wait and try again. (Timeout: ${Math.ceil(UNLOCK_TIMEOUT_MS / 1000)}s)`), 'text/html; charset=utf-8', {
        'Content-Security-Policy': "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'",
        'Retry-After': '2',
      });
      return;
    }

    busy = true;
    let bodyBuffer = Buffer.alloc(0);
    let password = '';
    try {
      bodyBuffer = await collectRequestBody(req);
      password = parsePassword(req, bodyBuffer);
      if (!password) {
        send(res, 400, unlockFormPage(basePath, 'Please enter your master password.'), 'text/html; charset=utf-8', {
          'Content-Security-Policy': "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'",
        });
        return;
      }

      const originalPinentry = await setPinentryInConfig(PINENTRY_PATH);
      let unlockOk = false;
      try {
        await attemptUnlock(password);
        unlockOk = true;
        send(res, 200, successPage(), 'text/html; charset=utf-8', {
          'Content-Security-Policy': "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'",
        });
      } finally {
        // Always restore pinentry after responding.
        res.on('finish', async () => {
          try {
            await restorePinentryInConfig(originalPinentry);
          } catch (e) {
            const msg = e instanceof Error ? e.message : String(e);
            console.error(`rbw remote unlock: pinentry restore failed: ${msg}`);
          }

          if (unlockOk && SYNC_AFTER_UNLOCK) {
            const syncResult = await runCommand(RBW_BIN, ['sync'], { env: process.env });
            if (syncResult.code !== 0) {
              console.error(`rbw remote unlock: sync failed: ${summarizeCommandFailure(syncResult, 'rbw sync failed')}`);
            }
          }

          busy = false;
          if (unlockOk) scheduleShutdown('unlock complete', 0);
        });
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unlock failed';
      send(res, 401, unlockFormPage(basePath, message), 'text/html; charset=utf-8', {
        'Content-Security-Policy': "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'",
      });
      // Best-effort: allow retry quickly.
      res.on('finish', () => {
        busy = false;
      });
    } finally {
      bodyBuffer.fill(0);
      password = '';
    }
  } catch (error) {
    send(res, 500, 'Internal Server Error');
    if (error instanceof Error) {
      console.error(`rbw remote unlock helper error: ${error.message}`);
    }
  }
});

server.on('clientError', (error, socket) => {
  socket.end('HTTP/1.1 400 Bad Request\r\n\r\n');
  if (error instanceof Error) {
    console.error(`rbw remote unlock client error: ${error.message}`);
  }
});

process.on('SIGINT', () => scheduleShutdown('received SIGINT', 0));
process.on('SIGTERM', () => scheduleShutdown('received SIGTERM', 0));

ttlTimer = setTimeout(() => scheduleShutdown(`TTL expired after ${TTL_SECONDS}s`, 0), TTL_SECONDS * 1000);

ttlTimer.unref();
server.listen(PORT, HOST, () => {
  const address = server.address();
  if (!address || typeof address === 'string') {
    console.error('Failed to determine listening address');
    process.exit(1);
    return;
  }
  console.log(`${READY_PREFIX}${JSON.stringify({ host: HOST, port: address.port, token: TOKEN, ttlSeconds: TTL_SECONDS, syncAfterUnlock: SYNC_AFTER_UNLOCK })}`);
});
