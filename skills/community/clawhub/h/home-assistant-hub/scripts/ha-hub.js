#!/usr/bin/env node
/**
 * Home Assistant WebSocket Hub
 * 
 * Connects to HA via WebSocket, subscribes to state changes,
 * evaluates alert rules, and writes notifications for OpenClaw.
 *
 * Usage:
 *   node ha-hub.js start      — start the hub
 *   node ha-hub.js stop       — stop the hub
 *   node ha-hub.js status     — check status
 *   node ha-hub.js test       — test connection
 *   node ha-cmd.js rules      — list rules
 *   node ha-cmd.js add-rule   — add a new alert rule
 */

const fs = require('fs');
const path = require('path');
const http = require('http');

const WORKSPACE = process.env.HOME + '/.openclaw/workspace';
const SKILL_DIR = path.join(WORKSPACE, 'skills', 'home-assistant-hub');
const CONFIG_DIR = path.join(SKILL_DIR, 'config');
const CONFIG_FILE = path.join(CONFIG_DIR, 'hub.json');
const PID_FILE = path.join(SKILL_DIR, 'hub.pid');
const LOG_DIR = path.join(SKILL_DIR, 'logs');
const MAX_LOG_LINES = 5000;
const MAX_DELIVERED_FILES = 100;

// ─── Config loader ────────────────────────────────────────────────

function loadConfig() {
  const defaults = {
    ha_url: 'http://homeassistant.local:8123',
    ha_token: '',
    poll_interval: 10,           // seconds between polls
    rules: [],
    notification_channel: 'telegram',
    quiet_hours: { enabled: false, start: '23:00', end: '07:00' },
    on_demand: {
      enabled: true,
      port: 9123                 // local API port for ha-cmd.js
    },
    echo_devices: {
      all_devices_announce_id: '',   // device_id per tutti gli Echo (annunci)
      echo_pop_device_id: '',        // Echo Pop individuale — usare entity notify Parla
      echo_show_device_id: ''        // Echo Show individuale — usare entity notify Parla
    }
  };

  if (!fs.existsSync(CONFIG_FILE)) {
    if (!fs.existsSync(CONFIG_DIR)) fs.mkdirSync(CONFIG_DIR, { recursive: true });
    fs.writeFileSync(CONFIG_FILE, JSON.stringify(defaults, null, 2));
    return { ...defaults };
  }

  const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
  for (const key of Object.keys(defaults)) {
    if (!(key in config)) config[key] = defaults[key];
  }
  return config;
}

function saveConfig(config) {
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
}

// ─── TTS via notify.send_message (removed — use ha-cmd.js call instead) ──────────
// Voice notifications should be sent directly:
//   node scripts/ha-cmd.js call notify.send_message entity_id="notify.echo_show_5_parla,notify.echo_pop_di_vincenzo_parla" message="Test"
// The old sendEchoVoice function passed entity_id as a JS array which may not trigger HA automations properly.


// ─── Logging with rotation ───────────────────────────────────────

let logStream = null;

function initLogging() {
  if (!fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR, { recursive: true });
  const dateStr = new Date().toISOString().slice(0,10);
  const logFile = path.join(LOG_DIR, `hub-${dateStr}.log`);
  
  // Clean old logs
  try {
    fs.readdirSync(LOG_DIR).forEach(f => {
      if (f.startsWith('hub-') && f !== `hub-${dateStr}.log`) {
        const parts = f.match(/hub-(\d{4}-\d{2}-\d{2})\.log/);
        if (parts) {
          const logDate = new Date(parts[1]);
          const thirtyDaysAgo = new Date(Date.now() - 30*86400000);
          if (logDate < thirtyDaysAgo) fs.unlinkSync(path.join(LOG_DIR, f));
        }
      }
    });
  } catch {}
  
  logStream = fs.createWriteStream(logFile, { flags: 'a' });
}

function log(level, msg) {
  const timestamp = new Date().toISOString();
  const line = `[${timestamp}] ${level.toUpperCase()}: ${msg}\n`;
  
  if (logStream) logStream.write(line);
  console.log(line.trim());
}

function rotateLogs(maxLines, logDir) {
  try {
    fs.readdirSync(logDir).forEach(f => {
      const fullPath = path.join(logDir, f);
      const lines = fs.readFileSync(fullPath, 'utf8').split('\n');
      if (lines.length > maxLines) {
        const recent = lines.slice(-maxLines).join('\n');
        fs.writeFileSync(fullPath, recent + '\n');
      }
    });
  } catch {}
}

// ─── HA WebSocket Connection ─────────────────────────────────────
let wsClient = null;
let isConnected = false;
const stateListeners = new Set();

async function connectHA(config) {
  const haUrl = config.ha_url.replace('http', 'ws');
  const wsPath = `${haUrl}/api/websocket`;
  
  log('info', `Connecting to HA at ${wsPath}`);
  
  return new Promise((resolve, reject) => {
    try {
      // Node.js native WebSocket (v24+)
      const ws = new WebSocket(wsPath);
      
      ws.onopen = () => log('info', 'WebSocket connected');
      ws.onerror = (err) => log('error', `WS error: ${err.message || err}`);
      ws.onclose = () => {
        isConnected = false;
        log('warn', 'WebSocket disconnected — polling fallback active');
      };

      ws.onmessage = async (event) => {
        try {
          const msg = JSON.parse(event.data);
          
          // Authentication required
          if (msg.type === 'auth_required') {
            ws.send(JSON.stringify({
              id: 1,
              type: 'auth',
              access_token: config.ha_token
            }));
            return;
          }
          
          if (msg.type === 'auth_ok') {
            isConnected = true;
            log('info', 'Authentication successful');
            
            // Subscribe to state changes
            ws.send(JSON.stringify({ id: 2, type: 'subscribe_entities' }));
            resolve();
          }
          
          if (msg.type === 'event') {
            const entityState = msg.event.data;
            for (const listener of stateListeners) {
              try { listener(entityState); } catch {}
            }
          }
        } catch (e) {
          log('error', `WS message parse error: ${e.message}`);
        }
      };

      wsClient = ws;
    } catch (e) {
      reject(e);
    }
  });
}

function subscribeToStates(listener) {
  stateListeners.add(listener);
  return () => stateListeners.delete(listener);
}

// ─── HA REST API via fetch ──────────────────────────────────────
async function haFetch(endpoint, token, baseUrl, method = 'GET', body = null) {
  const url = `${baseUrl}${endpoint}`;
  
  // Convert relative paths to absolute
  const fullUrl = endpoint.startsWith('/') ? url : `${url}/${endpoint}`;
  
  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };
  
  const options = { method, headers };
  if (body) options.body = JSON.stringify(body);
  
  try {
    const response = await fetch(fullUrl, options);
    
    if (!response.ok) {
      throw new Error(`HA API error ${response.status}: ${response.statusText}`);
    }
    
    // Some HA endpoints return empty body (e.g., service calls)
    const text = await response.text();
    return text ? JSON.parse(text) : {};
  } catch (e) {
    throw new Error(`HA fetch failed: ${e.message}`);
  }
}

// ─── Polling Fallback for State Changes ──────────────────────────
let pollTimer = null;
const previousStates = new Map(); // entity_id -> last known state

async function startPolling(config) {
  const interval = config.poll_interval || 10; // seconds
  log('info', `Starting polling every ${interval}s`);
  
  pollTimer = setInterval(async () => {
    try {
      const states = await haFetch(
        '/api/states',
        config.ha_token,
        config.ha_url
      );
      
      // Check for changes against previous state
      for (const entity of states) {
        const entityId = entity.entity_id;
        const currentState = JSON.stringify(entity);
        const prevState = previousStates.get(entityId);
        
        if (prevState !== currentState) {
          // State changed — check rules
          await evaluateRules(config, entity);
          previousStates.set(entityId, currentState);
        }
      }
    } catch (e) {
      log('error', `Polling failed: ${e.message}`);
    }
  }, interval * 1000);
}

function stopPolling() {
  if (pollTimer) {
    clearInterval(pollTimer);
    pollTimer = null;
    log('info', 'Polling stopped');
  }
}

// ─── Rule Evaluation ─────────────────────────────────────────────
const ruleCooldowns = new Map(); // entity_id -> last trigger timestamp

async function evaluateRules(config, entityState) {
  const { rules } = config;
  if (!rules || !Array.isArray(rules)) return;
  
  for (const rule of rules) {
    if (rule.entity_id !== entityState.entity_id) continue;
    
    // Check cooldown
    const lastTrigger = ruleCooldowns.get(rule.entity_id) || 0;
    if (Date.now() - lastTrigger < (rule.cooldown || 300) * 1000) {
      continue; // Still in cooldown period
    }
    
    // Evaluate condition
    const shouldTrigger = evaluateCondition(entityState, rule);
    if (!shouldTrigger) continue;
    
    // Check quiet hours
    if (isQuietHours(config)) {
      log('info', `Rule "${rule.name}" suppressed by quiet hours`);
      continue;
    }
    
    // Trigger notification
    const title = rule.title || 'Alert';
    let message = rule.template || `${title}: ${entityState.state}`;
    
    // Template substitution: replace {{state}} with actual state value
    if (rule.template) {
      message = message.replace(/\{\{(\w+)\}\}/g, (_, key) => {
        const val = entityState[key] !== undefined ? entityState[key] : entityState.state;
        return String(val);
      });
    }
    
    // Write notification
    await writeNotification(config, {
      title,
      message,
      source: rule.name,
      entity_id: rule.entity_id,
      state: entityState.state,
      timestamp: new Date().toISOString()
    });
    
    ruleCooldowns.set(rule.entity_id, Date.now());
    log('info', `Rule "${rule.name}" triggered: ${message}`);
    // TTS via sendEchoVoice removed — use ha-cmd.js call notify.send_message for voice notifications
  }
}

function evaluateCondition(entityState, rule) {
  const state = entityState.state;
  const numericState = parseFloat(state);
  
  switch (rule.condition) {
    case 'state':
      return state === String(rule.value);
    case 'not_state':
      return state !== String(rule.value);
    case 'above':
      return !isNaN(numericState) && numericState > Number(rule.value);
    case 'below':
      return !isNaN(numericState) && numericState < Number(rule.value);
    case 'changed':
      return true;
    default:
      log('warn', `Unknown condition: ${rule.condition}`);
      return false;
  }
}

// ─── Notification Delivery ───────────────────────────────────────
const NOTIFICATION_DIR = path.join(SKILL_DIR, 'notifications');

async function writeNotification(config, notification) {
  if (!fs.existsSync(NOTIFICATION_DIR)) fs.mkdirSync(NOTIFICATION_DIR, { recursive: true });
  
  const filename = `notif-${Date.now()}.json`;
  fs.writeFileSync(
    path.join(NOTIFICATION_DIR, filename),
    JSON.stringify(notification, null, 2)
  );
}

async function cleanupDelivered(maxFiles) {
  try {
    const deliveredDir = path.join(SKILL_DIR, 'delivered');
    if (!fs.existsSync(deliveredDir)) return;
    
    const files = fs.readdirSync(deliveredDir).sort();
    while (files.length > maxFiles) {
      fs.unlinkSync(path.join(deliveredDir, files.shift()));
    }
  } catch {}
}

// ─── Quiet Hours Check ──────────────────────────────────────────
function isQuietHours(config) {
  const { quiet_hours } = config;
  if (!quiet_hours || !quiet_hours.enabled) return false;
  
  const now = new Date();
  const currentMinutes = now.getHours() * 60 + now.getMinutes();
  const [startHour, startMin] = quiet_hours.start.split(':').map(Number);
  const [endHour, endMin] = quiet_hours.end.split(':').map(Number);
  
  const startMinutes = startHour * 60 + startMin;
  const endMinutes = endHour * 60 + endMin;
  
  // Handle overnight ranges (e.g., 23:00 to 07:00)
  if (startMinutes > endMinutes) {
    return currentMinutes >= startMinutes || currentMinutes < endMinutes;
  }
  
  return currentMinutes >= startMinutes && currentMinutes < endMinutes;
}

// ─── Daemon Management ──────────────────────────────────────────
function writePID() {
  fs.writeFileSync(PID_FILE, process.pid.toString());
}

function readPID() {
  try { return parseInt(fs.readFileSync(PID_FILE, 'utf8')); } catch { return null; }
}

function killProcess(pid) {
  try { process.kill(pid); log('info', `Killed daemon with PID ${pid}`); } catch {}
}

// ─── CLI Commands ────────────────────────────────────────────────
async function handleCommand(config, command, args) {
  switch (command) {
    case 'start': {
      const existing = readPID();
      if (existing && !isProcessDead(existing)) {
        log('warn', `Already running with PID ${existing}`);
        return;
      }
      writePID();
      initLogging();
      
      // Try WebSocket first, fall back to polling
      try {
        await connectHA(config);
        subscribeToStates(async (entityState) => {
          await evaluateRules(config, entityState);
        });
        log('info', 'Hub started with WebSocket');
      } catch (e) {
        log('warn', `WS connection failed: ${e.message}. Falling back to polling.`);
        // Initialize previous states for delta detection
        const initialStates = await haFetch(
          '/api/states',
          config.ha_token,
          config.ha_url
        );
        for (const entity of initialStates) {
          previousStates.set(entity.entity_id, JSON.stringify(entity));
        }
        startPolling(config);
      }
      
      // Handle graceful shutdown
      process.on('SIGINT', () => handleShutdown());
      process.on('SIGTERM', () => handleShutdown());
      break;
    }
    
    case 'stop': {
      const pid = readPID();
      if (pid) killProcess(pid);
      else log('info', 'No PID file found');
      break;
    }
    
    case 'status': {
      const pid = readPID();
      const running = pid ? isProcessDead(pid) : false;
      console.log(`\n=== Home Assistant Hub Status ===`);
      console.log(`Status: ${running ? '✅ Running' : '❌ Stopped'} (PID: ${pid || 'none'})`);
      console.log(`HA URL: ${config.ha_url}`);
      console.log(`Poll interval: ${config.poll_interval}s`);
      
      // Show recent logs
      const logDir = path.join(SKILL_DIR, 'logs');
      if (fs.existsSync(logDir)) {
        const files = fs.readdirSync(logDir).sort().reverse();
        if (files.length > 0) {
          console.log(`\nRecent log lines:`);
          try {
            const recentLines = fs.readFileSync(path.join(logDir, files[0]), 'utf8').split('\n');
            const tail = recentLines.slice(-10).join('\n');
            if (tail.trim()) console.log(tail);
          } catch {}
        }
      }
      break;
    }
    
    case 'test': {
      try {
        await haFetch('/api/', config.ha_token, config.ha_url);
        log('info', '✅ HA connection successful');
        // List entities count
        const states = await haFetch('/api/states', config.ha_token, config.ha_url);
        console.log(`Entities found: ${states.length}`);
      } catch (e) {
        log('error', `❌ HA connection failed: ${e.message}`);
      }
      break;
    }
    
    case 'add-rule':
    case 'ar': {
      await addRuleInteractive(config);
      saveConfig(config);
      break;
    }
    
    case 'add-rules':
    case 'arr': {
      // Read JSON from stdin
      const input = process.stdin.read();
      if (!input) {
        console.error('Usage: node ha-hub.js add-rules < rules.json');
        break;
      }
      try {
        const newRules = JSON.parse(input.toString());
        if (!Array.isArray(newRules)) throw new Error('Input must be a JSON array');
        
        config.rules = [...(config.rules || []), ...newRules];
        saveConfig(config);
        log('info', `Added ${newRules.length} rules`);
      } catch (e) {
        log('error', `Error adding rules: ${e.message}`);
      }
      break;
    }
    
    case 'rules':
    case 'rls': {
      if (!config.rules || config.rules.length === 0) {
        console.log('No alert rules configured.');
      } else {
        console.log(`\n=== Alert Rules (${config.rules.length}) ===`);
        config.rules.forEach((rule, i) => {
          const cooldown = rule.cooldown ? `${rule.cooldown}s` : '300s';
          console.log(`${i+1}. ${rule.name} — ${cooldown} cooldown`);
        });
      }
      break;
    }
    
    case 'tts': {
      console.error('[hub] ⚠️ TTS command removed — use ha-cmd.js call instead');
      console.error('Usage: node scripts/ha-cmd.js call notify.send_message entity_id="notify.echo_show_5_parla,notify.echo_pop_di_vincenzo_parla" message="Your message"');
      break;
    }
    
    case 'setup': {
      log('info', 'Run the setup script: node ha-cmd.js setup');
      console.log('Use: cd scripts && node ha-hub.js setup');
      break;
    }
    
    default:
      console.log(`Unknown command: ${command}`);
      console.log('Available commands: start, stop, status, test, add-rule, add-rules, rules, setup');
  }
}

async function addRuleInteractive(config) {
  const readline = require('readline').createInterface({ input: process.stdin });
  
  console.log('\n=== Add Alert Rule ===\n');
  
  const name = await ask(readline, 'Rule name:', 'My Rule');
  const entity_id = await ask(readline, 'HA Entity ID (e.g., binary_sensor.motion):', '');
  const condition = await ask(readline, 'Condition (state|not_state|above|below|changed):', 'state');
  const value = await ask(readline, `Value for "${condition}":`, '');
  const cooldownSec = await ask(readline, 'Cooldown in seconds:', '300');
  const title = await ask(readline, 'Alert title:', name);
  const template = await ask(readline, 'Message template ({{state}} for value):', `${title}: {{state}}`);
  
  readline.close();
  
  config.rules.push({
    name,
    entity_id,
    condition,
    value: isNaN(value) ? String(value) : parseFloat(value),
    cooldown: parseInt(cooldownSec),
    title,
    template
  });
}

function ask(readline, question, defaultVal) {
  return new Promise(resolve => {
    readline.question(`\x1b[36m${question} \x1b[0m`, (answer) => {
      resolve(answer.trim() || defaultVal);
    });
  });
}

// ─── Utility ─────────────────────────────────────────────────────
function isProcessDead(pid) {
  try { process.kill(pid, 0); return false; } catch { return true; }
}

async function handleShutdown() {
  log('info', 'Shutting down...');
  if (wsClient) wsClient.close();
  stopPolling();
  
  // Cleanup PID file and logs
  try { fs.unlinkSync(PID_FILE); } catch {}
  rotateLogs(MAX_LOG_LINES, LOG_DIR);
  cleanupDelivered(MAX_DELIVERED_FILES);
  
  log('info', 'Shutdown complete');
  process.exit(0);
}

// ─── Main ────────────────────────────────────────────────────────
const config = loadConfig();
const command = process.argv[2];
const args = process.argv.slice(3);

if (command) {
  handleCommand(config, command.toLowerCase(), args).catch(e => {
    console.error(`Error: ${e.message}`);
    process.exit(1);
  });
} else {
  console.log('Home Assistant Hub — usage: node ha-hub.js <command>');
}
