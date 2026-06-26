/**
 * FeedbackMiddleware - 用户反馈收集机制
 *
 * v2.4.0 新增：
 * - 任务完成后收集用户评分（1-5星）和文字反馈
 * - 简单的反馈存储和统计接口
 * - 反馈趋势分析和常见问题识别
 *
 * @module middleware/feedback-middleware
 */

const fs = require('fs');
const path = require('path');

// ─── 默认配置 ────────────────────────────────────────────

const DEFAULT_CONFIG = {
  storagePath: path.join(__dirname, '../../.feedback'),
  maxFeedbackPerTask: 10,       // 每个任务最大反馈数
  maxTotalFeedback: 1000,       // 总反馈上限（防止无限增长）
  ratingScale: { min: 1, max: 5 },
  onFeedbackReceived: null,     // 回调
};

// ─── 反馈数据模型 ─────────────────────────────────────────

/**
 * @typedef {Object} Feedback
 * @property {string} id           - 唯一 ID
 * @property {string} taskId       - 关联任务 ID
 * @property {string} skillName    - 被评价的技能
 * @property {number} rating       - 评分 (1-5)
 * @property {string} comment      - 文字反馈
 * @property {string[]} tags       - 反馈标签
 * @property {string} timestamp    - ISO 时间戳
 * @property {string} category     - 分类: praise|issue|suggestion|bug
 */

// ─── FeedbackMiddleware 类 ───────────────────────────────

class FeedbackMiddleware {
  constructor(config = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.feedbacks = [];
    this._initStorage();
  }

  // ── 初始化 ──────────────────────────────────────────────

  _initStorage() {
    const dir = this.config.storagePath;
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    const file = path.join(dir, 'feedbacks.json');
    if (fs.existsSync(file)) {
      try {
        this.feedbacks = JSON.parse(fs.readFileSync(file, 'utf-8'));
      } catch (e) {
        this.feedbacks = [];
      }
    }
  }

  save() {
    const file = path.join(this.config.storagePath, 'feedbacks.json');
    fs.writeFileSync(file, JSON.stringify(this.feedbacks, null, 2));
  }

  // ── 中间件接口：execute ─────────────────────────────────

  /**
   * Middleware 标准接口
   * 在任务完成后附加反馈收集接口
   */
  async execute(context, next) {
    const result = await next(context);

    // 标记任务已完成，准备收集反馈
    context._feedbackReady = true;
    context._feedbackSkill = context.skillName || 'unknown';
    context._feedbackTaskId = context.taskId || 'unknown';

    return result;
  }

  // ── 核心：提交反馈 ──────────────────────────────────────

  /**
   * 提交用户反馈
   * @param {Object} params
   * @param {string} params.taskId    - 任务 ID
   * @param {string} [params.skillName] - 技能名称
   * @param {number} params.rating    - 评分 (1-5)
   * @param {string} [params.comment]  - 文字反馈
   * @param {string[]} [params.tags]  - 标签
   * @param {string} [params.category] - 分类
   * @returns {Object} 创建的反馈记录
   */
  submit({ taskId, skillName = 'unknown', rating, comment = '', tags = [], category }) {
    // 验证评分
    const { min, max } = this.config.ratingScale;
    if (typeof rating !== 'number' || rating < min || rating > max) {
      throw new Error(`Rating must be between ${min} and ${max}, got ${rating}`);
    }

    // 检查任务反馈数量上限
    const taskCount = this.feedbacks.filter(f => f.taskId === taskId).length;
    if (taskCount >= this.config.maxFeedbackPerTask) {
      throw new Error(`Task ${taskId} has reached max feedback limit (${this.config.maxFeedbackPerTask})`);
    }

    // 自动分类（如果未指定）
    if (!category) {
      category = this._autoCategorize(rating, comment);
    }

    const feedback = {
      id: `fb_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
      taskId,
      skillName,
      rating,
      comment: comment.slice(0, 2000), // 限制长度
      tags,
      category,
      timestamp: new Date().toISOString(),
    };

    this.feedbacks.push(feedback);

    // 清理超出上限的旧反馈
    if (this.feedbacks.length > this.config.maxTotalFeedback) {
      this.feedbacks = this.feedbacks.slice(-this.config.maxTotalFeedback);
    }

    this.save();

    // 触发回调
    if (this.config.onFeedbackReceived) {
      this.config.onFeedbackReceived(feedback);
    }

    return feedback;
  }

  // ── 内部：自动分类 ──────────────────────────────────────

  _autoCategorize(rating, comment) {
    const lower = comment.toLowerCase();
    // 优先检查明确的 bug 关键词（不管评分）
    if (lower.includes('bug') || lower.includes('错误') || lower.includes('error') || lower.includes('崩溃') || lower.includes('fail')) {
      return 'bug';
    }
    if (lower.includes('建议') || lower.includes('希望') || lower.includes('改进') || lower.includes('suggestion') || lower.includes('improve')) {
      return 'suggestion';
    }
    // 按评分分类
    if (rating >= 4) return 'praise';
    return 'issue';
  }

  // ── 查询接口 ────────────────────────────────────────────

  /**
   * 获取任务的反馈统计
   * @param {string} taskId - 任务 ID（可选，不传则返回总体）
   * @returns {Object} 统计数据
   */
  getStats(taskId) {
    const filtered = taskId
      ? this.feedbacks.filter(f => f.taskId === taskId)
      : this.feedbacks;

    if (filtered.length === 0) {
      return {
        total: 0,
        avgRating: 0,
        ratingDistribution: {},
        categoryBreakdown: {},
        topTags: [],
        recentComments: [],
      };
    }

    // 评分分布
    const ratingDistribution = {};
    for (let i = 1; i <= 5; i++) ratingDistribution[i] = 0;
    filtered.forEach(f => { ratingDistribution[f.rating]++; });

    // 分类统计
    const categoryBreakdown = {};
    filtered.forEach(f => {
      categoryBreakdown[f.category] = (categoryBreakdown[f.category] || 0) + 1;
    });

    // 标签统计
    const tagCounts = {};
    filtered.forEach(f => {
      f.tags.forEach(t => { tagCounts[t] = (tagCounts[t] || 0) + 1; });
    });
    const topTags = Object.entries(tagCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([tag, count]) => ({ tag, count }));

    // 最近评论
    const recentComments = [...filtered]
      .filter(f => f.comment)
      .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
      .slice(0, 5)
      .map(f => ({
        rating: f.rating,
        comment: f.comment,
        category: f.category,
        timestamp: f.timestamp,
      }));

    const totalRating = filtered.reduce((sum, f) => sum + f.rating, 0);

    return {
      total: filtered.length,
      avgRating: Math.round((totalRating / filtered.length) * 100) / 100,
      ratingDistribution,
      categoryBreakdown,
      topTags,
      recentComments,
      latestUpdate: filtered[filtered.length - 1]?.timestamp,
    };
  }

  /**
   * 获取技能维度的评分排名
   * @returns {Array} 按平均评分排序的技能列表
   */
  getSkillRankings() {
    const skillMap = {};
    this.feedbacks.forEach(f => {
      if (!skillMap[f.skillName]) {
        skillMap[f.skillName] = { total: 0, sum: 0 };
      }
      skillMap[f.skillName].total++;
      skillMap[f.skillName].sum += f.rating;
    });

    return Object.entries(skillMap)
      .map(([name, data]) => ({
        skillName: name,
        avgRating: Math.round((data.sum / data.total) * 100) / 100,
        totalFeedbacks: data.total,
      }))
      .sort((a, b) => b.avgRating - a.avgRating);
  }

  /**
   * 搜索反馈
   * @param {Object} filters - 过滤条件
   * @returns {Array} 匹配的反馈
   */
  search(filters = {}) {
    return this.feedbacks.filter(f => {
      if (filters.taskId && f.taskId !== filters.taskId) return false;
      if (filters.skillName && f.skillName !== filters.skillName) return false;
      if (filters.category && f.category !== filters.category) return false;
      if (filters.minRating && f.rating < filters.minRating) return false;
      if (filters.maxRating && f.rating > filters.maxRating) return false;
      if (filters.tags && !filters.tags.every(t => f.tags.includes(t))) return false;
      if (filters.since && new Date(f.timestamp) < new Date(filters.since)) return false;
      return true;
    });
  }

  /**
   * 获取反馈趋势（按时间聚合）
   * @param {string} granularity - 'hourly' | 'daily' | 'weekly'
   * @returns {Array} 趋势数据
   */
  getTrend(granularity = 'daily') {
    const grouped = {};

    this.feedbacks.forEach(f => {
      const date = new Date(f.timestamp);
      let key;
      if (granularity === 'hourly') {
        key = date.toISOString().slice(0, 13); // YYYY-MM-DDTHH
      } else if (granularity === 'weekly') {
        const weekStart = new Date(date);
        weekStart.setDate(date.getDate() - date.getDay());
        key = weekStart.toISOString().slice(0, 10);
      } else {
        key = date.toISOString().slice(0, 10); // YYYY-MM-DD
      }

      if (!grouped[key]) {
        grouped[key] = { count: 0, totalRating: 0, issues: 0 };
      }
      grouped[key].count++;
      grouped[key].totalRating += f.rating;
      if (f.category === 'issue' || f.category === 'bug') {
        grouped[key].issues++;
      }
    });

    return Object.entries(grouped)
      .map(([period, data]) => ({
        period,
        count: data.count,
        avgRating: Math.round((data.totalRating / data.count) * 100) / 100,
        issueRate: Math.round((data.issues / data.count) * 1000) / 10,
      }))
      .sort((a, b) => a.period.localeCompare(b.period));
  }

  /**
   * 重置所有反馈数据（测试用）
   */
  reset() {
    this.feedbacks = [];
    this.save();
  }
}

module.exports = { FeedbackMiddleware, DEFAULT_CONFIG: DEFAULT_CONFIG };
