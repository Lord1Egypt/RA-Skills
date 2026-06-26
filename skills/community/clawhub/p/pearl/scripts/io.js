import { existsSync, mkdirSync, readFileSync, unlinkSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';

const dir = join(homedir(), '.pearl');
const configPath = join(dir, 'config.json');

export const PEARL_HOST = 'https://pearlcash.ai';

export function ensureDir() {
  mkdirSync(dir, { recursive: true, mode: 0o700 });
}

export function loadConfig() {
  return JSON.parse(readFileSync(configPath, 'utf8'));
}

export function saveConfig(data) {
  writeFileSync(configPath, JSON.stringify(data, null, 2) + '\n', { mode: 0o600 });
}

export function loadPending(name) {
  const p = join(dir, `pending-${name}.json`);
  if (!existsSync(p)) return null;
  return JSON.parse(readFileSync(p, 'utf8'));
}

export function savePending(name, data) {
  writeFileSync(join(dir, `pending-${name}.json`), JSON.stringify(data), { mode: 0o600 });
}

export function removePending(name) {
  const p = join(dir, `pending-${name}.json`);
  if (existsSync(p)) unlinkSync(p);
}
