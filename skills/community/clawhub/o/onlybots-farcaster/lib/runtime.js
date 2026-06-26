import 'dotenv/config';
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));

export function loadConfig() {
  return JSON.parse(readFileSync(resolve(__dirname, '../references/config.json'), 'utf8'));
}

export function loadCredentials() {
  const { NEYNAR_API_KEY, NEYNAR_SIGNER_UUID, FARCASTER_USERNAME } = process.env;

  if (!NEYNAR_API_KEY || !NEYNAR_SIGNER_UUID || !FARCASTER_USERNAME) {
    throw new Error('Missing NEYNAR_API_KEY, NEYNAR_SIGNER_UUID, or FARCASTER_USERNAME in .env');
  }

  return {
    apiKey: NEYNAR_API_KEY,
    signerUuid: NEYNAR_SIGNER_UUID,
    farcasterUsername: FARCASTER_USERNAME
  };
}

export function loadRuntime() {
  return {
    config: loadConfig(),
    credentials: loadCredentials()
  };
}
