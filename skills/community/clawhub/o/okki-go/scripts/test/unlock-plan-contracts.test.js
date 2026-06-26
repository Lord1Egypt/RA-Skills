const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const os = require('node:os');
const path = require('node:path');
const { spawn } = require('node:child_process');

const SCRIPTS_DIR = path.resolve(__dirname, '..');
const REPO_ROOT = path.resolve(__dirname, '..', '..', '..');

function makeTempDir(t) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'okki-unlock-plan-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  return dir;
}

function runScript(scriptName, args, env = {}) {
  return new Promise((resolve) => {
    const child = spawn(process.execPath, [path.join(SCRIPTS_DIR, scriptName), ...args], {
      cwd: REPO_ROOT,
      env: {
        ...process.env,
        OKKIGO_API_KEY: 'sk-test',
        OKKI_GO_API_KEY: '',
        OKKIGO_SKILL_API_KEY: '',
        ...env
      },
      stdio: ['ignore', 'pipe', 'pipe']
    });
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', (chunk) => { stdout += chunk.toString('utf8'); });
    child.stderr.on('data', (chunk) => { stderr += chunk.toString('utf8'); });
    child.on('close', (status) => resolve({ status, stdout, stderr }));
  });
}

function writeBatch(filePath, rows, requestSummary = 'original batch') {
  fs.writeFileSync(filePath, `${JSON.stringify({
    version: '1.0',
    request_summary: requestSummary,
    rows
  }, null, 2)}\n`);
}

function writeSelectionHandle(filePath, handle, batchPath, requestSummary = 'original batch') {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${JSON.stringify({
    version: '1.0',
    kind: 'company_selection',
    selection_handle: handle,
    batch_path: batchPath,
    batch_id: path.basename(batchPath).replace(/\.[^.]+$/, ''),
    displayed_rows: 2,
    request_summary: requestSummary,
    created_at: new Date().toISOString()
  }, null, 2)}\n`);
}

function writeSelectionSet(filePath, selections) {
  fs.writeFileSync(filePath, `${JSON.stringify({ selections }, null, 2)}\n`);
}

function row(rowNumber, companyName, domain, countryCode = 'DE') {
  return {
    row: rowNumber,
    domain,
    country_code: countryCode,
    company_name: companyName,
    raw: { domain, company_name: companyName }
  };
}

function createUnlockServer(t) {
  const requests = [];
  const server = http.createServer((req, res) => {
    if (req.method === 'POST' && req.url === '/api/v1/companies/unlock') {
      const chunks = [];
      req.on('data', (chunk) => chunks.push(chunk));
      req.on('end', () => {
        const body = JSON.parse(Buffer.concat(chunks).toString('utf8'));
        requests.push(body);
        const name = nameFromDomain(body.domain);
        res.writeHead(200, { 'content-type': 'application/json' });
        res.end(JSON.stringify({
          companyHashId: `hash-${body.domain.replace(/[^a-z0-9]+/gi, '-')}`,
          companyName: name,
          charged: true
        }));
      });
      return;
    }

    if (req.method === 'GET' && req.url.startsWith('/api/v1/companies/hash-') && req.url.endsWith('/profile')) {
      const domain = domainFromProfileUrl(req.url);
      const name = nameFromDomain(domain);
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify({
        name,
        domain,
        description: `${name} profile`
      }));
      return;
    }

    if (req.method === 'GET' && req.url.startsWith('/api/v1/companies/hash-') && req.url.endsWith('/profileEmails')) {
      const domain = domainFromProfileUrl(req.url);
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify({
        total: 1,
        emails: [{ email: `buyer@${domain}` }]
      }));
      return;
    }

    if (req.method === 'GET' && req.url === '/api/v1/credit/balance') {
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ monthlyPoints: 97, addonPoints: 0 }));
      return;
    }

    res.writeHead(404, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ error: 'not found' }));
  });

  return new Promise((resolve, reject) => {
    server.on('error', reject);
    server.listen(0, '127.0.0.1', () => {
      t.after(() => new Promise((done) => server.close(done)));
      resolve({ baseUrl: `http://127.0.0.1:${server.address().port}`, requests });
    });
  });
}

function createFailingUnlockServer(t, failureDomain, options = {}) {
  const requests = [];
  const server = http.createServer((req, res) => {
    if (req.method === 'POST' && req.url === '/api/v1/companies/unlock') {
      const chunks = [];
      req.on('data', (chunk) => chunks.push(chunk));
      req.on('end', () => {
        const body = JSON.parse(Buffer.concat(chunks).toString('utf8'));
        requests.push(body);
        if (body.domain === failureDomain) {
          res.writeHead(options.statusCode || 404, { 'content-type': 'application/json' });
          res.end(JSON.stringify({ detail: options.detail || 'No company found for the given domain and country' }));
          return;
        }
        res.writeHead(200, { 'content-type': 'application/json' });
        res.end(JSON.stringify({
          companyHashId: `hash-${body.domain.replace(/[^a-z0-9]+/gi, '-')}`,
          companyName: nameFromDomain(body.domain),
          charged: true
        }));
      });
      return;
    }

    res.writeHead(404, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ error: 'not found' }));
  });

  return new Promise((resolve, reject) => {
    server.on('error', reject);
    server.listen(0, '127.0.0.1', () => {
      t.after(() => new Promise((done) => server.close(done)));
      resolve({ baseUrl: `http://127.0.0.1:${server.address().port}`, requests });
    });
  });
}

function readJsonLines(filePath) {
  return fs.readFileSync(filePath, 'utf8')
    .trim()
    .split(/\r?\n/)
    .filter(Boolean)
    .map((line) => JSON.parse(line));
}

function nameFromDomain(domain) {
  return {
    'original-a.example': 'Original A',
    'original-b.example': 'Original B',
    'latest-a.example': 'Latest A',
    'latest-b.example': 'Latest B'
  }[domain] || domain;
}

function domainFromProfileUrl(url) {
  const encoded = url.split('/')[4] || '';
  const key = encoded.replace(/^hash-/, '').replace(/-example$/, '.example');
  return key.replace(/-/g, '.');
}

test('prepare-unlock-plan hides plan id by default and exposes it only in debug metadata', async (t) => {
  const tempDir = makeTempDir(t);
  const batchPath = path.join(tempDir, 'batch.json');
  writeBatch(batchPath, [
    row(1, 'Original A', 'original-a.example'),
    row(2, 'Original B', 'original-b.example')
  ]);

  const normal = await runScript('prepare-unlock-plan.js', [
    '--batch', batchPath,
    '--rows', '1,2',
    '--compact',
    '--locale', 'en-US'
  ]);
  assert.equal(normal.status, 0, normal.stderr || normal.stdout);
  const normalOutput = JSON.parse(normal.stdout);
  assert.equal(normalOutput.prepared, true);
  assert.equal(Object.hasOwn(normalOutput, 'unlock_plan_id'), false);
  assert.equal(Object.hasOwn(normalOutput, 'batch_id'), false);
  assert.equal(Object.hasOwn(normalOutput, 'debug_metadata'), false);
  assert.deepEqual(normalOutput.selected_companies.map((item) => item.company_name), ['Original A', 'Original B']);

  const debug = await runScript('prepare-unlock-plan.js', [
    '--batch', batchPath,
    '--rows', '1,2',
    '--compact',
    '--debug-metadata'
  ]);
  assert.equal(debug.status, 0, debug.stderr || debug.stdout);
  const debugOutput = JSON.parse(debug.stdout);
  assert.match(debugOutput.debug_metadata.unlock_plan_id, /^uplan_[a-f0-9]{24}$/);
  assert.equal(debugOutput.debug_metadata.batch_id, 'batch');
});

test('selection-set plans freeze a deduped final target set across multiple selections', async (t) => {
  const tempDir = makeTempDir(t);
  const batchOne = path.join(tempDir, 'batch-one.json');
  const batchTwo = path.join(tempDir, 'batch-two.json');
  const selectionDir = path.join(tempDir, 'selections');
  const firstHandle = 'sel_111111111111111111111111';
  const secondHandle = 'sel_222222222222222222222222';
  const selectionSetPath = path.join(tempDir, 'selection-set.json');

  writeBatch(batchOne, [
    row(1, 'Original A', 'original-a.example'),
    row(2, 'Original B', 'original-b.example')
  ], 'batch one');
  writeBatch(batchTwo, [
    row(1, 'Original B Duplicate', 'original-b.example'),
    row(2, 'Latest A', 'latest-a.example')
  ], 'batch two');
  writeSelectionHandle(path.join(selectionDir, `${firstHandle}.json`), firstHandle, batchOne, 'batch one');
  writeSelectionHandle(path.join(selectionDir, `${secondHandle}.json`), secondHandle, batchTwo, 'batch two');
  writeSelectionSet(selectionSetPath, [
    { selection_handle: firstHandle, rows: '1,2', reason: 'priority' },
    { selection_handle: secondHandle, rows: '1,2', reason: 'manual add' }
  ]);

  const env = {
    OKKIGO_SELECTION_DIR: selectionDir,
    OKKIGO_UNLOCK_PLAN_DIR: path.join(tempDir, 'plans'),
    OKKIGO_ACTIVE_UNLOCK_PLAN_DIR: path.join(tempDir, 'active-plans')
  };

  const prepare = await runScript('prepare-unlock-plan.js', [
    '--selection-set-file', selectionSetPath,
    '--compact',
    '--locale', 'en-US',
    '--debug-metadata'
  ], env);

  assert.equal(prepare.status, 0, prepare.stderr || prepare.stdout);
  const output = JSON.parse(prepare.stdout);
  assert.equal(output.max_credit_cost, 3);
  assert.deepEqual(output.selected_companies.map((item) => item.company_name), ['Original A', 'Original B', 'Latest A']);
  assert.match(output.debug_metadata.unlock_plan_id, /^uplan_[a-f0-9]{24}$/);
  assert.match(output.debug_metadata.target_set_fingerprint, /^[a-f0-9]{16}$/);

  const plan = JSON.parse(fs.readFileSync(path.join(env.OKKIGO_UNLOCK_PLAN_DIR, `${output.debug_metadata.unlock_plan_id}.json`), 'utf8'));
  assert.equal(plan.source.kind, 'target_set');
  assert.equal(plan.target_set_fingerprint, output.debug_metadata.target_set_fingerprint);
  assert.deepEqual(plan.rows.map((item) => item.domain), ['original-a.example', 'original-b.example', 'latest-a.example']);
  assert.deepEqual(plan.rows.map((item) => item.target_sources.length), [1, 2, 1]);
});

test('selection-set target changes supersede previously prepared final target set', async (t) => {
  const tempDir = makeTempDir(t);
  const batchPath = path.join(tempDir, 'batch.json');
  const selectionDir = path.join(tempDir, 'selections');
  const selectionHandle = 'sel_333333333333333333333333';
  const initialSetPath = path.join(tempDir, 'initial-set.json');
  const changedSetPath = path.join(tempDir, 'changed-set.json');

  writeBatch(batchPath, [
    row(1, 'Original A', 'original-a.example'),
    row(2, 'Original B', 'original-b.example')
  ]);
  writeSelectionHandle(path.join(selectionDir, `${selectionHandle}.json`), selectionHandle, batchPath);
  writeSelectionSet(initialSetPath, [{ selection_handle: selectionHandle, rows: '1' }]);
  writeSelectionSet(changedSetPath, [{ selection_handle: selectionHandle, rows: '1,2' }]);

  const env = {
    OKKIGO_SELECTION_DIR: selectionDir,
    OKKIGO_UNLOCK_PLAN_DIR: path.join(tempDir, 'plans'),
    OKKIGO_ACTIVE_UNLOCK_PLAN_DIR: path.join(tempDir, 'active-plans')
  };

  const initialPrepare = await runScript('prepare-unlock-plan.js', [
    '--selection-set-file', initialSetPath,
    '--compact',
    '--debug-metadata'
  ], env);
  assert.equal(initialPrepare.status, 0, initialPrepare.stderr || initialPrepare.stdout);
  const initialPlanId = JSON.parse(initialPrepare.stdout).debug_metadata.unlock_plan_id;

  const changedPrepare = await runScript('prepare-unlock-plan.js', [
    '--selection-set-file', changedSetPath,
    '--compact',
    '--debug-metadata'
  ], env);
  assert.equal(changedPrepare.status, 0, changedPrepare.stderr || changedPrepare.stdout);
  const changedOutput = JSON.parse(changedPrepare.stdout);
  assert.deepEqual(changedOutput.selected_companies.map((item) => item.company_name), ['Original A', 'Original B']);

  const { baseUrl, requests } = await createUnlockServer(t);
  const unlock = await runScript('unlock-companies.js', [
    '--plan', initialPlanId,
    '--compact',
    '--raw-file', path.join(tempDir, 'unlock-raw.json'),
    '--markdown-file', path.join(tempDir, 'details.md')
  ], { ...env, OKKIGO_BASE_URL: baseUrl });

  assert.equal(unlock.status, 2);
  assert.match(unlock.stderr, /stale|superseded|target set changed/i);
  assert.equal(requests.length, 0);
});

test('target-set fingerprint mismatch is rejected before paid unlock API', async (t) => {
  const tempDir = makeTempDir(t);
  const batchPath = path.join(tempDir, 'batch.json');
  const selectionDir = path.join(tempDir, 'selections');
  const selectionHandle = 'sel_444444444444444444444444';
  const selectionSetPath = path.join(tempDir, 'selection-set.json');

  writeBatch(batchPath, [
    row(1, 'Original A', 'original-a.example')
  ]);
  writeSelectionHandle(path.join(selectionDir, `${selectionHandle}.json`), selectionHandle, batchPath);
  writeSelectionSet(selectionSetPath, [{ selection_handle: selectionHandle, rows: '1' }]);

  const env = {
    OKKIGO_SELECTION_DIR: selectionDir,
    OKKIGO_UNLOCK_PLAN_DIR: path.join(tempDir, 'plans'),
    OKKIGO_ACTIVE_UNLOCK_PLAN_DIR: path.join(tempDir, 'active-plans')
  };

  const prepare = await runScript('prepare-unlock-plan.js', [
    '--selection-set-file', selectionSetPath,
    '--compact',
    '--debug-metadata'
  ], env);
  assert.equal(prepare.status, 0, prepare.stderr || prepare.stdout);
  const output = JSON.parse(prepare.stdout);
  const planId = output.debug_metadata.unlock_plan_id;
  const plan = JSON.parse(fs.readFileSync(path.join(env.OKKIGO_UNLOCK_PLAN_DIR, `${planId}.json`), 'utf8'));
  const activePath = path.join(env.OKKIGO_ACTIVE_UNLOCK_PLAN_DIR, 'target-set-company_unlock.json');
  const active = JSON.parse(fs.readFileSync(activePath, 'utf8'));
  active.target_set_fingerprint = 'ffffffffffffffff';
  fs.writeFileSync(activePath, `${JSON.stringify(active, null, 2)}\n`);

  const { baseUrl, requests } = await createUnlockServer(t);
  const unlock = await runScript('unlock-companies.js', [
    '--plan', plan.unlock_plan_id,
    '--compact',
    '--raw-file', path.join(tempDir, 'unlock-raw.json'),
    '--markdown-file', path.join(tempDir, 'details.md')
  ], { ...env, OKKIGO_BASE_URL: baseUrl });

  assert.equal(unlock.status, 2);
  assert.match(unlock.stderr, /target set fingerprint/i);
  assert.equal(requests.length, 0);
});

test('unlock plan freezes selected rows even when latest batch changes later', async (t) => {
  const tempDir = makeTempDir(t);
  const batchStatePath = path.join(tempDir, 'latest-batch.json');
  const batchA = path.join(tempDir, 'batch-a.json');
  const batchB = path.join(tempDir, 'batch-b.json');
  writeBatch(batchA, [
    row(1, 'Original A', 'original-a.example'),
    row(2, 'Original B', 'original-b.example')
  ], 'batch A');
  writeBatch(batchB, [
    row(1, 'Latest A', 'latest-a.example'),
    row(2, 'Latest B', 'latest-b.example')
  ], 'batch B');

  const env = {
    OKKIGO_BATCH_STATE_FILE: batchStatePath,
    OKKIGO_UNLOCK_PLAN_DIR: path.join(tempDir, 'plans'),
    OKKIGO_ACTIVE_UNLOCK_PLAN_DIR: path.join(tempDir, 'active-plans')
  };

  const prepare = await runScript('prepare-unlock-plan.js', [
    '--batch', batchA,
    '--rows', '1,2',
    '--compact',
    '--debug-metadata'
  ], env);
  assert.equal(prepare.status, 0, prepare.stderr || prepare.stdout);
  const planId = JSON.parse(prepare.stdout).debug_metadata.unlock_plan_id;

  fs.writeFileSync(batchStatePath, `${JSON.stringify({
    latest_batch: batchB,
    request_summary: 'batch B',
    created_at: new Date().toISOString()
  }, null, 2)}\n`);

  const { baseUrl, requests } = await createUnlockServer(t);
  const unlock = await runScript('unlock-companies.js', [
    '--plan', planId,
    '--compact',
    '--raw-file', path.join(tempDir, 'unlock-raw.json'),
    '--markdown-file', path.join(tempDir, 'details.md')
  ], { ...env, OKKIGO_BASE_URL: baseUrl });
  assert.equal(unlock.status, 0, unlock.stderr || unlock.stdout);
  assert.deepEqual(requests.map((request) => request.domain), ['original-a.example', 'original-b.example']);
  const output = JSON.parse(unlock.stdout);
  assert.equal(Object.hasOwn(output, 'unlock_plan_used'), false);
  assert.equal(output.latest_batch_used, false);

  const debugPrepare = await runScript('prepare-unlock-plan.js', [
    '--batch', batchA,
    '--rows', '1',
    '--compact',
    '--debug-metadata'
  ], env);
  assert.equal(debugPrepare.status, 0, debugPrepare.stderr || debugPrepare.stdout);
  const debugPlanId = JSON.parse(debugPrepare.stdout).debug_metadata.unlock_plan_id;

  const debugUnlock = await runScript('unlock-companies.js', [
    '--plan', debugPlanId,
    '--compact',
    '--debug-metadata',
    '--raw-file', path.join(tempDir, 'unlock-debug-raw.json'),
    '--markdown-file', path.join(tempDir, 'debug-details.md')
  ], { ...env, OKKIGO_BASE_URL: baseUrl });
  assert.equal(debugUnlock.status, 0, debugUnlock.stderr || debugUnlock.stdout);
  assert.equal(JSON.parse(debugUnlock.stdout).debug_metadata.unlock_plan_used, true);
});

test('stale unlock plan is rejected when user changes selection before confirmation', async (t) => {
  const tempDir = makeTempDir(t);
  const batchPath = path.join(tempDir, 'batch.json');
  const selectionDir = path.join(tempDir, 'selections');
  const selectionHandle = 'sel_aaaaaaaaaaaaaaaaaaaaaaaa';
  writeBatch(batchPath, [
    row(1, 'Original A', 'original-a.example'),
    row(2, 'Original B', 'original-b.example')
  ]);
  writeSelectionHandle(path.join(selectionDir, `${selectionHandle}.json`), selectionHandle, batchPath);

  const env = {
    OKKIGO_SELECTION_DIR: selectionDir,
    OKKIGO_UNLOCK_PLAN_DIR: path.join(tempDir, 'plans'),
    OKKIGO_ACTIVE_UNLOCK_PLAN_DIR: path.join(tempDir, 'active-plans')
  };

  const initialPrepare = await runScript('prepare-unlock-plan.js', [
    '--selection-handle', selectionHandle,
    '--rows', '1',
    '--compact',
    '--debug-metadata'
  ], env);
  assert.equal(initialPrepare.status, 0, initialPrepare.stderr || initialPrepare.stdout);
  const initialOutput = JSON.parse(initialPrepare.stdout);
  assert.deepEqual(initialOutput.selected_companies.map((item) => item.company_name), ['Original A']);

  const changedPrepare = await runScript('prepare-unlock-plan.js', [
    '--selection-handle', selectionHandle,
    '--rows', '2',
    '--compact',
    '--debug-metadata'
  ], env);
  assert.equal(changedPrepare.status, 0, changedPrepare.stderr || changedPrepare.stdout);
  const changedOutput = JSON.parse(changedPrepare.stdout);
  assert.notEqual(
    changedOutput.debug_metadata.unlock_plan_id,
    initialOutput.debug_metadata.unlock_plan_id
  );
  assert.deepEqual(changedOutput.selected_companies.map((item) => item.company_name), ['Original B']);

  const { baseUrl, requests } = await createUnlockServer(t);
  const unlock = await runScript('unlock-companies.js', [
    '--plan', initialOutput.debug_metadata.unlock_plan_id,
    '--compact',
    '--raw-file', path.join(tempDir, 'unlock-raw.json'),
    '--markdown-file', path.join(tempDir, 'details.md')
  ], { ...env, OKKIGO_BASE_URL: baseUrl });

  assert.equal(unlock.status, 2);
  assert.match(unlock.stderr, /stale|superseded|selection changed/i);
  assert.equal(requests.length, 0);
});

test('invalid unlock plan exits before calling paid unlock API', async (t) => {
  const tempDir = makeTempDir(t);
  const planDir = path.join(tempDir, 'plans');
  const activePlanDir = path.join(tempDir, 'active-plans');
  fs.mkdirSync(planDir, { recursive: true });
  fs.mkdirSync(activePlanDir, { recursive: true });
  const planId = 'uplan_aaaaaaaaaaaaaaaaaaaaaaaa';
  const batchPath = path.join(tempDir, 'broken-batch.json');
  const scopeKey = `batch-broken-batch-${require('node:crypto').createHash('sha256').update(batchPath).digest('hex').slice(0, 16)}-company_unlock`;
  fs.writeFileSync(path.join(planDir, `${planId}.json`), `${JSON.stringify({
    version: '1.0',
    kind: 'unlock_plan',
    action: 'company_unlock',
    unlock_plan_id: planId,
    created_at: new Date().toISOString(),
    source: {
      selection_handle: null,
      batch_path: batchPath,
      batch_id: 'broken-batch',
      request_summary: 'broken batch'
    },
    rows: [{ row: 1, company_name: 'Broken Plan' }]
  }, null, 2)}\n`);
  fs.writeFileSync(path.join(activePlanDir, `${scopeKey}.json`), `${JSON.stringify({
    version: '1.0',
    kind: 'active_unlock_plan',
    action: 'company_unlock',
    scope_key: scopeKey,
    unlock_plan_id: planId,
    updated_at: new Date().toISOString()
  }, null, 2)}\n`);

  const { baseUrl, requests } = await createUnlockServer(t);
  const result = await runScript('unlock-companies.js', [
    '--plan', planId,
    '--compact'
  ], {
    OKKIGO_UNLOCK_PLAN_DIR: planDir,
    OKKIGO_ACTIVE_UNLOCK_PLAN_DIR: activePlanDir,
    OKKIGO_BASE_URL: baseUrl
  });

  assert.equal(result.status, 2);
  assert.match(result.stderr, /missing domain/);
  assert.equal(requests.length, 0);
});

test('row-level unlock failure preserves compact result and continues deterministic rows', async (t) => {
  const tempDir = makeTempDir(t);
  const batchPath = path.join(tempDir, 'batch.json');
  const auditPath = path.join(tempDir, 'unlock-audit.jsonl');
  writeBatch(batchPath, [
    row(1, 'Missing Co', 'missing.example', 'US'),
    row(2, 'Original B', 'original-b.example', 'DE')
  ]);

  const env = {
    OKKIGO_UNLOCK_PLAN_DIR: path.join(tempDir, 'plans'),
    OKKIGO_ACTIVE_UNLOCK_PLAN_DIR: path.join(tempDir, 'active-plans')
  };

  const prepare = await runScript('prepare-unlock-plan.js', [
    '--batch', batchPath,
    '--rows', '1,2',
    '--compact',
    '--debug-metadata'
  ], env);
  assert.equal(prepare.status, 0, prepare.stderr || prepare.stdout);
  const planId = JSON.parse(prepare.stdout).debug_metadata.unlock_plan_id;

  const { baseUrl, requests } = await createFailingUnlockServer(t, 'missing.example');
  const unlock = await runScript('unlock-companies.js', [
    '--plan', planId,
    '--compact',
    '--audit-file', auditPath,
    '--raw-file', path.join(tempDir, 'unlock-raw.json'),
    '--markdown-file', path.join(tempDir, 'details.md')
  ], { ...env, OKKIGO_BASE_URL: baseUrl });

  assert.equal(unlock.status, 0, unlock.stderr || unlock.stdout);
  assert.deepEqual(requests, [
    { domain: 'missing.example', countryCode: 'US' },
    { domain: 'original-b.example', countryCode: 'DE' }
  ]);
  const output = JSON.parse(unlock.stdout);
  assert.equal(output.run_status, 'completed_with_failures');
  assert.equal(output.planned_count, 2);
  assert.equal(output.success_count, 1);
  assert.equal(output.failed_count, 1);
  assert.equal(Object.hasOwn(output, 'attempted_count'), false);
  assert.equal(Object.hasOwn(output, 'not_attempted_count'), false);
  assert.equal(output.next_action, 'draft_outreach');
  assert.match(output.unlock_details_markdown, /计划解锁: 2 家/);
  assert.match(output.unlock_details_markdown, /成功: 1 家/);
  assert.match(output.unlock_details_markdown, /失败: 1 家/);
  assert.doesNotMatch(output.unlock_details_markdown, /已尝试|未尝试/);
  assert.match(output.unlock_details_markdown, /\| 原序号 \| 公司名 \| 状态 \| 原因 \| 是否扣费 \|/);
  assert.match(output.unlock_details_markdown, /Missing Co/);
  assert.match(output.unlock_details_markdown, /Original B/);
  assert.match(output.unlock_details_markdown, /起草开发信草稿/);
  assert.equal(fs.existsSync(auditPath), true);

  const events = readJsonLines(auditPath);
  const request = events.find((event) => event.event === 'unlock_request');
  assert.equal(request.plan_id, planId);
  assert.equal(request.active_plan_id_at_execution, planId);
  assert.equal(request.row, 1);
  assert.equal(request.company_name, 'Missing Co');
  assert.equal(request.domain, 'missing.example');
  assert.equal(request.countryCode, 'US');
  assert.equal(request.request_index, 1);
  assert.match(request.request_payload_fingerprint, /^[a-f0-9]{16,64}$/);

  const failure = events.find((event) => event.event === 'unlock_failure');
  assert.equal(failure.plan_id, planId);
  assert.equal(failure.row, 1);
  assert.equal(failure.request_index, 1);
  assert.equal(failure.http_status, 404);
  assert.equal(failure.okki_error_message, 'No company found for the given domain and country');
});

test('billing-risk unlock failure stops remaining paid calls but emits structured stopped result', async (t) => {
  const tempDir = makeTempDir(t);
  const batchPath = path.join(tempDir, 'batch.json');
  writeBatch(batchPath, [
    row(1, 'Original A', 'original-a.example', 'DE'),
    row(2, 'Missing Credits', 'missing.example', 'US'),
    row(3, 'Latest A', 'latest-a.example', 'US')
  ]);

  const env = {
    OKKIGO_UNLOCK_PLAN_DIR: path.join(tempDir, 'plans'),
    OKKIGO_ACTIVE_UNLOCK_PLAN_DIR: path.join(tempDir, 'active-plans')
  };

  const prepare = await runScript('prepare-unlock-plan.js', [
    '--batch', batchPath,
    '--rows', '1,2,3',
    '--compact',
    '--debug-metadata'
  ], env);
  assert.equal(prepare.status, 0, prepare.stderr || prepare.stdout);
  const planId = JSON.parse(prepare.stdout).debug_metadata.unlock_plan_id;

  const { baseUrl, requests } = await createFailingUnlockServer(t, 'missing.example', {
    statusCode: 402,
    detail: 'Insufficient credits'
  });
  const unlock = await runScript('unlock-companies.js', [
    '--plan', planId,
    '--compact',
    '--raw-file', path.join(tempDir, 'unlock-raw.json'),
    '--markdown-file', path.join(tempDir, 'details.md')
  ], { ...env, OKKIGO_BASE_URL: baseUrl });

  assert.equal(unlock.status, 0, unlock.stderr || unlock.stdout);
  assert.deepEqual(requests.map((request) => request.domain), ['original-a.example', 'missing.example']);
  const output = JSON.parse(unlock.stdout);
  assert.equal(output.run_status, 'stopped');
  assert.equal(output.planned_count, 3);
  assert.equal(output.success_count, 1);
  assert.equal(output.failed_count, 1);
  assert.equal(output.stopped_count, 1);
  assert.equal(Object.hasOwn(output, 'not_attempted_count'), false);
  assert.match(output.unlock_details_markdown, /计划解锁: 3 家/);
  assert.match(output.unlock_details_markdown, /成功: 1 家/);
  assert.match(output.unlock_details_markdown, /失败: 1 家/);
  assert.match(output.unlock_details_markdown, /未执行: 1 家/);
  assert.match(output.unlock_details_markdown, /Latest A/);
  assert.doesNotMatch(output.unlock_details_markdown, /已尝试|未尝试/);
});

test('unlock details markdown is written to explicit artifact directory', async (t) => {
  const tempDir = makeTempDir(t);
  const batchPath = path.join(tempDir, 'batch.json');
  const artifactDir = path.join(tempDir, 'artifacts');
  const rawPath = path.join(tempDir, 'unlock-raw.json');
  const auditPath = path.join(tempDir, 'unlock-audit.jsonl');
  writeBatch(batchPath, [
    row(1, 'Original A', 'original-a.example', 'DE')
  ]);

  const { baseUrl, requests } = await createUnlockServer(t);
  const unlock = await runScript('unlock-companies.js', [
    '--batch', batchPath,
    '--rows', '1',
    '--compact',
    '--artifact-dir', artifactDir,
    '--raw-file', rawPath,
    '--audit-file', auditPath
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(unlock.status, 0, unlock.stderr || unlock.stdout);
  assert.equal(requests.length, 1);
  const output = JSON.parse(unlock.stdout);
  assert.equal(output.details_markdown_artifact, true);
  assert.equal(output.artifact_dir, artifactDir);
  assert.match(output.details_markdown_path, new RegExp(`^${escapeRegExp(artifactDir)}`));
  assert.equal(path.extname(output.details_markdown_path), '.md');
  assert.equal(fs.existsSync(output.details_markdown_path), true);
  assert.match(output.unlock_details_markdown, new RegExp(`全部详情见: ${escapeRegExp(output.details_markdown_path)}`));
  assert.equal(fs.existsSync(path.join(artifactDir, path.basename(rawPath))), false);
  assert.equal(fs.existsSync(path.join(artifactDir, path.basename(auditPath))), false);
});

test('unwritable explicit artifact path falls back to internal temporary details markdown', async (t) => {
  const tempDir = makeTempDir(t);
  const batchPath = path.join(tempDir, 'batch.json');
  const blockedArtifactDir = path.join(tempDir, 'blocked-artifact-dir');
  const rawPath = path.join(tempDir, 'unlock-raw.json');
  const auditPath = path.join(tempDir, 'unlock-audit.jsonl');
  fs.writeFileSync(blockedArtifactDir, 'not a directory');
  writeBatch(batchPath, [
    row(1, 'Original A', 'original-a.example', 'DE')
  ]);

  const { baseUrl, requests } = await createUnlockServer(t);
  const unlock = await runScript('unlock-companies.js', [
    '--batch', batchPath,
    '--rows', '1',
    '--compact',
    '--artifact-dir', blockedArtifactDir,
    '--raw-file', rawPath,
    '--audit-file', auditPath
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(unlock.status, 0, unlock.stderr || unlock.stdout);
  assert.equal(requests.length, 1);
  const output = JSON.parse(unlock.stdout);
  assert.equal(output.details_markdown_artifact, false);
  assert.equal(output.artifact_dir, null);
  assert.match(output.details_markdown_path, /^\/private\/tmp\/okki-go-batches\/company-details-/);
  assert.equal(fs.existsSync(output.details_markdown_path), true);
  assert.match(output.warnings.join('\n'), /artifact|详情|临时|temporary/i);
  assert.match(output.unlock_details_markdown, new RegExp(`全部详情见: ${escapeRegExp(output.details_markdown_path)}`));
  t.after(() => fs.rmSync(output.details_markdown_path, { force: true }));
});

test('details markdown precheck failure stops before paid unlock API when artifact and temp paths are unwritable', async (t) => {
  const tempDir = makeTempDir(t);
  const batchPath = path.join(tempDir, 'batch.json');
  const blockedMarkdownParent = path.join(tempDir, 'blocked-markdown-parent');
  const blockedInternalDir = path.join(tempDir, 'blocked-internal-dir');
  const rawPath = path.join(tempDir, 'unlock-raw.json');
  const auditPath = path.join(tempDir, 'unlock-audit.jsonl');
  fs.writeFileSync(blockedMarkdownParent, 'not a directory');
  fs.writeFileSync(blockedInternalDir, 'not a directory');
  writeBatch(batchPath, [
    row(1, 'Original A', 'original-a.example', 'DE')
  ]);

  const { baseUrl, requests } = await createUnlockServer(t);
  const unlock = await runScript('unlock-companies.js', [
    '--batch', batchPath,
    '--rows', '1',
    '--compact',
    '--markdown-file', path.join(blockedMarkdownParent, 'details.md'),
    '--raw-file', rawPath,
    '--audit-file', auditPath
  ], {
    OKKIGO_BASE_URL: baseUrl,
    OKKIGO_DETAILS_TEMP_DIR: blockedInternalDir
  });

  assert.equal(unlock.status, 2);
  assert.equal(requests.length, 0);
  assert.equal(unlock.stderr, '');
  const output = JSON.parse(unlock.stdout);
  assert.equal(output.error_code, 'DETAILS_MARKDOWN_PRECHECK_FAILED');
  assert.equal(output.paid_api_called, false);
  assert.equal(output.unlock_executed, false);
  assert.equal(output.next_action, 'authorize_artifact_dir');
  assert.match(output.recovery_suggestion, /未解锁|未扣费|授权|可写/);
});

function escapeRegExp(value) {
  return String(value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
