#!/usr/bin/env node

const { calculateROI, generateReport, parseArgs, getBenchmark, assessConfidence } = require('../src/generator.js');

let passed = 0;
let failed = 0;

function assert(condition, msg) {
  if (condition) {
    passed++;
  } else {
    failed++;
    console.error(`FAIL: ${msg}`);
  }
}

// ---- Test 1: Basic ROI calculation with full input ----
{
  const result = calculateROI({
    industry: '零售',
    companySize: 'medium',
    scenario: '客服',
    currentCost: 120,
    headcount: 15,
    avgSalary: 8,
  });
  assert(result.currentCost === 120, 'currentCost should use provided value');
  assert(result.implicitCost > 0, 'implicitCost should be calculated');
  assert(result.totalCurrentCost > 120, 'totalCurrentCost should include implicit cost');
  assert(result.aiCost !== null, 'aiCost should be calculated for medium company');
  assert(result.efficiencyGainAmount > 0, 'efficiency gain should be positive');
  assert(result.qualityGainAmount > 0, 'quality gain should be positive');
  assert(result.totalBenefit > 0, 'totalBenefit should be positive');
  assert(result.roi !== null, 'ROI should be calculated');
  assert(result.confidence === 'High', 'Full input should yield High confidence');
}

// ---- Test 2: Confidence scoring ----
{
  assert(assessConfidence({ industry: '零售', companySize: 'medium', scenario: '客服', currentCost: 100, headcount: 10, avgSalary: 8 }) === 'High', 'Full input = High');
  assert(assessConfidence({ industry: '零售', scenario: '客服', currentCost: 100 }) === 'Medium', 'Partial input = Medium');
  assert(assessConfidence({}) === 'Low', 'No input = Low');
}

// ---- Test 3: Medium confidence with missing cost ----
{
  const result = calculateROI({
    industry: '金融',
    companySize: 'large',
    scenario: '合规',
    currentCost: null,
  });
  assert(result.confidence === 'Medium', 'Missing currentCost (but has industry+size+scenario) = Medium');
  assert(result.currentCost === null, 'currentCost should be null when not provided');
}

// ---- Test 4: ROI anomaly detection ----
{
  // Very high current cost, small AI cost → anomaly
  const result = calculateROI({
    industry: '金融',
    companySize: 'small',
    scenario: '合规',
    currentCost: 5000,
    headcount: 100,
  });
  assert(result.isAnomaly === true, 'High ROI should trigger anomaly flag');
}

// ---- Test 5: Industry benchmark lookup ----
{
  const salary = getBenchmark(
    { '零售': { '客服': [6, 10] }, '金融': { '客服': [10, 16] } },
    '零售', '客服', [8, 16]
  );
  assert(salary[0] === 6 && salary[1] === 10, 'Should find retail CS salary');

  const fallback = getBenchmark({}, '未知行业', '客服', [8, 16]);
  assert(fallback[0] === 8 && fallback[1] === 16, 'Should return default for unknown industry');
}

// ---- Test 6: Report generation ----
{
  const report = generateReport({
    industry: '零售',
    companySize: 'medium',
    scenario: '客服',
    currentCost: 120,
    headcount: 15,
  });
  assert(report.includes('## 行业化 ROI 测算卡'), 'Report should contain ROI card header');
  assert(report.includes('ROI：'), 'Report should contain ROI value');
  assert(report.includes('## PoC 范围建议'), 'Report should contain PoC suggestions');
  assert(report.includes('## 风险假设'), 'Report should contain risk assumptions');
  assert(report.includes('## 案例参考'), 'Report should contain case reference');
  assert(report.includes('## 下一步'), 'Report should contain next steps');
  assert(report.includes('首呼解决率'), 'Retail CS PoC should mention FCR');
  assert(!report.includes('12345'), 'Should NOT contain 12345 (that\'s gov case, not retail)');
}

// ---- Test 7: Report with missing input ----
{
  const report = generateReport({
    industry: '政府',
    scenario: '合规',
    currentCost: null,
  });
  assert(report.includes('需补充当前成本数据'), 'Should warn about missing cost data');
  assert(report.includes('置信度：Low'), 'Should show Low confidence');
  assert(report.includes('偏差范围可达'), 'Should mention deviation range');
}

// ---- Test 8: CLI argument parsing ----
{
  const args = parseArgs([
    'node', 'cli.js',
    '--industry', '零售',
    '--company-size', 'medium',
    '--scenario', '客服',
    '--current-cost', '100',
    '--headcount', '10'
  ]);
  assert(args.industry === '零售', 'industry parsed');
  assert(args.companySize === 'medium', 'companySize parsed');
  assert(args.scenario === '客服', 'scenario parsed');
  assert(args.currentCost === 100, 'currentCost parsed as number');
  assert(args.headcount === 10, 'headcount parsed as number');
}

// ---- Test 9: PoC suggestions for different scenarios ----
{
  const report = generateReport({
    industry: '制造',
    companySize: 'large',
    scenario: '知识管理',
    currentCost: 200,
    headcount: 30,
  });
  assert(report.includes('知识检索命中率'), 'Knowledge mgmt PoC should mention retrieval rate');
  assert(report.includes('3-6 周'), 'Knowledge mgmt PoC duration should be 3-6 weeks');
}

// ---- Test 10: Anomaly warning in output ----
{
  const report = generateReport({
    industry: '金融',
    companySize: 'small',
    scenario: '合规',
    currentCost: 5000,
    headcount: 100,
  });
  assert(report.includes('异常值'), 'Should include anomaly warning');
}

// ---- Summary ----
console.log(`\nindustry-roi-calculator tests: ${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);
