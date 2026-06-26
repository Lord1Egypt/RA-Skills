'use strict';

// -----------------------------------------------------------------------
// prompt-builder.js — 报告助手 Prompt 构建器
//
// 依赖：仅 Node.js 内置模块（fs, path）
// 合规依据：噗滋慈善 Spec v1.0 + PIPL 第23/28条 + 慈善法第75/77条
// PII 安全：contact_name / contact_phone 绝不写入 prompt
// -----------------------------------------------------------------------

const fs = require('fs');
const path = require('path');

// -----------------------------------------------------------------------
// 报告类型 → 模板文件名映射
// -----------------------------------------------------------------------

/**
 * 根据报告类型和资助平台确定模板文件名
 * @param {string} reportType
 * @param {string} [funderPlatform]
 * @returns {string} 模板文件名
 */
function resolveTemplateFilename(reportType, funderPlatform) {
  if (reportType === 'annual_work') {
    return 'annual-work-v1.md';
  }
  if (reportType === 'project_final') {
    if (funderPlatform === 'tencent') {
      return 'project-final-tencent-v1.md';
    }
    return 'project-final-generic-v1.md';
  }
  if (reportType === 'finance_final') {
    return 'finance-final-v1.md';
  }
  throw new Error(`未知报告类型：${reportType}`);
}

// -----------------------------------------------------------------------
// YAML frontmatter 解析（仅用正则，不引入 yaml 库）
// -----------------------------------------------------------------------

/**
 * 解析 Markdown 文件中的 YAML frontmatter（--- 包裹的块）
 * 支持 "key: value" 格式，value 为字符串或简单布尔/数字
 * @param {string} raw 原始文件内容
 * @returns {{ metadata: Object, content: string }}
 */
function parseFrontmatter(raw) {
  const frontmatterPattern = /^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/;
  const match = raw.match(frontmatterPattern);

  if (!match) {
    // 无 frontmatter，整体作为 content
    return { metadata: {}, content: raw };
  }

  const yamlBlock = match[1];
  const content = match[2];
  const metadata = {};

  // 允许的 frontmatter 字段白名单（防供应链 prompt injection）
  const ALLOWED_METADATA_KEYS = new Set([
    'source_url', 'verified_date', 'next_review_date', 'version',
    'breaking_change', 'report_type', 'funder_platform',
  ]);

  for (const line of yamlBlock.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;

    // YAML 键值分隔符为 ": "（冒号+空格），支持 value 中含冒号（如 URL）
    const colonSpaceIdx = trimmed.indexOf(': ');
    const colonIdx = colonSpaceIdx !== -1 ? colonSpaceIdx : trimmed.indexOf(':');
    if (colonIdx === -1) continue;

    const key = trimmed.slice(0, colonIdx).trim();
    const rawVal = trimmed.slice(colonIdx + (colonSpaceIdx !== -1 ? 2 : 1)).trim();

    // 简单类型转换
    if (rawVal === 'true') {
      metadata[key] = true;
    } else if (rawVal === 'false') {
      metadata[key] = false;
    } else if (rawVal !== '' && !isNaN(Number(rawVal))) {
      metadata[key] = Number(rawVal);
    } else {
      // 移除可能的引号包裹
      metadata[key] = rawVal.replace(/^['"]|['"]$/g, '');
    }
  }

  // 白名单过滤：只保留已知安全字段，丢弃未知字段（防供应链注入）
  const filteredMetadata = {};
  for (const [k, v] of Object.entries(metadata)) {
    if (ALLOWED_METADATA_KEYS.has(k)) {
      filteredMetadata[k] = v;
    }
  }

  return { metadata: filteredMetadata, content };
}

// -----------------------------------------------------------------------
// 1. loadTemplate
// -----------------------------------------------------------------------

/**
 * 从 templates/ 目录读取对应模板文件，解析 YAML frontmatter 和 markdown 正文。
 *
 * 映射规则：
 *   annual_work                        → annual-work-v1.md
 *   project_final + tencent            → project-final-tencent-v1.md
 *   project_final + 其他               → project-final-generic-v1.md
 *   finance_final                      → finance-final-v1.md
 *
 * @param {string} reportType
 * @param {string} [funderPlatform]
 * @returns {{ metadata: Object, content: string }}
 */
function loadTemplate(reportType, funderPlatform) {
  const filename = resolveTemplateFilename(reportType, funderPlatform);
  const filePath = path.join(__dirname, '..', 'templates', filename);

  let raw;
  try {
    raw = fs.readFileSync(filePath, 'utf8');
  } catch {
    throw new Error(`模板加载失败：${filename}（报告类型：${reportType}）`);
  }

  return parseFrontmatter(raw);
}

// -----------------------------------------------------------------------
// 2. buildSystemPrompt
// -----------------------------------------------------------------------

/**
 * 根据报告类型获取法定必要章节列表（用于 system prompt 嵌入）
 * @param {string} reportType
 * @returns {string[]}
 */
function getRequiredSections(reportType) {
  const sections = {
    annual_work: [
      '组织基本信息',
      '年度工作概述',
      '项目执行情况',
      '财务概况',
      '人员与志愿者',
      '治理与内部管理',
      '面临的挑战与应对',
      '下一年度工作计划',
    ],
    project_final: [
      '项目基本信息',
      '目标与指标完成情况',
      '主要活动执行情况',
      '财务使用情况',
      '受益对象情况',
      '项目成效与经验总结',
      '问题与挑战',
    ],
    finance_final: [
      '项目收支概况',
      '支出明细',
      '预算执行分析',
      '结余资金处理方案',
    ],
  };
  return sections[reportType] || [];
}

/**
 * 根据报告类型和模型类型生成 system prompt。
 *
 * 公共部分（所有模型）：
 *   - 角色定义
 *   - 格式指令（正式公文体、第三方语气、中文数字章节标题）
 *   - 合规要求（法定必要章节）
 *   - 数据诚信约束（不编造数字、占位符）
 *
 * 模型差异追加：
 *   - hunyuan：政府公文用语
 *   - deepseek：仅输出正文，不添加元注释
 *   - doubao：受益人故事段落语气 + 整体风格边界 + Markdown 格式
 *
 * @param {string} reportType
 * @param {string} [modelType='hunyuan']
 * @returns {string}
 */
function buildSystemPrompt(reportType, modelType = 'hunyuan') {
  const requiredSections = getRequiredSections(reportType);
  const sectionsList = requiredSections.map((s) => `- ${s}`).join('\n');

  // 公共部分
  const common = [
    '你是一名经验丰富的公益项目报告撰写专家，熟悉中国慈善法规定的社会组织信息公开要求。',
    '这是一份提交给政府主管部门/资助基金会的正式工作报告。',
    '',
    '【重要】请直接根据用户提供的数据生成报告正文内容（封面+各章节完整文本），不要输出模板说明、字段定义或格式指引。',
    '',
    '请使用正式公文体，使用第三方陈述语气（"本组织"而非"我们"），章节标题用中文数字。',
    `请确保报告包含以下法定必要章节：\n${sectionsList}`,
    '不要添加任何非用户提供的数据，不要虚构具体数字。',
    '无法确认的字段请输出 [请填写实际数据] 占位符。',
    '受益人群体描述使用行政化表达（如"特殊困难群体"），避免直接描述敏感病情或残障细节。',
  ].join('\n');

  // 模型专项追加
  const modelSpecific = {
    hunyuan: '请使用规范的政府公文用语，避免口语化表达。',
    deepseek: [
      '支出差异超过预算±10%的每行必须给出解释说明。',
      '仅输出报告正文，不要添加任何解释或元注释。',
    ].join('\n'),
    doubao: [
      '受益人故事段落：请用温暖、有人情味但不煽情的语气撰写，字数控制在200字以内。',
      '报告整体保持正式，仅故事章节可适当情感化。',
      '不要使用过于励志或营销化的表达，保持公益机构的专业性。',
      '请用Markdown格式输出。',
    ].join('\n'),
  };

  const extra = modelSpecific[modelType] || '';

  return extra ? `${common}\n${extra}` : common;
}

// -----------------------------------------------------------------------
// 3. formatCurrency
// -----------------------------------------------------------------------

/**
 * 数值格式化：添加千位分隔符并追加"元"单位。
 * 有小数时保留两位小数，整数时不显示小数部分。
 *
 * 示例：
 *   formatCurrency(1580000)  → "1,580,000元"
 *   formatCurrency(287600.5) → "287,600.50元"
 *   formatCurrency(0)        → "0元"
 *
 * @param {number} amount
 * @returns {string}
 */
function formatCurrency(amount) {
  if (typeof amount !== 'number' || !isFinite(amount)) {
    return '[请填写实际金额]';
  }

  // 判断是否有小数（浮点精度处理：先固定到10位再判断）
  const hasDecimal = Math.abs(amount - Math.floor(amount)) > 1e-9;

  if (hasDecimal) {
    // 保留两位小数，再加千位分隔符
    const [intPart, decPart] = amount.toFixed(2).split('.');
    const intFormatted = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return `${intFormatted}.${decPart}元`;
  } else {
    const intStr = Math.round(amount).toString();
    const intFormatted = intStr.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return `${intFormatted}元`;
  }
}

// -----------------------------------------------------------------------
// 货币字段集合（用于 buildUserPrompt 中自动格式化）
// -----------------------------------------------------------------------

const CURRENCY_FIELDS = new Set([
  'total_income',
  'total_expenditure',
  'total_budget',
  'actual_expenditure',
  'total_grant',
  'unexpended_balance',
  'year_end_balance',
]);

// -----------------------------------------------------------------------
// 4. buildUserPrompt
// -----------------------------------------------------------------------

/**
 * 将用户输入数据格式化为 user prompt。
 *
 * 安全约束（F-07）：
 *   piiFields 中列出的字段（contact_name, contact_phone）必须从 input
 *   中排除，绝不出现在 prompt 文本中。
 *
 * 格式差异：
 *   - deepseek：使用 XML 标签 <data>...</data><instruction>...</instruction>
 *   - 其他模型：普通 JSON + 指令文本
 *
 * @param {object} input 用户输入数据
 * @param {string} templateContent 模板正文（已去除 frontmatter）
 * @param {string[]} piiFields 需要排除的 PII 字段名列表
 * @param {string} [modelType='hunyuan']
 * @returns {string}
 */
function buildUserPrompt(input, templateContent, piiFields, modelType = 'hunyuan') {
  // 构建排除集合（防御性处理：确保始终排除 contact_name / contact_phone）
  // 内部字段 + PII 字段统一排除
  const INTERNAL_FIELDS = ['_regenerate_section'];
  const excludeSet = new Set([
    ...INTERNAL_FIELDS,
    ...(Array.isArray(piiFields) ? piiFields : []),
    'contact_name',
    'contact_phone',
  ]);

  // 从 input 中剔除 PII 字段，并格式化货币字段
  const safeData = {};
  for (const [key, value] of Object.entries(input)) {
    if (excludeSet.has(key)) continue;

    // 货币字段：如果是数字则格式化显示，原始值也保留（以 _formatted 后缀区分）
    if (CURRENCY_FIELDS.has(key) && typeof value === 'number') {
      safeData[key] = formatCurrency(value);
    } else if (key === 'story_case' && Array.isArray(value)) {
      // 截断保护：最多取前 5 条案例（防 token 溢出）
      safeData[key] = value.slice(0, 5);
    } else {
      safeData[key] = value;
    }
  }

  const dataJson = JSON.stringify(safeData, null, 2);

  // 提取模板章节结构作为输出格式指引（取前 60 行避免 token 过长）
  const templateLines = templateContent.split('\n');
  const templateStructure = templateLines.slice(0, 60).join('\n');

  if (modelType === 'deepseek') {
    // DeepSeek：XML 标签分隔数据与指令（提升准确率）
    return [
      `<data>`,
      dataJson,
      `</data>`,
      `<instruction>`,
      `请根据上述数据和以下模板要求生成完整报告：`,
      ``,
      templateStructure,
      `</instruction>`,
    ].join('\n');
  }

  // 混元 / 豆包及其他模型：普通 JSON + 指令格式
  return [
    `以下是报告所需的数据（JSON格式）：`,
    ``,
    `\`\`\`json`,
    dataJson,
    `\`\`\``,
    ``,
    `请根据上述数据，按照以下模板章节结构生成完整报告：`,
    ``,
    templateStructure,
  ].join('\n');
}

// -----------------------------------------------------------------------
// 5. buildPrompt（主入口）
// -----------------------------------------------------------------------

/**
 * 组装完整 prompt messages 数组（OpenAI-compatible messages 格式）。
 *
 * @param {object} input 用户输入数据（已通过 validators.js 校验）
 * @param {string} [modelType='hunyuan'] 目标模型
 * @returns {Array<{ role: string, content: string }>}
 */
function buildPrompt(input, modelType = 'hunyuan') {
  const template = loadTemplate(input.report_type, input.funder_platform);
  const { piiFields } = require('./validators').validatePIISafety(input);
  const systemPrompt = buildSystemPrompt(input.report_type, modelType);
  const userPrompt = buildUserPrompt(input, template.content, piiFields, modelType);

  return [
    { role: 'system', content: systemPrompt },
    { role: 'user', content: userPrompt },
  ];
}

// -----------------------------------------------------------------------
// 导出
// -----------------------------------------------------------------------

module.exports = {
  buildPrompt,
  buildSystemPrompt,
  buildUserPrompt,
  loadTemplate,
  formatCurrency,
};
