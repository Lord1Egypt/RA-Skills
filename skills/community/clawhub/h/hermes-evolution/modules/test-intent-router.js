/**
 * IntentRouter 测试脚本
 */

const { IntentRouter } = require('./intent-router');

console.log('🧪 IntentRouter 测试\n');

const router = new IntentRouter();

// 测试用例
const testCases = [
  // 显式指定
  { input: '@marketing 发布小红书内容', expected: 'Marketing', type: 'explicit' },
  { input: '@rd 部署Gateway', expected: 'RD', type: 'explicit' },
  { input: '@strategy 制定财富计划', expected: 'Strategy', type: 'explicit' },

  // 内容创作
  { input: '帮我写一篇小红书笔记，关于职场成长', expected: 'Marketing' },
  { input: '发布抖音视频，主题是个人IP打造', expected: 'Marketing' },
  { input: '写一个知乎回答，关于职业规划', expected: 'Marketing' },

  // 运维
  { input: 'Gateway进程挂了吗？检查一下', expected: 'RD' },
  { input: '备份系统配置', expected: 'RD' },
  { input: '重启服务器', expected: 'RD' },

  // 技术开发
  { input: '帮我写一个Python自动化脚本', expected: 'RD' },
  { input: '修复API的bug', expected: 'RD' },
  { input: '优化系统架构', expected: 'RD' },

  // 战略
  { input: '分析一下市场机会', expected: 'Strategy' },
  { input: '财富自由路径规划', expected: 'Strategy' },
  { input: '商业模式画布设计', expected: 'Strategy' },

  // 产品
  { input: '产品Roadmap规划', expected: 'Product' },
  { input: 'MVP定义和优先级排序', expected: 'Product' },

  // HR
  { input: '筛选这份简历', expected: 'CEO' },
  { input: '安排面试候选人', expected: 'CEO' },

  // 汇报
  { input: '汇报一下今天的进展', expected: 'CEO' },
  { input: '同步各Agent状态', expected: 'CEO' },

  // 模糊/综合
  { input: '帮我看看这个', expected: 'CEO' },
  { input: '分析一下这个问题', expected: 'Strategy' },
];

let passed = 0;
let failed = 0;

console.log('═══════════════════════════════════════════════════════════════');
for (const { input, expected, type } of testCases) {
  const result = router.route(input);
  const match = result.agent === expected;
  
  if (match) {
    passed++;
    console.log(`✅ "${input.substring(0, 30)}${input.length > 30 ? '...' : ''}"`);
    console.log(`   → @${result.agent} (${type === 'explicit' ? '显式' : `置信度${result.confidence}`})`);
  } else {
    failed++;
    console.log(`❌ "${input.substring(0, 30)}${input.length > 30 ? '...' : ''}"`);
    console.log(`   期望: @${expected}, 实际: @${result.agent} (${result.confidence})`);
  }
}
console.log('═══════════════════════════════════════════════════════════════\n');

console.log(`📊 测试结果: ${passed} 通过, ${failed} 失败\n`);

// 测试置信度排名
console.log('📊 置信度排名测试');
console.log('───────────────────────────────────────────────────────────────');
const rankingTest = '分析一下小红书运营策略和市场机会';
const { primary, ranking } = router.routeWithRanking(rankingTest);
console.log(`输入: "${rankingTest}"`);
console.log(`主要路由: @${primary.agent} (${primary.confidence})`);
console.log('候选路由:');
for (const r of ranking) {
  console.log(`  ${r.confidence.toFixed(2)} - ${r.intent} → @${r.agent}`);
}

console.log('\n✅ IntentRouter 测试完成！');
