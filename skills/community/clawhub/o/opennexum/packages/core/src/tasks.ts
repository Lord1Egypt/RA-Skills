import { mkdir, open, readFile, readdir, rename, rm, writeFile } from "node:fs/promises";
import path from "node:path";

import { parseContract } from "./contract";
import { TaskStatus, type ActiveTasksFile, type Task } from "./types";

const ACTIVE_TASKS_PATH = path.join("nexum", "active-tasks.json");
const CONTRACTS_DIR_PATH = path.join("docs", "nexum", "contracts");
const LOCK_RETRY_MS = 20;
const LOCK_TIMEOUT_MS = 2_000;
const STALE_LOCK_MS = 30_000;

export interface TaskSyncResult {
  created: string[];
  updated: string[];
  skipped: string[];
  totalContracts: number;
}

export async function readTasks(projectDir: string): Promise<Task[]> {
  const activeTasks = await readActiveTasksFile(projectDir);
  return activeTasks.tasks;
}

export async function writeTasks(projectDir: string, tasks: Task[]): Promise<void> {
  await withTasksLock(projectDir, async () => {
    const activeTasks = await readActiveTasksFile(projectDir);
    await writeActiveTasksFile(projectDir, { ...activeTasks, tasks });
  });
}

export async function getBatchProgress(
  projectDir: string,
  batch: string
): Promise<{ done: number; total: number; batch: string }> {
  const tasks = await readTasks(projectDir);
  const batchTasks = tasks.filter((task) => task.batch === batch);

  return {
    done: batchTasks.filter((task) => task.status === TaskStatus.Done).length,
    total: batchTasks.length,
    batch
  };
}

export async function getActiveBatch(projectDir: string): Promise<string | undefined> {
  const activeTasks = await readActiveTasksFile(projectDir);
  return activeTasks.currentBatch;
}

export async function writeBatch(projectDir: string, batch?: string): Promise<void> {
  await withTasksLock(projectDir, async () => {
    const activeTasks = await readActiveTasksFile(projectDir);
    await writeActiveTasksFile(projectDir, { ...activeTasks, currentBatch: batch });
  });
}

export async function syncTasksWithContracts(
  projectDir: string,
  options: { taskId?: string } = {}
): Promise<TaskSyncResult> {
  const contractFiles = await findContractFiles(projectDir);
  const created: string[] = [];
  const updated: string[] = [];
  const skipped: string[] = [];
  const normalizedTaskId = options.taskId?.trim();

  return withTasksLock(projectDir, async () => {
    const activeTasks = await readActiveTasksFile(projectDir);
    const existingById = new Map(activeTasks.tasks.map((task) => [task.id, task]));
    const parsedContracts = await Promise.all(
      contractFiles.map(async (contractPath) => {
        const contract = await parseContract(contractPath);
        return { contract, contractPath };
      })
    );

    const selectedContracts = normalizedTaskId
      ? parsedContracts.filter(({ contract }) => contract.id === normalizedTaskId)
      : parsedContracts;

    const completedIds = new Set(
      activeTasks.tasks
        .filter((task) => task.status === TaskStatus.Done)
        .map((task) => task.id)
    );
    const nextTasks = activeTasks.tasks.slice();

    for (const { contract, contractPath } of selectedContracts) {
      const normalizedContractPath = path.relative(projectDir, contractPath);
      const existing = existingById.get(contract.id);
      const nextStatus = normalizeSchedulableStatus(
        existing?.status,
        contract.depends_on,
        completedIds
      );
      const syncedTask: Task = {
        ...(existing ?? {}),
        id: contract.id,
        name: contract.name,
        batch: contract.batch ?? existing?.batch,
        status: nextStatus,
        contract_path: normalizedContractPath,
        depends_on: contract.depends_on
      };

      if (!existing) {
        nextTasks.push(syncedTask);
        existingById.set(contract.id, syncedTask);
        created.push(contract.id);
        continue;
      }

      const index = nextTasks.findIndex((task) => task.id === contract.id);
      if (index < 0) {
        nextTasks.push(syncedTask);
        updated.push(contract.id);
        continue;
      }

      if (hasTaskMetadataChanged(existing, syncedTask)) {
        nextTasks[index] = syncedTask;
        updated.push(contract.id);
      } else {
        skipped.push(contract.id);
      }
    }

    if (created.length > 0 || updated.length > 0) {
      await writeActiveTasksFile(projectDir, { ...activeTasks, tasks: nextTasks });
    }

    return {
      created,
      updated,
      skipped,
      totalContracts: selectedContracts.length
    };
  });
}

async function writeActiveTasksFile(
  projectDir: string,
  activeTasks: ActiveTasksFile
): Promise<void> {
  const filePath = getTasksFilePath(projectDir);
  const temporaryPath = `${filePath}.${process.pid}.${Date.now()}.tmp`;
  const payload = JSON.stringify(serializeActiveTasks(activeTasks), null, 2) + "\n";

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
    const activeTasks = await readActiveTasksFile(projectDir);
    const index = activeTasks.tasks.findIndex((task) => task.id === taskId);

    if (index < 0) {
      throw new Error(`Task not found: ${taskId}`);
    }

    const nextTask: Task = {
      ...activeTasks.tasks[index],
      ...patch,
      updated_at: patch.updated_at ?? new Date().toISOString()
    };

    const nextTasks = activeTasks.tasks.slice();
    nextTasks[index] = nextTask;
    await writeActiveTasksFile(projectDir, { ...activeTasks, tasks: nextTasks });

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

async function readActiveTasksFile(projectDir: string): Promise<ActiveTasksFile> {
  const filePath = getTasksFilePath(projectDir);

  try {
    const contents = await readFile(filePath, "utf8");
    const parsed = JSON.parse(contents) as ActiveTasksFile;

    if (!parsed || !Array.isArray(parsed.tasks)) {
      throw new Error(`Invalid active tasks file: ${filePath}`);
    }

    if (parsed.currentBatch !== undefined && typeof parsed.currentBatch !== "string") {
      throw new Error(`Invalid currentBatch in ${filePath}`);
    }

    return {
      tasks: parsed.tasks.map((task) => normalizeTask(task, filePath)),
      currentBatch: parsed.currentBatch
    };
  } catch (error) {
    if (isNodeError(error) && error.code === "ENOENT") {
      return { tasks: [] };
    }

    throw error;
  }
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

  if (task.batch !== undefined && typeof task.batch !== "string") {
    throw new Error(`Invalid task batch for ${task.id} in ${filePath}`);
  }

  return task;
}

function hasTaskMetadataChanged(current: Task, next: Task): boolean {
  return (
    current.name !== next.name ||
    current.batch !== next.batch ||
    current.status !== next.status ||
    current.contract_path !== next.contract_path ||
    !sameStringArray(current.depends_on, next.depends_on)
  );
}

function normalizeSchedulableStatus(
  currentStatus: TaskStatus | undefined,
  dependsOn: string[],
  completedIds: Set<string>
): TaskStatus {
  if (
    currentStatus &&
    currentStatus !== TaskStatus.Pending &&
    currentStatus !== TaskStatus.Blocked
  ) {
    return currentStatus;
  }

  return dependsOn.every((dependencyId) => completedIds.has(dependencyId))
    ? TaskStatus.Pending
    : TaskStatus.Blocked;
}

async function findContractFiles(projectDir: string): Promise<string[]> {
  const contractsDir = path.join(projectDir, CONTRACTS_DIR_PATH);
  const discovered: string[] = [];

  await walkContractDir(contractsDir, discovered);

  return discovered.sort();
}

async function walkContractDir(dirPath: string, discovered: string[]): Promise<void> {
  try {
    const entries = await readdir(dirPath, { withFileTypes: true });

    for (const entry of entries) {
      if (entry.name.startsWith(".")) {
        continue;
      }

      const entryPath = path.join(dirPath, entry.name);
      if (entry.isDirectory()) {
        await walkContractDir(entryPath, discovered);
        continue;
      }

      if (entry.isFile() && /\.(yaml|yml)$/i.test(entry.name)) {
        discovered.push(entryPath);
      }
    }
  } catch (error) {
    if (isNodeError(error) && error.code === "ENOENT") {
      return;
    }

    throw error;
  }
}

function sameStringArray(left: string[], right: string[]): boolean {
  if (left.length !== right.length) {
    return false;
  }

  return left.every((entry, index) => entry === right[index]);
}

function serializeActiveTasks(activeTasks: ActiveTasksFile): ActiveTasksFile {
  return activeTasks.currentBatch === undefined
    ? { tasks: activeTasks.tasks }
    : { tasks: activeTasks.tasks, currentBatch: activeTasks.currentBatch };
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
