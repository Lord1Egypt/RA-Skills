import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import type { Command } from 'commander';
import {
  parseContract,
  getTask,
  updateTask,
  readTasks,
  TaskStatus,
  getHeadCommit,
  loadConfig,
  resolveAgentCli,
} from '@nexum/core';
import type { AgentCli } from '@nexum/core';
import { renderGeneratorPrompt } from '@nexum/prompts';

export interface SpawnPayload {
  taskId: string;
  taskName: string;
  agentId: string;
  agentCli: AgentCli;
  promptFile: string;
  promptContent: string;
  label: string;
  cwd: string;
}

export async function runSpawn(taskId: string, projectDir: string): Promise<SpawnPayload> {
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

  const gitCommitCmd = [
    `git add -- ${contract.scope.files.join(' ')}`,
    `git commit -m "feat(${taskId.toLowerCase()}): implement ${contract.name}"`,
  ].join(' && ');

  const promptContent = renderGeneratorPrompt({
    contract,
    task: { id: task.id, name: task.name },
    gitCommitCmd,
    evalResultPath,
    lessons: [],
  });

  const promptsDir = path.join(projectDir, 'nexum', 'runtime', 'prompts');
  await mkdir(promptsDir, { recursive: true });
  const promptFile = path.join(promptsDir, `${taskId}-gen-${Date.now()}.md`);
  await writeFile(promptFile, promptContent, 'utf8');

  const baseCommit = await getHeadCommit(projectDir).catch(() => '');

  await updateTask(projectDir, taskId, {
    status: TaskStatus.Running,
    started_at: new Date().toISOString(),
    ...(baseCommit ? { base_commit: baseCommit } : {}),
    iteration,
  });

  const config = await loadConfig(projectDir);
  const agentCli = resolveAgentCli(config, contract.generator);
  const label = `nexum-${taskId.toLowerCase()}-${contract.generator}`;

  return {
    taskId,
    taskName: contract.name,
    agentId: contract.generator,
    agentCli,
    promptFile,
    promptContent,
    label,
    cwd: projectDir,
  };
}

export async function runSpawnEval(taskId: string, projectDir: string): Promise<SpawnPayload> {
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

  const tasks = await readTasks(projectDir);
  const { renderEvaluatorPrompt } = await import('@nexum/prompts');
  const promptContent = renderEvaluatorPrompt({
    contract,
    task: { id: task.id, name: task.name },
    gitCommitCmd: '',
    evalResultPath,
    lessons: [],
  });

  const promptsDir = path.join(projectDir, 'nexum', 'runtime', 'prompts');
  await mkdir(promptsDir, { recursive: true });
  const promptFile = path.join(promptsDir, `${taskId}-eval-${Date.now()}.md`);
  await writeFile(promptFile, promptContent, 'utf8');

  await updateTask(projectDir, taskId, {
    status: TaskStatus.Evaluating,
    eval_result_path: evalResultPath,
  });

  const config = await loadConfig(projectDir);
  const agentCli = resolveAgentCli(config, contract.evaluator);
  const label = `nexum-${taskId.toLowerCase()}-eval`;

  return {
    taskId,
    taskName: contract.name,
    agentId: contract.evaluator,
    agentCli,
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
