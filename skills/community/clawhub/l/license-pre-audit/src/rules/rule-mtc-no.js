#!/usr/bin/env node
/**
 * 规则 8: 合格证编号检查
 * 验证申请表与附件合格证编号是否一致
 */

function checkMtcNo(certDoc, formDoc) {
  if (!certDoc || !formDoc) {
    return {
      reviewResult: '不通过',
      reviewDetail: { formdata: formDoc?.analysis?.mtcNo || '未提取', attachdata: certDoc?.analysis?.mtcNo || '未提取' }
    };
  }
  
  const cNo = certDoc.analysis?.mtcNo;
  const fNos = formDoc.analysis?.mtcNo;
  
  if (cNo && fNos && fNos.split(/[,,]/).includes(cNo)) {
    return {
      reviewResult: '通过',
      reviewDetail: { formdata: fNos, attachdata: cNo },
      note: fNos.includes(',') ? '申请表包含多个合格证编号' : '编号一致'
    };
  } else if (cNo && fNos) {
    // 检查 OCR 识别差异
    const normalizeForOCR = (str) => str.toUpperCase()
      .replace(/0/g, 'O').replace(/1/g, 'I').replace(/8/g, 'B')
      .replace(/3/g, 'E').replace(/5/g, 'S').replace(/2/g, 'Z').replace(/7/g, 'T');
    
    const normCNo = normalizeForOCR(cNo);
    const normFNos = normalizeForOCR(fNos);
    
    if (normFNos.split(/[,,]/).includes(normCNo)) {
      return {
        reviewResult: '建议通过，需人工复审',
        reviewDetail: { formdata: fNos, attachdata: cNo },
        note: '合格证编号存在 OCR 识别差异，建议通过但需人工确认'
      };
    }
    
    // 检查字符差异
    const cParts = cNo.split(/[,,]/);
    const fParts = fNos.split(/[,,]/);
    let hasSimilar = false;
    
    for (const cPart of cParts) {
      for (const fPart of fParts) {
        if (cPart.length === fPart.length) {
          let diffCount = 0;
          for (let i = 0; i < cPart.length; i++) {
            if (cPart[i] !== fPart[i]) diffCount++;
          }
          if (diffCount <= 2 && diffCount > 0) {
            hasSimilar = true;
            break;
          }
        }
        if (hasSimilar) break;
      }
      if (hasSimilar) break;
    }
    
    if (hasSimilar) {
      return {
        reviewResult: '建议通过，需人工复审',
        reviewDetail: { formdata: fNos, attachdata: cNo },
        note: '合格证编号存在字符差异，建议通过但需人工确认'
      };
    }
    
    return {
      reviewResult: '不通过',
      reviewDetail: { formdata: fNos, attachdata: cNo }
    };
  }
  
  return {
    reviewResult: '不通过',
    reviewDetail: { formdata: fNos || '未提取', attachdata: cNo || '未提取' }
  };
}

module.exports = { checkMtcNo };
