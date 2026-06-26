#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { randomUUID } = require('crypto');
const { checkEmails } = require('./imap');

const WORKSPACE_ROOT = (() => {
  if (process.env.OPENCLAW_WORKSPACE) return path.resolve(process.env.OPENCLAW_WORKSPACE);
  let dir = path.resolve(__dirname);
  while (dir !== path.dirname(dir)) {
    if (fs.existsSync(path.join(dir, '.openclaw')) || fs.existsSync(path.join(dir, 'AGENTS.md'))) return dir;
    dir = path.dirname(dir);
  }
  return path.resolve(__dirname, '../../..');
})();
const DEFAULT_STATE_PATH = path.resolve(WORKSPACE_ROOT, 'memory/email-watch-state.json');
const DEFAULT_ANALYZE_MESSAGE = 'Process the pending email UIDs listed in the email watch state file. For each email, analyze its content and importance. Re-fetch with --extract-attachments when an email has attachments that may be relevant. Your final answer must be either HEARTBEAT_OK (if nothing needs attention) or a clear actionable summary of what requires the user\'s attention.';
const UID_LIST_LIMIT = 200;

function parseArgs() {
  const args = process.argv.slice(2);
  const command = args[0] && !args[0].startsWith('--') ? args[0] : 'detect';
  const options = {};

  for (let i = command === 'detect' ? 0 : 1; i < args.length; i++) {
    const arg = args[i];
    if (!arg.startsWith('--')) continue;

    const key = arg.slice(2);
    const next = args[i + 1];
    if (next && !next.startsWith('--')) {
      options[key] = next;
      i++;
    } else {
      options[key] = true;
    }
  }

  return { command, options };
}

function isTruthy(value) {
  return value === true || value === 'true' || value === '1' || value === 'yes';
}

function expandHome(value) {
  if (!value) return value;
  const home = process.env.HOME || process.env.USERPROFILE || '';
  return value.replace(/^~(?=$|[\\/])/, home);
}

function toIso(value) {
  return value ? new Date(value).toISOString() : null;
}

function normalizeUidList(values) {
  const seen = new Set();
  const normalized = [];

  for (const raw of values || []) {
    const uid = Number(raw);
    if (!Number.isFinite(uid)) continue;
    if (seen.has(uid)) continue;
    seen.add(uid);
    normalized.push(uid);
  }

  return normalized.slice(-UID_LIST_LIMIT);
}

function mergeUidLists(...lists) {
  return normalizeUidList(lists.flat());
}

const DELIVERY_RETRY_CAP = 2;
const FAILURE_ALERT_THRESHOLD = 3;
const FAILURE_ALERT_COOLDOWN_MS = 30 * 60 * 1000; // 30 minutes
const CHILD_PROCESS_TIMEOUT_MS = 240 * 1000; // 4 minutes

function createDefaultState() {
  return {
    lastCheckedAt: null,
    lastSuccessfulCheckAt: null,
    baselineCapturedAt: null,
    failureStreak: 0,
    lastFailureAlertAt: null,
    lastErrorSummary: null,
    processedUids: [],
    enrichedUids: [],
    draftedUids: [],
    alertedUids: [],
    pendingUids: [],
    deliveryRetryCounts: {},
    lastAnalysisTriggeredAt: null,
    lastAnalysisCompletedAt: null,
  };
}

function loadState(statePath) {
  const defaults = createDefaultState();

  if (!fs.existsSync(statePath)) {
    return defaults;
  }

  try {
    const raw = JSON.parse(fs.readFileSync(statePath, 'utf8'));
    return {
      ...defaults,
      ...raw,
      processedUids: normalizeUidList(raw.processedUids),
      enrichedUids: normalizeUidList(raw.enrichedUids),
      draftedUids: normalizeUidList(raw.draftedUids),
      alertedUids: normalizeUidList(raw.alertedUids),
      pendingUids: normalizeUidList(raw.pendingUids),
      deliveryRetryCounts: raw.deliveryRetryCounts && typeof raw.deliveryRetryCounts === 'object'
        ? raw.deliveryRetryCounts : {},
    };
  } catch {
    return defaults;
  }
}

function saveState(statePath, state) {
  const payload = {
    ...createDefaultState(),
    ...state,
    processedUids: normalizeUidList(state.processedUids),
    enrichedUids: normalizeUidList(state.enrichedUids),
    draftedUids: normalizeUidList(state.draftedUids),
    alertedUids: normalizeUidList(state.alertedUids),
    pendingUids: normalizeUidList(state.pendingUids),
  };

  const dir = path.dirname(statePath);
  fs.mkdirSync(dir, { recursive: true });

  // Atomic write: write to temp file, then rename
  const tmpPath = path.join(dir, `.email-watch-state.tmp.${process.pid}`);
  fs.writeFileSync(tmpPath, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
  fs.renameSync(tmpPath, statePath);
}

function acquireLock(statePath) {
  const lockPath = `${statePath}.lock`;
  try {
    // O_EXCL fails if file already exists — simple mutex
    const fd = fs.openSync(lockPath, fs.constants.O_CREAT | fs.constants.O_EXCL | fs.constants.O_WRONLY);
    fs.writeSync(fd, `${process.pid}\n`);
    fs.closeSync(fd);
    return lockPath;
  } catch (err) {
    if (err.code === 'EEXIST') {
      // Check if holding process is still alive
      try {
        const holdingPid = Number(fs.readFileSync(lockPath, 'utf8').trim());
        if (holdingPid && holdingPid !== process.pid) {
          try { process.kill(holdingPid, 0); } catch {
            // Process is dead — stale lock, remove and retry
            fs.unlinkSync(lockPath);
            return acquireLock(statePath);
          }
        }
      } catch {
        // Can't read lock file — remove and retry
        try { fs.unlinkSync(lockPath); } catch { /* ignore */ }
        return acquireLock(statePath);
      }
    }
    return null;
  }
}

function releaseLock(lockPath) {
  try { fs.unlinkSync(lockPath); } catch { /* ignore */ }
}

function buildAgentArgs(options, sessionId) {
  const args = [
    'agent',
    '--message', options.message || DEFAULT_ANALYZE_MESSAGE,
    '--session-id', sessionId,
    '--channel', options.channel || 'whatsapp',
    '--to', options.to,
    '--timeout', String(Number(options.timeout || options['timeout-seconds']) || 180),
  ];

  const thinking = options.thinking || 'low';
  if (thinking) {
    args.push('--thinking', thinking);
  }

  return args;
}

function buildSendArgs(options, messageText) {
  return [
    'message',
    'send',
    '--channel', options.channel || 'whatsapp',
    '--target', options.to,
    '--message', messageText,
  ];
}

function normalizeAgentReply(output) {
  return String(output || '').replace(/\r/g, '').trim();
}

function extractAlertText(output) {
  // Return the normalized agent reply as the alert text.
  // The agent's --message prompt should define a clean output format.
  return normalizeAgentReply(output);
}

function isUsableAlert(output) {
  const reply = normalizeAgentReply(output);
  if (!reply || reply.includes('HEARTBEAT_OK')) return false;
  // Require meaningful content: at least 50 chars and multiple lines or sentences,
  // to avoid treating CLI noise or error fragments as actionable alerts
  if (reply.length < 50) return false;
  const hasStructure = reply.includes('\n') || (reply.match(/[.!?:]\s/g) || []).length >= 2;
  return hasStructure;
}



async function main() {
  const { command, options } = parseArgs();
  const trigger = command === 'detect-and-trigger' || isTruthy(options.trigger);
  const statePath = (() => {
    const raw = path.resolve(expandHome(options.state || DEFAULT_STATE_PATH));
    // Constrain state path to workspace unless OPENCLAW_WORKSPACE is explicitly set (admin override)
    if (!process.env.OPENCLAW_WORKSPACE && raw !== WORKSPACE_ROOT && !raw.startsWith(WORKSPACE_ROOT + path.sep)) {
      console.error(JSON.stringify({ status: 'error', message: `--state path must be inside workspace: ${raw}` }, null, 2));
      process.exit(1);
    }
    return raw;
  })();
  const mailbox = options.mailbox || undefined;
  const limit = Number(options.limit) || 20;
  const recent = options.recent || null;
  const openclawBin = expandHome(options['openclaw-bin'] || 'openclaw');
  const checkedAt = new Date().toISOString();

  const lockPath = acquireLock(statePath);
  if (!lockPath) {
    console.log(JSON.stringify({ status: 'skipped', reason: 'another instance is running' }, null, 2));
    return;
  }
  // Ensure lock is released on exit
  const cleanup = () => releaseLock(lockPath);
  process.on('exit', cleanup);
  process.on('SIGTERM', () => { cleanup(); process.exit(0); });
  process.on('SIGINT', () => { cleanup(); process.exit(0); });

  const state = loadState(statePath);
  state.lastCheckedAt = checkedAt;

  let messages;
  try {
    messages = await checkEmails(mailbox, limit, recent, true);
    state.lastSuccessfulCheckAt = checkedAt;
    state.failureStreak = 0;
    state.lastErrorSummary = null;
  } catch (error) {
    state.failureStreak = Number(state.failureStreak || 0) + 1;
    state.lastErrorSummary = error.message;
    saveState(statePath, state);

    // Escalate to the user after repeated failures
    if (trigger && options.to && state.failureStreak >= FAILURE_ALERT_THRESHOLD) {
      const lastAlert = state.lastFailureAlertAt ? new Date(state.lastFailureAlertAt).getTime() : 0;
      const now = Date.now();
      if (now - lastAlert > FAILURE_ALERT_COOLDOWN_MS) {
        const alertMsg = `⚠️ email-watch failure: ${state.failureStreak} consecutive attempts failed.\nError: ${error.message}\nAction: check IMAP connection and service.`;
        try {
          execFileSync(openclawBin, buildSendArgs(options, alertMsg), {
            cwd: WORKSPACE_ROOT, encoding: 'utf8', stdio: 'pipe', env: process.env,
            timeout: CHILD_PROCESS_TIMEOUT_MS,
          });
          state.lastFailureAlertAt = new Date().toISOString();
          saveState(statePath, state);
        } catch { /* alert send failed — don't crash the detector */ }
      }
    }

    console.error(JSON.stringify({ status: 'error', message: error.message }, null, 2));
    process.exit(1);
  }

  const unseenUids = normalizeUidList(messages.map(message => message.uid));

  if (!state.baselineCapturedAt) {
    state.baselineCapturedAt = checkedAt;
    // Move unseen UIDs into pendingUids so they get analyzed, not silently skipped
    state.pendingUids = mergeUidLists(state.pendingUids, unseenUids);
    saveState(statePath, state);
    console.log(JSON.stringify({
      status: 'baseline-captured',
      unseenCount: unseenUids.length,
      pendingUids: state.pendingUids,
    }, null, 2));
    // On first baseline with pending UIDs, fall through to trigger if enabled
    if (state.pendingUids.length === 0 || !trigger) return;
  }

  const processed = new Set(state.processedUids);
  const pending = new Set(state.pendingUids);
  const newPendingUids = unseenUids.filter(uid => !processed.has(uid) && !pending.has(uid));

  if (newPendingUids.length > 0) {
    state.pendingUids = mergeUidLists(state.pendingUids, newPendingUids);
  }

  saveState(statePath, state);

  if (state.pendingUids.length === 0) {
    console.log(JSON.stringify({
      status: 'idle',
      unseenCount: unseenUids.length,
      newPendingUids: [],
      pendingUids: [],
    }, null, 2));
    return;
  }

  if (!trigger) {
    console.log(JSON.stringify({
      status: 'pending',
      unseenCount: unseenUids.length,
      newPendingUids,
      pendingUids: state.pendingUids,
    }, null, 2));
    return;
  }

  if (!options.to) {
    console.error(JSON.stringify({
      status: 'error',
      message: '--to is required with detect-and-trigger',
    }, null, 2));
    process.exit(1);
  }

  state.lastAnalysisTriggeredAt = checkedAt;
  saveState(statePath, state);

  const sessionId = options['session-id'] || `email-watch-${Date.now()}-${randomUUID().slice(0, 8)}`;
  const agentArgs = buildAgentArgs(options, sessionId);

  if (isTruthy(options['dry-run'])) {
    console.log(JSON.stringify({
      status: 'dry-run',
      sessionId,
      newPendingUids,
      pendingUids: state.pendingUids,
      command: openclawBin,
      args: agentArgs,
    }, null, 2));
    return;
  }

  const pendingBeforeTrigger = [...state.pendingUids];
  const retryCountsBeforeTrigger = { ...(state.deliveryRetryCounts || {}) };

  try {

    const agentOutput = execFileSync(openclawBin, agentArgs, {
      cwd: WORKSPACE_ROOT,
      encoding: 'utf8',
      stdio: 'pipe',
      env: process.env,
      timeout: CHILD_PROCESS_TIMEOUT_MS,
    });

    const refreshedState = loadState(statePath);
    refreshedState.lastAnalysisTriggeredAt = toIso(refreshedState.lastAnalysisTriggeredAt) || checkedAt;
    refreshedState.lastAnalysisCompletedAt = new Date().toISOString();
    // Restore retry counts — the agent may have omitted or reset this field
    refreshedState.deliveryRetryCounts = retryCountsBeforeTrigger;

    const visibleReply = normalizeAgentReply(agentOutput);
    const pendingAfterTrigger = new Set(refreshedState.pendingUids);
    const handledUids = pendingBeforeTrigger.filter(uid => !pendingAfterTrigger.has(uid));

    let status;

    if (isUsableAlert(visibleReply)) {
      // Valid alert — extract clean alert text and send to the user, clear retry counts
      const alertText = extractAlertText(visibleReply);
      execFileSync(openclawBin, buildSendArgs(options, alertText), {
        cwd: WORKSPACE_ROOT,
        encoding: 'utf8',
        stdio: 'pipe',
        env: process.env,
        timeout: CHILD_PROCESS_TIMEOUT_MS,
      });
      for (const uid of handledUids) {
        delete refreshedState.deliveryRetryCounts[String(uid)];
      }
      status = 'triggered';
    } else if (handledUids.length > 0) {
      // Agent returned noop/malformed but handled UIDs — apply retry logic
      let requeuedCount = 0;
      for (const uid of handledUids) {
        const key = String(uid);
        const retries = Number(refreshedState.deliveryRetryCounts[key] || 0);
        if (retries < DELIVERY_RETRY_CAP) {
          refreshedState.deliveryRetryCounts[key] = retries + 1;
          if (!refreshedState.pendingUids.includes(uid)) {
            refreshedState.pendingUids.push(uid);
          }
          requeuedCount++;
        } else {
          // Cap reached — accept the agent's no-alert decision
          delete refreshedState.deliveryRetryCounts[key];
        }
      }
      status = requeuedCount > 0 ? 'retry-requeued' : 'no-alert';
    } else {
      // No UIDs handled (pendingUids was empty or agent left them pending)
      status = 'no-alert';
    }

    // Cleanup: remove retry entries for UIDs no longer relevant
    const relevantUids = new Set([
      ...refreshedState.pendingUids.map(String),
      ...handledUids.map(String),
    ]);
    for (const key of Object.keys(refreshedState.deliveryRetryCounts)) {
      if (!relevantUids.has(key)) {
        delete refreshedState.deliveryRetryCounts[key];
      }
    }

    saveState(statePath, refreshedState);

    console.log(JSON.stringify({
      status,
      sessionId,
      newPendingUids,
      pendingUids: refreshedState.pendingUids,
    }, null, 2));
  } catch (error) {
    const refreshedState = loadState(statePath);
    // Restore retry counts — agent may have rewritten state before crashing
    refreshedState.deliveryRetryCounts = retryCountsBeforeTrigger;
    // Preserve pending UIDs — if agent timed out or crashed, don't lose them
    const currentPending = new Set(refreshedState.pendingUids);
    for (const uid of pendingBeforeTrigger) {
      if (!currentPending.has(uid)) {
        refreshedState.pendingUids.push(uid);
      }
    }
    const stderr = error.stderr ? String(error.stderr).trim() : '';
    const stdout = error.stdout ? String(error.stdout).trim() : '';
    const isTimeout = error.killed || (error.signal === 'SIGTERM');
    refreshedState.lastErrorSummary = isTimeout
      ? `timeout after ${CHILD_PROCESS_TIMEOUT_MS / 1000}s`
      : (stderr || stdout || error.message);
    saveState(statePath, refreshedState);

    console.error(JSON.stringify({
      status: isTimeout ? 'timeout' : 'error',
      message: 'analysis trigger failed',
      detail: refreshedState.lastErrorSummary,
    }, null, 2));
    process.exit(1);
  }
}

main();
