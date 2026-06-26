#!/usr/bin/env node
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const homeDir = os.homedir();
const runtimeHome = process.env.SESSION_INSPECTOR_HOME || process.env.SESSION_INSPACTOR_HOME || path.join(homeDir, '.openclaw', 'inspector');
const registryPath = path.join(runtimeHome, 'registry.json');
const stateDir = path.join(runtimeHome, 'state');
const logsDir = path.join(runtimeHome, 'logs');
const systemdDir = path.join(runtimeHome, 'systemd');
const launchdDir = path.join(runtimeHome, 'launchd');
const windowsDir = path.join(runtimeHome, 'windows');
const configFile = path.join(runtimeHome, 'config.env');
const serviceName = 'openclaw-inspector';
const unitDir = path.join(homeDir, '.config', 'systemd', 'user');
const unitPath = path.join(unitDir, `${serviceName}.service`);
const launchAgentsDir = path.join(homeDir, 'Library', 'LaunchAgents');
const plistPath = path.join(launchAgentsDir, `${serviceName}.plist`);
const sessionsRoot = process.env.SESSION_INSPECTOR_SESSIONS_ROOT || process.env.SESSION_INSPACTOR_SESSIONS_ROOT || path.join(homeDir, '.openclaw', 'agents');
const openclawBin = process.env.OPENCLAW_BIN || 'openclaw';
const defaultConfig = {
  SCAN_INTERVAL_SECONDS: '30',
  DEFAULT_INACTIVE_THRESHOLD_SECONDS: '600',
  DEFAULT_COOLDOWN_SECONDS: '3600',
  DEFAULT_RUNNING_COOLDOWN_SECONDS: '600',
  DEFAULT_BLOCKED_COOLDOWN_SECONDS: '1800',
  DEFAULT_MAX_LAST_ACTIVITY_AGE_SECONDS: '43200',
  DEFAULT_MAX_STATUS_LOOKBACK_MESSAGES: '5',
  AGENT_CLI_TIMEOUT_SECONDS: '180',
};

function nowIso() {
  return new Date().toISOString();
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function ensureRuntimeDirs() {
  [runtimeHome, stateDir, logsDir, systemdDir, launchdDir, windowsDir].forEach(ensureDir);
}

function readJson(file, fallback = null) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (error) {
    if (fallback !== null) return fallback;
    throw error;
  }
}

function writeJson(file, value) {
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function ensureRegistry() {
  ensureRuntimeDirs();
  if (!fs.existsSync(registryPath)) {
    writeJson(registryPath, { sessions: [] });
  }
  const registry = readJson(registryPath, null);
  if (!registry || !Array.isArray(registry.sessions)) {
    throw new Error(`invalid registry json: ${registryPath}`);
  }
  return registry;
}

function isValidSessionUuid(value) {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value || '');
}

function parseEnvFile(file) {
  const result = {};
  if (!fs.existsSync(file)) return result;
  const lines = fs.readFileSync(file, 'utf8').split(/\r?\n/);
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eq = trimmed.indexOf('=');
    if (eq <= 0) continue;
    const key = trimmed.slice(0, eq).trim();
    let value = trimmed.slice(eq + 1).trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    result[key] = value;
  }
  return result;
}

function ensureConfigFile() {
  if (fs.existsSync(configFile)) return;
  const lines = Object.entries(defaultConfig).map(([k, v]) => `${k}=${v}`);
  fs.writeFileSync(configFile, `${lines.join('\n')}\n`, 'utf8');
}

function commandExists(command, args = ['--help']) {
  try {
    const result = spawnSync(command, args, { stdio: 'ignore' });
    return !result.error;
  } catch {
    return false;
  }
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'"'"'`)}'`;
}

function parseTimestamp(value) {
  if (!value) return 0;
  const ms = Date.parse(String(value));
  return Number.isFinite(ms) ? Math.floor(ms / 1000) : 0;
}

function extractText(content) {
  if (typeof content === 'string') return content.trim();
  if (Array.isArray(content)) {
    return content
      .filter((item) => item && typeof item === 'object' && item.type === 'text' && item.text)
      .map((item) => item.text)
      .join('\n')
      .trim();
  }
  return '';
}

function listImmediateSubdirs(dir) {
  try {
    return fs.readdirSync(dir, { withFileTypes: true })
      .filter((entry) => entry.isDirectory())
      .map((entry) => path.join(dir, entry.name));
  } catch {
    return [];
  }
}

function findSessionFile(sessionId) {
  for (const agentDir of listImmediateSubdirs(sessionsRoot)) {
    const candidate = path.join(agentDir, 'sessions', `${sessionId}.jsonl`);
    if (fs.existsSync(candidate)) return candidate;
  }
  return '';
}

function parseSessionFile(file, statusLookback = 5) {
  if (!file || !fs.existsSync(file)) return null;
  const stat = fs.statSync(file);
  const lastActivityEpoch = Math.floor(stat.mtimeMs / 1000);
  const lines = fs.readFileSync(file, 'utf8').split(/\r?\n/);
  const statusRe = /^STATUS:\s*(DONE|WAITING|BLOCKED|RUNNING)\s*\|\s*(.*)$/i;
  let workdir = '';
  let command = '';
  let lastMessage = {};
  let latestStatus = {};
  let terminalStatus = '';
  let terminalTimestamp = '';
  let terminalEpoch = 0;
  const assistantTail = [];

  for (const rawLine of lines) {
    const raw = rawLine.trim();
    if (!raw) continue;
    let obj;
    try {
      obj = JSON.parse(raw);
    } catch {
      continue;
    }

    if (obj.type === 'session' && !workdir) {
      workdir = obj.cwd || workdir;
    }

    if (obj.type === 'custom' && obj.customType === 'openclaw:prompt-error') {
      terminalStatus = 'error';
      terminalTimestamp = obj.timestamp || terminalTimestamp;
      terminalEpoch = parseTimestamp(terminalTimestamp);
    }

    if (obj.type !== 'message') continue;
    const msg = obj.message || {};
    const role = msg.role;
    const timestamp = obj.timestamp || '';
    const stopReason = msg.stopReason || '';
    const text = extractText(msg.content);

    if (!command) {
      command = obj.command || msg.command || '';
    }

    if (role === 'assistant' || role === 'user' || role === 'toolResult') {
      lastMessage = { role, timestamp, epoch: parseTimestamp(timestamp), stop_reason: stopReason, text };
    }

    if (role === 'assistant' && text) {
      assistantTail.push({ timestamp, epoch: parseTimestamp(timestamp), stop_reason: stopReason, text });
      while (assistantTail.length > statusLookback) assistantTail.shift();
      const firstLine = text.split(/\r?\n/, 1)[0].trim();
      const match = statusRe.exec(firstLine);
      if (match) {
        latestStatus = {
          marker: match[1].toUpperCase(),
          summary: match[2].trim(),
          timestamp,
          epoch: parseTimestamp(timestamp),
          first_line: firstLine,
        };
      }
    }

    if (role === 'assistant' && !terminalStatus && ['aborted', 'error', 'failed'].includes(stopReason)) {
      terminalStatus = stopReason;
      terminalTimestamp = timestamp;
      terminalEpoch = parseTimestamp(timestamp);
    }
  }

  return {
    session_file: file,
    last_activity_epoch: lastActivityEpoch,
    last_activity: new Date(lastActivityEpoch * 1000).toISOString(),
    workdir,
    command,
    last_message: lastMessage,
    latest_status: latestStatus,
    assistant_tail: assistantTail,
    terminal_status: terminalStatus,
    terminal_timestamp: terminalTimestamp,
    terminal_epoch: terminalEpoch,
  };
}

function stateFileFor(sessionId) {
  return path.join(stateDir, `${sessionId}.json`);
}

function readState(sessionId) {
  return readJson(stateFileFor(sessionId), {});
}

function writeState(sessionId, value) {
  writeJson(stateFileFor(sessionId), value);
}

function mergeConfig() {
  return { ...defaultConfig, ...parseEnvFile(configFile), ...process.env };
}

module.exports = {
  fs,
  os,
  path,
  spawnSync,
  homeDir,
  runtimeHome,
  registryPath,
  stateDir,
  logsDir,
  systemdDir,
  launchdDir,
  windowsDir,
  configFile,
  serviceName,
  unitDir,
  unitPath,
  launchAgentsDir,
  plistPath,
  sessionsRoot,
  openclawBin,
  defaultConfig,
  nowIso,
  ensureDir,
  ensureRuntimeDirs,
  readJson,
  writeJson,
  ensureRegistry,
  isValidSessionUuid,
  parseEnvFile,
  ensureConfigFile,
  commandExists,
  shellQuote,
  parseTimestamp,
  extractText,
  findSessionFile,
  parseSessionFile,
  stateFileFor,
  readState,
  writeState,
  mergeConfig,
};
