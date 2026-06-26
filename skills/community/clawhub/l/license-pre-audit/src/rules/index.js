#!/usr/bin/env node
/**
 * 审核规则总入口
 * 包含 11 条审核规则，每条规则一个独立函数
 */

const ruleStamp = require('./rule-stamp');
const ruleContractNo = require('./rule-contract-no');
const ruleExporter = require('./rule-exporter');
const ruleImporter = require('./rule-importer');
const ruleAmount = require('./rule-amount');
const ruleQuantity = require('./rule-quantity');
const ruleWeight = require('./rule-weight');
const ruleMtcNo = require('./rule-mtc-no');
const ruleManufacturer = require('./rule-manufacturer');
const ruleCustoms = require('./rule-customs');
const ruleSummary = require('./rule-summary');

/**
 * 执行所有审核规则
 * @param {Array} documents - 文档分析结果数组
 * @returns {Object} 审核摘要
 */
function runAllRules(documents) {
  return ruleSummary.generateSummary(documents, {
    ruleStamp,
    ruleContractNo,
    ruleExporter,
    ruleImporter,
    ruleAmount,
    ruleQuantity,
    ruleWeight,
    ruleMtcNo,
    ruleManufacturer,
    ruleCustoms
  });
}

module.exports = {
  runAllRules,
  // 导出单个规则（方便单独测试）
  ruleStamp,
  ruleContractNo,
  ruleExporter,
  ruleImporter,
  ruleAmount,
  ruleQuantity,
  ruleWeight,
  ruleMtcNo,
  ruleManufacturer,
  ruleCustoms,
  ruleSummary
};
