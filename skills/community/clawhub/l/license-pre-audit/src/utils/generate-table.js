#!/usr/bin/env node
/**
 * 生成二维表格数据
 * 横向：申请表、合同、预审结果
 * 纵向：9 个检查项
 */

/**
 * 生成表格数据
 * @param {Object} report - 审核报告
 * @returns {Object} 表格数据和 Markdown 格式
 */
function generateTableData(report) {
  const formDoc = report.auditResults.find(r => r.docType === '申请表');
  const contractDoc = report.auditResults.find(r => r.docType === '合同');
  const certDocs = report.auditResults.filter(r => r.docType === '合格证');
  
  // 表格行定义
  const rows = [
    {
      field: '合同编号',
      form: formDoc?.extractedFields?.contracNo || '-',
      contract: contractDoc?.extractedFields?.contractNo || '-',
      result: getContracNoResult(report.auditSummary.contracNo)
    },
    {
      field: '出口国',
      form: formDoc?.extractedFields?.exportCountry || '-',
      contract: contractDoc?.extractedFields?.exportCountry || '-',
      result: getExporterResult(report.auditSummary.exporter)
    },
    {
      field: '进口商（英文）',
      form: formDoc?.extractedFields?.importerEn || '-',
      contract: contractDoc?.extractedFields?.importerEn || '-',
      result: getImporterResult(report.auditSummary.importerEn)
    },
    {
      field: '总金额',
      form: formDoc?.extractedFields?.totalAmount || '-',
      contract: contractDoc?.extractedFields?.totalAmount || '-',
      result: getAmountResult(report.auditSummary.totalAmount)
    },
    {
      field: '总数量',
      form: formDoc?.extractedFields?.totalQuantity || '-',
      contract: contractDoc?.extractedFields?.totalQuantity || '-',
      result: getQuantityResult(report.auditSummary.totalQuantity)
    },
    {
      field: '合格证编号',
      form: formDoc?.extractedFields?.mtcNo || '-',
      contract: certDocs.length > 0 ? certDocs.map(c => c.extractedFields.mtcNo).join(', ') : '-',
      result: getMtcNoResult(report.auditSummary.mtcNo)
    },
    {
      field: '生产商',
      form: formDoc?.extractedFields?.manufacturer || '-',
      contract: certDocs.length > 0 ? certDocs.map(c => c.extractedFields.manufacturer).join(', ') : '-',
      result: getManufacturerResult(report.auditSummary.manufacturer)
    },
    {
      field: '报关口岸',
      form: formDoc?.extractedFields?.customsPort || '-',
      contract: '-',
      result: getCustomsResult(report.auditSummary.exporter)
    },
    {
      field: '盖章情况',
      form: formDoc?.hasStamp ? '已盖章' : '未盖章',
      contract: certDocs.length > 0 
        ? certDocs.map(c => c.hasStamp ? '已盖章' : '未盖章').join(', ')
        : '-',
      result: getStampResult(report.auditSummary.sign)
    }
  ];
  
  // 生成 Markdown 表格 - 按固定顺序显示 9 个检查项，不分类排序
  let markdown = '| 检查项 | 申请表 | 合同/合格证 | 预审结果 |\n';
  markdown += '|--------|--------|-------------|----------|\n';
  
  // 按固定顺序显示所有 9 个检查项
  for (const row of rows) {
    markdown += `| ${row.field} | ${row.form} | ${row.contract} | ${row.result} |\n`;
  }
  
  // 添加整体结果和详细审核说明（表格下面）
  markdown += `\n**整体结果**：${report.auditSummary.reviewResult}\n`;
  
  if (report.auditSummary.reviewDetail) {
    markdown += `\n**详细审核说明**：\n${report.auditSummary.reviewDetail}\n`;
  }
  
  return {
    rows,
    markdown,
    summary: report.auditSummary
  };
}

// 辅助函数：提取各种审核结果
function getContracNoResult(data) {
  if (data?.reviewResult === '通过') return '✅ 通过';
  if (data?.reviewResult === '建议通过，需人工复审') return '⚠️ 建议复审';
  return '❌ 不通过';
}

function getExporterResult(data) {
  if (data?.reviewResult === '通过') return '✅ 通过';
  if (data?.reviewResult === '建议通过，需人工复审') return '⚠️ 建议复审';
  return '❌ 不通过';
}

function getImporterResult(data) {
  if (data?.reviewResult === '通过') return '✅ 通过';
  if (data?.reviewResult === '建议通过，需人工复审') return '⚠️ 建议复审';
  return '❌ 不通过';
}

function getAmountResult(data) {
  if (data?.reviewResult === '通过') return '✅ 通过';
  if (data?.reviewResult === '建议通过，需人工复审') return '⚠️ 建议复审';
  return '❌ 不通过';
}

function getQuantityResult(data) {
  if (data?.reviewResult === '通过') return '✅ 通过';
  if (data?.reviewResult === '建议通过，需人工复审') return '⚠️ 建议复审';
  return '❌ 不通过';
}

function getMtcNoResult(data) {
  if (data?.reviewResult === '通过') return '✅ 通过';
  if (data?.reviewResult === '建议通过，需人工复审') return '⚠️ 建议复审';
  return '❌ 不通过';
}

function getManufacturerResult(data) {
  if (data?.reviewResult === '通过') return '✅ 通过';
  if (data?.reviewResult === '建议通过，需人工复审') return '⚠️ 建议复审';
  return '❌ 不通过';
}

function getCustomsResult(data) {
  if (data?.reviewResult === '通过') return '✅ 通过';
  if (data?.reviewResult === '建议通过，需人工复审') return '⚠️ 建议复审';
  return '❌ 不通过';
}

function getStampResult(data) {
  if (data?.reviewResult === '通过') return '✅ 通过';
  return '❌ 不通过';
}

module.exports = {
  generateTableData
};
