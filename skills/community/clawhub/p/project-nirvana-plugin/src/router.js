/**
 * Query Router - Local vs Cloud Decision Engine
 * 
 * Decides whether to:
 * 1. Answer locally (Ollama)
 * 2. Fall back to cloud (Claude/Gemini)
 * 3. Hybrid (local + cloud for validation)
 */

class Router {
  constructor(routingConfig, privacyConfig) {
    this.config = routingConfig || {};
    this.privacyConfig = privacyConfig || {};
    this.localFirst = this.config.localFirst !== false;
    this.localThreshold = this.config.localThreshold || 0.8;
    this.cloudFallback = this.config.cloudFallback !== false;
    this.cloudModels = this.config.cloudModels || [
      'anthropic/claude-haiku-4-5',
      'google/gemini-2.5-flash'
    ];
    this.routingLogic = this.config.routingLogic || 'hybrid';
    this.cache = new Map();
    this.stats = {
      localDecisions: 0,
      cloudDecisions: 0,
      hybridDecisions: 0
    };
  }

  /**
   * Main routing decision
   */
  async decide(context) {
    const {
      query,
      queryContext = {},
      ollamaAvailable,
      cloudAvailable
    } = context;

    // Step 1: Check cache
    const cacheKey = this.getCacheKey(query);
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    // Step 2: Analyze query characteristics
    const analysis = this.analyzeQuery(query, queryContext);

    // Step 3: Apply routing logic
    let decision;
    if (!this.localFirst || !ollamaAvailable) {
      // If no cloud available and local is down, error
      if (!cloudAvailable) {
        throw new Error('No inference provider available (Ollama down, no cloud API)');
      }
      // Fall back to cloud if local is disabled or unavailable
      decision = {
        provider: 'cloud',
        model: this.selectCloudModel(),
        reasoning: 'Local unavailable or disabled'
      };
      this.stats.cloudDecisions++;
    } else {
      // Determine routing based on analysis (local is available)
      decision = this.applyRoutingLogic(analysis);
    }

    // Step 4: Validate decision
    if (!cloudAvailable && decision.provider === 'cloud') {
      console.warn('[Router] Cloud unavailable, forcing local');
      decision = {
        provider: 'local',
        model: 'qwen3.5:9b',
        reasoning: 'Cloud unavailable'
      };
    }

    // Step 5: Cache decision
    if (this.config.cachingEnabled !== false) {
      this.cache.set(cacheKey, decision);
      this.pruneCache();
    }

    return decision;
  }

  /**
   * Analyze query characteristics
   */
  analyzeQuery(query, context = {}) {
    const text = typeof query === 'string' ? query : query.text || '';

    return {
      // Complexity signals
      tokenCount: this.estimateTokens(text),
      isQuestion: text.trim().endsWith('?'),
      requiresReasoning: this.hasReasoningKeywords(text),
      requiresCompute: this.hasComputeKeywords(text),
      requiresPrivacy: this.requiresPrivacy(text, context),

      // Domain signals
      domain: this.detectDomain(text),
      isSpecialized: this.isSpecializedQuery(text),

      // Length signals
      shortQuery: text.length < 100,
      mediumQuery: text.length >= 100 && text.length < 500,
      longQuery: text.length >= 500,

      // Intent signals
      isFactual: this.isFactualQuery(text),
      isCreative: this.isCreativeQuery(text),
      isAnalytical: this.isAnalyticalQuery(text)
    };
  }

  /**
   * Apply routing logic based on analysis
   */
  applyRoutingLogic(analysis) {
    switch (this.routingLogic) {
      case 'task-complexity':
        return this.routeByComplexity(analysis);

      case 'token-count':
        return this.routeByTokenCount(analysis);

      case 'domain-confidence':
        return this.routeByDomainConfidence(analysis);

      case 'hybrid':
      default:
        return this.routeHybrid(analysis);
    }
  }

  /**
   * Route by task complexity
   */
  routeByComplexity(analysis) {
    const complexity = this.calculateComplexity(analysis);

    // Simple queries: local
    if (complexity < 0.4) {
      this.stats.localDecisions++;
      return {
        provider: 'local',
        model: 'qwen3.5:9b',
        reasoning: 'Low complexity - local sufficient',
        confidence: 0.95
      };
    }

    // Medium complexity: try local first, hybrid validation
    if (complexity < 0.7) {
      this.stats.hybridDecisions++;
      return {
        provider: 'hybrid',
        primaryModel: 'qwen3.5:9b',
        validationModel: 'anthropic/claude-haiku-4-5',
        reasoning: 'Medium complexity - local with validation',
        confidence: 0.75
      };
    }

    // High complexity: cloud
    this.stats.cloudDecisions++;
    return {
      provider: 'cloud',
      model: this.selectCloudModel(),
      reasoning: 'High complexity - cloud preferred',
      confidence: 0.85
    };
  }

  /**
   * Route by token count
   */
  routeByTokenCount(analysis) {
    const tokens = analysis.tokenCount;

    // < 200 tokens: definitely local
    if (tokens < 200) {
      this.stats.localDecisions++;
      return {
        provider: 'local',
        model: 'qwen3.5:9b',
        reasoning: 'Few tokens - local efficient'
      };
    }

    // 200-1000 tokens: local preferred
    if (tokens < 1000) {
      this.stats.localDecisions++;
      return {
        provider: 'local',
        model: 'qwen3.5:9b',
        reasoning: 'Medium tokens - local preferred'
      };
    }

    // > 1000 tokens: cloud preferred
    this.stats.cloudDecisions++;
    return {
      provider: 'cloud',
      model: this.selectCloudModel(),
      reasoning: 'Many tokens - cloud preferred'
    };
  }

  /**
   * Route by domain confidence
   */
  routeByDomainConfidence(analysis) {
    const confidence = this.getDomainConfidence(analysis.domain);

    if (confidence > this.localThreshold) {
      this.stats.localDecisions++;
      return {
        provider: 'local',
        model: 'qwen3.5:9b',
        reasoning: `High confidence in ${analysis.domain} domain`,
        confidence
      };
    }

    this.stats.cloudDecisions++;
    return {
      provider: 'cloud',
      model: this.selectCloudModel(),
      reasoning: `Low confidence in domain - cloud preferred`,
      confidence: 1 - confidence
    };
  }

  /**
   * Hybrid routing (default)
   * Balances all signals
   */
  routeHybrid(analysis) {
    let localScore = 0;
    let maxScore = 0;

    // Scoring factors
    if (analysis.shortQuery) {
      localScore += 1;
      maxScore += 1;
    }
    if (!analysis.requiresCompute) {
      localScore += 1;
      maxScore += 1;
    }
    if (!analysis.requiresReasoning) {
      localScore += 0.5;
      maxScore += 1;
    }
    if (analysis.isFactual) {
      localScore += 0.5;
      maxScore += 1;
    }
    if (!analysis.requiresPrivacy) {
      localScore += 1;
      maxScore += 1;
    }

    const score = localScore / maxScore;

    // Decision thresholds
    if (score > 0.85) {
      // Definitely local
      this.stats.localDecisions++;
      return {
        provider: 'local',
        model: 'qwen3.5:9b',
        reasoning: 'All signals favor local',
        confidence: score
      };
    } else if (score > this.localThreshold) {
      // Prefer local
      this.stats.localDecisions++;
      return {
        provider: 'local',
        model: 'qwen3.5:9b',
        reasoning: 'Signals favor local',
        confidence: score
      };
    } else if (score > 0.5) {
      // Hybrid (local primary, cloud validation)
      this.stats.hybridDecisions++;
      return {
        provider: 'hybrid',
        primaryModel: 'qwen3.5:9b',
        validationModel: 'anthropic/claude-haiku-4-5',
        reasoning: 'Mixed signals - hybrid approach',
        confidence: score
      };
    } else {
      // Cloud preferred
      this.stats.cloudDecisions++;
      return {
        provider: 'cloud',
        model: this.selectCloudModel(),
        reasoning: 'Signals favor cloud',
        confidence: 1 - score
      };
    }
  }

  /**
   * Helper: Estimate token count
   */
  estimateTokens(text) {
    // Rough approximation: ~1 token per 4 characters
    return Math.ceil(text.length / 4);
  }

  /**
   * Helper: Detect reasoning keywords
   */
  hasReasoningKeywords(text) {
    const keywords = [
      'why', 'how', 'explain', 'analyze', 'prove', 'calculate',
      'derive', 'reason', 'logic', 'think', 'consider', 'evaluate'
    ];
    return keywords.some(kw => text.toLowerCase().includes(kw));
  }

  /**
   * Helper: Detect compute-intensive keywords
   */
  hasComputeKeywords(text) {
    const keywords = [
      'compute', 'calculate', 'simulate', 'model', 'algorithm',
      'optimize', 'train', 'regression', 'classification'
    ];
    return keywords.some(kw => text.toLowerCase().includes(kw));
  }

  /**
   * Helper: Check if requires privacy
   */
  requiresPrivacy(text, context) {
    // If query mentions identity/personal info, route to local
    const sensitiveKeywords = ['my', 'i ', 'me ', 'personal', 'private'];
    return sensitiveKeywords.some(kw => text.toLowerCase().includes(kw));
  }

  /**
   * Helper: Detect domain
   */
  detectDomain(text) {
    const domains = {
      biology: ['protein', 'gene', 'cell', 'dna', 'crispr', 'metabolic'],
      crypto: ['blockchain', 'defi', 'ethereum', 'bitcoin', 'zk', 'fhe'],
      trading: ['price', 'market', 'stock', 'volume', 'trend'],
      research: ['paper', 'study', 'hypothesis', 'experiment']
    };

    for (const [domain, keywords] of Object.entries(domains)) {
      if (keywords.some(kw => text.toLowerCase().includes(kw))) {
        return domain;
      }
    }

    return 'general';
  }

  /**
   * Helper: Is specialized query
   */
  isSpecializedQuery(text) {
    return text.length > 200 || text.match(/[^\w\s]/g)?.length > 5;
  }

  /**
   * Helper: Calculate overall complexity
   */
  calculateComplexity(analysis) {
    let score = 0;

    if (analysis.requiresReasoning) score += 0.3;
    if (analysis.requiresCompute) score += 0.2;
    if (analysis.longQuery) score += 0.2;
    if (analysis.isAnalytical) score += 0.15;
    if (analysis.isSpecialized) score += 0.15;

    return Math.min(score, 1.0);
  }

  /**
   * Helper: Get domain confidence
   */
  getDomainConfidence(domain) {
    // Local model confidence by domain
    const confidenceMap = {
      general: 0.9,
      biology: 0.75,
      crypto: 0.8,
      trading: 0.7,
      research: 0.65
    };

    return confidenceMap[domain] || 0.7;
  }

  /**
   * Helper: Is factual query
   */
  isFactualQuery(text) {
    return text.includes('what') || text.includes('when') || text.includes('where');
  }

  /**
   * Helper: Is creative query
   */
  isCreativeQuery(text) {
    const keywords = ['write', 'create', 'generate', 'compose', 'design'];
    return keywords.some(kw => text.toLowerCase().includes(kw));
  }

  /**
   * Helper: Is analytical query
   */
  isAnalyticalQuery(text) {
    const keywords = ['analyze', 'compare', 'evaluate', 'assess'];
    return keywords.some(kw => text.toLowerCase().includes(kw));
  }

  /**
   * Select cloud model
   */
  selectCloudModel() {
    // Round-robin or prefer cheaper model
    return this.cloudModels[0];
  }

  /**
   * Get cache key
   */
  getCacheKey(query) {
    const text = typeof query === 'string' ? query : query.text || '';
    return Buffer.from(text).toString('base64').slice(0, 32);
  }

  /**
   * Prune old cache entries
   */
  pruneCache() {
    const maxCacheSize = this.config.maxCacheSize || 1000;
    if (this.cache.size > maxCacheSize) {
      const keysToDelete = Array.from(this.cache.keys()).slice(0, this.cache.size - maxCacheSize);
      keysToDelete.forEach(key => this.cache.delete(key));
    }
  }

  /**
   * Reconfigure router
   */
  reconfigure(newConfig) {
    this.config = newConfig || {};
    this.localFirst = this.config.localFirst !== false;
    this.localThreshold = this.config.localThreshold || 0.8;
  }

  /**
   * Health check
   */
  healthCheck() {
    return {
      totalDecisions: this.stats.localDecisions + this.stats.cloudDecisions + this.stats.hybridDecisions,
      localDecisions: this.stats.localDecisions,
      cloudDecisions: this.stats.cloudDecisions,
      hybridDecisions: this.stats.hybridDecisions,
      cacheSize: this.cache.size,
      localPercentage: this.stats.localDecisions / (this.stats.localDecisions + this.stats.cloudDecisions + this.stats.hybridDecisions) || 0
    };
  }
}

module.exports = Router;
