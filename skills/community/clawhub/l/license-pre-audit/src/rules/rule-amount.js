#!/usr/bin/env node
/**
 * 规则 5: 金额检查
 * 验证申请表与附件金额是否一致（允许 5% 容忍度）
 */

/**
 * 检查金额一致性
 * @param {Object} formDoc - 申请表文档分析结果
 * @param {Object} contractDoc - 合同文档分析结果
 * @returns {Object} 金额检查结果
 */
function checkAmount(formDoc, contractDoc) {
  if (!formDoc) {
    return {
      reviewResult: '不通过',
      reviewDetail: { formdata: '未提供申请表', attachdata: '未提供' },
      note: '缺少申请表'
    };
  }
  
  const fAmt = formDoc.analysis?.totalAmount;
  
  if (!contractDoc) {
    return {
      reviewResult: '不通过',
      reviewDetail: { formdata: fAmt || '未提取', attachdata: '未提供合同' },
      note: '缺少合同附件，无法进行对比'
    };
  }
  
  const cAmt = contractDoc.analysis?.totalAmount;
  
  if (cAmt && fAmt) {
    const cNum = cAmt.replace(/[^0-9.]/g, '');
    const fNum = fAmt.replace(/[^0-9.]/g, '');
    
    if (cNum === fNum && cNum !== '') {
      return {
        reviewResult: '通过',
        reviewDetail: { formdata: fAmt, attachdata: cAmt },
        note: '金额数字一致，仅格式/币别描述差异'
      };
    } else if (isHighlySimilar(cAmt, fAmt)) {
      return {
        reviewResult: '建议通过，需人工复审',
        reviewDetail: { formdata: fAmt, attachdata: cAmt },
        note: '金额高度相似，建议通过但需人工确认'
      };
    } else {
      return {
        reviewResult: '不通过',
        reviewDetail: { formdata: fAmt, attachdata: cAmt },
        note: '金额不一致'
      };
    }
  }
  
  return {
    reviewResult: '不通过',
    reviewDetail: { formdata: fAmt || '未提取', attachdata: cAmt || '未提取' }
  };
}

/**
 * 判断两个金额字符串是否高度相似
 * @param {string} str1 
 * @param {string} str2 
 * @returns {boolean}
 */
function isHighlySimilar(str1, str2) {
  if (!str1 || !str2) return false;
  
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

module.exports = {
  checkAmount,
  isHighlySimilar
};
