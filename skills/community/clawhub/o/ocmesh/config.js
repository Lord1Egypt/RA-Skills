/**
 * config.js
 * Loads ~/.ocmesh/config.json — user-editable runtime config.
 * Created with defaults on first run.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const CONFIG_PATH = path.join(os.homedir(), '.ocmesh', 'config.json');

const DEFAULTS = {
  webhook: {
    enabled: false,
    url: 'http://127.0.0.1:7433/ocmesh-event',
    secret: null,
  },
  profile: {
    name: null,       // human-readable agent name
    about: null,      // short description
    picture: null,    // avatar URL
  },
  mesh: {
    announceInterval: 300000,   // 5 min
    discoveryInterval: 120000,  // 2 min
    peerTtl: 900000,            // 15 min
  },
};

function load() {
  if (!fs.existsSync(CONFIG_PATH)) {
    fs.writeFileSync(CONFIG_PATH, JSON.stringify(DEFAULTS, null, 2));
    return DEFAULTS;
  }
  try {
    const raw = fs.readFileSync(CONFIG_PATH, 'utf8');
    return deepMerge(DEFAULTS, JSON.parse(raw));
  } catch (err) {
    console.warn('[config] Failed to parse config.json, using defaults:', err.message);
    return DEFAULTS;
  }
}

function save(cfg) {
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(cfg, null, 2));
}

function deepMerge(base, override) {
  const result = { ...base };
  for (const key of Object.keys(override)) {
    if (override[key] && typeof override[key] === 'object' && !Array.isArray(override[key])) {
      result[key] = deepMerge(base[key] || {}, override[key]);
    } else {
      result[key] = override[key];
    }
  }
  return result;
}

module.exports = { load, save, CONFIG_PATH };
