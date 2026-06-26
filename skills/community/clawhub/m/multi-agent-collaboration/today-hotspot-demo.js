/**
 * 今日热点监测演示
 * 使用AI协作操作系统监测今日热点
 */

const { AICollaborationSystem } = require('./dist/index');

console.log('\n');
console.log('╔══════════════════════════════════════════════════════════════════════╗');
console.log('║           今日热点监测演示 - 2026年2月25日                           ║');
console.log('╚══════════════════════════════════════════════════════════════════════╝');
console.log('\n');

// ==================== 初始化系统 ====================

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('【第一步】初始化AI协作操作系统');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

const ai = new AICollaborationSystem('today_hotspot', 'memory');
console.log('✅ 系统初始化完成\n');

// ==================== 今日热点数据 ====================

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('【第二步】输入今日监测到的热点');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

// 模拟今日热点（包含各类型）
const todayHotspots = [
  // ===== S级热点 =====
  {
    title: 'DeepSeek发布新模型，性能超越GPT-4',
    source: 'DeepSeek官方',
    type: '科技热点',
    publishDate: new Date(),
    timeSensitivity: 'immediate',
    impactDepth: 'worldview',
    actionability: 9,
    compoundValue: 10,
    publicAttention: 98,
    discussionVolume: 120000,
    emotionIntensity: 92,
    brief: '国产AI公司DeepSeek发布新模型，多项指标超越GPT-4，引发行业震动'
  },
  {
    title: '某互联网大厂宣布大规模裁员',
    source: '财经媒体',
    type: '社会热点',
    publishDate: new Date(),
    timeSensitivity: 'immediate',
    impactDepth: 'strategy',
    actionability: 7,
    compoundValue: 6,
    publicAttention: 95,
    discussionVolume: 80000,
    emotionIntensity: 88,
    brief: '某知名互联网公司宣布裁员计划，涉及多个业务线'
  },
  
  // ===== A级热点 =====
  {
    title: '新能源汽车补贴政策调整',
    source: '政府公告',
    type: '政策热点',
    publishDate: new Date(),
    timeSensitivity: 'delayed',
    impactDepth: 'strategy',
    actionability: 8,
    compoundValue: 7,
    publicAttention: 72,
    discussionVolume: 35000,
    emotionIntensity: 55,
    brief: '相关部门发布新能源汽车补贴政策调整方案'
  },
  {
    title: '某明星代言品牌翻车事件',
    source: '社交媒体',
    type: '舆情热点',
    publishDate: new Date(),
    timeSensitivity: 'immediate',
    impactDepth: 'tool',
    actionability: 5,
    compoundValue: 4,
    publicAttention: 85,
    discussionVolume: 50000,
    emotionIntensity: 78,
    brief: '某明星代言品牌出现质量问题，引发舆论关注'
  },
  
  // ===== B级热点 =====
  {
    title: '国际油价波动',
    source: '财经新闻',
    type: '经济热点',
    publishDate: new Date(),
    timeSensitivity: 'continuous',
    impactDepth: 'strategy',
    actionability: 6,
    compoundValue: 5,
    publicAttention: 55,
    discussionVolume: 12000,
    emotionIntensity: 40,
    brief: '受国际形势影响，油价出现较大波动'
  },
  {
    title: '某科技公司发布新品',
    source: '科技媒体',
    type: '科技热点',
    publishDate: new Date(),
    timeSensitivity: 'immediate',
    impactDepth: 'method',
    actionability: 4,
    compoundValue: 4,
    publicAttention: 48,
    discussionVolume: 8000,
    emotionIntensity: 35,
    brief: '某科技公司召开发布会，推出多款新品'
  },
  
  // ===== 旧热点（测试时间衰减） =====
  {
    title: '上周的AI行业峰会',
    source: '行业新闻',
    type: '科技热点',
    publishDate: new Date(Date.now() - 8 * 24 * 60 * 60 * 1000), // 8天前
    timeSensitivity: 'delayed',
    impactDepth: 'cognition',
    actionability: 5,
    compoundValue: 5,
    publicAttention: 60,
    discussionVolume: 15000,
    emotionIntensity: 45,
    brief: '上周举办的AI行业峰会圆满落幕'
  }
];

console.log('今日监测到 ' + todayHotspots.length + ' 条热点：\n');
todayHotspots.forEach((h, i) => {
  const time = new Date(h.publishDate).toLocaleDateString('zh-CN');
  console.log(`  ${i+1}. [${h.type}] ${h.title}`);
  console.log(`     来源: ${h.source} | 时间: ${time}`);
  console.log(`     简介: ${h.brief}`);
  console.log('');
});

// ==================== 热点评估 ====================

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('【第三步】自动评估关注等级');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

// 评估函数
function evaluateHotspot(hotspot) {
  // 计算舆论热度
  const attentionScore = (
    hotspot.publicAttention * 0.4 +
    (hotspot.discussionVolume / 1000) * 0.3 +
    hotspot.emotionIntensity * 0.3
  );
  
  // 时间衰减
  const age = Math.floor((Date.now() - new Date(hotspot.publishDate)) / (24 * 60 * 60 * 1000));
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
  let needAnalysis = false;
  
  if (finalScore >= 75 && age <= 7) {
    level = 'S';
    needAnalysis = true;
  } else if (finalScore >= 60) {
    level = 'A';
    if (age <= 7) needAnalysis = hotspot.publicAttention >= 80;
  } else if (finalScore >= 40) {
    level = 'B';
  }
  
  // 时间限制
  if (age > 7) level = 'B';
  if (age > 14) level = 'C';
  
  return {
    ...hotspot,
    attentionScore: Math.round(attentionScore),
    finalScore,
    level,
    needAnalysis,
    age,
    decayRate
  };
}

const evaluated = todayHotspots.map(evaluateHotspot);

// 显示评估结果
console.log('评估结果：\n');
console.log('  等级  标题                                    评分   舆论热度  需分析');
console.log('  ─────────────────────────────────────────────────────────────────────');

// 按等级排序
const levelOrder = { 'S': 0, 'A': 1, 'B': 2, 'C': 3 };
evaluated.sort((a, b) => levelOrder[a.level] - levelOrder[b.level]);

evaluated.forEach(h => {
  const icon = { 'S': '🔴', 'A': '🟠', 'B': '🟡', 'C': '⚪' }[h.level];
  const title = h.title.substring(0, 24).padEnd(24);
  console.log(`  ${icon}${h.level}   ${title}  ${h.finalScore.toString().padStart(3)}    ${h.publicAttention.toString().padStart(3)}      ${h.needAnalysis ? '✅' : '❌'}`);
});
console.log('');

// ==================== 生成日报 ====================

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('【第四步】生成今日热点日报');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

const visible = evaluated.filter(h => h.level !== 'C');
const stats = {
  total: todayHotspots.length,
  S: evaluated.filter(h => h.level === 'S').length,
  A: evaluated.filter(h => h.level === 'A').length,
  B: evaluated.filter(h => h.level === 'B').length,
  needAnalysis: evaluated.filter(h => h.needAnalysis).length
};

// 生成日报文本
let reportText = '';
reportText += `【2026年2月25日 热点日报】\n\n`;
reportText += `监测时间：${new Date().toLocaleString('zh-CN')}\n`;
reportText += `值班人员：待安排\n\n`;

// S级热点
const sLevel = visible.filter(h => h.level === 'S');
if (sLevel.length > 0) {
  reportText += `【S级热点】（需要深度分析）\n`;
  sLevel.forEach(h => {
    reportText += `🔴 ${h.title}\n`;
    reportText += `   类型：${h.type} | 来源：${h.source}\n`;
    reportText += `   评分：${h.finalScore} | 舆论热度：${h.publicAttention} | 讨论量：${h.discussionVolume}\n`;
    reportText += `   简介：${h.brief}\n`;
    reportText += `   ⚠️ 需要输出深度分析材料（截止时间：次日12:00）\n\n`;
  });
}

// A级热点
const aLevel = visible.filter(h => h.level === 'A');
if (aLevel.length > 0) {
  reportText += `【A级热点】（高度关注）\n`;
  aLevel.forEach(h => {
    reportText += `🟠 ${h.title}\n`;
    reportText += `   类型：${h.type} | 来源：${h.source}\n`;
    reportText += `   评分：${h.finalScore} | 舆论热度：${h.publicAttention}\n`;
    reportText += `   简介：${h.brief}\n\n`;
  });
}

// B级热点
const bLevel = visible.filter(h => h.level === 'B');
if (bLevel.length > 0) {
  reportText += `【B级热点】（持续跟踪）\n`;
  bLevel.forEach(h => {
    reportText += `🟡 ${h.title}\n`;
    reportText += `   评分：${h.finalScore}\n\n`;
  });
}

// 统计
reportText += `【今日统计】\n`;
reportText += `共监测${stats.total}条热点，`;
reportText += `S级${stats.S}条，A级${stats.A}条，B级${stats.B}条\n\n`;

// 待处理
if (stats.needAnalysis > 0) {
  reportText += `【待处理事项】\n`;
  reportText += `• 需要输出分析材料：${stats.needAnalysis}条\n`;
  reportText += `  截止时间：次日12:00\n`;
}

console.log(reportText);

// ==================== 存储到记忆系统 ====================

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('【第五步】存储到记忆系统');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

// 存储S级热点到L2经验记忆
sLevel.forEach(h => {
  ai.memory.addToL2(
    `S级热点_${h.title}`,
    {
      title: h.title,
      type: h.type,
      score: h.finalScore,
      brief: h.brief,
      date: '2026-02-25'
    },
    'insight',
    5,
    ['S级', '热点', h.type],
    'signal'
  );
});

// 存储A级热点到L2
aLevel.forEach(h => {
  ai.memory.addToL2(
    `A级热点_${h.title}`,
    {
      title: h.title,
      type: h.type,
      score: h.finalScore,
      brief: h.brief,
      date: '2026-02-25'
    },
    'insight',
    4,
    ['A级', '热点', h.type],
    'signal'
  );
});

// 存储日报到L1工作记忆
ai.memory.addToL1('今日日报', `监测${stats.total}条，S级${stats.S}条，A级${stats.A}条`, 'task', 4);

console.log(`✅ 已存储 ${sLevel.length} 条S级热点到经验记忆`);
console.log(`✅ 已存储 ${aLevel.length} 条A级热点到经验记忆`);
console.log(`✅ 已存储今日日报到工作记忆`);
console.log('');

// ==================== 生成深度分析框架 ====================

if (sLevel.length > 0) {
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('【第六步】S级热点深度分析框架');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  sLevel.forEach((h, i) => {
    console.log(`【${i+1}】${h.title}`);
    console.log('─────────────────────────────────────');
    console.log('');
    console.log('一、事件概述');
    console.log('─────────────────────────────────────');
    console.log(`• 时间：2026年2月25日`);
    console.log(`• 来源：${h.source}`);
    console.log(`• 类型：${h.type}`);
    console.log(`• 简介：${h.brief}`);
    console.log('');
    console.log('二、舆论态势');
    console.log('─────────────────────────────────────');
    console.log(`• 关注度：${h.publicAttention}/100`);
    console.log(`• 讨论量：${h.discussionVolume}`);
    console.log(`• 情绪强度：${h.emotionIntensity}/100`);
    console.log(`• 综合评分：${h.finalScore}`);
    console.log('');
    console.log('三、影响分析');
    console.log('─────────────────────────────────────');
    console.log(`• 影响深度：${h.impactDepth}`);
    console.log(`• 时间敏感度：${h.timeSensitivity}`);
    console.log(`• 可行动性：${h.actionability}/10`);
    console.log('');
    console.log('四、建议措施');
    console.log('─────────────────────────────────────');
    console.log('• 监测建议：持续跟踪舆论发展，关注关键节点');
    console.log('• 应对建议：准备官方回应，协调相关部门');
    console.log('');
    console.log('五、后续跟踪');
    console.log('─────────────────────────────────────');
    console.log('• 需持续关注：舆论走向、相关方反应');
    console.log('• 预计发展：可能持续发酵，需准备多套方案');
    console.log('');
    console.log('─'.repeat(60));
    console.log('');
  });
}

// ==================== 系统状态 ====================

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('【系统状态】');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

console.log(ai.getSummary());
console.log('');

const health = ai.healthCheck();
console.log('健康检查：');
Object.entries(health.levels).forEach(([level, status]) => {
  console.log(`  ${level}: ${status.usage} [${status.status}]`);
});
console.log('');

// ==================== 查询历史热点 ====================

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('【查询功能】搜索历史热点');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

const searchResults = ai.memory.queryAll('热点');
console.log(`搜索"热点"：`);
console.log(`  L1工作记忆：${searchResults.L1.length}条`);
console.log(`  L2经验记忆：${searchResults.L2.length}条`);
console.log('');

// ==================== 总结 ====================

console.log('╔══════════════════════════════════════════════════════════════════════╗');
console.log('║                     ✅ 今日热点监测完成                               ║');
console.log('╠══════════════════════════════════════════════════════════════════════╣');
console.log('║                                                                      ║');
console.log('║  今日监测结果：                                                     ║');
console.log(`║  • 共监测 ${stats.total} 条热点                                              ║`);
console.log(`║  • S级（需深度分析）：${stats.S} 条                                        ║`);
console.log(`║  • A级（高度关注）：${stats.A} 条                                          ║`);
console.log(`║  • B级（持续跟踪）：${stats.B} 条                                          ║`);
console.log('║                                                                      ║');
console.log('║  已完成操作：                                                       ║');
console.log('║  ✅ 热点评估与分级                                                 ║');
console.log('║  ✅ 生成今日日报                                                   ║');
console.log('║  ✅ 存储到记忆系统                                                 ║');
console.log('║  ✅ 生成深度分析框架                                               ║');
console.log('║                                                                      ║');
console.log('║  待处理事项：                                                       ║');
console.log(`║  ⚠️  ${stats.needAnalysis}条热点需要输出深度分析材料                          ║`);
console.log('║     截止时间：次日12:00                                             ║');
console.log('║                                                                      ║');
console.log('╚══════════════════════════════════════════════════════════════════════╝');
console.log('\n');
