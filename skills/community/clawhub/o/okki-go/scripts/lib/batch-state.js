#!/usr/bin/env node
'use strict';

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const {
  batchIdFromPath,
  DEFAULT_BATCH_DIR,
  nowIso
} = require('./compact-output');
const {
  readJsonFile,
  writeJsonFile
} = require('./okki-api');

const DEFAULT_TTL_HOURS = 24;
const HANDLE_BYTES = 12;

function defaultBatchStatePath() {
  return process.env.OKKIGO_BATCH_STATE_FILE ||
    path.join(DEFAULT_BATCH_DIR, 'latest-batch.json');
}

function defaultSelectionDir() {
  return process.env.OKKIGO_SELECTION_DIR ||
    path.join(DEFAULT_BATCH_DIR, 'selections');
}

function defaultUnlockPlanDir() {
  return process.env.OKKIGO_UNLOCK_PLAN_DIR ||
    path.join(DEFAULT_BATCH_DIR, 'unlock-plans');
}

function defaultActiveUnlockPlanDir() {
  return process.env.OKKIGO_ACTIVE_UNLOCK_PLAN_DIR ||
    path.join(DEFAULT_BATCH_DIR, 'active-unlock-plans');
}

function parseNow(value) {
  const date = value ? new Date(value) : new Date();
  if (Number.isNaN(date.getTime())) {
    throw new Error(`Invalid --now value: ${value}`);
  }
  return date;
}

function ttlMs(ttlHours) {
  const hours = Number(ttlHours || process.env.OKKIGO_BATCH_TTL_HOURS || DEFAULT_TTL_HOURS);
  if (!Number.isFinite(hours) || hours <= 0) {
    throw new Error('Batch TTL must be a positive number of hours.');
  }
  return hours * 60 * 60 * 1000;
}

function opaqueId(prefix) {
  return `${prefix}_${crypto.randomBytes(HANDLE_BYTES).toString('hex')}`;
}

function assertOpaqueId(value, prefix, label) {
  const pattern = new RegExp(`^${prefix}_[a-f0-9]{${HANDLE_BYTES * 2}}$`);
  if (!pattern.test(String(value || ''))) {
    throw new Error(`${label} is invalid.`);
  }
}

function scopeKeyFromSource(source = {}) {
  if (source.kind === 'target_set') {
    return 'target-set-company_unlock';
  }

  const selectionHandle = source.selection_handle || source.selectionHandle || null;
  if (selectionHandle) {
    assertOpaqueId(selectionHandle, 'sel', 'Selection handle');
    return `selection-${selectionHandle}-company_unlock`;
  }

  const batchPath = source.batch_path || source.batchPath || '';
  const batchId = cleanScopePart(source.batch_id || batchIdFromPath(batchPath));
  if (!batchId) {
    throw new Error('Unlock plan is invalid: missing source scope.');
  }
  const batchKey = batchPath ? crypto.createHash('sha256').update(batchPath).digest('hex').slice(0, 16) : batchId;
  return `batch-${batchId}-${batchKey}-company_unlock`;
}

function cleanScopePart(value) {
  return String(value || '').replace(/[^a-zA-Z0-9_-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 120);
}

function assertFresh(createdAtValue, options = {}) {
  const now = options.now ? parseNow(options.now) : new Date();
  const createdAt = parseNow(createdAtValue || '');
  if (now.getTime() - createdAt.getTime() > ttlMs(options.ttlHours)) {
    throw new Error(`${options.label || 'Saved state'} expired; re-run the previous step.`);
  }
}

function writeLatestBatchPointer(options) {
  if (!options || !options.batchPath) {
    throw new Error('writeLatestBatchPointer requires batchPath.');
  }
  const statePath = options.statePath || defaultBatchStatePath();
  const now = options.now ? parseNow(options.now) : new Date();
  const pointer = {
    latest_batch: options.batchPath,
    displayed_rows: Number.isFinite(Number(options.displayedRows)) ? Number(options.displayedRows) : 0,
    request_summary: options.requestSummary || '',
    created_at: now.toISOString()
  };
  if (options.discoveryHealth && typeof options.discoveryHealth === 'object') {
    pointer.discovery_health = options.discoveryHealth;
  }
  writeJsonFile(statePath, pointer);
  return statePath;
}

function writeSelectionHandle(options) {
  if (!options || !options.batchPath) {
    throw new Error('writeSelectionHandle requires batchPath.');
  }
  const handle = options.handle || opaqueId('sel');
  assertOpaqueId(handle, 'sel', 'Selection handle');
  const dir = options.dir || defaultSelectionDir();
  const now = options.now ? parseNow(options.now) : new Date();
  const selection = {
    version: '1.0',
    kind: 'company_selection',
    selection_handle: handle,
    batch_path: options.batchPath,
    batch_id: batchIdFromPath(options.batchPath),
    displayed_rows: Number.isFinite(Number(options.displayedRows)) ? Number(options.displayedRows) : 0,
    request_summary: options.requestSummary || '',
    created_at: now.toISOString()
  };
  if (options.discoveryHealth && typeof options.discoveryHealth === 'object') {
    selection.discovery_health = options.discoveryHealth;
  }
  const selectionPath = path.join(dir, `${handle}.json`);
  writeJsonFile(selectionPath, selection);
  return { handle, selectionPath, selection };
}

function resolveSelectionHandle(handle, options = {}) {
  assertOpaqueId(handle, 'sel', 'Selection handle');
  const selectionPath = path.join(options.dir || defaultSelectionDir(), `${handle}.json`);
  if (!fs.existsSync(selectionPath)) {
    throw new Error('Selection handle is unavailable; re-run a free lookup before using row selections.');
  }
  const selection = readJsonFile(selectionPath);
  if (!selection || selection.kind !== 'company_selection') {
    throw new Error('Selection handle is invalid.');
  }
  if (selection.selection_handle !== handle) {
    throw new Error('Selection handle does not match the saved selection.');
  }
  assertFresh(selection.created_at, {
    now: options.now,
    ttlHours: options.ttlHours,
    label: 'Selection handle'
  });
  if (!selection.batch_path || typeof selection.batch_path !== 'string') {
    throw new Error('Selection handle is invalid: missing batch_path.');
  }
  if (!fs.existsSync(selection.batch_path)) {
    throw new Error('Selection batch file is unavailable; re-run a free lookup before using row selections.');
  }
  return {
    batchPath: selection.batch_path,
    selection,
    selectionPath
  };
}

function writeUnlockPlan(options) {
  if (!options || !Array.isArray(options.rows) || options.rows.length === 0) {
    throw new Error('writeUnlockPlan requires rows.');
  }
  const planId = options.planId || opaqueId('uplan');
  assertOpaqueId(planId, 'uplan', 'Unlock plan');
  const dir = options.dir || defaultUnlockPlanDir();
  const now = options.now ? parseNow(options.now) : new Date();
  const source = options.source || {
    selection_handle: options.selectionHandle || null,
    batch_path: options.batchPath || null,
    batch_id: batchIdFromPath(options.batchPath),
    request_summary: options.requestSummary || ''
  };
  const plan = {
    version: '1.0',
    kind: 'unlock_plan',
    action: 'company_unlock',
    unlock_plan_id: planId,
    created_at: now.toISOString(),
    source,
    max_credit_cost: options.rows.length,
    rows: options.rows
  };
  if (options.targetSetFingerprint) {
    plan.target_set_fingerprint = options.targetSetFingerprint;
  }
  const planPath = path.join(dir, `${planId}.json`);
  writeJsonFile(planPath, plan);
  writeActiveUnlockPlan(plan, { dir: options.activeDir, now: options.now });
  return { planId, planPath, plan };
}

function resolveUnlockPlan(planId, options = {}) {
  assertOpaqueId(planId, 'uplan', 'Unlock plan');
  const planPath = path.join(options.dir || defaultUnlockPlanDir(), `${planId}.json`);
  if (!fs.existsSync(planPath)) {
    throw new Error('Unlock plan is unavailable; prepare the selected rows again before unlocking.');
  }
  const plan = readJsonFile(planPath);
  if (!plan || plan.kind !== 'unlock_plan' || plan.action !== 'company_unlock') {
    throw new Error('Unlock plan is invalid.');
  }
  if (plan.unlock_plan_id !== planId) {
    throw new Error('Unlock plan does not match the requested plan id.');
  }
  assertFresh(plan.created_at, {
    now: options.now,
    ttlHours: options.ttlHours,
    label: 'Unlock plan'
  });
  if (!Array.isArray(plan.rows) || plan.rows.length === 0) {
    throw new Error('Unlock plan is invalid: missing rows.');
  }
  const active = validateActiveUnlockPlan(plan, options);
  return { plan, planPath, active };
}

function writeActiveUnlockPlan(plan, options = {}) {
  const scopeKey = scopeKeyFromSource(plan.source || {});
  const active = {
    version: '1.0',
    kind: 'active_unlock_plan',
    action: 'company_unlock',
    scope_key: scopeKey,
    unlock_plan_id: plan.unlock_plan_id,
    target_set_fingerprint: plan.target_set_fingerprint || null,
    updated_at: (options.now ? parseNow(options.now) : new Date()).toISOString()
  };
  const activePath = path.join(options.dir || defaultActiveUnlockPlanDir(), `${scopeKey}.json`);
  writeJsonFile(activePath, active);
  return { activePath, active };
}

function validateActiveUnlockPlan(plan, options = {}) {
  const scopeKey = scopeKeyFromSource(plan.source || {});
  const activePath = path.join(options.activeDir || defaultActiveUnlockPlanDir(), `${scopeKey}.json`);
  if (!fs.existsSync(activePath)) {
    throw new Error('Unlock plan is stale; prepare the selected rows again before unlocking.');
  }
  const active = readJsonFile(activePath);
  if (!active || active.kind !== 'active_unlock_plan' || active.action !== 'company_unlock') {
    throw new Error('Unlock plan active state is invalid; prepare the selected rows again before unlocking.');
  }
  if (active.scope_key !== scopeKey) {
    throw new Error('Unlock plan active state does not match the requested plan.');
  }
  assertFresh(active.updated_at, {
    now: options.now,
    ttlHours: options.ttlHours,
    label: 'Active unlock plan'
  });
  if (active.unlock_plan_id !== plan.unlock_plan_id) {
    const reason = plan.source && plan.source.kind === 'target_set'
      ? 'target set changed'
      : 'selection changed';
    throw new Error(`Unlock plan was superseded because the ${reason}; prepare the current selection again before unlocking.`);
  }
  if (plan.source && plan.source.kind === 'target_set') {
    if (!plan.target_set_fingerprint || active.target_set_fingerprint !== plan.target_set_fingerprint) {
      throw new Error('Unlock plan target set fingerprint changed; prepare the current target set again before unlocking.');
    }
  }
  return { activePath, active };
}

function readLatestBatchPointer(options = {}) {
  const statePath = options.statePath || defaultBatchStatePath();
  if (!fs.existsSync(statePath)) return null;
  try {
    return readJsonFile(statePath);
  } catch (error) {
    if (options.ignoreErrors) return null;
    throw error;
  }
}

function resolveBatchPath(batchArg, options = {}) {
  if (batchArg !== 'latest') {
    return {
      batchPath: batchArg,
      latestBatchUsed: false,
      pointer: null,
      statePath: null
    };
  }

  const statePath = options.statePath || defaultBatchStatePath();
  if (!fs.existsSync(statePath)) {
    throw new Error(`Latest batch pointer is unavailable: ${statePath}`);
  }

  const pointer = readJsonFile(statePath);
  const batchPath = pointer.latest_batch;
  if (!batchPath || typeof batchPath !== 'string') {
    throw new Error('Latest batch pointer is invalid: missing latest_batch.');
  }
  if (!fs.existsSync(batchPath)) {
    throw new Error(`Latest batch file is unavailable: ${batchPath}`);
  }

  const now = options.now ? parseNow(options.now) : new Date();
  const createdAt = parseNow(pointer.created_at || pointer.createdAt || '');
  if (now.getTime() - createdAt.getTime() > ttlMs(options.ttlHours)) {
    throw new Error('Latest batch pointer expired; re-run a free lookup before using row selections.');
  }

  return {
    batchPath,
    latestBatchUsed: true,
    pointer,
    statePath
  };
}

module.exports = {
  DEFAULT_TTL_HOURS,
  defaultActiveUnlockPlanDir,
  defaultBatchStatePath,
  defaultSelectionDir,
  defaultUnlockPlanDir,
  nowIso,
  parseNow,
  readLatestBatchPointer,
  resolveSelectionHandle,
  resolveUnlockPlan,
  resolveBatchPath,
  writeSelectionHandle,
  writeUnlockPlan,
  writeActiveUnlockPlan,
  writeLatestBatchPointer
};
