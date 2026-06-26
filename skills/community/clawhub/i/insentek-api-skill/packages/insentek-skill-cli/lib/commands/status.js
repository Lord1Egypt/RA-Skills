import path from 'node:path';
import { readInstalledManifest } from '../core/manifest.js';
import { resolveExistingInstallLocation, RUNTIMES } from '../runtime/index.js';
import { formatPath, pathExists, printInfo, printSuccess, removeDir } from '../utils.js';

export async function uninstallSkill({ runtimeId, scope, context = {}, silent = false }) {
  const runtime = RUNTIMES[runtimeId];
  const location = await resolveExistingInstallLocation(runtimeId, scope, context);
  const skillFile = path.join(location.installDir, 'SKILL.md');

  if (!(await pathExists(skillFile))) {
    if (!silent) {
      printInfo(`${runtime.label} skill was not found for scope "${scope}"`);
    }
    return { runtimeId, scope, installDir: location.installDir, removed: false };
  }

  await removeDir(location.installDir);
  if (!silent) {
    printSuccess(`${runtime.label} skill removed from ${formatPath(location.installDir)}`);
  }
  return { runtimeId, scope, installDir: location.installDir, removed: true };
}

export async function uninstallSkills({ runtimeIds, scope, context, silent = false }) {
  const results = [];
  for (const runtimeId of runtimeIds) {
    results.push(await uninstallSkill({ runtimeId, scope, context, silent }));
  }
  return results;
}

export async function getInstallStatus({ runtimeId, scope, context = {} }) {
  const runtime = RUNTIMES[runtimeId];
  const location = await resolveExistingInstallLocation(runtimeId, scope, context);
  const skillFile = path.join(location.installDir, 'SKILL.md');
  const installed = await pathExists(skillFile);
  const manifest = installed ? await readInstalledManifest(location.installDir) : null;

  return {
    runtimeId,
    label: runtime.label,
    scope,
    installDir: location.installDir,
    strategy: location.strategy,
    candidates: location.candidates,
    installed,
    version: manifest?.version ?? null,
    manifest,
  };
}

export async function getStatuses({ runtimeIds, scope, context }) {
  const statuses = [];
  for (const runtimeId of runtimeIds) {
    statuses.push(await getInstallStatus({ runtimeId, scope, context }));
  }
  return statuses;
}
