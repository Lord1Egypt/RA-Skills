/**
 * mofang_list_forms — 列出空间下所有表单
 * 接受 spaceHint（自然语言空间名），内部自动解析为 spaceId
 */
import { apiRequest } from './utils/http-client.js';
import { resolveSpace } from './utils/resolve.js';
function buildConfig(context) {
    return {
        baseUrl: context.config.BASE_URL,
        username: context.config.USERNAME,
        password: context.config.PASSWORD,
    };
}
function extractForms(data) {
    const entries = data?.feed?.entry;
    if (!Array.isArray(entries))
        return [];
    return entries.map((entry) => ({
        label: entry.content?.form?.label || '',
        id: entry.id,
        updated: entry.updated,
        version: entry.content?.form?.version,
    }));
}
export async function handler(params, context) {
    const config = buildConfig(context);
    if (!config.baseUrl) {
        return { success: false, message: '未配置 BASE_URL。' };
    }
    let spaceId;
    let spaceLabel;
    if (params.spaceHint) {
        const resolved = await resolveSpace(config, params.spaceHint);
        if (!resolved.success || !resolved.spaceId) {
            return { success: false, message: resolved.message };
        }
        spaceId = resolved.spaceId;
        spaceLabel = resolved.spaceLabel;
    }
    else {
        // 尝试用最近使用的空间
        const { getLastSpace } = await import('./utils/cache.js');
        const last = await getLastSpace(config.baseUrl);
        if (!last) {
            return { success: false, message: '未指定空间且无最近使用记录。请提供 spaceHint 参数。' };
        }
        spaceId = last.spaceId;
        spaceLabel = last.spaceLabel;
    }
    const path = `/magicflu/service/s/json/${spaceId}/forms/feed?start=0&limit=-1`;
    const result = await apiRequest(config, 'GET', path);
    if (!result.success) {
        return { success: false, message: `表单列表查询失败: ${result.message}` };
    }
    const forms = extractForms(result.data);
    if (forms.length === 0) {
        return { success: true, message: `空间「${spaceLabel || spaceId}」下没有表单。`, data: [], spaceLabel };
    }
    return {
        success: true,
        message: `空间「${spaceLabel || spaceId}」下找到 ${forms.length} 个表单。`,
        data: forms,
        spaceLabel,
    };
}
//# sourceMappingURL=forms.js.map