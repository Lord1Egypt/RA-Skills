/**
 * Memory Manager - 记忆管理脚本
 * 自动管理记忆的存储、合并、清理和归档
 */

const fs = require('fs');
const path = require('path');

const CONFIG = {
  memoryDir: 'D:\\OpenClaw\\workspace\\memory',
  tiersDir: 'D:\\OpenClaw\\workspace\\memory\\tiers',
  learningOutcomesDir: 'D:\\OpenClaw\\workspace\\workspace\\learning-outcomes',
  logsDir: 'D:\\OpenClaw\\workspace\\logs',

  // 记忆保留策略
  workingMemoryDays: 7,
  shortTermMemoryDays: 30,
  maxLearningRounds: 50,
  maxConversations: 10,
};

const STATE = {
  totalRounds: 0,
  workingMemoryCount: 0,
  shortTermMemoryCount: 0,
  longTermMemoryCount: 0,
};

function log(msg, level = 'INFO') {
  const ts = new Date().toISOString().replace('T', ' ').substring(0, 19);
  const emoji = {
    'INFO': '⚪',
    'SUCCESS': '🟢',
    'ERROR': '🔴',
    'WARN': '🟡',
    'MEMORY': '🧠'
  }[level] || '⚪';
  console.log(`${emoji} ${msg}`);

  // 写入日志
  const logFile = path.join(CONFIG.logsDir, 'memory-manager.log');
  fs.appendFileSync(logFile, `[${ts}] [${level}] ${msg}\n`);
}

function ensureDirs() {
  const dirs = [
    CONFIG.memoryDir,
    CONFIG.tiersDir,
    path.join(CONFIG.tiersDir, 'working'),
    path.join(CONFIG.tiersDir, 'short-term'),
    path.join(CONFIG.tiersDir, 'long-term'),
    CONFIG.learningOutcomesDir,
    CONFIG.logsDir,
  ];

  dirs.forEach(dir => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  });
}

function getLearningRoundFiles() {
  if (!fs.existsSync(CONFIG.memoryDir)) return [];

  return fs.readdirSync(CONFIG.memoryDir)
    .filter(f => f.startsWith('learning-round-') && f.endsWith('.json'));
}

function getConversationFiles() {
  if (!fs.existsSync(CONFIG.memoryDir)) return [];

  return fs.readdirSync(CONFIG.memoryDir)
    .filter(f => f.startsWith('conversation-') && f.endsWith('.json'));
}

function cleanupOldLearningRounds() {
  log('清理旧的学习轮次记录...', 'MEMORY');

  const files = getLearningRoundFiles();
  STATE.totalRounds = files.length;

  if (files.length <= CONFIG.maxLearningRounds) {
    log(`✅ 学习记录数量正常：${files.length}/${CONFIG.maxLearningRounds}`, 'SUCCESS');
    return;
  }

  // 按时间排序，删除最旧的
  const sorted = files.sort((a, b) => {
    const aMatch = a.match(/round-(\d+)/);
    const bMatch = b.match(/round-(\d+)/);
    return (aMatch ? parseInt(aMatch[1]) : 0) - (bMatch ? parseInt(bMatch[1]) : 0);
  });

  const toDelete = sorted.slice(0, sorted.length - CONFIG.maxLearningRounds);

  toDelete.forEach(file => {
    const filePath = path.join(CONFIG.memoryDir, file);
    try {
      // 读取并合并内容到归档
      const content = JSON.parse(fs.readFileSync(filePath, 'utf8'));
      const archivePath = path.join(CONFIG.tiersDir, 'long-term', `archive-${file}`);
      fs.writeFileSync(archivePath, JSON.stringify(content, null, 2));

      // 删除原文件
      fs.unlinkSync(filePath);
      log(`📦 归档：${file}`, 'INFO');
    } catch (e) {
      log(`❌ 处理失败 ${file}: ${e.message}`, 'ERROR');
    }
  });

  log(`✅ 清理了 ${toDelete.length} 个旧学习记录`, 'SUCCESS');
}

function cleanupOldConversations() {
  log('清理旧的会话记录...', 'MEMORY');

  const files = getConversationFiles();

  if (files.length <= CONFIG.maxConversations) {
    log(`✅ 会话记录数量正常：${files.length}/${CONFIG.maxConversations}`, 'SUCCESS');
    return;
  }

  // 按修改时间排序，删除最旧的
  const sorted = files.sort((a, b) => {
    const aPath = path.join(CONFIG.memoryDir, a);
    const bPath = path.join(CONFIG.memoryDir, b);
    return fs.statSync(aPath).mtimeMs - fs.statSync(bPath).mtimeMs;
  });

  const toDelete = sorted.slice(0, sorted.length - CONFIG.maxConversations);

  toDelete.forEach(file => {
    const filePath = path.join(CONFIG.memoryDir, file);
    fs.unlinkSync(filePath);
    log(`🗑️ 删除：${file}`, 'INFO');
  });

  log(`✅ 清理了 ${toDelete.length} 个旧会话记录`, 'SUCCESS');
}

function mergeWorkingToShortTerm() {
  log('合并工作记忆到短期记忆...', 'MEMORY');

  const workingDir = path.join(CONFIG.tiersDir, 'working');
  const shortTermDir = path.join(CONFIG.tiersDir, 'short-term');

  if (!fs.existsSync(workingDir)) {
    log('⚠️ 工作记忆目录不存在', 'WARN');
    return;
  }

  const files = fs.readdirSync(workingDir);
  const cutoffDate = Date.now() - (CONFIG.workingMemoryDays * 24 * 60 * 60 * 1000);

  let moved = 0;

  files.forEach(file => {
    const filePath = path.join(workingDir, file);
    const stat = fs.statSync(filePath);

    if (stat.mtimeMs < cutoffDate) {
      try {
        fs.copyFileSync(filePath, path.join(shortTermDir, file));
        fs.unlinkSync(filePath);
        log(`📦 移动：${file} → 短期记忆`, 'INFO');
        moved++;
      } catch (e) {
        log(`❌ 移动失败 ${file}: ${e.message}`, 'ERROR');
      }
    }
  });

  if (moved > 0) {
    log(`✅ 移动了 ${moved} 个文件到短期记忆`, 'SUCCESS');
  } else {
    log('✅ 没有需要移动的文件', 'INFO');
  }
}

function mergeShortTermToLongTerm() {
  log('合并短期记忆到长期记忆...', 'MEMORY');

  const shortTermDir = path.join(CONFIG.tiersDir, 'short-term');
  const longTermDir = path.join(CONFIG.tiersDir, 'long-term');

  if (!fs.existsSync(shortTermDir)) {
    log('⚠️ 短期记忆目录不存在', 'WARN');
    return;
  }

  const files = fs.readdirSync(shortTermDir);
  const cutoffDate = Date.now() - (CONFIG.shortTermMemoryDays * 24 * 60 * 60 * 1000);

  let moved = 0;

  files.forEach(file => {
    const filePath = path.join(shortTermDir, file);
    const stat = fs.statSync(filePath);

    if (stat.mtimeMs < cutoffDate) {
      try {
        fs.copyFileSync(filePath, path.join(longTermDir, file));
        fs.unlinkSync(filePath);
        log(`📦 移动：${file} → 长期记忆`, 'INFO');
        moved++;
      } catch (e) {
        log(`❌ 移动失败 ${file}: ${e.message}`, 'ERROR');
      }
    }
  });

  if (moved > 0) {
    log(`✅ 移动了 ${moved} 个文件到长期记忆`, 'SUCCESS');
  } else {
    log('✅ 没有需要移动的文件', 'INFO');
  }
}

function generateMemoryReport() {
  log('生成记忆统计报告...', 'MEMORY');

  const report = {
    timestamp: new Date().toISOString(),
    totals: {
      learningRounds: getLearningRoundFiles().length,
      conversations: getConversationFiles().length,
    },
    tiers: {
      working: 0,
      shortTerm: 0,
      longTerm: 0,
    },
    files: {
      capabilities: fs.existsSync(path.join(CONFIG.memoryDir, 'capabilities.json')),
      knowledgeGraph: fs.existsSync(path.join(CONFIG.memoryDir, 'knowledge-graph.json')),
      memoryMd: fs.existsSync(path.join(CONFIG.memoryDir, 'MEMORY.md')),
    }
  };

  // 统计各层记忆数量
  const tiers = ['working', 'short-term', 'long-term'];
  tiers.forEach(tier => {
    const dir = path.join(CONFIG.tiersDir, tier);
    if (fs.existsSync(dir)) {
      report.tiers[tier.replace('-', '')] = fs.readdirSync(dir).length;
    }
  });

  // 保存报告
  const reportPath = path.join(CONFIG.logsDir, 'memory-report.json');
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));

  log(`📊 记忆统计报告已保存：${reportPath}`, 'SUCCESS');
  log(`   学习轮次：${report.totals.learningRounds}`, 'INFO');
  log(`   会话记录：${report.totals.conversations}`, 'INFO');
  log(`   工作记忆：${report.tiers.working}`, 'INFO');
  log(`   短期记忆：${report.tiers.shortTerm}`, 'INFO');
  log(`   长期记忆：${report.tiers.longTerm}`, 'INFO');

  return report;
}

function run() {
  log('=========================================', 'MEMORY');
  log('🧠 Memory Manager 启动', 'MEMORY');
  log('=========================================', 'MEMORY');

  ensureDirs();

  cleanupOldLearningRounds();
  cleanupOldConversations();
  mergeWorkingToShortTerm();
  mergeShortTermToLongTerm();
  generateMemoryReport();

  log('=========================================', 'MEMORY');
  log('✅ Memory Manager 完成', 'SUCCESS');
  log('=========================================', 'MEMORY');
}

// 如果直接运行
if (require.main === module) {
  run();
}

module.exports = { run, cleanupOldLearningRounds, cleanupOldConversations, mergeWorkingToShortTerm, mergeShortTermToLongTerm, generateMemoryReport };
