/**
 * LoomLens Live — Model Cluster Definitions
 * Standalone module: works as ES module, CommonJS, or browser global
 *
 * Each cluster groups models that actually compete on cost + speed + capability.
 * Within a cluster: recommend the cheapest model that clears the capability bar (score ≥ 65).
 */

export const CLUSTERS = [
  // ─────────────────────────────────────────────────────────────────
  // CLUSTER: Flash Reasoning
  // Fast + cheap. Best for Q&A, summaries, simple tasks.
  // ─────────────────────────────────────────────────────────────────
  {
    id:          'flash',
    name:        'Flash Reasoning',
    description: 'Fast + cheap. Best for Q&A, summaries, simple tasks.',
    color:       '#10b981',
    models: [
      {
        id:        'minimax/MiniMax-M2',
        name:      'MiniMax M2',
        provider:  'MiniMax',
        tier:      3,
        latency:   'fast',
        capabilities: ['reasoning', 'fast', 'cheap', 'long-context'],
        inputPricePerM:  0.10,
        outputPricePerM: 0.40,
        contextWindow: 1_024_000,
      },
      {
        id:        'google/gemini-2.5-flash',
        name:      'Gemini 2.5 Flash',
        provider:  'Google',
        tier:      3,
        latency:   'fast',
        capabilities: ['reasoning', 'fast'],
        inputPricePerM:  0.15,
        outputPricePerM: 0.60,
        contextWindow: 1_000_000,
      },
      {
        id:        'anthropic/claude-haiku',
        name:      'Claude Haiku',
        provider:  'Anthropic',
        tier:      3,
        latency:   'fast',
        capabilities: ['fast', 'light-reasoning', 'cheap'],
        inputPricePerM:  0.80,
        outputPricePerM: 4.00,
        contextWindow: 200_000,
      },
      {
        id:        'deepseek/deepseek-chat-v3',
        name:      'DeepSeek Chat v3',
        provider:  'DeepSeek',
        tier:      3,
        latency:   'fast',
        capabilities: ['reasoning', 'fast'],
        inputPricePerM:  0.27,
        outputPricePerM: 1.10,
        contextWindow: 640_000,
      },
    ],
  },

  // ─────────────────────────────────────────────────────────────────
  // CLUSTER: Fast General
  // Fast general purpose. Best latency for typical prompts.
  // ─────────────────────────────────────────────────────────────────
  {
    id:          'fastgen',
    name:        'Fast General',
    description: 'Fast general purpose. Best latency for typical prompts.',
    color:       '#06b6d4',
    models: [
      {
        id:        'openai/gpt-4o-mini',
        name:      'GPT-4o Mini',
        provider:  'OpenAI',
        tier:      3,
        latency:   'fast',
        capabilities: ['fast', 'cheap'],
        inputPricePerM:  0.15,
        outputPricePerM: 0.60,
        contextWindow: 128_000,
      },
      {
        id:        'google/gemini-2.0-flash',
        name:      'Gemini 2.0 Flash',
        provider:  'Google',
        tier:      3,
        latency:   'fast',
        capabilities: ['fast', 'cheap', 'long-context'],
        inputPricePerM:  0.10,
        outputPricePerM: 0.40,
        contextWindow: 1_000_000,
      },
      {
        id:        'xai/grok-3',
        name:      'xAI Grok-3',
        provider:  'xAI',
        tier:      3,
        latency:   'fast',
        capabilities: ['fast', 'reasoning'],
        inputPricePerM:  2.00,
        outputPricePerM: 10.00,
        contextWindow: 131_072,
      },
    ],
  },

  // ─────────────────────────────────────────────────────────────────
  // CLUSTER: Balanced Coding
  // Best code capability per dollar. Medium complexity.
  // ─────────────────────────────────────────────────────────────────
  {
    id:          'code',
    name:        'Balanced Coding',
    description: 'Best code capability per dollar. Medium complexity.',
    color:       '#8b5cf6',
    models: [
      {
        id:        'anthropic/claude-sonnet-4-20250514',
        name:      'Claude Sonnet 4',
        provider:  'Anthropic',
        tier:      2,
        latency:   'medium',
        capabilities: ['reasoning', 'code', 'analysis', 'fast-reasoning'],
        inputPricePerM:  3.00,
        outputPricePerM: 15.00,
        contextWindow: 200_000,
      },
      {
        id:        'openai/gpt-4o',
        name:      'GPT-4o',
        provider:  'OpenAI',
        tier:      2,
        latency:   'medium',
        capabilities: ['reasoning', 'vision', 'code', 'multimodal'],
        inputPricePerM:  2.50,
        outputPricePerM: 10.00,
        contextWindow: 128_000,
      },
      {
        id:        'anthropic/claude-3.5-sonnet',
        name:      'Claude 3.5 Sonnet',
        provider:  'Anthropic',
        tier:      2,
        latency:   'medium',
        capabilities: ['reasoning', 'code', 'analysis'],
        inputPricePerM:  3.00,
        outputPricePerM: 15.00,
        contextWindow: 200_000,
      },
    ],
  },

  // ─────────────────────────────────────────────────────────────────
  // CLUSTER: Power / Architecture
  // Maximum reasoning. Pay for it only when needed.
  // ─────────────────────────────────────────────────────────────────
  {
    id:          'power',
    name:        'Power / Architecture',
    description: 'Maximum reasoning. Pay for it only when needed.',
    color:       '#3b82f6',
    models: [
      {
        id:        'anthropic/claude-opus-4-20250514',
        name:      'Claude Opus 4',
        provider:  'Anthropic',
        tier:      1,
        latency:   'slow',
        capabilities: ['reasoning', 'code', 'analysis', 'long-context'],
        inputPricePerM:  15.00,
        outputPricePerM: 75.00,
        contextWindow: 200_000,
      },
      {
        id:        'anthropic/claude-code',
        name:      'Claude Code',
        provider:  'Anthropic',
        tier:      1,
        latency:   'slow',
        capabilities: ['agentic', 'code', 'architecture', 'full-reasoning'],
        inputPricePerM:  15.00,
        outputPricePerM: 75.00,
        contextWindow: 200_000,
      },
    ],
  },

  // ─────────────────────────────────────────────────────────────────
  // CLUSTER: Vision / Multimodal
  // Image + document understanding.
  // ─────────────────────────────────────────────────────────────────
  {
    id:          'vision',
    name:        'Vision / Multimodal',
    description: 'Image + document understanding.',
    color:       '#ec4899',
    models: [
      {
        id:        'openai/gpt-4o',
        name:      'GPT-4o',
        provider:  'OpenAI',
        tier:      4,
        latency:   'medium',
        capabilities: ['vision', 'reasoning', 'multimodal'],
        inputPricePerM:  2.50,
        outputPricePerM: 10.00,
        contextWindow: 128_000,
      },
      {
        id:        'anthropic/claude-3.5',
        name:      'Claude 3.5',
        provider:  'Anthropic',
        tier:      4,
        latency:   'medium',
        capabilities: ['vision', 'code', 'analysis'],
        inputPricePerM:  3.00,
        outputPricePerM: 15.00,
        contextWindow: 200_000,
      },
    ],
  },
];

// ─── Latency Scoring ────────────────────────────────────────────────────────

export const LATENCY_SCORE = { fast: 100, medium: 62, slow: 22 };

// ─── Capability Fit Matrix ──────────────────────────────────────────────────
// task → cluster → fit 0-100

export const CAPABILITY_FIT = {
  simple_qa:        { flash: 95, fastgen: 80, code: 30, power: 20, vision: 20 },
  summary:          { flash: 90, fastgen: 75, code: 40, power: 30, vision: 20 },
  code_edit:        { flash: 60, fastgen: 40, code: 90, power: 40, vision: 20 },
  code_write:       { flash: 30, fastgen: 20, code: 95, power: 95, vision: 20 },
  complex_analysis: { flash: 40, fastgen: 30, code: 85, power: 98, vision: 20 },
  vision:           { flash: 10, fastgen: 10, code: 30, power: 30, vision: 98 },
  unknown:          { flash: 70, fastgen: 60, code: 60, power: 50, vision: 40 },
};

// ─── Task Detection Keywords ────────────────────────────────────────────────

export const TASK_KEYWORDS = {
  simple_qa:         ['what is','who is','define','explain','how do i','how does','what are','why does','when did','where is','tell me','give me','list the'],
  summary:           ['summarize','tl;dr','sum up','brief','recap','key points','highlights','overview','condense','shorten'],
  code_edit:         ['fix','bug','debug','hotfix','patch','tweak','adjust','correct','error','issue','typo','broken'],
  code_write:        ['write','build','create','implement','add feature','new function','generate',' scaffold','code for','make a','app that'],
  complex_analysis:  ['analyze','architecture','review','refactor','design','strategy','compare','evaluate','assess','plan','audit','investigate'],
  vision:            ['image','photo','picture','screenshot','diagram','chart','visual','frame','pdf','document','extract text from','read the'],
};

// ─── Output Token Estimates by Task ─────────────────────────────────────────

export const OUTPUT_TOKENS = {
  simple_qa:         { min: 50,   mid: 150,  max: 400  },
  summary:           { min: 80,   mid: 200,  max: 500  },
  code_edit:         { min: 100,  mid: 400,  max: 1000 },
  code_write:        { min: 200,  mid: 800,  max: 2500 },
  complex_analysis:  { min: 200,  mid: 600,  max: 1500 },
  vision:            { min: 100,  mid: 300,  max: 800  },
  unknown:           { min: 100,  mid: 400,  max: 1200 },
};

// ─── Helpers ────────────────────────────────────────────────────────────────

/** Get all models as a flat array */
export function getAllClusterModels() {
  return CLUSTERS.flatMap(c => c.models.map(m => ({ ...m, clusterId: c.id, clusterName: c.name })));
}

/** Get a single model by ID */
export function getModelById(id) {
  for (const cluster of CLUSTERS) {
    const m = cluster.models.find(m => m.id === id);
    if (m) return { ...m, clusterId: cluster.id, clusterName: cluster.name };
  }
  return null;
}

/** Get a cluster by ID */
export function getClusterById(id) {
  return CLUSTERS.find(c => c.id === id) ?? null;
}

/** All cluster IDs */
export function getClusterIds() {
  return CLUSTERS.map(c => c.id);
}

// ─── Browser global ─────────────────────────────────────────────────────────
// If loaded as a plain script (not module), expose as window.LoomLensClusters
if (typeof window !== 'undefined' && typeof module === 'undefined') {
  window.LoomLensClusters = {
    CLUSTERS,
    LATENCY_SCORE,
    CAPABILITY_FIT,
    TASK_KEYWORDS,
    OUTPUT_TOKENS,
    getAllClusterModels,
    getModelById,
    getClusterById,
    getClusterIds,
  };
}
