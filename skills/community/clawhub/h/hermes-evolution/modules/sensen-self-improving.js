/**
 * SENSEN Self-Improving Engine - Phase 3
 * 自改进闭环：老板纠正 → 自动记录 → 模式识别 → 规则生成
 * 
 * 核心思路：
 * 1. 每次老板纠正 → 记录到 corrections.log
 * 2. 检测重复模式（同一类纠正出现3次）→ 自动生成规则
 * 3. 规则存储到 rules/ 目录，被 PM Router 加载
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
  PREFERENCE: 'preference',      // 偏好：喜欢/不喜欢
  METHOD: 'method',              // 方法：做事方式
  FORMAT: 'format',              // 格式：输出格式
  TONE: 'tone',                  // 语气：沟通风格
  PRIORITY: 'priority',          // 优先级调整
  FORBIDDEN: 'forbidden',        // 禁止事项
  ERROR: 'error'                // 错误纠正
};

// 优先级
const Priority = {
  HIGH: 'high',     // P0-P1，立即遵守
  MEDIUM: 'medium', // P2，24小时内生效
  LOW: 'low'        // P3，提醒确认后生效
};

/**
 * 记录一次老板的纠正
 * @param {Object} correction - 纠正内容
 */
function logCorrection(correction) {
  init();
  
  const id = `corr_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
  const now = new Date();
  
  const record = {
    id,
    timestamp: now.toISOString(),
    type: correction.type || CorrectionType.PREFERENCE,
    originalText: correction.originalText,      // 老板原话
    correction: correction.correction,          // 纠正内容
    reason: correction.reason || '',           // 原因（如果有）
    context: correction.context || '',         // 上下文
    source: correction.source || 'boss_dm',     // 来源
    patternCount: 1,                           // 出现次数
    resolved: false,                           // 是否已生成规则
    ruleId: null                               // 关联的规则ID
  };
  
  // 写入当日corrections文件
  const dateStr = now.toISOString().split('T')[0]; // YYYY-MM-DD
  const filePath = path.join(CORRECTIONS_DIR, `${dateStr}.json`);
  
  let corrections = [];
  if (fs.existsSync(filePath)) {
    corrections = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  }
  
  corrections.push(record);
  fs.writeFileSync(filePath, JSON.stringify(corrections, null, 2), 'utf-8');
  
  console.log(`[SelfImproving] 📝 记录纠正: ${id}`);
  console.log(`  类型: ${record.type}`);
  console.log(`  内容: ${record.originalText}`);
  
  // 检查是否形成模式
  checkPattern(record);
  
  return record;
}

/**
 * 检查是否形成重复模式
 * 同一类型 + 相似内容出现3次 → 生成规则
 */
function checkPattern(correction) {
  const allCorrections = getAllCorrections();
  
  // 找相似纠正（相同类型 + 包含相似关键词）
  const similar = allCorrections.filter(c => {
    if (c.id === correction.id) return false;
    if (c.type !== correction.type) return false;
    if (c.resolved) return false;
    
    // 简单的关键词匹配
    const keywords1 = extractKeywords(correction.originalText);
    const keywords2 = extractKeywords(c.originalText);
    return keywords1.some(k => keywords2.includes(k));
  });
  
  // 加上当前这个
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
  // 简单分词：去除停用词，保留名词/动词
  const stopWords = ['的', '了', '是', '我', '你', '他', '她', '它', '在', '有', '和', '就', '不', '也', '都', '这', '那', '要', '会', '能', '可以'];
  const words = text.toLowerCase()
    .replace(/[^\u4e00-\u9fa5a-z0-9]/g, ' ')
    .split(/\s+/)
    .filter(w => w.length > 1 && !stopWords.includes(w));
  return [...new Set(words)];
}

/**
 * 生成规则
 */
function generateRule(corrections) {
  init();
  
  const first = corrections[0];
  const ruleId = `rule_${Date.now()}`;
  
  // 合并所有纠正的共同点
  const keywords = corrections.flatMap(c => extractKeywords(c.originalText));
  const uniqueKeywords = [...new Set(keywords)].slice(0, 10);
  
  const rule = {
    id: ruleId,
    name: `自动生成规则_${first.type}_${uniqueKeywords.slice(0, 3).join('_')}`,
    type: first.type,
    keywords: uniqueKeywords,
    description: corrections.map(c => c.correction).join('; '),
    createdAt: new Date().toISOString(),
    source: 'auto_pattern',
    sourceCorrections: corrections.map(c => c.id),
    priority: corrections.length >= 5 ? Priority.HIGH : Priority.MEDIUM,
    enabled: true,
    examples: corrections.map(c => ({
      original: c.originalText,
      correction: c.correction
    }))
  };
  
  // 写入规则文件
  const rulePath = path.join(RULES_DIR, `${ruleId}.json`);
  fs.writeFileSync(rulePath, JSON.stringify(rule, null, 2), 'utf-8');
  
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
  
  console.log(`[SelfImproving] ✅ 生成规则: ${ruleId}`);
  console.log(`  名称: ${rule.name}`);
  console.log(`  描述: ${rule.description}`);
  
  return rule;
}

/**
 * 获取所有未解决的纠正
 */
function getUnresolvedCorrections() {
  init();
  const files = fs.readdirSync(CORRECTIONS_DIR).filter(f => f.endsWith('.json'));
  
  let all = [];
  for (const file of files) {
    const content = JSON.parse(
      fs.readFileSync(path.join(CORRECTIONS_DIR, file), 'utf-8')
    );
    all = all.concat(content);
  }
  
  return all.filter(c => !c.resolved).sort((a, b) => 
    new Date(b.timestamp) - new Date(a.timestamp)
  );
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
    return content;
  }).filter(r => r.enabled);
}

/**
 * 获取启用的规则
 */
function getActiveRules() {
  return getAllRules().filter(r => r.enabled);
}

/**
 * 检查文本是否匹配某条规则
 */
function matchRule(text) {
  const rules = getActiveRules();
  const textLower = text.toLowerCase();
  
  for (const rule of rules) {
    // 使用更宽泛的匹配：规则关键词是文本的子串，或文本包含规则关键词
    const matchCount = rule.keywords.filter(k => 
      textLower.includes(k.toLowerCase()) || k.toLowerCase().split('').some(c => textLower.includes(c))
    ).length;
    
    // 更智能的匹配：检查是否有语义相关的中文词根
    const semanticMatches = rule.keywords.filter(k => {
      // 对于中文，检查词组是否相关
      // 例如："太长" 和 "太长了" 应该匹配
      // "简短" 和 "简" 应该匹配（取第一个字）
      if (textLower.includes(k)) return true;
      // 取关键词的第一个字，检查是否在文本中
      if (k.length > 1 && textLower.includes(k[0])) return true;
      return false;
    }).length;
    
    const effectiveMatchCount = Math.max(matchCount, semanticMatches);
    
    if (effectiveMatchCount >= 1) {  // 只要有1个匹配即可
      return {
        matched: true,
        rule,
        matchCount: effectiveMatchCount,
        matchRatio: effectiveMatchCount / rule.keywords.length
      };
    }
  }
  
  return { matched: false };
}

/**
 * 获取统计信息
 */
function getStats() {
  init();
  
  const corrections = getAllCorrections();
  const rules = getAllRules();
  
  const today = new Date().toISOString().split('T')[0];
  const todayCorrections = corrections.filter(c => c.timestamp.startsWith(today));
  
  return {
    totalCorrections: corrections.length,
    todayCorrections: todayCorrections.length,
    unresolved: corrections.filter(c => !c.resolved).length,
    resolved: corrections.filter(c => c.resolved).length,
    totalRules: rules.length,
    activeRules: rules.filter(r => r.enabled).length,
    byType: Object.fromEntries(
      Object.values(CorrectionType).map(type => [
        type,
        corrections.filter(c => c.type === type).length
      ])
    )
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
 * 打印最近纠正
 */
function printRecentCorrections(limit = 10) {
  const corrections = getUnresolvedCorrections().slice(0, limit);
  
  console.log('\n📝 最近纠正记录');
  console.log('═'.repeat(60));
  
  for (const c of corrections) {
    const date = new Date(c.timestamp).toLocaleString('zh-CN', { 
      month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' 
    });
    console.log(`[${c.type}] ${date}`);
    console.log(`  原话: "${c.originalText}"`);
    console.log(`  纠正: ${c.correction}`);
    console.log('');
  }
  
  console.log('═'.repeat(60));
}

/**
 * 打印当前规则
 */
function printRules() {
  const rules = getActiveRules();
  
  console.log('\n📋 当前生效规则');
  console.log('═'.repeat(60));
  
  if (rules.length === 0) {
    console.log('(暂无规则)');
  }
  
  for (const rule of rules) {
    console.log(`[${rule.type}] ${rule.name}`);
    console.log(`  关键词: ${rule.keywords.join(', ')}`);
    console.log(`  规则: ${rule.description}`);
    console.log('');
  }
  
  console.log('═'.repeat(60));
}

/**
 * 主动提醒（被PM Router调用）
 */
function getReminders() {
  const reminders = [];
  const rules = getActiveRules();
  const stats = getStats();
  
  // 有新的未解决纠正
  if (stats.unresolved > 0) {
    reminders.push({
      type: 'correction',
      priority: 'medium',
      message: `${stats.unresolved}条纠正待处理`
    });
  }
  
  // 模式检测（某类型纠正出现3次但还未生成规则）
  const unresolved = getUnresolvedCorrections();
  const typeCounts = {};
  for (const c of unresolved) {
    typeCounts[c.type] = (typeCounts[c.type] || 0) + 1;
  }
  
  for (const [type, count] of Object.entries(typeCounts)) {
    if (count >= 3) {
      reminders.push({
        type: 'pattern',
        priority: 'high',
        message: `${type}类型纠正出现${count}次，建议生成规则`
      });
    }
  }
  
  return reminders;
}

// 导出模块
module.exports = {
  CorrectionType,
  Priority,
  logCorrection,
  getUnresolvedCorrections,
  getAllCorrections,
  getAllRules,
  getActiveRules,
  matchRule,
  getStats,
  printRecentCorrections,
  printRules,
  getReminders,
  CORRECTIONS_DIR,
  RULES_DIR
};
