/**
 * 输入验证工具
 */
export interface ValidationResult {
    valid: boolean;
    error?: string;
}
/**
 * 验证数字人ID
 */
export declare function validateDigitalHumanId(id: string): ValidationResult;
/**
 * 验证用户ID
 */
export declare function validateUserId(id: string): ValidationResult;
/**
 * 验证消息内容
 */
export declare function validateMessage(content: string): ValidationResult;
/**
 * 验证内容类型
 */
export declare function validateContentType(type: string): ValidationResult;
/**
 * 验证 WebSocket URL
 */
export declare function validateWebSocketUrl(url: string): ValidationResult;
/**
 * 验证媒体 URL
 */
export declare function validateMediaUrl(url: string): ValidationResult;
/**
 * 验证语音时长
 */
export declare function validateDuration(duration: number): ValidationResult;
/**
 * 清理字符串（防止 XSS）
 */
export declare function sanitizeString(input: string): string;
//# sourceMappingURL=validator.d.ts.map