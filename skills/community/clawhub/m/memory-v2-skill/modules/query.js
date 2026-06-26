/**
 * Memory Query Module
 * 
 * Features:
 * - Local SQLite query with text search
 * - Multi-table search
 * - Result ranking
 * 
 * @module QueryModule
 * @version 2.5.3
 */

const sqlite3 = require('sqlite3').verbose();

class QueryModule {
  constructor(options = {}) {
    this.dbPath = options.dbPath || './memory-v2.5.db';
    this.db = null;
    this.stats = {
      totalQueries: 0,
      resultsFound: 0
    };
  }

  async init() {
    this.db = new sqlite3.Database(this.dbPath);
    console.log('✅ Query Module initialized');
    return this;
  }

  /**
   * Search across all memory tables
   * @param {string} queryText - Search text
   * @param {Object} options - Search options
   * @returns {Object} Search results
   */
  async search(queryText, options = {}) {
    const startTime = Date.now();
    
    console.log(`\n🔍 Search: "${queryText}"`);
    
    const results = [];
    
    // Search learning table
    try {
      const learning = await this.searchLearning(queryText);
      results.push(...learning.map(r => ({ ...r, _source: 'learning', _score: this.calculateScore(r, queryText) })));
    } catch (err) {
      // Table might not exist
    }
    
    // Search priorities table
    try {
      const priorities = await this.searchPriorities(queryText);
      results.push(...priorities.map(r => ({ ...r, _source: 'priority', _score: this.calculateScore(r, queryText) })));
    } catch (err) {
      // Table might not exist
    }
    
    // Search decisions table
    try {
      const decisions = await this.searchDecisions(queryText);
      results.push(...decisions.map(r => ({ ...r, _source: 'decision', _score: this.calculateScore(r, queryText) })));
    } catch (err) {
      // Table might not exist
    }
    
    // Search evolution table
    try {
      const evolution = await this.searchEvolution(queryText);
      results.push(...evolution.map(r => ({ ...r, _source: 'evolution', _score: this.calculateScore(r, queryText) })));
    } catch (err) {
      // Table might not exist
    }
    
    // Sort by score and limit
    results.sort((a, b) => b._score - a._score);
    const limited = results.slice(0, options.limit || 10);
    
    this.stats.totalQueries++;
    this.stats.resultsFound += limited.length;
    
    return {
      query: queryText,
      results: limited,
      total: results.length,
      time: Date.now() - startTime
    };
  }

  /**
   * Search learning table
   */
  async searchLearning(queryText) {
    const pattern = `%${queryText}%`;
    return new Promise((resolve, reject) => {
      const sql = `SELECT * FROM memory_learning 
                   WHERE learning_topic LIKE ? OR notes LIKE ? 
                   LIMIT 10`;
      this.db.all(sql, [pattern, pattern], (err, rows) => {
        if (err) reject(err);
        else resolve(rows || []);
      });
    });
  }

  /**
   * Search priorities table
   */
  async searchPriorities(queryText) {
    const pattern = `%${queryText}%`;
    return new Promise((resolve, reject) => {
      const sql = `SELECT * FROM memory_priorities 
                   WHERE context_summary LIKE ? OR keywords LIKE ? 
                   LIMIT 10`;
      this.db.all(sql, [pattern, pattern], (err, rows) => {
        if (err) reject(err);
        else resolve(rows || []);
      });
    });
  }

  /**
   * Search decisions table
   */
  async searchDecisions(queryText) {
    const pattern = `%${queryText}%`;
    return new Promise((resolve, reject) => {
      const sql = `SELECT * FROM memory_decisions 
                   WHERE decision_question LIKE ? OR decision_context LIKE ? OR rationale LIKE ? 
                   LIMIT 10`;
      this.db.all(sql, [pattern, pattern, pattern], (err, rows) => {
        if (err) reject(err);
        else resolve(rows || []);
      });
    });
  }

  /**
   * Search evolution table
   */
  async searchEvolution(queryText) {
    const pattern = `%${queryText}%`;
    return new Promise((resolve, reject) => {
      const sql = `SELECT * FROM memory_evolution 
                   WHERE skill_name LIKE ? OR skill_category LIKE ? 
                   LIMIT 10`;
      this.db.all(sql, [pattern, pattern], (err, rows) => {
        if (err) reject(err);
        else resolve(rows || []);
      });
    });
  }

  /**
   * Calculate relevance score
   */
  calculateScore(row, queryText) {
    const query = queryText.toLowerCase();
    let score = 0;
    
    // Check all text fields
    for (const key of Object.keys(row)) {
      if (typeof row[key] === 'string') {
        const value = row[key].toLowerCase();
        if (value.includes(query)) {
          score += 1;
          // Bonus for exact match
          if (value === query) score += 2;
        }
      }
    }
    
    return score;
  }

  getStats() {
    return this.stats;
  }

  close() {
    if (this.db) this.db.close();
  }
}

module.exports = QueryModule;
