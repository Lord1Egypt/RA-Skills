#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CONFIG = path.resolve(process.env.HOME || '/home/zqh2333', '.openclaw/openclaw.json');
const POLICY_PATH = path.join(__dirname, '..', 'references', 'model-sync-policy.json');
const REPORT_DIR = path.resolve(__dirname, '..', '..', '..', 'reports', 'model-registry');
const PROVIDER_ARG = process.argv[2] || 'all';
const VERIFY_LIMIT = Number(process.argv[3] || 0); // 0 => all
const RESTART = process.argv.includes('--restart');
const DRY_RUN = process.argv.includes('--dry-run');

function catalogKey(providerKey, modelId) {
  return `${providerKey}/${modelId}`;
}

function loadPolicy() {
  try {
    const raw = JSON.parse(fs.readFileSync(POLICY_PATH, 'utf8'));
    return {
      allowlist: Array.isArray(raw.allowlist) ? new Set(raw.allowlist.map(String)) : null,
      denylist: new Set(Array.isArray(raw.denylist) ? raw.denylist.map(String) : []),
      notes: raw.notes || '',
    };
  } catch {
    return { allowlist: null, denylist: new Set(), notes: '' };
  }
}

function isAllowed(policy, modelId) {
  if (policy.denylist.has(modelId)) return false;
  if (policy.allowlist && policy.allowlist.size > 0) return policy.allowlist.has(modelId);
  return true;
}

async function fetchModels(provider) {
  const url = provider.baseUrl.replace(/\/$/, '') + '/models';
  const res = await fetch(url, { headers: { Authorization: `Bearer ${provider.apiKey}` } });
  if (!res.ok) throw new Error(`GET /models failed: ${res.status}`);
  const json = await res.json();
  return Array.isArray(json.data) ? json.data : [];
}

async function probeModel(provider, modelId) {
  const url = provider.baseUrl.replace(/\/$/, '') + '/chat/completions';
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'content-type': 'application/json', Authorization: `Bearer ${provider.apiKey}` },
    body: JSON.stringify({ model: modelId, messages: [{ role: 'user', content: 'ping' }], max_tokens: 1, temperature: 0 }),
  });
  return res.ok;
}

function normalizeModel(remote, previous = {}) {
  return {
    id: remote.id,
    name: remote.name || previous.name || remote.id,
    reasoning: typeof remote.reasoning === 'boolean' ? remote.reasoning : (typeof previous.reasoning === 'boolean' ? previous.reasoning : false),
    input: Array.isArray(remote.input) ? remote.input : (Array.isArray(previous.input) ? previous.input : ['text']),
    cost: remote.cost || previous.cost || { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
    contextWindow: remote.contextWindow || previous.contextWindow || 200000,
    maxTokens: remote.maxTokens || previous.maxTokens || 8192,
  };
}

function diffKeys(beforeKeys, afterKeys) {
  const before = new Set(beforeKeys);
  const after = new Set(afterKeys);
  return {
    added: afterKeys.filter(k => !before.has(k)),
    removed: beforeKeys.filter(k => !after.has(k)),
    kept: afterKeys.filter(k => before.has(k)),
  };
}

function writeReportFiles(report) {
  fs.mkdirSync(REPORT_DIR, { recursive: true });
  fs.writeFileSync(path.join(REPORT_DIR, 'sync-latest.json'), JSON.stringify(report, null, 2) + '\n', 'utf8');

  const lines = [];
  lines.push('# Model Registry Sync Report');
  lines.push('');
  lines.push(`- dryRun: ${report.dryRun}`);
  lines.push(`- changed: ${report.changed}`);
  lines.push(`- registeredModels: ${report.registeredModels}`);
  lines.push(`- providers: ${report.providers.length}`);
  lines.push(`- policy.allowlist: ${report.policy.allowlistSize}`);
  lines.push(`- policy.denylist: ${report.policy.denylistSize}`);
  if (report.policy.notes) lines.push(`- policy.notes: ${report.policy.notes}`);
  lines.push('');
  lines.push('## Diff');
  lines.push(`- added: ${report.diff.added.length}`);
  lines.push(`- removed: ${report.diff.removed.length}`);
  lines.push(`- kept: ${report.diff.kept.length}`);
  lines.push('');
  lines.push('## Provider stats');
  lines.push('| provider | fetched | unique | verified | denied | duplicates | unusable |');
  lines.push('| --- | ---: | ---: | ---: | ---: | ---: | ---: |');
  for (const p of report.providers) {
    lines.push(`| ${p.provider} | ${p.fetched} | ${p.unique} | ${p.verified} | ${p.denied} | ${p.duplicateRemoteIds.length} | ${p.unusable.length} |`);
  }
  lines.push('');
  lines.push('## Denied / unusable');
  for (const p of report.providers) {
    if (p.denied.length) lines.push(`- ${p.provider} denied: ${p.denied.join(', ')}`);
    if (p.unusable.length) lines.push(`- ${p.provider} unusable: ${p.unusable.join(', ')}`);
  }
  fs.writeFileSync(path.join(REPORT_DIR, 'sync-latest.md'), lines.join('\n') + '\n', 'utf8');
}

(async () => {
  const before = fs.readFileSync(CONFIG, 'utf8');
  const cfg = JSON.parse(before);
  const policy = loadPolicy();
  const providers = cfg.models?.providers || {};
  const providerKeys = PROVIDER_ARG === 'all' ? Object.keys(providers) : [PROVIDER_ARG];
  if (providerKeys.length === 0) throw new Error('No providers found');

  const previousCatalogKeys = Object.keys(cfg.agents?.defaults?.models || {});
  const allVerified = [];
  const providerReports = [];

  for (const providerKey of providerKeys) {
    const provider = providers[providerKey];
    if (!provider) throw new Error(`Provider not found: ${providerKey}`);
    const previousModels = new Map((provider.models || []).map(m => [m.id, m]));
    const remote = await fetchModels(provider);

    const dedup = new Map();
    const duplicateRemoteIds = [];
    const denied = [];
    for (const m of remote) {
      if (!m?.id) continue;
      if (!isAllowed(policy, m.id)) {
        denied.push(m.id);
        continue;
      }
      if (dedup.has(m.id)) {
        duplicateRemoteIds.push(m.id);
        continue;
      }
      dedup.set(m.id, m);
    }

    const verified = [];
    const unusable = [];
    const ordered = [...dedup.values()];
    const limit = VERIFY_LIMIT > 0 ? Math.min(VERIFY_LIMIT, ordered.length) : ordered.length;

    for (const model of ordered.slice(0, limit)) {
      const ok = await probeModel(provider, model.id).catch(() => false);
      if (!ok) {
        unusable.push(model.id);
        continue;
      }
      const normalized = normalizeModel(model, previousModels.get(model.id));
      verified.push(normalized);
      allVerified.push({ providerKey, ...normalized });
    }

    provider.models = verified;
    providerReports.push({
      provider: providerKey,
      fetched: remote.length,
      unique: dedup.size,
      verified: verified.length,
      denied,
      duplicateRemoteIds,
      unusable,
    });
  }

  cfg.agents = cfg.agents || {};
  cfg.agents.defaults = cfg.agents.defaults || {};
  cfg.agents.defaults.models = {};
  for (const m of allVerified) cfg.agents.defaults.models[catalogKey(m.providerKey, m.id)] = {};

  const afterCatalogKeys = Object.keys(cfg.agents.defaults.models);
  const diff = diffKeys(previousCatalogKeys, afterCatalogKeys);
  const next = JSON.stringify(cfg, null, 2) + '\n';
  const changed = next !== before;

  if (!DRY_RUN) {
    fs.writeFileSync(CONFIG, next, 'utf8');
    if (changed && RESTART) execSync('openclaw gateway restart', { stdio: 'inherit' });
  }

  const report = {
    dryRun: DRY_RUN,
    changed,
    configWritten: !DRY_RUN,
    providers: providerReports,
    policy: {
      allowlistSize: policy.allowlist ? policy.allowlist.size : 0,
      denylistSize: policy.denylist.size,
      notes: policy.notes,
    },
    diff,
    registeredModels: allVerified.length,
  };

  writeReportFiles(report);
  console.log(JSON.stringify(report, null, 2));
})().catch(err => {
  console.error(err.stack || err.message || String(err));
  process.exit(1);
});
