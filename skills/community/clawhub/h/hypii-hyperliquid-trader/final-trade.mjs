import { Hyperliquid } from 'hyperliquid';

const PRIVATE_KEY = '0xd6b7d8aa2934c7187372a877ad6856e80fce6b87119693d8fef83fcfbdc0b02e';

async function executeFinalTrade() {
  console.log('🚀 HYPERLIQUID LIVE TRADE');
  console.log('==========================');
  console.log('');
  
  const sdk = new Hyperliquid({
    privateKey: PRIVATE_KEY,
    enableWs: false
  });
  
  try {
    // Get current price
    const prices = await sdk.info.getAllMids();
    const btcPrice = parseFloat(prices['BTC-PERP']);
    
    // Calculate valid price (tick size 0.1)
    const tickSize = 0.1;
    const slippagePrice = Math.ceil(btcPrice * 1.05 / tickSize) * tickSize;
    
    console.log('📊 Trade Parameters:');
    console.log('   Coin: BTC-PERP');
    console.log('   Side: BUY (Long)');
    console.log('   Size: 0.0001 BTC');
    console.log(`   Current Price: $${btcPrice}`);
    console.log(`   Limit Price: $${slippagePrice} (5% slippage)`);
    console.log(`   Estimated Value: $${(0.0001 * btcPrice).toFixed(2)}`);
    console.log('');
    
    // Execute trade
    console.log('⏳ Submitting order...');
    const result = await sdk.exchange.placeOrder({
      coin: 'BTC-PERP',
      is_buy: true,
      sz: 0.0001,
      limit_px: slippagePrice,
      order_type: { limit: { tif: 'Ioc' } },
      reduce_only: false
    });
    
    console.log('');
    console.log('📋 RAW RESULT:');
    console.log(JSON.stringify(result, null, 2));
    console.log('');
    
    // Parse result
    if (result.status === 'ok' && result.response?.data?.statuses) {
      const status = result.response.data.statuses[0];
      
      if (status.error) {
        console.log('❌ ORDER FAILED');
        console.log('   Error:', status.error);
      } else if (status.filled) {
        console.log('✅ ORDER FILLED!');
        console.log('   Total Size:', status.filled.totalSz);
        console.log('   Avg Price:', status.filled.avgPx);
        console.log('   Fee:', status.filled.fee);
        console.log('   Fee Token:', status.filled.feeToken);
      } else if (status.resting) {
        console.log('⏳ ORDER RESTING');
        console.log('   Order ID:', status.resting.oid);
      } else {
        console.log('⚠️  UNKNOWN STATUS');
        console.log('   Status:', JSON.stringify(status));
      }
    }
    
    console.log('');
    console.log('🔍 Check your position at:');
    console.log('   https://app.hyperliquid.xyz/portfolio');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    console.error('Stack:', error.stack);
  }
}

executeFinalTrade();
