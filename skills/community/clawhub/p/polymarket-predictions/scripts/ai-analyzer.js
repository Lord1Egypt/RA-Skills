/**
 * AI概率分析模块
 * 使用GLM-5分析事件发生概率，对比市场赔率
 */

const GLM5_API = process.env.GLM5_API_URL || 'https://open.bigmodel.cn/api/paas/v4/chat/completions';
const GLM5_KEY = process.env.GLM5_API_KEY;

/**
 * AI分析事件概率
 * @param {string} event - 事件描述
 * @returns {Promise<{probability: number, reasoning: string}>}
 */
async function analyzeEventProbability(event) {
  const prompt = `你是一个专业的预测市场分析师。请分析以下事件发生的概率。

事件：${event}

请给出：
1. 这个事件发生的概率（0-100%之间的一个数字）
2. 你的分析理由（3-5条关键因素）

请用JSON格式回复：
{
  "probability": 数字,
  "reasoning": ["因素1", "因素2", "因素3"]
}

只返回JSON，不要其他内容。`;

  try {
    // 如果没有API key，返回模拟数据
    if (!GLM5_KEY) {
      console.log('⚠️  未配置GLM5_API_KEY，使用模拟分析');
      return simulateAnalysis(event);
    }
    
    const resp = await fetch(GLM5_API, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${GLM5_KEY}`
      },
      body: JSON.stringify({
        model: 'glm-4',
        messages: [{ role: 'user', content: prompt }],
        temperature: 0.7,
        max_tokens: 500
      })
    });
    
    const data = await resp.json();
    const content = data.choices[0].message.content;
    
    // 解析JSON
    const jsonMatch = content.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      return JSON.parse(jsonMatch[0]);
    }
    
    throw new Error('无法解析AI响应');
  } catch (error) {
    console.log('⚠️  AI分析失败，使用模拟数据');
    return simulateAnalysis(event);
  }
}

/**
 * 模拟分析（无API key时使用）
 */
function simulateAnalysis(event) {
  // 简单的关键词匹配模拟
  const keywords = {
    '比特币': { prob: 0.65, factors: ['机构采用增加', '减半效应', '监管不确定性'] },
    'BTC': { prob: 0.65, factors: ['机构采用增加', '减半效应', '监管不确定性'] },
    '以太坊': { prob: 0.60, factors: ['ETH 2.0升级', 'DeFi生态增长', 'Gas费问题'] },
    'ETH': { prob: 0.60, factors: ['ETH 2.0升级', 'DeFi生态增长', 'Gas费问题'] },
    '特朗普': { prob: 0.55, factors: ['民调数据', '摇摆州竞争', '经济表现'] },
    'AI': { prob: 0.75, factors: ['技术进步', '投资热潮', '实际应用增长'] },
    '中国': { prob: 0.6, factors: ['政策因素', '经济数据', '国际关系'] },
    '利率': { prob: 0.7, factors: ['通胀数据', '就业市场', '美联储立场'] }
  };
  
  for (const [key, data] of Object.entries(keywords)) {
    if (event.includes(key)) {
      return {
        probability: data.prob,
        reasoning: data.factors
      };
    }
  }
  
  // 默认
  return {
    probability: 0.5,
    reasoning: ['信息不足', '需要更多数据', '建议查看市场详情']
  };
}

/**
 * 对比AI概率和市场赔率
 * @param {number} aiProb - AI概率 (0-1)
 * @param {number} marketProb - 市场赔率 (0-1)
 */
function compareProbabilities(aiProb, marketProb) {
  const diff = aiProb - marketProb;
  const diffPercent = (diff * 100).toFixed(1);
  
  if (Math.abs(diff) < 0.05) {
    return {
      verdict: 'NEUTRAL',
      message: `AI概率与市场赔率基本一致（差异${diffPercent}%）`,
      opportunity: false
    };
  }
  
  if (diff > 0) {
    return {
      verdict: 'UNDERPRICED',
      message: `AI认为市场低估了此事件（高${diffPercent}%）`,
      opportunity: true,
      direction: 'BUY YES'
    };
  } else {
    return {
      verdict: 'OVERPRICED',
      message: `AI认为市场高估了此事件（低${Math.abs(diffPercent)}%）`,
      opportunity: true,
      direction: 'BUY NO'
    };
  }
}

/**
 * 格式化分析结果
 */
function formatAnalysisOutput(event, aiResult, marketData) {
  const lines = [
    '═'.repeat(50),
    `📊 AI概率分析: "${event}"`,
    '═'.repeat(50),
    '',
    '🤖 AI分析结果:',
    `   概率: ${(aiResult.probability * 100).toFixed(1)}%`,
    '',
    '   分析理由:'
  ];
  
  for (const factor of aiResult.reasoning) {
    lines.push(`   • ${factor}`);
  }
  
  if (marketData) {
    lines.push('');
    lines.push('📈 相关市场:');
    if (marketData.question) {
      lines.push(`   ${marketData.question}`);
    }
    lines.push(`   Yes: ${(marketData.yesPrice * 100).toFixed(1)}%`);
    lines.push(`   No: ${(marketData.noPrice * 100).toFixed(1)}%`);
    
    const comparison = compareProbabilities(aiResult.probability, marketData.yesPrice);
    lines.push('');
    lines.push('💡 价值分析:');
    lines.push(`   ${comparison.message}`);
    
    if (comparison.opportunity) {
      lines.push(`   建议: ${comparison.direction}`);
    }
    
    lines.push('');
    lines.push(`🔗 ${marketData.url}`);
  } else {
    lines.push('');
    lines.push('📈 未找到相关市场');
    lines.push('💡 在Polymarket搜索: https://polymarket.com/markets');
  }
  
  lines.push('');
  lines.push('═'.repeat(50));
  
  return lines.join('\n');
}

module.exports = {
  analyzeEventProbability,
  compareProbabilities,
  formatAnalysisOutput
};
