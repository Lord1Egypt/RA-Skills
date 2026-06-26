import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import type { Command } from 'commander';
import {
  parseContract,
  getTask,
  readTasks,
  syncTasksWithContracts,
  updateTask,
  loadConfig,
  resolveAgentExecution,
  TaskStatus,
} from '@nexum/core';
import type { AgentCli, AgentRuntime } from '@nexum/core';
import { renderGeneratorPrompt } from '@nexum/prompts';
import { resolveContractAgents } from '../lib/resolve-contract-agents.js';

// ---------- commit type detection ----------

function detectCommitType(taskName: string): string {
  const lower = taskName.toLowerCase();
  if (/\bfix\b|bug|hotfix|修复|修补/.test(lower)) return 'fix';
  if (/\brefactor|重构/.test(lower)) return 'refactor';
  if (/\bdocs?|文档|readme|comment/.test(lower)) return 'docs';
  if (/\btest|测试/.test(lower)) return 'test';
  if (/\bperf|性能|optimize|优化/.test(lower)) return 'perf';
  if (/\bci|cd|pipeline|github/.test(lower)) return 'ci';
  if (/\bchore|杂务/.test(lower)) return 'chore';
  return 'feat';
}

function isAsciiOnly(value: string): boolean {
  return /^[\x00-\x7F]+$/.test(value);
}

function taskIdToKebabSlug(taskId: string): string {
  return taskId.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}

function toEnglishCommitSummary(name: string, taskId: string): string {
  return isAsciiOnly(name) ? name : taskIdToKebabSlug(taskId);
}

function quoteShellArg(value: string): string {
  if (value === '') {
    return "''";
  }

  return `'${value.replace(/'/g, `'\\''`)}'`;
}

export interface SpawnPayload {
  taskId: string;
  taskName: string;
  phase: 'generator' | 'evaluator';
  agentId: string;
  agentCli: AgentCli;
  runtime: AgentRuntime;
  runtimeAgentId: string;
  constraints: {
    dependsOn: string[];
    conflictsWith: string[];
    scopeFiles: string[];
    scopeBoundaries: string[];
  };
  promptFile: string;
  promptContent: string;
  label: string;
  cwd: string;
}

type ContractWithAgentCompat = {
  generator: string;
  evaluator: string;
  agent?: {
    generator?: string;
    evaluator?: string;
  };
};

function getGeneratorAgentId(contract: ContractWithAgentCompat): string {
  return contract.agent?.generator ?? contract.generator;
}

function getEvaluatorAgentId(contract: ContractWithAgentCompat): string {
  return contract.agent?.evaluator ?? contract.evaluator;
}

export async function runSpawn(taskId: string, projectDir: string): Promise<SpawnPayload> {
  await syncTasksWithContracts(projectDir, { taskId });
  const task = await getTask(projectDir, taskId);
  if (!task) {
    throw new Error(`Task not found: ${taskId}`);
  }

  const contractAbsPath = path.isAbsolute(task.contract_path)
    ? task.contract_path
    : path.join(projectDir, task.contract_path);
  const contract = await parseContract(contractAbsPath);

  const iteration = task.iteration ?? 0;
  const evalResultPath = path.join(
    projectDir,
    'nexum',
    'runtime',
    'eval',
    `${taskId}-iter-${iteration}.yaml`
  );
  const fieldReportPath = path.join(
    projectDir,
    'nexum',
    'runtime',
    'field-reports',
    `${taskId}.md`
  );

  const config = await loadConfig(projectDir);
  const resolvedContract = resolveContractAgents(contract, config);
  const tasks = await readTasks(projectDir);
  assertGeneratorReady(taskId, task.status, resolvedContract.depends_on, resolvedContract.scope.conflicts_with, tasks);
  // If git.remote is explicitly set to empty string, skip push; otherwise default to 'origin'
  const gitRemoteRaw = config.git?.remote;
  const gitRemote = gitRemoteRaw === '' ? '' : (gitRemoteRaw ?? 'origin');
  const gitBranch = config.git?.branch ?? 'main';

  const type = detectCommitType(resolvedContract.name);
  const scope = taskId.toUpperCase();
  const commitSummary = toEnglishCommitSummary(resolvedContract.name, taskId);
  const commitMsg = `${type}(${scope}): ${taskId}: ${commitSummary}`;
  const quotedScopeFiles = resolvedContract.scope.files.map((file) => quoteShellArg(file)).join(' ');
  const gitCommitCmd = gitRemote
    ? [
        `git add -- ${quotedScopeFiles}`,
        `git commit -m "${commitMsg}"`,
        `git push -u ${gitRemote} ${gitBranch}`,
      ].join(' && ')
    : [
        `git add -- ${quotedScopeFiles}`,
        `git commit -m "${commitMsg}"`,
      ].join(' && ');

  const promptContent = renderGeneratorPrompt({
    contract: resolvedContract,
    task: { id: task.id, name: task.name },
    gitCommitCmd,
    evalResultPath,
    fieldReportPath,
    lessons: [],
    projectDir,
  });

  const promptsDir = path.join(projectDir, 'nexum', 'runtime', 'prompts');
  await mkdir(promptsDir, { recursive: true });
  const promptFile = path.join(promptsDir, `${taskId}-gen-${Date.now()}.md`);
  await writeFile(promptFile, promptContent, 'utf8');

  const execution = resolveAgentExecution(config, resolvedContract.generator);
  const label = `nexum-${taskId.toLowerCase()}-${resolvedContract.generator}`;

  return {
    taskId,
    taskName: resolvedContract.name,
    phase: 'generator',
    agentId: resolvedContract.generator,
    agentCli: execution.cli,
    runtime: execution.runtime,
    runtimeAgentId: execution.runtimeAgentId,
    constraints: {
      dependsOn: resolvedContract.depends_on,
      conflictsWith: resolvedContract.scope.conflicts_with,
      scopeFiles: resolvedContract.scope.files,
      scopeBoundaries: resolvedContract.scope.boundaries,
    },
    promptFile,
    promptContent,
    label,
    cwd: projectDir,
  };
}

export async function runSpawnEval(taskId: string, projectDir: string): Promise<SpawnPayload> {
  await syncTasksWithContracts(projectDir, { taskId });
  const task = await getTask(projectDir, taskId);
  if (!task) {
    throw new Error(`Task not found: ${taskId}`);
  }

  const contractAbsPath = path.isAbsolute(task.contract_path)
    ? task.contract_path
    : path.join(projectDir, task.contract_path);
  const contract = await parseContract(contractAbsPath);
  const config = await loadConfig(projectDir);
  const contractWithAgents = {
    ...contract,
    generator: getGeneratorAgentId(contract),
    evaluator: getEvaluatorAgentId(contract),
  };
  const resolvedContract = resolveContractAgents(contractWithAgents, config);
  if (task.status !== TaskStatus.GeneratorDone) {
    throw new Error(
      `Task ${taskId} is not ready for evaluator spawn. Expected generator_done, got ${task.status}.`
    );
  }

  const iteration = task.iteration ?? 0;
  const evalResultPath = path.join(
    projectDir,
    'nexum',
    'runtime',
    'eval',
    `${taskId}-iter-${iteration}.yaml`
  );
  const fieldReportPath = path.join(
    projectDir,
    'nexum',
    'runtime',
    'field-reports',
    `${taskId}.md`
  );

  const { renderEvaluatorPrompt } = await import('@nexum/prompts');
  const promptContent = renderEvaluatorPrompt({
    contract: resolvedContract,
    task: { id: task.id, name: task.name },
    gitCommitCmd: '',
    evalResultPath,
    fieldReportPath,
    lessons: [],
  });

  const promptsDir = path.join(projectDir, 'nexum', 'runtime', 'prompts');
  await mkdir(promptsDir, { recursive: true });
  const promptFile = path.join(promptsDir, `${taskId}-eval-${Date.now()}.md`);
  await writeFile(promptFile, promptContent, 'utf8');

  await updateTask(projectDir, taskId, {
    eval_result_path: evalResultPath,
  });

  const execution = resolveAgentExecution(config, resolvedContract.evaluator);
  const label = `nexum-${taskId.toLowerCase()}-eval`;

  return {
    taskId,
    taskName: resolvedContract.name,
    phase: 'evaluator',
    agentId: resolvedContract.evaluator,
    agentCli: execution.cli,
    runtime: execution.runtime,
    runtimeAgentId: execution.runtimeAgentId,
    constraints: {
      dependsOn: resolvedContract.depends_on,
      conflictsWith: resolvedContract.scope.conflicts_with,
      scopeFiles: resolvedContract.scope.files,
      scopeBoundaries: resolvedContract.scope.boundaries,
    },
    promptFile,
    promptContent,
    label,
    cwd: projectDir,
  };
}

export function registerSpawn(program: Command): void {
  program
    .command('spawn <taskId>')
    .description('Prepare a generator task and output spawn payload as JSON')
    .option('--project <dir>', 'Project directory', process.cwd())
    .action(async (taskId: string, options: { project: string }) => {
      try {
        const payload = await runSpawn(taskId, options.project);
        console.log(JSON.stringify(payload, null, 2));
      } catch (err) {
        console.error('spawn failed:', err instanceof Error ? err.message : err);
        process.exit(1);
      }
    });
}

function assertGeneratorReady(
  taskId: string,
  status: TaskStatus,
  dependsOn: string[],
  conflictsWith: string[],
  tasks: Awaited<ReturnType<typeof readTasks>>
): void {
  if (status !== TaskStatus.Pending) {
    throw new Error(`Task ${taskId} is not ready for generator spawn. Expected pending, got ${status}.`);
  }

  const completedIds = new Set(
    tasks.filter((task) => task.status === TaskStatus.Done).map((task) => task.id)
  );
  const unmetDependencies = dependsOn.filter((dependencyId) => !completedIds.has(dependencyId));
  if (unmetDependencies.length > 0) {
    throw new Error(
      `Task ${taskId} still has unmet dependencies: ${unmetDependencies.join(', ')}.`
    );
  }

  const conflictingTasks = tasks.filter(
    (task) =>
      conflictsWith.includes(task.id) &&
      (task.status === TaskStatus.Running ||
        task.status === TaskStatus.GeneratorDone ||
        task.status === TaskStatus.Evaluating)
  );
  if (conflictingTasks.length > 0) {
    throw new Error(
      `Task ${taskId} conflicts with active tasks: ${conflictingTasks.map((task) => task.id).join(', ')}.`
    );
  }
}
