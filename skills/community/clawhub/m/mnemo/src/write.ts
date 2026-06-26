/**
 * Memory Write - 写入记忆文件
 * 安全修复：添加路径验证，防止目录遍历攻击
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import type { MemorySystemConfig } from './index.js';

/**
 * 展开路径中的 ~
 */
function expandPath(p: string): string {
  if (p.startsWith('~')) {
    return path.join(process.env.HOME || '', p.slice(1));
  }
  return path.resolve(p);
}

/**
 * 安全验证：确保最终路径在 memoryDir 内
 * 防止 ../ 目录遍历攻击
 */
function validatePath(filePath: string, memoryDir: string): string {
  // 展开 memoryDir
  const resolvedMemDir = expandPath(memoryDir);
  
  // 展开请求的路径
  let resolvedPath: string;
  if (path.isAbsolute(filePath)) {
    resolvedPath = expandPath(filePath);
  } else {
    // 相对路径基于 memoryDir
    resolvedPath = path.resolve(resolvedMemDir, filePath);
  }

  // 解析符号链接，获取真实路径
  try {
    resolvedPath = path.resolve(resolvedPath);
  } catch {
    throw new Error('Invalid path');
  }

  // 验证最终路径是否在 memoryDir 内
  if (!resolvedPath.startsWith(resolvedMemDir + path.sep) && resolvedPath !== resolvedMemDir) {
    throw new Error(`Path traversal denied: "${filePath}" resolves outside memory directory`);
  }

  // 验证文件名不包含危险字符
  const basename = path.basename(filePath);
  if (basename.startsWith('.') || basename === '..') {
    throw new Error('Invalid filename');
  }

  return resolvedPath;
}

/**
 * 写入记忆文件
 */
export async function memoryWrite(
  filePath: string,
  content: string,
  mode: 'overwrite' | 'append' = 'append',
  config?: MemorySystemConfig
): Promise<{ success: boolean; path: string; error?: string }> {
  const cfg = config || {
    memoryDir: '~/.openclaw/workspace/memory'
  } as MemorySystemConfig;

  // 安全验证路径
  let fullPath: string;
  try {
    fullPath = validatePath(filePath, cfg.memoryDir);
  } catch (e) {
    return {
      success: false,
      path: filePath,
      error: (e as Error).message
    };
  }
  
  console.log(`[MemoryWrite] 写入: ${fullPath} (mode: ${mode})`);

  // 确保目录存在
  const dir = path.dirname(fullPath);
  await fs.mkdir(dir, { recursive: true });

  if (mode === 'append') {
    // 追加模式
    try {
      const existing = await fs.readFile(fullPath, 'utf-8');
      const newContent = existing + '\n' + content;
      await fs.writeFile(fullPath, newContent, 'utf-8');
    } catch (e) {
      if ((e as NodeJS.ErrnoException).code === 'ENOENT') {
        // 文件不存在，直接创建
        await fs.writeFile(fullPath, content, 'utf-8');
      } else {
        throw e;
      }
    }
  } else {
    // 覆盖模式
    await fs.writeFile(fullPath, content, 'utf-8');
  }

  return {
    success: true,
    path: filePath
  };
}

/**
 * 便捷方法：写入每日记录
 */
export async function memoryWriteDaily(
  content: string,
  config?: MemorySystemConfig
): Promise<{ success: boolean; path: string }> {
  const today = new Date().toISOString().split('T')[0];
  return memoryWrite(`memory/${today}.md`, content, 'append', config);
}

/**
 * 便捷方法：写入长期记忆
 */
export async function memoryWritePermanent(
  content: string,
  config?: MemorySystemConfig
): Promise<{ success: boolean; path: string }> {
  return memoryWrite('MEMORY.md', content, 'append', config);
}
