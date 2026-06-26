/**
 * Brand configurations for gold price sources
 */

import type { Brand, ScrapingConfig } from '../types';

export const BRANDS: Record<Brand, { name: string; emoji: string; description: string }> = {
  antam: {
    name: 'Antam (Logam Mulia)',
    emoji: '🏆',
    description: 'Official PT Aneka Tambang Tbk'
  },
  hartadinata: {
    name: 'Hartadinata Abadi',
    emoji: '💎',
    description: 'EmasKITA, Kencana, Emasku'
  },
  ubs: {
    name: 'UBS',
    emoji: '🔷',
    description: 'Swiss gold refinery'
  },
  pegadaian: {
    name: 'Pegadaian (Galeri 24)',
    emoji: '🏛️',
    description: 'State-owned pawnshop'
  }
};

export const SCRAPING_CONFIGS: Record<Brand, ScrapingConfig> = {
  antam: {
    url: 'https://www.logammulia.com/id/harga-emas-hari-ini',
    selectors: {
      buy: '.price-buy',
      sell: '.price-sell',
      buyback: '.price-buyback',
      lastUpdate: '.last-update'
    },
    fallbackRegex: {
      buy: /Rp[\s]?([\d.,]+)/,
      sell: /Rp[\s]?([\d.,]+)/g,
      buyback: /Rp[\s]?([\d.,]+)/g
    }
  },
  hartadinata: {
    url: 'https://harga-emas.org/',
    selectors: {
      buy: '.hartadinata-buy',
      sell: '.hartadinata-sell',
      buyback: '.hartadinata-buyback',
      lastUpdate: '.update-time'
    },
    fallbackRegex: {
      buy: /Rp[\s]?([\d.,]+)/,
      sell: /Rp[\s]?([\d.,]+)/g
    }
  },
  ubs: {
    url: 'https://harga-emas.org/ubs',
    selectors: {
      buy: '.ubs-buy',
      sell: '.ubs-sell',
      buyback: '.ubs-buyback',
      lastUpdate: '.update-time'
    },
    fallbackRegex: {
      buy: /Rp[\s]?([\d.,]+)/,
      sell: /Rp[\s]?([\d.,]+)/g
    }
  },
  pegadaian: {
    url: 'https://www.pegadaian.co.id/harga-emas',
    selectors: {
      buy: '.pegadaian-buy',
      sell: '.pegadaian-sell',
      buyback: '.pegadaian-buyback',
      lastUpdate: '.last-update'
    },
    fallbackRegex: {
      buy: /Rp[\s]?([\d.,]+)/,
      sell: /Rp[\s]?([\d.,]+)/g
    }
  }
};

export const DEFAULT_BRAND: Brand = 'antam';

export const BRAND_PRIORITY: Brand[] = ['antam', 'hartadinata', 'ubs', 'pegadaian'];

export function getBrandInfo(brand: Brand) {
  return BRANDS[brand];
}

export function getScrapingConfig(brand: Brand): ScrapingConfig {
  return SCRAPING_CONFIGS[brand];
}
