/**
 * Default thresholds and constants
 */

import type { Brand } from '../types';

export const DEFAULT_ALERT_THRESHOLDS: Record<Brand, { min: number; max: number; step: number }> = {
  antam: {
    min: 2000000,
    max: 4000000,
    step: 50000
  },
  hartadinata: {
    min: 2000000,
    max: 3800000,
    step: 50000
  },
  ubs: {
    min: 2000000,
    max: 3800000,
    step: 50000
  },
  pegadaian: {
    min: 2000000,
    max: 4000000,
    step: 50000
  }
};

export const CACHE_DURATION = 30 * 60 * 1000; // 30 minutes in ms

export const HISTORY_RETENTION_DAYS = 365;

export const ALERT_CHECK_INTERVAL = 5 * 60 * 1000; // 5 minutes

export const DEFAULT_TREND_DAYS = [7, 30, 90];

export const PRICE_FORMAT_OPTIONS = {
  style: 'currency',
  currency: 'IDR',
  minimumFractionDigits: 0,
  maximumFractionDigits: 0
};

export const CHANGE_INDICATORS = {
  up: '📈',
  down: '📉',
  neutral: '➡️'
};

export const RECOMMENDATION_EMOJI = {
  buy: '🟢 BELI',
  hold: '🟡 TAHAN',
  sell: '🔴 JUAL',
  wait: '⚪ TUNGGU'
};

export const TREND_EMOJI = {
  bullish: '🐂 Bullish',
  bearish: '🐻 Bearish',
  neutral: '😐 Netral'
};

export const CONFIDENCE_LEVELS = {
  high: { min: 70, label: 'Tinggi' },
  medium: { min: 40, label: 'Sedang' },
  low: { min: 0, label: 'Rendah' }
};
