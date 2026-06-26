import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

export function expandHome(inputPath) {
  if (!inputPath) return inputPath;
  if (inputPath === '~') return os.homedir();
  if (inputPath.startsWith('~/')) {
    return path.join(os.homedir(), inputPath.slice(2));
  }
  return inputPath;
}

export async function pathExists(targetPath) {
  try {
    await fs.access(targetPath);
    return true;
  } catch {
    return false;
  }
}

export async function ensureDir(dirPath) {
  await fs.mkdir(dirPath, { recursive: true });
}

export async function removeDir(dirPath) {
  await fs.rm(dirPath, { recursive: true, force: true });
}

export function commandExists(command) {
  const checker = process.platform === 'win32' ? 'where' : 'which';
  const result = spawnSync(checker, [command], { stdio: 'ignore' });
  return result.status === 0;
}

export function runCommand(command, args, options = {}) {
  const result = spawnSync(command, args, {
    encoding: 'utf8',
    stdio: options.silent ? 'pipe' : 'inherit',
    cwd: options.cwd,
    shell: process.platform === 'win32',
  });

  if (result.status !== 0) {
    const stderr = result.stderr?.trim();
    throw new Error(stderr || `Command failed: ${command} ${args.join(' ')}`);
  }

  return result.stdout?.trim() ?? '';
}

export function formatPath(targetPath) {
  const home = os.homedir();
  if (targetPath.startsWith(home)) {
    if (process.platform === 'win32') {
      return `%USERPROFILE%${targetPath.slice(home.length)}`;
    }
    return `~${targetPath.slice(home.length).replace(/\\/g, '/')}`;
  }
  return targetPath;
}

export function printSuccess(message) {
  console.log(`✔ ${message}`);
}

export function printInfo(message) {
  console.log(`→ ${message}`);
}

export function printWarn(message) {
  console.log(`! ${message}`);
}
