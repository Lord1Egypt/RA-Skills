// ms365/src/config.js
const fs = require('fs');
const path = require('path');

const CREDENTIALS_DIR = path.join(process.env.HOME || '/data', '.openclaw', 'credentials');

function normalizeAccount(name) {
  return String(name || 'default').toLowerCase().replace(/[^a-z0-9_-]/g, '_');
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
}

function loadConfig(account) {
  const envFile = path.join(CREDENTIALS_DIR, 'ms365.env');
  if (fs.existsSync(envFile)) {
    const lines = fs.readFileSync(envFile, 'utf8').split('\n');
    for (const line of lines) {
      const m = line.match(/^([A-Z_]+)=(.+)$/);
      if (m && !process.env[m[1]]) process.env[m[1]] = m[2].trim();
    }
  }

  const skillDir = path.resolve(__dirname, '..');
  const configFile = path.join(skillDir, `config.${account}.json`);
  let fileConfig = {};
  if (fs.existsSync(configFile)) {
    fileConfig = JSON.parse(fs.readFileSync(configFile, 'utf8'));
  }

  return {
    clientId: fileConfig.clientId || process.env.MICROSOFT_CLIENT_ID || '',
    tenantId: fileConfig.tenantId || process.env.MICROSOFT_TENANT_ID || 'common',
  };
}

function tokenPath(account) {
  ensureDir(CREDENTIALS_DIR);
  return path.join(CREDENTIALS_DIR, `ms365.tokens.${normalizeAccount(account)}.json`);
}

function saveTokens(data, account) {
  const merged = { ...data, expires_at: Date.now() + (data.expires_in || 3600) * 1000 };
  fs.writeFileSync(tokenPath(account), JSON.stringify(merged, null, 2), { mode: 0o600 });
}

function loadTokens(account) {
  const p = tokenPath(account);
  if (!fs.existsSync(p)) return null;
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

module.exports = { normalizeAccount, loadConfig, saveTokens, loadTokens };
