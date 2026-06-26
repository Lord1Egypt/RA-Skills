/**
 * Memory Flush - 内存 flush 到文件系统
 */

import type { MemorySystemConfig } from './index.js';

/**
 * 获取当前 token 使用量（从 OpenClaw 上下文）
 */
async function getCurrentTokenCount(): Promise<number> {
  try {
    // 尝试从 OpenClaw 上下文获取
    // 这需要 OpenClaw 提供相应的 API
    const sessionStatus = await import('openclaw').then(m => 
      m.sessionStatus?.().catch(() => null)
    );
    
    if (sessionStatus?.tokens) {
      return sessionStatus.tokens;
    }
  } catch {
    // 忽略错误
  }
  
  // 默认返回 0，需要外部触发
  return 0;
}

/**
 * 检查是否需要 flush
 */
export async function shouldFlush(config: MemorySystemConfig): Promise<boolean> {
  if (config.flushMode === 'disabled') {
    return false;
  }

  if (config.flushMode === 'manual') {
    return false;
  }

  // safeguard 模式：检查 token 阈值
  const tokenCount = await getCurrentTokenCount();
  return tokenCount >= config.softThresholdTokens;
}

/**
 * 执行 flush 操作
 */
export async function memoryFlush(
  force: boolean = false,
  config?: MemorySystemConfig
): Promise<{ success: boolean; flushed: boolean; reason: string }> {
  const cfg = config || {
    memoryDir: '~/.openclaw/workspace/memory',
    flushMode: 'safeguard',
    softThresholdTokens: 300000
  } as MemorySystemConfig;

  console.log(`[MemoryFlush] 开始检查 flush (force: ${force})`);

  // 检查是否可以 flush
  if (!force) {
    const needFlush = await shouldFlush(cfg);
    if (!needFlush) {
      return {
        success: true,
        flushed: false,
        reason: '未达到 flush 阈值'
      };
    }
  }

  // 执行 flush
  // 这里需要保存当前会话的上下文到文件
  // 实际的保存逻辑由 OpenClaw 的 compaction 机制处理
  console.log('[MemoryFlush] 执行 flush...');

  try {
    // 记录 flush 时间戳
    const flushRecord = `[${new Date().toISOString()}] Memory flushed\n`;
    
    // 可以在这里写入一个 flush 记录文件
    // 实际实现依赖 OpenClaw 的会话状态
    console.log('[MemoryFlush] Flush 完成');

    return {
      success: true,
      flushed: true,
      reason: force ? '手动触发' : '达到 token 阈值'
    };
  } catch (e) {
    return {
      success: false,
      flushed: false,
      reason: `Flush 失败: ${e}`
    };
  }
}

/**
 * 注册 flush 钩子（供 OpenClaw 调用）
 */
export function registerFlushHook() {
  return {
    name: 'memory-flush',
    trigger: 'onTokenThreshold',
    handler: async (tokens: number, config: MemorySystemConfig) => {
      if (tokens >= config.softThresholdTokens) {
        return await memoryFlush(false, config);
      }
      return { success: true, flushed: false, reason: '阈值未达到' };
    }
  };
}
