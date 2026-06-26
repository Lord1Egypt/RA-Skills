/**
 * mofang_test_connection — 健康检查
 * 验证配置是否正确：获取 Token + 列出空间
 */
export declare function handler(_params: object, context: {
    config: Record<string, string>;
}): Promise<{
    success: boolean;
    message: string;
    data?: any;
}>;
//# sourceMappingURL=health.d.ts.map