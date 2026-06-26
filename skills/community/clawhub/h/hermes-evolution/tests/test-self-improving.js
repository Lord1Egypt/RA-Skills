/**
 * SENSEN Self-Improving - Phase 3 测试脚本
 */

const SelfImproving = require('./sensen-self-improving');

// 测试辅助函数
function log(label, data) {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`测试: ${label}`);
  console.log('='.repeat(60));
  if (typeof data === 'object') {
    console.log(JSON.stringify(data, null, 2));
  } else {
    console.log(data);
  }
}

async function runTests() {
  console.log('🚀 SENSEN Self-Improving Phase 3 - 测试开始');
  
  // 1. 记录几次相似的老板纠正
  log('1. 记录老板纠正（模拟同一模式的3次纠正）');
  
  // 第一次纠正
  SelfImproving.logCorrection({
    type: SelfImproving.CorrectionType.FORMAT,
    originalText: '报告太长了，简洁一点',
    correction: '输出控制在200字以内',
    context: '汇报工作时'
  });
  
  // 第二次纠正（相似）
  SelfImproving.logCorrection({
    type: SelfImproving.CorrectionType.FORMAT,
    originalText: '能不能简短些？我没时间看长文',
    correction: '保持简洁，重点突出',
    context: '发送消息时'
  });
  
  // 第三次纠正（触发规则生成）
  SelfImproving.logCorrection({
    type: SelfImproving.CorrectionType.FORMAT,
    originalText: '太啰嗦了，说重点',
    correction: '结论先行，不超过3点',
    context: '任何汇报场景'
  });
  
  // 2. 记录其他类型的纠正
  log('2. 记录其他类型纠正');
  
  SelfImproving.logCorrection({
    type: SelfImproving.CorrectionType.TONE,
    originalText: '说话别那么死板，轻松点',
    correction: '语气更自然，像和人聊天',
    context: '日常对话'
  });
  
  SelfImproving.logCorrection({
    type: SelfImproving.CorrectionType.PRIORITY,
    originalText: '健康检查不用每小时做，2小时一次就够了',
    correction: '降低检查频率',
    context: '定时任务设置'
  });
  
  // 3. 查看统计
  log('3. 统计信息', SelfImproving.getStats());
  
  // 4. 打印规则
  log('4. 当前生效规则');
  SelfImproving.printRules();
  
  // 5. 测试规则匹配
  log('5. 规则匹配测试');
  
  const testTexts = [
    '帮我写一个详细的项目报告',
    '太长了缩短一下',
    '今天的天气怎么样'
  ];
  
  for (const text of testTexts) {
    const result = SelfImproving.matchRule(text);
    if (result.matched) {
      console.log(`  "${text}"`);
      console.log(`    → 匹配规则: ${result.rule.name}`);
      console.log(`    → 建议: ${result.rule.description}`);
    } else {
      console.log(`  "${text}" → 无匹配规则`);
    }
  }
  
  // 6. 打印提醒
  log('6. 主动提醒');
  const reminders = SelfImproving.getReminders();
  if (reminders.length === 0) {
    console.log('(无提醒)');
  } else {
    reminders.forEach(r => console.log(`  [${r.priority}] ${r.message}`));
  }
  
  // 7. 打印最近纠正
  log('7. 最近纠正记录');
  SelfImproving.printRecentCorrections(5);
  
  console.log('\n✅ Phase 3 测试完成!');
  
  // 清理测试数据（可选）
  // 注意：保留数据用于演示
}

runTests().catch(console.error);
