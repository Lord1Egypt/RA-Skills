/**
 * send-telegram.mjs
 * 發送消息到 Telegram
 *
 * 用法：
 *   node send-telegram.mjs "消息文本"
 *   echo "消息文本" | node send-telegram.mjs
 *   node send-telegram.mjs < message.txt
 *
 * 從 .env 讀取 TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { createInterface } from 'readline';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = join(__dirname, '..');

// 讀取 .env
function loadEnv() {
  const envPath = join(PROJECT_ROOT, '.env');
  const env = {};
  try {
    const content = readFileSync(envPath, 'utf-8');
    for (const line of content.split('\n')) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;
      const eqIdx = trimmed.indexOf('=');
      if (eqIdx === -1) continue;
      const key = trimmed.slice(0, eqIdx).trim();
      const value = trimmed.slice(eqIdx + 1).trim().replace(/^["']|["']$/g, '');
      env[key] = value;
    }
  } catch (err) {
    process.stderr.write(`[send-telegram] 讀取 .env 失敗: ${err.message}\n`);
  }
  return env;
}

// 從 stdin 讀取所有輸入
async function readStdin() {
  return new Promise((resolve) => {
    const rl = createInterface({ input: process.stdin });
    const lines = [];
    rl.on('line', (line) => lines.push(line));
    rl.on('close', () => resolve(lines.join('\n')));
    // 如果 stdin 是 TTY（沒有 pipe），馬上 resolve 空字串
    if (process.stdin.isTTY) {
      rl.close();
    }
  });
}

// 發送 Telegram 消息
async function sendMessage(token, chatId, text) {
  const url = `https://api.telegram.org/bot${token}/sendMessage`;
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: chatId,
      text,
      parse_mode: 'Markdown',
    }),
    signal: AbortSignal.timeout(15000),
  });

  const data = await res.json();
  if (!res.ok || !data.ok) {
    throw new Error(data.description || `HTTP ${res.status}`);
  }
  return data;
}

async function main() {
  const env = loadEnv();
  const token = env.TELEGRAM_BOT_TOKEN;
  const chatId = env.TELEGRAM_CHAT_ID;

  if (!token || !chatId) {
    console.error('❌ 失敗: .env 缺少 TELEGRAM_BOT_TOKEN 或 TELEGRAM_CHAT_ID');
    process.exit(1);
  }

  // 優先從命令行參數讀取，否則從 stdin 讀取
  let message = process.argv[2] || '';
  if (!message) {
    message = await readStdin();
  }

  message = message.trim();
  if (!message) {
    console.error('❌ 失敗: 消息內容為空（請通過 argv[2] 或 stdin 提供）');
    process.exit(1);
  }

  try {
    await sendMessage(token, chatId, message);
    console.log('✅ 發送成功');
  } catch (err) {
    console.error(`❌ 失敗: ${err.message}`);
    process.exit(1);
  }
}

main().catch(err => {
  console.error(`❌ 失敗: ${err.message}`);
  process.exit(1);
});
