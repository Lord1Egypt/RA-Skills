/**
 * mofang_query_records — 查询记录
 * mofang_create_record — 创建记录
 * mofang_update_record — 修改记录
 * mofang_delete_record — 删除记录
 *
 * 所有 handler 接受 formHint + spaceHint，内部自动 resolve + 字段映射
 */
import { apiRequest } from './utils/http-client.js';
import { buildEncodedBq, } from './utils/bq-builder.js';
import { resolveSpaceForm } from './utils/resolve.js';
import { fetchFieldDefs, mapDataKeys, mapFilterFieldNames, buildFieldMaps, } from './utils/field-defs.js';
function buildConfig(context) {
    return {
        baseUrl: context.config.BASE_URL,
        username: context.config.USERNAME,
        password: context.config.PASSWORD,
    };
}
const ERROR_PATTERNS = [
    {
        pattern: /NumberFormatException.*""/i,
        hint: '数字字段被传了空字符串 ""。请检查该字段是否应传数字值，或该字段名是否映射正确（建议先调 mofang_get_field_definitions 确认）。',
    },
    {
        pattern: /NumberFormatException/i,
        hint: '数字字段收到了非数字值。请检查字段类型和传入的值格式。',
    },
    {
        pattern: /NullPointerException/i,
        hint: '服务端空指针异常，可能是缺少必填字段或字段名不正确。建议先调 mofang_get_field_definitions 确认字段定义。',
    },
    {
        pattern: /ClassCastException/i,
        hint: '字段值类型与服务端期望不匹配（如字符串传给了引用字段）。请检查字段类型。',
    },
];
function diagnoseServerError(msg) {
    for (const { pattern, hint } of ERROR_PATTERNS) {
        if (pattern.test(msg)) {
            return `${msg} —— 可能原因: ${hint}`;
        }
    }
    return msg;
}
/**
 * CLI 标准参数为 filters（数组）。若 Agent 误传 filter（含 filterType、value2、filterGroup），
 * 在 filters 为空时尝试转成 BqFilter；无法转换时返回明确错误，避免「条件被静默忽略」。
 */
function coalesceQueryFilters(params) {
    if (params.filters && params.filters.length > 0) {
        return { effective: params.filters };
    }
    const legacy = params.filter;
    if (legacy == null) {
        return { effective: undefined };
    }
    if (typeof legacy !== 'object' || !Array.isArray(legacy.items) || legacy.items.length === 0) {
        return {
            effective: undefined,
            error: '参数错误：本命令只接受 filters（数组），不要使用魔方前端的 filter / filterType / value2 / filterGroup。日期区间示例：{"filters":[{"fieldName":"填报日期","operator":"between","value":"2026-03-01,2026-04-01"}]}',
        };
    }
    const out = [];
    for (const item of legacy.items) {
        const fieldName = item.fieldName?.trim();
        if (!fieldName) {
            return {
                effective: undefined,
                error: 'filter.items 中存在缺少 fieldName 的项。请改用手写 filters 数组，每项含 fieldName、operator、value。',
            };
        }
        const ft = String(item.filterType ?? '')
            .trim()
            .toLowerCase();
        if (ft === 'between') {
            const v1 = item.value != null ? String(item.value).trim() : '';
            const v2 = item.value2 != null ? String(item.value2).trim() : '';
            if (!v1 || !v2) {
                return {
                    effective: undefined,
                    error: 'filter 中 BETWEEN 缺少 value 或 value2。CLI 请使用：{"filters":[{"fieldName":"…","operator":"between","value":"开始日期,结束日期"}]}（两个日期用英文逗号放在一个 value 里）。',
                };
            }
            out.push({ fieldName, operator: 'between', value: `${v1},${v2}` });
            continue;
        }
        if (ft === 'eq') {
            out.push({ fieldName, operator: 'eq', value: String(item.value ?? '') });
            continue;
        }
        if (ft === 'noteq') {
            out.push({ fieldName, operator: 'noteq', value: String(item.value ?? '') });
            continue;
        }
        if (ft === 'lt' || ft === 'gt' || ft === 'lte' || ft === 'gte') {
            out.push({ fieldName, operator: ft, value: String(item.value ?? '') });
            continue;
        }
        if (ft === 'like') {
            out.push({ fieldName, operator: 'like', value: String(item.value ?? '') });
            continue;
        }
        return {
            effective: undefined,
            error: `filter.filterType「${item.filterType}」无法从旧格式自动转换。请使用 filters 数组，operator 为小写：eq、noteq、like、between、lt、gt 等；between 的 value 为「开始,结束」。`,
        };
    }
    return { effective: out };
}
export async function queryRecordsHandler(params, context) {
    const config = buildConfig(context);
    if (!config.baseUrl) {
        return { success: false, message: '未配置 BASE_URL。' };
    }
    const merged = coalesceQueryFilters(params);
    if (merged.error) {
        return { success: false, message: merged.error };
    }
    const resolved = await resolveSpaceForm(config, params.formHint, params.spaceHint);
    if (!resolved.success || !resolved.spaceId || !resolved.formId) {
        return { success: false, message: resolved.message };
    }
    const { spaceId, formId } = resolved;
    // 获取字段定义用于 filter 映射和返回 fieldLabels
    const fieldResult = await fetchFieldDefs(config, spaceId, formId);
    let fieldLabels;
    let resolvedFilters = merged.effective;
    if (fieldResult.success && fieldResult.fields.length > 0) {
        const { nameToLabel } = buildFieldMaps(fieldResult.fields);
        fieldLabels = Object.fromEntries(nameToLabel);
        if (resolvedFilters && resolvedFilters.length > 0) {
            const { mapped } = mapFilterFieldNames(fieldResult.fields, resolvedFilters);
            resolvedFilters = mapped;
        }
    }
    const page = params.page ?? 1;
    const pageSize = params.pageSize ?? 10;
    const useAll = params.all ?? false;
    const start = useAll ? 0 : (page - 1) * pageSize;
    const limit = useAll ? -1 : pageSize;
    const bqOptions = {
        filters: resolvedFilters,
        orderBy: params.orderBy,
    };
    const encodedBq = buildEncodedBq(bqOptions);
    let path = `/magicflu/service/s/jsonv2/${spaceId}/forms/${formId}/records/entry?start=${start}&limit=${limit}`;
    if (encodedBq) {
        path += `&bq=${encodedBq}`;
    }
    const result = await apiRequest(config, 'GET', path);
    if (!result.success) {
        return { success: false, message: `记录查询失败: ${result.message}` };
    }
    const entries = result.data?.entry;
    const totalCount = result.data?.totalCount ?? 0;
    const records = Array.isArray(entries) ? entries : [];
    let msg = `表单「${resolved.formLabel}」查询到 ${totalCount} 条记录（当前返回 ${records.length} 条）。`;
    if (totalCount === 0 && params.spaceHint === undefined) {
        msg += ' 提示：若数据确实存在，请尝试传入 spaceHint 明确指定空间，避免缓存解析到错误空间。';
    }
    return {
        success: true,
        message: msg,
        data: { totalCount, records, fieldLabels },
        spaceLabel: resolved.spaceLabel,
        formLabel: resolved.formLabel,
    };
}
export async function createRecordHandler(params, context) {
    const config = buildConfig(context);
    if (!config.baseUrl) {
        return { success: false, message: '未配置 BASE_URL。' };
    }
    if (!params.data || Object.keys(params.data).length === 0) {
        return { success: false, message: '记录数据不能为空。' };
    }
    const resolved = await resolveSpaceForm(config, params.formHint, params.spaceHint);
    if (!resolved.success || !resolved.spaceId || !resolved.formId) {
        return { success: false, message: resolved.message };
    }
    const { spaceId, formId } = resolved;
    const fieldResult = await fetchFieldDefs(config, spaceId, formId);
    let submitData = params.data;
    let mappingWarnings = [];
    if (fieldResult.success && fieldResult.fields.length > 0) {
        const { mapped, warnings } = mapDataKeys(fieldResult.fields, params.data);
        submitData = mapped;
        mappingWarnings = warnings;
        if (warnings.length > 0 && Object.keys(mapped).length === 0) {
            return { success: false, message: `字段映射失败: ${warnings.join('; ')}。请先调用 mofang_get_field_definitions 确认正确的字段名称。` };
        }
    }
    const path = `/magicflu/service/s/jsonv2/${spaceId}/forms/${formId}/records`;
    const result = await apiRequest(config, 'POST', path, submitData);
    if (!result.success) {
        return { success: false, message: `创建记录失败: ${diagnoseServerError(result.message)}` };
    }
    const respData = result.data;
    if (respData?.errcode !== '0') {
        return {
            success: false,
            message: `创建记录失败: ${diagnoseServerError(respData?.errmsg || '未知错误')}`,
            data: respData,
        };
    }
    let msg = `表单「${resolved.formLabel}」记录创建成功，ID: ${respData.id}`;
    if (mappingWarnings.length > 0) {
        msg += `。警告: ${mappingWarnings.join('; ')}`;
    }
    return {
        success: true,
        message: msg,
        data: respData,
        spaceLabel: resolved.spaceLabel,
        formLabel: resolved.formLabel,
    };
}
export async function updateRecordHandler(params, context) {
    const config = buildConfig(context);
    if (!config.baseUrl) {
        return { success: false, message: '未配置 BASE_URL。' };
    }
    if (!params.data || Object.keys(params.data).length === 0) {
        return { success: false, message: '修改数据不能为空。' };
    }
    const resolved = await resolveSpaceForm(config, params.formHint, params.spaceHint);
    if (!resolved.success || !resolved.spaceId || !resolved.formId) {
        return { success: false, message: resolved.message };
    }
    const { spaceId, formId } = resolved;
    const fieldResult = await fetchFieldDefs(config, spaceId, formId);
    let submitData = params.data;
    let mappingWarnings = [];
    if (fieldResult.success && fieldResult.fields.length > 0) {
        const { mapped, warnings } = mapDataKeys(fieldResult.fields, params.data);
        submitData = mapped;
        mappingWarnings = warnings;
        if (warnings.length > 0 && Object.keys(mapped).length === 0) {
            return { success: false, message: `字段映射失败: ${warnings.join('; ')}。请先调用 mofang_get_field_definitions 确认正确的字段名称。` };
        }
    }
    const path = `/magicflu/service/s/jsonv2/${spaceId}/forms/${formId}/records/entry/${params.recordId}`;
    const result = await apiRequest(config, 'PUT', path, submitData);
    if (!result.success) {
        return { success: false, message: `修改记录失败: ${diagnoseServerError(result.message)}` };
    }
    const respData = result.data;
    if (respData?.errcode !== '0') {
        return {
            success: false,
            message: `修改记录失败: ${diagnoseServerError(respData?.errmsg || '未知错误')}`,
            data: respData,
        };
    }
    let msg = `表单「${resolved.formLabel}」记录修改成功。`;
    if (mappingWarnings.length > 0) {
        msg += ` 警告: ${mappingWarnings.join('; ')}`;
    }
    return {
        success: true,
        message: msg,
        data: respData,
        spaceLabel: resolved.spaceLabel,
        formLabel: resolved.formLabel,
    };
}
export async function deleteRecordHandler(params, context) {
    const config = buildConfig(context);
    if (!config.baseUrl) {
        return { success: false, message: '未配置 BASE_URL。' };
    }
    const resolved = await resolveSpaceForm(config, params.formHint, params.spaceHint);
    if (!resolved.success || !resolved.spaceId || !resolved.formId) {
        return { success: false, message: resolved.message };
    }
    const { spaceId, formId } = resolved;
    const path = `/magicflu/service/s/jsonv2/${spaceId}/forms/${formId}/records/entry/${params.recordId}`;
    const result = await apiRequest(config, 'DELETE', path);
    if (!result.success) {
        return { success: false, message: `删除记录失败: ${result.message}` };
    }
    const respData = result.data;
    if (respData?.errcode !== '0') {
        return {
            success: false,
            message: `删除记录失败: ${respData?.errmsg || '未知错误'}`,
            data: respData,
        };
    }
    return {
        success: true,
        message: `表单「${resolved.formLabel}」记录删除成功。`,
        data: respData,
        spaceLabel: resolved.spaceLabel,
        formLabel: resolved.formLabel,
    };
}
//# sourceMappingURL=records.js.map