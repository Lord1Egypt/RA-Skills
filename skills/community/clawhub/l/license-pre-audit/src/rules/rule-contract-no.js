#!/usr/bin/env node
/**
 * 规则 2: 合同号检查
 * 验证申请表与附件合同号是否一致
 */

/**
 * 检查合同号一致性
 * @param {Object} formDoc - 申请表文档分析结果
 * @param {Object} contractDoc - 合同文档分析结果
 * @returns {Object} 合同号检查结果
 */
function checkContractNo(formDoc, contractDoc) {
  if (!formDoc) {
    return {
      reviewResult: '不通过',
      reviewDetail: { formdata: '未提供申请表', attachdata: '未提供' }
    };
  }
  
  const fNo = formDoc.analysis?.contracNo;
  
  if (!contractDoc) {
    return {
      reviewResult: '不通过',
      reviewDetail: { formdata: fNo || '未提取', attachdata: '未提供合同' },
      note: '缺少合同附件，无法进行对比'
    };
  }
  
  const cNo = contractDoc.analysis?.contractNo;
  
  if (cNo && fNo && cNo === fNo) {
    return {
      reviewResult: '通过',
      reviewDetail: { formdata: fNo, attachdata: cNo }
    };
  } else if (cNo && fNo && isHighlySimilar(cNo, fNo)) {
    return {
      reviewResult: '通过',
      reviewDetail: { formdata: fNo, attachdata: cNo },
      note: '合同号核心数字相同，视为一致'
    };
  } else {
    return {
      reviewResult: '不通过',
      reviewDetail: { formdata: fNo || '未提取', attachdata: cNo || '未提取' }
    };
  }
}

/**
 * 判断两个字符串是否高度相似（合同号特殊处理）
 * @param {string} str1 
 * @param {string} str2 
 * @returns {boolean}
 */
function isHighlySimilar(str1, str2) {
  if (!str1 || !str2) return false;
  
  // 提取核心数字部分
  const extractCoreNumber = (str) => {
    const match = str.match(/\d+/g);
    return match ? match.join('') : '';
  };
  
  const coreNum1 = extractCoreNumber(str1);
  const coreNum2 = extractCoreNumber(str2);
  
  return coreNum1 && coreNum2 && coreNum1 === coreNum2;
}

module.exports = {
  checkContractNo,
  isHighlySimilar
};
