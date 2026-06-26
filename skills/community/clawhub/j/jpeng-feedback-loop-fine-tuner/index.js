/**
 * Feedback Loop Fine-Tuner - Implement feedback loops for LLM agent personalization
 * 
 * Features:
 * - User feedback collection and aggregation
 * - Training dataset generation from feedback
 * - Prompt optimization based on feedback
 * - Fine-tuning data formatting (JSONL, OpenAI format)
 * - Improvement metrics tracking
 * - A/B testing for prompt variants
 * - Feedback quality scoring
 * - Preference learning from comparisons
 * 
 * Usage:
 *   const fineTuner = require('./skills/feedback-loop-fine-tuner');
 *   const dataset = fineTuner.generateTrainingData(feedbackHistory);
 *   const metrics = fineTuner.trackImprovement(before, after);
 *   const optimized = fineTuner.optimizePrompts(feedback, templates);
 */

/**
 * Feedback Collector - Collect and aggregate user feedback
 */
class FeedbackCollector {
  constructor() {
    this.feedbackStore = [];
    this.aggregationRules = {
      positive: { weight: 1.0, signal: 'good_response' },
      negative: { weight: -1.0, signal: 'bad_response' },
      neutral: { weight: 0.0, signal: 'neutral_response' },
      correction: { weight: 0.5, signal: 'user_correction' }
    };
  }
  
  /**
   * Collect feedback from user interaction
   */
  collectFeedback(interaction) {
    const feedback = {
      id: `fb_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date().toISOString(),
      conversationId: interaction.conversationId,
      messageId: interaction.messageId,
      query: interaction.query,
      response: interaction.response,
      rating: interaction.rating, // 'positive', 'negative', 'neutral', 'correction'
      userCorrection: interaction.userCorrection || null,
      metadata: {
        model: interaction.model,
        temperature: interaction.temperature,
        promptTemplate: interaction.promptTemplate,
        responseTime: interaction.responseTime,
        tokensUsed: interaction.tokensUsed
      }
    };
    
    this.feedbackStore.push(feedback);
    return feedback;
  }
  
  /**
   * Batch collect feedback
   */
  batchCollect(interactions) {
    return interactions.map(i => this.collectFeedback(i));
  }
  
  /**
   * Aggregate feedback by category
   */
  aggregateByCategory(timeRange = null) {
    const filtered = timeRange 
      ? this.feedbackStore.filter(f => {
          const t = new Date(f.timestamp).getTime();
          return t >= timeRange.start && t <= timeRange.end;
        })
      : this.feedbackStore;
    
    const aggregation = {
      total: filtered.length,
      byRating: {},
      byPromptTemplate: {},
      avgResponseTime: 0,
      avgTokensUsed: 0,
      qualityScore: 0
    };
    
    let totalResponseTime = 0;
    let totalTokens = 0;
    let qualitySum = 0;
    
    for (const feedback of filtered) {
      // Aggregate by rating
      if (!aggregation.byRating[feedback.rating]) {
        aggregation.byRating[feedback.rating] = [];
      }
      aggregation.byRating[feedback.rating].push(feedback);
      
      // Aggregate by prompt template
      const template = feedback.metadata.promptTemplate || 'default';
      if (!aggregation.byPromptTemplate[template]) {
        aggregation.byPromptTemplate[template] = { total: 0, positive: 0, negative: 0 };
      }
      aggregation.byPromptTemplate[template].total++;
      if (feedback.rating === 'positive') {
        aggregation.byPromptTemplate[template].positive++;
      } else if (feedback.rating === 'negative') {
        aggregation.byPromptTemplate[template].negative++;
      }
      
      // Calculate averages
      totalResponseTime += feedback.metadata.responseTime || 0;
      totalTokens += feedback.metadata.tokensUsed || 0;
      
      // Calculate quality score
      const rule = this.aggregationRules[feedback.rating];
      if (rule) {
        qualitySum += rule.weight;
      }
    }
    
    aggregation.avgResponseTime = filtered.length > 0 ? totalResponseTime / filtered.length : 0;
    aggregation.avgTokensUsed = filtered.length > 0 ? totalTokens / filtered.length : 0;
    aggregation.qualityScore = filtered.length > 0 ? (qualitySum / filtered.length + 1) / 2 : 0.5;
    
    return aggregation;
  }
  
  /**
   * Get feedback for specific conversation
   */
  getConversationFeedback(conversationId) {
    return this.feedbackStore.filter(f => f.conversationId === conversationId);
  }
  
  /**
   * Export feedback for analysis
   */
  exportFeedback(format = 'json') {
    if (format === 'json') {
      return JSON.stringify(this.feedbackStore, null, 2);
    } else if (format === 'csv') {
      const headers = ['id', 'timestamp', 'conversationId', 'rating', 'query', 'response'];
      const rows = this.feedbackStore.map(f => [
        f.id,
        f.timestamp,
        f.conversationId,
        f.rating,
        `"${(f.query || '').replace(/"/g, '""')}"`,
        `"${(f.response || '').replace(/"/g, '""')}"`
      ]);
      return [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
    }
    return this.feedbackStore;
  }
}

/**
 * Training Dataset Generator - Generate fine-tuning datasets from feedback
 */
class TrainingDatasetGenerator {
  constructor() {
    this.formats = ['jsonl', 'openai', 'llama', 'alpaca'];
  }
  
  /**
   * Generate training data from feedback history
   */
  generateTrainingData(feedbackHistory, options = {}) {
    const {
      includeNegative = false,
      includeCorrections = true,
      minRating = 'neutral',
      format = 'jsonl'
    } = options;
    
    const trainingExamples = [];
    
    for (const feedback of feedbackHistory) {
      // Skip negative feedback unless explicitly included
      if (feedback.rating === 'negative' && !includeNegative) {
        continue;
      }
      
      // Use user corrections as training examples
      if (feedback.rating === 'correction' && feedback.userCorrection && includeCorrections) {
        trainingExamples.push({
          input: feedback.query,
          output: feedback.userCorrection,
          source: 'user_correction',
          quality: 'high'
        });
      }
      
      // Use positive feedback as training examples
      if (feedback.rating === 'positive') {
        trainingExamples.push({
          input: feedback.query,
          output: feedback.response,
          source: 'positive_feedback',
          quality: 'high'
        });
      }
      
      // Use neutral feedback with lower quality score
      if (feedback.rating === 'neutral' && minRating !== 'positive') {
        trainingExamples.push({
          input: feedback.query,
          output: feedback.response,
          source: 'neutral_feedback',
          quality: 'medium'
        });
      }
    }
    
    // Format output
    return this.formatDataset(trainingExamples, format);
  }
  
  /**
   * Format dataset according to specified format
   */
  formatDataset(examples, format) {
    switch (format) {
      case 'jsonl':
        return examples.map(e => JSON.stringify({
          prompt: e.input,
          completion: e.output,
          metadata: { source: e.source, quality: e.quality }
        })).join('\n');
      
      case 'openai':
        return examples.map(e => JSON.stringify({
          messages: [
            { role: 'user', content: e.input },
            { role: 'assistant', content: e.output }
          ]
        })).join('\n');
      
      case 'llama':
        return examples.map(e => 
          `<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n${e.input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n${e.output}<|eot_id|>`
        ).join('\n');
      
      case 'alpaca':
        return examples.map(e => JSON.stringify({
          instruction: e.input,
          input: '',
          output: e.output
        })).join('\n');
      
      default:
        return examples;
    }
  }
  
  /**
   * Generate preference pairs for RLHF
   */
  generatePreferencePairs(feedbackHistory) {
    const pairs = [];
    const positive = feedbackHistory.filter(f => f.rating === 'positive');
    const negative = feedbackHistory.filter(f => f.rating === 'negative');
    
    // Match similar queries with different ratings
    for (const pos of positive) {
      for (const neg of negative) {
        if (this.areSimilarQueries(pos.query, neg.query)) {
          pairs.push({
            prompt: pos.query,
            chosen: pos.response,
            rejected: neg.response,
            reason: 'user_preference'
          });
        }
      }
    }
    
    return pairs;
  }
  
  /**
   * Check if two queries are similar
   */
  areSimilarQueries(q1, q2) {
    const words1 = new Set(q1.toLowerCase().split(/\s+/));
    const words2 = new Set(q2.toLowerCase().split(/\s+/));
    const intersection = new Set([...words1].filter(x => words2.has(x)));
    const union = new Set([...words1, ...words2]);
    return intersection.size / union.size > 0.5; // Jaccard similarity > 0.5
  }
  
  /**
   * Split dataset for training/validation
   */
  splitDataset(examples, trainRatio = 0.8) {
    const shuffled = [...examples].sort(() => Math.random() - 0.5);
    const splitIndex = Math.floor(shuffled.length * trainRatio);
    
    return {
      train: shuffled.slice(0, splitIndex),
      validation: shuffled.slice(splitIndex)
    };
  }
}

/**
 * Prompt Optimizer - Optimize prompts based on feedback
 */
class PromptOptimizer {
  constructor() {
    this.templates = new Map();
    this.performance = new Map();
  }
  
  /**
   * Register a prompt template
   */
  registerTemplate(name, template) {
    this.templates.set(name, template);
    this.performance.set(name, {
      uses: 0,
      positiveRate: 0,
      avgResponseTime: 0,
      totalPositive: 0,
      totalNegative: 0
    });
  }
  
  /**
   * Update performance metrics for a template
   */
  updatePerformance(templateName, feedback) {
    const perf = this.performance.get(templateName);
    if (!perf) return;
    
    perf.uses++;
    if (feedback.rating === 'positive') {
      perf.totalPositive++;
    } else if (feedback.rating === 'negative') {
      perf.totalNegative++;
    }
    
    perf.positiveRate = perf.uses > 0 ? perf.totalPositive / perf.uses : 0;
    perf.avgResponseTime = (perf.avgResponseTime * (perf.uses - 1) + (feedback.metadata.responseTime || 0)) / perf.uses;
  }
  
  /**
   * Get best performing template
   */
  getBestTemplate() {
    let best = null;
    let bestScore = -1;
    
    for (const [name, perf] of this.performance) {
      const score = perf.positiveRate * 0.7 + (1 - perf.avgResponseTime / 10000) * 0.3;
      if (score > bestScore) {
        bestScore = score;
        best = name;
      }
    }
    
    return best;
  }
  
  /**
   * Suggest prompt improvements based on feedback
   */
  suggestImprovements(feedbackHistory, templateName) {
    const suggestions = [];
    const templateFeedback = feedbackHistory.filter(f => 
      f.metadata && f.metadata.promptTemplate === templateName
    );
    
    // Analyze negative feedback
    const negative = templateFeedback.filter(f => f.rating === 'negative');
    
    // Common issues
    const issues = {
      tooLong: 0,
      tooShort: 0,
      inaccurate: 0,
      unhelpful: 0,
      offTopic: 0
    };
    
    for (const fb of negative) {
      if (fb.userCorrection) {
        // Analyze the correction
        const responseLen = (fb.response || '').length;
        const correctionLen = (fb.userCorrection || '').length;
        
        if (correctionLen > responseLen * 1.5) {
          issues.tooShort++;
        } else if (correctionLen < responseLen * 0.5) {
          issues.tooLong++;
        }
      }
    }
    
    // Generate suggestions
    if (issues.tooShort > issues.tooLong) {
      suggestions.push({
        type: 'length',
        suggestion: 'Consider adding more detail to responses',
        confidence: issues.tooShort / negative.length
      });
    } else if (issues.tooLong > issues.tooShort) {
      suggestions.push({
        type: 'length',
        suggestion: 'Consider being more concise',
        confidence: issues.tooLong / negative.length
      });
    }
    
    return suggestions;
  }
  
  /**
   * Generate optimized prompt variant
   */
  generateVariant(templateName, suggestions) {
    const template = this.templates.get(templateName);
    if (!template) return null;
    
    let variant = template;
    
    for (const suggestion of suggestions) {
      if (suggestion.type === 'length') {
        if (suggestion.suggestion.includes('more detail')) {
          variant = variant.replace(/\n/g, '\n\nBe thorough and detailed in your response.\n');
        } else if (suggestion.suggestion.includes('concise')) {
          variant = variant.replace(/\n/g, '\n\nBe concise and to the point.\n');
        }
      }
    }
    
    return variant;
  }
}

/**
 * Improvement Tracker - Track improvement metrics over time
 */
class ImprovementTracker {
  constructor() {
    this.metrics = [];
    this.baselines = {};
  }
  
  /**
   * Set baseline metrics
   */
  setBaseline(name, metrics) {
    this.baselines[name] = {
      timestamp: new Date().toISOString(),
      ...metrics
    };
  }
  
  /**
   * Record metrics snapshot
   */
  recordSnapshot(metrics) {
    const snapshot = {
      timestamp: new Date().toISOString(),
      ...metrics
    };
    this.metrics.push(snapshot);
    return snapshot;
  }
  
  /**
   * Calculate improvement from baseline
   */
  calculateImprovement(currentMetrics, baselineName) {
    const baseline = this.baselines[baselineName];
    if (!baseline) return null;
    
    const improvement = {};
    
    for (const [key, value] of Object.entries(currentMetrics)) {
      if (typeof value === 'number' && typeof baseline[key] === 'number') {
        const change = value - baseline[key];
        const percentChange = baseline[key] !== 0 ? (change / baseline[key]) * 100 : 0;
        improvement[key] = {
          baseline: baseline[key],
          current: value,
          change,
          percentChange,
          improved: change > 0
        };
      }
    }
    
    return improvement;
  }
  
  /**
   * Get trend over time
   */
  getTrend(metricName, windowSize = 10) {
    const values = this.metrics
      .slice(-windowSize)
      .map(m => m[metricName])
      .filter(v => typeof v === 'number');
    
    if (values.length < 2) return null;
    
    // Simple linear regression
    const n = values.length;
    const xMean = (n - 1) / 2;
    const yMean = values.reduce((a, b) => a + b, 0) / n;
    
    let numerator = 0;
    let denominator = 0;
    
    for (let i = 0; i < n; i++) {
      numerator += (i - xMean) * (values[i] - yMean);
      denominator += (i - xMean) ** 2;
    }
    
    const slope = denominator !== 0 ? numerator / denominator : 0;
    
    return {
      direction: slope > 0 ? 'improving' : slope < 0 ? 'declining' : 'stable',
      slope,
      recentAverage: yMean,
      values
    };
  }
  
  /**
   * Generate improvement report
   */
  generateReport() {
    const report = {
      timestamp: new Date().toISOString(),
      totalSnapshots: this.metrics.length,
      baselines: Object.keys(this.baselines),
      trends: {},
      summary: {}
    };
    
    // Calculate trends for common metrics
    const metricNames = ['qualityScore', 'positiveRate', 'avgResponseTime', 'avgTokensUsed'];
    
    for (const name of metricNames) {
      const trend = this.getTrend(name);
      if (trend) {
        report.trends[name] = trend;
      }
    }
    
    // Calculate summary
    if (this.metrics.length > 0) {
      const latest = this.metrics[this.metrics.length - 1];
      report.summary = {
        latestQualityScore: latest.qualityScore,
        latestPositiveRate: latest.positiveRate,
        totalFeedback: latest.totalFeedback || this.metrics.length
      };
    }
    
    return report;
  }
}

/**
 * A/B Tester - Test prompt variants
 */
class ABTester {
  constructor() {
    this.experiments = new Map();
    this.results = new Map();
  }
  
  /**
   * Create an A/B test experiment
   */
  createExperiment(name, variants, config = {}) {
    const experiment = {
      name,
      variants,
      config: {
        trafficSplit: config.trafficSplit || variants.map(() => 1 / variants.length),
        minSamples: config.minSamples || 100,
        confidenceLevel: config.confidenceLevel || 0.95
      },
      samples: variants.map(() => []),
      startTime: new Date().toISOString(),
      status: 'running'
    };
    
    this.experiments.set(name, experiment);
    return experiment;
  }
  
  /**
   * Assign variant to a request
   */
  assignVariant(experimentName) {
    const experiment = this.experiments.get(experimentName);
    if (!experiment || experiment.status !== 'running') return null;
    
    const random = Math.random();
    let cumulative = 0;
    
    for (let i = 0; i < experiment.config.trafficSplit.length; i++) {
      cumulative += experiment.config.trafficSplit[i];
      if (random < cumulative) {
        return {
          variantIndex: i,
          variantName: experiment.variants[i].name,
          template: experiment.variants[i].template
        };
      }
    }
    
    return {
      variantIndex: 0,
      variantName: experiment.variants[0].name,
      template: experiment.variants[0].template
    };
  }
  
  /**
   * Record result for a variant
   */
  recordResult(experimentName, variantIndex, outcome) {
    const experiment = this.experiments.get(experimentName);
    if (!experiment) return;
    
    experiment.samples[variantIndex].push({
      timestamp: new Date().toISOString(),
      ...outcome
    });
  }
  
  /**
   * Analyze experiment results
   */
  analyzeResults(experimentName) {
    const experiment = this.experiments.get(experimentName);
    if (!experiment) return null;
    
    const analysis = {
      experimentName,
      status: experiment.status,
      variants: [],
      winner: null,
      confidence: 0
    };
    
    for (let i = 0; i < experiment.variants.length; i++) {
      const samples = experiment.samples[i];
      const positiveCount = samples.filter(s => s.rating === 'positive').length;
      const total = samples.length;
      
      analysis.variants.push({
        name: experiment.variants[i].name,
        samples: total,
        positiveCount,
        positiveRate: total > 0 ? positiveCount / total : 0,
        avgResponseTime: samples.length > 0 
          ? samples.reduce((sum, s) => sum + (s.responseTime || 0), 0) / samples.length 
          : 0
      });
    }
    
    // Determine winner using simple comparison
    // (In production, use proper statistical significance testing)
    if (analysis.variants.every(v => v.samples >= experiment.config.minSamples)) {
      const sorted = [...analysis.variants].sort((a, b) => b.positiveRate - a.positiveRate);
      analysis.winner = sorted[0].name;
      analysis.confidence = this.calculateConfidence(
        analysis.variants[0].positiveRate,
        analysis.variants[1]?.positiveRate || 0,
        analysis.variants[0].samples,
        analysis.variants[1]?.samples || 0
      );
    }
    
    return analysis;
  }
  
  /**
   * Calculate confidence (simplified)
   */
  calculateConfidence(rate1, rate2, n1, n2) {
    if (n1 < 30 || n2 < 30) return 0;
    
    // Simplified z-test
    const p1 = rate1;
    const p2 = rate2;
    const p = (p1 * n1 + p2 * n2) / (n1 + n2);
    
    const se = Math.sqrt(p * (1 - p) * (1/n1 + 1/n2));
    const z = se > 0 ? Math.abs(p1 - p2) / se : 0;
    
    // Approximate confidence from z-score
    return Math.min(1, z / 2.576); // 2.576 = z for 99% confidence
  }
  
  /**
   * Stop experiment
   */
  stopExperiment(name) {
    const experiment = this.experiments.get(name);
    if (experiment) {
      experiment.status = 'completed';
      experiment.endTime = new Date().toISOString();
    }
  }
}

/**
 * Collect feedback from interaction
 */
function collectFeedback(interaction) {
  const collector = new FeedbackCollector();
  return collector.collectFeedback(interaction);
}

/**
 * Generate training data from feedback
 */
function generateTrainingData(feedbackHistory, options) {
  const generator = new TrainingDatasetGenerator();
  return generator.generateTrainingData(feedbackHistory, options);
}

/**
 * Optimize prompts based on feedback
 */
function optimizePrompts(feedbackHistory, templates) {
  const optimizer = new PromptOptimizer();
  
  for (const [name, template] of Object.entries(templates)) {
    optimizer.registerTemplate(name, template);
  }
  
  const best = optimizer.getBestTemplate();
  const suggestions = optimizer.suggestImprovements(feedbackHistory, best);
  const variant = optimizer.generateVariant(best, suggestions);
  
  return {
    bestTemplate: best,
    suggestions,
    optimizedVariant: variant
  };
}

/**
 * Track improvement metrics
 */
function trackImprovement(before, after) {
  const tracker = new ImprovementTracker();
  tracker.setBaseline('before', before);
  return tracker.calculateImprovement(after, 'before');
}

/**
 * Generate improvement report
 */
function generateImprovementReport(metricsHistory) {
  const tracker = new ImprovementTracker();
  for (const metrics of metricsHistory) {
    tracker.recordSnapshot(metrics);
  }
  return tracker.generateReport();
}

/**
 * Create A/B test experiment
 */
function createABTest(name, variants, config) {
  const tester = new ABTester();
  return tester.createExperiment(name, variants, config);
}

module.exports = {
  collectFeedback,
  generateTrainingData,
  optimizePrompts,
  trackImprovement,
  generateImprovementReport,
  createABTest,
  FeedbackCollector,
  TrainingDatasetGenerator,
  PromptOptimizer,
  ImprovementTracker,
  ABTester
};
