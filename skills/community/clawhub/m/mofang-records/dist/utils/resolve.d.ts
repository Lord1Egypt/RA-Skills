/**
 * 空间/表单解析工具
 * 支持缓存别名、最近使用空间、多空间搜索
 * 被各 handler 内部调用，对外部透明
 */
import { type HttpClientConfig } from './http-client.js';
export interface ResolveResult {
    success: boolean;
    message: string;
    spaceId?: string;
    formId?: string;
    spaceLabel?: string;
    formLabel?: string;
}
/**
 * 解析 spaceHint → spaceId（不需要表单）
 */
export declare function resolveSpace(config: HttpClientConfig, spaceHint: string): Promise<ResolveResult>;
/**
 * 解析 formHint + spaceHint? → spaceId + formId
 * 策略: 缓存别名 → 指定空间查找 → 最近使用空间 → 多空间遍历
 */
export declare function resolveSpaceForm(config: HttpClientConfig, formHint: string, spaceHint?: string): Promise<ResolveResult>;
//# sourceMappingURL=resolve.d.ts.map