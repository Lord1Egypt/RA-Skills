#!/usr/bin/env node

/**
 * Parallel Responder - Parallel Executor
 * 
 * 并行执行器，根据任务类型选择执行策略
 */

const TaskClassifier = require('./task-classifier');
const TimeEstimator = require('./time-estimator');

class ParallelExecutor {
  constructor(config = {}) {
    this.classifier = new TaskClassifier(config.classification);
    this.estimator = new TimeEstimator(config.estimation);
    this.config = {
      reporting: {
        enabled: true,
        interval: 10
      },
      subAgent: {
        enabled: true,
        cleanup: 'keep'
      },
      ...config
    };

    // 当前执行的任务
    this.activeTasks = new Map();
  }

  /**
   * 执行任务
   * @param {string} message - 用户消息
   * @param {Object} context - 上下文
   * @returns {Promise<Object>} 执行结果
   */
  async execute(message, context = {}) {
    const startTime = Date.now();

    // 1. 任务分类
    const classification = this.classifier.classify(message);
    
    // 2. 时间预估
    const timeEstimate = this.estimator.estimate(
      classification.type,
      message,
      context
    );

    // 3. 根据策略执行
    let result;
    switch (classification.strategy) {
      case 'direct':
        result = await this.executeDirect(message, context);
        break;

      case 'execute-and-report':
        result = await this.executeWithReport(message, context, timeEstimate);
        break;

      case 'sub-agent':
        result = await this.executeWithSubAgent(message, context, timeEstimate);
        break;

      default:
        throw new Error(`Unknown strategy: ${classification.strategy}`);
    }

    // 4. 记录实际耗时
    const actualTime = (Date.now() - startTime) / 1000;
    this.estimator.recordActual(
      classification.type,
      timeEstimate.average,
      actualTime
    );

    return {
      classification,
      timeEstimate,
      actualTime,
      result
    };
  }

  /**
   * 直接执行（简单任务）
   */
  async executeDirect(message, context) {
    // 简单任务直接返回，由调用者执行
    return {
      strategy: 'direct',
      immediate: true,
      message: '直接执行'
    };
  }

  /**
   * 执行 + 汇报（中等任务）
   */
  async executeWithReport(message, context, timeEstimate) {
    // 立即回复
    const immediateResponse = `好的，开始处理，预计 ${timeEstimate.range}...`;

    // 这里应该由实际的任务执行器执行
    // 简化处理，返回执行标记
    return {
      strategy: 'execute-and-report',
      immediateResponse,
      estimatedTime: timeEstimate.range,
      willReportAfterComplete: true
    };
  }

  /**
   * 子 agent 执行（复杂任务）
   */
  async executeWithSubAgent(message, context, timeEstimate) {
    // 立即回复
    const immediateResponse = `好的，这个任务需要 ${timeEstimate.range}。

🚀 已启动子 agent 处理
⏱️ 预计耗时：${timeEstimate.range}
📊 当前进度：0%

你可以继续问我其他问题，我会每 ${this.config.reporting.interval} 秒汇报一次进度。`;

    // 启动子 agent（实际实现需要 sessions_spawn）
    const taskId = `task_${Date.now()}`;
    
    this.activeTasks.set(taskId, {
      message,
      context,
      startTime: Date.now(),
      estimatedTime: timeEstimate.average,
      status: 'running',
      progress: 0
    });

    return {
      strategy: 'sub-agent',
      immediateResponse,
      taskId,
      willReportPeriodically: true,
      reportInterval: this.config.reporting.interval
    };
  }

  /**
   * 更新任务进度
   */
  updateProgress(taskId, progress, message) {
    const task = this.activeTasks.get(taskId);
    if (!task) return;

    task.progress = progress;
    task.lastUpdate = Date.now();

    return {
      taskId,
      progress,
      message,
      eta: this.calculateETA(task)
    };
  }

  /**
   * 计算预计剩余时间
   */
  calculateETA(task) {
    const elapsed = (Date.now() - task.startTime) / 1000;
    const total = task.estimatedTime;
    const remaining = Math.max(0, total - elapsed);
    
    return {
      elapsed: Math.floor(elapsed),
      remaining: Math.floor(remaining),
      percent: Math.floor((elapsed / total) * 100)
    };
  }

  /**
   * 完成任务
   */
  completeTask(taskId, result) {
    const task = this.activeTasks.get(taskId);
    if (!task) return;

    task.status = 'completed';
    task.result = result;
    task.endTime = Date.now();

    const actualTime = (task.endTime - task.startTime) / 1000;

    return {
      taskId,
      status: 'completed',
      actualTime,
      result
    };
  }

  /**
   * 获取活跃任务列表
   */
  getActiveTasks() {
    return Array.from(this.activeTasks.entries()).map(([id, task]) => ({
      taskId: id,
      message: task.message,
      progress: task.progress,
      status: task.status,
      eta: this.calculateETA(task)
    }));
  }

  /**
   * 获取执行统计
   */
  getStats() {
    return {
      activeTasks: this.activeTasks.size,
      classifierStats: this.classifier.getStats(),
      estimatorStats: this.estimator.getStats()
    };
  }
}

// Export for use as module
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ParallelExecutor;
}

// CLI usage
if (require.main === module) {
  const executor = new ParallelExecutor();
  
  const message = process.argv.slice(2).join(' ');
  
  if (!message) {
    console.log('Usage: node parallel-executor.js <message>');
    console.log('Example: node parallel-executor.js "帮我整理记忆"');
    process.exit(1);
  }

  executor.execute(message).then(result => {
    console.log('🚀 执行结果:');
    console.log(JSON.stringify(result, null, 2));
  });
}
