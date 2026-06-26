/**
 * Memory System Skill - 入口文件
 * 注册工具和 hooks
 */

import { memorySearch } from './search.js';
import { memoryGet } from './get.js';
import { memoryWrite } from './write.js';
import { memoryFlush } from './flush.js';
import { setupAutoLoad } from './autoLoad.js';
import { 
  executeDream, 
  shouldTriggerDream, 
  getDreamStats,
  getLastDreamTime,
  type AutoDreamConfig 
} from './autoDream.js';

export interface MemorySystemConfig {
  memoryDir: string;
  flushMode: 'safeguard' | 'manual' | 'disabled';
  softThresholdTokens: number;
  vectorEnabled: boolean;
  embeddingModel: string;
  autoDream?: {
    enabled: boolean;
    minHours: number;
    minSessions: number;
    apiKey?: string;
  };
}

const DEFAULT_CONFIG: MemorySystemConfig = {
  memoryDir: '~/.openclaw/workspace/memory',
  flushMode: 'safeguard',
  softThresholdTokens: 300000,
  vectorEnabled: true,
  embeddingModel: 'nomic-embed-text',
  autoDream: {
    enabled: true,
    minHours: 24,
    minSessions: 3
  }
};

/**
 * 获取配置
 */
function getConfig(): MemorySystemConfig {
  try {
    const userConfig = globalThis.openclaw?.config?.get?.('skills.memory-system');
    return { ...DEFAULT_CONFIG, ...userConfig };
  } catch {
    return DEFAULT_CONFIG;
  }
}

/**
 * 获取 API Key
 */
function getApiKey(): string | undefined {
  // 1. 先从 config 读取
  const config = getConfig();
  if (config.autoDream?.apiKey) {
    // 支持 env: 前缀，从环境变量读取
    if (config.autoDream.apiKey.startsWith('env:')) {
      const envVar = config.autoDream.apiKey.slice(4);
      return process.env[envVar];
    }
    return config.autoDream.apiKey;
  }
  // 2. 回退到环境变量
  return process.env.MINIMAX_CODING_API_KEY;
}

/**
 * 注册所有工具
 */
export function registerMemorySystem() {
  const config = getConfig();
  const apiKey = getApiKey();

  console.log('[MemorySystem] 注册记忆系统工具...');

  const tools = {
    memory_search: {
      description: '语义搜索记忆',
      parameters: {
        query: { type: 'string', required: true },
        topK: { type: 'number', default: 5 },
        type: { type: 'string', description: '记忆类型: user/feedback/project/reference' },
        group: { type: 'string', description: '群组 ID' }
      },
      handler: async (params: { query: string; topK?: number; type?: string; group?: string }) => {
        return await memorySearch(params.query, params.topK || 5, params.group, config);
      }
    },
    memory_get: {
      description: '读取记忆文件',
      parameters: {
        path: { type: 'string', required: true },
        from: { type: 'number' },
        lines: { type: 'number' }
      },
      handler: async (params: { path: string; from?: number; lines?: number }) => {
        return await memoryGet(params.path, params.from, params.lines, config);
      }
    },
    memory_write: {
      description: '写入记忆文件（支持类型验证，写入后自动检查 AutoDream 触发条件）',
      parameters: {
        file: { type: 'string', required: true },
        content: { type: 'string', required: true },
        type: { type: 'string', description: '记忆类型: user/feedback/project/reference' },
        mode: { type: 'string', default: 'append' }
      },
      handler: async (params: { file: string; content: string; type?: string; mode?: string }) => {
        return await memoryWrite(params.file, params.content, params.mode as 'overwrite' | 'append' || 'append', params.type, config);
      }
    },
    memory_flush: {
      description: '手动触发 flush',
      parameters: {
        force: { type: 'boolean', default: false }
      },
      handler: async (params: { force?: boolean }) => {
        return await memoryFlush(params.force || false, config);
      }
    },
    memory_dream: {
      description: '执行 AutoDream 记忆整合',
      parameters: {
        force: { type: 'boolean', description: '强制触发，忽略时间/会话限制' }
      },
      handler: async (params: { force?: boolean }) => {
        if (params.force) {
          const result = await executeDream(config.autoDream, apiKey);
          return result;
        }
        
        // 检查是否应该触发
        const check = await shouldTriggerDream({
          enabled: config.autoDream?.enabled ?? true,
          minHours: config.autoDream?.minHours ?? 24,
          minSessions: config.autoDream?.minSessions ?? 3,
          memoryDir: config.memoryDir
        });
        
        if (!check.should) {
          return {
            success: true,
            triggered: false,
            reason: check.reason,
            canTriggerNow: false
          };
        }
        
        // 执行整合
        const result = await executeDream(config.autoDream, apiKey);
        return {
          ...result,
          canTriggerNow: true
        };
      }
    },
    memory_dream_status: {
      description: '查看 AutoDream 状态',
      parameters: {},
      handler: async () => {
        const stats = await getDreamStats(config.memoryDir);
        const lastDream = await getLastDreamTime(config.memoryDir);
        const check = await shouldTriggerDream({
          enabled: config.autoDream?.enabled ?? true,
          minHours: config.autoDream?.minHours ?? 24,
          minSessions: config.autoDream?.minSessions ?? 3,
          memoryDir: config.memoryDir
        });
        
        return {
          enabled: config.autoDream?.enabled ?? true,
          lastDream: lastDream?.toISOString() || null,
          hoursSince: stats.hoursSince === Infinity ? '从未执行' : `${stats.hoursSince.toFixed(1)} 小时前`,
          sessionsSinceLast: stats.sessionsSinceLast,
          totalMemoryFiles: stats.totalMemoryFiles,
          canTriggerNow: check.should,
          nextTriggerReason: check.reason
        };
      }
    }
  };

  // 注册 hooks - 这些会被 OpenClaw 在适当的时机调用
  const hooks = {
    onSessionStart: {
      description: '会话启动时自动加载记忆',
      handler: async (context: { sessionType: string; groupId?: string }) => {
        console.log('[MemorySystem] onSessionStart hook triggered');
        return await setupAutoLoad(context as { sessionType: 'direct' | 'group'; groupId?: string; userId?: string }, config);
      }
    },
    onHeartbeat: {
      description: '心跳时检查并触发 AutoDream',
      handler: async () => {
        console.log('[MemorySystem] onHeartbeat hook triggered - checking AutoDream');
        
        if (!config.autoDream?.enabled) {
          return { triggered: false, reason: 'AutoDream 已禁用' };
        }
        
        const check = await shouldTriggerDream({
          enabled: config.autoDream.enabled,
          minHours: config.autoDream.minHours || 24,
          minSessions: config.autoDream.minSessions || 3,
          memoryDir: config.memoryDir
        });
        
        if (!check.should) {
          console.log(`[MemorySystem] AutoDream 不满足触发条件: ${check.reason}`);
          return { triggered: false, reason: check.reason };
        }
        
        console.log('[MemorySystem] AutoDream 触发条件满足，执行整合...');
        const result = await executeDream(config.autoDream, apiKey);
        
        return {
          triggered: result.triggered,
          success: result.success,
          summary: result.summary,
          changes: result.changes
        };
      }
    },
    onSessionEnd: {
      description: '会话结束时自动保存记忆',
      handler: async () => {
        console.log('[MemorySystem] onSessionEnd hook triggered');
        // 可以在这里做清理或最终保存
        return { success: true };
      }
    }
  };

  return { tools, hooks, config };
}

/**
 * 启动检查
 */
export async function initMemorySystem() {
  const config = getConfig();
  const apiKey = getApiKey();
  
  console.log('[MemorySystem] 初始化记忆系统...');
  console.log(`[MemorySystem] 记忆目录: ${config.memoryDir}`);
  console.log(`[MemorySystem] Flush 模式: ${config.flushMode}`);
  console.log(`[MemorySystem] 向量搜索: ${config.vectorEnabled ? '启用' : '禁用'}`);
  console.log(`[MemorySystem] AutoDream: ${config.autoDream?.enabled ? '启用' : '禁用'}`);
  console.log(`[MemorySystem] API Key: ${apiKey ? '已配置' : '未配置'}`);

  if (config.vectorEnabled) {
    try {
      const { checkOllama } = await import('./embed.js');
      const ollamaStatus = await checkOllama();
      if (!ollamaStatus) {
        console.warn('[MemorySystem] ⚠️ Ollama 未运行，向量搜索将不可用');
      }
    } catch {
      console.warn('[MemorySystem] ⚠️ 无法检查 Ollama 状态');
    }
  }
}

export default { register: registerMemorySystem, init: initMemorySystem };
