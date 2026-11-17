/**
 * First-run / troubleshooting self-check for the powpow-integration skill.
 *
 * Verifies everything the other scripts depend on:
 *   1. Node.js version (>= 18, needs global fetch)
 *   2. config.json present and parseable, platformUrl set
 *   3. Platform reachable (unauthenticated network probe)
 *   4. Login session: local age + server-side validity probe
 *   5. Unsplash key (optional - only needed for --image search:...)
 *
 * Usage: node doctor.js
 * Exit code: 0 = all critical checks pass, 1 = something needs fixing.
 */
const fs = require('fs');
const path = require('path');
const { loadConfig, loadSession, api, SessionExpiredError, STATE_DIR, SESSION_PATH } = require('./lib/api-client');

// Session lives in the writable state dir (bundle itself is read-only in hosts
// such as OpenClaw). loadConfig() resolves user override -> bundled default.

function nodeCheck() {
  const major = parseInt(process.versions.node.split('.')[0], 10);
  if (major >= 18 && typeof fetch === 'function') {
    return { ok: true, msg: `Node.js ${process.versions.node} (>= 18, fetch available)` };
  }
  return {
    ok: false,
    msg: `Node.js ${process.versions.node} is too old or lacks fetch. Install Node.js 18+ from https://nodejs.org`,
  };
}

function configCheck() {
  try {
    const config = loadConfig();
    if (!config.platformUrl) {
      return { ok: false, msg: 'config.json is missing "platformUrl"' };
    }
    return { ok: true, msg: `config.json OK (platform: ${config.platformUrl})` };
  } catch (err) {
    return { ok: false, msg: `config.json is missing or not valid JSON: ${err.message}` };
  }
}

async function platformCheck() {
  try {
    const config = loadConfig();
    const resp = await fetch(config.platformUrl, { method: 'HEAD', signal: AbortSignal.timeout(10000) });
    if (resp.status < 500) return { ok: true, msg: `Platform reachable (HTTP ${resp.status})` };
    return { ok: false, msg: `Platform responded with HTTP ${resp.status}` };
  } catch (err) {
    return { ok: false, msg: `Cannot reach the platform: ${err.message} (check your network)` };
  }
}

function sessionLocalCheck() {
  if (!fs.existsSync(SESSION_PATH)) return { ok: false, msg: 'Not logged in yet' };
  const session = loadSession();
  if (!session) return { ok: false, msg: 'Session expired by local age limit - re-login required' };
  return { ok: true, msg: `Local session OK (user: ${session.username}, loginAt: ${session.loginAt})` };
}

async function sessionServerCheck() {
  try {
    await api('GET', '/api/digital-humans?scope=all');
    return { ok: true, msg: 'Session accepted by the platform server' };
  } catch (err) {
    if (err instanceof SessionExpiredError) {
      return { ok: false, msg: 'Session rejected by the server - re-login required' };
    }
    return { ok: false, msg: `Session probe failed: ${err.message}` };
  }
}

function unsplashCheck() {
  const fromEnv = !!process.env.UNSPLASH_ACCESS_KEY;
  let fromConfig = false;
  try { fromConfig = !!loadConfig().unsplashAccessKey; } catch { /* config errors reported above */ }
  if (fromConfig || fromEnv) {
    return { ok: true, warnOnly: true, msg: `Unsplash key configured (${fromConfig ? 'config.json' : 'env'})` };
  }
  return {
    ok: true,
    warnOnly: true,
    msg: 'No Unsplash key - image search disabled (posting without images still works; add "unsplashAccessKey" to config.json to enable)',
  };
}

async function main() {
  console.log('=== PowPow Integration - Self Check ===\n');

  const checks = [];
  const node = nodeCheck();
  checks.push(['Node.js', node]);
  const config = configCheck();
  checks.push(['config.json', config]);

  let platform = { ok: false, warnOnly: true, msg: 'Skipped (config.json broken)' };
  if (config.ok) platform = await platformCheck();
  checks.push(['Platform network', platform]);

  const sessionLocal = sessionLocalCheck();
  checks.push(['Session (local)', sessionLocal]);

  let sessionServer = { ok: false, warnOnly: true, msg: 'Skipped (no valid local session or network)' };
  if (sessionLocal.ok && platform.ok) sessionServer = await sessionServerCheck();
  checks.push(['Session (server)', sessionServer]);

  checks.push(['Unsplash key (optional)', unsplashCheck()]);

  let allCriticalOk = true;
  for (const [name, result] of checks) {
    const icon = result.ok ? '✅' : (result.warnOnly ? '⚠️ ' : '❌');
    console.log(`${icon} ${name}: ${result.msg}`);
    if (!result.ok && !result.warnOnly) allCriticalOk = false;
  }

  console.log('');
  if (!fs.existsSync(SESSION_PATH) || !sessionLocal.ok) {
    console.log('Next step: log in with  node scripts/login.js <username>  (it will ask for your password hidden)');
  } else if (!sessionServer.ok) {
    console.log('Next step: re-login with  node scripts/login.js <username>');
  } else if (allCriticalOk) {
    console.log('All checks passed. You are ready to compose and publish posts.');
  }

  process.exitCode = allCriticalOk ? 0 : 1;
}

main();
