import { Hyperliquid } from 'hyperliquid';

const address = '0x14de3De2C46E3Bf2D47B1ca8A6A6fd11A5F9D3Ca';

async function checkBalance() {
  const sdk = new Hyperliquid({ enableWs: false });
  
  try {
    console.log('🔍 Checking Hyperliquid balance for:', address);
    console.log('');
    
    const state = await sdk.info.perpetuals.getClearinghouseState(address);
    
    console.log('📊 Portfolio Summary');
    console.log('==================');
    console.log('💰 Account Value:', state.marginSummary?.accountValue || '0', 'USDC');
    console.log('💵 Withdrawable:', state.withdrawable || '0', 'USDC');
    console.log('');
    
    const positions = state.assetPositions || [];
    if (positions.length > 0) {
      console.log('📈 Open Positions');
      console.log('==================');
      positions.forEach((p, i) => {
        const pos = p.position;
        console.log(`\nPosition #${i + 1}:`);
        console.log(`  🪙 Coin: ${pos.coin}`);
        console.log(`  📊 Size: ${pos.szi}`);
        console.log(`  💵 Entry Price: $${pos.entryPx || 'N/A'}`);
        console.log(`  📈 Unrealized PnL: $${pos.unrealizedPnl || '0'}`);
        console.log(`  ⚡ Leverage: ${pos.leverage?.value || '1'}x`);
      });
    } else {
      console.log('📭 No open positions');
    }
    
    console.log('');
    console.log('⚠️  SECURITY REMINDER:');
    console.log('Private key was exposed in chat. Recommend:');
    console.log('1. Transfer funds to new wallet if > $100');
    console.log('2. Use testnet for development');
    console.log('3. Store private keys in 1Password');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

checkBalance();
