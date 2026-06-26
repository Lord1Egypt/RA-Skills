import { assistant } from './src/index';

async function testHiringDecision() {
  const sessionId = 'test-hiring-' + Date.now();
  const startTime = Date.now();
  
  console.log('=== 测试 2：人员决策 ===');
  console.log('决策问题：是否应该招聘这位前端工程师候选人（5年经验，要求月薪25K）\n');
  
  // 开始分析
  const start = await assistant.startAnalysis(sessionId, '是否应该招聘这位前端工程师候选人（5年经验，要求月薪25K）');
  console.log(start);
  console.log('\n---\n');
  
  // 模拟用户回答
  const answers = [
    '7分。我对前端技术栈有了解，但对候选人的实际能力评估经验有限。',
    '在能力圈内。我们需要前端工程师来开发小程序和H5页面，这是明确的需求。',
    '可以预测。招聘后1个月可以独立开发功能，3个月可以带来明显产出。',
    '有缓冲。即使这位候选人不合适，我们还有其他候选人可以选择。',
    '最多承受3个月试用期成本（约7.5万）。如果不合适需要重新招聘。',
    '有退出机制。试用期内可以双向选择，不合适可以终止合同。',
    '技能有一定壁垒。候选人熟悉React和小程序开发，有相关项目经验。',
    '可替代性中等。市场上有类似经验的前端工程师，但招聘周期较长。',
    '品牌价值一般。候选人来自中型互联网公司，有一定背景但不是大厂。',
    '最坏情况：1）技术能力不达标 2）团队协作有问题 3）试用期离职 4）薪资要求后续上涨',
    '可能失败原因：1）面试评估不准确 2）期望不匹配 3）工作强度不适应 4）团队文化不合',
    '风险可控。试用期可以充分评估，不合适及时止损。',
    '市场行情合理。5年经验前端工程师25K月薪在二线城市属于正常水平。',
    '候选人期望合理。没有明显高估或低估自己的价值。',
    '不存在泡沫。招聘需求真实，薪资水平符合市场行情。'
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

testHiringDecision().catch(console.error);
