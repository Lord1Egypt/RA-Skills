/**
 * x402 Payment Integration - Simplified Version
 * No external dependencies, works in dev mode
 */

export class X402Billing {
  constructor(recipientAddress, privateKey = null) {
    this.recipientAddress = recipientAddress;
    this.privateKey = privateKey;
    this.devMode = !privateKey;
  }

  /**
   * Request payment from user
   */
  async requestPayment(userId, amount, description = 'Hypii Trading Service') {
    const paymentId = `hypii-${Date.now()}-${userId}`;
    
    if (this.devMode) {
      return {
        status: 'dev_mode',
        paid: true,
        message: `💳 [DEV MODE] Would request ${amount} USDC`,
        paymentId,
        amount,
        recipient: this.recipientAddress,
        network: 'Base',
        note: 'Set X402_PRIVATE_KEY to enable real payments'
      };
    }

    // Production: Generate real payment request
    const paymentRequest = {
      version: 'x402-1.0',
      paymentId,
      amount: (amount * 1e6).toString(), // USDC has 6 decimals
      token: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913', // USDC on Base
      recipient: this.recipientAddress,
      network: 'base',
      description,
      timestamp: Date.now(),
      expiresAt: Date.now() + 300000 // 5 minutes
    };

    return {
      status: 'payment_required',
      message: `Please pay ${amount} USDC to continue`,
      paymentId,
      amount,
      recipient: this.recipientAddress,
      network: 'Base',
      paymentUrl: `https://x402.org/pay?r=${btoa(JSON.stringify(paymentRequest))}`,
      expiresAt: paymentRequest.expiresAt
    };
  }

  /**
   * Charge user for service
   */
  async charge(userId, amount, serviceType = 'trading') {
    const descriptions = {
      base_call: 'Basic market query',
      strategy_execution: 'AI strategy execution',
      auto_trade: 'Automated trade execution'
    };

    // Check free tier first
    if (this.hasFreeCalls && this.hasFreeCalls(userId)) {
      return {
        paid: true,
        free: true,
        message: '🆓 Free call (5 per day)'
      };
    }

    return this.requestPayment(
      userId, 
      amount, 
      descriptions[serviceType] || 'Hypii Trading Service'
    );
  }

  /**
   * Verify payment
   */
  async verifyPayment(paymentId) {
    if (this.devMode) {
      return { verified: true, devMode: true };
    }
    return { verified: false, message: 'Verification requires blockchain query' };
  }

  /**
   * Get status
   */
  getStatus() {
    if (this.devMode) {
      return {
        mode: 'development',
        provider: 'x402',
        message: 'x402 in dev mode - no real payments',
        recipient: this.recipientAddress,
        action: 'Set X402_PRIVATE_KEY for production'
      };
    }
    return {
      mode: 'production',
      provider: 'x402',
      message: 'x402 payments active',
      recipient: this.recipientAddress
    };
  }
}
