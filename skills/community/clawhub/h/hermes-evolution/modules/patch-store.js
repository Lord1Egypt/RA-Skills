/**
 * PatchStore - P0-1 patch增量更新
 * 
 * 核心改进：
 * 1. Append-only corrections - 新correction直接追加，不读写全量
 * 2. JSON Patch for rules - 只更新变化的字段
 * 3. 索引文件加速读取 - 内存索引 + 增量加载
 */

const fs = require('fs');
const path = require('path');

const BASE_DIR = path.join(__dirname);
const CORRECTIONS_DIR = path.join(BASE_DIR, 'corrections');
const RULES_DIR = path.join(BASE_DIR, 'rules');
const INDEX_DIR = path.join(BASE_DIR, '.patch-index');

// 确保目录存在
function init() {
  if (!fs.existsSync(CORRECTIONS_DIR)) {
    fs.mkdirSync(CORRECTIONS_DIR, { recursive: true });
  }
  if (!fs.existsSync(RULES_DIR)) {
    fs.mkdirSync(RULES_DIR, { recursive: true });
  }
  if (!fs.existsSync(INDEX_DIR)) {
    fs.mkdirSync(INDEX_DIR, { recursive: true });
  }
}

/**
 * 追加一条 correction（增量写入）
 */
function appendCorrection(record) {
  init();
  
  const dateStr = new Date().toISOString().split('T')[0];
  const appendFile = path.join(CORRECTIONS_DIR, `${dateStr}.jsonl`);  // .jsonl = JSON Lines
  
  // 每行一条JSON record
  const line = JSON.stringify(record) + '\n';
  fs.appendFileSync(appendFile, line, 'utf-8');
  
  // 更新索引
  updateCorrectionIndex(dateStr, record);
  
  console.log(`[PatchStore] ➕ 追加correction: ${record.id}`);
  return record;
}

/**
 * 读取某天的所有 corrections（兼容旧格式）
 */
function loadCorrectionsByDate(dateStr) {
  const jsonFile = path.join(CORRECTIONS_DIR, `${dateStr}.json`);  // 旧格式
  const jsonlFile = path.join(CORRECTIONS_DIR, `${dateStr}.jsonl`);  // 新格式
  
  const corrections = [];
  
  // 读取旧格式
  if (fs.existsSync(jsonFile)) {
    try {
      const data = JSON.parse(fs.readFileSync(jsonFile, 'utf-8'));
      if (Array.isArray(data)) {
        corrections.push(...data);
      }
    } catch (e) {
      console.warn(`[PatchStore] ⚠️ 读取旧格式失败: ${jsonFile}`);
    }
  }
  
  // 读取新格式（增量追加）
  if (fs.existsSync(jsonlFile)) {
    const lines = fs.readFileSync(jsonlFile, 'utf-8').split('\n').filter(l => l.trim());
    for (const line of lines) {
      try {
        corrections.push(JSON.parse(line));
      } catch (e) {
        // 忽略解析错误
      }
    }
  }
  
  // 按时间排序
  return corrections.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
}

/**
 * 更新 correction 索引
 */
function updateCorrectionIndex(dateStr, newRecord) {
  const indexFile = path.join(INDEX_DIR, `corrections-${dateStr}.json`);
  
  let index = { count: 0, ids: [], lastUpdated: null };
  if (fs.existsSync(indexFile)) {
    try {
      index = JSON.parse(fs.readFileSync(indexFile, 'utf-8'));
    } catch (e) {}
  }
  
  index.count++;
  index.ids.push(newRecord.id);
  index.lastUpdated = new Date().toISOString();
  
  fs.writeFileSync(indexFile, JSON.stringify(index, null, 2), 'utf-8');
}

/**
 * 增量更新规则（只写变化的部分）
 */
function patchRule(ruleId, patch) {
  init();
  
  const ruleFile = path.join(RULES_DIR, `${ruleId}.json`);
  
  if (!fs.existsSync(ruleFile)) {
    throw new Error(`规则 ${ruleId} 不存在`);
  }
  
  // 读取当前规则
  const rule = JSON.parse(fs.readFileSync(ruleFile, 'utf-8'));
  
  // 应用 patch
  const patchedRule = applyPatch(rule, patch);
  
  // 写入 patch 记录
  const patchFile = path.join(RULES_DIR, `${ruleId}.patch`);
  const patchRecord = {
    timestamp: new Date().toISOString(),
    patch,
    fromVersion: rule.version,
    toVersion: patchedRule.version
  };
  fs.appendFileSync(patchFile, JSON.stringify(patchRecord) + '\n', 'utf-8');
  
  // 只写入变化的部分 + 必要元数据（不是全部）
  const lightweightRule = {
    id: patchedRule.id,
    version: patchedRule.version,
    updatedAt: patchedRule.updatedAt,
    ...patch  // 只写入变化的字段
  };
  
  fs.writeFileSync(ruleFile, JSON.stringify(lightweightRule, null, 2), 'utf-8');
  
  console.log(`[PatchStore] 📝 PATCH规则: ${ruleId} (v${rule.version} → v${patchedRule.version})`);
  return patchedRule;
}

/**
 * 应用 JSON Merge Patch (RFC 7396)
 */
function applyPatch(obj, patch) {
  const result = { ...obj };
  
  for (const [key, value] of Object.entries(patch)) {
    if (value === null) {
      // null 表示删除
      delete result[key];
    } else if (typeof value === 'object' && !Array.isArray(value)) {
      // 递归合并
      result[key] = applyPatch(result[key] || {}, value);
    } else {
      result[key] = value;
    }
  }
  
  return result;
}

/**
 * 获取轻量级规则（只有变更）
 */
function getRuleLight(ruleId) {
  const ruleFile = path.join(RULES_DIR, `${ruleId}.json`);
  if (!fs.existsSync(ruleFile)) return null;
  return JSON.parse(fs.readFileSync(ruleFile, 'utf-8'));
}

/**
 * 获取完整规则（含历史）
 */
function getRuleFull(ruleId) {
  const ruleFile = path.join(RULES_DIR, `${ruleId}.json`);
  const patchFile = path.join(RULES_DIR, `${ruleId}.patch`);
  
  if (!fs.existsSync(ruleFile)) return null;
  
  // 读取基础规则
  let rule = JSON.parse(fs.readFileSync(ruleFile, 'utf-8'));
  
  // 应用所有 patch
  if (fs.existsSync(patchFile)) {
    const patches = fs.readFileSync(patchFile, 'utf-8')
      .split('\n')
      .filter(l => l.trim())
      .map(l => JSON.parse(l))
      .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
    
    for (const p of patches) {
      rule = applyPatch(rule, p.patch);
    }
  }
  
  return rule;
}

/**
 * 获取统计（使用索引加速）
 */
function getCorrectionStats() {
  init();
  
  const files = fs.readdirSync(CORRECTIONS_DIR).filter(f => f.endsWith('.json') || f.endsWith('.jsonl'));
  let total = 0;
  let unresolved = 0;
  
  for (const file of files) {
    const dateStr = file.replace('.json', '').replace('.jsonl', '');
    const indexFile = path.join(INDEX_DIR, `corrections-${dateStr}.json`);
    
    if (fs.existsSync(indexFile)) {
      try {
        const index = JSON.parse(fs.readFileSync(indexFile, 'utf-8'));
        total += index.count;
      } catch (e) {}
    }
  }
  
  // 需要精确统计时再读取文件
  const today = new Date().toISOString().split('T')[0];
  const todayCorrections = loadCorrectionsByDate(today);
  unresolved = todayCorrections.filter(c => !c.resolved).length;
  
  return { total, today: todayCorrections.length, unresolved };
}

// 导出
module.exports = {
  appendCorrection,
  loadCorrectionsByDate,
  patchRule,
  getRuleLight,
  getRuleFull,
  getCorrectionStats,
  CORRECTIONS_DIR,
  RULES_DIR
};
