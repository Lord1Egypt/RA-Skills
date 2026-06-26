#!/usr/bin/env node
/**
 * 规则 4: 进口商检查
 * 验证申请表与附件进口商英文名称是否一致（允许空格差异）
 */

/**
 * 检查进口商一致性
 * @param {Object} formDoc - 申请表文档分析结果
 * @param {Object} contractDoc - 合同文档分析结果
 * @returns {Object} 进口商检查结果
 */
function checkImporter(formDoc, contractDoc) {
  if (!formDoc) {
    return {
      reviewResult: '不通过',
      reviewDetail: { formdata: '未提供申请表', attachdata: '未提供' }
    };
  }
  
  const fImp = formDoc.analysis?.importerEn;
  
  if (!contractDoc) {
    return {
      reviewResult: '不通过',
      reviewDetail: { formdata: fImp || '未提取', attachdata: '未提供合同' }
    };
  }
  
  const cImp = contractDoc.analysis?.importerEn;
  
  // 检查去除空格后是否完全一致
  if (cImp && fImp && cImp.replace(/\s+/g, '') === fImp.replace(/\s+/g, '')) {
    return {
      reviewResult: '通过',
      reviewDetail: { formdata: fImp, attachdata: cImp },
      note: '仅空格差异，视为一致'
    };
  } else if (cImp && fImp && isHighlySimilar(cImp, fImp)) {
    return {
      reviewResult: '通过',
      reviewDetail: { formdata: fImp, attachdata: cImp },
      note: '进口商名称高度相似（空格/后缀差异），视为一致'
    };
  } else {
    return {
      reviewResult: '不通过',
      reviewDetail: { formdata: fImp || '未提取', attachdata: cImp || '未提取' }
    };
  }
}

/**
 * 判断两个字符串是否高度相似
 * @param {string} str1 
 * @param {string} str2 
 * @returns {boolean}
 */
function isHighlySimilar(str1, str2) {
  if (!str1 || !str2) return false;
  
  const s1 = str1.replace(/\s+/g, '').replace(/[,，]/g, '');
  const s2 = str2.replace(/\s+/g, '').replace(/[,，]/g, '');
  
  if (s1 === s2) return true;
  
  const minLen = Math.min(s1.length, s2.length);
  const maxLen = Math.max(s1.length, s2.length);
  
  if (minLen > 5 && (s1.includes(s2) || s2.includes(s1))) return true;
  if (maxLen - minLen <= 3 && minLen > 5 && !/^\d+\.?\d*$/.test(s1) && !/^\d+\.?\d*$/.test(s2)) return true;
  
  return false;
}

module.exports = {
  checkImporter,
  isHighlySimilar
};
