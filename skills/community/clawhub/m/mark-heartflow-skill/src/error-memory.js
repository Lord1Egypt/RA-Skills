/**
 * src/error-memory.js — 心虫跨会话错误记忆
 *
 * 轻量级文件型错误日志。记录每次被纠正的错误，
 * 下次同类情况自动触发预防规则。
 *
 * 结构：
 *   error-memory.json — 错误模式库
 *   logCorrection(category, detail, context) — 记录纠错
 *   checkRecurrence(context) — 检查当前有没有踩过同类坑
 *
 * 用法：
 *   const errMem = require('./error-memory.js');
 *   // 被纠正时记录
 *   errMem.logCorrection('overconfidence', '说"唯一方案"太绝对', currentQuestion);
 *   // 每次回复前检查
 *   const warning = errMem.checkRecurrence(currentContext);
 *   if (warning) { addCautionPrefix(); }
 */

'use strict';
const fs = require('fs');
const path = require('path');
const taxonomy = require('./shield/error-taxonomy.js');

// [v6.6.0] 测试隔离：NODE_ENV=test 时写独立记忆文件，不污染生产 error-memory
const MEMORY_FILE = process.env.NODE_ENV === 'test'
  ? path.join(__dirname, '..', 'data', 'error-memory.test.json')
  : path.join(__dirname, '..', 'data', 'error-memory.json');

// ─── 错误分类 ─────────────────────────

const CATEGORIES = {
  overconfidence: { label: '过度自信', preventionPatterns: ['毫无疑问', '唯一', '绝对', '肯定', '一定', '必须'] },
  hallucination: { label: '幻觉/编造', preventionPatterns: ['根据研究', '数据表明', '专家指出'] },
  sycophancy: { label: '谄媚附和', preventionPatterns: ['您说得对', '很好的问题', '完全同意'] },
  defensiveness: { label: '防御姿态', preventionPatterns: ['你可能没理解', '其实我意思是', '但更重要的是'] },
  vagueness: { label: '模糊回避', preventionPatterns: ['相关部门', '据了解', '业内人士'] },
  binary: { label: '二元论', preventionPatterns: ['不是...就是', '要么...要么', '唯一选择'] },
  omission: { label: '遗漏问题', preventionPatterns: ['没有遗漏', '完全覆盖', '全部完成'] },
};

// ─── 读写错误记忆 ─────────────────────────

function loadMemory() {
  try {
    const dir = path.dirname(MEMORY_FILE);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    if (!fs.existsSync(MEMORY_FILE)) return { errors: [], version: '1.0' };
    const raw = fs.readFileSync(MEMORY_FILE, 'utf8');
    return JSON.parse(raw);
  } catch {
    return { errors: [], version: '1.0' };
  }
}

function saveMemory(data) {
  const dir = path.dirname(MEMORY_FILE);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(MEMORY_FILE, JSON.stringify(data, null, 2), 'utf8');
}

// ─── 记录纠错 ─────────────────────────

// [v6.6.0] 测试/沙盒内容过滤：detail/context 含测试标记 → 拒绝写入（防污染生产记忆）
const TEST_MARKERS = ['test error', 'test action', 'integration test', 'test outcome', 'fixture', 'unit test'];
function isTestContent(detail, context) {
  const haystack = `${detail || ''} ${context || ''}`.toLowerCase();
  return TEST_MARKERS.some(m => haystack.includes(m));
}

function logCorrection(category, detail, context = '') {
  if (!category || !CATEGORIES[category]) return { success: false, reason: '未知错误分类' };
  if (isTestContent(detail, context)) return { success: false, reason: '测试内容拒绝写入' };

  const memory = loadMemory();
  const entry = {
    id: memory.errors.length + 1,
    category,
    detail: detail || '',
    context: context.slice(0, 200),
    timestamp: new Date().toISOString(),
    prevention: CATEGORIES[category].preventionPatterns,
    recurrenceCount: 0,
    // [v6.6.0] 闭环状态机: open(已记录) → fixed(已修复) → verified(已验证)
    status: 'open',
    fixDetail: null,
    verifiedAt: null,
  };

  // 去重：同类错误 1 小时内不重复记录
  const recent = memory.errors.filter(e =>
    e.category === category &&
    Date.now() - new Date(e.timestamp).getTime() < 3600000
  );
  if (recent.length > 0) {
    recent[0].recurrenceCount = (recent[0].recurrenceCount || 0) + 1;
    recent[0].lastSeen = entry.timestamp;
    saveMemory(memory);
    return { success: true, updated: recent[0].id, recurrence: true };
  }

  memory.errors.push(entry);

  // 限制最大 200 条（滚动淘汰最旧的）
  if (memory.errors.length > 200) {
    memory.errors = memory.errors.slice(-200);
  }

  saveMemory(memory);
  return { success: true, id: entry.id, recurrence: false };
}

// ─── [v6.6.0] 闭环状态机：错误 → 修复 → 验证 ─────────────

/**
 * 标记错误已修复（open → fixed）
 * @param {number} id - 错误 ID
 * @param {string} fixDetail - 修复说明
 */
function logFix(id, fixDetail = '') {
  const memory = loadMemory();
  const entry = memory.errors.find(e => e.id === id);
  if (!entry) return { success: false, reason: '错误不存在' };
  if (entry.status === 'verified') return { success: false, reason: '已验证无需再修复', id };
  entry.status = 'fixed';
  entry.fixDetail = fixDetail || entry.fixDetail || '';
  entry.fixedAt = new Date().toISOString();
  saveMemory(memory);
  return { success: true, id, status: 'fixed' };
}

/**
 * 验证修复有效（fixed → verified）
 * @param {number} id - 错误 ID
 * @param {string} verifyNote - 验证说明
 */
function logVerify(id, verifyNote = '') {
  const memory = loadMemory();
  const entry = memory.errors.find(e => e.id === id);
  if (!entry) return { success: false, reason: '错误不存在' };
  if (entry.status === 'open') {
    return { success: false, reason: '必须先 logFix 标记修复，才能验证', id };
  }
  entry.status = 'verified';
  entry.verifyNote = verifyNote || entry.verifyNote || '';
  entry.verifiedAt = new Date().toISOString();
  saveMemory(memory);
  return { success: true, id, status: 'verified' };
}

/**
 * 检查复发风险（闭环版）：已 verified 的错误降级为弱提醒，不再重复计数
 */
function checkRecurrence(context) {
  if (!context || typeof context !== 'string') return { warnings: [], safe: true };

  const memory = loadMemory();
  if (memory.errors.length === 0) return { warnings: [], safe: true };

  const warnings = [];

  // 只统计 open/fixed 的错误（verified 的不再算历史重犯）
  const activeErrors = memory.errors.filter(e => e.status !== 'verified');
  const categoryCounts = {};
  for (const e of activeErrors) {
    categoryCounts[e.category] = (categoryCounts[e.category] || 0) + 1;
  }

  // 对 open/fixed 错误生成预防警告
  for (const [category, count] of Object.entries(categoryCounts)) {
    if (count >= 1 && CATEGORIES[category]) {
      const cat = CATEGORIES[category];
      const triggered = cat.preventionPatterns.filter(p => context.includes(p));
      if (triggered.length > 0) {
        // 检查该分类是否有 verified 记录（已改好的）
        const verifiedCount = memory.errors.filter(e =>
          e.category === category && e.status === 'verified'
        ).length;
        const statusTag = verifiedCount > 0 ? `（同类已验证 ${verifiedCount} 次，但仍有 ${count} 条未闭环）` : '';
        warnings.push({
          category,
          label: cat.label,
          previousCount: count,
          triggeredPatterns: triggered,
          verifiedCount,
          advice: `之前${count}次在"${cat.label}"上犯过错${statusTag}，当前上下文有触发词"${triggered.join('、')}"，请注意。`,
        });
      }
    }
  }

  // 高频复发（open/fixed 且复发 2+ 次）
  const highRecurrence = activeErrors.filter(e => (e.recurrenceCount || 0) >= 2);
  for (const e of highRecurrence) {
    warnings.push({
      category: e.category,
      label: CATEGORIES[e.category]?.label || e.category,
      previousCount: (e.recurrenceCount || 0) + 1,
      status: e.status,
      advice: `"${e.detail.slice(0, 40)}"已经反复犯${(e.recurrenceCount || 0) + 1}次了${e.status === 'fixed' ? '（已标记修复，待验证）' : ''}。`,
      highRecurrence: true,
    });
  }

  return { warnings, safe: warnings.length === 0 };
}

// ─── 分类判别（错误分类学）─────────────────────────

/**
 * 判别任意错误属于哪一类，并给出恢复策略
 * @param {Error|string} error - 错误对象或消息
 * @param {object} [context] - { status, code, url }
 * @returns {object} 分类结果
 */
function classifyError(error, context = {}) {
  const result = taxonomy.classify(error, context);
  return {
    ...result,
    recovery: result.recovery,
    retryable: result.retryable,
    preventionRule: generatePreventionRule(result.code),
  };
}

/**
 * 获取某分类的恢复策略
 */
function getErrorRecovery(code) {
  return taxonomy.getRecovery(code);
}

/**
 * 错误分类统计
 */
function getTaxonomyStats() {
  return taxonomy.getStats();
}

// ─── 生成预防规则 ─────────────────────────

function generatePreventionRule(category) {
  if (!category || !CATEGORIES[category]) return null;

  const cat = CATEGORIES[category];
  return {
    category,
    name: `prevent_${category}`,
    triggeredBy: cat.preventionPatterns,
    action: 'caution',
    message: `上次在"${cat.label}"上犯过错，请注意避免同类问题。`,
  };
}

// ─── 获取统计 ─────────────────────────

function getStats() {
  const memory = loadMemory();
  const byCategory = {};
  const byStatus = { open: 0, fixed: 0, verified: 0 };
  for (const e of memory.errors) {
    byCategory[e.category] = (byCategory[e.category] || 0) + 1;
    byStatus[e.status || 'open'] = (byStatus[e.status || 'open'] || 0) + 1;
  }
  return {
    total: memory.errors.length,
    byCategory,
    byStatus,
    // [v6.6.0] 闭环率: 已闭环(verified) / 总数
    closedRate: memory.errors.length > 0
      ? Math.round((byStatus.verified / memory.errors.length) * 1000) / 100
      : 0,
    highRecurrence: memory.errors.filter(e => (e.recurrenceCount || 0) >= 2).length,
  };
}

module.exports = {
  logCorrection,
  logFix,
  logVerify,
  checkRecurrence,
  generatePreventionRule,
  getStats,
  classifyError,
  getErrorRecovery,
  getTaxonomyStats,
  CATEGORIES,
  clearMemory: () => saveMemory({ errors: [], version: '1.0' }),
};
