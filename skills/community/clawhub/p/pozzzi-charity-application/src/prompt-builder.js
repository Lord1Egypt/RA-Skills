'use strict';

// -----------------------------------------------------------------------
// prompt-builder.js — 申报助手 Prompt 构建器
//
// 依赖：仅 Node.js 内置模块（fs, path）
// 合规依据：噗滋慈善申报助手 Spec v1.0 + PIPL 第23/28条
//          + 慈善法第75/77条 + 生成式AI暂行办法第4/8条
// PII 安全：contact_name / contact_phone 绝不写入 prompt
// placeholder-enforcer：扫描模型输出，替换疑似 AI 编造的编号
// -----------------------------------------------------------------------

const fs = require('fs');
const path = require('path');

// -----------------------------------------------------------------------
// 申报类型 → 模板文件名映射
// -----------------------------------------------------------------------

/**
 * 根据申报类型确定模板文件名
 * @param {string} applicationType
 * @returns {string} 模板文件名
 */
function resolveTemplateFilename(applicationType) {
  const MAP = {
    generic: 'application-generic-v1.md',
    tencent99: 'application-tencent99-v1.md',
    govt_purchase: 'application-govt-purchase-v1.md',
  };

  if (!Object.prototype.hasOwnProperty.call(MAP, applicationType)) {
    throw new Error(`未知申报类型：${applicationType}`);
  }

  return MAP[applicationType];
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
  const rawMetadata = {};

  // 允许的 frontmatter 字段白名单（防供应链 prompt injection）
  const ALLOWED_METADATA_KEYS = new Set([
    'source_url', 'verified_date', 'next_review_date', 'version',
    'breaking_change', 'application_type',
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
      rawMetadata[key] = true;
    } else if (rawVal === 'false') {
      rawMetadata[key] = false;
    } else if (rawVal !== '' && !isNaN(Number(rawVal))) {
      rawMetadata[key] = Number(rawVal);
    } else {
      // 移除可能的引号包裹
      rawMetadata[key] = rawVal.replace(/^['"]|['"]$/g, '');
    }
  }

  // 白名单过滤：只保留已知安全字段，丢弃未知字段（防供应链注入）
  const metadata = {};
  for (const [k, v] of Object.entries(rawMetadata)) {
    if (ALLOWED_METADATA_KEYS.has(k)) {
      metadata[k] = v;
    }
  }

  return { metadata, content };
}

// -----------------------------------------------------------------------
// 1. loadTemplate
// -----------------------------------------------------------------------

/**
 * 从 templates/ 目录读取对应模板文件，解析 YAML frontmatter 和 markdown 正文。
 *
 * 映射规则：
 *   generic       → application-generic-v1.md
 *   tencent99     → application-tencent99-v1.md
 *   govt_purchase → application-govt-purchase-v1.md
 *
 * @param {string} applicationType
 * @returns {{ metadata: Object, content: string }}
 */
function loadTemplate(applicationType) {
  const filename = resolveTemplateFilename(applicationType);
  const filePath = path.join(__dirname, '..', 'templates', filename);

  let raw;
  try {
    raw = fs.readFileSync(filePath, 'utf8');
  } catch {
    // 错误消息不暴露完整文件系统路径
    throw new Error(`模板加载失败：${filename}（申报类型：${applicationType}）`);
  }

  return parseFrontmatter(raw);
}

// -----------------------------------------------------------------------
// 2. buildSystemPrompt
// -----------------------------------------------------------------------

/**
 * 生成内容真实性约束文本（Spec 第 420-432 行，所有模型通用）
 * @returns {string}
 */
function getIntegrityConstraint() {
  return [
    '【内容真实性约束】',
    '你正在帮助一家中国公益组织撰写项目申报书。以下规则不可违反：',
    '1. 禁止编造任何统计数字、调研数据、需求数据（如"本地区有XX名留守儿童"）',
    '   → 若用户未提供数据，在对应位置输出：[请填写来源数据]',
    '2. 禁止生成任何预算金额。预算数字必须严格来自用户输入的 budget_breakdown 字段',
    '   → 若某预算项金额未填写，输出：[请填写预算金额]',
    '3. 禁止生成任何证书编号、登记证号、项目编号、政府文件编号',
    '   → 在对应位置输出：[请填写XXX编号]',
    '4. 若某章节对应的用户输入内容不足，直接说明该章节需要补充，不要自行发挥填充',
    '5. 申报书中的预期成效数字必须来自用户填写的 expected_outcomes，不得自行设定指标值',
  ].join('\n');
}

/**
 * 根据申报类型和模型类型生成 system prompt。
 *
 * 公共部分（所有模型）：
 *   - 角色定义（公益申报专家）
 *   - 格式指令（正式公文体、本机构、中文数字章节标题）
 *   - 内容真实性约束（Spec 第420-432行完整嵌入）
 *
 * 模型差异追加：
 *   - hunyuan：注重逻辑性，"问题-目标-活动-成效"因果链
 *   - deepseek：XML 标签，严格禁止虚构，仅输出正文
 *   - doubao：温暖语气（仅项目简介章节），不过度煽情
 *   - glm：注重说服力（等同 deepseek 策略）
 *
 * temperature: 0.5（比报告助手的 0.3 高，申报书需更有说服力的叙事）
 *
 * @param {string} applicationType
 * @param {string} [modelType='hunyuan']
 * @returns {string}
 */
function buildSystemPrompt(applicationType, modelType = 'hunyuan') {
  // 公共部分
  const common = [
    '你是一名经验丰富的公益项目申报书撰写专家，熟悉中国各类资助平台的申报要求。',
    '这是一份提交给资助基金会或政府部门的正式项目申报书。',
    '',
    '【重要】请直接根据用户提供的数据生成申报书正文内容（封面+各章节完整文本），不要输出模板说明、字段定义或格式指引。',
    '',
    '请使用正式公文体（本机构），章节标题用中文数字（一、二、三...）。',
    getIntegrityConstraint(),
    '受益人群体描述使用行政化表达（如"特困家庭儿童"），避免描述敏感病情或个体信息。',
    '无法确认的字段请输出 [请填写实际数据] 占位符。',
  ].join('\n');

  // 模型专项追加（Spec 第434-492行）
  const modelSpecific = {
    hunyuan: [
      '请注重申报书的逻辑性，确保"问题-目标-活动-成效"的因果链清晰。',
      '请对用户提供的需求描述进行结构化整理，不要添加用户未提供的数据。',
      '请直接输出完整的申报书正文，包含封面信息和各章节内容，不要输出模板格式说明。',
    ].join('\n'),

    deepseek: [
      '预算表格中的每一个数字必须来自 <budget_data> 标签内的用户数据，不得自行计算或推断。',
      '绩效指标必须严格对应 <indicators> 标签内的内容，不得新增指标。',
      '明确禁止：不要添加任何非用户提供的统计数据，不要虚构数字，不要生成预算金额。',
      '仅输出申报书正文章节，不要添加任何解释或注释。',
    ].join('\n'),

    doubao: [
      '腾讯公益项目简介章节：请用温暖、有感染力但不煽情的语气撰写，字数控制在150字以内。',
      '受益群体描述：请基于用户提供的群体特征描述，不要编造具体个案。',
      '明确风格边界：不要使用过度励志或营销化表达，保持公益机构的真诚性。',
      '请用Markdown格式输出。',
    ].join('\n'),

    // GLM 等同 deepseek 策略，另注重说服力
    glm: [
      '请注意内容的说服力，确保每个活动设计都有对应的需求依据。',
      '预算表格中的每一个数字必须来自用户提供的数据，不得自行计算或推断。',
      '绩效指标必须严格对应用户填写的内容，不得新增指标。',
      '明确禁止：不要添加任何非用户提供的统计数据，不要虚构数字，不要生成预算金额。',
      '仅输出申报书正文章节，不要添加任何解释或注释。',
    ].join('\n'),
  };

  const extra = modelSpecific[modelType] || modelSpecific['deepseek'];

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
 *   formatCurrency(300000)   → "300,000元"
 *   formatCurrency(287600.5) → "287,600.50元"
 *   formatCurrency(0)        → "0元"
 *   formatCurrency(NaN)      → "[请填写实际金额]"
 *   formatCurrency(Infinity) → "[请填写实际金额]"
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

// 申报助手货币字段：Spec 中明确的金额字段
const CURRENCY_FIELDS = new Set([
  'total_budget',
  'matching_fund_amount',
  'tencent_fundraising_goal',
  'price_quote',
]);

// -----------------------------------------------------------------------
// 4. buildUserPrompt
// -----------------------------------------------------------------------

/**
 * 将用户输入数据格式化为 user prompt。
 *
 * 安全约束（F-08）：
 *   piiFields 中列出的字段（contact_name, contact_phone）必须从 input
 *   中排除，绝不出现在 prompt 文本中。
 *   _regenerate_section 等内部字段同样排除。
 *
 * 货币字段格式化（Spec 输入定义）：
 *   total_budget, budget_breakdown[].amount, tencent_fundraising_goal,
 *   matching_fund_amount, price_quote 使用 formatCurrency() 格式化。
 *
 * 格式差异：
 *   - deepseek/glm：使用 XML 标签 <data>...</data><instruction>...</instruction>
 *   - 其他模型：普通 JSON + 指令文本
 *
 * @param {object} input 用户输入数据
 * @param {string} templateContent 模板正文（已去除 frontmatter）
 * @param {string[]} piiFields 需要排除的 PII 字段名列表
 * @param {string} [modelType='hunyuan']
 * @returns {string}
 */
function buildUserPrompt(input, templateContent, piiFields, modelType = 'hunyuan') {
  // 构建排除集合（防御性处理：始终排除 contact_name / contact_phone）
  const INTERNAL_FIELDS = ['_regenerate_section'];
  const excludeSet = new Set([
    ...INTERNAL_FIELDS,
    ...(Array.isArray(piiFields) ? piiFields : []),
    'contact_name',
    'contact_phone',
  ]);

  // 从 input 中剔除 PII 字段，格式化货币字段
  const safeData = {};
  for (const [key, value] of Object.entries(input)) {
    if (excludeSet.has(key)) continue;

    if (CURRENCY_FIELDS.has(key) && typeof value === 'number') {
      // 顶级货币字段格式化
      safeData[key] = formatCurrency(value);
    } else if (key === 'budget_breakdown' && Array.isArray(value)) {
      // budget_breakdown[].amount 格式化（保留用户输入原始值，格式化显示）
      safeData[key] = value.map((item) => {
        if (!item || typeof item !== 'object') return item;
        const formatted = Object.assign({}, item);
        if (typeof formatted.amount === 'number') {
          formatted.amount = formatCurrency(formatted.amount);
        }
        return formatted;
      });
    } else {
      safeData[key] = value;
    }
  }

  const dataJson = JSON.stringify(safeData, null, 2);

  // 提取模板章节结构作为输出格式指引（取前 60 行避免 token 过长）
  const templateLines = templateContent.split('\n');
  const templateStructure = templateLines.slice(0, 60).join('\n');

  if (modelType === 'deepseek' || modelType === 'glm') {
    // DeepSeek / GLM：XML 标签分隔数据与指令（提升准确率，Spec 第458-464行）
    return [
      '<data>',
      dataJson,
      '</data>',
      '<instruction>',
      '请根据上述数据和以下模板要求生成完整申报书：',
      '',
      templateStructure,
      '</instruction>',
    ].join('\n');
  }

  // 混元 / 豆包及其他模型：普通 JSON + 指令格式
  return [
    '以下是申报书所需的数据（JSON格式）：',
    '',
    '```json',
    dataJson,
    '```',
    '',
    '请根据上述数据，按照以下模板章节结构生成完整申报书：',
    '',
    templateStructure,
  ].join('\n');
}

// -----------------------------------------------------------------------
// 5. enforcePlaceholders（placeholder-enforcer 核心函数）
// -----------------------------------------------------------------------

/**
 * 扫描模型输出文本，检测并替换疑似 AI 编造的内容。
 *
 * 检测模式（Spec Step 6 / 合规红线第8条）：
 *   - 8位以上连续数字 → 疑似证书编号/文件编号
 *   - 字母+4位以上数字 → 疑似编号格式
 *   - 银行账号格式（XXXX-XXXX-XXXX）
 *
 * 白名单豁免（F-14）：
 *   - input.budget_breakdown 中用户填写的金额不替换
 *   - input.total_budget / tencent_fundraising_goal / matching_fund_amount / price_quote 不替换
 *   - input.target_count（受益人数）不替换
 *
 * @param {string} text 模型输出文本
 * @param {object} [input={}] 用户输入数据（用于提取白名单金额，防止误替换）
 * @returns {{ text: string, replacements: Array<{original: string, replacement: string, position: number}>, count: number }}
 */
function enforcePlaceholders(text, input = {}) {
  if (typeof text !== 'string') {
    return { text: '', replacements: [], count: 0 };
  }

  // 构建白名单数字集合（用户填写的金额不替换）
  const whitelistNumbers = buildAmountWhitelist(input);

  const replacements = [];
  let result = text;
  // 累计偏移量（替换后字符串长度变化导致 position 需要修正）
  let offset = 0;

  // 检测规则列表：按优先级排序，先检测更具体的模式
  const PATTERNS = [
    {
      // 银行账号格式：XXXX-XXXX-XXXX 或连续16-19位数字
      regex: /\b\d{4}-\d{4}-\d{4}(?:-\d{4})?\b/g,
      getReplacement: () => '[请填写银行账号]',
    },
    {
      // 字母+4位以上数字（疑似证书编号/机构编号）
      regex: /\b[A-Z]{1,4}\d{4,}\b/g,
      getReplacement: (match) => `[请填写${match.slice(0, 2)}编号]`,
    },
    {
      // 8位以上连续纯数字（疑似证书编号/文件编号，排除年份4位/月日组合）
      // 排除已在白名单的数字
      regex: /\b\d{8,}\b/g,
      getReplacement: () => '[请填写编号]',
    },
  ];

  for (const { regex, getReplacement } of PATTERNS) {
    regex.lastIndex = 0; // 重置全局正则状态

    // 在当前 result 上扫描（每轮 regex 都在最新 result 上运行）
    const matches = [];
    let m;
    while ((m = regex.exec(result)) !== null) {
      matches.push({ original: m[0], index: m.index });
    }

    for (const { original, index } of matches) {
      // 检查是否在白名单内（用户填写的数字不替换）
      if (whitelistNumbers.has(original)) continue;

      const replacement = getReplacement(original);
      const position = index + offset;

      // 替换第一个出现（避免二次替换已替换的占位符）
      const before = result.slice(0, index);
      const after = result.slice(index + original.length);
      result = before + replacement + after;

      offset += replacement.length - original.length;

      replacements.push({ original, replacement, position });

      // 重置 offset 后再处理下一个 match 时，result 已变化，需重新索引
      // 此处利用 matches 预先记录的 index（基于替换前的 result），
      // 后续 matches 的 index 需要依次修正
      offset = result.length - text.length + replacements.reduce((acc) => acc, 0);
    }

    // 重新计算 offset 基于最终 result 与原始 text 的长度差
    offset = result.length - text.length;
  }

  return {
    text: result,
    replacements,
    count: replacements.length,
  };
}

/**
 * 从用户输入数据中提取应豁免替换的数字白名单（字符串形式）
 * @param {object} input
 * @returns {Set<string>}
 */
function buildAmountWhitelist(input) {
  const whitelist = new Set();

  if (!input || typeof input !== 'object') return whitelist;

  // 顶级货币字段
  const TOP_CURRENCY_FIELDS = [
    'total_budget', 'matching_fund_amount',
    'tencent_fundraising_goal', 'price_quote',
  ];
  for (const field of TOP_CURRENCY_FIELDS) {
    if (typeof input[field] === 'number' && isFinite(input[field])) {
      // 加入整数字符串形式（用户填写的原始值）
      whitelist.add(String(Math.round(input[field])));
    }
  }

  // budget_breakdown[].amount
  if (Array.isArray(input.budget_breakdown)) {
    for (const item of input.budget_breakdown) {
      if (item && typeof item.amount === 'number' && isFinite(item.amount)) {
        whitelist.add(String(Math.round(item.amount)));
      }
    }
  }

  // target_count（受益人数）
  if (typeof input.target_count === 'number' && isFinite(input.target_count)) {
    whitelist.add(String(Math.round(input.target_count)));
  }

  return whitelist;
}

// -----------------------------------------------------------------------
// 6. buildPrompt（主入口）
// -----------------------------------------------------------------------

/**
 * 组装完整 prompt messages 数组（OpenAI-compatible messages 格式）。
 *
 * 流程：loadTemplate → buildSystemPrompt → buildUserPrompt → 返回 messages
 *
 * @param {object} input 用户输入数据（已通过 validators.js 校验）
 * @param {string} [modelType='hunyuan'] 目标模型
 * @returns {Array<{ role: string, content: string }>}
 */
function buildPrompt(input, modelType = 'hunyuan') {
  const template = loadTemplate(input.application_type);
  const systemPrompt = buildSystemPrompt(input.application_type, modelType);

  // PII 字段固定排除（不依赖外部 validators，保持模块独立性）
  const piiFields = ['contact_name', 'contact_phone'];
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
  enforcePlaceholders,
};
