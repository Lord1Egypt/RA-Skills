#!/usr/bin/env node

/**
 * NeverDie Fallback Monitor — Detects model failures and sends alerts
 *
 * Sends alerts via Telegram Bot API directly (no LLM needed).
 * Also writes to session alert file for in-session visibility.
 * Runs as a standalone systemEvent cron — works even when all LLMs are down.
 *
 * Config: reads from ~/.openclaw/workspace/.neverdie-config.json
 * Fallback: environment variables NEVERDIE_TELEGRAM_TOKEN, NEVERDIE_TELEGRAM_CHAT_ID
 *
 * Usage:
 *   node fallback-monitor.js           # Normal run (scan logs, send alerts)
 *   node fallback-monitor.js --test    # Send a test alert to verify Telegram config
 *   node fallback-monitor.js --status  # Show current monitor state
 *   node fallback-monitor.js --version # Print version
 *
 * Zero npm dependencies — uses only fs, path, https.
 */

const VERSION = '1.2.0';
const fs = require('fs');
const path = require('path');
const https = require('https');

// --- Load config ---
const HOME = process.env.HOME || process.env.USERPROFILE || '/root';
const WORKSPACE = path.join(HOME, '.openclaw/workspace');
const CONFIG_FILE = path.join(WORKSPACE, '.neverdie-config.json');

let config = {
  telegramBotToken: '',
  telegramChatId: '',
  cooldownMinutes: 15,
  timezone: 'UTC',
  hostname: require('os').hostname()
};

if (fs.existsSync(CONFIG_FILE)) {
  try {
    const loaded = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
    config = { ...config, ...loaded };
  } catch (e) {
    log(`Failed to parse config: ${e.message}`);
  }
}

// Environment variable fallback
if (!config.telegramBotToken) {
  config.telegramBotToken = process.env.NEVERDIE_TELEGRAM_TOKEN || '';
}
if (!config.telegramChatId) {
  config.telegramChatId = process.env.NEVERDIE_TELEGRAM_CHAT_ID || '';
}

const COOLDOWN_MS = (config.cooldownMinutes || 15) * 60 * 1000;
const LOG_FILE = path.join(HOME, '.openclaw/logs/gateway.err.log');
const STATE_FILE = path.join(WORKSPACE, '.fallback-monitor-state.json');
const ALERT_FILE = path.join(WORKSPACE, '.fallback-alert-latest.json');
const MONITOR_LOG = path.join(WORKSPACE, 'fallback-monitor.log');

// --- CLI flags ---
const args = process.argv.slice(2);

if (args.includes('--version')) {
  console.log(`neverdie-monitor v${VERSION}`);
  process.exit(0);
}

if (args.includes('--status')) {
  showStatus();
  process.exit(0);
}

if (args.includes('--test')) {
  runTest();
  // runTest calls process.exit internally after async work
} else {
  runMonitor();
}

// --- Main monitor logic ---
function runMonitor() {
  // Load state
  let state = { lastPosition: 0, reported: {}, lastAlertAt: 0 };

  if (fs.existsSync(STATE_FILE)) {
    try {
      state = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
      const now = Date.now();
      for (const [key, ts] of Object.entries(state.reported)) {
        if (now - ts > COOLDOWN_MS) delete state.reported[key];
      }
    } catch (e) {
      state = { lastPosition: 0, reported: {}, lastAlertAt: 0 };
    }
  }

  // Read new log content
  if (!fs.existsSync(LOG_FILE)) {
    log('No gateway.err.log found');
    process.exit(0);
  }

  const stats = fs.statSync(LOG_FILE);
  if (stats.size < state.lastPosition) {
    state.lastPosition = 0; // Log rotation — file got smaller
  }

  const fd = fs.openSync(LOG_FILE, 'r');
  const bufSize = Math.min(stats.size - state.lastPosition, 512 * 1024);
  if (bufSize <= 0) {
    log('No new log content');
    saveState(state);
    process.exit(0);
  }

  const buf = Buffer.alloc(bufSize);
  fs.readSync(fd, buf, 0, bufSize, state.lastPosition);
  fs.closeSync(fd);
  state.lastPosition += bufSize;

  const newContent = buf.toString('utf8');

  // Detect failure patterns
  const alerts = [];
  const now = Date.now();
  const lines = newContent.split('\n');

  for (const line of lines) {
    // All models failed — critical
    if (/All models failed/i.test(line)) {
      const key = 'all-models-failed';
      if (!state.reported[key] || (now - state.reported[key] > COOLDOWN_MS)) {
        alerts.push({
          severity: 'CRITICAL',
          key,
          message: `All models in the fallback chain failed on ${config.hostname}. Check gateway logs for details.`,
          short: 'All models failed — no LLM available'
        });
        state.reported[key] = now;
      }
    }

    // Overloaded
    if (/overloaded/i.test(line) && !/telegram/i.test(line)) {
      const key = 'service-overloaded';
      if (!state.reported[key] || (now - state.reported[key] > COOLDOWN_MS)) {
        alerts.push({
          severity: 'WARNING',
          key,
          message: 'AI service temporarily overloaded. Fallback chain should handle this.',
          short: 'AI service overloaded — using fallbacks'
        });
        state.reported[key] = now;
      }
    }

    // Rate limited
    if (/rate.limit|429/i.test(line) && /FailoverError/i.test(line)) {
      const key = 'rate-limited';
      if (!state.reported[key] || (now - state.reported[key] > COOLDOWN_MS)) {
        alerts.push({
          severity: 'WARNING',
          key,
          message: 'Rate limited on primary model. Falling back to alternatives.',
          short: 'Rate limited — falling back'
        });
        state.reported[key] = now;
      }
    }

    // Auth failures
    if (/authentication_error|invalid.*api.key/i.test(line) && /FailoverError/i.test(line)) {
      const key = 'auth-failure';
      if (!state.reported[key] || (now - state.reported[key] > COOLDOWN_MS)) {
        alerts.push({
          severity: 'CRITICAL',
          key,
          message: `API key authentication failure! Check API keys in openclaw.json on ${config.hostname}`,
          short: 'Auth failure — check API keys'
        });
        state.reported[key] = now;
      }
    }

    // Timeout
    if (/LLM request timed out/i.test(line)) {
      const key = 'llm-timeout';
      if (!state.reported[key] || (now - state.reported[key] > COOLDOWN_MS)) {
        alerts.push({
          severity: 'WARNING',
          key,
          message: 'LLM request timed out. May be transient.',
          short: 'LLM timeout'
        });
        state.reported[key] = now;
      }
    }

    // Connection refused / network errors
    if (/ECONNREFUSED|ECONNRESET|ENOTFOUND|socket hang up/i.test(line)) {
      const key = 'connection-error';
      if (!state.reported[key] || (now - state.reported[key] > COOLDOWN_MS)) {
        alerts.push({
          severity: 'WARNING',
          key,
          message: 'Connection error to model provider. A provider may be unreachable.',
          short: 'Connection error — provider unreachable'
        });
        state.reported[key] = now;
      }
    }
  }

  // Save state
  saveState(state);

  // Send alerts
  if (alerts.length === 0) {
    log('No new alerts');
    process.exit(0);
  }

  log(`Found ${alerts.length} alert(s), sending...`);
  state.lastAlertAt = now;
  saveState(state);

  // Write latest alert to local file (for session pickup — stays on-machine, never sent externally)
  const alertPayload = {
    timestamp: new Date().toISOString(),
    alerts: alerts.map(a => ({ severity: a.severity, message: a.message })),
    acknowledged: false
  };
  fs.writeFileSync(ALERT_FILE, JSON.stringify(alertPayload, null, 2), 'utf8');

  // Send to Telegram (if configured)
  // SECURITY: Only sends the fixed 'short' string (hardcoded alert type) — never log content
  const promises = [];
  if (config.telegramBotToken && config.telegramChatId) {
    for (const alert of alerts) {
      const icon = alert.severity === 'CRITICAL' ? '\u{1F6A8}' : '\u{26A0}\u{FE0F}';
      const text = `${icon} <b>${config.hostname} ${alert.severity}</b>\n\n${alert.short}\n\n<i>${formatTime()}</i>`;
      promises.push(sendTelegram(text));
    }
  } else {
    log('Telegram not configured — alerts written to file only');
  }

  // Print to stdout (visible in session if run as systemEvent)
  for (const alert of alerts) {
    const icon = alert.severity === 'CRITICAL' ? '[!!!]' : '[!]';
    console.log(`${icon} ${alert.severity}: ${alert.short}`);
  }

  if (promises.length > 0) {
    Promise.all(promises).then(() => {
      log('All alerts sent');
      process.exit(0);
    }).catch(err => {
      log(`Alert send error: ${err.message}`);
      process.exit(1);
    });
  } else {
    process.exit(0);
  }
}

// --- Test mode: send a test alert ---
function runTest() {
  console.log(`NeverDie Monitor v${VERSION}`);
  console.log(`Config: ${CONFIG_FILE}`);
  console.log(`Hostname: ${config.hostname}`);
  console.log(`Timezone: ${config.timezone}`);
  console.log(`Cooldown: ${config.cooldownMinutes} min`);
  console.log(`Log file: ${LOG_FILE}`);
  console.log(`Telegram: ${config.telegramBotToken ? 'configured' : 'NOT configured'}`);
  console.log('');

  if (!config.telegramBotToken || !config.telegramChatId) {
    console.log('ERROR: Telegram not configured. Cannot send test alert.');
    console.log('Set telegramBotToken and telegramChatId in:');
    console.log(`  ${CONFIG_FILE}`);
    console.log('Or via environment variables:');
    console.log('  NEVERDIE_TELEGRAM_TOKEN, NEVERDIE_TELEGRAM_CHAT_ID');
    process.exit(1);
  }

  console.log('Sending test alert...');
  const text = `\u{1F6E1}\u{FE0F} <b>${config.hostname} — NeverDie Test</b>\n\nThis is a test alert. If you see this, Telegram alerts are working.\n\n<i>${formatTime()}</i>`;
  sendTelegram(text).then(() => {
    console.log('OK — test alert sent successfully');
    log('Test alert sent OK');
    process.exit(0);
  }).catch(err => {
    console.log(`FAILED — ${err.message}`);
    log(`Test alert failed: ${err.message}`);
    process.exit(1);
  });
}

// --- Status mode: show current state ---
function showStatus() {
  console.log(`NeverDie Monitor v${VERSION}`);
  console.log('');

  // Config
  console.log('=== Config ===');
  if (fs.existsSync(CONFIG_FILE)) {
    console.log(`Hostname: ${config.hostname}`);
    console.log(`Timezone: ${config.timezone}`);
    console.log(`Cooldown: ${config.cooldownMinutes} min`);
    console.log(`Telegram: ${config.telegramBotToken ? 'configured' : 'NOT configured'}`);
  } else {
    console.log(`No config file at ${CONFIG_FILE}`);
  }
  console.log('');

  // State
  console.log('=== Monitor State ===');
  if (fs.existsSync(STATE_FILE)) {
    try {
      const state = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
      console.log(`Log position: ${state.lastPosition} bytes`);
      console.log(`Last alert: ${state.lastAlertAt ? new Date(state.lastAlertAt).toISOString() : 'never'}`);
      const activeReports = Object.entries(state.reported || {});
      if (activeReports.length > 0) {
        console.log(`Active cooldowns: ${activeReports.map(([k, ts]) => `${k} (${Math.round((Date.now() - ts) / 60000)}m ago)`).join(', ')}`);
      } else {
        console.log('Active cooldowns: none');
      }
    } catch (e) {
      console.log(`State file corrupt: ${e.message}`);
    }
  } else {
    console.log('No state file — monitor has not run yet');
  }
  console.log('');

  // Latest alert
  console.log('=== Latest Alert ===');
  if (fs.existsSync(ALERT_FILE)) {
    try {
      const alert = JSON.parse(fs.readFileSync(ALERT_FILE, 'utf8'));
      console.log(`Time: ${alert.timestamp}`);
      console.log(`Acknowledged: ${alert.acknowledged}`);
      for (const a of alert.alerts) {
        console.log(`  [${a.severity}] ${a.message}`);
      }
    } catch (e) {
      console.log(`Alert file corrupt: ${e.message}`);
    }
  } else {
    console.log('No alerts recorded');
  }
  console.log('');

  // Log file
  console.log('=== Gateway Log ===');
  if (fs.existsSync(LOG_FILE)) {
    const stats = fs.statSync(LOG_FILE);
    console.log(`Size: ${(stats.size / 1024).toFixed(1)} KB`);
    console.log(`Modified: ${stats.mtime.toISOString()}`);
  } else {
    console.log('No gateway.err.log found');
  }
}

// --- Helpers ---

function sendTelegram(text) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      chat_id: config.telegramChatId,
      text: text,
      parse_mode: 'HTML'
    });

    const options = {
      hostname: 'api.telegram.org',
      port: 443,
      path: `/bot${config.telegramBotToken}/sendMessage`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data)
      },
      timeout: 10000
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          log('Telegram alert sent OK');
          resolve();
        } else {
          log(`Telegram error ${res.statusCode}: ${body}`);
          reject(new Error(`Telegram HTTP ${res.statusCode}`));
        }
      });
    });

    req.on('error', (e) => {
      log(`Telegram request error: ${e.message}`);
      reject(e);
    });

    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Telegram request timeout'));
    });

    req.write(data);
    req.end();
  });
}

function saveState(state) {
  try {
    fs.writeFileSync(STATE_FILE, JSON.stringify(state), 'utf8');
  } catch (e) {
    // Best effort
  }
}

function formatTime() {
  try {
    return new Date().toLocaleString(undefined, { timeZone: config.timezone, dateStyle: 'medium', timeStyle: 'long' });
  } catch (e) {
    return new Date().toISOString();
  }
}

function log(msg) {
  const ts = new Date().toISOString();
  const line = `[${ts}] [neverdie] ${msg}\n`;
  try {
    fs.appendFileSync(MONITOR_LOG, line);
  } catch (e) {
    // Best effort
  }
}
