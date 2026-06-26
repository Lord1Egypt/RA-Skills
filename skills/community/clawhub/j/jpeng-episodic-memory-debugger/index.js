/**
 * Episodic Memory Debugger - Diagnose and fix episodic memory issues
 * 
 * Features:
 * - Recall precision analysis
 * - Multi-modal encoding validation
 * - Indexing efficiency checks
 * - Irrelevant recall detection
 * - Memory drift detection
 * - Embedding quality analysis
 * - Retrieval ranking diagnostics
 * - Context relevance scoring
 * 
 * Usage:
 *   const debugger = require('./skills/episodic-memory-debugger');
 *   const analysis = debugger.analyzeRecallPrecision(memories, queries);
 *   const issues = debugger.detectEncodingIssues(memories);
 *   const report = debugger.generateDiagnosticReport(memories, queries, results);
 */

/**
 * Recall Precision Analyzer
 */
class RecallPrecisionAnalyzer {
  constructor() {
    this.metrics = {
      totalQueries: 0,
      relevantRetrievals: 0,
      irrelevantRetrievals: 0,
      missedRelevant: 0
    };
  }
  
  /**
   * Analyze recall precision for a set of queries
   */
  analyzeRecallPrecision(memories, queries, groundTruth) {
    const results = {
      overallPrecision: 0,
      overallRecall: 0,
      f1Score: 0,
      perQueryMetrics: [],
      issues: []
    };
    
    let totalRelevant = 0;
    let totalRetrieved = 0;
    let totalRelevantRetrieved = 0;
    
    for (const query of queries) {
      const queryId = query.id || query.text;
      const relevantIds = groundTruth[queryId] || [];
      const retrievedIds = query.results?.map(r => r.id) || [];
      
      const relevantRetrieved = retrievedIds.filter(id => relevantIds.includes(id));
      const precision = retrievedIds.length > 0 
        ? relevantRetrieved.length / retrievedIds.length 
        : 0;
      const recall = relevantIds.length > 0 
        ? relevantRetrieved.length / relevantIds.length 
        : 0;
      const f1 = precision + recall > 0 
        ? 2 * (precision * recall) / (precision + recall) 
        : 0;
      
      totalRelevant += relevantIds.length;
      totalRetrieved += retrievedIds.length;
      totalRelevantRetrieved += relevantRetrieved.length;
      
      results.perQueryMetrics.push({
        queryId,
        precision,
        recall,
        f1,
        retrievedCount: retrievedIds.length,
        relevantCount: relevantIds.length,
        relevantRetrieved: relevantRetrieved.length
      });
      
      // Detect issues
      if (precision < 0.5) {
        results.issues.push({
          type: 'low_precision',
          queryId,
          value: precision,
          message: `Low precision (${(precision * 100).toFixed(1)}%) - too many irrelevant results`
        });
      }
      
      if (recall < 0.5) {
        results.issues.push({
          type: 'low_recall',
          queryId,
          value: recall,
          message: `Low recall (${(recall * 100).toFixed(1)}%) - missing relevant memories`
        });
      }
    }
    
    results.overallPrecision = totalRetrieved > 0 
      ? totalRelevantRetrieved / totalRetrieved 
      : 0;
    results.overallRecall = totalRelevant > 0 
      ? totalRelevantRetrieved / totalRelevant 
      : 0;
    results.f1Score = results.overallPrecision + results.overallRecall > 0
      ? 2 * (results.overallPrecision * results.overallRecall) / 
        (results.overallPrecision + results.overallRecall)
      : 0;
    
    return results;
  }
  
  /**
   * Calculate Mean Reciprocal Rank
   */
  calculateMRR(queries, groundTruth) {
    let reciprocalRankSum = 0;
    
    for (const query of queries) {
      const queryId = query.id || query.text;
      const relevantIds = groundTruth[queryId] || [];
      const retrievedIds = query.results?.map(r => r.id) || [];
      
      // Find rank of first relevant result
      for (let i = 0; i < retrievedIds.length; i++) {
        if (relevantIds.includes(retrievedIds[i])) {
          reciprocalRankSum += 1 / (i + 1);
          break;
        }
      }
    }
    
    return queries.length > 0 ? reciprocalRankSum / queries.length : 0;
  }
  
  /**
   * Calculate Normalized Discounted Cumulative Gain
   */
  calculateNDCG(queries, groundTruth, relevanceScores, k = 10) {
    const ndcgScores = [];
    
    for (const query of queries) {
      const queryId = query.id || query.text;
      const retrievedIds = query.results?.slice(0, k)?.map(r => r.id) || [];
      const relevance = relevanceScores[queryId] || {};
      
      // Calculate DCG
      let dcg = 0;
      for (let i = 0; i < retrievedIds.length; i++) {
        const rel = relevance[retrievedIds[i]] || 0;
        dcg += rel / Math.log2(i + 2); // i+2 because log2(1) = 0
      }
      
      // Calculate ideal DCG
      const idealRelevance = Object.values(relevance).sort((a, b) => b - a).slice(0, k);
      let idcg = 0;
      for (let i = 0; i < idealRelevance.length; i++) {
        idcg += idealRelevance[i] / Math.log2(i + 2);
      }
      
      const ndcg = idcg > 0 ? dcg / idcg : 0;
      ndcgScores.push({ queryId, ndcg });
    }
    
    return {
      scores: ndcgScores,
      average: ndcgScores.reduce((sum, s) => sum + s.ndcg, 0) / ndcgScores.length
    };
  }
}

/**
 * Multi-Modal Encoding Validator
 */
class MultiModalEncodingValidator {
  constructor() {
    this.modalities = ['text', 'image', 'audio', 'video', 'structured'];
  }
  
  /**
   * Validate encoding consistency across modalities
   */
  validateEncodingConsistency(memories) {
    const issues = [];
    const modalityStats = {};
    
    for (const memory of memories) {
      const modalities = memory.modalities || ['text'];
      
      for (const mod of modalities) {
        if (!modalityStats[mod]) {
          modalityStats[mod] = { count: 0, hasEmbedding: 0, hasMetadata: 0 };
        }
        
        modalityStats[mod].count++;
        
        if (memory.embeddings?.[mod]) {
          modalityStats[mod].hasEmbedding++;
        } else {
          issues.push({
            type: 'missing_embedding',
            memoryId: memory.id,
            modality: mod,
            message: `Missing ${mod} embedding for memory ${memory.id}`
          });
        }
        
        if (memory.metadata?.[mod]) {
          modalityStats[mod].hasMetadata++;
        }
      }
    }
    
    // Check for modality imbalance
    const counts = Object.values(modalityStats).map(s => s.count);
    const maxCount = Math.max(...counts);
    const minCount = Math.min(...counts);
    
    if (maxCount > 0 && minCount > 0 && maxCount / minCount > 10) {
      issues.push({
        type: 'modality_imbalance',
        message: `Severe modality imbalance detected: ${JSON.stringify(modalityStats)}`,
        severity: 'warning'
      });
    }
    
    return {
      modalityStats,
      issues,
      consistency: this.calculateConsistencyScore(modalityStats)
    };
  }
  
  /**
   * Calculate consistency score
   */
  calculateConsistencyScore(modalityStats) {
    const scores = [];
    
    for (const [mod, stats] of Object.entries(modalityStats)) {
      if (stats.count > 0) {
        scores.push(stats.hasEmbedding / stats.count);
      }
    }
    
    return scores.length > 0 
      ? scores.reduce((a, b) => a + b, 0) / scores.length 
      : 0;
  }
  
  /**
   * Check embedding quality
   */
  checkEmbeddingQuality(memories, modality = 'text') {
    const issues = [];
    const stats = {
      total: 0,
      dimensions: new Set(),
      norms: [],
      sparsity: []
    };
    
    for (const memory of memories) {
      const embedding = memory.embeddings?.[modality];
      if (!embedding) continue;
      
      stats.total++;
      stats.dimensions.add(embedding.length);
      
      // Calculate norm
      const norm = Math.sqrt(embedding.reduce((sum, v) => sum + v * v, 0));
      stats.norms.push(norm);
      
      // Check for zero vectors
      if (norm === 0) {
        issues.push({
          type: 'zero_embedding',
          memoryId: memory.id,
          modality,
          message: `Zero vector embedding for memory ${memory.id}`
        });
      }
      
      // Calculate sparsity
      const zeros = embedding.filter(v => v === 0).length;
      const sparsity = zeros / embedding.length;
      stats.sparsity.push(sparsity);
      
      if (sparsity > 0.9) {
        issues.push({
          type: 'sparse_embedding',
          memoryId: memory.id,
          modality,
          value: sparsity,
          message: `Very sparse embedding (${(sparsity * 100).toFixed(1)}% zeros) for memory ${memory.id}`
        });
      }
    }
    
    // Check dimension consistency
    if (stats.dimensions.size > 1) {
      issues.push({
        type: 'inconsistent_dimensions',
        dimensions: Array.from(stats.dimensions),
        message: `Inconsistent embedding dimensions: ${Array.from(stats.dimensions).join(', ')}`
      });
    }
    
    return {
      stats: {
        total: stats.total,
        dimension: stats.dimensions.size === 1 ? Array.from(stats.dimensions)[0] : null,
        avgNorm: stats.norms.reduce((a, b) => a + b, 0) / stats.norms.length,
        avgSparsity: stats.sparsity.reduce((a, b) => a + b, 0) / stats.sparsity.length
      },
      issues
    };
  }
  
  /**
   * Detect cross-modal alignment issues
   */
  detectCrossModalAlignment(memories) {
    const issues = [];
    const alignments = [];
    
    for (const memory of memories) {
      const modalities = Object.keys(memory.embeddings || {});
      
      if (modalities.length < 2) continue;
      
      // Calculate cross-modal similarity
      for (let i = 0; i < modalities.length; i++) {
        for (let j = i + 1; j < modalities.length; j++) {
          const emb1 = memory.embeddings[modalities[i]];
          const emb2 = memory.embeddings[modalities[j]];
          
          if (!emb1 || !emb2) continue;
          
          const similarity = this.cosineSimilarity(emb1, emb2);
          alignments.push({
            memoryId: memory.id,
            modalities: [modalities[i], modalities[j]],
            similarity
          });
          
          // Low cross-modal alignment
          if (similarity < 0.3) {
            issues.push({
              type: 'low_cross_modal_alignment',
              memoryId: memory.id,
              modalities: [modalities[i], modalities[j]],
              value: similarity,
              message: `Low alignment between ${modalities[i]} and ${modalities[j]} (${similarity.toFixed(3)}) for memory ${memory.id}`
            });
          }
        }
      }
    }
    
    return {
      alignments,
      issues,
      avgAlignment: alignments.length > 0
        ? alignments.reduce((sum, a) => sum + a.similarity, 0) / alignments.length
        : 0
    };
  }
  
  /**
   * Calculate cosine similarity
   */
  cosineSimilarity(a, b) {
    if (a.length !== b.length) return 0;
    
    let dotProduct = 0;
    let normA = 0;
    let normB = 0;
    
    for (let i = 0; i < a.length; i++) {
      dotProduct += a[i] * b[i];
      normA += a[i] * a[i];
      normB += b[i] * b[i];
    }
    
    const denom = Math.sqrt(normA) * Math.sqrt(normB);
    return denom > 0 ? dotProduct / denom : 0;
  }
}

/**
 * Indexing Efficiency Checker
 */
class IndexingEfficiencyChecker {
  constructor() {
    this.metrics = {};
  }
  
  /**
   * Check indexing efficiency
   */
  checkIndexingEfficiency(memories, indexStats) {
    const issues = [];
    
    // Check index coverage
    const indexedCount = memories.filter(m => m.indexed).length;
    const coverage = memories.length > 0 ? indexedCount / memories.length : 0;
    
    if (coverage < 0.95) {
      issues.push({
        type: 'incomplete_indexing',
        value: coverage,
        message: `Only ${(coverage * 100).toFixed(1)}% of memories are indexed`
      });
    }
    
    // Check for stale indices
    const now = Date.now();
    const staleThreshold = 7 * 24 * 60 * 60 * 1000; // 7 days
    
    for (const memory of memories) {
      if (memory.indexed && memory.indexedAt) {
        const age = now - new Date(memory.indexedAt).getTime();
        if (age > staleThreshold && memory.updatedAt && new Date(memory.updatedAt).getTime() > new Date(memory.indexedAt).getTime()) {
          issues.push({
            type: 'stale_index',
            memoryId: memory.id,
            message: `Index is stale for memory ${memory.id}`
          });
        }
      }
    }
    
    // Check index fragmentation
    if (indexStats) {
      if (indexStats.fragmentationRatio > 0.3) {
        issues.push({
          type: 'high_fragmentation',
          value: indexStats.fragmentationRatio,
          message: `High index fragmentation: ${(indexStats.fragmentationRatio * 100).toFixed(1)}%`
        });
      }
      
      if (indexStats.avgLookupTime > 100) {
        issues.push({
          type: 'slow_lookup',
          value: indexStats.avgLookupTime,
          message: `Slow average lookup time: ${indexStats.avgLookupTime.toFixed(1)}ms`
        });
      }
    }
    
    return {
      coverage,
      indexedCount,
      totalCount: memories.length,
      issues
    };
  }
  
  /**
   * Analyze index structure
   */
  analyzeIndexStructure(memories, indexConfig) {
    const analysis = {
      depth: 0,
      branchFactor: 0,
      utilization: 0,
      issues: []
    };
    
    // Estimate tree depth (for tree-based indices)
    const n = memories.length;
    const branchFactor = indexConfig?.branchFactor || 100;
    analysis.branchFactor = branchFactor;
    analysis.depth = Math.ceil(Math.log(n) / Math.log(branchFactor));
    
    // Check for over-deep trees
    if (analysis.depth > 10) {
      analysis.issues.push({
        type: 'deep_tree',
        value: analysis.depth,
        message: `Index tree is too deep (${analysis.depth} levels)`
      });
    }
    
    // Estimate utilization
    const expectedNodes = Math.ceil(n / branchFactor);
    const actualNodes = indexConfig?.nodeCount || expectedNodes;
    analysis.utilization = expectedNodes > 0 ? n / (actualNodes * branchFactor) : 0;
    
    if (analysis.utilization < 0.5) {
      analysis.issues.push({
        type: 'low_utilization',
        value: analysis.utilization,
        message: `Low index utilization: ${(analysis.utilization * 100).toFixed(1)}%`
      });
    }
    
    return analysis;
  }
  
  /**
   * Check for duplicate entries
   */
  checkDuplicates(memories, similarityThreshold = 0.99) {
    const duplicates = [];
    const seen = new Map();
    
    for (const memory of memories) {
      const embedding = memory.embeddings?.text;
      if (!embedding) continue;
      
      // Create a simple hash for quick comparison
      const hash = embedding.slice(0, 10).map(v => v.toFixed(3)).join(',');
      
      if (seen.has(hash)) {
        const existing = seen.get(hash);
        duplicates.push({
          memory1: existing.id,
          memory2: memory.id,
          similarity: 1.0 // Approximate
        });
      } else {
        seen.set(hash, memory);
      }
    }
    
    return {
      duplicateCount: duplicates.length,
      duplicateRate: memories.length > 0 ? duplicates.length / memories.length : 0,
      duplicates
    };
  }
}

/**
 * Irrelevant Recall Detector
 */
class IrrelevantRecallDetector {
  constructor() {
    this.patterns = [];
  }
  
  /**
   * Detect patterns in irrelevant recalls
   */
  detectIrrelevantPatterns(queries, groundTruth) {
    const patterns = {
      byModality: {},
      byTimeRange: {},
      bySource: {},
      byTopic: {}
    };
    
    for (const query of queries) {
      const queryId = query.id || query.text;
      const relevantIds = new Set(groundTruth[queryId] || []);
      const retrieved = query.results || [];
      
      for (const result of retrieved) {
        if (!relevantIds.has(result.id)) {
          // This is an irrelevant recall
          const modality = result.modality || 'text';
          patterns.byModality[modality] = (patterns.byModality[modality] || 0) + 1;
          
          if (result.timestamp) {
            const age = Date.now() - new Date(result.timestamp).getTime();
            const ageBucket = this.getAgeBucket(age);
            patterns.byTimeRange[ageBucket] = (patterns.byTimeRange[ageBucket] || 0) + 1;
          }
          
          if (result.source) {
            patterns.bySource[result.source] = (patterns.bySource[result.source] || 0) + 1;
          }
          
          if (result.topic) {
            patterns.byTopic[result.topic] = (patterns.byTopic[result.topic] || 0) + 1;
          }
        }
      }
    }
    
    return patterns;
  }
  
  /**
   * Get age bucket for timestamp
   */
  getAgeBucket(ageMs) {
    const hours = ageMs / (1000 * 60 * 60);
    if (hours < 1) return '<1h';
    if (hours < 24) return '<1d';
    if (hours < 168) return '<1w';
    if (hours < 720) return '<1m';
    return '>1m';
  }
  
  /**
   * Score relevance of recalled memories
   */
  scoreRelevance(query, memories) {
    const queryTerms = this.tokenize(query.text || query);
    const scores = [];
    
    for (const memory of memories) {
      const memoryTerms = this.tokenize(memory.text || memory.content || '');
      
      // Calculate term overlap
      const overlap = queryTerms.filter(t => memoryTerms.includes(t));
      const jaccard = queryTerms.length + memoryTerms.length > 0
        ? overlap.length / (queryTerms.length + memoryTerms.length - overlap.length)
        : 0;
      
      // Calculate semantic similarity (if embeddings available)
      let semanticSimilarity = 0;
      if (query.embedding && memory.embeddings?.text) {
        semanticSimilarity = this.cosineSimilarity(query.embedding, memory.embeddings.text);
      }
      
      const relevanceScore = 0.4 * jaccard + 0.6 * semanticSimilarity;
      
      scores.push({
        memoryId: memory.id,
        relevanceScore,
        termOverlap: jaccard,
        semanticSimilarity,
        isLikelyIrrelevant: relevanceScore < 0.3
      });
    }
    
    return scores.sort((a, b) => b.relevanceScore - a.relevanceScore);
  }
  
  /**
   * Tokenize text
   */
  tokenize(text) {
    return (text || '')
      .toLowerCase()
      .replace(/[^\w\s]/g, ' ')
      .split(/\s+/)
      .filter(t => t.length > 2);
  }
  
  /**
   * Calculate cosine similarity
   */
  cosineSimilarity(a, b) {
    if (a.length !== b.length) return 0;
    
    let dotProduct = 0;
    let normA = 0;
    let normB = 0;
    
    for (let i = 0; i < a.length; i++) {
      dotProduct += a[i] * b[i];
      normA += a[i] * a[i];
      normB += b[i] * b[i];
    }
    
    const denom = Math.sqrt(normA) * Math.sqrt(normB);
    return denom > 0 ? dotProduct / denom : 0;
  }
}

/**
 * Memory Drift Detector
 */
class MemoryDriftDetector {
  constructor() {
    this.baseline = null;
  }
  
  /**
   * Set baseline for drift detection
   */
  setBaseline(memories) {
    this.baseline = {
      count: memories.length,
      avgEmbedding: this.calculateAverageEmbedding(memories),
      modalityDistribution: this.calculateModalityDistribution(memories),
      timeRange: this.calculateTimeRange(memories)
    };
  }
  
  /**
   * Detect drift from baseline
   */
  detectDrift(currentMemories) {
    if (!this.baseline) {
      return { drift: null, message: 'No baseline set' };
    }
    
    const current = {
      count: currentMemories.length,
      avgEmbedding: this.calculateAverageEmbedding(currentMemories),
      modalityDistribution: this.calculateModalityDistribution(currentMemories),
      timeRange: this.calculateTimeRange(currentMemories)
    };
    
    const drift = {
      countDrift: (current.count - this.baseline.count) / this.baseline.count,
      embeddingDrift: this.calculateEmbeddingDrift(this.baseline.avgEmbedding, current.avgEmbedding),
      modalityDrift: this.calculateDistributionDrift(this.baseline.modalityDistribution, current.modalityDistribution),
      timeDrift: this.calculateTimeDrift(this.baseline.timeRange, current.timeRange)
    };
    
    // Calculate overall drift score
    drift.overallDrift = Math.abs(drift.countDrift) * 0.2 +
                         Math.abs(drift.embeddingDrift) * 0.4 +
                         Math.abs(drift.modalityDrift) * 0.2 +
                         Math.abs(drift.timeDrift) * 0.2;
    
    drift.isSignificant = drift.overallDrift > 0.3;
    
    return drift;
  }
  
  /**
   * Calculate average embedding
   */
  calculateAverageEmbedding(memories) {
    const embeddings = memories
      .map(m => m.embeddings?.text)
      .filter(e => e && e.length > 0);
    
    if (embeddings.length === 0) return null;
    
    const dim = embeddings[0].length;
    const avg = new Array(dim).fill(0);
    
    for (const emb of embeddings) {
      for (let i = 0; i < dim; i++) {
        avg[i] += emb[i];
      }
    }
    
    return avg.map(v => v / embeddings.length);
  }
  
  /**
   * Calculate modality distribution
   */
  calculateModalityDistribution(memories) {
    const dist = {};
    
    for (const memory of memories) {
      const modalities = memory.modalities || ['text'];
      for (const mod of modalities) {
        dist[mod] = (dist[mod] || 0) + 1;
      }
    }
    
    const total = Object.values(dist).reduce((a, b) => a + b, 0);
    
    for (const mod of Object.keys(dist)) {
      dist[mod] /= total;
    }
    
    return dist;
  }
  
  /**
   * Calculate time range
   */
  calculateTimeRange(memories) {
    const timestamps = memories
      .map(m => m.timestamp && new Date(m.timestamp).getTime())
      .filter(t => t);
    
    if (timestamps.length === 0) return null;
    
    return {
      min: Math.min(...timestamps),
      max: Math.max(...timestamps),
      avg: timestamps.reduce((a, b) => a + b, 0) / timestamps.length
    };
  }
  
  /**
   * Calculate embedding drift
   */
  calculateEmbeddingDrift(baseline, current) {
    if (!baseline || !current) return 0;
    
    let diff = 0;
    const len = Math.min(baseline.length, current.length);
    
    for (let i = 0; i < len; i++) {
      diff += Math.abs(baseline[i] - current[i]);
    }
    
    return diff / len;
  }
  
  /**
   * Calculate distribution drift (KL divergence approximation)
   */
  calculateDistributionDrift(baseline, current) {
    const keys = new Set([...Object.keys(baseline), ...Object.keys(current)]);
    let drift = 0;
    
    for (const key of keys) {
      const p = baseline[key] || 0.001;
      const q = current[key] || 0.001;
      drift += p * Math.log(p / q);
    }
    
    return Math.abs(drift);
  }
  
  /**
   * Calculate time drift
   */
  calculateTimeDrift(baseline, current) {
    if (!baseline || !current) return 0;
    
    const baselineRange = baseline.max - baseline.min;
    const currentRange = current.max - current.min;
    
    if (baselineRange === 0) return 0;
    
    return Math.abs(currentRange - baselineRange) / baselineRange;
  }
}

/**
 * Analyze recall precision
 */
function analyzeRecallPrecision(memories, queries, groundTruth) {
  const analyzer = new RecallPrecisionAnalyzer();
  return analyzer.analyzeRecallPrecision(memories, queries, groundTruth);
}

/**
 * Detect encoding issues
 */
function detectEncodingIssues(memories) {
  const validator = new MultiModalEncodingValidator();
  return {
    consistency: validator.validateEncodingConsistency(memories),
    embeddingQuality: validator.checkEmbeddingQuality(memories),
    crossModalAlignment: validator.detectCrossModalAlignment(memories)
  };
}

/**
 * Check indexing efficiency
 */
function checkIndexingEfficiency(memories, indexStats) {
  const checker = new IndexingEfficiencyChecker();
  return {
    efficiency: checker.checkIndexingEfficiency(memories, indexStats),
    structure: checker.analyzeIndexStructure(memories, {}),
    duplicates: checker.checkDuplicates(memories)
  };
}

/**
 * Detect irrelevant recall patterns
 */
function detectIrrelevantRecall(queries, groundTruth) {
  const detector = new IrrelevantRecallDetector();
  return detector.detectIrrelevantPatterns(queries, groundTruth);
}

/**
 * Generate diagnostic report
 */
function generateDiagnosticReport(memories, queries, results, groundTruth) {
  const report = {
    timestamp: new Date().toISOString(),
    summary: {},
    details: {},
    recommendations: []
  };
  
  // Analyze recall precision
  if (queries && groundTruth) {
    const precisionAnalysis = analyzeRecallPrecision(memories, queries, groundTruth);
    report.details.recallPrecision = precisionAnalysis;
    report.summary.avgPrecision = precisionAnalysis.overallPrecision;
    report.summary.avgRecall = precisionAnalysis.overallRecall;
    report.summary.f1Score = precisionAnalysis.f1Score;
    
    if (precisionAnalysis.overallPrecision < 0.7) {
      report.recommendations.push({
        priority: 'high',
        area: 'recall_precision',
        recommendation: 'Consider improving query encoding or adjusting retrieval threshold'
      });
    }
  }
  
  // Detect encoding issues
  const encodingIssues = detectEncodingIssues(memories);
  report.details.encoding = encodingIssues;
  report.summary.encodingConsistency = encodingIssues.consistency.consistency;
  
  if (encodingIssues.consistency.consistency < 0.9) {
    report.recommendations.push({
      priority: 'medium',
      area: 'encoding',
      recommendation: 'Ensure all memories have consistent multi-modal embeddings'
    });
  }
  
  // Check indexing
  const indexingCheck = checkIndexingEfficiency(memories, {});
  report.details.indexing = indexingCheck;
  report.summary.indexCoverage = indexingCheck.efficiency.coverage;
  
  if (indexingCheck.efficiency.coverage < 0.95) {
    report.recommendations.push({
      priority: 'high',
      area: 'indexing',
      recommendation: 'Rebuild index to cover all memories'
    });
  }
  
  // Detect irrelevant patterns
  if (queries && groundTruth) {
    const irrelevantPatterns = detectIrrelevantRecall(queries, groundTruth);
    report.details.irrelevantPatterns = irrelevantPatterns;
  }
  
  // Overall health score
  report.summary.healthScore = (
    (report.summary.avgPrecision || 0.5) * 0.3 +
    report.summary.encodingConsistency * 0.3 +
    report.summary.indexCoverage * 0.2 +
    (report.summary.avgRecall || 0.5) * 0.2
  );
  
  return report;
}

module.exports = {
  analyzeRecallPrecision,
  detectEncodingIssues,
  checkIndexingEfficiency,
  detectIrrelevantRecall,
  generateDiagnosticReport,
  RecallPrecisionAnalyzer,
  MultiModalEncodingValidator,
  IndexingEfficiencyChecker,
  IrrelevantRecallDetector,
  MemoryDriftDetector
};
