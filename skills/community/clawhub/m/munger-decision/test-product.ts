import { assistant } from './src/index';

async function testProductDecision() {
  const sessionId = 'test-product-' + Date.now();
  const startTime = Date.now();
  
  console.log('=== 测试 1：产品决策 ===');
  console.log('决策问题：是否应该开发 AI 教培产品的题库功能\n');
  
  // 开始分析
  const start = await assistant.startAnalysis(sessionId, '是否应该开发 AI 教培产品的题库功能');
  console.log(start);
  console.log('\n---\n');
  
  // 模拟用户回答
  const answers = [
    '8分。我们团队对教培行业和用户需求有深入理解，但对题库技术实现细节还需要学习。',
    '能力圈内。我们了解专升本学生的学习痛点，知道他们需要什么样的题库功能。',
    '可以预测。题库功能可以提升用户留存率和付费转化率，预计3个月内可以看到效果。',
    '有30%缓冲。即使题库功能效果不如预期，我们还有其他核心功能支撑产品。',
    '最多投入2个月开发时间和5万元成本。如果超出预算会影响其他功能开发。',
    '有退出机制。如果用户反馈不好，可以快速下线或调整方向。',
    '题库功能有一定壁垒。需要积累大量高质量题目和解析，竞争对手短期内难以复制。',
    '竞争对手可以模仿。但我们可以通过AI生成题目和个性化推荐建立差异化优势。',
    '品牌价值中等。题库功能可以增强用户对产品专业性的认知。',
    '最坏情况：1）用户不买账，使用率低 2）题目质量不高被投诉 3）开发周期延长影响其他功能 4）竞品快速跟进',
    '可能失败原因：1）题目数量不足 2）解析质量差 3）交互体验不好 4）没有差异化优势',
    '风险可控。我们可以先做MVP测试，根据用户反馈快速迭代。',
    '市场需求旺盛。专升本学生普遍需要刷题，但现有产品体验不佳。',
    '竞品题库功能参差不齐。有机会通过AI技术提供更好的体验。',
    '不存在明显泡沫。教培市场需求真实存在，题库是刚需功能。'
  ];
  
  for (const answer of answers) {
    const response = await assistant.handleAnswer(sessionId, answer);
    console.log(response);
    console.log('\n---\n');
    
    if (response.includes('# 决策分析报告')) {
      const endTime = Date.now();
      const duration = (endTime - startTime) / 1000;
      console.log(`\n⏱️  报告生成时间：${duration.toFixed(2)} 秒`);
      break;
    }
  }
}

testProductDecision().catch(console.error);
