#!/usr/bin/env node
/**
 * model-rotation.js
 *
 * Tracks fix attempts per PR and suggests model rotation after repeated failures.
 *
 * Usage:
 *   node model-rotation.js check --pr <pr-number> --repo <repo>
 *   node model-rotation.js record --pr <pr-number> --repo <repo> --model <model>
 *   node model-rotation.js reset --pr <pr-number> --repo <repo>
 *
 * Config:
 *   Reads model rotation settings from skill config.json → modelRotation
 *
 * State default:
 *   ~/.openclaw/model-rotation-state.json
 */

'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { getConfig } = require('./lib/config');

const HOME = process.env.HOME || os.homedir();
const DEFAULT_STATE_PATH = path.join(HOME, '.openclaw', 'model-rotation-state.json');
const DEFAULT_MODEL_ROTATION = [
  'openai-codex/gpt-5.3-codex',
  'anthropic/claude-opus-4-6',
  'anthropic/claude-sonnet-4-6',
  'xai/grok-3',
];
const DEFAULT_THINKING_ESCALATION = ['default', 'high', 'xhigh'];
const DEFAULT_ATTEMPTS_PER_ROTATION = 3;

function expandHome(targetPath) {
  if (typeof targetPath !== 'string') return targetPath;
  if (targetPath === '~') return HOME;
  if (targetPath.startsWith('~/') || targetPath.startsWith('~\\')) {
    return path.join(HOME, targetPath.slice(2));
  }
  return targetPath;
}

function normalizeStringArray(value, fallback) {
  if (!Array.isArray(value)) return [...fallback];
  const normalized = value
    .map((entry) => (typeof entry === 'string' ? entry.trim() : ''))
    .filter(Boolean);
  return normalized.length > 0 ? normalized : [...fallback];
}

function resolveModelRotationConfig(config = getConfig()) {
  const raw = (config && typeof config.modelRotation === 'object' && config.modelRotation) || {};

  const statePath =
    typeof raw.statePath === 'string' && raw.statePath.trim()
      ? expandHome(raw.statePath.trim())
      : DEFAULT_STATE_PATH;

  return {
    statePath,
    rotationOrder: normalizeStringArray(raw.rotationOrder, DEFAULT_MODEL_ROTATION),
    thinkingLevels: normalizeStringArray(raw.thinkingLevels, DEFAULT_THINKING_ESCALATION),
    attemptsPerRotation:
      Number.isInteger(raw.attemptsPerRotation) && raw.attemptsPerRotation > 0
        ? raw.attemptsPerRotation
        : DEFAULT_ATTEMPTS_PER_ROTATION,
  };
}

function loadState(statePath = resolveModelRotationConfig().statePath) {
  try {
    if (fs.existsSync(statePath)) {
      return JSON.parse(fs.readFileSync(statePath, 'utf8'));
    }
  } catch {}
  return { prs: {} };
}

function saveState(state, statePath = resolveModelRotationConfig().statePath) {
  const dir = path.dirname(statePath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(statePath, JSON.stringify(state, null, 2));
}

function prKey(repo, pr) {
  return `${repo}#${pr}`;
}

function getDefaultPrState() {
  return { attempts: 0, models: [], lastModel: null };
}

function computeCheckResult(prState, key, rotationConfig = resolveModelRotationConfig()) {
  const { rotationOrder, thinkingLevels, attemptsPerRotation } = rotationConfig;
  const currentModel = rotationOrder.includes(prState.lastModel) ? prState.lastModel : rotationOrder[0];
  const shouldRotate = prState.attempts >= attemptsPerRotation;
  const currentModelIndex = rotationOrder.indexOf(currentModel);
  const nextModelIndex = (currentModelIndex + 1) % rotationOrder.length;
  const suggestedModel = shouldRotate ? rotationOrder[nextModelIndex] : currentModel;
  const thinkingIndex = Math.min(
    Math.floor(prState.attempts / attemptsPerRotation),
    thinkingLevels.length - 1,
  );

  return {
    pr: key,
    attempts: prState.attempts,
    shouldRotate,
    suggestedModel,
    suggestedThinking: thinkingLevels[thinkingIndex],
    previousModels: prState.models,
  };
}

function check(repo, pr, options = {}) {
  const rotationConfig = options.rotationConfig || resolveModelRotationConfig(options.config);
  const state = loadState(options.statePath || rotationConfig.statePath);
  const key = prKey(repo, pr);
  const prState = state.prs[key] || getDefaultPrState();
  const result = computeCheckResult(prState, key, rotationConfig);

  console.log(JSON.stringify(result, null, 2));
  return result;
}

function record(repo, pr, model, options = {}) {
  const rotationConfig = options.rotationConfig || resolveModelRotationConfig(options.config);
  const statePath = options.statePath || rotationConfig.statePath;
  const state = loadState(statePath);
  const key = prKey(repo, pr);

  if (!state.prs[key]) {
    state.prs[key] = getDefaultPrState();
  }

  state.prs[key].attempts += 1;
  state.prs[key].lastModel = model;
  if (!state.prs[key].models.includes(model)) {
    state.prs[key].models.push(model);
  }
  state.prs[key].lastAttempt = new Date().toISOString();

  saveState(state, statePath);

  const result = { recorded: true, ...state.prs[key] };
  console.log(JSON.stringify(result, null, 2));
  return result;
}

function reset(repo, pr, options = {}) {
  const rotationConfig = options.rotationConfig || resolveModelRotationConfig(options.config);
  const statePath = options.statePath || rotationConfig.statePath;
  const state = loadState(statePath);
  const key = prKey(repo, pr);
  delete state.prs[key];
  saveState(state, statePath);

  const result = { reset: true, pr: key };
  console.log(JSON.stringify(result, null, 2));
  return result;
}

function parseFlags(args) {
  const flags = {};
  for (let i = 1; i < args.length; i += 2) {
    if (args[i] && args[i].startsWith('--')) {
      flags[args[i].slice(2)] = args[i + 1];
    }
  }
  return flags;
}

function main(argv = process.argv.slice(2)) {
  const action = argv[0];
  const flags = parseFlags(argv);

  switch (action) {
    case 'check':
      check(flags.repo, flags.pr);
      break;
    case 'record':
      record(flags.repo, flags.pr, flags.model);
      break;
    case 'reset':
      reset(flags.repo, flags.pr);
      break;
    default:
      console.error('Usage: model-rotation.js <check|record|reset> --pr <num> --repo <repo> [--model <model>]');
      process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  DEFAULT_ATTEMPTS_PER_ROTATION,
  DEFAULT_MODEL_ROTATION,
  DEFAULT_STATE_PATH,
  DEFAULT_THINKING_ESCALATION,
  check,
  computeCheckResult,
  expandHome,
  getDefaultPrState,
  loadState,
  main,
  parseFlags,
  prKey,
  record,
  reset,
  resolveModelRotationConfig,
  saveState,
};
