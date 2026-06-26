import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import {
  buildHermesCronCreateCommand,
  buildHermesCronVerification,
  buildOpenClawCronAddCommand,
  buildOpenClawCronEditDeliveryCommand,
  buildOpenClawCronVerification,
  buildGrowthRunnerCommand,
  buildOpenClawGrowthSystemEvent,
  deriveSchedulerProofPathFromStatePath,
  deriveStatePathFromConfigPath,
  evaluateOpenClawCronRecords,
  evaluateOpenClawCronText,
  getGitHubArtifactModes,
  getOpenClawCronEditDeliveryCommandFromInspection,
  repairOpenClawCronDeliveryStore,
  shouldAutoCreateGitHubArtifact,
} from '../scripts/openclaw-growth-shared.mjs';

test('shouldAutoCreateGitHubArtifact auto-enables issues when GitHub token and repo are configured', () => {
  const previousToken = process.env.GITHUB_TOKEN;
  process.env.GITHUB_TOKEN = 'test-token';
  try {
    assert.equal(
      shouldAutoCreateGitHubArtifact({
        project: { githubRepo: 'owner/repo' },
        actions: { mode: 'issue', autoCreateIssues: false },
      }),
      true,
    );
  } finally {
    if (previousToken === undefined) {
      delete process.env.GITHUB_TOKEN;
    } else {
      process.env.GITHUB_TOKEN = previousToken;
    }
  }
});

test('shouldAutoCreateGitHubArtifact respects explicit GitHub artifact opt-out', () => {
  const previousToken = process.env.GITHUB_TOKEN;
  process.env.GITHUB_TOKEN = 'test-token';
  try {
    assert.equal(
      shouldAutoCreateGitHubArtifact({
        project: { githubRepo: 'owner/repo' },
        actions: { mode: 'issue', disableAutoCreateGitHubArtifacts: true },
      }),
      false,
    );
  } finally {
    if (previousToken === undefined) {
      delete process.env.GITHUB_TOKEN;
    } else {
      process.env.GITHUB_TOKEN = previousToken;
    }
  }
});

test('getGitHubArtifactModes supports multiple selected GitHub artifact outputs', () => {
  assert.deepEqual(
    getGitHubArtifactModes({
      actions: {
        outputDestinations: ['openclaw_chat', 'github_issue', 'github_pull_request'],
        autoCreateIssues: true,
        autoCreatePullRequests: true,
      },
      deliveries: {
        github: {
          modes: ['issue', 'pull_request'],
        },
      },
    }),
    ['issue', 'pull_request'],
  );
});

test('explicit chat-only output destinations disable GitHub artifact fallback', () => {
  const previousToken = process.env.GITHUB_TOKEN;
  process.env.GITHUB_TOKEN = 'test-token';
  try {
    const config = {
      project: { githubRepo: 'owner/repo' },
      actions: {
        mode: 'issue',
        outputDestinations: ['openclaw_chat'],
        autoCreateIssues: false,
        autoCreatePullRequests: false,
      },
    };
    assert.deepEqual(getGitHubArtifactModes(config), []);
    assert.equal(shouldAutoCreateGitHubArtifact(config), false);
  } finally {
    if (previousToken === undefined) {
      delete process.env.GITHUB_TOKEN;
    } else {
      process.env.GITHUB_TOKEN = previousToken;
    }
  }
});

test('OpenClaw cron commands keep state and proof beside the active config', () => {
  const configPath = '/home/lo/data/openclaw-growth-engineer/config.json';
  const statePath = '/home/lo/data/openclaw-growth-engineer/state.json';
  const proofPath = '/home/lo/data/openclaw-growth-engineer/runtime/scheduler-proof.jsonl';

  assert.equal(deriveStatePathFromConfigPath(configPath), statePath);
  assert.equal(deriveSchedulerProofPathFromStatePath(statePath), proofPath);
  assert.equal(
    buildGrowthRunnerCommand(configPath),
    `node scripts/openclaw-growth-runner.mjs --config ${configPath} --state ${statePath}`,
  );

  const eventText = buildOpenClawGrowthSystemEvent(configPath, {});
  assert.match(eventText, new RegExp(`--state ${statePath.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`));
  assert.match(eventText, new RegExp(proofPath.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
  assert.match(eventText, /Execute only that runner command/);
  assert.match(eventText, /Do not run sudo/);
  assert.match(eventText, /instead of prompting/);
  assert.match(eventText, /Always let the runner write state and proof logs/);
  assert.match(eventText, /only summarize new or changed findings/);
  assert.match(eventText, /skippedReason cadence_not_due, issue_set_unchanged, or no_data_change/);
  assert.match(eventText, /do not repeat old findings/);
  assert.match(eventText, /Persisted connectorHealth\.lastStatusOk=false is not by itself a new event/);
  assert.match(eventText, /connector_health_not_due, connector_health_unchanged/);
});

test('OpenClaw cron verification rejects stale name-only jobs', () => {
  const configPath = 'data/openclaw-growth-engineer/config.json';
  const verification = buildOpenClawCronVerification(configPath, {});

  const stale = evaluateOpenClawCronRecords(
    {
      jobs: [
        {
          name: 'OpenClaw Growth Engineer scheduler',
          schedule: '*/30 * * * *',
          timezone: 'UTC',
          systemEvent: 'Temporary Growth Engineer demo notification only',
        },
      ],
    },
    verification,
  );

  assert.equal(stale.exists, true);
  assert.equal(stale.verified, false);
  assert.equal(stale.reason, 'missing_required_fragments');
});

test('OpenClaw cron verification accepts jobs wired to the runner contract', () => {
  const configPath = 'data/openclaw-growth-engineer/config.json';
  const addCommand = buildOpenClawCronAddCommand(configPath, {});
  const verification = buildOpenClawCronVerification(configPath, {});

  const parsed = evaluateOpenClawCronRecords(
    {
      jobs: [
        {
          name: 'OpenClaw Growth Engineer scheduler',
          schedule: '*/30 * * * *',
          timezone: 'UTC',
          command: addCommand,
        },
      ],
    },
    verification,
  );

  assert.equal(parsed.exists, true);
  assert.equal(parsed.verified, true);

  const text = evaluateOpenClawCronText(addCommand, verification);
  assert.equal(text.exists, true);
  assert.equal(text.verified, true);
});

test('OpenClaw cron commands announce through the instance default channel by default', () => {
  const configPath = 'data/openclaw-growth-engineer/config.json';
  const addCommand = buildOpenClawCronAddCommand(configPath, {});
  const verification = buildOpenClawCronVerification(configPath, {});

  assert.match(addCommand, /--announce --channel last --wake now/);
  assert.equal(verification.delivery.enabled, true);
  assert.equal(verification.delivery.channel, 'last');

  const silentCommand = buildOpenClawCronAddCommand(configPath, {
    automation: {
      openclawCron: {
        delivery: { enabled: false },
      },
    },
  });
  assert.match(silentCommand, /--no-deliver --wake now/);
});

test('OpenClaw cron verification rejects runner jobs with disabled delivery', () => {
  const configPath = 'data/openclaw-growth-engineer/config.json';
  const addCommand = buildOpenClawCronAddCommand(configPath, {});
  const verification = buildOpenClawCronVerification(configPath, {});

  const parsed = evaluateOpenClawCronRecords(
    {
      jobs: [
        {
          name: 'OpenClaw Growth Engineer scheduler',
          schedule: '*/30 * * * *',
          timezone: 'UTC',
          command: addCommand,
          delivery: {
            mode: 'none',
          },
        },
      ],
    },
    verification,
  );

  assert.equal(parsed.exists, true);
  assert.equal(parsed.verified, false);
  assert.equal(parsed.reason, 'delivery_mismatch');
});

test('OpenClaw cron verification accepts pinned Discord announce delivery for the default channel config', () => {
  const configPath = 'data/openclaw-growth-engineer/config.json';
  const addCommand = buildOpenClawCronAddCommand(configPath, {});
  const verification = buildOpenClawCronVerification(configPath, {});

  const parsed = evaluateOpenClawCronRecords(
    {
      jobs: [
        {
          name: 'OpenClaw Growth Engineer scheduler',
          schedule: '*/30 * * * *',
          timezone: 'UTC',
          command: addCommand,
          delivery: {
            mode: 'announce',
            channel: 'discord',
            to: 'channel:1504655172947673139',
          },
        },
      ],
    },
    verification,
  );

  assert.equal(parsed.exists, true);
  assert.equal(parsed.verified, true);
});

test('OpenClaw cron delivery repair uses cron edit when a job id is available', () => {
  const config = {
    automation: {
      openclawCron: {
        delivery: {
          enabled: true,
          mode: 'announce',
          channel: 'discord',
          to: 'channel:1471908112100495617',
        },
      },
    },
  };
  const job = {
    id: '1eafd5f5-8bdd-4597-b6c5-e8a35a0308fa',
    name: 'OpenClaw Growth Engineer scheduler',
    delivery: {
      mode: 'none',
    },
  };

  assert.equal(
    buildOpenClawCronEditDeliveryCommand(job, config),
    'openclaw cron edit 1eafd5f5-8bdd-4597-b6c5-e8a35a0308fa --announce --channel discord --to channel:1471908112100495617 --best-effort-deliver',
  );
  assert.equal(
    getOpenClawCronEditDeliveryCommandFromInspection({ jobs: [job] }, config),
    'openclaw cron edit 1eafd5f5-8bdd-4597-b6c5-e8a35a0308fa --announce --channel discord --to channel:1471908112100495617 --best-effort-deliver',
  );
});

test('OpenClaw cron repair updates disabled delivery in the local job store', async () => {
  const home = mkdtempSync(join(tmpdir(), 'openclaw-cron-home-'));
  const configPath = 'data/openclaw-growth-engineer/config.json';
  const jobStoreDir = join(home, '.openclaw', 'cron');
  const jobStorePath = join(jobStoreDir, 'jobs.json');
  const addCommand = buildOpenClawCronAddCommand(configPath, {});

  try {
    mkdirSync(jobStoreDir, { recursive: true });
    writeFileSync(
      jobStorePath,
      JSON.stringify(
        {
          jobs: [
            {
              id: 'growth',
              name: 'OpenClaw Growth Engineer scheduler',
              schedule: '*/30 * * * *',
              timezone: 'UTC',
              command: addCommand,
              delivery: {
                mode: 'none',
              },
            },
          ],
        },
        null,
        2,
      ),
    );

    const result = await repairOpenClawCronDeliveryStore({
      configPath,
      readFile: async (filePath, encoding) => readFileSync(filePath, encoding),
      writeFile: async (filePath, content, encoding) => writeFileSync(filePath, content, encoding),
      home,
    });

    assert.equal(result.repaired, true);
    assert.equal(result.path, jobStorePath);

    const repaired = JSON.parse(readFileSync(jobStorePath, 'utf8'));
    assert.deepEqual(repaired.jobs[0].delivery, {
      mode: 'announce',
      channel: 'last',
      to: '',
    });
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
});

test('Hermes cron verification rejects stale name-only jobs', () => {
  const configPath = 'data/openclaw-growth-engineer/config.json';
  const workdir = '/srv/example-app';
  const verification = buildHermesCronVerification(configPath, {}, { workdir });

  const stale = evaluateOpenClawCronRecords(
    {
      jobs: [
        {
          name: 'Hermes Growth Engineer scheduler',
          schedule: '*/30 * * * *',
          prompt: 'Old placeholder task',
        },
      ],
    },
    verification,
  );

  assert.equal(stale.exists, true);
  assert.equal(stale.verified, false);
  assert.equal(stale.reason, 'missing_required_fragments');
});

test('Hermes cron verification accepts jobs wired to the runner contract', () => {
  const configPath = 'data/openclaw-growth-engineer/config.json';
  const workdir = '/srv/example-app';
  const createCommand = buildHermesCronCreateCommand(configPath, {}, { workdir });
  const verification = buildHermesCronVerification(configPath, {}, { workdir });

  const parsed = evaluateOpenClawCronRecords(
    {
      jobs: [
        {
          name: 'Hermes Growth Engineer scheduler',
          schedule: '*/30 * * * *',
          skill: 'growth-engineer',
          deliver: 'local',
          workdir,
          command: createCommand,
        },
      ],
    },
    verification,
  );

  assert.equal(parsed.exists, true);
  assert.equal(parsed.verified, true);
});
