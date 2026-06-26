/**
 * mofang_get_field_definitions — 获取表单字段结构定义
 * 接受 formHint + spaceHint，内部自动解析为 spaceId + formId
 */
import { resolveSpaceForm } from './utils/resolve.js';
import { fetchFieldDefs, buildMappingSummary } from './utils/field-defs.js';
function buildConfig(context) {
    return {
        baseUrl: context.config.BASE_URL,
        username: context.config.USERNAME,
        password: context.config.PASSWORD,
    };
}
export async function handler(params, context) {
    const config = buildConfig(context);
    if (!config.baseUrl) {
        return { success: false, message: '未配置 BASE_URL。' };
    }
    const resolved = await resolveSpaceForm(config, params.formHint, params.spaceHint);
    if (!resolved.success || !resolved.spaceId || !resolved.formId) {
        return { success: false, message: resolved.message };
    }
    const { success, message, fields } = await fetchFieldDefs(config, resolved.spaceId, resolved.formId);
    if (!success) {
        return { success: false, message };
    }
    const editableFields = fields.filter((f) => f.editable);
    const mappingSummary = buildMappingSummary(fields);
    return {
        success: true,
        message: `表单「${resolved.formLabel}」共 ${fields.length} 个字段，其中 ${editableFields.length} 个可编辑。\n\n可编辑字段映射: ${mappingSummary}`,
        data: fields,
        fieldMapping: mappingSummary,
        spaceLabel: resolved.spaceLabel,
        formLabel: resolved.formLabel,
    };
}
//# sourceMappingURL=fields.js.map