#!/usr/bin/env node
/**
 * config.js — Generic config loader for paperclip-resilience skill.
 *
 * Loads configuration from (in priority order):
 *   1. A config file at the path specified by PAPERCLIP_RESILIENCE_CONFIG env var
 *   2. config.json in the skill root (two directories above this file)
 *   3. Built-in defaults (no user-specific paths)
 *
 * All path values have ~ expanded to the real home directory.
 */

'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');

const SKILL_ROOT = path.resolve(__dirname, '..', '..');
const CONFIG_PATH = process.env.PAPERCLIP_RESILIENCE_CONFIG
  || path.join(SKILL_ROOT, 'config.json');

const HOME = os.homedir();

const DEFAULTS = {
  paths: {
    workspace: SKILL_ROOT,
    memory: path.join(SKILL_ROOT, 'memory'),
  },
  user: {
    name: 'User',
    timezone: 'UTC',
  },
};

function expandTilde(p) {
  if (typeof p !== 'string') return p;
  if (p === '~') return HOME;
  if (p.startsWith('~/') || p.startsWith('~\\')) {
    return path.join(HOME, p.slice(2));
  }
  return p;
}

let _config = null;

function getConfig() {
  if (_config) return _config;

  let raw = {};
  try {
    const configPath = CONFIG_PATH;
    if (fs.existsSync(configPath)) {
      raw = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    }
  } catch {
    // Config not found or invalid — use defaults
  }

  const { $schema: _ignored, ...rest } = raw;

  const userPaths = rest.paths || {};
  const validatedPaths = {};
  for (const [key, val] of Object.entries(userPaths)) {
    if (typeof val !== 'string' || val.trim() === '') continue;
    if (!path.isAbsolute(expandTilde(val))) continue;
    validatedPaths[key] = val;
  }

  const config = {
    paths: { ...DEFAULTS.paths, ...validatedPaths },
    user: { ...DEFAULTS.user, ...(rest.user || {}) },
  };

  for (const [key, val] of Object.entries(rest)) {
    if (key !== 'paths' && key !== 'user') {
      config[key] = val;
    }
  }

  for (const [key, val] of Object.entries(config.paths)) {
    config.paths[key] = expandTilde(val);
  }

  _config = config;
  return _config;
}

function resetConfig() {
  _config = null;
}

module.exports = { getConfig, resetConfig, CONFIG_PATH, SKILL_ROOT };
