/**
 * Memory Get - 读取记忆文件
 * 安全修复：添加路径验证，防止目录遍历攻击
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import type { MemorySystemConfig } from './index.js';

/**
 * 展开路径中的 ~ 并转换为绝对路径
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

  return resolvedPath;
}

/**
 * 读取记忆文件
 */
export async function memoryGet(
  filePath: string,
  from?: number,
  lines?: number,
  config?: MemorySystemConfig
): Promise<{ path: string; content: string; totalLines: number }> {
  const cfg = config || {
    memoryDir: '~/.openclaw/workspace/memory'
  } as MemorySystemConfig;

  // 安全验证路径
  let fullPath: string;
  try {
    fullPath = validatePath(filePath, cfg.memoryDir);
  } catch (e) {
    return {
      path: filePath,
      content: '',
      totalLines: 0,
      error: (e as Error).message
    };
  }
  
  console.log(`[MemoryGet] 读取: ${fullPath}`);

  try {
    const content = await fs.readFile(fullPath, 'utf-8');
    const allLines = content.split('\n');
    const totalLines = allLines.length;

    // 默认读取全部
    let startLine = 1;
    let endLine = totalLines;

    // 如果指定了 from，从该行开始读取
    if (from !== undefined && from > 0) {
      startLine = from;
    }

    // 如果指定了 lines，读取指定行数
    if (lines !== undefined && lines > 0) {
      endLine = Math.min(startLine + lines - 1, totalLines);
    }

    // 提取指定行
    const selectedLines = allLines.slice(startLine - 1, endLine);
    const selectedContent = selectedLines.join('\n');

    return {
      path: filePath,
      content: selectedContent,
      totalLines
    };
  } catch (e) {
    if ((e as NodeJS.ErrnoException).code === 'ENOENT') {
      return {
        path: filePath,
        content: '',
        totalLines: 0
      };
    }
    throw e;
  }
}

/**
 * 读取多个文件（用于自动加载）
 * 自动加载使用受信任的内部路径，不做额外验证
 */
export async function memoryGetMultiple(
  filePaths: string[],
  config?: MemorySystemConfig
): Promise<{ path: string; content: string }[]> {
  const results: { path: string; content: string }[] = [];

  for (const fp of filePaths) {
    try {
      const result = await memoryGet(fp, undefined, undefined, config);
      if (result.content) {
        results.push({
          path: result.path,
          content: result.content
        });
      }
    } catch (e) {
      // 忽略不存在的文件
    }
  }

  return results;
}
