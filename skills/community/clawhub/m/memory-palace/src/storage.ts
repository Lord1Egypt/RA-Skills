/**
 * Memory Palace - File Storage
 * 
 * Handles persistence of memories as Markdown files.
 * 
 * Concurrency: Uses in-memory locks to prevent race conditions within a single process.
 * For multi-process scenarios, consider using proper-lockfile or a database backend.
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import type { Memory, MemoryStatus, MemorySource, MemoryType, ExperienceMeta } from './types.js';

/**
 * Simple in-memory lock for file operations
 * Prevents race conditions within a single process
 */
class FileLock {
  private locks = new Map<string, Promise<void>>();
  
  async withLock<T>(key: string, fn: () => Promise<T>): Promise<T> {
    // Wait for any existing lock
    while (this.locks.has(key)) {
      await this.locks.get(key);
    }
    
    // Create new lock
    let releaseLock: () => void;
    const lockPromise = new Promise<void>(resolve => {
      releaseLock = resolve;
    });
    this.locks.set(key, lockPromise);
    
    try {
      return await fn();
    } finally {
      this.locks.delete(key);
      releaseLock!();
    }
  }
}

// Global lock instance
const fileLock = new FileLock();

/**
 * Parse frontmatter from markdown content
 */
function parseFrontmatter(content: string): { frontmatter: Record<string, unknown>; body: string } {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  
  if (!match) {
    return { frontmatter: {}, body: content };
  }
  
  const frontmatter: Record<string, unknown> = {};
  const lines = match[1].split('\n');
  
  for (const line of lines) {
    const colonIndex = line.indexOf(':');
    if (colonIndex > 0) {
      const key = line.slice(0, colonIndex).trim();
      let value: unknown = line.slice(colonIndex + 1).trim();
      
      // Parse JSON values (arrays, objects, quoted strings)
      if (typeof value === 'string') {
        if ((value.startsWith('[') && value.endsWith(']')) ||
            (value.startsWith('{') && value.endsWith('}')) ||
            (value.startsWith('"') && value.endsWith('"'))) {
          try {
            value = JSON.parse(value);
          } catch {
            // Keep as string
          }
        } else if (value === 'true' || value === 'false') {
          value = value === 'true';
        } else if (!isNaN(Number(value))) {
          value = Number(value);
        }
      }
      
      frontmatter[key] = value;
    }
  }
  
  return { frontmatter, body: match[2] };
}

/**
 * Generate frontmatter string
 */
function generateFrontmatter(memory: Memory): string {
  const lines = [
    '---',
    `id: ${JSON.stringify(memory.id)}`,
    `tags: ${JSON.stringify(memory.tags)}`,
    `importance: ${memory.importance}`,
    `status: ${JSON.stringify(memory.status)}`,
    `createdAt: ${JSON.stringify(memory.createdAt.toISOString())}`,
    `updatedAt: ${JSON.stringify(memory.updatedAt.toISOString())}`,
    `source: ${JSON.stringify(memory.source)}`,
    `location: ${JSON.stringify(memory.location)}`,
  ];
  
  if (memory.summary) {
    lines.push(`summary: ${JSON.stringify(memory.summary)}`);
  }
  
  if (memory.deletedAt) {
    lines.push(`deletedAt: ${JSON.stringify(memory.deletedAt.toISOString())}`);
  }
  
  if (memory.type) {
    lines.push(`type: ${JSON.stringify(memory.type)}`);
  }
  
  if (memory.experienceMeta) {
    lines.push(`experienceMeta: ${JSON.stringify(memory.experienceMeta)}`);
  }
  
  // Memory relations
  if (memory.relations && memory.relations.length > 0) {
    lines.push(`relations: ${JSON.stringify(memory.relations)}`);
  }
  
  // Ebbinghaus decay metrics
  if (memory.decay) {
    lines.push(`decay: ${JSON.stringify({
      decayScore: memory.decay.decayScore,
      accessCount: memory.decay.accessCount,
      lastAccessedAt: memory.decay.lastAccessedAt?.toISOString(),
    })}`);
  }
  
  lines.push('---');
  
  return lines.join('\n');
}

/**
 * Serialize memory to markdown
 */
export function serializeMemory(memory: Memory): string {
  const frontmatter = generateFrontmatter(memory);
  let body = memory.content;
  
  if (memory.summary) {
    body = memory.content + '\n\n## Summary\n' + memory.summary;
  }
  
  return frontmatter + '\n' + body;
}

/**
 * Deserialize memory from markdown
 */
export function deserializeMemory(content: string, id: string): Memory {
  const { frontmatter, body } = parseFrontmatter(content);
  
  // Extract summary from body if present
  let mainContent = body;
  let summary: string | undefined;
  
  const summaryMatch = body.match(/^(.*)\n\n## Summary\n([\s\S]*)$/);
  if (summaryMatch) {
    mainContent = summaryMatch[1];
    summary = summaryMatch[2].trim();
  }
  
  // Parse experienceMeta if present
  let experienceMeta: ExperienceMeta | undefined;
  if (frontmatter.experienceMeta && typeof frontmatter.experienceMeta === 'object') {
    const meta = frontmatter.experienceMeta as Record<string, unknown>;
    experienceMeta = {
      category: meta.category as string,
      applicability: meta.applicability as string,
      source: meta.source as string,
      verified: meta.verified as boolean,
      verifiedCount: meta.verifiedCount as number | undefined,
      lastVerifiedAt: meta.lastVerifiedAt ? new Date(meta.lastVerifiedAt as string) : undefined,
      effectivenessScore: meta.effectivenessScore as number ?? 0,
      usageCount: meta.usageCount as number ?? 0,
      lastUsedAt: meta.lastUsedAt ? new Date(meta.lastUsedAt as string) : undefined,
    };
  }
  
  // Parse decay metrics if present (Ebbinghaus forgetting curve)
  let decay: Memory['decay'] = undefined;
  if (frontmatter.decay && typeof frontmatter.decay === 'object') {
    const decayData = frontmatter.decay as Record<string, unknown>;
    decay = {
      decayScore: decayData.decayScore as number ?? 1.0,
      accessCount: decayData.accessCount as number ?? 0,
      lastAccessedAt: decayData.lastAccessedAt 
        ? new Date(decayData.lastAccessedAt as string) 
        : undefined,
    };
  }
  
  return {
    id: frontmatter.id as string || id,
    content: mainContent.trim(),
    summary,
    tags: frontmatter.tags as string[] || [],
    importance: frontmatter.importance as number || 0.5,
    status: (frontmatter.status as MemoryStatus) || 'active',
    source: (frontmatter.source as MemorySource) || 'user',
    location: frontmatter.location as string || 'default',
    createdAt: new Date(frontmatter.createdAt as string || Date.now()),
    updatedAt: new Date(frontmatter.updatedAt as string || Date.now()),
    deletedAt: frontmatter.deletedAt ? new Date(frontmatter.deletedAt as string) : undefined,
    type: frontmatter.type as MemoryType | undefined,
    experienceMeta,
    decay,
    relations: frontmatter.relations as Memory['relations'],
  };
}

/**
 * File storage for memories
 */
export class FileStorage {
  private storagePath: string;
  
  constructor(storagePath: string) {
    this.storagePath = storagePath;
  }
  
  /**
   * Ensure storage directory exists
   */
  async ensureDir(): Promise<void> {
    await fs.mkdir(this.storagePath, { recursive: true });
    
    // Also ensure trash directory
    await fs.mkdir(path.join(this.storagePath, '.trash'), { recursive: true });
  }
  
  /**
   * Get file path for a memory
   */
  private getFilePath(id: string): string {
    return path.join(this.storagePath, `${id}.md`);
  }
  
  /**
   * Get trash file path for a memory
   */
  private getTrashPath(id: string): string {
    return path.join(this.storagePath, '.trash', `${id}.md`);
  }

  /**
   * Save a memory to file
   */
  async save(memory: Memory): Promise<void> {
    return fileLock.withLock(memory.id, async () => {
      await this.ensureDir();
      const filePath = this.getFilePath(memory.id);
      const content = serializeMemory(memory);
      await fs.writeFile(filePath, content, 'utf-8');
    });
  }
  
  /**
   * Load a memory from file
   */
  async load(id: string): Promise<Memory | null> {
    return fileLock.withLock(id, async () => {
      try {
        const filePath = this.getFilePath(id);
        const content = await fs.readFile(filePath, 'utf-8');
        return deserializeMemory(content, id);
      } catch (error) {
        if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
          return null;
        }
        throw error;
      }
    });
  }
  
  /**
   * Load a memory from trash
   */
  async loadFromTrash(id: string): Promise<Memory | null> {
    return fileLock.withLock(id, async () => {
      try {
        const trashPath = this.getTrashPath(id);
        const content = await fs.readFile(trashPath, 'utf-8');
        return deserializeMemory(content, id);
      } catch (error) {
        if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
          return null;
        }
        throw error;
      }
    });
  }
  
  /**
   * Delete a memory file
   */
  async deleteFile(id: string): Promise<void> {
    return fileLock.withLock(id, async () => {
      const filePath = this.getFilePath(id);
      await fs.unlink(filePath).catch(err => {
        if ((err as NodeJS.ErrnoException).code !== 'ENOENT') {
          throw err;
        }
      });
    });
  }
  
  /**
   * Move to trash
   */
  async moveToTrash(memory: Memory): Promise<void> {
    return fileLock.withLock(memory.id, async () => {
      await this.ensureDir();
      const sourcePath = this.getFilePath(memory.id);
      const trashPath = this.getTrashPath(memory.id);
      
      // Read original content
      const content = await fs.readFile(sourcePath, 'utf-8');
      
      // Write to trash with updated frontmatter
      const trashedMemory = { ...memory, status: 'deleted' as MemoryStatus, deletedAt: new Date() };
      await fs.writeFile(trashPath, serializeMemory(trashedMemory), 'utf-8');
      
      // Remove original
      await fs.unlink(sourcePath).catch(() => {});
    });
  }
  
  /**
   * Restore from trash
   */
  async restoreFromTrash(id: string): Promise<Memory | null> {
    return fileLock.withLock(id, async () => {
      const trashPath = this.getTrashPath(id);
      
      try {
        const content = await fs.readFile(trashPath, 'utf-8');
        const memory = deserializeMemory(content, id);
        
        // Restore memory
        const restoredMemory: Memory = {
          ...memory,
          status: 'active',
          deletedAt: undefined,
          updatedAt: new Date(),
        };
        
        await this.ensureDir();
        const filePath = this.getFilePath(id);
        await fs.writeFile(filePath, serializeMemory(restoredMemory), 'utf-8');
        await fs.unlink(trashPath);
        
        return restoredMemory;
      } catch (error) {
        if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
          return null;
        }
        throw error;
      }
    });
  }
  
  /**
   * List all memory files
   */
  async listFiles(): Promise<string[]> {
    await this.ensureDir();
    const files = await fs.readdir(this.storagePath);
    return files.filter(f => f.endsWith('.md')).map(f => f.slice(0, -3));
  }
  
  /**
   * List trash files
   */
  async listTrashFiles(): Promise<string[]> {
    const trashDir = path.join(this.storagePath, '.trash');
    try {
      const files = await fs.readdir(trashDir);
      return files.filter(f => f.endsWith('.md')).map(f => f.slice(0, -3));
    } catch {
      return [];
    }
  }
  
  /**
   * Permanently delete from trash
   */
  async permanentDelete(id: string): Promise<void> {
    // Delete from both main directory and trash
    const filePath = this.getFilePath(id);
    const trashPath = this.getTrashPath(id);
    
    await Promise.all([
      fs.unlink(filePath).catch(err => {
        if ((err as NodeJS.ErrnoException).code !== 'ENOENT') throw err;
      }),
      fs.unlink(trashPath).catch(err => {
        if ((err as NodeJS.ErrnoException).code !== 'ENOENT') throw err;
      }),
    ]);
  }
  
  /**
   * Empty trash
   */
  async emptyTrash(): Promise<void> {
    const trashDir = path.join(this.storagePath, '.trash');
    try {
      const files = await fs.readdir(trashDir);
      for (const file of files) {
        await fs.unlink(path.join(trashDir, file));
      }
    } catch {
      // Ignore if trash doesn't exist
    }
  }
}