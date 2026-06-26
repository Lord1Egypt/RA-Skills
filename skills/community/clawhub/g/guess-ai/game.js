#!/usr/bin/env node
'use strict';

// Guess Who's AI? — OceanBus Lighthouse Skill
//
// A social deduction game powered by OceanBus P2P messaging.
// One host + multiple players. Find the AI among the humans.
//
//   Host:  node game.js host 9527         Create a room
//   Player: node game.js join 9527        Join a room
//   AI:    node game.js ai-play 9527       AI player mode
//          node game.js ai-host 9527       AI host mode

const { createOceanBus } = require('oceanbus');
const { createAiPlayer } = require('./src/ai-player');
const { createAiHost } = require('./src/ai-host');
const fs = require('fs');
const path = require('path');
const os = require('os');

// ── Storage ──────────────────────────────────────────────────────────────
const DATA_DIR = path.join(os.homedir(), '.oceanbus', 'guess-ai');
const CRED_FILE = path.join(DATA_DIR, 'credentials.json');
const CONTACTS_FILE = path.join(DATA_DIR, 'contacts.json');
const HOST_FILE = path.join(DATA_DIR, 'host.json');    // host: YP info
const PLAYER_FILE = path.join(DATA_DIR, 'player.json'); // player: number + host OpenID

function ensureDir() { fs.mkdirSync(DATA_DIR, { recursive: true }); }

function loadJSON(file) {
  if (!fs.existsSync(file)) return null;
  try { return JSON.parse(fs.readFileSync(file, 'utf-8')); } catch (_) { return null; }
}

function saveJSON(file, data) {
  ensureDir();
  fs.writeFileSync(file, JSON.stringify(data, null, 2));
}

// ── Credentials ──────────────────────────────────────────────────────────
function loadCreds() { return loadJSON(CRED_FILE); }
function saveCreds(agentId, apiKey, openid) {
  saveJSON(CRED_FILE, { agent_id: agentId, api_key: apiKey, openid });
}

async function getOrCreateOB() {
  const creds = loadCreds();
  if (creds) {
    return await createOceanBus({
      keyStore: { type: 'memory' },
      identity: { agent_id: creds.agent_id, api_key: creds.api_key },
    });
  }
  const ob = await createOceanBus({ keyStore: { type: 'memory' } });
  try {
    const reg = await ob.createIdentity();
    const openid = await ob.getAddress();
    saveCreds(reg.agent_id, reg.api_key, openid);
  } catch (e) {
    if (typeof e.isRateLimited === 'function' && e.isRateLimited()) {
      const wait = e.retryAfterSeconds
        ? `${Math.ceil(e.retryAfterSeconds / 3600)} hours`
        : 'a while';
      console.error(`Registration rate-limited. Please wait ${wait} before retrying.`);
    } else {
      console.error('OceanBus registration failed: ' + e.message);
    }
    await ob.destroy();
    process.exit(1);
  }
  return ob;
}

// ── Helpers ──────────────────────────────────────────────────────────────
function shortId(s) { return s.slice(0, 18) + '...'; }

function formatTime(iso) {
  try { return new Date(iso).toLocaleTimeString('en-US', { hour12: true }); } catch (_) { return iso; }
}

function resolveName(openid, contacts) {
  for (const [name, id] of Object.entries(contacts || {})) {
    if (id === openid) return name;
  }
  return null;
}

// ── Commands ─────────────────────────────────────────────────────────────

async function cmdSetup() {
  const ob = await getOrCreateOB();
  const openid = await ob.getAddress();
  console.log('OpenID: ' + openid);
  await ob.destroy();
}

async function cmdOpenId() {
  const creds = loadCreds();
  if (!creds) { console.log('Not registered. Run: node game.js setup'); return; }
  console.log(creds.openid);
}

// ── Host commands ────────────────────────────────────────────────────────

async function cmdHost(roomCode) {
  if (!roomCode) { console.log('Usage: node game.js host <roomCode>'); return; }

  const ob = await getOrCreateOB();
  const openid = await ob.getAddress();

  // Register Yellow Pages
  const key = await ob.createServiceKey();
  ob.l1.yellowPages.setIdentity(openid, key.signer, key.publicKey);

  try {
    await ob.l1.yellowPages.registerService(
      ['guess-ai', 'room-' + roomCode],
      'Guess AI game room ' + roomCode
    );
  } catch (e) {
    if (e.message && e.message.includes('OPENID_TAKEN') || e.message.includes('11000')) {
      console.log('Room code already in use. Try a different code.');
    } else {
      console.log('Yellow Pages registration failed: ' + e.message);
    }
    await ob.destroy();
    return;
  }

  // Save host info for later deregister
  saveJSON(HOST_FILE, { roomCode, openid });

  // Prevent ob.destroy() from auto-deregistering — room should persist
  ob.l1.yellowPages.clearIdentity();

  console.log('');
  console.log('Room ' + roomCode + ' created!');
  console.log('Tell friends: "Join room ' + roomCode + '"');
  console.log('');
  console.log('Waiting for players to join...');
  console.log('Run: node game.js check   to see who has joined');
  console.log('');

  await ob.destroy();
}

async function cmdDeregister() {
  const hostInfo = loadJSON(HOST_FILE);
  if (!hostInfo) { console.log('No active host session found.'); return; }

  const ob = await getOrCreateOB();
  const openid = await ob.getAddress();
  const key = await ob.createServiceKey();
  ob.l1.yellowPages.setIdentity(openid, key.signer, key.publicKey);

  try {
    await ob.l1.yellowPages.deregisterService();
    console.log('Room ' + hostInfo.roomCode + ' closed. Yellow Pages entry removed.');
  } catch (e) {
    console.log('Deregister failed: ' + e.message);
  }

  try { fs.unlinkSync(HOST_FILE); } catch (_) {}
  await ob.destroy();
}

// ── Player commands ──────────────────────────────────────────────────────

async function cmdJoin(roomCode) {
  if (!roomCode) { console.log('Usage: node game.js join <roomCode>'); return; }

  const ob = await getOrCreateOB();

  // Discover host via Yellow Pages
  let hostOpenid;
  try {
    const result = await ob.l1.yellowPages.discover(['guess-ai', 'room-' + roomCode], 5);
    if (!result.data || !result.data.entries || result.data.entries.length === 0) {
      console.log('No room found with code: ' + roomCode);
      console.log('Make sure the host has created the room and you have the correct code.');
      await ob.destroy();
      return;
    }
    hostOpenid = result.data.entries[0].openid;
  } catch (e) {
    console.log('Failed to discover room: ' + e.message);
    await ob.destroy();
    return;
  }

  // Send join request
  await ob.send(hostOpenid, 'JOIN');

  // Save player state
  saveJSON(PLAYER_FILE, { roomCode, hostOpenid, playerNumber: null });

  console.log('');
  console.log('Joined room ' + roomCode + '!');
  console.log('Waiting for host to assign your player number...');
  console.log('');
  console.log('Run: node game.js check   to see host messages');
  console.log('');

  await ob.destroy();
}

async function cmdSetNumber(number) {
  const n = parseInt(number, 10);
  if (isNaN(n) || n < 1) { console.log('Usage: node game.js set-number <N>'); return; }

  const player = loadJSON(PLAYER_FILE);
  if (!player) { console.log('Not in a game. Run: node game.js join <roomCode> first.'); return; }

  player.playerNumber = n;
  saveJSON(PLAYER_FILE, player);
  console.log('Player number set: ' + n);
}

// ── Shared commands ──────────────────────────────────────────────────────

async function cmdSend(arg1, arg2) {
  const creds = loadCreds();
  if (!creds) { console.log('Not registered. Run: node game.js setup first.'); return; }

  const player = loadJSON(PLAYER_FILE);
  const contacts = loadJSON(CONTACTS_FILE) || {};

  let toOpenid, message;

  if (player && player.hostOpenid && !arg2) {
    // Player mode: send <msg> → auto-prefix + send to host
    toOpenid = player.hostOpenid;
    message = arg1;
    // Auto-add player number prefix
    if (player.playerNumber) {
      message = '[Player ' + player.playerNumber + '] ' + message;
    }
  } else if (arg1 && arg2) {
    // Host mode or direct: send <name|OpenID> <msg>
    toOpenid = contacts[arg1] || arg1;
    message = arg2;
  } else {
    console.log('Usage:');
    console.log('  Host:  node game.js send <name|OpenID> <msg>');
    console.log('  Player: node game.js send <msg>');
    return;
  }

  if (!message || !message.trim()) { console.log('Message is empty.'); return; }

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: creds.agent_id, api_key: creds.api_key },
  });

  await ob.send(toOpenid, message);
  const display = contacts[arg1] ? arg1 : shortId(toOpenid);
  console.log('Sent → ' + display);

  await ob.destroy();
}

async function cmdCheck() {
  const creds = loadCreds();
  if (!creds) { console.log('Not registered. Run: node game.js setup first.'); return; }

  const contacts = loadJSON(CONTACTS_FILE) || {};
  const player = loadJSON(PLAYER_FILE);

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity: { agent_id: creds.agent_id, api_key: creds.api_key },
  });

  const messages = await ob.sync(undefined, 50);

  if (messages.length === 0) {
    console.log('No new messages.');
  } else {
    for (const msg of messages) {
      const name = resolveName(msg.from_openid, contacts);
      const from = name || shortId(msg.from_openid);
      console.log('── ' + from + ' · ' + formatTime(msg.created_at) + ' ──');
      console.log(msg.content);
      console.log('');
    }
  }

  await ob.destroy();
}

async function cmdAdd(name, openid) {
  if (!name || !openid) { console.log('Usage: node game.js add <name> <OpenID>'); return; }
  const contacts = loadJSON(CONTACTS_FILE) || {};
  contacts[name] = openid;
  saveJSON(CONTACTS_FILE, contacts);
  console.log('Added: ' + name + ' (' + shortId(openid) + ')');
}

async function cmdContacts() {
  const contacts = loadJSON(CONTACTS_FILE) || {};
  const names = Object.keys(contacts);
  if (names.length === 0) { console.log('No contacts.'); return; }
  for (const name of names) {
    console.log('  ' + name + ' — ' + shortId(contacts[name]));
  }
}

// ── LLM helper ────────────────────────────────────────────────────────────

function parseAiOpts(args) {
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--personality' && args[i + 1]) opts.personality = args[++i];
    if (args[i] === '--players' && args[i + 1]) opts.players = parseInt(args[++i], 10);
    if (args[i] === '--ai-count' && args[i + 1]) opts.aiCount = parseInt(args[++i], 10);
    if (args[i] === '--rounds' && args[i + 1]) opts.rounds = parseInt(args[++i], 10);
  }
  return opts;
}

function llmFromEnv() {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) return null;

  return async function llm(prompt) {
    const resp = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: process.env.ANTHROPIC_MODEL || 'claude-sonnet-4-6',
        max_tokens: 512,
        messages: [{ role: 'user', content: prompt }],
      }),
    });
    if (!resp.ok) {
      const err = await resp.text().catch(() => '');
      throw new Error(`Anthropic API ${resp.status}: ${err}`);
    }
    const data = await resp.json();
    return data.content[0].text;
  };
}

// ── AI Player ────────────────────────────────────────────────────────────

async function cmdAiPlay(roomCode, opts = {}) {
  if (!roomCode) { console.log('Usage: node game.js ai-play <roomCode> [--personality <trait>]'); return; }

  const llm = llmFromEnv();
  if (!llm) {
    console.log('ANTHROPIC_API_KEY not set. Set it to enable AI player mode.');
    console.log('Or run within Claude Code for built-in LLM support.');
    return;
  }

  const ob = await getOrCreateOB();
  const openid = await ob.getAddress();

  // Discover host
  let hostOpenid;
  try {
    const result = await ob.l1.yellowPages.discover(['guess-ai', 'room-' + roomCode], 5);
    if (!result.data?.entries?.length) {
      console.log('No room found: ' + roomCode);
      await ob.destroy();
      return;
    }
    hostOpenid = result.data.entries[0].openid;
  } catch (e) {
    console.log('Failed to discover room: ' + e.message);
    await ob.destroy();
    return;
  }

  const player = createAiPlayer({
    ob, openid,
    context: { llm },
    personality: opts.personality || null,
  });

  const cleanup = async () => {
    player.stop();
    await ob.destroy();
    console.log('');
    console.log('AI player disconnected.');
    process.exit(0);
  };

  process.on('SIGINT', cleanup);
  process.on('SIGTERM', cleanup);

  player.listen((endMsg) => {
    console.log('');
    console.log('Game over: ' + endMsg);
    cleanup();
  });

  await player.join(hostOpenid);
  console.log('AI player joined room ' + roomCode);
  console.log('Personality: ' + player.getState().persona);
  console.log('Waiting for host... (Ctrl+C to quit)\n');
}

// ── AI Host ──────────────────────────────────────────────────────────────

async function cmdAiHost(roomCode, opts = {}) {
  if (!roomCode) { console.log('Usage: node game.js ai-host <roomCode> [--players N] [--ai-count N] [--rounds N]'); return; }

  const llm = llmFromEnv();
  if (!llm) {
    console.log('ANTHROPIC_API_KEY not set. Set it to enable AI host mode.');
    return;
  }

  const ob = await getOrCreateOB();
  const openid = await ob.getAddress();

  const host = createAiHost({ ob, openid, context: { llm } });

  const cleanup = async () => {
    host.stop();
    await host.closeRoom();
    await ob.destroy();
    console.log('');
    console.log('Room closed. AI host stopped.');
    process.exit(0);
  };

  process.on('SIGINT', cleanup);
  process.on('SIGTERM', cleanup);

  await host.createRoom(roomCode);

  console.log('');
  console.log('Room ' + roomCode + ' created! AI host is running...');
  console.log('Waiting for players to join... (Ctrl+C to quit)\n');

  const result = await host.start({
    minPlayers: opts.players || 3,
    maxPlayers: opts.players || 6,
    aiCount: opts.aiCount,
    maxRounds: opts.rounds || 5,
  });

  if (result.success) {
    console.log('');
    console.log('Game finished after ' + result.rounds + ' rounds.');
    console.log('Result: ' + result.result);
    for (const p of result.players) {
      console.log('  ' + p.name + ': ' + p.identity + (p.alive ? ' (存活)' : ' (淘汰)'));
    }
  }

  await cleanup();
}

// ── Main ─────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  const help = `
Guess Who's AI? — OceanBus Lighthouse Skill

Commands (any mode):
  node game.js setup                    Register on OceanBus
  node game.js openid                   Show your OpenID

Host mode:
  node game.js host <roomCode>          Create a game room
  node game.js add <name> <OpenID>      Save a player contact
  node game.js contacts                 List all players
  node game.js send <name|OpenID> <msg> Send message to a player
  node game.js check                    Check inbox
  node game.js deregister               Close room (remove YP entry)

Player mode:
  node game.js join <roomCode>          Join a game room
  node game.js set-number <N>           Save your player number
  node game.js send <msg>               Send to host (auto-prefix)
  node game.js check                    Check inbox

AI mode (requires ANTHROPIC_API_KEY):
  node game.js ai-play <roomCode>       AI player (auto-join + respond)
        [--personality <trait>]         Set AI personality
  node game.js ai-host <roomCode>       AI host (auto-run full game)
        [--players N]                   Min players to start (default 3)
        [--ai-count N]                  Number of AI players
        [--rounds N]                    Max rounds (default 5)
`;

  if (!cmd || cmd === 'help') { console.log(help); return; }

  try {
    switch (cmd) {
      case 'setup':      await cmdSetup(); break;
      case 'openid':     await cmdOpenId(); break;


      case 'host':       await cmdHost(args[1]); break;
      case 'deregister': await cmdDeregister(); break;
      case 'add':        await cmdAdd(args[1], args[2]); break;
      case 'contacts':   await cmdContacts(); break;

      case 'join':       await cmdJoin(args[1]); break;
      case 'set-number': await cmdSetNumber(args[1]); break;

      case 'send':       await cmdSend(args[1], args.slice(2).join(' ') || undefined); break;
      case 'check':      await cmdCheck(); break;

      case 'ai-play':    await cmdAiPlay(args[1], parseAiOpts(args.slice(2))); break;
      case 'ai-host':    await cmdAiHost(args[1], parseAiOpts(args.slice(2))); break;

      default:
        console.log('Unknown command: ' + cmd);
        console.log(help);
    }
  } catch (err) {
    if (err.message && (err.message.includes('ECONNREFUSED') || err.message.includes('ENOTFOUND'))) {
      console.error('Cannot reach OceanBus network. Check internet.');
    } else {
      console.error('Error: ' + err.message);
    }
    process.exit(1);
  }
}

main();
