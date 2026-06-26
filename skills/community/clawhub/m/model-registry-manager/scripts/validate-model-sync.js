#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const CONFIG = path.resolve(process.env.HOME || '/home/zqh2333', '.openclaw/openclaw.json');
const POLICY_PATH = path.join(__dirname, '..', 'references', 'model-sync-policy.json');
const REPORT_DIR = path.resolve(__dirname, '..', '..', '..', 'reports', 'model-registry');
const PROVIDER_ARG = process.argv[2] || 'all';

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

function writeReportFiles(report) {
  fs.mkdirSync(REPORT_DIR, { recursive: true });
  fs.writeFileSync(path.join(REPORT_DIR, 'validate-latest.json'), JSON.stringify(report, null, 2) + '\n', 'utf8');

  const lines = [];
  lines.push('# Model Registry Validation Report');
  lines.push('');
  lines.push(`- fail: ${report.fail}`);
  lines.push(`- providers: ${report.providers.length}`);
  lines.push(`- registeredModels: ${report.registeredModels}`);
  lines.push(`- policy.allowlist: ${report.policy.allowlistSize}`);
  lines.push(`- policy.denylist: ${report.policy.denylistSize}`);
  if (report.policy.notes) lines.push(`- policy.notes: ${report.policy.notes}`);
  lines.push('');
  lines.push('## Provider stats');
  lines.push('| provider | fetched | unique | registered | usable | denied | duplicates |');
  lines.push('| --- | ---: | ---: | ---: | ---: | ---: | ---: |');
  for (const p of report.providers) {
    lines.push(`| ${p.provider} | ${p.fetched} | ${p.unique} | ${p.registered} | ${p.usable} | ${p.denied} | ${p.duplicates.length} |`);
  }
  lines.push('');
  lines.push('## Checks');
  for (const item of report.checks) lines.push(`- ${item.ok ? 'PASS' : 'FAIL'} ${item.message}`);
  fs.writeFileSync(path.join(REPORT_DIR, 'validate-latest.md'), lines.join('\n') + '\n', 'utf8');
}

(async () => {
  const cfg = JSON.parse(fs.readFileSync(CONFIG, 'utf8'));
  const policy = loadPolicy();
  const providers = cfg.models?.providers || {};
  const providerKeys = PROVIDER_ARG === 'all' ? Object.keys(providers) : [PROVIDER_ARG];
  if (providerKeys.length === 0) throw new Error('No providers found');

  const checks = [];
  const providerReports = [];
  const registered = [];
  let fail = 0;

  function check(ok, message) {
    checks.push({ ok, message });
    console.log(`${ok ? 'PASS' : 'FAIL'}\t${message}`);
    if (!ok) fail++;
  }

  for (const providerKey of providerKeys) {
    const provider = providers[providerKey];
    if (!provider) throw new Error(`Provider not found: ${providerKey}`);

    const remote = await fetchModels(provider);
    const remoteById = new Map();
    const duplicateRemoteIds = [];
    let allowedRemote = 0;
    for (const m of remote) {
      if (!m?.id) continue;
      if (!isAllowed(policy, m.id)) continue;
      allowedRemote++;
      if (remoteById.has(m.id)) {
        duplicateRemoteIds.push(m.id);
        continue;
      }
      remoteById.set(m.id, m);
    }

    const models = provider.models || [];
    const seen = new Set();
    const duplicateIds = [];
    let usable = 0;
    let denied = 0;

    for (const m of models) {
      registered.push({ providerKey, ...m });
      if (seen.has(m.id)) duplicateIds.push(m.id);
      seen.add(m.id);
      if (policy.denylist.has(m.id)) denied++;
      const remoteName = remoteById.get(m.id)?.name;
      const ok = await probeModel(provider, m.id).catch(() => false);
      if (ok) usable++;
      check(remoteById.has(m.id), `registered model exists remotely: ${providerKey}/${m.id}`);
      check(ok, `registered model is probe-usable: ${providerKey}/${m.id}`);
      check(Object.keys(cfg.agents?.defaults?.models || {}).includes(`${providerKey}/${m.id}`), `catalog key exists: ${providerKey}/${m.id}`);
      check(!remoteName || remoteName === m.name, `registered model name matches remote: ${providerKey}/${m.id}`);
    }

    check(duplicateIds.length === 0, `provider.models has no duplicate ids: ${providerKey}`);
    providerReports.push({
      provider: providerKey,
      fetched: remote.length,
      unique: remoteById.size,
      registered: models.length,
      usable,
      denied,
      duplicates: duplicateIds,
      allowedRemote,
      duplicateRemoteIds,
    });
  }

  check(Object.keys(cfg.agents?.defaults?.models || {}).length === registered.length, 'agents.defaults.models count matches registered models count across providers');

  const report = {
    fail,
    registeredModels: registered.length,
    providers: providerReports,
    policy: {
      allowlistSize: policy.allowlist ? policy.allowlist.size : 0,
      denylistSize: policy.denylist.size,
      notes: policy.notes,
    },
    checks,
  };

  writeReportFiles(report);
  console.log(`\nSUMMARY\tfail=${fail}\tregistered=${registered.length}\tproviders=${providerKeys.join(',')}`);
  process.exitCode = fail ? 1 : 0;
})().catch(err => {
  console.error(err.stack || err.message || String(err));
  process.exit(1);
});
