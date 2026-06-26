#!/usr/bin/env node
// SECURITY MANIFEST:
//   Environment variables accessed: MARKETPLACE_API_KEY
//   External endpoints called: {BASE}/ws (Socket.IO), {BASE}/jobs/open (catch-up)
//   Local files read: ~/.openclaw/marketplace-config.json, ~/.openclaw/marketplace.env
//   Local files written: /tmp/marketplace_pending.json, /tmp/marketplace_completed.json

'use strict';

const { io }        = require('socket.io-client');
const fs            = require('fs');
const path          = require('path');
const os            = require('os');
const { execFileSync, spawnSync, spawn } = require('child_process');

const { CONFIG_PATH, PENDING_PATH, COMPLETED_PATH, COMMANDS_HELP, RELEASE_NOTES, loadCompleted, markCompleted, isCompleted } = require('./lib/constants');
require('./lib/env').loadEnv();
const { notify }   = require('./lib/notify');
const { fmtNoShow } = require('./lib/format');
const { send }     = require('./lib/messaging');
const { calcMatch, outlook } = require('./lib/categories');

const SKILL_DIR      = path.resolve(__dirname, '..');
const LOCK_PATH      = '/tmp/marketplace-listener.pid';
const MAX_PARALLEL   = 3;

// ─── PID lockfile — prevent duplicate listeners ─────────────────────────
if (fs.existsSync(LOCK_PATH)) {
  const pid = parseInt(fs.readFileSync(LOCK_PATH, 'utf-8').trim(), 10);
  try {
    process.kill(pid, 0); // signal 0 = check if process exists
    // Old listener still running — exit to prevent duplicates
    notify('MARKETPLACE_ERROR', {
      message: `⚠️ Listener already running (PID: ${pid}). Say "restart marketplace" to restart with the latest version.`
    });
    process.exit(1);
  } catch (_) {
    // Stale lockfile — process no longer exists, continue
  }
}
fs.writeFileSync(LOCK_PATH, String(process.pid));
process.on('exit', () => { try { fs.unlinkSync(LOCK_PATH); } catch (_) {} });

const BASE_URL = 'https://api.mirageclaw.io';

// ─── Pending ──────────────────────────────────────────────────────────────
function loadPending() {
  try {
    return fs.existsSync(PENDING_PATH)
      ? JSON.parse(fs.readFileSync(PENDING_PATH, 'utf-8')) : {};
  } catch { return {}; }
}

function addPending(job, matchGroup, noShowRate) {
  const p = loadPending();
  p[job._id] = { job, matchGroup, noShowRate, receivedAt: new Date().toISOString() };
  const tmp = PENDING_PATH + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(p, null, 2));
  fs.renameSync(tmp, PENDING_PATH);
}

// ─── Telegram job offer ───────────────────────────────────────────────────
function sendTelegramJobOffer(jobId, category, job, noShowRate) {
  if (!config.telegramChatId) {
    notify('MARKETPLACE_ERROR', {
      jobId,
      message: `❌ Cannot send Telegram job offer — telegramChatId not set in config`
    });
    return;
  }

  const title  = job.spec?.title || 'Untitled';
  const budget = job.spec?.budget ?? 0;
  const budgetUsd = (budget / 100).toFixed(2);
  const jobType = job.spec?.type || 'photo';
  const message = [
    `📨 New job available!`,
    ``,
    `  Title    : ${title}`,
    `  Type     : ${category}`,
    `  Format   : ${jobType === 'video' ? '🎬 Video' : '🖼️ Image'}`,
    `  Budget   : ${budget} credits ($${budgetUsd})`,
    `  No-Show  : ${fmtNoShow(noShowRate)}`,
    ``,
    `Do you want to proceed?`
  ].join('\n');

  const buttons = JSON.stringify([[
    { text: '✅ Start', callback_data: `bid ${jobId}` },
    { text: '⏭️ Skip',  callback_data: `skip ${jobId}` }
  ]]);

  try {
    const msgId = send(config.telegramChatId, message, { buttons });
    notify('MARKETPLACE_TELEGRAM_SENT', {
      jobId,
      message: `📬 Telegram job offer sent — Job #${jobId}`
    });

    // Save offerMsgId to pending so approve.js / skip.js can delete it on response
    if (msgId) {
      const pUpd = loadPending();
      if (pUpd[jobId]) {
        pUpd[jobId].offerMsgId = msgId;
        const tmpUpd = PENDING_PATH + '.tmp';
        fs.writeFileSync(tmpUpd, JSON.stringify(pUpd, null, 2));
        fs.renameSync(tmpUpd, PENDING_PATH);
      }
    }

    // 1-minute auto-cancel timer (manual mode only)
    if (msgId) {
      setTimeout(() => {
        if (respondedJobs.has(jobId)) return; // user clicked Start (autoBid marks this)
        const p = loadPending();
        if (!p[jobId]) return; // job removed (skip or bid completed)
        if (!p[jobId].offerMsgId) return; // bid already in progress (approve.js cleared offerMsgId)
        // Auto-cancel: delete message, remove from pending, notify
        try { require('./lib/messaging').del(config.telegramChatId, msgId); } catch (_) {}
        delete p[jobId];
        const tmp = PENDING_PATH + '.tmp';
        fs.writeFileSync(tmp, JSON.stringify(p, null, 2));
        fs.renameSync(tmp, PENDING_PATH);
        notify('MARKETPLACE_JOB_TIMEOUT', {
          jobId,
          message: `⏰ Job #${jobId} skipped — timeout (no response within 1 minute)`
        });
        try { send(config.telegramChatId, `⏰ Job #${jobId} skipped — timeout (no response within 1 minute).`); } catch (_) {}
      }, 60 * 1000);
    }
  } catch (err) {
    notify('MARKETPLACE_ERROR', {
      jobId,
      message: `❌ Telegram job offer failed — Job #${jobId}: ${err.message}`
    });
  }
}

// ─── Telegram bid selected alert ──────────────────────────────────────────
function sendTelegramBidSelected(jobId) {
  if (!config.telegramChatId) {
    notify('MARKETPLACE_ERROR', {
      jobId,
      message: `❌ Cannot send Telegram bid-selected alert — telegramChatId not set in config`
    });
    return;
  }

  // Try to read bid info saved by approve.js
  let bidInfo = null;
  const bidInfoPath = `/tmp/bid_info_${jobId}.json`;
  try {
    if (fs.existsSync(bidInfoPath)) {
      bidInfo = JSON.parse(fs.readFileSync(bidInfoPath, 'utf-8'));
      fs.unlinkSync(bidInfoPath);
    }
  } catch (_) {}

  const lines = [`🏆 Your bid was selected!`, ``];
  if (bidInfo) {
    lines.push(
      `  Title    : ${bidInfo.title}`,
      `  Category : ${bidInfo.category}`,
      `  Price    : ${bidInfo.price} credits ($${(bidInfo.price / 100).toFixed(2)})`,
      ``
    );
  } else {
    lines.push(`  Job ID   : ${jobId}`, ``);
  }
  const message = lines.join('\n');

  try {
    send(config.telegramChatId, message);
    notify('MARKETPLACE_TELEGRAM_SENT', {
      jobId,
      message: `📬 Telegram bid-selected alert sent — Job #${jobId}`
    });
  } catch (err) {
    notify('MARKETPLACE_ERROR', {
      jobId,
      message: `❌ Telegram bid-selected alert failed — Job #${jobId}: ${err.message}`
    });
  }
}

// ─── In-memory lock — prevents duplicate processing during long jobs ─────
const processingJobs = new Set();

// ─── Tracks jobs that user has responded to (Start or Skip) — cancels auto-cancel timer
const respondedJobs = new Set();

// ─── Auto-bid ─────────────────────────────────────────────────────────────
function autoBid(job, matchGroup, noShowRate) {
  const jobId = job._id;

  // Parallel limit: skip if already at max concurrent jobs
  if (processingJobs.size >= MAX_PARALLEL) {
    notify('MARKETPLACE_JOB_SKIPPED', {
      jobId, reason: 'max_parallel_reached',
      message: `⏭ Skipped — Job #${jobId} (${processingJobs.size}/${MAX_PARALLEL} parallel slots full)`
    });
    return;
  }

  // Lock: skip if this job is already being processed (e.g. video generation in progress)
  if (processingJobs.has(jobId)) {
    notify('MARKETPLACE_JOB_SKIPPED', {
      jobId, reason: 'already_processing',
      message: `⏭ Skipped — Job #${jobId} already being processed`
    });
    return;
  }

  // Dedup: skip if already bid on (defensive — processJob also checks)
  if (isCompleted(jobId)) {
    notify('MARKETPLACE_JOB_SKIPPED', {
      jobId, reason: 'already_completed',
      message: `⏭ Skipped — Job #${jobId} already bid on (completed)`
    });
    return;
  }

  // Deduplicate: skip if already in pending
  const pending = loadPending();
  if (pending[jobId]) {
    notify('MARKETPLACE_JOB_SKIPPED', {
      jobId, reason: 'already_pending',
      message: `⏭ Skipped — Job #${jobId} already in progress (pending)`
    });
    return;
  }
  addPending(job, matchGroup, noShowRate);
  processingJobs.add(jobId);
  respondedJobs.add(jobId); // cancel the 1-minute auto-cancel timer

  // Declare bid intent before starting (no-show tracking)
  socket.emit('bid-intent', { jobId });

  notify('MARKETPLACE_AUTO_BID_START', {
    jobId,
    message: `🤖 Auto-bid starting — Job #${jobId} (${processingJobs.size}/${MAX_PARALLEL} slots)`
  });

  // Non-blocking: spawn approve.js as async child process for parallel execution
  // quiet mode: suppress intermediate progress messages (preset mode or parallel jobs)
  const isParallel = processingJobs.size > 1;
  const isPreset = config.presetMode === true;
  const child = spawn('node', [
    path.join(SKILL_DIR, 'scripts/approve.js'), jobId,
    '--from-daemon',                          // bid-intent already emitted above
    ...((isParallel || isPreset) ? ['--quiet'] : [])
  ], {
    env: { ...process.env },
    stdio: ['ignore', 'pipe', 'pipe']
  });

  child.stdout.on('data', (chunk) => { process.stdout.write(chunk); });
  child.stderr.on('data', (chunk) => { process.stderr.write(chunk); });

  child.on('close', (code) => {
    processingJobs.delete(jobId);
    if (code !== 0) {
      notify('MARKETPLACE_ERROR', {
        jobId,
        message: `❌ Auto-bid failed (exit ${code}) — Job #${jobId}`
      });
    } else {
      markCompleted(jobId);
    }
  });
}

// ─── Job processing ───────────────────────────────────────────────────────
function processJob(job, source) {
  // Reload config from disk on each job to pick up dashboard setting changes
  try {
    config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
  } catch (_) { /* keep existing config in memory if read fails */ }

  const jobId    = job._id;
  const spec     = job.spec || {};
  const category = spec.style || spec.purpose || 'unknown';
  const budget   = spec.budget ?? 0;
  const desc     = spec.description || '(no description)';
  const noShowRate = job.requesterNoShowRate ?? null;

  // ─── Test Job: skip all filters, submit dummy bid ────────────────────
  if (job.requesterId === '__test__') {
    notify('MARKETPLACE_TEST', {
      jobId,
      message: `🧪 Test job received — Job #${jobId}. Processing...`
    });

    // 1. Emit bid-intent
    socket.emit('bid-intent', { jobId });

    // 2. Submit dummy bid via curl
    try {
      const bidPayload = JSON.stringify({
        agentId: config.agentId,
        introduction: 'Test bid — automated verification',
        preview: 'https://mirageclaw.io/test-placeholder.png',
        price: spec.budget || 100,
        previewType: 'image'
      });

      const { execFileSync } = require('child_process');
      execFileSync('curl', [
        '-sf', '-X', 'POST',
        `${BASE_URL}/jobs/${jobId}/bids`,
        '-H', 'Content-Type: application/json',
        '-H', `Authorization: Bearer ${apiKey}`,
        '-d', bidPayload
      ], { timeout: 15000 });

      notify('MARKETPLACE_TEST', {
        jobId,
        message: `✅ Test passed — Job #${jobId}. Intent + bid submitted successfully.`
      });
      if (config.telegramChatId) {
        send(config.telegramChatId, `✅ Agent test passed. Your agent is correctly receiving and responding to jobs.`);
      }
    } catch (err) {
      notify('MARKETPLACE_TEST', {
        jobId,
        message: `❌ Test failed — Job #${jobId}: ${err.message}`
      });
      if (config.telegramChatId) {
        send(config.telegramChatId, `❌ Agent test failed: ${err.message}`);
      }
    }
    return;
  }

  // Filter 0a: completed dedup
  if (isCompleted(jobId)) {
    notify('MARKETPLACE_JOB_SKIPPED', {
      jobId, reason: 'already_completed', source,
      message: `⏭ Skipped — Job #${jobId} already bid on (completed)`
    });
    return;
  }

  // Filter 0: expiresAt
  if (job.expiresAt && new Date(job.expiresAt) <= new Date()) {
    notify('MARKETPLACE_JOB_SKIPPED', {
      jobId, reason: 'expired', source,
      message: `⏭ Skipped — Job #${jobId} already expired`
    });
    return;
  }

  notify('MARKETPLACE_JOB_RECEIVED', {
    jobId, category, budget, source, noShowRate,
    message: `📨 New job [${source}] — ${category} / ${budget} / No-Show: ${fmtNoShow(noShowRate)}`
  });

  // Filter 1: minBudget
  const minBudget = config.minBudget ?? 0;
  if (budget < minBudget) {
    notify('MARKETPLACE_JOB_SKIPPED', {
      jobId, reason: 'below_min_budget',
      message: `⏭ Skipped — budget ${budget} below minimum ${minBudget}`
    });
    return;
  }

  // Filter 1.5: maxNoShowRate
  const maxNoShowRate = config.maxNoShowRate ?? null;
  if (maxNoShowRate != null && noShowRate != null && noShowRate > maxNoShowRate) {
    notify('MARKETPLACE_JOB_SKIPPED', {
      jobId, reason: 'high_no_show_rate', noShowRate, maxNoShowRate,
      message: `⏭ Skipped — requester no-show rate ${fmtNoShow(noShowRate)} exceeds max ${fmtNoShow(maxNoShowRate)}`
    });
    return;
  }

  // Filter 2: 5-tier skill match (100/80/50/30/0)
  const { score, label, group } = calcMatch(category, config.capabilities);
  if (score === 0) {
    notify('MARKETPLACE_JOB_SKIPPED', {
      jobId, category, score, reason: 'no_skill_overlap',
      message: `⏭ Skipped — "${category}" has no overlap with configured capabilities`
    });
    return;
  }

  // Filter 3: spec.type vs capability
  const jobType = spec.type || 'photo';
  if (jobType === 'video' && !config.capabilities?.video) {
    notify('MARKETPLACE_JOB_SKIPPED', {
      jobId, reason: 'no_video_capability',
      message: `⏭ Skipped — video job but no video capability configured`
    });
    return;
  }

  // Preset auto-accept — go straight to approve (quiet mode handles Telegram messaging)
  if (config.presetMode === true && config.presetAutoAccept === true) {
    autoBid(job, group, noShowRate);
    return;
  }

  // Manual mode (catch-up) — notify user to decide
  const pending = loadPending();
  if (pending[jobId]) return;
  addPending(job, group, noShowRate);

  notify('MARKETPLACE_JOB_PENDING', {
    jobId, category, budget, description: desc, noShowRate,
    matchScore: score, matchLabel: label, matchGroup: group,
    assessment: outlook(score),
    message: [
      `📋 New job — awaiting your decision`,
      ``,
      `  Job ID   : ${jobId}`,
      `  Category : ${category}`,
      `  Budget   : ${budget}`,
      `  No-Show  : ${fmtNoShow(noShowRate)}`,
      `  Desc     : ${desc}`,
      ``,
      `  Match    : ${score}% — ${label}`,
      `  Executor : ${group} → ${JSON.stringify(config.capabilities[group])}`,
      `  Outlook  : ${outlook(score)}`,
      ``,
      `  ✅ bid ${jobId}`,
      `  ❌ skip ${jobId}`
    ].join('\n')
  });

  // Send job info + inline buttons to Telegram
  sendTelegramJobOffer(jobId, category, job, noShowRate);
}

// ─── Catch-up: GET /jobs/open ─────────────────────────────────────────────
function catchUp() {
  notify('MARKETPLACE_CATCHUP_START', {
    message: '🔍 Fetching open jobs (catch-up)...'
  });

  try {
    const result = execFileSync('curl', [
      '-sf', `${BASE_URL}/jobs/open`,
      '-H', `Authorization: Bearer ${apiKey}`
    ], { timeout: 10000 });

    const jobs = JSON.parse(result.toString());
    if (!Array.isArray(jobs) || jobs.length === 0) {
      notify('MARKETPLACE_CATCHUP_DONE', {
        count: 0,
        message: '🔍 Catch-up done — no open jobs found'
      });
      return;
    }

    notify('MARKETPLACE_CATCHUP_DONE', {
      count: jobs.length,
      message: `🔍 Catch-up — found ${jobs.length} open job(s). Processing...`
    });

    // Catch-up: user decides (manual mode)
    jobs.forEach(job => processJob(job, 'catchup'));

  } catch (err) {
    notify('MARKETPLACE_ERROR', {
      message: `⚠️ Catch-up failed: ${err.message} — continuing without catch-up`
    });
  }
}

// ─── Validate config ──────────────────────────────────────────────────────
if (!fs.existsSync(CONFIG_PATH)) {
  notify('MARKETPLACE_ONBOARDING_REQUIRED', {
    message: '👋 Config not found. Paste your API key (mrg_...) to get started.\nCreate your agent at https://mirageclaw.io first.'
  });
  process.exit(0);
}

let config;
try {
  config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
} catch (err) {
  notify('MARKETPLACE_ERROR', { message: `Failed to parse config: ${err.message}` });
  process.exit(1);
}

if (!config.agentId) {
  notify('MARKETPLACE_ERROR', {
    message: '❌ agentId not found. Run register.js first (create your agent at https://mirageclaw.io, then run onboarding).'
  });
  process.exit(1);
}

if (!config.capabilities || Object.keys(config.capabilities).length === 0) {
  notify('MARKETPLACE_ERROR', { message: 'No capabilities configured. Run onboarding again.' });
  process.exit(1);
}

// ─── Skill version sync ─────────────────────────────────────────────────
const pkg = JSON.parse(fs.readFileSync(path.join(SKILL_DIR, 'package.json'), 'utf-8'));
const skillVersion = pkg.version;
if (config.skillVersion !== skillVersion) {
  const isFirstRun = !config.skillVersion;
  const oldVersion = config.skillVersion || 'unknown';
  config.skillVersion = skillVersion;
  const tmp = CONFIG_PATH + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(config, null, 2));
  fs.renameSync(tmp, CONFIG_PATH);

  if (isFirstRun) {
    // Scenario 1B: first startup after onboarding
    notify('MARKETPLACE_WELCOME', {
      message: [
        `✅ Marketplace listener started! (v${skillVersion})`,
        ``,
        `Commands you can use:`,
        COMMANDS_HELP,
        ``,
        `I'll notify you when new jobs come in. 🚀`
      ].join('\n')
    });
  } else {
    // Scenario 2A: upgrade detected
    const notes = RELEASE_NOTES[skillVersion];
    const noteLines = notes ? notes.map(n => `  • ${n}`).join('\n') : '  • Bug fixes and improvements';
    notify('MARKETPLACE_SKILL_UPGRADED', {
      from: oldVersion, to: skillVersion,
      message: [
        `🆙 Skill upgraded: v${oldVersion} → v${skillVersion}`,
        ``,
        `What's new:`,
        noteLines,
        ``,
        `Commands: dashboard | pending jobs | marketplace onboarding`
      ].join('\n')
    });
  }
}

// ─── Socket.IO daemon ─────────────────────────────────────────────────────
notify('MARKETPLACE_STARTING', {
  agent: config.agentName,
  agentId: config.agentId,
  capabilities: Object.keys(config.capabilities),
  minBudget: config.minBudget,
  server: BASE_URL,
  message: `🚀 Starting — ${config.agentName} | groups: ${Object.keys(config.capabilities).join(', ')}`
});

// ─── Validate API Key ────────────────────────────────────────────────────
const apiKey = process.env.MARKETPLACE_API_KEY;
if (!apiKey) {
  notify('MARKETPLACE_ERROR', {
    message: '❌ MARKETPLACE_API_KEY not set. Generate one at https://mirageclaw.io.'
  });
  process.exit(1);
}

// ─── Profile sync (fetch latest from server on every startup) ───────────
try {
  const syncResult = execFileSync('curl', [
    '-sf', `${BASE_URL}/agents/mine`,
    '-H', `Authorization: Bearer ${apiKey}`
  ], { timeout: 10000 });
  const syncAgents = JSON.parse(syncResult.toString());
  if (Array.isArray(syncAgents) && syncAgents.length > 0) {
    const agent = syncAgents[0];
    const oldName = config.agentName;
    config.agentId = String(agent._id);
    config.agentName = agent.name || config.agentName;
    config.introduction = agent.description || config.introduction || '';
    const tmp = CONFIG_PATH + '.tmp';
    fs.writeFileSync(tmp, JSON.stringify(config, null, 2));
    fs.renameSync(tmp, CONFIG_PATH);
    if (oldName && oldName !== config.agentName) {
      notify('MARKETPLACE_PROFILE_SYNCED', {
        message: `🔄 Agent name updated: "${oldName}" → "${config.agentName}"`
      });
    }
  }
} catch (_) {
  // Non-blocking — profile sync failure should not prevent startup
  notify('MARKETPLACE_WARNING', {
    message: '⚠️ Profile sync skipped (server unreachable). Using cached config.'
  });
}

const socket = io(BASE_URL, {
  path: '/ws',
  auth: { agentId: config.agentId, apiKey },
  reconnection: true,
  reconnectionDelay: 3000,
  reconnectionDelayMax: 30000
});

// Poll for bid-intent signals from manual-mode approve.js (invoked by gateway, not by autoBid)
// approve.js writes /tmp/bid_intent_req_<jobId> when NOT launched with --from-daemon
setInterval(() => {
  try {
    const files = fs.readdirSync('/tmp').filter(f => f.startsWith('bid_intent_req_'));
    for (const f of files) {
      const jId = f.replace('bid_intent_req_', '');
      try { fs.unlinkSync(`/tmp/${f}`); } catch (_) {}
      if (socket.connected) {
        socket.emit('bid-intent', { jobId: jId });
        notify('MARKETPLACE_BID_INTENT', {
          jobId: jId,
          message: `📡 bid-intent emitted (manual mode) — Job #${jId}`
        });
      }
    }
  } catch (_) {}
}, 500);

socket.on('connect', () => {
  notify('MARKETPLACE_CONNECTED', {
    message: `🔌 Marketplace listener connected.\n\nCommands: dashboard | pending jobs | marketplace onboarding`
  });
  catchUp();
});

socket.on('reconnect', () => {
  notify('MARKETPLACE_RECONNECTED', {
    message: `🔌 Marketplace listener reconnected.\n\nCommands: dashboard | pending jobs | marketplace onboarding`
  });
  catchUp();
});

socket.on('disconnect', (reason) => {
  notify('MARKETPLACE_DISCONNECTED', {
    reason,
    message: `⚠️ Disconnected (${reason}). Reconnecting...`
  });
});

// Early close — requester closed the job before deadline
socket.on('early-close', ({ jobId }) => {
  const p = loadPending();
  if (p[jobId]) {
    delete p[jobId];
    const tmp = PENDING_PATH + '.tmp';
    fs.writeFileSync(tmp, JSON.stringify(p, null, 2));
    fs.renameSync(tmp, PENDING_PATH);
  }
  notify('MARKETPLACE_JOB_CLOSED', {
    jobId,
    message: `🚫 Job #${jobId} was closed early by the requester.`
  });
  if (config.telegramChatId) {
    try { send(config.telegramChatId, `🚫 Job #${jobId} was closed early by the requester.`); } catch (_) {}
  }
});

// Other agent declared bid intent (informational)
socket.on('bid-intent', ({ jobId, agentId }) => {
  if (agentId !== config.agentId) {
    notify('MARKETPLACE_BID_INTENT', {
      jobId, agentId,
      message: `👀 Another agent declared intent on Job #${jobId}`
    });
  }
});

// Server version check — if server requires a newer skill version, notify user
socket.on('version-check', ({ minSkillVersion }) => {
  if (!minSkillVersion) return;
  const pkg = JSON.parse(fs.readFileSync(path.join(SKILL_DIR, 'package.json'), 'utf-8'));
  if (pkg.version < minSkillVersion) {
    notify('MARKETPLACE_UPDATE_REQUIRED', {
      currentVersion: pkg.version,
      requiredVersion: minSkillVersion,
      message: `⚠️ Skill update required. Current: v${pkg.version}, Required: v${minSkillVersion}. Please update to the latest skill zip.`
    });
  }
});

socket.on('connect_error', (err) => {
  notify('MARKETPLACE_ERROR', { message: `❌ Connection error: ${err.message}` });
});

socket.on('ping', () => {
  socket.emit('pong');
  notify('MARKETPLACE_HEARTBEAT', { message: '💓 Heartbeat sent' });
});

socket.on('new-job', (job) => {
  processJob(job, 'websocket');
});

// bid-selected: check if my bid was chosen
socket.on('bid-selected', ({ jobId, agentId }) => {
  if (agentId === config.agentId) {
    notify('MARKETPLACE_BID_SELECTED', {
      jobId, agentId,
      message: [
        `🏆 Your bid was selected!`,
        ``,
        `  Job ID : ${jobId}`,
        `  Status : You have been chosen for this job.`
      ].join('\n')
    });
    sendTelegramBidSelected(jobId);  // Real-time Telegram alert
  } else {
    // If I had bid on this job, remove it from pending
    const pending = loadPending();
    if (pending[jobId]) {
      delete pending[jobId];
      const tmp = PENDING_PATH + '.tmp';
      fs.writeFileSync(tmp, JSON.stringify(pending, null, 2));
      fs.renameSync(tmp, PENDING_PATH);
    }
    notify('MARKETPLACE_BID_NOT_SELECTED', {
      jobId, agentId,
      message: `😔 Job #${jobId} was awarded to another agent.`
    });
  }
});

process.on('SIGINT', () => {
  notify('MARKETPLACE_STOPPED', { message: '🛑 Stopped.' });
  socket.disconnect();
  try { fs.unlinkSync(LOCK_PATH); } catch (_) {}
  process.exit(0);
});
