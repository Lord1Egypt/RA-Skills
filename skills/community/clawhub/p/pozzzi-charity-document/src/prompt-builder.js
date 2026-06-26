'use strict';

// -----------------------------------------------------------------------
// prompt-builder.js — 文书助手 Prompt 构建器
//
// 依赖：仅 Node.js 内置模块（fs, path）
// 合规依据：噗滋慈善文书助手 Spec v1.0 + PIPL 第23/28条
//          + 慈善法第75/77条 + 生成式AI暂行办法第4/8条
// PII 安全：contact_name / contact_phone 绝不写入 prompt
// fixed-clause-handler：提取 [FIXED]...[/FIXED] 标记的固定法律条款
//   - 固定条款不经过模型，直接注入输出
// -----------------------------------------------------------------------

const fs = require('fs');
const path = require('path');

// -----------------------------------------------------------------------
// 文书类型 + 子类型 → 模板文件名映射
// -----------------------------------------------------------------------

/**
 * 根据文书大类和子类型确定模板文件名
 *
 * 映射规则：
 *   contract + volunteer         → contract-volunteer-v1.md
 *   contract + cooperation       → contract-cooperation-v1.md
 *   contract + rental / service  → contract-cooperation-v1.md（通用合作协议）
 *   meeting_minutes              → meeting-minutes-v1.md（不区分子类型）
 *   official_letter              → official-letter-v1.md
 *   thank_you_letter             → thank-you-letter-v1.md
 *   work_plan                    → work-plan-v1.md
 *
 * @param {string} documentType    文书大类
 * @param {string} [documentSubtype=''] 文书子类型
 * @returns {string} 模板文件名
 */
/**
 * 标准化 documentType（兼容 validators 枚举和 prompt-builder 枚举）
 */
function normalizeDocumentType(type, subtype) {
  if (type === 'minutes') return 'meeting_minutes';
  if (type === 'plan_summary') return 'work_plan';
  if (type === 'letter') {
    // letter 分流：thanks_letter_* → thank_you_letter，其他 → official_letter
    if (subtype && subtype.startsWith('thanks_letter')) return 'thank_you_letter';
    return 'official_letter';
  }
  return type;
}

function resolveTemplateFilename(documentType, documentSubtype) {
  const subtype = (documentSubtype || '').toLowerCase();

  if (documentType === 'contract') {
    if (subtype === 'volunteer' || subtype === 'volunteer_agreement') {
      return 'contract-volunteer-v1.md';
    }
    if (subtype === 'cooperation' || subtype === 'cooperation_agreement' ||
        subtype === 'rental' || subtype === 'rental_agreement' ||
        subtype === 'service') {
      return 'contract-cooperation-v1.md';
    }
    throw new Error(`未知合同子类型：${documentSubtype}`);
  }

  // 兼容 validators 枚举（minutes/letter/plan_summary）和长格式枚举
  const SIMPLE_MAP = {
    meeting_minutes: 'meeting-minutes-v1.md',
    minutes: 'meeting-minutes-v1.md',
    official_letter: 'official-letter-v1.md',
    letter: 'official-letter-v1.md',
    thank_you_letter: 'thank-you-letter-v1.md',
    work_plan: 'work-plan-v1.md',
    plan_summary: 'work-plan-v1.md',
  };

  if (Object.prototype.hasOwnProperty.call(SIMPLE_MAP, documentType)) {
    return SIMPLE_MAP[documentType];
  }

  throw new Error(`未知文书类型：${documentType}`);
}

// -----------------------------------------------------------------------
// YAML frontmatter 解析（仅用正则，不引入 yaml 库）
// -----------------------------------------------------------------------

/**
 * 解析 Markdown 文件中的 YAML frontmatter（--- 包裹的块）
 * 支持 "key: value" 格式，value 为字符串或简单布尔/数字
 *
 * 白名单字段（防供应链 prompt injection）：
 *   source_url / verified_date / version / document_type / document_subtype
 *
 * @param {string} raw 原始文件内容
 * @returns {{ metadata: Object, content: string }}
 */
function parseFrontmatter(raw) {
  const frontmatterPattern = /^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/;
  const match = raw.match(frontmatterPattern);

  if (!match) {
    return { metadata: {}, content: raw };
  }

  const yamlBlock = match[1];
  const content = match[2];
  const rawMetadata = {};

  // 允许的 frontmatter 字段白名单（防供应链注入）
  const ALLOWED_METADATA_KEYS = new Set([
    'source_url', 'verified_date', 'version',
    'document_type', 'document_subtype',
  ]);

  for (const line of yamlBlock.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;

    const colonSpaceIdx = trimmed.indexOf(': ');
    const colonIdx = colonSpaceIdx !== -1 ? colonSpaceIdx : trimmed.indexOf(':');
    if (colonIdx === -1) continue;

    const key = trimmed.slice(0, colonIdx).trim();
    const rawVal = trimmed.slice(colonIdx + (colonSpaceIdx !== -1 ? 2 : 1)).trim();

    if (rawVal === 'true') {
      rawMetadata[key] = true;
    } else if (rawVal === 'false') {
      rawMetadata[key] = false;
    } else if (rawVal !== '' && !isNaN(Number(rawVal))) {
      rawMetadata[key] = Number(rawVal);
    } else {
      rawMetadata[key] = rawVal.replace(/^['"]|['"]$/g, '');
    }
  }

  // 白名单过滤：只保留已知安全字段
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
 * @param {string} documentType    文书大类
 * @param {string} [documentSubtype=''] 文书子类型
 * @returns {{ metadata: Object, content: string }}
 */
function loadTemplate(documentType, documentSubtype) {
  const normalizedType = normalizeDocumentType(documentType, documentSubtype || '');
  const filename = resolveTemplateFilename(normalizedType, documentSubtype || '');
  const filePath = path.join(__dirname, '..', 'templates', filename);

  let raw;
  try {
    raw = fs.readFileSync(filePath, 'utf8');
  } catch {
    throw new Error(`模板加载失败：${filename}（文书类型：${documentType}/${documentSubtype}）`);
  }

  return parseFrontmatter(raw);
}

// -----------------------------------------------------------------------
// 2. extractFixedClauses — fixed-clause-handler 核心（文书助手独有）
// -----------------------------------------------------------------------

/**
 * 从模板内容中提取所有 [FIXED]...[/FIXED] 标记的固定法律条款。
 *
 * 这些条款（保密条款、不可抗力条款、协议生效条款等）不经过模型，
 * 由 injectFixedClauses() 直接插入最终输出。
 *
 * @param {string} templateContent 模板正文（已去除 frontmatter）
 * @returns {{ clauses: string[], templateWithoutFixed: string }}
 *   clauses             - 提取的固定条款内容列表（不含 [FIXED] 标记本身）
 *   templateWithoutFixed - 去掉 [FIXED] 标记后的模板内容（保留条款文本，去掉标记行）
 */
function extractFixedClauses(templateContent) {
  if (typeof templateContent !== 'string') {
    return { clauses: [], templateWithoutFixed: '' };
  }

  // ReDoS 防护：模板大小上限
  const MAX_TEMPLATE_SIZE = 50000;
  if (templateContent.length > MAX_TEMPLATE_SIZE) {
    throw new Error(`模板文件超过最大允许大小（${MAX_TEMPLATE_SIZE} 字节）`);
  }

  const clauses = [];
  const fixedPattern = /\[FIXED\]([\s\S]*?)\[\/FIXED\]/g;

  let match;
  while ((match = fixedPattern.exec(templateContent)) !== null) {
    const clauseText = match[1].trim();
    if (clauseText && clauseText.length <= 5000) {
      clauses.push(clauseText);
    }
  }

  // 去掉 [FIXED]...[/FIXED] 整个块（包括内容），防止固定条款被模型看到
  const templateWithoutFixed = templateContent
    .replace(/\[FIXED\][\s\S]*?\[\/FIXED\]\r?\n?/g, '[此处为固定法律条款，已由系统处理]\n');

  return { clauses, templateWithoutFixed };
}

// -----------------------------------------------------------------------
// 3. injectFixedClauses — 将固定条款注入模型输出
// -----------------------------------------------------------------------

/**
 * 将 extractFixedClauses 提取的固定条款注入到模型输出的对应位置。
 *
 * 注入策略：在模型输出正文末尾（disclaimer 之前）追加固定条款内容。
 * 固定条款以明确的分隔线和说明注入，确保不被遗漏。
 *
 * @param {string} modelOutput 模型生成的文书正文
 * @param {string[]} clauses   由 extractFixedClauses 提取的固定条款列表
 * @returns {string} 注入固定条款后的完整文本
 */
function injectFixedClauses(modelOutput, clauses) {
  if (!modelOutput || typeof modelOutput !== 'string') {
    return modelOutput || '';
  }

  if (!Array.isArray(clauses) || clauses.length === 0) {
    return modelOutput;
  }

  const fixedSection = clauses
    .map((clause) => clause.trim())
    .filter(Boolean)
    .join('\n\n---\n\n');

  // 在正文末尾追加固定条款（disclaimer 之前插入）
  return `${modelOutput.trimEnd()}\n\n${fixedSection}`;
}

// -----------------------------------------------------------------------
// 4. getTemperature
// -----------------------------------------------------------------------

/**
 * 根据文书类型和子类型返回推荐的 temperature 参数。
 *
 * 规则（来自 Spec 国产模型适配章节）：
 *   contract                     → 0.2（合同需要高一致性）
 *   official_letter              → 0.3（公函格式严格）
 *   meeting_minutes              → 0.3（纪要需准确传达要点）
 *   work_plan                    → 0.4（计划/总结半结构化）
 *   thank_you_letter + donor     → 0.6（捐赠人感谢信需情感温度）
 *   thank_you_letter + volunteer → 0.5（志愿者感谢信适度灵活）
 *   默认                         → 0.4
 *
 * @param {string} documentType
 * @param {string} [documentSubtype='']
 * @returns {number}
 */
function getTemperature(documentType, documentSubtype) {
  const subtype = (documentSubtype || '').toLowerCase();
  const dt = normalizeDocumentType(documentType, subtype);

  if (dt === 'contract') {
    return 0.2;
  }

  if (dt === 'official_letter') {
    return 0.3;
  }

  if (dt === 'meeting_minutes') {
    return 0.3;
  }

  if (dt === 'work_plan') {
    return 0.4;
  }

  if (dt === 'thank_you_letter') {
    if (subtype.includes('donor')) {
      return 0.6;
    }
    if (subtype.includes('volunteer')) {
      return 0.5;
    }
    // funder 或其他感谢信子类型
    return 0.5;
  }

  return 0.4;
}

// -----------------------------------------------------------------------
// 5. buildSystemPrompt
// -----------------------------------------------------------------------

/**
 * 生成内容真实性约束文本（Spec 国产模型适配章节，所有模型通用）
 * @returns {string}
 */
function getIntegrityConstraint() {
  return [
    '【内容真实性约束】',
    '你正在帮助一家中国公益组织撰写行政文书。以下规则不可违反：',
    '1. 禁止生成任何金额数字。协议中的报酬、补贴、违约金等金额只能来自用户输入，',
    '   用户未填写时输出：[请填写金额]',
    '2. 禁止生成任何编号（证书编号/协议编号/文号等），一律输出：[请填写XXX编号]',
    '3. 禁止生成任何统计数据（如"本地区有XX名志愿者"），这类数据只能来自用户输入',
    '4. 会议决议（resolution 字段内容）必须原文保留，不做任何语言润色或修改',
    '5. 若某段落对应的用户输入内容不足，直接输出占位符提示，不要自行发挥填充',
  ].join('\n');
}

/**
 * 根据文书类型、子类型和模型类型生成 system prompt。
 *
 * 公共部分（所有模型）：
 *   - 角色定义（公益行政文书专家）
 *   - 格式指令（直接生成正文，不输出模板说明）
 *   - 内容真实性约束
 *
 * 按 documentType 追加特定指令：
 *   - contract    → 法律用语、条款逻辑性、不编造金额
 *   - meeting_minutes → 客观记录体、决议原文保留
 *   - official_letter → 政府公文体、GB/T 9704-2012
 *   - thank_you_letter → 按 subtype 决定语气（donor: 温暖/volunteer: 适度灵活）
 *   - work_plan   → 内部工作文体、数字来源于用户输入
 *
 * 模型差异追加（同申报助手/报告助手策略）：
 *   - hunyuan：注重逻辑性和条款完整性
 *   - deepseek：XML 标签，严格禁止虚构，仅输出正文
 *   - doubao：温暖语气（感谢信），格式化输出
 *   - glm：说服力与逻辑兼顾
 *
 * @param {string} documentType
 * @param {string} [documentSubtype='']
 * @param {string} [modelType='hunyuan']
 * @returns {string}
 */
function buildSystemPrompt(documentType, documentSubtype, modelType) {
  const subtype = (documentSubtype || '').toLowerCase();
  const dt = normalizeDocumentType(documentType, subtype);
  const model = modelType || 'hunyuan';

  // 公共基础
  const baseLines = [
    '你是一名经验丰富的公益组织行政文书撰写专家。',
    '【重要】请直接生成文书正文内容，不要输出模板说明或格式指引。',
    '',
    getIntegrityConstraint(),
    '无法确认的字段请输出 [请填写实际数据] 占位符。',
    '本文书仅供公益机构内部使用或对外官方沟通，请严格按照中国行政文书规范撰写。',
  ];

  // 按文书类型追加特定指令
  const typeSpecificLines = [];

  if (dt === 'contract') {
    typeSpecificLines.push(
      '【合同/协议类指令】',
      '请使用正式法律用语，条款表述严谨，每个权利对应义务须明确。',
      '协议中的金额（报酬、补贴、违约金等）一律来自用户输入，禁止 AI 生成任何金额数字。',
      '编号、证件号、账号等一律输出占位符，格式：[请填写XXX]。',
      '固定法律条款（保密、不可抗力、协议生效等）已由系统处理，请勿重复生成这些条款。',
    );
  } else if (dt === 'meeting_minutes') {
    typeSpecificLines.push(
      '【会议纪要类指令】',
      '请使用客观记录体，不做主观评价，准确传达各议程的讨论要点。',
      '会议决议内容必须原文保留，不做任何语言润色或修改。',
      '理事会/监事会纪要需在基本信息中注明出席人数和法定人数满足情况。',
    );
  } else if (dt === 'official_letter') {
    typeSpecificLines.push(
      '【政府公函类指令】',
      '请严格使用政府公文语体（参照 GB/T 9704-2012），避免口语化表达。',
      '标题格式为"关于[事项]的函"，收件方使用职务称谓，不得出现个人真实姓名。',
      '落款格式：机构名称 + 日期，不含个人签名信息。',
    );
  } else if (dt === 'thank_you_letter') {
    if (subtype.includes('donor')) {
      typeSpecificLines.push(
        '【捐赠人感谢信类指令】',
        '请用温暖、真诚的语气撰写，表达对捐赠人支持的感谢，字数控制在500字以内。',
        '不要使用过于商业化或套话式的表达，保持公益机构的真诚风格。',
        '感谢信中的项目成效描述必须严格来自用户提供的信息，不要编造具体数字。',
        '捐赠金额原文引用用户输入值，不修改、不补充。',
      );
    } else if (subtype.includes('volunteer')) {
      typeSpecificLines.push(
        '【志愿者感谢信类指令】',
        '请用温暖、正式兼顾的语气撰写，对志愿者贡献表达真诚感谢。',
        '字数控制在400字以内，语气应适度灵活，不过度煽情。',
        '不编造志愿服务的具体数字，数据严格来自用户输入。',
      );
    } else {
      // funder / 通用感谢信
      typeSpecificLines.push(
        '【资助方/合作伙伴感谢信类指令】',
        '请在正式框架内适度表达感谢和合作期望，既保持机构专业性，又体现对关系的重视。',
        '字数控制在500字以内，语气为正式中带温暖（mixed）。',
        '不编造项目成效数字，数据严格来自用户输入。',
      );
    }
  } else if (dt === 'work_plan') {
    typeSpecificLines.push(
      '【工作计划/总结类指令】',
      '请使用内部工作文体，结构清晰，按照用户提供的工作事项逐领域呈现。',
      '工作总结中成果数字严格来自用户填写的 work_items[].target，AI 不补充或修改数字。',
      '工作计划/总结长度目标：500-1,500字（月度计划：500字左右；年度总结：不超过1,500字）。',
    );
  }

  const common = [...baseLines, ...(typeSpecificLines.length > 0 ? ['', ...typeSpecificLines] : [])].join('\n');

  // 模型专项追加
  const modelSpecific = {
    hunyuan: [
      '请注重文书的逻辑性，确保各章节内容条理清晰、前后一贯。',
      '请对用户提供的信息进行结构化整理，不要添加用户未提供的数据。',
      '请直接输出完整的文书正文，不要输出模板格式说明。',
    ].join('\n'),

    deepseek: [
      '使用 XML 标签分隔数据和指令（提升准确率），文书正文内容在 <instruction> 标签指定的结构中生成。',
      '明确禁止：不要添加任何非用户提供的数字，不要虚构编号，不要生成金额数字。',
      '仅输出文书正文章节，不要添加任何解释或元注释。',
      '固定法律条款已由系统独立处理，不要在输出中重复生成这些条款。',
    ].join('\n'),

    doubao: [
      '请用温暖、有感染力但不煽情的语气撰写感谢信段落。',
      '明确风格边界：不要使用过度励志或营销化表达，保持公益机构的真诚性。',
      '请用Markdown格式输出。',
    ].join('\n'),

    glm: [
      '请注意内容的说服力和情感表达，确保文书既有逻辑严谨性又有人文温度。',
      '所有数字必须来自用户提供的数据，不得自行计算或推断。',
      '明确禁止：不要添加任何非用户提供的统计数据，不要虚构数字，不要生成金额数字。',
      '仅输出文书正文章节，不要添加任何解释或注释。',
    ].join('\n'),
  };

  const extra = modelSpecific[model] || modelSpecific['deepseek'];

  return extra ? `${common}\n${extra}` : common;
}

// -----------------------------------------------------------------------
// 6. formatCurrency
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
// 文书助手货币字段集合
// -----------------------------------------------------------------------

// 文书助手中涉及金额的顶级字段
const CURRENCY_FIELDS = new Set([
  'compensation_amount',
  'funding_amount',
  'penalty_amount',
]);

// -----------------------------------------------------------------------
// 7. buildUserPrompt
// -----------------------------------------------------------------------

/**
 * 将用户输入数据格式化为 user prompt。
 *
 * 安全约束（Spec F-07）：
 *   piiFields 中列出的字段（contact_name, contact_phone）必须从 input
 *   中排除，绝不出现在 prompt 文本中。
 *   _regenerate_section 等内部字段同样排除。
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
function buildUserPrompt(input, templateContent, piiFields, modelType) {
  const model = modelType || 'hunyuan';

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
      safeData[key] = formatCurrency(value);
    } else {
      safeData[key] = value;
    }
  }

  const dataJson = JSON.stringify(safeData, null, 2);

  // 提取模板章节结构作为输出格式指引（取前 60 行避免 token 过长）
  const templateLines = templateContent.split('\n');
  const templateStructure = templateLines.slice(0, 60).join('\n');

  if (model === 'deepseek' || model === 'glm') {
    // DeepSeek / GLM：XML 标签分隔数据与指令（提升准确率）
    return [
      '<data>',
      dataJson,
      '</data>',
      '<instruction>',
      '请根据上述数据和以下模板要求生成完整文书正文（固定法律条款已由系统处理，不要重复生成）：',
      '',
      templateStructure,
      '</instruction>',
    ].join('\n');
  }

  // 混元 / 豆包及其他模型：普通 JSON + 指令格式
  return [
    '以下是文书所需的数据（JSON格式）：',
    '',
    '```json',
    dataJson,
    '```',
    '',
    '请根据上述数据，按照以下模板章节结构生成完整文书正文（固定法律条款已由系统处理，不要重复生成）：',
    '',
    templateStructure,
  ].join('\n');
}

// -----------------------------------------------------------------------
// 8. buildPrompt（主入口）
// -----------------------------------------------------------------------

/**
 * 组装完整 prompt messages 数组（OpenAI-compatible messages 格式）。
 *
 * 流程：
 *   1. loadTemplate → 加载模板，解析 frontmatter
 *   2. extractFixedClauses → 提取固定条款，得到去掉标记后的模板内容
 *   3. buildSystemPrompt → 构建系统 prompt
 *   4. buildUserPrompt → 构建用户 prompt（使用去掉标记后的模板内容）
 *   5. 将 fixedClauses 附在 messages 中供调用方使用
 *
 * 返回值包含 fixedClauses 字段，供 index.js 在后处理阶段调用 injectFixedClauses()。
 *
 * @param {object} input 用户输入数据（已通过 validators.js 校验）
 * @param {string} [modelType='hunyuan'] 目标模型
 * @returns {{ messages: Array<{ role: string, content: string }>, fixedClauses: string[] }}
 */
function buildPrompt(input, modelType, externalPiiFields) {
  const model = modelType || 'hunyuan';
  const documentSubtype = input.document_subtype || '';
  const documentType = normalizeDocumentType(input.document_type, documentSubtype);

  const template = loadTemplate(documentType, documentSubtype);

  const { clauses: fixedClauses, templateWithoutFixed } = extractFixedClauses(template.content);

  const systemPrompt = buildSystemPrompt(documentType, documentSubtype, model);

  // 合并内置防御性 PII 字段和外部动态 PII 字段
  const piiFields = [
    ...['contact_name', 'contact_phone'],
    ...(Array.isArray(externalPiiFields) ? externalPiiFields : []),
  ];
  const userPrompt = buildUserPrompt(input, templateWithoutFixed, piiFields, model);

  return {
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userPrompt },
    ],
    fixedClauses,
  };
}

// -----------------------------------------------------------------------
// 导出
// -----------------------------------------------------------------------

module.exports = {
  buildPrompt,
  buildSystemPrompt,
  buildUserPrompt,
  loadTemplate,
  extractFixedClauses,
  injectFixedClauses,
  getTemperature,
  formatCurrency,
};
