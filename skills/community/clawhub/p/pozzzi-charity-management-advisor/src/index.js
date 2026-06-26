'use strict';

// ---------------------------------------------------------------------------
// index.js — 管理顾问 Skill 主工作流入口
//
// 依赖：仅 Node.js 内置模块（通过共享包间接使用 fs）
// 合规依据：噗滋慈善管理顾问 Spec v1.0 + charity CLAUDE.md 合规红线
//   - PII 不入模型（contact_name 由 prompt-builder 排除；question/context 经 pii-filter）
//   - AI 标识声明强制注入（disclaimer-injector）
//   - 非法律意见声明：每条回答末尾强制附加（由 prompt 约束 + disclaimer-injector 双重保障）
//   - 禁止编造条文编号：system prompt 强制规则
//   - 模型不可用时降级：返回知识库原文 + 免责声明
//   - 审计日志不含 question 原文，仅含 question_hash
//   - 日志保留 ≥6 个月（由 storage-adapter 强制）
// ---------------------------------------------------------------------------

const { injectDisclaimer } = require('../../../packages/shared/disclaimer-injector');
const { filterPII }        = require('../../../packages/shared/pii-filter');
const { validate }         = require('./validators');
const promptBuilder        = require('./prompt-builder');
const knowledgeBase        = require('./knowledge-base');

// ---------------------------------------------------------------------------
// Skill 元数据
// ---------------------------------------------------------------------------

/** Skill ID — 用于 storage.appendHistory 的分区键 */
const SKILL_ID = 'management-advisor';

/** Skill 当前版本 */
const SKILL_VERSION = '1.0.0';

/** Skill 显示名称 */
const SKILL_NAME = '管理顾问';

// ---------------------------------------------------------------------------
// maxTokens 配置（问答型 Skill，所有类型统一 2000）
// ---------------------------------------------------------------------------

/**
 * 所有问题类型统一 maxTokens = 2000（Spec 第6节 Step 4）
 *
 * urgency 控制输出字数通过 system prompt 指令实现，
 * maxTokens 不按 urgency 变化（避免截断）
 *
 * @param {string} _questionCategory - 未使用，保留参数以便 v1.1 扩展
 * @returns {number}
 */
function getMaxTokens(_questionCategory) {
  return 2000;
}

// ---------------------------------------------------------------------------
// 内部工具函数
// ---------------------------------------------------------------------------

/**
 * 计算字符串的简单哈希值（用于 audit log 中的 question_hash）
 * 不使用加密哈希，只做日志去重标识
 *
 * @param {string} str
 * @returns {string} 十六进制哈希字符串
 */
function simpleHash(str) {
  if (typeof str !== 'string') return '0';
  let hash = 5381;
  for (let i = 0; i < str.length; i++) {
    // djb2 算法
    hash = ((hash << 5) + hash) + str.charCodeAt(i);
    hash = hash & hash; // 转为 32 位整数
  }
  return (hash >>> 0).toString(16);
}

/**
 * 构建降级时的知识库原文输出（模型不可用时的备用回答）
 *
 * 管理顾问降级策略：
 *   modelClient 未提供或调用失败时，返回知识库原文 + 免责声明。
 *   降级输出仍然有效，不视为错误（degraded=true）。
 *
 * @param {object} input       - 用户输入
 * @param {string} kbText      - 相关知识库文本
 * @param {string} category    - 已识别的问题类别
 * @returns {string}
 */
function buildDegradedOutput(input, kbText, category) {
  const categoryLabels = {
    policy_qa:  '政策法规',
    charity_law: '慈善法规',
    compliance: '合规操作',
    governance: '组织管理',
    finance:    '财务税务',
    hr:         '人力资源',
    other:      '综合/其他',
  };
  const catLabel = categoryLabels[category] || '综合/其他';

  const lines = [
    `# 管理顾问（知识库参考模式）`,
    ``,
    `> 当前为降级模式：AI 模型暂时不可用，以下为 **${catLabel}** 相关知识库原文，供参考使用。`,
    ``,
    `## 您的提问`,
    ``,
    `${input.question || '[问题未填写]'}`,
    ``,
    `## 相关知识库内容`,
    ``,
    kbText || '[知识库内容加载失败]',
    ``,
    `---`,
    ``,
    `**重要说明**：以上为知识库原文，未经 AI 个性化处理。如需针对您具体情况的解答，请在 AI 服务恢复后重新提问。`,
    ``,
    `本回答不构成法律意见，建议就具体情况咨询专业律师、会计师或主管部门。`,
  ];
  return lines.join('\n');
}

// ---------------------------------------------------------------------------
// PII 过滤辅助函数
// ---------------------------------------------------------------------------

/**
 * 对提问文本执行 pii-filter，返回过滤结果。
 * blocked=true 时调用方必须中止，不得继续调用模型 API。
 *
 * @param {string} questionText
 * @returns {{ filtered: string, blocked: boolean, detected: Array }}
 */
function _filterQuestionText(questionText) {
  if (typeof questionText !== 'string' || !questionText) {
    return { filtered: '', blocked: false, detected: [] };
  }
  try {
    return filterPII(questionText);
  } catch (err) {
    // pii-filter 内部异常 → 保守处理：阻断调用
    return { filtered: '', blocked: true, detected: [], _error: err.message };
  }
}

// ---------------------------------------------------------------------------
// 主工作流
// ---------------------------------------------------------------------------

/**
 * 主工作流入口
 *
 * 管理顾问特有步骤：
 *   1. 输入校验（validate）
 *   2. PII 过滤（pii-filter 处理 question + question_context）
 *      → blocked:true 时提示用户删除个人信息，终止调用
 *   3. 自动问题分类（classifyQuestion，如未显式指定 question_category）
 *   4. Prompt 构建（promptBuilder.buildPrompt）
 *   5. 模型调用（temperature 0.4，maxTokens 2000）
 *   6. 注入 AI 标识声明（injectDisclaimer）
 *   7. 写审计日志（含 question_hash，不含 question 原文）
 *   8. 返回结果
 *
 * 降级策略（管理顾问独有）：
 *   - modelClient 未提供 → 返回知识库原文 + 免责声明（degraded=true）
 *   - 模型调用失败 → 降级返回知识库原文 + 免责声明（degraded=true）
 *
 * @param {object} input   - 用户输入对象（含 org_name/org_type/org_province/question 等）
 * @param {object} options - 配置对象
 * @param {object} [options.modelClient]     - model-gateway ModelClient 实例（依赖注入，可选）
 * @param {object} [options.storage]         - storage-adapter 实例（依赖注入）
 * @param {string} [options.modelType='hunyuan'] - 模型类型字符串，传给 promptBuilder
 * @returns {Promise<{
 *   success: boolean,
 *   answer?: string,
 *   metadata?: {
 *     model: string|null,
 *     provider: string|null,
 *     degraded: boolean,
 *     duration_ms: number,
 *     version: string,
 *     detectedCategory: string,
 *     knowledgeSources: string[],
 *     knowledgeVersion: string
 *   },
 *   warnings?: string[],
 *   errors?: string[]
 * }>}
 */
async function handleQuery(input, options = {}) {
  const { modelClient, storage, modelType = 'hunyuan' } = options;

  // -------------------------------------------------------------------
  // Step 1: 输入校验
  // -------------------------------------------------------------------
  const validationResult = validate(input);

  if (!validationResult.valid) {
    return {
      success: false,
      errors:  validationResult.errors,
      warnings: validationResult.warnings,
    };
  }

  // 有 warnings → 记录但不阻断
  const warnings = validationResult.warnings.slice();

  const startTime = Date.now();

  // -------------------------------------------------------------------
  // Step 2: PII 过滤（question + question_context）
  // blocked:true → 提示用户删除个人信息，终止调用
  // -------------------------------------------------------------------
  const questionText  = (input.question || '').trim();
  const contextText   = (input.question_context || '').trim();

  const questionFilter = _filterQuestionText(questionText);
  if (questionFilter.blocked) {
    return {
      success: false,
      errors: [
        '您的问题中包含个人信息（如姓名/手机号），为保护当事人隐私，请将姓名替换为职位描述' +
        '（如"项目负责人""受益人A"），删除手机号等识别信息后重新提问。',
      ],
      warnings,
    };
  }

  let filteredContext;
  if (contextText) {
    const contextFilter = _filterQuestionText(contextText);
    if (contextFilter.blocked) {
      return {
        success: false,
        errors: [
          '您填写的问题背景（question_context）中包含个人信息，请删除后重新提问。',
        ],
        warnings,
      };
    }
    filteredContext = contextFilter.filtered;
  }

  const filteredQuestion = questionFilter.filtered;
  const questionHash = simpleHash(questionText);

  // -------------------------------------------------------------------
  // Step 3: 自动分类（供降级路径和日志使用）
  // -------------------------------------------------------------------
  const detectedCategory = (input.question_category && input.question_category !== 'other')
    ? input.question_category
    : knowledgeBase.classifyQuestion(filteredQuestion);

  // -------------------------------------------------------------------
  // 降级判断：modelClient 未提供时直接返回知识库原文
  // -------------------------------------------------------------------
  if (!modelClient || typeof modelClient.chat !== 'function') {
    const durationMs = Date.now() - startTime;
    const kbResult   = knowledgeBase.parseKnowledgeBase(detectedCategory);
    const degradedContent = buildDegradedOutput(input, kbResult.text, detectedCategory);

    const { content: answerWithDisclaimer } = injectDisclaimer(
      degradedContent,
      {
        format:    'markdown',
        skillName: SKILL_NAME,
        modelName: '',
      },
    );

    await _safeAppendAuditLog(storage, {
      event:             'query_completed',
      org_name:          input.org_name,
      question_category: detectedCategory,
      question_hash:     questionHash,
      model_used:        null,
      provider:          null,
      degraded:          true,
      success:           true,
      duration_ms:       durationMs,
    });

    await _safeAppendHistory(storage, SKILL_ID, {
      org_name:          input.org_name,
      question_category: detectedCategory,
      timestamp:         new Date().toISOString(),
      model_used:        null,
      provider:          null,
      degraded:          true,
      success:           true,
      duration_ms:       durationMs,
    });

    return {
      success: true,
      answer:  answerWithDisclaimer,
      metadata: {
        model:             null,
        provider:          null,
        degraded:          true,
        duration_ms:       durationMs,
        version:           SKILL_VERSION,
        detectedCategory,
        knowledgeSources:  kbResult.sources,
        knowledgeVersion:  kbResult.version,
      },
      warnings,
    };
  }

  // -------------------------------------------------------------------
  // Step 4: Prompt 构建
  // -------------------------------------------------------------------
  try {
    const { messages, knowledgeSources, knowledgeVersion } = promptBuilder.buildPrompt(
      input,
      filteredQuestion,
      filteredContext,
      modelType,
      validationResult.piiFields,
    );

    // -------------------------------------------------------------------
    // Step 5: 模型调用（temperature 0.4，maxTokens 2000）
    // -------------------------------------------------------------------
    const maxTokens = getMaxTokens(detectedCategory);

    let chatResult;
    let degraded = false;

    try {
      chatResult = await modelClient.chat(messages, {
        temperature: 0.4,
        maxTokens,
      });
    } catch (modelErr) {
      // 模型调用失败 → 降级：返回知识库原文
      degraded = true;
      const durationMs = Date.now() - startTime;
      const kbResult   = knowledgeBase.parseKnowledgeBase(detectedCategory);
      const degradedContent = buildDegradedOutput(input, kbResult.text, detectedCategory);

      const { content: answerWithDisclaimer } = injectDisclaimer(
        degradedContent,
        {
          format:    'markdown',
          skillName: SKILL_NAME,
          modelName: '',
        },
      );

      await _safeAppendAuditLog(storage, {
        event:             'query_completed',
        org_name:          input.org_name,
        question_category: detectedCategory,
        question_hash:     questionHash,
        model_used:        null,
        provider:          null,
        degraded:          true,
        success:           true,
        duration_ms:       durationMs,
        degraded_reason:   modelErr.message,
      });

      await _safeAppendHistory(storage, SKILL_ID, {
        org_name:          input.org_name,
        question_category: detectedCategory,
        timestamp:         new Date().toISOString(),
        model_used:        null,
        provider:          null,
        degraded:          true,
        success:           true,
        duration_ms:       durationMs,
      });

      return {
        success: true,
        answer:  answerWithDisclaimer,
        metadata: {
          model:             null,
          provider:          null,
          degraded:          true,
          duration_ms:       durationMs,
          version:           SKILL_VERSION,
          detectedCategory,
          knowledgeSources:  kbResult.sources,
          knowledgeVersion:  kbResult.version,
        },
        warnings: [...warnings, `模型调用失败，已降级输出知识库原文：${modelErr.message}`],
      };
    }

    const durationMs = Date.now() - startTime;

    // -------------------------------------------------------------------
    // Step 6: 注入 AI 标识声明 + 免责提示（合规红线 P0）
    // -------------------------------------------------------------------
    const { content: answerWithDisclaimer } = injectDisclaimer(
      chatResult.content,
      {
        format:    'markdown',
        skillName: SKILL_NAME,
        modelName: chatResult.provider || chatResult.model,
      },
    );

    // -------------------------------------------------------------------
    // Step 7: 写入审计日志（不含 question 原文，仅含 question_hash）
    // -------------------------------------------------------------------
    await _safeAppendAuditLog(storage, {
      event:             'query_completed',
      org_name:          input.org_name,
      question_category: detectedCategory,
      question_hash:     questionHash,
      model_used:        chatResult.model,
      provider:          chatResult.provider,
      degraded:          chatResult.degraded || false,
      success:           true,
      duration_ms:       durationMs,
    });

    await _safeAppendHistory(storage, SKILL_ID, {
      org_name:          input.org_name,
      question_category: detectedCategory,
      timestamp:         new Date().toISOString(),
      model_used:        chatResult.model,
      provider:          chatResult.provider,
      degraded:          chatResult.degraded || false,
      success:           true,
      duration_ms:       durationMs,
    });

    // -------------------------------------------------------------------
    // Step 8: 返回结果
    // -------------------------------------------------------------------
    return {
      success: true,
      answer:  answerWithDisclaimer,
      metadata: {
        model:             chatResult.model,
        provider:          chatResult.provider,
        degraded:          chatResult.degraded || degraded,
        duration_ms:       durationMs,
        version:           SKILL_VERSION,
        detectedCategory,
        knowledgeSources,
        knowledgeVersion,
      },
      warnings,
    };

  } catch (err) {
    const durationMs = Date.now() - startTime;

    // 非模型调用的其他错误（如 prompt-builder 内部错误）— 写审计日志后返回失败
    await _safeAppendAuditLog(storage, {
      event:             'query_completed',
      org_name:          input.org_name,
      question_category: detectedCategory,
      question_hash:     questionHash,
      model_used:        null,
      success:           false,
      duration_ms:       durationMs,
      error_type:        err.name || 'Error',
    });

    return {
      success: false,
      errors:  [err.message],
      warnings,
    };
  }
}

// ---------------------------------------------------------------------------
// 内部辅助（日志写入容错）
// ---------------------------------------------------------------------------

/**
 * 安全写入审计日志（失败时 console.error，不抛出到主流程）
 *
 * @param {object|undefined} storage
 * @param {object} entry
 */
async function _safeAppendAuditLog(storage, entry) {
  if (!storage || typeof storage.appendAuditLog !== 'function') return;
  try {
    await Promise.resolve(storage.appendAuditLog(entry));
  } catch (err) {
    console.error('[management-advisor] 审计日志写入失败（非阻断）:', err.message);
  }
}

/**
 * 安全写入历史记录（失败时 console.error，不抛出到主流程）
 *
 * @param {object|undefined} storage
 * @param {string} skillId
 * @param {object} entry
 */
async function _safeAppendHistory(storage, skillId, entry) {
  if (!storage || typeof storage.appendHistory !== 'function') return;
  try {
    await Promise.resolve(storage.appendHistory(skillId, entry));
  } catch (err) {
    console.error('[management-advisor] 历史记录写入失败（非阻断）:', err.message);
  }
}

// ---------------------------------------------------------------------------
// 导出
// ---------------------------------------------------------------------------

module.exports = {
  handleQuery,
  getMaxTokens,
  simpleHash,
};
