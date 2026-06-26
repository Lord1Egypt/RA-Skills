/**
 * 字段定义获取 + label↔name 映射工具
 * 被 records/fields handler 内部调用
 */
import { apiRequest } from './http-client.js';
import { getQueryType } from './bq-builder.js';
const EDIT_TYPE_MAP = {
    text: true,
    multiline_text: true,
    date: true,
    datetime: true,
    number: true,
    dropdown_list: true,
    checkbox: true,
    url: true,
    html: true,
    tree: true,
    reference: true,
    webpage: false,
    webpage2: false,
    comment: false,
    system: false,
    attachment: false,
    image: false,
    embed: false,
    serial: false,
    external: false,
    location: false,
    singleuser: false,
    manyusers: false,
    singleorgnode: false,
    manyorgnodes: false,
};
const VALUE_DESC_MAP = {
    text: '填写字符串',
    multiline_text: '填写字符串',
    date: '填写日期，格式 YYYY-MM-DD',
    datetime: '填写日期时间，格式 YYYY-MM-DD HH:mm:ss',
    number: '填写数字',
    dropdown_list: '填写选项的ID，例如 "1"',
    checkbox: '填写选项的ID，多个用逗号隔开，例如 "1,2"',
    url: '填写URL字符串',
    html: '填写HTML片段',
    tree: '填写选项的ID，例如 "1"',
    reference: '填写引用记录的JSON，例如 {"id":"1"}',
    system: '系统自动生成，不可赋值',
    serial: '编码自动生成，不可赋值',
    embed: '嵌入表字段，不可在主表直接赋值。先在子表创建记录取得ID，再更新主表：{"entry":[{"id":"子记录ID"}]}',
    webpage: '不支持直接提交',
    webpage2: '不支持直接提交',
    comment: '不支持直接提交',
    attachment: '不支持直接提交',
    image: '不支持直接提交',
    external: '不支持直接提交',
    location: '不支持直接提交',
};
function isEditable(field) {
    const type = field.type;
    if (type === 'reference')
        return field.dependOn === field.name;
    return EDIT_TYPE_MAP[type] ?? false;
}
function getValueDesc(field) {
    const type = field.type;
    if (type === 'reference' && field.dependOn !== field.name) {
        return '辅引用字段，由后端根据主引用自动填充，不可赋值';
    }
    return VALUE_DESC_MAP[type] || '未知类型';
}
function extractOptions(field) {
    const type = field.type;
    if (type !== 'dropdown_list' && type !== 'checkbox' && type !== 'tree')
        return undefined;
    const raw = field.values ?? field.items ?? field.options ?? field.ddlValues;
    if (!Array.isArray(raw) || raw.length === 0)
        return undefined;
    return raw.map((item) => {
        const value = String(item.value ?? item.id ?? item.key ?? '');
        const content = String(item.content ?? item.label ?? item.text ?? item.name ?? '');
        const display = content || value;
        return { value, content: display, display };
    });
}
/**
 * 从 API 获取字段定义并解析为 FieldDef[]
 */
export async function fetchFieldDefs(config, spaceId, formId) {
    const path = `/magicflu/service/s/jsonv2/${spaceId}/forms/${formId}?selector=fielddef&lng=en`;
    const result = await apiRequest(config, 'GET', path);
    if (!result.success) {
        return { success: false, message: `字段定义获取失败: ${result.message}`, fields: [] };
    }
    const rawFields = result.data?.fields;
    if (!Array.isArray(rawFields)) {
        return { success: false, message: '返回的字段定义格式异常。', fields: [] };
    }
    const fields = rawFields.map((f) => {
        const def = {
            name: f.name,
            label: f.label,
            type: f.type,
            required: f.required === 'true',
            defaultValue: f.default || '',
            editable: isEditable(f),
            queryType: getQueryType(f.type, f.name),
            valueDesc: getValueDesc(f),
        };
        const opts = extractOptions(f);
        if (opts)
            def.options = opts;
        if (f.maxlen)
            def.maxlen = f.maxlen;
        if (f.maxvalue)
            def.maxvalue = f.maxvalue;
        if (f.minvalue)
            def.minvalue = f.minvalue;
        if (f.pointnum)
            def.pointnum = f.pointnum;
        if (f.unique === 'true')
            def.unique = true;
        if (f.dependOn)
            def.dependOn = f.dependOn;
        if (f.sourceFormId)
            def.sourceFormId = f.sourceFormId;
        if (f.sourceFieldName)
            def.sourceFieldName = f.sourceFieldName;
        return def;
    });
    return { success: true, message: 'ok', fields };
}
/**
 * 构建 label→name 和 name→label 映射
 */
export function buildFieldMaps(fields) {
    const labelToName = new Map();
    const nameToLabel = new Map();
    const nameSet = new Set();
    for (const f of fields) {
        nameSet.add(f.name);
        nameToLabel.set(f.name, f.label);
        if (f.editable) {
            labelToName.set(f.label, f.name);
        }
    }
    return { labelToName, nameToLabel, nameSet };
}
/**
 * 将 data 对象的 key 从 label 或 name 统一映射为 name
 * 同时支持中文 label 和英文 name 作为 key
 */
export function mapDataKeys(fields, data) {
    const { labelToName, nameSet } = buildFieldMaps(fields);
    const mapped = {};
    const warnings = [];
    for (const [key, value] of Object.entries(data)) {
        if (nameSet.has(key)) {
            mapped[key] = value;
        }
        else if (labelToName.has(key)) {
            mapped[labelToName.get(key)] = value;
        }
        else {
            warnings.push(`字段 "${key}" 未找到匹配的字段定义，已忽略`);
        }
    }
    return { mapped, warnings };
}
/**
 * 将 filters 中的 fieldName 从 label 转为 name（如果需要）
 */
export function mapFilterFieldNames(fields, filters) {
    const { labelToName, nameSet, nameToLabel } = buildFieldMaps(fields);
    const mapped = [];
    const warnings = [];
    for (const f of filters) {
        if (nameSet.has(f.fieldName) || f.fieldName === 'id') {
            mapped.push(f);
        }
        else if (labelToName.has(f.fieldName)) {
            mapped.push({ ...f, fieldName: labelToName.get(f.fieldName) });
        }
        else {
            // 也检查所有字段（含不可编辑的）
            const allMatch = fields.find((fd) => fd.label === f.fieldName);
            if (allMatch) {
                mapped.push({ ...f, fieldName: allMatch.name });
            }
            else {
                warnings.push(`过滤字段 "${f.fieldName}" 未找到匹配的字段定义`);
                mapped.push(f);
            }
        }
    }
    return { mapped, warnings };
}
/**
 * 生成可编辑字段的映射摘要（用于返回给 Agent）
 */
export function buildMappingSummary(fields) {
    return fields
        .filter((f) => f.editable)
        .map((f) => {
        let desc = `${f.label} → ${f.name} (${f.type})`;
        if (f.required)
            desc += ' [必填]';
        if (f.options) {
            const optStr = f.options.map((o) => `${o.display || o.content}(value: ${o.value})`).join(', ');
            desc += ` 选项: {${optStr}}`;
        }
        return desc;
    })
        .join('; ');
}
//# sourceMappingURL=field-defs.js.map