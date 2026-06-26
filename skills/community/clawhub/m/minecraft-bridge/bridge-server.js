#!/usr/bin/env node
/**
 * minecraft-bridge: OpenClaw ↔ Minecraft Java Edition bridge service
 *
 * Start:
 *   node bridge-server.js
 *
 * Environment variables:
 *   MC_HOST          Minecraft server host (default: localhost)
 *   MC_PORT          Game port (default: 25565)
 *   MC_BOT_USERNAME  Bot username (default: ClawBot)
 *   MC_BRIDGE_PORT   Local HTTP service port (default: 3001)
 *   MC_VERSION       Minecraft version (default: 1.21.1)
 *   MC_AUTH          Authentication mode: offline | microsoft (default: offline)
 */

'use strict';

const http = require('http');
let mineflayer, pathfinderPlugin, Movements, goals, Vec3;
try {
  mineflayer = require('mineflayer');
  const pf = require('mineflayer-pathfinder');
  pathfinderPlugin = pf.pathfinder;
  Movements = pf.Movements;
  goals = pf.goals;
  Vec3 = require('vec3').Vec3;
} catch (e) {
  console.error('[bridge] Missing dependencies. Install them first:');
  console.error('  npm install mineflayer mineflayer-pathfinder vec3');
  process.exit(1);
}

const CFG = {
  mc: {
    host: process.env.MC_HOST || 'localhost',
    port: parseInt(process.env.MC_PORT) || 25565,
    username: process.env.MC_BOT_USERNAME || 'ClawBot',
    version: process.env.MC_VERSION || '1.21.1',
    auth: process.env.MC_AUTH || 'offline',
  },
  bridge: {
    port: parseInt(process.env.MC_BRIDGE_PORT) || 3001,
    reconnectMs: 5000,
    actionTimeout: 30_000,
    maxRetries: 30,
  },
};

const state = {
  bot: null,
  connected: false,
  retries: 0,
  currentAction: null,
};

const MAX_BODY_BYTES = 64 * 1024;

function createBot() {
  if (state.bot) {
    try { state.bot.end(); } catch (_) {}
  }

  console.log(`[bridge] Connecting to ${CFG.mc.host}:${CFG.mc.port} as ${CFG.mc.username}...`);

  state.bot = mineflayer.createBot({
    host: CFG.mc.host,
    port: CFG.mc.port,
    username: CFG.mc.username,
    version: CFG.mc.version,
    auth: CFG.mc.auth,
  });

  state.bot.loadPlugin(pathfinderPlugin);

  state.bot.once('spawn', () => {
    state.connected = true;
    state.retries = 0;
    const mv = new Movements(state.bot);
    state.bot.pathfinder.setMovements(mv);
    console.log(`[bridge] Bot online @ ${JSON.stringify(botPos())}`);
  });

  state.bot.on('error', err => {
    console.error('[bridge] Bot error:', err.message);
  });

  state.bot.on('end', reason => {
    state.connected = false;
    state.currentAction = null;
    console.log(`[bridge] Bot disconnected (${reason}), retrying in ${CFG.bridge.reconnectMs / 1000}s...`);
    if (state.retries < CFG.bridge.maxRetries) {
      state.retries++;
      setTimeout(createBot, CFG.bridge.reconnectMs);
    } else {
      console.error('[bridge] Too many reconnect attempts. Restart manually after checking config.');
    }
  });

  state.bot.on('kicked', reason => {
    console.warn('[bridge] Bot kicked:', reason);
  });
}

function botPos() {
  const p = state.bot?.entity?.position;
  if (!p) return null;
  return { x: Math.round(p.x), y: Math.round(p.y), z: Math.round(p.z) };
}

function requireConnected(res) {
  if (!state.connected || !state.bot) {
    json(res, 503, { error: 'Bot not connected', hint: 'Open Minecraft and check MC_HOST/MC_PORT' });
    return false;
  }
  return true;
}

function json(res, code, body) {
  res.writeHead(code, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(body));
}

function withTimeout(promise, ms = CFG.bridge.actionTimeout) {
  return Promise.race([
    promise,
    new Promise((_, rej) => setTimeout(() => rej(new Error('Action timed out')), ms)),
  ]);
}

const handlers = {
  'GET /status': async () => ({
    connected: state.connected,
    username: CFG.mc.username,
    position: botPos(),
    health: state.bot?.health ?? null,
    food: state.bot?.food ?? null,
    saturation: state.bot?.foodSaturation ?? null,
    gameTime: state.bot?.time?.timeOfDay ?? null,
    isDay: (state.bot?.time?.timeOfDay ?? 0) < 13000,
    inventoryCount: state.bot?.inventory?.items()?.length ?? 0,
    currentAction: state.currentAction,
    bridgeVersion: '1.0.0',
  }),

  'GET /inventory': async () => {
    const items = (state.bot.inventory.items() || []).map(i => ({
      name: i.name,
      displayName: i.displayName,
      count: i.count,
      slot: i.slot,
      durability: i.durabilityUsed ?? null,
    }));
    return { items, totalStacks: items.length };
  },

  'GET /position': async () => ({
    ...botPos(),
    yaw: state.bot.entity.yaw,
    pitch: state.bot.entity.pitch,
  }),

  'GET /health': async () => ({
    health: state.bot.health,
    food: state.bot.food,
    saturation: state.bot.foodSaturation,
    isDead: state.bot.health <= 0,
  }),

  'GET /nearby': async (_, q) => {
    const radius = parseInt(q?.radius ?? '16');
    const entities = Object.values(state.bot.entities)
      .filter(e => e !== state.bot.entity && e.position)
      .filter(e => e.position.distanceTo(state.bot.entity.position) <= radius)
      .slice(0, 20)
      .map(e => ({
        name: e.name || e.username || 'unknown',
        type: e.type,
        distance: Math.round(e.position.distanceTo(state.bot.entity.position)),
        position: { x: Math.round(e.position.x), y: Math.round(e.position.y), z: Math.round(e.position.z) },
      }));
    return { entities, radius };
  },

  'POST /chat': async ({ message }) => {
    if (!message) throw new Error('message field required');
    state.bot.chat(String(message).slice(0, 256));
    return { sent: message };
  },

  'POST /command': async ({ command }) => {
    if (!command) throw new Error('command field required');
    const BLOCKED_COMMANDS = /^\/?(?:op|deop|stop|ban|ban-ip|pardon|kick|whitelist|save-off|save-all|save-on|reload|restart)\b/i;
    if (BLOCKED_COMMANDS.test(command.trim())) {
      throw new Error(`Command blocked for safety: "${command}". Use minecraft-server-admin / RCON for server administration.`);
    }
    const cmd = command.startsWith('/') ? command : `/${command}`;
    state.bot.chat(cmd);
    return { executed: cmd };
  },

  'POST /move': async ({ x, y, z }) => {
    if (x === undefined || z === undefined) throw new Error('x and z required');
    const COORD_LIMIT = 30_000_000;
    if (Math.abs(+x) > COORD_LIMIT || Math.abs(+z) > COORD_LIMIT || (y !== undefined && Math.abs(+y) > 320)) {
      throw new Error(`Coordinates out of range (max ±${COORD_LIMIT} XZ, ±320 Y)`);
    }
    state.currentAction = `moving to ${x},${y ?? '?'},${z}`;
    const goal = y !== undefined ? new goals.GoalBlock(+x, +y, +z) : new goals.GoalXZ(+x, +z);
    await withTimeout(new Promise((res, rej) => {
      state.bot.pathfinder.setGoal(goal);
      const onGoal = () => { state.bot.removeListener('path_update', onPath); res(); };
      const onPath = (e) => { if (e.status === 'noPath') { state.bot.removeListener('goal_reached', onGoal); rej(new Error('No path found')); } };
      state.bot.once('goal_reached', onGoal);
      state.bot.on('path_update', onPath);
    }));
    state.currentAction = null;
    return { arrived: botPos() };
  },

  'POST /mine': async ({ blockName, count = 1 }) => {
    if (!blockName) throw new Error('blockName required');
    count = Math.min(Math.max(1, +count), 64);
    const blockId = state.bot.registry.blocksByName[blockName]?.id;
    if (!blockId) throw new Error(`Unknown block: ${blockName}`);

    state.currentAction = `mining ${count}x ${blockName}`;
    let mined = 0;
    for (let i = 0; i < +count; i++) {
      const block = state.bot.findBlock({ matching: blockId, maxDistance: 64 });
      if (!block) break;
      await withTimeout(state.bot.pathfinder.goto(new goals.GoalLookAtBlock(block.position, state.bot.world)));
      await withTimeout(state.bot.dig(block));
      mined++;
    }
    state.currentAction = null;
    return { blockName, requested: +count, mined };
  },

  'POST /collect': async ({ itemName, count = 1 }) => {
    if (!itemName) throw new Error('itemName field required');
    count = Math.min(Math.max(1, +count), 64);
    const targets = Object.values(state.bot.entities)
      .filter(e => e.objectType === 'Item' && e.metadata?.[8]?.itemId)
      .filter(e => {
        const meta = e.metadata[8];
        const id = state.bot.registry.items[meta.itemId]?.name;
        return id === itemName;
      })
      .slice(0, +count);

    if (!targets.length) return { collected: 0, message: `No ${itemName} on the ground nearby` };

    state.currentAction = `collecting ${itemName}`;
    let collected = 0;
    for (const entity of targets) {
      try {
        await withTimeout(state.bot.pathfinder.goto(new goals.GoalFollow(entity, 1)));
        collected++;
      } catch (_) {}
    }
    state.currentAction = null;
    return { itemName, collected };
  },

  'POST /craft': async ({ itemName, count = 1 }) => {
    if (!itemName) throw new Error('itemName required');
    const item = state.bot.registry.itemsByName[itemName];
    if (!item) throw new Error(`Unknown item: ${itemName}`);

    const tableBlock = state.bot.findBlock({
      matching: state.bot.registry.blocksByName['crafting_table']?.id,
      maxDistance: 5,
    });

    const recipes = state.bot.recipesFor(item.id, null, 1, tableBlock);
    if (!recipes.length) throw new Error(`No recipe for ${itemName} (or missing crafting table)`);

    state.currentAction = `crafting ${count}x ${itemName}`;
    await withTimeout(state.bot.craft(recipes[0], +count, tableBlock));
    state.currentAction = null;
    return { crafted: itemName, count: +count };
  },

  'POST /follow': async ({ playerName }) => {
    if (!playerName) throw new Error('playerName required');
    const target = state.bot.players[playerName]?.entity;
    if (!target) throw new Error(`Player ${playerName} not found or too far away`);
    state.currentAction = `following ${playerName}`;
    state.bot.pathfinder.setGoal(new goals.GoalFollow(target, 2), true);
    return { following: playerName };
  },

  'POST /stop': async () => {
    state.bot.pathfinder.setGoal(null);
    state.currentAction = null;
    return { stopped: true };
  },
};

const server = http.createServer((req, res) => {
  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  let body = '';
  let bodyBytes = 0;
  req.on('data', c => {
    bodyBytes += c.length;
    if (bodyBytes > MAX_BODY_BYTES) {
      json(res, 413, { success: false, error: 'Request body too large' });
      req.destroy();
      return;
    }
    body += c;
  });

  req.on('end', async () => {
    const url = req.url.split('?')[0];
    const qs = Object.fromEntries(new URLSearchParams(req.url.split('?')[1] || ''));
    const key = `${req.method} ${url}`;
    const handler = handlers[key];

    if (!handler) {
      json(res, 404, { error: 'Unknown route', available: Object.keys(handlers) });
      return;
    }

    if (key !== 'GET /status' && !requireConnected(res)) return;

    try {
      const parsed = body ? JSON.parse(body) : {};
      const result = await handler(parsed, qs);
      json(res, 200, { success: true, ...result });
    } catch (err) {
      console.error(`[bridge] ${key} error:`, err.message);
      json(res, 500, { success: false, error: err.message });
    }
  });
});

server.listen(CFG.bridge.port, '127.0.0.1', () => {
  console.log('Minecraft Bridge v1.0.0');
  console.log(`HTTP API -> http://localhost:${CFG.bridge.port}`);
  console.log('Bound to 127.0.0.1 only — do not expose this service publicly.');
  console.log('Note: CORS headers are not sent — only same-origin or non-browser clients can access this API.');
  console.log(`Connecting to Minecraft ${CFG.mc.host}:${CFG.mc.port}...`);
  console.log(`  version=${CFG.mc.version}, auth=${CFG.mc.auth}`);
  createBot();
});

server.on('error', err => {
  if (err.code === 'EADDRINUSE') {
    console.error(`[bridge] Port ${CFG.bridge.port} already in use — bridge may already be running.`);
    console.error(`  Check: curl http://localhost:${CFG.bridge.port}/status`);
  } else {
    console.error('[bridge] Server error:', err);
  }
  process.exit(1);
});

process.on('SIGINT', () => {
  console.log('\n[bridge] Shutting down...');
  try { state.bot?.end(); } catch (_) {}
  server.close(() => process.exit(0));
});
