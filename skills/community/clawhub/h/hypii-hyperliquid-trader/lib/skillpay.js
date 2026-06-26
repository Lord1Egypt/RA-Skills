/**
 * SkillPay Billing Integration - Dev Mode
 * Temporary solution until official API key is obtained
 */

export class SkillPayBilling {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseUrl = 'https://api.skillpay.me/v1';
    this.devMode = !apiKey;
  }

  /**
   * Charge user for skill usage
   * DEV MODE: Logs charges but doesn't actually bill
   */
  async charge(userId, amount, skillSlug = 'hypii-hyperliquid-trader') {
    // Development mode - no real billing
    if (this.devMode) {
      console.log(`[SkillPay DEV MODE] Charge: ${amount} USDT to user ${userId}`);
      
      // Simulate successful charge
      return { 
        paid: true, 
        debug: true, 
        amount,
        message: `💳 [DEV MODE] Would charge ${amount} USDT`,
        note: 'SkillPay API key not configured - running in dev mode'
      };
    }

    // Production mode - real billing
    try {
      const response = await fetch(`${this.baseUrl}/billing/charge`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`
        },
        body: JSON.stringify({
          user_id: userId,
          amount: amount,
          currency: 'USDT',
          skill_slug: skillSlug,
          metadata: {
            timestamp: new Date().toISOString(),
            skill: skillSlug
          }
        })
      });

      const result = await response.json();

      if (result.success) {
        return {
          paid: true,
          amount: amount,
          transactionId: result.transaction_id,
          message: `Charged ${amount} USDT`
        };
      } else {
        return {
          paid: false,
          amount: amount,
          paymentUrl: result.payment_url,
          message: result.message || `Payment required: ${amount} USDT`,
          error: result.error
        };
      }
    } catch (error) {
      console.error('SkillPay charge error:', error);
      return {
        paid: false,
        error: error.message,
        message: `Billing error: ${error.message}`
      };
    }
  }

  /**
   * Check if running in dev mode
   */
  isDevMode() {
    return this.devMode;
  }

  /**
   * Get billing status
   */
  getStatus() {
    if (this.devMode) {
      return {
        mode: 'development',
        message: 'Running in dev mode - no real billing',
        action: 'Contact OpenClaw team for SkillPay API key'
      };
    }
    return {
      mode: 'production',
      message: 'SkillPay billing active'
    };
  }
}
