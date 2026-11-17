/**
 * Local-only demo grid trading server.
 *
 * Security properties:
 * - binds only to 127.0.0.1;
 * - accepts demo/sandbox mode only;
 * - keeps exchange credentials in memory and never writes them to config.json;
 * - does not enable CORS;
 * - exposes only the bundled static UI and a small same-origin JSON API.
 */
require('dotenv').config();

const fs = require('fs');
const path = require('path');
const express = require('express');
const ccxt = require('ccxt');
const strategy = require('./strategy');

const proxy = process.env.HTTPS_PROXY || process.env.HTTP_PROXY;
if (proxy && proxy.trim()) {
  try {
    const { setGlobalDispatcher, ProxyAgent } = require('undici');
    setGlobalDispatcher(new ProxyAgent(proxy.trim()));
  } catch (error) {
    console.warn('[proxy] ProxyAgent was not applied:', error.message);
  }
}

const HOST = '127.0.0.1';
const PORT = Number.parseInt(process.env.PORT || '3030', 10);
const CONFIG_PATH = path.join(__dirname, 'config.json');
const ALLOWED_EXCHANGES = new Set(['binance', 'okx', 'bitget', 'gateio']);

const defaultPublicConfig = {
  exchangeId: 'binance',
  paper: true,
  paperMode: 'demo',
  strategyParams:
    'symbol=BTC/USDT\n' +
    'gridLevels=5\n' +
    'rangePercent=5\n' +
    'amountPerOrder=0.001\n' +
    'intervalMs=60000'
};

function readPublicConfig() {
  try {
    const value = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    return {
      ...defaultPublicConfig,
      exchangeId: ALLOWED_EXCHANGES.has(value.exchangeId)
        ? value.exchangeId
        : defaultPublicConfig.exchangeId,
      paper: true,
      paperMode: 'demo',
      strategyParams:
        typeof value.strategyParams === 'string'
          ? value.strategyParams
          : defaultPublicConfig.strategyParams
    };
  } catch (_) {
    return { ...defaultPublicConfig };
  }
}

function writePublicConfig(config) {
  const publicConfig = {
    exchangeId: config.exchangeId,
    paper: true,
    paperMode: 'demo',
    strategyParams: config.strategyParams
  };
  fs.writeFileSync(CONFIG_PATH, `${JSON.stringify(publicConfig, null, 2)}\n`, {
    encoding: 'utf8',
    mode: 0o600
  });
  fs.chmodSync(CONFIG_PATH, 0o600);
}

function validatePayload(body) {
  if (!body || typeof body !== 'object') {
    throw new Error('Configuration must be a JSON object.');
  }
  if (!ALLOWED_EXCHANGES.has(body.exchangeId)) {
    throw new Error('Unsupported exchange.');
  }
  if (body.paper === false) {
    throw new Error('This marketplace build supports demo/sandbox trading only.');
  }
  if (typeof body.strategyParams !== 'string' || body.strategyParams.length > 20_000) {
    throw new Error('Strategy parameters must be text under 20 KB.');
  }
  const parsed = strategy.getParams({ strategyParams: body.strategyParams });
  if (
    !Number.isFinite(parsed.amountPerOrder) ||
    parsed.amountPerOrder <= 0 ||
    !Number.isFinite(parsed.intervalMs) ||
    parsed.intervalMs < 10_000
  ) {
    throw new Error('Invalid amountPerOrder or intervalMs.');
  }
  if (
    parsed.lowerPrice !== null &&
    parsed.upperPrice !== null &&
    parsed.upperPrice <= parsed.lowerPrice
  ) {
    throw new Error('upperPrice must be greater than lowerPrice.');
  }
  return {
    exchangeId: body.exchangeId,
    apiKey: typeof body.apiKey === 'string' ? body.apiKey.trim() : '',
    apiSecret: typeof body.apiSecret === 'string' ? body.apiSecret.trim() : '',
    passphrase: typeof body.passphrase === 'string' ? body.passphrase.trim() : '',
    paper: true,
    paperMode: 'demo',
    strategyParams: body.strategyParams
  };
}

function createExchange(config) {
  if (!config.apiKey || !config.apiSecret) {
    throw new Error('Enter demo/sandbox API credentials in the local page.');
  }
  const Exchange = ccxt[config.exchangeId];
  if (typeof Exchange !== 'function') {
    throw new Error('Exchange adapter is unavailable.');
  }
  const exchange = new Exchange({
    apiKey: config.apiKey,
    secret: config.apiSecret,
    password: config.passphrase || undefined,
    enableRateLimit: true,
    options: { defaultType: 'spot' }
  });
  if (typeof exchange.setSandboxMode !== 'function') {
    throw new Error('The selected exchange does not expose sandbox mode in this CCXT build.');
  }
  exchange.setSandboxMode(true);
  return exchange;
}

let memoryConfig = { ...readPublicConfig(), apiKey: '', apiSecret: '', passphrase: '' };
let running = false;
let abortState = null;
let lastActivity = null;

const app = express();
app.disable('x-powered-by');
app.use((request, response, next) => {
  response.setHeader('X-Content-Type-Options', 'nosniff');
  response.setHeader('X-Frame-Options', 'DENY');
  response.setHeader('Referrer-Policy', 'no-referrer');
  response.setHeader(
    'Content-Security-Policy',
    "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'"
  );
  next();
});
app.use(express.json({ limit: '64kb', type: 'application/json' }));

app.get('/api/config', (_request, response) => {
  response.setHeader('Cache-Control', 'no-store');
  response.json({
    exchangeId: memoryConfig.exchangeId,
    apiKey: '',
    apiSecret: '',
    passphrase: '',
    paper: true,
    paperMode: 'demo',
    strategyParams: memoryConfig.strategyParams,
    credentialsStored: false
  });
});

app.post('/api/config', (request, response) => {
  try {
    memoryConfig = validatePayload(request.body);
    writePublicConfig(memoryConfig);
    response.json({ ok: true, credentialsStored: false, paper: true });
  } catch (error) {
    response.status(400).json({ error: error.message });
  }
});

app.get('/api/strategy/status', (_request, response) => {
  response.setHeader('Cache-Control', 'no-store');
  response.json({ running, lastActivity, paper: true });
});

app.post('/api/strategy/start', async (_request, response) => {
  if (running) {
    response.status(409).json({ error: 'Strategy is already running.' });
    return;
  }
  try {
    const exchange = createExchange(memoryConfig);
    running = true;
    abortState = { aborted: false };
    lastActivity = { action: 'starting', at: new Date().toISOString() };
    response.status(202).json({ ok: true, paper: true });

    strategy
      .run(exchange, memoryConfig, abortState, (action) => {
        lastActivity = { action, at: new Date().toISOString() };
      })
      .catch((error) => {
        console.error('[Grid] Strategy failed:', error.message);
        lastActivity = { action: 'error', at: new Date().toISOString() };
      })
      .finally(() => {
        running = false;
        abortState = null;
      });
  } catch (error) {
    running = false;
    abortState = null;
    response.status(400).json({ error: error.message });
  }
});

app.post('/api/strategy/stop', async (_request, response) => {
  try {
    if (abortState) abortState.aborted = true;
    await strategy.stop();
    running = false;
    abortState = null;
    lastActivity = { action: 'stopped', at: new Date().toISOString() };
    response.json({ ok: true });
  } catch (error) {
    response.status(500).json({ error: error.message });
  }
});

app.use(express.static(path.join(__dirname, 'public'), {
  dotfiles: 'deny',
  index: 'index.html'
}));

const server = app.listen(PORT, HOST, () => {
  console.log(`Grid Trading Bot demo: http://${HOST}:${PORT}`);
  console.log('Demo/sandbox mode only. Credentials remain in memory.');
});

async function shutdown() {
  if (abortState) abortState.aborted = true;
  await strategy.stop().catch(() => {});
  server.close(() => process.exit(0));
}

process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);
