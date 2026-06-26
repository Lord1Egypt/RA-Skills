#!/usr/bin/env node
/**
 * 豆包聊天API - 带 session 检测/自动刷新
 */

const https = require('https');
const {
  DEFAULT_BOT_ID,
  DEFAULT_REQUEST_PATH,
  readSession,
  getCookieString,
  login,
  checkSession,
  ensureSession,
} = require('./doubao_session');

async function parseReplyFromSse(data) {
  let reply = '';
  const events = data.split('\n\n');

  for (const rawEvent of events) {
    const lines = rawEvent.split('\n').map(line => line.trim()).filter(Boolean);
    const eventLine = lines.find(line => line.startsWith('event:'));
    const dataLine = lines.find(line => line.startsWith('data:'));
    if (!eventLine || !dataLine) continue;

    const eventName = eventLine.replace(/^event:\s*/, '');
    if (eventName !== 'STREAM_MSG_NOTIFY' && eventName !== 'FULL_MSG_NOTIFY') continue;

    try {
      const json = JSON.parse(dataLine.replace(/^data:\s*/, ''));
      const isAssistantMessage = eventName === 'STREAM_MSG_NOTIFY' || json?.message?.user_type === 2;
      if (!isAssistantMessage) continue;

      const blocks =
        json?.content?.content_block ||
        json?.message?.content_block ||
        json?.data?.content?.content_block ||
        [];

      for (const block of blocks) {
        const text = block?.content?.text_block?.text;
        if (text) reply += text;
      }
    } catch {}
  }

  return reply;
}

async function chat(message, opts = {}) {
  if (opts.ensure !== false) {
    await ensureSession({ message: '你好', requestPath: DEFAULT_REQUEST_PATH, botId: DEFAULT_BOT_ID });
  }

  const session = readSession();
  const cookieStr = getCookieString(session);
  const localMsgId = 'local_' + Date.now();
  const postData = JSON.stringify({
    client_meta: { local_conversation_id: localMsgId, conversation_id: '', bot_id: DEFAULT_BOT_ID },
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
    path: DEFAULT_REQUEST_PATH,
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
      res.on('end', async () => {
        try {
          const reply = await parseReplyFromSse(data);
          console.log(`\n🤖 ${reply || '(无回复)'}`);
          resolve(reply);
        } catch (error) {
          reject(error);
        }
      });
    });
    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

function getFlagValue(args, flag, fallback) {
  const idx = args.indexOf(flag);
  if (idx === -1) return fallback;
  const next = args[idx + 1];
  return next == null ? fallback : next;
}

async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];
  const loginTimeoutMs = Number(getFlagValue(args, '--timeout-ms', '120000')) || 120000;
  const waitForManualLogin = !args.includes('--no-wait-login');
  const autoOpen = !args.includes('--no-open-browser');

  if (cmd === 'login') {
    const session = await login();
    console.log(JSON.stringify({ ok: true, action: 'login', cookieCount: session.cookies.length }, null, 2));
  } else if (cmd === 'check-session') {
    const result = await checkSession();
    console.log(JSON.stringify(result, null, 2));
    process.exit(result.ok ? 0 : 1);
  } else if (cmd === 'login-if-needed') {
    const result = await ensureSession({ autoOpen, waitForManualLogin, loginTimeoutMs });
    console.log(JSON.stringify(result, null, 2));
    process.exit(result.ok ? 0 : 1);
  } else if (cmd === 'ready') {
    const result = await ensureSession({ autoOpen, waitForManualLogin, loginTimeoutMs });
    const summary = {
      ok: !!result.ok,
      status: result.ok ? 'available' : 'unavailable',
      sessionFile: result.sessionFile,
      refreshed: !!result.refreshed,
      openedBrowser: !!result.openedBrowser,
      cookieCount: result.cookieCount || 0,
      reason: result.reason || null,
      loginUrl: result.loginUrl || null,
      waitedMs: result.waitedMs || 0,
    };
    console.log(JSON.stringify(summary, null, 2));
    process.exit(summary.ok ? 0 : 1);
  } else if (cmd === 'chat') {
    await chat(args.slice(1).join(' '));
  } else if (cmd === 'test') {
    await chat('hi');
  } else {
    console.log('Usage: node doubao_api.js login | check-session | login-if-needed [--timeout-ms 120000] [--no-wait-login] [--no-open-browser] | ready [--timeout-ms 120000] [--no-wait-login] [--no-open-browser] | chat "msg" | test');
  }
}

main().catch(error => {
  console.error(error.message);
  process.exit(1);
});
