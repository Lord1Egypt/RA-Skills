#!/usr/bin/env node
/**
 * PRD 版本更新与迭代管理脚本
 *
 * 用法：
 *   标准升级：
 *     node update.js patch "修正错误"     # 1.0.0 → 1.0.1
 *     node update.js minor "新增内容"     # 1.0.0 → 1.1.0
 *     node update.js major "重构"         # 1.0.0 → 2.0.0
 *     node update.js build                # 仅增加build号
 *
 *   迭代模式（推荐）：
 *     node update.js iterate              # 进入交互式迭代向导
 *
 *   其他命令：
 *     node update.js history              # 查看变更历史
 *     node update.js diff [v1] [v2]       # 对比版本差异
 *     node update.js rollback [version]   # 回滚到指定版本
 *     node update.js suggest              # 获取版本升级建议
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const readline = require('readline');

// 变更类型定义
const CHANGE_TYPES = {
  feat: { label: '新增功能', emoji: '✨', version: 'minor' },
  update: { label: '功能更新', emoji: '🔄', version: 'minor' },
  fix: { label: '问题修复', emoji: '🐛', version: 'patch' },
  docs: { label: '文档优化', emoji: '📝', version: 'patch' },
  refactor: { label: '代码重构', emoji: '♻️', version: 'minor' },
  style: { label: '格式调整', emoji: '💄', version: 'patch' },
  test: { label: '测试相关', emoji: '✅', version: 'patch' }
};

// 创建readline接口
function createRL() {
  return readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
}

// 提问函数
function ask(rl, question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer.trim());
    });
  });
}

// 主函数
function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'build';

  switch (command) {
    case 'patch':
    case 'minor':
    case 'major':
    case 'build':
      standardUpdate(command, args[1]);
      break;
    case 'iterate':
      interactiveIterate();
      break;
    case 'history':
      showHistory();
      break;
    case 'diff':
      showDiff(args[1], args[2]);
      break;
    case 'rollback':
      rollback(args[1]);
      break;
    case 'suggest':
      suggestVersion();
      break;
    default:
      console.log('❌ 未知命令:', command);
      console.log('');
      console.log('用法：');
      console.log('  node update.js patch "修正错误"     # PATCH升级');
      console.log('  node update.js minor "新增内容"     # MINOR升级');
      console.log('  node update.js major "重构"         # MAJOR升级');
      console.log('  node update.js build                # 仅增加build号');
      console.log('  node update.js iterate              # 交互式迭代向导');
      console.log('  node update.js history              # 查看变更历史');
      console.log('  node update.js diff [v1] [v2]       # 对比版本差异');
      console.log('  node update.js rollback [version]   # 回滚到指定版本');
      console.log('  node update.js suggest              # 获取版本升级建议');
      process.exit(1);
  }
}

// 标准更新模式
function standardUpdate(bumpType, message) {
  const scriptDir = process.cwd();
  const versionFile = path.join(scriptDir, 'version.json');
  const changelogFile = path.join(scriptDir, 'CHANGELOG.md');
  const iterationFile = path.join(scriptDir, 'ITERATION.json');

  if (!fs.existsSync(versionFile)) {
    console.error('❌ 找不到版本文件 version.json');
    process.exit(1);
  }

  const versionData = JSON.parse(fs.readFileSync(versionFile, 'utf-8'));
  let currentVersion = versionData.version;
  let currentBuild = versionData.build || 0;

  // 解析版本号
  let [major, minor, patch] = currentVersion.split('.').map(Number);

  // 计算新版本
  switch (bumpType) {
    case 'major':
      major++;
      minor = 0;
      patch = 0;
      break;
    case 'minor':
      minor++;
      patch = 0;
      break;
    case 'patch':
      patch++;
      break;
  }

  const newVersion = `${major}.${minor}.${patch}`;
  const newBuild = currentBuild + 1;
  const today = new Date().toISOString().split('T')[0];

  console.log(`📦 版本更新: v${currentVersion} (build #${currentBuild}) → v${newVersion} (build #${newBuild})`);

  // 更新 version.json
  versionData.version = newVersion;
  versionData.build = newBuild;
  versionData.lastUpdate = today;
  fs.writeFileSync(versionFile, JSON.stringify(versionData, null, 2) + '\n');

  // 记录变更历史
  const changeRecord = {
    version: newVersion,
    build: newBuild,
    date: today,
    type: bumpType,
    message: message || '无描述',
    changes: []
  };

  // 更新或创建 ITERATION.json
  let iterationData = { history: [] };
  if (fs.existsSync(iterationFile)) {
    iterationData = JSON.parse(fs.readFileSync(iterationFile, 'utf-8'));
  }
  iterationData.history.unshift(changeRecord);
  fs.writeFileSync(iterationFile, JSON.stringify(iterationData, null, 2) + '\n');

  // 更新 CHANGELOG
  if (bumpType !== 'build' && message) {
    updateChangelog(changelogFile, newVersion, today, bumpType, message);
  }

  // 构建输出
  buildOutput(scriptDir);

  // 备份到 versions 目录
  if (bumpType !== 'build') {
    backupVersion(scriptDir, versionData.title, newVersion);
  }

  console.log('');
  console.log(`✅ 完成！v${newVersion} (build #${newBuild})`);
  console.log(`   HTML: output/${versionData.title}-v${newVersion}.html`);
  console.log(`   PDF:  output/${versionData.title}-v${newVersion}.pdf`);
}

// 交互式迭代向导
async function interactiveIterate() {
  const rl = createRL();
  const scriptDir = process.cwd();

  console.log('╔════════════════════════════════════════════════╗');
  console.log('║          🔄 PRD 迭代向导                        ║');
  console.log('╚════════════════════════════════════════════════╝');
  console.log('');

  try {
    // 1. 选择变更类型
    console.log('请选择变更类型：');
    Object.entries(CHANGE_TYPES).forEach(([key, value]) => {
      console.log(`  ${key.padEnd(10)} ${value.emoji} ${value.label} → ${value.version}版本`);
    });

    let changeType = await ask(rl, '\n请输入类型（feat/fix/docs等）：');
    while (!CHANGE_TYPES[changeType]) {
      console.log('❌ 无效的类型');
      changeType = await ask(rl, '请输入类型：');
    }

    // 2. 输入变更描述
    let changeDesc = await ask(rl, '\n请输入变更描述：');
    while (!changeDesc) {
      console.log('❌ 变更描述不能为空');
      changeDesc = await ask(rl, '请输入变更描述：');
    }

    // 3. 详细变更列表
    console.log('\n请输入详细变更（每行一条，空行结束）：');
    const changes = [];
    while (true) {
      const change = await ask(rl, `  变更 ${changes.length + 1}（回车结束）：`);
      if (!change) break;
      changes.push(change);
    }

    // 4. 确认版本升级
    const suggestedVersion = CHANGE_TYPES[changeType].version;
    console.log(`\n💡 建议升级为 ${suggestedVersion.toUpperCase()} 版本`);
    const confirmVersion = await ask(rl, `确认升级${suggestedVersion}版本？(y/n/其他类型)：`);

    let finalVersionType = suggestedVersion;
    if (confirmVersion.toLowerCase() === 'n') {
      rl.close();
      console.log('❌ 已取消');
      return;
    } else if (['major', 'minor', 'patch'].includes(confirmVersion)) {
      finalVersionType = confirmVersion;
    }

    rl.close();

    // 执行更新
    const fullMessage = `${CHANGE_TYPES[changeType].emoji} ${changeDesc}`;
    standardUpdate(finalVersionType, fullMessage);

    // 追加详细变更到迭代记录
    appendDetailedChanges(scriptDir, changes);

  } catch (error) {
    console.error('\n❌ 发生错误:', error.message);
    rl.close();
    process.exit(1);
  }
}

// 追加详细变更记录
function appendDetailedChanges(scriptDir, changes) {
  const iterationFile = path.join(scriptDir, 'ITERATION.json');
  if (!fs.existsSync(iterationFile) || changes.length === 0) return;

  const iterationData = JSON.parse(fs.readFileSync(iterationFile, 'utf-8'));
  if (iterationData.history && iterationData.history.length > 0) {
    iterationData.history[0].changes = changes;
    fs.writeFileSync(iterationFile, JSON.stringify(iterationData, null, 2) + '\n');
  }
}

// 更新 CHANGELOG
function updateChangelog(changelogFile, newVersion, today, type, message) {
  if (!fs.existsSync(changelogFile)) {
    fs.writeFileSync(changelogFile, '# 更新日志\n\n');
  }

  let content = fs.readFileSync(changelogFile, 'utf-8');

  const typeEmoji = {
    major: '🚀',
    minor: '✨',
    patch: '🐛',
    build: '🔨'
  };

  const entry = `\n## [${newVersion}] ${today} ${typeEmoji[type] || '📝'}\n\n- ${message}\n`;

  // 在第一个 ## 之前插入
  const firstEntryIndex = content.indexOf('\n## [');
  if (firstEntryIndex !== -1) {
    content = content.slice(0, firstEntryIndex) + entry + content.slice(firstEntryIndex);
  } else {
    content += entry;
  }

  fs.writeFileSync(changelogFile, content);
  console.log('📝 CHANGELOG 已更新');
}

// 构建输出
function buildOutput(scriptDir) {
  console.log('');
  console.log('🔨 构建 HTML...');
  try {
    execSync('node build.js', { stdio: 'inherit', cwd: scriptDir });
  } catch (e) {
    console.error('❌ HTML构建失败');
  }

  console.log('');
  console.log('📄 生成 PDF...');
  try {
    execSync('node build-pdf.js', { stdio: 'inherit', cwd: scriptDir });
  } catch (e) {
    console.error('❌ PDF生成失败');
  }
}

// 备份版本
function backupVersion(scriptDir, title, version) {
  const versionsDir = path.join(scriptDir, 'versions');
  if (!fs.existsSync(versionsDir)) {
    fs.mkdirSync(versionsDir, { recursive: true });
  }

  const sourcePdf = path.join(scriptDir, 'output', `${title}-v${version}.pdf`);
  const backupPdf = path.join(versionsDir, `${title}-v${version}.pdf`);

  if (fs.existsSync(sourcePdf)) {
    fs.copyFileSync(sourcePdf, backupPdf);
    console.log(`💾 备份: versions/${title}-v${version}.pdf`);
  }
}

// 显示变更历史
function showHistory() {
  const scriptDir = process.cwd();
  const iterationFile = path.join(scriptDir, 'ITERATION.json');

  if (!fs.existsSync(iterationFile)) {
    console.log('暂无变更历史');
    return;
  }

  const iterationData = JSON.parse(fs.readFileSync(iterationFile, 'utf-8'));

  console.log('');
  console.log('╔════════════════════════════════════════════════╗');
  console.log('║          📜 变更历史                            ║');
  console.log('╚════════════════════════════════════════════════╝');
  console.log('');

  iterationData.history.forEach((record, index) => {
    console.log(`${index + 1}. v${record.version} (build #${record.build}) - ${record.date}`);
    console.log(`   ${record.message}`);
    if (record.changes && record.changes.length > 0) {
      record.changes.forEach(change => {
        console.log(`   • ${change}`);
      });
    }
    console.log('');
  });
}

// 显示版本差异
function showDiff(v1, v2) {
  const scriptDir = process.cwd();
  const versionsDir = path.join(scriptDir, 'versions');

  if (!v1 || !v2) {
    // 获取最近的两个版本
    if (!fs.existsSync(versionsDir)) {
      console.log('❌ 没有找到versions目录');
      return;
    }

    const versions = fs.readdirSync(versionsDir)
      .filter(f => f.endsWith('.pdf'))
      .sort()
      .reverse();

    if (versions.length < 2) {
      console.log('❌ 需要至少两个版本才能对比');
      return;
    }

    v1 = versions[0].match(/v[\d.]+/)?.[0] || 'unknown';
    v2 = versions[1].match(/v[\d.]+/)?.[0] || 'unknown';
  }

  console.log('');
  console.log(`📊 版本对比: ${v1} vs ${v2}`);
  console.log('');

  // 检查是否有 git
  try {
    execSync('git status', { stdio: 'pipe' });

    // 尝试使用 git diff
    console.log('变更文件：');
    try {
      const diff = execSync(
        `git diff --name-only`,
        { cwd: scriptDir, encoding: 'utf-8' }
      );
      if (diff) {
        console.log(diff);
      } else {
        console.log('  无文件变更');
      }
    } catch (e) {
      console.log('  无法获取文件差异');
    }

    // 显示行数统计
    console.log('\n代码统计：');
    const fragmentsDir = path.join(scriptDir, 'fragments');
    if (fs.existsSync(fragmentsDir)) {
      const files = fs.readdirSync(fragmentsDir).filter(f => f.endsWith('.html'));
      let totalLines = 0;
      files.forEach(file => {
        const content = fs.readFileSync(path.join(fragmentsDir, file), 'utf-8');
        const lines = content.split('\n').length;
        totalLines += lines;
        console.log(`  ${file}: ${lines} 行`);
      });
      console.log(`  总计: ${totalLines} 行`);
    }

  } catch (e) {
    console.log('⚠️  未找到git，仅显示文件列表');
  }
}

// 回滚到指定版本
function rollback(targetVersion) {
  const scriptDir = process.cwd();
  const versionsDir = path.join(scriptDir, 'versions');
  const versionFile = path.join(scriptDir, 'version.json');

  if (!fs.existsSync(versionsDir)) {
    console.error('❌ 没有找到versions目录');
    return;
  }

  // 如果没有指定版本，列出可用版本
  if (!targetVersion) {
    console.log('可用的备份版本：');
    const versions = fs.readdirSync(versionsDir)
      .filter(f => f.endsWith('.pdf'))
      .sort()
      .reverse();

    versions.forEach((v, i) => {
      console.log(`  ${i + 1}. ${v}`);
    });

    console.log('\n使用: node update.js rollback v1.0.0');
    return;
  }

  // 执行回滚
  const versionData = JSON.parse(fs.readFileSync(versionFile, 'utf-8'));
  const title = versionData.title;
  const backupFile = path.join(versionsDir, `${title}-${targetVersion}.pdf`);

  if (!fs.existsSync(backupFile)) {
    console.error(`❌ 找不到版本 ${targetVersion} 的备份`);
    return;
  }

  // 恢复文件
  const outputDir = path.join(scriptDir, 'output');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  fs.copyFileSync(backupFile, path.join(outputDir, `${title}-${targetVersion}.pdf`));

  // 更新 version.json
  versionData.version = targetVersion.replace('v', '');
  fs.writeFileSync(versionFile, JSON.stringify(versionData, null, 2) + '\n');

  console.log(`✅ 已回滚到 ${targetVersion}`);
}

// 建议版本升级
function suggestVersion() {
  const scriptDir = process.cwd();
  const fragmentsDir = path.join(scriptDir, 'fragments');

  console.log('');
  console.log('╔════════════════════════════════════════════════╗');
  console.log('║          💡 版本升级建议                        ║');
  console.log('╚════════════════════════════════════════════════╝');
  console.log('');

  let hasNewFeatures = false;
  let hasMajorChanges = false;
  let hasFixes = false;

  // 检查文件变更
  if (fs.existsSync(fragmentsDir)) {
    const files = fs.readdirSync(fragmentsDir);

    files.forEach(file => {
      const filePath = path.join(fragmentsDir, file);
      const content = fs.readFileSync(filePath, 'utf-8');
      const textContent = content.replace(/<[^>]*>/g, ' ');

      // 简单启发式判断
      if (/新增|新功能|添加|支持/i.test(textContent)) {
        hasNewFeatures = true;
      }
      if (/重构| redesign |重新设计|架构调整/i.test(textContent)) {
        hasMajorChanges = true;
      }
      if (/修复|修正|bug|问题/i.test(textContent)) {
        hasFixes = true;
      }
    });
  }

  console.log('基于当前内容分析：');
  console.log('');

  if (hasMajorChanges) {
    console.log('🚀 建议升级 MAJOR 版本 (v1.x → v2.0.0)');
    console.log('   原因：检测到重大架构调整或重构');
    console.log('   命令: node update.js major "重构产品架构"');
  } else if (hasNewFeatures) {
    console.log('✨ 建议升级 MINOR 版本 (v1.0 → v1.1.0)');
    console.log('   原因：检测到新增功能或章节');
    console.log('   命令: node update.js minor "新增功能模块"');
  } else if (hasFixes) {
    console.log('🐛 建议升级 PATCH 版本 (v1.0.0 → v1.0.1)');
    console.log('   原因：检测到问题修复或优化');
    console.log('   命令: node update.js patch "修复问题"');
  } else {
    console.log('🔨 建议仅增加构建号 (build +1)');
    console.log('   原因：内容稳定，无重大变更');
    console.log('   命令: node update.js build');
  }

  console.log('');
  console.log('或使用迭代向导：');
  console.log('   node update.js iterate');
}

// 执行主函数
main();
