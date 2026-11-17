import test from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';
import net from 'node:net';
import { Readable } from 'node:stream';
import { promises as fs } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createMagBox, configFromEnv } from '../scripts/magbox-server.mjs';

const packageDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

function multipart(files, boundary = 'magbox-test-boundary') {
  const buffers = [];
  for (const [name, data] of files) {
    buffers.push(Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${name}"\r\nContent-Type: application/octet-stream\r\n\r\n`));
    buffers.push(Buffer.isBuffer(data) ? data : Buffer.from(data));
    buffers.push(Buffer.from('\r\n'));
  }
  buffers.push(Buffer.from(`--${boundary}--\r\n`));
  return Buffer.concat(buffers);
}

async function fixture(t, overrides = {}) {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), 'magbox-test-'));
  const config = configFromEnv({ MAGBOX_PORT: '0', MAGBOX_TO_AGENT: path.join(dir, 'in'), MAGBOX_FROM_AGENT: path.join(dir, 'out'), ...overrides });
  const server = await createMagBox(config);
  await new Promise((resolve, reject) => { server.once('error', reject); server.listen(config.port, config.bind, resolve); });
  t.after(async () => {
    await new Promise(resolve => { server.close(resolve); server.closeAllConnections(); });
    await fs.rm(dir, { recursive: true, force: true });
  });
  const port = server.address().port;
  const request = (url, { method = 'GET', headers = {}, body, feed } = {}) => new Promise((resolve, reject) => {
    const req = http.request({ hostname: '127.0.0.1', port, path: url, method, headers, agent: false }, res => {
      const chunks = [];
      res.on('data', chunk => chunks.push(chunk));
      res.on('error', reject);
      res.on('end', () => {
        const data = Buffer.concat(chunks);
        resolve({ status: res.statusCode, headers: res.headers, data, text: data.toString(), json: () => JSON.parse(data.toString()) });
      });
    });
    req.on('error', reject);
    if (feed) feed(req);
    else req.end(body);
  });
  const upload = (files, options = {}) => {
    const boundary = options.boundary || 'magbox-test-boundary';
    return request('/api/to', { method: 'POST', headers: { 'Content-Type': `multipart/form-data; boundary="${boundary}"`, ...options.headers }, body: multipart(files, boundary) });
  };
  return { dir, config, server, port, request, upload };
}

// The suites stay sequential so fault-injection of filesystem failures is local.
test('download boundaries, nonregular files, ranges, and response headers', async t => {
  const f = await fixture(t);
  const content = Buffer.from('0123456789');
  await fs.writeFile(path.join(f.config.fromDir, 'clip.mp4'), content);
  await fs.writeFile(path.join(f.config.fromDir, 'empty.txt'), '');
  await fs.writeFile(path.join(f.dir, 'private.txt'), 'outside');
  await fs.symlink(path.join(f.dir, 'private.txt'), path.join(f.config.fromDir, 'link.txt'));
  await fs.mkdir(path.join(f.config.fromDir, 'directory'));
  const socket = net.createServer();
  await new Promise(resolve => socket.listen(path.join(f.config.fromDir, 'socket'), resolve));
  t.after(() => new Promise(resolve => socket.close(resolve)));
  const list = (await f.request('/api/from')).json();
  assert.deepEqual(list.files.map(file => file.name).sort(), ['clip.mp4', 'empty.txt']);
  assert.equal(list.count, 2); assert.equal(list.totalBytes, 10);
  for (const url of ['/dl/from/link.txt', '/dl/from/directory', '/dl/from/socket']) assert.equal((await f.request(url)).status, 403);
  for (const url of ['/dl/from/%ZZ', '/dl/from/%2e%2e%2fprivate.txt', '/dl/from/%00', '/dl/from/%5cprivate.txt']) assert.equal((await f.request(url)).status, 400);
  assert.equal((await f.request('/dl/from/missing')).status, 404);
  assert.equal((await f.request('/dl/from/clip.mp4?download=1')).text, content.toString());
  for (const [range, expected] of [['bytes=2-4', '234'], ['bytes=7-', '789'], ['bytes=-3', '789'], ['bytes=-99', '0123456789'], ['bytes=8-99', '89']]) {
    const response = await f.request('/dl/from/clip.mp4', { headers: { Range: range } });
    assert.equal(response.status, 206); assert.equal(response.text, expected);
    assert.equal(Number(response.headers['content-length']), expected.length);
  }
  for (const range of ['oops', 'bytes=', 'bytes=-', 'bytes=-0', 'bytes=10-', 'bytes=8-2', 'bytes=0-1,3-4', 'bytes=999999999999999999999-']) {
    const response = await f.request('/dl/from/clip.mp4', { headers: { Range: range } });
    assert.equal(response.status, 416); assert.equal(response.headers['content-range'], 'bytes */10');
  }
  assert.equal((await f.request('/dl/from/empty.txt', { headers: { Range: 'bytes=0-' } })).status, 416);
  const head = await f.request('/dl/from/clip.mp4', { method: 'HEAD', headers: { Range: 'malformed' } });
  assert.equal(head.status, 200); assert.equal(head.data.length, 0); assert.equal(head.headers['content-length'], '10');
  await fs.writeFile(path.join(f.config.fromDir, 'active.svg'), '<svg onload="alert(1)"></svg>');
  const svg = await f.request('/dl/from/active.svg');
  assert.equal(svg.headers['content-type'], 'application/octet-stream');
  assert.match(svg.headers['content-disposition'], /^attachment;/);
  assert.match(svg.headers['content-security-policy'], /sandbox/);
  assert.equal(svg.headers['x-content-type-options'], 'nosniff');
  assert.equal((await f.request('/api/from')).status, 200, 'malformed input leaves the server alive');
});

test('quoted multipart boundaries preserve binary data and reject malformed envelopes', async t => {
  const f = await fixture(t);
  const boundary = 'test:boundary';
  const binary = Buffer.concat([Buffer.from([0, 255, 128]), Buffer.from(`\r\n--${boundary}-not-a-delimiter\r\n--${boundary}--not-an-ending\r\n`), Buffer.from([255, 0])]);
  const response = await f.upload([['binary.bin', binary]], { boundary });
  assert.equal(response.status, 200);
  assert.deepEqual(await fs.readFile(path.join(f.config.toDir, 'binary.bin')), binary);
  for (const body of [Buffer.from('nonsense'), multipart([['bad.txt', 'abc']]).subarray(0, -7)]) {
    assert.equal((await f.request('/api/to', { method: 'POST', headers: { 'Content-Type': 'multipart/form-data; boundary=magbox-test-boundary' }, body })).status, 400);
  }
  for (const name of ['', '.', '..', 'a'.repeat(201), '.magbox-internal']) assert.equal((await f.upload([[name, 'x']])).status, 400);
  assert.equal((await f.upload(Array.from({ length: 9 }, (_, i) => [`part${i}`, 'x']))).status, 413);
  assert.equal((await f.request('/api/to', { method: 'POST', headers: { 'Content-Type': 'text/plain' }, body: 'x' })).status, 400);
  assert.deepEqual(await fs.readdir(f.config.toDir), ['binary.bin']);
});

test('exclusive creation versions concurrent and sanitized collisions without touching symlinks', async t => {
  const f = await fixture(t, { MAGBOX_MAX_UPLOADS: '8' });
  await fs.writeFile(path.join(f.config.toDir, 'report.txt'), 'original');
  const uploads = await Promise.all(Array.from({ length: 6 }, (_, i) => f.upload([['report.txt', `payload-${i}`]])));
  assert.ok(uploads.every(res => res.status === 200));
  const names = uploads.map(res => res.json().saved[0].name);
  assert.equal(new Set(names).size, 6);
  assert.deepEqual([...names].sort(), Array.from({ length: 6 }, (_, i) => `report-v${i + 2}.txt`));
  assert.equal(await fs.readFile(path.join(f.config.toDir, 'report.txt'), 'utf8'), 'original');
  for (const [i, name] of names.entries()) assert.equal(await fs.readFile(path.join(f.config.toDir, name), 'utf8'), `payload-${i}`);
  assert.equal((await f.upload([['a b.txt', 'one']])).json().saved[0].name, 'a_b.txt');
  assert.equal((await f.upload([['a?b.txt', 'two']])).json().saved[0].name, 'a_b-v2.txt');
  await fs.writeFile(path.join(f.dir, 'outside'), 'untouched');
  await fs.symlink(path.join(f.dir, 'outside'), path.join(f.config.toDir, 'symlink.txt'));
  assert.equal((await f.upload([['symlink.txt', 'new']])).json().saved[0].name, 'symlink-v2.txt');
  assert.equal(await fs.readFile(path.join(f.dir, 'outside'), 'utf8'), 'untouched');
  assert.equal((await f.request('/dl/to/symlink.txt')).status, 403);
  assert.ok(!(await f.request('/api/to/list')).json().files.some(file => file.name === 'symlink.txt'));
  assert.equal((await f.request('/api/to', { method: 'DELETE' })).status, 404);
});

test('Host and Origin checks reject foreign browser writes without affecting same-origin uploads', async t => {
  const f = await fixture(t);
  assert.equal((await f.request('/', { headers: { Host: `rebound.example:${f.port}` } })).status, 403);
  assert.equal((await f.request('/', { headers: { Host: '127.0.0.1:1' } })).status, 403);
  for (const origin of ['null', 'https://foreign.example', `http://localhost:${f.port}`]) {
    assert.equal((await f.upload([['blocked.txt', 'x']], { headers: { Origin: origin } })).status, 403);
  }
  assert.equal((await f.upload([['blocked.txt', 'x']], { headers: { 'Sec-Fetch-Site': 'cross-site' } })).status, 403);
  assert.equal((await f.upload([['allowed.txt', 'x']], { headers: { Origin: `http://127.0.0.1:${f.port}`, 'Sec-Fetch-Site': 'same-origin' } })).status, 200);
  assert.equal((await f.upload([['curl.txt', 'x']])).status, 200);
  assert.deepEqual((await fs.readdir(f.config.toDir)).sort(), ['allowed.txt', 'curl.txt']);
});

test('byte limits, receive timeout, concurrency cap, and aborted bodies release capacity', async t => {
  const f = await fixture(t, { MAGBOX_MAX_BYTES: '512', MAGBOX_MAX_UPLOADS: '1', MAGBOX_UPLOAD_TIMEOUT_MS: '180' });
  assert.equal((await f.upload([['large.txt', 'x'.repeat(600)]])).status, 413);
  assert.equal((await f.request('/api/to', { method: 'POST', headers: { 'Content-Type': 'multipart/form-data; boundary=x', 'Content-Length': '999' }, feed: req => req.flushHeaders() })).status, 413);
  const pending = f.request('/api/to', { method: 'POST', headers: { 'Content-Type': 'multipart/form-data; boundary=x' }, feed: req => req.write('--x\r\n') });
  await new Promise(resolve => setTimeout(resolve, 25));
  assert.equal((await f.upload([['busy.txt', 'x']])).status, 429);
  assert.equal((await pending).status, 408);
  const aborted = http.request({ hostname: '127.0.0.1', port: f.port, path: '/api/to', method: 'POST', headers: { 'Content-Type': 'multipart/form-data; boundary=x' } });
  aborted.on('error', () => {}); aborted.write('--x\r\n');
  await new Promise(resolve => setTimeout(resolve, 25)); aborted.destroy();
  await new Promise(resolve => setTimeout(resolve, 25));
  assert.equal((await f.upload([['small.txt', 'ok']])).status, 200);
  assert.deepEqual(await fs.readdir(f.config.toDir), ['small.txt']);
});

test('disk errors roll back partial files, and replaced roots fail closed', async t => {
  const f = await fixture(t);
  const originalOpen = fs.open;
  fs.open = async (...args) => {
    const handle = await originalOpen(...args);
    if (args[1] === 'wx' && path.basename(args[0]) === 'disk-full.txt') {
      const write = handle.writeFile.bind(handle);
      handle.writeFile = async data => { await write(data.subarray(0, 1)); const error = new Error('simulated full disk'); error.code = 'ENOSPC'; throw error; };
    }
    return handle;
  };
  try {
    assert.equal((await f.upload([['rollback.txt', 'one'], ['disk-full.txt', 'two']])).status, 507);
    assert.deepEqual(await fs.readdir(f.config.toDir), []);
  } finally { fs.open = originalOpen; }
  await fs.rename(f.config.toDir, path.join(f.dir, 'old-in'));
  await fs.symlink(f.config.fromDir, f.config.toDir);
  assert.equal((await f.upload([['outside.txt', 'no']])).status, 409);
  assert.deepEqual(await fs.readdir(f.config.fromDir), []);
});

test('generated pages use nonce policies and safe filename rendering; service defaults match CLI', async t => {
  const f = await fixture(t);
  const hostile = '<img src=x onerror=alert(1)>.txt';
  await fs.writeFile(path.join(f.config.fromDir, hostile), 'safe bytes');
  assert.equal((await f.request(`/dl/from/${encodeURIComponent(hostile)}`)).text, 'safe bytes');
  assert.equal((await f.request('/api/from')).json().files[0].name, hostile);
  for (const url of ['/', '/to']) {
    const response = await f.request(url);
    assert.equal(response.status, 200);
    const nonce = response.text.match(/<script nonce="([^"]+)"/)[1];
    assert.ok(response.headers['content-security-policy'].includes(`'nonce-${nonce}'`));
    assert.ok(!response.text.includes('innerHTML'));
    assert.ok(!response.text.includes(hostile));
    assert.ok(response.text.includes('textContent'));
    assert.ok(response.text.includes('totalBytes'));
  }
  const defaults = configFromEnv({});
  assert.equal(defaults.bind, '127.0.0.1'); assert.equal(defaults.port, 9900);
  assert.throws(() => configFromEnv({ MAGBOX_BIND: '0.0.0.0' }));
  assert.throws(() => configFromEnv({ MAGBOX_MAX_BYTES: 'no' }));
  assert.throws(() => configFromEnv({ MAGBOX_HOSTS: 'bad.example/path' }));
  const lan = configFromEnv({ MAGBOX_BIND: '0.0.0.0', MAGBOX_HOSTS: 'agent.local' });
  assert.equal(lan.advertisedHost, 'agent.local');
  const plist = await fs.readFile(path.join(packageDir, 'templates/magbox.plist'), 'utf8');
  assert.match(plist, /<key>MAGBOX_BIND<\/key><string>127\.0\.0\.1<\/string>/);
  assert.match(plist, /magbox-server\.mjs/);
  const service = await fs.readFile(path.join(packageDir, 'templates/magbox.service'), 'utf8');
  assert.match(service, /^ExecStart=\/usr\/bin\/node \/ABSOLUTE\/PATH\/TO\/magbox-server\.mjs$/m);
  assert.match(service, /^Environment=MAGBOX_BIND=127\.0\.0\.1$/m);
  assert.match(service, /^WantedBy=default\.target$/m);
  assert.ok(!/^User=root$/m.test(service));
});

test('a download stream failure closes its descriptor and a symlink swap cannot escape', async t => {
  const f = await fixture(t);
  await fs.writeFile(path.join(f.config.fromDir, 'broken.txt'), 'data');
  await fs.writeFile(path.join(f.config.fromDir, 'swap.txt'), 'data');
  await fs.writeFile(path.join(f.dir, 'outside.txt'), 'private');
  const originalOpen = fs.open;
  let openedHandle;
  fs.open = async (...args) => {
    if (path.basename(args[0]) === 'swap.txt') {
      await fs.rename(args[0], path.join(f.dir, 'original.txt'));
      await fs.symlink(path.join(f.dir, 'outside.txt'), args[0]);
    }
    const handle = await originalOpen(...args);
    if (path.basename(args[0]) === 'broken.txt') {
      openedHandle = handle;
      handle.createReadStream = () => new Readable({ read() { this.destroy(new Error('simulated read failure')); } });
    }
    return handle;
  };
  try {
    await assert.rejects(f.request('/dl/from/broken.txt'));
    assert.equal((await f.request('/dl/from/swap.txt')).status, 403);
    assert.equal((await f.request('/')).status, 200);
    assert.equal(openedHandle.fd, -1);
  } finally { fs.open = originalOpen; }
});

test('a disconnect during saving removes partial files and pending files stay hidden', async t => {
  const f = await fixture(t);
  const originalOpen = fs.open;
  let unlock;
  let entered;
  const gate = new Promise(resolve => { unlock = resolve; });
  const saving = new Promise(resolve => { entered = resolve; });
  fs.open = async (...args) => {
    const handle = await originalOpen(...args);
    if (args[1] === 'wx' && path.basename(args[0]) === 'pending.txt') {
      const write = handle.writeFile.bind(handle);
      handle.writeFile = async data => { await write(data); entered(); await gate; };
    }
    return handle;
  };
  let connection;
  const result = f.request('/api/to', {
    method: 'POST', headers: { 'Content-Type': 'multipart/form-data; boundary=magbox-test-boundary' },
    feed: req => { connection = req; req.end(multipart([['pending.txt', 'partial']])); },
  }).catch(() => null);
  try {
    await saving;
    assert.equal((await f.request('/api/to/list')).json().count, 0);
    assert.equal((await f.request('/dl/to/pending.txt')).status, 409);
    connection.destroy();
    await result;
    await new Promise(resolve => setTimeout(resolve, 20));
    unlock();
    for (let attempt = 0; attempt < 50; attempt++) {
      if (!(await fs.readdir(f.config.toDir)).length) break;
      await new Promise(resolve => setTimeout(resolve, 10));
    }
    assert.deepEqual(await fs.readdir(f.config.toDir), []);
    assert.equal((await f.upload([['after.txt', 'ok']])).status, 200);
  } finally { unlock(); fs.open = originalOpen; }
});
