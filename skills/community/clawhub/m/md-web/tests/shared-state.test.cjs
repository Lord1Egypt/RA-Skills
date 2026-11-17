const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const skill = path.resolve(__dirname, '..');
const {createPublishHelpers, parseLifecycleConfiguration} = require('../upload.js');
const config = {access_key: 'fixture', secret_key: 'fixture', endpoint: 's3.invalid', bucket: 'b', public_url: 'https://public.invalid/prefix'};
const userRule = '<Rule><ID>backups</ID><Filter><Prefix>backups/</Prefix></Filter><Status>Enabled</Status><Expiration><Days>365</Days></Expiration></Rule>';
const ownRule = '<Rule><ID>md-web-auto-expire</ID><Filter><Prefix>md-web/</Prefix></Filter><Status>Enabled</Status><Expiration><Days>7</Days></Expiration></Rule>';
const lifecycle = rules => '<LifecycleConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">' + rules + '</LifecycleConfiguration>';

function workspace(t) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'md-web-state-'));
  assert.equal(path.dirname(root), path.resolve(os.tmpdir()));
  t.after(() => fs.rmSync(root, {recursive: true, force: true}));
  const home = path.join(root, 'home');
  fs.mkdirSync(path.join(home, '.md-web'), {recursive: true});
  fs.writeFileSync(path.join(home, '.md-web/config.json'), JSON.stringify(config));
  fs.writeFileSync(path.join(home, 'doc.md'), '# Document\n\nExisting behavior.');
  const bundle = path.join(root, 'bundle');
  fs.cpSync(path.join(skill, 'docsify-server'), path.join(bundle, 'docsify-server'), {recursive: true});
  return {root, home, bundle};
}

class Bucket {
  objects = new Map();
  calls = [];
  before = () => null;
  etag(value) { return '"' + crypto.createHash('sha256').update(value).digest('hex') + '"'; }
  handle(call) {
    this.calls.push(call);
    const override = this.before(call, this);
    if (override) return override;
    const current = this.objects.get(call.path);
    if (call.method === 'GET') return current === undefined ? {status: 404, body: '<Error><Code>NoSuchKey</Code></Error>'}
      : {status: 200, body: current, headers: {etag: this.etag(current)}};
    if (call.headers['If-Match'] && (current === undefined || call.headers['If-Match'] !== this.etag(current)) ||
        call.headers['If-None-Match'] === '*' && current !== undefined) return {status: 412};
    if (call.method === 'DELETE') this.objects.delete(call.path);
    else this.objects.set(call.path, call.body);
    return {status: 200};
  }
}

async function runUpload({home, bundle}, bucket, args = ['--setup', '--confirm-shared-writes']) {
  const output = [];
  const fakeHttps = {
    Agent: class { destroy() {} },
    request(options, callback) {
      const listeners = {};
      const req = {
        on(name, fn) { listeners[name] = fn; return req; },
        destroy(error) { listeners.error?.(error); },
        end(payload) {
          Promise.resolve().then(() => bucket.handle({method: options.method, path: options.path,
            body: payload ? Buffer.from(payload).toString('utf8') : '', headers: options.headers})).then(result => {
            const handlers = {};
            const res = {statusCode: result.status, headers: result.headers || {}, on(name, fn) { handlers[name] = fn; return res; }};
            callback(res);
            queueMicrotask(() => { handlers.data?.(Buffer.from(result.body || '')); handlers.end?.(); });
          }).catch(error => listeners.error?.(error));
        },
      };
      return req;
    },
  };
  const file = path.join(bundle, 'upload.js');
  const sandbox = {Buffer, Promise, Date, setTimeout, encodeURIComponent, console: {
    log: (...parts) => output.push(parts.join(' ')), error: (...parts) => output.push(parts.join(' ')),
  }, module: {exports: {}}, __dirname: bundle,
  process: {argv: ['node', file, ...args], platform: process.platform, env: {}, exitCode: 0, exit(code) { throw new Error('exit ' + code); }},
  require(id) {
    if (id === 'node:https') return fakeHttps;
    if (id === 'node:os') return {...os, homedir: () => home};
    return require(id);
  }};
  sandbox.require.main = sandbox.module;
  vm.runInNewContext(fs.readFileSync(path.join(skill, 'upload.js'), 'utf8'), sandbox, {filename: file});
  await sandbox.completion;
  return {status: sandbox.process.exitCode, output: output.join('\n')};
}

test('upgrades retain immutable assets for cached pages and detect another client replacing the viewer', async t => {
  const a = workspace(t), b = workspace(t), bucket = new Bucket();
  assert.equal((await runUpload(a, bucket)).status, 0);
  const oldHtml = bucket.objects.get('/b/index.html');
  const oldAssets = [...oldHtml.matchAll(/(?:src|href)="(assets\/[^"?]+)"/g)].map(match => match[1]);
  assert.ok(oldAssets.length > 5);
  const oldBytes = oldAssets.map(key => bucket.objects.get('/b/' + key));
  assert.ok(oldBytes.every(value => value !== undefined));
  fs.appendFileSync(path.join(b.bundle, 'docsify-server/assets/config.js'), '\n// another viewer version');
  assert.equal((await runUpload(b, bucket)).status, 0);
  assert.notEqual(bucket.objects.get('/b/index.html'), oldHtml);
  assert.deepEqual(oldAssets.map(key => bucket.objects.get('/b/' + key)), oldBytes);
  const before = bucket.calls.length;
  const refused = await runUpload(a, bucket, [path.join(a.home, 'doc.md'), 'guide']);
  assert.equal(refused.status, 1);
  assert.match(refused.output, /SETUP_REQUIRED/);
  assert.ok(bucket.calls.slice(before).every(call => call.method === 'GET'));
  const published = await runUpload(b, bucket, [path.join(b.home, 'doc.md'), 'guide']);
  assert.equal(published.status, 0, published.output);
  assert.match(published.output.split('\n').at(-1), /^https:\/\/public.invalid\/prefix\/index.html#\/md-web\/\d{8}-\d{6}-guide-[a-f0-9]{4}$/);
  const writes = bucket.calls.slice(before).filter(call => call.method !== 'GET');
  assert.equal(writes.length, 1);
  assert.match(writes[0].path, /^\/b\/md-web\//);
  assert.equal(writes[0].body, fs.readFileSync(path.join(b.home, 'doc.md'), 'utf8'));
  assert.ok(bucket.calls.filter(call => /\/assets\//.test(call.path)).every(call => /immutable/.test(call.headers['Cache-Control'])));
});

test('deployment snapshots cannot mix bytes from a concurrent local Skill upgrade', t => {
  const a = workspace(t);
  const helpers = createPublishHelpers(a.bundle);
  const first = helpers.createViewerDeployment();
  const key = 'assets/' + first.hash + '/config.js';
  const contents = first.files.find(file => file.key === key).payload.toString();
  fs.appendFileSync(path.join(a.bundle, 'docsify-server/assets/config.js'), '\n// installed upgrade');
  assert.equal(first.files.find(file => file.key === key).payload.toString(), contents);
  assert.notEqual(helpers.createViewerDeployment().hash, first.hash);
});

test('a failed asset upload leaves the entry point and local deployment hint intact', async t => {
  const a = workspace(t), bucket = new Bucket();
  assert.equal((await runUpload(a, bucket)).status, 0);
  const index = bucket.objects.get('/b/index.html');
  const flag = fs.readFileSync(path.join(a.home, '.md-web/.deployed'), 'utf8');
  fs.appendFileSync(path.join(a.bundle, 'docsify-server/assets/config.js'), '\n// new build');
  bucket.before = call => call.path.endsWith('/config.js') ? {status: 403} : null;
  const start = bucket.calls.length;
  const run = await runUpload(a, bucket);
  assert.equal(run.status, 1);
  assert.equal(bucket.objects.get('/b/index.html'), index);
  assert.equal(fs.readFileSync(path.join(a.home, '.md-web/.deployed'), 'utf8'), flag);
  assert.ok(!bucket.calls.slice(start).some(call => call.path === '/b/index.html' && call.method === 'PUT'));
});

test('concurrent first setups and upgrades cannot both replace the shared entry point', async t => {
  for (const existing of [false, true]) {
    const a = workspace(t), b = workspace(t), bucket = new Bucket();
    if (existing) bucket.objects.set('/b/index.html', 'legacy viewer');
    fs.appendFileSync(path.join(b.bundle, 'docsify-server/assets/config.js'), '\n// second client');
    const results = await Promise.all([runUpload(a, bucket), runUpload(b, bucket)]);
    assert.deepEqual(results.map(result => result.status).sort(), [0, 1]);
    assert.match(results.find(result => result.status === 1).output, /SETUP_CONFLICT/);
    const puts = bucket.calls.filter(call => call.method === 'PUT' && call.path === '/b/index.html');
    assert.equal(puts.length, 2);
    assert.ok(puts.every(call => existing ? call.headers['If-Match'] : call.headers['If-None-Match'] === '*'));
    assert.ok(puts.every(call => call.headers.Authorization.includes(existing ? 'if-match' : 'if-none-match')));
  }
});

test('missing ETags, denied reads and remote deletion never silently overwrite or publish', async t => {
  const a = workspace(t), bucket = new Bucket();
  bucket.before = call => call.method === 'GET' ? {status: 200, body: 'old viewer'} : null;
  assert.match((await runUpload(a, bucket)).output, /SETUP_CONFLICT/);
  assert.ok(bucket.calls.every(call => call.method === 'GET'));
  bucket.before = () => null;
  assert.equal((await runUpload(a, bucket)).status, 0);
  for (const status of [403, 404]) {
    bucket.before = call => call.method === 'GET' ? {status, body: '<Error><Code>AccessDenied</Code></Error>'} : null;
    const start = bucket.calls.length;
    const run = await runUpload(a, bucket, [path.join(a.home, 'doc.md'), 'guide']);
    assert.equal(run.status, 1);
    assert.match(run.output, status === 403 ? /AccessDenied/ : /SETUP_REQUIRED/);
    assert.ok(bucket.calls.slice(start).every(call => call.method === 'GET'));
  }
});

test('conditional-write rejection has no unconditional fallback or local success marker', async t => {
  for (const status of [400, 409, 412]) {
    const a = workspace(t), bucket = new Bucket();
    bucket.before = call => call.method === 'PUT' && call.path === '/b/index.html' ? {status} : null;
    const run = await runUpload(a, bucket);
    assert.equal(run.status, 1);
    assert.match(run.output, status === 400 ? /HTTP 400/ : /SETUP_CONFLICT/);
    assert.equal(bucket.calls.filter(call => call.method === 'PUT' && call.path === '/b/index.html').length, 1);
    assert.equal(fs.existsSync(path.join(a.home, '.md-web/.deployed')), false);
    assert.equal(bucket.objects.has('/b/index.html'), false);
  }
});

test('lifecycle XML preserves unrelated rules, settings, comments and root attributes', () => {
  const extra = '<TransitionDefaultMinimumObjectSize>all_storage_classes_128K</TransitionDefaultMinimumObjectSize>';
  const comment = '<!-- <Rule><ID>md-web-auto-expire</ID></Rule> -->';
  const anonymous = '<Rule><Prefix>anonymous/</Prefix><Status>Enabled</Status></Rule>';
  const parsed = parseLifecycleConfiguration(lifecycle(comment + extra + userRule + ownRule + anonymous).replace('xmlns=', 'data-owner="fixture" xmlns='));
  assert.deepEqual(parsed.rules, [userRule, anonymous]);
  assert.equal(parsed.extras, comment + extra);
  assert.match(parsed.opening, /data-owner="fixture"/);
  for (const invalid of ['<LifecycleConfiguration><Rule>', lifecycle(ownRule).slice(0, -1),
    '<s3:LifecycleConfiguration xmlns:s3="urn:test"/>', lifecycle(ownRule.replace('md-web/', 'backups/')),
    lifecycle(ownRule + ownRule), '<!DOCTYPE x><LifecycleConfiguration/>']) {
    assert.throws(() => parseLifecycleConfiguration(invalid));
  }
});

test('lifecycle edits between reads are detected without writing the stale configuration', async t => {
  const a = workspace(t), bucket = new Bucket();
  fs.writeFileSync(path.join(a.home, '.md-web/config.json'), JSON.stringify({...config, expire_days: 30}));
  let reads = 0;
  bucket.before = call => call.path.includes('?lifecycle') && call.method === 'GET'
    ? {status: 200, body: lifecycle(userRule + (reads++ ? ownRule : ''))} : null;
  const run = await runUpload(a, bucket);
  assert.equal(run.status, 0); // Existing warning-only retention failure behavior.
  assert.match(run.output, /Warning: lifecycle.*changed during setup/);
  assert.ok(!bucket.calls.some(call => call.path.includes('?lifecycle') && call.method !== 'GET'));
});

test('malformed policy responses and conflicting rule ownership never trigger policy writes', async t => {
  for (const body of ['<LifecycleConfiguration><Rule>', lifecycle(ownRule.replace('md-web/', 'backups/')),
    '<s3:LifecycleConfiguration xmlns:s3="urn:test"/>']) {
    const a = workspace(t), bucket = new Bucket();
    fs.writeFileSync(path.join(a.home, '.md-web/config.json'), JSON.stringify({...config, expire_days: 30}));
    bucket.before = call => call.path.includes('?lifecycle') ? {status: 200, body} : null;
    const run = await runUpload(a, bucket);
    assert.equal(run.status, 0);
    assert.match(run.output, /Warning: lifecycle/);
    assert.ok(!bucket.calls.some(call => call.path.includes('?lifecycle') && call.method !== 'GET'));
  }
});

test('a failed bucket policy write is warned once rather than replayed over later edits', async t => {
  const a = workspace(t), bucket = new Bucket();
  fs.writeFileSync(path.join(a.home, '.md-web/config.json'), JSON.stringify({...config, expire_days: 30}));
  bucket.before = call => call.path.includes('?lifecycle') ? call.method === 'GET'
    ? {status: 200, body: lifecycle(userRule)} : {status: 500, body: 'uncertain result'} : null;
  const run = await runUpload(a, bucket);
  assert.equal(run.status, 0);
  assert.match(run.output, /Warning: lifecycle/);
  assert.equal(bucket.calls.filter(call => call.path.includes('?lifecycle') && call.method === 'PUT').length, 1);
});
