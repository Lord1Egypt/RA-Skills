/**
 * Tier configuration and feature gates
 */

import type { Tier, UserConfig } from '../types';

export const TIERS: Record<Tier, { name: string; price: number; description: string }> = {
  free: {
    name: 'Free',
    price: 0,
    description: 'Real-time prices & basic comparison'
  },
  pro: {
    name: 'Pro',
    price: 29,
    description: 'Charts, alerts, portfolio & export'
  },
  ai: {
    name: 'AI',
    price: 49,
    description: 'Claude-powered analysis & predictions'
  }
};

export interface Feature {
  name: string;
  free: boolean;
  pro: boolean;
  ai: boolean;
}

export const FEATURES: Feature[] = [
  { name: 'realtimePrices', free: true, pro: true, ai: true },
  { name: 'multiBrand', free: true, pro: true, ai: true },
  { name: 'priceComparison', free: true, pro: true, ai: true },
  { name: 'historicalCharts', free: false, pro: true, ai: true },
  { name: 'priceAlerts', free: false, pro: true, ai: true },
  { name: 'portfolioTracking', free: false, pro: true, ai: true },
  { name: 'dataExport', free: false, pro: true, ai: true },
  { name: 'buybackTracking', free: false, pro: true, ai: true },
  { name: 'aiAnalysis', free: false, pro: false, ai: true },
  { name: 'pricePrediction', free: false, pro: false, ai: true },
  { name: 'recommendations', free: false, pro: false, ai: true },
  { name: 'sentimentAnalysis', free: false, pro: false, ai: true },
  { name: 'personalizedAdvice', free: false, pro: false, ai: true }
];

/**
 * Check if feature is available for tier
 */
export function hasFeature(featureName: string, tier: Tier): boolean {
  const feature = FEATURES.find(f => f.name === featureName);
  if (!feature) return false;
  
  switch (tier) {
    case 'free': return feature.free;
    case 'pro': return feature.pro;
    case 'ai': return feature.ai;
    default: return false;
  }
}

/**
 * Get unavailable message
 */
export function getUpgradeMessage(featureName: string, currentTier: Tier): string {
  const feature = FEATURES.find(f => f.name === featureName);
  if (!feature) return 'Fitur tidak tersedia.';
  
  if (feature.ai && !feature.pro && !feature.free) {
    return `🔒 Fitur ini memerlukan tier AI ($${TIERS.ai.price}/bulan).\n\nUpgrade untuk mengaktifkan.`;
  }
  
  if (feature.pro && !feature.free) {
    return `🔒 Fitur ini memerlukan tier Pro ($${TIERS.pro.price}/bulan).\n\nUpgrade untuk mengaktifkan.`;
  }
  
  return 'Fitur tidak tersedia.';
}

/**
 * Get default config for tier
 */
export function getDefaultConfig(tier: Tier): UserConfig {
  return {
    tier,
    alerts: {
      enabled: tier !== 'free',
      channels: ['telegram']
    },
    portfolio: {
      autoSync: tier !== 'free',
      currency: 'IDR'
    },
    display: {
      showBuyback: tier !== 'free',
      showChangePercent: tier !== 'free',
      defaultBrand: 'antam'
    }
  };
}

/**
 * Validate tier upgrade
 */
export function canUpgrade(from: Tier, to: Tier): boolean {
  const tierOrder: Tier[] = ['free', 'pro', 'ai'];
  const fromIndex = tierOrder.indexOf(from);
  const toIndex = tierOrder.indexOf(to);
  return toIndex > fromIndex;
}
