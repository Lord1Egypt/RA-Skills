import { Hyperliquid } from 'hyperliquid';

async function debugMeta() {
  const sdk = new Hyperliquid({ enableWs: false });
  
  try {
    console.log('🔍 Debugging Hyperliquid Metadata');
    console.log('=================================');
    console.log('');
    
    const meta = await sdk.info.perpetuals.getMeta();
    console.log('Meta keys:', Object.keys(meta));
    console.log('');
    
    if (meta.universe) {
      console.log('Universe type:', typeof meta.universe);
      console.log('Universe is array:', Array.isArray(meta.universe));
      console.log('Universe length:', meta.universe.length);
      console.log('');
      
      console.log('First 3 assets:');
      meta.universe.slice(0, 3).forEach((asset, i) => {
        console.log(`  ${i}:`, JSON.stringify(asset));
      });
    }
    
    // Find BTC
    const btcAsset = meta.universe?.find(u => u.name === 'BTC');
    console.log('');
    console.log('BTC Asset:', JSON.stringify(btcAsset, null, 2));
    
  } catch (error) {
    console.error('Error:', error.message);
  }
}

debugMeta();
