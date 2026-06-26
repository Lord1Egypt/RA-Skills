#!/usr/bin/env node
/**
 * OpenClaw Cost Analyzer
 * 分析 session logs，识别高消耗场景，给出优化建议
 * 纯 Node.js，无外部依赖
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// 配置
const CONFIG = {
  logsDir: path.join(os.homedir(), '.openclaw/workspace/memory/conversations'),
  memoryDir: path.join(os.homedir(), '.openclaw/workspace/memory'),
  outputDir: path.join(os.homedir(), '.openclaw/workspace/memory'),
  
  // 模型成本 (USD per 1M tokens)
  modelCosts: {
    'yunyi-claude/claude-opus-4-6': { input: 15, output: 75 },
    'yunyi-claude/claude-sonnet-4-20250514': { input: 3, output: 15 },
    'yunyi-claude/claude-opus-4-20250514': { input: 15, output: 75 },
    'self/claude-opus-4-5-20251101': { input: 15, output: 75 },
    'deepseek/deepseek-chat': { input: 0.014, output: 0.028 }, // ¥2/M ≈ $0.28/M
    'local/qwen2.5:7b': { input: 0, output: 0 }
  },
  
  // 阈值
  thresholds: {
    longConversation: 50000, // tokens
    highContextSession: 30000,
    frequentCron: 10, // 每天超过10次
    expensiveModel: 10 // USD per 1M tokens
  }
};

/**
 * 读取所有 session logs
 */
function readSessionLogs(daysBack = 7) {
  const logs = [];
  const now = Date.now();
  const cutoff = now - (daysBack * 24 * 60 * 60 * 1000);
  
  try {
    if (!fs.existsSync(CONFIG.logsDir)) {
      return logs;
    }
    
    // 遍历所有月份目录
    const monthDirs = fs.readdirSync(CONFIG.logsDir).filter(d => {
      const fullPath = path.join(CONFIG.logsDir, d);
      return fs.statSync(fullPath).isDirectory() && /^\d{4}-\d{2}$/.test(d);
    });
    
    for (const monthDir of monthDirs) {
      const monthPath = path.join(CONFIG.logsDir, monthDir);
      const files = fs.readdirSync(monthPath);
      
      for (const file of files) {
        if (!file.endsWith('.jsonl')) continue;
        
        const filePath = path.join(monthPath, file);
        const stat = fs.statSync(filePath);
        
        if (stat.mtimeMs < cutoff) continue;
        
        const content = fs.readFileSync(filePath, 'utf8');
        const lines = content.trim().split('\n').filter(l => l);
        
        for (const line of lines) {
          try {
            const entry = JSON.parse(line);
            logs.push({ file, ...entry });
          } catch (e) {
            // 跳过无效行
          }
        }
      }
    }
  } catch (err) {
    console.error('读取 session logs 失败:', err.message);
  }
  
  return logs;
}

/**
 * 分析 token 消耗模式
 */
function analyzeTokenUsage(logs) {
  const analysis = {
    totalSessions: 0,
    totalInputTokens: 0,
    totalOutputTokens: 0,
    totalCost: 0,
    byModel: {},
    bySession: {},
    highCostSessions: [],
    longConversations: [],
    cronSessions: []
  };
  
  // 按文件分组（每个文件是一个 session）
  const sessionMap = new Map();
  
  // 先按文件分组所有日志
  const logsByFile = new Map();
  for (const log of logs) {
    const file = log.file || 'unknown';
    if (!logsByFile.has(file)) {
      logsByFile.set(file, []);
    }
    logsByFile.get(file).push(log);
  }
  
  // 处理每个 session
  for (const [file, sessionLogs] of logsByFile.entries()) {
    // 获取 session ID
    const sessionLog = sessionLogs.find(l => l.type === 'session');
    const sessionId = sessionLog ? sessionLog.id : file;
    
    // 获取模型信息
    const modelLog = sessionLogs.find(l => 
      l.type === 'custom' && 
      l.customType === 'model-snapshot' && 
      l.data && 
      l.data.modelId
    );
    
    let model = 'unknown';
    if (modelLog && modelLog.data) {
      const provider = modelLog.data.provider || 'unknown';
      const modelId = modelLog.data.modelId || 'unknown';
      model = `${provider}/${modelId}`;
    }
    
    // 统计 token 使用
    let inputTokens = 0;
    let outputTokens = 0;
    let messageCount = 0;
    
    for (const log of sessionLogs) {
      if (log.type === 'message' && log.message && log.message.role === 'assistant') {
        messageCount++;
        
        // 从 message 中提取 usage
        if (log.message.usage) {
          inputTokens += log.message.usage.input || 0;
          outputTokens += log.message.usage.output || 0;
        }
      }
    }
    
    // 跳过没有 token 使用的 session
    if (inputTokens === 0 && outputTokens === 0) continue;
    
    // 计算成本
    const costs = CONFIG.modelCosts[model] || { input: 3, output: 15 };
    const cost = (inputTokens * costs.input + outputTokens * costs.output) / 1000000;
    
    // 保存 session 信息
    sessionMap.set(sessionId, {
      id: sessionId,
      model,
      inputTokens,
      outputTokens,
      cost,
      messages: messageCount,
      isCron: false, // TODO: 从 label 判断
      firstSeen: sessionLog ? sessionLog.timestamp : null,
      lastSeen: sessionLogs[sessionLogs.length - 1].timestamp
    });
    
    // 按模型统计
    if (!analysis.byModel[model]) {
      analysis.byModel[model] = {
        sessions: 0,
        inputTokens: 0,
        outputTokens: 0,
        cost: 0
      };
    }
    analysis.byModel[model].sessions += 1;
    analysis.byModel[model].inputTokens += inputTokens;
    analysis.byModel[model].outputTokens += outputTokens;
    analysis.byModel[model].cost += cost;
    
    analysis.totalInputTokens += inputTokens;
    analysis.totalOutputTokens += outputTokens;
    analysis.totalCost += cost;
  }
  
  // 转换为数组并排序
  const sessions = Array.from(sessionMap.values());
  analysis.totalSessions = sessions.length;
  
  // 识别高消耗场景
  for (const session of sessions) {
    const totalTokens = session.inputTokens + session.outputTokens;
    
    if (session.cost > 0.5) {
      analysis.highCostSessions.push(session);
    }
    
    if (totalTokens > CONFIG.thresholds.longConversation) {
      analysis.longConversations.push(session);
    }
    
    if (session.isCron) {
      analysis.cronSessions.push(session);
    }
  }
  
  // 排序
  analysis.highCostSessions.sort((a, b) => b.cost - a.cost);
  analysis.longConversations.sort((a, b) => (b.inputTokens + b.outputTokens) - (a.inputTokens + a.outputTokens));
  
  return analysis;
}

/**
 * 生成优化建议
 */
function generateRecommendations(analysis) {
  const recommendations = [];
  
  // 1. 模型降级建议
  for (const [model, stats] of Object.entries(analysis.byModel)) {
    const costs = CONFIG.modelCosts[model] || { input: 3, output: 15 };
    const avgCost = (costs.input + costs.output) / 2;
    
    if (avgCost > CONFIG.thresholds.expensiveModel && stats.sessions > 5) {
      const savings = stats.cost * 0.8; // 假设降级可省 80%
      recommendations.push({
        type: 'model_downgrade',
        priority: 'high',
        title: `模型降级：${model}`,
        description: `该模型成本较高 ($${avgCost}/M tokens)，已使用 ${stats.sessions} 次会话`,
        suggestion: '对于简单任务使用 Sonnet 或 DeepSeek，复杂任务才用 Opus',
        potentialSavings: `$${savings.toFixed(2)}`,
        action: 'openclaw models set yunyi-claude/claude-sonnet-4-20250514'
      });
    }
  }
  
  // 2. 长对话优化
  if (analysis.longConversations.length > 0) {
    const topConv = analysis.longConversations[0];
    const tokens = topConv.inputTokens + topConv.outputTokens;
    recommendations.push({
      type: 'long_conversation',
      priority: 'medium',
      title: '长对话检测',
      description: `发现 ${analysis.longConversations.length} 个长对话，最长 ${tokens.toLocaleString()} tokens`,
      suggestion: '超过 50k tokens 时开启新会话，避免 context 累积',
      potentialSavings: `$${(topConv.cost * 0.3).toFixed(2)}`,
      action: '手动开启新会话或设置 context 限制'
    });
  }
  
  // 3. Cron 频率优化
  if (analysis.cronSessions.length > CONFIG.thresholds.frequentCron) {
    const cronCost = analysis.cronSessions.reduce((sum, s) => sum + s.cost, 0);
    recommendations.push({
      type: 'cron_frequency',
      priority: 'medium',
      title: 'Cron 任务频率过高',
      description: `检测到 ${analysis.cronSessions.length} 次 cron 执行，总成本 $${cronCost.toFixed(2)}`,
      suggestion: '降低非关键 cron 任务频率，或使用更便宜的模型',
      potentialSavings: `$${(cronCost * 0.5).toFixed(2)}`,
      action: 'openclaw cron list 检查并调整频率'
    });
  }
  
  // 4. Context 压缩
  const avgInputPerSession = analysis.totalInputTokens / analysis.totalSessions;
  if (avgInputPerSession > CONFIG.thresholds.highContextSession) {
    recommendations.push({
      type: 'context_compression',
      priority: 'high',
      title: 'Context 过大',
      description: `平均每次会话输入 ${avgInputPerSession.toFixed(0)} tokens，可能加载了过多文件`,
      suggestion: '优化 AGENTS.md、SOUL.md，移除不必要的内容；使用 lazy loading',
      potentialSavings: `$${(analysis.totalCost * 0.4).toFixed(2)}`,
      action: '参考 openclaw-token-optimizer skill 的 context_optimizer'
    });
  }
  
  // 5. 使用本地模型
  if (!analysis.byModel['local/qwen2.5:7b'] || analysis.byModel['local/qwen2.5:7b'].sessions < 5) {
    recommendations.push({
      type: 'local_model',
      priority: 'low',
      title: '启用本地模型',
      description: '简单任务可使用本地 Ollama 模型，完全免费',
      suggestion: '文件读取、简单查询等使用 local/qwen2.5:7b',
      potentialSavings: '$0.50+',
      action: 'openclaw models set local/qwen2.5:7b (临时切换)'
    });
  }
  
  return recommendations.sort((a, b) => {
    const priority = { high: 3, medium: 2, low: 1 };
    return priority[b.priority] - priority[a.priority];
  });
}

/**
 * 生成成本报告
 */
function generateReport(analysis, recommendations) {
  const report = [];
  
  report.push('# OpenClaw 成本分析报告');
  report.push('');
  report.push(`生成时间: ${new Date().toLocaleString('zh-CN', { timeZone: 'Australia/Melbourne' })}`);
  report.push('');
  
  // 总览
  report.push('## 📊 总览');
  report.push('');
  report.push(`- 总会话数: ${analysis.totalSessions}`);
  report.push(`- 总输入 tokens: ${analysis.totalInputTokens.toLocaleString()}`);
  report.push(`- 总输出 tokens: ${analysis.totalOutputTokens.toLocaleString()}`);
  report.push(`- 总成本: $${analysis.totalCost.toFixed(2)}`);
  report.push(`- 平均每会话: $${(analysis.totalCost / analysis.totalSessions).toFixed(3)}`);
  report.push('');
  
  // 按模型统计
  report.push('## 🤖 模型使用统计');
  report.push('');
  for (const [model, stats] of Object.entries(analysis.byModel)) {
    const shortModel = model.split('/').pop();
    report.push(`### ${shortModel}`);
    report.push(`- 会话数: ${stats.sessions}`);
    report.push(`- 输入: ${stats.inputTokens.toLocaleString()} tokens`);
    report.push(`- 输出: ${stats.outputTokens.toLocaleString()} tokens`);
    report.push(`- 成本: $${stats.cost.toFixed(2)}`);
    report.push('');
  }
  
  // 高消耗场景
  if (analysis.highCostSessions.length > 0) {
    report.push('## 💰 高成本会话 (Top 5)');
    report.push('');
    for (const session of analysis.highCostSessions.slice(0, 5)) {
      report.push(`- Session: ${session.id.substring(0, 8)}...`);
      report.push(`  - 模型: ${session.model.split('/').pop()}`);
      report.push(`  - Tokens: ${(session.inputTokens + session.outputTokens).toLocaleString()}`);
      report.push(`  - 成本: $${session.cost.toFixed(2)}`);
      report.push(`  - 消息数: ${session.messages}`);
      report.push('');
    }
  }
  
  // 优化建议
  report.push('## 💡 优化建议');
  report.push('');
  
  if (recommendations.length === 0) {
    report.push('✅ 当前配置已优化，暂无建议。');
  } else {
    for (let i = 0; i < recommendations.length; i++) {
      const rec = recommendations[i];
      const emoji = rec.priority === 'high' ? '🔴' : rec.priority === 'medium' ? '🟡' : '🟢';
      
      report.push(`### ${i + 1}. ${emoji} ${rec.title}`);
      report.push('');
      report.push(`**问题**: ${rec.description}`);
      report.push('');
      report.push(`**建议**: ${rec.suggestion}`);
      report.push('');
      report.push(`**预计节省**: ${rec.potentialSavings}`);
      report.push('');
      report.push(`**操作**: \`${rec.action}\``);
      report.push('');
    }
    
    const totalSavings = recommendations.reduce((sum, r) => {
      const amount = parseFloat(r.potentialSavings.replace('$', '').replace('+', ''));
      return sum + (isNaN(amount) ? 0 : amount);
    }, 0);
    
    report.push(`**总预计节省**: $${totalSavings.toFixed(2)}`);
  }
  
  return report.join('\n');
}

/**
 * 主函数
 */
function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'analyze';
  const daysBack = parseInt(args[1]) || 7;
  
  if (command === 'analyze') {
    console.log(`正在分析最近 ${daysBack} 天的 session logs...`);
    
    const logs = readSessionLogs(daysBack);
    if (logs.length === 0) {
      console.log('未找到 session logs，请确认路径正确。');
      return;
    }
    
    console.log(`读取到 ${logs.length} 条日志记录`);
    
    const analysis = analyzeTokenUsage(logs);
    const recommendations = generateRecommendations(analysis);
    const report = generateReport(analysis, recommendations);
    
    // 输出到文件
    const outputPath = path.join(CONFIG.outputDir, 'cost-analysis-report.md');
    fs.writeFileSync(outputPath, report, 'utf8');
    
    console.log('\n' + report);
    console.log(`\n报告已保存到: ${outputPath}`);
    
  } else if (command === 'quick') {
    // 快速检查
    const logs = readSessionLogs(1);
    const analysis = analyzeTokenUsage(logs);
    
    console.log('📊 今日成本快览:');
    console.log(`  总成本: $${analysis.totalCost.toFixed(2)}`);
    console.log(`  会话数: ${analysis.totalSessions}`);
    console.log(`  平均: $${(analysis.totalCost / analysis.totalSessions || 0).toFixed(3)}/会话`);
    
  } else {
    console.log('用法:');
    console.log('  node cost_analyzer.js analyze [天数]  - 生成完整分析报告 (默认7天)');
    console.log('  node cost_analyzer.js quick          - 快速查看今日成本');
  }
}

if (require.main === module) {
  main();
}

module.exports = { analyzeTokenUsage, generateRecommendations, generateReport };
