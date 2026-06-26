/**
 * PeriodicNudge - P1-3 Periodic Nudge
 * 从被动纠正 → 主动自检
 * 
 * 核心思路：
 * 1. 周期性自检 - 检查规则违反、超时任务、模式异常
 * 2. 主动提醒 - 不等老板纠正，主动发现并报告
 * 3. 学习闭环 - 从 nudges 中学习，自动更新规则
 */

const fs = require('fs');
const path = require('path');

const SELF_IMPROVING = require('./sensen-self-improving-v2');
const TASK_MANAGER = require('./task-manager');

/**
 * Nudge 类型
 */
const NudgeType = {
  RULE_VIOLATION: 'rule_violation',       // 违反规则
  TASK_TIMEOUT: 'task_timeout',           // 任务超时
  PATTERN_ANOMALY: 'pattern_anomaly',     // 模式异常
  CONTEXT_DRIFT: 'context_drift',         // 上下文漂移
  OPPORTUNITY: 'opportunity',             // 机会发现
  HEALTH_CHECK: 'health_check'            // 健康检查
};

/**
 * Nudge 优先级
 */
const NudgePriority = {
  CRITICAL: 'critical',   // 立即处理
  HIGH: 'high',          // 今天处理
  MEDIUM: 'medium',      // 本周处理
  LOW: 'low'            // 记录观察
};

/**
 * Nudge 类
 */
class Nudge {
  constructor(type, message, options = {}) {
    this.id = `nudge_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
    this.type = type;
    this.message = message;
    this.priority = options.priority || NudgePriority.MEDIUM;
    this.source = options.source || 'system';
    this.data = options.data || {};
    this.action = options.action || null;  // 建议的行动
    this.acknowledged = false;
    this.resolved = false;
    this.createdAt = new Date().toISOString();
    this.acknowledgedAt = null;
    this.resolvedAt = null;
  }

  /**
   * 确认 nudge
   */
  acknowledge() {
    this.acknowledged = true;
    this.acknowledgedAt = new Date().toISOString();
    return this;
  }

  /**
   * 解决 nudge
   */
  resolve(resolution = '') {
    this.resolved = true;
    this.resolvedAt = new Date().toISOString();
    this.resolution = resolution;
    return this;
  }
}

/**
 * Periodic Nudge Engine
 */
class PeriodicNudgeEngine {
  constructor(options = {}) {
    this.interval = options.interval || 60 * 60 * 1000;  // 默认1小时
    this.enabled = false;
    this.timer = null;
    this.nudges = [];  // 内存中的 nudges
    this.historyFile = path.join(__dirname, '.nudge-history.json');
    this.stats = {
      totalNudges: 0,
      byType: {},
      byPriority: {}
    };
  }

  /**
   * 启动引擎
   */
  start() {
    if (this.enabled) {
      console.log('[PeriodicNudge] ⚠️ 引擎已在运行');
      return this;
    }

    this.enabled = true;
    this.loadHistory();

    // 立即执行一次
    this.runChecks();

    // 设置定时器
    this.timer = setInterval(() => {
      this.runChecks();
    }, this.interval);

    console.log(`[PeriodicNudge] ✅ 引擎已启动 (间隔: ${this.interval / 1000 / 60}分钟)`);
    return this;
  }

  /**
   * 停止引擎
   */
  stop() {
    if (!this.enabled) {
      console.log('[PeriodicNudge] ⚠️ 引擎未运行');
      return this;
    }

    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }

    this.enabled = false;
    this.saveHistory();

    console.log('[PeriodicNudge] ⏹️ 引擎已停止');
    return this;
  }

  /**
   * 执行所有检查
   */
  async runChecks() {
    console.log('[PeriodicNudge] 🔍 执行自检...');

    const results = {
      checks: [],
      newNudges: []
    };

    // 1. 检查规则违反
    const ruleNudges = await this.checkRuleViolations();
    results.checks.push({ name: '规则违反', found: ruleNudges.length });
    results.newNudges.push(...ruleNudges);

    // 2. 检查任务超时
    const timeoutNudges = this.checkTaskTimeouts();
    results.checks.push({ name: '任务超时', found: timeoutNudges.length });
    results.newNudges.push(...timeoutNudges);

    // 3. 检查模式异常
    const patternNudges = await this.checkPatternAnomalies();
    results.checks.push({ name: '模式异常', found: patternNudges.length });
    results.newNudges.push(...patternNudges);

    // 4. 检查机会
    const opportunityNudges = await this.checkOpportunities();
    results.checks.push({ name: '机会发现', found: opportunityNudges.length });
    results.newNudges.push(...opportunityNudges);

    // 添加新 nudges
    for (const nudge of results.newNudges) {
      this.addNudge(nudge);
    }

    // 更新统计
    this.updateStats();

    // 打印摘要
    if (results.newNudges.length > 0) {
      console.log(`[PeriodicNudge] 📊 自检完成: ${results.newNudges.length} 个新发现`);
      for (const check of results.checks) {
        if (check.found > 0) {
          console.log(`   - ${check.name}: ${check.found}`);
        }
      }
    }

    return results;
  }

  /**
   * 检查规则违反
   */
  async checkRuleViolations() {
    const nudges = [];
    const rules = SELF_IMPROVING.getActiveRules();
    const todayCorrections = SELF_IMPROVING.getAllCorrections()
      .filter(c => !c.resolved && c.timestamp.startsWith(new Date().toISOString().split('T')[0]));

    // 如果今天有新的纠正，说明可能违反了某条规则
    for (const correction of todayCorrections) {
      nudges.push(new Nudge(
        NudgeType.RULE_VIOLATION,
        `检测到纠正: "${correction.originalText}" → "${correction.correction}"`,
        {
          priority: NudgePriority.MEDIUM,
          source: 'self_improving',
          data: { correction },
          action: '建议更新规则或调整行为'
        }
      ));
    }

    // 检查需要刷新的规则
    const needsRefresh = SELF_IMPROVING.getRulesNeedingRefresh();
    for (const rule of needsRefresh) {
      nudges.push(new Nudge(
        NudgeType.RULE_VIOLATION,
        `规则 "${rule.name}" 需要确认刷新`,
        {
          priority: rule.priority === 'high' ? NudgePriority.HIGH : NudgePriority.MEDIUM,
          source: 'self_improving',
          data: { rule }
        }
      ));
    }

    return nudges;
  }

  /**
   * 检查任务超时
   */
  checkTaskTimeouts() {
    const nudges = [];
    const alerts = TASK_MANAGER.checkTimeouts();

    for (const alert of alerts) {
      if (alert.level === 'critical') {
        nudges.push(new Nudge(
          NudgeType.TASK_TIMEOUT,
          `任务严重超时: "${alert.title}" 已超过 ${alert.elapsedMinutes} 分钟`,
          {
            priority: NudgePriority.HIGH,
            source: 'task_manager',
            data: { alert },
            action: '立即处理或重新分配'
          }
        ));
      } else {
        nudges.push(new Nudge(
          NudgeType.TASK_TIMEOUT,
          `任务超时: "${alert.title}" 已超过 ${alert.elapsedMinutes} 分钟`,
          {
            priority: NudgePriority.MEDIUM,
            source: 'task_manager',
            data: { alert }
          }
        ));
      }
    }

    return nudges;
  }

  /**
   * 检查模式异常
   */
  async checkPatternAnomalies() {
    const nudges = [];
    const corrections = SELF_IMPROVING.getAllCorrections();

    // 检测同一类型的频繁纠正
    const typeCounts = {};
    for (const c of corrections) {
      if (c.resolved) continue;
      typeCounts[c.type] = (typeCounts[c.type] || 0) + 1;
    }

    for (const [type, count] of Object.entries(typeCounts)) {
      if (count >= 3) {
        nudges.push(new Nudge(
          NudgeType.PATTERN_ANOMALY,
          `${type} 类型纠正已出现 ${count} 次`,
          {
            priority: NudgePriority.HIGH,
            source: 'self_improving',
            data: { type, count },
            action: '建议生成自动化规则'
          }
        ));
      }
    }

    return nudges;
  }

  /**
   * 检查机会
   */
  async checkOpportunities() {
    const nudges = [];

    // 检查任务统计，看是否有可以优化的地方
    const stats = TASK_MANAGER.getStats();

    // 如果有太多超时的任务
    if (stats.timeouts > 5) {
      nudges.push(new Nudge(
        NudgeType.OPPORTUNITY,
        `系统有 ${stats.timeouts} 个超时任务，可能需要优化超时配置`,
        {
          priority: NudgePriority.LOW,
          source: 'analytics',
          action: '考虑调整超时阈值或增加资源'
        }
      ));
    }

    return nudges;
  }

  /**
   * 添加 nudge
   */
  addNudge(nudge) {
    // 检查是否已存在类似的
    const exists = this.nudges.some(n => 
      !n.resolved && 
      n.type === nudge.type && 
      n.message === nudge.message
    );

    if (!exists) {
      this.nudges.push(nudge);
      this.totalNudges++;
    }

    return nudge;
  }

  /**
   * 获取未处理的 nudges
   */
  getPendingNudges(priority = null) {
    const pending = this.nudges.filter(n => !n.resolved);
    
    if (priority) {
      return pending.filter(n => n.priority === priority);
    }
    
    return pending;
  }

  /**
   * 获取摘要
   */
  getSummary() {
    const pending = this.getPendingNudges();
    const byType = {};
    const byPriority = {};

    for (const n of pending) {
      byType[n.type] = (byType[n.type] || 0) + 1;
      byPriority[n.priority] = (byPriority[n.priority] || 0) + 1;
    }

    return {
      total: pending.length,
      byType,
      byPriority,
      critical: pending.filter(n => n.priority === NudgePriority.CRITICAL).length,
      high: pending.filter(n => n.priority === NudgePriority.HIGH).length
    };
  }

  /**
   * 更新统计
   */
  updateStats() {
    const summary = this.getSummary();
    this.stats.lastUpdate = new Date().toISOString();
    this.stats.pending = summary.total;
  }

  /**
   * 保存历史
   */
  saveHistory() {
    const data = {
      nudges: this.nudges.filter(n => n.resolved).slice(-100),  // 只保留最近100条
      stats: this.stats,
      savedAt: new Date().toISOString()
    };

    fs.writeFileSync(this.historyFile, JSON.stringify(data, null, 2), 'utf-8');
  }

  /**
   * 加载历史
   */
  loadHistory() {
    if (fs.existsSync(this.historyFile)) {
      try {
        const data = JSON.parse(fs.readFileSync(this.historyFile, 'utf-8'));
        this.stats = data.stats || this.stats;
      } catch (e) {
        console.warn('[PeriodicNudge] ⚠️ 加载历史失败');
      }
    }
  }

  /**
   * 打印当前状态
   */
  printStatus() {
    const summary = this.getSummary();

    console.log('\n📊 Periodic Nudge 状态');
    console.log('═'.repeat(50));
    console.log(`引擎状态: ${this.enabled ? '✅ 运行中' : '⏹️ 已停止'}`);
    console.log(`待处理: ${summary.total} 个`);

    if (summary.critical > 0) {
      console.log(`🚨 紧急: ${summary.critical}`);
    }
    if (summary.high > 0) {
      console.log(`⚠️ 高优: ${summary.high}`);
    }

    if (summary.total > 0) {
      console.log('\n按类型:');
      for (const [type, count] of Object.entries(summary.byType)) {
        console.log(`  - ${type}: ${count}`);
      }
    }

    // 打印最新 nudges
    const recent = this.getPendingNudges().slice(-5);
    if (recent.length > 0) {
      console.log('\n最新发现:');
      for (const n of recent) {
        console.log(`  [${n.priority}] ${n.message.substring(0, 50)}`);
      }
    }

    console.log('═'.repeat(50));
  }
}

// 导出
module.exports = {
  Nudge,
  NudgeType,
  NudgePriority,
  PeriodicNudgeEngine,
  createEngine: (options) => new PeriodicNudgeEngine(options)
};
