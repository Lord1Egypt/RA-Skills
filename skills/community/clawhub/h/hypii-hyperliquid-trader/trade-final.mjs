import { Hyperliquid } from 'hyperliquid';

const PRIVATE_KEY = '0xd6b7d8aa2934c7187372a877ad6856e80fce6b87119693d8fef83fcfbdc0b02e';

async function executeTradeWithCorrectPrice() {
  console.log('🚀 HYPERLIQUID LIVE TRADE - FINAL ATTEMPT');
  console.log('==========================================');
  console.log('');
  
  const sdk = new Hyperliquid({
    privateKey: PRIVATE_KEY,
    enableWs: false
  });
  
  try {
    // 1. Get market metadata to find tick size
    console.log('📊 Step 1: Getting market metadata...');
    const meta = await sdk.info.perpetuals.getMeta();
    const btcInfo = meta.universe.find(u => u.name === 'BTC');
    console.log('   ✅ BTC Info:', JSON.stringify(btcInfo, null, 2));
    console.log('');
    
    // 2. Get current price
    console.log('💰 Step 2: Getting current price...');
    const prices = await sdk.info.getAllMids();
    const btcPrice = parseFloat(prices['BTC-PERP']);
    console.log(`   BTC-PERP: $${btcPrice}`);
    console.log('');
    
    // 3. Calculate valid price
    // BTC tick size is typically 0.1 on Hyperliquid
    const tickSize = 0.1;
    const targetPrice = btcPrice * 1.05; // 5% slippage
    const validPrice = Math.ceil(targetPrice / tickSize) * tickSize;
    
    console.log('📐 Step 3: Price calculation');
    console.log(`   Current: $${btcPrice}`);
    console.log(`   Target (5% slippage): $${targetPrice}`);
    console.log(`   Tick size: ${tickSize}`);
    console.log(`   Valid price: $${validPrice}`);
    console.log('');
    
    // 4. Execute trade
    console.log('🚀 Step 4: EXECUTING TRADE');
    console.log('   ========================');
    console.log(`   Coin: BTC-PERP`);
    console.log(`   Side: BUY`);
    console.log(`   Size: 0.0001`);
    console.log(`   Price: $${validPrice}`);
    console.log(`   Value: ~$${(0.0001 * btcPrice).toFixed(2)}`);
    console.log('');
    console.log('   ⏳ Submitting to Hyperliquid...');
    console.log('');
    
    const result = await sdk.exchange.placeOrder({
      coin: 'BTC-PERP',
      is_buy: true,
      sz: 0.0001,
      limit_px: validPrice,
      order_type: { limit: { tif: 'Ioc' } },
      reduce_only: false
    });
    
    console.log('📋 RESULT:');
    console.log(JSON.stringify(result, null, 2));
    console.log('');
    
    // Parse result
    if (result.status === 'ok') {
      const status = result.response?.data?.statuses?.[0];
      
      if (status.filled) {
        console.log('✅✅✅ TRADE SUCCESSFUL! ✅✅✅');
        console.log('');
        console.log('📊 Trade Details:');
        console.log(`   Total Size: ${status.filled.totalSz} BTC`);
        console.log(`   Avg Price: $${status.filled.avgPx}`);
        console.log(`   Fee: ${status.filled.fee} ${status.filled.feeToken}`);
        console.log('');
        console.log('🎉 Hypii Trading Agent is working!');
      } else if (status.resting) {
        console.log('⏳ Order resting, ID:', status.resting.oid);
      } else if (status.error) {
        console.log('❌ Error:', status.error);
      }
    } else {
      console.log('❌ Request failed:', result);
    }
    
    console.log('');
    console.log('🔗 Check position:');
    console.log('   https://app.hyperliquid.xyz/portfolio');
    
  } catch (error) {
    console.error('❌ Fatal error:', error.message);
    console.error('Stack:', error.stack);
  }
}

executeTradeWithCorrectPrice();
