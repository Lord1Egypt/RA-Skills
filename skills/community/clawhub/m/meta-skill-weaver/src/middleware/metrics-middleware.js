/**
 * MetricsMiddleware - 性能指标收集 + 自优化触发机制
 *
 * v2.4.0 新增：
 * - 任务失败率自动分析，超过阈值时触发优化建议
 * - 重试策略自动调整（基于历史失败模式）
 * - 指标持久化与趋势分析
 *
 * @module middleware/metrics-middleware
 */

const fs = require('fs');
const path = require('path');

// ─── 默认配置 ────────────────────────────────────────────

const DEFAULT_CONFIG = {
  // 失败率阈值：超过此比例触发优化建议
  failureRateThreshold: 0.25,
  // 连续失败次数：连续失败超过此次数触发优化
  consecutiveFailureThreshold: 3,
  // 指标存储路径
  storagePath: path.join(__dirname, '../../.metrics'),
  // 优化建议最大缓存数
  maxSuggestionHistory: 50,
  // 重试策略配置
  retry: {
    baseDelay: 1000,       // 基础延迟 (ms)
    maxRetries: 5,          // 最大重试次数
    backoffMultiplier: 2,   // 退避倍数
    maxDelay: 30000,        // 最大延迟 (ms)
  },
  // 触发回调
  onOptimizationTriggered: null,
};

// ─── MetricsMiddleware 类 ────────────────────────────────

class MetricsMiddleware {
  constructor(config = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.metrics = {
      totalTasks: 0,
      completedTasks: 0,
      failedTasks: 0,
      pausedTasks: 0,
      cancelledTasks: 0,
      // 子技能调用指标
      skillCalls: {},       // { skillName: { total, success, failed, avgLatency } }
      // 时间序列指标（用于趋势分析）
      timeSeries: [],       // [{ timestamp, failureRate, avgLatency }]
      // 优化建议历史
      suggestions: [],
    };
    this._retryStrategies = new Map();  // taskId -> retry config
    this._consecutiveFailures = new Map(); // skillName -> count
    this._initStorage();
  }

  // ── 初始化存储 ──────────────────────────────────────────

  _initStorage() {
    const dir = this.config.storagePath;
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    // 加载持久化指标
    const metricsFile = path.join(dir, 'metrics.json');
    if (fs.existsSync(metricsFile)) {
      try {
        const saved = JSON.parse(fs.readFileSync(metricsFile, 'utf-8'));
        this.metrics = { ...this.metrics, ...saved };
      } catch (e) {
        // 忽略损坏的存储文件
      }
    }
  }

  // ── 持久化 ──────────────────────────────────────────────

  save() {
    const metricsFile = path.join(this.config.storagePath, 'metrics.json');
    fs.writeFileSync(metricsFile, JSON.stringify(this.metrics, null, 2));
  }

  // ── 中间件接口：execute ─────────────────────────────────

  /**
   * Middleware 标准接口
   * @param {object} context - 任务上下文
   * @param {function} next - 下一个中间件
   */
  async execute(context, next) {
    const startTime = Date.now();
    const skillName = context.skillName || 'unknown';

    try {
      const result = await next(context);
      const latency = Date.now() - startTime;

      // 记录成功
      this.recordSuccess(context.taskId, skillName, latency);

      // 重置连续失败计数
      this._consecutiveFailures.set(skillName, 0);

      return result;
    } catch (error) {
      const latency = Date.now() - startTime;

      // 记录失败
      this.recordFailure(context.taskId, skillName, error, latency);

      // 检查是否需要触发优化
      const analysis = this.analyzeAndOptimize(skillName);

      // 自动调整重试策略
      const retryConfig = this.getAdaptiveRetryConfig(skillName);

      // 如果需要重试且有重试次数剩余
      if (retryConfig.shouldRetry && context.retryCount < retryConfig.maxRetries) {
        const delay = this._calculateBackoff(skillName, context.retryCount);
        context.retryDelay = delay;
        context.retryConfig = retryConfig;
      }

      throw Object.assign(error, {
        metricsAnalysis: analysis,
        retryConfig,
      });
    }
  }

  // ── 指标记录 ────────────────────────────────────────────

  recordSuccess(taskId, skillName, latency) {
    this.metrics.totalTasks++;
    this.metrics.completedTasks++;
    this._recordSkillCall(skillName, { success: true, latency });
    this._addTimeSeriesPoint();
    this.save();
  }

  recordFailure(taskId, skillName, error, latency) {
    this.metrics.totalTasks++;
    this.metrics.failedTasks++;
    this._recordSkillCall(skillName, { success: false, latency, error: error?.message });

    // 更新连续失败计数
    const prev = this._consecutiveFailures.get(skillName) || 0;
    this._consecutiveFailures.set(skillName, prev + 1);

    this._addTimeSeriesPoint();
    this.save();
  }

  recordPause(taskId) {
    this.metrics.pausedTasks++;
    this.save();
  }

  recordCancel(taskId) {
    this.metrics.cancelledTasks++;
    this.save();
  }

  // ── 内部：记录技能调用 ──────────────────────────────────

  _recordSkillCall(skillName, { success, latency, error }) {
    if (!this.metrics.skillCalls[skillName]) {
      this.metrics.skillCalls[skillName] = {
        total: 0, success: 0, failed: 0, totalLatency: 0,
      };
    }
    const call = this.metrics.skillCalls[skillName];
    call.total++;
    if (success) {
      call.success++;
    } else {
      call.failed++;
    }
    call.totalLatency += latency;
  }

  // ── 内部：添加时间序列点 ────────────────────────────────

  _addTimeSeriesPoint() {
    const failureRate = this.metrics.totalTasks > 0
      ? this.metrics.failedTasks / this.metrics.totalTasks
      : 0;
    const avgLatency = this._getOverallAvgLatency();

    this.metrics.timeSeries.push({
      timestamp: new Date().toISOString(),
      failureRate: Math.round(failureRate * 1000) / 1000,
      avgLatency: Math.round(avgLatency),
    });

    // 保留最近 100 个点
    if (this.metrics.timeSeries.length > 100) {
      this.metrics.timeSeries = this.metrics.timeSeries.slice(-100);
    }
  }

  _getOverallAvgLatency() {
    let totalLatency = 0;
    let totalCalls = 0;
    for (const skill of Object.values(this.metrics.skillCalls)) {
      totalLatency += skill.totalLatency;
      totalCalls += skill.total;
    }
    return totalCalls > 0 ? totalLatency / totalCalls : 0;
  }

  // ── 核心：分析并优化 ────────────────────────────────────

  /**
   * 分析当前指标，当失败率超过阈值时触发优化建议
   * @param {string} skillName - 可选，只分析特定技能
   * @returns {object} 分析结果
   */
  analyzeAndOptimize(skillName) {
    const analysis = {
      overall: this._analyzeOverall(),
      bySkill: skillName ? this._analyzeSkill(skillName) : null,
      suggestions: [],
      triggered: false,
      timestamp: new Date().toISOString(),
    };

    // 检查总体失败率
    if (analysis.overall.failureRate > this.config.failureRateThreshold) {
      analysis.triggered = true;
      analysis.suggestions.push({
        type: 'HIGH_FAILURE_RATE',
        severity: 'warning',
        message: `总体失败率 ${analysis.overall.failureRatePercent}% 超过阈值 ${this.config.failureRateThreshold * 100}%`,
        action: 'review_failed_tasks',
      });
    }

    // 检查特定技能
    if (analysis.bySkill && analysis.bySkill.failureRate > this.config.failureRateThreshold) {
      analysis.triggered = true;
      analysis.suggestions.push({
        type: 'SKILL_FAILURE_RATE',
        severity: 'critical',
        skillName,
        message: `技能 "${skillName}" 失败率 ${analysis.bySkill.failureRatePercent}% 超过阈值`,
        action: 'review_skill_config',
      });
    }

    // 检查连续失败
    if (skillName) {
      const consecutive = this._consecutiveFailures.get(skillName) || 0;
      if (consecutive >= this.config.consecutiveFailureThreshold) {
        analysis.triggered = true;
        analysis.suggestions.push({
          type: 'CONSECUTIVE_FAILURES',
          severity: 'critical',
          skillName,
          message: `技能 "${skillName}" 连续失败 ${consecutive} 次`,
          action: 'increase_retry_backoff',
        });
      }
    }

    // 缓存优化建议
    if (analysis.suggestions.length > 0) {
      this.metrics.suggestions.push(analysis);
      if (this.metrics.suggestions.length > this.config.maxSuggestionHistory) {
        this.metrics.suggestions = this.metrics.suggestions.slice(-this.config.maxSuggestionHistory);
      }
      this.save();
    }

    // 触发回调
    if (analysis.triggered && this.config.onOptimizationTriggered) {
      this.config.onOptimizationTriggered(analysis);
    }

    return analysis;
  }

  _analyzeOverall() {
    const total = this.metrics.totalTasks;
    const failed = this.metrics.failedTasks;
    const failureRate = total > 0 ? failed / total : 0;

    return {
      totalTasks: total,
      completedTasks: this.metrics.completedTasks,
      failedTasks: failed,
      failureRate: Math.round(failureRate * 1000) / 1000,
      failureRatePercent: (failureRate * 100).toFixed(1) + '%',
      avgLatency: Math.round(this._getOverallAvgLatency()),
    };
  }

  _analyzeSkill(skillName) {
    const call = this.metrics.skillCalls[skillName];
    if (!call || call.total === 0) {
      return { total: 0, failureRate: 0, failureRatePercent: '0.0%' };
    }

    return {
      total: call.total,
      success: call.success,
      failed: call.failed,
      failureRate: Math.round((call.failed / call.total) * 1000) / 1000,
      failureRatePercent: ((call.failed / call.total) * 100).toFixed(1) + '%',
      avgLatency: Math.round(call.totalLatency / call.total),
    };
  }

  // ── 核心：自适应重试策略 ────────────────────────────────

  /**
   * 根据历史失败模式自动调整重试策略
   * @param {string} skillName - 技能名称
   * @returns {object} 调整后的重试配置
   */
  getAdaptiveRetryConfig(skillName) {
    const call = this.metrics.skillCalls[skillName];
    const consecutive = this._consecutiveFailures.get(skillName) || 0;

    // 默认配置
    let config = { ...this.config.retry };

    if (call && call.total > 0) {
      const failureRate = call.failed / call.total;

      if (failureRate > 0.5) {
        // 高失败率：增加最大重试次数，延长退避
        config.maxRetries = Math.min(config.maxRetries + 2, 8);
        config.backoffMultiplier = Math.min(config.backoffMultiplier + 0.5, 4);
      } else if (failureRate > 0.3) {
        // 中等失败率：适度增加
        config.maxRetries = Math.min(config.maxRetries + 1, 6);
      } else if (failureRate < 0.05 && call.total > 10) {
        // 低失败率且有足够样本：减少重试以节省资源
        config.maxRetries = Math.max(config.maxRetries - 1, 2);
      }
    }

    // 连续失败：激进退避
    if (consecutive >= 3) {
      config.backoffMultiplier = Math.min(config.backoffMultiplier + consecutive * 0.5, 4);
      config.baseDelay = Math.min(config.baseDelay * consecutive, 10000);
    }

    // 决定是否应该重试
    const shouldRetry = consecutive < config.maxRetries;

    return { ...config, shouldRetry, consecutiveFailures: consecutive };
  }

  // ── 内部：计算退避延迟 ──────────────────────────────────

  _calculateBackoff(skillName, retryCount) {
    const config = this.getAdaptiveRetryConfig(skillName);
    const delay = config.baseDelay * Math.pow(config.backoffMultiplier, retryCount);
    // 添加随机抖动避免 thundering herd
    const jitter = Math.random() * delay * 0.1;
    return Math.min(delay + jitter, config.maxDelay);
  }

  // ── 查询接口 ────────────────────────────────────────────

  /**
   * 获取指标报告
   * @returns {object} 完整指标报告
   */
  getReport() {
    return {
      summary: this._analyzeOverall(),
      skills: Object.keys(this.metrics.skillCalls).reduce((acc, name) => {
        acc[name] = this._analyzeSkill(name);
        return acc;
      }, {}),
      recentSuggestions: this.metrics.suggestions.slice(-5),
      timestamp: new Date().toISOString(),
    };
  }

  /**
   * 获取趋势数据
   * @param {number} limit - 返回最近 N 个点
   * @returns {Array} 时间序列数据
   */
  getTrend(limit = 20) {
    return this.metrics.timeSeries.slice(-limit);
  }

  /**
   * 重置指标（用于测试或新版本部署）
   */
  reset() {
    this.metrics = {
      totalTasks: 0, completedTasks: 0, failedTasks: 0,
      pausedTasks: 0, cancelledTasks: 0,
      skillCalls: {}, timeSeries: [], suggestions: [],
    };
    this._consecutiveFailures.clear();
    this._retryStrategies.clear();
    this.save();
  }
}

module.exports = { MetricsMiddleware, DEFAULT_CONFIG };
