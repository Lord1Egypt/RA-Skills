/**
 * Memory-Master 敏感数据过滤模块
 *
 * 支持 16 种敏感数据类型检测
 * 基于 Anthropic 安全最佳实践
 */
/**
 * 敏感数据类型
 */
export type SensitiveType = 'api_key' | 'password' | 'credit_card' | 'id_card' | 'phone' | 'email' | 'bank_card' | 'address' | 'private_key' | 'database_url' | 'aws_key' | 'github_token' | 'openai_key' | 'anthropic_key' | 'aliyun_key' | 'other';
/**
 * 检测结果
 */
export interface DetectedSensitive {
    type: SensitiveType;
    value: string;
    position: number;
    original: string;
}
/**
 * 过滤结果
 */
export interface FilterResult {
    hasSensitive: boolean;
    filtered: string;
    detected: DetectedSensitive[];
}
/**
 * 过滤敏感数据
 */
export declare function filterSensitiveData(content: string): Promise<FilterResult>;
/**
 * 检测敏感数据（不替换）
 */
export declare function detectSensitiveData(content: string): Promise<DetectedSensitive[]>;
/**
 * 测试用例
 */
export declare function runFilterTests(): Promise<void>;
declare const _default: {
    filterSensitiveData: typeof filterSensitiveData;
    detectSensitiveData: typeof detectSensitiveData;
    runFilterTests: typeof runFilterTests;
};
export default _default;
