#!/usr/bin/env node
/**
 * 规则 6: 数量检查
 * 验证申请表与附件数量是否一致（允许 5% 容忍度）
 */

function checkQuantity(formDoc, contractDoc) {
  if (!formDoc) {
    return { reviewResult: '不通过', reviewDetail: { formdata: '未提供', attachdata: '未提供' } };
  }
  
  const fQty = formDoc.analysis?.totalQuantity;
  
  if (!contractDoc) {
    return {
      reviewResult: '不通过',
      reviewDetail: { formdata: fQty || '未提取', attachdata: '未提供合同' },
      note: '缺少合同附件'
    };
  }
  
  const cQty = contractDoc.analysis?.totalQuantity;
  
  if (cQty && fQty && cQty === fQty) {
    return { reviewResult: '通过', reviewDetail: { formdata: fQty, attachdata: cQty }, note: '货物总量一致' };
  } else if (cQty && fQty && isHighlySimilar(cQty, fQty)) {
    return {
      reviewResult: '建议通过，需人工复审',
      reviewDetail: { formdata: fQty, attachdata: cQty },
      note: '数量高度相似，建议通过但需人工确认'
    };
  } else if (cQty && fQty) {
    return { reviewResult: '不通过', reviewDetail: { formdata: fQty, attachdata: cQty }, note: '数量不一致' };
  }
  
  return { reviewResult: '不通过', reviewDetail: { formdata: fQty || '未提取', attachdata: cQty || '未提取' } };
}

function isHighlySimilar(str1, str2) {
  if (!str1 || !str2) return false;
  const s1 = str1.replace(/\s+/g, '').replace(/[,，]/g, '');
  const s2 = str2.replace(/\s+/g, '').replace(/[,，]/g, '');
  if (s1 === s2) return true;
  
  const extractNumber = (str) => {
    const numStr = str.replace(/[^0-9.]/g, '');
    const num = parseFloat(numStr);
    return isNaN(num) ? null : num;
  };
  
  const num1 = extractNumber(str1);
  const num2 = extractNumber(str2);
  
  if (num1 !== null && num2 !== null) {
    if (num1 === num2) return true;
    const avg = (Math.abs(num1) + Math.abs(num2)) / 2;
    if (avg === 0) return true;
    const relativeError = Math.abs(num1 - num2) / avg;
    return relativeError < 0.05;
  }
  
  return false;
}

module.exports = { checkQuantity, isHighlySimilar };
