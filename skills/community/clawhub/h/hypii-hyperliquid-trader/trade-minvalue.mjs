import { Hyperliquid } from 'hyperliquid';

const PRIVATE_KEY = '0xd6b7d8aa2934c7187372a877ad6856e80fce6b87119693d8fef83fcfbdc0b02e';

async function executeTradeMinValue() {
  console.log('🚀 HYPERLIQUID LIVE TRADE - MIN VALUE ADJUSTED');
  console.log('===============================================');
  console.log('');
  
  const sdk = new Hyperliquid({
    privateKey: PRIVATE_KEY,
    enableWs: false
  });
  
  try {
    // Get current price
    const prices = await sdk.info.getAllMids();
    const btcPrice = parseFloat(prices['BTC-PERP']);
    
    // Calculate size for $10.50 minimum value (with buffer)
    const minValue = 10.50;
    const size = minValue / btcPrice;
    
    // Round to szDecimals = 5 (0.00001)
    const validSize = Math.ceil(size * 100000) / 100000;
    
    // Price with 5% slippage, rounded to integer
    const validPrice = Math.ceil(btcPrice * 1.05);
    
    console.log('📊 Trade Parameters');
    console.log('===================');
    console.log(`   BTC Price: $${btcPrice}`);
    console.log(`   Size: ${validSize} BTC`);
    console.log(`   Price: $${validPrice}`);
    console.log(`   Value: ~$${(validSize * btcPrice).toFixed(2)}`);
    console.log('');
    
    // Check balance first
    console.log('💰 Checking balance...');
    const balance = await sdk.info.perpetuals.getClearinghouseState('0x14de3De2C46E3Bf2D47B1ca8A6A6fd11A5F9D3Ca');
    const available = parseFloat(balance.withdrawable || 0);
    console.log(`   Available: ${available} USDC`);
    console.log('');
    
    if (available < 11) {
      console.log('⚠️  Insufficient balance');
      console.log(`   Required: ~$11 (including fees)`);
      console.log(`   Available: $${available}`);
      console.log('');
      console.log('💡 Recommendation: Deposit more USDC to Hyperliquid');
      console.log('   Current balance too close to minimum order size');
      return;
    }
    
    // Execute trade
    console.log('🚀 EXECUTING TRADE');
    console.log('   ================');
    console.log('   ⏳ Submitting...');
    console.log('');
    
    const result = await sdk.exchange.placeOrder({
      coin: 'BTC-PERP',
      is_buy: true,
      sz: validSize,
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
        console.log('📊 Details:');
        console.log(`   Size: ${status.filled.totalSz} BTC`);
        console.log(`   Avg Price: $${status.filled.avgPx}`);
        console.log(`   Fee: ${status.filled.fee} ${status.filled.feeToken}`);
        console.log('');
        console.log('🎉 Hypii Trading Agent is LIVE!');
      } else if (status.resting) {
        console.log('⏳ Order resting, ID:', status.resting.oid);
      } else if (status.error) {
        console.log('❌ Error:', status.error);
      }
    }
    
    console.log('');
    console.log('🔗 View: https://app.hyperliquid.xyz/portfolio');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

executeTradeMinValue();
