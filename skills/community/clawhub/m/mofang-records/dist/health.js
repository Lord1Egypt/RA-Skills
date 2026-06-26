/**
 * mofang_test_connection — 健康检查
 * 验证配置是否正确：获取 Token + 列出空间
 */
import { obtainToken, apiRequest } from './utils/http-client.js';
function buildConfig(context) {
    return {
        baseUrl: context.config.BASE_URL,
        username: context.config.USERNAME,
        password: context.config.PASSWORD,
    };
}
export async function handler(_params, context) {
    const config = buildConfig(context);
    const missing = [];
    if (!config.baseUrl)
        missing.push('BASE_URL');
    if (!config.username)
        missing.push('USERNAME');
    if (!config.password)
        missing.push('PASSWORD');
    if (missing.length > 0) {
        return {
            success: false,
            message: `配置缺失: ${missing.join(', ')}。请在 .env 文件或环境变量中设置。`,
        };
    }
    let tokenInfo;
    try {
        tokenInfo = await obtainToken(config);
    }
    catch (err) {
        return {
            success: false,
            message: `Token 获取失败: ${err.message}。请检查 BASE_URL、USERNAME、PASSWORD 是否正确。`,
        };
    }
    const spacesResult = await apiRequest(config, 'GET', '/magicflu/service/json/spaces/feed?start=0&limit=-1');
    const spaceCount = Array.isArray(spacesResult.data?.items)
        ? spacesResult.data.items.length
        : 0;
    return {
        success: true,
        message: '连接成功',
        data: {
            server: config.baseUrl,
            user: tokenInfo.nickname || tokenInfo.username,
            spaceCount,
        },
    };
}
//# sourceMappingURL=health.js.map