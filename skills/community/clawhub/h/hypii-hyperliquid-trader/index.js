/**
 * Hypii Hyperliquid Trading Agent
 * AI-powered trading strategies with SkillPay integration
 */

import { Hyperliquid } from 'hyperliquid';
import axios from 'axios';
import { SkillPayBilling } from './lib/skillpay.js';
import { X402Billing } from './lib/x402.js';
import { HypiiStrategyEngine } from './lib/hypii.js';
import { formatPortfolio, formatTradeResult, formatError } from './lib/formatters.js';

const SKILLPAY_API_KEY = process.env.SKILLPAY_API_KEY;
const X402_RECIPIENT = process.env.X402_RECIPIENT_ADDRESS || '0x75b90dffbd7c75c42d1ef9513ff9be66806fe232';
const X402_PRIVATE_KEY = process.env.X402_PRIVATE_KEY;
const HYPERLIQUID_PRIVATE_KEY = process.env.HYPERLIQUID_PRIVATE_KEY;
const HYPERLIQUID_ADDRESS = process.env.HYPERLIQUID_ADDRESS;
const HYPERLIQUID_TESTNET = process.env.HYPERLIQUID_TESTNET === '1';

// Pricing configuration
const PRICING = {
  base_call: 0.01,        // Basic queries
  strategy_execution: 0.05,  // Strategy analysis
  auto_trade: 0.1         // Automated trade execution
};

class HypiiTrader {
  constructor() {
    // Use x402 for payments (preferred) or fallback to SkillPay
    this.billing = X402_PRIVATE_KEY 
      ? new X402Billing(X402_RECIPIENT, X402_PRIVATE_KEY)
      : new SkillPayBilling(SKILLPAY_API_KEY);
    this.strategyEngine = new HypiiStrategyEngine();
    this.sdk = null;
    this.userCallCount = new Map(); // Track daily calls per user
  }

  async initSDK() {
    if (!this.sdk) {
      this.sdk = new Hyperliquid({
        privateKey: HYPERLIQUID_PRIVATE_KEY || undefined,
        testnet: HYPERLIQUID_TESTNET,
        enableWs: false
      });
    }
    return this.sdk;
  }

  /**
   * Check if user has free calls remaining
   */
  hasFreeCalls(userId) {
    const count = this.userCallCount.get(userId) || 0;
    return count < 5; // 5 free calls per day
  }

  /**
   * Increment user's call count
   */
  incrementCallCount(userId) {
    const current = this.userCallCount.get(userId) || 0;
    this.userCallCount.set(userId, current + 1);
  }

  /**
   * Process billing - free tier or charge user
   */
  async processBilling(userId, callType = 'base') {
    // Check free tier
    if (this.hasFreeCalls(userId)) {
      this.incrementCallCount(userId);
      return { paid: true, free: true, remaining: 5 - (this.userCallCount.get(userId) || 0) };
    }

    // Determine price based on call type
    const amount = PRICING[callType] || PRICING.base_call;
    
    // Charge user via SkillPay
    const result = await this.billing.charge(userId, amount, 'hypii-hyperliquid-trader');
    return result;
  }

  /**
   * Get portfolio overview
   */
  async getPortfolio(userId, address) {
    const billing = await this.processBilling(userId, 'base');
    if (!billing.paid) {
      return { error: 'PAYMENT_REQUIRED', message: billing.message, paymentUrl: billing.paymentUrl };
    }

    try {
      const sdk = await this.initSDK();
      const addr = address || HYPERLIQUID_ADDRESS || sdk.walletAddress;
      
      if (!addr) {
        return { error: 'ADDRESS_REQUIRED', message: 'Please set HYPERLIQUID_ADDRESS or HYPERLIQUID_PRIVATE_KEY' };
      }

      const state = await sdk.info.perpetuals.getClearinghouseState(addr);
      const positions = state.assetPositions || [];
      
      return {
        success: true,
        free: billing.free,
        remaining: billing.remaining,
        data: {
          address: addr,
          equity: state.marginSummary?.accountValue || '0',
          available: state.withdrawable || '0',
          positions: positions.map(p => ({
            coin: p.position?.coin,
            size: p.position?.szi,
            entryPrice: p.position?.entryPx,
            unrealizedPnl: p.position?.unrealizedPnl,
            leverage: p.position?.leverage?.value
          }))
        },
        message: formatPortfolio(state, billing.free, billing.remaining)
      };
    } catch (error) {
      return { error: 'API_ERROR', message: formatError(error) };
    }
  }

  /**
   * Get current price for a coin
   */
  async getPrice(userId, coin) {
    const billing = await this.processBilling(userId, 'base');
    if (!billing.paid) {
      return { error: 'PAYMENT_REQUIRED', message: billing.message };
    }

    try {
      const sdk = await this.initSDK();
      const normalizedCoin = this.normalizeCoin(coin);
      const prices = await sdk.info.getAllMids();
      
      if (!prices[normalizedCoin]) {
        return { error: 'UNKNOWN_COIN', message: `Coin ${coin} not found` };
      }

      return {
        success: true,
        free: billing.free,
        remaining: billing.remaining,
        data: {
          coin: normalizedCoin,
          price: prices[normalizedCoin],
          timestamp: new Date().toISOString()
        },
        message: `💰 ${normalizedCoin}: $${prices[normalizedCoin]}\n${billing.free ? `🆓 Free call (${billing.remaining} remaining today)` : `💳 Charged: 0.01 USDT`}`
      };
    } catch (error) {
      return { error: 'API_ERROR', message: formatError(error) };
    }
  }

  /**
   * Execute DCA strategy
   */
  async executeDCA(userId, params) {
    const billing = await this.processBilling(userId, 'strategy_execution');
    if (!billing.paid) {
      return { error: 'PAYMENT_REQUIRED', message: billing.message };
    }

    const { coin, amount, frequency, totalOrders } = params;
    
    try {
      const strategy = this.strategyEngine.createDCAStrategy({
        coin: this.normalizeCoin(coin),
        amount: parseFloat(amount),
        frequency, // 'daily', 'weekly'
        totalOrders: parseInt(totalOrders) || 10
      });

      return {
        success: true,
        charged: 0.05,
        data: strategy,
        message: `📊 DCA Strategy Created\n\n🪙 Coin: ${strategy.coin}\n💵 Amount/Order: $${strategy.amount}\n📅 Frequency: ${strategy.frequency}\n🔢 Total Orders: ${strategy.totalOrders}\n💳 Charged: 0.05 USDT\n\n⚠️ Note: This is a strategy plan. To execute trades, use 'auto_trade' mode.`
      };
    } catch (error) {
      return { error: 'STRATEGY_ERROR', message: formatError(error) };
    }
  }

  /**
   * Execute Grid Trading strategy
   */
  async executeGrid(userId, params) {
    const billing = await this.processBilling(userId, 'strategy_execution');
    if (!billing.paid) {
      return { error: 'PAYMENT_REQUIRED', message: billing.message };
    }

    const { coin, lowerPrice, upperPrice, grids, totalInvestment } = params;

    try {
      const sdk = await this.initSDK();
      const normalizedCoin = this.normalizeCoin(coin);
      const currentPrice = await this.getCurrentPrice(normalizedCoin);

      const strategy = this.strategyEngine.createGridStrategy({
        coin: normalizedCoin,
        currentPrice,
        lowerPrice: parseFloat(lowerPrice),
        upperPrice: parseFloat(upperPrice),
        grids: parseInt(grids) || 10,
        totalInvestment: parseFloat(totalInvestment)
      });

      return {
        success: true,
        charged: 0.05,
        data: strategy,
        message: `📈 Grid Trading Strategy Created\n\n🪙 Coin: ${strategy.coin}\n📊 Price Range: $${strategy.lowerPrice} - $${strategy.upperPrice}\n🔲 Grid Levels: ${strategy.grids}\n💵 Investment: $${strategy.totalInvestment}\n📍 Current Price: $${currentPrice}\n💳 Charged: 0.05 USDT`
      };
    } catch (error) {
      return { error: 'STRATEGY_ERROR', message: formatError(error) };
    }
  }

  /**
   * Execute automated trade
   */
  async executeTrade(userId, params) {
    if (!HYPERLIQUID_PRIVATE_KEY) {
      return { error: 'PRIVATE_KEY_REQUIRED', message: 'Trading requires HYPERLIQUID_PRIVATE_KEY' };
    }

    const billing = await this.processBilling(userId, 'auto_trade');
    if (!billing.paid) {
      return { error: 'PAYMENT_REQUIRED', message: billing.message };
    }

    const { coin, side, size, orderType = 'market', price } = params;

    try {
      const sdk = await this.initSDK();
      const normalizedCoin = this.normalizeCoin(coin);
      
      // Get current price for slippage protection
      const prices = await sdk.info.getAllMids();
      const currentPrice = parseFloat(prices[normalizedCoin]);
      
      const isBuy = side.toLowerCase() === 'buy';
      
      let result;
      if (orderType === 'market') {
        // 5% slippage protection
        const slippagePrice = isBuy ? currentPrice * 1.05 : currentPrice * 0.95;
        
        result = await sdk.exchange.placeOrder({
          coin: normalizedCoin,
          is_buy: isBuy,
          sz: parseFloat(size),
          limit_px: slippagePrice,
          order_type: { limit: { tif: 'Ioc' } },
          reduce_only: false
        });
      } else {
        // Limit order
        result = await sdk.exchange.placeOrder({
          coin: normalizedCoin,
          is_buy: isBuy,
          sz: parseFloat(size),
          limit_px: parseFloat(price),
          order_type: { limit: { tif: 'Gtc' } },
          reduce_only: false
        });
      }

      return {
        success: true,
        charged: 0.1,
        data: result,
        message: formatTradeResult(result, normalizedCoin, side, size, orderType, 0.1)
      };
    } catch (error) {
      return { error: 'TRADE_ERROR', message: formatError(error) };
    }
  }

  /**
   * Get AI trading signal
   */
  async getSignal(userId, coin) {
    const billing = await this.processBilling(userId, 'strategy_execution');
    if (!billing.paid) {
      return { error: 'PAYMENT_REQUIRED', message: billing.message };
    }

    try {
      const sdk = await this.initSDK();
      const normalizedCoin = this.normalizeCoin(coin);
      
      // Get market data
      const prices = await sdk.info.getAllMids();
      const currentPrice = parseFloat(prices[normalizedCoin]);
      
      // Simple trend analysis (placeholder for more complex AI)
      const signal = this.strategyEngine.analyzeTrend({
        coin: normalizedCoin,
        currentPrice,
        timestamp: new Date().toISOString()
      });

      return {
        success: true,
        charged: 0.05,
        data: signal,
        message: `🤖 Hypii AI Signal\n\n🪙 ${normalizedCoin}: $${currentPrice}\n📊 Signal: ${signal.direction}\n💪 Confidence: ${signal.confidence}%\n📝 Analysis: ${signal.reasoning}\n💳 Charged: 0.05 USDT`
      };
    } catch (error) {
      return { error: 'ANALYSIS_ERROR', message: formatError(error) };
    }
  }

  normalizeCoin(coin) {
    if (!coin) return coin;
    const upper = coin.toUpperCase();
    if (upper.endsWith('-PERP') || upper.endsWith('-SPOT')) return upper;
    return upper + '-PERP';
  }

  async getCurrentPrice(coin) {
    const sdk = await this.initSDK();
    const prices = await sdk.info.getAllMids();
    return parseFloat(prices[coin]);
  }
}

// Main handler
const trader = new HypiiTrader();

export async function handler(input, context) {
  const userId = context?.userId || context?.sessionId || 'anonymous';
  const { action, ...params } = input;

  switch (action) {
    case 'portfolio':
    case 'balance':
      return await trader.getPortfolio(userId, params.address);
    
    case 'price':
      return await trader.getPrice(userId, params.coin);
    
    case 'dca':
      return await trader.executeDCA(userId, params);
    
    case 'grid':
      return await trader.executeGrid(userId, params);
    
    case 'trade':
    case 'buy':
    case 'sell':
      return await trader.executeTrade(userId, {
        ...params,
        side: action === 'sell' ? 'sell' : 'buy'
      });
    
    case 'signal':
    case 'analyze':
      return await trader.getSignal(userId, params.coin);
    
    case 'help':
    default:
      return {
        success: true,
        message: `🤖 Hypii Hyperliquid Trading Agent\n\n📚 Available Commands:\n\n🆓 FREE (5 calls/day):\n  • portfolio - View your portfolio\n  • price <coin> - Get current price\n\n💰 PAID (0.05 USDT):\n  • dca <coin> <amount> <frequency> - Create DCA strategy\n  • grid <coin> <lower> <upper> <grids> - Create grid strategy\n  • signal <coin> - Get AI trading signal\n\n🚀 TRADING (0.1 USDT):\n  • trade <coin> <side> <size> - Execute trade\n  • buy <coin> <size> - Market buy\n  • sell <coin> <size> - Market sell\n\n💎 SUBSCRIPTION:\n  • Basic: 9.9 USDT/month (unlimited basic calls)\n  • Pro: 19.9 USDT/month (unlimited everything)\n\n⚙️ Setup:\n  Set HYPERLIQUID_ADDRESS for read-only\n  Set HYPERLIQUID_PRIVATE_KEY for trading`
      };
  }
}

export default { handler };
