// ms365/src/auth.js
const { loadConfig, saveTokens, loadTokens, normalizeAccount } = require('./config');

const SCOPES = 'User.Read Mail.Read Mail.Send Calendars.ReadWrite offline_access';

async function startDeviceFlow(account = 'default') {
  const name = normalizeAccount(account);
  const config = loadConfig(name);
  if (!config.clientId) throw new Error(`No Client ID for account '${name}'. Set MICROSOFT_CLIENT_ID or create config.${name}.json`);

  const endpoint = `https://login.microsoftonline.com/${config.tenantId}/oauth2/v2.0/devicecode`;
  const res = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ client_id: config.clientId, scope: SCOPES }),
  });

  if (!res.ok) throw new Error(`Auth failed: ${res.status} ${await res.text()}`);
  const data = await res.json();

  console.log(`\n========================================`);
  console.log(`Account: ${name}`);
  console.log(`Go to: ${data.verification_uri}`);
  console.log(`Code:  ${data.user_code}`);
  console.log(`========================================\n`);

  return pollForToken(data.device_code, data.interval, config, name);
}

async function pollForToken(deviceCode, interval, config, account) {
  const endpoint = `https://login.microsoftonline.com/${config.tenantId}/oauth2/v2.0/token`;
  let wait = Number(interval || 5);

  while (true) {
    await new Promise(r => setTimeout(r, wait * 1000));
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'urn:ietf:params:oauth:grant-type:device_code',
        client_id: config.clientId,
        device_code: deviceCode,
      }),
    });

    const data = await res.json();
    if (data.error) {
      if (data.error === 'authorization_pending') { process.stdout.write('.'); continue; }
      if (data.error === 'slow_down') { wait += 5; continue; }
      if (data.error === 'expired_token') throw new Error('Code expired. Try again.');
      throw new Error(`Token error: ${data.error_description || data.error}`);
    }

    saveTokens(data, account);
    console.log(`\nAuthenticated! Tokens saved for '${account}'.`);
    return data.access_token;
  }
}

async function getAccessToken(account = 'default') {
  const name = normalizeAccount(account);
  const tokens = loadTokens(name);
  const config = loadConfig(name);
  if (!config.clientId) throw new Error(`No Client ID for account '${name}'.`);

  if (!tokens) return startDeviceFlow(name);
  if (!tokens.expires_at || Date.now() > tokens.expires_at - 300000) {
    return refreshAccessToken(tokens, config, name);
  }
  return tokens.access_token;
}

async function refreshAccessToken(existing, config, account) {
  const endpoint = `https://login.microsoftonline.com/${config.tenantId}/oauth2/v2.0/token`;
  const res = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'refresh_token',
      client_id: config.clientId,
      refresh_token: existing.refresh_token,
      scope: SCOPES,
    }),
  });

  if (!res.ok) {
    console.error('Refresh failed, re-authenticating...');
    return startDeviceFlow(account);
  }

  const data = await res.json();
  const merged = { ...existing, ...data, refresh_token: data.refresh_token || existing.refresh_token };
  saveTokens(merged, account);
  return merged.access_token;
}

module.exports = { startDeviceFlow, getAccessToken };
