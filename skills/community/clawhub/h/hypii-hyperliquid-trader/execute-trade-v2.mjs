import { HypiiTraderFixed } from './test-fixed.mjs';

const PRIVATE_KEY = '0xd6b7d8aa2934c7187372a877ad6856e80fce6b87119693d8fef83fcfbdc0b02e';

async function executeRealTrade() {
  console.log('🚀 EXECUTING REAL TRADE - ATTEMPT 2');
  console.log('====================================');
  console.log('⚠️  This will execute a real trade on Hyperliquid!');
  console.log('');
  
  const trader = new HypiiTraderFixed(PRIVATE_KEY);
  
  try {
    // Get current price first
    const btcPrice = await trader.getPrice('BTC');
    console.log(`📊 Current BTC Price: $${btcPrice}`);
    console.log('');
    
    // Use exact price from API
    const currentPrice = parseFloat(btcPrice);
    const slippagePrice = Math.round(currentPrice * 1.05 * 100) / 100; // Round to 2 decimals
    
    console.log('🚀 Executing Trade:');
    console.log(`   Coin: BTC-PERP`);
    console.log(`   Side: BUY`);
    console.log(`   Size: 0.0001`);
    console.log(`   Current Price: $${currentPrice}`);
    console.log(`   Limit Price: $${slippagePrice} (5% slippage, rounded)`);
    console.log('');
    
    // Execute with corrected price
    const sdk = await trader.init();
    const result = await sdk.exchange.placeOrder({
      coin: 'BTC-PERP',
      is_buy: true,
      sz: 0.0001,
      limit_px: slippagePrice,
      order_type: { limit: { tif: 'Ioc' } },
      reduce_only: false
    });
    
    console.log('');
    console.log('✅ TRADE RESULT:');
    console.log('================');
    console.log(JSON.stringify(result, null, 2));
    
    if (result.status === 'ok') {
      console.log('');
      console.log('🎉 Trade executed successfully!');
    } else {
      console.log('');
      console.log('⚠️  Trade may have issues, check result above');
    }
    
  } catch (error) {
    console.error('❌ Trade failed:', error.message);
    console.error('Stack:', error.stack);
  }
}

executeRealTrade();
