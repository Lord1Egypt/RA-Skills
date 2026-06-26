const axios = require('axios');

/**
 * SkillPay Payment Integration
 */
class SkillPayment {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseURL = 'https://api.skillpay.me/v1';
    this.pricePerCall = 0.001; // USDT
  }

  /**
   * Verify payment transaction
   * @param {string} userId - User ID
   * @param {string} transactionId - Transaction ID
   * @returns {Promise<boolean>}
   */
  async verifyPayment(userId, transactionId) {
    try {
      const response = await axios.post(
        `${this.baseURL}/verify`,
        {
          userId,
          transactionId,
          amount: this.pricePerCall,
          currency: 'USDT'
        },
        {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json'
          }
        }
      );

      return response.data.verified === true;
    } catch (error) {
      console.error('Payment verification failed:', error.message);
      return false;
    }
  }

  /**
   * Create payment request
   * @param {string} userId - User ID
   * @returns {Promise<object>}
   */
  async createPaymentRequest(userId) {
    try {
      const response = await axios.post(
        `${this.baseURL}/payment/create`,
        {
          userId,
          amount: this.pricePerCall,
          currency: 'USDT',
          description: 'GitHub Trending Monitor - API Call'
        },
        {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json'
          }
        }
      );

      return {
        paymentId: response.data.paymentId,
        paymentUrl: response.data.paymentUrl,
        amount: this.pricePerCall,
        currency: 'USDT'
      };
    } catch (error) {
      console.error('Payment request creation failed:', error.message);
      throw error;
    }
  }

  /**
   * Log usage for analytics
   * @param {string} userId - User ID
   * @param {string} action - Action type
   */
  async logUsage(userId, action) {
    try {
      await axios.post(
        `${this.baseURL}/usage/log`,
        {
          userId,
          action,
          timestamp: new Date().toISOString(),
          amount: this.pricePerCall
        },
        {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json'
          }
        }
      );
    } catch (error) {
      console.error('Usage logging failed:', error.message);
    }
  }
}

module.exports = SkillPayment;
