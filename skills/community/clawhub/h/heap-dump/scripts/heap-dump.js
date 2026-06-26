#!/usr/bin/env node
/**
 * Heap Dump — 内存快照 + 诊断
 * 基于 Claude Code heapDumpService.ts，适配 OpenClaw
 * 
 * 用法:
 *   node heap-dump.js              # 生成快照 + 诊断
 *   node heap-dump.js --snapshot   # 仅快照
 *   node heap-dump.js --stats      # 当前内存统计
 */

const v8 = require('v8');
const fs = require('fs');
const path = require('path');
const { pipeline } = require('stream/promises');

const SNAPSHOTS_DIR = process.env.HOME + '/.openclaw/heap-snapshots/';
const MAX_SNAPSHOTS = 10;

// 确保目录存在
fs.mkdirSync(SNAPSHOTS_DIR, { recursive: true });

/**
 * 清理旧快照（保留最新的 MAX_SNAPSHOTS 个）
 */
function cleanupOldSnapshots() {
  try {
    const files = fs.readdirSync(SNAPSHOTS_DIR)
      .filter(f => f.endsWith('.heapsnapshot') || f.endsWith('-diagnostics.json'))
      .map(f => ({ name: f, mtime: fs.statSync(path.join(SNAPSHOTS_DIR, f)).mtimeMs }))
      .sort((a, b) => b.mtime - a.mtime);
    
    while (files.length > MAX_SNAPSHOTS * 2) {
      const old = files.pop();
      fs.unlinkSync(path.join(SNAPSHOTS_DIR, old.name));
    }
  } catch (e) {
    console.log('[清理] 跳过:', e.message);
  }
}

/**
 * 获取内存诊断信息
 */
function getMemoryDiagnostics() {
  const usage = process.memoryUsage();
  const heapStats = v8.getHeapStatistics();
  
  // 活跃句柄数（Node.js 内部 API）
  let activeHandles = 0;
  let activeRequests = 0;
  try {
    activeHandles = process._getActiveHandles().length;
    activeRequests = process._getActiveRequests().length;
  } catch (e) {
    // 内部 API 可能在某些版本不可用
  }
  
  // 打开的文件描述符（仅 Linux）
  let openFileDescriptors;
  try {
    openFileDescriptors = fs.readdirSync('/proc/self/fd').length;
  } catch (e) {
    // 非 Linux 或无权限
  }
  
  // 内存增长率
  const uptimeSeconds = process.uptime();
  const bytesPerSecond = uptimeSeconds > 0 ? usage.rss / uptimeSeconds : 0;
  const mbPerHour = (bytesPerSecond * 3600) / (1024 * 1024);
  
  // 潜在泄漏检测
  const potentialLeaks = [];
  if (heapStats.number_of_detached_contexts > 0) {
    potentialLeaks.push(`${heapStats.number_of_detached_contexts} 个分离的上下文 — 可能的 iframe/上下文泄漏`);
  }
  if (activeHandles > 100) {
    potentialLeaks.push(`${activeHandles} 个活跃句柄 — 可能的定时器/socket 泄漏`);
  }
  if (usage.rss - usage.heapUsed > usage.heapUsed) {
    potentialLeaks.push('原生内存 > 堆内存 — 泄漏可能在原生插件中 (node-pty, sharp 等)');
  }
  if (mbPerHour > 100) {
    potentialLeaks.push(`高内存增长率: ${mbPerHour.toFixed(1)} MB/h`);
  }
  if (openFileDescriptors && openFileDescriptors > 500) {
    potentialLeaks.push(`${openFileDescriptors} 个打开的文件描述符 — 可能的文件/socket 泄漏`);
  }
  
  // V8 堆空间统计
  let heapSpaces;
  try {
    heapSpaces = v8.getHeapSpaceStatistics().map(space => ({
      name: space.space_name,
      size: space.space_size,
      used: space.space_used_size,
      available: space.space_available_size,
    }));
  } catch (e) {
    // 某些运行时不支持
  }
  
  return {
    timestamp: new Date().toISOString(),
    uptime: formatUptime(uptimeSeconds),
    nodeVersion: process.version,
    memoryUsage: {
      heapUsed: formatBytes(usage.heapUsed),
      heapTotal: formatBytes(usage.heapTotal),
      external: formatBytes(usage.external),
      arrayBuffers: formatBytes(usage.arrayBuffers),
      rss: formatBytes(usage.rss),
    },
    memoryGrowthRate: {
      bytesPerSecond: Math.round(bytesPerSecond),
      mbPerHour: mbPerHour.toFixed(1),
    },
    v8HeapStats: {
      heapSizeLimit: formatBytes(heapStats.heap_size_limit),
      mallocedMemory: formatBytes(heapStats.malloced_memory),
      peakMallocedMemory: formatBytes(heapStats.peak_malloced_memory),
      detachedContexts: heapStats.number_of_detached_contexts,
      nativeContexts: heapStats.number_of_native_contexts,
    },
    v8HeapSpaces: heapSpaces,
    activeHandles,
    activeRequests,
    openFileDescriptors,
    potentialLeaks,
    recommendation: potentialLeaks.length > 0
      ? `⚠️ 发现 ${potentialLeaks.length} 个潜在泄漏指标。查看 potentialLeaks 数组。`
      : '✅ 未发现明显泄漏指标。检查堆快照了解保留对象。',
  };
}

/**
 * 写入堆快照
 */
async function writeHeapSnapshot(filepath) {
  const writeStream = fs.createWriteStream(filepath, { mode: 0o600 });
  const heapSnapshotStream = v8.getHeapSnapshot();
  await pipeline(heapSnapshotStream, writeStream);
}

/**
 * 格式化字节
 */
function formatBytes(bytes) {
  if (bytes >= 1024 * 1024 * 1024) return (bytes / (1024 * 1024 * 1024)).toFixed(2) + ' GB';
  if (bytes >= 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  if (bytes >= 1024) return (bytes / 1024).toFixed(2) + ' KB';
  return bytes + ' B';
}

/**
 * 格式化运行时间
 */
function formatUptime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  return `${h}h ${m}m ${s}s`;
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  
  // 仅统计
  if (args.includes('--stats')) {
    const diag = getMemoryDiagnostics();
    console.log('=== 内存统计 ===\n');
    console.log(`运行时间: ${diag.uptime}`);
    console.log(`Node 版本: ${diag.nodeVersion}\n`);
    console.log('内存使用:');
    console.log(`  堆使用: ${diag.memoryUsage.heapUsed}`);
    console.log(`  堆总计: ${diag.memoryUsage.heapTotal}`);
    console.log(`  外部:   ${diag.memoryUsage.external}`);
    console.log(`  数组缓冲: ${diag.memoryUsage.arrayBuffers}`);
    console.log(`  RSS:    ${diag.memoryUsage.rss}`);
    console.log(`\n增长率: ${diag.memoryGrowthRate.mbPerHour} MB/h`);
    console.log(`\nV8 堆统计:`);
    console.log(`  堆大小限制: ${diag.v8HeapStats.heapSizeLimit}`);
    console.log(`  分配内存: ${diag.v8HeapStats.mallocedMemory}`);
    console.log(`  峰值分配: ${diag.v8HeapStats.peakMallocedMemory}`);
    console.log(`  分离上下文: ${diag.v8HeapStats.detachedContexts}`);
    console.log(`\n句柄: ${diag.activeHandles}`);
    console.log(`请求: ${diag.activeRequests}`);
    if (diag.openFileDescriptors) console.log(`文件描述符: ${diag.openFileDescriptors}`);
    if (diag.potentialLeaks.length > 0) {
      console.log(`\n⚠️ 潜在泄漏:`);
      diag.potentialLeaks.forEach(l => console.log(`  - ${l}`));
    }
    console.log(`\n${diag.recommendation}`);
    return;
  }
  
  // 生成快照
  console.log('📸 生成堆快照...\n');
  
  const diag = getMemoryDiagnostics();
  const timestamp = Date.now();
  const diagPath = path.join(SNAPSHOTS_DIR, `${timestamp}-diagnostics.json`);
  const snapshotPath = path.join(SNAPSHOTS_DIR, `${timestamp}.heapsnapshot`);
  
  // 先写诊断（快照可能失败）
  fs.writeFileSync(diagPath, JSON.stringify(diag, null, 2), { mode: 0o600 });
  console.log(`[诊断] ${diagPath}`);
  console.log(`  堆使用: ${diag.memoryUsage.heapUsed}`);
  console.log(`  RSS:    ${diag.memoryUsage.rss}\n`);
  
  try {
    await writeHeapSnapshot(snapshotPath);
    console.log(`[快照] ${snapshotPath}`);
    console.log(`\n✅ 完成。在 Chrome DevTools > Memory 中加载 .heapsnapshot 文件分析。`);
  } catch (err) {
    console.log(`\n❌ 快照失败: ${err.message}`);
    console.log('诊断文件已保存，可单独查看。');
  }
  
  // 清理旧快照
  cleanupOldSnapshots();
}

main().catch(err => {
  console.error('错误:', err.message);
  process.exit(1);
});
