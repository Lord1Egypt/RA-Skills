import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';
import { SkillError } from './errors.mjs';

function safeSessionId(sessionId) {
  const value = String(sessionId || '');
  if (!/^[a-zA-Z0-9-]{8,80}$/.test(value)) {
    throw new SkillError('INVALID_SESSION_ID', '任务编号格式不正确');
  }
  return value;
}

async function writePrivateJson(filePath, value) {
  const tempPath = `${filePath}.${process.pid}.${crypto.randomUUID()}.tmp`;
  await fs.writeFile(tempPath, `${JSON.stringify(value, null, 2)}\n`, { mode: 0o600 });
  await fs.chmod(tempPath, 0o600);
  await fs.rename(tempPath, filePath);
}

export class StateStore {
  constructor(config) {
    this.dir = config.stateDir;
    this.ttlMs = config.stateTtlMs;
  }

  async ensure() {
    await fs.mkdir(this.dir, { recursive: true, mode: 0o700 });
    await fs.chmod(this.dir, 0o700);
  }

  sessionPath(sessionId) {
    return path.join(this.dir, `${safeSessionId(sessionId)}.json`);
  }

  async identity() {
    await this.ensure();
    const identityPath = path.join(this.dir, 'identity.json');
    try {
      const value = JSON.parse(await fs.readFile(identityPath, 'utf8'));
      if (value?.userId) return value;
    } catch (error) {
      if (error.code !== 'ENOENT') throw error;
    }

    const value = {
      userId: `skill-${crypto.randomUUID()}`,
      machineId: `skill-${crypto.randomUUID()}`,
      createdAt: new Date().toISOString()
    };
    await writePrivateJson(identityPath, value);
    return value;
  }

  async create(initial = {}) {
    await this.ensure();
    const now = new Date().toISOString();
    const state = {
      sessionId: crypto.randomUUID(),
      createdAt: now,
      updatedAt: now,
      ...initial
    };
    await this.save(state);
    return state;
  }

  async load(sessionId) {
    await this.ensure();
    try {
      return JSON.parse(await fs.readFile(this.sessionPath(sessionId), 'utf8'));
    } catch (error) {
      if (error.code === 'ENOENT') {
        throw new SkillError('SESSION_NOT_FOUND', '没有找到对应任务，请重新开始');
      }
      if (error instanceof SyntaxError) {
        throw new SkillError('SESSION_CORRUPTED', '任务状态文件损坏，请重新开始');
      }
      throw error;
    }
  }

  async save(state) {
    await this.ensure();
    if (!state?.sessionId) {
      throw new SkillError('SESSION_ID_REQUIRED', '保存任务时缺少任务编号');
    }
    const next = { ...state, updatedAt: new Date().toISOString() };
    await writePrivateJson(this.sessionPath(next.sessionId), next);
    return next;
  }

  async remove(sessionId) {
    await fs.rm(this.sessionPath(sessionId), { force: true });
    await fs.rm(path.join(this.dir, safeSessionId(sessionId)), { recursive: true, force: true });
  }

  async writeArtifact(sessionId, filename, content) {
    await this.ensure();
    const artifactDir = path.join(this.dir, safeSessionId(sessionId));
    await fs.mkdir(artifactDir, { recursive: true, mode: 0o700 });
    const safeName = path.basename(String(filename)).replace(/[^a-zA-Z0-9._-]/g, '_');
    const filePath = path.join(artifactDir, safeName || 'artifact');
    await fs.writeFile(filePath, content, { mode: 0o600 });
    await fs.chmod(filePath, 0o600);
    return filePath;
  }

  async cleanup() {
    await this.ensure();
    const entries = await fs.readdir(this.dir, { withFileTypes: true });
    const now = Date.now();
    let removed = 0;
    for (const entry of entries) {
      if (!entry.isFile() || entry.name === 'identity.json' || !entry.name.endsWith('.json')) continue;
      const filePath = path.join(this.dir, entry.name);
      const stat = await fs.stat(filePath);
      if (now - stat.mtimeMs > this.ttlMs) {
        await fs.rm(filePath, { force: true });
        await fs.rm(path.join(this.dir, entry.name.replace(/\.json$/, '')), { recursive: true, force: true });
        removed += 1;
      }
    }
    return removed;
  }
}
