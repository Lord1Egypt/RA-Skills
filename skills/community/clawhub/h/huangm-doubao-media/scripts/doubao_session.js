#!/usr/bin/env node
const CDP = require('chrome-remote-interface');
const https = require('https');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const SESSION_FILE = path.join(process.env.USERPROFILE, '.doubao_chat_session.json');
const DEFAULT_REQUEST_PATH = '/chat/completion?aid=497858&device_id=7624889309955442216&device_platform=web&language=zh&pc_version=3.13.0&real_aid=497858&samantha_web=1&version_code=20800&web_id=7624889301977761331';
const DEFAULT_BOT_ID = process.env.DOUBAO_BOT_ID || '7338286299411103781';
const LOGIN_URL = 'https://www.doubao.com/';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function sessionExists() {
  return fs.existsSync(SESSION_FILE);
}

function readSession() {
  return JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
}

function writeSession(session) {
  fs.writeFileSync(SESSION_FILE, JSON.stringify(session, null, 2));
}

function getCookieString(session) {
  return (session.cookies || []).map(c => `${c.name}=${c.value}`).join('; ');
}

function openLoginPage() {
  return new Promise((resolve, reject) => {
    exec(`start "" "${LOGIN_URL}"`, { shell: 'cmd.exe' }, error => {
      if (error) return reject(error);
      resolve({ ok: true, url: LOGIN_URL });
    });
  });
}

async function login() {
  const client = await CDP({ port: 18800 });
  const { Network } = client;
  await Network.enable();
  const cookies = await Network.getCookies();
  await client.close();

  const dbCookies = cookies.cookies.filter(c =>
    c.domain.includes('doubao.com') || c.domain.includes('bytedance') || c.domain.includes('douyin.com')
  );

  if (!dbCookies.length) {
    throw new Error('No Doubao cookies found. Please open doubao.com in the logged-in browser first.');
  }

  const session = {
    cookies: dbCookies.map(c => ({ name: c.name, value: c.value })),
    savedAt: new Date().toISOString(),
  };
  writeSession(session);
  return session;
}

function sendProbeRequest(session, message = '你好', requestPath = DEFAULT_REQUEST_PATH, botId = DEFAULT_BOT_ID) {
  const cookieStr = getCookieString(session);
  const localMsgId = 'local_' + Date.now();
  const postData = JSON.stringify({
    client_meta: { local_conversation_id: localMsgId, conversation_id: '', bot_id: botId },
    messages: [{
      local_message_id: localMsgId,
      content_block: [{ block_type: 10000, content: { text_block: { text: message } }, block_id: 'msg_1' }],
      message_status: 0,
    }],
    option: { create_time_ms: Date.now(), is_audio: false },
  });

  const options = {
    hostname: 'www.doubao.com',
    port: 443,
    path: requestPath,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(postData),
      'Cookie': cookieStr,
      'Origin': 'https://www.doubao.com',
      'Referer': 'https://www.doubao.com/chat/',
      'Accept': 'text/event-stream',
    },
  };

  return new Promise((resolve, reject) => {
    let data = '';
    const req = https.request(options, res => {
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => {
        resolve({ statusCode: res.statusCode, body: data, headers: res.headers });
      });
    });
    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

function responseLooksLoggedIn(result) {
  const body = (result?.body || '').toLowerCase();
  if (result?.statusCode !== 200) return false;
  if (body.includes('login') || body.includes('登录') || body.includes('passport')) return false;
  return body.includes('stream_msg_notify') || body.includes('full_msg_notify') || body.includes('event:');
}

async function checkSession({ message = '你好', requestPath = DEFAULT_REQUEST_PATH, botId = DEFAULT_BOT_ID } = {}) {
  if (!sessionExists()) {
    return { ok: false, reason: 'missing-session-file', sessionFile: SESSION_FILE };
  }
  try {
    const session = readSession();
    if (!session.cookies || !session.cookies.length) {
      return { ok: false, reason: 'empty-session', sessionFile: SESSION_FILE };
    }
    const probe = await sendProbeRequest(session, message, requestPath, botId);
    if (responseLooksLoggedIn(probe)) {
      return {
        ok: true,
        reason: 'session-valid',
        sessionFile: SESSION_FILE,
        savedAt: session.savedAt || null,
        cookieCount: session.cookies.length,
        statusCode: probe.statusCode,
      };
    }
    return {
      ok: false,
      reason: 'probe-failed',
      sessionFile: SESSION_FILE,
      savedAt: session.savedAt || null,
      cookieCount: session.cookies.length,
      statusCode: probe.statusCode,
      bodyPreview: String(probe.body || '').slice(0, 300),
    };
  } catch (error) {
    return { ok: false, reason: 'check-error', sessionFile: SESSION_FILE, error: error.message };
  }
}

async function waitForLogin({ timeoutMs = 120000, pollMs = 5000 } = {}) {
  const started = Date.now();
  let lastError = null;

  while (Date.now() - started < timeoutMs) {
    try {
      const session = await login();
      return {
        ok: true,
        reason: 'cookies-captured',
        cookieCount: session.cookies.length,
        waitedMs: Date.now() - started,
      };
    } catch (error) {
      lastError = error;
      await sleep(pollMs);
    }
  }

  return {
    ok: false,
    reason: 'login-timeout',
    waitedMs: Date.now() - started,
    error: lastError ? lastError.message : 'Timed out waiting for login',
  };
}

async function ensureSession(opts = {}) {
  const {
    autoOpen = true,
    waitForManualLogin = true,
    loginTimeoutMs = 120000,
    pollMs = 5000,
  } = opts;

  const checked = await checkSession(opts);
  if (checked.ok) return { ...checked, refreshed: false, openedBrowser: false };

  try {
    const session = await login();
    const rechecked = await checkSession(opts);
    if (!rechecked.ok) throw new Error(`Session refresh failed: ${rechecked.reason}`);
    return {
      ...rechecked,
      refreshed: true,
      openedBrowser: false,
      cookieCount: session.cookies.length,
    };
  } catch (initialError) {
    if (!autoOpen) {
      throw initialError;
    }

    await openLoginPage();

    if (!waitForManualLogin) {
      return {
        ok: false,
        reason: 'login-required-browser-opened',
        openedBrowser: true,
        loginUrl: LOGIN_URL,
        sessionFile: SESSION_FILE,
      };
    }

    const waited = await waitForLogin({ timeoutMs: loginTimeoutMs, pollMs });
    if (!waited.ok) {
      return {
        ok: false,
        reason: waited.reason,
        openedBrowser: true,
        loginUrl: LOGIN_URL,
        sessionFile: SESSION_FILE,
        waitedMs: waited.waitedMs,
        error: waited.error,
      };
    }

    const rechecked = await checkSession(opts);
    if (!rechecked.ok) {
      throw new Error(`Session refresh failed after browser login: ${rechecked.reason}${rechecked.error ? ` (${rechecked.error})` : ''}`);
    }

    return {
      ...rechecked,
      refreshed: true,
      openedBrowser: true,
      loginUrl: LOGIN_URL,
      waitedMs: waited.waitedMs,
    };
  }
}

module.exports = {
  SESSION_FILE,
  DEFAULT_REQUEST_PATH,
  DEFAULT_BOT_ID,
  LOGIN_URL,
  sessionExists,
  readSession,
  writeSession,
  getCookieString,
  openLoginPage,
  login,
  sendProbeRequest,
  checkSession,
  waitForLogin,
  ensureSession,
};
