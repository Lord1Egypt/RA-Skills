import { access, mkdir, readFile, rename, rm, writeFile } from "node:fs/promises";
import path from "node:path";

import type { SessionRecord, SpawnOptions } from "./types.js";

const ACTIVE_TASKS_RELATIVE_PATH = path.join("nexum", "active-tasks.json");
type ExecaResult = {
  stdout: string;
  stderr: string;
  exitCode: number;
};
type ExecaRunner = (
  command: string,
  args: string[],
  options: { reject: false }
) => Promise<ExecaResult>;
const testingGlobals = globalThis as typeof globalThis & {
  __nexumSpawnExeca?: ExecaRunner;
};
let cachedExecaRunner: ExecaRunner | undefined;
const loadExecaModule = new Function("return import('execa')") as () => Promise<{ execa: ExecaRunner }>;

interface ActiveTask {
  id: string;
  acp_session_key?: string;
  updated_at?: string;
  [key: string]: unknown;
}

interface ActiveTasksFile {
  tasks: ActiveTask[];
}

export function buildPromptArgs(promptFilePath: string): string[] {
  return ["--task-file", promptFilePath];
}

export async function spawnAcpSession(options: SpawnOptions): Promise<SessionRecord> {
  const startedAt = new Date().toISOString();
  const args = [
    "sessions",
    "spawn",
    "--runtime",
    "acp",
    "--agent",
    options.agentId,
    "--mode",
    options.mode,
    "--cwd",
    options.cwd,
    "--label",
    options.label,
    ...buildPromptArgs(options.promptFile)
  ];
  const result = await (await getExecaRunner())("openclaw", args, { reject: false });

  if (result.exitCode !== 0) {
    throw new Error(result.stderr || result.stdout || "Failed to spawn ACP session.");
  }

  const sessionKey = parseSessionKey(result.stdout);
  await updateActiveTaskSessionKey(options.cwd, options.taskId, sessionKey, startedAt);

  return {
    taskId: options.taskId,
    sessionKey,
    agentId: options.agentId,
    startedAt,
    status: "running"
  };
}

function parseSessionKey(output: string): string {
  if (!output.trim()) {
    throw new Error("OpenClaw spawn command returned no output.");
  }

  try {
    const parsed = JSON.parse(output) as Record<string, unknown>;
    const value = pickSessionKey(parsed);

    if (value) {
      return value;
    }
  } catch {
    // Fall back to text parsing because some CLI builds print banners/log lines.
  }

  const match = output.match(
    /"(?:childSessionKey|sessionKey|key)"\s*:\s*"([^"]+)"|(?:childSessionKey|sessionKey|key)\s*[:=]\s*([^\s]+)/m
  );
  const sessionKey = match?.[1] ?? match?.[2];

  if (!sessionKey) {
    throw new Error(`Unable to parse session key from OpenClaw output: ${output}`);
  }

  return sessionKey.trim();
}

function pickSessionKey(record: Record<string, unknown>): string | undefined {
  for (const key of ["childSessionKey", "sessionKey", "key"]) {
    const value = record[key];

    if (typeof value === "string" && value.trim()) {
      return value.trim();
    }
  }

  return undefined;
}

async function updateActiveTaskSessionKey(
  startDir: string,
  taskId: string,
  sessionKey: string,
  updatedAt: string
): Promise<void> {
  const projectDir = await resolveProjectDir(startDir);
  const filePath = path.join(projectDir, ACTIVE_TASKS_RELATIVE_PATH);
  const temporaryPath = `${filePath}.${process.pid}.${Date.now()}.tmp`;
  const payload = await readActiveTasks(filePath);
  const task = payload.tasks.find((entry) => entry.id === taskId);

  if (!task) {
    throw new Error(`Task not found in active-tasks.json: ${taskId}`);
  }

  task.acp_session_key = sessionKey;
  task.updated_at = updatedAt;

  try {
    await mkdir(path.dirname(filePath), { recursive: true });
    await writeFile(temporaryPath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
    await rename(temporaryPath, filePath);
  } catch (error) {
    await rm(temporaryPath, { force: true });
    throw error;
  }
}

async function readActiveTasks(filePath: string): Promise<ActiveTasksFile> {
  const raw = await readFile(filePath, "utf8");
  const parsed = JSON.parse(raw) as ActiveTasksFile;

  if (!parsed || !Array.isArray(parsed.tasks)) {
    throw new Error(`Invalid active tasks file: ${filePath}`);
  }

  return parsed;
}

async function resolveProjectDir(startDir: string): Promise<string> {
  let currentDir = path.resolve(startDir);

  while (true) {
    try {
      await access(path.join(currentDir, ACTIVE_TASKS_RELATIVE_PATH));
      return currentDir;
    } catch {
      const parentDir = path.dirname(currentDir);

      if (parentDir === currentDir) {
        return path.resolve(startDir);
      }

      currentDir = parentDir;
    }
  }
}

async function getExecaRunner(): Promise<ExecaRunner> {
  if (testingGlobals.__nexumSpawnExeca) {
    return testingGlobals.__nexumSpawnExeca;
  }

  if (cachedExecaRunner) {
    return cachedExecaRunner;
  }

  const { execa } = await loadExecaModule();
  cachedExecaRunner = execa;
  return execa;
}
