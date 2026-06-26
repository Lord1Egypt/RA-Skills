// LoomLens Live — Engine (built)
/**
 * LoomLens Live — Model Cluster Definitions
 * Standalone module: works as ES module, CommonJS, or browser global
 *
 * Each cluster groups models that actually compete on cost + speed + capability.
 * Within a cluster: recommend the cheapest model that clears the capability bar (score ≥ 65).
 */

const CLUSTERS = [
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

const LATENCY_SCORE = { fast: 100, medium: 62, slow: 22 };

// ─── Capability Fit Matrix ──────────────────────────────────────────────────
// task → cluster → fit 0-100

const CAPABILITY_FIT = {
  simple_qa:        { flash: 95, fastgen: 80, code: 30, power: 20, vision: 20 },
  summary:          { flash: 90, fastgen: 75, code: 40, power: 30, vision: 20 },
  code_edit:        { flash: 60, fastgen: 40, code: 90, power: 40, vision: 20 },
  code_write:       { flash: 30, fastgen: 20, code: 95, power: 95, vision: 20 },
  complex_analysis: { flash: 40, fastgen: 30, code: 85, power: 98, vision: 20 },
  vision:           { flash: 10, fastgen: 10, code: 30, power: 30, vision: 98 },
  unknown:          { flash: 70, fastgen: 60, code: 60, power: 50, vision: 40 },
};

// ─── Task Detection Keywords ────────────────────────────────────────────────

const TASK_KEYWORDS = {
  simple_qa:         ['what is','who is','define','explain','how do i','how does','what are','why does','when did','where is','tell me','give me','list the'],
  summary:           ['summarize','tl;dr','sum up','brief','recap','key points','highlights','overview','condense','shorten'],
  code_edit:         ['fix','bug','debug','hotfix','patch','tweak','adjust','correct','error','issue','typo','broken'],
  code_write:        ['write','build','create','implement','add feature','new function','generate',' scaffold','code for','make a','app that'],
  complex_analysis:  ['analyze','architecture','review','refactor','design','strategy','compare','evaluate','assess','plan','audit','investigate'],
  vision:            ['image','photo','picture','screenshot','diagram','chart','visual','frame','pdf','document','extract text from','read the'],
};

// ─── Output Token Estimates by Task ─────────────────────────────────────────

const OUTPUT_TOKENS = {
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
function getAllClusterModels() {
  return CLUSTERS.flatMap(c => c.models.map(m => ({ ...m, clusterId: c.id, clusterName: c.name })));
}

/** Get a single model by ID */
function getModelById(id) {
  for (const cluster of CLUSTERS) {
    const m = cluster.models.find(m => m.id === id);
    if (m) return { ...m, clusterId: cluster.id, clusterName: cluster.name };
  }
  return null;
}

/** Get a cluster by ID */
function getClusterById(id) {
  return CLUSTERS.find(c => c.id === id) ?? null;
}

/** All cluster IDs */
function getClusterIds() {
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

/**
 * LoomLens Live — Cost Estimation Engine
 * Phase 1 updated: cluster-aware scoring + standalone (no imports needed)
 *
 * Estimator: char heuristics → token count → cost + cluster-aware fit score.
 * No API calls. No dependencies.
 */



// ─── Types ───────────────────────────────────────────────────────────────────

export type TaskType = keyof typeof TASK_KEYWORDS;
export type ClusterId = 'flash' | 'fastgen' | 'code' | 'power' | 'vision';

export interface TaskDetection {
  type: TaskType;
  confidence: number;
  keywords: string[];
}

export interface ModelEstimate {
  modelId: string;
  modelName: string;
  provider: string;
  clusterId: string;
  clusterName: string;
  inputTokens: number;
  outputTokens: number;
  inputCost: number;
  outputCost: number;
  totalCost: number;
  latencyScore: number;
  capFit: number;
  costEff: number;
  compositeScore: number;      // 0-100
  fitBadge: 'recommended' | 'sufficient' | 'overkill';
  insight: string;
  relativeCostPct: number;     // % of most expensive in same cluster
}

export interface ClusterResult {
  clusterId: string;
  clusterName: string;
  models: ModelEstimate[];
  best: ModelEstimate | null;  // cheapest that clears threshold
}

export interface LoomLensResult {
  prompt: string;
  taskType: TaskType;
  taskConfidence: number;
  inputTokens: number;
  outputTokens: number;
  clusters: Record<string, ClusterResult>;
  recommended: ModelEstimate | null;
  selected: ModelEstimate | null;
  allModels: ModelEstimate[];
  tip: string;
  estimatedAt: number;
}

// ─── Token Estimation ────────────────────────────────────────────────────────

const CHARS_PER_TOKEN = { en: 3.8, es: 3.5, ja: 1.2, zh: 1.0 };

function detectLanguage(text: string): keyof typeof CHARS_PER_TOKEN {
  if (/[\u3040-\u309F\u30A0-\u30FF]/.test(text)) return 'ja';
  if (/[\u4E00-\u9FFF]/.test(text)) return 'zh';
  if (/[áéíóúñ¿¡ü]/i.test(text)) return 'es';
  return 'en';
}

function detectContentMultiplier(text: string): number {
  const codeFences = (text.match(/```/g) || []).length;
  const newlines = (text.match(/\n/g) || []).length;
  const isCode = codeFences >= 2 || (newlines > 3 && codeFences >= 1);
  return isCode ? 1.2 : 1.0;
}

/**
 * Estimate input token count from raw text.
 * Uses language detection + content-type heuristics.
 */
export function estimateInputTokens(text: string): number {
  if (!text || !text.trim()) return 0;
  const lang = detectLanguage(text);
  const cpt = CHARS_PER_TOKEN[lang];
  const mult = detectContentMultiplier(text);
  return Math.ceil((text.length / cpt) * mult);
}

// ─── Task Detection ─────────────────────────────────────────────────────────

/**
 * Detect what type of task this prompt represents.
 */
export function detectTaskType(prompt: string): TaskDetection {
  const lower = prompt.toLowerCase();
  const scores: Partial<Record<TaskType, number>> = {};

  for (const [type, keywords] of Object.entries(TASK_KEYWORDS)) {
    scores[type as TaskType] = keywords.reduce((acc, kw) => acc + (lower.includes(kw) ? 1 : 0), 0);
  }

  // Structural boosts
  if (/```[\s\S]+```/.test(prompt))            (scores['code_write'] as number) += 2;
  if (/^\s*(import|from|const|let|function|class|def |fn |pub fn)/m.test(prompt))
                                                    (scores['code_write'] as number) += 2;
  if (/\b(fix|bug|error|issue)\b/i.test(prompt))  (scores['code_edit'] as number) += 1;
  if (/\b(write|build|create|implement)\b/i.test(prompt))
                                                    (scores['code_write'] as number) += 1;
  if (/\b(analyze|evaluate|compare|assess)\b/i.test(prompt))
                                                    (scores['complex_analysis'] as number) += 1;
  if (/\$\d+|\d+%|rate|spend|cost|budget/i.test(prompt))
                                                    (scores['complex_analysis'] as number) += 1;
  if (/\$\d+|\d+%|rate|spend/i.test(prompt))       (scores['simple_qa'] as number) += 1;

  const best = Object.entries(scores).sort((a, b) => (b[1] ?? 0) - (a[1] ?? 0))[0];
  const score = best?.[1] ?? 0;
  const type: TaskType = score === 0 ? 'unknown' : (best![0] as TaskType);
  const confidence = Math.min(score / 3, 1);
  const keywords = (TASK_KEYWORDS[type] ?? []).filter(kw => lower.includes(kw));

  return { type, confidence, keywords };
}

// ─── Cost Calculation ────────────────────────────────────────────────────────

export function calculateCost(
  inPricePerM: number,
  outPricePerM: number,
  inTokens: number,
  outTokens: number
): { inputCost: number; outputCost: number; totalCost: number } {
  const inputCost  = Math.round((inTokens  / 1_000_000) * inPricePerM  * 1e6) / 1e6;
  const outputCost = Math.round((outTokens / 1_000_000) * outPricePerM * 1e6) / 1e6;
  return { inputCost, outputCost, totalCost: Math.round((inputCost + outputCost) * 1e6) / 1e6 };
}

// ─── Fit Scoring ─────────────────────────────────────────────────────────────

/**
 * Composite score within a cluster:
 * score = (capability_fit × 0.35) + (cost_efficiency × 0.35) + (speed × 0.30)
 *
 * Returns { capFit, costEff, compositeScore }
 */
function scoreWithinCluster(
  model: { clusterId: string; latency: keyof typeof LATENCY_SCORE; inPricePerM: number; outPricePerM: number },
  task: TaskType,
  allInCluster: Array<{ inPricePerM: number; outPricePerM: number }>
): { capFit: number; costEff: number; compositeScore: number } {
  const capFit    = CAPABILITY_FIT[task]?.[model.clusterId] ?? 50;
  const costs     = allInCluster.map(m => calculateCost(m.inPricePerM, m.outPricePerM, 1, 1).totalCost);
  const minC      = Math.min(...costs);
  const maxC      = Math.max(...costs);
  const range     = maxC - minC || 1;
  const costEff   = Math.round(100 - ((calculateCost(model.inPricePerM, model.outPricePerM, 1, 1).totalCost - minC) / range * 100));
  const speed     = LATENCY_SCORE[model.latency] ?? 50;
  const composite = Math.round(capFit * 0.35 + costEff * 0.35 + speed * 0.30);
  return { capFit, costEff, compositeScore: composite };
}

function getFitBadge(score: number, clusterId: string): 'recommended' | 'sufficient' | 'overkill' {
  if (score >= 80) return 'recommended';
  if (score >= 65) return 'sufficient';
  return 'overkill';
}

function getInsight(
  modelName: string,
  clusterName: string,
  clusterId: string,
  task: TaskType,
  score: number,
  isBest: boolean
): string {
  const taskLabels: Record<TaskType, string> = {
    simple_qa: 'quick questions and lookups',
    summary: 'summarization and extraction',
    code_edit: 'code fixes and small changes',
    code_write: 'full code and feature builds',
    complex_analysis: 'deep reasoning and architecture',
    vision: 'image and document understanding',
    unknown: 'general purpose tasks',
  };
  const label = taskLabels[task] ?? 'general purpose';
  if (isBest) return `Best in ${clusterName} for ${label}`;
  if (score >= 80) return `Strong fit for ${label} in ${clusterName}`;
  if (score >= 65) return `Capable for ${label} in ${clusterName}`;
  if (score < 50) return `Consider ${clusterName} alternatives for ${label}`;
  return `Use ${modelName} in ${clusterName} for ${label}`;
}

// ─── Main Estimator ──────────────────────────────────────────────────────────

/**
 * Full estimation: token count → cost + cluster-aware fit score per model.
 */
export function estimatePrompt(
  prompt: string,
  selectedModelId: string = ''
): LoomLensResult {
  const task       = detectTaskType(prompt);
  const inTokens  = estimateInputTokens(prompt);
  const outTokens = OUTPUT_TOKENS[task]?.mid ?? 400;
  const allFlat   = getAllClusterModels();
  const result: LoomLensResult = {
    prompt,
    taskType: task.type,
    taskConfidence: task.confidence,
    inputTokens: inTokens,
    outputTokens: outTokens,
    clusters: {},
    recommended: null,
    selected: null,
    allModels: [],
    tip: '',
    estimatedAt: Date.now(),
  };

  // Score each model within its cluster
  for (const cluster of CLUSTERS) {
    const clusterModels = allFlat.filter(m => m.clusterId === cluster.id);
    const bestInCluster  = clusterModels[0]; // placeholder, will be sorted

    // Pre-compute cluster cost range
    const clusterCosts = clusterModels.map(m =>
      calculateCost(m.inputPricePerM, m.outputPricePerM, inTokens, outTokens).totalCost
    );
    const maxClusterCost = Math.max(...clusterCosts);

    // Score each model
    const scored = clusterModels.map(m => {
      const costs    = calculateCost(m.inputPricePerM, m.outputPricePerM, inTokens, outTokens);
      const { capFit, costEff, compositeScore } = scoreWithinCluster(m, task.type, clusterModels);
      const isBest   = false; // will be set after sort
      const fitBadge = getFitBadge(compositeScore, cluster.id);
      return {
        modelId:       m.id,
        modelName:     m.name,
        provider:      m.provider,
        clusterId:     m.clusterId,
        clusterName:   cluster.name,
        inputTokens:   inTokens,
        outputTokens:  outTokens,
        inputCost:     costs.inputCost,
        outputCost:    costs.outputCost,
        totalCost:     costs.totalCost,
        latencyScore:  LATENCY_SCORE[m.latency] ?? 50,
        capFit,
        costEff,
        compositeScore,
        fitBadge,
        insight:       '',
        relativeCostPct: Math.round((costs.totalCost / maxClusterCost) * 100),
        _isBest:       false,
      } as ModelEstimate & { _isBest: boolean };
    });

    // Sort by composite score desc, then find cheapest above threshold
    scored.sort((a, b) => b.compositeScore - a.compositeScore);
    const best = scored.find(m => m.compositeScore >= 65) ?? scored[0];
    if (best) best._isBest = true;

    // Set insights
    scored.forEach(m => {
      m.insight = getInsight(m.modelName, cluster.name, cluster.id, task.type, m.compositeScore, m._isBest);
      m.fitBadge = m._isBest ? 'recommended' : m.compositeScore >= 65 ? 'sufficient' : 'overkill';
    });

    result.clusters[cluster.id] = {
      clusterId:   cluster.id,
      clusterName: cluster.name,
      models:      scored,
      best:        best ?? null,
    };
    result.allModels.push(...scored);
  }

  // Global: find best across all models
  result.allModels.sort((a, b) => b.compositeScore - a.compositeScore);
  result.recommended = result.allModels.find(m => m.compositeScore >= 80) ?? null;

  // Selected
  if (selectedModelId) {
    result.selected = result.allModels.find(m => m.modelId === selectedModelId) ?? null;
  }
  if (!result.selected) {
    result.selected = result.allModels[0];
  }

  // Tip
  if (result.recommended && result.selected && result.recommended.modelId !== result.selected.modelId) {
    const selCost = result.selected?.totalCost ?? 0;
    const recCost = result.recommended.totalCost;
    const saving  = selCost - recCost;
    if (saving > 0.0001) {
      result.tip = `Switching to ${result.recommended.modelName} saves ${formatCost(saving)} and is better for this task.`;
    } else if (saving < -0.0001) {
      result.tip = `${result.selected?.modelName} is well-matched. ${result.recommended.modelName} would cost ${formatCost(Math.abs(saving))} more.`;
    }
  } else if (result.selected) {
    result.tip = `${result.selected.modelName} is a good fit for this task.`;
  }

  return result;
}

// ─── Utility ─────────────────────────────────────────────────────────────────

export function formatCost(n: number): string {
  if (n >= 1)     return '$' + n.toFixed(2);
  if (n >= 0.01)  return '$' + n.toFixed(3);
  return '$' + n.toFixed(4);
}
