#!/usr/bin/env node
/**
 * 混合模式盖章检测工具
 * LLM 优先 + OCR 关键词校准
 */

/**
 * 混合模式盖章检测：LLM 优先 + OCR/PDF 辅助校准
 * 检测关键词：盖章、公章、印章、seal、stamp、signature、质检章、合同章等
 * 
 * @param {string} text - 文档文本内容
 * @param {string} docType - 文档类型（合同/合格证/申请表/未知）
 * @param {string} filename - 文件名
 * @returns {boolean} 是否检测到盖章
 */
function detectStampByKeywords(text, docType, filename) {
  console.error('    → [DEBUG] detectStampByKeywords 入口:');
  console.error('    → [DEBUG]   filename:', filename);
  console.error('    → [DEBUG]   docType:', docType);
  console.error('    → [DEBUG]   text 长度:', text ? text.length : 0);
  if (text && text.length > 0) {
    console.error('    → [DEBUG]   text 前 150 字符:', text.substring(0, 150).replace(/\n/g, ' '));
  }
  
  // 特殊情况：根据文件名判断
  if (filename) {
    const fileNameLower = filename.toLowerCase();
    // 营业执照、许可证等文件通常是盖章的
    if (fileNameLower.includes('营业执照') || fileNameLower.includes('license') || 
        fileNameLower.includes('business') || fileNameLower.includes('permit')) {
      console.error('    → 营业执照/许可证检测：根据文件名和经验，判定为已盖章');
      return true;
    }
    // PI、Invoice、装箱单等贸易单据通常有签字或印章
    if (fileNameLower.includes('pi') || fileNameLower.includes('invoice') || 
        fileNameLower.includes('packing') || fileNameLower.includes('装箱单')) {
      if (!text || text.trim().length < 10) {
        console.error('    → 贸易单据检测：纯图片 PDF，根据经验判定为已签字/盖章');
        return true;
      }
    }
  }
  
  // 如果文本为空或极短，且不是上述特殊文件，返回 false
  if (!text || text.trim().length < 10) {
    return false;
  }

  const textLower = text.toLowerCase();
  
  // 忽略空格差异的关键词匹配
  function containsWithSpaceTolerance(text, keyword) {
    const pattern = keyword.split('').join('\s*');
    const regex = new RegExp(pattern, 'i');
    return regex.test(text);
  }
  
  // 根据文件名推断文档类型
  const fileNameLower = filename ? filename.toLowerCase() : '';
  const effectiveDocType = docType && docType !== '未知' ? docType : 
    (fileNameLower.includes('营业执照') || fileNameLower.includes('license') ? '营业执照' :
    fileNameLower.includes('pi') || fileNameLower.includes('invoice') ? '发票' :
    fileNameLower.includes('合格证') || fileNameLower.includes('certificate') ? '合格证' :
    fileNameLower.includes('合同') || fileNameLower.includes('contract') ? '合同' :
    '其他');

  // 合同/发票/PI：查找最后一页附近的盖章关键词
  if (effectiveDocType === '合同' || effectiveDocType === '发票' || effectiveDocType === '装箱单' || fileNameLower.includes('pi') || fileNameLower.includes('invoice')) {
    const lastPageKeywords = ['卖方', '买方', 'exporter', 'importer', 'signature', 'seal', '盖章', '公章', 'seller', 'buyer', 'authorized', 'date'];
    const lastText = text.split('\n').slice(-80).join('\n').toLowerCase();
    const matchCount = lastPageKeywords.filter(k => lastText.includes(k.toLowerCase())).length;
    if (matchCount >= 2) {
      console.error(`    → ${effectiveDocType}盖章检测：在末尾发现 ${matchCount} 个关键词，判定为已盖章`);
      return true;
    }
    
    const hasCompany = /company|limited|ltd|co\.?\.?|corporation|股份有限公司 | 有限公司/.test(textLower);
    const hasSignatureArea = /signature|签字|seal|盖章|date|日期/.test(textLower);
    if (hasCompany && hasSignatureArea) {
      console.error(`    → ${effectiveDocType}盖章检测：发现公司名称和签字栏，判定为已盖章`);
      return true;
    }
  }

  // 申请表：查找中间或角落的盖章关键词
  if (effectiveDocType === '申请表') {
    const hasProvince = containsWithSpaceTolerance(textLower, '江苏') || containsWithSpaceTolerance(textLower, '浙江') ||
      containsWithSpaceTolerance(textLower, '广东') || containsWithSpaceTolerance(textLower, '上海') ||
      containsWithSpaceTolerance(textLower, '北京') || containsWithSpaceTolerance(textLower, '天津') ||
      containsWithSpaceTolerance(textLower, '河北') || containsWithSpaceTolerance(textLower, '山东') ||
      containsWithSpaceTolerance(textLower, '河南') || containsWithSpaceTolerance(textLower, '湖北') ||
      containsWithSpaceTolerance(textLower, '湖南') || containsWithSpaceTolerance(textLower, '安徽') ||
      containsWithSpaceTolerance(textLower, '江西') || containsWithSpaceTolerance(textLower, '福建') ||
      containsWithSpaceTolerance(textLower, '四川') || containsWithSpaceTolerance(textLower, '重庆') ||
      containsWithSpaceTolerance(textLower, '陕西') || containsWithSpaceTolerance(textLower, '山西') ||
      containsWithSpaceTolerance(textLower, '辽宁') || containsWithSpaceTolerance(textLower, '吉林') ||
      containsWithSpaceTolerance(textLower, '黑龙江') || containsWithSpaceTolerance(textLower, '海南') ||
      containsWithSpaceTolerance(textLower, '云南') || containsWithSpaceTolerance(textLower, '贵州') ||
      containsWithSpaceTolerance(textLower, '广西') || containsWithSpaceTolerance(textLower, '甘肃') ||
      containsWithSpaceTolerance(textLower, '青海') || containsWithSpaceTolerance(textLower, '宁夏') ||
      containsWithSpaceTolerance(textLower, '新疆') || containsWithSpaceTolerance(textLower, '西藏') ||
      containsWithSpaceTolerance(textLower, '内蒙古');
    
    const hasCompanyWord = containsWithSpaceTolerance(textLower, '公司') || containsWithSpaceTolerance(textLower, '有限') ||
      containsWithSpaceTolerance(textLower, '股份') || containsWithSpaceTolerance(textLower, '集团') ||
      containsWithSpaceTolerance(textLower, '厂') || containsWithSpaceTolerance(textLower, '厂址') ||
      containsWithSpaceTolerance(textLower, '厂名');
    
    const hasStampWord = containsWithSpaceTolerance(textLower, '盖章') || containsWithSpaceTolerance(textLower, '公章') ||
      containsWithSpaceTolerance(textLower, '印章') || containsWithSpaceTolerance(textLower, 'seal') ||
      containsWithSpaceTolerance(textLower, 'stamp') || containsWithSpaceTolerance(textLower, '质检') ||
      containsWithSpaceTolerance(textLower, '合格') || containsWithSpaceTolerance(textLower, '检验') ||
      containsWithSpaceTolerance(textLower, '证明') || containsWithSpaceTolerance(textLower, '批复') ||
      containsWithSpaceTolerance(textLower, '发证') || containsWithSpaceTolerance(textLower, '商务厅') ||
      containsWithSpaceTolerance(textLower, '商务部');

    if (hasProvince && hasCompanyWord) {
      console.error(`    → 申请表盖章检测：发现省份和公司词汇（可能含红色印章），判定为已盖章`);
      return true;
    }
    if (hasStampWord) {
      console.error(`    → 申请表盖章检测：发现盖章相关词汇，判定为已盖章`);
      return true;
    }
  }

  // 合格证：通常有质检章
  if (effectiveDocType === '合格证') {
    const certKeywords = ['质检章', '合格证', '检验', 'qualified', 'passed', '盖章', '公章'];
    const matchCount = certKeywords.filter(k => containsWithSpaceTolerance(textLower, k)).length;
    if (matchCount >= 1) {
      console.error(`    → 合格证盖章检测：发现 ${matchCount} 个关键词，判定为已盖章`);
      return true;
    }
  }

  // 通用检测：如果文本中包含明显的盖章描述
  const generalStampPattern = /(盖章 | 公章 | 印章|seal|stamp|signature)/i;
  if (generalStampPattern.test(textLower)) {
    console.error(`    → 通用盖章检测：发现盖章关键词，判定为已盖章`);
    return true;
  }

  return false;
}

module.exports = {
  detectStampByKeywords
};
