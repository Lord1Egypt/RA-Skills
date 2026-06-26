#!/usr/bin/env node
/**
 * 字段标准化工具
 * 统一字段名称、布尔值格式、去重等
 */

/**
 * 标准化字段：统一 hasStamp 字段和布尔值格式
 * @param {Object} fields - 原始字段对象
 * @returns {Object} 标准化后的字段对象
 */
function normalizeFields(fields) {
  const normalizedFields = { ...fields };
  
  // 将 sign/allSign 统一转换为 hasStamp
  if (normalizedFields.sign !== undefined) {
    normalizedFields.hasStamp = normalizedFields.sign;
    delete normalizedFields.sign;
  }
  if (normalizedFields.allSign !== undefined) {
    normalizedFields.hasStamp = normalizedFields.allSign;
    delete normalizedFields.allSign;
  }
  
  // 统一 hasStamp 的值：将 true/false 转换为 是/否
  if (normalizedFields.hasStamp !== undefined) {
    if (normalizedFields.hasStamp === true || normalizedFields.hasStamp === 'true' || 
        normalizedFields.hasStamp === '是' || normalizedFields.hasStamp === 'Yes' || 
        normalizedFields.hasStamp === 'yes') {
      normalizedFields.hasStamp = '是';
    } else if (normalizedFields.hasStamp === false || normalizedFields.hasStamp === 'false' || 
               normalizedFields.hasStamp === '否' || normalizedFields.hasStamp === 'No' || 
               normalizedFields.hasStamp === 'no') {
      normalizedFields.hasStamp = '否';
    }
  }
  
  return normalizedFields;
}

/**
 * 移除 extractedFields 中的 hasStamp 字段（避免重复）
 * @param {Object} extractedFields - 提取的字段
 * @returns {Object} 移除 hasStamp 后的字段
 */
function removeHasStamp(extractedFields) {
  if (extractedFields?.hasStamp !== undefined) {
    const { hasStamp, ...fields } = extractedFields;
    return fields;
  }
  return extractedFields;
}

module.exports = {
  normalizeFields,
  removeHasStamp
};
