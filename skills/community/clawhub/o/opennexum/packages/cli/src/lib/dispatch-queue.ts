import { mkdir, open, readFile, rename, rm, writeFile } from "node:fs/promises";
import path from "node:path";

import { getTask, TaskStatus } from "@nexum/core";

import { dispatchAgentWebhook } from "./webhook.js";

export type DispatchAction = "spawn-evaluator" | "spawn-retry" | "spawn-next";

export interface DispatchQueueEntry {
  taskId: string;
  action: DispatchAction;
  role: "generator" | "evaluator";
  projectDir: string;
  sessionName: string;
  createdAt: string;
  lastAttemptAt?: string;
  attempts?: number;
}

const DISPATCH_QUEUE_PATH = path.join("nexum", "dispatch-queue.jsonl");
const LOCK_RETRY_MS = 20;
const LOCK_TIMEOUT_MS = 2_000;
const STALE_LOCK_MS = 30_000;

export async function enqueueDispatchEntry(
  projectDir: string,
  entry: Omit<DispatchQueueEntry, "createdAt" | "attempts" | "lastAttemptAt">
): Promise<void> {
  await withDispatchQueueLock(projectDir, async () => {
    const entries = await readDispatchQueueEntries(projectDir);
    if (entries.some((item) => item.taskId === entry.taskId && item.action === entry.action)) {
      return;
    }

    entries.push({
      ...entry,
      createdAt: new Date().toISOString(),
      attempts: 0
    });

    await writeDispatchQueueEntries(projectDir, entries);
  });
}

export async function acknowledgeDispatchEntries(
  projectDir: string,
  predicate: (entry: DispatchQueueEntry) => boolean
): Promise<void> {
  await withDispatchQueueLock(projectDir, async () => {
    const entries = await readDispatchQueueEntries(projectDir);
    const nextEntries = entries.filter((entry) => !predicate(entry));

    if (nextEntries.length !== entries.length) {
      await writeDispatchQueueEntries(projectDir, nextEntries);
    }
  });
}

export async function processDispatchQueue(projectDir: string): Promise<{
  queued: number;
  retried: number;
  acknowledged: number;
}> {
  const entries = await readDispatchQueueEntries(projectDir);
  let retried = 0;
  let acknowledged = 0;

  for (const entry of entries) {
    if (await isDispatchSatisfied(projectDir, entry)) {
      await acknowledgeDispatchEntries(
        projectDir,
        (candidate) => candidate.taskId === entry.taskId && candidate.action === entry.action
      );
      acknowledged += 1;
      continue;
    }

    const dispatched = await dispatchAgentWebhook(
      entry.taskId,
      entry.role,
      projectDir,
      entry.sessionName
    );

    if (!dispatched) {
      continue;
    }

    retried += 1;
    await withDispatchQueueLock(projectDir, async () => {
      const currentEntries = await readDispatchQueueEntries(projectDir);
      const nextEntries = currentEntries.map((candidate) =>
        candidate.taskId === entry.taskId && candidate.action === entry.action
          ? {
              ...candidate,
              attempts: (candidate.attempts ?? 0) + 1,
              lastAttemptAt: new Date().toISOString()
            }
          : candidate
      );
      await writeDispatchQueueEntries(projectDir, nextEntries);
    });
  }

  return { queued: entries.length, retried, acknowledged };
}

export async function readDispatchQueueEntries(
  projectDir: string
): Promise<DispatchQueueEntry[]> {
  const queuePath = getDispatchQueuePath(projectDir);

  try {
    const raw = await readFile(queuePath, "utf8");
    return raw
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line.length > 0)
      .map((line) => JSON.parse(line) as DispatchQueueEntry);
  } catch (error) {
    if (isNodeError(error) && error.code === "ENOENT") {
      return [];
    }

    throw error;
  }
}

async function writeDispatchQueueEntries(
  projectDir: string,
  entries: DispatchQueueEntry[]
): Promise<void> {
  const queuePath = getDispatchQueuePath(projectDir);
  const tempPath = `${queuePath}.${process.pid}.${Date.now()}.tmp`;
  const payload =
    entries.length === 0
      ? ""
      : `${entries.map((entry) => JSON.stringify(entry)).join("\n")}\n`;

  try {
    await mkdir(path.dirname(queuePath), { recursive: true });
    await writeFile(tempPath, payload, "utf8");
    await rename(tempPath, queuePath);
  } catch (error) {
    await rm(tempPath, { force: true });
    throw error;
  }
}

async function isDispatchSatisfied(
  projectDir: string,
  entry: DispatchQueueEntry
): Promise<boolean> {
  const task = await getTask(projectDir, entry.taskId);
  if (!task) {
    return true;
  }

  switch (entry.action) {
    case "spawn-evaluator":
      return task.status !== TaskStatus.GeneratorDone;
    case "spawn-retry":
    case "spawn-next":
      return task.status !== TaskStatus.Pending;
    default:
      return true;
  }
}

function getDispatchQueuePath(projectDir: string): string {
  return path.join(projectDir, DISPATCH_QUEUE_PATH);
}

function getDispatchQueueLockPath(projectDir: string): string {
  return `${getDispatchQueuePath(projectDir)}.lock`;
}

async function withDispatchQueueLock<T>(
  projectDir: string,
  callback: () => Promise<T>
): Promise<T> {
  const lockPath = getDispatchQueueLockPath(projectDir);
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
        throw new Error(`Timed out waiting for dispatch queue lock: ${lockPath}`);
      }

      await sleep(LOCK_RETRY_MS);
    }
  }
}

async function clearStaleLock(lockPath: string): Promise<void> {
  try {
    const raw = await readFile(lockPath, "utf8");
    const [, createdAtText] = raw.split(":");
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

function isNodeError(error: unknown): error is NodeJS.ErrnoException {
  return error instanceof Error;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}
