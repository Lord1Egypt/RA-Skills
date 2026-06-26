const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const os = require('node:os');
const path = require('node:path');
const { spawn } = require('node:child_process');

const SCRIPTS_DIR = path.resolve(__dirname, '..');
const REPO_ROOT = path.resolve(__dirname, '..', '..', '..');

const EXPECTED_ZH_HEADER = '| 序号 | 公司名称 | 国家/地区 | 公司类型 | 匹配理由 | 有邮箱 | 更多信息 |';
const EXPECTED_EN_HEADER = '| Row | Company Name | Country/Region | Company Type | Fit | Has Email | More Info |';
const EXPECTED_SEPARATOR = '|---:|---|---|---|---|---|---|';

function makeTempDir(t) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'okki-company-display-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  return dir;
}

function createCompanyServer(t) {
  const server = http.createServer((req, res) => {
    if (req.method !== 'POST' || req.url !== '/api/v1/companies/search-advanced') {
      res.writeHead(404, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ error: 'not found' }));
      return;
    }

    req.resume();
    req.on('end', () => {
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify({
        total: 2,
        list: [
          {
            company_name: 'Auto|Teile Import GmbH',
            country_code: 'DE',
            company_type: ['auto parts distributor'],
            main_products: ['brake parts'],
            email_count: 3,
            whatsapp_count: 1,
            founding_time: '1998',
            employees_count: '51-200',
            domain: 'autoteile.example',
            id: 'private-id-1'
          },
          {
            company_name: 'Berlin Components Trading',
            country_code: 'DE',
            company_type: ['automotive wholesaler'],
            main_products: ['vehicle parts'],
            email_count: 0,
            whatsapp_count: 0,
            employees_count: '',
            domain: 'berlin-components.example',
            companyHashId: 'private-id-2'
          }
        ]
      }));
    });
  });

  return new Promise((resolve, reject) => {
    server.on('error', reject);
    server.listen(0, '127.0.0.1', () => {
      t.after(() => new Promise((done) => server.close(done)));
      resolve(`http://127.0.0.1:${server.address().port}`);
    });
  });
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

function assertFixedDisplayTable(output, options = {}) {
  const {
    expectedHeader = EXPECTED_ZH_HEADER,
    firstInfo = 'WhatsApp：是；员工数：51-200；成立时间：1998',
    secondInfo = 'WhatsApp：否；员工数：未知；成立时间：未知',
    yes = '是',
    no = '否'
  } = options;
  assert.equal(typeof output.display_table_markdown, 'string');
  const lines = output.display_table_markdown.trim().split('\n');
  assert.equal(lines[0], expectedHeader);
  assert.equal(lines[1], EXPECTED_SEPARATOR);
  assert.equal(lines.length, 4);
  assert.match(lines[2], /^\| 1 \| Auto\\\|Teile Import GmbH \|/);
  assert.match(lines[2], new RegExp(`\\| ${yes} \\| ${escapeRegExp(firstInfo)} \\|$`));
  assert.match(lines[3], new RegExp(`\\| ${no} \\| ${escapeRegExp(secondInfo)} \\|$`));
  assert.equal(lines[2].includes('has_whatsapp'), false);
  assert.equal(lines[2].includes('employees_count'), false);
  assert.equal(lines[2].includes('founding_time'), false);

  for (const privateTerm of [
    'autoteile.example',
    'berlin-components.example',
    'private-id',
    'domain',
    'companyHashId',
    'email_count',
    'whatsapp_count',
    'raw_path',
    'batch_id'
  ]) {
    assert.equal(output.display_table_markdown.includes(privateTerm), false, privateTerm);
  }
}

function escapeRegExp(value) {
  return String(value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

test('search-companies compact output includes a script-rendered fixed display table', async (t) => {
  const baseUrl = await createCompanyServer(t);
  const tempDir = makeTempDir(t);
  const rawPath = path.join(tempDir, 'search-display.json');
  const payload = JSON.stringify({ productKeywords: ['汽车配件'], includeCountry: ['DE'], size: 2 });

  const result = await runScript('search-companies.js', [
    '--json', payload,
    '--compact',
    '--locale', 'zh-CN',
    '--save-raw', rawPath
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  const output = JSON.parse(result.stdout);
  assert.equal(Object.hasOwn(output, 'display_rows'), false);
  assertFixedDisplayTable(output);
  assert.equal(output.next_action, 'ask_unlock_selection');
  assert.match(output.selection_handle, /^sel_[a-f0-9]{24}$/);
  assert.equal(typeof output.discovery_health, 'object');
});

test('search-companies compact display table localizes English headers and detail labels', async (t) => {
  const baseUrl = await createCompanyServer(t);
  const payload = JSON.stringify({ productKeywords: ['auto parts'], includeCountry: ['DE'], size: 2 });

  const result = await runScript('search-companies.js', [
    '--json', payload,
    '--compact',
    '--locale', 'en-US'
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  const output = JSON.parse(result.stdout);
  assertFixedDisplayTable(output, {
    expectedHeader: EXPECTED_EN_HEADER,
    firstInfo: 'WhatsApp: Yes; Employees: 51-200; Founded: 1998',
    secondInfo: 'WhatsApp: No; Employees: Unknown; Founded: Unknown',
    yes: 'Yes',
    no: 'No'
  });
  const lines = output.display_table_markdown.trim().split('\n');
  assert.match(lines[2], /\| Yes \| WhatsApp: Yes; Employees: 51-200; Founded: 1998 \|$/);
  assert.match(lines[3], /\| No \| WhatsApp: No; Employees: Unknown; Founded: Unknown \|$/);
});

test('search-companies fixed display table ignores legacy row field projection', async (t) => {
  const baseUrl = await createCompanyServer(t);
  const payload = JSON.stringify({ productKeywords: ['汽车配件'], includeCountry: ['DE'], size: 2 });

  const result = await runScript('search-companies.js', [
    '--json', payload,
    '--compact',
    '--locale', 'zh-CN',
    '--fields', 'company_name'
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  const output = JSON.parse(result.stdout);
  assert.equal(Object.hasOwn(output, 'display_rows'), false);
  assert.deepEqual(Object.keys(output.rows[0]), ['company_name']);
  assertFixedDisplayTable(output);
});

test('discover-companies-batch compact output includes the same fixed display table', async (t) => {
  const baseUrl = await createCompanyServer(t);
  const tempDir = makeTempDir(t);
  const batchPath = path.join(tempDir, 'discover-display.json');
  const plan = {
    request_summary: 'German auto parts buyers',
    target_count: 2,
    payloads: [{
      productKeywords: ['汽车配件'],
      includeCountry: ['DE'],
      size: 2
    }]
  };

  const result = await runScript('discover-companies-batch.js', [
    '--json', JSON.stringify(plan),
    '--target-count', '2',
    '--save-batch', batchPath,
    '--compact',
    '--locale', 'zh-CN',
    '--concurrency', '1'
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  const output = JSON.parse(result.stdout);
  assert.equal(Object.hasOwn(output, 'display_rows'), false);
  assertFixedDisplayTable(output);
  assert.equal(output.next_action, 'ask_unlock_selection');
  assert.match(output.selection_handle, /^sel_[a-f0-9]{24}$/);
  assert.equal(typeof output.discovery_health, 'object');
});
