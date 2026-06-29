const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const os = require('node:os');
const path = require('node:path');
const { spawn, spawnSync } = require('node:child_process');

const SCRIPTS_DIR = path.resolve(__dirname, '..');
const REPO_ROOT = path.resolve(__dirname, '..', '..', '..');
const {
  curlHeaderArgumentLines,
  resolveRuntimeAttribution,
  runtimeAttributionHeaders
} = require('../lib/runtime-attribution');

function makeTempDir(t) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'okki-runtime-attribution-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  return dir;
}

function writeJson(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`);
}

function createServer(t, route, responseBody) {
  const requests = [];
  const server = http.createServer((req, res) => {
    if (req.url !== route) {
      res.writeHead(404, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ error: 'not found' }));
      return;
    }
    const chunks = [];
    req.on('data', (chunk) => chunks.push(chunk));
    req.on('end', () => {
      requests.push({
        method: req.method,
        headers: req.headers,
        body: Buffer.concat(chunks).toString('utf8')
      });
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify(responseBody));
    });
  });
  return new Promise((resolve, reject) => {
    server.on('error', reject);
    server.listen(0, '127.0.0.1', () => {
      t.after(() => new Promise((done) => server.close(done)));
      resolve({ baseUrl: `http://127.0.0.1:${server.address().port}`, requests });
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
        OKKIGO_INSTALL_ID: '',
        OKKI_GO_INSTALL_ID: '',
        OKKIGO_SOURCE_PACKAGE: '',
        OKKI_GO_SOURCE_PACKAGE: '',
        OKKIGO_CHANNEL_CODE: '',
        OKKI_GO_CHANNEL_CODE: '',
        OKKIGO_CAMPAIGN_ID: '',
        OKKI_GO_CAMPAIGN_ID: '',
        OKKIGO_SKILL_VERSION: '',
        OKKIGO_SKILL_RUNTIME: '',
        OKKIGO_AGENT: '',
        OKKIGO_AGENT_MODEL: '',
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

test('runtime attribution headers prefer current environment variables', (t) => {
  const headers = runtimeAttributionHeaders({
    env: {
      OKKIGO_INSTALL_ID: 'install-env',
      OKKIGO_SOURCE_PACKAGE: '@okki-global/okki-go-taroball',
      OKKIGO_CHANNEL_CODE: 'taroball',
      OKKIGO_CAMPAIGN_ID: 'op_taroball_default',
      OKKIGO_SKILL_VERSION: '9.9.9',
      OKKIGO_SKILL_RUNTIME: 'codex',
      OKKIGO_AGENT: 'codex-cli',
      OKKIGO_AGENT_MODEL: 'gpt-5'
    },
    configHome: makeTempDir(t),
    skillRoot: makeTempDir(t)
  });

  assert.equal(headers['X-Okki-Install-Id'], 'install-env');
  assert.equal(headers['X-Okki-Source-Type'], 'npm_wrapper');
  assert.equal(headers['X-Okki-Source-Package'], '@okki-global/okki-go-taroball');
  assert.equal(headers['X-Okki-Channel-Code'], 'taroball');
  assert.equal(headers['X-Okki-Campaign-Id'], 'op_taroball_default');
  assert.equal(headers['X-Okki-Skill-Version'], '9.9.9');
  assert.equal(headers['X-Okki-Skill-Runtime'], 'codex');
  assert.equal(headers['X-Okki-Agent'], 'codex-cli');
  assert.equal(headers['X-Okki-Agent-Model'], 'gpt-5');
});

test('runtime attribution reads installed attribution file and manifest fallback', (t) => {
  const configHome = makeTempDir(t);
  const skillRoot = makeTempDir(t);
  writeJson(path.join(configHome, 'okki-go', 'install-attribution.json'), {
    installId: 'install-file',
    sourcePackage: '@okki-global/okki-go-taroball',
    channelCode: 'taroball',
    campaignId: 'op_taroball_default',
    skillVersion: '1.3.3'
  });
  writeJson(path.join(skillRoot, '.okki-go-manifest.json'), {
    runtime: 'codex'
  });

  const attribution = resolveRuntimeAttribution({ env: {}, configHome, skillRoot });
  assert.equal(attribution.installId, 'install-file');
  assert.equal(attribution.sourceType, 'npm_wrapper');
  assert.equal(attribution.sourcePackage, '@okki-global/okki-go-taroball');
  assert.equal(attribution.channelCode, 'taroball');
  assert.equal(attribution.campaignId, 'op_taroball_default');
  assert.equal(attribution.skillVersion, '1.3.3');
  assert.equal(attribution.runtime, 'codex');
});

test('runtime attribution falls back to manifest and does not mark organic install as wrapper', (t) => {
  const configHome = makeTempDir(t);
  const skillRoot = makeTempDir(t);
  writeJson(path.join(skillRoot, '.okki-go-manifest.json'), {
    installId: 'install-manifest',
    version: '1.3.3',
    runtime: 'claude',
    sourcePackage: '@okki-global/okki-go',
    channelCode: 'organic',
    campaignId: ''
  });

  const headers = runtimeAttributionHeaders({ env: {}, configHome, skillRoot });
  assert.equal(headers['X-Okki-Install-Id'], 'install-manifest');
  assert.equal(headers['X-Okki-Skill-Version'], '1.3.3');
  assert.equal(headers['X-Okki-Skill-Runtime'], 'claude');
  assert.equal(Object.hasOwn(headers, 'X-Okki-Source-Type'), false);
  assert.equal(Object.hasOwn(headers, 'X-Okki-Source-Package'), false);
});

test('runtime attribution fails open when attribution JSON is damaged', (t) => {
  const configHome = makeTempDir(t);
  const skillRoot = makeTempDir(t);
  fs.mkdirSync(path.join(configHome, 'okki-go'), { recursive: true });
  fs.writeFileSync(path.join(configHome, 'okki-go', 'install-attribution.json'), '{bad json');

  const headers = runtimeAttributionHeaders({ env: {}, configHome, skillRoot });
  assert.equal(headers['X-Okki-Skill-Version'], '1.3.3');
  assert.equal(headers['X-Okki-Skill-Runtime'], 'unknown');
  assert.equal(Object.hasOwn(headers, 'X-Okki-Source-Type'), false);
});

test('runtime attribution exposes curl argument output for authentication examples', (t) => {
  const configHome = makeTempDir(t);
  writeJson(path.join(configHome, 'okki-go', 'install-attribution.json'), {
    installId: 'install-curl',
    sourcePackage: '@okki-global/okki-go-taroball',
    channelCode: 'taroball',
    campaignId: 'op_taroball_default',
    skillVersion: '1.3.3'
  });

  const args = curlHeaderArgumentLines(runtimeAttributionHeaders({ env: {}, configHome, skillRoot: makeTempDir(t) }));
  assert.deepEqual(args.slice(0, 4), [
    '-H',
    'X-Okki-Skill-Version: 1.3.3',
    '-H',
    'X-Okki-Skill-Runtime: unknown'
  ]);
  assert.equal(args.includes('X-Okki-Source-Type: npm_wrapper'), true);

  const result = spawnSync(process.execPath, [path.join(SCRIPTS_DIR, 'lib', 'runtime-attribution.js'), '--curl-null'], {
    env: {
      ...process.env,
      XDG_CONFIG_HOME: configHome,
      OKKIGO_INSTALL_ID: '',
      OKKI_GO_INSTALL_ID: '',
      OKKIGO_SOURCE_PACKAGE: '',
      OKKI_GO_SOURCE_PACKAGE: '',
      OKKIGO_CHANNEL_CODE: '',
      OKKI_GO_CHANNEL_CODE: '',
      OKKIGO_CAMPAIGN_ID: '',
      OKKI_GO_CAMPAIGN_ID: '',
      OKKIGO_SKILL_VERSION: '',
      OKKIGO_SKILL_RUNTIME: '',
      OKKIGO_AGENT: '',
      OKKIGO_AGENT_MODEL: ''
    },
    encoding: 'utf8'
  });

  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout.includes('\0X-Okki-Source-Type: npm_wrapper\0'), true);
  assert.equal(result.stdout.endsWith('\0'), true);
});

test('shared API helper sends wrapper attribution headers', async (t) => {
  const { baseUrl, requests } = await createServer(t, '/api/v1/contacts/search', { total: 0, list: [] });
  const configHome = makeTempDir(t);
  writeJson(path.join(configHome, 'okki-go', 'install-attribution.json'), {
    installId: 'install-shared',
    sourcePackage: '@okki-global/okki-go-taroball',
    channelCode: 'taroball',
    campaignId: 'op_taroball_default',
    skillVersion: '1.3.3'
  });

  const result = await runScript('search-contacts.js', [
    '--json', JSON.stringify({ title: 'Procurement Manager', size: 1 }),
    '--compact'
  ], {
    OKKIGO_BASE_URL: baseUrl,
    XDG_CONFIG_HOME: configHome
  });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.equal(requests[0].headers['x-okki-install-id'], 'install-shared');
  assert.equal(requests[0].headers['x-okki-source-type'], 'npm_wrapper');
  assert.equal(requests[0].headers['x-okki-source-package'], '@okki-global/okki-go-taroball');
  assert.equal(requests[0].headers['x-okki-channel-code'], 'taroball');
  assert.equal(requests[0].headers['x-okki-campaign-id'], 'op_taroball_default');
});

test('search-companies sends same wrapper attribution headers as shared helper', async (t) => {
  const { baseUrl, requests } = await createServer(t, '/api/v1/companies/search-advanced', { total: 0, list: [] });
  const configHome = makeTempDir(t);
  writeJson(path.join(configHome, 'okki-go', 'install-attribution.json'), {
    installId: 'install-company',
    sourcePackage: '@okki-global/okki-go-taroball',
    channelCode: 'taroball',
    campaignId: 'op_taroball_default',
    skillVersion: '1.3.3'
  });

  const result = await runScript('search-companies.js', [
    '--json', JSON.stringify({ productKeywords: ['包装材料'], size: 1 }),
    '--compact'
  ], {
    OKKIGO_BASE_URL: baseUrl,
    XDG_CONFIG_HOME: configHome
  });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.equal(requests[0].headers['x-okki-install-id'], 'install-company');
  assert.equal(requests[0].headers['x-okki-source-type'], 'npm_wrapper');
  assert.equal(requests[0].headers['x-okki-source-package'], '@okki-global/okki-go-taroball');
  assert.equal(requests[0].headers['x-okki-channel-code'], 'taroball');
  assert.equal(requests[0].headers['x-okki-campaign-id'], 'op_taroball_default');
});
