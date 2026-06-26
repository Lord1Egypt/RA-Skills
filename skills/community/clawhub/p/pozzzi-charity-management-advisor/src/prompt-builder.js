'use strict';

// -----------------------------------------------------------------------
// prompt-builder.js — 管理顾问 Skill Prompt 构建器
//
// 依赖：仅 Node.js 内置模块（fs, path）+ 本 Skill 内部模块（knowledge-base）
// 合规依据：噗滋慈善管理顾问 Spec v1.0
//           PIPL 第23/28条 + 生成式AI暂行办法第4/8/17条 + 慈善法第75/77条
//
// 核心特征（与其他 Skill 的差异）：
//   - 这是问答型 Skill：输入是用户自然语言问题，输出是咨询回答
//   - 知识库驱动：按问题类别加载对应知识库段落嵌入 system prompt
//   - temperature 0.4：准确为主，允许有表达灵活性（Spec 明确规定）
//   - 强制免责：每条回答必须标注"非法律意见"（Spec 第9节）
//   - 禁止编造：system prompt 明确禁止编造条文编号/政府文件编号
//
// PII 安全：
//   - contact_name 仅写入本地日志，绝不写入 prompt
//   - question / question_context 经 pii-filter 过滤后传入（由 index.js 负责）
//
// temperature 0.4：由调用方（index.js）设置，本文件不控制
// -----------------------------------------------------------------------

const knowledgeBase = require('./knowledge-base');

// -----------------------------------------------------------------------
// 内置 PII 排除字段（硬编码，不可缩减）
// -----------------------------------------------------------------------

/** 永远不进入 prompt 的顶级 PII 字段 */
const BUILTIN_PII_FIELDS = ['contact_name'];

// -----------------------------------------------------------------------
// 1. 强制合规约束（system prompt 中必须包含的规则）
// -----------------------------------------------------------------------

/**
 * 生成管理顾问强制合规约束文本（所有模型通用，不可删减）。
 *
 * 来源：Spec 第 8 节（绝对禁止）+ 第 9 节（合规要求）
 *
 * @returns {string}
 */
function getAdvisorConstraints() {
  return [
    '【管理顾问强制合规约束——不可违反】',
    '',
    '1. 禁止出具法律意见',
    '   → 不得给出"您应该/必须/合法/违法"等结论性法律判断',
    '   → 涉及法律问题时，明确说明这是参考信息，建议咨询专业律师',
    '',
    '2. 禁止编造法规条文编号',
    '   → 引用条文时只使用知识库中已记录的条款编号',
    '   → 不确定具体条款编号时，必须说明"建议核查具体条文"，不得给出推测编号',
    '   → 格式示例：（《慈善法》第72条）——仅在确认该条文时使用',
    '',
    '3. 禁止编造政府文件编号',
    '   → 只在知识库有记录的情况下引用文件编号（如"民发[20XX]X号"）',
    '   → 未记录时描述文件性质（如"民政部关于……的通知"），不给出具体编号',
    '',
    '4. 禁止处理诉讼/纠纷问题',
    '   → 涉及纠纷、行政处罚、诉讼、仲裁的问题，必须建议咨询律师，不做任何实质性处理指引',
    '',
    '5. 超出知识库范围时必须诚实声明',
    '   → 禁止以看似合理的方式编造回答',
    '   → 超出覆盖范围时，说明"超出当前知识库覆盖范围"并引导咨询权威渠道',
    '',
    '6. 地方差异必须提示',
    '   → 涉及各地民政局要求差异的内容，明确提示"以您所在地民政局通知为准"',
    '',
    '7. 每条回答末尾必须包含标准免责声明',
    '   → 声明不可省略，不可简化',
  ].join('\n');
}

// -----------------------------------------------------------------------
// 2. 输出格式要求
// -----------------------------------------------------------------------

/**
 * 生成输出格式说明（四段式结构，Spec 第5节）。
 *
 * @param {string} urgency - 'high' | 'medium' | 'low' | undefined
 * @returns {string}
 */
function getOutputFormatInstructions(urgency) {
  const urgencyGuide = {
    high:   '【紧急模式（urgency=high）】回答控制在150-300字，直接给出结论和最关键的行动建议，去掉背景解释。',
    medium: '【标准模式（urgency=medium）】回答控制在300-500字，包含背景+结论+建议行动。',
    low:    '【详尽模式（urgency=low）】回答控制在400-600字，包含背景解释+条文引用+多种情形说明+建议行动。',
  };

  const lengthGuide = urgencyGuide[urgency] || urgencyGuide['medium'];

  return [
    '【输出格式要求——严格遵守以下四段式结构】',
    '',
    '【问题理解】',
    '一句话重述用户问题，确认理解正确。',
    '',
    '【参考回答】',
    '核心回答内容。',
    '- 涉及具体数字/比例/期限时，必须标注依据法规/文件名称和条文编号（不确定时标注"建议核查具体条文"）',
    '- 涉及地方差异时，明确提示"以下以通用规则为参考，您所在地区可能有差异"',
    '- 知识库覆盖不足时，标注"[超出当前知识库覆盖范围，建议向主管民政部门或专业律师咨询]"，禁止编造',
    '',
    '【建议行动】',
    '具体可执行的下一步建议，2-4条，编号列出。',
    '如问题属于其他工具更适合处理的范围，提示"您可以使用噗滋 XX 助手完成这一步"。',
    '',
    '【重要提示】',
    'AI 生成，仅供参考，请核实数据。此回答为公益管理领域的参考信息，不构成法律意见。涉及具体法律问题、纠纷处理或行政处罚，建议咨询专业律师；涉及税务操作，建议咨询注册税务师或当地税务机关。法规条文建议核查最新有效版本。',
    '',
    lengthGuide,
  ].join('\n');
}

// -----------------------------------------------------------------------
// 3. buildSystemPrompt
// -----------------------------------------------------------------------

/**
 * 根据问题类别、urgency 和模型类型生成 system prompt。
 *
 * 结构（按顺序）：
 *   1. 角色定义（NGO 管理顾问）
 *   2. 强制合规约束（禁止编造/禁止法律意见/超出范围诚实声明）
 *   3. 内嵌知识库段落（按 category 加载）
 *   4. 输出格式要求（四段式结构）
 *   5. 模型专项优化（按 modelType）
 *
 * @param {string|undefined} category   - 问题类别（来自 validators 或自动分类）
 * @param {string|undefined} urgency    - 'high' | 'medium' | 'low'
 * @param {string} [modelType='hunyuan'] - 目标模型
 * @returns {{ systemPrompt: string, knowledgeSources: string[], knowledgeVersion: string }}
 */
function buildSystemPrompt(category, urgency, modelType) {
  const model = modelType || 'hunyuan';

  // 加载知识库
  const kb = knowledgeBase.parseKnowledgeBase(category);

  // 公共基础（所有模型通用）
  const roleDefinition = [
    '你是噗滋慈善的 NGO 管理顾问，专为中国中小型草根公益机构提供管理知识支持。',
    '你熟悉中国慈善法规、社会组织登记管理规定、非营利组织治理规范和公益行业实践。',
    '你的定位是知识型顾问，不是律师或会计师。你提供参考信息，帮助 NGO 了解相关规则，',
    '但不出具任何法律意见，不替代专业律师、会计师或主管部门的权威判断。',
  ].join('\n');

  const systemPrompt = [
    roleDefinition,
    '',
    getAdvisorConstraints(),
    '',
    '【内嵌知识库（请基于以下内容回答问题，超出范围时明确说明）】',
    `知识库版本：${kb.version}`,
    `来源文件：${kb.sources.join(', ')}`,
    '',
    kb.text,
    '',
    getOutputFormatInstructions(urgency),
    '',
    _getModelSpecificInstructions(model),
  ].join('\n');

  return {
    systemPrompt,
    knowledgeSources: kb.sources,
    knowledgeVersion: kb.version,
  };
}

/**
 * 模型专项优化指令（私有辅助函数）
 *
 * @param {string} model
 * @returns {string}
 */
function _getModelSpecificInstructions(model) {
  const instructions = {
    hunyuan: [
      '【混元专项指令】',
      '请用专业但易懂的语气回答，避免过于学术化的表达。',
      '重要规则和截止日期请加粗或使用列表突出显示。',
      '直接输出四段式回答，不要输出开场白或模板说明。',
    ].join('\n'),

    deepseek: [
      '【DeepSeek 专项指令】',
      '严格按照四段式结构输出，不添加额外分析说明。',
      '引用知识库内容时保持准确，不做额外推断。',
      '仅输出回答正文，不要输出开场白。',
    ].join('\n'),

    doubao: [
      '【豆包专项指令】',
      '采用专业规范的语气，避免过于活泼的表达。',
      '必须输出完整的四段式结构，不得省略任何段落。',
      '每段标题使用【】格式（如【参考回答】），不使用其他格式。',
    ].join('\n'),

    glm: [
      '【GLM 专项指令】',
      '注重内容的逻辑严谨性，确保知识引用与回答逻辑一致。',
      '禁止自行推断知识库以外的法规内容。',
      '仅输出回答正文，不要添加任何元注释。',
    ].join('\n'),
  };

  return instructions[model] || instructions['hunyuan'];
}

// -----------------------------------------------------------------------
// 4. buildUserPrompt
// -----------------------------------------------------------------------

/**
 * 构建用户 prompt。
 *
 * 安全约束（Spec PII 处理章节）：
 *   - piiFields 中列出的字段（contact_name）必须从 input 中排除
 *   - question / question_context 须在调用前经 pii-filter 过滤（由 index.js 负责）
 *   - 此函数接收的 filteredQuestion / filteredContext 已经是过滤后的文本
 *
 * @param {object} input             - 用户输入数据（已通过 validators.js 校验）
 * @param {string} filteredQuestion  - pii-filter 过滤后的提问文本
 * @param {string|undefined} filteredContext - pii-filter 过滤后的背景文本（可选）
 * @param {string} detectedCategory  - 自动识别或用户指定的问题类别
 * @param {string[]} piiFields       - 需要排除的 PII 字段名列表（传递给排除逻辑）
 * @param {string} [modelType='hunyuan']
 * @returns {string}
 */
function buildUserPrompt(input, filteredQuestion, filteredContext, detectedCategory, piiFields, modelType) {
  const model = modelType || 'hunyuan';

  // 构建排除集合（防御性处理：始终排除 contact_name）
  const excludeSet = new Set([
    ...BUILTIN_PII_FIELDS,
    ...(Array.isArray(piiFields) ? piiFields : []),
  ]);

  // 提取机构上下文（排除 PII 字段）
  const contextFields = ['org_name', 'org_type', 'org_province', 'urgency'];
  const ctx = {};
  for (const key of contextFields) {
    if (!excludeSet.has(key) && input[key] !== undefined) {
      ctx[key] = input[key];
    }
  }

  // 机构信息段
  const orgTypeLabels = {
    foundation:          '基金会',
    social_group:        '社会团体',
    social_service_org:  '社会服务机构（原民办非企业单位）',
    other:               '其他类型组织',
  };

  const orgTypeLabel = orgTypeLabels[ctx.org_type] || ctx.org_type || '未知类型';
  const urgencyLabel = { high: '今日必须', medium: '本周内', low: '了解性质' };
  const urgencyText  = urgencyLabel[ctx.urgency] || '未指定';
  const categoryLabel = {
    policy_qa:  '政策法规',
    charity_law: '慈善法规',
    compliance: '合规操作',
    governance: '组织管理',
    finance:    '财务税务',
    hr:         '人力资源',
    other:      '综合/其他',
  };
  const catLabel = categoryLabel[detectedCategory] || '综合/其他';

  const orgContext = [
    `机构名称：${ctx.org_name || '[未填写]'}`,
    `机构类型：${orgTypeLabel}`,
    `注册省份：${ctx.org_province || '[未填写]'}`,
    `问题类别：${catLabel}`,
    `紧急程度：${urgencyText}`,
  ].join('\n');

  // 用户问题段
  const questionSection = [
    `提问：`,
    filteredQuestion,
  ].join('\n');

  // 补充背景段（可选）
  const contextSection = filteredContext && filteredContext.trim()
    ? `\n补充背景：\n${filteredContext}`
    : '';

  // DeepSeek/GLM 使用 XML 标签分隔（提升准确率）
  if (model === 'deepseek' || model === 'glm') {
    return [
      '<org_context>',
      orgContext,
      '</org_context>',
      '<question>',
      questionSection,
      contextSection,
      '</question>',
      '<instruction>',
      '请基于知识库内容，严格按照四段式结构（【问题理解】【参考回答】【建议行动】【重要提示】）回答上述问题。',
      '</instruction>',
    ].join('\n');
  }

  // 混元/豆包及其他模型：普通格式
  return [
    `【机构信息】`,
    orgContext,
    '',
    `【用户提问】`,
    questionSection,
    contextSection,
    '',
    '请基于知识库内容，严格按照四段式结构（【问题理解】【参考回答】【建议行动】【重要提示】）回答上述问题。',
  ].join('\n');
}

// -----------------------------------------------------------------------
// 5. buildPrompt（主入口）
// -----------------------------------------------------------------------

/**
 * 组装完整 prompt messages 数组（OpenAI-compatible messages 格式）。
 *
 * 流程：
 *   1. 自动识别问题类别（如未由用户指定）
 *   2. buildSystemPrompt → 构建系统 prompt（含知识库嵌入）
 *   3. buildUserPrompt → 构建用户 prompt（排除 PII）
 *   4. 返回 messages 数组 + 元数据
 *
 * 注意：filteredQuestion / filteredContext 须在调用前经 pii-filter 处理（由 index.js 负责）
 *
 * @param {object} input             - 用户输入（已通过 validators.js 校验）
 * @param {string} filteredQuestion  - pii-filter 过滤后的提问文本
 * @param {string|undefined} filteredContext - pii-filter 过滤后的背景文本（可选）
 * @param {string} [modelType='hunyuan'] - 目标模型
 * @param {string[]} [externalPiiFields=[]] - 额外需要排除的 PII 字段
 * @returns {{
 *   messages: Array<{ role: string, content: string }>,
 *   detectedCategory: string,
 *   knowledgeSources: string[],
 *   knowledgeVersion: string
 * }}
 */
function buildPrompt(input, filteredQuestion, filteredContext, modelType, externalPiiFields) {
  const model = modelType || 'hunyuan';

  // 确定问题类别：优先使用用户指定（question_category），否则自动分类
  const detectedCategory = (input.question_category && input.question_category !== 'other')
    ? input.question_category
    : knowledgeBase.classifyQuestion(filteredQuestion || '');

  const { systemPrompt, knowledgeSources, knowledgeVersion } = buildSystemPrompt(
    detectedCategory,
    input.urgency,
    model,
  );

  // 合并 PII 字段
  const piiFields = [
    ...BUILTIN_PII_FIELDS,
    ...(Array.isArray(externalPiiFields) ? externalPiiFields : []),
  ];

  const userPrompt = buildUserPrompt(
    input,
    filteredQuestion,
    filteredContext,
    detectedCategory,
    piiFields,
    model,
  );

  return {
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userPrompt },
    ],
    detectedCategory,
    knowledgeSources,
    knowledgeVersion,
  };
}

// -----------------------------------------------------------------------
// 导出
// -----------------------------------------------------------------------

module.exports = {
  buildPrompt,
  buildSystemPrompt,
  buildUserPrompt,
  getAdvisorConstraints,
  getOutputFormatInstructions,
  BUILTIN_PII_FIELDS,
};
