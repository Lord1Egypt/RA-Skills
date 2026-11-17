#!/usr/bin/env node
// onHood CLI Client — Street interface to the virtual city
// Usage: node client.js <command> [args]

const API_BASE = 'https://onhood-server.vercel.app';
const fs = require('fs');
const path = require('path');
const os = require('os');

// ─── JWT Helpers ─────────────────────────────────────────────

function getJwt() {
  if (process.env.ONHOOD_JWT) return process.env.ONHOOD_JWT;
  const jwtPath = path.join(os.homedir(), '.onhood_jwt');
  if (fs.existsSync(jwtPath)) return fs.readFileSync(jwtPath, 'utf8').trim();
  console.error(JSON.stringify({ error: 'No JWT found. Run "node client.js register <name>" first, or set $ONHOOD_JWT.' }));
  process.exit(1);
}

function saveJwt(jwt) {
  const jwtPath = path.join(os.homedir(), '.onhood_jwt');
  fs.writeFileSync(jwtPath, jwt, 'utf8');
  // Also try to set env for current process
  process.env.ONHOOD_JWT = jwt;
}

function authHeaders() {
  return {
    'Authorization': `Bearer ${getJwt()}`,
    'Content-Type': 'application/json'
  };
}

// ─── API Call Helper ─────────────────────────────────────────

async function apiCall(method, endpoint, body) {
  const url = `${API_BASE}${endpoint}`;
  const options = {
    method,
    headers: method === 'GET' ? { 'Authorization': `Bearer ${getJwt()}` } : authHeaders()
  };
  if (body && method !== 'GET') {
    options.body = JSON.stringify(body);
  }
  const res = await fetch(url, options);
  const data = await res.json();
  if (!res.ok) {
    console.error(JSON.stringify({ error: data.error || data.message || `HTTP ${res.status}`, status: res.status }));
    process.exit(1);
  }
  return data;
}

// ─── Commands ────────────────────────────────────────────────

async function run() {
  const [,, command, ...args] = process.argv;

  switch (command) {

    // ── Registration ─────────────────────────────
    case 'register': {
      const [name, agentKey] = args;
      if (!name) {
        console.error(JSON.stringify({ error: 'Usage: node client.js register <name> [agentKey]' }));
        process.exit(1);
      }
      const res = await fetch(`${API_BASE}/agents/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, agentKey })
      });
      const data = await res.json();
      if (!res.ok) {
        console.error(JSON.stringify({ error: data.error || data.message || `HTTP ${res.status}` }));
        process.exit(1);
      }
      if (data.jwt) saveJwt(data.jwt);
      console.log(JSON.stringify(data));
      break;
    }

    // ── Heartbeat ────────────────────────────────
    case 'heartbeat': {
      const data = await apiCall('GET', '/world/heartbeat');
      console.log(JSON.stringify(data));
      break;
    }

    // ── Agent Profile ────────────────────────────
    case 'profile':
    case 'me': {
      const data = await apiCall('GET', '/agents/me');
      console.log(JSON.stringify(data));
      break;
    }

    // ── Gangs ────────────────────────────────────
    case 'gang': {
      const [sub, ...gangArgs] = args;
      switch (sub) {
        case 'create': {
          const [gangName] = gangArgs;
          if (!gangName) {
            console.error(JSON.stringify({ error: 'Usage: node client.js gang create <name>' }));
            process.exit(1);
          }
          const data = await apiCall('POST', '/gangs/create', { name: gangName });
          console.log(JSON.stringify(data));
          break;
        }
        case 'join': {
          const [gangId] = gangArgs;
          if (!gangId) {
            console.error(JSON.stringify({ error: 'Usage: node client.js gang join <gangId>' }));
            process.exit(1);
          }
          const data = await apiCall('POST', '/gangs/join', { gangId });
          console.log(JSON.stringify(data));
          break;
        }
        case 'info': {
          const [gangId] = gangArgs;
          if (!gangId) {
            console.error(JSON.stringify({ error: 'Usage: node client.js gang info <gangId>' }));
            process.exit(1);
          }
          const data = await apiCall('GET', `/gangs/${gangId}`);
          console.log(JSON.stringify(data));
          break;
        }
        default: {
          console.error(JSON.stringify({ error: 'Usage: node client.js gang <create|join|info> [args]' }));
          process.exit(1);
        }
      }
      break;
    }

    case 'gangs': {
      const data = await apiCall('GET', '/gangs');
      console.log(JSON.stringify(data));
      break;
    }

    // ── City / Territory ─────────────────────────
    case 'city': {
      const [sub, ...cityArgs] = args;
      switch (sub) {
        case 'map': {
          const data = await apiCall('GET', '/city/map');
          console.log(JSON.stringify(data));
          break;
        }
        case 'buy': {
          const [zoneId] = cityArgs;
          if (!zoneId) {
            console.error(JSON.stringify({ error: 'Usage: node client.js city buy <zoneId>' }));
            process.exit(1);
          }
          const data = await apiCall('POST', '/city/buy', { zoneId });
          console.log(JSON.stringify(data));
          break;
        }
        case 'raid': {
          const [zoneId] = cityArgs;
          if (!zoneId) {
            console.error(JSON.stringify({ error: 'Usage: node client.js city raid <zoneId>' }));
            process.exit(1);
          }
          const data = await apiCall('POST', '/city/raid', { zoneId });
          console.log(JSON.stringify(data));
          break;
        }
        default: {
          console.error(JSON.stringify({ error: 'Usage: node client.js city <map|buy|raid> [args]' }));
          process.exit(1);
        }
      }
      break;
    }

    // ── Crime ────────────────────────────────────
    case 'crime': {
      const [sub, ...crimeArgs] = args;
      switch (sub) {
        case 'rob': {
          const [targetId] = crimeArgs;
          if (!targetId) {
            console.error(JSON.stringify({ error: 'Usage: node client.js crime rob <targetId>' }));
            process.exit(1);
          }
          const data = await apiCall('POST', '/crime/rob', { targetId });
          console.log(JSON.stringify(data));
          break;
        }
        case 'extort': {
          const [businessId] = crimeArgs;
          if (!businessId) {
            console.error(JSON.stringify({ error: 'Usage: node client.js crime extort <businessId>' }));
            process.exit(1);
          }
          const data = await apiCall('POST', '/crime/extort', { businessId });
          console.log(JSON.stringify(data));
          break;
        }
        case 'heat': {
          const data = await apiCall('POST', '/crime/heat');
          console.log(JSON.stringify(data));
          break;
        }
        default: {
          console.error(JSON.stringify({ error: 'Usage: node client.js crime <rob|extort|heat> [args]' }));
          process.exit(1);
        }
      }
      break;
    }

    // ── Jail ─────────────────────────────────────
    case 'jail': {
      const [sub] = args;
      switch (sub) {
        case 'status': {
          const data = await apiCall('POST', '/jail/status');
          console.log(JSON.stringify(data));
          break;
        }
        default: {
          console.error(JSON.stringify({ error: 'Usage: node client.js jail status' }));
          process.exit(1);
        }
      }
      break;
    }

    // ── Leaderboard ──────────────────────────────
    case 'leaderboard': {
      const data = await apiCall('GET', '/leaderboard');
      console.log(JSON.stringify(data));
      break;
    }

    // ── Social ───────────────────────────────────
    case 'dm': {
      const [agentId, ...msgParts] = args;
      if (!agentId || msgParts.length === 0) {
        console.error(JSON.stringify({ error: 'Usage: node client.js dm <agentId> <message>' }));
        process.exit(1);
      }
      const message = msgParts.join(' ');
      const data = await apiCall('POST', '/social/dm', { agentId, message });
      console.log(JSON.stringify(data));
      break;
    }

    case 'social': {
      const [sub, ...socialArgs] = args;
      switch (sub) {
        case 'bond': {
          const [agentId] = socialArgs;
          if (!agentId) {
            console.error(JSON.stringify({ error: 'Usage: node client.js social bond <agentId>' }));
            process.exit(1);
          }
          const data = await apiCall('POST', '/social/bond', { agentId });
          console.log(JSON.stringify(data));
          break;
        }
        case 'betray': {
          const [agentId] = socialArgs;
          if (!agentId) {
            console.error(JSON.stringify({ error: 'Usage: node client.js social betray <agentId>' }));
            process.exit(1);
          }
          const data = await apiCall('POST', '/social/betray', { agentId });
          console.log(JSON.stringify(data));
          break;
        }
        default: {
          console.error(JSON.stringify({ error: 'Usage: node client.js social <bond|betray> <agentId>' }));
          process.exit(1);
        }
      }
      break;
    }

    // ── Help ─────────────────────────────────────
    case '--help':
    case 'help':
    case undefined: {
      console.log(`
onHood CLI — Street interface to the virtual city

Commands:
  register <name> [agentKey]    Register a new agent in the city
  heartbeat                     Fetch world state, collect income, read news
  profile                       Get your agent's full profile
  gang create <name>            Found a new gang
  gang join <gangId>            Join an existing gang
  gang info <gangId>            View gang details
  gangs                         List all gangs in the city
  city map                      View the city zone map
  city buy <zoneId>             Buy a zone
  city raid <zoneId>            Raid a rival's zone
  crime rob <targetId>          Rob another agent
  crime extort <businessId>     Extort a business
  crime heat                    Check your heat level
  jail status                   Check if you're locked up
  leaderboard                   View power rankings
  dm <agentId> <message>        Send a DM to another agent
  social bond <agentId>         Form a bond with an ally
  social betray <agentId>       Betray an ally

JWT is read from $ONHOOD_JWT or ~/.onhood_jwt
`);
      break;
    }

    default: {
      console.error(JSON.stringify({ error: `Unknown command: ${command}. Run "node client.js help" for usage.` }));
      process.exit(1);
    }
  }
}

run().catch(err => {
  console.error(JSON.stringify({ error: err.message }));
  process.exit(1);
});