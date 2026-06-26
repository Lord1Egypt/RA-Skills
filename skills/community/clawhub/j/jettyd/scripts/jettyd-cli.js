#!/usr/bin/env node
/**
 * jettyd CLI — OpenClaw skill for jettyd IoT platform
 * Usage: node jettyd-cli.js <command> [args...]
 */

import { readFileSync, existsSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

// ── Config ────────────────────────────────────────────────────────────────────

function getConfig() {
  let apiKey = process.env.JETTYD_API_KEY;
  let baseUrl = process.env.JETTYD_BASE_URL || 'https://api.jettyd.com/v1';

  if (!apiKey) {
    const cfgPath = join(homedir(), '.openclaw', 'openclaw.json');
    if (existsSync(cfgPath)) {
      try {
        const cfg = JSON.parse(readFileSync(cfgPath, 'utf8'));
        const entry = cfg?.skills?.entries?.jettyd;
        if (entry?.apiKey) apiKey = entry.apiKey;
        if (entry?.baseUrl) baseUrl = entry.baseUrl;
      } catch {}
    }
  }

  if (!apiKey) {
    console.error('❌ No API key found. Set JETTYD_API_KEY or add to ~/.openclaw/openclaw.json');
    process.exit(1);
  }

  return { apiKey, baseUrl };
}

// ── HTTP ──────────────────────────────────────────────────────────────────────

async function api(method, path, body) {
  const { apiKey, baseUrl } = getConfig();
  const res = await fetch(`${baseUrl}${path}`, {
    method,
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${res.status}: ${text}`);
  }

  return res.json();
}

// ── Formatting ────────────────────────────────────────────────────────────────

function statusDot(status) {
  return status === 'online' ? '●' : status === 'provisioning' ? '◐' : '○';
}

function relativeTime(iso) {
  if (!iso) return 'never';
  const diff = Date.now() - new Date(iso).getTime();
  const s = Math.floor(diff / 1000);
  if (s < 60) return `${s}s ago`;
  if (s < 3600) return `${Math.floor(s / 60)}m ago`;
  if (s < 86400) return `${Math.floor(s / 3600)}h ago`;
  return `${Math.floor(s / 86400)}d ago`;
}

function formatShadow(shadow) {
  if (!shadow || Object.keys(shadow).length === 0) return '  (no readings yet)';
  const reported = shadow.reported || shadow;
  return Object.entries(reported)
    .filter(([k]) => !k.startsWith('_') && k !== 'mac_address')
    .map(([k, v]) => {
      const val = typeof v === 'number' ? v.toFixed(2) : v;
      return `  ${k.padEnd(20)} ${val}`;
    })
    .join('\n');
}

// ── Commands ──────────────────────────────────────────────────────────────────

async function cmdList() {
  const devices = await api('GET', '/devices');
  if (!devices.length) {
    console.log('No devices found.');
    return;
  }
  console.log(`\n${'Status'.padEnd(8)} ${'Name'.padEnd(24)} ${'Device ID'.padEnd(38)} ${'Last seen'}`);
  console.log('─'.repeat(90));
  for (const d of devices) {
    const dot = statusDot(d.status);
    console.log(`${(dot + ' ' + d.status).padEnd(8)} ${d.name.padEnd(24)} ${d.id.padEnd(38)} ${relativeTime(d.last_seen_at)}`);
  }
  console.log(`\n${devices.length} device(s) total`);
}

async function cmdDevice(id) {
  const d = await api('GET', `/devices/${id}`);
  const shadow = await api('GET', `/devices/${id}/shadow`).catch(() => ({}));

  console.log(`\n━━━ ${d.name} ━━━`);
  console.log(`  ID:            ${d.id}`);
  console.log(`  Status:        ${statusDot(d.status)} ${d.status}`);
  console.log(`  Type:          ${d.device_type_id || 'unknown'}`);
  console.log(`  Firmware:      ${d.firmware_version || 'unknown'}`);
  console.log(`  Last seen:     ${relativeTime(d.last_seen_at)}`);
  console.log(`\n  Sensor readings:`);
  console.log(formatShadow(shadow));
}

async function cmdTelemetry(id, metric, period = '24h') {
  const periodMap = { '1h': 1, '6h': 6, '24h': 24, '7d': 168 };
  const hours = periodMap[period] || 24;
  const from = new Date(Date.now() - hours * 3600 * 1000).toISOString();

  const params = new URLSearchParams({ from, limit: 100 });
  if (metric) params.set('metric', metric);

  const data = await api('GET', `/devices/${id}/telemetry?${params}`);

  if (!data.length) {
    console.log(`No telemetry for device ${id}${metric ? ` (${metric})` : ''} in the last ${period}.`);
    return;
  }

  // Group by metric name
  const grouped = {};
  for (const row of data) {
    for (const [k, v] of Object.entries(row.readings || {})) {
      if (!grouped[k]) grouped[k] = [];
      grouped[k].push(v);
    }
  }

  console.log(`\nTelemetry — ${id} — last ${period} (${data.length} readings)\n`);
  for (const [name, vals] of Object.entries(grouped)) {
    if (metric && name !== metric) continue;
    const nums = vals.filter(v => typeof v === 'number');
    if (!nums.length) continue;
    const min = Math.min(...nums).toFixed(2);
    const max = Math.max(...nums).toFixed(2);
    const avg = (nums.reduce((a, b) => a + b, 0) / nums.length).toFixed(2);
    const latest = nums[nums.length - 1].toFixed(2);
    console.log(`  ${name.padEnd(20)} latest: ${latest.padStart(8)}  avg: ${avg.padStart(8)}  min: ${min.padStart(8)}  max: ${max.padStart(8)}`);
  }
}

async function cmdCommand(id, action, paramsStr) {
  let params = {};
  if (paramsStr) {
    try { params = JSON.parse(paramsStr); }
    catch { console.error('❌ Invalid params JSON'); process.exit(1); }
  }

  const result = await api('POST', `/devices/${id}/commands`, { action, params });
  console.log(`✅ Command sent — ID: ${result.id || 'ok'}`);
  if (result.status) console.log(`   Status: ${result.status}`);
}

async function cmdPushConfig(id, configArg) {
  let config;
  try {
    // Try as file path first, then inline JSON
    if (existsSync(configArg)) {
      config = JSON.parse(readFileSync(configArg, 'utf8'));
    } else {
      config = JSON.parse(configArg);
    }
  } catch {
    console.error('❌ Invalid config — provide a JSON file path or inline JSON string');
    process.exit(1);
  }

  await api('PUT', `/devices/${id}/config`, config);
  console.log(`✅ Config pushed to device ${id}`);
  console.log(`   ${config.rules?.length || 0} rules, ${config.heartbeats?.length || 0} heartbeats`);
}

async function cmdWebhooks() {
  const hooks = await api('GET', '/webhooks');
  if (!hooks.length) { console.log('No webhooks configured.'); return; }
  console.log(`\n${'Name'.padEnd(24)} ${'Events'.padEnd(30)} URL`);
  console.log('─'.repeat(90));
  for (const h of hooks) {
    const events = (h.events || []).join(', ');
    console.log(`${h.name.padEnd(24)} ${events.padEnd(30)} ${h.url}`);
  }
}

async function cmdCreateWebhook(name, url, ...events) {
  const hook = await api('POST', '/webhooks', { name, url, events });
  console.log(`✅ Webhook created — ID: ${hook.id}`);
  console.log(`   Events: ${events.join(', ')}`);
}

// ── Main ──────────────────────────────────────────────────────────────────────

const [,, cmd, ...args] = process.argv;

const commands = {
  list:           () => cmdList(),
  device:         () => cmdDevice(args[0]),
  telemetry:      () => cmdTelemetry(args[0], args[1], args[2]),
  command:        () => cmdCommand(args[0], args[1], args[2]),
  push_config:    () => cmdPushConfig(args[0], args[1]),
  webhooks:       () => cmdWebhooks(),
  create_webhook: () => cmdCreateWebhook(...args),
};

if (!cmd || !commands[cmd]) {
  console.log(`jettyd CLI\n\nUsage: jettyd-cli.js <command> [args]\n\nCommands:\n${Object.keys(commands).map(c => `  ${c}`).join('\n')}`);
  process.exit(1);
}

commands[cmd]().catch(e => { console.error(`❌ ${e.message}`); process.exit(1); });
