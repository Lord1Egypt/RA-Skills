#!/usr/bin/env ts-node
/**
 * 完整测试：场景识别 + 智能推荐 + 对话流程
 */
import { MungerDecisionAssistant } from './src/index';

const assistant = new MungerDecisionAssistant();

async function test() {
  console.log('🎯 芒格决策助手 - 完整流程测试\n');
  
  // 测试案例 1：投资决策
  console.log('=' .repeat(60));
  console.log('📊 测试案例 1：投资决策（情绪化 + 不了解）\n');
  
  const sessionId1 = 'test-session-1';
  const input1 = '中宠股份现在估值合理吗？我对宠物食品行业不太了解，但看到最近涨得很猛，大家都在买';
  
  const response1 = await assistant.startAnalysis(sessionId1, input1);
  console.log(response1);
  console.log('\n');
  
  // 测试案例 2：风险分析
  console.log('=' .repeat(60));
  console.log('📊 测试案例 2：投资决策（风险导向）\n');
  
  const sessionId2 = 'test-session-2';
  const input2 = '昭衍新药有什么风险？最坏的情况会怎样？我担心行业政策变化';
  
  const response2 = await assistant.startAnalysis(sessionId2, input2);
  console.log(response2);
  console.log('\n');
  
  // 测试案例 3：产品决策
  console.log('=' .repeat(60));
  console.log('📊 测试案例 3：产品决策（第一性原理）\n');
  
  const sessionId3 = 'test-session-3';
  const input3 = '升本智途 MVP 最核心的功能是什么？用户真正需要什么？不要参考竞品';
  
  const response3 = await assistant.startAnalysis(sessionId3, input3);
  console.log(response3);
  console.log('\n');
  
  // 测试案例 4：战略决策
  console.log('=' .repeat(60));
  console.log('📊 测试案例 4：战略决策（竞争分析）\n');
  
  const sessionId4 = 'test-session-4';
  const input4 = '是否应该进入短视频赛道？竞争对手很多，我们有什么长期优势？';
  
  const response4 = await assistant.startAnalysis(sessionId4, input4);
  console.log(response4);
  console.log('\n');
  
  console.log('=' .repeat(60));
  console.log('✅ 测试完成\n');
}

test().catch(console.error);
