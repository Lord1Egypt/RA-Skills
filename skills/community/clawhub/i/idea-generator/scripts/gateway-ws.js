#!/usr/bin/env node
/**
 * Gateway WebSocket client — 直接操作 openclaw webchat 对话
 * 用法:
 *   node gateway-ws.js create <sessionKey>            创建新会话
 *   node gateway-ws.js send <sessionKey> <message>    发送消息到会话
 *   node gateway-ws.js abort <sessionKey>             中止会话
 */
const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');

// 读取 gateway 配置
const configPath = path.join(process.env.HOME, '.openclaw/openclaw.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
const port = config.gateway?.port || 18789;
const token = config.gateway?.auth?.token || '';

const action = process.argv[2]; // create | send | abort
const sessionKey = process.argv[3];
const message = process.argv.slice(4).join(' ');

if (!action || !sessionKey) {
  console.error('Usage: node gateway-ws.js <create|send|abort> <sessionKey> [message]');
  process.exit(1);
}

const wsUrl = `ws://127.0.0.1:${port}`;

function run() {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(wsUrl);
    let msgId = 1;
    let authenticated = false;
    let done = false;

    const timeout = setTimeout(() => {
      if (!done) {
        done = true;
        console.error('TIMEOUT');
        ws.close();
        resolve({ ok: false, error: 'timeout' });
      }
    }, 10000);

    function sendMsg(method, params) {
      const id = msgId++;
      const payload = JSON.stringify({ jsonrpc: '2.0', id, method, params });
      ws.send(payload);
      return id;
    }

    ws.on('open', () => {
      // Authenticate
      sendMsg('auth', { token });
    });

    ws.on('message', (data) => {
      let msg;
      try { msg = JSON.parse(data.toString()); } catch { return; }

      // Auth response
      if (msg.result && msg.result.authenticated) {
        authenticated = true;

        if (action === 'create') {
          sendMsg('sessions.create', { key: sessionKey });
        } else if (action === 'send') {
          sendMsg('sessions.send', { key: sessionKey, message });
        } else if (action === 'abort') {
          sendMsg('sessions.abort', { key: sessionKey });
        }
        return;
      }

      // Handle response to our action
      if (msg.id && msg.id >= 2 && !done) {
        done = true;
        clearTimeout(timeout);
        if (msg.error) {
          console.log(JSON.stringify({ ok: false, error: msg.error }));
        } else {
          console.log(JSON.stringify({ ok: true, result: msg.result }));
        }
        ws.close();
        resolve(msg);
      }
    });

    ws.on('error', (err) => {
      if (!done) {
        done = true;
        clearTimeout(timeout);
        console.error('WS_ERROR:', err.message);
        resolve({ ok: false, error: err.message });
      }
    });

    ws.on('close', () => {
      if (!done) {
        done = true;
        clearTimeout(timeout);
        resolve({ ok: false, error: 'connection closed' });
      }
    });
  });
}

run().then(() => process.exit(0)).catch(() => process.exit(1));
