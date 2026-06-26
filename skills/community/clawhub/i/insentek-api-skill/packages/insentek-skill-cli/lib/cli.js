import { select, confirm } from '@inquirer/prompts';
import { createRequire } from 'node:module';
import { Command } from 'commander';
import { CLI_NAME, PACKAGE_NAME, SKILL_ID } from './constants.js';
import { NOT_CONNECTED_MESSAGE } from './core/credentials.js';
import { runAuthStatus } from './commands/auth.js';
import { runDoctor } from './commands/doctor.js';
import { ensureCredentialsForInstall, runLogin } from './commands/login.js';
import { runLogout } from './commands/logout.js';
import { getStatuses, uninstallSkills } from './commands/status.js';
import { installSkills, updateSkills } from './core/installer.js';
import {
  getScopeChoices,
  getScopeOptionHelp,
  getScopesForRuntime,
  normalizeScope,
  validateScopeForRuntimes,
} from './core/scope.js';
import { findWorkspaceRoot } from './core/resolver.js';
import { detectOS, getOSLabel } from './os.js';
import {
  assertNonInteractive,
  buildInfoPayload,
  getJsonFlag,
  serializeInstallResult,
  serializeStatus,
  serializeUninstallResult,
  serializeUpdateResult,
  writeJson,
} from './output.js';
import {
  getRuntimeOptionHelp,
  resolveInstallLocation,
  resolveRuntimeIds,
  RUNTIME_IDS,
  RUNTIMES,
} from './runtime/index.js';
import { formatPath, printInfo } from './utils.js';

const require = createRequire(import.meta.url);
const pkg = require('../package.json');

function buildCommandContext() {
  return { cwd: process.cwd() };
}

function buildOptions(opts, runtimeIds = []) {
  const scope = opts.scope ? normalizeScope(opts.scope) : 'global';
  if (runtimeIds.length > 0) {
    validateScopeForRuntimes(runtimeIds, scope);
  }
  return {
    runtime: opts.runtime,
    scope,
    force: opts.force,
    yes: opts.yes,
  };
}

function resolveDoctorRuntimeIds(defaults) {
  const runtimeIds = defaults.runtime
    ? resolveRuntimeIds(defaults.runtime)
    : RUNTIME_IDS.filter((id) => getScopesForRuntime(id).includes(defaults.scope));
  if (defaults.runtime) {
    validateScopeForRuntimes(runtimeIds, defaults.scope);
  } else if (runtimeIds.length === 0) {
    throw new Error(`Scope "${defaults.scope}" is not supported by any runtime.`);
  }
  return runtimeIds;
}

function resolveStatusRuntimeIds(defaults) {
  const runtimeIds = defaults.runtime ? resolveRuntimeIds(defaults.runtime) : RUNTIME_IDS;
  if (defaults.runtime) {
    validateScopeForRuntimes(runtimeIds, defaults.scope);
  }
  const compatibleRuntimeIds = runtimeIds.filter((runtimeId) => (
    getScopesForRuntime(runtimeId).includes(defaults.scope)
  ));
  if (compatibleRuntimeIds.length === 0) {
    throw new Error(`Scope "${defaults.scope}" is not supported for selected runtime(s).`);
  }
  return compatibleRuntimeIds;
}

async function promptRuntimeSelection(message = 'Select AI agent runtime') {
  return select({
    message,
    choices: RUNTIME_IDS.map((id) => {
      const location = resolveInstallLocation(id, 'global', buildCommandContext());
      return {
        name: `${RUNTIMES[id].label}  →  ${formatPath(location.installDir)}`,
        value: id,
      };
    }),
  });
}

async function resolveRuntimeIdsFromOptions({ runtime, yes, promptMessage }) {
  if (runtime) {
    return resolveRuntimeIds(runtime);
  }
  if (yes) {
    throw new Error('Runtime is required when using --yes. Example: -r claude');
  }
  return [await promptRuntimeSelection(promptMessage)];
}

async function promptInstallOptions(defaults) {
  const runtimeIds = await resolveRuntimeIdsFromOptions({
    runtime: defaults.runtime,
    yes: defaults.yes,
    promptMessage: 'Select AI agent runtime to install',
  });

  const scope = defaults.scope === 'global' && !defaults.yes
    ? await select({
      message: 'Install scope',
      choices: getScopeChoices(runtimeIds),
      default: 'global',
    })
    : validateScopeForRuntimes(runtimeIds, defaults.scope);

  const force = defaults.force ?? await confirm({
    message: 'Overwrite existing installation if present?',
    default: false,
  });

  return { runtimeIds, scope, force };
}

function printInstallSummary(results) {
  console.log('\nInstallation complete.\n');
  for (const item of results) {
    console.log(`  • ${RUNTIMES[item.runtimeId].label}: ${formatPath(item.installDir)}`);
    console.log(`    skill: ${item.manifest.id} v${item.manifest.version}`);
    console.log(`    strategy: ${item.strategy}`);
  }
  console.log('\nNext step: open your agent and ask, for example:');
  console.log('  "查看所有设备"\n');
}

function printInstallCredentialHint(connection) {
  if (connection.connected) {
    return;
  }
  console.log(`${NOT_CONNECTED_MESSAGE}\n`);
}

function printUpdateSummary(results) {
  console.log('\nUpdate complete.\n');
  for (const item of results) {
    const from = item.previousVersion ?? 'not installed';
    console.log(`  • ${RUNTIMES[item.runtimeId].label}: ${from} → ${item.nextVersion}`);
    console.log(`    ${formatPath(item.installDir)}`);
  }
  console.log('');
}

function printStatusTable(statuses) {
  console.log('\nInstallation status:\n');
  for (const item of statuses) {
    const state = item.installed ? `installed (${item.version || 'unknown version'})` : 'not installed';
    console.log(`  • ${item.label} [${item.scope}]: ${state}`);
    console.log(`    ${formatPath(item.installDir)}`);
    console.log(`    strategy: ${item.strategy}`);
  }
  console.log('');
}

function printWelcome() {
  const osLabel = getOSLabel(detectOS());
  const workspaceRoot = findWorkspaceRoot();
  console.log(`\n${CLI_NAME} v${pkg.version}`);
  console.log(`Package: ${PACKAGE_NAME}`);
  console.log(`Skill ID: ${SKILL_ID}`);
  console.log(`Detected OS: ${osLabel}`);
  console.log(`Workspace root: ${formatPath(workspaceRoot)}`);
  console.log('Install locations are resolved dynamically per runtime/scope.\n');
}

async function runDoctorCommand(defaults, context, json) {
  const runtimeIds = resolveDoctorRuntimeIds(defaults);
  const result = await runDoctor({
    runtimeIds,
    scope: defaults.scope,
    context,
    silent: json,
  });

  if (json) {
    writeJson({
      ok: result.allPassed,
      command: 'doctor',
      scope: defaults.scope,
      runtimeIds,
      allPassed: result.allPassed,
      checks: result.checks,
    });
  }

  if (!result.allPassed) {
    process.exitCode = 1;
  }
}

export async function runCli(argv) {
  const program = new Command();
  const runtimeHelp = getRuntimeOptionHelp();
  const scopeHelp = getScopeOptionHelp();

  program
    .name(CLI_NAME)
    .description('Bootstrap insentek-openapi skill for OpenClaw and Claude Code')
    .option('--json', 'Output machine-readable JSON to stdout', false)
    .version(pkg.version, '-V, --version', 'Show package version');

  program
    .command('install', { isDefault: true })
    .description('Install skill to selected runtime')
    .option('-r, --runtime <names>', `Runtime: ${runtimeHelp}`)
    .option('-s, --scope <scope>', `Scope: ${scopeHelp}`, 'global')
    .option('-f, --force', 'Overwrite existing installation', false)
    .option('-y, --yes', 'Skip prompts (requires --runtime)', false)
    .action(async (opts, command) => {
      const json = getJsonFlag(command);
      assertNonInteractive(json, opts.yes, 'install');

      if (!json) {
        printWelcome();
      }

      const defaults = buildOptions(opts);
      const context = buildCommandContext();
      let finalOptions;
      if (defaults.yes) {
        const runtimeIds = await resolveRuntimeIdsFromOptions(defaults);
        validateScopeForRuntimes(runtimeIds, defaults.scope);
        finalOptions = { runtimeIds, scope: defaults.scope, force: defaults.force };
      } else {
        finalOptions = await promptInstallOptions(defaults);
      }

      const connection = await ensureCredentialsForInstall({
        yes: defaults.yes,
        silent: json,
      });

      if (!json) {
        printInfo(`Installing ${SKILL_ID} v${pkg.version}...`);
      }

      const results = await installSkills({ ...finalOptions, context, silent: json });

      if (json) {
        writeJson({
          ok: true,
          command: 'install',
          results: results.map(serializeInstallResult),
        });
        return;
      }

      printInstallSummary(results);
      printInstallCredentialHint(connection);
    });

  program
    .command('update')
    .description('Update installed skill to bundled version')
    .option('-r, --runtime <names>', `Runtime: ${runtimeHelp}`)
    .option('-s, --scope <scope>', `Scope: ${scopeHelp}`, 'global')
    .option('-y, --yes', 'Skip prompts (requires --runtime)', false)
    .action(async (opts, command) => {
      const json = getJsonFlag(command);
      assertNonInteractive(json, opts.yes, 'update');

      const defaults = buildOptions(opts);
      const context = buildCommandContext();
      const runtimeIds = await resolveRuntimeIdsFromOptions({
        runtime: defaults.runtime,
        yes: defaults.yes,
        promptMessage: 'Select AI agent runtime to update',
      });
      validateScopeForRuntimes(runtimeIds, defaults.scope);

      if (!json) {
        printInfo(`Updating ${SKILL_ID}...`);
      }

      const results = await updateSkills({
        runtimeIds,
        scope: defaults.scope,
        context,
        silent: json,
      });

      if (json) {
        writeJson({
          ok: true,
          command: 'update',
          results: results.map(serializeUpdateResult),
        });
        return;
      }

      printUpdateSummary(results);
    });

  program
    .command('uninstall')
    .description('Remove installed skill files')
    .option('-r, --runtime <names>', `Runtime: ${runtimeHelp}`)
    .option('-s, --scope <scope>', `Scope: ${scopeHelp}`, 'global')
    .option('-y, --yes', 'Skip prompts (requires --runtime)', false)
    .action(async (opts, command) => {
      const json = getJsonFlag(command);
      assertNonInteractive(json, opts.yes, 'uninstall');

      const defaults = buildOptions(opts);
      const context = buildCommandContext();
      const runtimeIds = await resolveRuntimeIdsFromOptions({
        runtime: defaults.runtime,
        yes: defaults.yes,
        promptMessage: 'Select AI agent runtime to uninstall',
      });
      validateScopeForRuntimes(runtimeIds, defaults.scope);

      if (!defaults.yes) {
        const confirmed = await confirm({
          message: `Remove ${SKILL_ID} from ${runtimeIds.join(', ')} (${defaults.scope})?`,
          default: false,
        });
        if (!confirmed) {
          if (json) {
            writeJson({ ok: true, command: 'uninstall', cancelled: true, results: [] });
          } else {
            printInfo('Cancelled.');
          }
          return;
        }
      }

      const results = await uninstallSkills({
        runtimeIds,
        scope: defaults.scope,
        context,
        silent: json,
      });

      if (json) {
        writeJson({
          ok: true,
          command: 'uninstall',
          results: results.map(serializeUninstallResult),
        });
      }
    });

  program
    .command('status')
    .description('Show installation status')
    .option('-r, --runtime <names>', `Runtime: ${runtimeHelp}`)
    .option('-s, --scope <scope>', `Scope: ${scopeHelp}`, 'global')
    .action(async (opts, command) => {
      const json = getJsonFlag(command);
      const defaults = buildOptions(opts);
      const context = buildCommandContext();
      const runtimeIds = resolveStatusRuntimeIds(defaults);
      const statuses = await getStatuses({
        runtimeIds,
        scope: defaults.scope,
        context,
      });

      if (json) {
        writeJson({
          ok: true,
          command: 'status',
          scope: defaults.scope,
          results: statuses.map(serializeStatus),
        });
        return;
      }

      printStatusTable(statuses);
    });

  program
    .command('doctor')
    .description('Diagnose runtime paths, manifest, scripts and environment')
    .option('-r, --runtime <names>', `Runtime: ${runtimeHelp}`)
    .option('-s, --scope <scope>', `Scope: ${scopeHelp}`, 'global')
    .action(async (opts, command) => {
      const defaults = buildOptions(opts);
      await runDoctorCommand(defaults, buildCommandContext(), getJsonFlag(command));
    });

  program
    .command('info')
    .description('Show package, skill manifest and resolved install locations')
    .option('-s, --scope <scope>', `Scope: ${scopeHelp}`, 'global')
    .action((opts, command) => {
      const json = getJsonFlag(command);
      const context = buildCommandContext();

      if (json) {
        writeJson(buildInfoPayload(context));
        return;
      }

      printWelcome();
      buildOptions(opts);
      console.log('Supported runtimes:\n');
      for (const id of RUNTIME_IDS) {
        console.log(`  ${RUNTIMES[id].label}:`);
        for (const scope of getScopesForRuntime(id)) {
          const location = resolveInstallLocation(id, scope, context);
          console.log(`    • [${scope}] ${formatPath(location.installDir)}`);
          if (location.candidates.length > 1) {
            console.log(`      candidates: ${location.candidates.map(formatPath).join(' | ')}`);
          }
        }
        console.log('');
      }
      console.log(`Quick start:\n  npx ${PACKAGE_NAME}\n`);
    });

  program
    .command('login')
    .description('Configure Insentek API credentials (encrypted local storage)')
    .option('--appid <id>', 'App ID (non-interactive)')
    .option('--secret <secret>', 'App Secret (non-interactive)')
    .option('-y, --yes', 'Overwrite existing credentials without prompting', false)
    .action(async (opts, command) => {
      const json = getJsonFlag(command);
      try {
        const result = await runLogin({
          yes: opts.yes,
          appid: opts.appid,
          secret: opts.secret,
          json,
        });
        if (json) {
          writeJson(result);
        }
      } catch (error) {
        if (json) {
          writeJson({ ok: false, command: 'login', error: error.message });
        } else {
          console.error(`Login failed: ${error.message}`);
        }
        process.exitCode = 1;
      }
    });

  program
    .command('logout')
    .description('Remove saved Insentek API credentials')
    .action(async (_opts, command) => {
      const json = getJsonFlag(command);
      const result = await runLogout({ json });
      if (json) {
        writeJson(result);
      }
    });

  const auth = program
    .command('auth')
    .description('Manage Insentek API credentials');

  auth
    .command('status')
    .description('Show credential connection status')
    .action(async (_opts, command) => {
      const json = getJsonFlag(command);
      const result = await runAuthStatus({ json });
      if (json) {
        writeJson(result);
      }
    });

  program
    .command('check')
    .description('Alias of doctor')
    .option('-r, --runtime <names>', `Runtime: ${runtimeHelp}`)
    .option('-s, --scope <scope>', `Scope: ${scopeHelp}`, 'global')
    .action(async (opts, command) => {
      const defaults = buildOptions(opts);
      await runDoctorCommand(defaults, buildCommandContext(), getJsonFlag(command));
    });

  await program.parseAsync(argv);
}
