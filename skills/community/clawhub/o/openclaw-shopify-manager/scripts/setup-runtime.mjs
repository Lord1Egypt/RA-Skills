#!/usr/bin/env node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import readline from 'node:readline';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const skillRoot = path.resolve(__dirname, '..');
const assetsDir = path.join(skillRoot, 'assets');

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
const command = args._[0] || 'help';

function expandHome(input) {
  if (!input) return input;
  if (input === '~') return os.homedir();
  if (input.startsWith('~/')) return path.join(os.homedir(), input.slice(2));
  return input;
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function readJson(file, fallback = {}) {
  if (!fs.existsSync(file)) return fallback;
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function writeJson(file, data) {
  fs.writeFileSync(file, JSON.stringify(data, null, 2) + '\n');
}

function parseEnvFile(file) {
  if (!fs.existsSync(file)) return {};
  const out = {};
  for (const line of fs.readFileSync(file, 'utf8').split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const idx = trimmed.indexOf('=');
    if (idx === -1) continue;
    out[trimmed.slice(0, idx)] = trimmed.slice(idx + 1);
  }
  return out;
}

function writeEnvFile(file, values) {
  const lines = [
    '# OpenClaw Shopify Manager runtime secrets',
    ...Object.entries(values).map(([key, value]) => `${key}=${value ?? ''}`)
  ];
  fs.writeFileSync(file, lines.join('\n') + '\n');
}

function promptFactory() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const ask = (question) => new Promise((resolve) => rl.question(question, resolve));
  const askSecret = async (question, fallback = '') => {
    if (!process.stdin.isTTY || !process.stdout.isTTY) return fallback;
    process.stdout.write(`${question}${fallback ? ' [stored/keep current]' : ''}: `);
    const stdin = process.stdin;
    stdin.resume();
    stdin.setRawMode(true);
    let value = '';
    while (true) {
      const chunk = await new Promise((resolve) => stdin.once('data', resolve));
      const text = String(chunk);
      if (text === '\r' || text === '\n') {
        process.stdout.write('\n');
        break;
      }
      if (text === '\u0003') {
        process.stdout.write('^C\n');
        process.exit(130);
      }
      if (text === '\u007f') {
        if (value.length > 0) value = value.slice(0, -1);
        continue;
      }
      value += text;
    }
    stdin.setRawMode(false);
    return value || fallback;
  };
  return { ask, askSecret, close: () => rl.close() };
}

function defaultRuntimeRoot() {
  return path.join(os.homedir(), 'oc', 'shopify-runtime');
}

function buildDefaultPublicBase(hostname) {
  return hostname ? `https://${hostname}/shopify-manager` : 'https://YOUR-TAILSCALE-HOSTNAME/shopify-manager';
}

function inferRedirectUri(publicBaseUrl) {
  return `${String(publicBaseUrl).replace(/\/$/, '')}/shopify/callback`;
}

function normalizeScopes(scopes) {
  if (!scopes) return ['read_products', 'write_products', 'read_content', 'write_content', 'read_orders'];
  if (Array.isArray(scopes)) return scopes;
  return String(scopes).split(',').map((x) => x.trim()).filter(Boolean);
}

function loadTemplateFiles() {
  return {
    config: readJson(path.join(assetsDir, 'config.example.json')),
    env: parseEnvFile(path.join(assetsDir, 'env.example')),
    service: fs.readFileSync(path.join(assetsDir, 'shopify-connector.service.txt'), 'utf8'),
    connector: fs.readFileSync(path.join(__dirname, 'shopify-connector.mjs'), 'utf8')
  };
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'\\''`)}'`;
}

function redact(value) {
  if (!value) return '(missing)';
  if (value.length <= 8) return 'set';
  return `${value.slice(0, 4)}…${value.slice(-2)}`;
}

function commandExists(bin) {
  try {
    execFileSync('bash', ['-lc', `command -v ${bin}`], { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

function getTailscaleStatus() {
  const result = { installed: false, loggedIn: false, serveSupported: false, funnelSupported: false };
  if (!commandExists('tailscale')) return result;
  result.installed = true;
  try {
    const status = execFileSync('bash', ['-lc', 'tailscale status 2>/dev/null || true'], { encoding: 'utf8' }).trim();
    result.loggedIn = Boolean(status);
  } catch {}
  try {
    execFileSync('bash', ['-lc', 'tailscale serve --help >/dev/null 2>&1'], { stdio: 'ignore' });
    result.serveSupported = true;
  } catch {}
  try {
    execFileSync('bash', ['-lc', 'tailscale funnel --help >/dev/null 2>&1'], { stdio: 'ignore' });
    result.funnelSupported = true;
  } catch {}
  return result;
}

function isLikelyPlaceholder(value) {
  if (!value) return true;
  return /YOUR-|example\.myshopify\.com|your-store\.myshopify\.com|YOUR_API_|YOUR-HOST/i.test(String(value));
}

function validateRedirectAgainstBase(publicBaseUrl, redirectUri) {
  try {
    const redirect = new URL(redirectUri);
    const base = new URL(publicBaseUrl);
    return redirect.origin === base.origin && redirect.pathname === `${base.pathname.replace(/\/$/, '')}/shopify/callback`;
  } catch {
    return false;
  }
}

function ensureRuntimeGitignore(runtimeRoot) {
  const gitignorePath = path.join(runtimeRoot, '.gitignore');
  const required = ['.env', 'state/', 'logs/'];
  const existing = fs.existsSync(gitignorePath) ? fs.readFileSync(gitignorePath, 'utf8') : '';
  const lines = existing.split(/\r?\n/).filter(Boolean);
  let changed = false;
  for (const item of required) {
    if (!lines.includes(item)) {
      lines.push(item);
      changed = true;
    }
  }
  if (!fs.existsSync(gitignorePath) || changed) {
    fs.writeFileSync(gitignorePath, lines.join('\n') + '\n');
  }
  return gitignorePath;
}

function hasRuntimeGitignoreProtection(runtimeRoot) {
  const gitignorePath = path.join(runtimeRoot, '.gitignore');
  if (!fs.existsSync(gitignorePath)) return false;
  const content = fs.readFileSync(gitignorePath, 'utf8');
  return ['.env', 'state/', 'logs/'].every((item) => content.split(/\r?\n/).includes(item));
}

function usage() {
  console.log(`OpenClaw Shopify Manager setup helper

Usage:
  node setup-runtime.mjs init [--runtime-root <dir>] [--shop <shop.myshopify.com>] [--public-base-url <https://host/path>] [--mode <read-only|require-confirmation-for-mutations|allow-approved-operations>] [--scopes <csv>] [--write-service]
  node setup-runtime.mjs guided-setup [same flags as init]
  node setup-runtime.mjs doctor [--runtime-root <dir>]
  node setup-runtime.mjs help

Notes:
- init creates a canonical runtime folder with config.json, .env, state/, logs/, shopify-connector.mjs, and an optional systemd service template.
- guided-setup is an explicit alias for init and is the recommended user-facing command.
- guided-setup prompts for Shopify secrets and stores them in .env.
- doctor checks completeness, placeholder values, callback consistency, and likely ingress readiness.
- avoid passing secrets as CLI flags because they can leak via shell history and process inspection.
`);
}

async function collectSetupValues(prompter, tpl, existingEnv = {}) {
  async function getValue(flag, question, fallback = '') {
    if (args[flag] !== undefined) return args[flag];
    if (!prompter) return fallback;
    const answer = await prompter.ask(`${question}${fallback ? ` [${fallback}]` : ''}: `);
    return answer.trim() || fallback;
  }

  async function getSecret(flag, question, fallback = '') {
    if (args[flag] !== undefined) return args[flag];
    if (!prompter) return fallback;
    return prompter.askSecret(question, fallback);
  }

  const tailscaleHostname = await getValue('tailscale-hostname', 'Tailscale/custom hostname for public HTTPS (omit https://, optional)', '');
  const publicBaseUrl = (await getValue('public-base-url', 'Public base URL for the connector', buildDefaultPublicBase(tailscaleHostname))).replace(/\/$/, '');
  const shop = await getValue('shop', 'Shopify shop domain', existingEnv.SHOPIFY_SHOP || tpl.config.shop || 'example.myshopify.com');
  const apiKey = await getSecret('api-key', 'Shopify API key / client ID (stored in .env only)', existingEnv.SHOPIFY_API_KEY || '');
  const apiSecret = await getSecret('api-secret', 'Shopify API secret / client secret (stored in .env only)', existingEnv.SHOPIFY_API_SECRET || '');
  const mode = await getValue('mode', 'Operating mode', args.mode || tpl.config.mode || 'require-confirmation-for-mutations');
  const scopes = normalizeScopes(await getValue('scopes', 'Admin API scopes (comma-separated)', normalizeScopes(args.scopes || existingEnv.SHOPIFY_SCOPES || tpl.env.SHOPIFY_SCOPES).join(',')));
  const redirectUri = await getValue('redirect-uri', 'Redirect URI', existingEnv.SHOPIFY_REDIRECT_URI || inferRedirectUri(publicBaseUrl));
  const writeService = Boolean(args['write-service']);
  return { tailscaleHostname, publicBaseUrl, shop, apiKey, apiSecret, mode, scopes, redirectUri, writeService };
}

async function initRuntime() {
  const runtimeRoot = path.resolve(expandHome(args['runtime-root'] || defaultRuntimeRoot()));
  const tpl = loadTemplateFiles();
  const prompter = process.stdin.isTTY ? promptFactory() : null;
  const existingEnvPath = path.join(runtimeRoot, '.env');
  const existingEnv = parseEnvFile(existingEnvPath);
  const values = await collectSetupValues(prompter, tpl, existingEnv);

  ensureDir(runtimeRoot);
  ensureDir(path.join(runtimeRoot, 'state'));
  ensureDir(path.join(runtimeRoot, 'logs'));

  const configPath = path.join(runtimeRoot, 'config.json');
  const envPath = path.join(runtimeRoot, '.env');
  const connectorPath = path.join(runtimeRoot, 'shopify-connector.mjs');
  const servicePath = path.join(runtimeRoot, 'shopify-connector.service');

  const config = {
    ...tpl.config,
    shop: values.shop,
    scopes: values.scopes,
    publicBaseUrl: values.publicBaseUrl,
    redirectUri: values.redirectUri,
    mode: values.mode
  };

  const env = {
    ...tpl.env,
    ...existingEnv,
    SHOPIFY_SHOP: values.shop,
    SHOPIFY_API_KEY: values.apiKey,
    SHOPIFY_API_SECRET: values.apiSecret,
    SHOPIFY_SCOPES: values.scopes.join(','),
    SHOPIFY_PUBLIC_BASE_URL: values.publicBaseUrl,
    SHOPIFY_REDIRECT_URI: values.redirectUri,
    SHOPIFY_MODE: values.mode
  };

  writeJson(configPath, config);
  writeEnvFile(envPath, env);
  fs.writeFileSync(connectorPath, tpl.connector);
  const runtimeGitignorePath = ensureRuntimeGitignore(runtimeRoot);

  if (values.writeService) {
    fs.writeFileSync(servicePath, tpl.service.replaceAll('%h/oc/shopify-runtime', runtimeRoot));
  }

  if (prompter) prompter.close();

  const nextAuthCommand = `cd ${shellQuote(runtimeRoot)} && node ./shopify-connector.mjs auth-url`;
  const nextRunCommand = `cd ${shellQuote(runtimeRoot)} && node ./shopify-connector.mjs run-server`;
  const tailscale = getTailscaleStatus();
  const cliSecretsUsed = args['api-key'] !== undefined || args['api-secret'] !== undefined;

  console.log(JSON.stringify({
    ok: true,
    mode: command === 'guided-setup' ? 'guided-setup' : 'init',
    runtimeRoot,
    files: {
      configPath,
      envPath,
      connectorPath,
      servicePath: values.writeService ? servicePath : null,
      gitignorePath: runtimeGitignorePath
    },
    setupSummary: {
      shop: values.shop,
      publicBaseUrl: values.publicBaseUrl,
      redirectUri: values.redirectUri,
      mode: values.mode,
      scopes: values.scopes,
      apiKey: redact(values.apiKey),
      apiSecret: redact(values.apiSecret),
      accessToken: existingEnv.SHOPIFY_ACCESS_TOKEN ? 'already stored in .env' : 'stored in .env after OAuth'
    },
    secretHandling: {
      secretsFile: envPath,
      tokenStorage: `${envPath} -> SHOPIFY_ACCESS_TOKEN`,
      runtimeGitignore: runtimeGitignorePath,
      cliSecretsUsed,
      warning: cliSecretsUsed ? 'Secrets were passed via CLI flags. Prefer interactive entry or direct .env editing next time.' : null
    },
    shopifyAppValues: {
      appUrl: values.publicBaseUrl,
      redirectUrl: values.redirectUri
    },
    ingressHints: {
      tailscaleInstalled: tailscale.installed,
      tailscaleLoggedIn: tailscale.loggedIn,
      recommendedServe: values.publicBaseUrl.includes('/shopify-manager') ? 'tailscale serve --https=443 /shopify-manager http://127.0.0.1:8787' : null,
      recommendedFunnel: tailscale.funnelSupported ? 'tailscale funnel --https=443 on' : null
    },
    next: {
      step1_startLocalServer: nextRunCommand,
      step2_verifyLocalHealth: 'curl http://127.0.0.1:8787/healthz',
      step3_exposeHttps: values.publicBaseUrl.includes('/shopify-manager') ? 'tailscale serve --https=443 /shopify-manager http://127.0.0.1:8787' : 'Expose the connector publicBaseUrl over HTTPS using your existing ingress',
      step4_generateInstallUrl: nextAuthCommand,
      step5_verifyStoreRead: `cd ${shellQuote(runtimeRoot)} && node ./shopify-connector.mjs shop-info`
    },
    notes: [
      'Paste and keep Shopify secrets in .env only. Do not commit .env.',
      'A runtime .gitignore is written to ignore .env, state/, and logs/.',
      'Point the Shopify app App URL and Allowed redirection URL to the printed values above.',
      'Expose the local connector over HTTPS before completing OAuth.',
      'After OAuth succeeds, SHOPIFY_ACCESS_TOKEN will be stored locally in .env.',
      values.writeService ? 'A local systemd unit template was written to the runtime directory.' : 'Re-run with --write-service if you want a local systemd unit template generated.'
    ]
  }, null, 2));
}

function doctor() {
  const runtimeRoot = path.resolve(expandHome(args['runtime-root'] || defaultRuntimeRoot()));
  const configPath = path.join(runtimeRoot, 'config.json');
  const envPath = path.join(runtimeRoot, '.env');
  const connectorPath = path.join(runtimeRoot, 'shopify-connector.mjs');
  const gitignorePath = path.join(runtimeRoot, '.gitignore');
  const stateDir = path.join(runtimeRoot, 'state');
  const logsDir = path.join(runtimeRoot, 'logs');
  const installLogPath = path.join(logsDir, 'shopify-install.log');
  const config = readJson(configPath, {});
  const env = parseEnvFile(envPath);
  const publicBaseUrl = env.SHOPIFY_PUBLIC_BASE_URL || config.publicBaseUrl || '';
  const redirectUri = env.SHOPIFY_REDIRECT_URI || config.redirectUri || '';
  const accessToken = env.SHOPIFY_ACCESS_TOKEN || config.accessToken || '';
  const tailscale = getTailscaleStatus();

  const checks = [
    { key: 'runtimeRoot', ok: fs.existsSync(runtimeRoot), severity: 'error', detail: runtimeRoot },
    { key: 'config.json', ok: fs.existsSync(configPath), severity: 'error', detail: configPath },
    { key: '.env', ok: fs.existsSync(envPath), severity: 'error', detail: envPath },
    { key: 'shopify-connector.mjs', ok: fs.existsSync(connectorPath), severity: 'error', detail: connectorPath },
    { key: 'runtime.gitignore', ok: fs.existsSync(gitignorePath), severity: 'warn', detail: gitignorePath },
    { key: 'runtime.gitignore.protectsSecrets', ok: hasRuntimeGitignoreProtection(runtimeRoot), severity: 'warn', detail: '.gitignore should include .env, state/, logs/' },
    { key: 'stateDir', ok: fs.existsSync(stateDir), severity: 'warn', detail: stateDir },
    { key: 'logsDir', ok: fs.existsSync(logsDir), severity: 'warn', detail: logsDir },
    { key: 'shop', ok: Boolean(env.SHOPIFY_SHOP || config.shop) && !isLikelyPlaceholder(env.SHOPIFY_SHOP || config.shop), severity: 'error', detail: env.SHOPIFY_SHOP || config.shop || null },
    { key: 'apiKey', ok: Boolean(env.SHOPIFY_API_KEY || config.apiKey) && !isLikelyPlaceholder(env.SHOPIFY_API_KEY || config.apiKey), severity: 'error', detail: redact(env.SHOPIFY_API_KEY || config.apiKey || '') },
    { key: 'apiSecret', ok: Boolean(env.SHOPIFY_API_SECRET || config.apiSecret) && !isLikelyPlaceholder(env.SHOPIFY_API_SECRET || config.apiSecret), severity: 'error', detail: redact(env.SHOPIFY_API_SECRET || config.apiSecret || '') },
    { key: 'publicBaseUrl', ok: Boolean(publicBaseUrl) && !isLikelyPlaceholder(publicBaseUrl), severity: 'error', detail: publicBaseUrl || null },
    { key: 'redirectUri', ok: Boolean(redirectUri) && !isLikelyPlaceholder(redirectUri), severity: 'error', detail: redirectUri || null },
    { key: 'redirectMatchesBase', ok: Boolean(publicBaseUrl && redirectUri) && validateRedirectAgainstBase(publicBaseUrl, redirectUri), severity: 'error', detail: 'redirect should be <publicBaseUrl>/shopify/callback' },
    { key: 'accessToken', ok: Boolean(accessToken), severity: 'info', detail: accessToken ? 'stored in .env' : 'missing until OAuth completes' },
    { key: 'installLog', ok: fs.existsSync(installLogPath), severity: 'info', detail: fs.existsSync(installLogPath) ? installLogPath : 'missing until server/OAuth activity' },
    { key: 'tailscaleInstalled', ok: !publicBaseUrl.includes('ts.net') || tailscale.installed, severity: 'warn', detail: tailscale.installed ? 'installed' : 'not installed' },
    { key: 'tailscaleLoggedIn', ok: !tailscale.installed || tailscale.loggedIn, severity: 'warn', detail: tailscale.installed ? (tailscale.loggedIn ? 'logged in' : 'installed but not logged in') : 'not checked' },
    { key: 'tailscaleServe', ok: !tailscale.installed || tailscale.serveSupported, severity: 'warn', detail: tailscale.installed ? (tailscale.serveSupported ? 'supported' : 'not available') : 'not checked' }
  ];

  const errors = checks.filter((x) => x.severity === 'error' && !x.ok);
  const warnings = checks.filter((x) => x.severity === 'warn' && !x.ok);
  const suggestions = [];

  if (errors.some((x) => ['config.json', '.env', 'shopify-connector.mjs'].includes(x.key))) {
    suggestions.push(`Recreate the canonical runtime: node ./scripts/setup-runtime.mjs guided-setup --runtime-root ${shellQuote(runtimeRoot)}`);
  }
  if (warnings.some((x) => ['runtime.gitignore', 'runtime.gitignore.protectsSecrets'].includes(x.key))) {
    suggestions.push(`Add a runtime .gitignore that ignores .env, state/, and logs/ under ${runtimeRoot}.`);
  }
  if (errors.some((x) => ['shop', 'apiKey', 'apiSecret', 'publicBaseUrl', 'redirectUri'].includes(x.key))) {
    suggestions.push(`Fill the missing or placeholder values in ${envPath} and ${configPath}. Keep secrets only in ${envPath}.`);
  }
  if (errors.some((x) => x.key === 'redirectMatchesBase')) {
    suggestions.push('Set SHOPIFY_REDIRECT_URI to exactly <publicBaseUrl>/shopify/callback.');
  }
  if (!accessToken) {
    suggestions.push(`After the server is reachable, complete OAuth with: cd ${shellQuote(runtimeRoot)} && node ./shopify-connector.mjs auth-url`);
  }
  if (!tailscale.installed && publicBaseUrl.includes('ts.net')) {
    suggestions.push('Install and log into Tailscale before using the ts.net callback URL.');
  }
  if (tailscale.installed && !tailscale.loggedIn) {
    suggestions.push('Run: sudo tailscale up');
  }

  console.log(JSON.stringify({
    ok: errors.length === 0,
    runtimeRoot,
    secretHandling: {
      secretsFile: envPath,
      tokenStorage: `${envPath} -> SHOPIFY_ACCESS_TOKEN`,
      runtimeGitignore: gitignorePath,
      committedSecretsRecommended: false
    },
    checks,
    summary: {
      errors: errors.length,
      warnings: warnings.length,
      oauthCompleted: Boolean(accessToken)
    },
    next: {
      startServer: `cd ${shellQuote(runtimeRoot)} && node ./shopify-connector.mjs run-server`,
      verifyHealth: 'curl http://127.0.0.1:8787/healthz',
      exposeWithTailscale: 'tailscale serve --https=443 /shopify-manager http://127.0.0.1:8787',
      completeOAuth: `cd ${shellQuote(runtimeRoot)} && node ./shopify-connector.mjs auth-url`,
      verifyStoreRead: `cd ${shellQuote(runtimeRoot)} && node ./shopify-connector.mjs shop-info`
    },
    suggestions
  }, null, 2));
}

switch (command) {
  case 'init':
  case 'guided-setup':
    await initRuntime();
    break;
  case 'doctor':
    doctor();
    break;
  case 'help':
  default:
    usage();
    break;
}
