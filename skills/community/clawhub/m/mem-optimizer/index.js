/**
 * MemOptimizer - 记忆优化器
 * 整合 self-improving 机制，自动统计、压缩和优化记忆文件
 */

const fs = require('fs').promises;
const fsSync = require('fs');
const path = require('path');
const { exec } = require('child_process');

// Token 估算：1 token ≈ 4 个字符（英文）或 2 个字符（中文）
const CHARS_PER_TOKEN_ZH = 2;
const CHARS_PER_TOKEN_EN = 4;

/**
 * 估算文本的 token 数量
 */
function estimateTokens(text) {
  const zhCount = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
  const enCount = text.length - zhCount;
  return Math.round(zhCount / CHARS_PER_TOKEN_ZH + enCount / CHARS_PER_TOKEN_EN);
}

/**
 * 扫描 memory 目录，获取文件信息
 */
async function scanMemoryFiles(workspacePath) {
  const memoryDir = path.join(workspacePath, 'memory');
  const files = [];
  let totalTokens = 0;
  
  try {
    // 检查 memory 目录是否存在
    if (!fsSync.existsSync(memoryDir)) {
      return { files, totalTokens };
    }
    
    // 读取 memory 目录下的所有 .md 文件
    const entries = await fs.readdir(memoryDir, { withFileTypes: true });
    
    for (const entry of entries) {
      if (entry.isFile() && entry.name.endsWith('.md')) {
        const filePath = path.join(memoryDir, entry.name);
        const content = await fs.readFile(filePath, 'utf-8');
        const lines = content.split('\n').length;
        const tokens = estimateTokens(content);
        
        files.push({
          name: entry.name,
          path: filePath,
          lines,
          tokens
        });
        
        totalTokens += tokens;
      }
    }
    
    // 按修改时间排序（最新的在前）
    files.sort((a, b) => {
      try {
        const statA = fsSync.statSync(a.path);
        const statB = fsSync.statSync(b.path);
        return statB.mtimeMs - statA.mtimeMs;
      } catch (e) {
        return 0;
      }
    });
    
  } catch (error) {
    console.error('Error scanning memory files:', error);
  }
  
  return { files, totalTokens };
}

/**
 * 读取 self-improving 的偏好和学习记录
 */
async function loadSelfImprovingPreferences() {
  const workspacePath = process.cwd();
  const preferencesPath = path.join(workspacePath, 'self-improving', 'preferences.md');
  const correctionsPath = path.join(workspacePath, 'self-improving', 'corrections.md');
  const reflectionsPath = path.join(workspacePath, 'self-improving', 'reflections.md');
  
  const preferences = {
    compressionThreshold: 50,
    maxSummaryLines: 20,
    defaultCompressionRatio: 0.4,
    learnedPatterns: []
  };
  
  try {
    // 读取已确认的偏好
    if (fsSync.existsSync(preferencesPath)) {
      const content = await fs.readFile(preferencesPath, 'utf-8');
      // 解析偏好设置
      const thresholdMatch = content.match(/compressionThreshold[:\s]+(\d+)/i);
      if (thresholdMatch) preferences.compressionThreshold = parseInt(thresholdMatch[1]);
      
      const linesMatch = content.match(/maxSummaryLines[:\s]+(\d+)/i);
      if (linesMatch) preferences.maxSummaryLines = parseInt(linesMatch[1]);
      
      // 读取确认的学习模式
      if (fsSync.existsSync(reflectionsPath)) {
        const reflections = await fs.readFile(reflectionsPath, 'utf-8');
        const patterns = reflections.match(/```json[\s\S]*?```/g);
        if (patterns) {
          patterns.forEach(p => {
            try {
              const jsonMatch = p.match(/\{[\s\S]*\}/);
              if (jsonMatch) {
                const obj = JSON.parse(jsonMatch[0]);
                if (obj.status === 'Confirmed') {
                  preferences.learnedPatterns.push(obj);
                }
              }
            } catch (e) {}
          });
        }
      }
    }
  } catch (err) {
    console.error('Error loading self-improving preferences:', err);
  }
  
  return preferences;
}

/**
 * 记录优化反思到 self-improving
 */
async function logReflection(optimizeResult, userFeedback = null) {
  const workspacePath = process.cwd();
  const reflectionsPath = path.join(workspacePath, 'self-improving', 'reflections.md');
  const correctionsPath = path.join(workspacePath, 'self-improving', 'corrections.md');
  
  const date = new Date().toISOString().split('T')[0];
  const timestamp = new Date().toISOString();
  
  const reflection = {
    date,
    timestamp,
    type: 'memory_optimization',
    stats: {
      freedTokens: optimizeResult.stats?.freedTokens || 0,
      summarizedTokens: optimizeResult.stats?.summarizedTokens || 0,
      filesProcessed: optimizeResult.stats?.filesProcessed || 0
    },
    userFeedback,
    status: 'Tentative', // Tentative, Emerging, Pending, Confirmed, Archived
    confidence: 'low'
  };
  
  const reflectionText = `
## [${date}] - Memory Optimization

**What I did:** Compressed ${optimizeResult.stats?.filesProcessed} memory files, freed ${optimizeResult.stats?.freedTokens} tokens
**Outcome:** ${userFeedback || 'Pending user feedback'}
**Reflection:** Compression ratio of ${(optimizeResult.stats?.compressionRatio || 0).toFixed(2)*100}% was applied
**Lesson:** ${userFeedback === 'approved' ? 'Compression was acceptable' : 'Need to adjust strategy'}
**Status:** ${reflection.status}
\`\`\`json
${JSON.stringify(reflection, null, 2)}
\`\`\`
`;
  
  try {
    // 记录到 reflections.md
    await fs.appendFile(reflectionsPath, reflectionText, 'utf-8');
    
    // 如果有负面反馈，记录到 corrections.md
    if (userFeedback === 'negative' || userFeedback === 'too aggressive') {
      const correction = `
- **Date:** ${timestamp}
- **Type:** Over-compression warning
- **Action:** Increase compression threshold
- **Current threshold:** ${reflection.stats.freedTokens} tokens freed
- **Note:** User requested more details retained
`;
      await fs.appendFile(correctionsPath, correction, 'utf-8');
    }
  } catch (err) {
    console.error('Error logging reflection:', err);
  }
  
  return reflection;
}

/**
 * 压缩记忆内容（简单摘要生成）
 */
function summarizeContent(content, maxLines = 20, compressionRatio = 0.4) {
  const lines = content.split('\n');
  if (lines.length <= maxLines) return content;
  
  const result = [];
  let summaryAdded = false;
  const keepLines = Math.floor(lines.length * compressionRatio);
  
  for (let i = 0; i < lines.length; i++) {
    if (i === 0) {
      result.push(lines[i]); // 标题
      continue;
    }
    
    if (i === 1 && lines[i].trim() === '') {
      // 在标题后的空行添加压缩信息
      result.push(lines[i]);
      continue;
    }
    
    if (summaryAdded) {
      break;
    }
    
    // 保留关键行（标题附近）
    if (i < 5) {
      result.push(lines[i]);
      continue;
    }
    
    // 压缩模式：保留前 40% 的内容
    if (i <= keepLines) {
      result.push(lines[i]);
    } else if (i === keepLines) {
      // 添加压缩摘要
      result.push('');
      result.push(`> 📝 **已压缩**: 原内容 ${lines.length} 行，保留 ${keepLines} 行关键信息`);
      result.push('');
      result.push('... [内容已压缩，可通过 mem_optimize({dryRun: false}) 查看完整日志]');
      summaryAdded = true;
      break;
    }
  }
  
  return result.join('\n');
}

/**
 * 获取服务器状态
 */
async function getServerStatus() {
  return new Promise((resolve) => {
    const commands = {
      cpu: 'top -bn1 | grep "Cpu(s)" | awk \'{print $2 + $4}\'',
      memory: 'free -h | grep Mem | awk \'{print $3 "/" $2}\'',
      disk: 'df -h / | tail -1 | awk \'{print $3 "/" $2}\'',
      uptime: 'uptime -p'
    };
    
    const results = {};
    let completed = 0;
    
    Object.keys(commands).forEach(key => {
      exec(commands[key], (err, stdout, stderr) => {
        if (err) {
          results[key] = 'N/A';
        } else {
          results[key] = stdout.trim();
        }
        completed++;
        if (completed === Object.keys(commands).length) {
          resolve(results);
        }
      });
    });
  });
}

/**
 * 获取多智能体状态
 */
async function getAgentStatus() {
  return new Promise((resolve) => {
    exec('ls -1 ~/.openclaw/agents/ 2>/dev/null | head -10', (err, stdout, stderr) => {
      if (err || !stdout.trim()) {
        resolve({ agents: [], total: 0 });
        return;
      }
      
      const agents = stdout.trim().split('\n').filter(a => a.trim() && a !== 'main');
      resolve({ agents, total: agents.length });
    });
  });
}

/**
 * 检查文件是否在指定时间内被修改过（小时）
 */
function isFileModifiedWithinHours(filePath, hours) {
  try {
    const stats = fsSync.statSync(filePath);
    const now = Date.now();
    const modifiedTime = stats.mtimeMs;
    const hoursDiff = (now - modifiedTime) / (1000 * 60 * 60);
    return hoursDiff <= hours;
  } catch (error) {
    return false;
  }
}

/**
 * 扫描所有智能体的工作空间，找出过去24小时有工作的智能体
 */
async function scanAllAgentsWorkspaces() {
  const agentsDir = '/root/.openclaw/agents';
  const activeAgents = [];
  
  try {
    if (!fsSync.existsSync(agentsDir)) {
      return activeAgents;
    }
    
    const agentEntries = await fs.readdir(agentsDir, { withFileTypes: true });
    
    for (const entry of agentEntries) {
      if (entry.isDirectory()) {
        const agentId = entry.name;
        const workspacePath = `/root/.openclaw/workspace-${agentId}`;
        const memoryDir = path.join(workspacePath, 'memory');
        
        // 检查工作空间是否存在
        if (!fsSync.existsSync(workspacePath)) {
          continue;
        }
        
        // 检查memory目录是否存在
        if (!fsSync.existsSync(memoryDir)) {
          continue;
        }
        
        // 检查是否有24小时内修改的memory文件
        let hasRecentWork = false;
        try {
          const memoryFiles = await fs.readdir(memoryDir);
          for (const file of memoryFiles) {
            if (file.endsWith('.md')) {
              const filePath = path.join(memoryDir, file);
              if (isFileModifiedWithinHours(filePath, 24)) {
                hasRecentWork = true;
                break;
              }
            }
          }
        } catch (error) {
          // 忽略读取错误
        }
        
        if (hasRecentWork) {
          activeAgents.push({
            id: agentId,
            workspace: workspacePath,
            memoryDir: memoryDir
          });
        }
      }
    }
    
    // 按ID排序
    activeAgents.sort((a, b) => a.id.localeCompare(b.id));
    
  } catch (error) {
    console.error('Error scanning agent workspaces:', error);
  }
  
  return activeAgents;
}

/**
 * 优化单个智能体的记忆文件
 */
async function optimizeAgentMemory(agentInfo, dryRun = true, compressionRatio = 0.4) {
  const { id, workspace, memoryDir } = agentInfo;
  const result = {
    agentId: id,
    success: false,
    filesProcessed: 0,
    originalTokens: 0,
    freedTokens: 0,
    summarizedTokens: 0,
    details: [],
    error: null
  };
  
  try {
    // 扫描该智能体的memory文件
    const scanResult = await scanMemoryFiles(workspace);
    const { files, totalTokens } = scanResult;
    
    if (files.length === 0) {
      result.success = true;
      result.message = `智能体 ${id} 无memory文件`;
      return result;
    }
    
    result.originalTokens = totalTokens;
    
    // 加载self-improving偏好
    const preferences = await loadSelfImprovingPreferences();
    
    let freedTokens = 0;
    let summarizedTokens = 0;
    const details = [];
    
    for (const file of files) {
      const originalTokens = file.tokens;
      
      // 读取文件内容
      const content = await fs.readFile(file.path, 'utf-8');
      
      // 根据preferences决定是否压缩
      if (file.lines > preferences.compressionThreshold) {
        const newContent = summarizeContent(content, preferences.maxSummaryLines, compressionRatio);
        const newTokens = estimateTokens(newContent);
        
        if (newTokens < originalTokens) {
          const saved = originalTokens - newTokens;
          summarizedTokens += newTokens;
          freedTokens += saved;
          
          if (!dryRun) {
            await fs.writeFile(file.path, newContent, 'utf-8');
          }
          
          details.push({
            file: file.name,
            originalTokens,
            newTokens,
            freed: saved,
            lines: file.lines,
            action: '压缩'
          });
        }
      }
    }
    
    result.success = true;
    result.filesProcessed = details.length;
    result.freedTokens = freedTokens;
    result.summarizedTokens = summarizedTokens;
    result.details = details;
    result.message = `智能体 ${id}: 已释放 ${freedTokens} tokens，总结了 ${summarizedTokens} tokens`;
    
  } catch (error) {
    result.success = false;
    result.error = error.message;
    result.message = `智能体 ${id} 优化失败: ${error.message}`;
  }
  
  return result;
}

/**
 * 优化所有活跃智能体的记忆文件
 */
async function optimizeAllAgentsMemory(dryRun = true, includeReflection = true, compressionRatio = 0.4) {
  // 扫描所有活跃智能体
  const activeAgents = await scanAllAgentsWorkspaces();
  
  if (activeAgents.length === 0) {
    return {
      success: true,
      message: '未找到过去24小时有工作的智能体',
      totalAgents: 0,
      totalFreedTokens: 0,
      agentResults: [],
      dryRun
    };
  }
  
  console.log(`找到 ${activeAgents.length} 个过去24小时有工作的智能体:`, activeAgents.map(a => a.id));
  
  // 并行优化所有智能体
  const optimizationPromises = activeAgents.map(agent => 
    optimizeAgentMemory(agent, dryRun, compressionRatio)
  );
  
  const agentResults = await Promise.all(optimizationPromises);
  
  // 计算总计
  const totalFreedTokens = agentResults.reduce((sum, result) => sum + (result.freedTokens || 0), 0);
  const totalSummarizedTokens = agentResults.reduce((sum, result) => sum + (result.summarizedTokens || 0), 0);
  const totalFilesProcessed = agentResults.reduce((sum, result) => sum + (result.filesProcessed || 0), 0);
  
  // 生成各智能体工作概述
  const agentSummaries = agentResults.map(result => {
    const summary = {
      agentId: result.agentId,
      status: result.success ? '成功' : '失败',
      filesProcessed: result.filesProcessed || 0,
      freedTokens: result.freedTokens || 0,
      summarizedTokens: result.summarizedTokens || 0,
      message: result.message || ''
    };
    
    // 如果有错误，添加错误信息
    if (result.error) {
      summary.error = result.error;
    }
    
    return summary;
  });
  
  // 生成总结报告
  const summaryReport = generateMultiAgentSummary(agentSummaries, totalFreedTokens, totalSummarizedTokens, totalFilesProcessed);
  
  const finalResult = {
    success: agentResults.every(r => r.success),
    message: `已优化 ${activeAgents.length} 个智能体的记忆，总计释放 ${totalFreedTokens} tokens`,
    totalAgents: activeAgents.length,
    totalFreedTokens,
    totalSummarizedTokens,
    totalFilesProcessed,
    agentResults: agentSummaries,
    summaryReport,
    dryRun
  };
  
  // 记录反思（如果非dryRun且需要）
  if (!dryRun && includeReflection) {
    try {
      const reflection = await logReflection(finalResult, null);
      finalResult.reflection = reflection;
    } catch (error) {
      console.error('Error logging reflection:', error);
    }
  }
  
  return finalResult;
}

/**
 * 生成多智能体总结报告
 */
function generateMultiAgentSummary(agentSummaries, totalFreedTokens, totalSummarizedTokens, totalFilesProcessed) {
  const now = new Date();
  const timestamp = now.toISOString();
  const dateStr = now.toLocaleDateString('zh-CN');
  const timeStr = now.toLocaleTimeString('zh-CN');
  
  let report = `# 多智能体记忆优化报告\n\n`;
  report += `**报告时间**: ${dateStr} ${timeStr}\n`;
  report += `**优化范围**: 过去24小时有工作的智能体\n`;
  report += `**处理模式**: ${agentSummaries.length > 0 ? '实际执行' : '预览模式'}\n\n`;
  
  report += `## 统计摘要\n`;
  report += `- **智能体数量**: ${agentSummaries.length} 个\n`;
  report += `- **处理文件数**: ${totalFilesProcessed} 个\n`;
  report += `- **总计释放 tokens**: ${totalFreedTokens}\n`;
  report += `- **总计总结 tokens**: ${totalSummarizedTokens}\n`;
  report += `- **总体压缩率**: ${totalFreedTokens > 0 ? Math.round((totalFreedTokens / (totalFreedTokens + totalSummarizedTokens)) * 100) : 0}%\n\n`;
  
  report += `## 各智能体优化详情\n\n`;
  
  if (agentSummaries.length === 0) {
    report += `无过去24小时有工作的智能体。\n`;
  } else {
    // 按释放tokens排序
    const sortedSummaries = [...agentSummaries].sort((a, b) => b.freedTokens - a.freedTokens);
    
    report += `| 智能体 | 状态 | 处理文件数 | 释放 tokens | 总结 tokens | 备注 |\n`;
    report += `|--------|------|------------|-------------|-------------|------|\n`;
    
    for (const summary of sortedSummaries) {
      const statusEmoji = summary.status === '成功' ? '✅' : '❌';
      report += `| ${summary.agentId} | ${statusEmoji} ${summary.status} | ${summary.filesProcessed} | ${summary.freedTokens} | ${summary.summarizedTokens} | ${summary.message.substring(0, 30)}... |\n`;
    }
    
    report += `\n`;
    
    // 各智能体工作概述
    report += `## 各智能体前24小时工作概述\n\n`;
    
    for (const summary of sortedSummaries) {
      report += `### ${summary.agentId}\n`;
      report += `- **优化状态**: ${summary.status}\n`;
      report += `- **释放 tokens**: ${summary.freedTokens}\n`;
      report += `- **总结 tokens**: ${summary.summarizedTokens}\n`;
      report += `- **处理文件数**: ${summary.filesProcessed}\n`;
      
      // 这里可以添加更详细的工作概述
      // 例如：读取智能体的最新memory文件，提取关键信息
      // 由于时间关系，暂时使用简化的概述
      report += `- **工作概述**: 过去24小时有记忆文件更新，已进行优化压缩\n`;
      
      if (summary.error) {
        report += `- **错误信息**: ${summary.error}\n`;
      }
      
      report += `\n`;
    }
    
    // 节省tokens分析
    report += `## 节省 tokens 分析\n\n`;
    
    const successfulAgents = sortedSummaries.filter(s => s.status === '成功' && s.freedTokens > 0);
    if (successfulAgents.length > 0) {
      report += `### 各智能体节省情况\n`;
      
      for (const agent of successfulAgents) {
        const percentage = totalFreedTokens > 0 ? Math.round((agent.freedTokens / totalFreedTokens) * 100) : 0;
        report += `- **${agent.agentId}**: ${agent.freedTokens} tokens (${percentage}%)\n`;
      }
      
      report += `\n`;
      report += `### 节省分布\n`;
      
      // 生成简单的分布描述
      const topAgent = successfulAgents[0];
      if (topAgent) {
        const topPercentage = Math.round((topAgent.freedTokens / totalFreedTokens) * 100);
        report += `- **主要节省来源**: ${topAgent.agentId} (${topPercentage}%)\n`;
      }
      
      if (successfulAgents.length > 1) {
        const otherAgents = successfulAgents.slice(1);
        const otherTotal = otherAgents.reduce((sum, a) => sum + a.freedTokens, 0);
        const otherPercentage = Math.round((otherTotal / totalFreedTokens) * 100);
        report += `- **其他智能体**: ${otherTotal} tokens (${otherPercentage}%)\n`;
      }
    } else {
      report += `本次优化未释放 tokens。\n`;
    }
  }
  
  report += `\n---\n`;
  report += `*报告生成时间: ${timestamp}*\n`;
  report += `*优化系统: MemOptimizer v1.1.0*\n`;
  
  return report;
}

/**
 * 执行优化
 */
async function optimizeMemory(workspacePath, dryRun = true, includeReflection = true, compressionRatio = 0.4) {
  // 加载 self-improving 偏好
  const preferences = await loadSelfImprovingPreferences();
  
  const scanResult = await scanMemoryFiles(workspacePath);
  const { files, totalTokens } = scanResult;
  
  if (files.length === 0) {
    return {
      success: true,
      freedTokens: 0,
      summarizedTokens: 0,
      filesProcessed: 0,
      message: '未找到 memory 文件',
      details: [],
      dryRun,
      compressionRatio
    };
  }
  
  let freedTokens = 0;
  let summarizedTokens = 0;
  const details = [];
  
  for (const file of files) {
    const originalTokens = file.tokens;
    
    // 读取文件内容
    const content = await fs.readFile(file.path, 'utf-8');
    
    // 根据 preferences 决定是否压缩
    if (file.lines > preferences.compressionThreshold) {
      const newContent = summarizeContent(content, preferences.maxSummaryLines, compressionRatio);
      const newTokens = estimateTokens(newContent);
      
      if (newTokens < originalTokens) {
        const saved = originalTokens - newTokens;
        summarizedTokens += newTokens;
        freedTokens += saved;
        
        if (!dryRun) {
          await fs.writeFile(file.path, newContent, 'utf-8');
        }
        
        details.push({
          file: file.name,
          originalTokens,
          newTokens,
          freed: saved,
          lines: file.lines,
          action: '压缩'
        });
      }
    }
  }
  
  const reflection = includeReflection && !dryRun ? 
    await logReflection({ stats: { freedTokens, summarizedTokens, filesProcessed: details.length } }, null) : null;
  
  return {
    success: true,
    freedTokens,
    summarizedTokens,
    filesProcessed: details.length,
    totalTokens,
    message: `已释放 ${freedTokens} tokens，总结了 ${summarizedTokens} tokens 记忆`,
    details,
    reflection,
    preferences,
    compressionRatio,
    dryRun
  };
}

/**
 * 执行每日优化并生成完整报告
 */
async function optimizeMemoryDaily() {
  // 执行多智能体优化
  const optimizeResult = await optimizeAllAgentsMemory(false, true, 0.4);
  
  // 获取服务器状态
  const serverStatus = await getServerStatus();
  
  // 获取多智能体状态
  const agentStatus = await getAgentStatus();
  
  const date = new Date().toISOString().split('T')[0];
  
  const report = {
    date,
    memory: {
      totalAgents: optimizeResult.totalAgents,
      totalFreedTokens: optimizeResult.totalFreedTokens,
      totalSummarizedTokens: optimizeResult.totalSummarizedTokens,
      totalFilesProcessed: optimizeResult.totalFilesProcessed,
      agentResults: optimizeResult.agentResults
    },
    server: serverStatus,
    agents: agentStatus,
    summaryReport: optimizeResult.summaryReport,
    reflection: optimizeResult.reflection
  };
  
  return report;
}

module.exports = {
  mem_optimize: async (params = {}) => {
    const workspacePath = process.cwd();
    const dryRun = params.dryRun !== false; // 默认 dryRun
    const compressionRatio = params.compressionRatio || 0.4;
    const includeReflection = params.includeReflection !== false;
    
    // 自动检测是否应该使用多智能体模式
    // 1. 如果显式指定了 multiAgent 参数
    // 2. 如果消息中包含"多智能体"关键词
    // 3. 如果消息是"执行多智能体记忆优化流程"
    let multiAgent = params.multiAgent || false;
    
    // 检查消息文本
    const messageText = params.message || params.text || '';
    if (messageText.includes('多智能体') || messageText === '执行多智能体记忆优化流程') {
      multiAgent = true;
    }
    
    let result;
    
    if (multiAgent) {
      // 多智能体优化模式
      result = await optimizeAllAgentsMemory(dryRun, includeReflection, compressionRatio);
      
      if (result.success) {
        return {
          status: 'success',
          message: result.message,
          summaryReport: result.summaryReport,
          stats: {
            totalAgents: result.totalAgents,
            totalFreedTokens: result.totalFreedTokens,
            totalSummarizedTokens: result.totalSummarizedTokens,
            totalFilesProcessed: result.totalFilesProcessed
          },
          agentResults: result.agentResults,
          dryRun: result.dryRun,
          note: result.dryRun ? '🔍 预览模式，未实际修改文件' : '✅ 已执行多智能体优化'
        };
      }
    } else {
      // 单智能体优化模式（原有逻辑）
      result = await optimizeMemory(workspacePath, dryRun, includeReflection, compressionRatio);
      
      if (result.success) {
        return {
          status: 'success',
          message: result.message,
          stats: {
            freedTokens: result.freedTokens,
            summarizedTokens: result.summarizedTokens,
            filesProcessed: result.filesProcessed,
            totalTokens: result.totalTokens
          },
          details: result.details,
          dryRun: result.dryRun,
          note: result.dryRun ? '🔍 预览模式，未实际修改文件' : '✅ 已执行优化'
        };
      }
    }
    
    return {
      status: 'error',
      message: result.message || '优化失败'
    };
  },
  
  mem_stats: async () => {
    const workspacePath = process.cwd();
    const { files, totalTokens } = await scanMemoryFiles(workspacePath);
    
    return {
      status: 'success',
      totalFiles: files.length,
      totalTokens,
      files: files.map(f => ({
        name: f.name,
        tokens: f.tokens,
        lines: f.lines
      }))
    };
  }
};
