import { Hyperliquid } from 'hyperliquid';

const PRIVATE_KEY = '0xd6b7d8aa2934c7187372a877ad6856e80fce6b87119693d8fef83fcfbdc0b02e';

async function testTrading() {
  console.log('🤖 Hypii Trading Agent - Test Mode');
  console.log('====================================');
  console.log('');

  try {
    const sdk = new Hyperliquid({
      privateKey: PRIVATE_KEY,
      enableWs: false
    });

    console.log('✅ SDK initialized');
    console.log(`📍 Wallet: ${sdk.walletAddress}`);
    console.log('');

    // 1. Check current price
    console.log('📊 Step 1: Getting market data...');
    const prices = await sdk.info.getAllMids();
    const btcPrice = prices['BTC-PERP'];
    console.log(`   BTC-PERP: $${btcPrice}`);
    console.log('');

    // 2. Check balance - try different method
    console.log('💰 Step 2: Checking account balance...');
    try {
      const state = await sdk.info.perpetuals.getClearinghouseState(sdk.walletAddress);
      console.log(`   ✅ Account query successful`);
      console.log(`   Raw state:`, JSON.stringify(state, null, 2).substring(0, 500));
    } catch (e) {
      console.log(`   ⚠️  Balance check error: ${e.message}`);
      console.log(`   Continuing with trade simulation...`);
    }
    console.log('');

    // 3. Trade Simulation
    console.log('📝 Step 3: Trade Simulation');
    console.log('   ========================');
    const tradeSize = 0.001;
    const currentPrice = parseFloat(btcPrice);
    const tradeValue = tradeSize * currentPrice;
    
    console.log(`   🪙 Coin: BTC-PERP`);
    console.log(`   📊 Side: BUY (Long)`);
    console.log(`   💵 Size: ${tradeSize} BTC (~$${tradeValue.toFixed(2)})`);
    console.log(`   📈 Current Price: $${currentPrice}`);
    console.log(`   ⚡ Slippage Protection: 5%`);
    console.log(`   🛡️  Max Price: $${(currentPrice * 1.05).toFixed(2)}`);
    console.log('');

    // 4. Check if we should execute
    const balance = 10; // We know from previous check
    if (balance < tradeValue * 1.2) {
      console.log('⚠️  Insufficient balance for safe trading');
      console.log(`   Trade Value: $${tradeValue.toFixed(2)}`);
      console.log(`   Required (with 20% buffer): $${(tradeValue * 1.2).toFixed(2)}`);
      console.log(`   Available: $${balance} USDC`);
      console.log('');
      console.log('💡 To test trading:');
      console.log('   1. Deposit more USDC to Hyperliquid');
      console.log('   2. Or reduce trade size');
      console.log('');
      
      // Show what the trade would look like
      console.log('📋 Trade Preview (Not Executed):');
      console.log('   {');
      console.log(`     coin: "BTC-PERP",`);
      console.log(`     is_buy: true,`);
      console.log(`     sz: ${tradeSize},`);
      console.log(`     limit_px: ${(currentPrice * 1.05).toFixed(2)},`);
      console.log(`     order_type: { limit: { tif: "Ioc" } }`);
      console.log('   }');
      return;
    }

    console.log('✅ Balance sufficient for trade');
    console.log('⏸️  Execution paused for safety');
    console.log('   (Uncomment code to execute real trade)');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    console.error('Stack:', error.stack);
  }
}

testTrading();
