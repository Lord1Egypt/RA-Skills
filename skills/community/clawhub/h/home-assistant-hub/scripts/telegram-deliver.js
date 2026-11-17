#!/usr/bin/env node
/**
 * Telegram notification deliverer for Home Assistant Hub
 * 
 * Polls the notifications directory and sends pending alerts to Telegram.
 * Designed to run as a persistent background process.
 * 
 * Usage:
 *   node telegram-deliver.js start   — start the deliverer
 *   node telegram-deliver.js stop    — stop the deliverer
 *   node telegram-deliver.js status  — check status
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const WORKSPACE = process.env.HOME + '/.openclaw/workspace';
const SKILL_DIR = path.join(WORKSPACE, 'skills', 'home-assistant-hub');
const CONFIG_FILE = path.join(SKILL_DIR, 'config', 'hub.json');
const PID_FILE = path.join(SKILL_DIR, 'deliverer.pid');
const NOTIF_DIR = path.join(SKILL_DIR, 'notifications');
const DELIVERED_DIR = path.join(SKILL_DIR, 'delivered');

// ─── Config ───────────────────────────────────────────────────────

function loadConfig() {
  if (!fs.existsSync(CONFIG_FILE)) {
    console.error('[deliverer] No config found at', CONFIG_FILE);
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
}

// ─── PID management ───────────────────────────────────────────────

function isRunning() {
  if (!fs.existsSync(PID_FILE)) return false;
  const pid = parseInt(fs.readFileSync(PID_FILE, 'utf8').trim());
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    fs.unlinkSync(PID_FILE);
    return false;
  }
}

function writePid(pid) {
  fs.writeFileSync(PID_FILE, String(pid));
}

function clearPid() {
  try { fs.unlinkSync(PID_FILE); } catch {}
}

// ─── Telegram API ─────────────────────────────────────────────────

function sendTelegram(text, chatId, botToken) {
  return new Promise((resolve, reject) => {
    const url = `https://api.telegram.org/bot${botToken}/sendMessage`;

    const data = JSON.stringify({
      chat_id: chatId,
      text: text,
      parse_mode: 'HTML',
      disable_web_page_preview: true
    });

    const req = https.request(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data)
      }
    }, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          if (result.ok) resolve(result);
          else reject(new Error(`Telegram error: ${result.description}`));
        } catch {
          reject(new Error(`Telegram response: ${body}`));
        }
      });
    });

    req.on('error', reject);
    req.setTimeout(10000, () => { req.destroy(); reject(new Error('Telegram timeout')); });
    req.write(data);
    req.end();
  });
}

// ─── Echo voice notification (TTS via notify.send_message) ──────────
// ⛔ SAFE-DOMAINS GATE: only calls notify domain, which is already
//    approved in call_safe_domains. Verifies on_demand endpoint auth.

async function sendEchoVoice(config, message) {
  const echoConfig = config.echo_devices || {};
  if (!echoConfig.all_devices_announce_id) {
    return false;
  }

  // Verify on_demand is enabled and ha_token is configured — refuse to call without auth
  if (!config.ha_token) {
    console.error('[deliverer] ⛔ ha_token not set — refusing Echo voice notification (no auth)');
    return false;
  }

  const http = require('http');
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({ device_id: [echoConfig.all_devices_announce_id], message });
    const req = http.request({
      hostname:'127.0.0.1',
      port:9123,
      path:'/call_service?domain=notify&service=send_message',
      method:'POST',
      headers:{
        'Content-Type':'application/json',
        'Content-Length':Buffer.byteLength(payload),
        'Authorization':'Bearer '+config.ha_token
      }
    }, res => {
      let d=''; res.on('data',c=>d+=c); res.on('end',()=>{
        if (res.statusCode === 200) { console.log('[deliverer] 📢 Voice sent to all Echo devices'); resolve(true); }
        else { console.error(`[deliverer] ⚠️ Echo voice failed: ${res.statusCode}`); resolve(false); }
      });
    });
    req.on('error', reject);
    req.write(payload); req.end();
  });
}

// ─── Notification processing ──────────────────────────────────────

async function processNotifications(config) {
  if (!fs.existsSync(NOTIF_DIR)) return;

  const files = fs.readdirSync(NOTIF_DIR)
    .filter(f => f.endsWith('.json'))
    .sort();

  if (files.length === 0) return;

  // Get Telegram config from hub config — NO hardcoded fallbacks
  const botToken = config.telegram_bot_token;
  const chatId = config.telegram_chat_id;

  if (!botToken) {
    console.error('[deliverer] ⛔ telegram_bot_token not set in hub.json — refusing to send (no fallback)');
    return; // skip notifications, don't send with missing token
  }
  if (!chatId) {
    console.warn('[deliverer] ⚠️ telegram_chat_id not set in hub.json — skipping delivery until configured');
    return;
  }

  let sent = 0;
  for (const file of files) {
    try {
      const notif = JSON.parse(fs.readFileSync(path.join(NOTIF_DIR, file), 'utf8'));
      
      // Move to delivered
      const deliveredPath = path.join(DELIVERED_DIR, file);
      fs.renameSync(path.join(NOTIF_DIR, file), deliveredPath);
      
      // Send to Telegram
      await sendTelegram(notif.text || 'New notification from Home Assistant', chatId, botToken);
      console.log(`[deliverer] Sent: ${notif.text}`);
      sent++;
      
      // Optionally also send voice notification on Echo (if configured)
      if (config.tts_echo) {
        try { await sendEchoVoice(config, notif.text || 'New notification'); } catch(e) {}
      }
    } catch (e) {
      console.error(`[deliverer] Error processing ${file}: ${e.message}`);
    }
  }

  if (sent > 0) {
    console.log(`[deliverer] ${sent} notification(s) delivered`);
  }
}

// ─── Main ─────────────────────────────────────────────────────────

async function main() {
  const cmd = process.argv[2];

  switch (cmd) {
    case 'start': {
      if (isRunning()) {
        console.log('[deliverer] Already running');
        process.exit(0);
      }

      const config = loadConfig();
      writePid(process.pid);

      // Ensure Telegram config exists — NO hardcoded fallbacks
      if (!config.telegram_bot_token) {
        console.warn('[deliverer] ⚠️ telegram_bot_token not set in hub.json — deliverer will refuse to send');
      }
      if (!config.telegram_chat_id) {
        console.warn('[deliverer] ⚠️ telegram_chat_id not set in hub.json — delivery skipped until configured');
      }

      console.log('[deliverer] Starting...');
      console.log(`[deliverer] Polling notifications every 30s`);
      console.log(`[deliverer] PID: ${process.pid}`);

      // Ensure directories exist
      if (!fs.existsSync(NOTIF_DIR)) fs.mkdirSync(NOTIF_DIR, { recursive: true });
      if (!fs.existsSync(DELIVERED_DIR)) fs.mkdirSync(DELIVERED_DIR, { recursive: true });

      // Main loop
      const loop = async () => {
        try {
          await processNotifications(config);
        } catch (e) {
          console.error(`[deliverer] Error: ${e.message}`);
        }
        setTimeout(loop, 30000); // 30 seconds
      };
      loop();

      // Graceful shutdown
      process.on('SIGTERM', () => { clearPid(); process.exit(0); });
      process.on('SIGINT', () => { clearPid(); process.exit(0); });
      break;
    }

    case 'stop': {
      if (!isRunning()) {
        console.log('[deliverer] Not running');
        process.exit(0);
      }
      const pid = parseInt(fs.readFileSync(PID_FILE, 'utf8').trim());
      process.kill(pid, 'SIGTERM');
      clearPid();
      console.log(`[deliverer] Stopped (PID: ${pid})`);
      break;
    }

    case 'status': {
      if (isRunning()) {
        console.log('[deliverer] Running');
      } else {
        console.log('[deliverer] Stopped');
      }
      if (fs.existsSync(NOTIF_DIR)) {
        const pending = fs.readdirSync(NOTIF_DIR).filter(f => f.endsWith('.json')).length;
        console.log(`[deliverer] Pending notifications: ${pending}`);
      }
      break;
    }

    default:
      console.log(`Home Assistant Telegram Deliverer\n`);
      console.log('Usage:');
      console.log('  node telegram-deliver.js start   — start the deliverer');
      console.log('  node telegram-deliver.js stop    — stop the deliverer');
      console.log('  node telegram-deliver.js status  — check status');
      break;
  }
}

main().catch(err => {
  console.error(`[deliverer] Fatal: ${err.message}`);
  process.exit(1);
});