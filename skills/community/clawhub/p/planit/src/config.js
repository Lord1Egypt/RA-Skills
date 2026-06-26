'use strict';

/**
 * Config loader — reads backend API URL from ~/.openclaw/data/planit/config.json
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const CONFIG_FILE = path.join(os.homedir(), '.openclaw', 'data', 'planit', 'config.json');

let _config = null;

function loadConfig() {
  if (_config) return _config;
  try {
    _config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
  } catch {
    _config = {};
  }
  return _config;
}

module.exports = { loadConfig };
