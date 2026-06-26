import { HypiiTraderFixed } from './test-fixed.mjs';

const PRIVATE_KEY = '0xd6b7d8aa2934c7187372a877ad6856e80fce6b87119693d8fef83fcfbdc0b02e';

async function executeRealTrade() {
  console.log('🚀 EXECUTING REAL TRADE');
  console.log('=======================');
  console.log('⚠️  This will execute a real trade on Hyperliquid!');
  console.log('');
  
  const trader = new HypiiTraderFixed(PRIVATE_KEY);
  
  try {
    // Execute small test trade
    const result = await trader.executeTrade('BTC', 'buy', 0.0001);
    
    console.log('');
    console.log('✅ TRADE EXECUTED!');
    console.log('===================');
    console.log('Result:', JSON.stringify(result, null, 2));
    
  } catch (error) {
    console.error('❌ Trade failed:', error.message);
    console.error('Details:', error.stack);
  }
}

executeRealTrade();
