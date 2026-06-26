import { X402Billing } from './lib/x402.js';

async function testX402() {
  console.log('🧪 Testing x402 Integration');
  console.log('===========================');
  console.log('');

  // Test with dev mode (no private key)
  const billing = new X402Billing('0x14de3De2C46E3Bf2D47B1ca8A6A6fd11A5F9D3Ca');
  
  console.log('📊 Status:', billing.getStatus());
  console.log('');

  // Test payment request
  console.log('💰 Requesting payment...');
  const payment = await billing.requestPayment('user-123', 0.05, 'Strategy execution');
  console.log('Payment request:', JSON.stringify(payment, null, 2));
  console.log('');

  // Test charge method
  console.log('⚡ Charging for service...');
  const charge = await billing.charge('user-456', 0.1, 'auto_trade');
  console.log('Charge result:', JSON.stringify(charge, null, 2));
  console.log('');

  console.log('✅ x402 test complete!');
}

testX402().catch(console.error);
