#!/usr/bin/env node
/**
 * Home Assistant on-demand commands
 * 
 * Routes commands to either:
 * 1. The local hub API (ha-hub.js running)
 * 2. Direct HA API (fallback)
 * 
 * Usage:
 *   node ha-cmd.js info              — HA info
 *   node ha-cmd.js state             — all states
 *   node ha-cmd.js state get light.living_room
 *   node ha-cmd.js state list light
 *   node ha-cmd.js call light.turn_on entity_id=light.living_room
 *
 * Service domains are gated: dangerous domains (lock, alarm_control_panel,
 * cover) are ALWAYS blocked. Safe domains require explicit opt-in.
 */

const fs = require('fs');
const path = require('path');
const http = require('http');

const WORKSPACE = process.env.HOME + '/.openclaw/workspace';
const SKILL_DIR = path.join(WORKSPACE, 'skills', 'home-assistant-hub');
const CONFIG_FILE = path.join(SKILL_DIR, 'config', 'hub.json');

// ─── Config ───────────────────────────────────────────────────────

function loadConfig() {
  if (!fs.existsSync(CONFIG_FILE)) {
    console.error('No config found. Run: node ha-hub.js setup');
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
}

// ─── API call ─────────────────────────────────────────────────────

function apiCall(path, token, haUrl = null, method = 'GET', body = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, haUrl || 'http://localhost:8123');
    const isHttps = url.protocol === 'https:';
    const lib = isHttps ? require('https') : require('http');

    const options = {
      hostname: url.hostname,
      port: url.port || (isHttps ? 443 : 80),
      path: url.pathname + url.search,
      method,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'User-Agent': 'openclaw-ha-cmd/1.0'
      }
    };

    const req = lib.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); } catch { resolve(data); }
      });
    });
    req.on('error', reject);
    req.setTimeout(15000, () => { req.destroy(); reject(new Error('Timeout')); });
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

// ─── Local hub API ────────────────────────────────────────────────

function hubCall(path, method = 'GET', body = null) {
  return new Promise((resolve, reject) => {
    const port = config.on_demand?.port || 9123;
    const options = {
      hostname: '127.0.0.1',
      port,
      path,
      method,
      headers: { 'Content-Type': 'application/json' }
    };
    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); } catch { resolve(data); }
      });
    });
    req.on('error', reject);
    req.setTimeout(5000, () => { req.destroy(); reject(new Error('Hub timeout')); });
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

// ─── Main ─────────────────────────────────────────────────────────

async function main() {
  const config = loadConfig();
  const args = process.argv.slice(2);
  const cmd = args[0];
  const subcmd = args[1];

  // Helper: try hub first, fall back to direct
  async function fetch(path, method = 'GET', body = null) {
    try {
      return await hubCall(path, method, body);
    } catch {
      return await apiCall(path, config.ha_token, config.ha_url, method, body);
    }
  }

  switch (cmd) {
    case 'info': {
      const data = await apiCall('/api/', config.ha_token, config.ha_url);
      console.log(`Home Assistant ${data.version || 'unknown'}`);
      console.log(`  URL: ${data.base_url || config.ha_url}`);
      console.log(`  OS: ${data.os_name || 'unknown'}`);
      break;
    }

    case 'state': {
      if (subcmd === 'get' && args[2]) {
        const data = await fetch(`/api/states/${args[2]}`);
        console.log(JSON.stringify(data, null, 2));
      } else if (subcmd === 'list' && args[2]) {
        // Filter by domain
        const all = await fetch('/api/states');
        const domain = args[2];
        const filtered = Array.isArray(all) ? all.filter(s => s.entity_id.startsWith(domain + '.')) : [];
        console.log(JSON.stringify(filtered, null, 2));
      } else if (subcmd === 'history' && args[2]) {
        const entity = args[2];
        const since = args[3] || '1h';
        const data = await fetch(`/api/history/period/${encodeURIComponent(entity)}?filter_entity_id=${entity}&end_time=${new Date().toISOString()}`);
        console.log(JSON.stringify(data, null, 2));
      } else {
        const all = await fetch('/api/states');
        console.log(JSON.stringify(all, null, 2));
      }
      break;
    }

    case 'call': {
      if (!subcmd) {
        console.error('Usage: node ha-cmd.js call <domain.service> [key=value ...]');
        console.log('\nExamples:');
        console.log('  node ha-cmd.js call light.turn_on entity_id=light.living_room');
        console.log('  node ha-cmd.js call climate.set_temperature entity_id=climate.hvac temperature=22');
        console.log('  node ha-cmd.js call scene.turn_on entity_id=scene.movie_time');
        process.exit(1);
      }

      const parts = subcmd.split('.');
      if (parts.length !== 2) {
        console.error('Service must be in format: domain.service');
        process.exit(1);
      }

      // ─── Hardcoded deny list — NEVER allowed, regardless of config ──
      const DENIED_DOMAINS = ['lock', 'alarm_control_panel', 'cover'];
      if (DENIED_DOMAINS.includes(parts[0])) {
        console.error(`\n⛔ Service domain "${parts[0]}" is HARD-LOCKED.`);
        console.error(`   This category is never permitted: ${DENIED_DOMAINS.join(', ')}`);
        process.exit(1);
      }

      // ─── Safe domains require explicit opt-in in config ──────────
      const safeDomains = config.call_safe_domains || [];
      if (safeDomains.length === 0) {
        console.error('\n⛔ Service calls are disabled by default.');
        console.error('   To enable, add allowed domains to "call_safe_domains" in hub.json:');
        console.error('   Example: "call_safe_domains": ["light", "climate", "scene"]');
        process.exit(1);
      }
      if (!safeDomains.includes(parts[0])) {
        console.error(`\n⛔ Service domain "${parts[0]}" is not in the safe domains list.`);
        console.error('   Add it to "call_safe_domains" in hub.json:');
        console.error(`   Example: "call_safe_domains": ["light", "climate", "scene", "${parts[0]}"]`);
        process.exit(1);
      }

      const data = {};
      for (const arg of args.slice(2)) {
        const [key, ...val] = arg.split('=');
        if (val.length) data[key] = val.join('=');
      }

      // ─── Dry-run mode: show what would be called without executing ──
      const dryRunIndex = args.indexOf('--dry-run');
      if (dryRunIndex !== -1) {
        console.log(`\n[DRY-RUN] Would call:`);
        console.log(`  Service: ${parts[0]}.${parts[1]}`);
        console.log(`  Target URL: ${config.ha_url}/api/services/${parts[0]}/${parts[1]}`);
        console.log(`  Payload: ${JSON.stringify(data, null, 2)}`);
        process.exit(0);
      }

      const result = await fetch(`/api/services/${parts[0]}/${parts[1]}`, 'POST', data);
      console.log(JSON.stringify(result, null, 2));
      break;
    }

    case 'scenes': {
      const all = await fetch('/api/states');
      const scenes = Array.isArray(all) ? all.filter(s => s.entity_id.startsWith('scene.')) : [];
      console.log(`\n${scenes.length} scenes:\n`);
      scenes.forEach(s => {
        console.log(`  ${s.entity_id} — ${s.attributes.friendly_name || s.entity_id}`);
      });
      break;
    }

    case 'persons': {
      const all = await fetch('/api/states');
      const persons = Array.isArray(all) ? all.filter(s => s.entity_id.startsWith('person.')) : [];
      console.log(`\n${persons.length} persons:\n`);
      persons.forEach(p => {
        console.log(`  ${p.entity_id} — state: ${p.state} (${p.attributes.friendly_name || '?'})`);
      });
      break;
    }

    case 'areas': {
      const all = await fetch('/api/states');
      const areas = new Map();
      if (Array.isArray(all)) {
        for (const s of all) {
          if (s.attributes?.area_id) {
            const areaName = s.attributes.friendly_name || s.attributes.area_id;
            if (!areas.has(areaName)) areas.set(areaName, []);
            areas.get(areaName).push(s.entity_id);
          }
        }
      }
      console.log(`\n${areas.size} areas:\n`);
      for (const [name, entities] of areas) {
        console.log(`  📍 ${name} (${entities.length} devices)`);
        entities.forEach(e => console.log(`    - ${e}`));
      }
      break;
    }

    case 'devices': {
      const all = await fetch('/api/states');
      const deviceIds = new Set();
      if (Array.isArray(all)) {
        for (const s of all) {
          if (s.attributes?.device_id) deviceIds.add(s.attributes.device_id);
        }
      }
      console.log(`\n${deviceIds.size} devices\n`);
      deviceIds.forEach(id => console.log(`  ${id}`));
      break;
    }

    case 'help':
    default:
      console.log(`Home Assistant Commands\n`);
      console.log('  info                        — HA info');
      console.log('  state [get|list|history]    — entity states');
      console.log('  call <domain.service>       — call a service');
      console.log('  scenes                      — list scenes');
      console.log('  persons                     — list persons');
      console.log('  areas                       — list areas with devices');
      console.log('  devices                     — list devices');
      console.log('  help                        — this help');
      break;
  }
}

main().catch(err => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
