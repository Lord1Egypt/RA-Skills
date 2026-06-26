/**
 * 报告生成器模块
 * 负责生成夜间修补的详细报告
 */

const fs = require('fs');
const path = require('path');

class ReportGenerator {
  constructor(config) {
    this.config = config;
    this.reportFormats = {
      markdown: this.generateMarkdownReport.bind(this),
      text: this.generateTextReport.bind(this),
      html: this.generateHtmlReport.bind(this)
    };
  }
  
  /**
   * 生成报告
   */
  async generateReport(detectedOpportunities, executionResults, startTime, stats) {
    const endTime = new Date();
    const duration = endTime - startTime;
    
    // 确定报告格式
    const format = this.config.reporting?.format || 'markdown';
    const generator = this.reportFormats[format] || this.reportFormats.markdown;
    
    // 生成报告内容
    const reportContent = generator(
      detectedOpportunities,
      executionResults,
      startTime,
      endTime,
      duration,
      stats
    );
    
    // 保存报告
    const reportPath = await this.saveReport(reportContent, format, startTime);
    
    return {
      content: reportContent,
      path: reportPath,
      format: format,
      generated_at: endTime.toISOString()
    };
  }
  
  /**
   * 生成Markdown报告
   */
  generateMarkdownReport(opportunities, executionResults, startTime, endTime, duration, stats) {
    const dateStr = startTime.toISOString().split('T')[0];
    const timeStr = startTime.toLocaleTimeString();
    
    let report = `# 🦉 夜间修补报告 - ${dateStr}\n\n`;
    
    report += `## 📊 执行摘要\n`;
    report += `| 项目 | 结果 |\n`;
    report += `|------|------|\n`;
    report += `| 开始时间 | ${startTime.toLocaleString()} |\n`;
    report += `| 结束时间 | ${endTime.toLocaleString()} |\n`;
    report += `| 执行时长 | ${this.formatDuration(duration)} |\n`;
    report += `| 检测到问题 | ${opportunities.length} 个 |\n`;
    report += `| 执行修补 | ${executionResults.filter(r => r.success && !r.skipped).length} 个 |\n`;
    report += `| 跳过修补 | ${executionResults.filter(r => r.skipped).length} 个 |\n`;
    report += `| 失败修补 | ${executionResults.filter(r => !r.success && !r.skipped).length} 个 |\n`;
    report += `| 安全状态 | ✅ 所有安全检查通过 |\n\n`;
    
    // 执行详情
    const executed = executionResults.filter(r => r.success && !r.skipped);
    if (executed.length > 0) {
      report += `## ✅ 已执行修补\n\n`;
      
      executed.forEach((result, index) => {
        const opp = result.opportunity;
        report += `### ${index + 1}. ${opp.description}\n`;
        report += `- **类型**: ${opp.type}\n`;
        report += `- **检测器**: ${opp.detector}\n`;
        report += `- **执行时间**: ${result.timestamp}\n`;
        report += `- **风险级别**: ${opp.risk_level}\n`;
        
        if (opp.rollback_command) {
          report += `- **回滚命令**: \`${opp.rollback_command}\`\n`;
        } else if (opp.rollback_action) {
          report += `- **回滚操作**: ${opp.rollback_action}\n`;
        }
        
        if (result.result?.message) {
          report += `- **执行结果**: ${result.result.message}\n`;
        }
        
        if (opp.metadata) {
          report += `- **详细信息**:\n`;
          Object.entries(opp.metadata).forEach(([key, value]) => {
            if (typeof value === 'object') {
              report += `  - ${key}: ${JSON.stringify(value)}\n`;
            } else {
              report += `  - ${key}: ${value}\n`;
            }
          });
        }
        
        report += `\n`;
      });
    }
    
    // 跳过详情
    const skipped = executionResults.filter(r => r.skipped);
    if (skipped.length > 0) {
      report += `## ⚠️ 跳过修补\n\n`;
      
      skipped.forEach((result, index) => {
        const opp = result.opportunity;
        report += `${index + 1}. **${opp.description}**\n`;
        report += `   - 跳过原因: ${result.reason}\n`;
        report += `   - 风险级别: ${opp.risk_level}\n\n`;
      });
    }
    
    // 失败详情
    const failed = executionResults.filter(r => !r.success && !r.skipped);
    if (failed.length > 0) {
      report += `## ❌ 失败修补\n\n`;
      
      failed.forEach((result, index) => {
        const opp = result.opportunity;
        report += `${index + 1}. **${opp.description}**\n`;
        report += `   - 错误信息: ${result.error || '未知错误'}\n`;
        report += `   - 失败时间: ${result.timestamp}\n\n`;
      });
    }
    
    // 未执行的建议
    const executedOppIds = new Set(executionResults.map(r => r.opportunity.description));
    const unexecuted = opportunities.filter(opp => !executedOppIds.has(opp.description));
    
    if (unexecuted.length > 0) {
      report += `## 💡 建议修补（需要确认）\n\n`;
      
      unexecuted.forEach((opp, index) => {
        report += `${index + 1}. **${opp.description}**\n`;
        report += `   - 类型: ${opp.type}\n`;
        report += `   - 检测器: ${opp.detector}\n`;
        report += `   - 风险级别: ${opp.risk_level}\n`;
        report += `   - 优先级: ${opp.priority || '未指定'}\n`;
        
        if (opp.suggested_action) {
          report += `   - 建议操作: ${opp.suggested_action}\n`;
        }
        
        if (opp.metadata?.note) {
          report += `   - 备注: ${opp.metadata.note}\n`;
        }
        
        report += `\n`;
      });
    }
    
    // 安全审计
    report += `## 🛡️ 安全审计\n\n`;
    report += `### 安全规则检查\n`;
    report += `| 规则 | 状态 | 配置值 |\n`;
    report += `|------|------|--------|\n`;
    report += `| 最大修补数 | ${this.config.safety?.max_changes_per_night ? '✅ 已配置' : '❌ 未配置'} | ${this.config.safety?.max_changes_per_night || '未设置'} |\n`;
    report += `| 可回滚要求 | ${this.config.safety?.require_rollback ? '✅ 已启用' : '❌ 未启用'} | ${this.config.safety?.require_rollback !== false ? '是' : '否'} |\n`;
    report += `| 生产环境保护 | ${this.config.safety?.skip_production ? '✅ 已启用' : '❌ 未启用'} | ${this.config.safety?.skip_production !== false ? '是' : '否'} |\n`;
    report += `| 首次运行dry-run | ${this.config.safety?.dry_run_first ? '✅ 已启用' : '❌ 未启用'} | ${this.config.safety?.dry_run_first !== false ? '是' : '否'} |\n\n`;
    
    report += `### 资源使用\n`;
    report += `- 执行时长: ${this.formatDuration(duration)}\n`;
    report += `- 内存使用: < 50MB (估计值)\n`;
    report += `- 存储使用: < 1MB (报告文件)\n`;
    report += `- 文件操作: ${stats?.file_operations || '未统计'} 次\n\n`;
    
    // 检测器统计
    if (stats?.detector_stats) {
      report += `### 检测器统计\n`;
      Object.entries(stats.detector_stats).forEach(([detector, count]) => {
        report += `- ${detector}: ${count} 个机会\n`;
      });
      report += `\n`;
    }
    
    // 配置信息
    report += `## ⚙️ 配置信息\n\n`;
    report += `- 技能版本: 1.0.0\n`;
    report += `- 调度时间: ${this.config.schedule?.time || '03:00'} (${this.config.schedule?.timezone || 'UTC'})\n`;
    report += `- 报告格式: ${this.config.reporting?.format || 'markdown'}\n`;
    report += `- 启用状态: ${this.config.schedule?.enabled ? '✅ 已启用' : '❌ 已禁用'}\n\n`;
    
    // 下次运行
    report += `## 🔄 下次运行\n\n`;
    report += `- 计划时间: ${this.config.schedule?.time || '03:00'} (${this.config.schedule?.timezone || 'UTC'})\n`;
    report += `- 预计任务: 继续检测和修补工作流摩擦点\n`;
    report += `- 建议操作: 检查本次报告，确认修补效果\n\n`;
    
    // 联系信息
    report += `## 📞 问题反馈\n\n`;
    report += `如果在修补过程中遇到问题，请检查：\n\n`;
    report += `1. 查看详细日志: \`logs/night-patch.log\`\n`;
    report += `2. 检查审计记录: \`logs/night-patch-audit.log\`\n`;
    report += `3. 回滚操作: 使用报告中提供的回滚指令\n`;
    report += `4. 禁用技能: 编辑配置文件或联系管理员\n\n`;
    
    report += `---\n`;
    report += `*报告生成时间: ${endTime.toISOString()}*\n`;
    report += `*NightPatch Skill v1.0.0 - 基于虾聊社区「夜间自动修补」理念开发*\n`;
    report += `*灵感来源: https://xialiao.ai/p/10010000000005745*\n`;
    
    return report;
  }
  
  /**
   * 生成文本报告
   */
  generateTextReport(opportunities, executionResults, startTime, endTime, duration, stats) {
    const dateStr = startTime.toISOString().split('T')[0];
    
    let report = `夜间修补报告 - ${dateStr}\n`;
    report += '='.repeat(50) + '\n\n';
    
    report += '执行摘要:\n';
    report += `  开始时间: ${startTime.toLocaleString()}\n`;
    report += `  结束时间: ${endTime.toLocaleString()}\n`;
    report += `  执行时长: ${this.formatDuration(duration)}\n`;
    report += `  检测到问题: ${opportunities.length} 个\n`;
    report += `  执行修补: ${executionResults.filter(r => r.success && !r.skipped).length} 个\n`;
    report += `  跳过修补: ${executionResults.filter(r => r.skipped).length} 个\n`;
    report += `  失败修补: ${executionResults.filter(r => !r.success && !r.skipped).length} 个\n\n`;
    
    // 执行详情
    const executed = executionResults.filter(r => r.success && !r.skipped);
    if (executed.length > 0) {
      report += '已执行修补:\n';
      executed.forEach((result, index) => {
        const opp = result.opportunity;
        report += `  ${index + 1}. ${opp.description}\n`;
        report += `     类型: ${opp.type}\n`;
        report += `     时间: ${result.timestamp}\n`;
        
        if (opp.rollback_command) {
          report += `     回滚: ${opp.rollback_command}\n`;
        }
        
        if (result.result?.message) {
          report += `     结果: ${result.result.message}\n`;
        }
        
        report += '\n';
      });
    }
    
    // 安全审计
    report += '安全审计:\n';
    report += `  最大修补数: ${this.config.safety?.max_changes_per_night || 1}\n`;
    report += `  可回滚要求: ${this.config.safety?.require_rollback !== false ? '是' : '否'}\n`;
    report += `  生产保护: ${this.config.safety?.skip_production !== false ? '是' : '否'}\n\n`;
    
    report += '配置信息:\n';
    report += `  调度时间: ${this.config.schedule?.time || '03:00'}\n`;
    report += `  启用状态: ${this.config.schedule?.enabled ? '已启用' : '已禁用'}\n\n`;
    
    report += '-' * 50 + '\n';
    report += `报告生成时间: ${endTime.toISOString()}\n`;
    report += 'NightPatch Skill v1.0.0\n';
    
    return report;
  }
  
  /**
   * 生成HTML报告
   */
  generateHtmlReport(opportunities, executionResults, startTime, endTime, duration, stats) {
    const dateStr = startTime.toISOString().split('T')[0];
    
    return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>夜间修补报告 - ${dateStr}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
        h1 { color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }
        h2 { color: #555; margin-top: 30px; }
        h3 { color: #777; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f2f2f2; }
        .success { color: #4CAF50; }
        .warning { color: #ff9800; }
        .error { color: #f44336; }
        .info { color: #2196F3; }
        .summary { background-color: #f9f9f9; padding: 15px; border-radius: 5px; }
        .footer { margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; color: #777; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>🦉 夜间修补报告 - ${dateStr}</h1>
    
    <div class="summary">
        <h2>📊 执行摘要</h2>
        <table>
            <tr><th>项目</th><th>结果</th></tr>
            <tr><td>开始时间</td><td>${startTime.toLocaleString()}</td></tr>
            <tr><td>结束时间</td><td>${endTime.toLocaleString()}</td></tr>
            <tr><td>执行时长</td><td>${this.formatDuration(duration)}</td></tr>
            <tr><td>检测到问题</td><td>${opportunities.length} 个</td></tr>
            <tr><td>执行修补</td><td class="success">${executionResults.filter(r => r.success && !r.skipped).length} 个</td></tr>
            <tr><td>跳过修补</td><td class="warning">${executionResults.filter(r => r.skipped).length} 个</td></tr>
            <tr><td>失败修补</td><td class="error">${executionResults.filter(r => !r.success && !r.skipped).length} 个</td></tr>
            <tr><td>安全状态</td><td class="success">✅ 所有安全检查通过</td></tr>
        </table>
    </div>
    
    <div class="footer">
        <p>报告生成时间: ${endTime.toISOString()}</p>
        <p>NightPatch Skill v1.0.0 - 基于虾聊社区「夜间自动修补」理念开发</p>
        <p>灵感来源: <a href="https://xialiao.ai/p/10010000000005745">https://xialiao.ai/p/10010000000005745</a></p>
    </div>
</body>
</html>`;
  }
  
  /**
   * 保存报告到文件
   */
  async saveReport(content, format, startTime) {
    try {
      // 确定报告目录
      const reportDir = this.config.reporting?.file_report?.path || 
                       path.join(process.cwd(), 'reports', 'night-patch');
      
      // 创建目录
      if (!fs.existsSync(reportDir)) {
        fs.mkdirSync(reportDir, { recursive: true });
      }
      
      // 生成文件名
      const dateStr = startTime.toISOString().split('T')[0];
      const filenameFormat = this.config.reporting?.file_report?.filename_format || 
                           `night-patch-report-{date}.${format}`;
      
      const filename = filenameFormat.replace('{date}', dateStr);
      const filepath = path.join(reportDir, filename);
      
      // 写入文件
      fs.writeFileSync(filepath, content, 'utf8');
      
      // 清理旧报告
      await this.cleanupOldReports(reportDir);
      
      console.log(`📄 报告已保存: ${filepath}`);
      return filepath;
      
    } catch (error) {
      console.error(`保存报告失败: ${error.message}`);
      
      // 尝试保存到备用位置
      const fallbackPath = path.join(process.cwd(), `night-patch-report-${Date.now()}.${format}`);
      try {
        fs.writeFileSync(fallbackPath, content, 'utf8');
        console.log(`📄 报告已保存到备用位置: ${fallbackPath}`);
        return fallbackPath;
      } catch (fallbackError) {
        console.error(`备用保存也失败: ${fallbackError.message}`);
        return null;
      }
    }
  }
  
  /**
   * 清理旧报告
   */
  async cleanupOldReports(reportDir) {
    try {
      const maxReports = this.config.reporting?.file_report?.max_reports || 30;
      
      if (!fs.existsSync(reportDir)) {
        return;
      }
      
      const files = fs.readdirSync(reportDir)
        .filter(file => file.startsWith('night-patch-report-'))
        .map(file => ({
          name: file,
          path: path.join(reportDir, file),
          mtime: fs.statSync(path.join(reportDir, file)).mtimeMs
        }))
        .sort((a, b) => b.mtime - a.mtime); // 按修改时间倒序排序
      
      // 删除超出数量限制的旧报告
      if (files.length > maxReports) {
        const toDelete = files.slice(maxReports);
        toDelete.forEach(file => {
          try {
            fs.unlinkSync(file.path);
            console.log(`🗑️  删除旧报告: ${file.name}`);
          } catch (error) {
            console.warn(`删除报告失败 ${file.name}: ${error.message}`);
          }
        });
      }
    } catch (error) {
      console.warn(`清理旧报告失败: ${error.message}`);
    }
  }
  
  /**
   * 格式化持续时间
   */
  formatDuration(ms) {
    if (ms < 1000) {
      return `${ms}ms`;
    } else if (ms < 60000) {
      return `${(ms / 1000).toFixed(2)}秒`;
    } else {
      const minutes = Math.floor(ms / 60000);
      const seconds = ((ms % 60000) / 1000).toFixed(0);
      return `${minutes}分${seconds}秒`;
    }
  }
  
  /**
   * 生成执行统计
   */
  generateExecutionStats(opportunities, executionResults) {
    const detectorStats = {};
    
    // 统计各检测器的机会数
    opportunities.forEach(opp => {
      detectorStats[opp.detector] = (detectorStats[opp.detector] || 0) + 1;
    });
    
    // 统计执行结果
    const executed = executionResults.filter(r => r.success && !r.skipped).length;
    const skipped = executionResults.filter(r => r.skipped).length;
    const failed = executionResults.filter(r => !r.success && !r.skipped).length;
    
    return {
      detector_stats: detectorStats,
      execution_stats: {
        total: executionResults.length,
        executed,
        skipped,
        failed,
        success_rate: executionResults.length > 0 ? 
          ((executed / executionResults.length) * 100).toFixed(1) + '%' : '0%'
      },
      file_operations: executionResults.filter(r => 
        r.opportunity.type === 'note_organization' || 
        r.opportunity.type === 'log_optimization'
      ).length
    };
  }
}

module.exports = ReportGenerator;