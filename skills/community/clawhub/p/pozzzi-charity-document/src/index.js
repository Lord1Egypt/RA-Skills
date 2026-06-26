'use strict';

// ---------------------------------------------------------------------------
// index.js — 文书助手 Skill 主工作流入口
//
// 依赖：仅 Node.js 内置模块（通过共享包间接使用 fs）
// 合规依据：噗滋慈善文书助手 Spec v1.0 + charity CLAUDE.md 合规红线
//   - PII 不入模型（contact_name / contact_phone 由 prompt-builder 排除）
//   - AI 标识声明强制注入（disclaimer-injector）
//   - 固定条款注入（fixed-clause-handler via promptBuilder.injectFixedClauses）
//   - 审计日志不含 prompt 正文和生成内容
//   - 日志保留 ≥6 个月（由 storage-adapter 强制）
// ---------------------------------------------------------------------------

const { injectDisclaimer }  = require('../../../packages/shared/disclaimer-injector');
const { validate }          = require('./validators');
const promptBuilder         = require('./prompt-builder');

// ---------------------------------------------------------------------------
// Skill 元数据
// ---------------------------------------------------------------------------

/** Skill ID — 用于 storage.appendHistory 的分区键 */
const SKILL_ID = 'document-assistant';

/** Skill 当前版本 */
const SKILL_VERSION = '1.0.0';

// ---------------------------------------------------------------------------
// maxTokens 配置表（对应文书类型）
// ---------------------------------------------------------------------------

/**
 * 文书类型 → maxTokens 映射
 *
 * prompt-builder 使用的文书类型枚举（来自 resolveTemplateFilename）：
 *   contract / meeting_minutes / official_letter / thank_you_letter / work_plan
 *
 * @type {Record<string, number>}
 */
const MAX_TOKENS_MAP = {
  contract:       3000,
  meeting_minutes: 2000,
  official_letter: 1500,
  thank_you_letter: 1000,
  work_plan:       2500,
};

/** 未知类型默认值 */
const DEFAULT_MAX_TOKENS = 2000;

// ---------------------------------------------------------------------------
// 工具函数
// ---------------------------------------------------------------------------

/**
 * 根据文书类型返回 maxTokens
 *
 * @param {string} documentType - 'contract' | 'meeting_minutes' | 'official_letter'
 *                                | 'thank_you_letter' | 'work_plan'
 * @returns {number} maxTokens；未知类型返回 DEFAULT_MAX_TOKENS（2000）
 */
function getMaxTokens(documentType) {
  return MAX_TOKENS_MAP[documentType] || DEFAULT_MAX_TOKENS;
}

/**
 * 从包含多个章节的 Markdown 文书中提取指定章节的内容
 *
 * 策略：匹配以 "## <sectionName>" 开头的段落，
 * 直到下一个同级或更高级标题（## / #）或文档结束。
 *
 * @param {string} docContent  - 完整 Markdown 文书正文
 * @param {string} sectionName - 目标章节名（不含 "## " 前缀）
 * @returns {{ found: boolean, content: string, startIndex: number, endIndex: number }}
 */
function extractSection(docContent, sectionName) {
  const headingPattern = new RegExp(
    `^#{1,3}\\s+[^\\n]*${escapeRegex(sectionName)}[^\\n]*$`,
    'm',
  );
  const match = headingPattern.exec(docContent);

  if (!match) {
    return { found: false, content: '', startIndex: -1, endIndex: -1 };
  }

  const startIndex = match.index;

  const afterMatch = docContent.slice(startIndex + match[0].length);
  const nextHeadingPattern = /^#{1,2}\s+/m;
  const nextMatch = nextHeadingPattern.exec(afterMatch);

  const endIndex = nextMatch !== null
    ? startIndex + match[0].length + nextMatch.index
    : docContent.length;

  return {
    found: true,
    content: docContent.slice(startIndex, endIndex),
    startIndex,
    endIndex,
  };
}

/**
 * 将新章节内容替换到原始文书的对应位置
 *
 * @param {string} docContent        - 完整文书（已去除 disclaimer）
 * @param {string} sectionName       - 目标章节名
 * @param {string} newSectionContent - 新章节内容（已包含标题行）
 * @returns {{ success: boolean, content: string }}
 */
function replaceSection(docContent, sectionName, newSectionContent) {
  const { found, startIndex, endIndex } = extractSection(docContent, sectionName);

  if (!found) {
    return { success: false, content: docContent };
  }

  const updated =
    docContent.slice(0, startIndex) +
    newSectionContent.trimEnd() +
    '\n' +
    docContent.slice(endIndex);

  return { success: true, content: updated };
}

/**
 * 转义正则特殊字符
 *
 * @param {string} str
 * @returns {string}
 */
function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * 从已注入 disclaimer 的完整文书中剥离声明部分，返回纯内容
 *
 * disclaimer-injector 注入格式为：
 *   <headerText>\n\n<content>\n\n<footerText>
 *
 * 剥离策略：
 *   - 找到第一个 "\n\n" 后的内容作为正文起点
 *   - 找到最后一个 "\n\n---\n" 之前的内容作为正文终点（markdown footer 以 "---" 开头）
 *
 * @param {string} docWithDisclaimer
 * @returns {string} 纯文书内容（不含 disclaimer）
 */
function stripDisclaimer(docWithDisclaimer) {
  const firstSep = docWithDisclaimer.indexOf('\n\n');
  if (firstSep === -1) return docWithDisclaimer;

  const bodyStart = firstSep + 2;

  const footerSep = docWithDisclaimer.lastIndexOf('\n\n---\n');
  if (footerSep === -1 || footerSep <= bodyStart) {
    return docWithDisclaimer.slice(bodyStart);
  }

  return docWithDisclaimer.slice(bodyStart, footerSep);
}

// ---------------------------------------------------------------------------
// 主工作流
// ---------------------------------------------------------------------------

/**
 * 主工作流入口（对应 Spec Step 1-8）
 *
 * 文书助手特有步骤：
 *   1. buildPrompt 返回 { messages, fixedClauses }
 *   2. 模型调用后先注入固定条款（injectFixedClauses）
 *   3. 再注入 AI 标识声明（injectDisclaimer）
 *   4. metadata 额外含 fixedClauseCount（注入的固定条款数）
 *   5. temperature 动态（getTemperature）而非固定值
 *
 * @param {object} input   - 用户输入对象（含 document_type、document_subtype、org_name 等字段）
 * @param {object} options - 配置对象
 * @param {object} options.modelClient  - model-gateway ModelClient 实例（依赖注入）
 * @param {object} options.storage      - storage-adapter 实例（依赖注入）
 * @param {string} [options.modelType='hunyuan'] - 模型类型字符串，传给 promptBuilder
 * @returns {Promise<{
 *   success: boolean,
 *   report?: string,
 *   metadata?: {
 *     model: string,
 *     provider: string,
 *     degraded: boolean,
 *     duration_ms: number,
 *     version: string,
 *     fixedClauseCount: number
 *   },
 *   warnings?: string[],
 *   errors?: string[]
 * }>}
 */
async function handleDocument(input, options = {}) {
  const { modelClient, storage, modelType = 'hunyuan' } = options;

  // -------------------------------------------------------------------
  // Step 1-3: 输入校验
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

  try {
    // -------------------------------------------------------------------
    // Step 4: Prompt 构建
    // 文书助手特有：buildPrompt 返回 { messages, fixedClauses }
    // -------------------------------------------------------------------
    const { messages, fixedClauses } = promptBuilder.buildPrompt(input, modelType, validationResult.piiFields);

    // -------------------------------------------------------------------
    // Step 5: 模型调用
    // temperature 动态（按文书类型）
    // maxTokens 按文书类型
    // PII 前置过滤由 model-gateway 内置，此处不重复调用 pii-filter
    // -------------------------------------------------------------------
    const temperature = promptBuilder.getTemperature(
      input.document_type,
      input.document_subtype,
    );
    const maxTokens = getMaxTokens(input.document_type);

    const chatResult = await modelClient.chat(messages, {
      temperature,
      maxTokens,
    });

    const durationMs = Date.now() - startTime;

    // -------------------------------------------------------------------
    // Step 6a: 文书助手特有 — 注入固定法律条款（在 disclaimer 注入前）
    // 固定条款（保密、不可抗力、协议生效等）不经过模型，直接注入
    // -------------------------------------------------------------------
    const contentWithClauses = promptBuilder.injectFixedClauses(
      chatResult.content,
      fixedClauses,
    );

    // -------------------------------------------------------------------
    // Step 6b: 注入 AI 标识声明 + 免责提示（合规红线 P0）
    // -------------------------------------------------------------------
    const { content: reportWithDisclaimer } = injectDisclaimer(
      contentWithClauses,
      {
        format:    'markdown',
        skillName: '文书助手',
        modelName: chatResult.provider || chatResult.model,
      },
    );

    // -------------------------------------------------------------------
    // Step 6c: 写入审计日志（不含 prompt 正文和生成内容）
    // 文书助手额外记录 fixed_clause_count
    // -------------------------------------------------------------------
    await _safeAppendAuditLog(storage, {
      event:              'document_generated',
      org_name:           input.org_name,
      document_type:      input.document_type,
      document_subtype:   input.document_subtype,
      model_used:         chatResult.model,
      provider:           chatResult.provider,
      degraded:           chatResult.degraded,
      success:            true,
      duration_ms:        durationMs,
      fixed_clause_count: fixedClauses.length,
    });

    // Step 6d: 写入生成历史
    await _safeAppendHistory(storage, SKILL_ID, {
      org_name:         input.org_name,
      document_type:    input.document_type,
      document_subtype: input.document_subtype,
      timestamp:        new Date().toISOString(),
      model_used:       chatResult.model,
      provider:         chatResult.provider,
      success:          true,
      duration_ms:      durationMs,
    });

    // -------------------------------------------------------------------
    // 返回结果
    // -------------------------------------------------------------------
    return {
      success: true,
      report:  reportWithDisclaimer,
      metadata: {
        model:           chatResult.model,
        provider:        chatResult.provider,
        degraded:        chatResult.degraded,
        duration_ms:     durationMs,
        version:         SKILL_VERSION,
        fixedClauseCount: fixedClauses.length,
      },
      warnings,
    };

  } catch (err) {
    const durationMs = Date.now() - startTime;

    // 模型调用失败（含 PII 阻断）— 写审计日志后向上透出
    await _safeAppendAuditLog(storage, {
      event:          'document_generated',
      org_name:       input.org_name,
      document_type:  input.document_type,
      document_subtype: input.document_subtype,
      model_used:     null,
      success:        false,
      duration_ms:    durationMs,
      error_type:     err.name || 'Error',
    });

    return {
      success: false,
      errors:  [err.message],
      warnings,
    };
  }
}

// ---------------------------------------------------------------------------
// 单章节重生成
// ---------------------------------------------------------------------------

/**
 * 对指定章节重新调用模型生成，并合并回完整文书
 *
 * @param {object} input           - 原始用户输入对象（与 handleDocument 相同结构）
 * @param {string} sectionName     - 目标章节名（如 "甲方义务"）
 * @param {string} previousReport  - 上一次 handleDocument 返回的带 disclaimer 完整文书
 * @param {object} options         - 同 handleDocument options
 * @returns {Promise<{
 *   success: boolean,
 *   report?: string,
 *   metadata?: {
 *     model: string,
 *     provider: string,
 *     degraded: boolean,
 *     duration_ms: number,
 *     version: string,
 *     fixedClauseCount: number
 *   },
 *   warnings?: string[],
 *   errors?: string[]
 * }>}
 */
async function regenerateSection(input, sectionName, previousReport, options = {}) {
  const { modelClient, storage, modelType = 'hunyuan' } = options;

  if (!sectionName || typeof sectionName !== 'string' || !sectionName.trim()) {
    return { success: false, errors: ['sectionName 不能为空'] };
  }

  if (sectionName.length > 100) {
    return { success: false, errors: ['sectionName 不能超过 100 个字符'] };
  }

  if (!previousReport || typeof previousReport !== 'string') {
    return { success: false, errors: ['previousReport 不能为空'] };
  }

  const MAX_REPORT_LENGTH = 500000;
  if (previousReport.length > MAX_REPORT_LENGTH) {
    return {
      success: false,
      errors: [`previousReport 超过最大长度限制（${MAX_REPORT_LENGTH} 字符）`],
    };
  }

  // 同 handleDocument 一样先校验输入（合规必经）
  const validationResult = validate(input);
  if (!validationResult.valid) {
    return {
      success: false,
      errors:  validationResult.errors,
      warnings: validationResult.warnings,
    };
  }

  const warnings = validationResult.warnings.slice();
  const startTime = Date.now();

  try {
    // 从完整文书中剥离 disclaimer，得到纯内容
    const pureContent = stripDisclaimer(previousReport);

    // 检查目标章节是否存在
    const { found: sectionFound } = extractSection(pureContent, sectionName);
    if (!sectionFound) {
      warnings.push(
        `章节 "${sectionName}" 在原文书中未找到，将生成新章节并附加到文书末尾`,
      );
    }

    // 构建章节重生成专用 prompt（传入 sectionName 提示模型只生成指定章节）
    const { messages, fixedClauses } = promptBuilder.buildPrompt(
      { ...input, _regenerate_section: sectionName },
      modelType,
      validationResult.piiFields,
    );

    // 只对该章节调用模型（token 预算减少为全量的 1/3）
    const temperature = promptBuilder.getTemperature(
      input.document_type,
      input.document_subtype,
    );
    const maxTokens = Math.ceil(getMaxTokens(input.document_type) / 3);

    const chatResult = await modelClient.chat(messages, {
      temperature,
      maxTokens,
    });

    const durationMs = Date.now() - startTime;

    // 注入固定法律条款（仅对当前重生成的章节内容）
    const sectionWithClauses = promptBuilder.injectFixedClauses(
      chatResult.content,
      fixedClauses,
    );

    // 将新章节内容合并回原始纯文书
    let updatedContent;
    if (sectionFound) {
      const { success: replaced, content } = replaceSection(
        pureContent,
        sectionName,
        sectionWithClauses,
      );
      if (!replaced) {
        // replaceSection 失败，降级为整体追加
        updatedContent = pureContent + '\n\n' + sectionWithClauses;
        warnings.push(`章节 "${sectionName}" 替换失败，已追加到文书末尾`);
      } else {
        updatedContent = content;
      }
    } else {
      // 原文书中无此章节，追加到末尾
      updatedContent = pureContent + '\n\n' + sectionWithClauses;
    }

    // 重新注入完整文书的 disclaimer
    const { content: reportWithDisclaimer } = injectDisclaimer(
      updatedContent,
      {
        format:    'markdown',
        skillName: '文书助手',
        modelName: chatResult.provider || chatResult.model,
      },
    );

    // 写入审计日志
    await _safeAppendAuditLog(storage, {
      event:              'section_regenerated',
      org_name:           input.org_name,
      document_type:      input.document_type,
      document_subtype:   input.document_subtype,
      section_name:       sectionName,
      model_used:         chatResult.model,
      provider:           chatResult.provider,
      degraded:           chatResult.degraded,
      success:            true,
      duration_ms:        durationMs,
      fixed_clause_count: fixedClauses.length,
    });

    // 写入历史
    await _safeAppendHistory(storage, SKILL_ID, {
      org_name:         input.org_name,
      document_type:    input.document_type,
      document_subtype: input.document_subtype,
      section_name:     sectionName,
      timestamp:        new Date().toISOString(),
      model_used:       chatResult.model,
      provider:         chatResult.provider,
      success:          true,
      duration_ms:      durationMs,
    });

    return {
      success: true,
      report:  reportWithDisclaimer,
      metadata: {
        model:            chatResult.model,
        provider:         chatResult.provider,
        degraded:         chatResult.degraded,
        duration_ms:      durationMs,
        version:          SKILL_VERSION,
        fixedClauseCount: fixedClauses.length,
      },
      warnings,
    };

  } catch (err) {
    const durationMs = Date.now() - startTime;

    await _safeAppendAuditLog(storage, {
      event:          'section_regenerated',
      org_name:       input.org_name,
      document_type:  input.document_type,
      document_subtype: input.document_subtype,
      section_name:   sectionName,
      model_used:     null,
      success:        false,
      duration_ms:    durationMs,
      error_type:     err.name || 'Error',
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
    console.error('[document-assistant] 审计日志写入失败（非阻断）:', err.message);
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
    console.error('[document-assistant] 历史记录写入失败（非阻断）:', err.message);
  }
}

// ---------------------------------------------------------------------------
// 导出
// ---------------------------------------------------------------------------

module.exports = {
  handleDocument,
  regenerateSection,
  getMaxTokens,
};
