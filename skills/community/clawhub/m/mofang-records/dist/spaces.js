/**
 * mofang_list_spaces — 列出所有空间
 */
import { apiRequest } from './utils/http-client.js';
function buildConfig(context) {
    return {
        baseUrl: context.config.BASE_URL,
        username: context.config.USERNAME,
        password: context.config.PASSWORD,
    };
}
function extractSpaces(data) {
    const items = data?.items;
    if (!Array.isArray(items))
        return [];
    return items.map((item) => ({
        label: item.label,
        id: item.id,
    }));
}
async function fetchSpacePage(config, start, limit, bq) {
    let path = `/magicflu/service/json/spaces/feed?start=${start}&limit=${limit}`;
    if (bq)
        path += `&bq=${encodeURIComponent(bq)}`;
    const result = await apiRequest(config, 'GET', path);
    if (!result.success) {
        return { success: false, message: result.message, spaces: [] };
    }
    return { success: true, message: 'ok', spaces: extractSpaces(result.data) };
}
async function fetchSpacesByCreatedDesc(config, start, limit) {
    return fetchSpacePage(config, start, limit, '(created,orderby,desc)');
}
export async function handler(params, context) {
    const config = buildConfig(context);
    if (!config.baseUrl) {
        return { success: false, message: '未配置 BASE_URL，请先设置魔方网表服务器地址。' };
    }
    const q = (params.spaceHint || params.q || '').trim();
    const page = params.page ?? 1;
    const pageSize = Math.min(Math.max(params.pageSize ?? 100, 1), 100);
    if (q) {
        const exact = await fetchSpacePage(config, 0, pageSize, `(label,eq,${q})`);
        if (!exact.success) {
            return { success: false, message: `空间搜索失败: ${exact.message}` };
        }
        let spaces = exact.spaces;
        if (spaces.length === 0) {
            const fuzzy = await fetchSpacePage(config, 0, pageSize, `(label,like_and,${q})`);
            if (!fuzzy.success) {
                return { success: false, message: `空间搜索失败: ${fuzzy.message}` };
            }
            spaces = fuzzy.spaces;
        }
        return {
            success: true,
            message: `搜索「${q}」找到 ${spaces.length} 个空间。`,
            data: spaces,
        };
    }
    const useAll = params.all !== false;
    const start = useAll ? 0 : (page - 1) * pageSize;
    const limit = useAll ? -1 : pageSize;
    const result = await fetchSpacesByCreatedDesc(config, start, limit);
    if (!result.success) {
        return { success: false, message: `空间列表查询失败: ${result.message}` };
    }
    const spaces = result.spaces;
    return {
        success: true,
        message: useAll ? `找到 ${spaces.length} 个空间。` : `找到 ${spaces.length} 个空间（第 ${page} 页）。`,
        data: spaces,
    };
}
//# sourceMappingURL=spaces.js.map