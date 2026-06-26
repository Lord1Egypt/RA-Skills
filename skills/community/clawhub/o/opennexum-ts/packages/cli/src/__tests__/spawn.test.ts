import assert from 'node:assert/strict';
import { mkdir, writeFile, readFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { mkdtemp } from 'node:fs/promises';
import path from 'node:path';
import test from 'node:test';

import type { SpawnOptions, SessionRecord } from '@nexum/spawn';

const testingGlobals = globalThis as typeof globalThis & {
  __nexumCliSpawnAcpSession?: (opts: SpawnOptions) => Promise<SessionRecord>;
  __nexumCliSendMessage?: (chatId: string, text: string, token: string) => Promise<void>;
};

// Minimal valid contract YAML for tests
const CONTRACT_YAML = `id: TEST-001
name: Test Task
type: coding
created_at: "2026-01-01T00:00:00Z"
scope:
  files:
    - src/foo.ts
  boundaries:
    - packages/core/
  conflicts_with: []
deliverables:
  - "src/foo.ts: implement foo"
eval_strategy:
  type: unit
  criteria:
    - id: C1
      desc: foo is implemented
      method: "unit: check foo"
      threshold: pass
generator: cc-frontend
evaluator: eval
max_iterations: 3
depends_on: []
`;

async function setupProject(
  tasks: object[],
  contract = CONTRACT_YAML,
  taskId = 'TEST-001'
): Promise<string> {
  const projectDir = await mkdtemp(path.join(tmpdir(), 'nexum-cli-test-'));
  const nexumDir = path.join(projectDir, 'nexum');
  const contractDir = path.join(projectDir, 'docs', 'nexum', 'contracts');
  await mkdir(nexumDir, { recursive: true });
  await mkdir(contractDir, { recursive: true });
  await writeFile(
    path.join(nexumDir, 'active-tasks.json'),
    JSON.stringify({ tasks }, null, 2) + '\n',
    'utf8'
  );
  await writeFile(path.join(contractDir, `${taskId}.yaml`), contract, 'utf8');
  return projectDir;
}

// ─── C2: spawn reads contract and calls spawnAcpSession with correct agentId ───

test('runSpawn reads contract and calls spawnAcpSession with correct agentId', async () => {
  const taskId = 'TEST-001';
  const projectDir = await setupProject([
    {
      id: taskId,
      name: 'Test Task',
      status: 'pending',
      contract_path: `docs/nexum/contracts/${taskId}.yaml`,
      depends_on: [],
      iteration: 0,
    },
  ]);

  const spawnCalls: SpawnOptions[] = [];
  testingGlobals.__nexumCliSpawnAcpSession = async (opts) => {
    spawnCalls.push(opts);
    return {
      taskId: opts.taskId,
      sessionKey: 'test-session-key',
      agentId: opts.agentId,
      startedAt: new Date().toISOString(),
      status: 'running',
    };
  };
  testingGlobals.__nexumCliSendMessage = async () => {};

  const { runSpawn } = await import(`../commands/spawn.ts?t=${Date.now()}`);
  await runSpawn(taskId, projectDir);

  assert.equal(spawnCalls.length, 1);
  assert.equal(spawnCalls[0]?.agentId, 'cc-frontend', 'agentId should match contract.generator');
  assert.equal(spawnCalls[0]?.taskId, taskId);
  assert.ok(
    spawnCalls[0]?.promptFile.includes(taskId),
    'promptFile should contain taskId'
  );
  assert.ok(
    (await readFile(spawnCalls[0]?.promptFile ?? '', 'utf8')).includes('Test Task'),
    'prompt file should contain task name'
  );

  // Verify task was updated with session key
  const tasksRaw = JSON.parse(
    await readFile(path.join(projectDir, 'nexum', 'active-tasks.json'), 'utf8')
  ) as { tasks: Array<{ id: string; acp_session_key?: string; status?: string }> };
  const updatedTask = tasksRaw.tasks.find((t) => t.id === taskId);
  assert.equal(updatedTask?.acp_session_key, 'test-session-key');

  delete testingGlobals.__nexumCliSpawnAcpSession;
  delete testingGlobals.__nexumCliSendMessage;
});

// ─── C3: complete pass updates task to done and unlocks downstream tasks ───

test('runComplete with pass marks task done and unlocks blocked downstream tasks', async () => {
  const taskId = 'TEST-001';
  const downstreamId = 'TEST-002';
  const projectDir = await setupProject([
    {
      id: taskId,
      name: 'Test Task',
      status: 'running',
      contract_path: `docs/nexum/contracts/${taskId}.yaml`,
      depends_on: [],
      iteration: 0,
      started_at: new Date(Date.now() - 5000).toISOString(),
    },
    {
      id: downstreamId,
      name: 'Downstream Task',
      status: 'blocked',
      contract_path: `docs/nexum/contracts/${taskId}.yaml`,
      depends_on: [taskId],
    },
  ]);

  testingGlobals.__nexumCliSendMessage = async () => {};

  const { runComplete } = await import(`../commands/complete.ts?t=${Date.now()}`);
  await runComplete(taskId, 'pass', projectDir);

  const tasksRaw = JSON.parse(
    await readFile(path.join(projectDir, 'nexum', 'active-tasks.json'), 'utf8')
  ) as { tasks: Array<{ id: string; status: string }> };

  const upstream = tasksRaw.tasks.find((t) => t.id === taskId);
  const downstream = tasksRaw.tasks.find((t) => t.id === downstreamId);

  assert.equal(upstream?.status, 'done', 'upstream task should be done');
  assert.equal(downstream?.status, 'pending', 'downstream blocked task should become pending');

  delete testingGlobals.__nexumCliSendMessage;
});

// ─── C4: complete fail with iteration < max_iterations triggers retry ───

test('runComplete with fail and iteration < max_iterations triggers retry spawn', async () => {
  const taskId = 'TEST-001';
  const projectDir = await setupProject([
    {
      id: taskId,
      name: 'Test Task',
      status: 'evaluating',
      contract_path: `docs/nexum/contracts/${taskId}.yaml`,
      depends_on: [],
      iteration: 0,
      started_at: new Date(Date.now() - 5000).toISOString(),
    },
  ]);

  const spawnCalls: SpawnOptions[] = [];
  testingGlobals.__nexumCliSpawnAcpSession = async (opts) => {
    spawnCalls.push(opts);
    return {
      taskId: opts.taskId,
      sessionKey: 'retry-session-key',
      agentId: opts.agentId,
      startedAt: new Date().toISOString(),
      status: 'running',
    };
  };
  testingGlobals.__nexumCliSendMessage = async () => {};

  const { runComplete } = await import(`../commands/complete.ts?t2=${Date.now()}`);
  await runComplete(taskId, 'fail', projectDir);

  assert.equal(spawnCalls.length, 1, 'spawnAcpSession should be called once for retry');
  assert.equal(spawnCalls[0]?.agentId, 'cc-frontend', 'retry should use contract.generator');
  assert.equal(spawnCalls[0]?.taskId, taskId);

  const tasksRaw = JSON.parse(
    await readFile(path.join(projectDir, 'nexum', 'active-tasks.json'), 'utf8')
  ) as { tasks: Array<{ id: string; status: string; iteration?: number }> };

  const retried = tasksRaw.tasks.find((t) => t.id === taskId);
  assert.equal(retried?.status, 'running', 'task should be running after retry');
  assert.equal(retried?.iteration, 1, 'iteration should be incremented to 1');

  delete testingGlobals.__nexumCliSpawnAcpSession;
  delete testingGlobals.__nexumCliSendMessage;
});

// ─── C5: config eval→codex mapping is resolved in spawn payload ───

test('runSpawnEval resolves evaluator agentCli from config (eval→codex)', async () => {
  const taskId = 'TEST-001';
  const projectDir = await setupProject([
    {
      id: taskId,
      name: 'Test Task',
      status: 'running',
      contract_path: `docs/nexum/contracts/${taskId}.yaml`,
      depends_on: [],
      iteration: 0,
    },
  ]);

  // Write config mapping 'eval' agent to codex
  const nexumDir = path.join(projectDir, 'nexum');
  await writeFile(
    path.join(nexumDir, 'config.json'),
    JSON.stringify({ agents: { eval: { cli: 'codex', model: 'gpt-4o' } } }, null, 2),
    'utf8'
  );

  testingGlobals.__nexumCliSendMessage = async () => {};

  const { runSpawnEval } = await import(`../commands/spawn.ts?t=${Date.now()}`);
  const payload = await runSpawnEval(taskId, projectDir);

  assert.equal(payload.agentCli, 'codex', 'agentCli should be codex per config');
  assert.equal(payload.agentId, 'eval', 'agentId should be contract.evaluator');

  delete testingGlobals.__nexumCliSendMessage;
});
