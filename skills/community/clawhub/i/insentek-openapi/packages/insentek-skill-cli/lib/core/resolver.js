import { existsSync } from 'node:fs';
import path from 'node:path';
import { SKILL_ID } from '../constants.js';

export function findWorkspaceRoot(startDir = process.cwd()) {
  let current = path.resolve(startDir);
  const root = path.parse(current).root;

  while (current !== root) {
    const markers = [
      path.join(current, '.openclaw'),
      path.join(current, 'openclaw.json'),
      path.join(current, '.claude'),
    ];
    if (markers.some((marker) => existsSync(marker))) {
      return current;
    }
    if (existsSync(path.join(current, '.git')) && existsSync(path.join(current, 'skills'))) {
      return current;
    }
    current = path.dirname(current);
  }

  return path.resolve(startDir);
}

export function resolveScopeRoot(scope, context = {}) {
  const cwd = path.resolve(context.cwd || process.cwd());
  if (scope === 'global') {
    return null;
  }
  if (scope === 'workspace') {
    return findWorkspaceRoot(cwd);
  }
  return cwd;
}

export function buildInstallTarget(baseDir) {
  return path.join(baseDir, SKILL_ID);
}

export function formatResolverResult({ runtime, scope, installDir, strategy, candidates }) {
  return {
    runtime,
    scope,
    installDir,
    strategy,
    candidates,
  };
}
