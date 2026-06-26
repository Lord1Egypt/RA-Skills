#!/usr/bin/env node
import { hostname, platform, arch } from 'node:os';
import { ensureDir, loadPending, removePending, saveConfig, savePending, PEARL_HOST } from './io.js';

function formatPlatform() {
  const p = platform();
  const a = arch();
  const names = { darwin: 'macOS', linux: 'Linux', win32: 'Windows' };
  return `${names[p] || p} ${a}`;
}

async function check() {
  const pending = loadPending('session');
  if (!pending) {
    console.error('No pending session. Run setup first (without --check).');
    process.exit(1);
  }

  const res = await fetch(`${PEARL_HOST}/api/connect/sessions/${pending.code}`);

  if (res.status === 404) {
    removePending('session');
    console.error('Session expired. Run setup again (without --check).');
    process.exit(1);
  }

  const { data } = await res.json();

  if (data.status === 'approved') {
    const { read_token, skill_token, user_id } = data;
    saveConfig({ user_id, read_token, skill_token });
    removePending('session');
    console.log('Pearl config saved to ~/.pearl/config.json');
    process.exit(0);
  }

  console.log('Still waiting for login. Ask the user to open the link and log in.');
  process.exit(2);
}

if (process.argv.includes('--check')) {
  await check();
}

ensureDir();

const deviceInfo = {
  hostname: hostname().replace(/\.local$/, ''),
  platform: formatPlatform(),
};

const res = await fetch(`${PEARL_HOST}/api/connect/sessions`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(deviceInfo),
});
const { data } = await res.json();
const code = data.code;

savePending('session', { code });

const connectUrl = `${PEARL_HOST}/c/${code}`;

console.log('Send this link to the user to connect their Pearl wallet:');
console.log(connectUrl);

console.log('Link expires in 15 minutes. After the user logs in, run this script with --check.');
