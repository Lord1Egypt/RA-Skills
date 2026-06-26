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
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'okki-debug-metadata-'));
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
            company_name: 'AutoTeile Import GmbH',
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
            email_count: 1,
            whatsapp_count: 0,
            domain: 'berlin-components.example',
            id: 'private-id-2'
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

test('search-companies hides debug metadata unless explicitly requested', async (t) => {
  const baseUrl = await createCompanyServer(t);
  const tempDir = makeTempDir(t);
  const rawPath = path.join(tempDir, 'search-raw.json');
  const payload = JSON.stringify({ productKeywords: ['汽车配件'], includeCountry: ['DE'], size: 2 });

  const normal = await runScript('search-companies.js', [
    '--json', payload,
    '--compact',
    '--limit-output', '1',
    '--save-raw', rawPath
  ], { OKKIGO_BASE_URL: baseUrl });
  assert.equal(normal.status, 0, normal.stderr || normal.stdout);

  const normalOutput = JSON.parse(normal.stdout);
  assert.equal(Object.hasOwn(normalOutput, 'batch_id'), false);
  assert.equal(Object.hasOwn(normalOutput, 'raw_path'), false);
  assert.equal(Object.hasOwn(normalOutput, 'private_mapping_saved'), false);
  assert.equal(Object.hasOwn(normalOutput, 'output_budget'), false);
  assert.equal(Object.hasOwn(normalOutput, 'debug_metadata'), false);
  assert.equal(normalOutput.rows[0].company_name, 'AutoTeile Import GmbH');
  assert.equal(normalOutput.rows[0].has_email, true);
  assert.equal(normalOutput.rows[0].has_whatsapp, true);
  assert.equal(normalOutput.rows[0].founding_time, '1998');
  assert.equal(normalOutput.rows[0].employees_count, '51-200');
  assert.equal(Object.hasOwn(normalOutput.rows[0], 'email_count'), false);
  assert.equal(Object.hasOwn(normalOutput.rows[0], 'whatsapp_count'), false);
  assert.equal(normalOutput.discovery_health.health_action, 'fetch_next_page');
  assert.equal(normalOutput.next_action, 'paginate_next');
  assert.match(normalOutput.display_table_markdown, /^\| Row \| Company Name \| Country\/Region \| Company Type \| Fit \| Has Email \| More Info \|/);
  assert.match(normalOutput.display_table_markdown, /WhatsApp: Yes; Employees: 51-200; Founded: 1998/);
  assert.match(normalOutput.display_table_markdown, /AutoTeile Import GmbH/);
  assert.equal(normalOutput.display_table_markdown.includes('autoteile.example'), false);
  assert.equal(normal.stdout.includes('autoteile.example'), false);
  assert.equal(fs.existsSync(rawPath), true);

  const debug = await runScript('search-companies.js', [
    '--json', payload,
    '--compact',
    '--limit-output', '1',
    '--save-raw', rawPath,
    '--debug-metadata'
  ], { OKKIGO_BASE_URL: baseUrl });
  assert.equal(debug.status, 0, debug.stderr || debug.stdout);

  const debugOutput = JSON.parse(debug.stdout);
  assert.match(debugOutput.display_table_markdown, /^\| Row \| Company Name \| Country\/Region \| Company Type \| Fit \| Has Email \| More Info \|/);
  assert.equal(debugOutput.debug_metadata.raw_path, rawPath);
  assert.equal(debugOutput.debug_metadata.private_mapping_saved, true);
  assert.equal(debugOutput.debug_metadata.batch_id, 'search-raw');
  assert.equal(typeof debugOutput.debug_metadata.output_budget, 'object');
});

test('local wrappers hide debug metadata unless explicitly requested', async (t) => {
  const tempDir = makeTempDir(t);
  const batchPath = path.join(tempDir, 'displayed-batch.json');
  const rawPath = path.join(tempDir, 'unlock-raw.json');
  const markdownPath = path.join(tempDir, 'company-details.md');
  fs.writeFileSync(batchPath, JSON.stringify({
    version: '1.0',
    request_summary: 'German buyers',
    rows: [
      {
        row: 1,
        domain: 'autoteile.example',
        country_code: 'DE',
        company_name: 'AutoTeile Import GmbH',
        raw: {
          domain: 'autoteile.example',
          company_type: ['auto parts distributor'],
          main_products: ['brake parts'],
          founding_time: '1998',
          employees_count: '51-200',
          whatsapp_count: 1
        }
      },
      {
        row: 2,
        domain: 'berlin-components.example',
        country_code: 'DE',
        company_name: 'Berlin Components Trading',
        raw: {
          domain: 'berlin-components.example',
          company_type: ['automotive wholesaler'],
          main_products: ['vehicle parts']
        }
      },
      {
        row: 3,
        domain: 'munich-parts.example',
        country_code: 'DE',
        company_name: 'Munich Parts GmbH',
        raw: { domain: 'munich-parts.example' }
      },
      {
        row: 4,
        domain: 'hamburg-fleet.example',
        country_code: 'DE',
        company_name: 'Hamburg Fleet Service',
        raw: { domain: 'hamburg-fleet.example' }
      },
      {
        row: 5,
        domain: 'cologne-auto.example',
        country_code: 'DE',
        company_name: 'Cologne Auto Supply',
        raw: { domain: 'cologne-auto.example' }
      },
      {
        row: 6,
        domain: 'stuttgart-wheels.example',
        country_code: 'DE',
        company_name: 'Stuttgart Wheels',
        raw: { domain: 'stuttgart-wheels.example' }
      }
    ]
  }));

  const noDebug = await runScript('unlock-companies.js', [
    '--batch', batchPath,
    '--rows', '1-6',
    '--compact',
    '--raw-file', rawPath,
    '--markdown-file', markdownPath
  ], { OKKIGO_BASE_URL: await createUnlockServer(t) });
  assert.equal(noDebug.status, 0, noDebug.stderr || noDebug.stdout);

  const normalOutput = JSON.parse(noDebug.stdout);
  assert.equal(Object.hasOwn(normalOutput, 'batch_id'), false);
  assert.equal(Object.hasOwn(normalOutput, 'raw_path'), false);
  assert.equal(Object.hasOwn(normalOutput, 'output_budget'), false);
  assert.equal(Object.hasOwn(normalOutput, 'debug_metadata'), false);
  assert.equal(normalOutput.raw_saved, true);
  assert.equal(Object.hasOwn(normalOutput, 'results'), false);
  assert.equal(normalOutput.total_details_count, 6);
  assert.equal(normalOutput.displayed_details_count, 5);
  assert.equal(normalOutput.details_markdown_saved, true);
  assert.equal(normalOutput.details_markdown_path, markdownPath);
  assert.equal(typeof normalOutput.unlock_details_markdown, 'string');
  assert.match(normalOutput.unlock_details_markdown, /# OKKI Go 解锁结果/);
  assert.match(normalOutput.unlock_details_markdown, /计划解锁: 6 家/);
  assert.match(normalOutput.unlock_details_markdown, /成功: 6 家/);
  assert.match(normalOutput.unlock_details_markdown, /失败: 0 家/);
  assert.doesNotMatch(normalOutput.unlock_details_markdown, /已尝试|未尝试/);
  assert.equal(Object.hasOwn(normalOutput, 'stopped_count'), false);
  assert.equal(normalOutput.next_action, 'draft_outreach');
  assert.match(normalOutput.unlock_details_markdown, new RegExp(`全部详情见: ${escapeRegExp(markdownPath)}`));
  assert.match(normalOutput.unlock_details_markdown, /\| 字段 \| 内容 \|/);
  assert.match(normalOutput.unlock_details_markdown, /\| 原序号 \| 1 \|/);
  assert.match(normalOutput.unlock_details_markdown, /\| 公司名 \| AutoTeile Import GmbH \|/);
  assert.match(normalOutput.unlock_details_markdown, /\| 国家\/地区 \| Germany \|/);
  assert.match(normalOutput.unlock_details_markdown, /\| 官网\/域名 \| autoteile\.example \|/);
  assert.match(normalOutput.unlock_details_markdown, /\| 邮箱 \| buyer@autoteile\.example \|/);
  assert.match(normalOutput.unlock_details_markdown, /\| 电话\/WhatsApp \| \+49 123 456 \|/);
  const chatDescription = normalOutput.unlock_details_markdown.match(/\| 公司简介 \| ([\s\S]*?) \|/)[1];
  assert.equal(chatDescription.length, 201);
  assert.match(chatDescription, /…$/);
  assert.match(chatDescription, /^This distributor profile is intentionally long/);
  assert.match(normalOutput.unlock_details_markdown, /## 5\. Cologne Auto Supply/);
  assert.equal(normalOutput.unlock_details_markdown.includes('## 6. Stuttgart Wheels'), false);
  assert.equal(normalOutput.unlock_details_markdown.includes('有邮箱'), false);
  assert.equal(normalOutput.unlock_details_markdown.includes('有 WhatsApp'), false);
  assert.equal(normalOutput.company_details.length, 5);
  assert.equal(normalOutput.company_details[0].company_name, 'AutoTeile Import GmbH');
  assert.equal(normalOutput.company_details[0].display_website, 'autoteile.example');
  assert.equal(normalOutput.company_details[0].has_email, true);
  assert.equal(normalOutput.company_details[0].has_whatsapp, true);
  assert.deepEqual(normalOutput.company_details[0].main_products, ['brake parts']);
  assert.equal(normalOutput.company_details[0].employees, '51-200');
  assert.equal(fs.existsSync(markdownPath), true);
  const markdown = fs.readFileSync(markdownPath, 'utf8');
  assert.match(markdown, /# OKKI Go 公司详情/);
  assert.match(markdown, /## 1\. AutoTeile Import GmbH/);
  assert.match(markdown, /## 6\. Stuttgart Wheels/);
  assert.match(markdown, /全部公司详情/);
  assert.match(markdown, /- 邮箱: buyer@autoteile\.example/);
  assert.match(markdown, /- 电话\/WhatsApp: \+49 123 456/);
  assert.match(markdown, /additional descriptive content that should remain complete in the markdown file/);
  assert.equal(markdown.includes('- 有邮箱:'), false);
  assert.equal(markdown.includes('- 有 WhatsApp:'), false);

  const debug = await runScript('unlock-companies.js', [
    '--batch', batchPath,
    '--rows', '1',
    '--compact',
    '--raw-file', rawPath,
    '--markdown-file', path.join(tempDir, 'debug-company-details.md'),
    '--debug-metadata'
  ], { OKKIGO_BASE_URL: await createUnlockServer(t) });
  assert.equal(debug.status, 0, debug.stderr || debug.stdout);

  const debugOutput = JSON.parse(debug.stdout);
  assert.equal(debugOutput.debug_metadata.batch_id, 'displayed-batch');
  assert.equal(debugOutput.debug_metadata.raw_path, rawPath);
  assert.equal(typeof debugOutput.debug_metadata.output_budget, 'object');
});

function createUnlockServer(t) {
  const longDescription = [
    'This distributor profile is intentionally long to verify chat truncation. ',
    'It contains operational coverage, import readiness, foodservice distribution notes, ',
    'regional customer segments, and additional descriptive content that should remain complete in the markdown file.'
  ].join('');
  const server = http.createServer((req, res) => {
    if (req.method === 'POST' && req.url === '/api/v1/companies/unlock') {
      const chunks = [];
      req.on('data', (chunk) => chunks.push(chunk));
      req.on('end', () => {
        const body = JSON.parse(Buffer.concat(chunks).toString('utf8'));
        const name = unlockNameFromDomain(body.domain);
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
      const name = unlockNameFromDomain(domain);
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify({
        name,
        domain,
        founded_year: 1998,
        employee_count: 75,
        employee_desc: '51-200',
        description: domain === 'autoteile.example'
          ? longDescription
          : `${name} is a German automotive parts distributor.`,
        profile: `${name} supplies automotive parts and services.`,
        social_links: ['https://www.linkedin.com/company/example']
      }));
      return;
    }

    if (req.method === 'GET' && req.url.startsWith('/api/v1/companies/hash-') && req.url.endsWith('/profileEmails')) {
      const domain = domainFromProfileUrl(req.url);
      const name = unlockNameFromDomain(domain);
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify({
        totalCount: 1,
        contactCount: 1,
        emailCount: 1,
        domain,
        emails: [{
          name: 'Buyer One',
          first_name: 'Buyer',
          last_name: 'One',
          position: 'Purchasing Manager',
          value: `buyer@${domain}`,
          emails: [`buyer@${domain}`],
          phone_numbers: ['+49 123 456'],
          linkedin: 'https://www.linkedin.com/in/buyer-one',
          company_name: name
        }]
      }));
      return;
    }

    if (req.method === 'GET' && req.url === '/api/v1/credit/balance') {
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ monthlyPoints: 79, addonPoints: 0 }));
      return;
    }

    res.writeHead(404, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ error: 'not found' }));
  });

  return new Promise((resolve, reject) => {
    server.on('error', reject);
    server.listen(0, '127.0.0.1', () => {
      t.after(() => new Promise((done) => server.close(done)));
      resolve(`http://127.0.0.1:${server.address().port}`);
    });
  });
}

function unlockNameFromDomain(domain) {
  return {
    'autoteile.example': 'AutoTeile Import GmbH',
    'berlin-components.example': 'Berlin Components Trading',
    'munich-parts.example': 'Munich Parts GmbH',
    'hamburg-fleet.example': 'Hamburg Fleet Service',
    'cologne-auto.example': 'Cologne Auto Supply',
    'stuttgart-wheels.example': 'Stuttgart Wheels'
  }[domain] || domain;
}

function domainFromProfileUrl(url) {
  const encoded = url.split('/')[4] || '';
  return {
    'hash-autoteile-example': 'autoteile.example',
    'hash-berlin-components-example': 'berlin-components.example',
    'hash-munich-parts-example': 'munich-parts.example',
    'hash-hamburg-fleet-example': 'hamburg-fleet.example',
    'hash-cologne-auto-example': 'cologne-auto.example',
    'hash-stuttgart-wheels-example': 'stuttgart-wheels.example'
  }[encoded] || encoded.replace(/^hash-/, '').replace(/-example$/, '.example').replace(/-/g, '.');
}

function escapeRegExp(value) {
  return String(value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
