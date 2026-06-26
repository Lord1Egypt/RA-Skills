// sessions.js — Multi-agent session key lookup and tag formatting
const fs = require('fs');
const path = require('path');
const { AGENTS, buildNameMaps } = require('./config');

const TAG_MAX = 40;

const CHANNEL_ICONS = {
  telegram: '✈',
};

// Per-agent state
const agentStates = new Map(); // agentName → { dir, keyMap, labelMap, derivedMap, DIRECT_NAMES, GROUP_NAMES, agentId }

function initAgents() {
  for (const agent of AGENTS) {
    const m = agent.dir.match(/agents\/([^/]+)\/sessions/);
    const agentId = m ? m[1] : 'main';
    const { DIRECT_NAMES, GROUP_NAMES } = buildNameMaps(agent.name);
    agentStates.set(agent.name, {
      dir: agent.dir,
      agentId,
      keyMap: {},
      labelMap: {},
      derivedMap: {},
      DIRECT_NAMES,
      GROUP_NAMES,
    });
  }
}

initAgents();

function loadKeys() {
  for (const [name, state] of agentStates) {
    try {
      const data = JSON.parse(fs.readFileSync(path.join(state.dir, 'sessions.json'), 'utf8'));
      state.keyMap = {};
      state.labelMap = {};
      for (const [key, s] of Object.entries(data)) {
        const id = s.sessionId || s.id;
        if (!id) continue;
        state.keyMap[id] = key;
        if (s.label) {
          const m = key.match(/subagent:([0-9a-f]{8})/);
          if (m) state.labelMap[m[1]] = s.label;
        }
      }
    } catch {}
  }
}

// Find which agent owns a session ID
function findAgent(sid) {
  for (const [name, state] of agentStates) {
    if (state.keyMap[sid]) return { name, state };
  }
  return null;
}

function getSubagentName(sid, key, state) {
  const m = key.match(/subagent:([0-9a-f]{8})/);
  const uuid = m ? m[1] : null;

  if (uuid && state.labelMap[uuid]) return state.labelMap[uuid];
  if (state.derivedMap[sid]) return state.derivedMap[sid];
  try {
    const fp = path.join(state.dir, sid + '.jsonl');
    const fd = fs.openSync(fp, 'r');
    const buf = Buffer.alloc(4000);
    const bytesRead = fs.readSync(fd, buf, 0, 4000, 0);
    fs.closeSync(fd);
    const head = buf.toString('utf8', 0, bytesRead);
    const pm = head.match(/\/prompts\/(.+?)\.txt/);
    if (pm) { state.derivedMap[sid] = pm[1]; return pm[1]; }
  } catch {}

  return uuid || sid.slice(0, 8);
}

function getTag(sid, agentName) {
  const agent = agentName ? { name: agentName, state: agentStates.get(agentName) } : findAgent(sid);
  if (!agent || !agent.state) return sid.slice(0, 8);

  const { name, state } = agent;
  const prefix = AGENTS.length > 1 ? `[${name}] ` : '';
  let key = state.keyMap[sid] || sid;

  key = key.replace(/^agent:/, '').replace(new RegExp('^' + state.agentId + ':'), '');

  // External channels
  for (const [channel, icon] of Object.entries(CHANNEL_ICONS)) {
    if (!key.startsWith(channel + ':')) continue;
    const rest = key.slice(channel.length + 1);

    for (const [pattern, dname] of Object.entries(state.DIRECT_NAMES)) {
      if (rest.startsWith(pattern)) {
        const suffix = rest.slice(pattern.length);
        const extra = suffix.replace(/:/g, '∙').replace(/\bheartbeat\b/g, '💓');
        return extra ? `${prefix}${icon} ${dname}${extra}` : `${prefix}${icon} ${dname}`;
      }
    }

    for (const [pattern, gname] of Object.entries(state.GROUP_NAMES)) {
      if (rest.startsWith(pattern)) {
        const suffix = rest.slice(pattern.length);
        const extra = suffix.replace(/:/g, '∙').replace(/\bheartbeat\b/g, '💓');
        return extra ? `${prefix}${icon} ${gname}${extra}` : `${prefix}${icon} ${gname}`;
      }
    }

    let tag = `${icon} ${rest}`;
    tag = tag.replace(/\bheartbeat\b/g, '💓');
    tag = tag.replace(/\b([0-9a-f]{6,})-[0-9a-f-]+\b/g, '$1');
    tag = tag.replace(/:/g, '∙');
    tag = prefix + tag;
    return tag.length > TAG_MAX + prefix.length ? tag.slice(0, TAG_MAX + prefix.length) : tag;
  }

  // Subagent
  if (/\bsubagent\b/.test(key)) {
    const m = key.match(/subagent:([0-9a-f]{8})/);
    const uuid = m ? m[1] : sid.slice(0, 8);
    const sname = getSubagentName(sid, key, state);
    const hasHb = /heartbeat/.test(key.split('subagent:')[1] || '');
    const base = sname !== uuid ? `👶∙${sname}∙${uuid}` : `👶∙${uuid}`;
    return hasHb ? `${prefix}${base}∙💓` : `${prefix}${base}`;
  }

  // Internal
  key = key.replace(/\bheartbeat\b/g, '💓');
  key = key.replace(/\b([0-9a-f]{6,})-[0-9a-f-]+\b/g, '$1');
  key = key.replace(/:+$/g, '').replace(/^:+/g, '');
  key = key.replace(/:/g, '∙');
  key = prefix + key;
  return key.length > TAG_MAX + prefix.length ? key.slice(0, TAG_MAX + prefix.length) : key;
}

// Return all session dirs for polling
function getAllDirs() {
  return Array.from(agentStates.entries()).map(([name, state]) => ({ name, dir: state.dir }));
}

module.exports = { loadKeys, getTag, getAllDirs };
