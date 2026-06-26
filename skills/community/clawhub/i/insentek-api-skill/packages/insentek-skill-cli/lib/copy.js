import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { ASSET_ENTRIES, ASSETS_DIR } from './constants.js';
import { ensureDir, pathExists, removeDir } from './utils.js';

const COPY_IGNORE_DIRS = new Set(['__pycache__']);

function shouldCopyAssetEntry(name) {
  return !COPY_IGNORE_DIRS.has(name);
}

export async function copyDirectoryFiltered(sourcePath, targetPath) {
  await fs.cp(sourcePath, targetPath, {
    recursive: true,
    force: true,
    filter: (src) => shouldCopyAssetEntry(path.basename(src)),
  });
}

async function copyEntry(sourceRoot, entryName, targetRoot) {
  const sourcePath = path.join(sourceRoot, entryName);
  const targetPath = path.join(targetRoot, entryName);

  if (!(await pathExists(sourcePath))) {
    throw new Error(`Missing bundled asset: ${entryName}`);
  }

  const stat = await fs.stat(sourcePath);
  if (stat.isDirectory()) {
    await copyDirectoryFiltered(sourcePath, targetPath);
  } else {
    await ensureDir(path.dirname(targetPath));
    await fs.copyFile(sourcePath, targetPath);
  }
}

async function copyAssetsFromSource(sourceRoot, targetRoot) {
  await ensureDir(targetRoot);
  for (const entry of ASSET_ENTRIES) {
    await copyEntry(sourceRoot, entry, targetRoot);
  }
}

function buildSidecarDir(targetDir, suffix) {
  return path.join(
    path.dirname(targetDir),
    `${path.basename(targetDir)}.${suffix}-${process.pid}-${Date.now()}`,
  );
}

async function cleanupSidecarDir(dirPath) {
  if (dirPath && await pathExists(dirPath)) {
    await removeDir(dirPath);
  }
}

function isRenameLockError(error) {
  return ['EPERM', 'EACCES', 'EBUSY', 'EXDEV'].includes(error?.code);
}

export async function replaceDirectoryAtomic(sourceRoot, targetDir) {
  const stagingDir = buildSidecarDir(targetDir, 'staging');
  let backupDir = null;

  try {
    await copyAssetsFromSource(sourceRoot, stagingDir);

    const hadExisting = await pathExists(targetDir);
    if (!hadExisting) {
      await fs.rename(stagingDir, targetDir);
      return;
    }

    // Windows often locks skill dirs (e.g. OpenClaw); in-place overwrite avoids EPERM on rename.
    if (process.platform === 'win32') {
      await copyAssetsFromSource(stagingDir, targetDir);
      await cleanupSidecarDir(stagingDir);
      return;
    }

    try {
      backupDir = buildSidecarDir(targetDir, 'backup');
      await fs.rename(targetDir, backupDir);
      await fs.rename(stagingDir, targetDir);
      await cleanupSidecarDir(backupDir);
    } catch (renameError) {
      if (!isRenameLockError(renameError)) {
        throw renameError;
      }
      await copyAssetsFromSource(stagingDir, targetDir);
      await cleanupSidecarDir(stagingDir);
      await cleanupSidecarDir(backupDir);
    }
  } catch (error) {
    await cleanupSidecarDir(stagingDir);

    if (backupDir && await pathExists(backupDir)) {
      if (!(await pathExists(targetDir))) {
        await fs.rename(backupDir, targetDir);
      } else {
        await cleanupSidecarDir(targetDir);
        await fs.rename(backupDir, targetDir);
      }
    }

    throw error;
  }
}

export async function copySkillAssets(targetDir, { force = false } = {}) {
  if (!(await pathExists(ASSETS_DIR))) {
    throw new Error(
      'Skill assets not found. Run "npm run sync-assets" inside packages/insentek-skill-cli.',
    );
  }

  const exists = await pathExists(targetDir);
  if (exists && !force) {
    throw new Error(`Target already exists: ${targetDir}. Use --force to overwrite.`);
  }

  if (exists && force) {
    await replaceDirectoryAtomic(ASSETS_DIR, targetDir);
    return;
  }

  await copyAssetsFromSource(ASSETS_DIR, targetDir);
}
