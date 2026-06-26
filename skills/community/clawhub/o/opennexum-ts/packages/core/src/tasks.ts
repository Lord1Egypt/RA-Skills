import { mkdir, open, readFile, rename, rm, writeFile } from "node:fs/promises";
import path from "node:path";

import { TaskStatus, type ActiveTasksFile, type Task } from "./types";

const ACTIVE_TASKS_PATH = path.join("nexum", "active-tasks.json");
const LOCK_RETRY_MS = 20;
const LOCK_TIMEOUT_MS = 2_000;
const STALE_LOCK_MS = 30_000;

export async function readTasks(projectDir: string): Promise<Task[]> {
  const filePath = getTasksFilePath(projectDir);

  try {
    const contents = await readFile(filePath, "utf8");
    const parsed = JSON.parse(contents) as ActiveTasksFile;

    if (!parsed || !Array.isArray(parsed.tasks)) {
      throw new Error(`Invalid active tasks file: ${filePath}`);
    }

    return parsed.tasks.map((task) => normalizeTask(task, filePath));
  } catch (error) {
    if (isNodeError(error) && error.code === "ENOENT") {
      return [];
    }

    throw error;
  }
}

export async function writeTasks(projectDir: string, tasks: Task[]): Promise<void> {
  const filePath = getTasksFilePath(projectDir);
  const temporaryPath = `${filePath}.${process.pid}.${Date.now()}.tmp`;
  const payload = JSON.stringify({ tasks }, null, 2) + "\n";

  try {
    await mkdir(path.dirname(filePath), { recursive: true });
    await writeFile(temporaryPath, payload, "utf8");
    await rename(temporaryPath, filePath);
  } catch (error) {
    await rm(temporaryPath, { force: true });
    throw error;
  }
}

export async function updateTask(
  projectDir: string,
  taskId: string,
  patch: Partial<Task>
): Promise<Task> {
  return withTasksLock(projectDir, async () => {
    const tasks = await readTasks(projectDir);
    const index = tasks.findIndex((task) => task.id === taskId);

    if (index < 0) {
      throw new Error(`Task not found: ${taskId}`);
    }

    const nextTask: Task = {
      ...tasks[index],
      ...patch,
      updated_at: patch.updated_at ?? new Date().toISOString()
    };

    const nextTasks = tasks.slice();
    nextTasks[index] = nextTask;
    await writeTasks(projectDir, nextTasks);

    return nextTask;
  });
}

export async function getTask(projectDir: string, taskId: string): Promise<Task | undefined> {
  const tasks = await readTasks(projectDir);
  return tasks.find((task) => task.id === taskId);
}

export async function getUnlockedTasks(
  projectDir: string,
  completedTaskId: string
): Promise<Task[]> {
  const tasks = await readTasks(projectDir);
  const completedIds = new Set(
    tasks.filter((task) => task.status === TaskStatus.Done).map((task) => task.id)
  );
  completedIds.add(completedTaskId);

  return tasks.filter(
    (task) =>
      task.status === TaskStatus.Pending &&
      task.depends_on.includes(completedTaskId) &&
      task.depends_on.every((dependencyId) => completedIds.has(dependencyId))
  );
}

function getTasksFilePath(projectDir: string): string {
  return path.join(projectDir, ACTIVE_TASKS_PATH);
}

function getLockFilePath(projectDir: string): string {
  return `${getTasksFilePath(projectDir)}.lock`;
}

async function withTasksLock<T>(
  projectDir: string,
  callback: () => Promise<T>
): Promise<T> {
  const lockPath = getLockFilePath(projectDir);
  const startedAt = Date.now();

  while (true) {
    try {
      const handle = await open(lockPath, "wx");

      try {
        await handle.writeFile(`${process.pid}:${startedAt}`, "utf8");
        return await callback();
      } finally {
        await handle.close();
        await rm(lockPath, { force: true });
      }
    } catch (error) {
      if (!isNodeError(error) || error.code !== "EEXIST") {
        throw error;
      }

      await clearStaleLock(lockPath);

      if (Date.now() - startedAt >= LOCK_TIMEOUT_MS) {
        throw new Error(`Timed out waiting for task lock: ${lockPath}`);
      }

      await sleep(LOCK_RETRY_MS);
    }
  }
}

async function clearStaleLock(lockPath: string): Promise<void> {
  try {
    const stats = await readFile(lockPath, "utf8");
    const [, createdAtText] = stats.split(":");
    const createdAt = Number.parseInt(createdAtText ?? "0", 10);

    if (Number.isFinite(createdAt) && Date.now() - createdAt > STALE_LOCK_MS) {
      await rm(lockPath, { force: true });
    }
  } catch (error) {
    if (isNodeError(error) && error.code === "ENOENT") {
      return;
    }

    throw error;
  }
}

function normalizeTask(task: Task, filePath: string): Task {
  if (
    !task ||
    typeof task.id !== "string" ||
    typeof task.name !== "string" ||
    typeof task.contract_path !== "string" ||
    !Array.isArray(task.depends_on) ||
    !task.depends_on.every((dependency) => typeof dependency === "string")
  ) {
    throw new Error(`Invalid task entry in ${filePath}`);
  }

  if (!isTaskStatus(task.status)) {
    throw new Error(`Invalid task status for ${task.id} in ${filePath}`);
  }

  return task;
}

function isTaskStatus(value: unknown): value is TaskStatus {
  return Object.values(TaskStatus).includes(value as TaskStatus);
}

function isNodeError(error: unknown): error is NodeJS.ErrnoException {
  return error instanceof Error;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}
