#!/usr/bin/env node
/**
 * Paid Content Generator
 * 收费版内容生成器 - 每次调用 0.001 USDT
 */

const { chargeUser, getPaymentLink, SKILL_PRICE } = require('./skillpay');

// 内容类型配置
const CONTENT_TYPES = {
  xiaohongshu: {
    name: '小红书文案',
    price: 0.001,
    template: require('../templates/xiaohongshu')
  },
  video: {
    name: '视频脚本',
    price: 0.001,
    template: require('../templates/video')
  },
  article: {
    name: '公众号文章',
    price: 0.001,
    template: require('../templates/article')
  }
};

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.log(`
╔════════════════════════════════════════════════════════╗
║        AI Content Generator - 收费版                    ║
║        每次调用 0.001 USDT (约0.007元)                  ║
╚════════════════════════════════════════════════════════╝

用法: node generate.js <类型> <主题> [用户ID]

类型:
  xiaohongshu  - 小红书文案
  video        - 视频脚本
  article      - 公众号文章

示例:
  node generate.js xiaohongshu "布偶猫品相分析"
  node generate.js video "2026国产AI测评" user_123

💰 支付: BNB Chain USDT，最低充值 8 USDT
`);
    process.exit(1);
  }

  const [type, topic, userId = 'anonymous'] = args;
  const config = CONTENT_TYPES[type];

  if (!config) {
    console.error(`❌ 错误: 未知类型 "${type}"`);
    console.error('支持类型:', Object.keys(CONTENT_TYPES).join(', '));
    process.exit(1);
  }

  console.log(`\n📝 生成${config.name}: ${topic}`);
  console.log(`💰 费用: ${config.price} USDT`);
  console.log(`👤 用户: ${userId}`);

  // 扣费
  console.log('\n⏳ 检查余额并扣费...');
  const chargeResult = await chargeUser(userId, config.price);

  if (!chargeResult.ok) {
    console.log('\n❌ 余额不足');
    console.log(`当前余额: ${chargeResult.balance} USDT`);
    console.log('\n💳 请充值后继续:');
    const paymentUrl = await getPaymentLink(userId, 8);
    console.log(paymentUrl);
    process.exit(1);
  }

  console.log(`✅ 扣费成功，剩余余额: ${chargeResult.balance} USDT`);

  // 生成内容
  console.log('\n🤖 生成内容中...');
  const content = await config.template.generate(topic);

  console.log('\n' + '═'.repeat(50));
  console.log('📄 生成结果');
  console.log('═'.repeat(50) + '\n');
  console.log(content);
  console.log('\n' + '═'.repeat(50));
  console.log('✅ 完成');
}

main().catch(err => {
  console.error('\n❌ 错误:', err.message);
  process.exit(1);
});
