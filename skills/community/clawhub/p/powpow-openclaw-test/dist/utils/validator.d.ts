/**
 * 输入验证工具
 */
export interface ValidationResult {
    valid: boolean;
    error?: string;
}
export declare function validateUsername(username: string): ValidationResult;
export declare function validateEmail(email: string): ValidationResult;
export declare function validatePassword(password: string): ValidationResult;
export declare function validateMessage(content: string): ValidationResult;
export declare function sanitizeString(input: string): string;
