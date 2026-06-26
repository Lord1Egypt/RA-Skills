#!/usr/bin/env node
/**
 * OneBot 11 WebSocket Action 调用工具
 * 通过 napcat 的 WebSocket 接口调用任意 OneBot API
 * 
 * 用法: node onebot-action.js <action> [params...]
 * 
 * 示例:
 *   node onebot-action.js set_group_name group_id=885928377 group_name="新群名"
 *   node onebot-action.js set_group_ban group_id=885928377 user_id=123456 duration=600
 *   node onebot-action.js send_group_notice group_id=885928377 content="公告内容"
 */

const NODE_PATH = '/root/.nvm/versions/node/v24.14.1/lib/node_modules/openclaw/node_modules';
if (!module.paths.includes(NODE_PATH)) module.paths.push(NODE_PATH);

const WS_URL = process.env.ONEBOT_WS_URL || 'ws://127.0.0.1:13001';
const WS_TOKEN = process.env.ONEBOT_WS_TOKEN || 'FTubmd6pc77aX~XK';

function parseArgs(argv) {
  const action = argv[2];
  if (!action) {
    console.error('Usage: node onebot-action.js <action> [key=value ...]');
    console.error('Special: key=@/path/to/file reads file content as value');
    process.exit(1);
  }

  const params = {};
  for (let i = 3; i < argv.length; i++) {
    const arg = argv[i];
    const eqIdx = arg.indexOf('=');
    if (eqIdx === -1) {
      console.error(`Invalid param format: ${arg} (expected key=value)`);
      process.exit(1);
    }
    let key = arg.slice(0, eqIdx).trim();
    let val = arg.slice(eqIdx + 1).trim();
    // Remove surrounding quotes
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    // Read from file: key=@/path/to/file
    if (val.startsWith('@/')) {
      const fs = require('fs');
      val = fs.readFileSync(val.slice(1), 'utf8').trim();
    }
    // Auto-convert numeric values
    if (/^\d+$/.test(val)) val = parseInt(val, 10);
    params[key] = val;
  }

  return { action, params };
}

function callOneBot(action, params) {
  return new Promise((resolve, reject) => {
    const WebSocket = require('ws');
    const echo = `${action}_${Date.now()}`;
    
    const url = WS_TOKEN ? `${WS_URL}?access_token=${encodeURIComponent(WS_TOKEN)}` : WS_URL;
    const ws = new WebSocket(url);
    const timeout = setTimeout(() => {
      ws.close();
      reject(new Error(`Timeout waiting for response to ${action}`));
    }, 15000);

    ws.on('open', () => {
      const payload = { action, params, echo };
      ws.send(JSON.stringify(payload));
    });

    ws.on('message', (data) => {
      try {
        const msg = JSON.parse(data.toString());
        if (msg.echo === echo) {
          clearTimeout(timeout);
          ws.close();
          resolve(msg);
        }
      } catch (e) {
        // ignore parse errors for heartbeats etc.
      }
    });

    ws.on('error', (err) => {
      clearTimeout(timeout);
      reject(err);
    });

    ws.on('close', () => {
      clearTimeout(timeout);
    });
  });
}

async function main() {
  const { action, params } = parseArgs(process.argv);
  
  try {
    const result = await callOneBot(action, params);
    
    if (result.retcode === 0) {
      console.log(JSON.stringify({ ok: true, data: result.data, message: result.msg || 'success' }, null, 2));
    } else {
      console.error(JSON.stringify({ ok: false, retcode: result.retcode, message: result.msg || 'failed' }, null, 2));
      process.exit(1);
    }
  } catch (err) {
    console.error(JSON.stringify({ ok: false, error: err.message }, null, 2));
    process.exit(1);
  }
}

main();
