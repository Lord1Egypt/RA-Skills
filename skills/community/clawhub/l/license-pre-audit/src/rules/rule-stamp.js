#!/usr/bin/env node
/**
 * 规则 1: 盖章检查
 * 检测合同和合格证是否已盖章
 */

/**
 * 检查盖章情况
 * @param {Object} contractDoc - 合同文档分析结果
 * @param {Object} certDoc - 合格证文档分析结果
 * @returns {Object} 盖章检查结果
 */
function checkStamp(contractDoc, certDoc) {
  const signDetail = [];
  let failCount = 0;
  
  // hasStamp 现在在顶层，不在 analysis 中
  if (contractDoc?.hasStamp === true) {
    signDetail.push('合同已盖章');
  } else if (contractDoc?.hasStamp === false) {
    signDetail.push('合同未盖章');
    failCount++;
  }
  
  if (certDoc?.hasStamp === true) {
    signDetail.push('合格证已盖章');
  } else if (certDoc?.hasStamp === false) {
    signDetail.push('合格证未盖章');
    failCount++;
  }
  
  return {
    reviewResult: failCount > 0 ? '不通过' : '通过',
    reviewDetail: signDetail.join('。') || '未检测到合同或合格证'
  };
}

module.exports = {
  checkStamp
};
