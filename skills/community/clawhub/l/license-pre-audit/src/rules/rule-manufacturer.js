#!/usr/bin/env node
/**
 * 规则 9: 生产商检查
 * 验证申请表与附件生产商是否一致
 */

function checkManufacturer(certDoc, formDoc) {
  if (!certDoc || !formDoc) {
    return {
      reviewResult: '不通过',
      reviewDetail: { formdata: formDoc?.analysis?.manufacturer || '未提取', attachdata: certDoc?.analysis?.manufacturer || '未提取' }
    };
  }
  
  const cManu = certDoc.analysis?.manufacturer;
  const fManu = formDoc.analysis?.manufacturer;
  
  if (cManu && fManu && cManu === fManu) {
    return { reviewResult: '通过', reviewDetail: { formdata: fManu, attachdata: cManu } };
  } else if (cManu && fManu && isHighlySimilar(cManu, fManu)) {
    return {
      reviewResult: '建议通过，需人工复审',
      reviewDetail: { formdata: fManu, attachdata: cManu },
      note: '生产商名称高度相似（可能为 OCR 识别差异），建议通过但需人工确认'
    };
  } else {
    return {
      reviewResult: '不通过',
      reviewDetail: { formdata: fManu || '未提取', attachdata: cManu || '未提取' }
    };
  }
}

function isHighlySimilar(str1, str2) {
  if (!str1 || !str2) return false;
  const s1 = str1.replace(/\s+/g, '');
  const s2 = str2.replace(/\s+/g, '');
  
  if (s1 === s2) return true;
  
  const minLen = Math.min(s1.length, s2.length);
  const maxLen = Math.max(s1.length, s2.length);
  
  if (minLen > 5 && (s1.includes(s2) || s2.includes(s1))) return true;
  if (maxLen - minLen <= 3 && minLen > 5) return true;
  
  return false;
}

module.exports = { checkManufacturer, isHighlySimilar };
