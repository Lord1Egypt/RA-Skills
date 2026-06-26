#!/usr/bin/env node
/**
 * 规则 11: 审核摘要生成
 * 汇总所有规则的执行结果，生成最终审核报告
 */

/**
 * 生成审核摘要
 * @param {Array} documents - 文档分析结果数组
 * @param {Object} rules - 规则对象集合
 * @returns {Object} 审核摘要
 */
function generateSummary(documents, rules) {
  const contractDoc = documents.find(d => d.docType === '合同');
  const certDoc = documents.find(d => d.docType === '合格证');
  const formDoc = documents.find(d => d.docType === '申请表');
  
  const summary = {
    reviewResult: '',
    reviewDetail: '',
    sign: { reviewResult: '', reviewDetail: '' },
    contracNo: { reviewResult: '', reviewDetail: {} },
    exporter: { reviewResult: '', reviewDetail: {}, note: '' },
    importerEn: { reviewResult: '', reviewDetail: {} },
    bussDetial: { reviewResult: '', reviewDetail: {} },
    totalAmount: { reviewResult: '', reviewDetail: {}, note: '' },
    totalQuantity: { reviewResult: '', reviewDetail: {}, note: '' },
    mtcNo: { reviewResult: '', reviewDetail: {}, note: '' },
    manufacturer: { reviewResult: '', reviewDetail: {} }
  };
  
  let failCount = 0;
  const checks = [];
  
  // 1. 盖章检查
  summary.sign = rules.ruleStamp.checkStamp(contractDoc, certDoc);
  if (summary.sign.reviewResult === '不通过') failCount++;
  
  // 2. 合同号检查
  summary.contracNo = rules.ruleContractNo.checkContractNo(formDoc, contractDoc);
  if (summary.contracNo.reviewResult === '通过') {
    checks.push(`1. 合同编号一致：${contractDoc?.analysis?.contractNo}`);
  } else {
    checks.push(`1. 合同编号不一致`);
    failCount++;
  }
  
  // 3. 出口国检查
  summary.exporter = rules.ruleExporter.checkExporter(formDoc, contractDoc);
  if (summary.exporter.reviewResult === '通过') {
    checks.push(`2. 出口国一致：${contractDoc?.analysis?.exportCountry}`);
  } else if (summary.exporter.reviewResult === '建议通过，需人工复审') {
    checks.push(`2. 出口国建议复审`);
  } else {
    checks.push(`2. 出口国不一致`);
    failCount++;
  }
  
  // 4. 进口商检查
  summary.importerEn = rules.ruleImporter.checkImporter(formDoc, contractDoc);
  if (summary.importerEn.reviewResult === '通过') {
    checks.push(`3. 进口商英文名称一致：${contractDoc?.analysis?.importerEn}`);
  } else if (summary.importerEn.reviewResult === '建议通过，需人工复审') {
    checks.push(`3. 进口商名称建议复审`);
  } else {
    checks.push(`3. 进口商英文名称不一致`);
    failCount++;
  }
  
  // 5. 货物详情检查（简化）
  if (formDoc && contractDoc) {
    const fGoods = formDoc.analysis?.bussDetial?.[0];
    const cGoods = contractDoc.analysis?.bussDetial?.[0];
    
    if (cGoods && fGoods) {
      const match = cGoods.commodity === fGoods.commodity || 
        (cGoods.commodity && cGoods.commodity.includes(fGoods.commodity));
      
      if (match) {
        checks.push(`7. 货物详情一致：${cGoods.commodity}`);
        summary.bussDetial = {
          reviewResult: '通过',
          reviewDetail: {
            formdata: `${fGoods.commodity}，${fGoods.quantity}，单价${fGoods.unitPrice}，总价${fGoods.amount}`,
            attachdata: `${cGoods.commodity}，${cGoods.quantity}，单价${cGoods.unitPrice}，总价${cGoods.amount}`
          }
        };
      } else {
        checks.push(`7. 货物详情不一致`);
        summary.bussDetial = { reviewResult: '不通过', reviewDetail: { formdata: '未匹配', attachdata: '未匹配' } };
        failCount++;
      }
    }
  } else {
    checks.push(`7. 货物详情：未提供完整数据`);
    summary.bussDetial = { reviewResult: '不通过', reviewDetail: { formdata: '未提取', attachdata: '未提供合同' } };
    failCount++;
  }
  
  // 6. 金额检查
  summary.totalAmount = rules.ruleAmount.checkAmount(formDoc, contractDoc);
  if (summary.totalAmount.reviewResult === '通过') {
    checks.push(`8. 价格总计一致：${contractDoc?.analysis?.totalAmount}`);
  } else if (summary.totalAmount.reviewResult === '建议通过，需人工复审') {
    checks.push(`8. 价格总计建议复审`);
  } else {
    checks.push(`8. 价格总计不一致`);
    failCount++;
  }
  
  // 7. 数量检查
  summary.totalQuantity = rules.ruleQuantity.checkQuantity(formDoc, contractDoc);
  if (summary.totalQuantity.reviewResult === '通过') {
    checks.push(`9. 货物总量一致：${contractDoc?.analysis?.totalQuantity}`);
  } else if (summary.totalQuantity.reviewResult === '建议通过，需人工复审') {
    checks.push(`9. 货物总量建议复审`);
  } else {
    checks.push(`9. 货物总量不一致`);
    failCount++;
  }
  
  // 8. 合格证编号检查
  summary.mtcNo = rules.ruleMtcNo.checkMtcNo(certDoc, formDoc);
  if (summary.mtcNo.reviewResult === '通过') {
    checks.push(`5. 合格证编号一致：${certDoc?.analysis?.mtcNo}`);
  } else if (summary.mtcNo.reviewResult === '建议通过，需人工复审') {
    checks.push(`5. 合格证编号建议复审`);
  } else {
    checks.push(`5. 合格证编号不一致`);
    failCount++;
  }
  
  // 9. 生产商检查
  summary.manufacturer = rules.ruleManufacturer.checkManufacturer(certDoc, formDoc);
  if (summary.manufacturer.reviewResult === '通过') {
    checks.push(`6. 生产商信息一致：${certDoc?.analysis?.manufacturer}`);
  } else if (summary.manufacturer.reviewResult === '建议通过，需人工复审') {
    checks.push(`6. 生产商信息高度相似：${certDoc?.analysis?.manufacturer} vs ${formDoc?.analysis?.manufacturer}`);
  } else {
    failCount++;
  }
  
  // 生成最终结果
  summary.reviewResult = failCount === 0 
    ? '整体审核结果：建议通过' 
    : '整体审核结果：建议不通过';
  summary.reviewDetail = checks.join('\n') + (failCount > 0 ? `\n\n不通过项共 ${failCount} 项。` : '');
  
  return summary;
}

module.exports = {
  generateSummary
};
