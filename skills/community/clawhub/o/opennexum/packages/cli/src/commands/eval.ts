import type { Command } from 'commander';
import { runSpawnEval, type SpawnPayload } from './spawn.js';

export async function runEval(taskId: string, projectDir: string): Promise<SpawnPayload> {
  return runSpawnEval(taskId, projectDir);
}

export function registerEval(program: Command): void {
  program
    .command('eval <taskId>')
    .description('Prepare evaluator task and output spawn payload as JSON')
    .option('--project <dir>', 'Project directory', process.cwd())
    .action(async (taskId: string, options: { project: string }) => {
      try {
        const payload = await runEval(taskId, options.project);
        console.log(JSON.stringify(payload, null, 2));
      } catch (err) {
        console.error('eval failed:', err instanceof Error ? err.message : err);
        process.exit(1);
      }
    });
}
