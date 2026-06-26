/**
 * Metrics Collector - Observability & Performance Monitoring
 * 
 * Tracks routing decisions, inference latency, cache hit rates,
 * and other performance metrics.
 */

const fs = require('fs').promises;
const path = require('path');

class MetricsCollector {
  constructor(monitoringConfig = {}) {
    this.config = monitoringConfig || {};
    this.metricsPath = monitoringConfig.metricsPath || 'memory/nirvana-metrics.json';
    this.debugLogging = monitoringConfig.debugLogging || false;
    this.metrics = {
      queries: 0,
      localQueries: 0,
      cloudQueries: 0,
      hybridQueries: 0,
      totalLatency: 0,
      averageLatency: 0,
      cacheHits: 0,
      cacheMisses: 0,
      errors: 0,
      lastUpdated: new Date().toISOString()
    };
  }

  /**
   * Initialize metrics collector
   */
  async initialize() {
    try {
      const dir = path.dirname(this.metricsPath);
      await fs.mkdir(dir, { recursive: true });
      
      // Try to load existing metrics
      try {
        const content = await fs.readFile(this.metricsPath, 'utf8');
        this.metrics = JSON.parse(content);
      } catch (e) {
        // File doesn't exist yet, use defaults
      }

      console.log('[MetricsCollector] Initialized');
    } catch (error) {
      console.warn('[MetricsCollector] Initialization warning:', error.message);
    }
  }

  /**
   * Record query metrics
   */
  async record(event) {
    const {
      query,
      provider,
      model,
      duration,
      success,
      error
    } = event;

    // Update counters
    this.metrics.queries++;
    this.metrics.totalLatency += duration || 0;
    this.metrics.averageLatency = this.metrics.totalLatency / this.metrics.queries;

    if (provider === 'local') {
      this.metrics.localQueries++;
    } else if (provider === 'cloud') {
      this.metrics.cloudQueries++;
    } else if (provider === 'hybrid') {
      this.metrics.hybridQueries++;
    }

    if (!success) {
      this.metrics.errors++;
    }

    this.metrics.lastUpdated = new Date().toISOString();

    // Debug logging
    if (this.debugLogging) {
      console.log('[Metrics]', {
        provider,
        duration,
        success,
        totalQueries: this.metrics.queries
      });
    }

    // Persist periodically (every 100 queries)
    if (this.metrics.queries % 100 === 0) {
      await this.flush();
    }
  }

  /**
   * Record cache hit
   */
  recordCacheHit() {
    this.metrics.cacheHits++;
  }

  /**
   * Record cache miss
   */
  recordCacheMiss() {
    this.metrics.cacheMisses++;
  }

  /**
   * Record query metric
   */
  async recordQueryMetric(query, response, duration) {
    const success = !!response;
    await this.record({
      query,
      duration,
      success
    });
  }

  /**
   * Get current metrics
   */
  getMetrics() {
    const cacheTotal = this.metrics.cacheHits + this.metrics.cacheMisses;
    const cacheHitRate = cacheTotal > 0
      ? (this.metrics.cacheHits / cacheTotal * 100).toFixed(2)
      : 0;

    const localPercentage = this.metrics.queries > 0
      ? (this.metrics.localQueries / this.metrics.queries * 100).toFixed(2)
      : 0;

    return {
      ...this.metrics,
      cacheHitRate: parseFloat(cacheHitRate),
      localPercentage: parseFloat(localPercentage)
    };
  }

  /**
   * Flush metrics to disk
   */
  async flush() {
    try {
      const metricsToWrite = this.getMetrics();
      await fs.writeFile(
        this.metricsPath,
        JSON.stringify(metricsToWrite, null, 2)
      );

      if (this.debugLogging) {
        console.log('[MetricsCollector] Flushed metrics to:', this.metricsPath);
      }
    } catch (error) {
      console.warn('[MetricsCollector] Failed to flush metrics:', error.message);
    }
  }

  /**
   * Health check
   */
  healthCheck() {
    return this.getMetrics();
  }
}

module.exports = MetricsCollector;
