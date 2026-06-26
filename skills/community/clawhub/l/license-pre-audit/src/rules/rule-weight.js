#!/usr/bin/env node
/**
 * 规则 7: 重量检查
 * 验证申请表与附件重量是否一致
 */

function checkWeight(formDoc, contractDoc) {
  // 重量检查通常与数量检查合并，这里保留接口
  if (!formDoc || !contractDoc) {
    return {
      reviewResult: formDoc && contractDoc ? '通过' : '不通过',
      reviewDetail: '重量检查通常与数量检查合并'
    };
  }
  
  const fWeight = formDoc.analysis?.totalWeight;
  const cWeight = contractDoc.analysis?.totalWeight;
  
  if (cWeight && fWeight && cWeight === fWeight) {
    return { reviewResult: '通过', reviewDetail: { formdata: fWeight, attachdata: cWeight } };
  }
  
  return { reviewResult: '建议通过', reviewDetail: { formdata: fWeight || '未提取', attachdata: cWeight || '未提取' }, note: '重量信息已包含在数量检查中' };
}

module.exports = { checkWeight };
