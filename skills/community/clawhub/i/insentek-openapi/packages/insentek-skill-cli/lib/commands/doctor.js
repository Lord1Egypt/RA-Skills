import fs from 'node:fs/promises';
import path from 'node:path';
import { ASSETS_DIR, PACKAGE_NAME, SKILL_ID } from '../constants.js';
import { getCredentialStatus, hasCredentials } from '../core/credentials.js';
import { readBundledManifest, validateManifest } from '../core/manifest.js';
import { resolveInstallLocation, RUNTIMES } from '../runtime/index.js';
import { getInstallStatus } from './status.js';
import { formatPath, pathExists, printInfo, printSuccess, printWarn } from '../utils.js';
import {
  getScopesForRuntime,
  normalizeScope,
  validateScopeForRuntime,
} from '../core/scope.js';

import { findPythonCommand } from '../python.js';

function checkLineEndings(content) {
  if (content.includes('\r\n')) {
    return { ok: true, message: 'CRLF detected (Windows)' };
  }
  if (content.includes('\n')) {
    return { ok: true, message: 'LF detected (Unix)' };
  }
  return { ok: false, message: 'No line endings detected' };
}

async function checkBundledAssets() {
  const manifest = await readBundledManifest();
  await validateManifest(manifest);
  const skillPath = path.join(ASSETS_DIR, 'SKILL.md');
  if (!(await pathExists(skillPath))) {
    throw new Error('Bundled SKILL.md not found');
  }
  return manifest;
}

async function checkRuntimeInstall(runtimeId, scope, context) {
  const runtime = RUNTIMES[runtimeId];
  const location = resolveInstallLocation(runtimeId, scope, context);
  const status = await getInstallStatus({ runtimeId, scope, context });
  const checks = [];

  checks.push({
    name: `${runtime.label} install directory`,
    ok: status.installed,
    message: status.installed
      ? `Installed at ${formatPath(status.installDir)}`
      : `Not installed (expected: ${formatPath(location.installDir)})`,
  });

  if (status.installed) {
    checks.push({
      name: `${runtime.label} manifest`,
      ok: Boolean(status.manifest?.id === SKILL_ID),
      message: status.manifest
        ? `skill.json id=${status.manifest.id}, version=${status.manifest.version}`
        : 'skill.json missing',
    });

    const skillContent = await fs.readFile(path.join(status.installDir, 'SKILL.md'), 'utf8');
    checks.push({
      name: `${runtime.label} SKILL.md`,
      ok: skillContent.includes('name: insentek-openapi'),
      message: 'SKILL.md present and id matches',
    });

    checks.push({
      name: `${runtime.label} line endings`,
      ...checkLineEndings(skillContent),
    });

    const cliScript = path.join(status.installDir, 'scripts', 'insentek_cli.py');
    checks.push({
      name: `${runtime.label} scripts`,
      ok: await pathExists(cliScript),
      message: await pathExists(cliScript) ? 'scripts/insentek_cli.py found' : 'scripts missing',
    });
  }

  return checks;
}

export async function runDoctor({ runtimeIds, scope, context, silent = false }) {
  const checks = [];
  let allPassed = true;

  if (!silent) {
    printInfo('Running doctor checks...');
  }

  try {
    const bundled = await checkBundledAssets();
    checks.push({
      name: 'Bundled manifest',
      ok: true,
      message: `${bundled.id} v${bundled.version}`,
    });
  } catch (error) {
    allPassed = false;
    checks.push({ name: 'Bundled manifest', ok: false, message: error.message });
  }

  for (const runtimeId of runtimeIds) {
    const allowed = getScopesForRuntime(runtimeId);
    checks.push({
      name: `${RUNTIMES[runtimeId].label} scopes`,
      ok: allowed.includes(normalizeScope(scope)),
      message: allowed.join(', '),
    });
  }

  const python = findPythonCommand();
  checks.push({
    name: 'Python',
    ok: Boolean(python),
    message: python
      ? `${python.command}: ${python.version} (scripts require >=3.10)`
      : 'Python 3.10+ not found in PATH. Install python3 from python.org / brew / your distro package manager.',
  });

  const connected = await hasCredentials();
  const credentialStatus = await getCredentialStatus();
  checks.push({
    name: 'Insentek API credentials',
    ok: connected,
    message: connected
      ? `Connected as ${credentialStatus.appid} (${credentialStatus.encrypted ? 'encrypted' : 'legacy'})`
      : `Not connected. Run: npx ${PACKAGE_NAME} login`,
  });

  for (const runtimeId of runtimeIds) {
    validateScopeForRuntime(runtimeId, scope);
    const runtimeChecks = await checkRuntimeInstall(runtimeId, scope, context);
    checks.push(...runtimeChecks);
  }

  allPassed = checks.every((check) => check.ok);

  if (!silent) {
    console.log('\nDoctor report:\n');
    for (const check of checks) {
      const icon = check.ok ? '✔' : '✖';
      console.log(`  ${icon} ${check.name}: ${check.message}`);
    }

    console.log('');
    if (allPassed) {
      printSuccess('All doctor checks passed');
    } else {
      printWarn('Some doctor checks failed');
    }
  }

  return { allPassed, checks };
}
