import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { readTasks, TaskStatus, type Task, writeTasks } from '@nexum/core';

export interface ArchiveResult {
  archivePath: string;
  archivedCount: number;
}

export async function archiveDoneTasks(
  projectDir: string,
  batch?: string
): Promise<ArchiveResult> {
  const archiveName = batch ?? new Date().toISOString().slice(0, 10);
  const archivePath = path.join(projectDir, 'nexum', 'history', `${archiveName}.json`);
  const tasks = await readTasks(projectDir);
  const tasksToArchive = tasks.filter(
    (task) => task.status === TaskStatus.Done && (batch === undefined || task.batch === batch)
  );

  if (tasksToArchive.length === 0) {
    return { archivePath, archivedCount: 0 };
  }

  const existingTasks = await readArchiveFile(archivePath);
  await mkdir(path.dirname(archivePath), { recursive: true });
  await writeFile(
    archivePath,
    JSON.stringify([...existingTasks, ...tasksToArchive], null, 2) + '\n',
    'utf8'
  );

  const remainingTasks = tasks.filter(
    (task) => task.status !== TaskStatus.Done || (batch !== undefined && task.batch !== batch)
  );
  await writeTasks(projectDir, remainingTasks);

  return { archivePath, archivedCount: tasksToArchive.length };
}

async function readArchiveFile(archivePath: string): Promise<Task[]> {
  try {
    const raw = await readFile(archivePath, 'utf8');
    const parsed = JSON.parse(raw) as Task[];

    if (!Array.isArray(parsed)) {
      throw new Error(`Invalid archive file: ${archivePath}`);
    }

    return parsed;
  } catch (error) {
    if (isNodeError(error) && error.code === 'ENOENT') {
      return [];
    }

    throw error;
  }
}

function isNodeError(error: unknown): error is NodeJS.ErrnoException {
  return error instanceof Error;
}
