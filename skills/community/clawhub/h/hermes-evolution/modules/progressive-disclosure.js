/**
 * ProgressiveDisclosure - P1-2 渐进式披露
 * Skills分级加载，Token开销稳定
 * 
 * 分级策略：
 * L1 - 核心（始终加载）- 基础描述和用途
 * L2 - 标准（按需加载）- 详细说明和参数
 * L3 - 完整（显式请求）- 完整文档和示例
 * 
 * 实现：
 * 1. Skill 标记分级
 * 2. 上下文预算管理
 * 3. 按需触发加载
 */

const fs = require('fs');
const path = require('path');

const DEFAULT_CONTEXT_BUDGET = 8000;  // 默认上下文预算（Token）
const LEVEL_DESCRIPTIONS = {
  1: { name: '核心', desc: '始终加载，基础描述', maxTokens: 200 },
  2: { name: '标准', desc: '按需加载，详细说明', maxTokens: 800 },
  3: { name: '完整', desc: '显式请求，完整文档', maxTokens: 3000 }
};

/**
 * Skill 分级类
 */
class TieredSkill {
  constructor(skill) {
    this.name = skill.name;
    this.description = skill.description || '';
    this.level = skill.tier || 1;  // 默认L1
    
    // L1 核心信息
    this.l1Core = {
      name: this.name,
      description: this.description,
      tier: this.level
    };
    
    // L2 标准信息
    this.l2Standard = {
      parameters: skill.parameters || [],
      usage: skill.usage || '',
      examples: skill.examples || [],
      tips: skill.tips || []
    };
    
    // L3 完整信息
    this.l3Full = {
      pitfalls: skill.pitfalls || [],
      procedure: skill.procedure || [],
      verification: skill.verification || null,
      metadata: skill.metadata || {},
      fullContent: skill.fullContent || skill.description
    };
  }
  
  /**
   * 获取指定层级的信息
   */
  getLevel(level) {
    switch (level) {
      case 1: return { ...this.l1Core, tokens: this.estimateTokens(this.l1Core) };
      case 2: return { ...this.l1Core, ...this.l2Standard, tokens: this.estimateTokens(this.l2Standard) };
      case 3: return { ...this.l1Core, ...this.l2Standard, ...this.l3Full, tokens: this.estimateTokens(this.l3Full) };
      default: return this.getLevel(1);
    }
  }
  
  /**
   * 估算 Token 数（粗略：中文1Token≈1字，英文1Token≈4字符）
   */
  estimateTokens(obj) {
    const str = JSON.stringify(obj);
    const chinese = (str.match(/[\u4e00-\u9fa5]/g) || []).length;
    const english = (str.match(/[a-zA-Z]/g) || []).length;
    return chinese + Math.ceil(english / 4);
  }
  
  /**
   * 检查是否符合条件
   */
  matches(context) {
    if (!context.keywords && !context.intent) return false;
    
    const searchIn = `${this.name} ${this.description}`.toLowerCase();
    
    if (context.keywords) {
      return context.keywords.some(kw => searchIn.includes(kw.toLowerCase()));
    }
    
    if (context.intent) {
      return searchIn.includes(context.intent.toLowerCase());
    }
    
    return false;
  }
}

/**
 * 渐进式加载器
 */
class ProgressiveDisclosureLoader {
  constructor(options = {}) {
    this.budget = options.budget || DEFAULT_CONTEXT_BUDGET;
    this.reservedBudget = options.reservedBudget || 1000;  // 保留给系统消息
    this.skills = new Map();  // name → TieredSkill
    this.loadedSkills = new Map();  // name → currentLevel
    this.contextBudget = 0;  // 当前已用
  }
  
  /**
   * 注册 Skill
   */
  register(skill) {
    const tiered = new TieredSkill(skill);
    this.skills.set(skill.name, tiered);
    
    // 自动加载 L1
    this.loadedSkills.set(skill.name, 1);
    this.contextBudget += tiered.getLevel(1).tokens;
    
    return this;
  }
  
  /**
   * 注册多个 Skills
   */
  registerAll(skills) {
    for (const skill of skills) {
      this.register(skill);
    }
    return this;
  }
  
  /**
   * 查询可用预算
   */
  getAvailableBudget() {
    return this.budget - this.reservedBudget - this.contextBudget;
  }
  
  /**
   * 获取当前加载的 Skills 摘要
   */
  getLoadedSummary() {
    const summary = [];
    
    for (const [name, level] of this.loadedSkills) {
      const skill = this.skills.get(name);
      const levelInfo = LEVEL_DESCRIPTIONS[level];
      summary.push({
        name,
        level,
        levelName: levelInfo.name,
        tokens: skill.getLevel(level).tokens
      });
    }
    
    return {
      totalSkills: this.skills.size,
      loadedCount: this.loadedSkills.size,
      totalTokens: this.contextBudget,
      availableBudget: this.getAvailableBudget(),
      skills: summary
    };
  }
  
  /**
   * 搜索匹配的 Skills（不加载）
   */
  findMatching(context, limit = 5) {
    const matches = [];
    
    for (const [name, skill] of this.skills) {
      if (skill.matches(context)) {
        matches.push({
          name,
          tier: skill.level,
          currentLevel: this.loadedSkills.get(name) || 1,
          score: this.calculateRelevance(skill, context)
        });
      }
    }
    
    return matches
      .sort((a, b) => b.score - a.score)
      .slice(0, limit);
  }
  
  /**
   * 计算相关性分数
   */
  calculateRelevance(skill, context) {
    let score = 0;
    
    // 名称匹配权重高
    if (context.keywords) {
      for (const kw of context.keywords) {
        if (skill.name.toLowerCase().includes(kw.toLowerCase())) {
          score += 10;
        }
        if (skill.description.toLowerCase().includes(kw.toLowerCase())) {
          score += 5;
        }
      }
    }
    
    // 层级权重（高层级更重要）
    score += skill.level * 2;
    
    return score;
  }
  
  /**
   * 尝试升级 Skill 层级
   */
  tryUpgrade(skillName, targetLevel = 2) {
    const skill = this.skills.get(skillName);
    if (!skill) return { success: false, reason: 'Skill不存在' };
    
    const currentLevel = this.loadedSkills.get(skillName) || 1;
    if (currentLevel >= targetLevel) {
      return { success: true, reason: '已是目标层级或更高' };
    }
    
    const targetTokens = skill.getLevel(targetLevel).tokens;
    const currentTokens = skill.getLevel(currentLevel).tokens;
    const additionalTokens = targetTokens - currentTokens;
    
    // 检查预算
    if (additionalTokens > this.getAvailableBudget()) {
      return { 
        success: false, 
        reason: '预算不足',
        required: additionalTokens,
        available: this.getAvailableBudget()
      };
    }
    
    // 执行升级
    this.loadedSkills.set(skillName, targetLevel);
    this.contextBudget += additionalTokens;
    
    return { 
      success: true, 
      fromLevel: currentLevel,
      toLevel: targetLevel,
      additionalTokens,
      newTotalTokens: this.contextBudget
    };
  }
  
  /**
   * 获取上下文文本（用于注入 Prompt）
   */
  getContextText(options = {}) {
    const { format = 'markdown', maxLevel = 2 } = options;
    
    const parts = [];
    
    for (const [name, level] of this.loadedSkills) {
      if (level > maxLevel) continue;
      
      const skill = this.skills.get(name);
      const data = skill.getLevel(level);
      
      if (format === 'markdown') {
        parts.push(`## ${data.name}\n${data.description}`);
        
        if (level >= 2 && data.usage) {
          parts.push(`\n用法: ${data.usage}`);
        }
        if (level >= 2 && data.examples && data.examples.length > 0) {
          parts.push(`\n示例:\n${data.examples.map(e => `- ${e}`).join('\n')}`);
        }
        if (level >= 3 && data.procedure && data.procedure.length > 0) {
          parts.push(`\n步骤:\n${data.procedure.map((p, i) => `${i+1}. ${p.step || p}`).join('\n')}`);
        }
      } else {
        parts.push(JSON.stringify(data));
      }
    }
    
    return parts.join('\n\n');
  }
  
  /**
   * 智能加载：根据上下文自动决定加载哪些 Skills
   */
  autoLoad(context) {
    const results = {
      upgraded: [],
      failed: [],
      skipped: []
    };
    
    // 找到匹配的
    const matches = this.findMatching(context);
    
    for (const match of matches) {
      // 尝试升级到 L2
      const upgrade = this.tryUpgrade(match.name, 2);
      if (upgrade.success) {
        results.upgraded.push({
          name: match.name,
          level: upgrade.toLevel,
          additionalTokens: upgrade.additionalTokens
        });
      } else if (upgrade.reason === '预算不足') {
        results.failed.push({ name: match.name, reason: upgrade.reason });
      }
    }
    
    return results;
  }
  
  /**
   * 重置加载状态（释放预算）
   */
  reset() {
    this.loadedSkills.clear();
    this.contextBudget = 0;
    
    // 重新加载 L1
    for (const [name, skill] of this.skills) {
      this.loadedSkills.set(name, 1);
      this.contextBudget += skill.getLevel(1).tokens;
    }
    
    return this;
  }
  
  /**
   * 保存加载状态
   */
  saveState() {
    return {
      loadedSkills: Array.from(this.loadedSkills.entries()),
      contextBudget: this.contextBudget
    };
  }
  
  /**
   * 恢复加载状态
   */
  restoreState(state) {
    this.loadedSkills = new Map(state.loadedSkills);
    this.contextBudget = state.contextBudget;
    return this;
  }
}

// 导出
module.exports = {
  TieredSkill,
  ProgressiveDisclosureLoader,
  LEVEL_DESCRIPTIONS,
  DEFAULT_CONTEXT_BUDGET
};
