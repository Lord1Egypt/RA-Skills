#!/usr/bin/env node
'use strict';

const crypto = require('crypto');
const { spawnSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');
const {
  getJson,
  readJsonFile,
  postJsonWithMeta,
  writeJsonFile
} = require('./lib/okki-api');
const {
  batchIdFromPath,
  cleanString,
  compactList,
  countryCode,
  countryName,
  DEFAULT_BATCH_DIR,
  defaultRawPath,
  nowIso,
  outputBudgetMetadata,
  applyDebugMetadata,
  selectedRows,
  truncateText
} = require('./lib/compact-output');
const { resolveBatchPath } = require('./lib/batch-state');
const { resolveUnlockPlan } = require('./lib/batch-state');

const VIEWED_STATE_WARNING = '公司已解锁，但本地已查看记录未更新。解锁结果仍然有效；不要因此重新解锁。下次使用 --mark-unlocked 前，可预先授权 OKKI Go viewed 状态目录写入权限以保存本地记录。';

function usage() {
  console.error([
    'Usage:',
    '  node scripts/unlock-companies.js --plan PLAN_ID --compact [--locale en-US] [--mark-unlocked] [--artifact-dir DIR] [--raw-file PATH] [--markdown-file PATH] [--audit-file PATH] [--debug-metadata]',
    '  node scripts/unlock-companies.js --batch batch.json --rows ROWS --compact [--locale en-US] [--mark-unlocked] [--artifact-dir DIR] [--raw-file PATH] [--markdown-file PATH] [--audit-file PATH] [--debug-metadata]',
    '  node scripts/unlock-companies.js --batch latest --rows ROWS --compact [--locale en-US] [--mark-unlocked] [--artifact-dir DIR] [--raw-file PATH] [--markdown-file PATH] [--audit-file PATH] [--debug-metadata]',
    '  node scripts/unlock-companies.js --batch batch.json --rows ROWS --detail [--locale en-US] [--artifact-dir DIR] [--raw-file PATH] [--markdown-file PATH] [--audit-file PATH] [--debug-metadata]'
  ].join('\n'));
}

function parseArgs(argv) {
  const args = {
    plan: null,
    batch: null,
    rows: null,
    compact: false,
    detail: false,
    rawFile: null,
    markdownFile: null,
    artifactDir: null,
    auditFile: null,
    markUnlocked: false,
    now: null,
    locale: null,
    debugMetadata: false
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--plan') {
      args.plan = argv[++i];
    } else if (arg === '--batch') {
      args.batch = argv[++i];
    } else if (arg === '--rows') {
      args.rows = argv[++i];
    } else if (arg === '--compact') {
      args.compact = true;
    } else if (arg === '--detail') {
      args.detail = true;
    } else if (arg === '--raw-file') {
      args.rawFile = argv[++i];
    } else if (arg === '--markdown-file') {
      args.markdownFile = argv[++i];
    } else if (arg === '--artifact-dir') {
      args.artifactDir = argv[++i];
    } else if (arg === '--audit-file') {
      args.auditFile = argv[++i];
    } else if (arg === '--mark-unlocked') {
      args.markUnlocked = true;
    } else if (arg === '--now') {
      args.now = argv[++i];
    } else if (arg === '--locale') {
      args.locale = argv[++i];
    } else if (arg === '--debug-metadata') {
      args.debugMetadata = true;
    } else if (arg === '--help' || arg === '-h') {
      usage();
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  if (args.plan) {
    if (args.batch || args.rows) throw new Error('--plan cannot be combined with --batch or --rows');
    return args;
  }
  if (!args.batch) throw new Error('Missing --batch');
  if (!args.rows) throw new Error('Missing --rows');
  return args;
}

function validateBatchRows(rows) {
  if (rows.length > 50) {
    throw new Error('Selected rows exceed compact unlock hard cap 50. Split the unlock into smaller confirmed batches.');
  }
  for (const row of rows) {
    if (!row.domain) throw new Error(`Selected row ${row.row} is missing domain.`);
    if (!countryCode(row)) throw new Error(`Selected row ${row.row} is missing country_code.`);
  }
}

function validateLatestBatchPointer(resolvedBatch, batch) {
  if (!resolvedBatch.latestBatchUsed) return;
  const pointerSummary = cleanString(resolvedBatch.pointer && resolvedBatch.pointer.request_summary);
  const batchSummary = cleanString(batch && batch.request_summary);
  if (pointerSummary && batchSummary && pointerSummary !== batchSummary) {
    throw new Error('Latest batch request summary does not match the batch file; re-run a free lookup before using row selections.');
  }
}

async function unlockOne(row, context = {}) {
  const payload = {
    domain: row.domain,
    countryCode: countryCode(row)
  };
  const auditBase = unlockAuditBase(row, context, payload);
  writeUnlockAudit(context.auditFile, {
    ...auditBase,
    event: 'unlock_request'
  });

  let unlock;
  try {
    const response = await postJsonWithMeta('/api/v1/companies/unlock', payload);
    unlock = response.body;
    writeUnlockAudit(context.auditFile, {
      ...auditBase,
      event: 'unlock_success',
      http_status: response.statusCode,
      unlock_hash_present: Boolean(unlock && (unlock.companyHashId || unlock.company_hash_id)),
      charged_if_known: unlock && Object.prototype.hasOwnProperty.call(unlock, 'charged') ? Boolean(unlock.charged) : null
    });
  } catch (error) {
    writeUnlockAudit(context.auditFile, {
      ...auditBase,
      event: 'unlock_failure',
      http_status: error.statusCode || null,
      okki_error_message: error.message || null,
      okki_error_body_summary: summarizeAuditBody(error.body),
      exception_name: error.name || null,
      exception_message: error.message || null
    });
    if (context.auditFile && !error.auditPath) error.auditPath = context.auditFile;
    throw error;
  }
  const hash = unlock.companyHashId || unlock.company_hash_id;
  let profile = null;
  let profileEmails = null;
  if (hash) {
    const encoded = encodeURIComponent(hash);
    [profile, profileEmails] = await Promise.all([
      getJson(`/api/v1/companies/${encoded}/profile`).catch((error) => ({ error: error.message })),
      getJson(`/api/v1/companies/${encoded}/profileEmails`).catch((error) => ({ error: error.message }))
    ]);
  }
  return { row, unlock, profile, profileEmails };
}

function failedUnlockItem(row, error) {
  return {
    row,
    unlock: {
      charged: false,
      error: error.message || String(error),
      statusCode: error.statusCode || null
    },
    profile: null,
    profileEmails: null
  };
}

function stoppedUnlockItem(row, error) {
  return {
    row,
    unlock: {
      charged: false,
      skipped: true,
      error: error && error.message ? `Not executed after prior failure: ${error.message}` : 'Not executed after prior failure',
      statusCode: null
    },
    profile: null,
    profileEmails: null
  };
}

function isRowLevelUnlockFailure(error) {
  return error && (error.statusCode === 404 || error.statusCode === 422);
}

function isStoppedItem(item) {
  return Boolean(item && item.unlock && item.unlock.skipped);
}

function isFailedItem(item) {
  return Boolean(item && item.unlock && item.unlock.error && !isStoppedItem(item));
}

function isSuccessfulItem(item) {
  return Boolean(item && item.unlock && !item.unlock.error && !isStoppedItem(item) && (item.unlock.companyHashId || item.unlock.company_hash_id));
}

function unlockAuditBase(row, context, payload) {
  const source = context.source || {};
  const active = context.activePlan && context.activePlan.active ? context.activePlan.active : {};
  return {
    audit_id: context.auditId,
    timestamp: nowIso(),
    event: null,
    plan_id: context.planId || null,
    selection_handle: source.selection_handle || source.selectionHandle || null,
    batch_path: source.batch_path || source.batchPath || context.batchPath || null,
    row: row.row,
    company_name: row.company_name || null,
    domain: row.domain || null,
    countryCode: payload.countryCode || null,
    request_index: context.requestIndex,
    request_payload_fingerprint: auditFingerprint(payload),
    active_plan_scope: active.scope_key || null,
    active_plan_id_at_execution: active.unlock_plan_id || null
  };
}

function writeUnlockAudit(filePath, event) {
  if (!filePath) return;
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.appendFileSync(filePath, `${JSON.stringify(event)}\n`, { mode: 0o600 });
  try {
    fs.chmodSync(filePath, 0o600);
  } catch (_) {
    // Best effort on platforms that do not support POSIX modes.
  }
}

function auditFingerprint(value) {
  return crypto
    .createHash('sha256')
    .update(JSON.stringify(value))
    .digest('hex')
    .slice(0, 16);
}

function summarizeAuditBody(body) {
  if (body === null || body === undefined) return null;
  if (typeof body === 'string') return truncateAuditText(body);
  if (typeof body !== 'object') return truncateAuditText(String(body));
  const summary = {};
  for (const key of ['detail', 'title', 'message', 'error', 'code']) {
    if (Object.prototype.hasOwnProperty.call(body, key)) {
      summary[key] = truncateAuditText(body[key]);
    }
  }
  return Object.keys(summary).length > 0 ? summary : { type: Array.isArray(body) ? 'array' : 'object' };
}

function truncateAuditText(value) {
  const text = cleanString(value);
  if (text.length <= 500) return text;
  return `${text.slice(0, 500)}...`;
}

function emailsFrom(profileEmails) {
  if (!profileEmails || typeof profileEmails !== 'object') return [];
  const rows = Array.isArray(profileEmails.emails) ? profileEmails.emails : [];
  const emails = [];
  const seen = new Set();
  for (const row of rows) {
    collectEmailValues(row, emails, seen);
  }
  return emails;
}

function collectEmailValues(value, emails, seen) {
  if (Array.isArray(value)) {
    for (const item of value) collectEmailValues(item, emails, seen);
    return;
  }
  if (typeof value === 'string') {
    addEmail(value, emails, seen);
    return;
  }
  if (!value || typeof value !== 'object') return;
  addEmail(value.email, emails, seen);
  addEmail(value.value, emails, seen);
  collectEmailValues(value.emails, emails, seen);
}

function addEmail(value, emails, seen) {
  const email = cleanString(value).toLowerCase();
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || seen.has(email)) return;
  seen.add(email);
  emails.push(email);
}

function phonesFrom(profileEmails) {
  if (!profileEmails || typeof profileEmails !== 'object') return [];
  const rows = Array.isArray(profileEmails.emails) ? profileEmails.emails : [];
  const phones = [];
  const seen = new Set();
  for (const row of rows) {
    collectPhoneValues(row.phone, phones, seen);
    collectPhoneValues(row.phone_number, phones, seen);
    collectPhoneValues(row.phone_numbers, phones, seen);
  }
  return phones;
}

function collectPhoneValues(value, phones, seen) {
  if (Array.isArray(value)) {
    for (const item of value) collectPhoneValues(item, phones, seen);
    return;
  }
  const phone = cleanString(value);
  if (!phone || seen.has(phone)) return;
  seen.add(phone);
  phones.push(phone);
}

function emailTotal(profileEmails) {
  if (!profileEmails || typeof profileEmails !== 'object') return 0;
  if (Number.isFinite(Number(profileEmails.total))) return Number(profileEmails.total);
  return emailsFrom(profileEmails).length;
}

function profileDescription(profile) {
  if (!profile || typeof profile !== 'object') return '';
  return cleanString(profile.description || profile.company_profile || profile.profile || '');
}

function companyDetails(item, mode, options = {}) {
  const profile = item.profile && !item.profile.error ? item.profile : null;
  const profileEmails = item.profileEmails && !item.profileEmails.error ? item.profileEmails : null;
  const raw = item.row.raw && typeof item.row.raw === 'object' ? item.row.raw : {};
  const code = countryCode(item.row);
  const emails = emailsFrom(profileEmails);
  const phones = phonesFrom(profileEmails);
  const contacts = contactRows(profileEmails).slice(0, mode === 'detail' ? 20 : 5);
  const displayWebsite = cleanString(profile && (profile.website || profile.domain)) || cleanString(item.row.domain);
  const result = {
    row: item.row.row,
    company_name: cleanString(profile && (profile.name || profile.company_name)) ||
      item.row.company_name ||
      item.unlock.companyName ||
      'Unknown company',
    country_code: code || null,
    country_name: countryName(code, options.locale) || null,
    status: isStoppedItem(item) ? 'not_executed' : item.unlock.companyHashId ? 'unlocked' : 'failed',
    charged: Boolean(item.unlock.charged),
    display_website: displayWebsite || null,
    founded_year: firstVisible(raw.founding_time, raw.foundingTime, profile && (profile.founded_year || profile.founding_year), profile && profile.foundedYear),
    employees: firstVisible(profile && (profile.employee_desc || profile.employeeCount || profile.employee_count), raw.employees_count, raw.employeeCount, raw.employeesCount, raw.employee_range),
    company_type: compactList(firstVisible(raw.company_type, raw.companyType, profile && (profile.company_type || profile.industry), raw.industry), 2),
    main_products: visibleList(firstVisible(raw.main_products, raw.mainProducts, raw.products), 8),
    has_email: emailTotal(profileEmails) > 0 || emails.length > 0,
    has_whatsapp: positiveCount(firstVisible(raw.whatsapp_count, raw.whatsappCount, profile && (profile.whatsapp_count || profile.whatsappCount))),
    email_preview: emails.slice(0, mode === 'detail' ? 20 : 3),
    phone_preview: phones.slice(0, mode === 'detail' ? 10 : 3),
    social_links: visibleList(profile && profile.social_links, mode === 'detail' ? 20 : 5),
    description: truncateText(profileDescription(profile), mode === 'detail' ? 1200 : 360),
    contacts,
    profile_available: Boolean(profile),
    emails_total: emailTotal(profileEmails)
  };
  return result;
}

function firstVisible(...values) {
  for (const value of values) {
    if (value === 0) return value;
    if (Array.isArray(value) && value.length > 0) return value;
    if (value !== null && value !== undefined && String(value).trim() !== '') return value;
  }
  return null;
}

function positiveCount(value) {
  if (value === null || value === undefined || value === '') return false;
  const number = Number(value);
  return Number.isFinite(number) ? number > 0 : false;
}

function visibleList(value, maxItems) {
  if (Array.isArray(value)) {
    return value.map(cleanString).filter(Boolean).slice(0, maxItems);
  }
  const text = cleanString(value);
  return text ? [text].slice(0, maxItems) : [];
}

function contactRows(profileEmails) {
  if (!profileEmails || typeof profileEmails !== 'object' || !Array.isArray(profileEmails.emails)) return [];
  return profileEmails.emails.map((row) => ({
    name: cleanString(row.name || [row.first_name, row.last_name].filter(Boolean).join(' ')) || null,
    position: cleanString(row.position || row.title) || null,
    email: emailsFrom({ emails: [row] })[0] || null,
    phone: phonesFrom({ emails: [row] })[0] || null,
    linkedin: cleanString(row.linkedin) || null
  }));
}

function rawRows(results) {
  return results.map((item) => ({
    row: item.row.row,
    domain: item.row.domain,
    country_code: countryCode(item.row),
    company_name: item.row.company_name || null,
    unlock: item.unlock,
    profile: item.profile,
    profileEmails: item.profileEmails
  }));
}

function markUnlockedBatch(rows) {
  const stateScript = path.join(__dirname, 'okki-state.js');
  const payload = rows.map((row) => ({ domain: row.domain, country_code: countryCode(row) }));
  const result = spawnSync(process.execPath, [
    stateScript,
    'viewed',
    'mark-unlocked-batch',
    '--json',
    JSON.stringify(payload)
  ], {
    cwd: path.join(__dirname, '..', '..'),
    env: process.env,
    encoding: 'utf8'
  });
  if (result.status !== 0) {
    throw new Error(`mark-unlocked-batch failed: ${result.stderr || result.stdout}`);
  }
  return JSON.parse(result.stdout);
}

function tryMarkUnlockedBatch(rows) {
  try {
    return { state: markUnlockedBatch(rows) };
  } catch (error) {
    return { error: localStateErrorMessage(error) };
  }
}

function viewedStatePreflight() {
  const file = viewedStatePath();
  try {
    if (fs.existsSync(file)) {
      fs.accessSync(file, fs.constants.W_OK);
      return { ok: true };
    }

    const dir = path.dirname(file);
    if (fs.existsSync(dir)) {
      fs.accessSync(dir, fs.constants.W_OK);
      return { ok: true };
    }

    fs.accessSync(nearestExistingParent(dir), fs.constants.W_OK);
    return { ok: true };
  } catch (error) {
    return { ok: false, error: localStateErrorMessage(error) };
  }
}

function viewedStatePath() {
  const configHome = process.env.XDG_CONFIG_HOME || path.join(process.env.HOME || os.homedir(), '.config');
  return path.join(configHome, 'okki-go', 'viewed.json');
}

function nearestExistingParent(filePath) {
  let current = filePath;
  while (current && !fs.existsSync(current)) {
    const parent = path.dirname(current);
    if (parent === current) break;
    current = parent;
  }
  return current || path.dirname(filePath);
}

function localStateErrorMessage(error) {
  const text = String(error && (error.stderr || error.stdout || error.message || error) || '');
  const code = text.match(/\b(EPERM|EACCES|EROFS|ENOENT|ENOTDIR|EISDIR|EINVAL)\b/);
  if (code) return `local viewed state update failed (${code[1]}).`;
  if (/permission denied/i.test(text)) return 'local viewed state update failed (permission denied).';
  return 'local viewed state update failed.';
}

function outputFileStamp() {
  return new Date().toISOString()
    .replace(/[-:]/g, '')
    .replace(/\..*$/, '')
    .replace('T', '-');
}

function detailsFileName() {
  return `company-details-${outputFileStamp()}.md`;
}

function internalDetailsPath() {
  return path.join(process.env.OKKIGO_DETAILS_TEMP_DIR || DEFAULT_BATCH_DIR, detailsFileName());
}

function cwdArtifactDetailsPath() {
  return path.join(process.cwd(), 'okki-go-artifacts', detailsFileName());
}

function normalizePath(value) {
  const text = cleanString(value);
  return text ? path.resolve(text) : null;
}

function preflightWritableFile(filePath) {
  const resolved = normalizePath(filePath);
  if (!resolved) {
    return { ok: false, path: filePath, error: 'missing path' };
  }
  try {
    fs.mkdirSync(path.dirname(resolved), { recursive: true });
    if (fs.existsSync(resolved)) {
      const stat = fs.statSync(resolved);
      if (stat.isDirectory()) return { ok: false, path: resolved, error: 'path is a directory' };
    }
    const handle = fs.openSync(resolved, 'a');
    fs.closeSync(handle);
    return { ok: true, path: resolved };
  } catch (error) {
    return { ok: false, path: resolved, error: filesystemErrorMessage(error) };
  }
}

function filesystemErrorMessage(error) {
  const text = String(error && (error.code || error.message) || error || '');
  const code = text.match(/\b(EPERM|EACCES|EROFS|ENOENT|ENOTDIR|EISDIR|EINVAL)\b/);
  if (code) return code[1];
  return text || 'not writable';
}

function artifactFallbackWarning(candidate, fallbackPath) {
  const label = candidate.explicit
    ? '显式提供的详情文档 artifact/markdown 路径不可写'
    : '默认详情文档 artifact 路径不可写';
  return `${label}，已在扣费前回退到内部临时详情路径 ${fallbackPath}。原因: ${candidate.reason || 'not writable'}。`;
}

function detailsPrecheckFailure(candidates) {
  return {
    error_code: 'DETAILS_MARKDOWN_PRECHECK_FAILED',
    paid_api_called: false,
    unlock_executed: false,
    next_action: 'authorize_artifact_dir',
    recovery_suggestion: '本次未解锁、未扣费。失败原因是详情文档没有任何可写位置。请授权 Agent 使用一个可写文件夹，或改用一个已可写目录后重试。',
    attempted_details_paths: candidates.map((candidate) => ({
      path: candidate.path,
      kind: candidate.kind,
      reason: candidate.reason || null
    }))
  };
}

function resolveDetailsMarkdownTarget(args) {
  const candidates = [];
  if (args.markdownFile) {
    candidates.push({
      kind: 'markdown_file',
      path: args.markdownFile,
      artifact: true,
      explicit: true,
      artifactDir: path.dirname(normalizePath(args.markdownFile) || args.markdownFile)
    });
  } else if (args.artifactDir) {
    const dir = normalizePath(args.artifactDir);
    candidates.push({
      kind: 'artifact_dir',
      path: dir ? path.join(dir, detailsFileName()) : null,
      artifact: true,
      explicit: true,
      artifactDir: dir
    });
  } else if (process.env.OKKIGO_ARTIFACT_DIR) {
    const dir = normalizePath(process.env.OKKIGO_ARTIFACT_DIR);
    candidates.push({
      kind: 'env_artifact_dir',
      path: dir ? path.join(dir, detailsFileName()) : null,
      artifact: true,
      explicit: true,
      artifactDir: dir
    });
  } else {
    const defaultArtifactPath = cwdArtifactDetailsPath();
    candidates.push({
      kind: 'cwd_artifact_dir',
      path: defaultArtifactPath,
      artifact: true,
      explicit: false,
      artifactDir: path.dirname(defaultArtifactPath)
    });
  }

  const internalPath = internalDetailsPath();
  candidates.push({
    kind: 'internal_temp',
    path: internalPath,
    artifact: false,
    explicit: false,
    artifactDir: null
  });

  const warnings = [];
  const attempted = [];
  for (const candidate of candidates) {
    const preflight = preflightWritableFile(candidate.path);
    const checked = {
      ...candidate,
      path: preflight.path || candidate.path,
      reason: preflight.ok ? null : preflight.error
    };
    attempted.push(checked);
    if (preflight.ok) {
      if (candidate.kind === 'internal_temp' && attempted.length > 1) {
        warnings.push(artifactFallbackWarning(attempted[attempted.length - 2], checked.path));
      }
      return {
        ok: true,
        path: checked.path,
        artifact: candidate.artifact,
        artifactDir: candidate.artifact ? candidate.artifactDir : null,
        accessNote: candidate.artifact
          ? '详情文档已写入 Agent 提供或默认的用户交付物目录。'
          : '详情文档已写入内部临时路径；该路径可能不方便直接打开。',
        warnings,
        attempted
      };
    }
  }

  return {
    ok: false,
    errorOutput: detailsPrecheckFailure(attempted)
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const resolved = resolveUnlockRows(args);
  const selected = resolved.selected;
  validateBatchRows(selected);
  const rawPath = args.rawFile || defaultRawPath('unlock-companies');
  const auditPath = args.auditFile || defaultRawPath('unlock-audit').replace(/\.json$/i, '.jsonl');
  const detailsTarget = resolveDetailsMarkdownTarget(args);
  if (!detailsTarget.ok) {
    process.stdout.write(`${JSON.stringify(detailsTarget.errorOutput, null, 2)}\n`);
    process.exitCode = 2;
    return;
  }
  const markdownPath = detailsTarget.path;
  const statePreflight = args.markUnlocked ? viewedStatePreflight() : null;
  const auditId = `unlock_audit_${crypto.randomBytes(12).toString('hex')}`;

  const results = [];
  for (let index = 0; index < selected.length; index += 1) {
    const context = {
      auditFile: auditPath,
      auditId,
      requestIndex: index + 1,
      planId: resolved.planId,
      source: resolved.source,
      batchPath: resolved.batchPath,
      activePlan: resolved.activePlan
    };
    try {
      results.push(await unlockOne(selected[index], context));
    } catch (error) {
      results.push(failedUnlockItem(selected[index], error));
      if (!isRowLevelUnlockFailure(error)) {
        for (let rest = index + 1; rest < selected.length; rest += 1) {
          results.push(stoppedUnlockItem(selected[rest], error));
        }
        break;
      }
    }
  }

  const balance = await getJson('/api/v1/credit/balance').catch(() => null);
  const raw = {
    version: '1.0',
    created_at: nowIso(),
    batch_id: batchIdFromPath(resolved.batchPath),
    rows: rawRows(results),
    balance
  };
  writeJsonFile(rawPath, raw);
  const mode = args.detail ? 'detail' : 'compact';
  const successfulResults = results.filter(isSuccessfulItem);
  const stateUpdate = args.markUnlocked ? tryMarkUnlockedBatch(successfulResults.map((item) => item.row)) : null;
  const details = successfulResults.map((item) => companyDetails(item, mode, { locale: args.locale }));
  const fileDetails = mode === 'detail'
    ? details
    : successfulResults.map((item) => companyDetails(item, 'detail', { locale: args.locale }));
  const chargedCount = results.filter((item) => item.unlock && item.unlock.charged).length;
  const failureDetails = results.filter((item) => isFailedItem(item) || isStoppedItem(item)).map((item) => failureDetail(item));
  const successCount = successfulResults.length;
  const failedCount = results.filter(isFailedItem).length;
  const stoppedCount = results.filter(isStoppedItem).length;
  const runStatus = stoppedCount > 0
    ? 'stopped'
    : failedCount > 0
      ? 'completed_with_failures'
      : 'completed';
  writeMarkdownFile(markdownPath, {
    createdAt: raw.created_at,
    chargedCount,
    balance,
    details: fileDetails,
    failureDetails,
    plannedCount: selected.length,
    successCount,
    failedCount,
    stoppedCount
  });
  const visibleDetails = details.slice(0, 5);
  const unlockDetailsMarkdown = renderUnlockChatMarkdown({
    chargedCount,
    balance,
    details: visibleDetails,
    failureDetails,
    plannedCount: selected.length,
    successCount,
    failedCount,
    stoppedCount,
    detailsMarkdownPath: markdownPath
  });
  const warnings = [...detailsTarget.warnings];
  if (stateUpdate && stateUpdate.error) {
    warnings.push(VIEWED_STATE_WARNING);
    if (statePreflight && !statePreflight.ok) {
      warnings.push('Local viewed state was not writable before unlock; callers in restricted sandboxes can request file_system write permission for the OKKI Go viewed state directory before the next --mark-unlocked run.');
    }
  }
  const output = {
    batch_id: batchIdFromPath(resolved.batchPath),
    latest_batch_used: resolved.latestBatchUsed,
    unlock_plan_used: Boolean(resolved.unlockPlanUsed),
    run_status: runStatus,
    planned_count: selected.length,
    success_count: successCount,
    failed_count: failedCount,
    charged_count: chargedCount,
    balance,
    unlock_details_markdown: unlockDetailsMarkdown,
    company_details: visibleDetails,
    total_details_count: details.length,
    displayed_details_count: visibleDetails.length,
    next_action: successCount > 0 ? 'draft_outreach' : undefined,
    details_markdown_saved: true,
    details_markdown_path: markdownPath,
    details_markdown_artifact: detailsTarget.artifact,
    artifact_dir: detailsTarget.artifactDir,
    artifact_access_note: detailsTarget.accessNote,
    raw_saved: true,
    raw_path: rawPath,
    audit_saved: true,
    audit_path: auditPath,
    ...outputBudgetMetadata({
      defaultCap: mode === 'detail' ? 50 : 50,
      hardCap: 50,
      requestedLimit: selected.length,
      returned: visibleDetails.length,
      available: selected.length
    })
  };
  if (stateUpdate && stateUpdate.state) output.state_updated = stateUpdate.state.updated;
  if (stateUpdate && stateUpdate.error) {
    output.state_update_failed = true;
    output.state_update_error = stateUpdate.error;
  }
  if (warnings.length > 0) output.warnings = warnings;
  if (!output.next_action) delete output.next_action;
  if (stoppedCount > 0) output.stopped_count = stoppedCount;

  process.stdout.write(`${JSON.stringify(unlockNormalOutput(output, args.debugMetadata), null, 2)}\n`);
}

function failureDetail(item) {
  return {
    row: item.row.row,
    company_name: item.row.company_name || 'Unknown company',
    country_code: countryCode(item.row) || null,
    status: isStoppedItem(item) ? 'not_executed' : 'failed',
    reason: cleanString(item.unlock && item.unlock.error) || '-',
    charged: Boolean(item.unlock && item.unlock.charged)
  };
}

function resolveUnlockRows(args) {
  if (args.plan) {
    const resolvedPlan = resolveUnlockPlan(args.plan, { now: args.now });
    return {
      batchPath: resolvedPlan.plan.source && resolvedPlan.plan.source.batch_path,
      latestBatchUsed: false,
      unlockPlanUsed: true,
      planId: resolvedPlan.plan.unlock_plan_id,
      source: resolvedPlan.plan.source || {},
      activePlan: resolvedPlan.active,
      selected: resolvedPlan.plan.rows
    };
  }
  const resolvedBatch = resolveBatchPath(args.batch, { now: args.now });
  const batch = readJsonFile(resolvedBatch.batchPath);
  validateLatestBatchPointer(resolvedBatch, batch);
  const rows = Array.isArray(batch.rows) ? batch.rows : [];
  return {
    batchPath: resolvedBatch.batchPath,
    latestBatchUsed: resolvedBatch.latestBatchUsed,
    unlockPlanUsed: false,
    planId: null,
    source: {
      batch_path: resolvedBatch.batchPath,
      batch_id: batchIdFromPath(resolvedBatch.batchPath)
    },
    activePlan: null,
    selected: selectedRows(rows, args.rows)
  };
}

function writeMarkdownFile(filePath, context) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, renderUnlockDetailsMarkdown(context), 'utf8');
}

function renderUnlockChatMarkdown(context) {
  const lines = [
    '# OKKI Go 解锁结果',
    '',
    `计划解锁: ${context.plannedCount} 家`,
    `成功: ${context.successCount} 家`,
    `失败: ${context.failedCount} 家`,
    `本次扣费: ${context.chargedCount}`
  ];
  if (context.stoppedCount > 0) lines.push(`未执行: ${context.stoppedCount} 家`);
  const balanceText = balanceSummary(context.balance);
  lines.push(`剩余积分: ${balanceText || '-'}`);
  lines.push('');
  lines.push(`> 聊天中最多展示 5 家；全部详情见: ${context.detailsMarkdownPath}`);
  lines.push('');

  context.details.forEach((detail, index) => {
    lines.push(`## ${index + 1}. ${detail.company_name}`);
    lines.push('');
    lines.push('| 字段 | 内容 |');
    lines.push('|---|---|');
    lines.push(`| 原序号 | ${mdCell(detail.row)} |`);
    lines.push(`| 公司名 | ${mdCell(detail.company_name)} |`);
    lines.push(`| 国家/地区 | ${mdCell(detail.country_name || detail.country_code)} |`);
    lines.push(`| 官网/域名 | ${mdCell(detail.display_website)} |`);
    lines.push(`| 公司类型 | ${mdCell(detail.company_type)} |`);
    lines.push(`| 成立时间 | ${mdCell(detail.founded_year)} |`);
    lines.push(`| 员工规模 | ${mdCell(detail.employees)} |`);
    lines.push(`| 主营产品 | ${mdCell(detail.main_products)} |`);
    lines.push(`| 邮箱 | ${mdCell(detail.email_preview)} |`);
    lines.push(`| 电话/WhatsApp | ${mdCell(detail.phone_preview)} |`);
    lines.push(`| 社交链接 | ${mdCell(detail.social_links)} |`);
    lines.push(`| 公司简介 | ${mdCell(truncateChatDescription(detail.description))} |`);
    lines.push('');
  });

  if (context.failureDetails && context.failureDetails.length > 0) {
    lines.push('| 原序号 | 公司名 | 状态 | 原因 | 是否扣费 |');
    lines.push('|---|---|---|---|---|');
    for (const detail of context.failureDetails) {
      lines.push(`| ${mdCell(detail.row)} | ${mdCell(detail.company_name)} | ${mdCell(displayFailureStatus(detail.status))} | ${mdCell(detail.reason)} | ${detail.charged ? '是' : '否'} |`);
    }
    lines.push('');
  }

  if (context.successCount > 0) {
    lines.push('下一步可以基于已解锁公司和已有联系人信息起草开发信草稿，先不发送。');
    lines.push('');
  }

  return `${lines.join('\n')}\n`;
}

function renderUnlockDetailsMarkdown(context) {
  const lines = [
    '# OKKI Go 公司详情',
    '',
    `生成时间: ${context.createdAt}`,
    `计划解锁: ${context.plannedCount || context.details.length}`,
    `成功: ${context.successCount || context.details.length}`,
    `失败: ${context.failedCount || 0}`,
    `本次扣费: ${context.chargedCount}`
  ];
  if (context.stoppedCount > 0) lines.push(`未执行: ${context.stoppedCount}`);
  const balanceText = balanceSummary(context.balance);
  if (balanceText) lines.push(`剩余积分: ${balanceText}`);
  lines.push('', '> 本文件包含本次解锁的全部公司详情。', '');

  context.details.forEach((detail, index) => {
    lines.push(`## ${index + 1}. ${detail.company_name}`);
    lines.push('');
    lines.push(`- 原序号: ${valueOrDash(detail.row)}`);
    lines.push(`- 国家/地区: ${valueOrDash(detail.country_name || detail.country_code)}`);
    lines.push(`- 官网/域名: ${valueOrDash(detail.display_website)}`);
    lines.push(`- 公司类型: ${valueOrDash(detail.company_type)}`);
    lines.push(`- 成立时间: ${valueOrDash(detail.founded_year)}`);
    lines.push(`- 员工规模: ${valueOrDash(detail.employees)}`);
    lines.push(`- 主营产品: ${valueOrDash(detail.main_products)}`);
    lines.push(`- 邮箱: ${valueOrDash(detail.email_preview)}`);
    lines.push(`- 电话/WhatsApp: ${valueOrDash(detail.phone_preview)}`);
    lines.push(`- 社交链接: ${valueOrDash(detail.social_links)}`);
    lines.push('');
    lines.push('### 公司简介');
    lines.push('');
    lines.push(valueOrDash(detail.description));
    lines.push('');
    lines.push('### 联系人/邮箱');
    lines.push('');
    lines.push('| 姓名 | 职位 | 邮箱 | 电话 | LinkedIn |');
    lines.push('|---|---|---|---|---|');
    if (detail.contacts.length === 0) {
      lines.push('| - | - | - | - | - |');
    } else {
      for (const contact of detail.contacts) {
        lines.push(`| ${mdCell(contact.name)} | ${mdCell(contact.position)} | ${mdCell(contact.email)} | ${mdCell(contact.phone)} | ${mdCell(contact.linkedin)} |`);
      }
    }
    lines.push('');
  });

  if (context.failureDetails && context.failureDetails.length > 0) {
    lines.push('| 原序号 | 公司名 | 状态 | 原因 | 是否扣费 |');
    lines.push('|---|---|---|---|---|');
    for (const detail of context.failureDetails) {
      lines.push(`| ${mdCell(detail.row)} | ${mdCell(detail.company_name)} | ${mdCell(displayFailureStatus(detail.status))} | ${mdCell(detail.reason)} | ${detail.charged ? '是' : '否'} |`);
    }
    lines.push('');
  }

  return `${lines.join('\n')}\n`;
}

function displayFailureStatus(status) {
  return status === 'not_executed' ? '未执行' : '失败';
}

function balanceSummary(balance) {
  if (!balance || typeof balance !== 'object') return '';
  const parts = [];
  if (Number.isFinite(Number(balance.monthlyPoints))) parts.push(`monthlyPoints ${balance.monthlyPoints}`);
  if (Number.isFinite(Number(balance.addonPoints))) parts.push(`addonPoints ${balance.addonPoints}`);
  return parts.join(', ');
}

function valueOrDash(value) {
  if (Array.isArray(value)) {
    const text = value.map(cleanString).filter(Boolean).join(', ');
    return text || '-';
  }
  const text = cleanString(value);
  return text || '-';
}

function mdCell(value) {
  return valueOrDash(value).replace(/\|/g, '\\|');
}

function truncateChatDescription(value) {
  const text = cleanString(value);
  if (text.length <= 200) return text;
  return `${text.slice(0, 200)}…`;
}

function unlockNormalOutput(output, debugMetadata) {
  return applyDebugMetadata(output, [
    'batch_id',
    'unlock_plan_used',
    'raw_path',
    'audit_path',
    'output_budget'
  ], debugMetadata);
}

main().catch((error) => {
  console.error(error.message);
  if (error.auditPath) {
    console.error(`Unlock audit saved: ${error.auditPath}`);
  }
  usage();
  process.exit(2);
});
