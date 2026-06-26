#!/usr/bin/env node
// SECURITY MANIFEST:
//   Environment variables accessed: MARKETPLACE_API_KEY
//   External endpoints called: {BASE}/agents/mine (GET — API key auth, 1:1 agent)
//   Local files read: ~/.openclaw/marketplace-config.json, ~/.openclaw/marketplace.env
//   Local files written: ~/.openclaw/marketplace-config.json (agentId, agentName, introduction)

'use strict';

const fs   = require('fs');
const path = require('path');
const os   = require('os');
const { execFileSync } = require('child_process');

const { CONFIG_PATH } = require('./lib/constants');
require('./lib/env').loadEnv();

const BASE_URL = 'https://api.mirageclaw.io';

if (!fs.existsSync(CONFIG_PATH)) {
  console.error('[Register] ERROR: marketplace-config.json not found. Run onboarding first.');
  process.exit(1);
}

let config;
try {
  config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
} catch (err) {
  console.error('[Register] ERROR: Failed to parse config:', err.message);
  process.exit(1);
}

// ─── Validate API Key ────────────────────────────────────────────────────
const apiKey = process.env.MARKETPLACE_API_KEY;
if (!apiKey) {
  console.error('[Register] ERROR: MARKETPLACE_API_KEY not set. Get your API key from https://mirageclaw.io.');
  process.exit(1);
}

// ─── Fetch my agent via GET /agents/mine (API key auth, 1:1) ────────────
try {
  const result = execFileSync('curl', [
    '-sf',
    `${BASE_URL}/agents/mine`,
    '-H', `Authorization: Bearer ${apiKey}`
  ], { timeout: 15000 });

  const agents = JSON.parse(result.toString());
  if (!Array.isArray(agents) || agents.length === 0) {
    console.error('[Register] ERROR: No agent linked to this API key.');
    console.error('[Register] Create your agent at https://mirageclaw.io first.');
    process.exit(1);
  }

  // API key:agent is 1:1 — take the first (and only) agent
  const agent = agents[0];

  // Sync agent info to config
  config.agentId = String(agent._id);
  config.agentName = agent.name || config.agentName || 'Unknown';
  config.introduction = agent.description || config.introduction || '';

  const tmp = CONFIG_PATH + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(config, null, 2));
  fs.renameSync(tmp, CONFIG_PATH);

  console.log(`[Register] ✅ Connected: ${config.agentName} (agentId: ${config.agentId})`);

} catch (err) {
  const msg = err.message || '';
  if (msg.includes('status 401') || msg.includes('Unauthorized') || err.status === 22) {
    console.error('[Register] ERROR: API key is invalid or expired.');
    console.error('[Register] Generate a new one at https://mirageclaw.io.');
  } else {
    console.error(`[Register] ERROR: Failed to fetch agent: ${msg}`);
  }
  process.exit(1);
}
