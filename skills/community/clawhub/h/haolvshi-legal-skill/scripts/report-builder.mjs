import fs from 'node:fs';
import { plainText } from './interaction-normalizer.mjs';

const CONSULTATION_TEMPLATE = fs.readFileSync(
  new URL('../assets/consultation-report.html', import.meta.url),
  'utf8'
);
const CONTRACT_TEMPLATE = fs.readFileSync(
  new URL('../assets/contract-report.html', import.meta.url),
  'utf8'
);

function escapeHtml(value = '') {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function renderTemplate(template, values) {
  return template.replace(/\{\{([A-Z_]+)\}\}/g, (_, key) => values[key] ?? '');
}

export function buildQuestionReportHtml({ title, reportContent, related }) {
  const report = typeof reportContent === 'object'
    ? (reportContent.content || reportContent.report || JSON.stringify(reportContent, null, 2))
    : String(reportContent || '');
  const reportHtml = /<[^>]+>/.test(report)
    ? report
    : `<div class="source">${escapeHtml(report)}</div>`;
  const laws = related?.laws || [];
  const cases = related?.caseList || [];
  const lawHtml = laws.length
    ? `<h2>相关法规</h2><ul>${laws.map(item => `<li>${escapeHtml(item.title || item.name || item.lawName || plainText(JSON.stringify(item)))}</li>`).join('')}</ul>`
    : '';
  const caseHtml = cases.length
    ? `<h2>相似案例</h2><ul>${cases.map(item => `<li>${escapeHtml(item.title || item.name || item.caseName || plainText(JSON.stringify(item)))}</li>`).join('')}</ul>`
    : '';
  return renderTemplate(CONSULTATION_TEMPLATE, {
    TITLE: escapeHtml(title || '法律服务报告'),
    REPORT: reportHtml,
    LAWS: lawHtml,
    CASES: caseHtml
  });
}

function riskLevelClass(level = '') {
  if (/高|重大|严重/i.test(level)) return 'level-high';
  if (/中|一般/i.test(level)) return 'level-medium';
  return 'level-low';
}

export function buildContractReportHtml({ riskPoints = [], standing }) {
  const rows = riskPoints.map((risk, index) => `<tr>
<td>${index + 1}</td>
<td class="${riskLevelClass(risk.riskPointLevel)}">${escapeHtml(risk.riskPointLevel || '未分级')}</td>
<td>${escapeHtml(risk.riskPoint || risk.checkListItem || '')}</td>
<td>${escapeHtml(risk.riskPointDescription || '')}</td>
<td>${escapeHtml(risk.riskPointSolution || risk.replacementText || '')}</td>
</tr>`).join('');
  return renderTemplate(CONTRACT_TEMPLATE, {
    STANDING: standing === 2 ? '乙方' : '甲方',
    RISK_COUNT: String(riskPoints.length),
    RISK_ROWS: rows
  });
}

export function reportSummary(reportContent) {
  const content = typeof reportContent === 'object'
    ? reportContent.content || reportContent.report || JSON.stringify(reportContent)
    : String(reportContent || '');
  return plainText(content).slice(0, 1600);
}
