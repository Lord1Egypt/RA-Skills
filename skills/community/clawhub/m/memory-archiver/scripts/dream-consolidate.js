#!/usr/bin/env node
/**
 * Dream Consolidation - 记忆巩固脚本（原 auto-dream 合并）
 * 定期整理、合并、去重、老化记忆
 * 
 * 用法:
 *   node dream-consolidate.js            # 检查闸门条件，通过后执行巩固
 *   node dream-consolidate.js --force    # 强制执行巩固
 *   node dream-consolidate.js --status   # 查看巩固状态
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const WORKSPACE = process.env.HOME + '/.openclaw/workspace';
const MEMORY_DIR = WORKSPACE + '/memory';
const AUTO_DIR = MEMORY_DIR + '/auto';
const STATE_FILE = MEMORY_DIR + '/.dream-state.json';
const LOCK_FILE = MEMORY_DIR + '/.dream.lock';
const MEMORY_INDEX = WORKSPACE + '/MEMORY.md';
const MEMORY_DEDUP = path.join(__dirname, 'memory-dedup.js');
const MEMORY_AGING = path.join(__dirname, 'memory-aging.js');

const MEMORY_TYPES = ['user', 'feedback', 'project', 'reference'];

// 闸门配置
const CONFIG = {
  minHours: 24,        // 最小时间间隔（小时）
  minSessions: 5,      // 最小新会话数
  maxAge: 30,          // 记忆老化天数
  maxPerType: 50,      // 每类型最大记忆数
};

// 读取巩固状态
function readState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  } catch (e) {
    return {
      lastConsolidatedAt: null,
      lastSessionCount: 0,
      totalConsolidations: 0
    };
  }
}

// 保存巩固状态
function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

// 获取会话数（通过会话文件数估算）
function getSessionCount() {
  const sessionsDir = MEMORY_DIR + '/sessions';
  if (!fs.existsSync(sessionsDir)) return 0;
  return fs.readdirSync(sessionsDir).filter(f => f.endsWith('.md')).length;
}

// 使用 Shell 锁脚本（支持 PID 复用保护 + mtime 防并发）
const LOCK_SCRIPT = path.join(__dirname, 'dream-lock.js');

function tryLock() {
  try {
    const result = execSync(`bash "${LOCK_SCRIPT}" "${MEMORY_DIR}" acquire`, {
      encoding: 'utf8',
      timeout: 5000
    }).trim();
    console.log(`[锁] ${result}`);
    return result.startsWith('ACQUIRED') || result.startsWith('FORCED');
  } catch (e) {
    console.log(`[锁] 获取失败: ${e.stdout?.trim() || e.message}`);
    return false;
  }
}

function releaseLock() {
  try {
    const result = execSync(`bash "${LOCK_SCRIPT}" "${MEMORY_DIR}" release`, {
      encoding: 'utf8',
      timeout: 5000
    }).trim();
    console.log(`[锁] ${result}`);
  } catch (e) {
    console.log(`[锁] 释放异常: ${e.message}`);
  }
}

function checkLock() {
  try {
    const result = execSync(`bash "${LOCK_SCRIPT}" "${MEMORY_DIR}" check`, {
      encoding: 'utf8',
      timeout: 5000
    }).trim();
    return result.startsWith('FREE');
  } catch (e) {
    return false;
  }
}

// 检查闸门条件
function checkGates() {
  const state = readState();
  const now = Date.now();
  
  // 时间闸门
  if (state.lastConsolidatedAt) {
    const hoursSince = (now - state.lastConsolidatedAt) / (1000 * 60 * 60);
    if (hoursSince < CONFIG.minHours) {
      console.log(`[闸门] 时间未达：${hoursSince.toFixed(1)}h < ${CONFIG.minHours}h`);
      return false;
    }
    console.log(`[闸门] 时间通过：${hoursSince.toFixed(1)}h ≥ ${CONFIG.minHours}h`);
  } else {
    console.log('[闸门] 时间通过：首次巩固');
  }
  
  // 会话闸门
  const sessionCount = getSessionCount();
  const newSessions = sessionCount - state.lastSessionCount;
  if (newSessions < CONFIG.minSessions && state.lastConsolidatedAt) {
    console.log(`[闸门] 会话未达：${newSessions} < ${CONFIG.minSessions}`);
    return false;
  }
  console.log(`[闸门] 会话通过：${newSessions} ≥ ${CONFIG.minSessions}`);
  
  return true;
}

// 老化检查
function ageCheck() {
  const now = Date.now();
  const agedFiles = [];
  
  for (const type of MEMORY_TYPES) {
    const dir = path.join(AUTO_DIR, type);
    if (!fs.existsSync(dir)) continue;
    
    const files = fs.readdirSync(dir).filter(f => f.endsWith('.md') && !f.startsWith('.'));
    
    for (const file of files) {
      const filepath = path.join(dir, file);
      const stat = fs.statSync(filepath);
      const ageDays = (now - stat.mtimeMs) / (1000 * 60 * 60 * 24);
      
      if (ageDays > CONFIG.maxAge) {
        agedFiles.push({ type, file, ageDays, filepath });
      }
    }
  }
  
  return agedFiles;
}

// 数量限制检查
function countCheck() {
  const excessFiles = [];
  
  for (const type of MEMORY_TYPES) {
    const dir = path.join(AUTO_DIR, type);
    if (!fs.existsSync(dir)) continue;
    
    const files = fs.readdirSync(dir).filter(f => f.endsWith('.md') && !f.startsWith('.'));
    
    if (files.length > CONFIG.maxPerType) {
      // 按修改时间排序，删除最旧的
      const sorted = files
        .map(f => ({ file: f, mtime: fs.statSync(path.join(dir, f)).mtimeMs }))
        .sort((a, b) => a.mtime - b.mtime);
      
      for (const item of sorted.slice(0, files.length - CONFIG.maxPerType)) {
        excessFiles.push({ type, file: item.file, filepath: path.join(dir, item.file) });
      }
    }
  }
  
  return excessFiles;
}

// 执行巩固
function consolidate() {
  console.log('\n=== 开始记忆巩固 ===\n');
  
  const report = {
    timestamp: new Date().toISOString(),
    aged: [],
    excess: [],
    cleaned: [],
    indexUpdated: false
  };
  
  // 1. 老化检查
  console.log('[1/3] 老化检查...');
  const aged = ageCheck();
  if (aged.length > 0) {
    console.log(`  发现 ${aged.length} 条过期记忆（>${CONFIG.maxAge}天）`);
    for (const item of aged) {
      console.log(`  标记: ${item.type}/${item.file} (${item.ageDays.toFixed(0)}天)`);
    }
    report.aged = aged;
  } else {
    console.log('  无过期记忆');
  }
  
  // 2. 数量限制
  console.log('[2/3] 数量限制检查...');
  const excess = countCheck();
  if (excess.length > 0) {
    console.log(`  发现 ${excess.length} 条超出限制的记忆`);
    for (const item of excess) {
      console.log(`  清理: ${item.type}/${item.file}`);
      // 不直接删除，移动到 archive
      const archiveDir = path.join(AUTO_DIR, '.archive', item.type);
      fs.mkdirSync(archiveDir, { recursive: true });
      fs.renameSync(item.filepath, path.join(archiveDir, item.file));
      report.cleaned.push(item);
    }
  } else {
    console.log('  未超出限制');
  }
  report.excess = excess;
  
  // 3. 更新索引
  console.log('[3/3] 更新索引...');
  updateIndex();
  report.indexUpdated = true;
  
  // 4. 调用 memory-archiver 去重（合并功能）
  console.log('[4/4] 记忆去重...');
  try {
    if (fs.existsSync(MEMORY_DEDUP)) {
      const dedupOutput = execSync(`bash "${MEMORY_DEDUP}"`, {
        encoding: 'utf8',
        timeout: 30000
      }).trim();
      console.log(`  ${dedupOutput.split('\n').slice(-1).join('')}`);
      report.dedupDone = true;
    } else {
      console.log('  跳过: memory-dedup.js 不存在');
      report.dedupDone = false;
    }
  } catch (e) {
    console.log(`  去重异常: ${e.message}`);
    report.dedupDone = false;
  }
  
  // 保存状态
  const state = readState();
  state.lastConsolidatedAt = Date.now();
  state.lastSessionCount = getSessionCount();
  state.totalConsolidations = (state.totalConsolidations || 0) + 1;
  saveState(state);
  
  console.log('\n=== 巩固完成 ===');
  console.log(`  老化: ${aged.length} 条`);
  console.log(`  清理: ${report.cleaned.length} 条`);
  console.log(`  总巩固次数: ${state.totalConsolidations}`);
  
  return report;
}

// 更新索引（简化版）
function updateIndex() {
  if (!fs.existsSync(MEMORY_INDEX)) {
    fs.writeFileSync(MEMORY_INDEX, '# MEMORY.md - 长期记忆\n\n> 精选知识与模式\n\n---\n', 'utf8');
    return;
  }
  
  // 读取现有内容
  let content = fs.readFileSync(MEMORY_INDEX, 'utf8');
  
  // 查找并替换索引部分
  const marker = '## 记忆索引';
  let indexStart = content.indexOf(marker);
  
  if (indexStart === -1) {
    content += '\n## 记忆索引\n\n_由 Auto-Memory 自动维护_\n\n';
    indexStart = content.indexOf(marker);
  }
  
  // 重建索引
  const entries = [];
  for (const type of MEMORY_TYPES) {
    const dir = path.join(AUTO_DIR, type);
    if (!fs.existsSync(dir)) continue;
    
    const files = fs.readdirSync(dir).filter(f => f.endsWith('.md') && !f.startsWith('.'));
    if (files.length === 0) continue;
    
    entries.push(`### ${type}\n`);
    for (const file of files.slice(0, 10)) {
      const filepath = path.join(dir, file);
      const fileContent = fs.readFileSync(filepath, 'utf8');
      const titleMatch = fileContent.match(/^# (.+)$/m);
      const title = titleMatch ? titleMatch[1] : file;
      entries.push(`- ${title} \`memory/auto/${type}/${file}\``);
    }
    entries.push('');
  }
  
  const newIndex = entries.join('\n');
  const nextSection = content.indexOf('\n## ', indexStart + 1);
  const beforeIndex = content.substring(0, indexStart);
  const afterIndex = nextSection !== -1 ? content.substring(nextSection) : '';
  
  let newContent = beforeIndex + '## 记忆索引\n\n_由 Auto-Memory 自动维护_\n\n' + newIndex + afterIndex;
  
  // 大小限制
  const lines = newContent.split('\n');
  if (lines.length > 200) newContent = lines.slice(0, 200).join('\n');
  if (Buffer.byteLength(newContent, 'utf8') > 25000) {
    newContent = newContent.substring(0, 25000);
  }
  
  fs.writeFileSync(MEMORY_INDEX, newContent, 'utf8');
}

// 主函数
function main() {
  const args = process.argv.slice(2);
  
  if (args.includes('--status')) {
    const state = readState();
    const now = Date.now();
    const hoursSince = state.lastConsolidatedAt ? ((now - state.lastConsolidatedAt) / (1000 * 60 * 60)).toFixed(1) : '从未';
    const sessions = getSessionCount();
    const newSessions = state.lastConsolidatedAt ? sessions - state.lastSessionCount : sessions;
    
    console.log('=== 巩固状态 ===');
    console.log(`上次巩固: ${hoursSince}h 前`);
    console.log(`总会话数: ${sessions}`);
    console.log(`新会话数: ${newSessions} (阈值: ${CONFIG.minSessions})`);
    console.log(`总巩固次数: ${state.totalConsolidations || 0}`);
    console.log(`\n闸门状态:`);
    console.log(`  时间: ${parseFloat(hoursSince) >= CONFIG.minHours ? '✅ 通过' : '❌ 未达'}`);
    console.log(`  会话: ${newSessions >= CONFIG.minSessions ? '✅ 通过' : '❌ 未达'}`);
    return;
  }
  
  const force = args.includes('--force');
  
  if (force) {
    console.log('[强制] 跳过闸门检查');
    if (tryLock()) {
      try {
        consolidate();
      } finally {
        releaseLock();
      }
    }
    return;
  }
  
  // 正常模式：检查闸门
  if (checkGates()) {
    if (tryLock()) {
      try {
        consolidate();
      } finally {
        releaseLock();
      }
    }
  } else {
    console.log('\n[跳过] 闸门条件未满足');
  }
}

main();
