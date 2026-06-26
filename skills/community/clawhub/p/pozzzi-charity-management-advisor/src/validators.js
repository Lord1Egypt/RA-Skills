'use strict';

// -----------------------------------------------------------------------
// validators.js — 管理顾问 Skill 输入校验器
//
// 依赖：仅 Node.js 内置模块
// 合规依据：噗滋慈善管理顾问 Spec v1.0 + PIPL 第23/28条 + 慈善法第75/77条
// -----------------------------------------------------------------------

/**
 * 合并两个校验结果对象（将 src 的 errors/warnings 追加到 dest）
 * @param {{ errors: string[], warnings: string[] }} dest
 * @param {{ errors: string[], warnings: string[] }} src
 */
function mergeResult(dest, src) {
  dest.errors.push(...src.errors);
  dest.warnings.push(...src.warnings);
}

// -----------------------------------------------------------------------
// 枚举常量
// -----------------------------------------------------------------------

/**
 * org_type 有效枚举值
 * @type {string[]}
 */
const VALID_ORG_TYPES = ['foundation', 'social_group', 'social_service_org', 'other'];

/**
 * question_category 有效枚举值
 * - charity_law    : 政策法规问答
 * - compliance     : 合规操作指引
 * - governance     : 组织管理建议
 * - finance        : 财务相关
 * - hr             : 人力资源
 * - other          : 其他/混合
 *
 * @type {string[]}
 */
const VALID_QUESTION_CATEGORIES = [
  'charity_law',
  'policy_qa',
  'compliance',
  'governance',
  'finance',
  'hr',
  'other',
];

/**
 * urgency 有效枚举值
 * @type {string[]}
 */
const VALID_URGENCY = ['high', 'medium', 'low'];

/**
 * question 最大长度（字符数）
 */
const QUESTION_MAX_LENGTH = 500;

/**
 * question_context 最大长度（字符数）
 */
const QUESTION_CONTEXT_MAX_LENGTH = 200;

// -----------------------------------------------------------------------
// 1. 通用必填字段校验
// -----------------------------------------------------------------------

/**
 * 校验管理顾问通用必填字段。
 *
 * PII 安全注释：contact_name 在此仅做非空校验，
 * 不进入 Prompt，由 validatePIISafety 负责标记和排除。
 *
 * @param {object} input
 * @returns {{ valid: boolean, errors: string[], warnings: string[] }}
 */
function validateCommonInput(input) {
  const errors = [];
  const warnings = [];

  if (!input || typeof input !== 'object') {
    return { valid: false, errors: ['input 必须是对象'], warnings: [] };
  }

  // org_name — 非空字符串
  if (!input.org_name || typeof input.org_name !== 'string' || !input.org_name.trim()) {
    errors.push('org_name 为必填字段，不能为空');
  }

  // org_type — 枚举，必填
  if (!input.org_type) {
    errors.push('org_type 为必填字段');
  } else if (!VALID_ORG_TYPES.includes(input.org_type)) {
    errors.push(
      `org_type 值无效："${input.org_type}"，有效值为：${VALID_ORG_TYPES.join('/')}`,
    );
  }

  // org_province — 非空字符串，必填
  if (!input.org_province || typeof input.org_province !== 'string' || !input.org_province.trim()) {
    errors.push('org_province 为必填字段，不能为空');
  }

  // question — 非空字符串，必填，最长 500 字
  if (!input.question || typeof input.question !== 'string' || !input.question.trim()) {
    errors.push('question 为必填字段，不能为空');
  } else if (input.question.trim().length > QUESTION_MAX_LENGTH) {
    errors.push(
      `question 长度超出限制（当前 ${input.question.trim().length} 字，最大 ${QUESTION_MAX_LENGTH} 字）。请聚焦核心问题后重新提问`,
    );
  }

  // contact_name — 必填（PII，仅存本地日志，不进模型）
  if (
    !input.contact_name ||
    typeof input.contact_name !== 'string' ||
    !input.contact_name.trim()
  ) {
    errors.push('contact_name 为必填字段，不能为空');
  }

  return { valid: errors.length === 0, errors, warnings };
}

// -----------------------------------------------------------------------
// 2. 可选字段校验
// -----------------------------------------------------------------------

/**
 * 校验可选字段（question_category / question_context / urgency）。
 * 应在 validateCommonInput 通过后调用。
 *
 * @param {object} input
 * @returns {{ valid: boolean, errors: string[], warnings: string[] }}
 */
function validateOptionalInput(input) {
  const errors = [];
  const warnings = [];

  if (!input || typeof input !== 'object') {
    return { valid: false, errors: ['input 必须是对象'], warnings: [] };
  }

  // question_category — 可选枚举
  if (input.question_category !== undefined && input.question_category !== null) {
    if (!VALID_QUESTION_CATEGORIES.includes(input.question_category)) {
      errors.push(
        `question_category 值无效："${input.question_category}"，有效值为：${VALID_QUESTION_CATEGORIES.join('/')}`,
      );
    }
  }

  // question_context — 可选，如提供则最长 200 字
  if (input.question_context !== undefined && input.question_context !== null) {
    if (typeof input.question_context !== 'string') {
      errors.push('question_context 如提供则必须是字符串');
    } else if (input.question_context.trim().length > QUESTION_CONTEXT_MAX_LENGTH) {
      errors.push(
        `question_context 长度超出限制（当前 ${input.question_context.trim().length} 字，最大 ${QUESTION_CONTEXT_MAX_LENGTH} 字）`,
      );
    }
  }

  // urgency — 可选枚举
  if (input.urgency !== undefined && input.urgency !== null) {
    if (!VALID_URGENCY.includes(input.urgency)) {
      errors.push(
        `urgency 值无效："${input.urgency}"，有效值为：${VALID_URGENCY.join('/')}`,
      );
    }
  }

  return { valid: errors.length === 0, errors, warnings };
}

// -----------------------------------------------------------------------
// 3. PII 安全校验
// -----------------------------------------------------------------------

/**
 * PII 安全校验（管理顾问版）。
 *
 * 合规依据：PIPL 第23/28条、管理顾问 Spec v1.0
 * - 标记 contact_name 为 piiFields，供 prompt-builder 排除
 * - 检测 question / question_context 中疑似中文真实姓名 → warning 提示替换
 *
 * 注意：PII 拦截（blocked）由 index.js 在调用 pii-filter.filterPII() 时处理。
 * 本函数只做静态字段标记和 warning 预提示，不执行 blockOnDetect 逻辑。
 *
 * @param {object} input
 * @returns {{ piiFields: string[], warnings: string[] }}
 */
function validatePIISafety(input) {
  // contact_name 是唯一必须从 prompt 中排除的顶级 PII 字段
  const piiFields = ['contact_name'];
  const warnings = [];

  if (!input || typeof input !== 'object') {
    return { piiFields, warnings };
  }

  // 检测 question / question_context 中疑似中文真实姓名（关键词前缀形式）
  // 与 pii-filter 使用相同的模式逻辑，提前在 validate 阶段给用户友好提示
  const nameContextPattern = /(?:姓名|受益人|申请人|联系人|负责人|户主|监护人|家长|学生|志愿者)[：:]\s*[\u4e00-\u9fa5]{2,4}/;
  const phonePattern = /(?:(?:\+?0{0,2}86)[-\s]?)?1[3-9]\d{9}/;
  const idCardPattern = /[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dX]/i;

  const fieldsToCheck = [
    { field: 'question', label: '提问内容' },
    { field: 'question_context', label: '问题背景' },
  ];

  for (const { field, label } of fieldsToCheck) {
    const text = input[field];
    if (typeof text !== 'string' || !text.trim()) continue;

    if (nameContextPattern.test(text)) {
      warnings.push(
        `${label}（${field}）中检测到疑似真实姓名。请将姓名替换为职位描述（如"项目负责人""受益人A"），以保护相关人员隐私。`,
      );
    }
    if (phonePattern.test(text)) {
      warnings.push(
        `${label}（${field}）中检测到疑似手机号码。请删除手机号后重新提问，以保护个人隐私。`,
      );
    }
    if (idCardPattern.test(text)) {
      warnings.push(
        `${label}（${field}）中检测到疑似身份证号码。请删除身份证号后重新提问，以保护个人隐私。`,
      );
    }
  }

  return { piiFields, warnings };
}

// -----------------------------------------------------------------------
// 4. 总入口
// -----------------------------------------------------------------------

/**
 * 总校验入口。按顺序执行：
 * 1. 通用必填字段校验（validateCommonInput）
 * 2. 可选字段校验（validateOptionalInput）
 * 3. PII 安全校验（validatePIISafety，仅追加 warnings，不影响 valid）
 *
 * @param {object} input
 * @returns {{ valid: boolean, errors: string[], warnings: string[], piiFields: string[] }}
 */
function validate(input) {
  const result = { valid: true, errors: [], warnings: [], piiFields: [] };

  // Step 1: 通用必填校验
  const commonResult = validateCommonInput(input);
  mergeResult(result, commonResult);

  // Step 2: 可选字段校验（即使通用校验失败也继续，收集全部错误）
  const optionalResult = validateOptionalInput(input);
  mergeResult(result, optionalResult);

  // Step 3: PII 安全校验（仅追加 warnings/piiFields，不影响 valid）
  const piiResult = validatePIISafety(input);
  result.warnings.push(...piiResult.warnings);
  result.piiFields = piiResult.piiFields;

  // 汇总：有 error 则 valid = false
  result.valid = result.errors.length === 0;

  return result;
}

// -----------------------------------------------------------------------
// 导出
// -----------------------------------------------------------------------

module.exports = {
  validate,
  validateCommonInput,
  validateOptionalInput,
  validatePIISafety,
  VALID_ORG_TYPES,
  VALID_QUESTION_CATEGORIES,
  VALID_URGENCY,
  QUESTION_MAX_LENGTH,
  QUESTION_CONTEXT_MAX_LENGTH,
};
