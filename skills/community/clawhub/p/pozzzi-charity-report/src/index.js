'use strict';

// ---------------------------------------------------------------------------
// index.js — 报告助手 Skill 主工作流入口
//
// 依赖：仅 Node.js 内置模块（通过共享包间接使用 fs）
// 合规依据：噗滋慈善 Spec v1.0 + charity CLAUDE.md 合规红线
//   - PII 不入模型（model-gateway 内置前置过滤，index.js 不再直接调用 pii-filter）
//   - AI 标识声明强制注入（disclaimer-injector）
//   - 审计日志不含 prompt 正文和生成内容（合规红线第2条）
//   - 日志保留 ≥6 个月（由 storage-adapter 强制）
// ---------------------------------------------------------------------------

const { injectDisclaimer }  = require('../../../packages/shared/disclaimer-injector');
const { validate }          = require('./validators');
const promptBuilder         = require('./prompt-builder');

// ---------------------------------------------------------------------------
// Skill 元数据
// ---------------------------------------------------------------------------

/** Skill ID — 用于 storage.appendHistory 的分区键 */
const SKILL_ID = 'report-assistant';

/** Skill 当前版本 */
const SKILL_VERSION = '1.0.0';

// ---------------------------------------------------------------------------
// maxTokens 配置表（对应 Spec Step 5）
// ---------------------------------------------------------------------------

/**
 * 报告类型 → maxTokens 映射
 * @type {Record<string, number>}
 */
const MAX_TOKENS_MAP = {
  annual_work:   4000,
  project_final: 3000,
  finance_final: 2000,
};

// ---------------------------------------------------------------------------
// 工具函数
// ---------------------------------------------------------------------------

/**
 * 根据报告类型返回 maxTokens
 *
 * @param {string} reportType - 'annual_work' | 'project_final' | 'finance_final'
 * @returns {number} maxTokens；未知类型返回 3000（默认）
 */
function getMaxTokens(reportType) {
  return MAX_TOKENS_MAP[reportType] || 3000;
}

/**
 * 从包含多个章节的 Markdown 报告中提取指定章节的内容
 *
 * 策略：匹配以 "## <sectionName>" 开头的段落，
 * 直到下一个同级或更高级标题（## / #）或文档结束。
 *
 * @param {string} reportContent - 完整 Markdown 报告正文
 * @param {string} sectionName   - 目标章节名（不含 "## " 前缀）
 * @returns {{ found: boolean, content: string, startIndex: number, endIndex: number }}
 */
function extractSection(reportContent, sectionName) {
  // 兼容带/不带序号前缀的章节标题，例如 "一、工作概述" 或 "工作概述"
  // 使用 multiline 模式，^ 匹配每一行开头
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
 * 将新章节内容替换到原始报告的对应位置
 *
 * @param {string} reportContent    - 完整报告（已去除 disclaimer）
 * @param {string} sectionName      - 目标章节名
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
 * 从已注入 disclaimer 的完整报告中剥离声明部分，返回纯内容
 *
 * disclaimer-injector 注入格式为：
 *   <headerText>\n\n<content>\n\n<footerText>
 *
 * 剥离策略：
 *   - 找到第一个 "\n\n" 后的内容作为正文起点
 *   - 找到最后一个 "\n\n---\n" 之前的内容作为正文终点（markdown footer 以 "---" 开头）
 *
 * @param {string} reportWithDisclaimer
 * @returns {string} 纯报告内容（不含 disclaimer）
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
 * @param {object} input   - 用户输入对象（含 report_type、org_name 等字段）
 * @param {object} options - 配置对象
 * @param {object} options.modelClient  - model-gateway ModelClient 实例（依赖注入）
 * @param {object} options.storage      - storage-adapter 实例（依赖注入）
 * @param {string} [options.modelType='hunyuan'] - 模型类型字符串，传给 promptBuilder
 * @returns {Promise<{
 *   success: boolean,
 *   report?: string,
 *   metadata?: { model: string, provider: string, degraded: boolean, duration_ms: number, version: string },
 *   warnings?: string[],
 *   errors?: string[]
 * }>}
 */
async function handleReport(input, options = {}) {
  const { modelClient, storage, modelType = 'hunyuan' } = options;

  // -------------------------------------------------------------------
  // Step 3: 输入校验（Spec Step 1-3）
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
    // -------------------------------------------------------------------
    const maxTokens = getMaxTokens(input.report_type);
    const chatResult = await modelClient.chat(messages, {
      temperature: 0.3,
      maxTokens,
    });

    const durationMs = Date.now() - startTime;

    // -------------------------------------------------------------------
    // Step 6: 输出后处理（Spec Step 6）
    // a. 注入 AI 标识声明 + 免责提示（合规红线 P0）
    // -------------------------------------------------------------------
    const { content: reportWithDisclaimer } = injectDisclaimer(
      chatResult.content,
      {
        format:    'markdown',
        skillName: '报告助手',
        modelName: chatResult.provider || chatResult.model,
      },
    );

    // b. 写入审计日志（不含 prompt 正文和生成内容）
    await _safeAppendAuditLog(storage, {
      event:       'report_generated',
      org_name:    input.org_name,
      report_type: input.report_type,
      model_used:  chatResult.model,
      provider:    chatResult.provider,
      degraded:    chatResult.degraded,
      success:     true,
      duration_ms: durationMs,
    });

    // c. 写入生成历史
    await _safeAppendHistory(storage, SKILL_ID, {
      org_name:    input.org_name,
      report_type: input.report_type,
      timestamp:   new Date().toISOString(),
      model_used:  chatResult.model,
      provider:    chatResult.provider,
      success:     true,
      duration_ms: durationMs,
    });

    // -------------------------------------------------------------------
    // 返回结果（Spec Step 7 的上下文在此处作为 metadata 透出）
    // -------------------------------------------------------------------
    return {
      success:  true,
      report:   reportWithDisclaimer,
      metadata: {
        model:       chatResult.model,
        provider:    chatResult.provider,
        degraded:    chatResult.degraded,
        duration_ms: durationMs,
        version:     SKILL_VERSION,
      },
      warnings,
    };

  } catch (err) {
    const durationMs = Date.now() - startTime;

    // 模型调用失败（含 PII 阻断）— 写审计日志后向上透出
    await _safeAppendAuditLog(storage, {
      event:       'report_generated',
      org_name:    input.org_name,
      report_type: input.report_type,
      model_used:  null,
      success:     false,
      duration_ms: durationMs,
      error_type:  err.name || 'Error',
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
 * 对指定章节重新调用模型生成，并合并回完整报告
 *
 * @param {object} input           - 原始用户输入对象（与 handleReport 相同结构）
 * @param {string} sectionName     - 目标章节名（如 "年度工作概述"）
 * @param {string} previousReport  - 上一次 handleReport 返回的带 disclaimer 完整报告
 * @param {object} options         - 同 handleReport options
 * @returns {Promise<{
 *   success: boolean,
 *   report?: string,
 *   metadata?: { model: string, provider: string, degraded: boolean, duration_ms: number, version: string },
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
    return { success: false, errors: [`previousReport 超过最大长度限制（${MAX_REPORT_LENGTH} 字符）`] };
  }

  // 同 handleReport 一样先校验输入（合规必经）
  const validationResult = validate(input);
  if (!validationResult.valid) {
    return { success: false, errors: validationResult.errors, warnings: validationResult.warnings };
  }

  const warnings = validationResult.warnings.slice();
  const startTime = Date.now();

  try {
    // 从完整报告中剥离 disclaimer，得到纯内容
    const pureContent = stripDisclaimer(previousReport);

    // 检查目标章节是否存在
    const { found: sectionFound } = extractSection(pureContent, sectionName);
    if (!sectionFound) {
      warnings.push(`章节 "${sectionName}" 在原报告中未找到，将生成新章节并附加到报告末尾`);
    }

    // 构建章节重生成专用 prompt（沿用 buildPrompt，传入 sectionName 提示模型只生成指定章节）
    const messages = promptBuilder.buildPrompt(
      { ...input, _regenerate_section: sectionName },
      modelType,
    );

    // 只对该章节调用模型
    const maxTokens = Math.ceil(getMaxTokens(input.report_type) / 3);
    const chatResult = await modelClient.chat(messages, {
      temperature: 0.3,
      maxTokens,
    });

    const durationMs = Date.now() - startTime;

    // 将新章节内容合并回原始纯报告
    let updatedContent;
    if (sectionFound) {
      const { success: replaced, content } = replaceSection(
        pureContent,
        sectionName,
        chatResult.content,
      );
      if (!replaced) {
        // replaceSection 失败，降级为整体追加
        updatedContent = pureContent + '\n\n' + chatResult.content;
        warnings.push(`章节 "${sectionName}" 替换失败，已追加到报告末尾`);
      } else {
        updatedContent = content;
      }
    } else {
      // 原报告中无此章节，追加到末尾
      updatedContent = pureContent + '\n\n' + chatResult.content;
    }

    // 重新注入完整报告的 disclaimer
    const { content: reportWithDisclaimer } = injectDisclaimer(
      updatedContent,
      {
        format:    'markdown',
        skillName: '报告助手',
        modelName: chatResult.provider || chatResult.model,
      },
    );

    // 写入审计日志
    await _safeAppendAuditLog(storage, {
      event:        'section_regenerated',
      org_name:     input.org_name,
      report_type:  input.report_type,
      section_name: sectionName,
      model_used:   chatResult.model,
      provider:     chatResult.provider,
      degraded:     chatResult.degraded,
      success:      true,
      duration_ms:  durationMs,
    });

    // 写入历史
    await _safeAppendHistory(storage, SKILL_ID, {
      org_name:     input.org_name,
      report_type:  input.report_type,
      section_name: sectionName,
      timestamp:    new Date().toISOString(),
      model_used:   chatResult.model,
      provider:     chatResult.provider,
      success:      true,
      duration_ms:  durationMs,
    });

    return {
      success:  true,
      report:   reportWithDisclaimer,
      metadata: {
        model:       chatResult.model,
        provider:    chatResult.provider,
        degraded:    chatResult.degraded,
        duration_ms: durationMs,
        version:     SKILL_VERSION,
      },
      warnings,
    };

  } catch (err) {
    const durationMs = Date.now() - startTime;

    await _safeAppendAuditLog(storage, {
      event:        'section_regenerated',
      org_name:     input.org_name,
      report_type:  input.report_type,
      section_name: sectionName,
      model_used:   null,
      success:      false,
      duration_ms:  durationMs,
      error_type:   err.name || 'Error',
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
    console.error('[report-assistant] 审计日志写入失败（非阻断）:', err.message);
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
    console.error('[report-assistant] 历史记录写入失败（非阻断）:', err.message);
  }
}

// ---------------------------------------------------------------------------
// 导出
// ---------------------------------------------------------------------------

module.exports = {
  handleReport,
  regenerateSection,
  getMaxTokens,
};
