// config.js — Load configuration from .env file (multi-agent support)
const fs = require('fs');
const path = require('path');

function loadEnv() {
  const envPath = path.join(__dirname, '.env');
  try {
    const lines = fs.readFileSync(envPath, 'utf8').split('\n');
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;
      const eq = trimmed.indexOf('=');
      if (eq < 0) continue;
      const key = trimmed.slice(0, eq).trim();
      const val = trimmed.slice(eq + 1).trim();
      if (!process.env[key]) process.env[key] = val;
    }
  } catch {}
}

loadEnv();

const BOT_TOKEN = process.env.BOT_TOKEN || '';
const CHAT_ID = process.env.CHAT_ID || '';

// Parse "id:name,id:name" format
function parseMap(str) {
  const map = {};
  if (!str) return map;
  for (const pair of str.split(',')) {
    const colon = pair.indexOf(':');
    if (colon < 0) continue;
    const id = pair.slice(0, colon).trim();
    const name = pair.slice(colon + 1).trim();
    if (id && name) map[id] = name;
  }
  return map;
}

// Multi-agent: parse AGENTS env "name|dir,name|dir"
// Fallback to legacy AGENT_NAME + SESSIONS_DIR
function parseAgents() {
  const raw = process.env.AGENTS || '';
  if (raw) {
    return raw.split(',').map(entry => {
      const [name, dir] = entry.split('|').map(s => s.trim());
      return { name, dir };
    }).filter(a => a.name && a.dir);
  }
  // Legacy single-agent
  const name = process.env.AGENT_NAME || 'Agent';
  const dir = process.env.SESSIONS_DIR || path.join(process.env.HOME, '.openclaw/agents/main/sessions');
  return [{ name, dir }];
}

const AGENTS = parseAgents();

const directUsers = parseMap(process.env.DIRECT_USERS || '');
const groups = parseMap(process.env.GROUPS || '');

// Build name maps per-agent (keyed by agent name for tag prefixing)
function buildNameMaps(agentName) {
  const DIRECT_NAMES = {};
  for (const [id, name] of Object.entries(directUsers)) {
    DIRECT_NAMES[`direct:${id}`] = `${agentName}↔${name}`;
  }
  const GROUP_NAMES = {};
  for (const [id, name] of Object.entries(groups)) {
    GROUP_NAMES[`group:${id}`] = name;
  }
  return { DIRECT_NAMES, GROUP_NAMES };
}

module.exports = { BOT_TOKEN, CHAT_ID, AGENTS, buildNameMaps, parseMap };
