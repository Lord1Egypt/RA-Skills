#!/usr/bin/env ts-node
/**
 * 测试智能推荐算法
 */
import { SmartRecommender } from './src/smart-recommender';

const recommender = new SmartRecommender();

async function test() {
  console.log('🧪 测试智能推荐算法\n');
  
  const testCases = [
    {
      scenario: 'investment',
      input: '中宠股份现在估值合理吗？我对宠物食品行业不太了解，但看到最近涨得很猛，大家都在买',
      expected: ['06-误判心理学', '10-安全边际', '07-逆向思维']
    },
    {
      scenario: 'investment',
      input: '昭衍新药有什么风险？最坏的情况会怎样？',
      expected: ['07-逆向思维', '10-安全边际']
    },
    {
      scenario: 'product',
      input: '升本智途 MVP 最核心的功能是什么？用户真正需要什么？',
      expected: ['08-第一性原理']
    },
    {
      scenario: 'strategy',
      input: '是否应该进入短视频赛道？竞争对手很多，我们有什么优势？',
      expected: ['09-护城河', '07-逆向思维']
    }
  ];
  
  for (const testCase of testCases) {
    console.log(`📋 场景：${testCase.scenario}`);
    console.log(`💬 输入：${testCase.input}\n`);
    
    const scores = await recommender.analyzeAndScore(
      testCase.input,
      testCase.scenario
    );
    
    console.log('🎯 推荐结果：');
    scores.forEach((s, i) => {
      console.log(`  ${i + 1}. ${s.model.name} (${s.modelId}) - 得分: ${s.score}`);
      console.log(`     理由: ${s.reason}`);
    });
    
    console.log('\n' + '='.repeat(60) + '\n');
  }
}

test().catch(console.error);
