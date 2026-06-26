/**
 * 输入清理和安全验证工具
 *
 * 安全特性：
 * - 白名单字符验证
 * - 命令注入防护
 * - 长度限制
 * - 类型验证
 */
/**
 * 清理用户输入，防止命令注入
 * 移除危险字符并转义特殊字符
 *
 * @param input - 用户输入字符串
 * @returns 清理后的安全字符串
 * @throws Error 如果输入不是字符串
 */
export declare function sanitizeInput(input: string): string;
/**
 * 验证输入长度
 * 防止超长输入导致的问题
 *
 * @param input - 输入字符串
 * @param maxLength - 最大允许长度（默认 500）
 * @returns 验证后的字符串
 * @throws Error 如果输入超过最大长度
 */
export declare function validateInputLength(input: string, maxLength?: number): string;
/**
 * 使用白名单验证输入字符
 * 只允许安全字符通过
 *
 * @param input - 输入字符串
 * @returns 验证后的字符串
 * @throws Error 如果包含非法字符
 */
export declare function validateWithWhitelist(input: string): string;
/**
 * 检测潜在的注入攻击模式
 *
 * @param input - 输入字符串
 * @returns 是否检测到潜在攻击
 */
export declare function detectInjectionAttempt(input: string): {
    detected: boolean;
    patterns: string[];
};
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
export declare function validateSearchQuery(query: string): string;
/**
 * 导出所有验证函数供测试使用
 */
export declare const validators: {
    sanitizeInput: typeof sanitizeInput;
    validateInputLength: typeof validateInputLength;
    validateWithWhitelist: typeof validateWithWhitelist;
    detectInjectionAttempt: typeof detectInjectionAttempt;
    validateSearchQuery: typeof validateSearchQuery;
};
//# sourceMappingURL=sanitize.d.ts.map