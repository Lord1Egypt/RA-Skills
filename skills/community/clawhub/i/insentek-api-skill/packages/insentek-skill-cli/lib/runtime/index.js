import { existsSync } from 'node:fs';
import path from 'node:path';
import { claudeRuntime } from './claude.js';
import { openclawRuntime } from './openclaw.js';

export const RUNTIMES = {
  claude: claudeRuntime,
  openclaw: openclawRuntime,
};

export const RUNTIME_IDS = Object.keys(RUNTIMES);

export function getRuntimeOptionHelp() {
  return `${RUNTIME_IDS.join(', ')}, all`;
}

export function normalizeRuntimeToken(token) {
  const key = token.trim().toLowerCase();
  if (key === 'all') {
    return 'all';
  }
  if (!RUNTIMES[key]) {
    throw new Error(`Unknown runtime "${token}". Supported: ${getRuntimeOptionHelp()}`);
  }
  return key;
}

export function resolveRuntimeIds(input) {
  const tokens = input.split(',').map((item) => normalizeRuntimeToken(item));
  if (tokens.includes('all')) {
    return RUNTIME_IDS;
  }
  return [...new Set(tokens)];
}

export function resolveInstallLocation(runtimeId, scope, context = {}) {
  const runtime = RUNTIMES[runtimeId];
  if (!runtime) {
    throw new Error(`Unknown runtime: ${runtimeId}`);
  }
  return runtime.resolve(scope, context);
}

export async function resolveExistingInstallLocation(runtimeId, scope, context = {}) {
  const resolved = resolveInstallLocation(runtimeId, scope, context);
  for (const candidate of resolved.candidates) {
    if (existsSync(path.join(candidate, 'SKILL.md'))) {
      return { ...resolved, installDir: candidate };
    }
  }
  return resolved;
}

export { claudeRuntime, openclawRuntime };
