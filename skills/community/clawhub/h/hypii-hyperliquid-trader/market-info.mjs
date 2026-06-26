import { Hyperliquid } from 'hyperliquid';

async function getMarketInfo() {
  const sdk = new Hyperliquid({ enableWs: false });
  
  try {
    console.log('📊 Getting Hyperliquid Market Info');
    console.log('==================================');
    console.log('');
    
    // Get meta information
    const meta = await sdk.info.perpetuals.getMeta();
    console.log('✅ Meta data retrieved');
    console.log('');
    
    // Find BTC info
    const btcInfo = meta.universe.find(u => u.name === 'BTC');
    if (btcInfo) {
      console.log('🪙 BTC-PERP Info:');
      console.log('   Name:', btcInfo.name);
      console.log('   SzDecimals:', btcInfo.szDecimals);
      console.log('   MaxLeverage:', btcInfo.maxLeverage);
      console.log('   OnlyIsolated:', btcInfo.onlyIsolated);
      console.log('');
    }
    
    // Get current price
    const prices = await sdk.info.getAllMids();
    console.log('💰 Current Prices:');
    console.log('   BTC-PERP:', prices['BTC-PERP']);
    console.log('   ETH-PERP:', prices['ETH-PERP']);
    console.log('');
    
    // Calculate valid price
    const btcPrice = parseFloat(prices['BTC-PERP']);
    const tickSize = 0.1; // BTC tick size is typically 0.1
    const validPrice = Math.ceil(btcPrice * 1.05 / tickSize) * tickSize;
    
    console.log('📐 Price Calculation:');
    console.log('   Current Price:', btcPrice);
    console.log('   Tick Size:', tickSize);
    console.log('   With 5% slippage:', btcPrice * 1.05);
    console.log('   Valid Price (rounded):', validPrice);
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

getMarketInfo();
