/**
 * mock-data.js — Mock data module for kechuang-collection
 *
 * Provides pre-built sample scientific innovation (科创) lead data for dry-run evaluation.
 * Usage: load this module when --mock flag is detected.
 */

const MOCK_KECHUANG_LEADS = [
  {
    priority: '⭐⭐⭐ 紧急',
    title: '2026年省科学技术奖提名通知',
    source: '省科技厅官网',
    category: '[申报]',
    kpiDimension: '🏆 科技奖',
    kpiWeight: '高',
    issueDate: '2026-06-01',
    deadline: '2026-07-01',
    summary: '2026年度XX省科学技术奖提名工作启动，设自然科学奖、技术发明奖、科技进步奖三类。',
    url: 'https://kjt.example.gov.cn/notice-001',
    score: 18,
    suggestedAction: '立即组织材料，准备提名书'
  },
  {
    priority: '⭐⭐ 重要',
    title: '专精特新中小企业认定办法(2026修订)',
    source: '工信厅官网',
    category: '[政策]',
    kpiDimension: '🏭 资质认定',
    kpiWeight: '高',
    issueDate: '2026-06-05',
    deadline: null,
    summary: '2026年专精特新中小企业认定标准修订，新增数字化水平评价指标。',
    url: 'https://gxt.example.gov.cn/policy-002',
    score: 12,
    suggestedAction: '研究新标准，评估企业达标情况'
  },
  {
    priority: '⭐⭐ 重要',
    title: '2026年重点研发计划项目立项公示',
    source: '国家科技部',
    category: '[公示]',
    kpiDimension: '📋 项目立项',
    kpiWeight: '高',
    issueDate: '2026-06-10',
    deadline: null,
    summary: '2026年度重点研发计划项目立项清单公示，涵盖人工智能、量子信息、生物医药等领域。',
    url: 'https://most.gov.cn/project-003',
    score: 10,
    suggestedAction: '分析立项方向，调整研发规划'
  },
  {
    priority: '⭐⭐ 重要',
    title: '2026年度高新技术企业认定申报指南',
    source: '科技厅/财政厅',
    category: '[申报]',
    kpiDimension: '🏭 资质认定',
    kpiWeight: '高',
    issueDate: '2026-06-08',
    deadline: '2026-08-15',
    summary: '2026年高新技术企业认定工作启动，首次认定和重新认定均适用。',
    url: 'https://kjt.example.gov.cn/gaoxin-004',
    score: 14,
    suggestedAction: '确认企业高企资格有效期，准备续期或首次申报'
  },
  {
    priority: '⭐ 关注',
    title: 'XX公司与XX大学共建AI联合实验室',
    source: '36氪',
    category: '[动态]',
    kpiDimension: '🤝 产学研合作',
    kpiWeight: '低',
    issueDate: '2026-06-09',
    deadline: null,
    summary: 'XX公司与XX大学宣布共建人工智能联合实验室，聚焦大模型应用研究。',
    url: 'https://36kr.com/p/ai-lab-005',
    score: 4,
    suggestedAction: '关注合作模式，可作为产学研合作参考'
  },
  {
    priority: '⭐ 关注',
    title: '2026年团体标准征集通知',
    source: '行业协会',
    category: '[申报]',
    kpiDimension: '📐 标准制定',
    kpiWeight: '中',
    issueDate: '2026-06-03',
    deadline: '2026-09-30',
    summary: '2026年团体标准制定计划征集，涵盖AI、大数据、云计算等领域。',
    url: 'https://example-assoc.org/standard-006',
    score: 7,
    suggestedAction: '评估是否参与标准制定'
  }
];

const MOCK_KPI_STATS = {
  '🏆 科技奖': { count: 1, weight: 'high' },
  '🏭 资质认定': { count: 2, weight: 'high' },
  '📋 项目立项': { count: 1, weight: 'high' },
  '🤝 产学研合作': { count: 1, weight: 'low' },
  '📐 标准制定': { count: 1, weight: 'medium' }
};

function getMockScanResults() {
  return MOCK_KECHUANG_LEADS;
}

function getMockReport() {
  return {
    leads: MOCK_KECHUANG_LEADS,
    kpiStats: MOCK_KPI_STATS,
    urgentCount: 1,
    importantCount: 3,
    watchCount: 2,
    generatedAt: new Date().toISOString()
  };
}

module.exports = { getMockScanResults, getMockReport, MOCK_KECHUANG_LEADS };