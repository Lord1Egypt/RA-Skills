/**
 * SENSEN Self-Improving Engine - Phase 3 (增强版 P1-1)
 * 自改进闭环 v2.0：规则权重 + 版本管理 + 有效期
 * 
 * 核心改进：
 * 1. 规则权重 - 每条规则有置信度权重，影响匹配优先级
 * 2. 版本管理 - 规则更新保留历史，支持回滚
 * 3. 有效期机制 - 规则可设置过期时间，过期自动提醒
 */

const fs = require('fs');
const path = require('path');

const BASE_DIR = path.join(__dirname);
const CORRECTIONS_DIR = path.join(BASE_DIR, 'corrections');
const RULES_DIR = path.join(BASE_DIR, 'rules');

// 确保目录存在
function init() {
  if (!fs.existsSync(CORRECTIONS_DIR)) {
    fs.mkdirSync(CORRECTIONS_DIR, { recursive: true });
  }
  if (!fs.existsSync(RULES_DIR)) {
    fs.mkdirSync(RULES_DIR, { recursive: true });
  }
}

// 纠正类型枚举
const CorrectionType = {
  PREFERENCE: 'preference',
  METHOD: 'method',
  FORMAT: 'format',
  TONE: 'tone',
  PRIORITY: 'priority',
  FORBIDDEN: 'forbidden',
  ERROR: 'error'
};

// 优先级
const Priority = {
  HIGH: 'high',
  MEDIUM: 'medium',
  LOW: 'low'
};

// 默认有效期（天）
const DEFAULT_EXPIRE_DAYS = {
  [Priority.HIGH]: 90,    // 高优先级规则90天
  [Priority.MEDIUM]: 30,  // 中优先级30天
  [Priority.LOW]: 7       // 低优先级7天
};

/**
 * 规则类 - 支持权重、版本、有效期
 */
class Rule {
  constructor(data) {
    this.id = data.id || `rule_${Date.now()}`;
    this.version = data.version || 1;
    this.versions = data.versions || [];  // 版本历史
    
    // 核心内容
    this.name = data.name || '';
    this.type = data.type || CorrectionType.PREFERENCE;
    this.keywords = data.keywords || [];
    this.description = data.description || '';
    
    // P1-1 新增：权重
    this.weight = data.weight || 0.5;  // 0.0 - 1.0，置信度权重
    
    // 优先级
    this.priority = data.priority || Priority.MEDIUM;
    
    // P1-1 新增：有效期
    this.expiresAt = data.expiresAt || null;  // ISO时间戳，null=永不过期
    this.refreshAfter = data.refreshAfter || DEFAULT_EXPIRE_DAYS[this.priority] * 24 * 60 * 60 * 1000;
    this.lastConfirmed = data.lastConfirmed || null;
    
    // 状态
    this.enabled = data.enabled !== undefined ? data.enabled : true;
    this.source = data.source || 'manual';  // auto_pattern / manual / imported
    this.sourceCorrections = data.sourceCorrections || [];
    this.examples = data.examples || [];
    
    // 元数据
    this.createdAt = data.createdAt || new Date().toISOString();
    this.updatedAt = data.updatedAt || new Date().toISOString();
    
    // 如果有描述但没有版本历史，记录初始版本
    if (this.description && this.versions.length === 0) {
      this.versions.push({
        version: 1,
        description: this.description,
        weight: this.weight,
        keywords: this.keywords,
        createdAt: this.createdAt
      });
    }
  }

  /**
   * 检查规则是否过期
   */
  isExpired() {
    if (!this.expiresAt) return false;
    return new Date(this.expiresAt) < new Date();
  }

  /**
   * 检查是否需要刷新确认
   */
  needsRefresh() {
    if (!this.lastConfirmed) return true;
    const nextRefresh = new Date(this.lastConfirmed).getTime() + this.refreshAfter;
    return Date.now() > nextRefresh;
  }

  /**
   * 获取规则状态
   */
  getStatus() {
    if (!this.enabled) return 'disabled';
    if (this.isExpired()) return 'expired';
    if (this.needsRefresh()) return 'needs_refresh';
    return 'active';
  }

  /**
   * 更新规则（创建新版本）
   */
  update(updates) {
    const oldVersion = { ...this };
    
    // 增加版本号
    this.version++;
    
    // 记录旧版本到历史
    this.versions.push({
      version: oldVersion.version,
      description: oldVersion.description,
      weight: oldVersion.weight,
      keywords: [...oldVersion.keywords],
      updatedAt: oldVersion.updatedAt
    });
    
    // 应用更新
    if (updates.description !== undefined) this.description = updates.description;
    if (updates.keywords !== undefined) this.keywords = updates.keywords;
    if (updates.weight !== undefined) this.weight = updates.weight;
    if (updates.priority !== undefined) this.priority = updates.priority;
    if (updates.expiresAt !== undefined) this.expiresAt = updates.expiresAt;
    if (updates.refreshAfter !== undefined) this.refreshAfter = updates.refreshAfter;
    if (updates.enabled !== undefined) this.enabled = updates.enabled;
    
    this.updatedAt = new Date().toISOString();
    
    return { oldVersion, newVersion: this };
  }

  /**
   * 确认规则（刷新有效期）
   */
  confirm() {
    this.lastConfirmed = new Date().toISOString();
    this.enabled = true;
    this.updatedAt = new Date().toISOString();
  }

  /**
   * 回滚到指定版本
   */
  rollback(targetVersion) {
    const target = this.versions.find(v => v.version === targetVersion);
    if (!target) {
      throw new Error(`版本 ${targetVersion} 不存在`);
    }
    
    this.description = target.description;
    this.weight = target.weight;
    this.keywords = [...target.keywords];
    this.version++;  // 仍然增加版本号表示回滚操作
    this.versions.push({
      version: target.version,
      description: `回滚到v${targetVersion}: ${target.description}`,
      weight: target.weight,
      keywords: target.keywords,
      createdAt: new Date().toISOString(),
      note: '回滚操作'
    });
    this.updatedAt = new Date().toISOString();
    
    return this;
  }

  toJSON() {
    return {
      id: this.id,
      version: this.version,
      versions: this.versions,
      name: this.name,
      type: this.type,
      keywords: this.keywords,
      description: this.description,
      weight: this.weight,
      priority: this.priority,
      expiresAt: this.expiresAt,
      refreshAfter: this.refreshAfter,
      lastConfirmed: this.lastConfirmed,
      enabled: this.enabled,
      source: this.source,
      sourceCorrections: this.sourceCorrections,
      examples: this.examples,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt
    };
  }
}

/**
 * 记录一次老板的纠正
 */
function logCorrection(correction) {
  init();
  
  const id = `corr_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
  const now = new Date();
  
  const record = {
    id,
    timestamp: now.toISOString(),
    type: correction.type || CorrectionType.PREFERENCE,
    originalText: correction.originalText,
    correction: correction.correction,
    reason: correction.reason || '',
    context: correction.context || '',
    source: correction.source || 'boss_dm',
    patternCount: 1,
    resolved: false,
    ruleId: null
  };
  
  // 写入当日corrections文件
  const dateStr = now.toISOString().split('T')[0];
  const filePath = path.join(CORRECTIONS_DIR, `${dateStr}.json`);
  
  let corrections = [];
  if (fs.existsSync(filePath)) {
    corrections = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  }
  
  corrections.push(record);
  fs.writeFileSync(filePath, JSON.stringify(corrections, null, 2), 'utf-8');
  
  console.log(`[SelfImproving] 📝 记录纠正: ${id}`);
  
  // 检查是否形成模式
  checkPattern(record);
  
  return record;
}

/**
 * 检查是否形成重复模式
 */
function checkPattern(correction) {
  const allCorrections = getAllCorrections();
  
  const similar = allCorrections.filter(c => {
    if (c.id === correction.id) return false;
    if (c.type !== correction.type) return false;
    if (c.resolved) return false;
    
    const keywords1 = extractKeywords(correction.originalText);
    const keywords2 = extractKeywords(c.originalText);
    return keywords1.some(k => keywords2.includes(k));
  });
  
  const totalSimilar = [...similar, correction];
  
  if (totalSimilar.length >= 3) {
    console.log(`[SelfImproving] 🔄 检测到模式! 出现${totalSimilar.length}次`);
    generateRule(totalSimilar);
  }
}

/**
 * 提取关键词
 */
function extractKeywords(text) {
  if (!text) return [];
  const stopWords = ['的', '了', '是', '我', '你', '他', '她', '它', '在', '有', '和', '就', '不', '也', '都', '这', '那', '要', '会', '能', '可以'];
  const words = text.toLowerCase()
    .replace(/[^\u4e00-\u9fa5a-z0-9]/g, ' ')
    .split(/\s+/)
    .filter(w => w.length > 1 && !stopWords.includes(w));
  return [...new Set(words)];
}

/**
 * 生成规则（v2 - 支持权重和有效期）
 */
function generateRule(corrections) {
  init();
  
  const first = corrections[0];
  const ruleId = `rule_${Date.now()}`;
  
  const keywords = corrections.flatMap(c => extractKeywords(c.originalText));
  const uniqueKeywords = [...new Set(keywords)].slice(0, 10);
  
  // 计算权重：基于纠正次数，次数越多权重越高
  const baseWeight = 0.5;
  const countBonus = Math.min(corrections.length * 0.05, 0.4);  // 最多+0.4
  const weight = Math.min(baseWeight + countBonus, 1.0);
  
  // 计算优先级
  let priority = Priority.MEDIUM;
  if (corrections.length >= 5) priority = Priority.HIGH;
  else if (corrections.length <= 2) priority = Priority.LOW;
  
  const rule = new Rule({
    id: ruleId,
    name: `自动规则_${first.type}_${uniqueKeywords.slice(0, 3).join('_')}`,
    type: first.type,
    keywords: uniqueKeywords,
    description: corrections.map(c => c.correction).join('; '),
    weight,
    priority,
    source: 'auto_pattern',
    sourceCorrections: corrections.map(c => c.id),
    examples: corrections.map(c => ({
      original: c.originalText,
      correction: c.correction
    }))
  });
  
  // 写入规则文件
  const rulePath = path.join(RULES_DIR, `${ruleId}.json`);
  fs.writeFileSync(rulePath, JSON.stringify(rule.toJSON(), null, 2), 'utf-8');
  
  // 标记相关的corrections为已解决
  const dateStr = new Date().toISOString().split('T')[0];
  const filePath = path.join(CORRECTIONS_DIR, `${dateStr}.json`);
  
  if (fs.existsSync(filePath)) {
    const allCorrections = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    const updated = allCorrections.map(c => {
      if (corrections.some(sc => sc.id === c.id)) {
        c.resolved = true;
        c.ruleId = ruleId;
      }
      return c;
    });
    fs.writeFileSync(filePath, JSON.stringify(updated, null, 2), 'utf-8');
  }
  
  console.log(`[SelfImproving] ✅ 生成规则: ${ruleId} (v${rule.version})`);
  console.log(`  权重: ${rule.weight}`);
  console.log(`  优先级: ${rule.priority}`);
  
  return rule;
}

/**
 * 获取所有规则
 */
function getAllRules() {
  init();
  if (!fs.existsSync(RULES_DIR)) return [];
  
  const files = fs.readdirSync(RULES_DIR).filter(f => f.endsWith('.json'));
  return files.map(f => {
    const content = JSON.parse(
      fs.readFileSync(path.join(RULES_DIR, f), 'utf-8')
    );
    return new Rule(content);
  });
}

/**
 * 获取激活的规则（未过期且启用）
 */
function getActiveRules() {
  return getAllRules().filter(r => r.getStatus() === 'active');
}

/**
 * 获取需要刷新的规则
 */
function getRulesNeedingRefresh() {
  return getAllRules().filter(r => r.needsRefresh() || r.isExpired());
}

/**
 * 检查文本是否匹配规则（v2 - 按权重排序）
 */
function matchRule(text) {
  const rules = getActiveRules();
  
  if (rules.length === 0) {
    return { matched: false };
  }
  
  const textLower = text.toLowerCase();
  const matches = [];
  
  for (const rule of rules) {
    const matchCount = rule.keywords.filter(k => 
      textLower.includes(k.toLowerCase()) || 
      (k.length > 1 && textLower.includes(k[0]))
    ).length;
    
    if (matchCount >= 1) {
      matches.push({
        rule,
        matchCount,
        weightedScore: matchCount * rule.weight  // 加权得分
      });
    }
  }
  
  // 按加权得分排序
  matches.sort((a, b) => b.weightedScore - a.weightedScore);
  
  if (matches.length > 0) {
    const best = matches[0];
    return {
      matched: true,
      rule: best.rule,
      matchCount: best.matchCount,
      weightedScore: best.weightedScore,
      allMatches: matches.slice(0, 3)  // 返回前3个匹配
    };
  }
  
  return { matched: false };
}

/**
 * 更新规则
 */
function updateRule(ruleId, updates) {
  const rules = getAllRules();
  const rule = rules.find(r => r.id === ruleId);
  
  if (!rule) {
    throw new Error(`规则 ${ruleId} 不存在`);
  }
  
  rule.update(updates);
  
  const rulePath = path.join(RULES_DIR, `${ruleId}.json`);
  fs.writeFileSync(rulePath, JSON.stringify(rule.toJSON(), null, 2), 'utf-8');
  
  console.log(`[SelfImproving] ✅ 更新规则: ${ruleId} (v${rule.version})`);
  
  return rule;
}

/**
 * 确认规则（刷新有效期）
 */
function confirmRule(ruleId) {
  const rules = getAllRules();
  const rule = rules.find(r => r.id === ruleId);
  
  if (!rule) {
    throw new Error(`规则 ${ruleId} 不存在`);
  }
  
  rule.confirm();
  
  const rulePath = path.join(RULES_DIR, `${ruleId}.json`);
  fs.writeFileSync(rulePath, JSON.stringify(rule.toJSON(), null, 2), 'utf-8');
  
  console.log(`[SelfImproving] ✅ 确认规则: ${ruleId}`);
  
  return rule;
}

/**
 * 回滚规则
 */
function rollbackRule(ruleId, targetVersion) {
  const rules = getAllRules();
  const rule = rules.find(r => r.id === ruleId);
  
  if (!rule) {
    throw new Error(`规则 ${ruleId} 不存在`);
  }
  
  rule.rollback(targetVersion);
  
  const rulePath = path.join(RULES_DIR, `${ruleId}.json`);
  fs.writeFileSync(rulePath, JSON.stringify(rule.toJSON(), null, 2), 'utf-8');
  
  console.log(`[SelfImproving] ✅ 回滚规则: ${ruleId} -> v${targetVersion}`);
  
  return rule;
}

/**
 * 获取统计信息
 */
function getStats() {
  init();
  
  const rules = getAllRules();
  const corrections = getAllCorrections();
  
  const today = new Date().toISOString().split('T')[0];
  const todayCorrections = corrections.filter(c => c.timestamp.startsWith(today));
  
  const expiredRules = rules.filter(r => r.isExpired());
  const needsRefresh = rules.filter(r => r.needsRefresh());
  
  return {
    corrections: {
      total: corrections.length,
      today: todayCorrections.length,
      unresolved: corrections.filter(c => !c.resolved).length
    },
    rules: {
      total: rules.length,
      active: rules.filter(r => r.getStatus() === 'active').length,
      expired: expiredRules.length,
      needsRefresh: needsRefresh.length,
      byPriority: {
        high: rules.filter(r => r.priority === Priority.HIGH).length,
        medium: rules.filter(r => r.priority === Priority.MEDIUM).length,
        low: rules.filter(r => r.priority === Priority.LOW).length
      }
    },
    refreshNeeded: [...expiredRules, ...needsRefresh].map(r => ({
      id: r.id,
      name: r.name,
      status: r.getStatus()
    }))
  };
}

/**
 * 获取所有纠正记录
 */
function getAllCorrections() {
  init();
  if (!fs.existsSync(CORRECTIONS_DIR)) return [];
  
  const files = fs.readdirSync(CORRECTIONS_DIR).filter(f => f.endsWith('.json'));
  
  let all = [];
  for (const file of files) {
    const content = JSON.parse(
      fs.readFileSync(path.join(CORRECTIONS_DIR, file), 'utf-8')
    );
    all = all.concat(content);
  }
  
  return all.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
}

/**
 * 打印规则状态
 */
function printRuleStatus() {
  const rules = getAllRules();
  
  console.log('\n📋 规则状态总览');
  console.log('═'.repeat(70));
  
  const byStatus = {
    active: rules.filter(r => r.getStatus() === 'active'),
    needs_refresh: rules.filter(r => r.getStatus() === 'needs_refresh'),
    expired: rules.filter(r => r.getStatus() === 'expired'),
    disabled: rules.filter(r => r.getStatus() === 'disabled')
  };
  
  for (const [status, list] of Object.entries(byStatus)) {
    if (list.length === 0) continue;
    
    const labels = {
      active: '✅ 生效中',
      needs_refresh: '⚠️ 需刷新',
      expired: '❌ 已过期',
      disabled: '⛔ 已禁用'
    };
    
    console.log(`\n${labels[status]} (${list.length})`);
    console.log('-'.repeat(70));
    
    for (const rule of list) {
      console.log(`  [v${rule.version}] ${rule.name}`);
      console.log(`    权重: ${rule.weight} | 优先级: ${rule.priority}`);
      if (rule.lastConfirmed) {
        console.log(`    上次确认: ${new Date(rule.lastConfirmed).toLocaleDateString('zh-CN')}`);
      }
    }
  }
  
  console.log('\n' + '═'.repeat(70));
}

/**
 * 主动提醒
 */
function getReminders() {
  const reminders = [];
  const stats = getStats();
  
  // 需要刷新的规则
  for (const rule of stats.refreshNeeded) {
    reminders.push({
      type: 'rule_refresh',
      priority: 'medium',
      ruleId: rule.id,
      message: `规则 "${rule.name}" 需要确认刷新`
    });
  }
  
  // 未解决的纠正
  const unresolved = getAllCorrections().filter(c => !c.resolved);
  if (unresolved.length > 0) {
    reminders.push({
      type: 'correction',
      priority: 'medium',
      message: `${unresolved.length}条纠正待处理`
    });
  }
  
  return reminders;
}

// 导出
module.exports = {
  Rule,
  CorrectionType,
  Priority,
  logCorrection,
  getAllCorrections,
  getAllRules,
  getActiveRules,
  getRulesNeedingRefresh,
  matchRule,
  updateRule,
  confirmRule,
  rollbackRule,
  getStats,
  printRuleStatus,
  getReminders,
  CORRECTIONS_DIR,
  RULES_DIR
};
