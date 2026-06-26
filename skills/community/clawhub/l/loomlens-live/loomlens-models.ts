/**
 * LoomLens Live — Model Registry
 *
 * Canonical model definitions used by the estimation engine.
 * Cluster assignments and full model metadata live in loomlens-clusters.js.
 * This file provides supplementary metadata (provider URLs, descriptions, etc.)
 *
 * Note: For the standalone sidebar, cluster definitions in loomlens-clusters.js
 * are the source of truth for all pricing, latency, and cluster membership.
 */

export interface ModelInfo {
  id: string;
  name: string;
  provider: string;
  tier: 1 | 2 | 3 | 4 | 5;
  tierName: string;
  inputPricePerM: number;
  outputPricePerM: number;
  contextWindow: number;
  latency: 'slow' | 'medium' | 'fast';
  capabilities: string[];
  /** Short one-line description for tooltips/cards */
  tagline: string;
  /** URL to provider docs */
  docsUrl?: string;
}

export const ModelDescriptions: Record<string, ModelInfo> = {

  'minimax/MiniMax-M2': {
    id: 'minimax/MiniMax-M2',
    name: 'MiniMax M2',
    provider: 'MiniMax',
    tier: 3,
    tierName: 'Fast',
    inputPricePerM: 0.10,
    outputPricePerM: 0.40,
    contextWindow: 1_024_000,
    latency: 'fast',
    capabilities: ['reasoning', 'fast', 'cheap', 'long-context'],
    tagline: 'Best value reasoning model available',
    docsUrl: 'https://www.minimaxi.com/',
  },
  'google/gemini-2.5-flash': {
    id: 'google/gemini-2.5-flash',
    name: 'Gemini 2.5 Flash',
    provider: 'Google',
    tier: 3,
    tierName: 'Fast',
    inputPricePerM: 0.15,
    outputPricePerM: 0.60,
    contextWindow: 1_000_000,
    latency: 'fast',
    capabilities: ['reasoning', 'fast'],
    tagline: 'Google\'s fastest reasoning model',
    docsUrl: 'https://ai.google.dev/',
  },
  'anthropic/claude-haiku': {
    id: 'anthropic/claude-haiku',
    name: 'Claude Haiku',
    provider: 'Anthropic',
    tier: 3,
    tierName: 'Fast',
    inputPricePerM: 0.80,
    outputPricePerM: 4.00,
    contextWindow: 200_000,
    latency: 'fast',
    capabilities: ['fast', 'light-reasoning', 'cheap'],
    tagline: 'Anthropic\'s fastest, most affordable',
    docsUrl: 'https://www.anthropic.com/',
  },
  'deepseek/deepseek-chat-v3': {
    id: 'deepseek/deepseek-chat-v3',
    name: 'DeepSeek Chat v3',
    provider: 'DeepSeek',
    tier: 3,
    tierName: 'Fast',
    inputPricePerM: 0.27,
    outputPricePerM: 1.10,
    contextWindow: 640_000,
    latency: 'fast',
    capabilities: ['reasoning', 'fast'],
    tagline: 'Strong open-weights reasoning at low cost',
    docsUrl: 'https://www.deepseek.com/',
  },
  'openai/gpt-4o-mini': {
    id: 'openai/gpt-4o-mini',
    name: 'GPT-4o Mini',
    provider: 'OpenAI',
    tier: 3,
    tierName: 'Fast',
    inputPricePerM: 0.15,
    outputPricePerM: 0.60,
    contextWindow: 128_000,
    latency: 'fast',
    capabilities: ['fast', 'cheap'],
    tagline: 'OpenAI\'s cheapest GPT-4 class model',
    docsUrl: 'https://platform.openai.com/',
  },
  'google/gemini-2.0-flash': {
    id: 'google/gemini-2.0-flash',
    name: 'Gemini 2.0 Flash',
    provider: 'Google',
    tier: 3,
    tierName: 'Fast',
    inputPricePerM: 0.10,
    outputPricePerM: 0.40,
    contextWindow: 1_000_000,
    latency: 'fast',
    capabilities: ['fast', 'cheap', 'long-context'],
    tagline: 'Google\'s original Flash speed at lowest price',
    docsUrl: 'https://ai.google.dev/',
  },
  'xai/grok-3': {
    id: 'xai/grok-3',
    name: 'xAI Grok-3',
    provider: 'xAI',
    tier: 3,
    tierName: 'Fast',
    inputPricePerM: 2.00,
    outputPricePerM: 10.00,
    contextWindow: 131_072,
    latency: 'fast',
    capabilities: ['fast', 'reasoning'],
    tagline: 'xAI\'s fastest model with real-time data access',
    docsUrl: 'https://x.ai/',
  },
  'anthropic/claude-sonnet-4-20250514': {
    id: 'anthropic/claude-sonnet-4-20250514',
    name: 'Claude Sonnet 4',
    provider: 'Anthropic',
    tier: 2,
    tierName: 'Balanced',
    inputPricePerM: 3.00,
    outputPricePerM: 15.00,
    contextWindow: 200_000,
    latency: 'medium',
    capabilities: ['reasoning', 'code', 'analysis', 'fast-reasoning'],
    tagline: 'Best overall code + reasoning value from Anthropic',
    docsUrl: 'https://www.anthropic.com/',
  },
  'openai/gpt-4o': {
    id: 'openai/gpt-4o',
    name: 'GPT-4o',
    provider: 'OpenAI',
    tier: 2,
    tierName: 'Balanced',
    inputPricePerM: 2.50,
    outputPricePerM: 10.00,
    contextWindow: 128_000,
    latency: 'medium',
    capabilities: ['reasoning', 'vision', 'code', 'multimodal'],
    tagline: 'OpenAI\'s flagship — vision + reasoning in one',
    docsUrl: 'https://platform.openai.com/',
  },
  'anthropic/claude-3.5-sonnet': {
    id: 'anthropic/claude-3.5-sonnet',
    name: 'Claude 3.5 Sonnet',
    provider: 'Anthropic',
    tier: 2,
    tierName: 'Balanced',
    inputPricePerM: 3.00,
    outputPricePerM: 15.00,
    contextWindow: 200_000,
    latency: 'medium',
    capabilities: ['reasoning', 'code', 'analysis'],
    tagline: 'Battle-tested coding and reasoning',
    docsUrl: 'https://www.anthropic.com/',
  },
  'anthropic/claude-opus-4-20250514': {
    id: 'anthropic/claude-opus-4-20250514',
    name: 'Claude Opus 4',
    provider: 'Anthropic',
    tier: 1,
    tierName: 'Power',
    inputPricePerM: 15.00,
    outputPricePerM: 75.00,
    contextWindow: 200_000,
    latency: 'slow',
    capabilities: ['reasoning', 'code', 'analysis', 'long-context'],
    tagline: 'Anthropic\'s most capable model',
    docsUrl: 'https://www.anthropic.com/',
  },
  'anthropic/claude-code': {
    id: 'anthropic/claude-code',
    name: 'Claude Code',
    provider: 'Anthropic',
    tier: 1,
    tierName: 'Power',
    inputPricePerM: 15.00,
    outputPricePerM: 75.00,
    contextWindow: 200_000,
    latency: 'slow',
    capabilities: ['agentic', 'code', 'architecture', 'full-reasoning'],
    tagline: 'Agentic coding — runs in your codebase',
    docsUrl: 'https://www.anthropic.com/',
  },
  'anthropic/claude-3.5': {
    id: 'anthropic/claude-3.5',
    name: 'Claude 3.5',
    provider: 'Anthropic',
    tier: 4,
    tierName: 'Vision',
    inputPricePerM: 3.00,
    outputPricePerM: 15.00,
    contextWindow: 200_000,
    latency: 'medium',
    capabilities: ['vision', 'code', 'analysis'],
    tagline: 'Anthropic\'s strongest vision + document understanding',
    docsUrl: 'https://www.anthropic.com/',
  },
};
