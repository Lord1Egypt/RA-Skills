/**
 * 场景化示例：节假日值班热点监测
 * 
 * 这是一个使用AI协作操作系统的示例场景
 * 展示如何用原有系统来实现节假日值班热点监测
 * 
 * 注意：这不是一个独立系统，只是演示如何使用原有系统
 * 可以监测任何类型的热点，不限于科技热点
 */

const { AICollaborationSystem } = require('../dist/index');

console.log('\n');
console.log('╔══════════════════════════════════════════════════════════════════════╗');
console.log('║     场景示例：节假日值班热点监测（使用AI协作操作系统）              ║');
console.log('╚══════════════════════════════════════════════════════════════════════╝');
console.log('\n');

// ==================== 使用原有系统 ====================

// 初始化AI协作操作系统
const ai = new AICollaborationSystem('duty_example');

console.log('【说明】');
console.log('─────────────────────────────────────');
console.log('这是一个场景化示例，展示如何使用AI协作操作系统');
console.log('来实现节假日值班热点监测功能。');
console.log('');
console.log('可以监测任何类型的热点：');
console.log('  • 产业热点');
console.log('  • 政策热点');
console.log('  • 社会热点');
console.log('  • 舆情热点');
console.log('  • 任何你关心的热点...');
console.log('');

// ==================== 配置 ====================

// 关注等级配置（可根据需要调整）
const LEVELS = {
  S: { min: 75, desc: '舆论非常火爆，需要立即输出分析材料', color: '🔴' },
  A: { min: 60, desc: '高度关注，需要重点监测', color: '🟠' },
  B: { min: 40, desc: '中等关注，持续跟踪', color: '🟡' },
  C: { min: 0,  desc: '低关注，可忽略', color: '⚪' }
};

// 深度分析触发条件（可根据需要调整）
const ANALYSIS_TRIGGERS = {
  publicAttention: 80,
  discussionVolume: 30000,
  emotionIntensity: 85,
  finalScore: 75
};

// ==================== 核心功能函数 ====================

/**
 * 评估热点等级
 * @param {Object} hotspot 热点信息
 * @returns {Object} 评估结果
 */
function evaluateHotspot(hotspot) {
  // 计算舆论热度
  const attentionScore = (
    (hotspot.publicAttention || 50) * 0.4 +
    ((hotspot.discussionVolume || 0) / 1000) * 0.3 +
    (hotspot.emotionIntensity || 50) * 0.3
  );
  
  // 时间衰减
  const age = hotspot.publishDate ? 
    Math.floor((Date.now() - new Date(hotspot.publishDate)) / (24 * 60 * 60 * 1000)) : 0;
  
  let decayRate = 1.0;
  if (age <= 1) decayRate = 1.0;
  else if (age <= 3) decayRate = 0.9;
  else if (age <= 7) decayRate = 0.7;
  else if (age <= 14) decayRate = 0.4;
  else decayRate = 0.1;
  
  // 最终评分
  const finalScore = Math.round(attentionScore * decayRate);
  
  // 确定等级
  let level = 'C';
  if (finalScore >= 75 && age <= 7) level = 'S';
  else if (finalScore >= 60) level = 'A';
  else if (finalScore >= 40) level = 'B';
  
  // 时间限制
  if (age > 7) level = 'B';
  if (age > 14) level = 'C';
  
  // 是否需要深度分析
  const needAnalysis = (
    (hotspot.publicAttention || 0) >= ANALYSIS_TRIGGERS.publicAttention ||
    (hotspot.discussionVolume || 0) >= ANALYSIS_TRIGGERS.discussionVolume ||
    (hotspot.emotionIntensity || 0) >= ANALYSIS_TRIGGERS.emotionIntensity ||
    finalScore >= ANALYSIS_TRIGGERS.finalScore
  ) && age <= 7;
  
  return {
    ...hotspot,
    finalScore,
    level,
    needAnalysis,
    age,
    decayRate
  };
}

/**
 * 生成日报
 */
function generateDailyReport(hotspots, dutyPersons) {
  const evaluated = hotspots.map(evaluateHotspot);
  const visible = evaluated.filter(h => h.level !== 'C');
  
  // 按等级排序
  visible.sort((a, b) => {
    const order = { 'S': 0, 'A': 1, 'B': 2 };
    return order[a.level] - order[b.level];
  });
  
  // 统计
  const stats = {
    total: hotspots.length,
    S: evaluated.filter(h => h.level === 'S').length,
    A: evaluated.filter(h => h.level === 'A').length,
    B: evaluated.filter(h => h.level === 'B').length,
    needAnalysis: evaluated.filter(h => h.needAnalysis).length
  };
  
  // 生成文本
  let text = `【${new Date().toLocaleDateString('zh-CN')} 热点日报】\n\n`;
  text += `值班人员：${dutyPersons.join('、')}\n\n`;
  
  const sLevel = visible.filter(h => h.level === 'S');
  if (sLevel.length > 0) {
    text += `【S级热点】（需要深度分析）\n`;
    sLevel.forEach(h => {
      text += `🔴 ${h.title}\n`;
      text += `   评分：${h.finalScore} | 来源：${h.source}\n`;
      text += `   ⚠️ 需要输出深度分析材料\n\n`;
    });
  }
  
  const aLevel = visible.filter(h => h.level === 'A');
  if (aLevel.length > 0) {
    text += `【A级热点】（高度关注）\n`;
    aLevel.forEach(h => {
      text += `🟠 ${h.title}\n`;
      text += `   评分：${h.finalScore} | 来源：${h.source}\n\n`;
    });
  }
  
  const bLevel = visible.filter(h => h.level === 'B');
  if (bLevel.length > 0) {
    text += `【B级热点】（持续跟踪）\n`;
    bLevel.forEach(h => {
      text += `🟡 ${h.title}\n`;
      text += `   评分：${h.finalScore}\n\n`;
    });
  }
  
  text += `【今日统计】\n`;
  text += `共监测${stats.total}条热点，S级${stats.S}条，A级${stats.A}条，B级${stats.B}条\n`;
  
  if (stats.needAnalysis > 0) {
    text += `\n【待处理】需要输出分析材料：${stats.needAnalysis}条\n`;
  }
  
  // 存储到记忆系统
  ai.memory.addToL2(
    `日报_${new Date().toLocaleDateString('zh-CN')}`,
    { hotspots: evaluated, stats, dutyPersons },
    'insight',
    4,
    ['daily-report', 'duty'],
    'shared'
  );
  
  return { text, evaluated, stats, visible };
}

// ==================== 示例数据 ====================

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('【示例】监测各类热点');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

// 示例：各类热点（不限类型）
const exampleHotspots = [
  // 政策热点
  {
    title: '新政策发布：支持民营经济发展',
    source: '政府公告',
    type: '政策热点',
    publishDate: new Date(),
    publicAttention: 85,
    discussionVolume: 40000,
    emotionIntensity: 75
  },
  // 社会热点
  {
    title: '某地发生重大事件',
    source: '新闻媒体',
    type: '社会热点',
    publishDate: new Date(),
    publicAttention: 90,
    discussionVolume: 80000,
    emotionIntensity: 95
  },
  // 产业热点
  {
    title: '某行业迎来重大变革',
    source: '行业报告',
    type: '产业热点',
    publishDate: new Date(),
    publicAttention: 65,
    discussionVolume: 15000,
    emotionIntensity: 55
  },
  // 舆情热点
  {
    title: '某企业负面舆情发酵',
    source: '社交媒体',
    type: '舆情热点',
    publishDate: new Date(),
    publicAttention: 88,
    discussionVolume: 60000,
    emotionIntensity: 85
  },
  // 国际热点
  {
    title: '国际重大事件',
    source: '国际新闻',
    type: '国际热点',
    publishDate: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
    publicAttention: 70,
    discussionVolume: 25000,
    emotionIntensity: 60
  },
  // 一周前的热点（会被降级）
  {
    title: '一周前的新闻',
    source: '新闻媒体',
    type: '旧闻',
    publishDate: new Date(Date.now() - 8 * 24 * 60 * 60 * 1000),
    publicAttention: 80,
    discussionVolume: 30000,
    emotionIntensity: 70
  }
];

console.log('监测到的热点（不限类型）：');
exampleHotspots.forEach((h, i) => {
  console.log(`  ${i+1}. [${h.type}] ${h.title}`);
});
console.log('');

// ==================== 评估和生成日报 ====================

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('【评估结果】');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

const evaluated = exampleHotspots.map(evaluateHotspot);

console.log('  类型        标题                    等级  评分   需分析');
console.log('  ─────────────────────────────────────────────────────────────');
evaluated.forEach(h => {
  const type = h.type.substring(0, 4).padEnd(4);
  const title = h.title.substring(0, 14).padEnd(14);
  const icon = { 'S': '🔴', 'A': '🟠', 'B': '🟡', 'C': '⚪' }[h.level];
  console.log(`  ${type}    ${title}  ${icon}${h.level}   ${h.finalScore.toString().padStart(3)}    ${h.needAnalysis ? '是' : '否'}`);
});
console.log('');

// ==================== 生成日报 ====================

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('【生成的日报】');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

const report = generateDailyReport(exampleHotspots, ['张三', '李四']);
console.log(report.text);

// ==================== 使用原有系统的其他功能 ====================

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('【使用原有系统的其他功能】');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

// 使用信息信号识别系统
console.log('▶ 使用信息信号识别系统');
const signalResult = ai.signal.evaluateSignal({
  title: '测试信号',
  source: '测试',
  timeSensitivity: 'immediate',
  impactDepth: 'worldview',
  actionability: 8,
  compoundValue: 9
});
console.log(`  信号评估: ${signalResult.level} - ${signalResult.reason}`);
console.log('');

// 使用工作流沉淀系统
console.log('▶ 使用工作流沉淀系统');
ai.workflow.explicitizeTacitKnowledge('值班任务', {
  operation: '监测热点',
  experience: '关注舆论热度',
  decision: 'S级需要分析',
  thinking: '时间衰减很重要',
  value: '不错过重要信息'
});
console.log('  已沉淀隐性知识');
console.log('');

// 使用AI镜像
console.log('▶ 使用AI镜像');
const insight = ai.generateInsight();
console.log(`  观察: ${insight.observation}`);
console.log(`  建议: ${insight.suggestion}`);
console.log('');

// 健康检查
console.log('▶ 系统健康检查');
const health = ai.healthCheck();
console.log(`  L1: ${health.levels.L1.usage} [${health.levels.L1.status}]`);
console.log(`  L2: ${health.levels.L2.usage} [${health.levels.L2.status}]`);
console.log('');

// ==================== 总结 ====================

console.log('╔══════════════════════════════════════════════════════════════════════╗');
console.log('║                          总结                                        ║');
console.log('╠══════════════════════════════════════════════════════════════════════╣');
console.log('║                                                                      ║');
console.log('║  这是一个场景化示例，展示如何使用AI协作操作系统：                   ║');
console.log('║                                                                      ║');
console.log('║  1. 可以监测任何类型的热点（政策、社会、产业、舆情等）              ║');
console.log('║  2. 使用原有系统的核心功能                                          ║');
console.log('║  3. 不改变原有系统，只是演示用法                                    ║');
console.log('║  4. 可根据实际需求调整配置                                          ║');
console.log('║                                                                      ║');
console.log('║  原有系统功能完全可用：                                             ║');
console.log('║  • ai.memory - 统一记忆系统                                         ║');
console.log('║  • ai.signal - 信息信号识别                                         ║');
console.log('║  • ai.workflow - 工作流沉淀                                         ║');
console.log('║  • ai.goal - 目标追踪                                               ║');
console.log('║                                                                      ║');
console.log('╚══════════════════════════════════════════════════════════════════════╝');
console.log('\n');
