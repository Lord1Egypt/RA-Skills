/**
 * moltpost register [--force]
 * Generate key pair, POST /register, write config.json
 */

import {
  ensureMoltpostHome,
  keysExist,
  writePrivateKey,
  writePublicKey,
  writeConfig,
  readConfig,
  getPath,
} from '../lib/storage.mjs';
import { generateKeyPair } from '../lib/crypto.mjs';
import { resolveClawid, resolveBrokerUrl } from '../lib/identity.mjs';

function parseArg(args, ...flags) {
  for (const flag of flags) {
    const eqIdx = args.findIndex((a) => a.startsWith(`${flag}=`));
    if (eqIdx !== -1) return args[eqIdx].slice(flag.length + 1);
    const spaceIdx = args.indexOf(flag);
    if (spaceIdx !== -1 && spaceIdx + 1 < args.length && !args[spaceIdx + 1].startsWith('--')) {
      return args[spaceIdx + 1];
    }
  }
  return undefined;
}

export async function cmdRegister(args) {
  const force = args.includes('--force');
  const brokerUrl = resolveBrokerUrl(parseArg(args, '--broker'));
  const clawid = resolveClawid(parseArg(args, '--clawid', '--id'));
  const groupName = parseArg(args, '--group') || null;

  if (!brokerUrl) {
    console.error('Error: set Broker URL via --broker=<url> or MOLTPOST_BROKER_URL');
    process.exit(1);
  }

  ensureMoltpostHome();

  if (keysExist() && !force) {
    console.error(
      'Registration already exists. Use --force to re-register.\nWarning: --force invalidates the old access_token immediately.'
    );
    process.exit(1);
  }

  console.log('Generating RSA-2048 key pair...');
  const { privateKey, publicKey } = generateKeyPair();

  writePrivateKey(privateKey);
  writePublicKey(publicKey);
  console.log(`Key pair written to ${getPath('keys')}`);

  const headers = {
    'Content-Type': 'application/json',
    'X-Request-Id': `req_${Date.now()}`,
  };
  if (force) {
    const existingConfig = readConfig();
    if (existingConfig?.access_token) {
      headers['Authorization'] = `Bearer ${existingConfig.access_token}`;
    }
    headers['X-Force-Register'] = 'true';
  }

  let res, data;
  try {
    res = await fetch(`${brokerUrl}/register`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ clawid, pubkey: publicKey, group_name: groupName }),
    });
    data = await res.json();
  } catch (err) {
    console.error(`Register failed (network): ${err.message}`);
    process.exit(1);
  }

  if (res.status !== 200) {
    console.error(`Register failed (${res.status}): ${data.error || JSON.stringify(data)}`);
    process.exit(1);
  }

  const config = {
    broker_url: brokerUrl,
    clawid,
    access_token: data.access_token,
    pull_batch_size: 10,
    inbox: {
      active_max: 200,
      archive_after_days: 7,
    },
    auto_reply: {
      enabled: false,
      rules_file: getPath('auto-reply-rules.json'),
    },
    security: {
      scan_patterns: ['OPENAI_API_KEY', 'sk-', 'Bearer '],
      forward_secrecy: false,
    },
    groups: {},
  };

  writeConfig(config);
  console.log(`✓ Registered. ClawID: ${clawid}`);
  console.log(`  Data directory: ${getPath()}`);
  if (groupName) {
    console.log(`  ClawGroup auto-created: ${groupName}`);
  }
}
