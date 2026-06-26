/**
 * Type definitions for id-emas-pro
 */

export interface GoldPrice {
  brand: Brand;
  buyPrice: number;
  sellPrice: number;
  buybackPrice: number;
  lastUpdate: string;
  unit: 'gram';
}

export type Brand = 'antam' | 'hartadinata' | 'ubs' | 'pegadaian';

export interface PriceResult {
  success: boolean;
  data?: GoldPrice;
  error?: string;
}

export interface PriceRecord extends GoldPrice {
  timestamp: string;
}

export interface PortfolioItem {
  id: string;
  brand: Brand;
  grams: number;
  buyPrice: number;
  buyDate: string;
  notes?: string;
}

export interface PortfolioSummary {
  totalGrams: number;
  totalCost: number;
  currentValue: number;
  unrealizedPnL: number;
  unrealizedPnLPercent: number;
  items: PortfolioItem[];
}

export interface AlertConfig {
  id: string;
  brand: Brand;
  targetPrice: number;
  condition: 'above' | 'below';
  enabled: boolean;
  createdAt: string;
  triggeredAt?: string;
}

export interface TrendData {
  brand: Brand;
  days: number;
  dataPoints: PriceRecord[];
  changeAmount: number;
  changePercent: number;
  high: number;
  low: number;
  average: number;
}

export interface AIAnalysis {
  summary: string;
  trend: 'bullish' | 'bearish' | 'neutral';
  confidence: number; // 0-100
  recommendation: 'buy' | 'hold' | 'sell' | 'wait';
  targetPrice?: number;
  supportLevel?: number;
  resistanceLevel?: number;
  reasoning: string[];
  risks: string[];
}

export type Tier = 'free' | 'pro' | 'ai';

export interface UserConfig {
  tier: Tier;
  claudeApiKey?: string;
  alerts: {
    enabled: boolean;
    channels: ('telegram' | 'email' | 'push')[];
  };
  portfolio: {
    autoSync: boolean;
    currency: 'IDR' | 'USD';
  };
  display: {
    showBuyback: boolean;
    showChangePercent: boolean;
    defaultBrand: Brand;
  };
}

export interface ScrapingConfig {
  url: string;
  selectors: {
    buy?: string;
    sell?: string;
    buyback?: string;
    lastUpdate?: string;
  };
  fallbackRegex?: {
    buy?: RegExp;
    sell?: RegExp;
    buyback?: RegExp;
  };
}
