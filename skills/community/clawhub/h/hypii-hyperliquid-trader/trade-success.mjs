import { Hyperliquid } from 'hyperliquid';

const PRIVATE_KEY = '0xd6b7d8aa2934c7187372a877ad6856e80fce6b87119693d8fef83fcfbdc0b02e';

async function executeTradeFixed() {
  console.log('🚀 HYPERLIQUID LIVE TRADE - TICK SIZE FIXED');
  console.log('============================================');
  console.log('');
  
  const sdk = new Hyperliquid({
    privateKey: PRIVATE_KEY,
    enableWs: false
  });
  
  try {
    // 1. Get market metadata
    console.log('📊 Getting market metadata...');
    const meta = await sdk.info.perpetuals.getMeta();
    const btcInfo = meta.universe.find(u => u.name === 'BTC-PERP');
    console.log('   ✅ BTC Info:', JSON.stringify(btcInfo));
    console.log(`   📏 szDecimals: ${btcInfo.szDecimals}`);
    console.log('');
    
    // 2. Get current price
    console.log('💰 Getting current price...');
    const prices = await sdk.info.getAllMids();
    const btcPrice = parseFloat(prices['BTC-PERP']);
    console.log(`   BTC-PERP: $${btcPrice}`);
    console.log('');
    
    // 3. Calculate valid price based on szDecimals
    // szDecimals = 5 means size must be in multiples of 10^-5 = 0.00001
    // But for price, we need to check what the actual tick size is
    // Let's try with price rounded to nearest integer
    const targetPrice = btcPrice * 1.05;
    const validPrice = Math.ceil(targetPrice); // Round to integer
    
    console.log('📐 Price calculation');
    console.log(`   Current: $${btcPrice}`);
    console.log(`   Target (5%): $${targetPrice.toFixed(2)}`);
    console.log(`   Valid price: $${validPrice} (rounded to integer)`);
    console.log('');
    
    // 4. Execute trade
    console.log('🚀 EXECUTING TRADE');
    console.log('   ================');
    console.log(`   Coin: BTC-PERP`);
    console.log(`   Side: BUY`);
    console.log(`   Size: 0.00001 (minimum for szDecimals=5)`);
    console.log(`   Price: $${validPrice}`);
    console.log('');
    
    const result = await sdk.exchange.placeOrder({
      coin: 'BTC-PERP',
      is_buy: true,
      sz: 0.00001,  // Minimum size for szDecimals=5
      limit_px: validPrice,
      order_type: { limit: { tif: 'Ioc' } },
      reduce_only: false
    });
    
    console.log('📋 RAW RESULT:');
    console.log(JSON.stringify(result, null, 2));
    console.log('');
    
    // Parse result
    if (result.status === 'ok') {
      const status = result.response?.data?.statuses?.[0];
      
      if (status.filled) {
        console.log('✅✅✅ SUCCESS! ✅✅✅');
        console.log('');
        console.log('📊 Trade Executed:');
        console.log(`   Size: ${status.filled.totalSz} BTC`);
        console.log(`   Avg Price: $${status.filled.avgPx}`);
        console.log(`   Fee: ${status.filled.fee} ${status.filled.feeToken}`);
        console.log('');
        console.log('🎉 Hypii Trading Agent is LIVE!');
      } else if (status.resting) {
        console.log('⏳ Order resting, ID:', status.resting.oid);
      } else if (status.error) {
        console.log('❌ Order error:', status.error);
      }
    }
    
    console.log('');
    console.log('🔗 View position: https://app.hyperliquid.xyz/portfolio');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    console.error('Stack:', error.stack);
  }
}

executeTradeFixed();
