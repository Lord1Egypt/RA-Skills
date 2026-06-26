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
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'okki-paid-wrapper-'));
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

function createContactServer(t) {
  const requests = [];
  const server = http.createServer((req, res) => {
    if (req.method !== 'POST' || req.url !== '/api/v1/contacts/search') {
      res.writeHead(404, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ error: 'not found' }));
      return;
    }
    const chunks = [];
    req.on('data', (chunk) => chunks.push(chunk));
    req.on('end', () => {
      const body = JSON.parse(Buffer.concat(chunks).toString('utf8'));
      requests.push(body);
      const size = Number(body.size) || 20;
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify({
        total: size,
        list: Array.from({ length: size }, (_, index) => ({
          name: `Buyer ${index + 1}`,
          title: 'Procurement Manager',
          company_name: `Company ${index + 1}`,
          country_code: 'DE',
          email: `buyer${index + 1}@example.com`
        }))
      }));
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

function createEmailServer(t) {
  const requests = [];
  const server = http.createServer((req, res) => {
    if (req.method !== 'POST' || !req.url.startsWith('/api/v1/emails/send/')) {
      res.writeHead(404, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ error: 'not found' }));
      return;
    }
    const chunks = [];
    req.on('data', (chunk) => chunks.push(chunk));
    req.on('end', () => {
      const body = JSON.parse(Buffer.concat(chunks).toString('utf8'));
      requests.push({ url: req.url, body });
      const list = Array.isArray(body.recipients) ? body.recipients : body.emails;
      res.writeHead(201, { 'content-type': 'application/json' });
      res.end(JSON.stringify({
        total: list.length,
        status: 'pending',
        tasks: list.map((_, index) => ({ task_id: 1000 + index, mail_id: 2000 + index }))
      }));
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

test('search-contacts honors requested size up to 100 and keeps compact charge semantics explicit', async (t) => {
  const { baseUrl, requests } = await createContactServer(t);
  const tempDir = makeTempDir(t);
  const batchPath = path.join(tempDir, 'contacts.json');
  const result = await runScript('search-contacts.js', [
    '--json', JSON.stringify({ title: 'Procurement Manager', country_codes: 'DE', has_email: 1, size: 50 }),
    '--save-batch', batchPath,
    '--compact'
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.equal(requests[0].size, 50);
  const output = JSON.parse(result.stdout);
  assert.equal(output.contacts.length, 50);
  assert.equal(output.charged, true);
  assert.equal(output.charge_type, 'credit_per_query');
  assert.equal(output.balance_available, false);
  assert.equal(fs.existsSync(batchPath), true);
});

test('search-contacts accepts size 100 and rejects size above 100', async (t) => {
  const { baseUrl, requests } = await createContactServer(t);
  const ok = await runScript('search-contacts.js', [
    '--json', JSON.stringify({ title: 'Procurement Manager', size: 100 }),
    '--compact'
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(ok.status, 0, ok.stderr || ok.stdout);
  assert.equal(requests[0].size, 100);

  const tooLarge = await runScript('search-contacts.js', [
    '--json', JSON.stringify({ title: 'Procurement Manager', size: 101 }),
    '--compact'
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(tooLarge.status, 2);
  assert.match(tooLarge.stderr, /size must be an integer between 1 and 100/);
});

test('send-email validates batch recipients and personalized emails by mode', async (t) => {
  const { baseUrl, requests } = await createEmailServer(t);
  const tempDir = makeTempDir(t);

  const batch = await runScript('send-email.js', [
    'batch',
    '--json', JSON.stringify({
      content: 'Hello company_name',
      body_format: 'text',
      recipients: [{ email: 'buyer@example.com', subject: 'Hello' }]
    }),
    '--mapping-file', path.join(tempDir, 'batch.json'),
    '--compact'
  ], { OKKIGO_BASE_URL: baseUrl });
  assert.equal(batch.status, 0, batch.stderr || batch.stdout);

  const personalized = await runScript('send-email.js', [
    'personalized',
    '--json', JSON.stringify({
      emails: [{ email: 'buyer2@example.com', subject: 'Hello', content: 'Hi', body_format: 'text' }]
    }),
    '--mapping-file', path.join(tempDir, 'personalized.json'),
    '--compact'
  ], { OKKIGO_BASE_URL: baseUrl });
  assert.equal(personalized.status, 0, personalized.stderr || personalized.stdout);

  assert.equal(requests[0].url, '/api/v1/emails/send/batch');
  assert.equal(requests[1].url, '/api/v1/emails/send/personalized');
  const output = JSON.parse(personalized.stdout);
  assert.equal(output.submitted, true);
  assert.equal(output.status, 'pending');
  assert.equal(output.accepted_count, 1);
  assert.equal(output.rejected_count, 0);
  assert.match(output.next_status_command, /email-status\.js tasks/);
});

test('send-email rejects payload list shape that does not match mode', async (t) => {
  const { baseUrl } = await createEmailServer(t);
  const result = await runScript('send-email.js', [
    'personalized',
    '--json', JSON.stringify({
      recipients: [{ email: 'buyer@example.com', subject: 'Hello' }]
    }),
    '--compact'
  ], { OKKIGO_BASE_URL: baseUrl });

  assert.equal(result.status, 2);
  assert.match(result.stderr, /personalized mode must include emails\[\]/);
});
