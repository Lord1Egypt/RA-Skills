import { Hyperliquid } from 'hyperliquid';

async function getDetailedMarketInfo() {
  const sdk = new Hyperliquid({ enableWs: false });
  
  try {
    console.log('🔍 Detailed Market Info');
    console.log('=======================');
    console.log('');
    
    const meta = await sdk.info.perpetuals.getMeta();
    
    // Print all assets
    console.log('📋 All Available Assets:');
    meta.universe.forEach((asset, index) => {
      console.log(`   ${index}: ${asset.name} - szDecimals: ${asset.szDecimals}`);
    });
    console.log('');
    
    // Get BTC specifically
    const btcIndex = meta.universe.findIndex(u => u.name === 'BTC');
    const btcInfo = meta.universe[btcIndex];
    
    console.log('🪙 BTC Details:');
    console.log('   Index:', btcIndex);
    console.log('   Name:', btcInfo.name);
    console.log('   szDecimals:', btcInfo.szDecimals);
    console.log('   maxLeverage:', btcInfo.maxLeverage);
    console.log('');
    
    // Try to get more info about tick sizes
    const prices = await sdk.info.getAllMids();
    const btcPrice = prices['BTC-PERP'];
    
    console.log('💰 Price Info:');
    console.log('   Current Price:', btcPrice);
    console.log('   Price Type:', typeof btcPrice);
    console.log('');
    
    // Test different price formats
    console.log('📐 Testing Price Formats:');
    const currentPrice = parseFloat(btcPrice);
    const testPrices = [
      Math.round(currentPrice * 1.05),
      Math.round(currentPrice * 1.05 * 10) / 10,
      Math.round(currentPrice * 1.05 * 100) / 100,
      Math.round(currentPrice * 1.05 * 1000) / 1000,
      currentPrice * 1.05
    ];
    
    testPrices.forEach((p, i) => {
      console.log(`   Test ${i + 1}: ${p} (type: ${typeof p})`);
    });
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

getDetailedMarketInfo();
