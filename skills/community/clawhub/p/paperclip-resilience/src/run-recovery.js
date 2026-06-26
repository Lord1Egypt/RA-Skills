#!/usr/bin/env node
/**
 * paperclip-run-recovery.js
 *
 * Detects recent Paperclip heartbeat-run failures caused by configured error codes
 * (default: openclaw_gateway_wait_error, timeout) and re-invokes the assigned
 * agent's heartbeat so it can resume work after a gateway restart.
 *
 * Also detects 429 rate-limit deaths from session transcripts. When a session
 * dies from a 429/rate_limit error, re-wakes the agent with an explicit model
 * override to the next fallback in the chain. Model fallback order is read from
 * the agent's config in ~/.openclaw/openclaw.json, not hardcoded.
 *
 * Recovery target, auth, paths, and recovery parameters are fully configurable
 * via CLI flags, environment variables, and config files.
 *
 * Run:
 *   node scripts/paperclip-run-recovery.js [--dry-run] [--verbose] [--force]
 *     [--max-age-hours=3] [--invoke-gap-minutes=5]
 *     [--error-codes=openclaw_gateway_wait_error,timeout]
 *     [--agent-id=<paperclip-agent-uuid>] [--openclaw-agent-id=<session-key>]
 *     [--state-path=/abs/path/state.json]
 */

'use strict';

const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const https = require('node:https');

// ── Defaults ────────────────────────────────────────────────────────────────

const DEFAULT_WORKSPACE = path.resolve(__dirname, '..');
const DEFAULT_HOME_DIR = process.env.HOME || require('os').homedir();
const DEFAULT_MAX_AGE_HOURS = 3;
const DEFAULT_MIN_INVOKE_GAP_MS = 5 * 60 * 1000; // 5 min
const DEFAULT_RECOVERY_ERROR_CODES = ['openclaw_gateway_wait_error', 'timeout'];
const MAX_PROCESSED_IDS = 500;
const RATE_LIMIT_PATTERNS = [/429/i, /rate.?limit/i, /cooling.?down/i];
const TRANSCRIPT_TAIL_LINES = 10;

// ── Helpers ─────────────────────────────────────────────────────────────────

function parseBoolean(value) {
  if (typeof value !== 'string') return false;
  return ['1', 'true', 'yes', 'on'].includes(value.trim().toLowerCase());
}

function parseNumber(value, fallback) {
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

function parseCsv(value, fallback = []) {
  if (!value) return fallback;
  return String(value)
    .split(',')
    .map((part) => part.trim())
    .filter(Boolean);
}

function resolveMaybeRelative(baseDir, targetPath) {
  if (!targetPath) return null;
  return path.isAbsolute(targetPath) ? targetPath : path.resolve(baseDir, targetPath);
}

function fileExists(targetPath) {
  try {
    return fs.existsSync(targetPath);
  } catch {
    return false;
  }
}

function sanitizeFileSegment(value) {
  return String(value || 'unknown').replace(/[^a-zA-Z0-9._-]+/g, '-');
}

function parseEnvFile(filePath) {
  const values = {};
  if (!filePath || !fileExists(filePath)) return values;

  const content = fs.readFileSync(filePath, 'utf8');
  for (const rawLine of content.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) continue;
    const match = line.match(/^(?:export\s+)?([A-Z0-9_]+)=(.*)$/);
    if (!match) continue;
    let [, key, value] = match;
    value = value.trim();
    value = value.replace(/^['"]|['"]$/g, '');
    values[key] = value;
  }
  return values;
}

// ── Arg parsing ─────────────────────────────────────────────────────────────

function parseArgs(argv) {
  const args = {
    dryRun: false,
    verbose: false,
    force: false,
    maxAgeHours: null,
    minInvokeGapMs: null,
    recoveryErrorCodes: null,
    runId: process.env.PAPERCLIP_RUN_ID || null,
    workspace: null,
    envPath: null,
    apiKeyFile: null,
    openclawConfigPath: null,
    sessionsBaseDir: null,
    statePath: null,
    lockPath: null,
    apiKey: null,
    apiUrl: null,
    companyId: null,
    agentId: null,
    openclawAgentId: null,
  };

  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--dry-run') args.dryRun = true;
    else if (arg === '--verbose' || arg === '-v') args.verbose = true;
    else if (arg === '--force') args.force = true;
    else if (arg.startsWith('--max-age-hours=') || arg.startsWith('--window-hours=')) {
      args.maxAgeHours = Number(arg.split('=')[1]);
    } else if (arg.startsWith('--invoke-gap-ms=')) {
      args.minInvokeGapMs = Number(arg.split('=')[1]);
    } else if (arg.startsWith('--invoke-gap-minutes=')) {
      args.minInvokeGapMs = Number(arg.split('=')[1]) * 60 * 1000;
    } else if (arg.startsWith('--error-codes=')) {
      args.recoveryErrorCodes = parseCsv(arg.split('=')[1]);
    } else if (arg.startsWith('--run-id=')) {
      args.runId = arg.split('=')[1] || null;
    } else if (arg.startsWith('--workspace=')) {
      args.workspace = arg.split('=')[1] || null;
    } else if (arg.startsWith('--env-path=')) {
      args.envPath = arg.split('=')[1] || null;
    } else if (arg.startsWith('--api-key-file=')) {
      args.apiKeyFile = arg.split('=')[1] || null;
    } else if (arg.startsWith('--openclaw-config-path=')) {
      args.openclawConfigPath = arg.split('=')[1] || null;
    } else if (arg.startsWith('--sessions-base-dir=')) {
      args.sessionsBaseDir = arg.split('=')[1] || null;
    } else if (arg.startsWith('--state-path=')) {
      args.statePath = arg.split('=')[1] || null;
    } else if (arg.startsWith('--lock-path=')) {
      args.lockPath = arg.split('=')[1] || null;
    } else if (arg.startsWith('--api-key=')) {
      args.apiKey = arg.split('=')[1] || null;
    } else if (arg.startsWith('--api-url=')) {
      args.apiUrl = arg.split('=')[1] || null;
    } else if (arg.startsWith('--company-id=')) {
      args.companyId = arg.split('=')[1] || null;
    } else if (arg.startsWith('--agent-id=')) {
      args.agentId = arg.split('=')[1] || null;
    } else if (arg.startsWith('--openclaw-agent-id=')) {
      args.openclawAgentId = arg.split('=')[1] || null;
    }
  }

  return args;
}

function buildRuntimeConfig(args) {
  const workspace = resolveMaybeRelative(process.cwd(),
    args.workspace || process.env.PAPERCLIP_RUN_RECOVERY_WORKSPACE || DEFAULT_WORKSPACE,
  );
  const homeDir = process.env.HOME || DEFAULT_HOME_DIR;

  const envPath = resolveMaybeRelative(workspace,
    args.envPath || process.env.PAPERCLIP_RUN_RECOVERY_ENV_PATH || path.join(workspace, 'config', 'paperclip-env.sh'),
  );

  return {
    dryRun: args.dryRun || parseBoolean(process.env.PAPERCLIP_RUN_RECOVERY_DRY_RUN),
    verbose: args.verbose || parseBoolean(process.env.PAPERCLIP_RUN_RECOVERY_VERBOSE),
    force: args.force || parseBoolean(process.env.PAPERCLIP_RUN_RECOVERY_FORCE),
    runId: args.runId || process.env.PAPERCLIP_RUN_ID || null,
    workspace,
    envPath,
    apiKeyFile: resolveMaybeRelative(workspace,
      args.apiKeyFile || process.env.PAPERCLIP_RUN_RECOVERY_API_KEY_FILE ||
      path.join(homeDir, '.openclaw', 'workspace', 'paperclip-api-key.json'),
    ),
    openclawConfigPath: resolveMaybeRelative(workspace,
      args.openclawConfigPath || process.env.PAPERCLIP_RUN_RECOVERY_OPENCLAW_CONFIG_PATH ||
      path.join(homeDir, '.openclaw', 'openclaw.json'),
    ),
    sessionsBaseDir: resolveMaybeRelative(workspace,
      args.sessionsBaseDir || process.env.PAPERCLIP_RUN_RECOVERY_SESSIONS_BASE_DIR ||
      path.join(homeDir, '.openclaw', 'agents'),
    ),
    statePathOverride: resolveMaybeRelative(workspace,
      args.statePath || process.env.PAPERCLIP_RUN_RECOVERY_STATE_PATH || null,
    ),
    lockPathOverride: resolveMaybeRelative(workspace,
      args.lockPath || process.env.PAPERCLIP_RUN_RECOVERY_LOCK_PATH || null,
    ),
    maxAgeHours: parseNumber(
      args.maxAgeHours ?? process.env.PAPERCLIP_RUN_RECOVERY_MAX_AGE_HOURS,
      DEFAULT_MAX_AGE_HOURS,
    ),
    minInvokeGapMs: parseNumber(
      args.minInvokeGapMs ?? process.env.PAPERCLIP_RUN_RECOVERY_MIN_INVOKE_GAP_MS,
      DEFAULT_MIN_INVOKE_GAP_MS,
    ),
    recoveryErrorCodes: new Set(
      parseCsv(
        args.recoveryErrorCodes?.join(',') ?? process.env.PAPERCLIP_RUN_RECOVERY_ERROR_CODES,
        DEFAULT_RECOVERY_ERROR_CODES,
      ),
    ),
    authOverrides: {
      apiKey:
        args.apiKey ||
        process.env.PAPERCLIP_RUN_RECOVERY_API_KEY ||
        process.env.PAPERCLIP_API_KEY ||
        null,
      apiUrl:
        args.apiUrl ||
        process.env.PAPERCLIP_RUN_RECOVERY_API_URL ||
        process.env.PAPERCLIP_API_URL ||
        null,
      companyId:
        args.companyId ||
        process.env.PAPERCLIP_RUN_RECOVERY_COMPANY_ID ||
        process.env.PAPERCLIP_COMPANY_ID ||
        null,
      agentId:
        args.agentId ||
        process.env.PAPERCLIP_RUN_RECOVERY_AGENT_ID ||
        process.env.PAPERCLIP_AGENT_ID ||
        null,
      openclawAgentId:
        args.openclawAgentId ||
        process.env.PAPERCLIP_RUN_RECOVERY_OPENCLAW_AGENT_ID ||
        process.env.PAPERCLIP_AGENT_NAME ||
        null,
    },
  };
}

// ── Auth loading ────────────────────────────────────────────────────────────

function loadAuth(runtime) {
  const envFile = parseEnvFile(runtime.envPath);

  let apiKey = runtime.authOverrides.apiKey;
  let apiUrl = runtime.authOverrides.apiUrl;
  let companyId = runtime.authOverrides.companyId;
  let agentId = runtime.authOverrides.agentId;
  let openclawAgentId = runtime.authOverrides.openclawAgentId;

  if (!apiKey) {
    apiKey =
      envFile.PAPERCLIP_RUN_RECOVERY_API_KEY ||
      envFile.PAPERCLIP_API_KEY ||
      null;
  }
  if (!agentId) {
    agentId =
      envFile.PAPERCLIP_RUN_RECOVERY_AGENT_ID ||
      envFile.PAPERCLIP_AGENT_ID ||
      null;
  }
  if (!apiUrl) {
    apiUrl =
      envFile.PAPERCLIP_RUN_RECOVERY_API_URL ||
      envFile.PAPERCLIP_API_URL ||
      null;
  }
  if (!companyId) {
    companyId =
      envFile.PAPERCLIP_RUN_RECOVERY_COMPANY_ID ||
      envFile.PAPERCLIP_COMPANY_ID ||
      null;
  }
  if (!openclawAgentId) {
    openclawAgentId =
      envFile.PAPERCLIP_RUN_RECOVERY_OPENCLAW_AGENT_ID ||
      envFile.PAPERCLIP_AGENT_NAME ||
      null;
  }

  if (!apiKey || !agentId) {
    try {
      const fileAuth = JSON.parse(fs.readFileSync(runtime.apiKeyFile, 'utf8'));
      if (!apiKey) apiKey = fileAuth.token;
      if (!agentId) agentId = fileAuth.agentId;
      if (!apiUrl) apiUrl = fileAuth.apiUrl;
      if (!companyId) companyId = fileAuth.companyId;
    } catch {
      throw new Error(
        'Cannot load Paperclip auth. Provide PAPERCLIP_RUN_RECOVERY_* env vars, ' +
        `configure ${runtime.envPath}, or provide ${runtime.apiKeyFile}.`,
      );
    }
  }

  if (!apiKey) throw new Error('Paperclip API key not found');
  if (!agentId) throw new Error('Paperclip agent ID not found');
  if (!companyId) throw new Error('Paperclip company ID not found');

  return {
    apiKey,
    agentId,
    apiUrl: (apiUrl || '').replace(/\/$/, '') || (() => { throw new Error('Paperclip API URL not found. Set PAPERCLIP_API_URL or pass --api-url.'); })(),
    companyId,
    openclawAgentId,
  };
}

// ── HTTP helper ─────────────────────────────────────────────────────────────

function apiFetch(auth, method, pathname, body = null, runId = null) {
  const url = new URL(`${auth.apiUrl}${pathname}`);
  const lib = url.protocol === 'https:' ? https : http;
  const bodyStr = body != null ? JSON.stringify(body) : null;

  const headers = {
    Authorization: `Bearer ${auth.apiKey}`,
    'Content-Type': 'application/json',
  };
  if (runId && method !== 'GET') {
    headers['X-Paperclip-Run-Id'] = runId;
  }
  if (bodyStr) {
    headers['Content-Length'] = Buffer.byteLength(bodyStr);
  }

  return new Promise((resolve, reject) => {
    const req = lib.request(
      {
        hostname: url.hostname,
        port: url.port || (url.protocol === 'https:' ? 443 : 80),
        path: url.pathname + url.search,
        method,
        headers,
        timeout: 30_000,
      },
      (res) => {
        let data = '';
        res.on('data', (chunk) => { data += chunk; });
        res.on('end', () => {
          if (res.statusCode >= 200 && res.statusCode < 300) {
            try { resolve(JSON.parse(data)); } catch { resolve(data); }
          } else {
            reject(new Error(`HTTP ${res.statusCode}: ${data.slice(0, 300)}`));
          }
        });
      },
    );
    req.on('timeout', () => { req.destroy(); reject(new Error('Request timed out after 30s')); });
    req.on('error', reject);
    if (bodyStr) req.write(bodyStr);
    req.end();
  });
}

// ── Agent identity & paths ──────────────────────────────────────────────────

async function resolveAgentIdentity(auth) {
  if (auth.openclawAgentId) {
    return {
      paperclipAgentId: auth.agentId,
      openclawAgentId: auth.openclawAgentId,
      displayName: auth.openclawAgentId,
    };
  }

  try {
    const me = await apiFetch(auth, 'GET', '/api/agents/me');
    if (!me || me.id !== auth.agentId) {
      return {
        paperclipAgentId: auth.agentId,
        openclawAgentId: null,
        displayName: me?.name || auth.agentId,
      };
    }
    return {
      paperclipAgentId: auth.agentId,
      openclawAgentId: me?.adapterConfig?.agentId || me?.urlKey || null,
      displayName: me?.name || me?.urlKey || auth.agentId,
    };
  } catch {
    return {
      paperclipAgentId: auth.agentId,
      openclawAgentId: null,
      displayName: auth.agentId,
    };
  }
}

function resolveStatePath(runtime, identity) {
  if (runtime.statePathOverride) return runtime.statePathOverride;

  const legacyStatePath = path.join(runtime.workspace, 'memory', 'paperclip-run-recovery-state.json');
  const agentKey = sanitizeFileSegment(identity.openclawAgentId || identity.paperclipAgentId);
  const perAgentStatePath = path.join(
    runtime.workspace,
    'memory',
    `paperclip-run-recovery-state-${agentKey}.json`,
  );

  // Check for legacy state file (backward compat for existing deployments)
  if (fileExists(legacyStatePath)) {
    return legacyStatePath;
  }
  return perAgentStatePath;
}

function resolveLockPath(runtime, statePath) {
  if (runtime.lockPathOverride) return runtime.lockPathOverride;
  const baseName = path.basename(statePath, path.extname(statePath));
  return path.join(runtime.workspace, 'tmp', `${baseName}.lock`);
}

function resolveModelRotationLogPath(runtime) {
  return path.join(runtime.workspace, 'memory', 'model-rotation-log.jsonl');
}

// ── Agent config & model fallback ───────────────────────────────────────────

function loadAgentModelConfig(openclawConfigPath, openclawAgentId) {
  const fallback = { primary: null, fallbacks: [] };
  if (!openclawAgentId) return fallback;

  try {
    const config = JSON.parse(fs.readFileSync(openclawConfigPath, 'utf8'));
    const agents = config.agents || {};

    if (agents.list && Array.isArray(agents.list)) {
      const entry = agents.list.find(
        (agent) => agent.id === openclawAgentId || agent.name?.toLowerCase().startsWith(openclawAgentId),
      );
      if (entry?.model) {
        return {
          primary: entry.model.primary || null,
          fallbacks: Array.isArray(entry.model.fallbacks) ? entry.model.fallbacks : [],
        };
      }
    }

    if (agents.defaults?.model) {
      return {
        primary: agents.defaults.model.primary || null,
        fallbacks: Array.isArray(agents.defaults.model.fallbacks)
          ? agents.defaults.model.fallbacks
          : [],
      };
    }
  } catch {
    // Config missing or unparseable — use fallback
  }

  return fallback;
}

function getNextFallbackModel(failedModel, modelConfig) {
  const chain = [modelConfig.primary, ...modelConfig.fallbacks].filter(Boolean);
  if (chain.length === 0) return null;

  const normalize = (model) => (model || '').toLowerCase().replace(/\s+/g, '');
  const failedNorm = normalize(failedModel);

  const idx = chain.findIndex((model) => normalize(model) === failedNorm);
  if (idx >= 0 && idx < chain.length - 1) {
    return chain[idx + 1];
  }
  return modelConfig.fallbacks[0] || chain[0] || null;
}

// ── Session transcript analysis ─────────────────────────────────────────────

function analyzeSessionTranscript(sessionsBaseDir, openclawAgentId, sessionId) {
  const sessionDir = path.join(sessionsBaseDir, openclawAgentId, 'sessions');
  const sessionFile = path.join(sessionDir, `${sessionId}.jsonl`);

  try {
    if (!fileExists(sessionFile)) return null;

    const content = fs.readFileSync(sessionFile, 'utf8');
    const lines = content.trim().split('\n');
    const tailLines = lines.slice(-TRANSCRIPT_TAIL_LINES);

    let lastErrorMessage = null;
    let lastModel = null;

    for (const line of tailLines) {
      try {
        const entry = JSON.parse(line);
        const msg = entry.message;
        if (!msg) continue;

        if (msg.role === 'assistant' && msg.model) {
          lastModel = msg.model;
        }

        if (msg.stopReason === 'error' && msg.errorMessage) {
          const isRateLimit = RATE_LIMIT_PATTERNS.some((pattern) => pattern.test(msg.errorMessage));
          if (isRateLimit) {
            lastErrorMessage = msg.errorMessage;
            if (msg.model) lastModel = msg.model;
          }
        }
      } catch {
        // Skip malformed lines
      }
    }

    if (!lastErrorMessage) return null;
    return {
      isRateLimitDeath: true,
      failedModel: lastModel,
      errorMessage: lastErrorMessage,
    };
  } catch {
    return null;
  }
}

function checkLatestSessionForRateLimit(sessionsBaseDir, openclawAgentId) {
  if (!openclawAgentId) return null;

  const sessionDir = path.join(sessionsBaseDir, openclawAgentId, 'sessions');
  try {
    if (!fileExists(sessionDir)) return null;

    const files = fs.readdirSync(sessionDir)
      .filter((file) => file.endsWith('.jsonl'))
      .map((file) => ({
        name: file,
        id: file.replace(/\.jsonl$/, ''),
        mtime: fs.statSync(path.join(sessionDir, file)).mtimeMs,
      }))
      .sort((a, b) => b.mtime - a.mtime);

    for (const file of files.slice(0, 5)) {
      const result = analyzeSessionTranscript(sessionsBaseDir, openclawAgentId, file.id);
      if (result?.isRateLimitDeath) {
        return { ...result, sessionId: file.id, sessionMtime: file.mtime };
      }
    }
  } catch {
    return null;
  }

  return null;
}

// ── State helpers ───────────────────────────────────────────────────────────

function loadState(statePath) {
  try {
    if (!fileExists(statePath)) return {};
    const raw = fs.readFileSync(statePath, 'utf8');
    const parsed = JSON.parse(raw);
    return (parsed && typeof parsed === 'object') ? parsed : {};
  } catch {
    return {};
  }
}

function saveState(statePath, state) {
  fs.mkdirSync(path.dirname(statePath), { recursive: true });
  fs.writeFileSync(statePath, JSON.stringify(state, null, 2));
}

// ── Lock helpers ────────────────────────────────────────────────────────────

function acquireLock(lockPath) {
  fs.mkdirSync(path.dirname(lockPath), { recursive: true });

  try {
    const stat = fs.statSync(lockPath);
    if (Date.now() - stat.mtimeMs > 2 * 60 * 1000) {
      fs.unlinkSync(lockPath);
    }
  } catch {
    // no stale lock to clear
  }

  try {
    const fd = fs.openSync(lockPath, 'wx');
    fs.writeSync(fd, String(process.pid));
    return { ok: true, fd };
  } catch {
    return { ok: false };
  }
}

function releaseLock(lockPath, fd) {
  try { fs.closeSync(fd); } catch {}
  try { fs.unlinkSync(lockPath); } catch {}
}

// ── Model rotation log ──────────────────────────────────────────────────────

function logModelRotation(logPath, entry) {
  try {
    fs.mkdirSync(path.dirname(logPath), { recursive: true });
    fs.appendFileSync(logPath, `${JSON.stringify(entry)}\n`);
  } catch {
    // Non-critical
  }
}

// ── Main ────────────────────────────────────────────────────────────────────

async function main() {
  const args = parseArgs(process.argv);
  const runtime = buildRuntimeConfig(args);
  const nowMs = Date.now();
  const maxAgeMs = runtime.maxAgeHours * 60 * 60 * 1000;
  const auth = loadAuth(runtime);
  const identity = await resolveAgentIdentity(auth);
  const statePath = resolveStatePath(runtime, identity);
  const lockPath = resolveLockPath(runtime, statePath);
  const modelRotationLogPath = resolveModelRotationLogPath(runtime);

  const lock = acquireLock(lockPath);
  if (!lock.ok) {
    if (runtime.verbose) console.log(`paperclip-run-recovery: lock held (${lockPath}), skipping`);
    else process.stdout.write('NO_REPLY\n');
    return;
  }

  try {
    const state = loadState(statePath);

    const lastInvokeAt = typeof state.lastInvokeAt === 'number' ? state.lastInvokeAt : 0;
    const sinceLastMs = nowMs - lastInvokeAt;
    if (!runtime.force && sinceLastMs < runtime.minInvokeGapMs) {
      if (runtime.verbose) {
        console.log(
          `paperclip-run-recovery: last invoke ${Math.round(sinceLastMs / 1000)}s ago, ` +
          `min gap is ${Math.round(runtime.minInvokeGapMs / 1000)}s — skipping`,
        );
      } else {
        process.stdout.write('NO_REPLY\n');
      }
      return;
    }

    const runsPath =
      `/api/companies/${auth.companyId}/heartbeat-runs` +
      `?agentId=${auth.agentId}&status=failed&limit=100`;

    let allFailedRuns;
    try {
      allFailedRuns = await apiFetch(auth, 'GET', runsPath);
    } catch (err) {
      if (runtime.verbose) console.error(`paperclip-run-recovery: fetch failed: ${err.message}`);
      else process.stdout.write('NO_REPLY\n');
      return;
    }

    if (!Array.isArray(allFailedRuns)) {
      if (runtime.verbose) console.error('paperclip-run-recovery: unexpected heartbeat-runs response');
      else process.stdout.write('NO_REPLY\n');
      return;
    }

    const processedIds = new Set(
      Array.isArray(state.processedRunIds) ? state.processedRunIds : [],
    );

    const recentFailures = allFailedRuns.filter((run) => {
      if (!run || !run.id) return false;
      if (processedIds.has(run.id)) return false;
      if (!runtime.recoveryErrorCodes.has(run.errorCode)) return false;
      const failedAt = run.finishedAt ? Date.parse(run.finishedAt) : null;
      if (!failedAt || (nowMs - failedAt) > maxAgeMs) return false;
      return true;
    });

    if (runtime.verbose) {
      console.log(
        `paperclip-run-recovery: agent=${identity.displayName}` +
        ` paperclipAgentId=${auth.agentId}` +
        (identity.openclawAgentId ? ` openclawAgentId=${identity.openclawAgentId}` : '') +
        ` state=${statePath}` +
        ` maxAgeHours=${runtime.maxAgeHours}` +
        ` invokeGapMs=${runtime.minInvokeGapMs}` +
        ` errorCodes=[${[...runtime.recoveryErrorCodes].join(', ')}]`,
      );
      console.log(
        `paperclip-run-recovery: scanned ${allFailedRuns.length} failed run(s), found ` +
        `${recentFailures.length} recent recoverable failure(s)`,
      );
    }

    let rateLimitAnalysis = null;
    let modelOverride = null;
    let rateLimitRecovery = false;

    if (identity.openclawAgentId) {
      rateLimitAnalysis = checkLatestSessionForRateLimit(
        runtime.sessionsBaseDir,
        identity.openclawAgentId,
      );
    } else if (runtime.verbose) {
      console.log(
        'paperclip-run-recovery: skipping transcript-based 429 detection ' +
        '(no OpenClaw agent id resolved; set --openclaw-agent-id if needed)',
      );
    }

    if (rateLimitAnalysis) {
      const modelConfig = loadAgentModelConfig(runtime.openclawConfigPath, identity.openclawAgentId);
      const nextModel = getNextFallbackModel(rateLimitAnalysis.failedModel, modelConfig);
      const sessionAgeMs = nowMs - (rateLimitAnalysis.sessionMtime || 0);
      const isRecent = sessionAgeMs < maxAgeMs;
      const alreadyRecovered = state.lastRateLimitSessionId === rateLimitAnalysis.sessionId;

      if (isRecent && !alreadyRecovered) {
        rateLimitRecovery = true;
        modelOverride = nextModel;

        if (runtime.verbose) {
          console.log(
            `paperclip-run-recovery: 429 detected session=${rateLimitAnalysis.sessionId}` +
            ` failedModel=${rateLimitAnalysis.failedModel || 'unknown'}` +
            ` nextFallback=${modelOverride || 'none'}`,
          );
        }
      } else if (runtime.verbose) {
        console.log(
          `paperclip-run-recovery: found rate-limit session but skipped ` +
          `(recent=${isRecent}, alreadyRecovered=${alreadyRecovered}) ` +
          `session=${rateLimitAnalysis.sessionId}`,
        );
      }
    }

    if (recentFailures.length === 0 && !rateLimitRecovery) {
      saveState(statePath, {
        ...state,
        lastCheckedAt: nowMs,
        processedRunIds: [...processedIds].slice(-MAX_PROCESSED_IDS),
      });
      if (!runtime.verbose) process.stdout.write('NO_REPLY\n');
      return;
    }

    const recoveryReason = rateLimitRecovery
      ? 'recovery_after_429_rate_limit'
      : 'recovery_after_gateway_restart';

    const invokePayload = { reason: recoveryReason };
    if (modelOverride) invokePayload.modelOverride = modelOverride;

    let invokeResult = null;
    if (!runtime.dryRun) {
      try {
        invokeResult = await apiFetch(
          auth,
          'POST',
          `/api/agents/${auth.agentId}/heartbeat/invoke`,
          invokePayload,
          runtime.runId || null,
        );
        if (runtime.verbose) {
          console.log(
            `paperclip-run-recovery: heartbeat invoke queued invokeRun=${invokeResult?.id || 'unknown'}` +
            (modelOverride ? ` modelOverride=${modelOverride}` : ''),
          );
        }

        if (rateLimitRecovery && modelOverride) {
          logModelRotation(modelRotationLogPath, {
            timestamp: new Date(nowMs).toISOString(),
            paperclipAgentId: auth.agentId,
            openclawAgentId: identity.openclawAgentId,
            failedModel: rateLimitAnalysis.failedModel,
            fallbackModel: modelOverride,
            sessionId: rateLimitAnalysis.sessionId,
            invokeRunId: invokeResult?.id || null,
            errorMessage: rateLimitAnalysis.errorMessage.slice(0, 300),
          });
        }
      } catch (err) {
        console.error(`paperclip-run-recovery: heartbeat invoke failed: ${err.message}`);
        return;
      }
    } else {
      console.log(
        `paperclip-run-recovery: DRY RUN would invoke heartbeat for agent=${auth.agentId}` +
        ` reason=${recoveryReason}` +
        (modelOverride ? ` modelOverride=${modelOverride}` : ''),
      );
      if (recentFailures.length > 0) {
        console.log(`paperclip-run-recovery: would mark ${recentFailures.length} failed run(s) as processed`);
      }
    }

    const newProcessedIds = [
      ...processedIds,
      ...recentFailures.map((run) => run.id),
    ].slice(-MAX_PROCESSED_IDS);

    const newState = {
      ...state,
      lastCheckedAt: nowMs,
      lastInvokeAt: runtime.dryRun ? (state.lastInvokeAt || null) : nowMs,
      lastInvokeRunId: runtime.dryRun
        ? (state.lastInvokeRunId || null)
        : (invokeResult?.id || null),
      recoveryCount: (Number.isFinite(state.recoveryCount) ? state.recoveryCount : 0) +
        (runtime.dryRun ? 0 : 1),
      processedRunIds: newProcessedIds,
      lastRecoveredFailures: recentFailures.map((run) => ({
        id: run.id,
        errorCode: run.errorCode,
        finishedAt: run.finishedAt,
        taskId: run.contextSnapshot?.taskId || null,
      })),
    };

    if (rateLimitRecovery) {
      newState.lastRateLimitSessionId = rateLimitAnalysis.sessionId;
      newState.lastRateLimitRecovery = {
        timestamp: new Date(nowMs).toISOString(),
        paperclipAgentId: auth.agentId,
        openclawAgentId: identity.openclawAgentId,
        failedModel: rateLimitAnalysis.failedModel,
        fallbackModel: modelOverride,
        sessionId: rateLimitAnalysis.sessionId,
      };
      newState.rateLimitRecoveryCount =
        (Number.isFinite(state.rateLimitRecoveryCount) ? state.rateLimitRecoveryCount : 0) +
        (runtime.dryRun ? 0 : 1);
    }

    saveState(statePath, newState);

    if (!runtime.dryRun && !runtime.verbose) {
      process.stdout.write('NO_REPLY\n');
    }
  } finally {
    releaseLock(lockPath, lock.fd);
  }
}

main().catch((err) => {
  console.error(`paperclip-run-recovery: fatal: ${err.message}`);
  process.exitCode = 1;
});
