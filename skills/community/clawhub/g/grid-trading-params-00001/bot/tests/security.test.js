const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const root = path.resolve(__dirname, '..');
const port = 33030 + Math.floor(Math.random() * 1000);
const base = `http://127.0.0.1:${port}`;
const configPath = path.join(root, 'config.json');

function waitForExit(child) {
  return new Promise((resolve) => child.once('exit', resolve));
}

async function waitForServer() {
  let lastError;
  for (let attempt = 0; attempt < 60; attempt += 1) {
    try {
      const response = await fetch(`${base}/api/config`);
      if (response.ok) return;
    } catch (error) {
      lastError = error;
    }
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw lastError || new Error('Server did not start.');
}

async function json(pathname, init) {
  const response = await fetch(`${base}${pathname}`, init);
  return { response, body: await response.json() };
}

async function main() {
  const child = spawn(process.execPath, ['server.js'], {
    cwd: root,
    env: { ...process.env, PORT: String(port) },
    stdio: ['ignore', 'pipe', 'pipe']
  });
  let stderr = '';
  child.stderr.on('data', (chunk) => {
    stderr += chunk.toString();
  });

  try {
    await waitForServer();

    const initial = await json('/api/config');
    assert.equal(initial.response.status, 200);
    assert.equal(initial.body.paper, true);
    assert.equal(initial.body.apiKey, '');
    assert.equal(initial.body.apiSecret, '');
    assert.equal(initial.body.credentialsStored, false);
    assert.equal(initial.response.headers.get('access-control-allow-origin'), null);

    const liveAttempt = await json('/api/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        exchangeId: 'binance',
        apiKey: 'demo-key-value',
        apiSecret: 'demo-secret-value',
        paper: false,
        strategyParams: 'symbol=BTC/USDT'
      })
    });
    assert.equal(liveAttempt.response.status, 400);
    assert.match(liveAttempt.body.error, /demo\/sandbox/i);

    const saveAttempt = await json('/api/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        exchangeId: 'binance',
        apiKey: 'demo-key-value',
        apiSecret: 'demo-secret-value',
        passphrase: 'demo-passphrase-value',
        paper: true,
        strategyParams:
          'symbol=BTC/USDT\n' +
          'gridLevels=5\n' +
          'rangePercent=5\n' +
          'amountPerOrder=0.001\n' +
          'intervalMs=60000'
      })
    });
    assert.equal(saveAttempt.response.status, 200);
    assert.equal(saveAttempt.body.credentialsStored, false);

    const savedText = fs.readFileSync(configPath, 'utf8');
    assert(!savedText.includes('demo-key-value'));
    assert(!savedText.includes('demo-secret-value'));
    assert(!savedText.includes('demo-passphrase-value'));
    assert.equal(fs.statSync(configPath).mode & 0o777, 0o600);

    const afterSave = await json('/api/config');
    assert.equal(afterSave.body.apiKey, '');
    assert.equal(afterSave.body.apiSecret, '');
    assert.equal(afterSave.body.passphrase, '');

    const status = await json('/api/strategy/status');
    assert.equal(status.response.status, 200);
    assert.equal(status.body.running, false);
    assert.equal(status.body.paper, true);
  } finally {
    child.kill('SIGTERM');
    await waitForExit(child);
    if (fs.existsSync(configPath)) fs.unlinkSync(configPath);
  }

  if (stderr) {
    throw new Error(`Server wrote unexpected stderr:\n${stderr}`);
  }
  console.log('security tests passed');
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
