#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const token = argv[i];
    if (token.startsWith('--')) {
      const key = token.slice(2);
      const next = argv[i + 1];
      if (!next || next.startsWith('--')) {
        out[key] = true;
      } else {
        out[key] = next;
        i++;
      }
    } else {
      out._.push(token);
    }
  }
  return out;
}

const args = parseArgs(process.argv.slice(2));
const runtimeRoot = path.resolve(args['runtime-root'] || process.env.SHOPIFY_RUNTIME_ROOT || process.cwd());
const stateDir = path.resolve(args['state-dir'] || process.env.SHOPIFY_STATE_DIR || path.join(runtimeRoot, 'state'));
const logsDir = path.resolve(args['logs-dir'] || process.env.SHOPIFY_LOGS_DIR || path.join(runtimeRoot, 'logs'));
const configPath = path.resolve(args.config || process.env.SHOPIFY_CONFIG_PATH || path.join(runtimeRoot, 'config.json'));
const envPath = path.resolve(args.env || process.env.SHOPIFY_ENV_PATH || path.join(runtimeRoot, '.env'));
const oauthStatePath = path.join(stateDir, 'oauth-state.json');
const installLogPath = path.join(logsDir, 'shopify-install.log');
const webhookLogPath = path.join(logsDir, 'shopify-webhooks.ndjson');

fs.mkdirSync(stateDir, { recursive: true });
fs.mkdirSync(logsDir, { recursive: true });

function usage() {
  console.log(`OpenClaw Shopify Manager Connector

Usage:
  node shopify-connector.mjs auth-url [--runtime-root <dir>]
  node shopify-connector.mjs exchange-code --code <CODE> [--shop <SHOP>]
  node shopify-connector.mjs run-server [--host 127.0.0.1] [--port 8787]
  node shopify-connector.mjs test
  node shopify-connector.mjs shop-info
  node shopify-connector.mjs list-products [--limit 10]
  node shopify-connector.mjs find-products --query <TEXT> [--limit 10]
  node shopify-connector.mjs get-product --id <PRODUCT_GID>
  node shopify-connector.mjs get-product --title <TEXT>
  node shopify-connector.mjs update-product --id <PRODUCT_GID> [--title <TITLE>] [--descriptionHtml <HTML>] [--tags <A,B>] [--status ACTIVE|DRAFT|ARCHIVED]
  node shopify-connector.mjs list-blogs
  node shopify-connector.mjs list-articles --blogId <BLOG_GID>
  node shopify-connector.mjs create-article --blogId <BLOG_GID> --title <TITLE> [--handle <HANDLE>] [--bodyHtml <HTML>] [--published true|false]
  node shopify-connector.mjs update-article --id <ARTICLE_GID> [--title <TITLE>] [--handle <HANDLE>] [--bodyHtml <HTML>] [--published true|false]
`);
}

function parseEnvFile(file) {
  if (!fs.existsSync(file)) return {};
  const lines = fs.readFileSync(file, 'utf8').split(/\r?\n/);
  const out = {};
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const idx = trimmed.indexOf('=');
    if (idx === -1) continue;
    const key = trimmed.slice(0, idx).trim();
    let value = trimmed.slice(idx + 1);
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    out[key] = value;
  }
  return out;
}

function writeEnvFile(file, values) {
  const lines = [
    '# OpenClaw Shopify Manager runtime secrets',
    ...Object.entries(values)
      .filter(([, value]) => value !== undefined && value !== null)
      .map(([key, value]) => `${key}=${String(value)}`)
  ];
  fs.writeFileSync(file, lines.join('\n') + '\n');
}

function updateEnvFile(file, patch) {
  const current = parseEnvFile(file);
  writeEnvFile(file, { ...current, ...patch });
}

function loadConfig() {
  const json = fs.existsSync(configPath) ? JSON.parse(fs.readFileSync(configPath, 'utf8')) : {};
  const env = parseEnvFile(envPath);
  const scopes = env.SHOPIFY_SCOPES
    ? env.SHOPIFY_SCOPES.split(',').map((x) => x.trim()).filter(Boolean)
    : Array.isArray(json.scopes)
      ? json.scopes
      : typeof json.scopes === 'string'
        ? json.scopes.split(',').map((x) => x.trim()).filter(Boolean)
        : [];
  return {
    shop: env.SHOPIFY_SHOP || json.shop,
    apiVersion: env.SHOPIFY_API_VERSION || json.apiVersion || '2026-01',
    apiKey: env.SHOPIFY_API_KEY || json.apiKey,
    apiSecret: env.SHOPIFY_API_SECRET || json.apiSecret,
    scopes,
    redirectUri: env.SHOPIFY_REDIRECT_URI || json.redirectUri,
    accessToken: env.SHOPIFY_ACCESS_TOKEN || json.accessToken || '',
    publicBaseUrl: env.SHOPIFY_PUBLIC_BASE_URL || json.publicBaseUrl || '',
    serverHost: env.SHOPIFY_SERVER_HOST || json.serverHost || '127.0.0.1',
    serverPort: Number(env.SHOPIFY_SERVER_PORT || json.serverPort || 8787),
    mode: env.SHOPIFY_MODE || json.mode || 'require-confirmation-for-mutations',
    allowedMutations: Array.isArray(json.allowedMutations)
      ? json.allowedMutations
      : typeof json.allowedMutations === 'string'
        ? json.allowedMutations.split(',').map((x) => x.trim()).filter(Boolean)
        : []
  };
}

function ensureRequired(config, keys) {
  const missing = keys.filter((key) => !config[key] || (Array.isArray(config[key]) && config[key].length === 0));
  if (missing.length) {
    throw new Error(`Config missing: ${missing.join(', ')}. Fill config.json and/or .env first.`);
  }
}

function saveJson(file, data) {
  fs.writeFileSync(file, JSON.stringify(data, null, 2) + '\n');
}

function appendLog(file, line) {
  fs.appendFileSync(file, line + '\n');
}

function sha256(input) {
  return crypto.createHash('sha256').update(input).digest('hex');
}

function buildShopifyHmacMessageFromSearchParams(params) {
  const cloned = new URLSearchParams(params.toString());
  cloned.delete('hmac');
  cloned.delete('signature');
  return [...cloned.entries()]
    .sort((a, b) => a[0].localeCompare(b[0]))
    .map(([key, value]) => `${key}=${value}`)
    .join('&');
}

function callbackHmacIsValid(searchParams, secret) {
  const hmac = searchParams.get('hmac');
  if (!hmac) return false;
  const message = buildShopifyHmacMessageFromSearchParams(searchParams);
  const digest = crypto.createHmac('sha256', secret).update(message).digest('hex');
  return crypto.timingSafeEqual(Buffer.from(digest), Buffer.from(hmac));
}

function webhookHmacIsValid(rawBody, secret, receivedHmac) {
  if (!receivedHmac) return false;
  const digest = crypto.createHmac('sha256', secret).update(rawBody).digest('base64');
  return crypto.timingSafeEqual(Buffer.from(digest), Buffer.from(receivedHmac));
}

function buildAuthUrl(config) {
  ensureRequired(config, ['shop', 'apiKey', 'apiSecret', 'redirectUri']);
  if (!config.scopes.length) throw new Error('Config missing scopes');
  const state = crypto.randomBytes(16).toString('hex');
  const params = new URLSearchParams({
    client_id: config.apiKey,
    scope: config.scopes.join(','),
    redirect_uri: config.redirectUri,
    state,
    'grant_options[]': ''
  });
  saveJson(oauthStatePath, {
    state,
    createdAt: new Date().toISOString(),
    shop: config.shop,
    redirectUri: config.redirectUri,
    scopes: config.scopes
  });
  return `https://${config.shop}/admin/oauth/authorize?${params.toString()}`;
}

async function exchangeCode(config, code, shop) {
  const targetShop = shop || config.shop;
  if (!code) throw new Error('Missing --code');
  ensureRequired({ ...config, shop: targetShop }, ['apiKey', 'apiSecret', 'shop']);
  const res = await fetch(`https://${targetShop}/admin/oauth/access_token`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({
      client_id: config.apiKey,
      client_secret: config.apiSecret,
      code
    })
  });
  const json = await res.json();
  if (!res.ok) {
    throw new Error(`Token exchange failed (${res.status}): ${JSON.stringify(json, null, 2)}`);
  }
  updateEnvFile(envPath, {
    SHOPIFY_SHOP: targetShop,
    SHOPIFY_ACCESS_TOKEN: json.access_token,
    SHOPIFY_SCOPES: json.scope || config.scopes.join(','),
    SHOPIFY_API_VERSION: config.apiVersion,
    SHOPIFY_REDIRECT_URI: config.redirectUri,
    SHOPIFY_PUBLIC_BASE_URL: config.publicBaseUrl,
    SHOPIFY_SERVER_HOST: config.serverHost,
    SHOPIFY_SERVER_PORT: config.serverPort,
    SHOPIFY_MODE: config.mode
  });
  appendLog(installLogPath, JSON.stringify({ at: new Date().toISOString(), event: 'token-exchanged', shop: targetShop, scope: json.scope || null }));
  return json;
}

async function graphql(config, query, variables = {}) {
  if (!config.accessToken) throw new Error('Missing accessToken. Complete OAuth first.');
  const res = await fetch(`https://${config.shop}/admin/api/${config.apiVersion}/graphql.json`, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'X-Shopify-Access-Token': config.accessToken
    },
    body: JSON.stringify({ query, variables })
  });
  const json = await res.json();
  if (!res.ok || json.errors) {
    throw new Error(`GraphQL request failed (${res.status}): ${JSON.stringify(json, null, 2)}`);
  }
  return json.data;
}

function ensureMutationAllowed(config, action) {
  if (config.mode === 'read-only') {
    throw new Error(`Mutation blocked: mode is read-only (${action})`);
  }
  if (config.mode === 'allow-approved-operations' && config.allowedMutations.length && !config.allowedMutations.includes(action)) {
    throw new Error(`Mutation blocked: ${action} is not in allowedMutations`);
  }
}

async function test(config) {
  const data = await graphql(config, `query { shop { name myshopifyDomain primaryDomain { url } } }`);
  console.log(JSON.stringify(data, null, 2));
}

async function shopInfo(config) {
  const data = await graphql(config, `query { shop { id name email myshopifyDomain plan { displayName partnerDevelopment } primaryDomain { url } } }`);
  console.log(JSON.stringify(data, null, 2));
}

async function listProducts(config, limit = 10) {
  const data = await graphql(config, `query($first:Int!){ products(first:$first){ edges{ node{ id title handle status tags onlineStoreUrl } } } }`, { first: Number(limit) });
  console.log(JSON.stringify(data, null, 2));
}

async function findProducts(config, query, limit = 10) {
  if (!query) throw new Error('Missing --query');
  const data = await graphql(config, `query($first:Int!, $query:String!){ products(first:$first, query:$query){ edges{ node{ id title handle status tags onlineStoreUrl } } } }`, {
    first: Number(limit),
    query: `title:*${query}*`
  });
  console.log(JSON.stringify(data, null, 2));
}

async function getProduct(config, id, title) {
  if (!id && !title) throw new Error('Missing --id or --title');
  if (id) {
    const data = await graphql(config, `query($id:ID!){ product(id:$id){ id title handle status tags descriptionHtml onlineStoreUrl } }`, { id });
    console.log(JSON.stringify(data, null, 2));
    return;
  }
  const data = await graphql(config, `query($first:Int!, $query:String!){ products(first:$first, query:$query){ edges{ node{ id title handle status tags descriptionHtml onlineStoreUrl } } } }`, {
    first: 1,
    query: `title:*${title}*`
  });
  console.log(JSON.stringify(data, null, 2));
}

async function updateProduct(config, input) {
  ensureMutationAllowed(config, 'productUpdate');
  if (!input.id) throw new Error('Missing --id');
  const product = { id: input.id };
  if (input.title !== undefined) product.title = input.title;
  if (input.descriptionHtml !== undefined) product.descriptionHtml = input.descriptionHtml;
  if (input.tags !== undefined) product.tags = String(input.tags).split(',').map((x) => x.trim()).filter(Boolean);
  if (input.status !== undefined) product.status = input.status;
  const data = await graphql(config, `mutation($product: ProductUpdateInput!){ productUpdate(product:$product){ product{ id title handle status tags } userErrors{ field message } } }`, { product });
  console.log(JSON.stringify(data, null, 2));
}

async function listBlogs(config) {
  const data = await graphql(config, `query { blogs(first:20){ edges{ node{ id title handle } } } }`);
  console.log(JSON.stringify(data, null, 2));
}

async function listArticles(config, blogId) {
  if (!blogId) throw new Error('Missing --blogId');
  const data = await graphql(config, `query($id:ID!){ blog(id:$id){ id title articles(first:20){ edges{ node{ id title handle isPublished publishedAt onlineStoreUrl } } } } }`, { id: blogId });
  console.log(JSON.stringify(data, null, 2));
}

function parseBooleanish(value, fallback = undefined) {
  if (value === undefined) return fallback;
  if (typeof value === 'boolean') return value;
  const normalized = String(value).trim().toLowerCase();
  if (['true', '1', 'yes', 'y'].includes(normalized)) return true;
  if (['false', '0', 'no', 'n'].includes(normalized)) return false;
  return fallback;
}

async function createArticle(config, input) {
  ensureMutationAllowed(config, 'articleCreate');
  if (!input.blogId) throw new Error('Missing --blogId');
  if (!input.title) throw new Error('Missing --title');
  const article = { title: input.title };
  if (input.handle !== undefined) article.handle = input.handle;
  if (input.bodyHtml !== undefined) article.body = input.bodyHtml;
  const isPublished = parseBooleanish(input.published, undefined);
  if (isPublished !== undefined) article.isPublished = isPublished;
  const data = await graphql(config, `mutation($blogId:ID!, $article: OnlineStoreArticleCreateInput!){ articleCreate(blogId:$blogId, article:$article){ article{ id title handle isPublished onlineStoreUrl } userErrors{ field message } } }`, { blogId: input.blogId, article });
  console.log(JSON.stringify(data, null, 2));
}

async function updateArticle(config, input) {
  ensureMutationAllowed(config, 'articleUpdate');
  if (!input.id) throw new Error('Missing --id');
  const article = { id: input.id };
  if (input.title !== undefined) article.title = input.title;
  if (input.handle !== undefined) article.handle = input.handle;
  if (input.bodyHtml !== undefined) article.body = input.bodyHtml;
  const isPublished = parseBooleanish(input.published, undefined);
  if (isPublished !== undefined) article.isPublished = isPublished;
  const data = await graphql(config, `mutation($article: OnlineStoreArticleUpdateInput!){ articleUpdate(article:$article){ article{ id title handle isPublished onlineStoreUrl } userErrors{ field message } } }`, { article });
  console.log(JSON.stringify(data, null, 2));
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on('data', (chunk) => chunks.push(chunk));
    req.on('end', () => resolve(Buffer.concat(chunks)));
    req.on('error', reject);
  });
}

function send(res, status, body, headers = {}) {
  res.writeHead(status, { 'content-type': 'text/plain; charset=utf-8', ...headers });
  res.end(body);
}

async function runServer(config, options = {}) {
  ensureRequired(config, ['shop', 'apiKey', 'apiSecret', 'redirectUri']);
  const host = options.host || config.serverHost || '127.0.0.1';
  const port = Number(options.port || config.serverPort || 8787);
  const redirectUrl = new URL(config.redirectUri);
  const publicBase = config.publicBaseUrl || redirectUrl.origin;
  const publicBasePath = new URL(publicBase).pathname.replace(/\/$/, '');
  const callbackPath = redirectUrl.pathname;
  const callbackPathStripped = publicBasePath && callbackPath.startsWith(publicBasePath)
    ? callbackPath.slice(publicBasePath.length) || '/'
    : callbackPath;
  const webhookPath = '/shopify/webhooks';

  const server = http.createServer(async (req, res) => {
    const url = new URL(req.url, `http://${req.headers.host || `${host}:${port}`}`);
    try {
      if (req.method === 'GET' && url.pathname === '/healthz') return send(res, 200, 'ok');

      if (req.method === 'GET' && (url.pathname === callbackPath || url.pathname === callbackPathStripped)) {
        const params = url.searchParams;
        const saved = fs.existsSync(oauthStatePath) ? JSON.parse(fs.readFileSync(oauthStatePath, 'utf8')) : null;
        if (!callbackHmacIsValid(params, config.apiSecret)) {
          appendLog(installLogPath, JSON.stringify({ at: new Date().toISOString(), event: 'callback-invalid-hmac', queryHash: sha256(url.search) }));
          return send(res, 400, 'Invalid Shopify callback HMAC');
        }
        if (!saved || params.get('state') !== saved.state) {
          appendLog(installLogPath, JSON.stringify({ at: new Date().toISOString(), event: 'callback-invalid-state', queryHash: sha256(url.search) }));
          return send(res, 400, 'Invalid OAuth state');
        }
        const result = await exchangeCode(config, params.get('code'), params.get('shop'));
        appendLog(installLogPath, JSON.stringify({ at: new Date().toISOString(), event: 'callback-success', shop: params.get('shop'), scope: result.scope || null }));
        return send(res, 200, `OpenClaw Shopify Manager install complete for ${params.get('shop')}. Offline token stored locally.`);
      }

      if (req.method === 'POST' && url.pathname.startsWith(webhookPath)) {
        const rawBody = await readBody(req);
        const receivedHmac = req.headers['x-shopify-hmac-sha256'];
        if (!webhookHmacIsValid(rawBody, config.apiSecret, receivedHmac)) {
          appendLog(webhookLogPath, JSON.stringify({ at: new Date().toISOString(), event: 'invalid-hmac', path: url.pathname }));
          return send(res, 401, 'Invalid webhook HMAC');
        }
        appendLog(webhookLogPath, JSON.stringify({
          at: new Date().toISOString(),
          event: 'webhook',
          topic: req.headers['x-shopify-topic'] || null,
          shop: req.headers['x-shopify-shop-domain'] || null,
          webhookId: req.headers['x-shopify-webhook-id'] || null,
          path: url.pathname,
          bodySha256: sha256(rawBody),
          bodyBytes: rawBody.length
        }));
        return send(res, 200, 'ok');
      }

      return send(res, 404, 'Not found');
    } catch (err) {
      appendLog(installLogPath, JSON.stringify({ at: new Date().toISOString(), event: 'server-error', path: url.pathname, error: err.message || String(err) }));
      return send(res, 500, err.message || 'Internal error');
    }
  });

  server.listen(port, host, () => {
    console.log(JSON.stringify({
      ok: true,
      host,
      port,
      runtimeRoot,
      configPath,
      envPath,
      callbackUrl: config.redirectUri,
      webhookBaseUrl: `${publicBase}${webhookPath}`,
      healthUrl: `http://${host}:${port}/healthz`
    }, null, 2));
  });
}

async function main() {
  const command = args._[0];
  if (!command) {
    usage();
    process.exit(1);
  }
  const config = loadConfig();

  switch (command) {
    case 'auth-url':
      console.log(buildAuthUrl(config));
      break;
    case 'exchange-code':
      console.log(JSON.stringify({ ok: true, scope: (await exchangeCode(config, args.code, args.shop)).scope || null }, null, 2));
      break;
    case 'run-server':
      await runServer(config, { host: args.host, port: args.port });
      break;
    case 'test':
      await test(loadConfig());
      break;
    case 'shop-info':
      await shopInfo(loadConfig());
      break;
    case 'list-products':
      await listProducts(loadConfig(), args.limit || 10);
      break;
    case 'find-products':
      await findProducts(loadConfig(), args.query, args.limit || 10);
      break;
    case 'get-product':
      await getProduct(loadConfig(), args.id, args.title);
      break;
    case 'update-product':
      await updateProduct(loadConfig(), args);
      break;
    case 'list-blogs':
      await listBlogs(loadConfig());
      break;
    case 'list-articles':
      await listArticles(loadConfig(), args.blogId);
      break;
    case 'create-article':
      await createArticle(loadConfig(), args);
      break;
    case 'update-article':
      await updateArticle(loadConfig(), args);
      break;
    case 'check-hmac': {
      const query = args.query;
      if (!query) throw new Error('Missing --query');
      const params = new URLSearchParams(query.startsWith('?') ? query.slice(1) : query);
      console.log(JSON.stringify({ valid: callbackHmacIsValid(params, loadConfig().apiSecret), checksum: sha256(query) }, null, 2));
      break;
    }
    default:
      usage();
      process.exit(1);
  }
}

main().catch((err) => {
  console.error(err.message || err);
  process.exit(1);
});
