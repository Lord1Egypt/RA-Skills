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
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'okki-company-split-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  return dir;
}

function createRecordingServer(t, options = {}) {
  const requests = [];
  let activeRequests = 0;
  let maxActiveRequests = 0;
  const failureCounts = new Map();
  const server = http.createServer((req, res) => {
    if (req.method !== 'POST' || req.url !== '/api/v1/companies/search-advanced') {
      res.writeHead(404, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ error: 'not found' }));
      return;
    }

    activeRequests += 1;
    maxActiveRequests = Math.max(maxActiveRequests, activeRequests);
    const chunks = [];
    req.on('data', (chunk) => chunks.push(chunk));
    req.on('end', () => {
      const body = JSON.parse(Buffer.concat(chunks).toString('utf8'));
      requests.push(body);
      const finish = () => { activeRequests -= 1; };
      const transientFailureKey = options.transientFailureKey
        ? options.transientFailureKey(body)
        : `${body.from || 0}:${JSON.stringify(body.productKeywords || [])}`;
      const failureCount = failureCounts.get(transientFailureKey) || 0;
      if (failureCount < (options.transientFailuresPerKey || 0)) {
        failureCounts.set(transientFailureKey, failureCount + 1);
        const status = options.transientFailureStatus || 502;
        res.writeHead(status, { 'content-type': 'application/json' });
        res.end(options.transientFailureBody || JSON.stringify({
          type: 'https://go.okki.ai/errors/upstream-error',
          title: 'Bad Gateway',
          status,
          detail: '系统繁忙，请稍后重试',
          instance: '/api/v1/companies/search-advanced'
        }));
        finish();
        return;
      }
      const index = requests.length;
      const companyName = options.duplicateCompany ? 'Shared Buyer Co' : `Split Search Company ${index}`;
      const domain = options.duplicateCompany ? 'shared-buyer.example' : `split-${index}.example`;
      const sendSuccess = () => {
        res.writeHead(200, { 'content-type': 'application/json' });
        const total = options.total ?? 1;
        const size = options.pageListSize || 1;
        res.end(JSON.stringify({
          total,
          list: Array.from({ length: size }, (_, rowIndex) => ({
            company_name: size === 1 ? companyName : `Page Company ${body.from + rowIndex + 1}`,
            country_code: 'SG',
            company_type: ['buyer'],
            main_products: body.productKeywords || body.companyTypeKeywords || body.industryKeywords || [],
            email_count: index + rowIndex,
            domain: size === 1 ? domain : `page-${body.from + rowIndex + 1}.example`
          }))
        }));
        finish();
      };
      if (options.delayMs) {
        setTimeout(sendSuccess, options.delayMs);
      } else {
        sendSuccess();
      }
    });
  });

  return new Promise((resolve, reject) => {
    server.on('error', reject);
    server.listen(0, '127.0.0.1', () => {
      t.after(() => new Promise((done) => server.close(done)));
      resolve({
        baseUrl: `http://127.0.0.1:${server.address().port}`,
        requests,
        getMaxActiveRequests: () => maxActiveRequests
      });
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

test('search-companies splits long keyword fields before API calls', async (t) => {
  const { baseUrl, requests } = await createRecordingServer(t);
  const tempDir = makeTempDir(t);
  const rawPath = path.join(tempDir, 'split-search.json');
  const payload = {
    productKeywords: Array.from({ length: 12 }, (_, index) => `keyword-${index + 1}`),
    includeCountry: ['SG', 'MY', 'TH', 'VN', 'ID', 'PH'],
    size: 20
  };

  const result = await runScript('search-companies.js', [
    '--json', JSON.stringify(payload),
    '--compact',
    '--save-raw', rawPath
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.equal(requests.length, 3);
  assert.deepEqual(requests.map((request) => request.productKeywords.length), [5, 5, 2]);
  assert.ok(requests.every((request) => request.includeCountry.length === 6));

  const output = JSON.parse(result.stdout);
  assert.equal(output.split_query_count, 3);
  assert.equal(output.rows.length, 3);
  assert.equal(fs.existsSync(rawPath), true);
});

test('search-companies splits company type roles into one role per API call', async (t) => {
  const { baseUrl, requests } = await createRecordingServer(t);
  const payload = {
    productKeywords: ['汽车玻璃', '挡风玻璃'],
    companyTypeKeywords: ['进口商', '经销商', '供应商', '维修服务商'],
    includeCountry: ['IN', 'PK', 'BD'],
    size: 20
  };

  const result = await runScript('search-companies.js', [
    '--json', JSON.stringify(payload),
    '--compact'
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.equal(requests.length, 4);
  assert.deepEqual(requests.map((request) => request.companyTypeKeywords), [
    ['进口商'],
    ['经销商'],
    ['供应商'],
    ['维修服务商']
  ]);
  assert.ok(requests.every((request) => request.productKeywords.length === 2));
  assert.ok(requests.every((request) => request.includeCountry.length === 3));

  const output = JSON.parse(result.stdout);
  assert.equal(output.split_query_count, 4);
});

test('search-companies does not semantically split one compound company type term', async (t) => {
  const { baseUrl, requests } = await createRecordingServer(t);
  const payload = {
    companyTypeKeywords: ['汽车玻璃供应商'],
    includeCountry: ['IN'],
    size: 20
  };

  const result = await runScript('search-companies.js', [
    '--json', JSON.stringify(payload),
    '--compact'
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.equal(requests.length, 1);
  assert.deepEqual(requests[0].companyTypeKeywords, ['汽车玻璃供应商']);
  assert.equal(Object.hasOwn(requests[0], 'productKeywords'), false);

  const output = JSON.parse(result.stdout);
  assert.equal(Object.hasOwn(output, 'split_query_count'), false);
});

test('discover-companies-batch splits each oversized keyword dimension and keeps countries intact', async (t) => {
  const { baseUrl, requests } = await createRecordingServer(t);
  const tempDir = makeTempDir(t);
  const batchPath = path.join(tempDir, 'discover-split.json');
  const plan = {
    request_summary: 'split batch',
    target_count: 20,
    payloads: [{
      productKeywords: Array.from({ length: 11 }, (_, index) => `product-${index + 1}`),
      companyTypeKeywords: Array.from({ length: 6 }, (_, index) => `type-${index + 1}`),
      includeCountry: ['SG', 'MY', 'TH', 'VN', 'ID', 'PH'],
      size: 10
    }]
  };

  const result = await runScript('discover-companies-batch.js', [
    '--json', JSON.stringify(plan),
    '--save-batch', batchPath,
    '--compact',
    '--concurrency', '1'
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.equal(requests.length, 18);
  assert.ok(requests.every((request) => request.productKeywords.length <= 5));
  assert.ok(requests.every((request) => request.companyTypeKeywords.length <= 1));
  assert.ok(requests.every((request) => request.includeCountry.length === 6));

  const output = JSON.parse(result.stdout);
  assert.equal(output.scanned_pages, 18);
  assert.equal(output.split_query_count, 18);
  assert.equal(fs.existsSync(batchPath), true);
});

test('discover-companies-batch splits company type roles into one role per API call', async (t) => {
  const { baseUrl, requests } = await createRecordingServer(t);
  const tempDir = makeTempDir(t);
  const batchPath = path.join(tempDir, 'discover-company-type-split.json');
  const plan = {
    request_summary: 'split company type roles',
    target_count: 20,
    payloads: [{
      productKeywords: ['汽车玻璃', '挡风玻璃'],
      companyTypeKeywords: ['进口商', '经销商', '供应商', '维修服务商'],
      includeCountry: ['IN', 'PK', 'BD'],
      size: 10
    }]
  };

  const result = await runScript('discover-companies-batch.js', [
    '--json', JSON.stringify(plan),
    '--save-batch', batchPath,
    '--compact'
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.equal(requests.length, 4);
  assert.deepEqual(requests.map((request) => request.companyTypeKeywords), [
    ['进口商'],
    ['经销商'],
    ['供应商'],
    ['维修服务商']
  ]);
  assert.ok(requests.every((request) => request.productKeywords.length === 2));
  assert.ok(requests.every((request) => request.includeCountry.length === 3));

  const output = JSON.parse(result.stdout);
  assert.equal(output.scanned_pages, 4);
  assert.equal(output.split_query_count, 4);
  assert.equal(fs.existsSync(batchPath), true);
});

test('search-companies deduplicates compact results after splitting', async (t) => {
  const { baseUrl, requests } = await createRecordingServer(t, { duplicateCompany: true });
  const payload = {
    productKeywords: Array.from({ length: 6 }, (_, index) => `keyword-${index + 1}`),
    includeCountry: ['SG'],
    size: 10
  };

  const result = await runScript('search-companies.js', [
    '--json', JSON.stringify(payload),
    '--compact'
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.equal(requests.length, 2);

  const output = JSON.parse(result.stdout);
  assert.equal(output.split_query_count, 2);
  assert.equal(output.rows.length, 1);
  assert.equal(output.rows[0].company_name, 'Shared Buyer Co');
});

test('search-companies retries one transient busy response before failing the free search', async (t) => {
  const { baseUrl, requests } = await createRecordingServer(t, {
    transientFailuresPerKey: 1,
    transientFailureStatus: 502
  });
  const payload = {
    productKeywords: ['gift packaging'],
    includeCountry: ['SG'],
    size: 10
  };

  const result = await runScript('search-companies.js', [
    '--json', JSON.stringify(payload),
    '--compact'
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.equal(requests.length, 2);
  const output = JSON.parse(result.stdout);
  assert.equal(output.rows.length, 1);
});

test('discover-companies-batch omits split_query_count when no split is needed', async (t) => {
  const { baseUrl, requests } = await createRecordingServer(t);
  const plan = {
    request_summary: 'normal batch',
    payloads: [{
      productKeywords: ['gift boxes', 'gift packaging'],
      includeCountry: ['SG', 'MY', 'TH', 'VN', 'ID', 'PH'],
      size: 10
    }]
  };

  const result = await runScript('discover-companies-batch.js', [
    '--json', JSON.stringify(plan),
    '--compact',
    '--concurrency', '1'
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.equal(requests.length, 1);

  const output = JSON.parse(result.stdout);
  assert.equal(Object.hasOwn(output, 'split_query_count'), false);
});

test('discover-companies-batch normalizes payloads and drops unsupported fields before API calls', async (t) => {
  const { baseUrl, requests } = await createRecordingServer(t);
  const plan = {
    request_summary: 'normalized batch',
    payloads: [{
      productKeywords: 'gift packaging',
      includeCountry: 'de',
      employeeRange: '50-200',
      website: 'example.com',
      size: 10,
      pages: 1
    }]
  };

  const result = await runScript('discover-companies-batch.js', [
    '--json', JSON.stringify(plan),
    '--compact',
    '--concurrency', '1'
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.deepEqual(requests[0].productKeywords, ['gift packaging']);
  assert.deepEqual(requests[0].includeCountry, ['DE']);
  assert.equal(Object.hasOwn(requests[0], 'employeeRange'), false);
  assert.equal(Object.hasOwn(requests[0], 'website'), false);
  assert.equal(Object.hasOwn(requests[0], 'pages'), false);
});

test('discover-companies-batch defaults to serial API calls to avoid internal busy limits', async (t) => {
  const { baseUrl, requests, getMaxActiveRequests } = await createRecordingServer(t, { delayMs: 30 });
  const plan = {
    request_summary: 'serial default batch',
    payloads: [{
      productKeywords: Array.from({ length: 12 }, (_, index) => `keyword-${index + 1}`),
      includeCountry: ['SG'],
      size: 10
    }]
  };

  const result = await runScript('discover-companies-batch.js', [
    '--json', JSON.stringify(plan),
    '--compact'
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.equal(requests.length, 3);
  assert.equal(getMaxActiveRequests(), 1);
});

test('discover-companies-batch retries one transient busy response before failing the batch', async (t) => {
  const { baseUrl, requests } = await createRecordingServer(t, {
    transientFailuresPerKey: 1,
    transientFailureStatus: 502
  });
  const plan = {
    request_summary: 'busy retry batch',
    payloads: [{
      productKeywords: ['gift packaging'],
      includeCountry: ['SG'],
      size: 10
    }]
  };

  const result = await runScript('discover-companies-batch.js', [
    '--json', JSON.stringify(plan),
    '--compact'
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.equal(requests.length, 2);
  const output = JSON.parse(result.stdout);
  assert.equal(output.rows.length, 1);
});

test('search-companies next_offset is absolute API offset for paginated requests', async (t) => {
  const { baseUrl, requests } = await createRecordingServer(t, { total: 100, pageListSize: 20 });
  const result = await runScript('search-companies.js', [
    '--json', JSON.stringify({ productKeywords: ['gift packaging'], includeCountry: ['SG'], from: 20, size: 20 }),
    '--compact'
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.equal(requests[0].from, 20);
  const output = JSON.parse(result.stdout);
  assert.equal(output.returned, 20);
  assert.equal(output.truncated, true);
  assert.equal(output.next_offset, 40);
  assert.equal(output.discovery_health.has_next_page, true);
  assert.equal(output.next_action, 'paginate_next');
});
