/**
 * Memory Archiver - 统一 Hook Handler
 *
 * 事件：message:received
 * 功能：
 *   1. 自动记忆搜索 - 检测消息类型，搜索相关记忆并注入上下文
 *   2. 自动记忆提取 - 从对话中提取持久记忆，分类存储
 *   3. 会话笔记追踪 - 维护当前活跃会话笔记
 */

import { execFile, execFileSync, execSync } from 'child_process';
import { promisify } from 'util';
import * as path from 'path';
import * as fs from 'fs';

const execFileAsync = promisify(execFile);

const HOME_DIR = process.env.HOME || '/root';
const WORKSPACE = path.join(HOME_DIR, '.openclaw', 'workspace');
const SKILLS_DIR = path.join(WORKSPACE, 'skills', 'memory-archiver');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');

// ========== 模块 1: 自动记忆搜索 ==========

/**
 * 检测消息类型
 */
function detectMessageType(message) {
  const lowerMsg = message.toLowerCase();

  if (/怎么|如何|为什么|什么|哪里|何时|谁|哪个|whether|what|how|why|where|when|who/.test(lowerMsg)) {
    return '疑问';
  }
  if (/修复|bug|错误|问题|故障|解决|repair|fix|error|issue|debug/.test(lowerMsg)) {
    return '修复';
  }
  if (/规范|规则|标准|要求|必须|应该|spec|standard|rule|require/.test(lowerMsg)) {
    return '规范';
  }
  if (/特征|特点|特性|特色|feature|characteristic/.test(lowerMsg)) {
    return '特征';
  }
  if (/配置|设置|安装|部署|环境|config|setup|install|deploy|environment/.test(lowerMsg)) {
    return '配置';
  }
  if (/命令|指令|脚本|用法|example|command|script|usage/.test(lowerMsg)) {
    return '命令';
  }
  if (/\b(css|html|php|javascript|node|npm|tailwind|vite|thinkphp)\b/i.test(lowerMsg)) {
    return '技术';
  }
  return null;
}

/**
 * 提取关键词
 */
function extractKeywords(message) {
  const enKeywords = message.match(/[A-Za-z0-9_]{2,}/g) || [];
  const cnKeywords = message
    .split(/[\s,，.。!?！？;；:：]+/)
    .filter(w => w.length >= 2 && /[\u4e00-\u9fa5]/.test(w));
  const all = [...new Set([...enKeywords, ...cnKeywords])];
  return all.slice(0, 5);
}

/**
 * 搜索记忆
 * 
 * 安全修复: 使用 execFile 传参数数组，不经过 shell，
 * 彻底杜绝命令注入（backtick、$()、;、|、&& 等）
 */
async function searchMemory(message) {
  const scriptPath = path.join(SKILLS_DIR, 'scripts', 'auto-memory-search.js');
  if (!fs.existsSync(scriptPath)) {
    console.log('[MemorySearch] 脚本不存在');
    return null;
  }
  try {
    const { stdout } = await execFileAsync('node', [scriptPath, message]);
    return stdout.trim() || null;
  } catch (error) {
    console.log('[MemorySearch] 搜索失败:', error.message);
    return null;
  }
}

// ========== 模块 2: 自动记忆提取 ==========

/**
 * 记忆分类（基于关键词规则）
 */
function classifyMemory(content) {
  const rules = {
    user: {
      keywords: ['偏好', '喜欢', '习惯', '角色', '目标', '负责', '职位', '身份', '称呼', '语言', '时区'],
      patterns: [/我是.+/, /我叫.+/, /我的.+是/, /我希望.+/, /我偏好.+/],
      weight: 1
    },
    feedback: {
      keywords: ['不对', '错误', '纠正', '不是', '应该', '不要', '禁止', '避免', '改进', '修复', '教训'],
      patterns: [/不要.+/, /禁止.+/, /避免.+/, /应该.+/, /不应该.+/],
      weight: 1.2
    },
    project: {
      keywords: ['项目', '任务', '需求', '架构', '方案', '设计', '部署', '工作区', '路由', '数据库'],
      patterns: [/我们.+做/, /这个.+是/, /需要.+/, /计划.+/, /决定.+/],
      weight: 1
    },
    reference: {
      keywords: ['命令', '脚本', '配置', '参数', '格式', '用法', 'api', '接口', '协议'],
      patterns: [/用.+.实现/, /通过.+方式/, /使用.+方法/],
      weight: 0.8
    }
  };

  let bestType = 'reference';
  let bestScore = 0;

  for (const [type, rule] of Object.entries(rules)) {
    let score = 0;
    for (const kw of rule.keywords) {
      if (content.includes(kw)) score += rule.weight;
    }
    for (const pattern of rule.patterns) {
      if (pattern.test(content)) score += rule.weight * 1.5;
    }
    if (score > bestScore) {
      bestScore = score;
      bestType = type;
    }
  }

  return bestScore > 0 ? bestType : 'reference';
}

/**
 * 提取记忆（后台执行，不阻塞 hook）
 * 
 * 安全修复: 使用 execFile 传参数数组，不经过 shell
 */
function extractMemoryAsync(message) {
  const scriptPath = path.join(SKILLS_DIR, 'scripts', 'memory-extract.js');
  if (!fs.existsSync(scriptPath)) return;

  try {
    execFile('node', [scriptPath, message], { stdio: 'ignore' });
  } catch (e) {
    console.log('[MemoryExtract] 提取失败:', e.message);
  }
}

// ========== 模块 3: 会话笔记追踪 ==========

const SESSIONS_DIR = path.join(MEMORY_DIR, 'sessions');
const CURRENT_FILE = path.join(SESSIONS_DIR, '.current-session.json');
const ARCHIVE_DIR = path.join(SESSIONS_DIR, 'archive');
const COUNTER_FILE = path.join(SESSIONS_DIR, '.message-counter');

function getMessageCount() {
  try {
    return parseInt(fs.readFileSync(COUNTER_FILE, 'utf8').trim()) || 0;
  } catch (e) {
    return 0;
  }
}

function incrementMessageCount() {
  const count = getMessageCount() + 1;
  fs.writeFileSync(COUNTER_FILE, count.toString());
  return count;
}

function hasActiveSession() {
  return fs.existsSync(CURRENT_FILE);
}

function generateSessionId() {
  return Date.now().toString(36) + Math.random().toString(36).substring(2, 8);
}

function initSession(topic = '未命名会话') {
  if (!fs.existsSync(SESSIONS_DIR)) {
    fs.mkdirSync(SESSIONS_DIR, { recursive: true });
  }
  if (!fs.existsSync(ARCHIVE_DIR)) {
    fs.mkdirSync(ARCHIVE_DIR, { recursive: true });
  }

  const sessionId = generateSessionId();
  const now = new Date().toISOString();
  const filepath = path.join(SESSIONS_DIR, `${sessionId}.md`);

  const meta = {
    sessionId,
    topic,
    startedAt: now,
    endedAt: null,
    filepath,
    messageCount: 0,
    lastUpdatedAt: now,
    archived: false
  };

  const content = `---
session_id: ${sessionId}
topic: ${topic}
started: ${now}
ended: 
message_count: 0
archived: false
---

# 会话笔记: ${topic}

## 关键决策


## 待办事项


## 重要发现


## 用户偏好


`;

  fs.writeFileSync(filepath, content, 'utf8');
  fs.writeFileSync(CURRENT_FILE, JSON.stringify(meta, null, 2));
  console.log(`[SessionNotes] 初始化会话: ${sessionId} (${topic})`);
  return meta;
}

function updateSessionNote(content) {
  if (!hasActiveSession()) {
    initSession('自动会话 ' + new Date().toLocaleString('zh-CN'));
    return updateSessionNote(content);
  }

  const meta = JSON.parse(fs.readFileSync(CURRENT_FILE, 'utf8'));
  if (!fs.existsSync(meta.filepath)) return;

  let fileContent = fs.readFileSync(meta.filepath, 'utf8');
  fileContent += `\n${content}\n`;

  meta.messageCount = (meta.messageCount || 0) + 1;
  meta.lastUpdatedAt = new Date().toISOString();
  fs.writeFileSync(CURRENT_FILE, JSON.stringify(meta, null, 2));

  fileContent = fileContent.replace(/message_count: \d+/, `message_count: ${meta.messageCount}`);
  fs.writeFileSync(meta.filepath, fileContent, 'utf8');
}

// ========== 统一主 Hook ==========

const handler = async (event) => {
  console.log(`[MemoryArchiver] Hook triggered: type=${event.type}, action=${event.action}`);

  if (event.type !== 'message' || event.action !== 'received') {
    return;
  }

  const userMessage = event.context?.content || event.message?.text || '';
  if (!userMessage) {
    console.log('[MemoryArchiver] No message content');
    return;
  }

  // 跳过系统消息/cron/心跳
  if (userMessage.startsWith('System:') ||
      userMessage.includes('记忆及时写入检查') ||
      userMessage.includes('工作进度检查') ||
      userMessage.includes('错误监控检查') ||
      userMessage.includes('全量工作监控') ||
      userMessage.includes('Token 使用自动记录') ||
      userMessage.includes('HEARTBEAT')) {
    console.log('[MemoryArchiver] Skipping system/cron/heartbeat');
    return;
  }

  // === 模块 1: 自动记忆搜索 ===
  const msgType = detectMessageType(userMessage);
  if (msgType) {
    console.log(`[MemorySearch] 检测到消息类型: ${msgType}`);
    const searchResults = await searchMemory(userMessage);
    if (searchResults) {
      event.messages.push(`📚 相关记忆:\n${searchResults}`);
      console.log('[MemorySearch] 记忆已注入');
    }
  }

  // === 模块 2: 自动记忆提取（后台） ===
  console.log('[MemoryExtract] 触发后台记忆提取');
  extractMemoryAsync(userMessage);

  // === 模块 3: 会话笔记追踪 ===
  if (!hasActiveSession()) {
    // 从消息内容猜测主题
    const topic = userMessage.substring(0, 50).replace(/[\n\r]/g, ' ');
    initSession(topic);
  }

  const count = incrementMessageCount();
  if (count % 10 === 0) {
    // 每 10 条消息更新一次笔记
    updateSessionNote(`- [${new Date().toLocaleTimeString('zh-CN')}] 消息 #${count}`);
    console.log(`[SessionNotes] 更新笔记 (第 ${count} 条)`);
  }
};

export default handler;
