import { assistant } from './src/index';

async function testStrategyDecision() {
  const sessionId = 'test-strategy-' + Date.now();
  const startTime = Date.now();
  
  console.log('=== 测试 3：战略决策 ===');
  console.log('决策问题：是否应该进入短视频赛道进行业务扩张\n');
  
  // 开始分析
  const start = await assistant.startAnalysis(sessionId, '是否应该进入短视频赛道进行业务扩张');
  console.log(start);
  console.log('\n---\n');
  
  // 模拟用户回答
  const answers = [
    '5分。我们对短视频内容创作有一定了解，但对算法推荐、流量运营不够熟悉。',
    '在能力圈边缘。我们擅长教培内容，但短视频运营是新领域，需要学习。',
    '难以预测。短视频赛道竞争激烈，能否获得流量存在很大不确定性。',
    '缓冲不足。如果投入短视频失败，会影响现有业务的资源投入。',
    '最多承受10万元试错成本和3个月时间。超出会影响主营业务。',
    '退出机制不明确。一旦投入人力和资源，短期内难以快速撤出。',
    '护城河很浅。短视频内容容易被模仿，我们没有明显优势。',
    '竞争对手众多。抖音、快手上已有大量教培类账号，竞争激烈。',
    '品牌价值有限。我们是新账号，没有粉丝基础和品牌认知。',
    '最坏情况：1）投入大量精力但没有流量 2）内容质量不高被用户吐槽 3）团队疲于应付影响主业 4）错过其他更好的机会',
    '可能失败原因：1）内容不够吸引人 2）算法推荐不给流量 3）团队经验不足 4）投入产出比太低',
    '风险较高。短视频赛道不确定性大，我们没有明显优势。',
    '市场过热。大量创作者涌入，流量红利已过，新账号很难起来。',
    '竞争白热化。头部账号占据大部分流量，新账号机会渺茫。',
    '存在泡沫。很多人高估了短视频的变现能力，实际转化率很低。'
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

testStrategyDecision().catch(console.error);
