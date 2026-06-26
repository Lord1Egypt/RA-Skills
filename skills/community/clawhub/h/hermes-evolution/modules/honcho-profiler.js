/**
 * HonchoProfiler - P2-3 Honcho用户建模
 * 角色画像 + 偏好学习
 * 
 * 核心思路：
 * 1. 用户画像 - 身份、背景、目标
 * 2. 偏好学习 - 沟通风格、响应偏好
 * 3. 行为预测 - 提前预测需求
 */

const fs = require('fs');
const path = require('path');

const PROFILE_DIR = path.join(__dirname, '.honcho-profiles');

/**
 * 用户画像
 */
class UserProfile {
  constructor(userId) {
    this.userId = userId;
    this.identity = {
      name: null,
      title: null,         // 职位
      company: null,       // 公司
      timezone: 'Asia/Shanghai',
      language: 'zh-CN'
    };
    this.goals = [];        // 目标列表
    this.preferences = {
      communicationStyle: 'direct',  // direct | detailed | brief
      responseFormat: 'concise',     // concise | detailed | structured
      notificationLevel: 'normal',   // minimal | normal | verbose
      activeHours: { start: 9, end: 22 },
      preferredLanguage: 'chinese'
    };
    this.behaviorPattern = {
      avgResponseTime: 0,     // 平均响应时间（毫秒）
      mostActiveHours: [],   // 最活跃时段
      commonIntents: [],     // 常见意图
      preferredAgents: {}    // 各任务类型偏好的Agent
    };
    this.learnedRules = [];   // 从交互中学到的规则
    this.relationship = {
      trust: 0.5,           // 信任度 0-1
      authority: 0.7,       // 权威度 0-1
      rapport: 0.3          // 亲密度 0-1
    };
    this.metadata = {
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      interactionCount: 0,
      lastSeen: null
    };
  }

  /**
   * 更新互动计数
   */
  incrementInteraction() {
    this.metadata.interactionCount++;
    this.metadata.lastSeen = new Date().toISOString();
    this.metadata.updatedAt = new Date().toISOString();
  }

  /**
   * 更新身份信息
   */
  updateIdentity(updates) {
    Object.assign(this.identity, updates);
    this.metadata.updatedAt = new Date().toISOString();
  }

  /**
   * 添加目标
   */
  addGoal(goal) {
    this.goals.push({
      id: `goal_${Date.now()}`,
      text: goal,
      status: 'active',
      createdAt: new Date().toISOString()
    });
  }

  /**
   * 学习偏好
   */
  learnPreference(key, value) {
    if (this.preferences[key] !== undefined) {
      const oldValue = this.preferences[key];
      this.preferences[key] = value;
      
      // 记录学习历史
      this.behaviorPattern[`${key}History`] = this.behaviorPattern[`${key}History`] || [];
      this.behaviorPattern[`${key}History`].push({
        from: oldValue,
        to: value,
        at: new Date().toISOString()
      });
    }
  }

  /**
   * 学习行为模式
   */
  learnBehavior(type, data) {
    switch (type) {
      case 'response_time':
        this.behaviorPattern.avgResponseTime = 
          (this.behaviorPattern.avgResponseTime * (this.metadata.interactionCount - 1) + data) 
          / this.metadata.interactionCount;
        break;
        
      case 'active_hour':
        if (!this.behaviorPattern.mostActiveHours.includes(data)) {
          this.behaviorPattern.mostActiveHours.push(data);
        }
        break;
        
      case 'intent':
        const intentCount = this.behaviorPattern.intentCounts || {};
        intentCount[data] = (intentCount[data] || 0) + 1;
        this.behaviorPattern.intentCounts = intentCount;
        
        // 更新常见意图
        const sorted = Object.entries(intentCount)
          .sort((a, b) => b[1] - a[1])
          .slice(0, 5)
          .map(([k]) => k);
        this.behaviorPattern.commonIntents = sorted;
        break;
        
      case 'agent_preference':
        const taskType = data.taskType;
        const agent = data.agent;
        if (!this.behaviorPattern.preferredAgents[taskType]) {
          this.behaviorPattern.preferredAgents[taskType] = {};
        }
        this.behaviorPattern.preferredAgents[taskType][agent] = 
          (this.behaviorPattern.preferredAgents[taskType][agent] || 0) + 1;
        break;
    }
  }

  /**
   * 添加学到的规则
   */
  addLearnedRule(rule) {
    this.learnedRules.push({
      id: `rule_${Date.now()}`,
      ...rule,
      createdAt: new Date().toISOString()
    });
  }

  /**
   * 获取推荐（基于学习）
   */
  getRecommendations() {
    const recs = [];
    
    // 基于常见意图推荐
    if (this.behaviorPattern.commonIntents.length > 0) {
      recs.push({
        type: 'intent',
        suggestions: this.behaviorPattern.commonIntents.slice(0, 3)
      });
    }
    
    // 基于时间推荐
    const hour = new Date().getHours();
    if (hour >= 9 && hour <= 11) {
      recs.push({
        type: 'time',
        message: '上午适合处理复杂任务'
      });
    } else if (hour >= 14 && hour <= 17) {
      recs.push({
        type: 'time',
        message: '下午适合快速决策'
      });
    }
    
    // 基于目标推荐
    const activeGoals = this.goals.filter(g => g.status === 'active');
    if (activeGoals.length > 0) {
      recs.push({
        type: 'goal',
        goals: activeGoals.slice(0, 2)
      });
    }
    
    return recs;
  }

  /**
   * 预测需求
   */
  predictNeeds() {
    const predictions = [];
    const hour = new Date().getHours();
    
    // 基于时间预测
    if (hour === 9 && this.behaviorPattern.mostActiveHours.includes(9)) {
      predictions.push({
        need: 'daily_briefing',
        confidence: 0.8,
        message: '您通常在9点查看日程'
      });
    }
    
    if (hour === 17 && this.behaviorPattern.mostActiveHours.includes(17)) {
      predictions.push({
        need: 'end_of_day_summary',
        confidence: 0.7,
        message: '您通常在17点查看进度'
      });
    }
    
    // 基于常见意图预测
    if (this.behaviorPattern.commonIntents.includes('小红书发布')) {
      predictions.push({
        need: 'content_queue_check',
        confidence: 0.6,
        message: '检查内容发布队列'
      });
    }
    
    return predictions;
  }

  /**
   * 导出JSON
   */
  toJSON() {
    return {
      userId: this.userId,
      identity: this.identity,
      goals: this.goals,
      preferences: this.preferences,
      behaviorPattern: this.behaviorPattern,
      learnedRules: this.learnedRules,
      relationship: this.relationship,
      metadata: this.metadata
    };
  }
}

/**
 * Honcho Profile Manager
 */
class HonchoProfiler {
  constructor() {
    this.profiles = new Map();  // userId → UserProfile
    this.currentProfile = null;
    
    if (!fs.existsSync(PROFILE_DIR)) {
      fs.mkdirSync(PROFILE_DIR, { recursive: true });
    }
  }

  /**
   * 创建或获取用户画像
   */
  getProfile(userId) {
    if (!this.profiles.has(userId)) {
      const profile = new UserProfile(userId);
      
      // 尝试从文件加载
      const filePath = path.join(PROFILE_DIR, `${userId}.json`);
      if (fs.existsSync(filePath)) {
        try {
          const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
          Object.assign(profile, data);
        } catch (e) {
          console.warn(`[HonchoProfiler] ⚠️ 加载画像失败: ${userId}`);
        }
      }
      
      this.profiles.set(userId, profile);
    }
    
    return this.profiles.get(userId);
  }

  /**
   * 设置当前用户
   */
  setCurrentUser(userId) {
    this.currentProfile = this.getProfile(userId);
    return this.currentProfile;
  }

  /**
   * 记录交互
   */
  recordInteraction(userId, interaction) {
    const profile = this.getProfile(userId);
    profile.incrementInteraction();
    
    // 学习各种行为
    if (interaction.responseTime) {
      profile.learnBehavior('response_time', interaction.responseTime);
    }
    
    if (interaction.hour !== undefined) {
      profile.learnBehavior('active_hour', interaction.hour);
    }
    
    if (interaction.intent) {
      profile.learnBehavior('intent', interaction.intent);
    }
    
    if (interaction.agentPreference) {
      profile.learnBehavior('agent_preference', interaction.agentPreference);
    }
    
    // 保存
    this.saveProfile(userId);
    
    return profile;
  }

  /**
   * 保存画像
   */
  saveProfile(userId) {
    const profile = this.profiles.get(userId);
    if (!profile) return;
    
    const filePath = path.join(PROFILE_DIR, `${userId}.json`);
    fs.writeFileSync(filePath, JSON.stringify(profile.toJSON(), null, 2), 'utf-8');
  }

  /**
   * 保存所有画像
   */
  saveAll() {
    for (const userId of this.profiles.keys()) {
      this.saveProfile(userId);
    }
    console.log(`[HonchoProfiler] 💾 已保存 ${this.profiles.size} 个用户画像`);
  }

  /**
   * 获取当前用户画像
   */
  getCurrentProfile() {
    return this.currentProfile;
  }

  /**
   * 获取所有画像摘要
   */
  getAllProfilesSummary() {
    const summaries = [];
    for (const [userId, profile] of this.profiles) {
      summaries.push({
        userId,
        name: profile.identity.name,
        interactionCount: profile.metadata.interactionCount,
        lastSeen: profile.metadata.lastSeen
      });
    }
    return summaries;
  }

  /**
   * 打印当前用户画像
   */
  printCurrentProfile() {
    if (!this.currentProfile) {
      console.log('[HonchoProfiler] ⚠️ 未设置当前用户');
      return;
    }
    
    const p = this.currentProfile;
    
    console.log('\n👤 Honcho 用户画像');
    console.log('═'.repeat(50));
    console.log(`用户ID: ${p.userId}`);
    console.log(`姓名: ${p.identity.name || '未知'}`);
    console.log(`职位: ${p.identity.title || '未知'}`);
    console.log(`公司: ${p.identity.company || '未知'}`);
    console.log(`\n📊 互动统计`);
    console.log(`互动次数: ${p.metadata.interactionCount}`);
    console.log(`最后活跃: ${p.metadata.lastSeen || '从未'}`);
    console.log(`\n🎯 目标 (${p.goals.length})`);
    for (const goal of p.goals.slice(0, 3)) {
      console.log(`  - ${goal.text} [${goal.status}]`);
    }
    console.log(`\n⚙️ 偏好`);
    console.log(`沟通风格: ${p.preferences.communicationStyle}`);
    console.log(`响应格式: ${p.preferences.responseFormat}`);
    console.log(`通知级别: ${p.preferences.notificationLevel}`);
    console.log(`\n🧠 行为模式`);
    console.log(`常见意图: ${p.behaviorPattern.commonIntents.slice(0, 5).join(', ') || '暂无'}`);
    console.log(`活跃时段: ${p.behaviorPattern.mostActiveHours.join(', ') || '暂无'}`);
    console.log(`\n📈 关系`);
    console.log(`信任度: ${(p.relationship.trust * 100).toFixed(0)}%`);
    console.log(`权威度: ${(p.relationship.authority * 100).toFixed(0)}%`);
    console.log(`亲密度: ${(p.relationship.rapport * 100).toFixed(0)}%`);
    console.log('═'.repeat(50));
  }
}

// 导出
module.exports = {
  UserProfile,
  HonchoProfiler
};
