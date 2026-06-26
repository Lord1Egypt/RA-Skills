#!/usr/bin/env node

/**
 * memory-refiner.js - MEMORY.md 提炼工具。MEMORY.md refiner utility.
 * 
 * 负责从 Daily 笔记中提炼长期记忆，使用 OpenClaw 主 LLM 智能分析和分类。
 * Responsible for refining long-term memory from Daily notes using OpenClaw main LLM.
 * 
 * 2026-03-27 更新：新增活跃 session 增量更新功能（方案 C）
 * - 检测活跃 session（比较 lastMessageTime）
 * - 增量获取 session 历史（从 lastMessageIndex 开始）
 * - 生成增量摘要
 */

const fs = require('fs');
const path = require('path');

// 注意：MEMORY.md 提炼使用规则引擎（降级方案），不使用 subagent
// 原因：subagent-runner.js 已在优化阶段删除（代码模块化）
// 如需使用 LLM 提炼，需要在 index.js 中直接调用 sessions_spawn

/**
 * 读取所有 Daily 笔记
 */
function readAllDailyNotes(dailyDir) {
  if (!fs.existsSync(dailyDir)) {
    return [];
  }
  
  const files = fs.readdirSync(dailyDir)
    .filter(f => f.endsWith('.md'))
    .sort()
    .reverse(); // 最新的在前
  
  const notes = [];
  
  for (const file of files) {
    try {
      const content = fs.readFileSync(path.join(dailyDir, file), 'utf-8');
      notes.push({
        filename: file,
        date: file.replace('.md', ''),
        content
      });
    } catch (error) {
      console.error(`读取 ${file} 失败:`, error.message);
    }
  }
  
  return notes;
}

/**
 * 使用 LLM 从 Daily 笔记中提炼长期记忆
 */
async function refineMemoryWithLLM(dailyNotes) {
  if (dailyNotes.length === 0) {
    console.log('⚠️  没有 Daily 笔记可提炼');
    return { success: false, reason: 'no_notes' };
  }
  
  console.log(`📄 读取了 ${dailyNotes.length} 篇 Daily 笔记`);
  
  // 如果笔记太多，只处理最近的 10 篇
  const notesToProcess = dailyNotes.slice(0, 10);
  
  const notesContent = notesToProcess.map(note => {
    return `【${note.date}】\n${note.content.substring(0, 2000)}`;
  });
  
  // 注意：已移除 subagent 调用，直接使用规则提炼
  // 原因：subagent-runner.js 已在代码模块化时删除
  // 如需 LLM 提炼，应在 index.js 主流程中调用 sessions_spawn
  console.log('  📝 使用规则提炼长期记忆...');
  return refineMemoryWithRules(dailyNotes);
}

/**
 * 使用规则提炼记忆（降级方案）
 */
function refineMemoryWithRules(dailyNotes) {
  const MEMORY_CATEGORIES = {
    USER_PREFERENCES: {
      key: 'userPreferences',
      title: '🎯 用户偏好',
      keywords: ['偏好', '喜欢', '习惯', '风格', '语言', '时区', '格式', '配置']
    },
    DECISIONS: {
      key: 'decisions',
      title: '💡 重要决策',
      keywords: ['决定', '决策', '确定', '选择', '采用', '使用']
    },
    PROJECTS: {
      key: 'projects',
      title: '📈 项目进展',
      keywords: ['项目', '进展', '完成', '进行中', '任务', '目标']
    },
    TODOS: {
      key: 'todos',
      title: '📋 待办事项',
      keywords: ['待办', '计划', '要做', '未完成', '接下来', '后续']
    },
    SKILLS: {
      key: 'skills',
      title: '🔧 技能配置',
      keywords: ['Skill', '技能', '安装', '配置', '工具', '扩展']
    },
    LEARNINGS: {
      key: 'learnings',
      title: '📚 关键学习',
      keywords: ['学习', '经验', '教训', '问题', '解决', '方案', '发现']
    }
  };
  
  const memories = {};
  
  // 初始化分类
  Object.values(MEMORY_CATEGORIES).forEach(cat => {
    memories[cat.key] = [];
  });
  
  for (const note of dailyNotes) {
    const lines = note.content.split('\n');
    
    for (const line of lines) {
      const trimmedLine = line.trim();
      if (trimmedLine.length < 10 || trimmedLine.startsWith('#')) continue;
      
      // 检查每个分类
      for (const category of Object.values(MEMORY_CATEGORIES)) {
        for (const keyword of category.keywords) {
          if (trimmedLine.toLowerCase().includes(keyword.toLowerCase())) {
            // 避免重复
            const exists = memories[category.key].some(
              m => m.content.includes(trimmedLine.substring(0, 50))
            );
            
            if (!exists) {
              memories[category.key].push({
                content: trimmedLine,
                source: note.date,
                category: category.key
              });
            }
            break;
          }
        }
      }
    }
  }
  
  // 生成 MEMORY.md 内容
  let content = `# MEMORY.md - 长期记忆\n\n`;
  content += `_最后更新：${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}_\n\n`;
  content += `> 此文件由 heartbeat-memory Skill 自动维护，记录重要的长期记忆。\n\n`;
  content += `---\n\n`;
  
  for (const category of Object.values(MEMORY_CATEGORIES)) {
    const items = memories[category.key] || [];
    
    content += `## ${category.title}\n\n`;
    
    if (items.length === 0) {
      content += `_暂无内容_\n\n`;
    } else {
      // 限制每个分类最多 10 条，按日期排序（最新的在前）
      const sorted = items.sort((a, b) => b.source.localeCompare(a.source)).slice(0, 10);
      for (const item of sorted) {
        content += `- ${item.content} _(${item.source})_\n`;
      }
      content += '\n';
    }
    
    content += `---\n\n`;
  }
  
  return {
    success: true,
    content,
    notesProcessed: dailyNotes.length,
    totalItems: Object.values(memories).reduce((sum, items) => sum + items.length, 0)
  };
}

/**
 * 写入 MEMORY.md
 */
function writeMemoryFile(content, memoryPath) {
  try {
    // 确保目录存在
    const dir = path.dirname(memoryPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    fs.writeFileSync(memoryPath, content, 'utf-8');
    return { success: true, path: memoryPath };
  } catch (error) {
    console.error('写入 MEMORY.md 失败:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * 检查是否需要提炼
 * 使用 lastRefine 字段（只记录提炼时间），和 lastCheck（检查时间）分离
 */
function shouldRefine(state, config) {
  const schedule = config.memorySave?.refineSchedule || { type: 'weekly', dayOfWeek: 'sunday', time: '20:00' };
  
  // 首次运行：强制触发提炼
  if (!state.lastRefine) {
    return true;
  }
  
  const now = new Date();
  const lastRefine = new Date(state.lastRefine);
  
  if (schedule.type === 'weekly') {
    const days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
    const targetDay = days.indexOf(schedule.dayOfWeek);
    const currentDay = now.getDay();
    
    if (currentDay === targetDay) {
      const [targetHour, targetMinute] = (schedule.time || '20:00').split(':').map(Number);
      const lastHour = lastRefine.getHours();
      const lastMinute = lastRefine.getMinutes();
      const currentHour = now.getHours();
      const currentMinute = now.getMinutes();
      
      const lastTotalMinutes = lastHour * 60 + lastMinute;
      const currentTotalMinutes = currentHour * 60 + currentMinute;
      const targetTotalMinutes = targetHour * 60 + targetMinute;
      
      // 检查是否已过目标时间且上次提炼在目标时间之前
      return currentTotalMinutes >= targetTotalMinutes && lastTotalMinutes < targetTotalMinutes;
    }
  } else if (schedule.type === 'interval') {
    const daysDiff = (now - lastRefine) / (1000 * 60 * 60 * 24);
    return daysDiff >= (schedule.days || 7);
  }
  
  return false;
}

/**
 * 【新增功能】检测活跃 session（比较 lastMessageTime）
 * 
 * @param {Array} sessions - 当前 sessions 列表
 * @param {Object} processedSessions - 已处理的 session 状态对象
 * @param {Set|Array} [ownSubagentIds] - heartbeat-memory 自身产生的 subagent session IDs（可选）
 * @returns {Array} 活跃 session 列表（有新消息的已处理 session）
 */
function detectActiveSessions(sessions, processedSessions, ownSubagentIds) {
  const activeSessions = [];
  const ownIds = ownSubagentIds instanceof Set ? ownSubagentIds : new Set(ownSubagentIds || []);
  
  for (const session of sessions) {
    const sessionKey = session.sessionKey || session.key || '';
    const sessionId = session.sessionId || session.id || '';
    // 跳过 subagent session（内部会话，非用户交互）
    if (sessionKey.includes(':subagent:')) continue;
    if (session.kind === 'subagent' || session.kind === 'heartbeat') continue;
    // 跳过 heartbeat-memory 自身追踪的 subagent IDs
    if (ownIds.has(sessionKey) || ownIds.has(sessionId)) continue;

    const resolvedId = session.sessionKey || session.sessionId || session.key;
    const sessionInfo = processedSessions[resolvedId];
    
    if (!sessionInfo) {
      // 新 session，不在活跃检测范围内
      continue;
    }
    
    // 检查是否有新消息
    const currentMessageCount = session.messageCount ?? (session.lastMessageIndex ?? 0);
    const lastMessageCount = sessionInfo.lastMessageCount ?? 0;
    
    if (currentMessageCount > lastMessageCount) {
      // 有新消息，标记为活跃
      activeSessions.push({
        ...session,
        id: resolvedId,
        newMessageCount: currentMessageCount - lastMessageCount,
        lastMessageIndex: lastMessageCount // 从上次的位置继续
      });
      
      console.log(`  🔄 检测到活跃 session: ${resolvedId.substring(0, 20)}... (+${currentMessageCount - lastMessageCount} 条消息)`);
    }
  }
  
  return activeSessions;
}

/**
 * 【新增功能】增量获取 session 历史（从 lastMessageIndex 开始）
 * 
 * @param {Object} session - session 对象
 * @param {Function} sessions_history_fn - sessions_history 工具函数
 * @returns {Promise<Array>} 新增的消息列表
 */
async function getIncrementalMessages(session, sessions_history_fn) {
  const lastMessageIndex = session.lastMessageIndex || 0;
  
  try {
    const historyResult = await sessions_history_fn({
      sessionKey: session.id,
      limit: 100, // 获取足够的消息
      includeTools: false
    });
    
    const allMessages = historyResult.messages || [];
    
    // 只返回新增的消息
    const newMessages = allMessages.slice(lastMessageIndex);
    
    console.log(`    📝 获取到 ${newMessages.length} 条新增消息（从第 ${lastMessageIndex} 条开始）`);
    
    return newMessages;
  } catch (error) {
    console.error(`    ⚠️  获取增量消息失败:`, error.message);
    return [];
  }
}

/**
 * 【新增功能】生成增量摘要
 * 
 * @param {Array} newMessages - 新增的消息列表
 * @param {Object} existingSummary - 现有的摘要信息
 * @param {Function} sessions_spawn_fn - sessions_spawn 工具函数
 * @param {Object} config - 配置对象
 * @returns {Promise<Object>} 增量摘要
 */
async function generateIncrementalSummary(newMessages, existingSummary, sessions_spawn_fn, config) {
  if (newMessages.length === 0) {
    return {
      updateSummary: '无新内容',
      newDecisions: [],
      newTopics: [],
      hasUpdate: false
    };
  }
  
  // 优化消息处理：优先处理用户消息，根据消息长度动态调整处理数量
  const userMessages = newMessages.filter(m => m.role === 'user');
  const assistantMessages = newMessages.filter(m => m.role === 'assistant');
  
  // 动态调整处理数量：消息短则多处理，消息长则少处理
  const avgLength = newMessages.reduce((sum, m) => sum + (m.content?.length || 0), 0) / newMessages.length;
  const maxMessages = avgLength > 500 ? 8 : (avgLength > 200 ? 12 : 20);
  
  // 优先取用户消息，再补充 AI 回复
  const selectedUserMsgs = userMessages.slice(0, Math.ceil(maxMessages * 0.7)); // 70% 用户消息
  const selectedAssistantMsgs = assistantMessages.slice(0, Math.floor(maxMessages * 0.3)); // 30% AI 回复
  
  // 提取关键片段：长消息截取首尾，保留上下文
  const extractKeyContent = (msg, maxLength = 300) => {
    const content = msg.content || '';
    if (content.length <= maxLength) return content;
    // 保留开头 150 字和结尾 150 字
    const start = content.substring(0, 150);
    const end = content.substring(content.length - 150);
    return `${start}...[省略]...${end}`;
  };
  
  // 构建消息内容：包含上下文信息
  const newContent = [
    '【对话上下文】',
    `新增消息数：${newMessages.length} 条（用户：${userMessages.length}, AI: ${assistantMessages.length}）`,
    `平均消息长度：${Math.round(avgLength)} 字`,
    '',
    '【新增对话内容】',
    ...selectedUserMsgs.map(m => `用户：${extractKeyContent(m)}`),
    ...selectedAssistantMsgs.map(m => `AI: ${extractKeyContent(m)}`)
  ].join('\n');
  
  console.log(`    🤖 调用 LLM 生成增量摘要... (处理 ${selectedUserMsgs.length + selectedAssistantMsgs.length} 条消息)`);
  
  // 使用 LLM 提炼新增内容
  if (sessions_spawn_fn) {
    try {
      const llmResult = await sessions_spawn_fn({
        task: buildIncrementalSummarizeTask(newContent, existingSummary),
        runtime: 'subagent',
        mode: 'run',
        timeoutSeconds: config.memorySave?.timeoutSeconds || 1000,
        cleanup: 'delete'
      });
      
      const parsed = parseIncrementalLLMResult(llmResult);
      if (parsed) {
        return {
          ...parsed,
          hasUpdate: true
        };
      }
    } catch (error) {
      console.log(`    ⚠️  LLM 调用失败，使用降级方案：${error.message}`);
    }
  }
  
  // 降级方案：简单总结
  return {
    updateSummary: `新增 ${newMessages.length} 条消息，讨论了 ${newContent.substring(0, 100)}...`,
    newDecisions: [],
    newTopics: ['#更新'],
    hasUpdate: true
  };
}

/**
 * 【新增功能】构建增量摘要 LLM Prompt
 * 
 * 增强版 Prompt：
 * - 添加上下文（之前的决策/话题）
 * - 明确要求（区分新增 vs 已有）
 * - 输出格式更严格
 */
function buildIncrementalSummarizeTask(newContent, existingSummary) {
  return `你是一名专业的会话分析助手，负责从新增对话中提取关键信息并生成增量摘要。

## 背景上下文
这是某个会话的新增消息，之前已经处理过部分历史消息。你需要：
1. 理解新增内容与之前话题的关联
2. 识别是否有新的话题分支或决策
3. 避免重复记录已有的信息

## 现有摘要（之前的处理结果）
${existingSummary.summary ? `**核心内容：** ${existingSummary.summary}` : '无历史记录'}
${existingSummary.decisions && existingSummary.decisions.length > 0 ? `**已有决策：**\n${existingSummary.decisions.map(d => `- ${d}`).join('\n')}` : ''}
${existingSummary.topics && existingSummary.topics.length > 0 ? `**话题标签：** ${existingSummary.topics.join(', ')}` : ''}

## 新增对话内容
${newContent}

## 任务要求

### 1. 总结新增内容（50-150 字）
- 聚焦**新增**的讨论点，不要重复已有摘要
- 如果有延续之前的话题，说明进展/变化
- 如果是全新话题，明确指出

### 2. 提取新的关键决策/发现（0-3 个）
- 只提取**本次新增**的决策，不要重复已有决策
- 包括：明确的选择、确定的方案、达成的共识、重要的发现
- 如果没有新决策，返回空数组

### 3. 识别新的话题标签（0-3 个）
- 使用 #关键词 格式
- 只添加**新出现**的话题标签
- 优先从以下常见标签中选择：#Skill #配置 #修复 #飞书 #OpenClaw #对话 #代码 #文档 #项目 #决策 #问题 #方案
- 如果有全新的主题，可以自定义标签

## 输出格式（严格 JSON）

请只返回纯 JSON 对象，不要任何其他文字、解释或 Markdown 格式：

{
  "updateSummary": "用 1-2 句话总结新增内容，突出与之前的差异或进展",
  "newDecisions": ["仅在有新决策时填写，否则为空数组"],
  "newTopics": ["#仅在有新话题时填写", "#否则为空数组"]
}

## 注意事项
- 如果新增内容只是日常对话/问候，没有实质信息，updateSummary 可以简短
- 如果新增内容与之前完全无关（新话题），在 summary 中明确指出
- 确保 JSON 格式正确，可以被直接解析
- 不要输出 json 代码块标记或其他 Markdown 标记`;
}

/**
 * 【新增功能】解析增量 LLM 结果
 */
function parseIncrementalLLMResult(llmResult) {
  try {
    // 尝试解析 JSON
    let parsed;
    if (typeof llmResult === 'string') {
      const jsonMatch = llmResult.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        parsed = JSON.parse(jsonMatch[0]);
      }
    } else if (typeof llmResult === 'object') {
      parsed = llmResult;
    }
    
    if (parsed && parsed.updateSummary) {
      return {
        updateSummary: parsed.updateSummary || '无新内容',
        newDecisions: parsed.newDecisions || [],
        newTopics: parsed.newTopics || []
      };
    }
  } catch (error) {
    console.log(`    ⚠️  解析增量 LLM 结果失败：${error.message}`);
  }
  
  return null;
}

/**
 * 【新增功能】更新 Daily 笔记（支持追加/更新）
 * 
 * @param {string} dailyDir - Daily 笔记目录
 * @param {Array} activeSessionUpdates - 活跃 session 更新列表
 * @param {string} date - 日期字符串
 * @returns {Object} 写入结果
 */
function updateDailyNoteForActiveSessions(dailyDir, activeSessionUpdates, date) {
  const dateStr = typeof date === 'string' ? date : date.toISOString().split('T')[0];
  const filePath = path.join(dailyDir, `${dateStr}.md`);
  
  if (!fs.existsSync(filePath)) {
    console.log(`  ⚠️  Daily 笔记不存在：${filePath}，跳过更新`);
    return { success: false, reason: 'file_not_found' };
  }
  
  try {
    let content = fs.readFileSync(filePath, 'utf-8');
    let hasChanges = false;
    
    for (const update of activeSessionUpdates) {
      const sessionId = update.id;
      const emoji = statusEmoji(update.status || 'active');
      const tags = Array.isArray(update.topics) ? update.topics.join(' ') : (update.topics || '#日常');
      
      // 检查是否已存在该 session
      const sessionRegex = new RegExp(`(### 📋 .*?)\\n\\*\\*标签：\\*\\*.*?${sessionId.substring(0, 10)}`, 'i');
      
      if (sessionRegex.test(content)) {
        // 已存在，追加更新内容
        const updateSection = `
**🔄 更新（${new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })}）：**
${update.updateSummary || '有新对话'}
${update.newDecisions && update.newDecisions.length > 0 ? `\n**新增决策：**\n${update.newDecisions.map(d => `- ${d}`).join('\n')}` : ''}
`;
        
        // 在现有 session 后追加更新
        content = content.replace(
          new RegExp(`(### 📋 .*?---)`, 's'),
          `$1\n${updateSection}`
        );
        
        console.log(`  ✅ 已更新 session: ${sessionId.substring(0, 20)}...`);
      } else {
        // 不存在，添加新小节（这种情况不应该出现，因为活跃 session 应该已处理过）
        const newSection = `
### 📋 ${update.title || '会话更新'}

**标签：** ${emoji} | ${tags} | 🔄 已更新
**时间：** ${new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })}
**摘要：** ${update.updateSummary || '有新对话'}
${update.newDecisions && update.newDecisions.length > 0 ? `\n**新增决策：**\n${update.newDecisions.map(d => `- ${d}`).join('\n')}` : ''}

---
`;
        content += newSection;
        console.log(`  ✅ 已添加 session 更新：${sessionId.substring(0, 20)}...`);
      }
      
      hasChanges = true;
    }
    
    if (hasChanges) {
      fs.writeFileSync(filePath, content, 'utf-8');
      console.log(`  ✅ Daily 笔记已更新：${filePath}`);
      return { success: true, path: filePath };
    }
    
    return { success: false, reason: 'no_changes' };
  } catch (error) {
    console.error(`  ❌ 更新 Daily 笔记失败：${error.message}`);
    return { success: false, error: error.message };
  }
}

/**
 * 主提炼函数
 */
async function refineMemory(dailyDir, memoryPath, state, config, saveStateFn) {
  console.log('🧠 开始提炼 MEMORY.md...');
  
  // 读取所有 Daily 笔记
  const notes = readAllDailyNotes(dailyDir);
  
  if (notes.length === 0) {
    console.log('⚠️  没有 Daily 笔记可提炼');
    return { success: false, reason: 'no_notes' };
  }
  
  // 使用 LLM 提炼记忆
  const result = await refineMemoryWithLLM(notes);
  
  if (result.success) {
    // 写入文件
    const writeResult = writeMemoryFile(result.content, memoryPath);
    
    if (writeResult.success) {
      console.log('✅ MEMORY.md 提炼完成');
      
      // 更新 lastRefine 记录
      if (saveStateFn && state) {
        state.lastRefine = new Date().toISOString();
        saveStateFn(state);
      }
      
      // 统计
      if (result.totalItems) {
        console.log(`📊 共提炼 ${result.totalItems} 条记忆`);
      } else {
        console.log(`📊 处理了 ${result.notesProcessed} 篇 Daily 笔记`);
      }
      
      return { success: true, ...result };
    }
    
    return writeResult;
  }
  
  return result;
}

/**
 * 生成 MEMORY.md 内容（兼容测试）
 */
function generateMemoryContent(refinedMemories) {
  const MEMORY_CATEGORIES = {
    USER_PREFERENCES: { key: 'userPreferences', title: '🎯 用户偏好' },
    DECISIONS: { key: 'decisions', title: '💡 重要决策' },
    PROJECTS: { key: 'projects', title: '📈 项目进展' },
    TODOS: { key: 'todos', title: '📋 待办事项' },
    SKILLS: { key: 'skills', title: '🔧 技能配置' },
    LEARNINGS: { key: 'learnings', title: '📚 关键学习' }
  };
  
  let content = `# MEMORY.md - 长期记忆\n\n`;
  content += `_最后更新：${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}_\n\n`;
  content += `> 此文件由 heartbeat-memory Skill 自动维护，记录重要的长期记忆。\n\n`;
  content += `---\n\n`;
  
  for (const category of Object.values(MEMORY_CATEGORIES)) {
    const items = refinedMemories[category.key] || [];
    
    content += `## ${category.title}\n\n`;
    
    if (items.length === 0) {
      content += `_暂无内容_\n\n`;
    } else {
      for (const item of items) {
        content += `- ${item.content} _(${item.source})_\n`;
      }
      content += '\n';
    }
    
    content += `---\n\n`;
  }
  
  return content;
}

/**
 * 展示层：状态转 emoji
 */
function statusEmoji(status) {
  return { active: '✅', deleted: '❌', reset: '🔄' }[status] || '✅';
}

module.exports = {
  readAllDailyNotes,
  refineMemoryWithLLM,
  refineMemoryWithRules,
  generateMemoryContent,
  writeMemoryFile,
  shouldRefine,
  refineMemory,
  // 新增功能
  detectActiveSessions,
  getIncrementalMessages,
  generateIncrementalSummary,
  updateDailyNoteForActiveSessions,
  buildIncrementalSummarizeTask,
  parseIncrementalLLMResult,
  statusEmoji
};
