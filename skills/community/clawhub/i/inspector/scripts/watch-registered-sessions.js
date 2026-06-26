#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const {
  registryPath,
  logsDir,
  openclawBin,
  nowIso,
  ensureRegistry,
  parseSessionFile,
  findSessionFile,
  readState,
  writeState,
  mergeConfig,
} = require('./common');

const skillHome = path.resolve(__dirname, '..');

function loadPromptFile(relativePath) {
  const fullPath = path.join(skillHome, relativePath);
  return fs.readFileSync(fullPath, 'utf8').trimEnd();
}

const RECOVERY_MESSAGE_TEMPLATE = loadPromptFile('prompts/recovery.txt');

const INACTIVE_MESSAGE_TEMPLATE = loadPromptFile('prompts/inactive.txt');

function usage() {
  console.log(`Usage:\n  node scripts/watch-registered-sessions.js [--once] [--dry-run] [--test] [--interval <sec>]\n\nCompatibility wrappers on Unix-like systems:\n  scripts/watch-registered-sessions.sh ...`);
}

function parseArgs(argv) {
  const args = {
    once: false,
    dryRun: false,
    test: false,
    interval: undefined,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    switch (arg) {
      case '--once':
        args.once = true;
        break;
      case '--dry-run':
        args.dryRun = true;
        break;
      case '--test':
        args.test = true;
        args.once = true;
        break;
      case '--interval':
        if (argv[i + 1] === undefined) throw new Error('missing value for --interval');
        args.interval = Number(argv[i + 1]);
        if (!Number.isFinite(args.interval) || args.interval <= 0) throw new Error('--interval must be a positive number');
        i += 1;
        break;
      case '-h':
      case '--help':
        args.help = true;
        break;
      default:
        throw new Error(`unknown arg: ${arg}`);
    }
  }
  return args;
}

function numberEnv(config, key, fallback) {
  const value = Number(config[key]);
  return Number.isFinite(value) ? value : fallback;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function scanRegisteredSessions(config) {
  const registry = ensureRegistry();
  const maxAge = numberEnv(config, 'DEFAULT_MAX_LAST_ACTIVITY_AGE_SECONDS', 43200);
  const statusLookback = numberEnv(config, 'DEFAULT_MAX_STATUS_LOOKBACK_MESSAGES', 5);
  const nowEpoch = Math.floor(Date.now() / 1000);
  const items = [];

  for (const entry of registry.sessions) {
    if (entry.enabled === false) continue;
    if (!entry.session_id) {
      items.push({ registry: entry, error: 'missing_session_id' });
      continue;
    }
    const sessionFile = findSessionFile(entry.session_id);
    const parsed = parseSessionFile(sessionFile, statusLookback);
    if (!parsed) {
      items.push({ registry: entry, error: 'session_file_not_found' });
      continue;
    }
    parsed.too_old = (nowEpoch - parsed.last_activity_epoch) > maxAge;
    items.push({ registry: entry, session: parsed });
  }

  return {
    generated_at: nowIso(),
    items,
  };
}

function mergedCandidate(registry, session, config) {
  return {
    ...session,
    session_id: registry.session_id,
    session_key: registry.session_key || '',
    delivery_channel: registry.delivery_channel || '',
    delivery_target: registry.delivery_target || '',
    delivery_account_id: registry.delivery_account_id || '',
    profile: registry.profile || 'default',
    registry_agent: registry.agent || '',
    inactive_threshold_seconds: registry.inactive_threshold_seconds ?? numberEnv(config, 'DEFAULT_INACTIVE_THRESHOLD_SECONDS', 1800),
    cooldown_seconds: registry.cooldown_seconds ?? numberEnv(config, 'DEFAULT_COOLDOWN_SECONDS', 3600),
    running_cooldown_seconds: registry.running_cooldown_seconds ?? numberEnv(config, 'DEFAULT_RUNNING_COOLDOWN_SECONDS', 600),
    blocked_cooldown_seconds: registry.blocked_cooldown_seconds ?? numberEnv(config, 'DEFAULT_BLOCKED_COOLDOWN_SECONDS', 3600),
    notes: registry.notes || '',
  };
}

function buildCandidateLists(scanJson, config) {
  const nowEpoch = Math.floor(Date.now() / 1000);
  const recovery = [];
  const inactive = [];
  const errors = [];

  for (const item of scanJson.items) {
    if (item.error) {
      errors.push(item);
      continue;
    }
    if (!item.session || item.session.too_old) continue;
    const candidate = mergedCandidate(item.registry, item.session, config);
    if (
      ['aborted', 'error', 'failed'].includes(candidate.terminal_status)
      && candidate.terminal_epoch > 0
      && candidate.terminal_epoch >= candidate.last_activity_epoch
      && (nowEpoch - candidate.terminal_epoch) >= 300
    ) {
      recovery.push(candidate);
    }
    if (candidate.last_activity_epoch > 0 && (nowEpoch - candidate.last_activity_epoch) >= candidate.inactive_threshold_seconds) {
      inactive.push(candidate);
    }
  }

  return { recovery, inactive, errors };
}

function markLatestStatuses(scanJson, config) {
  for (const item of scanJson.items) {
    const status = item.session?.latest_status?.marker;
    if (!status) continue;
    const sessionId = item.registry.session_id;
    const epoch = item.session.latest_status.epoch || 0;
    let cooldownUntil = 0;
    if (status === 'RUNNING') cooldownUntil = epoch + (item.registry.running_cooldown_seconds ?? numberEnv(config, 'DEFAULT_RUNNING_COOLDOWN_SECONDS', 600));
    if (status === 'BLOCKED') cooldownUntil = epoch + (item.registry.blocked_cooldown_seconds ?? numberEnv(config, 'DEFAULT_BLOCKED_COOLDOWN_SECONDS', 3600));
    writeState(sessionId, {
      session_id: sessionId,
      status: 'status_ack',
      reason: `assistant_reported_${String(status).toLowerCase()}`,
      workdir: item.session.workdir || '',
      session_file: item.session.session_file || '',
      last_activity: item.session.last_activity || '',
      last_activity_epoch: item.session.last_activity_epoch || 0,
      alert_type: 'status',
      status_ack: status,
      status_ack_at: epoch,
      cooldown_until: cooldownUntil,
      updated_at: nowIso(),
    });
  }
}

function shouldSkipCandidate(candidate, alertType) {
  const nowEpoch = Math.floor(Date.now() / 1000);
  const latestMarker = candidate.latest_status?.marker || '';
  const latestEpoch = candidate.latest_status?.epoch || 0;
  const lastActivityEpoch = candidate.last_activity_epoch || 0;

  if ((latestMarker === 'DONE' || latestMarker === 'WAITING') && latestEpoch > 0 && lastActivityEpoch <= latestEpoch) {
    return true;
  }
  if (latestMarker === 'RUNNING' && latestEpoch > 0 && lastActivityEpoch <= latestEpoch && latestEpoch + candidate.running_cooldown_seconds > nowEpoch) {
    return true;
  }
  if (latestMarker === 'BLOCKED' && latestEpoch > 0 && lastActivityEpoch <= latestEpoch && latestEpoch + candidate.blocked_cooldown_seconds > nowEpoch) {
    return true;
  }

  const state = readState(candidate.session_id);
  if (state.status_ack && state.status_ack_at) {
    if ((state.status_ack === 'DONE' || state.status_ack === 'WAITING') && lastActivityEpoch <= state.status_ack_at) return true;
    if ((state.status_ack === 'RUNNING' || state.status_ack === 'BLOCKED') && lastActivityEpoch <= state.status_ack_at && Number(state.cooldown_until || 0) > nowEpoch) return true;
  }

  if (
    state.status === 'notified'
    && Number(state.notified_at || 0) > 0
    && lastActivityEpoch <= Number(state.notified_at || 0)
    && state.alert_type === alertType
    && (Number(state.notified_at) + candidate.cooldown_seconds) > nowEpoch
  ) {
    return true;
  }

  return false;
}

function writeLog(file, lines) {
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function resolveDeliveryTarget(candidate) {
  const channel = String(candidate.delivery_channel || '').trim();
  const target = String(candidate.delivery_target || '').trim();
  const accountId = String(candidate.delivery_account_id || '').trim();
  if (!channel || !target || !accountId) return null;

  return {
    channel,
    target,
    accountId,
    source: 'registry',
  };
}

function dispatchNotification(candidate, alertType, args, config) {
  const sessionId = candidate.session_id;
  const logPrefix = path.join(logsDir, `${sessionId}.${alertType}`);
  const logFile = `${logPrefix}.log`;
  const agentLog = `${logPrefix}.agent.log`;
  const nowEpoch = Math.floor(Date.now() / 1000);
  const message = alertType === 'recovery' ? RECOVERY_MESSAGE_TEMPLATE : INACTIVE_MESSAGE_TEMPLATE;
  const delivery = resolveDeliveryTarget(candidate);

  if (args.dryRun || args.test) {
    console.log(`[dry-run] would inspect ${sessionId} via ${alertType}`);
    return;
  }

  writeLog(logFile, [
    `timestamp=${nowIso()}`,
    `session_id=${sessionId}`,
    `alert_type=${alertType}`,
    `workdir=${candidate.workdir || ''}`,
    `session_key=${candidate.session_key || ''}`,
    `delivery_channel=${delivery?.channel || ''}`,
    `delivery_target=${delivery?.target || ''}`,
    `delivery_account_id=${delivery?.accountId || ''}`,
    `delivery_source=${delivery?.source || ''}`,
  ]);

  if (!delivery) {
    writeState(sessionId, {
      session_id: sessionId,
      status: 'pending',
      reason: 'missing_delivery_target',
      workdir: candidate.workdir || '',
      session_file: candidate.session_file || '',
      last_activity: candidate.last_activity || '',
      last_activity_epoch: candidate.last_activity_epoch || 0,
      alert_type: alertType,
      log_file: logFile,
      updated_at: nowIso(),
    });
    writeLog(agentLog, [
      'exit_code=',
      'signal=',
      '--- stdout ---',
      '',
      '--- stderr ---',
      `ERROR: missing complete delivery triple in registry for session_id=${sessionId}`,
    ]);
    return;
  }

  writeState(sessionId, {
    session_id: sessionId,
    status: 'dispatching',
    reason: `${alertType}_delivery_in_progress`,
    workdir: candidate.workdir || '',
    session_file: candidate.session_file || '',
    last_activity: candidate.last_activity || '',
    last_activity_epoch: candidate.last_activity_epoch || 0,
    alert_type: alertType,
    notified_at: nowEpoch,
    updated_at: nowIso(),
  });

  const timeoutSeconds = numberEnv(config, 'AGENT_CLI_TIMEOUT_SECONDS', 180);
  const result = spawnSync(openclawBin, [
    'agent',
    '--session-id', sessionId,
    '--message', message,
    ...(delivery.accountId ? ['--reply-account', delivery.accountId] : []),
    '--reply-channel', delivery.channel,
    '--to', delivery.target,
    '--deliver',
    '--timeout', '120',
    '--thinking', 'minimal',
    '--json',
  ], {
    encoding: 'utf8',
    timeout: timeoutSeconds * 1000,
  });

  writeLog(agentLog, [
    `exit_code=${result.status ?? ''}`,
    `signal=${result.signal ?? ''}`,
    '--- stdout ---',
    result.stdout || '',
    '--- stderr ---',
    result.stderr || '',
  ]);

  if (result.error || result.status !== 0) {
    let reason = 'agent_cli_failed';
    let status = 'pending';
    const stderr = `${result.stderr || ''}\n${result.stdout || ''}`;
    if (result.error && result.error.code === 'ETIMEDOUT') reason = 'agent_cli_timeout';
    if (/Unknown sessionId/i.test(stderr)) {
      reason = 'unknown_session_id';
      status = 'abandoned';
    }
    writeState(sessionId, {
      session_id: sessionId,
      status,
      reason,
      workdir: candidate.workdir || '',
      session_file: candidate.session_file || '',
      last_activity: candidate.last_activity || '',
      last_activity_epoch: candidate.last_activity_epoch || 0,
      alert_type: alertType,
      log_file: logFile,
      updated_at: nowIso(),
    });
    return;
  }

  writeState(sessionId, {
    session_id: sessionId,
    status: 'notified',
    reason: `${alertType}_delivery_requested`,
    workdir: candidate.workdir || '',
    session_file: candidate.session_file || '',
    last_activity: candidate.last_activity || '',
    last_activity_epoch: candidate.last_activity_epoch || 0,
    alert_type: alertType,
    notified_at: nowEpoch,
    log_file: logFile,
    updated_at: nowIso(),
  });
}

function runScan(args) {
  const config = mergeConfig();
  const scanJson = scanRegisteredSessions(config);
  markLatestStatuses(scanJson, config);
  const candidates = buildCandidateLists(scanJson, config);

  if (args.test) {
    console.log(JSON.stringify({ scan: scanJson, candidates }, null, 2));
    return;
  }

  for (const item of candidates.recovery) {
    if (!shouldSkipCandidate(item, 'recovery')) dispatchNotification(item, 'recovery', args, config);
  }
  for (const item of candidates.inactive) {
    if (!shouldSkipCandidate(item, 'inactive')) dispatchNotification(item, 'inactive', args, config);
  }

  if (!args.dryRun) {
    console.log(`[${nowIso()}] scan complete`);
  }
}

async function main() {
  let args;
  try {
    args = parseArgs(process.argv.slice(2));
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    process.exit(1);
  }

  if (args.help) {
    usage();
    return;
  }

  ensureRegistry();
  while (true) {
    runScan(args);
    if (args.once) break;
    const config = mergeConfig();
    const interval = args.interval || numberEnv(config, 'SCAN_INTERVAL_SECONDS', 30);
    await sleep(interval * 1000);
  }
}

main().catch((error) => {
  console.error(`ERROR: ${error.stack || error.message}`);
  process.exit(1);
});
