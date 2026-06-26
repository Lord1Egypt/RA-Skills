#!/usr/bin/env node
/**
 * 规则 3: 出口国检查
 * 验证申请表与附件出口国是否一致；若为中国，报关口岸必须是保税区
 */

/**
 * 检查出口国一致性
 * @param {Object} formDoc - 申请表文档分析结果
 * @param {Object} contractDoc - 合同文档分析结果
 * @returns {Object} 出口国检查结果
 */
function checkExporter(formDoc, contractDoc) {
  if (!formDoc) {
    return {
      reviewResult: '不通过',
      reviewDetail: { formdata: '未提供申请表', customsPort: '', attachdata: '未提供' }
    };
  }
  
  const fCountry = formDoc.analysis?.exportCountry;
  const port = formDoc.analysis?.customsPort;
  
  if (!contractDoc) {
    return {
      reviewResult: '不通过',
      reviewDetail: { formdata: fCountry || '未提取', customsPort: port || '', attachdata: '未提供合同' },
      note: '缺少合同附件，无法进行对比'
    };
  }
  
  const cCountry = contractDoc.analysis?.exportCountry;
  
  if (cCountry && fCountry && cCountry === fCountry) {
    let note = cCountry !== '中国' 
      ? `出口国为${cCountry}，非中国境内，无需保税区审核。` 
      : '';
    
    if (cCountry === '中国' && port && !port.includes('保税')) {
      note = '出口国为中国，报关口岸非保税区，需复核。';
    }
    
    return {
      reviewResult: (cCountry === '中国' && port && !port.includes('保税')) 
        ? '建议通过，需人工复审' 
        : '通过',
      reviewDetail: { formdata: fCountry, customsPort: port || '未提取', attachdata: cCountry },
      note: note
    };
  } else {
    return {
      reviewResult: '不通过',
      reviewDetail: { formdata: fCountry || '未提取', customsPort: port || '', attachdata: cCountry || '未提取' },
      note: ''
    };
  }
}

module.exports = {
  checkExporter
};
