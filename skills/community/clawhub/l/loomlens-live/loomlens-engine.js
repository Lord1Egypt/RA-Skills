/**
 * LoomLens Live — Cost Estimation Engine
 * Pure JavaScript: no TypeScript, no build step required.
 * Works as ES module, CommonJS, or browser global.
 *
 * Token estimation → cost calculation → cluster-aware fit scoring.
 * Zero API calls. Zero dependencies.
 */

// ─── Inline Cluster Data ────────────────────────────────────────────────────
// (Cluster definitions are inlined at bottom of this file or injected by build)

const CLUSTERS = [
  {
    id: 'flash', name: 'Flash Reasoning',
    models: [
      { id:'minimax/MiniMax-M2',     name:'MiniMax M2',       provider:'MiniMax',    tier:3, latency:'fast', inputPricePerM:0.10, outputPricePerM:0.40 },
      { id:'google/gemini-2.5-flash', name:'Gemini 2.5 Flash',  provider:'Google',    tier:3, latency:'fast', inputPricePerM:0.15, outputPricePerM:0.60 },
      { id:'anthropic/claude-haiku',  name:'Claude Haiku',      provider:'Anthropic', tier:3, latency:'fast', inputPricePerM:0.80, outputPricePerM:4.00 },
      { id:'deepseek/deepseek-chat-v3',name:'DeepSeek Chat v3',provider:'DeepSeek',  tier:3, latency:'fast', inputPricePerM:0.27, outputPricePerM:1.10 },
    ],
  },
  {
    id: 'fastgen', name: 'Fast General',
    models: [
      { id:'openai/gpt-4o-mini',      name:'GPT-4o Mini',      provider:'OpenAI',  tier:3, latency:'fast', inputPricePerM:0.15, outputPricePerM:0.60 },
      { id:'google/gemini-2.0-flash', name:'Gemini 2.0 Flash', provider:'Google',   tier:3, latency:'fast', inputPricePerM:0.10, outputPricePerM:0.40 },
      { id:'xai/grok-3',              name:'xAI Grok-3',       provider:'xAI',     tier:3, latency:'fast', inputPricePerM:2.00, outputPricePerM:10.0 },
    ],
  },
  {
    id: 'code', name: 'Balanced Coding',
    models: [
      { id:'anthropic/claude-sonnet-4-20250514', name:'Claude Sonnet 4', provider:'Anthropic', tier:2, latency:'medium', inputPricePerM:3.00, outputPricePerM:15.0 },
      { id:'openai/gpt-4o',             name:'GPT-4o',              provider:'OpenAI',   tier:2, latency:'medium', inputPricePerM:2.50, outputPricePerM:10.0 },
      { id:'anthropic/claude-3.5-sonnet', name:'Claude 3.5 Sonnet', provider:'Anthropic',tier:2, latency:'medium', inputPricePerM:3.00, outputPricePerM:15.0 },
    ],
  },
  {
    id: 'power', name: 'Power / Architecture',
    models: [
      { id:'anthropic/claude-opus-4-20250514', name:'Claude Opus 4',  provider:'Anthropic', tier:1, latency:'slow', inputPricePerM:15.0, outputPricePerM:75.0 },
      { id:'anthropic/claude-code',       name:'Claude Code',       provider:'Anthropic', tier:1, latency:'slow', inputPricePerM:15.0, outputPricePerM:75.0 },
    ],
  },
  {
    id: 'vision', name: 'Vision / Multimodal',
    models: [
      { id:'openai/gpt-4o',      name:'GPT-4o',     provider:'OpenAI',   tier:4, latency:'medium', inputPricePerM:2.50, outputPricePerM:10.0 },
      { id:'anthropic/claude-3.5', name:'Claude 3.5', provider:'Anthropic', tier:4, latency:'medium', inputPricePerM:3.00, outputPricePerM:15.0 },
    ],
  },
];

const LATENCY_SCORE = { fast: 100, medium: 62, slow: 22 };

const CAPABILITY_FIT = {
  simple_qa:        { flash: 95, fastgen: 80, code: 30, power: 20, vision: 20 },
  summary:          { flash: 90, fastgen: 75, code: 40, power: 30, vision: 20 },
  code_edit:        { flash: 60, fastgen: 40, code: 90, power: 40, vision: 20 },
  code_write:       { flash: 30, fastgen: 20, code: 95, power: 95, vision: 20 },
  complex_analysis: { flash: 40, fastgen: 30, code: 85, power: 98, vision: 20 },
  vision:           { flash: 10, fastgen: 10, code: 30, power: 30, vision: 98 },
  unknown:          { flash: 70, fastgen: 60, code: 60, power: 50, vision: 40 },
};

const TASK_KEYWORDS = {
  simple_qa:         ['what is','who is','define','explain','how do i','how does','what are','why does','when did','where is','tell me','give me'],
  summary:           ['summarize','tl;dr','sum up','brief','recap','key points','highlights','overview','condense','shorten'],
  code_edit:         ['fix','bug','debug','hotfix','patch','tweak','adjust','correct','error','issue'],
  code_write:        ['write','build','create','implement','add feature','new function','generate',' scaffold','code for','make a'],
  complex_analysis:  ['analyze','architecture','review','refactor','design','strategy','compare','evaluate','assess','plan'],
  vision:            ['image','photo','picture','screenshot','diagram','chart','visual','frame','pdf','document'],
};

const OUTPUT_TOKENS = { simple_qa:150, summary:200, code_edit:400, code_write:800, complex_analysis:600, vision:300, unknown:400 };

const CHARS_PER_TOKEN = { en: 3.8, es: 3.5, ja: 1.2, zh: 1.0 };

// ─── Token Estimation ────────────────────────────────────────────────────────

export function detectLanguage(text) {
  if (/[\u3040-\u309F\u30A0-\u30FF]/.test(text)) return 'ja';
  if (/[\u4E00-\u9FFF]/.test(text)) return 'zh';
  if (/[áéíóúñ¿¡ü]/i.test(text)) return 'es';
  return 'en';
}

export function estimateInputTokens(text) {
  if (!text || !text.trim()) return 0;
  const lang = detectLanguage(text);
  const cpt = CHARS_PER_TOKEN[lang];
  const multiline = (text.match(/\n/g)||[]).length;
  const codeFences = (text.match(/```/g)||[]).length;
  const mult = (codeFences >= 2 || multiline > 3) ? 1.2 : 1.0;
  return Math.ceil((text.length / cpt) * mult);
}

// ─── Task Detection ─────────────────────────────────────────────────────────

export function detectTaskType(prompt) {
  const lower = prompt.toLowerCase();
  const scores = {};
  for (const [type, keywords] of Object.entries(TASK_KEYWORDS)) {
    scores[type] = keywords.reduce((acc, kw) => acc + (lower.includes(kw) ? 1 : 0), 0);
  }
  if (/```[\s\S]+```/.test(prompt)) scores['code_write'] = (scores['code_write']||0) + 2;
  if (/^\s*(import|from|const|let|function|class|def |fn |pub fn)/m.test(prompt)) scores['code_write'] = (scores['code_write']||0) + 2;
  if (/\b(fix|bug|error|issue)\b/i.test(prompt)) scores['code_edit'] = (scores['code_edit']||0) + 1;
  if (/\b(write|build|create|implement)\b/i.test(prompt)) scores['code_write'] = (scores['code_write']||0) + 1;
  if (/\b(analyze|evaluate|compare|assess)\b/i.test(prompt)) scores['complex_analysis'] = (scores['complex_analysis']||0) + 1;

  const best = Object.entries(scores).sort((a,b) => (b[1]??0) - (a[1]??0))[0];
  const score = best?.[1] ?? 0;
  const type = score === 0 ? 'unknown' : best[0];
  return { type, confidence: Math.min(score/3, 1), keywords: (TASK_KEYWORDS[type]??[]).filter(kw=>lower.includes(kw)) };
}

// ─── Cost ──────────────────────────────────────────────────────────────────

export function calcCost(inPrice, outPrice, inTokens, outTokens) {
  return { inputCost: Math.round((inTokens/1e6)*inPrice*1e6)/1e6, outputCost: Math.round((outTokens/1e6)*outPrice*1e6)/1e6,
    totalCost: Math.round(((inTokens/1e6)*inPrice + (outTokens/1e6)*outPrice)*1e6)/1e6 };
}

// ─── Fit Scoring ────────────────────────────────────────────────────────────

export function scoreWithinCluster(model, task, clusterModels) {
  const capFit  = CAPABILITY_FIT[task]?.[model.clusterId] ?? 50;
  const costs   = clusterModels.map(m => calcCost(m.inputPricePerM, m.outputPricePerM, 1, 1).totalCost);
  const minC    = Math.min(...costs);
  const maxC    = Math.max(...costs);
  const range   = maxC - minC || 1;
  const costEff = Math.round(100 - ((calcCost(model.inputPricePerM, model.outputPricePerM, 1, 1).totalCost - minC) / range * 100));
  const speed   = LATENCY_SCORE[model.latency] ?? 50;
  return Math.round(capFit * 0.35 + costEff * 0.35 + speed * 0.30);
}

export function getInsight(modelName, clusterName, clusterId, task, score, isBest) {
  const labels = { simple_qa:'quick Q&A', summary:'summarization', code_edit:'code fixes', code_write:'code builds',
    complex_analysis:'deep analysis', vision:'image/doc understanding', unknown:'general purpose' };
  const label = labels[task] ?? 'general purpose';
  if (isBest) return `Best in ${clusterName} for ${label}`;
  if (score >= 80) return `Strong fit for ${label}`;
  if (score >= 65) return `Capable for ${label}`;
  return `Consider alternatives for ${label}`;
}

// ─── Main Estimator ─────────────────────────────────────────────────────────

/**
 * estimatePrompt(prompt, selectedModelId?) → LoomLensResult
 */
export function estimatePrompt(prompt, selectedModelId = '') {
  const task      = detectTaskType(prompt);
  const inTokens  = estimateInputTokens(prompt);
  const outTokens = OUTPUT_TOKENS[task.type] ?? 400;

  const allFlat  = CLUSTERS.flatMap(c => c.models.map(m => ({ ...m, clusterId: c.id, clusterName: c.name })));
  const clusters = {};
  const allModels = [];

  for (const cluster of CLUSTERS) {
    const clusterModels = allFlat.filter(m => m.clusterId === cluster.id);
    const clusterCosts  = clusterModels.map(m => calcCost(m.inputPricePerM, m.outputPricePerM, inTokens, outTokens).totalCost);
    const maxCost       = Math.max(...clusterCosts);

    const scored = clusterModels.map(m => {
      const costs   = calcCost(m.inputPricePerM, m.outputPricePerM, inTokens, outTokens);
      const score   = scoreWithinCluster(m, task.type, clusterModels);
      const isBest   = false;
      return {
        modelId: m.id, modelName: m.name, provider: m.provider,
        clusterId: m.clusterId, clusterName: cluster.name,
        inputTokens: inTokens, outputTokens: outTokens,
        inputCost: costs.inputCost, outputCost: costs.outputCost, totalCost: costs.totalCost,
        latencyScore: LATENCY_SCORE[m.latency] ?? 50,
        compositeScore: score,
        relativeCostPct: Math.round((costs.totalCost / maxCost) * 100),
        _isBest: false,
      };
    });

    scored.sort((a,b) => b.compositeScore - a.compositeScore);
    const best = scored.find(m => m.compositeScore >= 65) ?? scored[0];
    if (best) best._isBest = true;
    scored.forEach(m => {
      m.fitBadge = m._isBest ? 'recommended' : m.compositeScore >= 65 ? 'sufficient' : 'overkill';
      m.insight  = getInsight(m.modelName, cluster.name, cluster.id, task.type, m.compositeScore, m._isBest);
    });

    clusters[cluster.id] = { clusterId: cluster.id, clusterName: cluster.name, models: scored, best: best??null };
    allModels.push(...scored);
  }

  allModels.sort((a,b) => b.compositeScore - a.compositeScore);
  const recommended = allModels.find(m => m.compositeScore >= 80) ?? null;
  const selected    = allModels.find(m => m.modelId === selectedModelId) ?? allModels[0];

  let tip = '';
  if (recommended && selected && recommended.modelId !== selected.modelId) {
    const saving = selected.totalCost - recommended.totalCost;
    if (saving > 0.0001) tip = `Switch to ${recommended.modelName} and save ${formatCost(saving)}.`;
    else if (saving < -0.0001) tip = `${selected.modelName} costs ${formatCost(Math.abs(saving))} more than ${recommended.modelName}.`;
  } else if (selected) {
    tip = `${selected.modelName} is a good fit for this task.`;
  }

  return { prompt, taskType: task.type, taskConfidence: task.confidence, inputTokens: inTokens, outputTokens: outTokens,
    clusters, recommended, selected, allModels, tip, estimatedAt: Date.now() };
}

export function formatCost(n) {
  if (n >= 1)    return '$' + n.toFixed(2);
  if (n >= 0.01) return '$' + n.toFixed(3);
  return '$' + n.toFixed(4);
}

// ─── Exports ─────────────────────────────────────────────────────────────────


export function getAllClusterModels() {
  return CLUSTERS.flatMap(c => c.models.map(m => ({ ...m, clusterId: c.id, clusterName: c.name })));
}
export function getModelById(id) {
  for (const c of CLUSTERS) { const m = c.models.find(m => m.id === id); if (m) return { ...m, clusterId: c.id, clusterName: c.name }; }
  return null;
}
export function getClusterById(id) { return CLUSTERS.find(c => c.id === id) ?? null; }
export function getClusterIds()    { return CLUSTERS.map(c => c.id); }

// ─── Browser global ─────────────────────────────────────────────────────────
if (typeof window !== 'undefined' && typeof module === 'undefined') {
  window.LoomLensEngine = { estimatePrompt, formatCost, estimateInputTokens, detectTaskType,
    CLUSTERS, LATENCY_SCORE, CAPABILITY_FIT, TASK_KEYWORDS, OUTPUT_TOKENS,
    getAllClusterModels, getModelById, getClusterById, getClusterIds };
}
