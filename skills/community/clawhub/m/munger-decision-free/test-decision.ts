import { assistant } from './src/index';

async function testRealDecision() {
  console.log('=== 芒格决策助手 - 内部测试 ===\n');
  
  // 测试决策 1：投资决策
  console.log('【测试 1：投资决策】');
  const sessionId = 'test-session-1';
  const decision = '是否应该投资中宠股份（股票代码：002891）';
  
  console.log(`决策问题：${decision}\n`);
  
  // 开始分析
  const response1 = await assistant.startAnalysis(sessionId, decision);
  console.log(response1);
  console.log('\n---\n');
  
  // 回答第一个问题（能力圈）
  const answer1 = await assistant.handleAnswer(sessionId, '7分。我对宠物食品行业有一定了解，知道行业增长趋势和主要竞争对手，但对供应链细节不够熟悉。');
  console.log(answer1);
  console.log('\n---\n');
  
  // 回答第二个问题（安全边际）
  const answer2 = await assistant.handleAnswer(sessionId, '最多承受 30% 的损失。如果股价下跌超过 30%，会影响我的现金流和心理承受能力。');
  console.log(answer2);
  console.log('\n---\n');
  
  // 回答第三个问题（护城河）
  const answer3 = await assistant.handleAnswer(sessionId, '中宠有一定品牌优势和渠道优势，但护城河不算很深。竞争对手可以通过价格战或新品类进入市场。');
  console.log(answer3);
  console.log('\n---\n');
  
  // 继续回答剩余问题直到生成报告
  const answer4 = await assistant.handleAnswer(sessionId, '最坏情况：1）宠物食品行业增速放缓 2）原材料成本上涨 3）竞争加剧导致利润率下降 4）食品安全事故');
  console.log(answer4);
  console.log('\n---\n');
  
  const answer5 = await assistant.handleAnswer(sessionId, '市场先生目前情绪乐观，宠物概念股普遍高估。中宠股份 PE 约 40 倍，高于行业平均。可能存在泡沫风险。');
  console.log(answer5);
}

testRealDecision().catch(console.error);
