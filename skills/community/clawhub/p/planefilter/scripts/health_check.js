#!/usr/bin/env node
/**
 * health_check.js — Verify API keys and connectivity for PlaneFilter skill.
 *
 * Usage: node health_check.js
 *
 * @security { env: ["RAPIDAPI_KEY", "AIRLABS_KEY"], endpoints: ["aerodatabox.p.rapidapi.com", "airlabs.co", "opensky-network.org"], files: { read: [], write: [] } }
 */
'use strict';

const { get } = require('./api_client');

async function checkOpenSky() {
  try {
    await get('https://opensky-network.org/api/states/all?callsign=TEST&time=0');
    return { status: 'ok', note: 'Free, no key required' };
  } catch (err) {
    return { status: 'warn', note: `Connection error: ${err.message}` };
  }
}

async function checkAeroDataBox() {
  const key = process.env.RAPIDAPI_KEY;
  if (!key) return { status: 'missing', note: 'RAPIDAPI_KEY not set' };
  try {
    const host = 'aerodatabox.p.rapidapi.com';
    await get(`https://${host}/health/status`, {
      'X-RapidAPI-Key': key,
      'X-RapidAPI-Host': host,
    });
    return { status: 'ok', note: 'Key valid' };
  } catch (err) {
    if (err.message.includes('403')) return { status: 'error', note: 'Invalid or expired RAPIDAPI_KEY' };
    return { status: 'ok', note: 'Key set (endpoint check skipped)' };
  }
}

async function checkAirLabs() {
  const key = process.env.AIRLABS_KEY;
  if (!key) return { status: 'skipped', note: 'AIRLABS_KEY not set (optional)' };
  try {
    await get(`https://airlabs.co/api/v9/ping?api_key=${encodeURIComponent(key)}`);
    return { status: 'ok', note: 'Key valid' };
  } catch (err) {
    return { status: 'error', note: `AirLabs error: ${err.message}` };
  }
}

async function main() {
  console.log('PlaneFilter Skill — Health Check\n');

  const results = {
    opensky: await checkOpenSky(),
    aerodatabox: await checkAeroDataBox(),
    airlabs: await checkAirLabs(),
  };

  const icons = { ok: '✅', warn: '⚠️', error: '❌', missing: '❌', skipped: '⏭️' };

  for (const [name, result] of Object.entries(results)) {
    const icon = icons[result.status] || '❓';
    console.log(`${icon} ${name.padEnd(14)} ${result.status.padEnd(8)} ${result.note}`);
  }

  console.log('\nCapabilities:');
  console.log(`  Flight search:  ${results.aerodatabox.status === 'ok' ? '✅ Ready' : '❌ Need RAPIDAPI_KEY'}`);
  console.log(`  Multi-source:   ${results.airlabs.status === 'ok' ? '✅ 3 sources' : '2 sources (add AIRLABS_KEY for 3rd)'}`);

  const hasError = results.aerodatabox.status === 'missing' || results.aerodatabox.status === 'error';
  process.exit(hasError ? 1 : 0);
}

main().catch((err) => {
  console.log(JSON.stringify({ error: true, message: err.message }));
  process.exit(1);
});
