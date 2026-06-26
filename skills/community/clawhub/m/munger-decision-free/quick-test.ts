import { assistant } from './src/index';

async function quickTest() {
  const sessionId = 'quick-test-' + Date.now();
  
  console.log('=== 快速测试：投资决策 ===\n');
  
  // 1. 开始分析
  const start = await assistant.startAnalysis(sessionId, '是否应该投资中宠股份');
  console.log('✅ 场景识别成功\n');
  
  // 2. 快速回答所有问题（模拟用户输入）
  const answers = [
    '7分，有一定了解',
    '能解释核心逻辑',
    '能预测未来3年',
    '有30%缓冲',
    '最多承受30%损失',
    '有退出机制',
    '护城河一般',
    '竞争对手可以复制',
    '品牌有一定价值',
    '最坏情况是行业衰退',
    '可能的失败原因是竞争加剧',
    '风险可控',
    '市场情绪乐观',
    'PE偏高',
    '可能存在泡沫'
  ];
  
  for (let i = 0; i < answers.length; i++) {
    const response = await assistant.handleAnswer(sessionId, answers[i]);
    if (response.includes('# 决策分析报告')) {
      console.log('✅ 报告生成成功\n');
      console.log(response);
      break;
    }
  }
}

quickTest().catch(console.error);
