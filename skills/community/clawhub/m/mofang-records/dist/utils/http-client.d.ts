/**
 * 统一 HTTP 请求封装
 * 负责 Token 管理、请求发送、错误处理和自动重试
 */
export interface TokenInfo {
    token: string;
    obtainedAt: number;
    nickname: string;
    username: string;
    userId: string;
}
export interface HttpClientConfig {
    baseUrl: string;
    username: string;
    password: string;
}
export interface ApiResponse<T = any> {
    success: boolean;
    data?: T;
    message: string;
}
export declare function fetchWithTimeout(url: string, init?: RequestInit): Promise<Response>;
export declare function obtainToken(config: HttpClientConfig): Promise<TokenInfo>;
export declare function getToken(config: HttpClientConfig): Promise<string>;
export declare function clearTokenCache(): void;
export declare function getTokenInfo(): TokenInfo | null;
export declare function apiRequest<T = any>(config: HttpClientConfig, method: string, path: string, body?: any, isRetry?: boolean): Promise<ApiResponse<T>>;
/** URL-Safe Base64，与 Java Base64.encodeBase64URLSafeString(utf8(userId)) 对齐 */
export declare function currentUserDigitalIdCookie(userId: string): string;
/**
 * Activiti / BPM 相关请求：Bearer + Cookie CURRENT_USER_DIGITALID（与前端、Java RESTCaller 一致）。
 * 兼容 204、正文为纯文本 ok、非 JSON。
 */
export declare function bpmRequest(config: HttpClientConfig, method: string, path: string, body?: unknown, extraCookie?: string, isRetry?: boolean): Promise<ApiResponse<any>>;
export type BpmFetchOptions = {
    /** 作为 application/json 发送（对象会 JSON.stringify） */
    jsonBody?: unknown;
    /** 原样作为请求体（已含 Content-Type 时用于空 JSON 体等） */
    textBody?: string;
    extraCookie?: string;
};
/**
 * 与 bpmRequest 相同鉴权，可发 JSON 或原始正文（如 `updateDesc` 的空 body）。
 */
export declare function bpmFetch(config: HttpClientConfig, method: string, path: string, options?: BpmFetchOptions, isRetry?: boolean): Promise<ApiResponse<any>>;
//# sourceMappingURL=http-client.d.ts.map