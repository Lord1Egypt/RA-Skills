#!/usr/bin/env node
/**
 * spawn-with-fallback.js (configurable edition)
 *
 * Wrapper for OpenClaw sessions_spawn with automatic provider fallback.
 * If the primary model fails due to credits/quota/auth, retries with the
 * equivalent fallback model from the other provider.
 *
 * Configuration is loaded from (in priority order):
 *   1. Explicit `config` object passed to spawnWithFallback()
 *   2. config.json in this module's directory (skill directory)
 *   3. Built-in defaults (matches original hardcoded behavior)
 *
 * Usage (as CLI):
 *   node spawn-with-fallback.js --model sonnet --task "do something" [--mode run]
 *   node spawn-with-fallback.js --model sonnet --task @/path/to/task.txt --dry-run
 *   node spawn-with-fallback.js --config /path/to/config.json --model opus --task "..."
 *
 * Usage (as module):
 *   const { spawnWithFallback, loadConfig } = require('./spawn-with-fallback')
 *   const config = loadConfig('/optional/path/to/config.json')
 *   const result = await spawnWithFallback({ model: 'sonnet', task: '...', config })
 */

'use strict';

const { execFile } = require('child_process');
const fs = require('fs');
const path = require('path');

// ---------------------------------------------------------------------------
// Built-in defaults (match original hardcoded behavior)
// ---------------------------------------------------------------------------

const DEFAULT_ALIASES = {
  haiku: 'anthropic/claude-haiku-4-5',
  sonnet: 'anthropic/claude-sonnet-4-6',
  sonnet45: 'anthropic/claude-sonnet-4-20250514',
  opus: 'anthropic/claude-opus-4-6',
  opus46: 'anthropic/claude-opus-4-6',
  opus45: 'anthropic/claude-opus-4-5',
  flash: 'openrouter/google/gemini-2.0-flash-001',
  'flash-lite': 'openrouter/google/gemini-2.0-flash-lite-001',
  codex: 'openai-codex/gpt-5.3-codex',
};

const DEFAULT_FALLBACKS = {
  'openai-codex/gpt-5.3-codex': 'anthropic/claude-sonnet-4-6',
  'openai-codex/gpt-5.2': 'anthropic/claude-sonnet-4-6',
  'anthropic/claude-sonnet-4-6': 'openai-codex/gpt-5.3-codex',
  'anthropic/claude-sonnet-4-20250514': 'openai-codex/gpt-5.3-codex',
  'anthropic/claude-opus-4-6': 'openai-codex/gpt-5.3-codex',
  'anthropic/claude-opus-4-5': 'openai-codex/gpt-5.3-codex',
  'anthropic/claude-haiku-4-5': 'openrouter/google/gemini-2.0-flash-lite-001',
  'openrouter/google/gemini-2.0-flash-lite-001': 'anthropic/claude-haiku-4-5',
  'openrouter/google/gemini-2.0-flash-001': 'anthropic/claude-sonnet-4-6',
};

const DEFAULT_FAILURE_PATTERN_STRINGS = [
  'credits',
  'quota',
  '402',
  'insufficient_quota',
  'billing',
  'rate[\\s_-]?limit',
  'no credits',
  'payment required',
  'provider error',
  'credits_exhausted',
  'quota_exceeded',
];

const DEFAULT_FAILURE_STOP_REASONS = ['error', 'credits_exhausted', 'quota_exceeded'];

// ---------------------------------------------------------------------------
// Config loading
// ---------------------------------------------------------------------------

/**
 * Load configuration from a JSON file path, or from the skill directory's
 * config.json, or fall back to built-in defaults.
 *
 * @param {string} [configPath] - Optional explicit path to a config.json
 * @returns {object} Resolved config with aliases, fallbacks, failurePatterns, failureStopReasons
 */
function loadConfig(configPath) {
  let raw = null;

  // 1. Explicit path
  if (configPath) {
    if (!fs.existsSync(configPath)) {
      throw new Error(`Config file not found: ${configPath}`);
    }
    raw = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  }

  // 2. Skill-directory config.json
  if (!raw) {
    const skillDirConfig = path.join(__dirname, '..', 'config.json');
    if (fs.existsSync(skillDirConfig)) {
      raw = JSON.parse(fs.readFileSync(skillDirConfig, 'utf8'));
    }
  }

  // 3. Build resolved config (config values override defaults per-key)
  const aliases = {};
  const fallbacks = {};

  // Start with defaults
  Object.assign(aliases, DEFAULT_ALIASES);
  Object.assign(fallbacks, DEFAULT_FALLBACKS);

  // Overlay config values (strip $doc keys)
  if (raw && raw.aliases) {
    for (const [k, v] of Object.entries(raw.aliases)) {
      if (k.startsWith('$')) continue;
      aliases[k] = v;
    }
  }
  if (raw && raw.fallbacks) {
    for (const [k, v] of Object.entries(raw.fallbacks)) {
      if (k.startsWith('$')) continue;
      fallbacks[k] = v;
    }
  }

  // Failure patterns: if config provides them, use config's list; otherwise defaults
  const patternStrings =
    raw && raw.failurePatterns && Array.isArray(raw.failurePatterns.patterns)
      ? raw.failurePatterns.patterns
      : DEFAULT_FAILURE_PATTERN_STRINGS;

  // Validate regex patterns to prevent ReDoS attacks
  const MAX_PATTERN_LENGTH = 256;
  const MAX_PATTERNS = 50;
  const validatedPatterns = patternStrings
    .slice(0, MAX_PATTERNS)
    .filter((s) => typeof s === 'string' && s.length > 0 && s.length <= MAX_PATTERN_LENGTH);

  const failurePatterns = validatedPatterns.map((s) => {
    try {
      return new RegExp(s, 'i');
    } catch (e) {
      console.error(`[spawn-with-fallback] Invalid regex pattern skipped: ${s}`);
      return null;
    }
  }).filter(Boolean);

  const stopReasons =
    raw && raw.failureStopReasons && Array.isArray(raw.failureStopReasons.reasons)
      ? raw.failureStopReasons.reasons
      : DEFAULT_FAILURE_STOP_REASONS;

  const failureStopReasons = new Set(stopReasons);

  return { aliases, fallbacks, failurePatterns, failureStopReasons };
}

// ---------------------------------------------------------------------------
// Alias resolution
// ---------------------------------------------------------------------------

/**
 * Validates model input to prevent injection via malicious model names.
 * Model names must follow a strict pattern: alphanumeric, hyphens, underscores, slashes, dots.
 */
function validateModelInput(modelInput) {
  if (typeof modelInput !== 'string') {
    throw new Error('Model must be a string');
  }
  const trimmed = modelInput.trim();
  if (trimmed.length === 0) {
    throw new Error('--model is required');
  }
  if (trimmed.length > 256) {
    throw new Error('Model name exceeds maximum length of 256 characters');
  }
  // Allow only provider/model-safe characters, including version suffixes like :free.
  if (!/^[a-zA-Z0-9/_.:-]+$/.test(trimmed)) {
    throw new Error('Model name contains invalid characters. Allowed: alphanumeric, /, _, ., :, -');
  }

  const segments = trimmed.split('/');
  if (segments.some((segment) => segment.length === 0 || segment === '.' || segment === '..')) {
    throw new Error('Model name contains invalid path traversal segments');
  }

  return trimmed;
}

function resolveModel(modelInput, aliases) {
  const validated = validateModelInput(modelInput);
  const lower = validated.toLowerCase();
  return aliases[lower] || validated;
}

// ---------------------------------------------------------------------------
// Failure detection
// ---------------------------------------------------------------------------

function detectFailure(exitCode, output, failurePatterns, failureStopReasons) {
  if (exitCode !== 0) {
    const combined = (output || '').toLowerCase();

    for (const pattern of failurePatterns) {
      if (pattern.test(combined)) {
        const reason = extractReason(combined);
        return { failed: true, reason };
      }
    }

    return { failed: true, reason: 'spawn_error' };
  }

  const combined = (output || '').toLowerCase();
  for (const pattern of failurePatterns) {
    if (pattern.test(combined)) {
      const reason = extractReason(combined);
      return { failed: true, reason };
    }
  }

  try {
    const jsonMatch = output && output.match(/\{[\s\S]*"stop_reason"\s*:\s*"([^"]+)"/);
    if (jsonMatch) {
      const stopReason = jsonMatch[1];
      if (failureStopReasons.has(stopReason)) {
        return { failed: true, reason: stopReason };
      }
    }
  } catch (_) {
    // ignore
  }

  return { failed: false, reason: null };
}

function extractReason(output) {
  if (/credits_exhausted/i.test(output)) return 'credits_exhausted';
  if (/quota_exceeded/i.test(output)) return 'quota_exceeded';
  if (/402/.test(output) || /payment required/i.test(output)) return 'payment_required';
  if (/billing/i.test(output)) return 'billing_error';
  if (/rate[\s_-]?limit/i.test(output)) return 'rate_limit';
  if (/quota/i.test(output) || /insufficient_quota/i.test(output)) return 'quota_exceeded';
  if (/credits/i.test(output) || /no credits/i.test(output)) return 'credits_exhausted';
  if (/provider error/i.test(output)) return 'provider_error';
  return 'spawn_error';
}

// ---------------------------------------------------------------------------
// Task resolution (@file support)
// ---------------------------------------------------------------------------

/**
 * Validates that a file path doesn't traverse outside allowed directories.
 * Prevents path traversal attacks via ../../../etc/passwd style inputs.
 */
function validateFilePath(filePath) {
  if (typeof filePath !== 'string' || filePath.length === 0) {
    throw new Error('File path must be a non-empty string');
  }

  // Resolve to absolute path to detect traversal.
  const resolvedPath = path.resolve(filePath);

  // Block explicit path traversal attempts.
  if (filePath.includes('..')) {
    throw new Error('Path traversal (../) is not allowed in file paths');
  }

  // Resolve symlinks when the file exists so temp symlinks cannot tunnel into
  // blocked system paths like /etc/passwd.
  const canonicalPath = fs.existsSync(resolvedPath)
    ? fs.realpathSync(resolvedPath)
    : resolvedPath;

  // Allowlist for temp directories (must check before blocklist).
  const ALLOWED_PREFIXES = [
    '/var/folders/',  // macOS temp dir
    '/tmp/',          // Unix temp dir
    require('os').tmpdir() + '/',  // System temp dir (cross-platform)
  ];

  const isAllowedTemp = ALLOWED_PREFIXES.some((prefix) =>
    canonicalPath.startsWith(prefix) || canonicalPath === prefix.slice(0, -1)
  );

  if (!isAllowedTemp) {
    // Block access to sensitive system paths.
    const BLOCKED_PREFIXES = ['/etc/', '/var/', '/usr/', '/root/', '/private/etc/'];
    const lowerCanonical = canonicalPath.toLowerCase();
    for (const prefix of BLOCKED_PREFIXES) {
      if (lowerCanonical.startsWith(prefix)) {
        throw new Error(`Access to system path ${prefix} is not allowed`);
      }
    }
  }

  if (fs.existsSync(canonicalPath)) {
    const stats = fs.statSync(canonicalPath);
    if (!stats.isFile()) {
      throw new Error('Task path must point to a regular file');
    }
  }

  return canonicalPath;
}

function resolveTask(taskInput) {
  if (!taskInput) throw new Error('--task is required');
  if (typeof taskInput !== 'string') throw new Error('--task must be a string');

  // Limit task size to prevent DoS via huge tasks
  const MAX_TASK_SIZE = 1024 * 1024; // 1MB max
  if (taskInput.length > MAX_TASK_SIZE) {
    throw new Error(`Task input exceeds maximum size of ${MAX_TASK_SIZE} bytes`);
  }

  if (taskInput.startsWith('@')) {
    const rawPath = taskInput.slice(1);
    const filePath = validateFilePath(rawPath);

    if (!fs.existsSync(filePath)) {
      throw new Error(`Task file not found: ${filePath}`);
    }

    const stats = fs.statSync(filePath);
    if (stats.size > MAX_TASK_SIZE) {
      throw new Error(`Task file exceeds maximum size of ${MAX_TASK_SIZE} bytes`);
    }

    return fs.readFileSync(filePath, 'utf8').trim();
  }
  return taskInput;
}

// ---------------------------------------------------------------------------
// Spawn execution
// ---------------------------------------------------------------------------

/**
 * Validates spawn arguments to prevent injection attacks.
 * Mode and label are strictly validated before being passed to execFile.
 */
function validateSpawnArgs(mode, label) {
  const ALLOWED_MODES = ['run', 'session', null, undefined, ''];
  if (mode && !ALLOWED_MODES.includes(mode)) {
    throw new Error(`Invalid mode: ${mode}. Allowed: run, session`);
  }

  if (label) {
    if (typeof label !== 'string') {
      throw new Error('Label must be a string');
    }
    if (label.length > 256) {
      throw new Error('Label exceeds maximum length of 256 characters');
    }
    // Allow only safe characters in labels
    if (!/^[a-zA-Z0-9 _.-]+$/.test(label)) {
      throw new Error('Label contains invalid characters. Allowed: alphanumeric, space, _, ., -');
    }
  }
}

function runSpawn(model, task, mode, label) {
  return new Promise((resolve) => {
    // Validate mode and label before use
    validateSpawnArgs(mode, label);

    // Note: model and task are validated by resolveModel and resolveTask respectively
    // execFile is used (not exec) which prevents shell injection
    const args = ['session', 'spawn', '--model', model, '--task', task];
    if (mode) args.push('--mode', mode);
    if (label) args.push('--label', label);

    execFile('openclaw', args, { maxBuffer: 10 * 1024 * 1024 }, (err, out, errOut) => {
      const stdout = out || '';
      const stderr = errOut || '';
      const exitCode = err ? (err.code || 1) : 0;
      resolve({ exitCode, stdout, stderr, combined: stdout + '\n' + stderr });
    });
  });
}

// ---------------------------------------------------------------------------
// Core function (module export)
// ---------------------------------------------------------------------------

async function spawnWithFallback({ model, task, mode = 'run', label, dryRun = false, config }) {
  // Resolve config
  const cfg = config || loadConfig();

  const modelRequested = model;
  const resolvedModel = resolveModel(model, cfg.aliases);
  const resolvedTask = resolveTask(task);
  const fallbackModel = cfg.fallbacks[resolvedModel] || null;

  console.error(`[spawn-with-fallback] Model requested: ${modelRequested}`);
  console.error(`[spawn-with-fallback] Resolved to:     ${resolvedModel}`);
  if (fallbackModel) {
    console.error(`[spawn-with-fallback] Fallback ready:  ${fallbackModel}`);
  } else {
    console.error(`[spawn-with-fallback] No fallback configured for ${resolvedModel}`);
  }

  // ── Dry-run mode ──
  if (dryRun) {
    const dryResult = {
      success: true,
      dry_run: true,
      model_requested: modelRequested,
      model_resolved: resolvedModel,
      model_used: resolvedModel,
      fallback_available: fallbackModel || null,
      fallback_triggered: false,
      fallback_reason: null,
      mode: mode || 'run',
      label: label || null,
      task_preview: resolvedTask.slice(0, 120) + (resolvedTask.length > 120 ? '...' : ''),
      result: '[dry-run: no spawn executed]',
    };
    console.log(JSON.stringify(dryResult, null, 2));
    return dryResult;
  }

  // ── Primary attempt ──
  console.error(`[spawn-with-fallback] Attempting primary model: ${resolvedModel}`);
  const primary = await runSpawn(resolvedModel, resolvedTask, mode, label);
  const primaryFailure = detectFailure(
    primary.exitCode, primary.combined,
    cfg.failurePatterns, cfg.failureStopReasons,
  );

  if (!primaryFailure.failed) {
    const result = {
      success: true,
      model_requested: modelRequested,
      model_used: resolvedModel,
      fallback_triggered: false,
      fallback_reason: null,
      result: primary.stdout.trim(),
    };
    console.error(`[spawn-with-fallback] ✅ Primary succeeded with ${resolvedModel}`);
    return result;
  }

  console.error(`[spawn-with-fallback] ⚠️  Primary failed (${primaryFailure.reason}): ${resolvedModel}`);

  // ── Fallback attempt ──
  if (!fallbackModel) {
    const result = {
      success: false,
      model_requested: modelRequested,
      model_used: resolvedModel,
      fallback_triggered: false,
      fallback_reason: primaryFailure.reason,
      error: `Primary model failed and no fallback is configured for ${resolvedModel}`,
      result: primary.combined.trim(),
    };
    console.error(`[spawn-with-fallback] ❌ No fallback available. Giving up.`);
    return result;
  }

  console.error(`[spawn-with-fallback] 🔄 Retrying with fallback: ${fallbackModel}`);
  const fallback = await runSpawn(fallbackModel, resolvedTask, mode, label);
  const fallbackFailure = detectFailure(
    fallback.exitCode, fallback.combined,
    cfg.failurePatterns, cfg.failureStopReasons,
  );

  if (!fallbackFailure.failed) {
    const result = {
      success: true,
      model_requested: modelRequested,
      model_used: fallbackModel,
      fallback_triggered: true,
      fallback_reason: primaryFailure.reason,
      result: fallback.stdout.trim(),
    };
    console.error(`[spawn-with-fallback] ✅ Fallback succeeded with ${fallbackModel}`);
    return result;
  }

  // Both failed
  const result = {
    success: false,
    model_requested: modelRequested,
    model_used: fallbackModel,
    fallback_triggered: true,
    fallback_reason: primaryFailure.reason,
    error: `Both primary (${resolvedModel}) and fallback (${fallbackModel}) failed`,
    primary_error: primaryFailure.reason,
    fallback_error: fallbackFailure.reason,
    result: fallback.combined.trim(),
  };
  console.error(`[spawn-with-fallback] ❌ Both primary and fallback failed. Giving up.`);
  return result;
}

// ---------------------------------------------------------------------------
// CLI entry point
// ---------------------------------------------------------------------------

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--dry-run') {
      args.dryRun = true;
    } else if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) {
        args[key] = next;
        i++;
      } else {
        args[key] = true;
      }
    }
  }
  return args;
}

async function main() {
  const cliArgs = parseArgs(process.argv.slice(2));

  if (cliArgs.help || cliArgs.h) {
    console.log(`
Usage: node spawn-with-fallback.js [options]

Options:
  --model    <alias|full>   Model alias or full model string (required)
  --task     <text|@file>   Task description or @path/to/file.txt (required)
  --mode     run|session    Spawn mode (default: run)
  --label    <string>       Optional label for the spawned session
  --config   <path>         Path to config.json (optional; uses skill dir or defaults)
  --dry-run                 Print what would happen without spawning
  --help                    Show this help

Configuration:
  Copy config.example.json to config.json in the skill directory.
  Customize aliases, fallbacks, and failure patterns.
  Without config.json, built-in defaults are used.
`);
    process.exit(0);
  }

  if (!cliArgs.model) {
    console.error('Error: --model is required');
    process.exit(1);
  }
  if (!cliArgs.task) {
    console.error('Error: --task is required');
    process.exit(1);
  }

  // Load config (CLI --config flag or auto-detect)
  const config = loadConfig(cliArgs.config);

  let result;
  try {
    result = await spawnWithFallback({
      model: cliArgs.model,
      task: cliArgs.task,
      mode: cliArgs.mode || 'run',
      label: cliArgs.label,
      dryRun: !!cliArgs.dryRun,
      config,
    });
  } catch (err) {
    console.error(`[spawn-with-fallback] Fatal error: ${err.message}`);
    process.exit(1);
  }

  if (result.success) {
    console.error(`\n[spawn-with-fallback] Result: SUCCESS`);
    console.error(`  Model used:        ${result.model_used}`);
    if (result.fallback_triggered) {
      console.error(`  Fallback:          triggered (reason: ${result.fallback_reason})`);
    }
  } else {
    console.error(`\n[spawn-with-fallback] Result: FAILED`);
    console.error(`  Error: ${result.error}`);
    process.exitCode = 1;
  }

  if (!result.dry_run) {
    console.log(JSON.stringify(result, null, 2));
  }
}

// Run as CLI or export as module
if (require.main === module) {
  main().catch((err) => {
    console.error(err);
    process.exit(1);
  });
} else {
  module.exports = {
    spawnWithFallback,
    resolveModel,
    loadConfig,
    detectFailure,
    extractReason,
    validateFilePath,
    validateModelInput,
    validateSpawnArgs,
    DEFAULT_ALIASES,
    DEFAULT_FALLBACKS,
    DEFAULT_FAILURE_PATTERN_STRINGS,
    DEFAULT_FAILURE_STOP_REASONS,
  };
}
