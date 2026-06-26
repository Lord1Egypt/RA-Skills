/**
 * 工作流归档与清理器 (Workflow Archiver & Cleaner)
 *
 * 职责：
 * 1. 工作流完成后，将所有产出物归档到 archive/{workflow_id}/
 * 2. 生成归档索引（摘要 + 文件清单 + 执行统计）
 * 3. 清理 shared/ 临时目录（为下一轮工作流做准备）
 * 4. 生成最终执行摘要（替代散落的子代理消息）
 *
 * 归档结构：
 * archive/{workflow_id}/
 * ├── index.json          # 归档元数据（工作流信息、执行统计、文件清单）
 * ├── summary.md          # 可读的执行摘要（Markdown）
 * ├── reports/            # 各子代理产出报告
 * │   ├── Research_Analyst_report.md
 * │   ├── Technical_Specialist_report.md
 * │   ├── Strategy_Analyst_report.md
 * │   └── Critic_report.md
 * ├── final/              # 最终交付物
 * │   ├── AGGREGATED_REPORT.md
 * │   └── FINAL_REPORT.md
 * ├── dashboard.json      # 任务看板快照
 * ├── execution_plan.json # 执行计划
 * └── logs/               # 进度文件等
 */

import fs from 'fs';
import path from 'path';

const CONFIG_DIR = path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'workspace');
const ARCHIVE_DIR = path.join(CONFIG_DIR, 'archive');

// ===================== 核心函数 =====================

/**
 * 归档工作流所有产出物
 *
 * @param {object} workflow - 工作流实例
 * @param {object} options - 可选参数
 * @param {string} options.goal - 工作流目标（覆盖 workflow.goal）
 * @param {object} options.stats - 执行统计（覆盖自动检测）
 * @returns {object} { archivePath, summary, fileCount, totalSize }
 */
export function archiveWorkflow(workflow, options = {}) {
  const wfId = workflow.id || `wf_${Date.now()}`;
  const archivePath = path.join(ARCHIVE_DIR, wfId);

  // 创建归档目录结构
  const dirs = ['reports', 'final', 'logs'].map(d => path.join(archivePath, d));
  for (const d of dirs) fs.mkdirSync(d, { recursive: true });

  const sharedDir = path.join(CONFIG_DIR, 'shared');
  const sharedFinal = path.join(sharedDir, 'final');
  const sharedProgress = path.join(sharedDir, 'progress');

  const fileManifest = [];
  let totalSize = 0;

  // 1. 归档子代理报告
  // 1. 归档所有子代理报告（扫描 *_report.md，不限定代理名）
  if (fs.existsSync(sharedFinal)) {
    const reportFiles = fs.readdirSync(sharedFinal).filter(f => f.endsWith('_report.md'));
    for (const f of reportFiles) {
      copyFile(
        path.join(sharedFinal, f),
        path.join(archivePath, 'reports', f),
        fileManifest
      );
    }
  }

  // 1b. 归档子代理独立工作区文件
  const agentsDir = path.join(CONFIG_DIR, 'agents');
  if (fs.existsSync(agentsDir)) {
    const agentDirs = fs.readdirSync(agentsDir, { withFileTypes: true }).filter(e => e.isDirectory());
    for (const agentDir of agentDirs) {
      const srcDir = path.join(agentsDir, agentDir.name);
      const destDir = path.join(archivePath, 'agents', agentDir.name);
      fs.mkdirSync(destDir, { recursive: true });
      const files = fs.readdirSync(srcDir).filter(f => !f.startsWith('.'));
      for (const f of files) {
        const src = path.join(srcDir, f);
        if (fs.statSync(src).isFile()) {
          copyFile(src, path.join(destDir, f), fileManifest);
        }
      }
    }
  }

  // 2. 归档最终交付物（扫描已知文件名 + 其他非报告文件）
  if (fs.existsSync(sharedFinal)) {
    const allFiles = fs.readdirSync(sharedFinal);
    for (const f of allFiles) {
      if (f.endsWith('_report.md')) continue;  // 已在上面归档
      const src = path.join(sharedFinal, f);
      if (fs.statSync(src).isFile()) {
        const dest = path.join(archivePath, 'final', f);
        copyFile(src, dest, fileManifest);
      }
    }
  }

  // 3. 归档执行计划
  const planSrc = path.join(sharedDir, 'execution_plan.json');
  if (fs.existsSync(planSrc)) {
    copyFile(planSrc, path.join(archivePath, 'execution_plan.json'), fileManifest);
  }

  // 4. 归档看板快照
  const dashSrc = path.join(sharedDir, 'dashboard.json');
  if (fs.existsSync(dashSrc)) {
    copyFile(dashSrc, path.join(archivePath, 'dashboard.json'), fileManifest);
  }

  // 5. 归档进度文件
  if (fs.existsSync(sharedProgress)) {
    const progressFiles = fs.readdirSync(sharedProgress).filter(f => f.endsWith('.json'));
    for (const f of progressFiles) {
      copyFile(
        path.join(sharedProgress, f),
        path.join(archivePath, 'logs', f),
        fileManifest
      );
    }
  }

  // 6. 统计
  totalSize = fileManifest.reduce((sum, f) => sum + f.size, 0);

  // 7. 生成归档索引
  const reportCount = fileManifest.filter(f => f.category === 'reports').length;
  const finalCount = fileManifest.filter(f => f.category === 'final').length;

  const index = {
    workflow_id: wfId,
    goal: options.goal || workflow.goal || '未指定',
    template: workflow.template || 'unknown',
    archived_at: new Date().toISOString(),
    stats: options.stats || {
      agents_spawned: reportCount,
      reports_produced: reportCount,
      final_artifacts: finalCount,
      total_files: fileManifest.length,
      total_size_kb: Math.round(totalSize / 1024),
    },
    files: fileManifest,
  };

  fs.writeFileSync(
    path.join(archivePath, 'index.json'),
    JSON.stringify(index, null, 2),
    'utf-8'
  );

  // 8. 生成可读摘要
  const summary = generateSummary(index);
  fs.writeFileSync(path.join(archivePath, 'summary.md'), summary, 'utf-8');

  return {
    archivePath,
    summary,
    fileCount: fileManifest.length,
    totalSize
  };
}

/**
 * 清理 shared/ 临时目录
 * 保留目录结构，删除所有文件
 *
 * @param {object} options
 * @param {boolean} options.dryRun - 仅列出要删除的文件，不实际删除
 * @returns {object} { deleted: number, freed: number, files: string[] }
 */
export function cleanShared(options = {}) {
  const { dryRun = false } = options;
  const toDelete = [];
  let freed = 0;

  function walk(dir) {
    if (!fs.existsSync(dir)) return;
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(fullPath);
      } else {
        const size = fs.statSync(fullPath).size;
        toDelete.push({ path: fullPath, size });
        freed += size;
      }
    }
  }

  // 清理 shared/
  walk(path.join(CONFIG_DIR, 'shared'));


  if (!dryRun) {
    for (const f of toDelete) {
      try { fs.unlinkSync(f.path); } catch { /* 忽略 */ }
    }
  }

  return {
    deleted: toDelete.length,
    freed: Math.round(freed / 1024),
    files: toDelete.map(f => f.path.replace(CONFIG_DIR, '~')),
  };
}

/**
 * 生成最终执行摘要（替代散落的子代理消息）
 * 主代理可以在工作流完成后输出这段摘要
 *
 * @param {object} workflow - 工作流实例
 * @param {object} dashboard - 任务看板状态
 * @param {string} archivePath - 归档路径
 * @returns {string} 格式化摘要文本
 */
export function generateFinalSummary(workflow, dashboard, archivePath) {
  const goal = workflow?.goal || '未指定';
  const wfId = workflow?.id || 'unknown';
  const elapsed = dashboard?.started_at
    ? Math.round((Date.now() - new Date(dashboard.started_at).getTime()) / 1000)
    : 0;

  let output = '';
  output += `📋 工作流执行完毕\n`;
  output += `${'═'.repeat(50)}\n`;
  output += `📌 目标: ${goal}\n`;
  output += `🆔 工作流: ${wfId}\n`;
  output += `⏱️ 耗时: ${formatDuration(elapsed)}\n\n`;

  if (dashboard?.stats) {
    const s = dashboard.stats;
    output += `📊 执行统计:\n`;
    output += `   ✅ 完成: ${s.completed}/${s.total}\n`;
    if (s.failed > 0) output += `   ❌ 失败: ${s.failed}\n`;
    if (s.retried > 0) output += `   🔁 重试: ${s.retried}\n`;
  }

  // 各代理状态摘要
  if (dashboard?.agents) {
    output += `\n📋 代理执行结果:\n`;
    for (const [name, agent] of Object.entries(dashboard.agents)) {
      const icon = agent.output_exists ? '✅' : '❌';
      output += `   ${icon} ${name}: ${agent.model} → ${agent.output_exists ? '已完成' : '未产出'}\n`;
    }
  }

  output += `\n📁 归档位置: ${archivePath ? archivePath.replace(CONFIG_DIR, '~/.openclaw/workspace') : '未归档'}\n`;
  output += `💡 查看详细报告: archive/{workflow_id}/summary.md\n`;
  output += `${'═'.repeat(50)}\n`;

  return output;
}

/**
 * 一键归档 + 清理（主入口）
 *
 * @param {object} workflow - 工作流实例
 * @param {object} dashboard - 任务看板（可选）
 * @returns {object} { archiveResult, cleanResult, summary }
 */
export function archiveAndClean(workflow, dashboard = null) {
  // 1. 归档
  const archiveResult = archiveWorkflow(workflow);

  // 2. 清理
  const cleanResult = cleanShared();

  // 3. 生成摘要
  const summary = generateFinalSummary(workflow, dashboard, archiveResult.archivePath);

  return {
    archiveResult,
    cleanResult,
    summary
  };
}

// ===================== 辅助函数 =====================

function copyFile(src, dest, manifest) {
  try {
    const stat = fs.statSync(src);
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.copyFileSync(src, dest);

    // 确定分类
    let category = 'other';
    if (dest.includes(`${path.sep}reports${path.sep}`)) category = 'reports';
    else if (dest.includes(`${path.sep}final${path.sep}`)) category = 'final';
    else if (dest.includes(`${path.sep}logs${path.sep}`)) category = 'logs';

    manifest.push({
      file: dest.replace(ARCHIVE_DIR, '').replace(/^[\\/]/, ''),
      category,
      size: stat.size,
      modified: stat.mtime.toISOString()
    });
  } catch { /* 忽略复制失败 */ }
}

function generateSummary(index) {
  let md = `# 工作流归档摘要\n\n`;
  md += `- **工作流 ID**: ${index.workflow_id}\n`;
  md += `- **目标**: ${index.goal}\n`;
  md += `- **归档时间**: ${index.archived_at}\n`;
  md += `- **文件数**: ${index.stats.total_files}\n`;
  md += `- **总大小**: ${index.stats.total_size_kb} KB\n\n`;

  md += `## 文件清单\n\n`;
  md += `| 分类 | 文件 | 大小 |\n`;
  md += `|------|------|------|\n`;
  for (const f of index.files) {
    md += `| ${f.category} | ${f.file} | ${formatBytes(f.size)} |\n`;
  }

  return md;
}

function formatDuration(seconds) {
  if (seconds < 60) return `${seconds}s`;
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  if (mins < 60) return `${mins}m${secs}s`;
  const hours = Math.floor(mins / 60);
  return `${hours}h${mins % 60}m`;
}

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}

export { ARCHIVE_DIR, formatDuration, formatBytes };
