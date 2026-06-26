import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, it } from 'node:test';

const originalHome = process.env.USERPROFILE || process.env.HOME;
const testHome = path.join(os.tmpdir(), `insentek-cred-test-${process.pid}`);

async function importCredentialsModule() {
  const modulePath = new URL('../lib/core/credentials.js', import.meta.url).href;
  return import(`${modulePath}?t=${Date.now()}`);
}

beforeEach(async () => {
  process.env.USERPROFILE = testHome;
  process.env.HOME = testHome;
  await fs.rm(testHome, { recursive: true, force: true });
});

afterEach(async () => {
  await fs.rm(testHome, { recursive: true, force: true });
  if (originalHome) {
    process.env.USERPROFILE = originalHome;
    process.env.HOME = originalHome;
  }
});

describe('credentials storage', () => {
  it('saves and loads encrypted credentials', async () => {
    const {
      saveCredentials,
      loadCredentials,
      hasCredentials,
      CREDENTIALS_FILE,
    } = await importCredentialsModule();

    await saveCredentials({
      appid: 'demo-app',
      secret: 'demo-secret-value',
      token: 'demo-token-value',
    });

    const raw = JSON.parse(await fs.readFile(CREDENTIALS_FILE, 'utf8'));
    assert.equal(raw.encrypted, true);
    assert.notEqual(raw.secret_enc, 'demo-secret-value');

    const creds = await loadCredentials();
    assert.equal(creds.appid, 'demo-app');
    assert.equal(creds.secret, 'demo-secret-value');
    assert.equal(creds.token, 'demo-token-value');
    assert.equal(await hasCredentials(), true);
  });

  it('clears saved credentials', async () => {
    const {
      saveCredentials,
      clearCredentials,
      hasCredentials,
    } = await importCredentialsModule();

    await saveCredentials({ appid: 'demo-app', secret: 'demo-secret-value' });
    assert.equal(await clearCredentials(), true);
    assert.equal(await hasCredentials(), false);
    assert.equal(await clearCredentials(), false);
  });

  it('masks secrets in status output', async () => {
    const {
      saveCredentials,
      getCredentialStatus,
    } = await importCredentialsModule();

    await saveCredentials({
      appid: 'demo-app',
      secret: 'abcdefghijklmnop',
      token: '0123456789abcdef',
    });

    const status = await getCredentialStatus();
    assert.equal(status.connected, true);
    assert.match(status.secret, /^abcd\*\*\*\*mnop$/);
    assert.match(status.token, /^01234567\*\*\*\*cdef$/);
  });
});
