/**
 * FrozenMemory - P0-2 Frozen记忆
 * 
 * 核心概念：
 * 记忆编辑仅下次会话生效，避免上下文抖动
 * 
 * 实现：
 * 1. 当前会话读取 "frozen" 版本的记忆
 * 2. 编辑操作写入 "staging" 区域（待生效）
 * 3. 下次会话启动时，staging → frozen（合并生效）
 * 4. 当前会话继续使用 frozen，不受编辑影响
 */

const fs = require('fs');
const path = require('path');

const MEMORY_DIR = path.join(__dirname, '..', 'memory');
const FROZEN_DIR = path.join(MEMORY_DIR, '.frozen');
const STAGING_DIR = path.join(MEMORY_DIR, '.staging');

/**
 * 确保目录存在
 */
function init() {
  if (!fs.existsSync(MEMORY_DIR)) {
    fs.mkdirSync(MEMORY_DIR, { recursive: true });
  }
  if (!fs.existsSync(FROZEN_DIR)) {
    fs.mkdirSync(FROZEN_DIR, { recursive: true });
  }
  if (!fs.existsSync(STAGING_DIR)) {
    fs.mkdirSync(STAGING_DIR, { recursive: true });
  }
}

/**
 * 获取冻结的记忆文件名
 */
function getFrozenPath(dateStr) {
  return path.join(FROZEN_DIR, `${dateStr}.md`);
}

/**
 * 获取待生效的记忆文件名
 */
function getStagingPath(dateStr) {
  return path.join(STAGING_DIR, `${dateStr}.md`);
}

/**
 * 获取常规记忆文件
 */
function getMemoryPath(dateStr) {
  return path.join(MEMORY_DIR, `${dateStr}.md`);
}

/**
 * 检查是否是 frozen 版本
 */
function isFrozen(dateStr) {
  const frozenPath = getFrozenPath(dateStr);
  return fs.existsSync(frozenPath);
}

/**
 * 读取记忆（优先 frozen，仅下次会话生效）
 */
function readMemory(dateStr) {
  init();
  
  // 如果有 frozen 版本，读取 frozen
  const frozenPath = getFrozenPath(dateStr);
  if (fs.existsSync(frozenPath)) {
    return {
      content: fs.readFileSync(frozenPath, 'utf-8'),
      source: 'frozen',
      date: dateStr
    };
  }
  
  // 否则读取常规记忆
  const memoryPath = getMemoryPath(dateStr);
  if (fs.existsSync(memoryPath)) {
    return {
      content: fs.readFileSync(memoryPath, 'utf-8'),
      source: 'memory',
      date: dateStr
    };
  }
  
  return { content: '', source: 'none', date: dateStr };
}

/**
 * 读取所有相关记忆（用于会话初始化）
 */
function readAllMemoryForSession() {
  init();
  
  const memories = [];
  
  // 1. 读取 frozen 记忆（优先级最高）
  if (fs.existsSync(FROZEN_DIR)) {
    const frozenFiles = fs.readdirSync(FROZEN_DIR).filter(f => f.endsWith('.md'));
    for (const file of frozenFiles.sort()) {
      const dateStr = file.replace('.md', '');
      const content = fs.readFileSync(path.join(FROZEN_DIR, file), 'utf-8');
      memories.push({ date: dateStr, content, source: 'frozen' });
    }
  }
  
  // 2. 读取 staging 记忆（标记为 pending）
  if (fs.existsSync(STAGING_DIR)) {
    const stagingFiles = fs.readdirSync(STAGING_DIR).filter(f => f.endsWith('.md'));
    for (const file of stagingFiles.sort()) {
      const dateStr = file.replace('.md', '');
      // 检查是否已经在 frozen 中
      if (!isFrozen(dateStr)) {
        const content = fs.readFileSync(path.join(STAGING_DIR, file), 'utf-8');
        memories.push({ date: dateStr, content, source: 'staging', pending: true });
      }
    }
  }
  
  return memories;
}

/**
 * 写入编辑到 staging（不直接影响当前会话）
 */
function stageEdit(dateStr, newContent, description = '') {
  init();
  
  const stagingPath = getStagingPath(dateStr);
  const oldContent = fs.existsSync(stagingPath) 
    ? fs.readFileSync(stagingPath, 'utf-8')
    : '';
  
  // 写入 staging
  fs.writeFileSync(stagingPath, newContent, 'utf-8');
  
  // 记录变更日志
  const logPath = path.join(STAGING_DIR, '.change-log.json');
  let log = [];
  if (fs.existsSync(logPath)) {
    try {
      log = JSON.parse(fs.readFileSync(logPath, 'utf-8'));
    } catch (e) {}
  }
  
  log.push({
    timestamp: new Date().toISOString(),
    date: dateStr,
    description: description || '记忆编辑',
    length: newContent.length
  });
  
  fs.writeFileSync(logPath, JSON.stringify(log, null, 2), 'utf-8');
  
  console.log(`[FrozenMemory] 📝 编辑已存入 staging: ${dateStr}`);
  console.log(`   说明: ${description || '无'}`);
  console.log(`   状态: 下次会话生效`);
  
  return { date: dateStr, source: 'staging', pending: true };
}

/**
 * 冻结记忆（下次会话时合并 staging → frozen）
 */
function freezeMemory(dateStr) {
  init();
  
  const stagingPath = getStagingPath(dateStr);
  const frozenPath = getFrozenPath(dateStr);
  
  // staging → frozen
  if (fs.existsSync(stagingPath)) {
    fs.renameSync(stagingPath, frozenPath);
    console.log(`[FrozenMemory] ❄️ 记忆已冻结: ${dateStr}`);
    return { date: dateStr, source: 'frozen' };
  }
  
  // 如果没有 staging，但有常规记忆，也冻结一份
  const memoryPath = getMemoryPath(dateStr);
  if (fs.existsSync(memoryPath)) {
    fs.copyFileSync(memoryPath, frozenPath);
    console.log(`[FrozenMemory] ❄️ 记忆已冻结(副本): ${dateStr}`);
    return { date: dateStr, source: 'frozen' };
  }
  
  return null;
}

/**
 * 合并 staging 到 frozen（启动时调用）
 */
function applyPendingChanges() {
  init();
  
  if (!fs.existsSync(STAGING_DIR)) return { applied: 0 };
  
  const stagingFiles = fs.readdirSync(STAGING_DIR).filter(f => f.endsWith('.md'));
  let applied = 0;
  
  for (const file of stagingFiles) {
    const dateStr = file.replace('.md', '');
    freezeMemory(dateStr);
    applied++;
  }
  
  console.log(`[FrozenMemory] ✅ 已合并 ${applied} 个待生效记忆`);
  return { applied };
}

/**
 * 获取当前冻结状态
 */
function getFrozenStatus() {
  init();
  
  const status = {
    frozen: [],
    staging: [],
    memory: []
  };
  
  // frozen 文件
  if (fs.existsSync(FROZEN_DIR)) {
    status.frozen = fs.readdirSync(FROZEN_DIR)
      .filter(f => f.endsWith('.md'))
      .map(f => f.replace('.md', ''));
  }
  
  // staging 文件
  if (fs.existsSync(STAGING_DIR)) {
    status.staging = fs.readdirSync(STAGING_DIR)
      .filter(f => f.endsWith('.md'))
      .map(f => f.replace('.md', ''));
  }
  
  // 常规 memory 文件
  if (fs.existsSync(MEMORY_DIR)) {
    status.memory = fs.readdirSync(MEMORY_DIR)
      .filter(f => f.endsWith('.md'))
      .map(f => f.replace('.md', ''));
  }
  
  return status;
}

/**
 * 清除 staging（放弃未生效的编辑）
 */
function clearStaging(dateStr = null) {
  init();
  
  if (dateStr) {
    // 清除指定日期
    const stagingPath = getStagingPath(dateStr);
    if (fs.existsSync(stagingPath)) {
      fs.unlinkSync(stagingPath);
      console.log(`[FrozenMemory] 🗑️ 已清除 staging: ${dateStr}`);
    }
  } else {
    // 清除所有 staging
    const files = fs.readdirSync(STAGING_DIR).filter(f => f.endsWith('.md'));
    for (const file of files) {
      fs.unlinkSync(path.join(STAGING_DIR, file));
    }
    console.log(`[FrozenMemory] 🗑️ 已清除所有 staging`);
  }
}

// 导出
module.exports = {
  readMemory,
  readAllMemoryForSession,
  stageEdit,
  freezeMemory,
  applyPendingChanges,
  getFrozenStatus,
  clearStaging,
  FROZEN_DIR,
  STAGING_DIR
};
