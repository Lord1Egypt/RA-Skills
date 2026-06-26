import type { Command } from "commander";

import { syncTasksWithContracts } from "@nexum/core";

export async function runSync(
  projectDir: string,
  taskId?: string
): Promise<Awaited<ReturnType<typeof syncTasksWithContracts>>> {
  return syncTasksWithContracts(projectDir, taskId ? { taskId } : {});
}

export function registerSync(program: Command): void {
  program
    .command("sync [taskId]")
    .description("Sync docs/nexum/contracts into nexum/active-tasks.json")
    .option("--project <dir>", "Project directory", process.cwd())
    .option("--json", "Output sync summary as JSON")
    .action(async (taskId: string | undefined, options: { project: string; json?: boolean }) => {
      try {
        const result = await runSync(options.project, taskId);

        if (options.json) {
          console.log(JSON.stringify(result, null, 2));
          return;
        }

        console.log(
          `Synced ${result.totalContracts} contract(s): ${result.created.length} created, ${result.updated.length} updated, ${result.skipped.length} unchanged.`
        );
      } catch (err) {
        console.error("sync failed:", err instanceof Error ? err.message : err);
        process.exit(1);
      }
    });
}
