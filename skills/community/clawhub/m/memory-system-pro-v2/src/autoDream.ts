/**
 * AutoDream - 定时记忆整合系统
 * 
 * 灵感来自 Claude Code 的 autoDream 系统
 * 在空闲时自动整合记忆，保持记忆新鲜和结构化
 */

import * as fs from 'fs/promises';
import * as path from 'path';

export interface AutoDreamConfig {
  enabled: boolean;
  minHours: number;        // 最小触发间隔（小时）
  minSessions: number;      // 最小会话数
  memoryDir: string;
  apiKey?: string;
}

const DEFAULT_AUTO_DREAM_CONFIG: AutoDreamConfig = {
  enabled: true,
  minHours: 24,
  minSessions: 3,
  memoryDir: '~/.openclaw/workspace/memory'
};

/**
 * MiniMax API 调用
 */
async function callMiniMax(prompt: string, apiKey: string): Promise<string> {
  const response = await fetch('https://api.minimaxi.com/anthropic/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
      'anthropic-version': '2023-06-01'
    },
    body: JSON.stringify({
      model: 'MiniMax-M2.7',
      max_tokens: 8192,
      messages: [
        { role: 'user', content: prompt }
      ]
    })
  });

  if (!response.ok) {
    throw new Error(`MiniMax API error: ${response.status}`);
  }

  const data = await response.json() as { content?: Array<{ type: string; text?: string }> };
  return data.content?.find(c => c.type === 'text')?.text || '';
}

/**
 * 整合状态文件
 */
const STATE_FILE = '.auto-dream-state.json';

interface DreamState {
  lastConsolidatedAt: number;
  lastConsolidatedSessions: number;
}

interface DreamFile {
  path: string;
  content: string;
}

interface DreamResult {
  added: DreamFile[];
  deleted: string[];
  updated: string[];
  summary: string;
  newIndexContent?: string;
}

/**
 * 展开路径
 */
function expandPath(p: string): string {
  if (p.startsWith('~')) {
    return path.join(process.env.HOME || '', p.slice(1));
  }
  return path.resolve(p);
}

/**
 * 读取整合状态
 */
async function readDreamState(memoryDir: string): Promise<DreamState> {
  const statePath = path.join(expandPath(memoryDir), STATE_FILE);
  try {
    const content = await fs.readFile(statePath, 'utf-8');
    return JSON.parse(content);
  } catch {
    return { lastConsolidatedAt: 0, lastConsolidatedSessions: 0 };
  }
}

/**
 * 写入整合状态
 */
async function writeDreamState(memoryDir: string, state: DreamState): Promise<void> {
  const statePath = path.join(expandPath(memoryDir), STATE_FILE);
  await fs.writeFile(statePath, JSON.stringify(state, null, 2));
}

/**
 * 扫描会话目录
 */
async function scanSessions(memoryDir: string): Promise<string[]> {
  const sessionsDir = path.join(expandPath(memoryDir), 'sessions');
  try {
    const entries = await fs.readdir(sessionsDir, { withFileTypes: true });
    return entries
      .filter(e => e.isFile() && e.name.endsWith('.json'))
      .map(e => path.join(sessionsDir, e.name));
  } catch {
    return [];
  }
}

/**
 * 读取 MEMORY.md 索引
 */
async function readMemoryIndex(memoryDir: string): Promise<string> {
  const indexPath = path.join(expandPath(memoryDir), 'MEMORY.md');
  try {
    return await fs.readFile(indexPath, 'utf-8');
  } catch {
    return '';
  }
}

/**
 * 扫描所有记忆文件
 */
async function scanMemoryFiles(memoryDir: string): Promise<{ path: string; relativePath: string; content: string; modified: Date }[]> {
  const files: { path: string; relativePath: string; content: string; modified: Date }[] = [];
  const baseDir = expandPath(memoryDir);
  
  async function scan(dir: string) {
    try {
      const entries = await fs.readdir(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== 'sessions') {
          await scan(fullPath);
        } else if (entry.name.endsWith('.md')) {
          const stat = await fs.stat(fullPath);
          const content = await fs.readFile(fullPath, 'utf-8');
          const relativePath = fullPath.replace(baseDir + '/', '');
          files.push({ path: fullPath, relativePath, content, modified: stat.mtime });
        }
      }
    } catch {
      // 忽略错误
    }
  }
  
  await scan(baseDir);
  return files;
}

/**
 * 获取最近修改的文件
 */
async function getRecentlyModifiedFiles(
  memoryDir: string, 
  since: number
): Promise<{ path: string; relativePath: string; content: string }[]> {
  const files = await scanMemoryFiles(memoryDir);
  return files
    .filter(f => f.modified.getTime() > since)
    .map(f => ({ path: f.path, relativePath: f.relativePath, content: f.content }));
}

/**
 * 解析 LLM 返回的整合结果
 */
function parseDreamResult(llmOutput: string): DreamResult {
  const result: DreamResult = {
    added: [],
    deleted: [],
    updated: [],
    summary: ''
  };

  // 提取新增记忆块
  // 格式: ### NEW: filename.md\n 内容
  const newFileRegex = /###\s*NEW:\s*([^\n]+)\n([\s\S]*?)(?=###\s*(?:DELETE|UPDATE|NEW)|```|###\s*总结|$)/gi;
  let match;
  while ((match = newFileRegex.exec(llmOutput)) !== null) {
    const fileName = match[1].trim();
    const fileContent = match[2].trim();
    if (fileName && fileContent) {
      result.added.push({ path: fileName, content: fileContent });
    }
  }

  // 如果没找到 NEW: 格式，尝试查找文件名作为标题
  if (result.added.length === 0) {
    const mdBlockRegex = /```markdown\n([\s\S]*?)```/g;
    const indexBlocks: string[] = [];
    let blockMatch;
    while ((blockMatch = mdBlockRegex.exec(llmOutput)) !== null) {
      indexBlocks.push(blockMatch[1]);
    }
    
    // 检查是否有关于索引的更新
    if (indexBlocks.length > 0) {
      result.updated.push('MEMORY.md');
      result.newIndexContent = indexBlocks[indexBlocks.length - 1];
    }
  }

  // 提取删除文件名
  // 格式: ### DELETE: filename.md 或 - [filename.md]: 原因
  const deleteFileRegex = /###\s*DELETE:\s*([^\n]+)/gi;
  while ((match = deleteFileRegex.exec(llmOutput)) !== null) {
    const fileName = match[1].trim();
    if (fileName) result.deleted.push(fileName);
  }

  // 也支持列表格式: - [filename.md]
  const listDeleteRegex = /-\s*\[[^\]]+\.md\]:/gi;
  const deleteListMatches = llmOutput.match(listDeleteRegex);
  if (deleteListMatches) {
    for (const m of deleteListMatches) {
      const fnMatch = m.match(/\[([^\]]+\.md)\]/);
      if (fnMatch && !result.deleted.includes(fnMatch[1])) {
        result.deleted.push(fnMatch[1]);
      }
    }
  }

  // 提取总结
  const summaryMatch = llmOutput.match(/\*\*总结[:：]?\s*([\s\S]+)$/im);
  if (summaryMatch) {
    result.summary = summaryMatch[1].trim().slice(0, 200);
  } else {
    // 取最后一段非代码块的内容
    const parts = llmOutput.split(/```/);
    if (parts.length > 1) {
      result.summary = parts[parts.length - 1].trim().slice(0, 200);
    } else {
      result.summary = llmOutput.slice(-300).trim().split('\n').slice(-5).join(' ');
    }
  }

  return result;
}

/**
 * 检查是否应该触发整合
 */
export async function shouldTriggerDream(config: AutoDreamConfig): Promise<{ should: boolean; reason: string }> {
  if (!config.enabled) {
    return { should: false, reason: 'AutoDream 已禁用' };
  }
  
  const state = await readDreamState(config.memoryDir);
  const now = Date.now();
  
  const hoursSince = (now - state.lastConsolidatedAt) / (1000 * 60 * 60);
  if (hoursSince < config.minHours) {
    return { 
      should: false, 
      reason: `距离上次整合 ${hoursSince.toFixed(1)} 小时，需等待 ${config.minHours} 小时` 
    };
  }
  
  const sessions = await scanSessions(config.memoryDir);
  const sessionsSinceLast = sessions.length - state.lastConsolidatedSessions;
  
  if (sessionsSinceLast < config.minSessions) {
    return { 
      should: false, 
      reason: `新会话 ${sessionsSinceLast} 个，需 ${config.minSessions} 个才触发` 
    };
  }
  
  return { 
    should: true, 
    reason: `时间 ${hoursSince.toFixed(1)}h OK，会话 ${sessionsSinceLast} 个 OK` 
  };
}

/**
 * 生成整合 Prompt
 */
function buildDreamPrompt(
  indexContent: string, 
  recentFiles: { relativePath: string; content: string }[],
  oldFiles: { relativePath: string; content: string }[],
  stats: { totalFiles: number; recentCount: number; oldCount: number }
): string {
  const today = new Date().toISOString().split('T')[0];

  const recentFilesSection = recentFiles
    .map(f => `## ${f.relativePath}\n${f.content.slice(0, 3000)}`)
    .join('\n\n---\n\n');

  const oldFilesSection = oldFiles.length > 0
    ? oldFiles
        .map(f => `## ${f.relativePath} (建议检查是否过时)\n${f.content.slice(0, 1500)}`)
        .join('\n\n---\n\n')
    : '(无早期文件)';

  return `# Dream: 记忆整合

你是记忆整合专家。你的任务是对记忆文件进行系统性整理，让记忆保持新鲜、结构化、易于查找。

## 当前统计
- 总记忆文件: ${stats.totalFiles} 个
- 新增/修改文件: ${stats.recentCount} 个
- 早期文件: ${stats.oldCount} 个
- 整合日期: ${today}

---

## 当前索引 (MEMORY.md)
${indexContent || '(空)'}

---

## 最近新增/修改的记忆文件
${recentFilesSection || '(无新文件)'}

---

## 早期记忆文件（请检查是否过时）
${oldFilesSection}

---

## 整合原则

### 1. 四类记忆分类
- **user** (私密): 用户角色、偏好，知识背景
- **feedback** (negative/positive): 用户的纠正和确认
- **project** (团队): 项目进展、目标、决策
- **reference** (team): 外部系统资源指针

### 2. Feedback 双向记录格式
\`\`\`markdown
### [规则名称]
**Type:** negative | positive
**Why:** [原因]
**How to apply:** [何时应用]
**Date:** ${today}
\`\`\`

### 3. 索引规范
- 每条 <= 150 字符
- 使用绝对日期
- 按 user / feedback / project / reference 分类

---

## 输出格式（严格按此格式）

### DELETE: 要删除的文件名.md
(如无需删除，请写"无")

### NEW: 要新增的文件名.md
文件内容...
(如无需新增，请写"无")

### UPDATE: MEMORY.md
\`\`\`markdown
# Memory Index

## User
- [用户角色](user/xxx.md) — 一句话描述

## Feedback
...

## Project
...

## Reference
...
\`\`\`
(如无需更新索引，请写"无")

### **总结**: 50字以内简述本次整合内容

---

请开始整合。`;
}

/**
 * 执行整合
 */
export async function executeDream(
  config?: Partial<AutoDreamConfig>,
  apiKey?: string
): Promise<{
  success: boolean;
  triggered: boolean;
  summary: string;
  changes: { added: string[]; deleted: string[]; updated: string[]; summary: string };
  reason?: string;
}> {
  const cfg: AutoDreamConfig = {
    ...DEFAULT_AUTO_DREAM_CONFIG,
    ...config
  };
  
  const memoryDir = expandPath(cfg.memoryDir);
  const resolvedApiKey = apiKey || process.env.MINIMAX_CODING_API_KEY;
  
  console.log('[AutoDream] 开始执行记忆整合...');
  
  try {
    // 1. 读取状态
    const state = await readDreamState(memoryDir);
    const indexContent = await readMemoryIndex(memoryDir);
    const allFiles = await scanMemoryFiles(memoryDir);
    const sessions = await scanSessions(memoryDir);
    
    // 2. 获取最近修改的文件
    const recentFiles = await getRecentlyModifiedFiles(memoryDir, state.lastConsolidatedAt);
    const oldFiles = allFiles
      .filter(f => !recentFiles.some(r => r.path === f.path))
      .map(f => ({ relativePath: f.relativePath, content: f.content }));
    
    console.log(`[AutoDream] 总文件: ${allFiles.length}, 新文件: ${recentFiles.length}, 旧文件: ${oldFiles.length}`);
    
    // 3. 生成 Prompt
    const prompt = buildDreamPrompt(indexContent, recentFiles, oldFiles, {
      totalFiles: allFiles.length,
      recentCount: recentFiles.length,
      oldCount: oldFiles.length
    });
    
    // 4. 调用 LLM
    if (!resolvedApiKey) {
      return {
        success: false,
        triggered: false,
        summary: 'API Key 未配置',
        changes: { added: [], deleted: [], updated: [], summary: '未执行' },
        reason: 'missing_api_key'
      };
    }
    
    console.log('[AutoDream] 调用 MiniMax LLM...');
    const llmOutput = await callMiniMax(prompt, resolvedApiKey);
    console.log(`[AutoDream] LLM 返回 ${llmOutput.length} 字符`);
    
    // 5. 解析结果
    const changes = parseDreamResult(llmOutput);
    console.log('[AutoDream] 解析结果:', JSON.stringify(changes, null, 2));
    
    // 6. 应用更改 - 新增文件
    for (const file of changes.added) {
      try {
        const fullPath = path.join(memoryDir, file.path);
        await fs.mkdir(path.dirname(fullPath), { recursive: true });
        await fs.writeFile(fullPath, file.content, 'utf-8');
        console.log(`[AutoDream] 创建文件: ${file.path}`);
      } catch (e) {
        console.error(`[AutoDream] 创建文件失败: ${file.path}`, e);
      }
    }
    
    // 7. 应用更改 - 删除文件
    for (const filePath of changes.deleted) {
      try {
        const fullPath = path.join(memoryDir, filePath);
        await fs.unlink(fullPath);
        console.log(`[AutoDream] 删除文件: ${filePath}`);
      } catch (e) {
        console.error(`[AutoDream] 删除文件失败: ${filePath}`, e);
      }
    }
    
    // 8. 更新索引
    if (changes.newIndexContent) {
      await fs.writeFile(path.join(memoryDir, 'MEMORY.md'), changes.newIndexContent, 'utf-8');
      console.log('[AutoDream] 更新 MEMORY.md');
    }
    
    // 9. 更新状态
    await writeDreamState(memoryDir, {
      lastConsolidatedAt: Date.now(),
      lastConsolidatedSessions: sessions.length
    });
    
    console.log('[AutoDream] 整合完成');
    
    return {
      success: true,
      triggered: true,
      summary: changes.summary || '整合完成',
      changes: {
        added: changes.added.map(f => f.path),
        deleted: changes.deleted,
        updated: changes.updated,
        summary: changes.summary
      }
    };
    
  } catch (e) {
    console.error('[AutoDream] 执行失败:', e);
    return {
      success: false,
      triggered: false,
      summary: `整合失败: ${e}`,
      changes: { added: [], deleted: [], updated: [], summary: `失败: ${e}` }
    };
  }
}

/**
 * 获取最近整合的时间
 */
export async function getLastDreamTime(memoryDir: string): Promise<Date | null> {
  const state = await readDreamState(memoryDir);
  return state.lastConsolidatedAt > 0 ? new Date(state.lastConsolidatedAt) : null;
}

/**
 * 获取整合统计
 */
export async function getDreamStats(memoryDir: string): Promise<{
  lastDream: Date | null;
  hoursSince: number;
  sessionsSinceLast: number;
  totalMemoryFiles: number;
}> {
  const state = await readDreamState(memoryDir);
  const memoryFiles = await scanMemoryFiles(memoryDir);
  const sessions = await scanSessions(memoryDir);
  
  const lastDream = state.lastConsolidatedAt > 0 ? new Date(state.lastConsolidatedAt) : null;
  const hoursSince = lastDream 
    ? (Date.now() - state.lastConsolidatedAt) / (1000 * 60 * 60)
    : Infinity;
  
  return {
    lastDream,
    hoursSince,
    sessionsSinceLast: sessions.length - state.lastConsolidatedSessions,
    totalMemoryFiles: memoryFiles.length
  };
}
