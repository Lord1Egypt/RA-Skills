'use strict';

const fs   = require('fs');
const path = require('path');
const os   = require('os');

const ENV_PATH = path.join(os.homedir(), '.openclaw/marketplace.env');

/**
 * Load ~/.openclaw/marketplace.env into process.env.
 * Shell env takes priority (existing keys are not overwritten).
 */
function loadEnv() {
  if (!fs.existsSync(ENV_PATH)) return;
  fs.readFileSync(ENV_PATH, 'utf-8').split('\n').forEach(line => {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) return;
    const idx = trimmed.indexOf('=');
    if (idx === -1) return;
    const key = trimmed.slice(0, idx).trim();
    const val = trimmed.slice(idx + 1).trim().replace(/^["']|["']$/g, '');
    if (key && !(key in process.env)) process.env[key] = val;
  });
}

module.exports = { loadEnv, ENV_PATH };
