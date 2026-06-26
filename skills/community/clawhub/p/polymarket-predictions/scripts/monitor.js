#!/usr/bin/env node
/**
 * Polymarket Monitor
 * 预测市场监控 - 每次调用 0.002 USDT
 */

const { chargeUser, getPaymentLink, SKILL_PRICE } = require('./skillpay');
const { getHotMarkets, searchMarkets, formatMarketOutput } = require('./polymarket');
const { analyzeEventProbability, formatAnalysisOutput } = require('./ai-analyzer');

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 1) {
    console.log(`
╔════════════════════════════════════════════════════════╗
║        Polymarket Monitor - 预测市场监控               ║
║        每次调用 0.002 USDT                             ║
╚════════════════════════════════════════════════════════╝

用法: node monitor.js <命令> [参数]

命令:
  hot              查看热门市场
  market <关键词>   搜索特定市场
  analyze <事件>    AI概率分析（开发中）
  whales           聪明钱追踪（开发中）

示例:
  node monitor.js hot
  node monitor.js market "比特币"

💰 支付: BNB Chain USDT，最低充值 8 USDT
`);
    process.exit(1);
  }

  const [command, ...params] = args;
  const userId = 'user_' + Date.now(); // 简化用户ID

  // 扣费
  console.log('\n⏳ 检查余额并扣费...');
  const chargeResult = await chargeUser(userId, SKILL_PRICE);

  if (!chargeResult.ok) {
    console.log('\n❌ 余额不足');
    console.log(`当前余额: ${chargeResult.balance} USDT`);
    console.log('\n💳 请充值后继续:');
    const paymentUrl = await getPaymentLink(userId, 8);
    console.log(paymentUrl);
    process.exit(1);
  }

  console.log(`✅ 扣费成功`);

  // 执行命令
  console.log('\n' + '═'.repeat(50));
  
  try {
    switch (command) {
      case 'hot': {
        console.log('🔥 热门市场\n');
        const markets = await getHotMarkets(5);
        for (const m of markets) {
          console.log(formatMarketOutput(m));
          console.log('\n' + '-'.repeat(50) + '\n');
        }
        break;
      }
      
      case 'market': {
        const query = params[0];
        if (!query) {
          console.log('❌ 请输入搜索关键词');
          process.exit(1);
        }
        console.log(`🔍 搜索: "${query}"\n`);
        const markets = await searchMarkets(query);
        const filtered = markets
          .filter(m => m.accepting_orders && m.tokens)
          .slice(0, 3)
          .map(m => ({
            question: m.question,
            slug: m.market_slug,
            url: `https://polymarket.com/event/${m.market_slug}`,
            options: m.tokens.map(t => ({
              outcome: t.outcome,
              price: t.price
            }))
          }));
        
        for (const m of filtered) {
          console.log(formatMarketOutput(m));
          console.log('\n' + '-'.repeat(50) + '\n');
        }
        break;
      }
      
      case 'analyze': {
        const event = params[0];
        if (!event) {
          console.log('❌ 请输入要分析的事件');
          console.log('示例: node monitor.js analyze "比特币年底突破10万美元"');
          process.exit(1);
        }
        
        console.log(`🤖 AI分析中: "${event}"\n`);
        
        // AI分析
        const aiResult = await analyzeEventProbability(event);
        
        // 搜索相关市场
        let marketData = null;
        try {
          // 提取关键词：比特币、特朗普等
          const keywords = event.match(/比特币|特朗普|AI|利率|中国|美国|以太坊|ETH|BTC/i);
          const searchTerm = keywords ? keywords[0] : event.split(' ').slice(0, 2).join(' ');
          
          const markets = await searchMarkets(searchTerm);
          if (markets.length > 0 && markets[0].tokens && markets[0].question.toLowerCase().includes(searchTerm.toLowerCase())) {
            const m = markets[0];
            marketData = {
              yesPrice: m.tokens[0]?.price || 0.5,
              noPrice: m.tokens[1]?.price || 0.5,
              url: `https://polymarket.com/event/${m.market_slug}`,
              question: m.question
            };
          }
        } catch (e) {
          // 搜索失败也没关系
        }
        
        console.log(formatAnalysisOutput(event, aiResult, marketData));
        break;
      }
      
      case 'whales': {
        console.log('🐋 聪明钱追踪功能开发中...');
        console.log('预计下周上线，敬请期待！');
        break;
      }
      
      default:
        console.log(`❌ 未知命令: ${command}`);
    }
  } catch (error) {
    console.log('❌ 错误:', error.message);
  }
  
  console.log('═'.repeat(50));
  console.log('✅ 完成');
}

main().catch(err => {
  console.error('\n❌ 错误:', err.message);
  process.exit(1);
});
