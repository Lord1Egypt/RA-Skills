'use strict';

// ---------------------------------------------------------------------------
// index.js — 申报助手 Skill 主工作流入口
//
// 依赖：仅 Node.js 内置模块（通过共享包间接使用 fs）
// 合规依据：噗滋慈善申报助手 Spec v1.0 + charity CLAUDE.md 合规红线
//   - PII 不入模型（model-gateway 内置前置过滤，index.js 不再直接调用 pii-filter）
//   - AI 标识声明强制注入（disclaimer-injector）
//   - 强制占位符替换（enforcePlaceholders）：防止 AI 编造证书编号/预算金额
//   - 审计日志不含 prompt 正文和生成内容（合规红线第2条）
//   - 日志保留 ≥6 个月（由 storage-adapter 强制）
// ---------------------------------------------------------------------------

const { injectDisclaimer }    = require('../../../packages/shared/disclaimer-injector');
const { validate }            = require('./validators');
const promptBuilder           = require('./prompt-builder');

// 占位符强制执行（独立模块，申报助手特有后处理步骤）
const { enforcePlaceholders } = require('./placeholder-enforcer');

// ---------------------------------------------------------------------------
// Skill 元数据
// ---------------------------------------------------------------------------

/** Skill ID — 用于 storage.appendHistory 的分区键 */
const SKILL_ID = 'application-assistant';

/** Skill 当前版本 */
const SKILL_VERSION = '1.0.0';

// ---------------------------------------------------------------------------
// maxTokens 配置表（对应 Spec Step 5）
// ---------------------------------------------------------------------------

/**
 * 申报类型 → maxTokens 映射
 * @type {Record<string, number>}
 */
const MAX_TOKENS_MAP = {
  generic:       5000,
  tencent99:     4000,
  govt_purchase: 5000,
};

// ---------------------------------------------------------------------------
// 工具函数
// ---------------------------------------------------------------------------

/**
 * 根据申报类型返回 maxTokens
 *
 * @param {string} applicationType - 'generic' | 'tencent99' | 'govt_purchase'
 * @returns {number} maxTokens；未知类型返回 5000（默认）
 */
function getMaxTokens(applicationType) {
  return MAX_TOKENS_MAP[applicationType] || 5000;
}

/**
 * 从包含多个章节的 Markdown 申报书中提取指定章节的内容
 *
 * 策略：匹配以 "## <sectionName>" 开头的段落，
 * 直到下一个同级或更高级标题（## / #）或文档结束。
 *
 * @param {string} reportContent - 完整 Markdown 申报书正文
 * @param {string} sectionName   - 目标章节名（不含 "## " 前缀）
 * @returns {{ found: boolean, content: string, startIndex: number, endIndex: number }}
 */
function extractSection(reportContent, sectionName) {
  // 兼容带/不带序号前缀的章节标题，例如 "一、机构基本信息" 或 "机构基本信息"
  const headingPattern = new RegExp(
    `^#{1,3}\\s+[^\\n]*${escapeRegex(sectionName)}[^\\n]*$`,
    'm',
  );
  const match = headingPattern.exec(reportContent);

  if (!match) {
    return { found: false, content: '', startIndex: -1, endIndex: -1 };
  }

  const startIndex = match.index;

  // 找到下一个同级或更高级 heading（## 或 #，不含 ###）
  const afterMatch = reportContent.slice(startIndex + match[0].length);
  const nextHeadingPattern = /^#{1,2}\s+/m;
  const nextMatch = nextHeadingPattern.exec(afterMatch);

  const endIndex = nextMatch !== null
    ? startIndex + match[0].length + nextMatch.index
    : reportContent.length;

  return {
    found: true,
    content: reportContent.slice(startIndex, endIndex),
    startIndex,
    endIndex,
  };
}

/**
 * 将新章节内容替换到原始申报书的对应位置
 *
 * @param {string} reportContent     - 完整申报书（已去除 disclaimer）
 * @param {string} sectionName       - 目标章节名
 * @param {string} newSectionContent - 新章节内容（已包含标题行）
 * @returns {{ success: boolean, content: string }}
 */
function replaceSection(reportContent, sectionName, newSectionContent) {
  const { found, startIndex, endIndex } = extractSection(reportContent, sectionName);

  if (!found) {
    return { success: false, content: reportContent };
  }

  const updated =
    reportContent.slice(0, startIndex) +
    newSectionContent.trimEnd() +
    '\n' +
    reportContent.slice(endIndex);

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
 * 从已注入 disclaimer 的完整申报书中剥离声明部分，返回纯内容
 *
 * disclaimer-injector 注入格式为：
 *   <headerText>\n\n<content>\n\n<footerText>
 *
 * 剥离策略：
 *   - 找到第一个 "\n\n" 后的内容作为正文起点
 *   - 找到最后一个 "\n\n---\n" 之前的内容作为正文终点（markdown footer 以 "---" 开头）
 *
 * @param {string} reportWithDisclaimer
 * @returns {string} 纯申报书内容（不含 disclaimer）
 */
function stripDisclaimer(reportWithDisclaimer) {
  const firstSep = reportWithDisclaimer.indexOf('\n\n');
  if (firstSep === -1) return reportWithDisclaimer;

  const bodyStart = firstSep + 2;

  // markdown footer 以 "\n\n---\n" 开头
  const footerSep = reportWithDisclaimer.lastIndexOf('\n\n---\n');
  if (footerSep === -1 || footerSep <= bodyStart) {
    // 没有找到 footer，返回从 bodyStart 到结尾
    return reportWithDisclaimer.slice(bodyStart);
  }

  return reportWithDisclaimer.slice(bodyStart, footerSep);
}

// ---------------------------------------------------------------------------
// 主工作流
// ---------------------------------------------------------------------------

/**
 * 主工作流入口（对应 Spec Step 1-8）
 *
 * 申报助手特有步骤：在 disclaimer 注入前执行 enforcePlaceholders，
 * 将模型疑似编造的证书编号/文件编号替换为强制占位符。
 *
 * @param {object} input   - 用户输入对象（含 application_type、org_name 等字段）
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
 *     placeholderCount: number,
 *     placeholders: Array<{original: string, replacement: string, position: number}>
 *   },
 *   warnings?: string[],
 *   errors?: string[]
 * }>}
 */
async function handleApplication(input, options = {}) {
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
    // Step 4: Prompt 构建（Spec Step 4）
    // -------------------------------------------------------------------
    const messages = promptBuilder.buildPrompt(input, modelType);

    // -------------------------------------------------------------------
    // Step 5: 模型调用（Spec Step 5）
    // PII 前置过滤由 model-gateway 内置，此处不重复调用 pii-filter
    // temperature: 0.5（申报书需适度叙事流畅性，高于报告助手的 0.3）
    // -------------------------------------------------------------------
    const maxTokens = getMaxTokens(input.application_type);
    const chatResult = await modelClient.chat(messages, {
      temperature: 0.5,
      maxTokens,
    });

    const durationMs = Date.now() - startTime;

    // -------------------------------------------------------------------
    // Step 6a: 申报助手特有 — 强制占位符替换（Spec Step 6 / 合规红线第8条）
    // 在 disclaimer 注入前执行，防止 AI 编造的证书编号/文件编号进入最终输出
    // -------------------------------------------------------------------
    const enforceResult = enforcePlaceholders(chatResult.content, input);
    const processedContent = enforceResult.text;

    if (enforceResult.count > 0) {
      warnings.push(
        `已自动替换 ${enforceResult.count} 处疑似 AI 编造的编号/格式（占位符强制执行），请在提交前手动填写。`,
      );
    }

    // -------------------------------------------------------------------
    // Step 6b: 注入 AI 标识声明 + 免责提示（合规红线 P0）
    // -------------------------------------------------------------------
    const { content: reportWithDisclaimer } = injectDisclaimer(
      processedContent,
      {
        format:    'markdown',
        skillName: '申报助手',
        modelName: chatResult.provider || chatResult.model,
      },
    );

    // -------------------------------------------------------------------
    // Step 6c: 写入审计日志（不含 prompt 正文和生成内容）
    // 申报助手额外记录 placeholder_count
    // -------------------------------------------------------------------
    await _safeAppendAuditLog(storage, {
      event:             'application_generated',
      org_name:          input.org_name,
      application_type:  input.application_type,
      model_used:        chatResult.model,
      provider:          chatResult.provider,
      degraded:          chatResult.degraded,
      success:           true,
      duration_ms:       durationMs,
      placeholder_count: enforceResult.count,
    });

    // Step 6d: 写入生成历史
    await _safeAppendHistory(storage, SKILL_ID, {
      org_name:         input.org_name,
      application_type: input.application_type,
      timestamp:        new Date().toISOString(),
      model_used:       chatResult.model,
      provider:         chatResult.provider,
      success:          true,
      duration_ms:      durationMs,
    });

    // -------------------------------------------------------------------
    // 返回结果（Spec Step 7 的上下文在此处作为 metadata 透出）
    // -------------------------------------------------------------------
    return {
      success: true,
      report:  reportWithDisclaimer,
      metadata: {
        model:            chatResult.model,
        provider:         chatResult.provider,
        degraded:         chatResult.degraded,
        duration_ms:      durationMs,
        version:          SKILL_VERSION,
        placeholderCount: enforceResult.count,
        placeholders:     enforceResult.replacements,
      },
      warnings,
    };

  } catch (err) {
    const durationMs = Date.now() - startTime;

    // 模型调用失败（含 PII 阻断）— 写审计日志后向上透出
    await _safeAppendAuditLog(storage, {
      event:            'application_generated',
      org_name:         input.org_name,
      application_type: input.application_type,
      model_used:       null,
      success:          false,
      duration_ms:      durationMs,
      error_type:       err.name || 'Error',
    });

    return {
      success: false,
      errors:  [err.message],
      warnings,
    };
  }
}

// ---------------------------------------------------------------------------
// 单章节重生成（Spec Step 8）
// ---------------------------------------------------------------------------

/**
 * 对指定章节重新调用模型生成，并合并回完整申报书
 *
 * @param {object} input           - 原始用户输入对象（与 handleApplication 相同结构）
 * @param {string} sectionName     - 目标章节名（如 "机构基本信息"）
 * @param {string} previousReport  - 上一次 handleApplication 返回的带 disclaimer 完整申报书
 * @param {object} options         - 同 handleApplication options
 * @returns {Promise<{
 *   success: boolean,
 *   report?: string,
 *   metadata?: {
 *     model: string,
 *     provider: string,
 *     degraded: boolean,
 *     duration_ms: number,
 *     version: string,
 *     placeholderCount: number,
 *     placeholders: Array<{original: string, replacement: string, position: number}>
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

  // 同 handleApplication 一样先校验输入（合规必经）
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
    // 从完整申报书中剥离 disclaimer，得到纯内容
    const pureContent = stripDisclaimer(previousReport);

    // 检查目标章节是否存在
    const { found: sectionFound } = extractSection(pureContent, sectionName);
    if (!sectionFound) {
      warnings.push(
        `章节 "${sectionName}" 在原申报书中未找到，将生成新章节并附加到申报书末尾`,
      );
    }

    // 构建章节重生成专用 prompt（沿用 buildPrompt，传入 sectionName 提示模型只生成指定章节）
    const messages = promptBuilder.buildPrompt(
      { ...input, _regenerate_section: sectionName },
      modelType,
    );

    // 只对该章节调用模型（token 预算减少为全量的 1/3）
    const maxTokens = Math.ceil(getMaxTokens(input.application_type) / 3);
    const chatResult = await modelClient.chat(messages, {
      temperature: 0.5,
      maxTokens,
    });

    const durationMs = Date.now() - startTime;

    // -------------------------------------------------------------------
    // 申报助手特有：对重生成章节也执行 enforcePlaceholders
    // -------------------------------------------------------------------
    const enforceResult = enforcePlaceholders(chatResult.content, input);
    const processedSectionContent = enforceResult.text;

    if (enforceResult.count > 0) {
      warnings.push(
        `已自动替换 ${enforceResult.count} 处疑似 AI 编造的编号/格式（占位符强制执行），请在提交前手动填写。`,
      );
    }

    // 将新章节内容合并回原始纯申报书
    let updatedContent;
    if (sectionFound) {
      const { success: replaced, content } = replaceSection(
        pureContent,
        sectionName,
        processedSectionContent,
      );
      if (!replaced) {
        // replaceSection 失败，降级为整体追加
        updatedContent = pureContent + '\n\n' + processedSectionContent;
        warnings.push(`章节 "${sectionName}" 替换失败，已追加到申报书末尾`);
      } else {
        updatedContent = content;
      }
    } else {
      // 原申报书中无此章节，追加到末尾
      updatedContent = pureContent + '\n\n' + processedSectionContent;
    }

    // 重新注入完整申报书的 disclaimer
    const { content: reportWithDisclaimer } = injectDisclaimer(
      updatedContent,
      {
        format:    'markdown',
        skillName: '申报助手',
        modelName: chatResult.provider || chatResult.model,
      },
    );

    // 写入审计日志
    await _safeAppendAuditLog(storage, {
      event:             'section_regenerated',
      org_name:          input.org_name,
      application_type:  input.application_type,
      section_name:      sectionName,
      model_used:        chatResult.model,
      provider:          chatResult.provider,
      degraded:          chatResult.degraded,
      success:           true,
      duration_ms:       durationMs,
      placeholder_count: enforceResult.count,
    });

    // 写入历史
    await _safeAppendHistory(storage, SKILL_ID, {
      org_name:         input.org_name,
      application_type: input.application_type,
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
        placeholderCount: enforceResult.count,
        placeholders:     enforceResult.replacements,
      },
      warnings,
    };

  } catch (err) {
    const durationMs = Date.now() - startTime;

    await _safeAppendAuditLog(storage, {
      event:            'section_regenerated',
      org_name:         input.org_name,
      application_type: input.application_type,
      section_name:     sectionName,
      model_used:       null,
      success:          false,
      duration_ms:      durationMs,
      error_type:       err.name || 'Error',
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
    console.error('[application-assistant] 审计日志写入失败（非阻断）:', err.message);
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
    console.error('[application-assistant] 历史记录写入失败（非阻断）:', err.message);
  }
}

// ---------------------------------------------------------------------------
// 导出
// ---------------------------------------------------------------------------

module.exports = {
  handleApplication,
  regenerateSection,
  getMaxTokens,
};
