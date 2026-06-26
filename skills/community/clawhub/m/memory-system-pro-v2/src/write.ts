/**
 * Memory Write - 写入记忆文件
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import type { MemorySystemConfig } from './index.js';
import { shouldTriggerDream } from './autoDream.js';

/**
 * 展开路径中的 ~
 */
function expandPath(p: string, baseDir: string): string {
  if (p.startsWith('~')) {
    return path.join(process.env.HOME || '', p.slice(1));
  }
  if (!path.isAbsolute(p)) {
    return path.join(baseDir, p);
  }
  return path.resolve(p);
}

/**
 * 记忆类型白名单
 */
const VALID_MEMORY_TYPES = ['user', 'feedback', 'project', 'reference'];

/**
 * 验证记忆类型
 */
function validateMemoryType(type?: string): string | null {
  if (!type) return null;
  if (!VALID_MEMORY_TYPES.includes(type)) {
    return `Invalid type: ${type}. Must be one of: ${VALID_MEMORY_TYPES.join(', ')}`;
  }
  return null;
}

/**
 * 写入记忆文件
 */
export async function memoryWrite(
  filePath: string,
  content: string,
  mode: 'overwrite' | 'append' = 'append',
  memoryType?: string,
  config?: MemorySystemConfig
): Promise<{ 
  success: boolean; 
  path: string;
  typeValidation?: string;
  dreamCheck?: { should: boolean; reason: string };
}> {
  const cfg = config || {
    memoryDir: '~/.openclaw/workspace/memory',
    autoDream: { enabled: true, minHours: 24, minSessions: 3 }
  } as MemorySystemConfig;

  const fullPath = expandPath(filePath, cfg.memoryDir);
  
  // 验证类型
  const typeValidation = validateMemoryType(memoryType);
  
  console.log(`[MemoryWrite] 写入: ${fullPath} (mode: ${mode}, type: ${memoryType || 'auto'})`);

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

  // 检查是否应该触发 AutoDream
  let dreamCheck = { should: false, reason: '' };
  if (cfg.autoDream?.enabled) {
    const check = await shouldTriggerDream({
      enabled: cfg.autoDream.enabled,
      minHours: cfg.autoDream.minHours || 24,
      minSessions: cfg.autoDream.minSessions || 3,
      memoryDir: cfg.memoryDir || '~/.openclaw/workspace/memory'
    });
    dreamCheck = check;
  }

  return {
    success: true,
    path: filePath,
    typeValidation: typeValidation || undefined,
    dreamCheck
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
  return memoryWrite(`memory/${today}.md`, content, 'append', undefined, config);
}

/**
 * 便捷方法：写入长期记忆
 */
export async function memoryWritePermanent(
  content: string,
  config?: MemorySystemConfig
): Promise<{ success: boolean; path: string }> {
  return memoryWrite('MEMORY.md', content, 'append', undefined, config);
}

/**
 * 便捷方法：写入用户记忆
 */
export async function memoryWriteUser(
  content: string,
  userId: string,
  config?: MemorySystemConfig
): Promise<{ success: boolean; path: string }> {
  return memoryWrite(`user/${userId}.md`, content, 'append', 'user', config);
}

/**
 * 便捷方法：写入反馈记忆
 */
export async function memoryWriteFeedback(
  content: string,
  subtype: 'positive' | 'negative',
  config?: MemorySystemConfig
): Promise<{ success: boolean; path: string }> {
  return memoryWrite(`feedback/${subtype}/auto.md`, content, 'append', 'feedback', config);
}

/**
 * 便捷方法：写入项目记忆
 */
export async function memoryWriteProject(
  content: string,
  projectName: string,
  config?: MemorySystemConfig
): Promise<{ success: boolean; path: string }> {
  return memoryWrite(`project/${projectName}.md`, content, 'append', 'project', config);
}

/**
 * 便捷方法：写入引用记忆
 */
export async function memoryWriteReference(
  content: string,
  config?: MemorySystemConfig
): Promise<{ success: boolean; path: string }> {
  return memoryWrite('reference/external.md', content, 'append', 'reference', config);
}
