import { copySkillAssets } from '../copy.js';
import { resolveInstallLocation, RUNTIMES } from '../runtime/index.js';
import { formatPath, printSuccess } from '../utils.js';
import { readBundledManifest, readInstalledManifest } from './manifest.js';
import { validateScopeForRuntime } from './scope.js';

export async function installSkill({
  runtimeId,
  scope,
  context = {},
  force = false,
  silent = false,
}) {
  validateScopeForRuntime(runtimeId, scope);
  const runtime = RUNTIMES[runtimeId];
  const location = resolveInstallLocation(runtimeId, scope, context);
  await copySkillAssets(location.installDir, { force });
  if (!silent) {
    printSuccess(`${runtime.label} skill installed at ${formatPath(location.installDir)}`);
  }
  return {
    runtimeId,
    scope,
    installDir: location.installDir,
    strategy: location.strategy,
    manifest: await readBundledManifest(),
  };
}

export async function installSkills({ runtimeIds, scope, context, force = false, silent = false }) {
  const results = [];
  for (const runtimeId of runtimeIds) {
    results.push(await installSkill({ runtimeId, scope, context, force, silent }));
  }
  return results;
}

export async function updateSkill(options) {
  const location = resolveInstallLocation(options.runtimeId, options.scope, options.context);
  const current = await readInstalledManifest(location.installDir);
  const result = await installSkill({ ...options, force: true });
  return {
    ...result,
    previousVersion: current?.version ?? null,
    nextVersion: result.manifest.version,
  };
}

export async function updateSkills({ runtimeIds, scope, context, silent = false }) {
  const results = [];
  for (const runtimeId of runtimeIds) {
    results.push(await updateSkill({ runtimeId, scope, context, silent }));
  }
  return results;
}
