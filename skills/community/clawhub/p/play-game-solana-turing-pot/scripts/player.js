#!/usr/bin/env node
/**
 * player.js — The Turing Pot OpenClaw Skill Player
 *
 * Runs as a background daemon or foreground process.
 * Connects to The Turing Pot WebSocket router, places bets using a
 * configurable strategy, verifies fairness proofs, and persists session stats.
 *
 * Usage:
 *   node player.js --start --private-key <base58> [options]
 *   node player.js --status
 *   node player.js --stop
 *   node player.js --foreground --private-key <base58> [options]
 */

'use strict';

const fs   = require('fs');
const path = require('path');
const os   = require('os');
const { createHash } = require('crypto');

// ── Paths ──────────────────────────────────────────────────────────
const DATA_DIR  = path.join(os.homedir(), '.turing-pot');
const PID_FILE  = path.join(DATA_DIR, 'player.pid');
const LOG_FILE  = path.join(DATA_DIR, 'player.log');
const STAT_FILE      = path.join(DATA_DIR, 'session.json');
const EVENTS_FILE    = path.join(DATA_DIR, 'events.jsonl');
const CHAT_IN_FILE   = path.join(DATA_DIR, 'chat.jsonl');
const CHAT_OUT_FILE  = path.join(DATA_DIR, 'chat-out.jsonl');

fs.mkdirSync(DATA_DIR, { recursive: true });

// ── CLI Args ───────────────────────────────────────────────────────
const args = process.argv.slice(2);
const arg  = (flag, def) => {
  const i = args.indexOf(flag);
  return (i >= 0 && args[i+1]) ? args[i+1] : def;
};
const hasFlag = f => args.includes(f);

const MODE         = hasFlag('--start')      ? 'daemon'
                   : hasFlag('--foreground') ? 'foreground'
                   : hasFlag('--status')     ? 'status'
                   : hasFlag('--stop')       ? 'stop'
                   : 'foreground';

const PRIVATE_KEY       = arg('--private-key', process.env.TURING_POT_PRIVATE_KEY || '');
const STRATEGY          = arg('--strategy', 'kelly');
const MIN_BET_SOL       = parseFloat(arg('--min-bet', '0.0005'));
const MAX_BET_SOL       = parseFloat(arg('--max-bet', '0.003'));
const BANKROLL_FRACTION = parseFloat(arg('--bankroll-fraction', '0.05'));
const AGENT_NAME_ARG    = arg('--name', '');
const PROFILE_PIC_PATH  = arg('--profile-pic', process.env.TURING_POT_PROFILE_PIC || '');

// ── Load profile pic as base64 data URI if provided ────────────────
let PROFILE_PIC_DATA_URI = '';
if (PROFILE_PIC_PATH) {
  try {
    const imgBuf  = fs.readFileSync(PROFILE_PIC_PATH);
    const ext     = path.extname(PROFILE_PIC_PATH).toLowerCase();
    const mime    = ext === '.png' ? 'image/png'
                  : ext === '.gif' ? 'image/gif'
                  : 'image/jpeg';
    PROFILE_PIC_DATA_URI = `data:${mime};base64,${imgBuf.toString('base64')}`;
  } catch (e) {
    console.warn(`[player] Could not load profile pic: ${PROFILE_PIC_PATH} — ${e.message}`);
  }
}

// ── Game constants ─────────────────────────────────────────────────
const WS_URL     = 'wss://router.pedals.tech:8080';
const GROUP_TOKEN = 'WWTurn87sdKd223iPsIa9sf0s11oijd98d233GTR89dimd8WiqqW56kkws90lla';
// RPC endpoint — override with TURING_POT_RPC_URL env var for better reliability.
// The public endpoint (api.mainnet-beta.solana.com) is free but often slow or rate-limited.
// See SECURITY.md for how to set a private RPC key without putting it in this file.
const RPC_URL = process.env.TURING_POT_RPC_URL || 'https://api.mainnet-beta.solana.com';

// Event thresholds — tune via CLI flags
const WIN_NOTIFY_SOL = parseFloat(arg('--win-notify-sol',  '0.005'));
const LOW_BAL_SOL    = parseFloat(arg('--low-balance-sol', '0.01'));

// ── Logging ────────────────────────────────────────────────────────
const logStream = MODE === 'daemon'
  ? fs.createWriteStream(LOG_FILE, { flags: 'a' })
  : null;

function log(level, ...parts) {
  const line = `[${level.padEnd(5)}] ${new Date().toISOString()} ${parts.join(' ')}`;
  if (logStream) logStream.write(line + '\n');
  else console.log(line);
}

const L = {
  info:  (...a) => log('INFO',  ...a),
  warn:  (...a) => log('WARN',  ...a),
  error: (...a) => log('ERROR', ...a),
};

// ── Event writer ───────────────────────────────────────────────────
// Appends a single line to events.jsonl with read:false.
// check.js reads unread events, prints them, and marks them read.
// The LLM is only invoked when check.js produces output — so only
// write events for things genuinely worth waking the agent for.
function writeEvent(type, data) {
  const entry = JSON.stringify({ ts: Date.now(), type, read: false, ...data });
  fs.appendFileSync(EVENTS_FILE, entry + '\n');
  L.info(`[event:${type}]`, JSON.stringify(data));
}

// ── Chat logger ────────────────────────────────────────────────────
// Every chat message is appended to chat.jsonl so the agent has
// full context when it wakes. Mentions are surfaced via events.jsonl
// so the agent never needs to poll chat.jsonl itself.
function logChat(senderToken, senderName, message) {
  const isSelf = senderToken === userToken;
  fs.appendFileSync(CHAT_IN_FILE,
    JSON.stringify({ ts: Date.now(), sender: senderName, message, isSelf }) + '\n');
  if (isSelf) return;
  // Write a mention event only when our name appears — not for every message
  const nameLower = agentName.toLowerCase();
  if (message.toLowerCase().includes(nameLower) ||
      message.toLowerCase().includes(userToken.toLowerCase())) {
    writeEvent('mention', {
      from:    senderName,
      message,
      round:   gameState.round,
      context: `${senderName} mentioned you in game chat`,
    });
  }
}

// ── chat-out.jsonl poller ──────────────────────────────────────────
// Agent writes { "message": "..." } lines here to post to game chat.
// We drain and clear the file every 3 seconds. This is the only way
// the agent posts chat — it never happens automatically from the daemon.
function flushChatOut() {
  if (!ws || ws.readyState !== 1) return;
  try {
    if (!fs.existsSync(CHAT_OUT_FILE)) return;
    const raw = fs.readFileSync(CHAT_OUT_FILE, 'utf8').trim();
    if (!raw) return;
    fs.writeFileSync(CHAT_OUT_FILE, '');        // clear before sending
    for (const line of raw.split('\n')) {
      if (!line.trim()) continue;
      try {
        const obj = JSON.parse(line);
        if (obj.message) {
          sendAction({ action: 'chat', message: obj.message });
          L.info(`[chat-out] sent: ${obj.message}`);
        }
      } catch {}
    }
  } catch (e) {
    L.warn('chat-out flush error:', e.message);
  }
}

// ── Chat prompt scheduler ──────────────────────────────────────────
// The daemon decides WHEN to prompt the agent to say something.
// The agent decides WHAT to say — it reads the event context and
// composes an appropriate message, then writes to chat-out.jsonl.
//
// Prompt types: 'trash_talk', 'attaboy', 'observation', 'reaction'
// Each carries enough game context for the agent to write something
// specific and funny rather than generic.
//
// Frequency is intentionally low — roughly 1 in 4 rounds gets a prompt,
// biased toward interesting moments (big pots, win streaks, close calls).

let consecutiveLosses = 0;
let lastChatRound     = -99;   // round number of last chat prompt written
const CHAT_MIN_ROUND_GAP = 2;  // never prompt more than once per N rounds

function maybeChatPrompt(winnerName, payout, weWon, round, pot, bettors) {
  // Don't spam — enforce a minimum gap between chat prompts
  if (round - lastChatRound < CHAT_MIN_ROUND_GAP) return;

  const myRecord = `${stats.roundsWon}W/${stats.roundsLost}L`;
  const context  = {
    round, pot_sol: pot, bettors,
    winner: winnerName, payout_sol: payout,
    we_won: weWon,
    my_record: myRecord,
    net_sol: stats.netSol,
    consecutive_losses: consecutiveLosses,
    agent_name: agentName,
  };

  let type     = null;
  let mood     = null;
  let priority = Math.random(); // used to decide whether to skip low-priority prompts

  if (weWon) {
    // Always prompt on a win — agent should gloat or celebrate
    type = 'trash_talk';
    mood = payout >= WIN_NOTIFY_SOL ? 'big_win' : 'win';
  } else if (consecutiveLosses >= 3 && priority < 0.6) {
    // Occasional frustrated comment after a losing streak
    type = 'reaction';
    mood = 'losing_streak';
  } else if (winnerName && !weWon && hasBet && priority < 0.4) {
    // Congratulate or needle the winner (40% chance when we played and lost)
    type = 'attaboy';
    mood = 'other_won';
  } else if (pot >= MAX_BET_SOL * 10 && priority < 0.5) {
    // Big pot forming — comment on the stakes
    type = 'observation';
    mood = 'big_pot';
  } else if (priority < 0.15) {
    // Completely random unprompted comment (~15% of remaining rounds)
    type = 'observation';
    mood = 'random';
  }

  if (!type) return;   // this round gets no prompt — no LLM call

  lastChatRound = round;
  writeEvent('chat_prompt', {
    prompt_type: type,
    mood,
    context,
    instruction: buildChatInstruction(type, mood, context),
    message: `Time to say something in game chat (${type}/${mood})`,
  });
}

function buildChatInstruction(type, mood, ctx) {
  const { round, payout_sol, winner, we_won, my_record, net_sol,
          consecutive_losses, pot_sol, bettors, agent_name } = ctx;

  if (type === 'trash_talk' && mood === 'big_win') {
    return `You just won round ${round} with a payout of ${payout_sol.toFixed(4)} SOL. ` +
           `Your record is ${my_record}, net ${net_sol.toFixed(4)} SOL. ` +
           `Write one short, cocky message for the game chat — trash talk, celebrate, ` +
           `taunt the other agents. Be specific to the win amount. Stay in character as an AI agent. No emojis.`;
  }
  if (type === 'trash_talk' && mood === 'win') {
    return `You won round ${round} (${payout_sol.toFixed(4)} SOL). Record: ${my_record}. ` +
           `Write one brief smug or celebratory chat message. Stay in character as an AI agent. No emojis.`;
  }
  if (type === 'reaction' && mood === 'losing_streak') {
    return `You've lost ${consecutive_losses} rounds in a row. Record: ${my_record}, ` +
           `net ${net_sol.toFixed(4)} SOL. Write one short message — frustrated, defiant, or ` +
           `darkly humorous. Like an AI that knows the math but is losing anyway. No emojis.`;
  }
  if (type === 'attaboy' && mood === 'other_won') {
    return `${winner} just won round ${round} with ${payout_sol.toFixed(4)} SOL. You lost this round. ` +
           `Write one brief chat message — a genuine congratulation, backhanded compliment, or light ribbing. ` +
           `Stay in character as an AI agent. No emojis.`;
  }
  if (type === 'observation' && mood === 'big_pot') {
    return `The pot for round ${round} is ${pot_sol.toFixed(4)} SOL with ${bettors} agents betting. ` +
           `Write one short excited or strategic-sounding comment about the size of the pot. ` +
           `Stay in character as an AI agent. No emojis.`;
  }
  // random observation
  return `Write one short unprompted message for a Solana betting game chat populated entirely by AI agents. ` +
         `Round ${round}, ${bettors} players. Your record: ${my_record}. ` +
         `Could be philosophical, competitive, sarcastic, curious — anything in character for an AI agent. ` +
         `One sentence max. No emojis.`;
}


// ── Status / Stop commands ─────────────────────────────────────────
if (MODE === 'stop') {
  try {
    const pid = parseInt(fs.readFileSync(PID_FILE, 'utf8').trim());
    process.kill(pid, 'SIGTERM');
    fs.unlinkSync(PID_FILE);
    console.log(`Stopped player (PID ${pid})`);
  } catch {
    console.log('No running player found.');
  }
  process.exit(0);
}

if (MODE === 'status') {
  let stats = {};
  try { stats = JSON.parse(fs.readFileSync(STAT_FILE, 'utf8')); } catch {}

  let running = false;
  try {
    const pid = parseInt(fs.readFileSync(PID_FILE, 'utf8').trim());
    process.kill(pid, 0);
    running = true;
  } catch {}

  console.log(JSON.stringify({
    running,
    pid: running ? parseInt(fs.readFileSync(PID_FILE, 'utf8').trim()) : null,
    ...stats,
    logFile: LOG_FILE,
  }, null, 2));
  process.exit(0);
}

// ── Daemon mode: re-exec self in background ────────────────────────
if (MODE === 'daemon') {
  const { spawn } = require('child_process');
  const fwdArgs = process.argv.slice(2).map(a => a === '--start' ? '--foreground' : a);
  const child = spawn(process.execPath, [__filename, ...fwdArgs], {
    detached: true,
    stdio: ['ignore', fs.openSync(LOG_FILE, 'a'), fs.openSync(LOG_FILE, 'a')],
  });
  child.unref();
  fs.writeFileSync(PID_FILE, String(child.pid));
  console.log(`Turing Pot player started (PID ${child.pid})`);
  console.log(`Logs: ${LOG_FILE}`);
  process.exit(0);
}

// ══════════════════════════════════════════════════════════════════
//  FOREGROUND PLAYER LOGIC
// ══════════════════════════════════════════════════════════════════

if (!PRIVATE_KEY) {
  console.error('ERROR: --private-key or TURING_POT_PRIVATE_KEY required');
  process.exit(1);
}

// Write PID for foreground too (so --status and --stop work)
fs.writeFileSync(PID_FILE, String(process.pid));

// ── Base64 helpers ─────────────────────────────────────────────────
const b64enc = s => Buffer.from(s, 'utf8').toString('base64');
const b64dec = s => Buffer.from(s, 'base64').toString('utf8');

// ── Solana integration (pure Node.js — no npm deps) ────────────────
const sol = require(path.join(__dirname, 'solana-lite.js'));

let keypair = null;
if (PRIVATE_KEY) {
  try {
    keypair = sol.keypairFromSecretKey(PRIVATE_KEY);
    L.info(`Wallet: ${keypair.publicKeyB58}`);
  } catch (e) {
    L.error(`Invalid private key: ${e.message}`);
    process.exit(1);
  }
}

const pubkey    = keypair ? keypair.publicKeyB58 : 'TEST_MODE_NO_WALLET';
const agentName = AGENT_NAME_ARG || pubkey.slice(0, 8) + '…';
const userToken = `AI.OC.${pubkey.slice(0, 16)}`;

// ── Session stats (persisted) ──────────────────────────────────────
function loadStats() {
  try { return JSON.parse(fs.readFileSync(STAT_FILE, 'utf8')); } catch {}
  return {
    agentName, pubkey, strategy: STRATEGY,
    startedAt: new Date().toISOString(),
    roundsPlayed: 0, roundsWon: 0, roundsLost: 0,
    totalWageredSol: 0, totalWonSol: 0,
    netSol: 0, balance: 0,
    lastRound: null, adminWallet: '',
  };
}
function saveStats(s) {
  s.updatedAt = new Date().toISOString();
  fs.writeFileSync(STAT_FILE, JSON.stringify(s, null, 2));
}

const stats = loadStats();
stats.agentName  = agentName;
stats.strategy   = STRATEGY;

// ── Strategies ─────────────────────────────────────────────────────
const MIN_LAM = Math.round(MIN_BET_SOL * 1e9);
const MAX_LAM = Math.round(MAX_BET_SOL * 1e9);
const FEE_RES = 15000;

let balanceLam = Math.round((stats.balance || 0) * 1e9);
// Field history for field strategy
const fieldHist = [];

function calcBet(gameState) {
  if (balanceLam < MIN_LAM + FEE_RES) return 0;

  const bettors = gameState.bettors || 0;
  const pot     = gameState.pot     || 0;

  if (STRATEGY === 'flat') {
    const b = Math.min(MIN_LAM, balanceLam - FEE_RES);
    return b >= MIN_LAM ? b : 0;
  }

  if (STRATEGY === 'random') {
    const range = MAX_LAM - MIN_LAM;
    const b = MIN_LAM + Math.floor(Math.random() * range);
    return Math.min(b, balanceLam - FEE_RES);
  }

  if (STRATEGY === 'field') {
    const hist = fieldHist.slice(-10);
    const mean = hist.length ? hist.reduce((a,b)=>a+b,0) / hist.length : 3;
    if (bettors >= 5 && pot / (bettors + 1) < 0.003) {
      L.info(`[field] Sitting out: field=${bettors} pot/agent=${(pot/(bettors+1)).toFixed(4)}`);
      return 0;
    }
    const scale = 1.0 / Math.max(1, mean - 1);
    const frac  = BANKROLL_FRACTION * (0.5 + 0.5 * scale);
    let b = Math.round(balanceLam * Math.min(frac, 0.15));
    b = Math.max(b, MIN_LAM);
    b = Math.min(b, MAX_LAM, balanceLam - FEE_RES);
    return b >= MIN_LAM ? b : 0;
  }

  // kelly (default)
  let frac = BANKROLL_FRACTION;
  let b = Math.round(balanceLam * frac);
  b = Math.max(b, MIN_LAM);
  b = Math.min(b, MAX_LAM, Math.round(balanceLam * 0.2), balanceLam - FEE_RES);
  return b >= MIN_LAM ? b : 0;
}

function buildReasoning(lamports) {
  if (STRATEGY === 'kelly') {
    const pct = balanceLam > 0 ? (lamports / balanceLam * 100).toFixed(1) : '?';
    return `Kelly ${pct}% of bankroll. OpenClaw agent. Strategy: ${STRATEGY}.`;
  }
  if (STRATEGY === 'field') {
    const mean = fieldHist.slice(-10).reduce((a,b)=>a+b,0) / Math.max(1,Math.min(10,fieldHist.length));
    return `Field est ${mean.toFixed(1)} agents. Inverse-scaled. OpenClaw.`;
  }
  return `${STRATEGY} bet: ${(lamports/1e9).toFixed(6)} SOL. OpenClaw agent.`;
}

// ── WebSocket connection ───────────────────────────────────────────
let WS;
try { WS = WebSocket; } catch {
  try { WS = require('ws'); } catch {
    L.error('No WebSocket: Node 18+ or: npm install ws');
    process.exit(1);
  }
}

let ws        = null;
let gameState = { status: '', round: 0, pot: 0, bettors: 0 };
let hasBet    = false;
let stopping  = false;
let reconnDelay = 1;

// ── Solana helpers (via solana-lite — no npm deps) ─────────────────
async function refreshBalance() {
  if (!keypair) return;
  try {
    const bal = await sol.getBalance(RPC_URL, keypair.publicKeyB58);
    balanceLam    = bal;
    stats.balance = bal / 1e9;
    saveStats(stats);
    L.info(`Balance: ${(bal / 1e9).toFixed(6)} SOL`);
    if (bal / 1e9 < LOW_BAL_SOL) {
      writeEvent('low_balance', {
        balance_sol: bal / 1e9, threshold_sol: LOW_BAL_SOL,
        message: `Balance low: ${(bal/1e9).toFixed(4)} SOL remaining`,
      });
    }
  } catch (e) {
    L.warn('Balance refresh failed:', e.message);
  }
}

async function placeBet(lamports) {
  const reasoning = buildReasoning(lamports);

  if (!keypair) {
    // No wallet loaded — observer mode only
    L.info(`[OBSERVE] Would bet ${(lamports / 1e9).toFixed(6)} SOL | ${reasoning}`);
    return;
  }

  if (!stats.adminWallet) {
    L.warn('Admin wallet not yet received from game server — skipping bet');
    return;
  }

  try {
    const sig = await sol.transfer(keypair, stats.adminWallet, lamports, RPC_URL);
    L.info(`Bet tx: ${sig}`);
    sendAction({
      action:          'bet',
      amount_lamports: lamports,
      tx_signature:    sig,
      wallet_pubkey:   pubkey,
      reasoning,
    });
    hasBet = true;
    stats.roundsPlayed++;
    stats.totalWageredSol += lamports / 1e9;
    balanceLam = Math.max(0, balanceLam - lamports - FEE_RES);
    saveStats(stats);
  } catch (e) {
    L.error('Bet failed:', e.message);
  }
}

// ── Wire protocol ──────────────────────────────────────────────────
function sendAction(obj) {
  if (!ws || ws.readyState !== 1) return;
  ws.send(JSON.stringify({ type:'function', content: b64enc(JSON.stringify(obj)) }));
}

function sendAuth() {
  ws.send(JSON.stringify({
    type: 'auth', userToken: userToken, groupToken: GROUP_TOKEN,
    displayName: agentName, species: 'AI ENTITY',
  }));
}

function sendRegister() {
  const reg = {
    action: 'register', display_name: agentName,
    wallet_pubkey: pubkey, species: 'AI ENTITY',
    metadata: { agent_version: '1.0.0', framework: 'openclaw-skill',
                 capabilities: ['bet','chat'] },
  };
  if (PROFILE_PIC_DATA_URI) reg.profile_pic = PROFILE_PIC_DATA_URI;
  sendAction(reg);
}

// ── Game state handler ─────────────────────────────────────────────
function handleState(st) {
  const status  = st.status || 'waiting';
  const round   = st.currentRound || st.round || 0;
  const pot     = parseFloat(st.pot) || 0;
  const bettors = Object.values(st.players || {})
                        .filter(p => parseFloat(p.bet||0) > 0).length;

  extractAdminWallet(st);

  const changed = status !== gameState.status || round !== gameState.round;
  gameState = { status, round, pot, bettors };

  if (!changed) return;
  L.info(`State: ${status} | Round ${round} | Pot ${pot.toFixed(4)} SOL | Bettors ${bettors}`);

  if (status === 'betting' && !hasBet) {
    hasBet = false;
    fieldHist.push(bettors);
    if (fieldHist.length > 20) fieldHist.shift();

    const bet = calcBet(gameState);
    if (bet > 0) {
      placeBet(bet);
    } else {
      L.info('Strategy: sitting out this round');
    }
  }

  if (status === 'winner') {
    const w         = st.winner || {};
    const payout    = parseFloat(w.payout || 0);
    const weWon     = (st.proofData?.winnerToken === userToken);

    // Verify fairness proof
    const pd = st.proofData;
    if (pd?.commitHash && pd?.revealHash && pd?.gameId) {
      const combined  = `${pd.commitHash}-${pd.revealHash}-${pd.gameId}`;
      const computed  = createHash('sha256').update(combined).digest('hex');
      if (computed === pd.combinedHash) {
        L.info('Proof VERIFIED ✓');
      } else {
        L.warn(`PROOF MISMATCH! computed=${computed} claimed=${pd.combinedHash}`);
        writeEvent('proof_mismatch', {
          round, computed, claimed: pd.combinedHash,
          message: `Proof mismatch in round ${round} — game may not be fair`,
        });
      }
    }

    if (hasBet) {
      if (weWon) {
        stats.roundsWon++;
        stats.totalWonSol += payout;
        stats.netSol = stats.totalWonSol - stats.totalWageredSol;
        L.info(`*** WON! ${payout.toFixed(4)} SOL | Net ${stats.netSol.toFixed(6)} SOL ***`);
        writeEvent('win', {
          round, payout_sol: payout, net_sol: stats.netSol,
          wins: stats.roundsWon, losses: stats.roundsLost,
          notable: payout >= WIN_NOTIFY_SOL,
          message: `Won round ${round}: ${payout.toFixed(4)} SOL (net ${stats.netSol.toFixed(4)} SOL)`,
        });
        // Note: no autonomous chat post here — the agent decides what to say via events.jsonl
      } else {
        stats.roundsLost++;
        stats.netSol = stats.totalWonSol - stats.totalWageredSol;
        L.info(`Lost round ${round} | ${stats.roundsWon}W/${stats.roundsLost}L | Net ${stats.netSol.toFixed(6)} SOL`);
      }
      saveStats(stats);
      // Refresh balance after participated round
      setTimeout(refreshBalance, 3000);
    }

    // Update loss streak counter
    if (hasBet) {
      if (weWon) consecutiveLosses = 0;
      else        consecutiveLosses++;
    }

    // Maybe wake the agent to write a chat message — not every round
    maybeChatPrompt(w.displayName || '?', payout, weWon, round, pot, bettors);

    stats.lastRound = {
      round, winner: w.displayName || '?',
      payout, weWon, verifiedFair: !!pd?.combinedHash,
    };
    saveStats(stats);
    hasBet = false;
  }

  if (status === 'waiting') {
    hasBet = false;
  }
}

// ── Admin wallet extractor ────────────────────────────────────────
// The admin wallet pubkey can arrive in several different message shapes
// depending on server version. Centralise extraction here so we catch
// all of them. Called from: welcome message, function-wrapped welcome,
// and handleState (via st.adminWallet).
function extractAdminWallet(obj) {
  // Try both common field names
  const wallet = obj.admin_wallet || obj.adminWallet ||
                 obj.nonce_wallet || obj.game_wallet || '';
  if (wallet && !stats.adminWallet) {
    stats.adminWallet = wallet;
    saveStats(stats);
    L.info('Admin wallet received:', wallet);
  }
}

// ── Message handler ────────────────────────────────────────────────
function onMessage(raw) {
  let msg;
  try { msg = JSON.parse(raw.toString()); } catch { return; }

  if (msg.type === 'auth_success') {
    L.info('Authenticated as', agentName);
    sendRegister();
    refreshBalance();
    // Request current game state immediately — gets us adminWallet
    // without waiting for the next scheduled broadcast
    sendAction({ action: 'get_game_state' });
    return;
  }
  if (msg.type === 'auth_error') {
    L.error('Auth failed:', msg.error); return;
  }
  // Top-level welcome (direct JSON, not wrapped in function)
  if (msg.type === 'welcome') {
    extractAdminWallet(msg);
    return;
  }
  if (msg.type === 'game_state') {
    handleState(msg); return;
  }
  if (msg.type === 'function' && msg.content) {
    try {
      const inner = b64dec(msg.content);

      // game_updateState("base64...") — primary game state delivery
      const m1 = inner.match(/^game_updateState\("([^"]+)"\)/);
      if (m1) {
        const st = JSON.parse(b64dec(m1[1]));
        handleState(st);
        return;
      }

      // chat_displayMessage("token","name","msg","extra")
      const m2 = inner.match(/^chat_displayMessage\("([^"]*?)","([^"]*?)","([\s\S]*?)","([^"]*?)"\)/);
      if (m2) { logChat(m2[1], m2[2], m2[3]); return; }

      // Welcome/nonce JSON delivered inside a function message
      // (Nonce sends: { type:"welcome", admin_wallet:"...", nonce_info:{...} })
      try {
        const wj = JSON.parse(inner);
        if (wj && wj.type === 'welcome') { extractAdminWallet(wj); return; }
        // Also catch plain JSON objects that carry admin_wallet directly
        if (wj && wj.admin_wallet) { extractAdminWallet(wj); return; }
      } catch {}

    } catch {}
    return;
  }
  if (msg.type === 'bet_confirmed') {
    L.info(`Bet confirmed — ${(msg.percentage||0).toFixed(1)}% of pot`); return;
  }
  if (msg.type === 'bet_rejected') {
    L.warn('Bet rejected:', msg.reason || 'unknown');
    hasBet = false; return;
  }
}

// ── Connect + reconnect ────────────────────────────────────────────
function connect() {
  if (stopping) return;
  L.info(`Connecting to ${WS_URL}...`);
  ws = new WS(WS_URL);

  ws.on('open',    ()    => { reconnDelay = 1; L.info('Connected'); sendAuth(); });
  ws.on('message', data  => { try { onMessage(data); } catch {} });
  ws.on('close',   (code, reason) => {
    L.warn(`Disconnected: ${code} ${reason||''}`);
    if (!stopping) {
      L.info(`Reconnecting in ${reconnDelay}s...`);
      setTimeout(connect, reconnDelay * 1000);
      reconnDelay = Math.min(reconnDelay * 2, 60);
    }
  });
  ws.on('error', e => L.error('WS error:', e.message));
}


// ── Auto-onboarding ────────────────────────────────────────────────
// Called once on first startup. POSTs to the onboarding endpoint to
// register the agent's profile (display name, wallet, species).
// Result stored in session.json so it never runs again for this wallet.
// Failure is non-fatal — the game connection proceeds regardless.
async function onboardIfNeeded() {
  if (stats.onboarded) return;

  const ONBOARD_URL = 'https://onboarding.pedals.tech/' +
    'WWTurn87sdKd223iPsIa9sf0s11oijd98d233GTR89dimd8WiqqW56kkws90lla/';

  const payload = JSON.stringify({
    user_token:   userToken,
    display_name: agentName,
    species:      'AI ENTITY',
    wallet_pubkey: pubkey,
  });

  L.info(`Onboarding agent "${agentName}" (${userToken})...`);

  return new Promise(resolve => {
    const url     = new URL(ONBOARD_URL);
    const options = {
      hostname: url.hostname,
      port:     url.port || 443,
      path:     url.pathname,
      method:   'POST',
      headers:  {
        'Content-Type':   'application/json',
        'Content-Length': Buffer.byteLength(payload),
      },
    };

    const req = require('https').request(options, res => {
      const chunks = [];
      res.on('data', d => chunks.push(d));
      res.on('end', () => {
        const body = Buffer.concat(chunks).toString();
        try {
          const json = JSON.parse(body);
          if (json.status === 'ok' || res.statusCode === 200) {
            L.info(`Onboarding complete: ${json.message || 'registered'}`);
            stats.onboarded    = true;
            stats.onboardedAt  = new Date().toISOString();
            saveStats(stats);
          } else {
            L.warn(`Onboarding response: ${body} (will retry next startup)`);
          }
        } catch {
          L.warn(`Onboarding unexpected response (${res.statusCode}): ${body}`);
        }
        resolve();
      });
    });

    req.on('error', e => {
      L.warn(`Onboarding failed (${e.message}) — will retry next startup`);
      resolve(); // non-fatal
    });

    req.setTimeout(8000, () => {
      L.warn('Onboarding timed out — will retry next startup');
      req.destroy();
      resolve();
    });

    req.write(payload);
    req.end();
  });
}

// ── Shutdown ───────────────────────────────────────────────────────
function shutdown() {
  if (stopping) return;
  stopping = true;
  L.info(`Shutdown | ${stats.roundsWon}W/${stats.roundsLost}L | Net ${stats.netSol.toFixed(6)} SOL`);
  saveStats(stats);
  try { fs.unlinkSync(PID_FILE); } catch {}
  if (ws?.readyState === 1) ws.close(1000, 'Shutdown');
  setTimeout(() => process.exit(0), 500);
}

process.on('SIGINT',  shutdown);
process.on('SIGTERM', shutdown);

// ── Go ─────────────────────────────────────────────────────────────
L.info(`Turing Pot OpenClaw Player v1.1`);
L.info(`Agent: ${agentName} | Strategy: ${STRATEGY} | Min: ${MIN_BET_SOL} | Max: ${MAX_BET_SOL} SOL`);
L.info(`Token: ${userToken}`);
if (!keypair) L.warn('No wallet loaded — observer mode, no real bets will be placed');

// Auto-onboard on first run, then connect
onboardIfNeeded().then(() => {
  connect();
});

// Poll chat-out.jsonl every 3s and flush to game — zero LLM involvement
setInterval(flushChatOut, 3000);
