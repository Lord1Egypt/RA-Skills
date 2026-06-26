'use strict';

/**
 * 报告助手输出验证脚本
 * 在 SKILL.md 的 scripts/ 中运行，验证生成的报告是否符合规范
 */

/**
 * 验证报告输出是否包含必要章节
 * @param {string} content - 生成的报告内容
 * @param {string[]} requiredSections - 必须包含的章节标题列表
 * @returns {{ valid: boolean, missing: string[] }}
 */
function validateSections(content, requiredSections) {
  const missing = requiredSections.filter(
    (section) => !content.includes(section),
  );
  return { valid: missing.length === 0, missing };
}

/**
 * 验证报告中是否存在未替换的占位符
 * @param {string} content
 * @returns {{ valid: boolean, placeholders: string[] }}
 */
function validatePlaceholders(content) {
  const placeholderPattern = /\[请填写[^\]]*\]/g;
  const found = content.match(placeholderPattern) || [];
  return { valid: found.length === 0, placeholders: found };
}

/**
 * 验证报告是否包含 AI 声明（disclaimer-injector 已注入）
 * @param {string} content
 * @returns {{ valid: boolean, reason?: string }}
 */
function validateDisclaimer(content) {
  if (!content.includes('AI 辅助生成')) {
    return { valid: false, reason: '缺少 AI 辅助生成声明' };
  }
  if (!content.includes('仅供参考')) {
    return { valid: false, reason: '缺少免责提示' };
  }
  return { valid: true };
}

module.exports = { validateSections, validatePlaceholders, validateDisclaimer };
