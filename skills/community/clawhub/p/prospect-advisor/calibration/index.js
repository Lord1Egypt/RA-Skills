/**
 * 惠迈校准框架 — 高考志愿填报Skill校准模块
 * 
 * 三级校准设计：
 * - quick:   每次加载时执行，检测基础环境 (<1秒)
 * - standard:首次安装/版本更新时执行，协调测试 (3-5秒)
 * - deep:    用户手动触发，全量测试+优化报告 (10-30秒)
 */

const CALIBRATION_INTERVAL = 30 * 60 * 1000; // 30分钟冷却
let lastCalibrationTime = 0;

/**
 * 快速校准 — 基础环境检测
 */
async function quickCalibration(env) {
  const startTime = Date.now();
  const results = { passed: [], warnings: [], failed: [] };
  
  // 1. API可达性检测
  try {
    const apiOk = await env.checkApi(env.config.model);
    if (apiOk) {
      results.passed.push({ check: 'API可达性', detail: `${env.config.model} 响应正常` });
    } else {
      results.failed.push({ check: 'API可达性', detail: 'API不可达' });
    }
  } catch (e) {
    results.failed.push({ check: 'API可达性', detail: e.message });
  }

  // 2. 数据源检测
  try {
    const dataOk = await env.checkDataSources();
    if (dataOk.complete) {
      results.passed.push({ check: '数据源完整性', detail: `${dataOk.yearCount}年数据可用` });
    } else {
      results.warnings.push({ check: '数据源', detail: `缺少${dataOk.missing}年数据` });
    }
  } catch (e) {
    results.warnings.push({ check: '数据源', detail: `检测异常: ${e.message}` });
  }

  // 3. 模型响应测试
  try {
    const modelOk = await env.testModelResponse();
    if (modelOk) {
      results.passed.push({ check: '模型响应', detail: `响应时间: ${modelOk.latency}ms` });
    }
  } catch (e) {
    results.failed.push({ check: '模型响应', detail: e.message });
  }

  const duration = Date.now() - startTime;
  return {
    level: 'quick',
    duration,
    passed: results.passed.length,
    warnings: results.warnings.length,
    failed: results.failed.length,
    results,
    ok: results.failed.length === 0
  };
}

/**
 * 标准校准 — 环境协调+数据完整性+情绪输出测试
 */
async function standardCalibration(env) {
  const startTime = Date.now();
  const results = { passed: [], warnings: [], failed: [] };

  // 先跑快速校准
  const quickResult = await quickCalibration(env);
  results.passed.push(...quickResult.results.passed);
  results.warnings.push(...quickResult.results.warnings);
  results.failed.push(...quickResult.results.failed);

  if (quickResult.failed > 0) {
    return { 
      level: 'standard', duration: Date.now() - startTime,
      passed: results.passed.length, warnings: results.warnings.length,
      failed: results.failed.length, results,
      ok: false, message: '快速校准未通过，终止标准校准'
    };
  }

  // 4. 已安装Skill兼容性检测
  try {
    const installedSkills = await env.getInstalledSkills();
    if (installedSkills && installedSkills.length > 0) {
      const conflicts = await env.checkSkillConflicts(installedSkills, 'gaokao-advisor');
      if (conflicts.length === 0) {
        results.passed.push({ check: 'Skill兼容性', detail: `与${installedSkills.length}个已安装Skill无冲突` });
      } else {
        conflicts.forEach(c => {
          results.warnings.push({ check: `冲突: ${c.skill}`, detail: c.description, autoFixed: c.autoFixed || false });
        });
      }
    } else {
      results.passed.push({ check: 'Skill兼容性', detail: '无其他Skill，环境纯净' });
    }
  } catch (e) {
    results.warnings.push({ check: 'Skill兼容性', detail: `检测异常: ${e.message}` });
  }

  // 5. 温情模式输出测试
  try {
    const warmTest = await env.testWarmMode();
    if (warmTest.pass) {
      results.passed.push({ check: '温情模式', detail: '输出含鼓励+建议+方案，符合标准' });
    } else {
      results.failed.push({ check: '温情模式', detail: '输出不符合温情标准' });
    }
  } catch (e) {
    results.failed.push({ check: '温情模式', detail: e.message });
  }

  // 6. 边界场景测试
  try {
    const boundaryTests = await env.runBoundaryTests();
    const boundaryPass = boundaryTests.filter(t => t.pass).length;
    const boundaryFail = boundaryTests.filter(t => !t.pass).length;
    if (boundaryFail === 0) {
      results.passed.push({ check: '边界测试', detail: `${boundaryPass}/${boundaryTests.length} 通过` });
    } else {
      results.failed.push({ check: '边界测试', detail: `${boundaryFail}个场景未通过` });
    }
  } catch (e) {
    results.failed.push({ check: '边界测试', detail: e.message });
  }

  return {
    level: 'standard',
    duration: Date.now() - startTime,
    passed: results.passed.length,
    warnings: results.warnings.length,
    failed: results.failed.length,
    results,
    ok: results.failed.length <= 1
  };
}

/**
 * 深度校准 — 全量测试+性能基线+调优建议（用户手动触发）
 */
async function deepCalibration(env) {
  const startTime = Date.now();
  const results = { passed: [], warnings: [], failed: [] };
  const optimizations = [];

  // 先跑标准校准
  const standardResult = await standardCalibration(env);
  results.passed.push(...standardResult.results.passed);
  results.warnings.push(...standardResult.results.warnings);
  results.failed.push(...standardResult.results.failed);

  // 7. 全量20个标准测试用例
  try {
    const testCases = await env.loadTestCases();
    let casePass = 0, caseFail = 0;
    for (const testCase of testCases) {
      const result = await env.runTestCase(testCase);
      if (result.pass) casePass++;
      else {
        caseFail++;
        results.failed.push({ check: `用例: ${testCase.name}`, detail: `预期: ${testCase.expected}, 实际: ${result.actual}` });
      }
    }
    const passRate = (casePass / testCases.length) * 100;
    if (passRate >= 80) {
      results.passed.push({ check: '全量测试', detail: `${casePass}/${testCases.length} 通过 (${passRate.toFixed(1)}%)` });
    } else {
      results.failed.push({ check: '全量测试', detail: `通过率 ${passRate.toFixed(1)}% < 80%` });
    }
    // 优化建议
    if (passRate >= 80 && passRate < 95) {
      optimizations.push({ type: 'accuracy', suggestion: '可考虑增加测试用例或调整模型温度参数' });
    }
  } catch (e) {
    results.failed.push({ check: '全量测试', detail: e.message });
  }

  // 8. 性能基线
  try {
    const perf = await env.benchmark();
    results.passed.push({ check: '性能基线', detail: `平均响应: ${perf.avgLatency}ms, 上下文使用: ${perf.contextUsage}%` });
    if (perf.avgLatency > 2000) {
      optimizations.push({ type: 'performance', suggestion: `响应时间 ${perf.avgLatency}ms 偏高，建议优化模型选择` });
    }
    if (perf.contextUsage > 90) {
      optimizations.push({ type: 'context', suggestion: `上下文使用率 ${perf.contextUsage}% 过高，建议限制对话轮次` });
    }
  } catch (e) {
    results.failed.push({ check: '性能基线', detail: e.message });
  }

  // 9. 裂变逻辑验证
  try {
    const pricingOk = await env.verifyPricing();
    if (pricingOk.valid) {
      results.passed.push({ check: '裂变逻辑', detail: `${pricingOk.tierCount}级套餐计费计算正确` });
    } else {
      results.failed.push({ check: '裂变逻辑', detail: pricingOk.error });
    }
  } catch (e) {
    results.warnings.push({ check: '裂变逻辑', detail: `验证异常: ${e.message}` });
  }

  return {
    level: 'deep',
    duration: Date.now() - startTime,
    passed: results.passed.length,
    warnings: results.warnings.length,
    failed: results.failed.length,
    results,
    optimizations,
    ok: results.failed.length <= 2
  };
}

/**
 * 校准程序入口 — 自动判断执行级别
 */
async function runCalibration(env, level = 'auto') {
  // 冷却检测
  const now = Date.now();
  if (level !== 'deep' && now - lastCalibrationTime < CALIBRATION_INTERVAL) {
    return { skipped: true, reason: `冷却中 (剩余 ${Math.ceil((CALIBRATION_INTERVAL - (now - lastCalibrationTime)) / 60000)} 分钟)` };
  }

  // 级别选择
  if (level === 'auto') {
    const config = env.config || {};
    if (config.firstInstall) level = 'standard';
    else if (config.versionUpdated) level = 'standard';
    else level = 'quick';
  }

  let result;
  switch (level) {
    case 'deep': result = await deepCalibration(env); break;
    case 'standard': result = await standardCalibration(env); break;
    default: result = await quickCalibration(env); break;
  }

  lastCalibrationTime = now;
  
  // 生成报告
  result.report = generateReport(result, level);
  return result;
}

/**
 * 生成可读报告
 */
function generateReport(result, level) {
  const emoji = result.ok ? '✅' : '⚠️';
  const levelNames = { quick: '快速校准', standard: '标准校准', deep: '深度校准' };
  
  let report = `${emoji} 惠迈校准报告 — ${levelNames[level] || level}\n`;
  report += `├── 环境检测: ${result.passed > 0 ? `✅ ${result.passed}项通过` : '—'}\n`;
  
  if (result.warnings > 0) {
    report += `├── 兼容性: ⚠️ ${result.warnings}个注意点\n`;
    result.results.warnings.forEach(w => {
      report += `│   └─ ${w.check}: ${w.detail}\n`;
    });
  }
  
  if (result.failed > 0) {
    report += `├── 问题: 🔴 ${result.failed}项未通过\n`;
    result.results.failed.forEach(f => {
      report += `│   └─ ${f.check}: ${f.detail}\n`;
    });
  }
  
  report += `├── 耗时: ${result.duration}ms\n`;
  
  if (result.optimizations && result.optimizations.length > 0) {
    report += `└── 优化建议:\n`;
    result.optimizations.forEach(o => {
      report += `    └─ ${o.suggestion}\n`;
    });
  }
  
  return report;
}

module.exports = { runCalibration, quickCalibration, standardCalibration, deepCalibration };
