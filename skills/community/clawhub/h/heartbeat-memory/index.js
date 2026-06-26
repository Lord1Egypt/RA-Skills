#!/usr/bin/env node

/**
 * heartbeat-memory - Heartbeat 自动记忆保存
 * 
 * 在 Heartbeat 触发时自动检查新 sessions，
 * 生成/更新 daily 笔记，并定期提炼 MEMORY.md。
 * 
 * 架构：Skill 作为协调器
 * - 使用 sessions_list 获取会话列表
 * - 使用 sessions_history 获取消息内容
 * - 启动 subagent 进行 LLM 提炼
 * - 结果写入 Daily 笔记和 MEMORY.md
 * 
 * 工作区检测优先级：
 * 1. 直接读取 openclaw.json（最快）
 * 2. 扫描 workspace* 目录验证存在性
 * 3. CLI 命令（备选）
 * 4. 报错让用户指定
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

// 导入工具模块
let configSync, dateDetector, sessionFilters, memoryRefiner;

try {
  configSync = require('./utils/config-sync');
  dateDetector = require('./utils/date-detector');
  sessionFilters = require('./utils/session-filters');
  memoryRefiner = require('./utils/memory-refiner');
} catch (e) {
  console.error('❌ 模块加载失败:', e.message);
  process.exit(1);
}

const { syncHeartbeatMD, computeConfigHash } = configSync;
const { autoDetectProcessSessionsAfter } = dateDetector;
const { filterSessions, limitSessions } = sessionFilters;
const { detectActiveSessions, getIncrementalMessages, generateIncrementalSummary, updateDailyNoteForActiveSessions } = memoryRefiner;

// ============================================================
// 工作区检测模块
// ============================================================

/**
 * 方案1：直接从 openclaw.json 读取 agent → workspace 映射
 * 
 * @returns {Object} agentId → workspacePath 的映射
 */
function getWorkspacesFromConfig() {
  try {
    const configPath = path.join(os.homedir(), '.openclaw', 'openclaw.json');
    const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    const map = {};
    
    for (const agent of config.agents?.list || []) {
      if (agent.id && agent.workspace) {
        // 路径已经是绝对路径
        map[agent.id] = agent.workspace;
      } else if (agent.id === 'main') {
        // main 没有 workspace 字段，用默认值
        map['main'] = path.join(os.homedir(), '.openclaw', 'workspace');
      }
    }
    
    if (Object.keys(map).length > 0) {
      console.log('✅ [方案1] 从 openclaw.json 获取工作区成功');
      return map;
    }
  } catch (e) {
    console.log('⚠️  [方案1] 读取 openclaw.json 失败:', e.message);
  }
  
  return null;
}

/**
 * 方案2：扫描 ~/.openclaw/workspace* 目录
 * 验证工作区存在（检查 AGENTS.md 或 SOUL.md）
 * 
 * @returns {Object} agentId → workspacePath 的映射
 */
function getWorkspacesFromScan() {
  try {
    const openclawDir = path.join(os.homedir(), '.openclaw');
    const entries = fs.readdirSync(openclawDir);
    const map = {};
    
    for (const entry of entries) {
      // 只处理 workspace 开头的目录
      if (!entry.startsWith('workspace')) continue;
      
      const fullPath = path.join(openclawDir, entry);
      if (!fs.statSync(fullPath).isDirectory()) continue;
      
      // 验证是有效工作区（有 AGENTS.md 或 SOUL.md）
      const hasAgents = fs.existsSync(path.join(fullPath, 'AGENTS.md'));
      const hasSoul = fs.existsSync(path.join(fullPath, 'SOUL.md'));
      
      if (hasAgents || hasSoul) {
        // 用目录名作为 agent ID（如 'workspace', 'workspace-whatever'）
        map[entry] = fullPath;
        console.log(`✅ [方案2] 扫描发现工作区: ${entry} → ${fullPath}`);
      }
    }
    
    if (Object.keys(map).length > 0) {
      console.log('✅ [方案2] 扫描工作区目录成功');
      return map;
    }
  } catch (e) {
    console.log('⚠️  [方案2] 扫描目录失败:', e.message);
  }
  
  return null;
}

/**
 * 方案3：使用 CLI 命令获取工作区列表
 * 通过 LLM 解析输出或正则提取
 * 
 * @returns {Object} agentId → workspacePath 的映射
 */
function getWorkspacesFromCLI() {
  try {
    // 使用 openclaw agents list，提取 JSON 部分
    const raw = execSync('openclaw agents list 2>/dev/null', { encoding: 'utf-8' });
    
    // 提取 JSON 数组（CLI 输出可能包含日志，找到 [...] 部分）
    const jsonMatch = raw.match(/\[[\s\S]*?\]\s*$/);
    if (!jsonMatch) {
      throw new Error('无法解析 CLI 输出');
    }
    
    // 解析精简格式
    const lines = raw.split('\n');
    const map = {};
    let currentAgent = null;
    
    for (const line of lines) {
      // 匹配 agent 行: "- agent-name (default)"
      const agentMatch = line.match(/^-\s+(\S+)/);
      if (agentMatch) {
        currentAgent = agentMatch[1].replace('(default)', '').trim();
        continue;
      }
      
      // 匹配 workspace 行: "  Workspace: /path/to/workspace"
      const wsMatch = line.match(/Workspace:\s*(.+)/);
      if (wsMatch && currentAgent) {
        let wsPath = wsMatch[1].trim();
        // 展开 ~ 为 home 目录
        if (wsPath.startsWith('~/')) {
          wsPath = path.join(os.homedir(), wsPath.slice(2));
        }
        map[currentAgent] = wsPath;
        currentAgent = null;
      }
    }
    
    if (Object.keys(map).length > 0) {
      console.log('✅ [方案3] 从 CLI 获取工作区成功');
      return map;
    }
  } catch (e) {
    console.log('⚠️  [方案3] CLI 命令失败:', e.message);
  }
  
  return null;
}

/**
 * 获取所有 agent → workspace 映射
 * 按优先级尝试各种方案
 * 
 * @returns {Object} agentId → workspacePath 的映射
 */
function getAgentWorkspaceMap() {
  // 方案1：读配置文件
  const fromConfig = getWorkspacesFromConfig();
  if (fromConfig) return fromConfig;
  
  // 方案2：扫描目录
  const fromScan = getWorkspacesFromScan();
  if (fromScan) return fromScan;
  
  // 方案3：CLI
  const fromCLI = getWorkspacesFromCLI();
  if (fromCLI) return fromCLI;
  
  // 全部失败
  return null;
}

/**
 * 确定当前 agent 的工作区
 * 
 * @param {Array} sessions - sessions 列表
 * @param {string} specifiedWorkspace - 用户手动指定的工作区路径（可选）
 * @returns {Object} { agentId, workspace, isDefault }
 */
function determineCurrentWorkspace(sessions, specifiedWorkspace) {
  // Issue #4 修复：支持用户手动指定工作区
  if (specifiedWorkspace) {
    if (fs.existsSync(path.join(specifiedWorkspace, 'AGENTS.md'))) {
      console.log('✅ 使用用户指定的工作区:', specifiedWorkspace);
      return {
        agentId: 'specified',
        workspace: specifiedWorkspace,
        isDefault: false
      };
    } else {
      throw new Error(
        `❌ 用户指定的工作区无效：${specifiedWorkspace}\n` +
        `该目录不存在 AGENTS.md 文件。`
      );
    }
  }
  
  const map = getAgentWorkspaceMap();
  
  if (!map) {
    throw new Error(
      '❌ 无法获取工作区列表。\n' +
      '解决方案：\n' +
      '1. 在 openclaw.json 中配置 agent.workspace 字段\n' +
      '2. 或在 processSessions 调用时传入 specifiedWorkspace 参数\n' +
      '3. 或确保 ~/.openclaw/workspace* 目录下有 AGENTS.md'
    );
  }
  
  // 尝试从 transcriptPath 提取 agent ID
  // 格式: /Users/L/.openclaw/agents/<agent-id>/sessions/xxx.jsonl
  let detectedAgent = null;
  if (sessions && sessions.length > 0) {
    let transcriptPath = sessions[0].transcriptPath || '';
    // 标准化路径分隔符（Windows → UNIX 风格）
    transcriptPath = transcriptPath.replace(/\\/g, '/');
    // 从路径中提取 agent ID
    const match = transcriptPath.match(/\/agents\/([^\/]+)\/sessions\//);
    if (match) {
      detectedAgent = match[1];
      console.log(`🔍 从 transcriptPath 提取到 agent: ${detectedAgent}`);
    }
    
    // 如果没提取到，尝试从 session key 提取
    if (!detectedAgent) {
      const sessionKey = sessions[0].sessionKey || sessions[0].key || '';
      const keyMatch = sessionKey.match(/^agent:([^:]+):/);
      if (keyMatch) {
        detectedAgent = keyMatch[1];
        console.log(`🔍 从 sessionKey 提取到 agent: ${detectedAgent}`);
      }
    }
  }
  
  // 如果检测到 agent，尝试匹配
  if (detectedAgent && map[detectedAgent]) {
    return {
      agentId: detectedAgent,
      workspace: map[detectedAgent],
      isDefault: false
    };
  }
  
  // 尝试前缀匹配（如 'whatever-agent' 匹配 'whatever'）
  if (detectedAgent) {
    for (const [agentId, wsPath] of Object.entries(map)) {
      const key = agentId.replace('-agent', '');
      if (detectedAgent.includes(key) || key.includes(detectedAgent.replace('-agent', ''))) {
        return {
          agentId,
          workspace: wsPath,
          isDefault: agentId === 'workspace' || agentId === 'main'
        };
      }
    }
  }
  
  // 只有一个工作区，直接用
  const entries = Object.entries(map);
  if (entries.length === 1) {
    const [agentId, wsPath] = entries[0];
    return { agentId, workspace: wsPath, isDefault: true };
  }
  
  // 多个工作区，尝试从 HEARTBEAT.md 读取
  try {
    const heartbeatPath = path.join(os.homedir(), '.openclaw', 'workspace', 'HEARTBEAT.md');
    if (fs.existsSync(heartbeatPath)) {
      const content = fs.readFileSync(heartbeatPath, 'utf-8');
      const match = content.match(/工作区：\s*(\S+)/);
      if (match && match[1]) {
        const workspaceName = match[1];
        // 尝试匹配：workspace 名称 或 agent ID
        let wsPath = map[workspaceName];  // 直接匹配 agent ID
        if (!wsPath) {
          // 尝试匹配 workspace 路径
          wsPath = Object.values(map).find(ws => ws.includes(workspaceName));
        }
        if (wsPath) {
          const agentId = Object.keys(map).find(k => map[k] === wsPath) || workspaceName;
          console.log(`✅ 从 HEARTBEAT.md 读取工作区：${agentId} → ${wsPath}`);
          return { agentId, workspace: wsPath, isDefault: false };
        }
      }
    }
  } catch (e) {
    console.log('⚠️  读取 HEARTBEAT.md 失败:', e.message);
  }
  
  // 多个工作区，无法自动判断
  const list = entries.map(([id, ws]) => `- ${id}: ${ws}`).join('\n');
  throw new Error(
    '❌ 检测到多个工作区，无法自动判断当前 agent 使用哪一个：\n' +
    list + '\n\n' +
    '请在 HEARTBEAT.md 中指定当前工作区路径（例如：工作区：workspace）。'
  );
}

/**
 * 确保工作区必要的目录和文件存在
 * 如果已存在，不覆盖
 * 
 * @param {string} wsPath - 工作区路径
 * @returns {Object} 各路径
 */
function ensureWorkspaceStructure(wsPath) {
  const memoryDir = path.join(wsPath, 'memory');
  const dailyDir = path.join(memoryDir, 'daily');
  const memoryFile = path.join(wsPath, 'MEMORY.md');
  const stateFile = path.join(memoryDir, 'heartbeat-state.json');
  const configFile = path.join(memoryDir, 'heartbeat-memory-config.json');
  
  // 创建 memory 目录（若不存在）
  if (!fs.existsSync(memoryDir)) {
    fs.mkdirSync(memoryDir, { recursive: true });
    console.log(`✅ 创建目录: ${memoryDir}`);
  } else {
    console.log(`📁 目录已存在: ${memoryDir}`);
  }
  
  // 创建 daily 目录（若不存在）
  if (!fs.existsSync(dailyDir)) {
    fs.mkdirSync(dailyDir, { recursive: true });
    console.log(`✅ 创建目录: ${dailyDir}`);
  } else {
    console.log(`📁 目录已存在: ${dailyDir}`);
  }
  
  // 创建 MEMORY.md（若不存在）
  if (!fs.existsSync(memoryFile)) {
    const template = `# MEMORY.md - 长期记忆

_最后更新：${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}_

`;
    fs.writeFileSync(memoryFile, template, 'utf-8');
    console.log(`✅ 创建文件: ${memoryFile}`);
  } else {
    console.log(`📁 文件已存在: ${memoryFile}（不覆盖）`);
  }
  
  return { memoryDir, dailyDir, memoryFile, stateFile, configFile };
}

// ============================================================
// 路径配置（后续会动态更新）
// ============================================================

let workspace = path.join(os.homedir(), '.openclaw', 'workspace');
let PATHS = {
  workspace,
  dailyDir: path.join(workspace, 'memory', 'daily'),
  memoryFile: path.join(workspace, 'MEMORY.md'),
  stateFile: path.join(workspace, 'memory', 'heartbeat-state.json'),
  configFile: path.join(workspace, 'memory', 'heartbeat-memory-config.json')
};

const DEFAULT_CONFIG = {
  memorySave: {
    enabled: true,
    batchSize: 5,
    largeTaskThreshold: 10,
    // Issue #2 修复：LLM 超时时间（默认 1000 秒，防止大量 sessions 超时）
    timeoutSeconds: 1000, // 16 分钟，可配置 300-3600
    maxRetries: 3,
    // Issue #6 修复：首次运行限制处理日期范围
    processSessionsAfter: null, // ISO 日期，如 "2026-01-01T00:00:00Z"，null=处理所有
    // Issue #9 修复：限制单次处理 sessions 数量，防止 OOM
    maxSessionsPerRun: 50, // 单次最多处理 50 个 sessions
    // Issue #10 修复：支持扫描文件系统获取 deleted sessions
    scanFileSystem: true,  // 是否扫描文件系统（默认开启）
    scanFileSystemDays: 30,  // 只扫描最近 N 天的文件（0=不限制，扫描所有）
    refineSchedule: {
      type: 'weekly',
      dayOfWeek: 'sunday',
      time: '20:00'
    }
  }
};

function loadConfig() {
  try {
    if (fs.existsSync(PATHS.configFile)) {
      const config = JSON.parse(fs.readFileSync(PATHS.configFile, 'utf-8'));
      return { ...DEFAULT_CONFIG, ...config };
    }
  } catch (e) {
    console.error('读取配置失败:', e.message);
  }
  return DEFAULT_CONFIG;
}

function loadState() {
  try {
    if (fs.existsSync(PATHS.stateFile)) {
      const state = JSON.parse(fs.readFileSync(PATHS.stateFile, 'utf-8'));
      
      // 兼容性处理：如果 processedSessions 是数组，转换为对象格式
      if (Array.isArray(state.processedSessions)) {
        const oldArray = state.processedSessions;
        state.processedSessions = {};
        for (const sessionId of oldArray) {
          state.processedSessions[sessionId] = {
            lastMessageTime: null,
            lastMessageCount: 0,
            status: 'active'
          };
        }
        console.log('✅ 状态文件格式已升级（数组 → 对象）');
      }
      
      return state;
    }
  } catch (e) {
    console.error('读取状态失败:', e.message);
  }
  return {
    memorySave: { enabled: true, firstRunDetected: false },
    processedSessions: {}, // 改为对象，支持详细状态
    lastCheck: null,
    pendingSessions: [],
    lastRefine: null
  };
}

function saveState(state) {
  try {
    const dir = path.dirname(PATHS.stateFile);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(PATHS.stateFile, JSON.stringify(state, null, 2), 'utf-8');
    return true;
  } catch (e) {
    console.error('保存状态失败:', e.message);
    return false;
  }
}

/**
 * 展示层：状态转 emoji
 */
function statusEmoji(status) {
  return { active: '✅', deleted: '❌', reset: '🔄' }[status] || '✅';
}

/**
 * 生成 Daily 笔记（展示层用 emoji）
 */
function generateDailyNote(sessionSummaries, date) {
  const dateStr = typeof date === 'string' ? date : date.toISOString().split('T')[0];

  const activeCount = sessionSummaries.filter(s => s.status === 'active').length;
  const deletedCount = sessionSummaries.filter(s => s.status === 'deleted').length;
  const resetCount = sessionSummaries.filter(s => s.status === 'reset').length;

  let content = `# ${dateStr} 聊天记录

## 📊 当日总结

- 总会话数：${sessionSummaries.length} 个
- 活跃：${activeCount} | 删除：${deletedCount} | 重置：${resetCount}
- 主要话题：${sessionSummaries.map(s => s.title).join(', ') || '无'}
- 关键决策：${sessionSummaries.flatMap(s => s.decisions || []).join('、') || '无'}

## 💬 会话详情

`;

  for (const session of sessionSummaries) {
    const emoji = statusEmoji(session.status);
    const tags = Array.isArray(session.topics) ? session.topics.join(' ') : (session.topics || '#日常');
    const time = session.startTime ? new Date(session.startTime).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }) : '未知';

    content += `### 📋 ${session.title}

**标签：** ${emoji} | ${tags}
**时间：** ${time}
**摘要：** ${session.summary || '无'}

`;

    if (session.decisions && session.decisions.length > 0) {
      content += `**关键发现/决策：**\n${session.decisions.map(d => `- ${d}`).join('\n')}\n\n`;
    }

    content += `---\n\n`;
  }

  return content;
}

/**
 * 写入 Daily 笔记
 */
function writeDailyNote(content, date) {
  const dateStr = typeof date === 'string' ? date : date.toISOString().split('T')[0];
  const filePath = path.join(PATHS.dailyDir, `${dateStr}.md`);

  try {
    if (!fs.existsSync(PATHS.dailyDir)) {
      fs.mkdirSync(PATHS.dailyDir, { recursive: true });
    }

    if (fs.existsSync(filePath)) {
      const existing = fs.readFileSync(filePath, 'utf-8');
      if (existing.includes('## 💬 会话详情') && existing.includes(dateStr)) {
        fs.writeFileSync(filePath, content, 'utf-8');
      } else {
        fs.writeFileSync(filePath, existing + '\n\n---\n\n' + content, 'utf-8');
      }
    } else {
      fs.writeFileSync(filePath, content, 'utf-8');
    }

    console.log('✅ Daily 笔记已写入:', filePath);
    return { success: true, path: filePath };
  } catch (e) {
    console.error('写入 Daily 笔记失败:', e.message);
    return { success: false, error: e.message };
  }
}

/**
 * 兼容多种 session 路径字段
 */
function getSessionPath(session) {
  return session.transcriptPath ||
    session.path ||
    session.key ||
    session.sessionKey ||
    null;
}

/**
 * 读取 session 消息（降级方案 - 文件系统）
 */
function readSessionMessages(sessionPath) {
  try {
    if (!sessionPath || !fs.existsSync(sessionPath)) return [];
    if (!sessionPath.endsWith('.jsonl')) return [];

    const content = fs.readFileSync(sessionPath, 'utf-8');
    const messages = [];

    for (const line of content.trim().split('\n')) {
      if (!line.trim()) continue;
      try {
        const entry = JSON.parse(line);
        if (entry.type === 'message' && entry.message) {
          messages.push({
            role: entry.message.role,
            content: Array.isArray(entry.message.content)
              ? entry.message.content.map(c => c.text || '').join('')
              : (entry.message.content || ''),
            timestamp: entry.timestamp
          });
        }
      } catch (e) { /* skip */ }
    }
    return messages;
  } catch (e) {
    return [];
  }
}

/**
 * 判断 session 状态
 */
function determineSessionStatus(session) {
  if (session.kind) {
    if (session.kind === 'deleted') return 'deleted';
    if (session.kind === 'reset') return 'reset';
  }
  const id = (session.sessionKey || session.sessionId || '').toLowerCase();
  if (id.includes('deleted') || id.includes('removed')) return 'deleted';
  if (id.includes('reset') || id.includes('restart')) return 'reset';
  return 'active';
}

/**
 * 本地简单摘要（无 LLM 时降级）
 * Issue #8 修复：改进降级质量
 */
function summarizeSessionLocal(messages, sessionId) {
  if (!messages || messages.length === 0) {
    return { title: '未命名会话', summary: '无内容', decisions: [], topics: ['#日常'] };
  }

  // 改进标题：找第一条有意义的用户消息
  const userMessages = messages.filter(m => m.role === 'user' && (m.content || '').trim().length > 5);
  const firstMsg = userMessages[0];
  let title = firstMsg?.content?.split('\n')[0]?.substring(0, 40) || '未命名会话';
  // 清理标题中的特殊字符
  title = title.replace(/[\[\]{}<>"']/g, '').trim();
  if (title.length < 5) title = '未命名会话';

  // 改进摘要：提取关键消息（跳过工具调用和思考过程）
  const significantMessages = messages
    .filter(m => m.role === 'user' || (m.role === 'assistant' && !m.content?.includes('thinking')))
    .slice(0, 5)
    .map(m => {
      const text = (m.content || '').split('\n').slice(0, 2).join(' ');
      return text.length > 150 ? text.substring(0, 150) + '...' : text;
    });

  const summary = significantMessages.join(' | ').substring(0, 400);

  // 改进标签：更多关键词 + 权重
  const tags = [];
  const text = JSON.stringify(messages).toLowerCase();
  
  const keywordMap = {
    '#Skill': ['技能', 'skill', '安装', '扩展'],
    '#配置': ['配置', 'config', '设置', 'environment'],
    '#修复': ['修复', 'bug', 'error', '错误', '问题'],
    '#飞书': ['飞书', 'feishu', 'lark', 'bot'],
    '#OpenClaw': ['openclaw', 'agent', 'session', 'gateway'],
    '#对话': ['你好', '谢谢', '再见', 'help'],
    '#代码': ['code', 'function', '变量', 'js', 'python'],
    '#文档': ['doc', 'readme', '文档', '说明']
  };
  
  for (const [tag, keywords] of Object.entries(keywordMap)) {
    if (keywords.some(kw => text.includes(kw))) {
      tags.push(tag);
    }
    if (tags.length >= 5) break;
  }

  // 提取简单决策（查找包含"决定"、"确定"、"选择"的句子）
  const decisions = [];
  for (const msg of messages.slice(-10)) {
    const content = msg.content || '';
    if (content.includes('决定') || content.includes('确定') || content.includes('选择')) {
      const sentence = content.split(/[.!?。！？]/).find(s => 
        s.includes('决定') || s.includes('确定') || s.includes('选择')
      );
      if (sentence && sentence.length < 100) {
        decisions.push(sentence.trim());
      }
    }
  }

  return {
    title,
    summary: summary.trim() || '无摘要',
    decisions: decisions.slice(0, 3),
    topics: tags.length > 0 ? tags : ['#日常']
  };
}

/**
 * 构建 LLM 提炼任务
 */
function buildSummarizeTask(sessionContent, sessionId) {
  return `请分析以下会话内容，提炼：
1. 话题标题（10-20 字，清晰描述话题）
2. 摘要（200-300 字，抓住核心内容）
3. 关键决策/发现（1-3 个要点）
4. 话题标签（3-5 个，#关键词 格式）

会话内容：
${sessionContent.substring(0, 3000)}

请只返回 JSON 格式，不要其他内容：
{
  "title": "话题标题",
  "summary": "摘要内容",
  "decisions": ["决策 1", "决策 2"],
  "topics": ["#标签 1", "#标签 2", "#标签 3"]
}`;
}

/**
 * 解析 LLM 返回结果
 */
function parseLLMResult(result) {
  if (typeof result === 'string') {
    try {
      return JSON.parse(result);
    } catch (e) {
      return null;
    }
  }
  if (result.content) {
    try {
      return JSON.parse(result.content);
    } catch (e) {
      return null;
    }
  }
  return null;
}

/**
 * 扫描文件系统中的 sessions（包括 deleted/inactive 的）
 * 
 * @param {string} sessionsDir - sessions 目录路径
 * @param {number} maxDays - 只扫描最近 N 天的文件（0=不限制，默认 30 天）
 * @returns {Array} session 列表
 */
function scanSessionFiles(sessionsDir, maxDays = 30) {
  try {
    if (!fs.existsSync(sessionsDir)) {
      console.log('⚠️  sessions 目录不存在:', sessionsDir);
      return [];
    }
    
    const files = fs.readdirSync(sessionsDir);
    const sessions = [];
    
    // maxDays = 0 表示不限制，扫描所有文件
    const cutoffTime = maxDays > 0 ? Date.now() - (maxDays * 24 * 60 * 60 * 1000) : 0;
    
    for (const file of files) {
      if (!file.endsWith('.jsonl')) continue;
      
      const sessionId = file.replace('.jsonl', '');
      const fullPath = path.join(sessionsDir, file);
      
      try {
        const stats = fs.statSync(fullPath);
        
        // 只处理最近 N 天的文件（maxDays=0 时不限制）
        if (maxDays > 0 && stats.mtimeMs < cutoffTime) {
          continue;
        }
        
        sessions.push({
          sessionId,
          transcriptPath: fullPath,
          updatedAt: stats.mtimeMs,
          kind: 'deleted'  // 文件系统中找到但不在 sessions_list 中的，标记为 deleted
        });
      } catch (e) {
        // 跳过无法读取的文件
      }
    }
    
    const daysText = maxDays > 0 ? `最近${maxDays}天` : '全部';
    console.log(`📁 文件系统扫描发现 ${sessions.length} 个 sessions（${daysText}）`);
    return sessions;
  } catch (e) {
    console.error('文件系统扫描失败:', e.message);
    return [];
  }
}

/**
 * 主处理函数 - 核心流程
 * 
 * 流程：
 * 1. 获取 sessions 列表（sessions_list 工具）
 * 2. 扫描文件系统获取 deleted sessions（可选）
 * 3. 动态检测正确的工作区
 * 4. 确保目录结构存在
 * 5. 过滤新 sessions
 * 6. 获取消息内容（sessions_history 工具）
 * 7. 启动 subagent 进行 LLM 提炼
 * 8. 写入 Daily 笔记
 * 9. 检查是否需要提炼 MEMORY.md
 * 10. 发送通知
 */
async function processSessions(sessions_list_fn, sessions_history_fn, sessions_spawn_fn, message_fn, feishu_get_user_fn, config_override, specifiedWorkspace) {
  console.log('\n🚀 heartbeat-memory 开始执行...');

  // ========== 步骤 1：获取 sessions 列表 ==========
  let sessions = [];
  try {
    if (sessions_list_fn) {
      const result = await sessions_list_fn({ limit: 50 });
      sessions = result.sessions || [];
      console.log(`📊 sessions_list 返回 ${sessions.length} 个活跃 sessions`);
    } else {
      console.log('⚠️  sessions_list 不可用');
      return { success: false, reason: 'no_sessions_list' };
    }
  } catch (e) {
    console.error('获取 sessions 列表失败:', e.message);
    return { success: false, reason: 'error', error: e.message };
  }

  // ========== 步骤 2：动态检测正确的工作区 ==========
  let wsInfo;
  try {
    wsInfo = determineCurrentWorkspace(sessions, specifiedWorkspace);
    console.log(`🔍 检测到 agent: ${wsInfo.agentId}`);
    console.log(`🔍 工作区: ${wsInfo.workspace}${wsInfo.isDefault ? ' (默认)' : ''}`);
    
    // 更新全局 workspace 和 PATHS
    workspace = wsInfo.workspace;
    PATHS.workspace = workspace;
    PATHS.dailyDir = path.join(workspace, 'memory', 'daily');
    PATHS.memoryFile = path.join(workspace, 'MEMORY.md');
    PATHS.stateFile = path.join(workspace, 'memory', 'heartbeat-state.json');
    PATHS.configFile = path.join(workspace, 'memory', 'heartbeat-memory-config.json');
    
    console.log('✅ 工作区检测完成');
  } catch (e) {
    console.error('❌ 工作区检测失败:', e.message);
    return { success: false, reason: 'workspace_detection_failed', error: e.message };
  }

  // ========== 步骤 3：扫描文件系统获取 deleted sessions（可选配置） ==========
  // 从第一个 session 的 transcriptPath 推断 sessions 目录
  let fsSessions = [];
  if (sessions.length > 0 && sessions[0].transcriptPath) {
    const sessionsDir = path.dirname(sessions[0].transcriptPath);
    console.log(`📁 推断 sessions 目录：${sessionsDir}`);
    
    // 读取配置，默认扫描最近 30 天
    const scanDays = config.memorySave?.scanFileSystemDays || 30;
    const enableScan = config.memorySave?.scanFileSystem !== false;  // 默认开启
    
    if (enableScan) {
      fsSessions = scanSessionFiles(sessionsDir, scanDays);
      
      // 合并：过滤掉已处理的
      const activeIds = new Set(sessions.map(s => s.sessionId || s.key));
      const processedIdsSet = new Set(state.processedSessions || []);
      
      // 只添加新的、未处理的 deleted sessions
      const newDeleted = fsSessions.filter(s => 
        !activeIds.has(s.sessionId) && !processedIdsSet.has(s.sessionId)
      );
      
      console.log(`📊 活跃 sessions: ${activeIds.size}, deleted: ${newDeleted.length}`);
      
      // 合并到 sessions 列表
      sessions = [...sessions, ...newDeleted.map(s => ({
        ...s,
        key: s.sessionId,
        sessionKey: s.sessionId
      }))];
      
      console.log(`📊 总计 ${sessions.length} 个 sessions（活跃 + deleted）`);
    }
  }

  // ========== 步骤 4：检查工作区权限 ==========
  // Issue #7 修复：启动前检查读写权限
  try {
    const testFile = path.join(workspace, '.heartbeat-memory-permission-test');
    fs.writeFileSync(testFile, 'test', 'utf-8');
    fs.unlinkSync(testFile);
    console.log('✅ 工作区权限检查通过');
  } catch (e) {
    console.error('❌ 工作区权限不足:', e.message);
    return { success: false, reason: 'permission_denied', error: e.message };
  }

  // ========== 步骤 4：确保工作区目录结构存在 ==========
  ensureWorkspaceStructure(workspace);

  // ========== 步骤 5：加载配置和状态 ==========
  const config = config_override || loadConfig();

  if (!config.memorySave?.enabled) {
    console.log('⚠️  自动保存已禁用');
    return { success: true, reason: 'disabled' };
  }

  // ========== 步骤 5.1：自动检测 processSessionsAfter（首次运行时） ==========
  // 如果配置为 null，自动检测最早的 session 日期
  if (!config.memorySave?.processSessionsAfter) {
    const detectedDate = autoDetectProcessSessionsAfter(workspace, sessions);
    if (detectedDate) {
      config.memorySave.processSessionsAfter = detectedDate;
      console.log('✅ 自动设置 processSessionsAfter:', detectedDate);
      
      // 保存配置（只保存一次，后续不再覆盖）
      try {
        const configToSave = Object.assign({}, DEFAULT_CONFIG, config);
        fs.writeFileSync(PATHS.configFile, JSON.stringify(configToSave, null, 2), 'utf-8');
        console.log('✅ 已保存配置到 heartbeat-memory-config.json');
      } catch (e) {
        console.error('⚠️  保存配置失败:', e.message);
      }
    }
  }

  let state = loadState();
  // 向后兼容：processedSessions 可能是数组（旧格式）或对象（新格式）
  const processedSessions = state.processedSessions || {};
  const processedIds = Array.isArray(processedSessions) 
    ? new Set(processedSessions) 
    : new Set(Object.keys(processedSessions));

  // ========== 步骤 5.5：同步 HEARTBEAT.md（配置变更时更新） ==========
  // 计算当前配置 hash，对比 state 中保存的 hash
  const currentHash = computeConfigHash(config);
  if (state.configHash !== currentHash) {
    console.log('📝 检测到配置变更，同步 HEARTBEAT.md...');
    syncHeartbeatMD(config, workspace);
    state.configHash = currentHash;
    saveState(state);
    console.log('✅ HEARTBEAT.md 已更新');
  } else {
    console.log('⏭️  配置未变更，跳过 HEARTBEAT.md 同步');
  }

  // ========== 步骤 5.6：加载自身 subagent 追踪列表 ==========
  const ownSubagentIds = new Set(state.ownSubagentIds || []);
  if (ownSubagentIds.size > 0) {
    console.log(`🔍 已追踪 ${ownSubagentIds.size} 个自身 subagent IDs`);
  }

  // ========== 步骤 6：过滤新 sessions + 字段兼容性检查 ==========
  const processedIdsArray = Array.isArray(state.processedSessions) ? state.processedSessions : Object.keys(state.processedSessions);
  const processedIdsSet = new Set(processedIdsArray);
  const { validSessions, newSessions, skippedCount } = filterSessions(sessions, processedIdsSet, config, ownSubagentIds);

  console.log(`📊 新 sessions: ${newSessions.length} 个`);

  // ========== 步骤 6.5：【新增】检测活跃 session（已处理 session 的新消息） ==========
  const activeSessions = detectActiveSessions(sessions, state.processedSessions, ownSubagentIds);
  console.log(`📊 活跃 sessions: ${activeSessions.length} 个`);

  // Issue #9 修复：限制单次处理数量
  const { limitedSessions, remainingCount } = limitSessions(newSessions, config.memorySave?.maxSessionsPerRun || 50);
  const sessionsToProcess = limitedSessions;

  if (sessionsToProcess.length === 0 && activeSessions.length === 0) {
    console.log('✅ 没有新 sessions 或活跃 session，检查 MEMORY.md 提炼...');
    state.lastCheck = new Date().toISOString();
    saveState(state);
    return { success: true, processed: 0 };
  }

  // ========== 步骤 7 & 8：获取消息 + LLM 提炼 ==========
  const summaries = [];
  const batchSize = config.memorySave?.batchSize || 5;

  for (let i = 0; i < sessionsToProcess.length; i += batchSize) {
    const batch = sessionsToProcess.slice(i, i + batchSize);
    console.log(`\n📦 批次 ${Math.floor(i / batchSize) + 1}/${Math.ceil(sessionsToProcess.length / batchSize)} (${batch.length} 个)`);

    for (const session of batch) {
      const sessionId = session.sessionKey || session.sessionId;
      console.log(`  📝 处理: ${sessionId.substring(0, 20)}...`);

      // 获取消息内容
      let messages = [];
      if (sessions_history_fn) {
        try {
          const historyResult = await sessions_history_fn({
            sessionKey: sessionId,
            limit: 50,
            includeTools: false
          });
          messages = historyResult.messages || [];
        } catch (e) {
          console.log(`    ⚠️  获取消息失败，使用降级: ${e.message}`);
        }
      }

      // 如果拿不到消息，尝试文件系统降级
      if (messages.length === 0) {
        const sessionPath = getSessionPath(session);
        if (sessionPath) {
          messages = readSessionMessages(sessionPath);
        }
      }

      const status = determineSessionStatus(session);

      // LLM 提炼
      let summary = { title: '未命名会话', summary: '无内容', decisions: [], topics: ['#日常'] };

      if (messages.length > 0) {
        const content = messages.slice(0, 10).map(m =>
          `${m.role}: ${(m.content || '').substring(0, 200)}`
        ).join('\n');

        if (sessions_spawn_fn) {
          try {
            console.log(`    🤖 调用 LLM 提炼...`);
            const llmResult = await sessions_spawn_fn({
              task: buildSummarizeTask(content, sessionId),
              runtime: 'subagent',
              mode: 'run',
              // 使用配置的 timeout，默认 1000 秒（防止 subagent 超时）
              timeoutSeconds: config.memorySave?.timeoutSeconds || DEFAULT_CONFIG.memorySave.timeoutSeconds,
              // 执行完毕后自动删除 subagent session，避免残留导致下一轮 heartbeat 被误处理
              cleanup: 'delete'
            });
            // 追踪自身产生的 subagent session ID（防止下一轮被当作新 session 处理）
            if (llmResult && llmResult.sessionId) {
              ownSubagentIds.add(llmResult.sessionId);
            }
            const parsed = parseLLMResult(llmResult);
            if (parsed) {
              summary = parsed;
            } else {
              console.log(`    ⚠️  LLM 解析失败，使用降级方案`);
              summary = summarizeSessionLocal(messages, sessionId);
            }
          } catch (e) {
            console.log(`    ⚠️  LLM 调用失败: ${e.message}`);
            summary = summarizeSessionLocal(messages, sessionId);
          }
        } else {
          console.log(`    ⚠️  subagent 不可用，使用降级方案`);
          summary = summarizeSessionLocal(messages, sessionId);
        }
      }

      summary.status = status;
      summary.id = sessionId;
      summary.startTime = session.updatedAt || session.modified || Date.now();
      summaries.push(summary);
      processedIds.add(sessionId);
    }

    // 批次间延迟
    if (i + batchSize < newSessions.length) {
      await new Promise(r => setTimeout(r, 300));
    }
  }


  // ========== 步骤 8.5：【新增】处理活跃 session 增量更新 ==========
  const activeSessionUpdates = [];
  if (activeSessions.length > 0) {
    console.log('\n🔄 处理活跃 session 增量更新...');
    
    for (const session of activeSessions) {
      const sessionId = session.id;
      console.log(`  📝 增量更新：${sessionId.substring(0, 20)}... (+${session.newMessageCount}条)`);
      
      // 获取增量消息
      const newMessages = await getIncrementalMessages(session, sessions_history_fn);
      
      if (newMessages.length > 0) {
        // 获取现有摘要
        const existingSummary = {
          summary: '已有会话摘要',
          decisions: [],
          topics: session.topics || ['#日常']
        };
        
        // 生成增量摘要
        const incrementalResult = await generateIncrementalSummary(
          newMessages,
          existingSummary,
          sessions_spawn_fn,
          config
        );
        
        if (incrementalResult.hasUpdate) {
          activeSessionUpdates.push({
            id: sessionId,
            title: session.title || '会话更新',
            status: 'active',
            topics: [...existingSummary.topics, ...incrementalResult.newTopics],
            updateSummary: incrementalResult.updateSummary,
            newDecisions: incrementalResult.newDecisions
          });
        }
      }
    }
    
    // 更新 Daily 笔记
    if (activeSessionUpdates.length > 0) {
      const today = new Date().toISOString().split('T')[0];
      const updateResult = updateDailyNoteForActiveSessions(PATHS.dailyDir, activeSessionUpdates, today);
      if (updateResult.success) {
        console.log(`\n📁 Daily 笔记已更新：${path.basename(updateResult.path)}`);
      }
    }
  }

  // ========== 步骤 9：写入 Daily 笔记（带空转保护） ==========
  if (summaries.length > 0) {
    // 空转保护：如果所有摘要都是自身 subagent 的记录，跳过写入
    const hasRealContent = summaries.some(s => !ownSubagentIds.has(s.id));
    if (hasRealContent) {
      const today = new Date().toISOString().split('T')[0];
      const noteContent = generateDailyNote(summaries, today);
      const result = writeDailyNote(noteContent, today);

      if (result.success) {
        console.log(`\n📁 Daily 笔记已生成: ${path.basename(result.path)}`);
      }
    } else {
      console.log('\n⏭️  本轮处理的全是自身 subagent session，跳过 Daily 笔记写入（空转保护）');
    }
  }

  // ========== 步骤 10：更新状态 + MEMORY.md 提炼检查 ==========
  // 更新状态：使用对象格式保存每个 session 的详细状态
  const newProcessedSessions = {};
  for (const id of processedIdsSet) {
    const existingInfo = state.processedSessions[id] || {};
    
    // 从 sessions 列表中查找对应的 session 对象
    const sessionObj = sessions.find(s => (s.sessionKey || s.sessionId || s.key) === id);
    
    // 获取实际消息数：优先从 session 对象获取，否则使用 sessions_history_fn 查询
    let actualMessageCount = existingInfo.lastMessageCount || 0;
    if (sessionObj) {
      // 方案 1：检查 session 对象中是否有 messageCount 字段
      if (typeof sessionObj.messageCount === 'number') {
        actualMessageCount = sessionObj.messageCount;
      }
      // 方案 2：从 lastMessageIndex 推断（如果有）
      else if (typeof sessionObj.lastMessageIndex === 'number') {
        actualMessageCount = sessionObj.lastMessageIndex;
      }
    }
    
    newProcessedSessions[id] = {
      lastMessageTime: new Date().toISOString(),
      lastMessageCount: actualMessageCount,
      status: 'active'
    };
  }
  // 合并活跃 session 的更新
  for (const update of activeSessionUpdates) {
    if (newProcessedSessions[update.id]) {
      newProcessedSessions[update.id].lastMessageTime = new Date().toISOString();
    }
  }
  state.processedSessions = newProcessedSessions;
  // 持久化自身 subagent 追踪列表（保留最近 200 个，避免无限增长）
  const ownIdsArray = Array.from(ownSubagentIds);
  state.ownSubagentIds = ownIdsArray.slice(-200);
  state.lastCheck = new Date().toISOString();
  saveState(state);

  // 检查是否需要提炼 MEMORY.md
  const { shouldRefine } = require('./utils/memory-refiner');
  const needsRefine = shouldRefine(state, config);

  console.log(`\n${needsRefine ? '🧠 需要提炼 MEMORY.md' : '⏭️  跳过 MEMORY.md 提炼'}`);

  if (needsRefine && sessions_spawn_fn) {
    try {
      const { refineMemory } = require('./utils/memory-refiner');
      const result = await refineMemory(PATHS.dailyDir, PATHS.memoryFile, state, config, saveState);
      if (result.success) {
        console.log('✅ MEMORY.md 提炼完成');
      }
    } catch (e) {
      console.log('⚠️  MEMORY.md 提炼失败:', e.message);
    }
  }

  // ========== 步骤 11：发送通知 ==========
  if (message_fn) {
    try {
      // Issue #1 修复：动态获取当前用户 ID
      let target = config.notifyTarget;
      
      if (!target) {
        // 优先用 feishu_get_user 获取当前用户
        if (feishu_get_user_fn) {
          try {
            const userInfo = await feishu_get_user_fn();
            target = `user:${userInfo.open_id || userInfo.user_id}`;
            console.log('✅ 自动获取当前用户 ID:', target);
          } catch (e) {
            console.log('⚠️  feishu_get_user 失败，使用 fallback');
          }
        }
        
        // Fallback: 从 sessions 提取用户 ID
        if (!target && sessions && sessions.length > 0) {
          const sessionKey = sessions[0].sessionKey || sessions[0].key || '';
          const match = sessionKey.match(/:(ou_[a-z0-9]+)$/);
          if (match) {
            target = `user:${match[1]}`;
            console.log('✅ 从 sessionKey 提取用户 ID:', target);
          }
        }
        
        // 最终 fallback: 不发送通知
        if (!target) {
          console.log('⚠️  无法获取通知目标，跳过通知发送');
          target = null;
        }
      }
      
      // Issue #2 修复：支持多种通知渠道
      if (target) {
        await message_fn({
          action: 'send',
          target: target,
          message: `📊 heartbeat-memory 执行完成

✅ 检查 sessions: ${sessions.length} 个
✅ 新处理：${summaries.length} 个
${needsRefine ? '✅ MEMORY.md 已提炼' : ''}
⏰ ${new Date().toLocaleString('zh-CN')}`
        });
        console.log('✅ 通知已发送');
      }
    } catch (e) {
      console.log('⚠️  发送通知失败:', e.message);
    }
  }

  console.log('\n✅ heartbeat-memory 执行完成！');
  return { success: true, processed: summaries.length };
}

// ============================================================
// 自包含执行入口（subagent 直接使用全局工具）
// ============================================================

/**
 * 自包含执行入口 - 直接使用全局工具函数
 * 适用于 OpenClaw Agent 运行时环境（工具已注入）
 */
async function run(configOverride, specifiedWorkspace) {
  console.log('🚀 heartbeat-memory 启动...\n');
  
  // 检查工具是否全局可用
  const tools = {
    sessions_list: typeof sessions_list !== 'undefined' ? sessions_list : null,
    sessions_history: typeof sessions_history !== 'undefined' ? sessions_history : null,
    sessions_spawn: typeof sessions_spawn !== 'undefined' ? sessions_spawn : null,
    message: typeof message !== 'undefined' ? message : null,
    feishu_get_user: typeof feishu_get_user !== 'undefined' ? feishu_get_user : null
  };
  
  // 验证必要工具
  if (!tools.sessions_list) {
    const errorMsg = `❌ sessions_list 工具不可用

💡 正确调用方式：
1. Heartbeat 自动触发（推荐）- 系统会在 Heartbeat 时自动调用
2. 在主 Agent 会话中直接调用 - const heartbeat = require('~/.openclaw/skills/heartbeat-memory/index.js'); await heartbeat.run();

❌ 错误方式：独立 Node.js 进程或 sessions_spawn 调用（无工具注入）

📖 详细文档：~/.openclaw/skills/heartbeat-memory/SKILL.md`;
    console.error(errorMsg);
    throw new Error('sessions_list 工具不可用 - 需要在主 Agent 会话中调用');
  }
  
  if (!tools.sessions_history) {
    throw new Error('sessions_history 工具不可用 - 需要在 Agent 运行时环境中调用');
  }
  
  console.log('✅ 工具检查通过:');
  Object.entries(tools).forEach(([name, available]) => {
    console.log(`   ${available ? '✅' : '⚠️'}  ${name}`);
  });
  console.log('');
  
  // 检查 Heartbeat 是否启用
  try {
    const fs = require('fs');
    const path = require('path');
    const os = require('os');
    const configPath = path.join(os.homedir(), '.openclaw', 'openclaw.json');
    const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    const heartbeatConfig = config?.agents?.defaults?.heartbeat;
    
    // 检查 Heartbeat 是否启用（有 every 字段即表示启用）
    const hasHeartbeat = heartbeatConfig && (heartbeatConfig.every || heartbeatConfig.enabled);
    
    if (!hasHeartbeat) {
      console.warn('⚠️  警告：Heartbeat 未启用！heartbeat-memory 需要 Heartbeat 机制才能自动运行。');
      console.warn('解决方案：在 openclaw.json 中添加 "agents.defaults.heartbeat": {"every": "30m"}，然后重启 Gateway');
      console.warn('或者手动触发：在聊天中发送 "执行 heartbeat-memory"');
    } else {
      const interval = heartbeatConfig.every || `${heartbeatConfig.intervalMinutes || 30}m`;
      console.log('✅ Heartbeat 已启用（interval:', interval, '）');
    }
  } catch (e) {
    console.warn('⚠️  无法检查 Heartbeat 配置:', e.message);
    console.log('');
  }
  
  // 调用主处理函数
  return await processSessions(
    tools.sessions_list,
    tools.sessions_history,
    tools.sessions_spawn,
    tools.message,
    tools.feishu_get_user,
    configOverride,
    specifiedWorkspace
  );
}

// 导出（供 subagent 调用）
module.exports = {
  run,
  processSessions,
  loadConfig,
  loadState,
  saveState,
  generateDailyNote,
  writeDailyNote,
  statusEmoji,
  PATHS,
  DEFAULT_CONFIG,
  getAgentWorkspaceMap,
  determineCurrentWorkspace,
  ensureWorkspaceStructure,
  // 导出工具模块（供外部使用）
  syncHeartbeatMD: require('./utils/config-sync').syncHeartbeatMD,
  computeConfigHash: require('./utils/config-sync').computeConfigHash,
  autoDetectProcessSessionsAfter: require('./utils/date-detector').autoDetectProcessSessionsAfter,
  filterSessions: require('./utils/session-filters').filterSessions,
  limitSessions: require('./utils/session-filters').limitSessions
};

// 如果直接运行此文件（Node.js CLI 模式）
if (require.main === module) {
  run().catch(e => {
    console.error('执行失败:', e.message);
    process.exit(1);
  });
}
