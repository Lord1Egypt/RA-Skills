import assert from 'node:assert/strict';
import { chmodSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import test from 'node:test';

const skillRoot = resolve(import.meta.dirname, '..');

test('connector health defaults to a 6 hour cadence', () => {
  const config = JSON.parse(
    readFileSync(join(skillRoot, 'data/openclaw-growth-engineer/config.example.json'), 'utf8'),
  );
  const runner = readFileSync(join(skillRoot, 'scripts/openclaw-growth-runner.mjs'), 'utf8');
  const start = readFileSync(join(skillRoot, 'scripts/openclaw-growth-start.mjs'), 'utf8');

  assert.equal(config.schedule.connectorHealthCheckIntervalMinutes, 360);
  assert.match(runner, /DEFAULT_CONNECTOR_HEALTH_INTERVAL_MINUTES = 360/);
  assert.match(start, /connectorHealthCheckIntervalMinutes/);
  assert.match(start, /Math\.min/);
});

test('ASC access answers come from Growth Engineer status, not loaded chat tools', () => {
  const skill = readFileSync(join(skillRoot, 'SKILL.md'), 'utf8');
  const start = readFileSync(join(skillRoot, 'scripts/openclaw-growth-start.mjs'), 'utf8');
  const bootstrap = readFileSync(join(skillRoot, 'scripts/bootstrap-openclaw-workspace.sh'), 'utf8');

  assert.match(skill, /Growth Engineer connectors are local CLI\/secrets-backed sources, not chat\/MCP tools/);
  assert.match(skill, /ASC\/App Store Connect is not expected to appear as a loaded chat tool/);
  assert.match(skill, /never inspect loaded tools/);
  assert.match(skill, /node scripts\/openclaw-growth-status\.mjs --config <config> --json --only-connectors asc/);
  assert.match(skill, /If ASC status\/setup reports pass, connected, healthy, or the wizard just finished ASC connector setup successfully/);
  assert.match(skill, /Yes\. ASC analytics is connected through Growth Engineer local asc CLI\/API-key setup/);
  assert.match(start, /ASC\/App Store Connect is a Growth Engineer local CLI connector, not a chat tool/);
  assert.match(start, /never answer no because no Apple tool is callable/);
  assert.match(start, /setup just finished successfully, answer exactly: Yes\. ASC analytics is connected through Growth Engineer local asc CLI\/API-key setup/);
  assert.match(start, /openclaw-growth-status\.mjs --config .* --json --only-connectors asc/);
  assert.match(bootstrap, /ASC\/App Store Connect is a Growth Engineer local CLI connector, not a chat tool/);
  assert.match(bootstrap, /never answer no because no Apple tool is callable/);
  assert.match(bootstrap, /answer exactly: Yes\. ASC analytics is connected through Growth Engineer local asc CLI\/API-key setup/);
});

test('connector wizard can refresh OpenClaw session instructions after setup changes', () => {
  const wizard = readFileSync(join(skillRoot, 'scripts/openclaw-growth-wizard.mjs'), 'utf8');

  assert.match(wizard, /Update OpenClaw runtime and heartbeat files now/);
  assert.match(wizard, /maybeRefreshOpenClawSessionInstructions\(rl, args\.config\)/);
  assert.match(wizard, /let ascBootstrapRevokeEnv/);
  assert.match(wizard, /ascBootstrapRevokeEnv = bootstrapEnv/);
  assert.match(wizard, /if \(ascBootstrapRevokeEnv\)\s*\{\s*printAscBootstrapAdminRevokeNotice\(ascBootstrapRevokeEnv\)/);
  assert.match(wizard, /refreshWorkspaceRuntimeFromCurrentWizard/);
  assert.match(wizard, /writeOpenClawHeartbeat/);
  assert.match(wizard, /writeOpenClawSessionNote/);
  assert.match(wizard, /OpenClaw files updated/);
  assert.match(wizard, /ASC will not appear as a chat tool/);
  assert.match(wizard, /If an existing OpenClaw chat still checks loaded tools/);
  assert.match(wizard, /OPENCLAW_GROWTH_REFRESH_OPENCLAW_SESSION/);
  assert.match(wizard, /HEARTBEAT_MARKER_START/);
  assert.match(wizard, /never answer no because no Apple tool is callable/);
  assert.match(wizard, /ascAnswerPolicy/);
  assert.match(wizard, /Do not answer no only because no App Store Connect chat tool is callable/);
  assert.match(wizard, /If ASC setup just finished with SUCCESS, answer: Yes\. ASC analytics is connected through Growth Engineer local asc CLI\/API-key setup/);
});

test('connector wizard does not recheck unrelated connectors after focused setup', () => {
  const wizard = readFileSync(join(skillRoot, 'scripts/openclaw-growth-wizard.mjs'), 'utf8');

  assert.match(wizard, /const requestedConnectors = args\.connectors \? parseConnectorList\(args\.connectors\) : \[\]/);
  assert.match(wizard, /requestedConnectors\.length > 0\s*\?\s*orderConnectors\(requestedConnectors\)\s*:\s*await connectorKeysForHealthCheck\(args\.config\)/);
  assert.match(wizard, /setupOk = await runConnectorSetupSteps/);
  assert.match(wizard, /if \(!setupOk\)\s+return 'done'/);
  assert.match(wizard, /return 'done'/);
});

test('wizard supports back navigation in menus and connector setup', () => {
  const wizard = readFileSync(join(skillRoot, 'scripts/openclaw-growth-wizard.mjs'), 'utf8');

  assert.match(wizard, /class WizardBackError extends Error/);
  assert.match(wizard, /Use Esc\/← in menus or type :back in text prompts to return/);
  assert.match(wizard, /Esc\/← back\. Ctrl\+C cancels/);
  assert.match(wizard, /function isBackAnswer/);
  assert.match(wizard, /return \[':back', '\\x1b'\]\.includes\(normalized\)/);
  assert.match(wizard, /async function askQuestionWithEscBack/);
  assert.match(wizard, /controller\.abort\(\)/);
  assert.match(wizard, /await askQuestionWithEscBack\(rl,/);
  assert.match(wizard, /if \(isBackAnswer\(answer\)\)\s+throw new WizardBackError/);
  assert.match(wizard, /if \(key\?\.name === 'escape' \|\| key\?\.name === 'left'\)/);
  assert.match(wizard, /while \(true\)\s*\{\s*clearTerminal\(\);\s*printConnectorIntro/);
  assert.match(wizard, /if \(error instanceof WizardBackError\)\s+continue/);
  assert.match(wizard, /const result = await runConnectorSetupWizard/);
  assert.match(wizard, /if \(result === 'back'\)\s+continue/);
});

test('unchanged unhealthy connectors are retried until an external alert is delivered', () => {
  const runner = readFileSync(join(skillRoot, 'scripts/openclaw-growth-runner.mjs'), 'utf8');

  assert.match(runner, /previousExternallyDeliveredFingerprint !== fingerprint/);
  assert.match(runner, /activeIncidentFingerprint = fingerprint/);
  assert.match(runner, /lastExternalAlertedFingerprint = fingerprint/);
  assert.match(runner, /hasSuccessfulExternalDelivery\(deliveries\)/);
  assert.match(runner, /connector_health_unchanged/);
  assert.match(runner, /persisted unhealthy state is not a new event/);
  assert.match(runner, /alertTriggered \? 'CONNECTOR_HEALTH_ALERT' : 'HEARTBEAT_OK'/);
  assert.doesNotMatch(runner, /isDue\(healthState\.lastAlertedAt, intervalMinutes\)/);
});

test('notification delivery fallbacks are merged with explicit channels', () => {
  const runner = readFileSync(join(skillRoot, 'scripts/openclaw-growth-runner.mjs'), 'utf8');
  const wizard = readFileSync(join(skillRoot, 'scripts/openclaw-growth-wizard.mjs'), 'utf8');

  assert.match(runner, /function mergeNotificationChannelsWithDeliveries/);
  assert.match(runner, /getDeliveryNotificationChannels\(config, 'connectorHealth'\)/);
  assert.match(runner, /getDeliveryNotificationChannels\(config, 'growthRun'\)/);
  assert.match(runner, /if \(type === 'command'\)\s+return `command:\$\{channel\?\.label \|\| channel\?\.command \|\| 'command'\}`/);
  assert.match(runner, /deliveries\.command\?\.enabled/);
  assert.match(runner, /external: false/);
  assert.match(runner, /Alert written locally, but no external notification channel configured/);
  assert.doesNotMatch(runner, /if \(configuredChannels\.length > 0\)\s*return configuredChannels/);
  assert.doesNotMatch(runner, /discord-openclaw-bridge/);
  assert.doesNotMatch(wizard, /discord-openclaw-bridge/);
});

test('discord deliveries use embeds and hide successful message ids from state details', () => {
  const runner = readFileSync(join(skillRoot, 'scripts/openclaw-growth-runner.mjs'), 'utf8');
  const bridge = readFileSync(resolve(skillRoot, '../../scripts/discord-openclaw-bridge.mjs'), 'utf8');
  const skillBridge = readFileSync(join(skillRoot, 'scripts/discord-openclaw-bridge.mjs'), 'utf8');
  const shared = readFileSync(join(skillRoot, 'scripts/openclaw-growth-shared.mjs'), 'utf8');

  assert.match(runner, /type: 'discord'/);
  assert.match(runner, /buildDiscordConnectorHealthPayload/);
  assert.match(runner, /buildDiscordGrowthRunPayload/);
  assert.match(runner, /OPENCLAW_DISCORD_DELIVERY_FORMAT: 'embed'/);
  assert.match(runner, /detail: result\.ok \? 'sent'/);
  assert.match(bridge, /normalizeEmbedPayload/);
  assert.match(bridge, /structuredTextToEmbedPayload/);
  assert.match(bridge, /buildStructuredOpenClawDailyPayload/);
  assert.match(bridge, /buildStructuredConnectorPayload/);
  assert.match(bridge, /return structuredTextToEmbedPayload\(raw\)/);
  assert.match(bridge, /chunkMessage\(content\)/);
  assert.match(bridge, /embeds: payload\.embeds/);
  assert.match(skillBridge, /normalizeEmbedPayload/);
  assert.match(skillBridge, /structuredTextToEmbedPayload/);
  assert.match(shared, /Never mention successful delivery metadata/);
});

test('ASC vendor setup uses only ASC_VENDOR_NUMBER', () => {
  const removedVendorAlias = ['ASC', 'ANALYTICS', 'VENDOR', 'NUMBER'].join('_');
  const files = [
    'scripts/openclaw-growth-status.mjs',
    'scripts/openclaw-growth-wizard.mjs',
    'scripts/export-asc-summary.mjs',
    'scripts/openclaw-growth-shared.mjs',
  ];

  for (const file of files) {
    const source = readFileSync(join(skillRoot, file), 'utf8');
    assert.doesNotMatch(source, new RegExp(removedVendorAlias));
  }
});

test('ASC analytics commands avoid state filter and use a longer default timeout', () => {
  const start = readFileSync(join(skillRoot, 'scripts/openclaw-growth-start.mjs'), 'utf8');
  const exporter = readFileSync(join(skillRoot, 'scripts/export-asc-summary.mjs'), 'utf8');

  assert.match(start, /ASC_TIMEOUT_SECONDS: normalizeString\(process\.env\.ASC_TIMEOUT_SECONDS\) \|\| DEFAULT_ASC_TIMEOUT_SECONDS/);
  assert.match(exporter, /--command-timeout-ms <n>/);
  assert.match(exporter, /delete env\.ASC_TIMEOUT_SECONDS/);
  assert.match(exporter, /delete env\.ASC_VENDOR_NUMBER/);
  assert.doesNotMatch(exporter, /'--state',\s*'COMPLETED'/);
});

test('successful setup progress clears non-blocking preflight attention state', () => {
  const wizard = readFileSync(join(skillRoot, 'scripts/openclaw-growth-wizard.mjs'), 'utf8');

  assert.match(wizard, /function reconcileSuccessfulSetupProgress/);
  assert.match(wizard, /passed with non-blocking checks/);
  assert.match(wizard, /if \(result\.ok\)\s*\{\s*reconcileSuccessfulSetupProgress\(plan\)/);
});

test('connector picker honors active runner health incidents', () => {
  const wizard = readFileSync(join(skillRoot, 'scripts/openclaw-growth-wizard.mjs'), 'utf8');

  assert.match(wizard, /function readActiveConnectorIncidents/);
  assert.match(wizard, /state\?\.connectorHealth/);
  assert.match(wizard, /activeIncidentFingerprint/);
  assert.match(wizard, /lastAlertJsonPath/);
  assert.match(wizard, /function mergeActiveConnectorIncidents/);
  assert.match(wizard, /if \(liveHealth\.status === 'connected'\)\s*\{\s*return \[key, liveHealth\]/);
  assert.doesNotMatch(wizard, /Live wizard check passed, but the runner still has an active/);
  assert.match(wizard, /connectorKeyFromRunnerHealthKey/);
  assert.match(wizard, /if \(normalized === 'appStoreConnect'\)\s+return 'asc'/);
  assert.match(wizard, /return mergeActiveConnectorIncidents\(liveHealth, activeIncidents\)/);
});

test('due growth cadences still run and log, but suppress social delivery when findings are unchanged', () => {
  const runner = readFileSync(join(skillRoot, 'scripts/openclaw-growth-runner.mjs'), 'utf8');

  assert.match(runner, /skippedReason: 'cadence_not_due'/);
  assert.doesNotMatch(runner, /activeCadences\.length === 0 &&\s+unchangedIssueSet/);
  assert.match(runner, /Skip GitHub creation and external growth notification/);
  assert.match(runner, /issue set unchanged; external growth notification suppressed/);
  assert.match(runner, /externalGrowthNotification: 'suppressed_unchanged_issue_set'/);
  assert.match(runner, /issueSetChangedOrExplicitlyAllowed/);
  assert.match(runner, /lastGrowthRunNotifications: await deliverGrowthRunSummary/);
});

test('short operational findings are deduped per issue per day unless events spike', () => {
  const runner = readFileSync(join(skillRoot, 'scripts/openclaw-growth-runner.mjs'), 'utf8');

  assert.match(runner, /DEFAULT_DAILY_ISSUE_EVENT_GROWTH_MULTIPLIER = 2/);
  assert.match(runner, /DEFAULT_DAILY_ISSUE_EVENT_GROWTH_MIN_DELTA = 10/);
  assert.match(runner, /function applyDailyIssueDedupe/);
  assert.match(runner, /function buildDailyIssueKey/);
  assert.match(runner, /function issueEventCount/);
  assert.match(runner, /isDrasticDailyIssueEventGrowth/);
  assert.match(runner, /skippedReason: 'daily_issue_dedupe'/);
  assert.match(runner, /externalGrowthNotification: 'suppressed_daily_issue_dedupe'/);
  assert.match(runner, /Suppressed today: \$\{suppressedIssueCount\} previously reported finding\(s\)\./);
  assert.doesNotMatch(runner, /dailyIssueDedupe\.suppressedCount === 0/);
});

test('scheduled source collection retries transient upstream failures once', () => {
  const runner = readFileSync(join(skillRoot, 'scripts/openclaw-growth-runner.mjs'), 'utf8');

  assert.match(runner, /function isTransientNetworkFailure/);
  assert.match(runner, /function isRequiredSource/);
  assert.match(runner, /upstream connect error/);
  assert.match(runner, /disconnect\\\/reset before headers/);
  assert.match(runner, /isTransientNetworkFailure\(result\.stderr \|\| result\.stdout\)/);
  assert.match(runner, /transient network error persisted after retry/);
  assert.match(runner, /lastRetriedTransientFailureAt/);
  assert.match(runner, /source_collection_degraded/);
  assert.match(runner, /lastSourceFailures/);
  assert.match(runner, /socialOutput: 'HEARTBEAT_OK'/);
});

test('required analytics transient fetch failures degrade without failing repeated scheduled runs', () => {
  const tmp = mkdtempSync(join(tmpdir(), 'openclaw-growth-analytics-transient-'));
  try {
    const binDir = join(tmp, 'bin');
    mkdirSync(binDir, { recursive: true });
    const analyticscliBin = join(binDir, 'analyticscli');
    writeFileSync(analyticscliBin, '#!/bin/sh\nexit 0\n', 'utf8');
    chmodSync(analyticscliBin, 0o755);

    const failingSource = join(tmp, 'failing-analytics.mjs');
    writeFileSync(failingSource, 'process.stderr.write("fetch failed\\n"); process.exit(1);\n', 'utf8');

    const notifier = join(tmp, 'notify.mjs');
    writeFileSync(notifier, 'process.stdin.resume();\n', 'utf8');

    const configPath = join(tmp, 'config.json');
    const statePath = join(tmp, 'state.json');
    const now = new Date().toISOString();
    const cadenceState = Object.fromEntries(
      ['healthcheck', 'daily', 'weekly', 'monthly', 'quarterly', 'six_months', 'yearly'].map((key) => [
        key,
        { lastRanAt: now, title: key },
      ]),
    );
    writeFileSync(
      configPath,
      `${JSON.stringify(
        {
          version: 7,
          project: { repoRoot: tmp },
          schedule: { connectorHealthCheckIntervalMinutes: 360 },
          sources: {
            analytics: {
              enabled: true,
              required: true,
              mode: 'command',
              command: `node ${failingSource}`,
            },
          },
          notifications: {
            connectorHealth: {
              channels: [{ type: 'command', label: 'test_external', command: `node ${notifier}` }],
            },
          },
        },
        null,
        2,
      )}\n`,
      'utf8',
    );
    writeFileSync(
      statePath,
      `${JSON.stringify(
        {
          sourceHashes: {},
          sourceCursors: {},
          lastRunAt: now,
          cadences: cadenceState,
          connectorHealth: {
            lastCheckedAt: now,
            lastStatusOk: true,
          },
        },
        null,
        2,
      )}\n`,
      'utf8',
    );

    const env = { ...process.env, PATH: `${binDir}:${process.env.PATH || ''}` };
    const args = [
      join(skillRoot, 'scripts/openclaw-growth-runner.mjs'),
      '--no-self-update',
      '--config',
      configPath,
      '--state',
      statePath,
    ];
    const first = spawnSync(process.execPath, args, { cwd: tmp, env, encoding: 'utf8' });
    assert.equal(first.status, 0, first.stderr || first.stdout);
    const second = spawnSync(process.execPath, args, { cwd: tmp, env, encoding: 'utf8' });
    assert.equal(second.status, 0, second.stderr || second.stdout);

    const state = JSON.parse(readFileSync(statePath, 'utf8'));
    assert.equal(state.connectorHealth.lastStatusOk, false);
    assert.equal(state.lastSourceFailures?.[0]?.key, 'analytics');
    assert.match(state.lastSourceFailures?.[0]?.detail || '', /transient network error persisted after retry/);

    const proofPath = join(tmp, 'runtime/scheduler-proof.jsonl');
    const proofEvents = readFileSync(proofPath, 'utf8')
      .trim()
      .split('\n')
      .map((line) => JSON.parse(line));
    const sourceCollectionEvents = proofEvents.filter(
      (event) => event.event === 'source_collection_degraded' && Object.hasOwn(event, 'alertTriggered'),
    );
    assert.equal(sourceCollectionEvents.at(-1)?.alertTriggered, false);
    assert.equal(sourceCollectionEvents.at(-1)?.socialOutput, 'HEARTBEAT_OK');
    assert.equal(proofEvents.some((event) => event.event === 'runner_failed'), false);
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
});

test('required source transient API failures are degraded after retry', () => {
  const runner = readFileSync(join(skillRoot, 'scripts/openclaw-growth-runner.mjs'), 'utf8');

  assert.match(runner, /function isSentryCompatibleSource/);
  assert.match(runner, /sourceKey === 'sentry'/);
  assert.match(runner, /sourceKey === 'glitchtip'/);
  assert.match(runner, /command\.includes\('export-sentry-summary'\)/);
  assert.match(runner, /function shouldDegradeTransientSourceFailure/);
  assert.match(runner, /sourceConfig\?\.degradeTransientFailures === false/);
  assert.match(runner, /if \(!isRequiredSource\(sourceConfig, sourceName\)\)\s+return true/);
  assert.match(runner, /if \(isSentryCompatibleSource\(sourceConfig, sourceName\)\)\s+return true/);
  assert.match(runner, /degradeRequiredTransientFailures !== false/);
  assert.match(runner, /shouldDegradeTransientSourceFailure\(sourceConfig, sourceName, retried\)/);
});

test('runner self-update uses the installed Growth Engineer skill slug', () => {
  const runner = readFileSync(join(skillRoot, 'scripts/openclaw-growth-runner.mjs'), 'utf8');

  assert.match(runner, /SELF_UPDATE_SKILL_SLUG_CANDIDATES = \['growth-engineer', 'openclaw-growth-engineer'\]/);
  assert.match(runner, /OPENCLAW_GROWTH_SKILL_SLUG/);
  assert.match(runner, /function resolveInstalledSelfUpdateSkill/);
  assert.match(runner, /skills\/growth-engineer\/scripts/);
  assert.match(runner, /clawhub --no-input --dir skills update \$\{quote\(installedSkill\.slug\)\} --force/);
  assert.match(runner, /installedSkill\.bootstrapPath/);
  assert.doesNotMatch(runner, /skills update openclaw-growth-engineer --force/);
  assert.doesNotMatch(runner, /bash skills\/openclaw-growth-engineer\/scripts\/bootstrap-openclaw-workspace\.sh/);
});

test('wizard self-update uses the installed Growth Engineer skill slug', () => {
  const wizard = readFileSync(join(skillRoot, 'scripts/openclaw-growth-wizard.mjs'), 'utf8');

  assert.match(wizard, /SELF_UPDATE_SKILL_SLUG_CANDIDATES = \['growth-engineer', 'openclaw-growth-engineer'\]/);
  assert.match(wizard, /OPENCLAW_GROWTH_SKILL_SLUG/);
  assert.match(wizard, /function resolveInstalledSelfUpdateSkill/);
  assert.match(wizard, /skills\/growth-engineer\/scripts/);
  assert.match(wizard, /clawhub --no-input --dir skills update \$\{quote\(installedSkill\.slug\)\} --force/);
  assert.match(wizard, /installedSkill\.bootstrapPath/);
  assert.doesNotMatch(wizard, /SELF_UPDATE_INTERVAL_MS/);
  assert.doesNotMatch(wizard, /shouldRunSelfUpdate/);
  assert.doesNotMatch(wizard, /Date\.now\(\) - lastCheckedAt/);
  assert.doesNotMatch(wizard, /skills update openclaw-growth-engineer --force/);
  assert.doesNotMatch(wizard, /bash skills\/openclaw-growth-engineer\/scripts\/bootstrap-openclaw-workspace\.sh/);
});

test('Sentry exporter retries retryable API failures before surfacing the error', () => {
  const exporter = readFileSync(join(skillRoot, 'scripts/export-sentry-summary.mjs'), 'utf8');

  assert.match(exporter, /DEFAULT_SENTRY_FETCH_RETRIES = 3/);
  assert.match(exporter, /DEFAULT_SENTRY_REQUEST_TIMEOUT_MS = 15_000/);
  assert.match(exporter, /DEFAULT_SENTRY_FETCH_CONCURRENCY = 3/);
  assert.match(exporter, /function isRetryableSentryStatus/);
  assert.match(exporter, /status === 429 \|\| status >= 500/);
  assert.match(exporter, /function isRetryableSentryError/);
  assert.match(exporter, /function compactErrorDetail/);
  assert.match(exporter, /AbortController/);
  assert.match(exporter, /OPENCLAW_SENTRY_REQUEST_TIMEOUT_MS/);
  assert.match(exporter, /OPENCLAW_SENTRY_FETCH_CONCURRENCY/);
  assert.match(exporter, /retry-after/);
  assert.match(exporter, /Sentry API \$\{response\.status\}/);
  assert.match(exporter, /function describeAccountTarget/);
  assert.match(exporter, /baseUrl=\$\{account\.baseUrl \|\| DEFAULT_BASE_URL\}/);
  assert.match(exporter, /project=\$\{account\.project\}/);
  assert.match(exporter, /environment=\$\{account\.environment\}/);
  assert.match(exporter, /withAccountTargetError\(error, account, 'Sentry issue fetch'\)/);
  assert.match(exporter, /withAccountTargetError\(error, account, 'Sentry project discovery'\)/);
});

test('Sentry exporter keeps transient provider failures out of connector-health alerts', () => {
  const exporter = readFileSync(join(skillRoot, 'scripts/export-sentry-summary.mjs'), 'utf8');

  assert.match(exporter, /function dedupeAccountConfigs/);
  assert.match(exporter, /return dedupeAccountConfigs\(normalized\)/);
  assert.match(exporter, /function buildFailureRecord/);
  assert.match(exporter, /function attachFailureMeta/);
  assert.match(exporter, /partial: true/);
  assert.match(exporter, /failureCount: failures\.length/);
  assert.match(exporter, /await mapLimit\(accounts, sentryFetchConcurrency\(\)/);
  assert.match(exporter, /eventsPerIssue: 0/);
  assert.match(exporter, /default: 0/);
  assert.match(exporter, /const blockingFailures = failures\.filter\(\(failure\) => !failure\.retryable && failure\.action !== 'issue_event_fetch'\)/);
  assert.match(exporter, /Sentry connector has non-retryable configuration\/auth failures/);
  assert.doesNotMatch(exporter, /throw withAccountTargetError\(error, account, 'Sentry project discovery'\)/);
});

test('short operational growth notifications stay compact', () => {
  const runner = readFileSync(join(skillRoot, 'scripts/openclaw-growth-runner.mjs'), 'utf8');

  assert.match(runner, /function truncateMessageText/);
  assert.match(runner, /function groupIssuesByProject/);
  assert.match(runner, /function issueSourceUrl/);
  assert.match(runner, /OpenClaw healthcheck/);
  assert.match(runner, /OpenClaw daily/);
  assert.match(runner, /Top by project:/);
  assert.match(runner, /formatIssueSummaryLine/);
  assert.match(runner, /Action: external alert only\./);
  assert.doesNotMatch(runner, /Sources: \$\{sourceNames\}/);
  assert.doesNotMatch(runner, /Action: alert\/handoff only; GitHub auto-create is disabled or unavailable\./);
});

test('Sentry connector setup cannot report success with disabled or placeholder-only config', () => {
  const wizard = readFileSync(join(skillRoot, 'scripts/openclaw-growth-wizard.mjs'), 'utf8');
  const preflight = readFileSync(join(skillRoot, 'scripts/openclaw-growth-preflight.mjs'), 'utf8');

  assert.match(wizard, /function isPlaceholderSentryAccount/);
  assert.match(wizard, /owner-org/);
  assert.match(wizard, /example\.com/);
  assert.match(wizard, /function verifySentryAccountsConfig/);
  assert.match(wizard, /sources\.sentry\.enabled is not true/);
  assert.match(wizard, /Sentry-compatible account config is up to date/);
  assert.match(wizard, /--only-connectors \$\{quote\(selected\.join\(','\)\)\}/);
  assert.match(preflight, /selected Sentry connector is still disabled in sources\.sentry/);
});

test('AnalyticsCLI-only connector setup reports configured ASC failures without blaming AnalyticsCLI', () => {
  const start = readFileSync(join(skillRoot, 'scripts/openclaw-growth-start.mjs'), 'utf8');
  const wizard = readFileSync(join(skillRoot, 'scripts/openclaw-growth-wizard.mjs'), 'utf8');

  assert.match(start, /const shouldRunAscSetup = args\.onlyConnectors\.length === 0/);
  assert.match(start, /args\.onlyConnectors\.includes\('asc'\)/);
  assert.match(start, /configHasEnabledAscSource\(initialConfig\)/);
  assert.match(start, /appScope: 'skipped_by_connector_filter'/);
  assert.match(start, /detail: 'ASC connector was not selected'/);
  assert.match(wizard, /App Store Connect\|app-store-connect\|app_store_connect\|Analytics Report Request/);
  assert.match(wizard, /return 'asc';\s+if \(value\.includes\('analytics'\) \|\| value\.includes\('ANALYTICSCLI'\)\)/);
  assert.match(wizard, /function payloadOtherConnectorFailures/);
  assert.match(wizard, /another configured connector needs attention/);
});

test('wizard persists active config paths for config-driven exporters', () => {
  const wizard = readFileSync(join(skillRoot, 'scripts/openclaw-growth-wizard.mjs'), 'utf8');

  assert.match(wizard, /function sourceCommandNeedsActiveConfig/);
  assert.match(wizard, /value\.includes\('export-sentry-summary'\)/);
  assert.match(wizard, /value\.includes\('exporters coolify-summary'\)/);
  assert.match(wizard, /function withWizardConfigArg/);
  assert.match(wizard, /--config \$\{quote\(configPath\)\}/);
  assert.match(wizard, /migrateRuntimeSourceCommands\(existing, configPath\)/);
  assert.match(wizard, /normalizeWizardSourceCommand\('sentry', config\.sources\?\.sentry \|\| \{\}, configPath\)/);
  assert.match(wizard, /buildDefaultWizardConfig\(configPath\)/);
  assert.match(wizard, /buildRecommendedSourceConfig\(configPath\)/);
  assert.match(wizard, /buildSourceConfigFromInputChannels\(selected, config\.sources \|\| \{\}, configPath\)/);
});

test('wizard sandbox smoke migrates Sentry and Coolify commands to the active config', () => {
  const tmp = mkdtempSync(join(tmpdir(), 'openclaw-growth-sandbox-'));
  try {
    const configPath = join(tmp, 'custom-config.json');
    writeFileSync(
      configPath,
      `${JSON.stringify({
        version: 7,
        sources: {
          sentry: {
            enabled: true,
            mode: 'command',
            command: 'node scripts/export-sentry-summary.mjs',
            accounts: [
              {
                id: 'sentry_cloud',
                label: 'Sentry Cloud',
                baseUrl: 'https://sentry.io',
                tokenEnv: 'SENTRY_CLOUD_TOKEN',
                org: 'example-org',
                projects: ['example-app'],
              },
            ],
          },
          coolify: {
            enabled: true,
            mode: 'command',
            command: 'npx -y @analyticscli/growth-engineer exporters coolify-summary',
            baseUrl: 'https://coolify.example.com',
            tokenEnv: 'COOLIFY_API_TOKEN',
          },
          extra: [
            {
              key: 'asc_cli',
              service: 'asc-cli',
              label: 'ASC / App Store Connect CLI',
              enabled: true,
              mode: 'command',
              command: "node '/home/lo/.npm/_npx/9bdf6aa37e0ec220/node_modules/@analyticscli/growth-engineer/dist/runtime/export-asc-summary.mjs' --max-signals 6",
            },
          ],
        },
      }, null, 2)}\n`,
    );

    const result = spawnSync(
      process.execPath,
      [
        join(skillRoot, 'scripts/openclaw-growth-wizard.mjs'),
        '--config',
        configPath,
        '--sandbox-smoke',
      ],
      {
        cwd: tmp,
        env: {
          ...process.env,
          OPENCLAW_GROWTH_SKIP_SELF_UPDATE: '1',
        },
        encoding: 'utf8',
      },
    );

    assert.equal(result.status, 0, result.stderr || result.stdout);
    const migrated = JSON.parse(readFileSync(configPath, 'utf8'));
    assert.match(migrated.sources.sentry.command, /export-sentry-summary\.mjs/);
    assert.match(migrated.sources.sentry.command, new RegExp(`--config ${configPath.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`));
    assert.match(migrated.sources.coolify.command, /exporters coolify-summary/);
    assert.match(migrated.sources.coolify.command, new RegExp(`--config ${configPath.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`));
    assert.match(migrated.sources.extra[0].command, /export-asc-summary\.mjs/);
    assert.match(migrated.sources.extra[0].command, /--max-signals 6/);
    assert.doesNotMatch(migrated.sources.extra[0].command, /node_modules\/@analyticscli\/growth-engineer/);
    assert.doesNotMatch(migrated.sources.extra[0].command, /_npx\/9bdf6aa37e0ec220/);
    assert.doesNotMatch(migrated.sources.sentry.command, /data\/openclaw-growth-engineer\/config\.json/);
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
});

test('wizard persists active config paths for config-driven exporters', () => {
  const wizard = readFileSync(join(skillRoot, 'scripts/openclaw-growth-wizard.mjs'), 'utf8');

  assert.match(wizard, /function sourceCommandNeedsActiveConfig/);
  assert.match(wizard, /value\.includes\('export-sentry-summary'\)/);
  assert.match(wizard, /value\.includes\('exporters coolify-summary'\)/);
  assert.match(wizard, /function withWizardConfigArg/);
  assert.match(wizard, /--config \$\{quote\(configPath\)\}/);
  assert.match(wizard, /migrateRuntimeSourceCommands\(existing, configPath\)/);
  assert.match(wizard, /normalizeWizardSourceCommand\('sentry', config\.sources\?\.sentry \|\| \{\}, configPath\)/);
  assert.match(wizard, /buildDefaultWizardConfig\(configPath\)/);
  assert.match(wizard, /buildRecommendedSourceConfig\(configPath\)/);
  assert.match(wizard, /buildSourceConfigFromInputChannels\(selected, config\.sources \|\| \{\}, configPath\)/);
});

test('wizard sandbox smoke migrates Sentry and Coolify commands to the active config', () => {
  const tmp = mkdtempSync(join(tmpdir(), 'openclaw-growth-sandbox-'));
  try {
    const configPath = join(tmp, 'custom-config.json');
    writeFileSync(
      configPath,
      `${JSON.stringify({
        version: 7,
        sources: {
          sentry: {
            enabled: true,
            mode: 'command',
            command: 'node scripts/export-sentry-summary.mjs',
            accounts: [
              {
                id: 'sentry_cloud',
                label: 'Sentry Cloud',
                baseUrl: 'https://sentry.io',
                tokenEnv: 'SENTRY_CLOUD_TOKEN',
                org: 'example-org',
                projects: ['example-app'],
              },
            ],
          },
          coolify: {
            enabled: true,
            mode: 'command',
            command: 'npx -y @analyticscli/growth-engineer exporters coolify-summary',
            baseUrl: 'https://coolify.example.com',
            tokenEnv: 'COOLIFY_API_TOKEN',
          },
        },
      }, null, 2)}\n`,
    );

    const result = spawnSync(
      process.execPath,
      [
        join(skillRoot, 'scripts/openclaw-growth-wizard.mjs'),
        '--config',
        configPath,
        '--sandbox-smoke',
      ],
      {
        cwd: tmp,
        env: {
          ...process.env,
          OPENCLAW_GROWTH_SKIP_SELF_UPDATE: '1',
        },
        encoding: 'utf8',
      },
    );

    assert.equal(result.status, 0, result.stderr || result.stdout);
    const migrated = JSON.parse(readFileSync(configPath, 'utf8'));
    assert.match(migrated.sources.sentry.command, /export-sentry-summary\.mjs/);
    assert.match(migrated.sources.sentry.command, new RegExp(`--config ${configPath.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`));
    assert.match(migrated.sources.coolify.command, /exporters coolify-summary/);
    assert.match(migrated.sources.coolify.command, new RegExp(`--config ${configPath.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`));
    assert.doesNotMatch(migrated.sources.sentry.command, /data\/openclaw-growth-engineer\/config\.json/);
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
});

test('optional source collection failures become connector-health incidents', () => {
  const runner = readFileSync(join(skillRoot, 'scripts/openclaw-growth-runner.mjs'), 'utf8');

  assert.match(runner, /source_collection_degraded/);
  assert.match(runner, /Source collection failed during scheduled run/);
  assert.match(runner, /Optional source "\$\{source\.key\}" failed; continuing without it/);
  assert.match(runner, /if \(source\.key === 'analytics'\)/);
  assert.match(runner, /recordSourceCollectionFailures/);
  assert.match(runner, /new or changed source-collection connector incident/);
});

test('connector health alerts include direct repair commands without broad menu detours', () => {
  const runner = readFileSync(join(skillRoot, 'scripts/openclaw-growth-runner.mjs'), 'utf8');
  const wizard = readFileSync(join(skillRoot, 'scripts/openclaw-growth-wizard.mjs'), 'utf8');

  assert.match(runner, /OpenClaw connector health: \$\{unhealthyConnectors\.length\} issue/);
  assert.ok(runner.includes('Fix: \\`${command}\\`'));
  assert.match(runner, /SENTRY_AUTH_TOKEN missing for source collection/);
  assert.doesNotMatch(runner, /lines\.push\('  Account targets:'\)/);
  assert.match(runner, /npx -y @analyticscli\/growth-engineer wizard/);
  assert.match(runner, /--connectors \$\{quote\(connector\)\}/);
  assert.doesNotMatch(runner, /nodeRuntimeScriptCommand\('openclaw-growth-wizard\.mjs'\)/);
  assert.doesNotMatch(runner, /ASC web-auth only/);
  assert.doesNotMatch(runner, /asc web auth login/);
  assert.match(runner, /Secrets stay in the host terminal or secret store/);
  assert.match(wizard, /requestedConnectors\.length > 0\s+\? orderConnectors\(requestedConnectors\)/);
  assert.doesNotMatch(wizard, /requestedConnectors\.length > 0\s+\? orderConnectors\(\[\.\.\.new Set\(\[\.\.\.requestedConnectors, \.\.\.existingFixes\]\)\]\)/);
  assert.match(wizard, /return isConnectorLocallyConfigured\(key\) \|\| status !== 'not_connected'/);
  assert.match(wizard, /new Set\(CONNECTOR_KEYS\.filter\(\(key\) => required\.has\(key\) \|\| initial\.has\(key\)\)\)/);
  assert.doesNotMatch(wizard, /copy\.mode !== 'input' && !isConnectorLocallyConfigured\(key\)/);
});

test('agent-facing wizard guidance uses the npx Growth Engineer wizard', () => {
  const files = [
    'SKILL.md',
    'scripts/openclaw-growth-preflight.mjs',
    'scripts/openclaw-growth-status.mjs',
    'scripts/openclaw-growth-start.mjs',
    'scripts/openclaw-growth-runner.mjs',
    'scripts/openclaw-growth-wizard.mjs',
  ];

  for (const file of files) {
    const source = readFileSync(join(skillRoot, file), 'utf8');
    assert.match(source, /npx -y @analyticscli\/growth-engineer wizard/);
  }
});

test('ASC wizard requests the report-creation role and vendor number', () => {
  const wizard = readFileSync(join(skillRoot, 'scripts/openclaw-growth-wizard.mjs'), 'utf8');
  const start = readFileSync(join(skillRoot, 'scripts/openclaw-growth-start.mjs'), 'utf8');
  const status = readFileSync(join(skillRoot, 'scripts/openclaw-growth-status.mjs'), 'utf8');
  const preflight = readFileSync(join(skillRoot, 'scripts/openclaw-growth-preflight.mjs'), 'utf8');
  const exportAsc = readFileSync(join(skillRoot, 'scripts/export-asc-summary.mjs'), 'utf8');
  const skill = readFileSync(join(skillRoot, 'SKILL.md'), 'utf8');
  const setupReference = readFileSync(join(skillRoot, 'references/setup-and-scheduling.md'), 'utf8');
  const secretsReference = readFileSync(join(skillRoot, 'references/required-secrets.md'), 'utf8');

  assert.match(wizard, /Create 2 API keys/);
  assert.match(wizard, /https:\/\/appstoreconnect\.apple\.com\/access\/integrations\/api/);
  assert.match(wizard, /Reports key/);
  assert.match(wizard, /Sales and Reports/);
  assert.match(wizard, /Setup key/);
  assert.match(skill, /ASC setup uses two API keys/);
  assert.match(skill, /Reports key with `Sales and Reports`/);
  assert.match(skill, /temporary Setup key with `Admin`/);
  assert.match(skill, /revoke the Admin key in App Store Connect after setup/);
  assert.doesNotMatch(skill, /Say the main role is `Sales`/);
  assert.doesNotMatch(skill, /Avoid `Admin` unless/);
  assert.match(setupReference, /ASC setup uses two API keys/);
  assert.match(setupReference, /Reports key: `Sales and Reports`/);
  assert.match(setupReference, /Setup key: temporary `Admin`/);
  assert.doesNotMatch(setupReference, /Recommended least privilege: Sales/);
  assert.doesNotMatch(setupReference, /Avoid Admin unless/);
  assert.match(secretsReference, /Ongoing Reports key should use `Sales and Reports`/);
  assert.match(secretsReference, /separate temporary Setup key with `Admin`/);
  assert.match(secretsReference, /ASC_BOOTSTRAP_PRIVATE_KEY_PATH/);
  assert.match(wizard, /inferAscKeyIdFromPrivateKeyPath/);
  assert.match(wizard, /Reports \.p8 path \(AuthKey_<KEY_ID>\.p8, empty = paste\)/);
  assert.match(wizard, /Inferred ASC_KEY_ID=/);
  assert.match(wizard, /Do not rename it/);
  assert.match(wizard, /copyAscPrivateKeyToSecurePath/);
  assert.match(wizard, /Saved secure Reports key copy/);
  assert.match(wizard, /chmod 600/);
  assert.match(wizard, /DELETE_SECRET/);
  assert.match(wizard, /secrets\.ASC_PRIVATE_KEY = DELETE_SECRET/);
  assert.match(wizard, /secrets\.ASC_PRIVATE_KEY_B64 = DELETE_SECRET/);
  assert.match(wizard, /applySecretsToProcessEnv/);
  assert.match(wizard, /ASC_BYPASS_KEYCHAIN: '1'/);
  assert.match(wizard, /connector === 'asc'/);
  assert.match(wizard, /selected\.includes\('asc'\)/);
  assert.match(wizard, /delete env\[key\]/);
  assert.match(wizard, /extractFirstJsonValue/);
  assert.match(wizard, /stripProgressOutput/);
  assert.doesNotMatch(wizard, /Run manually for full output/);
  assert.match(wizard, /could not be parsed\|failed to parse\|asn1/);
  assert.doesNotMatch(wizard, /Checks complete/);
  assert.match(wizard, /ASC auth failed: the \.p8 key could not be parsed/);
  assert.match(start, /ascIsolatedEnv/);
  assert.match(start, /ASC_BYPASS_KEYCHAIN: '1'/);
  assert.match(start, /ASC_CONFIG_PATH/);
  assert.match(start, /openclaw-growth-asc-env/);
  assert.match(start, /if \(value === undefined\)\s+delete childEnv\[key\]/);
  assert.match(start, /env\.ASC_PRIVATE_KEY = undefined/);
  assert.doesNotMatch(start, /env\.ASC_PRIVATE_KEY = ''/);
  assert.match(start, /ASC Reports key auth failed: the \.p8 key could not be parsed/);
  assert.match(start, /describeAscPrivateKeyAuthFailure/);
  assert.match(start, /ASC \$\{role\} key auth failed: the \.p8 key could not be parsed/);
  assert.match(start, /ASC \$\{role\} key auth failed: the \.p8 file permissions are too open/);
  assert.match(start, /bypasses old asc keychain\/config credentials/);
  assert.match(wizard, /ASC_ISSUER_ID \(same for both keys, empty = skip\)/);
  assert.match(wizard, /Same value for both keys/);
  assert.match(wizard, /Paste the full \.p8 file content for \$\{keyLabel\}/);
  assert.match(wizard, /keyLabel: 'the normal reporting key'/);
  assert.match(wizard, /role \$\{bold\('Admin'\)\}/);
  assert.match(wizard, /Role must be Admin/);
  assert.match(wizard, /ASC_BOOTSTRAP_KEY_ID/);
  assert.match(wizard, /ASC_ISSUER_ID \(same API keys page\)/);
  assert.doesNotMatch(wizard, /ask\(rl, 'ASC_BOOTSTRAP_ISSUER_ID'/);
  assert.match(wizard, /Enter the Setup Admin key/);
  assert.match(wizard, /Setup Admin \.p8 path \(AuthKey_<KEY_ID>\.p8, empty = paste\)/);
  assert.match(wizard, /Inferred ASC_BOOTSTRAP_KEY_ID=/);
  assert.match(wizard, /Saved secure temporary Admin key copy/);
  assert.match(wizard, /ASC_BOOTSTRAP_KEY_ID \(from AuthKey_<KEY_ID>\.p8\)/);
  assert.match(wizard, /Not saved/);
  assert.match(wizard, /keyLabel: 'the temporary Admin key'/);
  assert.match(wizard, /Kept temporary Admin \.p8 copy/);
  assert.doesNotMatch(wizard, /Deleted temporary Admin \.p8/);
  assert.doesNotMatch(wizard, /fs\.unlink\(privateKeyPath\)/);
  assert.match(wizard, /function printAscBootstrapAdminRevokeNotice/);
  assert.match(wizard, /IMPORTANT: Revoke the ASC \$\{keyLabel\} now/);
  assert.match(wizard, /Growth Engineer only needed this Admin key once for setup/);
  assert.match(wizard, /https:\/\/appstoreconnect\.apple\.com\/access\/integrations\/api/);
  assert.match(wizard, /ascBootstrapRevokeEnv = bootstrapEnv/);
  assert.match(wizard, /printAscBootstrapAdminRevokeNotice\(ascBootstrapRevokeEnv\)/);
  assert.doesNotMatch(wizard, /Delete this temporary Admin \.p8 file from this host/);
  assert.doesNotMatch(wizard, /Provide a temporary Admin API key now/);
  assert.doesNotMatch(wizard, /payloadNeedsAscAnalyticsBootstrap/);
  assert.match(wizard, /Sales and Reports/);
  assert.doesNotMatch(wizard, /Recommended for normal continuous analytics downloads/);
  assert.doesNotMatch(wizard, /Daily ingestion does not create a new request every day/);
  assert.doesNotMatch(wizard, /Growth Engineer uses App Store Connect API-key reports only/);
  assert.match(wizard, /ASC_VENDOR_NUMBER \(Sales and Trends > Reports\)/);
  assert.doesNotMatch(wizard, new RegExp(['ASC', 'ANALYTICS', 'VENDOR', 'NUMBER'].join('_')));
  assert.match(status, /checkAscAnalyticsReadiness/);
  assert.match(status, /listAscAppIdsDirect/);
  assert.match(status, /isAscAppListDeferredError/);
  assert.match(status, /ASC credentials and ASC_VENDOR_NUMBER are configured; Apple app discovery is temporarily unavailable/);
  assert.match(status, /api\.appstoreconnect\.apple\.com/);
  assert.match(status, /\/v1\/apps\?limit=200/);
  assert.match(status, /could not list apps with asc CLI or direct Apple API/);
  assert.match(status, /asc analytics requests --app/);
  assert.match(status, /isAscAnalyticsRequestCollectionUnsupported/);
  assert.match(status, /does not allow 'get_collection'/);
  assert.match(status, /create\/duplicate handling/);
  assert.match(status, /ASC_VENDOR_NUMBER is missing/);
  assert.match(status, /appAnalyticsReports: 'required'/);
  assert.doesNotMatch(status, /ASC API-key exporter smoke test passed for accessible apps/);
  assert.match(start, /configureAscAllApps/);
  assert.match(start, /listAscAppsDirect/);
  assert.match(start, /isAscAppListDeferredError/);
  assert.match(start, /all_accessible_apps_deferred/);
  assert.match(start, /Analytics Report Request check deferred/);
  assert.match(start, /isAscAnalyticsRequestCreationDeferredError/);
  assert.match(start, /forbidden for security/);
  assert.match(start, /Apple did not create the Analytics Report Request now; setup saved ASC credentials and will retry later/);
  assert.match(start, /api\.appstoreconnect\.apple\.com/);
  assert.match(start, /\/v1\/apps\?limit=200/);
  assert.match(start, /Direct Apple API fallback also failed/);
  assert.match(start, /removeAscAppFlag/);
  assert.match(start, /delete process\.env\.ASC_APP_ID/);
  assert.match(start, /function isAscSource/);
  assert.match(start, /function buildAscExtraSource/);
  assert.match(start, /const hasAscExtra = extra\.some\(isAscSource\)/);
  assert.match(start, /concat\(connectors\.includes\('asc'\) && !hasAscExtra \? \[buildAscExtraSource\(\)\] : \[\]\)/);
  assert.match(start, /if \(config\?\.sources\?\.asc && config\.sources\.asc\.enabled !== false\)\s+return true/);
  assert.doesNotMatch(start, /connectors\.includes\('asc'\) && source\?\.service === 'asc-cli'/);
  assert.match(status, /function isAscSource/);
  assert.match(status, /function configHasEnabledAscSource/);
  assert.match(status, /config\?\.sources\?\.asc && config\.sources\.asc\.enabled !== false/);
  assert.match(status, /if \(!configHasEnabledAscSource\(config\)\)/);
  assert.doesNotMatch(status, /source\?\.service === 'asc-cli' && source\.enabled !== false/);
  assert.match(start, /ensureAscAnalyticsRequestsForAppScope/);
  assert.match(start, /asc analytics request --app/);
  assert.match(start, /isAscAnalyticsRequestAlreadyExists/);
  assert.match(start, /already have such an entity/);
  assert.match(start, /ongoing Analytics Report Request already exists/);
  assert.match(start, /extractAscAnalyticsRequests/);
  assert.match(start, /normalizeString\(request\.state\)\?\.toUpperCase\(\) === 'COMPLETED'/);
  assert.doesNotMatch(start, /request\.state\.toUpperCase\(\)/);
  assert.match(start, /report instances may still be processing/);
  assert.doesNotMatch(start, /asc analytics requests --app \$\{quote\(appId\)\}\$\{stateArg\}/);
  assert.doesNotMatch(start, /listAscAnalyticsRequests\(normalizedAppId, 'COMPLETED'\)/);
  assert.match(start, /--access-type ONGOING/);
  assert.match(preflight, /ASC_COMMAND_SMOKE_TIMEOUT_MS = 120_000/);
  assert.match(preflight, /--analytics-instance-limit 1/);
  assert.match(preflight, /testAscCliAppsList/);
  assert.match(preflight, /testAscAppsListDirect/);
  assert.match(preflight, /isAscAppListDeferredError/);
  assert.match(preflight, /direct Apple API apps list returned JSON/);
  assert.match(preflight, /credentials are saved and app discovery will retry later/);
  assert.match(preflight, /asc apps list --output json/);
  assert.match(start, /phase: 'asc_analytics_request_setup'/);
  assert.match(start, /ASC_BOOTSTRAP_PRIVATE_KEY_DELETE_AFTER_USE/);
  assert.match(start, /kept temporary Admin \.p8 copy/);
  assert.doesNotMatch(start, /await fs\.unlink\(privateKeyPath\)/);
  assert.match(start, /removeTemporaryAscBootstrapPrivateKey/);
  assert.match(start, /temporary ASC Admin key/);
  assert.match(start, /Sales and Reports or Finance for daily downloads/);
  assert.doesNotMatch(wizard, /ASC_APP_ID for the app to analyze/);
  assert.doesNotMatch(exportAsc, /app: String\(process\.env\.ASC_APP_ID/);
  assert.doesNotMatch(wizard, /Avoid: Admin unless/);
});

test('wizard exposes connector and output interval setup paths', () => {
  const wizard = readFileSync(join(skillRoot, 'scripts/openclaw-growth-wizard.mjs'), 'utf8');
  const shared = readFileSync(join(skillRoot, 'scripts/openclaw-growth-shared.mjs'), 'utf8');

  assert.match(wizard, /What do you want to configure/);
  assert.match(wizard, /Use Up\/Down to move, Enter to continue, or press 1-4/);
  assert.match(wizard, /label: 'Connectors'/);
  assert.match(wizard, /Credentials, provider setup, and health checks/);
  assert.match(wizard, /label: 'Outputs and intervals'/);
  assert.match(wizard, /Daily\/weekly\/monthly jobs, GitHub issue\/PR delivery, and OpenClaw chat notifications/);
  assert.match(wizard, /label: 'Advanced intervals only'/);
  assert.match(wizard, /Runner wake-up interval and connector health check cadence/);
  assert.match(wizard, /90-minute production error healthcheck/);
  assert.match(wizard, /Daily behavioral anomaly guardrail/);
  assert.match(wizard, /openClawCanEditConnectors: true/);
  assert.match(wizard, /openClawCanEditConnectorSecrets: false/);
  assert.match(wizard, /non-secret connector config/);
  assert.match(wizard, /ENABLE_ISOLATED_SECRET_RUNNER_WIZARD = false/);
  assert.match(wizard, /mode: 'openclaw-secret-refs'/);
  assert.match(wizard, /analyticsTokenRef: \{ source: 'env', provider: 'default', id: 'ANALYTICSCLI_ACCESS_TOKEN' \}/);
  assert.match(wizard, /once_per_unhealthy_incident_until_recovery_or_changed_fingerprint/);
  assert.doesNotMatch(wizard, /GitHub repo \(owner\/name/);
  assert.doesNotMatch(wizard, /Project slugs for/);
  assert.doesNotMatch(wizard, /Issue labels \(comma-separated\)/);
  assert.doesNotMatch(wizard, /Preferred GitHub artifact mode/);
  assert.doesNotMatch(wizard, /Use recommended input channels and default fetch commands/);
  assert.doesNotMatch(wizard, /Connector credentials are configured through the connector setup/);
  assert.doesNotMatch(wizard, /Usage mode \(1\/2\/3\)/);
  assert.doesNotMatch(wizard, /Output type \(1\/2\/3\)/);
  assert.match(wizard, /Project scope remains unpinned/);
  assert.match(wizard, /Input channels/);
  assert.match(wizard, /Select input channels/);
  assert.match(wizard, /runConnectorSetupSteps/);
  assert.match(wizard, /migrateRuntimeSourceCommandsFile/);
  assert.match(wizard, /replaceLegacyRuntimeScriptCommand/);
  assert.match(wizard, /export-analytics-summary\.mjs/);
  assert.match(wizard, /How should OpenClaw Growth Engineer run/);
  assert.match(wizard, /Output destinations/);
  assert.match(wizard, /Scheduled review cadences/);
  assert.match(wizard, /OpenClaw Gateway cron/);
  assert.match(wizard, /Hermes cron job/);
  assert.match(shared, /openclaw cron add/);
  assert.match(shared, /hermes cron create/);
  assert.match(wizard, /inspectOpenClawCronInstall/);
  assert.match(wizard, /inspectHermesCronInstall/);
  assert.match(wizard, /scheduler-proof\.jsonl/);
  assert.match(wizard, /Default growth cadence/);
  assert.match(wizard, /What it decides/);
  assert.match(wizard, /Space toggles, Enter continues/);
  assert.match(wizard, /Customize GitHub issue\/PR limits, labels, or chart attachment settings/);
});

test('growth connector wizard keeps AnalyticsCLI as the only product analytics service', () => {
  const wizard = readFileSync(join(skillRoot, 'scripts/openclaw-growth-wizard.mjs'), 'utf8');
  const start = readFileSync(join(skillRoot, 'scripts/openclaw-growth-start.mjs'), 'utf8');
  const preflight = readFileSync(join(skillRoot, 'scripts/openclaw-growth-preflight.mjs'), 'utf8');

  for (const connector of [
    'Stripe billing and checkout',
    'Lemon Squeezy sales and licensing',
    'Adapty subscriptions and paywalls',
    'Superwall paywall experiments',
    'Google Play Console',
    'Datadog observability',
    'Bugsnag crash monitoring',
    'Intercom support and feedback',
    'Zendesk support and feedback',
  ]) {
    assert.match(wizard, new RegExp(connector));
  }

  for (const connector of [
    /Apple Search Ads \(experimental\)/,
    /Google Ads \(experimental\)/,
    /Meta Ads \(experimental\)/,
    /TikTok Ads \(experimental\)/,
    /Vercel deployments \(experimental\)/,
    /Cloudflare traffic and edge \(experimental\)/,
    /Resend lifecycle email \(experimental\)/,
    /Customer\.io lifecycle messaging \(experimental\)/,
    /Mailchimp lifecycle email \(experimental\)/,
    /AppFollow reviews and ASO \(experimental\)/,
    /AppTweak ASO intelligence \(experimental\)/,
    /Linear planning context \(experimental\)/,
    /Postiz social publishing \(experimental\)/,
  ]) {
    assert.match(wizard, connector);
  }

  for (const connectorKey of [
    'apple-search-ads',
    'google-ads',
    'meta-ads',
    'tiktok-ads',
    'vercel',
    'cloudflare',
    'resend',
    'customerio',
    'mailchimp',
    'appfollow',
    'apptweak',
    'linear',
    'postiz',
  ]) {
    assert.match(start, new RegExp(`'${connectorKey}'`));
    assert.match(preflight, new RegExp(`'${connectorKey}'`));
  }

  assert.match(wizard, /experimental: true/);
  assert.match(wizard, /sourceKind: 'acquisition'/);
  assert.match(wizard, /sourceKind: 'lifecycle'/);
  assert.match(wizard, /Setup is account-wide/);
  assert.match(wizard, /projectScope: 'discover_from_account'/);
  assert.match(wizard, /experimental: Boolean\(definition\.experimental\)/);
  assert.match(wizard, /Do not paste project IDs, app IDs, product IDs, package names, paywall IDs, service names, or tags here/);
  assert.doesNotMatch(wizard, /PostHog product analytics/);
  assert.doesNotMatch(wizard, /Amplitude analytics/);
  assert.doesNotMatch(wizard, /Mixpanel analytics/);
  assert.doesNotMatch(wizard, /Firebase \/ GA4 analytics/);
});

test('wizard connector menus stay compact', () => {
  const wizard = readFileSync(join(skillRoot, 'scripts/openclaw-growth-wizard.mjs'), 'utf8');

  assert.match(wizard, /if \(!configured\)\s+return ''/);
  assert.match(wizard, /if \(!label\)\s+return ''/);
  assert.doesNotMatch(wizard, /Status: not configured/);
  assert.doesNotMatch(wizard, /writeWrapped\(connector\.summary/);
  assert.doesNotMatch(wizard, /formatConnectorHealthText\(connector\.key/);
  assert.doesNotMatch(wizard, /const statusText = formatConnectorHealthText\(connector\.key/);
  assert.doesNotMatch(
    wizard,
    /process\.stdout\.write\(`\$\{pointer\} \$\{box\} \$\{title\}\\n`\);\s*process\.stdout\.write\('\\n'\);/,
  );
  assert.doesNotMatch(wizard, /entry\.description \? ` - \$\{entry\.description\}`/);
  assert.doesNotMatch(wizard, /\$\{entry\.label\}\$\{description\}/);
});

test('config example enables OpenClaw and Hermes cron with runner proof logs', () => {
  const config = JSON.parse(
    readFileSync(join(skillRoot, 'data/openclaw-growth-engineer/config.example.json'), 'utf8'),
  );
  const runner = readFileSync(join(skillRoot, 'scripts/openclaw-growth-runner.mjs'), 'utf8');
  const start = readFileSync(join(skillRoot, 'scripts/openclaw-growth-start.mjs'), 'utf8');

  assert.deepEqual(config.automation.openclawCron, {
    enabled: true,
    mode: 'main',
    schedule: '*/30 * * * *',
    timezone: 'UTC',
    name: 'OpenClaw Growth Engineer scheduler',
    delivery: {
      enabled: true,
      mode: 'announce',
      channel: 'last',
      to: '',
    },
  });
  assert.deepEqual(config.automation.hermesCron, {
    enabled: true,
    schedule: '*/30 * * * *',
    name: 'Hermes Growth Engineer scheduler',
    skill: 'growth-engineer',
    deliver: 'local',
  });
  assert.match(start, /openclaw cron add/);
  assert.match(start, /hermes cron create/);
  assert.match(start, /openclaw system event/);
  assert.match(start, /inspectOpenClawCronInstall/);
  assert.match(start, /inspectHermesCronInstall/);
  assert.match(runner, /DEFAULT_SCHEDULER_PROOF_PATH = 'data\/openclaw-growth-engineer\/runtime\/scheduler-proof\.jsonl'/);
  assert.match(runner, /deriveRuntimeDirFromStatePath\(statePath\)/);
  assert.match(runner, /deriveSchedulerProofPathFromStatePath\(statePath\)/);
  assert.match(runner, /runner_invoked/);
  assert.match(runner, /repairOpenClawCronDeliveryStore/);
  assert.match(runner, /openclaw_cron_delivery_repaired/);
  assert.match(runner, /function hardenUnattendedShellCommand/);
  assert.match(runner, /sudo -n/);
  assert.match(runner, /Blocked non-interactive sudo prompt/);
  assert.match(runner, /connector_health_checked/);
  assert.match(runner, /runner_completed/);
  assert.match(runner, /runner_failed/);
  assert.match(runner, /function recordRunnerFailure/);
  assert.match(runner, /dailyRunnerFailures/);
  assert.match(runner, /runner_failed_suppressed/);
  assert.match(runner, /runner failure unchanged and already reported today/);
  assert.match(runner, /process\.exitCode = failureDecision\?\.exitCode \?\? 1/);
  assert.match(runner, /function redactCommandForDiagnostics/);
  assert.match(runner, /Source "\$\{sourceName\}" command failed: command/);
});

test('setup and preflight harden sudo commands for unattended VPS runs', () => {
  const start = readFileSync(join(skillRoot, 'scripts/openclaw-growth-start.mjs'), 'utf8');
  const preflight = readFileSync(join(skillRoot, 'scripts/openclaw-growth-preflight.mjs'), 'utf8');

  assert.match(start, /function hardenUnattendedShellCommand/);
  assert.match(start, /SUDO_ASKPASS/);
  assert.match(preflight, /function hardenUnattendedShellCommand/);
  assert.match(preflight, /SUDO_ASKPASS/);
});

test('config example stores connector credentials as OpenClaw-style secret refs', () => {
  const config = JSON.parse(
    readFileSync(join(skillRoot, 'data/openclaw-growth-engineer/config.example.json'), 'utf8'),
  );

  assert.deepEqual(config.secrets.githubTokenRef, {
    source: 'env',
    provider: 'default',
    id: 'GITHUB_TOKEN',
  });
  assert.deepEqual(config.secrets.analyticsTokenRef, {
    source: 'env',
    provider: 'default',
    id: 'ANALYTICSCLI_ACCESS_TOKEN',
  });
});
