#!/usr/bin/env node
/**
 * 合并报告技能入口脚本
 * 用法：node merge-reports.js <询盘单号>
 *
 * 功能：合并询盘报告和 OKKI 背调报告，生成完整汇总（自包含模式）
 * 依赖：需要先运行 run-analysis.js 和 run-okki.js 生成报告
 */

const fs = require('fs');
const path = require('path');

// ============ 路径查找逻辑（自包含模式） ============
/**
 * 查找工作目录
 * 查找顺序：
 * 1. 当前脚本所在目录的上级目录（自包含模式）
 * 2. 环境变量 INQUIRY_ANALYZER_PATH
 */
function findWorkingDir() {
  const currentDir = __dirname;
  const parentDir = path.dirname(currentDir);

  // 1. 自包含模式：上级目录
  if (fs.existsSync(path.join(parentDir, 'inquiry-analyzer.js'))) {
    return parentDir;
  }

  // 2. 环境变量
  if (process.env.INQUIRY_ANALYZER_PATH) {
    if (fs.existsSync(process.env.INQUIRY_ANALYZER_PATH)) {
      return process.env.INQUIRY_ANALYZER_PATH;
    }
  }

  return null;
}

// ============ 主程序 ============
const targetInquiry = process.argv[2];
if (!targetInquiry) {
  console.error('用法: node merge-reports.js <目标询盘号>');
  console.error('示例: node merge-reports.js 50000126101155');
  process.exit(1);
}

const baseDir = findWorkingDir();
if (!baseDir) {
  console.error('错误: 无法找到工作目录');
  console.error('');
  console.error('请确保 skill 目录包含以下文件：');
  console.error('  - inquiry-analyzer.js');
  console.error('  - okki-background.js');
  process.exit(1);
}

console.log(`使用目录: ${baseDir}`);

const today = new Date().toISOString().slice(0, 10);

// 确保 reports 和 csv-reports 目录存在
const reportsDir = path.join(baseDir, 'reports');
const csvDir = path.join(baseDir, 'csv-reports');
const okkiDir = path.join(baseDir, 'okki-reports');

if (!fs.existsSync(reportsDir)) fs.mkdirSync(reportsDir, { recursive: true });
if (!fs.existsSync(csvDir)) fs.mkdirSync(csvDir, { recursive: true });
if (!fs.existsSync(okkiDir)) fs.mkdirSync(okkiDir, { recursive: true });

// 读取询盘报告
const inquiryFiles = fs.readdirSync(reportsDir)
  .filter(f => f.startsWith(`inquiry-report-${targetInquiry}`) && f.endsWith('.md'));

if (inquiryFiles.length === 0) {
  console.error(`未找到询盘报告: inquiry-report-${targetInquiry}*.md`);
  console.error(`查找目录: ${reportsDir}`);
  process.exit(1);
}

const inquiryFile = path.join(reportsDir, inquiryFiles[0]);
const inquiryReport = fs.readFileSync(inquiryFile, 'utf-8');
const inquiryLines = inquiryReport.split('\n').slice(3).filter(l => l.trim() && l.startsWith('|')).map(l => {
  const parts = l.split('|').map(c => c.trim());
  return {
    id: parts[1],
    month: parts[2],
    date: parts[3],
    responder: parts[4],
    product: parts[5],
    time: parts[6],
    customerType: parts[7],
    totalNew: parts[8],
    country: parts[9],
    name: parts[10],
    level: parts[11]
  };
});

// 读取OKKI报告
const okkiFiles = fs.readdirSync(okkiDir)
  .filter(f => f.startsWith(`okki-report-${targetInquiry}`) && f.endsWith('.md'));

if (okkiFiles.length === 0) {
  console.error(`未找到OKKI背调报告: okki-report-${targetInquiry}*.md`);
  console.error(`查找目录: ${okkiDir}`);
  process.exit(1);
}

const okkiFile = path.join(okkiDir, okkiFiles[0]);
const okkiReport = fs.readFileSync(okkiFile, 'utf-8');
const okkiLines = okkiReport.split('\n').slice(11).filter(l => l.trim() && l.startsWith('|') && !l.includes('询盘单号')).map(l => {
  const parts = l.split('|').map(c => c.trim());
  return {
    id: parts[1],
    okkiName: parts[2],
    okkiCountry: parts[3],
    company: parts[4],
    tags: parts[5],
    analysis: parts[6]
  };
});

// 构建OKKI映射
const okkiMap = {};
okkiLines.forEach(o => {
  okkiMap[o.id] = o;
});

// 合并数据
const merged = inquiryLines.map(inv => {
  const okki = okkiMap[inv.id] || {};

  let name = inv.name;
  if (!name || name === 'Manufacturers' || name === '--') {
    name = okki.okkiName || '';
  }

  let country = inv.country;
  if (!country || country === '--') {
    country = okki.okkiCountry || '';
  }

  return {
    id: inv.id,
    month: inv.month,
    date: inv.date,
    responder: inv.responder,
    product: inv.product,
    time: inv.time,
    customerType: inv.customerType,
    country: country,
    name: name,
    level: inv.level,
    company: okki.company || '',
    tags: okki.tags || '',
    analysis: okki.analysis || ''
  };
});

// 生成MD报告
let md = `# 合并报告

- **目标询盘**：${targetInquiry}
- **生成日期**：${today}
- **询盘总数**：${merged.length}
- **有背调数据**：${merged.filter(m => m.tags && m.tags !== '--' && m.tags !== '').length}

---

## 合并汇总表

| 询盘单号 | 月份 | 登记日期 | 询盘回复人 | 产品型号 | 时间段 | 客户类型 | 国家 | 客户名称 | L几 | 公司 | 标签 | 背调分析 |
|----------|------|----------|------------|----------|--------|----------|------|----------|-----|------|------|----------|
`;

merged.forEach(m => {
  md += `| ${m.id} | ${m.month} | ${m.date} | ${m.responder} | ${m.product} | ${m.time} | ${m.customerType} | ${m.country} | ${m.name} | ${m.level} | ${m.company} | ${m.tags} | ${m.analysis} |\n`;
});

fs.writeFileSync(path.join(reportsDir, `merged-report-${today}.md`), md);

// 生成CSV
const csvHeader = '询盘单号,月份,登记日期,询盘回复人,产品型号,时间段,客户类型,国家,客户名称,L几,公司,标签,背调分析';
const csvRows = merged.map(m => {
  const escapeCsv = s => (s && (s.includes(',') || s.includes('"') || s.includes('\n'))) ? '"' + s.replace(/"/g, '""') + '"' : (s || '');
  return [m.id, m.month, m.date, m.responder, m.product, m.time, m.customerType, m.country, m.name, m.level, escapeCsv(m.company), escapeCsv(m.tags), escapeCsv(m.analysis)].join(',');
});
const csv = [csvHeader, ...csvRows].join('\n');

fs.writeFileSync(path.join(csvDir, `merged-report-${today}.csv`), '\uFEFF' + csv);

console.log('合并报告已生成：');
console.log(`- reports/merged-report-${today}.md`);
console.log(`- csv-reports/merged-report-${today}.csv`);
console.log(`询盘总数：${merged.length}`);
console.log(`有背调数据：${merged.filter(m => m.tags && m.tags !== '--' && m.tags !== '').length}`);
