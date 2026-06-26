/**
 * 2-Signal Fusion Retrieval Module
 * Combines vector similarity search with temporal relevance scoring
 */

const fs = require('fs');
const path = require('path');

/**
 * Calculate temporal relevance score using exponential decay
 * @param {Date} itemDate - Date of the item
 * @param {Date} referenceDate - Reference date (usually now)
 * @param {number} decayFactor - Decay factor (default: 0.95)
 * @returns {number} Temporal score between 0 and 1
 */
function calculateTemporalScore(itemDate, referenceDate = new Date(), decayFactor = 0.95) {
  const daysDiff = Math.abs(referenceDate - itemDate) / (1000 * 60 * 60 * 24);
  return Math.pow(decayFactor, daysDiff);
}

/**
 * Calculate cosine similarity between two vectors
 * @param {number[]} vec1 - First vector
 * @param {number[]} vec2 - Second vector
 * @returns {number} Cosine similarity (0-1)
 */
function cosineSimilarity(vec1, vec2) {
  if (!vec1 || !vec2 || vec1.length !== vec2.length) {
    return 0;
  }
  
  let dotProduct = 0;
  let norm1 = 0;
  let norm2 = 0;
  
  for (let i = 0; i < vec1.length; i++) {
    dotProduct += vec1[i] * vec2[i];
    norm1 += vec1[i] * vec1[i];
    norm2 += vec2[i] * vec2[i];
  }
  
  if (norm1 === 0 || norm2 === 0) return 0;
  
  return dotProduct / (Math.sqrt(norm1) * Math.sqrt(norm2));
}

/**
 * Fuse vector and temporal scores
 * @param {number} vectorScore - Vector similarity score (0-1)
 * @param {number} temporalScore - Temporal relevance score (0-1)
 * @param {object} weights - Weight configuration
 * @returns {number} Fused score (0-1)
 */
function fuseScores(vectorScore, temporalScore, weights = { vector: 0.6, time: 0.4 }) {
  return (vectorScore * weights.vector) + (temporalScore * weights.time);
}

/**
 * Retrieve items using 2-signal fusion
 * @param {string} query - Search query
 * @param {object} options - Retrieval options
 * @param {number[]} options.queryVector - Query embedding vector
 * @param {object[]} options.items - Items to search (must have vector and date)
 * @param {object} options.weights - Score weights
 * @param {object} options.dateRange - Date range filter {start, end}
 * @param {number} options.decayFactor - Temporal decay factor
 * @param {number} options.topK - Number of results to return
 * @returns {object[]} Ranked results with scores
 */
function retrieve(query, options = {}) {
  const {
    queryVector,
    items = [],
    weights = { vector: 0.6, time: 0.4 },
    dateRange = null,
    decayFactor = 0.95,
    topK = 10
  } = options;
  
  const referenceDate = new Date();
  const results = [];
  
  for (const item of items) {
    // Apply date range filter if specified
    if (dateRange) {
      const itemDate = new Date(item.date);
      if (itemDate < dateRange.start || itemDate > dateRange.end) {
        continue;
      }
    }
    
    // Calculate vector similarity
    const vectorScore = queryVector ? cosineSimilarity(queryVector, item.vector) : 0;
    
    // Calculate temporal relevance
    const itemDate = new Date(item.date);
    const temporalScore = calculateTemporalScore(itemDate, referenceDate, decayFactor);
    
    // Fuse scores
    const fusedScore = fuseScores(vectorScore, temporalScore, weights);
    
    results.push({
      ...item,
      scores: {
        vector: vectorScore,
        temporal: temporalScore,
        fused: fusedScore
      }
    });
  }
  
  // Sort by fused score descending
  results.sort((a, b) => b.scores.fused - a.scores.fused);
  
  // Return top K results
  return results.slice(0, topK);
}

/**
 * Batch retrieve with multiple queries
 * @param {object[]} queries - Array of query objects
 * @param {object} options - Retrieval options
 * @returns {object[][]} Results for each query
 */
function batchRetrieve(queries, options = {}) {
  return queries.map(query => retrieve(query, options));
}

/**
 * Get retrieval statistics
 * @param {object[]} results - Retrieval results
 * @returns {object} Statistics
 */
function getRetrievalStats(results) {
  if (!results || results.length === 0) {
    return {
      count: 0,
      avgVectorScore: 0,
      avgTemporalScore: 0,
      avgFusedScore: 0
    };
  }
  
  const count = results.length;
  const avgVectorScore = results.reduce((sum, r) => sum + r.scores.vector, 0) / count;
  const avgTemporalScore = results.reduce((sum, r) => sum + r.scores.temporal, 0) / count;
  const avgFusedScore = results.reduce((sum, r) => sum + r.scores.fused, 0) / count;
  
  return {
    count,
    avgVectorScore: Math.round(avgVectorScore * 1000) / 1000,
    avgTemporalScore: Math.round(avgTemporalScore * 1000) / 1000,
    avgFusedScore: Math.round(avgFusedScore * 1000) / 1000
  };
}

module.exports = {
  retrieve,
  batchRetrieve,
  calculateTemporalScore,
  cosineSimilarity,
  fuseScores,
  getRetrievalStats
};
