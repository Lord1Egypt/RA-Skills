export const RUNTIME_SCOPES = {
  claude: ['global', 'project'],
  openclaw: ['global', 'project', 'workspace'],
};

export const ALL_SCOPES = ['global', 'project', 'workspace'];

export function normalizeScope(scope = 'global') {
  const key = scope.trim().toLowerCase();
  if (!ALL_SCOPES.includes(key)) {
    throw new Error(`Unknown scope "${scope}". Supported: ${ALL_SCOPES.join(', ')}`);
  }
  return key;
}

export function getScopesForRuntime(runtimeId) {
  return RUNTIME_SCOPES[runtimeId] ?? ALL_SCOPES;
}

export function getScopesForRuntimes(runtimeIds) {
  if (!runtimeIds.length) {
    return ALL_SCOPES;
  }
  return runtimeIds.reduce((allowed, runtimeId) => {
    const runtimeScopes = getScopesForRuntime(runtimeId);
    return allowed.filter((scope) => runtimeScopes.includes(scope));
  }, ALL_SCOPES);
}

export function getScopeOptionHelp(runtimeIds = []) {
  if (!runtimeIds.length) {
    return 'global, project (claude) | global, project, workspace (openclaw)';
  }
  return getScopesForRuntimes(runtimeIds).join(', ');
}

export function validateScopeForRuntime(runtimeId, scope) {
  const normalized = normalizeScope(scope);
  const allowed = getScopesForRuntime(runtimeId);
  if (!allowed.includes(normalized)) {
    throw new Error(
      `Scope "${scope}" is not supported for ${runtimeId}. Supported: ${allowed.join(', ')}`,
    );
  }
  return normalized;
}

export function validateScopeForRuntimes(runtimeIds, scope) {
  const normalized = normalizeScope(scope);
  for (const runtimeId of runtimeIds) {
    validateScopeForRuntime(runtimeId, normalized);
  }
  return normalized;
}

export function getScopeChoices(runtimeIds) {
  const allowed = getScopesForRuntimes(runtimeIds);
  const labels = {
    global: 'global — user-level, available everywhere',
    project: 'project — current project directory',
    workspace: 'workspace — ~/.openclaw/workspace/skills (OpenClaw only)',
  };

  return allowed.map((scope) => ({
    name: labels[scope],
    value: scope,
  }));
}
