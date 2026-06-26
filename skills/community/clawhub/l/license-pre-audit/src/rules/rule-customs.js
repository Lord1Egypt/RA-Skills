#!/usr/bin/env node
/**
 * 规则 10: 报关口岸检查
 * 验证报关口岸信息（通常与出口国检查合并）
 */

function checkCustoms(formDoc, contractDoc) {
  if (!formDoc) {
    return { reviewResult: '不通过', reviewDetail: '未提供申请表' };
  }
  
  const port = formDoc.analysis?.customsPort;
  
  if (!port) {
    return { reviewResult: '建议通过', reviewDetail: '报关口岸未填写', note: '非必填项' };
  }
  
  // 如果出口国是中国，报关口岸应该是保税区
  const exportCountry = formDoc.analysis?.exportCountry;
  if (exportCountry === '中国' && !port.includes('保税')) {
    return {
      reviewResult: '建议通过，需人工复审',
      reviewDetail: { port: port, note: '出口国为中国，报关口岸非保税区' },
      note: '需复核是否合规'
    };
  }
  
  return { reviewResult: '通过', reviewDetail: { port: port } };
}

module.exports = { checkCustoms };
