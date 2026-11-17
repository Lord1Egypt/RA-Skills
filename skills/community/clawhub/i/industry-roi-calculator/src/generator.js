#!/usr/bin/env node

// ============================================================
// industry-roi-calculator — Core calculation engine
// ============================================================

// ---- Industry benchmarks ----

const SALARY_BENCHMARKS = {
  '政府':  { '客服': [8, 12], '知识管理': [12, 18], '数据分析': [15, 22], '内容生成': [10, 15], '流程自动化': [10, 15], '培训': [8, 12], '合规': [12, 18] },
  '零售':  { '客服': [6, 10], '知识管理': [10, 15], '数据分析': [12, 18], '内容生成': [8, 12], '流程自动化': [8, 12], '培训': [7, 11], '合规': [10, 15] },
  '制造':  { '客服': [7, 11], '知识管理': [11, 16], '数据分析': [14, 20], '内容生成': [9, 14], '流程自动化': [10, 14], '培训': [8, 12], '合规': [11, 16] },
  '金融':  { '客服': [10, 16], '知识管理': [15, 25], '数据分析': [18, 30], '内容生成': [12, 18], '流程自动化': [12, 18], '培训': [10, 15], '合规': [18, 30] },
  '教育':  { '客服': [6, 10], '知识管理': [9, 14], '数据分析': [12, 18], '内容生成': [7, 11], '流程自动化': [8, 12], '培训': [6, 10], '合规': [9, 14] },
  '医疗':  { '客服': [8, 12], '知识管理': [12, 18], '数据分析': [15, 22], '内容生成': [9, 14], '流程自动化': [10, 14], '培训': [8, 12], '合规': [12, 18] },
  '能源':  { '客服': [8, 12], '知识管理': [12, 18], '数据分析': [15, 22], '内容生成': [9, 14], '流程自动化': [10, 15], '培训': [8, 12], '合规': [15, 22] },
  '互联网': { '客服': [10, 16], '知识管理': [14, 22], '数据分析': [18, 28], '内容生成': [12, 18], '流程自动化': [12, 18], '培训': [10, 15], '合规': [14, 22] },
};

// Default fallback if industry not in benchmark
const DEFAULT_SALARY = [8, 16];

const AI_COST_BENCHMARKS = {
  small:  { light: [5, 15],  medium: [20, 40],  heavy: [50, 80] },
  medium: { light: [10, 30], medium: [40, 80],  heavy: [80, 150] },
  large:  { light: [20, 50], medium: [80, 150], heavy: [150, 300] },
};

const EFFICIENCY_BENCHMARKS = {
  '政府':  { '客服': [0.20, 0.35], '知识管理': [0.15, 0.25], '数据分析': [0.15, 0.25], '内容生成': [0.25, 0.40], '流程自动化': [0.20, 0.30], '培训': [0.15, 0.25], '合规': [0.15, 0.25] },
  '零售':  { '客服': [0.25, 0.40], '知识管理': [0.15, 0.25], '数据分析': [0.15, 0.25], '内容生成': [0.25, 0.40], '流程自动化': [0.20, 0.30], '培训': [0.15, 0.25], '合规': [0.15, 0.20] },
  '制造':  { '客服': [0.20, 0.30], '知识管理': [0.20, 0.30], '数据分析': [0.15, 0.25], '内容生成': [0.20, 0.35], '流程自动化': [0.20, 0.30], '培训': [0.15, 0.25], '合规': [0.15, 0.25] },
  '金融':  { '客服': [0.20, 0.35], '知识管理': [0.15, 0.25], '数据分析': [0.15, 0.25], '内容生成': [0.20, 0.30], '流程自动化': [0.20, 0.30], '培训': [0.15, 0.25], '合规': [0.15, 0.25] },
  '教育':  { '客服': [0.20, 0.35], '知识管理': [0.15, 0.25], '数据分析': [0.15, 0.25], '内容生成': [0.30, 0.50], '流程自动化': [0.20, 0.30], '培训': [0.20, 0.30], '合规': [0.10, 0.20] },
  '医疗':  { '客服': [0.20, 0.30], '知识管理': [0.15, 0.25], '数据分析': [0.15, 0.25], '内容生成': [0.20, 0.35], '流程自动化': [0.20, 0.30], '培训': [0.15, 0.25], '合规': [0.15, 0.25] },
  '能源':  { '客服': [0.20, 0.30], '知识管理': [0.15, 0.25], '数据分析': [0.15, 0.25], '内容生成': [0.20, 0.35], '流程自动化': [0.20, 0.30], '培训': [0.15, 0.25], '合规': [0.15, 0.25] },
  '互联网': { '客服': [0.20, 0.35], '知识管理': [0.15, 0.25], '数据分析': [0.15, 0.25], '内容生成': [0.30, 0.50], '流程自动化': [0.20, 0.30], '培训': [0.15, 0.25], '合规': [0.15, 0.25] },
};

// Default efficiency ranges if not found
const DEFAULT_EFFICIENCY = [0.15, 0.30];

// ---- Quality improvement benchmarks ----
const QUALITY_BENCHMARKS = {
  '政府':  { '客服': [0.10, 0.20], '知识管理': [0.10, 0.18], '合规': [0.15, 0.25] },
  '零售':  { '客服': [0.15, 0.25], '知识管理': [0.10, 0.18], '内容生成': [0.10, 0.18] },
  '制造':  { '知识管理': [0.15, 0.25], '数据分析': [0.10, 0.20], '合规': [0.15, 0.25] },
  '金融':  { '合规': [0.20, 0.35], '客服': [0.12, 0.20], '风控': [0.15, 0.25] },
  '教育':  { '内容生成': [0.10, 0.20], '知识管理': [0.10, 0.18] },
  '医疗':  { '知识管理': [0.15, 0.25], '客服': [0.10, 0.18] },
  '能源':  { '知识管理': [0.12, 0.20], '合规': [0.15, 0.25] },
  '互联网': { '内容生成': [0.10, 0.20], '知识管理': [0.10, 0.18] },
};
const DEFAULT_QUALITY = [0.10, 0.20];

// ---- Case references (de-identified) ----
const CASE_REFERENCES = {
  '政府': {
    '客服': { title: '某省会城市 12345 政务热线智能化改造', metric: '工单处理时效提升 32%，人力投入减少 28%', reusable: '先做高频场景覆盖（占工单量 60% 的前 20 类），再扩展到长尾。知识库清洗比模型选择更重要。' },
    '知识管理': { title: '某省级政务知识库建设', metric: '知识检索命中率从 42% 提升至 78%，内部培训周期缩短 40%', reusable: '知识源标准化是关键，非结构化文档占比 >50% 时需先做知识治理。' },
    '合规': { title: '某市数据合规自动化审查', metric: '审查周期从 5 个工作日缩短至 1 天，漏审率下降 60%', reusable: '合规场景需保留人工复核节点，AI 做初筛而非终判。' },
  },
  '零售': {
    '客服': { title: '某全国连锁零售客服智能化', metric: '首次响应时间从 3 分钟降至 15 秒，人工坐席工作量减少 35%', reusable: '客服场景 ROI 最高的是「高频简单问题」自动化，复杂转人工。先跑通 Top-20 问题覆盖。' },
    '知识管理': { title: '某零售企业产品知识库建设', metric: '新品上线培训周期从 2 周缩短至 3 天，一线查询成功率提升 45%', reusable: '零售知识库要对接 ERP/商品系统，否则知识更新跟不上上新节奏。' },
    '内容生成': { title: '某电商商品描述自动化生成', metric: '商品上架周期缩短 60%，内容一致性提升', reusable: '需要品牌 tone-of-voice 模板，否则 AI 生成内容调性不统一。' },
  },
  '制造': {
    '知识管理': { title: '某制造企业设备运维知识库', metric: '故障排查平均时间缩短 30%，新员工上手周期从 3 月缩短至 3 周', reusable: '制造业知识分散在老师傅脑子里，需要先做知识萃取工作坊。' },
    '流程自动化': { title: '某制造企业质检流程自动化', metric: '质检效率提升 40%，漏检率下降 50%', reusable: '先选标准化程度最高的产线做 PoC，再横向推广。' },
    '数据分析': { title: '某制造企业生产数据分析助手', metric: '异常检测响应时间从 2 小时缩短至 5 分钟', reusable: '需要打通 MES/ERP 数据源，否则数据孤岛导致 AI 盲区。' },
  },
  '金融': {
    '合规': { title: '某银行合规文档自动化审查', metric: '审查周期缩短 65%，合规风险事件下降 40%', reusable: '金融合规需要可解释性，不能只给结论，要给出判定依据和法规条目。' },
    '客服': { title: '某保险公司智能客服', metric: '首呼解决率提升 25%，人工转接率下降 30%', reusable: '金融客服需严格区分「咨询」和「交易」场景，交易场景 AI 只能辅助不能替代。' },
    '数据分析': { title: '某券商投研数据分析助手', metric: '研报数据整理时间减少 50%', reusable: '投研场景对数据准确性要求极高，需要双人复核机制。' },
  },
  '教育': {
    '内容生成': { title: '某在线教育课程内容自动化生成', metric: '课件制作周期缩短 55%，教师备课时间减少 40%', reusable: '教育内容需要教研团队审核闭环，AI 生成 + 人工审校效率最高。' },
    '知识管理': { title: '某高校教学资源库建设', metric: '教师知识检索成功率从 35% 提升至 72%', reusable: '教育知识跨院系标准化难度大，需要先统一知识分类体系。' },
    '培训': { title: '某教育集团新员工培训智能化', metric: '培训周期缩短 45%，考核通过率提升 20%', reusable: '培训场景最适合「AI 模拟练习 + 真人导师点评」混合模式。' },
  },
  '医疗': {
    '知识管理': { title: '某三甲医院临床知识库建设', metric: '医生文献查阅时间减少 50%，处方合规率提升 25%', reusable: '医疗知识更新快，需要对接最新指南和文献库，否则知识时效性不够。' },
    '客服': { title: '某医院智能导诊系统', metric: '导诊准确率提升至 85%，人工咨询台工作量减少 30%', reusable: '导诊场景必须有明确免责边界，AI 只做分流不做诊断。' },
    '合规': { title: '某医疗集团病历合规审查', metric: '审查效率提升 40%，漏审率下降 55%', reusable: '病历涉及隐私合规，需要本地化部署 + 脱敏处理。' },
  },
  '能源': {
    '知识管理': { title: '某能源企业安全规程知识库', metric: '安全规程查询时间缩短 60%，新员工安全培训周期减少 35%', reusable: '能源行业知识涉及安全红线，AI 输出必须有法规依据引用。' },
    '合规': { title: '某能源企业环保合规自动化', metric: '合规报告生成周期从 2 周缩短至 2 天', reusable: '环保合规需对接政府监管接口，否则数据无法直接用于报告。' },
    '流程自动化': { title: '某能源企业巡检流程智能化', metric: '巡检效率提升 35%，异常发现率提升 50%', reusable: '巡检需考虑离线场景，边缘部署比云端更实用。' },
  },
  '互联网': {
    '内容生成': { title: '某互联网平台营销内容自动化', metric: '内容产出效率提升 3 倍，A/B 测试周期缩短 40%', reusable: '互联网内容生成需要与数据看板打通，否则无法做效果归因。' },
    '知识管理': { title: '某互联网公司技术知识库', metric: '技术问题平均解决时间缩短 35%', reusable: '技术知识更新极快，需要对接代码仓库和工单系统做自动更新。' },
    '数据分析': { title: '某互联网平台运营数据分析', metric: '报表生成时间从 3 天缩短至 2 小时', reusable: '数据分析场景需要先统一指标口径，否则 AI 查询结果不可信。' },
  },
};

// ---- PoC scope recommendations ----
const POC_SUGGESTIONS = {
  '客服': {
    verify: ['首呼解决率（FCR）', '平均响应时间', '人工转接率'],
    exclude: ['复杂投诉处理', '涉及交易的场景', '需人工审批的场景'],
    threshold: 'Top-20 问题覆盖率 ≥ 80%，人工转接率下降 ≥ 20%',
    duration: '2-4 周',
  },
  '知识管理': {
    verify: ['知识检索命中率', '平均查找时间', '知识更新及时率'],
    exclude: ['非结构化文档清洗', '跨系统数据打通', '知识权限体系设计'],
    threshold: '检索命中率 ≥ 70%，查找时间缩短 ≥ 40%',
    duration: '3-6 周',
  },
  '内容生成': {
    verify: ['内容产出效率', '内容一致性评分', '人工审核通过率'],
    exclude: ['品牌调性深度定制', '多语言本地化', '复杂创意内容'],
    threshold: '产出效率提升 ≥ 40%，审核通过率 ≥ 85%',
    duration: '2-4 周',
  },
  '数据分析': {
    verify: ['报表生成时间', '数据查询准确率', '异常检测召回率'],
    exclude: ['数据仓库建设', '实时数据流处理', '跨源数据融合'],
    threshold: '报表生成时间缩短 ≥ 50%，查询准确率 ≥ 90%',
    duration: '3-6 周',
  },
  '流程自动化': {
    verify: ['流程处理效率', '错误率下降幅度', '人工干预率'],
    exclude: ['流程重新设计', '遗留系统改造', '跨部门流程协调'],
    threshold: '处理效率提升 ≥ 30%，错误率下降 ≥ 40%',
    duration: '4-6 周',
  },
  '培训': {
    verify: ['培训周期缩短比例', '考核通过率', '学员满意度'],
    exclude: ['课程体系设计', '讲师培养', '线下实操环节'],
    threshold: '培训周期缩短 ≥ 30%，考核通过率提升 ≥ 15%',
    duration: '2-4 周',
  },
  '合规': {
    verify: ['审查周期缩短比例', '漏审率下降幅度', '合规覆盖率'],
    exclude: ['法规库建设', '合规流程重新设计', '外部审计对接'],
    threshold: '审查周期缩短 ≥ 40%，漏审率下降 ≥ 30%',
    duration: '4-6 周',
  },
};
const DEFAULT_POC = {
  verify: ['核心业务指标提升幅度', '人工介入率下降', '用户满意度'],
  exclude: ['非核心场景', '遗留系统改造', '组织变革管理'],
  threshold: '核心指标提升 ≥ 30%，人工介入率下降 ≥ 20%',
  duration: '4-6 周',
};

// ---- Helper functions ----

function getBenchmark(table, industry, scenario, defaultVal) {
  const industryData = table[industry];
  if (!industryData) return defaultVal;
  const val = industryData[scenario];
  return val || defaultVal;
}

function avgBenchmark(range) {
  return (range[0] + range[1]) / 2;
}

function formatNum(n) {
  if (n === null || n === undefined) return '—';
  return Math.round(n);
}

function formatPct(n) {
  if (n === null || n === undefined) return '—';
  return Math.round(n * 100) + '%';
}

function parseNumber(value) {
  const n = Number.parseFloat(value);
  return Number.isFinite(n) ? n : null;
}

function normalize(value) {
  return (value || '').trim();
}

function assessConfidence(config) {
  let score = 0;
  const missing = [];
  if (config.industry) score += 2; else missing.push('行业');
  if (config.companySize) score += 1; else missing.push('规模');
  if (config.scenario) score += 2; else missing.push('场景');
  if (config.currentCost !== null) score += 2; else missing.push('当前成本');
  if (config.headcount) score += 1; else missing.push('相关人数');
  if (config.avgSalary) score += 1; else missing.push('岗位薪资');
  if (config.painPoints) score += 1;
  if (score >= 8) return 'High';
  if (score >= 5) return 'Medium';
  return 'Low';
}

function estimateCurrentCost(config, salaryRange) {
  const headcount = config.headcount || 0;
  const avgSalary = config.avgSalary || (salaryRange ? avgBenchmark(salaryRange) : null);

  if (config.currentCost !== null && config.currentCost > 0) {
    return config.currentCost;
  }

  if (headcount > 0 && avgSalary) {
    return headcount * avgSalary;
  }

  return null;
}

function estimateAICost(companySize, deploymentLevel) {
  const sizeData = AI_COST_BENCHMARKS[companySize] || AI_COST_BENCHMARKS.medium;
  const level = deploymentLevel || 'medium';
  const range = sizeData[level];
  if (!range) return null;
  return { min: range[0], max: range[1], estimate: avgBenchmark(range) };
}

function estimateEfficiencyGain(industry, scenario) {
  const range = getBenchmark(EFFICIENCY_BENCHMARKS, industry, scenario, DEFAULT_EFFICIENCY);
  return { min: range[0], max: range[1], estimate: avgBenchmark(range) };
}

function estimateQualityGain(industry, scenario) {
  const range = getBenchmark(QUALITY_BENCHMARKS, industry, scenario, DEFAULT_QUALITY);
  return { min: range[0], max: range[1], estimate: avgBenchmark(range) };
}

function getCaseReference(industry, scenario) {
  const industryCases = CASE_REFERENCES[industry];
  if (!industryCases) return null;
  return industryCases[scenario] || null;
}

function getPocSuggestions(scenario) {
  return POC_SUGGESTIONS[scenario] || DEFAULT_POC;
}

// ---- Main calculation ----

function calculateROI(config) {
  const salaryRange = getBenchmark(SALARY_BENCHMARKS, config.industry, config.scenario, DEFAULT_SALARY);

  // Current cost
  const currentCost = estimateCurrentCost(config, salaryRange);
  const implicitCost = currentCost ? currentCost * 0.15 : null; // 15% implicit cost
  const totalCurrentCost = (currentCost !== null && implicitCost !== null) ? currentCost + implicitCost : null;

  // AI cost
  const aiCost = estimateAICost(config.companySize, config.deploymentLevel);

  // Efficiency gain (in monetary terms)
  const effGain = estimateEfficiencyGain(config.industry, config.scenario);
  const effGainAmount = currentCost ? currentCost * effGain.estimate : null;

  // Quality gain (estimated as % of implicit cost avoided)
  const qualGain = estimateQualityGain(config.industry, config.scenario);
  const qualGainAmount = implicitCost ? implicitCost * qualGain.estimate : null;

  // Total benefit
  const totalBenefit = ((effGainAmount || 0) + (qualGainAmount || 0));

  // ROI
  const aiCostEstimate = aiCost ? aiCost.estimate : null;
  const roi = (aiCostEstimate && aiCostEstimate > 0 && totalBenefit > 0)
    ? (totalBenefit - aiCostEstimate) / aiCostEstimate
    : null;

  // Payback period (months)
  const monthlyNet = (totalBenefit && aiCostEstimate) ? (totalBenefit - aiCostEstimate) / 12 : null;
  const paybackMonths = (monthlyNet && monthlyNet > 0 && aiCostEstimate)
    ? Math.round(aiCostEstimate / monthlyNet)
    : null;

  // Confidence
  const confidence = assessConfidence(config);

  // Risk: ROI anomaly check
  const isAnomaly = roi !== null && roi > 5;

  return {
    currentCost,
    implicitCost,
    totalCurrentCost,
    aiCost,
    efficiencyGain: effGain,
    efficiencyGainAmount: effGainAmount,
    qualityGain: qualGain,
    qualityGainAmount: qualGainAmount,
    totalBenefit,
    roi,
    paybackMonths,
    confidence,
    isAnomaly,
  };
}

// ---- Report generation ----

function generateReport(config) {
  const result = calculateROI(config);
  const poc = getPocSuggestions(config.scenario);
  const caseRef = getCaseReference(config.industry, config.scenario);
  const lines = [];

  lines.push('## 行业化 ROI 测算卡');
  lines.push('');

  // Section 1: ROI Card
  lines.push('### 核心指标');
  lines.push(`- 现状年化成本：${result.totalCurrentCost !== null ? formatNum(result.totalCurrentCost) + ' 万元/年' : '（需补充当前成本数据）'}`);
  lines.push(`- AI 方案成本：${result.aiCost ? formatNum(result.aiCost.estimate) + ' 万元/年（范围：' + formatNum(result.aiCost.min) + '-' + formatNum(result.aiCost.max) + '）' : '（需确认部署级别）'}`);
  lines.push(`- 可量化收益：${result.totalBenefit !== null ? formatNum(result.totalBenefit) + ' 万元/年' : '—'}`);
  const roiDisplay = result.roi !== null
    ? (result.roi < 0.5
      ? result.roi.toFixed(2) + 'x（⚠️ ROI 偏低，投入可能超过可量化收益，建议补充隐性收益评估或缩小方案范围）'
      : result.roi.toFixed(1) + 'x')
    : '（无法计算，输入不足）';
  lines.push(`- ROI：${roiDisplay}`);
  const paybackDisplay = result.paybackMonths !== null
    ? (result.paybackMonths > 36 ? result.paybackMonths + ' 个月（⚠️ 回本周超过 3 年，需重新评估方案投入或扩大收益范围）' : result.paybackMonths + ' 个月')
    : '（无法计算）';
  lines.push(`- 回本周期：${paybackDisplay}`);
  lines.push(`- 置信度：${result.confidence}`);
  if (result.isAnomaly) {
    lines.push('- ⚠️ 异常值警告：ROI > 5x，需进一步验证输入数据的准确性');
  }
  lines.push('');

  // Cost breakdown
  lines.push('### 成本拆解');
  if (result.currentCost !== null) {
    const headcount = config.headcount || '—';
    const avgSal = result.currentCost && config.headcount ? (result.currentCost / config.headcount).toFixed(1) : '—';
    lines.push(`- 人力成本：${formatNum(result.currentCost)} 万元/年（${headcount} 人 × ${avgSal} 万元/人）`);
  } else {
    lines.push('- 人力成本：（未提供当前成本或人数）');
  }
  lines.push(`- 隐性成本：${result.implicitCost !== null ? formatNum(result.implicitCost) + ' 万元/年（效率损失、流失、合规风险等，按人力成本 15% 估算）' : '—'}`);
  lines.push('');

  // Benefit breakdown
  lines.push('### 收益拆解');
  lines.push(`- 效率提升：${result.efficiencyGainAmount !== null ? formatNum(result.efficiencyGainAmount) + ' 万元/年（效率提升 ' + formatPct(result.efficiencyGain.estimate) + '，范围 ' + formatPct(result.efficiencyGain.min) + '-' + formatPct(result.efficiencyGain.max) + '）' : '—'}`);
  lines.push(`- 质量提升：${result.qualityGainAmount !== null ? formatNum(result.qualityGainAmount) + ' 万元/年（质量提升 ' + formatPct(result.qualityGain.estimate) + '，范围 ' + formatPct(result.qualityGain.min) + '-' + formatPct(result.qualityGain.max) + '）' : '—'}`);
  lines.push('');

  // Section 2: PoC scope
  lines.push('## PoC 范围建议');
  lines.push(`- **PoC 验证指标**：${poc.verify.join('、')}`);
  lines.push(`- **PoC 排除范围**：${poc.exclude.join('、')}`);
  lines.push(`- **成功门槛**：${poc.threshold}`);
  lines.push(`- **建议时长**：${poc.duration}`);
  lines.push('');

  // Section 3: Risk assumptions
  lines.push('## 风险假设');
  // Data risk
  const dataRisks = ['知识管理', '内容生成', '客服'].includes(config.scenario);
  lines.push(`- **数据风险**：${dataRisks ? '知识库质量直接影响效果。非结构化文档占比高时需先做知识治理。建议 PoC 前完成 Top-20 高频场景知识清洗。' : '数据源可用性需评估，建议梳理现有数据结构。'}`);
  lines.push(`- **集成风险**：${config.scenario === '流程自动化' ? '需评估与现有系统（ERP/MES/CRM）对接复杂度。建议 PoC 阶段先选单一系统做集成验证。' : '需评估与现有工作流工具的集成，建议明确 API 可用性。'}`);
  lines.push(`- **组织风险**：一线人员接受度是关键变量。建议配套培训计划，且将 AI 使用率纳入 KPI。`);
  const complianceRisks = ['金融', '医疗', '政府', '能源'].includes(config.industry);
  lines.push(`- **合规风险**：${complianceRisks ? config.industry + '行业有严格的合规要求，AI 输出需保留人工复核节点。建议 PoC 阶段同步验证合规审查流程。' : '需确认是否有行业特有合规要求，避免上线后返工。'}`);
  lines.push(`- **测算偏差**：${result.confidence === 'Low' ? '输入信息不完整，ROI 测算偏差范围可达 ±50%。建议补充当前成本和人数后再评估。' : result.confidence === 'Medium' ? '输入信息部分完整，ROI 测算偏差范围约 ±30%。' : '输入信息较完整，ROI 测算偏差范围约 ±15-20%。'}`);
  lines.push('');

  // Section 4: Case reference
  lines.push('## 案例参考');
  if (caseRef) {
    lines.push(`- **行业标杆**：${caseRef.title}`);
    lines.push(`- **关键指标**：${caseRef.metric}`);
    lines.push(`- **可复用经验**：${caseRef.reusable}`);
  } else {
    lines.push(`- 暂无 ${config.industry}+${config.scenario} 的精确匹配案例，建议参考同类场景标杆`);
  }
  lines.push('');

  // Section 5: Next step
  lines.push('## 下一步');
  const nextSteps = [];
  if (result.confidence === 'Low') {
    nextSteps.push('补充当前成本和相关人数数据，重新生成 ROI 测算卡');
  } else {
    nextSteps.push('将 ROI 测算卡中的核心指标转为 PoC 验收标准');
    nextSteps.push('与客户确认 PoC 范围和成功门槛');
  }
  nextSteps.push('准备内部通关材料：ROI 测算卡 + PoC 范围建议 + 风险假设');
  lines.push(`- **下一步动作**：${nextSteps.join(' → ')}`);
  lines.push('');

  return lines.join('\n');
}

// ---- CLI argument parsing ----

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case '--industry': args.industry = argv[++i]; break;
      case '--company-size': args.companySize = argv[++i]; break;
      case '--scenario': args.scenario = argv[++i]; break;
      case '--current-cost': args.currentCost = parseNumber(argv[++i]); break;
      case '--pain-points': args.painPoints = argv[++i]; break;
      case '--headcount': args.headcount = parseNumber(argv[++i]); break;
      case '--avg-salary': args.avgSalary = parseNumber(argv[++i]); break;
      case '--target-metric': args.targetMetric = argv[++i]; break;
      case '--deal-size': args.dealSize = parseNumber(argv[++i]); break;
      case '--deployment-level': args.deploymentLevel = argv[++i]; break;
    }
  }
  return args;
}

// ---- Entry point ----

function main() {
  const args = parseArgs(process.argv);
  if (!args.industry && !args.scenario && !args.currentCost) {
    console.log('Usage: node cli.js --industry "零售" --company-size "medium" --scenario "客服" --current-cost 100 --headcount 20');
    console.log('');
    console.log('Parameters:');
    console.log('  --industry        行业：政府/零售/制造/金融/教育/医疗/能源/互联网');
    console.log('  --company-size    规模：small/medium/large');
    console.log('  --scenario        场景：客服/知识管理/内容生成/数据分析/流程自动化/培训/合规');
    console.log('  --current-cost    当前成本（万元/年）');
    console.log('  --headcount       相关岗位人数');
    console.log('  --avg-salary      岗位平均年薪（万元）');
    console.log('  --deployment-level 部署级别：light/medium/heavy（默认 medium）');
    console.log('  --pain-points     痛点描述（逗号分隔）');
    console.log('  --target-metric   核心指标');
    console.log('  --deal-size       预计合同量级（万元）');
    process.exit(0);
  }
  console.log(generateReport(args));
}

if (require.main === module) {
  main();
}

module.exports = { calculateROI, generateReport, parseArgs, getBenchmark, assessConfidence };
