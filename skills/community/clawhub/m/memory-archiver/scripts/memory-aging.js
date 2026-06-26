#!/usr/bin/env node
/**
 * Memory Aging & Cleanup - 记忆老化检查与清理
 * 
 * 功能（从 auto-dream 合并而来）：
 * 1. 老化检查：标记超过 30 天的记忆文件
 * 2. 数量限制：每类型最多 50 条，超出清理最旧的
 * 3. 报告生成：输出清理统计
 * 
 * 用法:
 *   node memory-aging.js              # 检查并清理
 *   node memory-aging.js --dry-run    # 只报告不删除
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.HOME + '/.openclaw/workspace';
const AUTO_DIR = path.join(WORKSPACE, 'memory/auto');
const MEMORY_TYPES = ['user', 'feedback', 'project', 'reference'];

// 配置
const CONFIG = {
  maxAge: 30,          // 记忆老化天数
  maxPerType: 50,      // 每类型最大记忆数
};

// ============================================================================
// 老化检查
// ============================================================================

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

// ============================================================================
// 数量限制检查
// ============================================================================

function countCheck() {
  const excessFiles = [];

  for (const type of MEMORY_TYPES) {
    const dir = path.join(AUTO_DIR, type);
    if (!fs.existsSync(dir)) continue;

    const files = fs.readdirSync(dir).filter(f => f.endsWith('.md') && !f.startsWith('.'));

    if (files.length > CONFIG.maxPerType) {
      // 按修改时间排序，清理最旧的
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

// ============================================================================
// 执行清理
// ============================================================================

function cleanup(dryRun) {
  console.log('🔍 记忆老化与清理检查');
  console.log('═'.repeat(40));

  const aged = ageCheck();
  const excess = countCheck();

  if (aged.length === 0 && excess.length === 0) {
    console.log('✅ 所有记忆正常，无需清理');
    return { aged: 0, excess: 0, cleaned: 0 };
  }

  // 统计每类型数量
  console.log('\n📊 各类型记忆数量:');
  for (const type of MEMORY_TYPES) {
    const dir = path.join(AUTO_DIR, type);
    if (!fs.existsSync(dir)) {
      console.log(`  ${type}: 0`);
      continue;
    }
    const count = fs.readdirSync(dir).filter(f => f.endsWith('.md') && !f.startsWith('.')).length;
    const status = count > CONFIG.maxPerType ? '⚠️ 超出' : '✅';
    console.log(`  ${type}: ${count} ${status}`);
  }

  // 老化文件
  if (aged.length > 0) {
    console.log(`\n⏰ 老化文件 (${aged.length} 条，>${CONFIG.maxAge}天):`);
    for (const item of aged) {
      console.log(`  • ${item.type}/${item.file} (${item.ageDays.toFixed(0)}天)`);
    }
  }

  // 超出文件
  if (excess.length > 0) {
    console.log(`\n📦 超出限制文件 (${excess.length} 条):`);
    for (const item of excess) {
      console.log(`  • ${item.type}/${item.file}`);
    }
  }

  if (dryRun) {
    console.log('\n[DRY RUN] 未执行删除');
    return { aged: aged.length, excess: excess.length, cleaned: 0 };
  }

  // 执行删除
  let cleaned = 0;
  const allToDelete = [...aged, ...excess];
  const uniquePaths = new Set(allToDelete.map(f => f.filepath));

  for (const filepath of uniquePaths) {
    try {
      fs.unlinkSync(filepath);
      cleaned++;
    } catch (e) {
      console.log(`  ❌ 删除失败: ${filepath} - ${e.message}`);
    }
  }

  console.log(`\n✅ 已清理 ${cleaned} 个文件`);
  return { aged: aged.length, excess: excess.length, cleaned };
}

// ============================================================================
// 主入口
// ============================================================================

function main() {
  const dryRun = process.argv.includes('--dry-run');
  const result = cleanup(dryRun);

  // 静默模式：无问题时不输出
  if (result.aged === 0 && result.excess === 0) {
    console.log('NO_REPLY');
  }
}

main();
