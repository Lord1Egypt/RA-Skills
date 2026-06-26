import path from 'node:path';
import { getHomeDir } from '../os.js';
import {
  buildInstallTarget,
  formatResolverResult,
  resolveScopeRoot,
} from '../core/resolver.js';
import { validateScopeForRuntime } from '../core/scope.js';

function homeSkills(...segments) {
  return buildInstallTarget(path.join(getHomeDir(), ...segments));
}

function scopedSkills(scopeRoot, ...segments) {
  return buildInstallTarget(path.join(scopeRoot, ...segments));
}

export const openclawRuntime = {
  id: 'openclaw',
  label: 'OpenClaw',
  description: 'OpenClaw skills directory',
  resolve(scope, context = {}) {
    validateScopeForRuntime('openclaw', scope);
    const scopeRoot = resolveScopeRoot(scope, context);
    let candidates;
    let strategy;

    if (scope === 'global') {
      candidates = [
        homeSkills('.openclaw', 'skills'),
        homeSkills('.config', 'openclaw', 'skills'),
      ];
      strategy = 'OpenClaw global skills directory (first available location)';
    } else if (scope === 'workspace') {
      candidates = [
        homeSkills('.openclaw', 'workspace', 'skills'),
      ];
      strategy = 'OpenClaw workspace skills directory (~/.openclaw/workspace/skills)';
    } else {
      candidates = [
        scopedSkills(scopeRoot, 'skills'),
        scopedSkills(scopeRoot, '.openclaw', 'skills'),
      ];
      strategy = 'OpenClaw project skills directory';
    }

    candidates = candidates.filter((candidate, index, list) => list.indexOf(candidate) === index);

    return formatResolverResult({
      runtime: 'openclaw',
      scope,
      installDir: candidates[0],
      strategy,
      candidates,
    });
  },
};
