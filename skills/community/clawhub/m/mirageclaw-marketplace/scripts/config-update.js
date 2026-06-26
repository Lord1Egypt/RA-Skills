#!/usr/bin/env node
// SECURITY MANIFEST:
//   Environment variables accessed: none
//   External endpoints called: none
//   Local files read: ~/.openclaw/marketplace-config.json
//   Local files written: ~/.openclaw/marketplace-config.json

'use strict';

const fs   = require('fs');
const path = require('path');
const os   = require('os');

const { CONFIG_PATH } = require('./lib/constants');
// messaging.js not needed — dashboard.js handles UI update via edit-in-place

// ─── Load config ──────────────────────────────────────────────────────────
if (!fs.existsSync(CONFIG_PATH)) {
  process.stderr.write('[ConfigUpdate] ERROR: marketplace-config.json not found.\n');
  process.exit(1);
}

let config;
try {
  config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
} catch (err) {
  process.stderr.write(`[ConfigUpdate] ERROR: Failed to parse config: ${err.message}\n`);
  process.exit(1);
}

// ─── Parse arguments ─────────────────────────────────────────────────────
const field = process.argv[2];
const value = process.argv[3];

if (!field) {
  process.stderr.write('[ConfigUpdate] ERROR: Usage: config-update.js <field> <value>\n');
  process.stderr.write('  Fields: preset, autoaccept, protection, bidprice, minbudget, maxnoshow\n');
  process.exit(1);
}

// ─── Update config ───────────────────────────────────────────────────────
let message = '';
let updated = false;

switch (field) {
  case 'preset': {
    config.presetMode = !config.presetMode;
    message = `Preset mode: ${config.presetMode ? '✅ On' : '❌ Off'}`;
    updated = true;
    break;
  }
  case 'autoaccept': {
    config.presetAutoAccept = !config.presetAutoAccept;
    message = `Auto-accept: ${config.presetAutoAccept ? '✅ Yes' : '❌ No'}`;
    updated = true;
    break;
  }
  case 'protection': {
    const levels = ['low', 'medium', 'high'];
    if (!value || !levels.includes(value)) {
      process.stderr.write(`[ConfigUpdate] ERROR: Invalid protection level. Use: ${levels.join(', ')}\n`);
      process.exit(1);
    }
    config.presetProtection = value;
    message = `Protection level: ${value}`;
    updated = true;
    break;
  }
  case 'bidprice': {
    const pct = parseInt(value, 10);
    if (isNaN(pct) || pct < 10 || pct > 100) {
      process.stderr.write('[ConfigUpdate] ERROR: Bid price must be 10-100 (percentage).\n');
      process.exit(1);
    }
    config.presetPricePercent = pct;
    message = `Bid price: ${pct}% of budget`;
    updated = true;
    break;
  }
  case 'minbudget': {
    const budget = parseInt(value, 10);
    if (isNaN(budget) || budget < 0) {
      process.stderr.write('[ConfigUpdate] ERROR: Min budget must be >= 0 (credits).\n');
      process.exit(1);
    }
    config.minBudget = budget;
    message = `Min budget: ${budget} credits ($${(budget / 100).toFixed(2)})`;
    updated = true;
    break;
  }
  case 'maxnoshow': {
    if (value === 'off' || value === 'null' || value === '') {
      config.maxNoShowRate = null;
      message = 'Max no-show rate: Off (accept all)';
    } else {
      const rate = parseInt(value, 10);
      if (isNaN(rate) || rate < 0 || rate > 100) {
        process.stderr.write('[ConfigUpdate] ERROR: Max no-show rate must be 0-100 or "off".\n');
        process.exit(1);
      }
      config.maxNoShowRate = rate;
      message = `Max no-show rate: ${rate}%`;
    }
    updated = true;
    break;
  }
  default:
    process.stderr.write(`[ConfigUpdate] ERROR: Unknown field: ${field}\n`);
    process.exit(1);
}

// ─── Write config (atomic) ───────────────────────────────────────────────
if (updated) {
  const tmpPath = CONFIG_PATH + '.tmp';
  fs.writeFileSync(tmpPath, JSON.stringify(config, null, 2));
  fs.renameSync(tmpPath, CONFIG_PATH);

  // stdout event (save only — dashboard.js edit-in-place handles the UI update)
  process.stdout.write(JSON.stringify({
    type: 'MARKETPLACE_CONFIG_UPDATED',
    ts: new Date().toISOString(),
    field,
    value: config[field === 'preset' ? 'presetMode' :
           field === 'autoaccept' ? 'presetAutoAccept' :
           field === 'protection' ? 'presetProtection' :
           field === 'bidprice' ? 'presetPricePercent' :
           field === 'minbudget' ? 'minBudget' : 'maxNoShowRate']
  }) + '\n');
}
