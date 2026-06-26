#!/usr/bin/env node

/**
 * Parallel Responder - Progress Reporter
 * 
 * 进度汇报器，定期向用户汇报任务进展
 */

class ProgressReporter {
  constructor(config = {}) {
    this.config = {
      format: 'markdown',
      includeETA: true,
      includeSteps: true,
      ...config
    };

    // 活跃汇报
    this.activeReports = new Map();
  }

  /**
   * 生成进度汇报消息
   * @param {Object} options - 汇报选项
   * @returns {string} 格式化的汇报消息
   */
  generateReport(options) {
    const {
      taskId,
      percentage,
      currentStep,
      completedSteps = [],
      remainingSteps = [],
      eta,
      message
    } = options;

    let report = '';

    // 进度条
    report += `📊 进度汇报：${percentage}%\n\n`;

    // 进度条可视化
    report += this.createProgressBar(percentage) + '\n\n';

    // 当前步骤
    if (currentStep) {
      report += `**当前步骤：** ${currentStep}\n`;
    }

    // 已完成
    if (completedSteps.length > 0) {
      report += `\n**已完成：**\n`;
      completedSteps.forEach(step => {
        report += `✅ ${step}\n`;
      });
    }

    // 预计剩余
    if (this.config.includeETA && eta) {
      report += `\n**预计剩余：** ${eta.remaining}秒`;
    }

    // 提示信息
    report += `\n\n你可以继续问我其他问题，我会在 ${this.config.interval || 10} 秒后再次汇报。`;

    return report;
  }

  /**
   * 创建进度条
   */
  createProgressBar(percentage) {
    const totalBars = 20;
    const filledBars = Math.floor((percentage / 100) * totalBars);
    const emptyBars = totalBars - filledBars;

    return '[' + '█'.repeat(filledBars) + '░'.repeat(emptyBars) + ']';
  }

  /**
   * 生成完成汇报
   */
  generateCompletionReport(options) {
    const {
      taskId,
      totalTime,
      result,
      summary
    } = options;

    let report = '';

    report += `✅ 任务完成！\n\n`;

    if (totalTime) {
      report += `**实际耗时：** ${totalTime}秒\n`;
    }

    if (summary) {
      report += `\n**总结：**\n${summary}\n`;
    }

    if (result) {
      report += `\n**结果：**\n${result}\n`;
    }

    return report;
  }

  /**
   * 开始定期汇报
   */
  startPeriodicReporting(taskId, config) {
    const {
      interval = 10,
      onReport,
      onComplete
    } = config;

    const reportInterval = setInterval(() => {
      // 这里应该调用 onReport 获取最新进度
      // 简化处理，实际实现需要从任务获取进度
      onReport && onReport();
    }, interval * 1000);

    this.activeReports.set(taskId, {
      interval: reportInterval,
      config
    });

    return reportInterval;
  }

  /**
   * 停止定期汇报
   */
  stopReporting(taskId) {
    const report = this.activeReports.get(taskId);
    if (!report) return;

    clearInterval(report.interval);
    this.activeReports.delete(taskId);
  }

  /**
   * 停止所有汇报
   */
  stopAllReporting() {
    this.activeReports.forEach((report, taskId) => {
      clearInterval(report.interval);
    });
    this.activeReports.clear();
  }

  /**
   * 获取活跃汇报列表
   */
  getActiveReports() {
    return Array.from(this.activeReports.keys());
  }
}

// Export for use as module
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ProgressReporter;
}

// CLI usage
if (require.main === module) {
  const reporter = new ProgressReporter();
  
  // 测试进度汇报
  const report = reporter.generateReport({
    taskId: 'test_123',
    percentage: 60,
    currentStep: '正在更新情感记忆',
    completedSteps: ['读取 daily 文件', '提取关键信息'],
    remainingSteps: ['更新知识库', '归档文件'],
    eta: { remaining: 15 }
  });

  console.log('📊 进度汇报示例:');
  console.log(report);
}
