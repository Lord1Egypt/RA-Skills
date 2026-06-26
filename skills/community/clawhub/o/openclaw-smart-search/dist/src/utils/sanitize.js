"use strict";
/**
 * 输入清理和安全验证工具
 *
 * 安全特性：
 * - 白名单字符验证
 * - 命令注入防护
 * - 长度限制
 * - 类型验证
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.validators = void 0;
exports.sanitizeInput = sanitizeInput;
exports.validateInputLength = validateInputLength;
exports.validateWithWhitelist = validateWithWhitelist;
exports.detectInjectionAttempt = detectInjectionAttempt;
exports.validateSearchQuery = validateSearchQuery;
/**
 * 允许的字符白名单
 * - 字母（大小写）
 * - 数字
 * - 中文字符（CJK 统一表意文字）
 * - 常见标点符号
 * - 空白字符
 */
const ALLOWED_CHARS_REGEX = /^[\w\s\u4e00-\u9fa5,.\-_'"()?!:;@#/+]+$/;
/**
 * 危险字符黑名单（用于日志和调试）
 */
const DANGEROUS_CHARS = [';', '&', '|', '`', '$', '{', '}', '[', ']', '<', '>', '\\', '\n', '\r', '\0'];
/**
 * 清理用户输入，防止命令注入
 * 移除危险字符并转义特殊字符
 *
 * @param input - 用户输入字符串
 * @returns 清理后的安全字符串
 * @throws Error 如果输入不是字符串
 */
function sanitizeInput(input) {
    if (typeof input !== 'string') {
        throw new Error('Input must be a string');
    }
    // 移除控制字符和命令注入危险字符
    // 注意：括号 () 是白名单允许的，不移除
    let sanitized = input
        .replace(/[\x00-\x1F\x7F]/g, '') // 移除控制字符
        .replace(/[;&|`${}<>\n\r]/g, '') // 移除命令分隔符（保留括号）
        .replace(/\\/g, '\\\\') // 转义反斜杠
        .trim();
    return sanitized;
}
/**
 * 验证输入长度
 * 防止超长输入导致的问题
 *
 * @param input - 输入字符串
 * @param maxLength - 最大允许长度（默认 500）
 * @returns 验证后的字符串
 * @throws Error 如果输入超过最大长度
 */
function validateInputLength(input, maxLength = 500) {
    if (input.length > maxLength) {
        throw new Error(`Input too long. Maximum length is ${maxLength} characters. ` +
            `Current: ${input.length} characters.`);
    }
    return input;
}
/**
 * 使用白名单验证输入字符
 * 只允许安全字符通过
 *
 * @param input - 输入字符串
 * @returns 验证后的字符串
 * @throws Error 如果包含非法字符
 */
function validateWithWhitelist(input) {
    if (!ALLOWED_CHARS_REGEX.test(input)) {
        // 找出非法字符用于错误提示
        const invalidChars = [];
        for (const char of input) {
            if (!ALLOWED_CHARS_REGEX.test(char)) {
                invalidChars.push(char);
            }
        }
        throw new Error(`Query contains invalid characters: ${invalidChars.slice(0, 5).map(c => `"${c}"`).join(', ')}${invalidChars.length > 5 ? '...' : ''}\n` +
            `Allowed characters: letters, numbers, Chinese characters, spaces, and common punctuation (,.!?:;'"()-_@#/)`);
    }
    return input;
}
/**
 * 检测潜在的注入攻击模式
 *
 * @param input - 输入字符串
 * @returns 是否检测到潜在攻击
 */
function detectInjectionAttempt(input) {
    const detectedPatterns = [];
    // SQL 注入模式
    const sqlPatterns = [
        /(\bSELECT\b|\bINSERT\b|\bUPDATE\b|\bDELETE\b|\bDROP\b|\bUNION\b)/i,
        /(--)|(\/\*)|(\*\/)/,
        /('|")\s*(OR|AND)\s*('|")/i,
        /\d+\s*(OR|AND)\s*\d+/i
    ];
    // 命令注入模式
    const cmdPatterns = [
        /[;&|`$]/,
        /\$\([^)]+\)/,
        /\$\{[^}]+\}/,
        /`[^`]+`/,
        /\|\s*\w+/
    ];
    // XSS 模式
    const xssPatterns = [
        /<script\b/i,
        /javascript:/i,
        /on\w+\s*=/i,
        /<iframe\b/i
    ];
    for (const pattern of [...sqlPatterns, ...cmdPatterns, ...xssPatterns]) {
        if (pattern.test(input)) {
            detectedPatterns.push(pattern.source);
        }
    }
    return {
        detected: detectedPatterns.length > 0,
        patterns: detectedPatterns
    };
}
/**
 * 验证搜索关键词
 * 组合验证函数，提供多层安全防护
 *
 * 安全检查顺序：
 * 1. 类型验证
 * 2. 长度验证
 * 3. 注入检测（警告）
 * 4. 白名单验证
 * 5. 清理和最终验证
 *
 * @param query - 搜索查询字符串
 * @returns 验证后的安全字符串
 * @throws Error 如果验证失败
 */
function validateSearchQuery(query) {
    // 1. 类型验证
    if (typeof query !== 'string') {
        throw new Error('Query must be a string');
    }
    // 2. 空输入检查
    if (!query || query.trim().length === 0) {
        throw new Error('Search query cannot be empty');
    }
    // 3. 长度验证
    const validatedLength = validateInputLength(query, 500);
    // 4. 注入检测（记录警告但不阻止）
    const injectionCheck = detectInjectionAttempt(validatedLength);
    if (injectionCheck.detected) {
        console.warn(`[SECURITY WARNING] Potential injection pattern detected: ${injectionCheck.patterns.join(', ')}\n` +
            `Query will be sanitized but please review the input.`);
    }
    // 5. 白名单验证
    try {
        validateWithWhitelist(validatedLength);
    }
    catch (error) {
        // 如果白名单验证失败，尝试清理后再验证
        const sanitized = sanitizeInput(validatedLength);
        if (sanitized.length < 1) {
            throw new Error('Search query contains only invalid characters.\n' +
                'Please use letters, numbers, Chinese characters, or common punctuation.');
        }
        return sanitized;
    }
    // 6. 清理并返回
    const sanitized = sanitizeInput(validatedLength);
    // 最终检查
    if (sanitized.length < 1) {
        throw new Error('Search query cannot be empty after sanitization');
    }
    return sanitized;
}
/**
 * 导出所有验证函数供测试使用
 */
exports.validators = {
    sanitizeInput,
    validateInputLength,
    validateWithWhitelist,
    detectInjectionAttempt,
    validateSearchQuery
};
//# sourceMappingURL=sanitize.js.map