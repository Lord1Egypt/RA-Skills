'use strict';

// -----------------------------------------------------------------------
// knowledge-base.js — 管理顾问 Skill 内嵌知识库（v1.0）
//
// 依赖：仅 Node.js 内置模块（fs, path）
// 职责：从 templates/*.md 加载知识库文件，按问题类别索引，
//       供 prompt-builder.js 将相关知识段落嵌入 system prompt。
//
// 架构说明：
//   - v1.0：知识内嵌 prompt（本文件），8000 tokens 以内
//   - v1.1（规划中）：迁移至向量数据库 RAG 检索
//
// 知识库文件（templates/ 目录）：
//   knowledge-charity-law.md   → policy_qa（慈善法/公募/信息公开）
//   knowledge-compliance-faq.md → compliance_ops + faq（年检/税务/劳动）
//   knowledge-governance.md    → governance（理事会/财务内控/人力）
//
// 问题类型映射（Spec 第4节）：
//   policy_qa      → knowledge-charity-law.md
//   compliance     → knowledge-compliance-faq.md（Segment B）
//   governance     → knowledge-governance.md
//   finance        → knowledge-compliance-faq.md（Segment D 税务部分）
//   hr             → knowledge-compliance-faq.md（Segment D 劳动用工）
//   other / mixed  → 全量知识段落
// -----------------------------------------------------------------------

const fs   = require('fs');
const path = require('path');

// -----------------------------------------------------------------------
// 知识库文件路径常量
// -----------------------------------------------------------------------

const KNOWLEDGE_DIR = path.join(__dirname, '..', 'templates');

const KB_FILES = {
  charity_law:  'knowledge-charity-law.md',
  compliance:   'knowledge-compliance-faq.md',
  governance:   'knowledge-governance.md',
};

// -----------------------------------------------------------------------
// YAML frontmatter 解析（轻量实现，不引入 yaml 库）
// -----------------------------------------------------------------------

/**
 * 白名单 frontmatter 字段（防供应链 prompt injection）
 * 只解析已知安全的元数据字段
 */
const ALLOWED_METADATA_KEYS = new Set([
  'version', 'source_url', 'verified_date', 'segment',
]);

/**
 * 解析 Markdown 文件中的 YAML frontmatter（--- 包裹的块）
 *
 * @param {string} raw - 原始文件内容
 * @returns {{ metadata: Object, content: string }}
 */
function parseFrontmatter(raw) {
  const frontmatterPattern = /^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/;
  const match = raw.match(frontmatterPattern);

  if (!match) {
    return { metadata: {}, content: raw };
  }

  const yamlBlock = match[1];
  const content   = match[2];
  const rawMeta   = {};

  for (const line of yamlBlock.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;

    const colonIdx = trimmed.indexOf(': ');
    const colonOnly = colonIdx === -1 ? trimmed.indexOf(':') : -1;
    const idx = colonIdx !== -1 ? colonIdx : colonOnly;
    if (idx === -1) continue;

    const key    = trimmed.slice(0, idx).trim();
    const rawVal = trimmed.slice(idx + (colonIdx !== -1 ? 2 : 1)).trim();

    rawMeta[key] = rawVal.replace(/^['"]|['"]$/g, '');
  }

  // 白名单过滤：只保留已知安全字段
  const metadata = {};
  for (const [k, v] of Object.entries(rawMeta)) {
    if (ALLOWED_METADATA_KEYS.has(k)) {
      metadata[k] = v;
    }
  }

  return { metadata, content };
}

// -----------------------------------------------------------------------
// 知识库加载缓存（进程内单例，避免每次请求重复读盘）
// -----------------------------------------------------------------------

/** @type {Map<string, { metadata: Object, content: string }>} */
const _cache = new Map();

/**
 * 加载单个知识库文件，解析 frontmatter 和正文。
 * 结果缓存在进程内存，重启后重新加载。
 *
 * @param {string} filename - 文件名（如 'knowledge-charity-law.md'）
 * @returns {{ metadata: Object, content: string }}
 * @throws {Error} 文件不存在或读取失败
 */
function loadKnowledgeFile(filename) {
  if (_cache.has(filename)) {
    return _cache.get(filename);
  }

  const filePath = path.join(KNOWLEDGE_DIR, filename);
  let raw;
  try {
    raw = fs.readFileSync(filePath, 'utf8');
  } catch {
    throw new Error(`知识库文件加载失败：${filename}（路径：${filePath}）`);
  }

  const parsed = parseFrontmatter(raw);
  _cache.set(filename, parsed);
  return parsed;
}

/**
 * 清除进程内知识库缓存（主要用于测试）
 */
function clearCache() {
  _cache.clear();
}

// -----------------------------------------------------------------------
// 问题类别 → 知识库文件映射
// -----------------------------------------------------------------------

/**
 * 按 question_category（或自动识别的内部类型）返回需要加载的知识库文件列表。
 *
 * 映射规则（与 Spec 第 4、7 节一致）：
 *   policy_qa  → charity_law
 *   compliance → compliance（含 B1-B4）
 *   governance → governance
 *   finance    → compliance（Segment D 税务部分）
 *   hr         → compliance（Segment D 劳动用工）
 *   other/mixed/undefined → 全量（全部三个文件）
 *
 * @param {string|undefined} category - question_category 枚举值或内部分类标签
 * @returns {string[]} 需要加载的文件名列表
 */
function resolveCategoryFiles(category) {
  const map = {
    policy_qa:  [KB_FILES.charity_law],
    charity_law: [KB_FILES.charity_law],
    compliance: [KB_FILES.compliance],
    governance: [KB_FILES.governance],
    finance:    [KB_FILES.compliance],
    hr:         [KB_FILES.compliance],
    other:      [KB_FILES.charity_law, KB_FILES.compliance, KB_FILES.governance],
  };

  const files = map[category];
  if (!files) {
    // 未知类别或 mixed → 全量
    return [KB_FILES.charity_law, KB_FILES.compliance, KB_FILES.governance];
  }
  return files;
}

// -----------------------------------------------------------------------
// 关键词自动分类（Spec 第 4 节，v1.0 关键词匹配）
// -----------------------------------------------------------------------

/**
 * 关键词 → 内部分类标签映射
 * 顺序重要：先匹配到的类型优先
 *
 * @type {Array<{ category: string, keywords: string[] }>}
 */
const KEYWORD_CATEGORY_MAP = [
  {
    category: 'policy_qa',
    keywords: [
      '慈善法', '法规', '政策', '修订', '要求规定', '违法', '处罚',
      '公募', '募捐', '基金会管理', '登记管理', '认定', '资格证',
    ],
  },
  {
    category: 'compliance',
    keywords: [
      '年检', '信息公开', '章程变更', '平台报告', '公示', '期限', '流程',
      '年度报告', '腾讯公益', '壹基金', '南都', '慈善中国', '年度检查',
    ],
  },
  {
    category: 'governance',
    keywords: [
      '理事会', '监事会', '章程', '决议', '法定代表人', '财务印章',
      '档案', '理事', '监事', '会议', '印章', '内控', '授权审批',
    ],
  },
  {
    category: 'finance',
    keywords: [
      '税务', '发票', '增值税', '企业所得税', '免税', '捐赠扣除',
      'PD资格', '税前扣除', '开票', '财务报告', '审计', '会计',
    ],
  },
  {
    category: 'hr',
    keywords: [
      '劳动合同', '社保', '个税', '志愿者', '实习', '试用期',
      '员工', '工资', '报销', '话费', '离职', '辞职', '解雇',
    ],
  },
];

/**
 * 根据问题文本进行关键词匹配，自动识别问题类别。
 *
 * 匹配逻辑：
 *   - 遍历 KEYWORD_CATEGORY_MAP，统计各类别的关键词命中数
 *   - 命中数最多的类别胜出
 *   - 多个类别命中数并列（且命中数>0）→ 返回 'other'（mixed，加载全量知识）
 *   - 无任何命中 → 返回 'other'
 *
 * @param {string} questionText - 用户提问文本
 * @returns {string} 识别到的内部类别标签
 */
function classifyQuestion(questionText) {
  if (typeof questionText !== 'string' || !questionText.trim()) {
    return 'other';
  }

  const counts = {};
  let maxCount = 0;

  for (const { category, keywords } of KEYWORD_CATEGORY_MAP) {
    let count = 0;
    for (const kw of keywords) {
      if (questionText.includes(kw)) {
        count++;
      }
    }
    counts[category] = count;
    if (count > maxCount) maxCount = count;
  }

  if (maxCount === 0) {
    return 'other';
  }

  // 找出并列最高的类别
  const topCategories = Object.entries(counts)
    .filter(([, c]) => c === maxCount)
    .map(([cat]) => cat);

  if (topCategories.length === 1) {
    return topCategories[0];
  }

  // 多类别并列 → mixed，加载全量
  return 'other';
}

// -----------------------------------------------------------------------
// 主入口：parseKnowledgeBase
// -----------------------------------------------------------------------

/**
 * 根据问题类别加载并返回相关知识库条目，供嵌入 system prompt。
 *
 * 流程：
 *   1. 根据 category 确定需要加载的文件列表
 *   2. 加载各文件（使用缓存）
 *   3. 返回知识库文本（按文件拼接，含 metadata 版本信息）
 *
 * @param {string|undefined} category - question_category 枚举值或 classifyQuestion 的返回值
 * @returns {{ text: string, sources: string[], version: string }}
 *   - text：知识库正文，供嵌入 prompt
 *   - sources：文件来源列表（用于日志）
 *   - version：知识库版本摘要（格式："v20260330"）
 */
function parseKnowledgeBase(category) {
  const filenames = resolveCategoryFiles(category);
  const parts     = [];
  const sources   = [];
  const versions  = [];

  for (const filename of filenames) {
    let parsed;
    try {
      parsed = loadKnowledgeFile(filename);
    } catch {
      // 知识库文件加载失败 → 记录错误但不抛出，返回降级内容
      parts.push(`[知识库加载失败：${filename}，请稍后重试]`);
      sources.push(filename);
      continue;
    }

    const { metadata, content } = parsed;
    parts.push(content);
    sources.push(filename);
    if (metadata.version) {
      versions.push(metadata.version);
    }
  }

  const text    = parts.join('\n\n---\n\n');
  const version = versions.length > 0
    ? versions[0]
    : 'unknown';

  return { text, sources, version };
}

// -----------------------------------------------------------------------
// 导出
// -----------------------------------------------------------------------

module.exports = {
  parseKnowledgeBase,
  classifyQuestion,
  loadKnowledgeFile,
  clearCache,
  resolveCategoryFiles,
  KB_FILES,
  KEYWORD_CATEGORY_MAP,
};
