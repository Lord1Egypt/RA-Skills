#!/usr/bin/env node
'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const net = require('node:net');
const os = require('node:os');
const path = require('node:path');
const vm = require('node:vm');
const { spawn } = require('node:child_process');

const root = path.join(__dirname, '..');

function read(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), 'utf8');
}

function getFreePort() {
  return new Promise((resolve, reject) => {
    const probe = net.createServer();
    probe.once('error', reject);
    probe.listen(0, '127.0.0.1', () => {
      const { port } = probe.address();
      probe.close(() => resolve(port));
    });
  });
}

function request(port, pathname, options = {}) {
  return new Promise((resolve, reject) => {
    const req = http.request({
      host: '127.0.0.1',
      port,
      path: pathname,
      method: options.method || 'GET',
      headers: options.headers || {},
    }, (res) => {
      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => resolve({
        status: res.statusCode,
        headers: res.headers,
        body: Buffer.concat(chunks).toString('utf8'),
      }));
    });
    req.on('error', reject);
    if (options.body) req.write(options.body);
    req.end();
  });
}

function rawRequest(port, payload) {
  return new Promise((resolve, reject) => {
    const socket = net.createConnection({ host: '127.0.0.1', port });
    let response = '';
    socket.setEncoding('utf8');
    socket.setTimeout(3000);
    socket.on('connect', () => socket.end(payload));
    socket.on('data', (chunk) => { response += chunk; });
    socket.on('end', () => resolve(response));
    socket.on('timeout', () => {
      socket.destroy();
      reject(new Error('Raw HTTP request timed out'));
    });
    socket.on('error', reject);
  });
}

async function waitForHealth(port, child) {
  for (let attempt = 0; attempt < 50; attempt += 1) {
    if (child.exitCode !== null) throw new Error(`Server exited early with code ${child.exitCode}`);
    try {
      const response = await request(port, '/health');
      if (response.status === 200) return response;
    } catch {
      // Retry while the server initializes.
    }
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw new Error('Dashboard server did not become healthy');
}

async function main() {
  const html = read('frontend/index.html');
  const css = read('frontend/shared/styles.css');
  const api = read('frontend/shared/api.js');
  const server = read('backend/server.js');
  const copilot = read('backend/providers/copilot.js');
  const modelsRegistry = read('models-registry.json');
  const sparkMonitor = read('frontend/tabs/spark-monitor.js');
  const tasksProvider = read('backend/providers/tasks.js');
  const configProvider = read('backend/providers/config.js');
  const compatibilityProvider = read('backend/providers/ops-legacy.js');
  const gitignore = read('.gitignore');
  const packageJson = JSON.parse(read('package.json'));
  const start = read('start.sh');
  const startExample = read('start.sh.example');
  const envExample = read('env.example');
  const envExampleText = read('env.example.txt');
  const browserBundle = [
    'frontend/shared/api.js',
    'frontend/shared/ui-utils.js',
    'frontend/tabs/overview.js',
    'frontend/tabs/cost.js',
    'frontend/tabs/cron.js',
    'frontend/tabs/health.js',
    'frontend/tabs/spark-monitor.js',
    'frontend/tabs/copilot.js',
    'frontend/tabs/config.js',
    'frontend/shared/boot.js',
  ].map(read).join('\n;\n');
  assert.doesNotThrow(() => new vm.Script(browserBundle, { filename: 'dashboard-browser-bundle.js' }));

  assert.match(html, /class="app-shell"/);
  assert.match(html, /class="shell-nav"/);
  assert.match(html, /id="themeToggleBtn"/);
  assert.match(html, /data-tab="copilot"/);
  assert.match(html, /data-tab="spark"/);
  const htmlIds = [...html.matchAll(/\bid="([^"]+)"/g)].map((match) => match[1]);
  assert.equal(new Set(htmlIds).size, htmlIds.length, 'frontend/index.html must not contain duplicate ids');
  assert.match(css, /--accent:#ff5c5c/);
  assert.match(css, /grid-template-columns:258px minmax\(0,1fr\)/);
  assert.match(css, /data-theme-mode="light"/);
  assert.doesNotMatch(css, /rgba\(124,92,252|#6b4ce6/);
  assert.doesNotMatch(`${css}\n${sparkMonitor}`, /#7c6af7|#a78bfa|rgba\(124,106,247/);
  assert.match(api, /const API = '';/);
  assert.match(api, /PUBLIC_PREVIEW_MODE/);
  assert.match(api, /OpenClaw Gateway/);
  assert.match(html, /id="previewModeBadge"[^>]*hidden/);
  assert.doesNotMatch(api, /\['18789'.*18793/);
  assert.doesNotMatch(api, /URLSearchParams\(location\.search\).*token/s);
  assert.match(server, /helpers\.authenticate\(request\)/);
  assert.match(server, /parseRequestUrl\(req\)/);
  assert.doesNotMatch(server, /query\.token/);
  assert.match(server, /Refusing to start without OPENCLAW_AUTH_TOKEN/);
  assert.match(copilot, /OPENCLAW_ENABLE_COPILOT|ENABLE_COPILOT/);
  assert.match(copilot, /meetingChannel\(meetingId, 'transcript'\)/);
  assert.match(copilot, /LegacyMeetingCoordinator/);
  assert.doesNotMatch(copilot, /readFileSync|keys\.env|\.openclaw\/\.env/);
  assert.doesNotMatch(tasksProvider, /triggerTaskExecution|writeFileSync|renameSync|HOOK_TOKEN/);
  assert.doesNotMatch(configProvider, /req\.method === 'PUT'|writeFileSync/);
  assert.doesNotMatch(compatibilityProvider, /proxyToOld|router\.add\('POST'/);
  assert.doesNotMatch(compatibilityProvider, /url\.parse\(/);
  assert.doesNotMatch(server, /ENABLE_LEGACY_PROXY|proxyToOld/);
  assert.match(start, /backend\/server\.js/);
  assert.doesNotMatch(start, /api-server\.js/);
  assert.equal(start, startExample);
  assert.equal(envExample, envExampleText);
  assert.ok((fs.statSync(path.join(root, 'start.sh')).mode & 0o111) !== 0, 'start.sh must be executable');
  assert.doesNotMatch(gitignore, /^start\.sh$/m);
  assert.match(gitignore, /^scripts\/\*$/m);
  assert.match(gitignore, /^!scripts\/test-dashboard\.js$/m);
  assert.equal(packageJson.scripts.test, 'node scripts/test-dashboard.js');
  assert.ok(packageJson.files.includes('start.sh'));
  assert.ok(packageJson.files.includes('scripts/test-dashboard.js'));
  assert.ok(packageJson.files.includes('env.example.txt'));
  assert.ok(packageJson.files.includes('screenshots/overview-v2-light.png'));
  assert.ok(packageJson.files.includes('screenshots/usage-v2-dark.png'));
  assert.ok(packageJson.files.includes('screenshots/mobile-v2-dark.png'));
  assert.match(html, /id="controlUiLink"[^>]*hidden/);
  assert.doesNotMatch(html, /href="http:\/\/127\.0\.0\.1:18789\//);
  assert.doesNotMatch(html, /id="btnRestart"|id="btnDoctor"/);
  assert.doesNotMatch(html, /id="createModal"|id="createTaskBtn"|id="editToggleBtn"|id="saveBtn"/);
  assert.doesNotMatch(read('frontend/tabs/config.js'), /createTask\(|toggleEditMode|saveFile\(|toggleContentEdit|kanbanDrop/);

  const publicFiles = [
    'backend/server.js',
    'backend/lib/config.js',
    'backend/lib/http-helpers.js',
    'backend/providers/copilot.js',
    'backend/providers/config.js',
    'backend/providers/ops-legacy.js',
    'backend/providers/tasks.js',
    'frontend/shared/api.js',
    'frontend/tabs/config.js',
    'scripts/test-dashboard.js',
    'start.sh',
    'start.sh.example',
  ].map(read).join('\n');
  assert.doesNotMatch(publicFiles, /\/Users\/[A-Za-z0-9._-]+/);
  assert.doesNotMatch(publicFiles, /OPENCLAW_AUTH_TOKEN\s*=\s*["'][A-Za-z0-9_-]{16,}/);
  assert.doesNotMatch(publicFiles, /sk-[A-Za-z0-9_-]{16,}/);
  assert.doesNotMatch(modelsRegistry, /\b(?:10|127\.0\.0\.1|192\.168|172\.(?:1[6-9]|2[0-9]|3[01]))\./);
  assert.doesNotMatch(modelsRegistry, /"baseUrl"/);
  assert.doesNotMatch(compatibilityProvider, /\b192\.168\./);

  const configModule = require(path.join(root, 'backend/providers/config.js'));
  const secretFixture = {
    apiKey: 'sk-test-secret',
    OPENAI_API_KEY: 'sk-env-secret',
    token: 'tok-secret',
    author: 'public-author',
    nested: { webhookUrl: 'https://example.invalid/private' },
  };
  configModule._test.redactSecrets(secretFixture);
  assert.equal(secretFixture.apiKey, '[REDACTED]');
  assert.equal(secretFixture.OPENAI_API_KEY, '[REDACTED]');
  assert.equal(secretFixture.token, '[REDACTED]');
  assert.equal(secretFixture.nested.webhookUrl, '[REDACTED]');
  assert.equal(secretFixture.author, 'public-author');

  const { LegacyMeetingCoordinator } = require(path.join(root, 'backend/providers/copilot.js'))._test;
  const coordinator = new LegacyMeetingCoordinator();
  const promoted = [];
  assert.equal(coordinator.add('meeting-a', async () => promoted.push('meeting-a')), true);
  assert.equal(coordinator.add('meeting-b', async () => promoted.push('meeting-b')), false);
  await coordinator.remove('meeting-a');
  assert.equal(coordinator.ownerId, 'meeting-b');
  assert.deepEqual(promoted, ['meeting-b']);
  assert.equal(coordinator.size, 1);

  const port = await getFreePort();
  const tempHome = fs.mkdtempSync(path.join(os.tmpdir(), 'openclaw-dashboard-test-'));
  const tempOpenClaw = path.join(tempHome, '.openclaw');
  fs.mkdirSync(path.join(tempOpenClaw, 'workspace'), { recursive: true });
  fs.writeFileSync(path.join(tempOpenClaw, 'openclaw.json'), JSON.stringify(secretFixture));
  const token = 'dashboard=test-token=';
  const child = spawn(process.execPath, ['backend/server.js'], {
    cwd: root,
    env: {
      ...process.env,
      HOME: tempHome,
      DASHBOARD_HOST: '127.0.0.1',
      DASHBOARD_PORT: String(port),
      OPENCLAW_AUTH_TOKEN: token,
      OPENCLAW_ENABLE_COPILOT: '0',
      OPENCLAW_ENABLE_CONFIG_ENDPOINT: '1',
      DASHBOARD_COOKIE_SECURE: '1',
      OPENCLAW_CONTROL_UI_URL: 'https://gateway.example/openclaw/',
    },
    stdio: ['ignore', 'pipe', 'pipe'],
  });

  try {
    const health = await waitForHealth(port, child);
    const healthJson = JSON.parse(health.body);
    assert.equal(healthJson.status, 'ok');
    assert.equal(healthJson.capabilities.copilot, false);
    assert.equal(healthJson.capabilities.mutatingOps, false);
    assert.equal(healthJson.capabilities.operatorActions, false);
    assert.equal(healthJson.links.controlUi, 'https://gateway.example/openclaw/');

    const malformedHost = await rawRequest(
      port,
      'GET /health HTTP/1.1\r\nHost: [\r\nConnection: close\r\n\r\n'
    );
    assert.match(malformedHost, /^HTTP\/1\.1 (200|400)/);
    assert.equal((await request(port, '/health')).status, 200);

    const unauthenticated = await request(port, '/');
    assert.equal(unauthenticated.status, 302);
    assert.equal(unauthenticated.headers.location, '/login');

    const malformedCookie = await request(port, '/api/copilot/status', {
      headers: { Cookie: 'ds=%' },
    });
    assert.equal(malformedCookie.status, 401);
    assert.equal((await request(port, '/health')).status, 200);

    const login = await request(port, '/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token }),
    });
    assert.equal(login.status, 200);
    const setCookie = login.headers['set-cookie']?.[0] || '';
    const loginCookie = setCookie.split(';')[0] || '';
    assert.match(loginCookie, /^ds=dashboard%3Dtest-token%3D$/);
    assert.match(setCookie, /HttpOnly/);
    assert.match(setCookie, /SameSite=Strict/);
    assert.match(setCookie, /Secure/);

    const cookieAuthenticated = await request(port, '/api/copilot/status', {
      headers: { Cookie: loginCookie },
    });
    assert.equal(cookieAuthenticated.status, 200);

    const configResponse = await request(port, '/ops/config', {
      headers: { Cookie: loginCookie },
    });
    assert.equal(configResponse.status, 200);
    const configJson = JSON.parse(configResponse.body);
    assert.equal(configJson.config.apiKey, '[REDACTED]');
    assert.equal(configJson.config.OPENAI_API_KEY, '[REDACTED]');
    assert.equal(configJson.config.token, '[REDACTED]');
    assert.equal(configJson.config.nested.webhookUrl, '[REDACTED]');
    assert.equal(configJson.config.author, 'public-author');
    assert.doesNotMatch(configResponse.body, /sk-test-secret|sk-env-secret|tok-secret|example\.invalid\/private/);

    const tokenHandoff = await request(port, `/?token=${encodeURIComponent(token)}`);
    assert.equal(tokenHandoff.status, 302);
    assert.equal(tokenHandoff.headers.location, '/login');
    assert.equal(tokenHandoff.body, '');

    const queryTokenApi = await request(port, `/api/copilot/status?token=${encodeURIComponent(token)}`);
    assert.equal(queryTokenApi.status, 401);

    const authenticated = await request(port, '/api/copilot/status', {
      headers: { Authorization: `Bearer ${token}` },
    });
    assert.equal(authenticated.status, 200);
    assert.equal(JSON.parse(authenticated.body).configured, false);

    for (const [method, pathname] of [
      ['POST', '/ops/restart'],
      ['POST', '/ops/doctor'],
      ['POST', '/tasks'],
      ['PUT', '/files?path=README.md'],
    ]) {
      const response = await request(port, pathname, {
        method,
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: '{}',
      });
      assert.equal(response.status, 404, `${method} ${pathname} must remain unregistered`);
    }

    const dashboard = await request(port, '/', {
      headers: { Authorization: `Bearer ${token}` },
    });
    assert.equal(dashboard.status, 200);
    assert.match(dashboard.body, /OpenClaw/);
  } finally {
    if (child.exitCode === null) {
      child.kill('SIGTERM');
      await new Promise((resolve) => child.once('exit', resolve));
    }
    fs.rmSync(tempHome, { recursive: true, force: true });
  }

  console.log('Dashboard checks passed.');
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
