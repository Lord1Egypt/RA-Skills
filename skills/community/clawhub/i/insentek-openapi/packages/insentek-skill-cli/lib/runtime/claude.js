import path from 'node:path';
import { getHomeDir } from '../os.js';
import { SKILL_ID } from '../constants.js';
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

export const claudeRuntime = {
  id: 'claude',
  label: 'Claude Code',
  description: 'Claude Code skills directory (global or project)',
  resolve(scope, context = {}) {
    validateScopeForRuntime('claude', scope);
    const scopeRoot = resolveScopeRoot(scope, context);

    const candidates = scope === 'global'
      ? [homeSkills('.claude', 'skills')]
      : [scopedSkills(scopeRoot, '.claude', 'skills')];

    const strategy = scope === 'global'
      ? 'Claude Code global skills directory'
      : 'Claude Code project skills directory';

    return formatResolverResult({
      runtime: 'claude',
      scope,
      installDir: candidates[0],
      strategy,
      candidates,
    });
  },
};
