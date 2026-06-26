/**
 * bq 查询条件构造器
 *
 * 语法: filter (CONCAT filter)*
 * filter: [!!]fieldName(operator):value
 * CONCAT: && | ||
 *
 * 文本值需要 _Base64 编码，数字/日期直接使用
 */
import { encodeBqTextValue } from './base64.js';
const STRING_OPERATORS = new Set([
    'eq', 'noteq', 'like', 'like_and', 'like_or',
    'or_like_and', 'fulltext', 'in', 'notin',
    'checkbox_in', 'checkbox_eq', 'tree', 'rddl',
    'isnull', 'isnotnull',
]);
const REGION_OPERATORS = new Set([
    'eq', 'noteq', 'lt', 'gt', 'lte', 'gte', 'between',
    'isnull', 'isnotnull',
]);
const NO_ENCODE_OPERATORS = new Set([
    'isnull', 'isnotnull', 'in', 'notin',
    'checkbox_in', 'checkbox_eq', 'between',
]);
/**
 * 根据字段类型和名称判断查询类型
 */
export function getQueryType(fieldType, fieldName) {
    if (fieldType === 'system') {
        if (fieldName === 'id' || fieldName === 'created' || fieldName === 'updated') {
            return 'region';
        }
        return 'string';
    }
    if (fieldType === 'date' || fieldType === 'datetime' || fieldType === 'number') {
        return 'region';
    }
    return 'string';
}
/**
 * 格式化单个 filter 的值
 */
function formatFilterValue(operator, value, queryType) {
    if (operator === 'isnull' || operator === 'isnotnull') {
        return '-1';
    }
    if (operator === 'orderby') {
        return value === 'desc' ? 'desc' : 'asc';
    }
    if (NO_ENCODE_OPERATORS.has(operator)) {
        return value;
    }
    if (queryType === 'region') {
        return value;
    }
    return encodeBqTextValue(value);
}
/**
 * 构建单个 filter 字符串
 */
function buildSingleFilter(filter, queryType) {
    const prefix = filter.not ? '!!' : '';
    const formattedValue = formatFilterValue(filter.operator, filter.value, queryType);
    return `${prefix}${filter.fieldName}(${filter.operator}):${formattedValue}`;
}
/**
 * 构建完整的 bq 查询字符串（未经 encodeURIComponent）
 */
export function buildBq(options) {
    const { filters = [], orderBy, fieldQueryTypes } = options;
    const parts = [];
    for (let i = 0; i < filters.length; i++) {
        const filter = filters[i];
        const queryType = fieldQueryTypes?.get(filter.fieldName) || 'string';
        const filterStr = buildSingleFilter(filter, queryType);
        if (i > 0) {
            const concat = filter.concat || '&&';
            parts.push(concat);
        }
        parts.push(filterStr);
    }
    if (orderBy) {
        if (parts.length > 0) {
            parts.push('&&');
        }
        parts.push(`${orderBy.fieldName}(orderby):${orderBy.direction}`);
    }
    return parts.join('');
}
/**
 * 构建完整的 bq 查询字符串并进行 URL 编码
 */
export function buildEncodedBq(options) {
    const bq = buildBq(options);
    if (!bq)
        return '';
    return encodeURIComponent(bq);
}
//# sourceMappingURL=bq-builder.js.map