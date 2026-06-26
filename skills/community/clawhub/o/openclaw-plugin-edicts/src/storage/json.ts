import { readFile, writeFile, rename, access } from 'node:fs/promises';
import { createHash, randomUUID } from 'node:crypto';
import type { EdictFileSchema } from '../types.js';
import { DEFAULT_SCHEMA, type Storage } from './base.js';

export class JsonStorage implements Storage {
  constructor(private readonly path: string) {}

  async read(): Promise<EdictFileSchema> {
    if (!(await this.exists())) {
      return structuredClone(DEFAULT_SCHEMA);
    }
    const content = await readFile(this.path, 'utf-8');
    return JSON.parse(content) as EdictFileSchema;
  }

  async write(data: EdictFileSchema): Promise<void> {
    const content = JSON.stringify(data, null, 2) + '\n';
    const tmpPath = `${this.path}.${randomUUID()}.tmp`;
    await writeFile(tmpPath, content, 'utf-8');
    await rename(tmpPath, this.path);
  }

  async hash(): Promise<string | null> {
    if (!(await this.exists())) return null;
    const content = await readFile(this.path, 'utf-8');
    return createHash('sha256').update(content).digest('hex');
  }

  async exists(): Promise<boolean> {
    try {
      await access(this.path);
      return true;
    } catch {
      return false;
    }
  }
}
