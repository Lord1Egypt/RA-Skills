/**
 * Agent Metrics Monitor - Monitor and alert agent abnormal behavior metrics
 * 
 * Features:
 * - Metrics collection for agent operations
 * - Percentile latency calculation (P50, P95, P99)
 * - Error rate and success rate tracking
 * - Prometheus-compatible metrics export
 * - Grafana dashboard configuration generation
 * - Alert rule definitions for anomalies
 * - Time-series data storage
 * - Anomaly detection
 * 
 * Usage:
 *   const monitor = require('./skills/agent-metrics-monitor');
 *   const collector = monitor.createMetricsCollector({ serviceName: 'my-agent' });
 *   collector.recordLatency('tool_call', 150);
 *   collector.recordError('tool_call', 'timeout');
 *   const prometheus = collector.exportPrometheus();
 */

/**
 * Histogram - For latency percentile calculation
 */
class Histogram {
  constructor(options = {}) {
    this.buckets = options.buckets || [1, 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000];
    this.counts = new Array(this.buckets.length + 1).fill(0); // +1 for overflow
    this.sum = 0;
    this.count = 0;
    this.values = []; // Store recent values for exact percentile calculation
    this.maxValues = options.maxValues || 10000;
  }
  
  /**
   * Observe a value
   */
  observe(value) {
    this.sum += value;
    this.count++;
    
    // Find bucket
    let bucketIndex = this.buckets.length;
    for (let i = 0; i < this.buckets.length; i++) {
      if (value <= this.buckets[i]) {
        bucketIndex = i;
        break;
      }
    }
    this.counts[bucketIndex]++;
    
    // Store value for exact percentile
    this.values.push(value);
    if (this.values.length > this.maxValues) {
      this.values.shift();
    }
  }
  
  /**
   * Calculate percentile
   */
  percentile(p) {
    if (this.values.length === 0) return 0;
    
    const sorted = [...this.values].sort((a, b) => a - b);
    const index = Math.ceil((p / 100) * sorted.length) - 1;
    return sorted[Math.max(0, index)];
  }
  
  /**
   * Get P50 (median)
   */
  p50() {
    return this.percentile(50);
  }
  
  /**
   * Get P95
   */
  p95() {
    return this.percentile(95);
  }
  
  /**
   * Get P99
   */
  p99() {
    return this.percentile(99);
  }
  
  /**
   * Get statistics
   */
  getStats() {
    return {
      count: this.count,
      sum: this.sum,
      mean: this.count > 0 ? this.sum / this.count : 0,
      p50: this.p50(),
      p95: this.p95(),
      p99: this.p99(),
      buckets: this.buckets.map((b, i) => ({
        le: b,
        count: this.counts[i]
      }))
    };
  }
  
  /**
   * Reset histogram
   */
  reset() {
    this.counts.fill(0);
    this.sum = 0;
    this.count = 0;
    this.values = [];
  }
}

/**
 * Counter - Monotonically increasing value
 */
class Counter {
  constructor(name, labels = {}) {
    this.name = name;
    this.labels = labels;
    this.value = 0;
    this.lastIncrement = Date.now();
  }
  
  /**
   * Increment counter
   */
  inc(value = 1) {
    this.value += value;
    this.lastIncrement = Date.now();
  }
  
  /**
   * Get current value
   */
  get() {
    return this.value;
  }
  
  /**
   * Reset counter
   */
  reset() {
    this.value = 0;
    this.lastIncrement = Date.now();
  }
}

/**
 * Gauge - Point-in-time value
 */
class Gauge {
  constructor(name, labels = {}) {
    this.name = name;
    this.labels = labels;
    this.value = 0;
    this.lastUpdate = Date.now();
  }
  
  /**
   * Set gauge value
   */
  set(value) {
    this.value = value;
    this.lastUpdate = Date.now();
  }
  
  /**
   * Increment gauge
   */
  inc(value = 1) {
    this.value += value;
    this.lastUpdate = Date.now();
  }
  
  /**
   * Decrement gauge
   */
  dec(value = 1) {
    this.value -= value;
    this.lastUpdate = Date.now();
  }
  
  /**
   * Get current value
   */
  get() {
    return this.value;
  }
}

/**
 * Time Series Store - Store metrics over time
 */
class TimeSeriesStore {
  constructor(options = {}) {
    this.maxPoints = options.maxPoints || 10000;
    this.series = new Map(); // metric_name -> [{ timestamp, value, labels }]
    this.retentionMs = options.retentionMs || 24 * 60 * 60 * 1000; // 24 hours
  }
  
  /**
   * Add data point
   */
  addPoint(name, value, labels = {}) {
    if (!this.series.has(name)) {
      this.series.set(name, []);
    }
    
    const points = this.series.get(name);
    points.push({
      timestamp: Date.now(),
      value,
      labels
    });
    
    // Trim old points
    if (points.length > this.maxPoints) {
      points.shift();
    }
  }
  
  /**
   * Get points for a metric
   */
  getPoints(name, since = null) {
    const points = this.series.get(name) || [];
    const cutoff = since || Date.now() - this.retentionMs;
    return points.filter(p => p.timestamp >= cutoff);
  }
  
  /**
   * Get all series
   */
  getAllSeries() {
    const result = {};
    for (const [name, points] of this.series) {
      result[name] = points;
    }
    return result;
  }
  
  /**
   * Clean up old data
   */
  cleanup() {
    const cutoff = Date.now() - this.retentionMs;
    for (const [name, points] of this.series) {
      const filtered = points.filter(p => p.timestamp >= cutoff);
      this.series.set(name, filtered);
    }
  }
}

/**
 * Alert Rule - Define alert conditions
 */
class AlertRule {
  constructor(options) {
    this.name = options.name;
    this.metric = options.metric;
    this.condition = options.condition; // 'gt', 'lt', 'eq', 'gte', 'lte'
    this.threshold = options.threshold;
    this.duration = options.duration || 60000; // 1 minute default
    this.severity = options.severity || 'warning'; // 'info', 'warning', 'critical'
    this.message = options.message;
    this.labels = options.labels || {};
    this.state = 'inactive'; // 'inactive', 'pending', 'firing'
    this.lastEvaluation = null;
    this.firingSince = null;
  }
  
  /**
   * Evaluate the rule
   */
  evaluate(value) {
    this.lastEvaluation = Date.now();
    
    let triggered = false;
    switch (this.condition) {
      case 'gt': triggered = value > this.threshold; break;
      case 'lt': triggered = value < this.threshold; break;
      case 'eq': triggered = value === this.threshold; break;
      case 'gte': triggered = value >= this.threshold; break;
      case 'lte': triggered = value <= this.threshold; break;
    }
    
    if (triggered) {
      if (this.state === 'inactive') {
        this.state = 'pending';
        this.firingSince = Date.now();
      } else if (this.state === 'pending') {
        if (Date.now() - this.firingSince >= this.duration) {
          this.state = 'firing';
        }
      }
    } else {
      this.state = 'inactive';
      this.firingSince = null;
    }
    
    return {
      name: this.name,
      state: this.state,
      value,
      threshold: this.threshold,
      severity: this.severity,
      message: this.message,
      duration: this.duration,
      firingSince: this.firingSince
    };
  }
}

/**
 * Metrics Collector - Collect and aggregate metrics
 */
class MetricsCollector {
  constructor(options = {}) {
    this.serviceName = options.serviceName || 'agent';
    this.prefix = options.prefix || 'agent';
    this.counters = new Map();
    this.gauges = new Map();
    this.histograms = new Map();
    this.timeSeries = new TimeSeriesStore(options.timeSeries);
    this.alertRules = new Map();
    this.alertHistory = [];
    this.maxAlertHistory = options.maxAlertHistory || 1000;
    this.labelSets = new Map();
  }
  
  /**
   * Create or get counter
   */
  counter(name, labels = {}) {
    const key = this._makeKey(name, labels);
    if (!this.counters.has(key)) {
      this.counters.set(key, new Counter(name, labels));
    }
    return this.counters.get(key);
  }
  
  /**
   * Create or get gauge
   */
  gauge(name, labels = {}) {
    const key = this._makeKey(name, labels);
    if (!this.gauges.has(key)) {
      this.gauges.set(key, new Gauge(name, labels));
    }
    return this.gauges.get(key);
  }
  
  /**
   * Create or get histogram
   */
  histogram(name, labels = {}, options = {}) {
    const key = this._makeKey(name, labels);
    if (!this.histograms.has(key)) {
      this.histograms.set(key, new Histogram(options));
    }
    return this.histograms.get(key);
  }
  
  /**
   * Record latency
   */
  recordLatency(operation, latencyMs, labels = {}) {
    const h = this.histogram(`${operation}_latency`, labels);
    h.observe(latencyMs);
    
    // Store in time series
    this.timeSeries.addPoint(`${operation}_latency_p99`, h.p99(), labels);
    this.timeSeries.addPoint(`${operation}_latency_p95`, h.p95(), labels);
    this.timeSeries.addPoint(`${operation}_latency_p50`, h.p50(), labels);
    
    return h;
  }
  
  /**
   * Record error
   */
  recordError(operation, errorType, labels = {}) {
    const errorCounter = this.counter(`${operation}_errors_total`, { ...labels, error_type: errorType });
    errorCounter.inc();
    
    const totalCounter = this.counter(`${operation}_total`, labels);
    totalCounter.inc();
    
    // Store in time series
    this.timeSeries.addPoint(`${operation}_errors`, errorCounter.get(), { ...labels, error_type: errorType });
    
    return errorCounter;
  }
  
  /**
   * Record success
   */
  recordSuccess(operation, labels = {}) {
    const successCounter = this.counter(`${operation}_success_total`, labels);
    successCounter.inc();
    
    const totalCounter = this.counter(`${operation}_total`, labels);
    totalCounter.inc();
    
    return successCounter;
  }
  
  /**
   * Calculate error rate
   */
  getErrorRate(operation, labels = {}, windowMs = 60000) {
    const errors = this.counter(`${operation}_errors_total`, labels).get();
    const total = this.counter(`${operation}_total`, labels).get();
    
    return total > 0 ? errors / total : 0;
  }
  
  /**
   * Calculate success rate
   */
  getSuccessRate(operation, labels = {}, windowMs = 60000) {
    const successes = this.counter(`${operation}_success_total`, labels).get();
    const total = this.counter(`${operation}_total`, labels).get();
    
    return total > 0 ? successes / total : 0;
  }
  
  /**
   * Add alert rule
   */
  addAlertRule(rule) {
    const alertRule = rule instanceof AlertRule ? rule : new AlertRule(rule);
    this.alertRules.set(alertRule.name, alertRule);
    return alertRule;
  }
  
  /**
   * Evaluate all alert rules
   */
  evaluateAlerts() {
    const results = [];
    
    for (const [name, rule] of this.alertRules) {
      // Get current metric value
      let value = 0;
      
      if (this.counters.has(rule.metric)) {
        value = this.counters.get(rule.metric).get();
      } else if (this.gauges.has(rule.metric)) {
        value = this.gauges.get(rule.metric).get();
      } else if (this.histograms.has(rule.metric)) {
        value = this.histograms.get(rule.metric).p99();
      }
      
      const result = rule.evaluate(value);
      results.push(result);
      
      // Record firing alerts
      if (result.state === 'firing') {
        this.alertHistory.push({
          ...result,
          timestamp: Date.now()
        });
        
        if (this.alertHistory.length > this.maxAlertHistory) {
          this.alertHistory.shift();
        }
      }
    }
    
    return results;
  }
  
  /**
   * Get alert history
   */
  getAlertHistory(since = null) {
    const cutoff = since || Date.now() - 24 * 60 * 60 * 1000;
    return this.alertHistory.filter(a => a.timestamp >= cutoff);
  }
  
  /**
   * Export Prometheus format
   */
  exportPrometheus() {
    const lines = [];
    
    // Export counters
    for (const [key, counter] of this.counters) {
      const labels = Object.entries(counter.labels)
        .map(([k, v]) => `${k}="${v}"`)
        .join(',');
      const labelStr = labels ? `{${labels}}` : '';
      
      lines.push(`# TYPE ${this.prefix}_${counter.name} counter`);
      lines.push(`${this.prefix}_${counter.name}${labelStr} ${counter.get()}`);
    }
    
    // Export gauges
    for (const [key, gauge] of this.gauges) {
      const labels = Object.entries(gauge.labels)
        .map(([k, v]) => `${k}="${v}"`)
        .join(',');
      const labelStr = labels ? `{${labels}}` : '';
      
      lines.push(`# TYPE ${this.prefix}_${gauge.name} gauge`);
      lines.push(`${this.prefix}_${gauge.name}${labelStr} ${gauge.get()}`);
    }
    
    // Export histograms
    for (const [key, histogram] of this.histograms) {
      const stats = histogram.getStats();
      
      lines.push(`# TYPE ${this.prefix}_${key.replace(/_[^_]+$/, '')} histogram`);
      
      for (const bucket of stats.buckets) {
        lines.push(`${this.prefix}_${key.replace(/_[^_]+$/, '')}_bucket{le="${bucket.le}"} ${bucket.count}`);
      }
      lines.push(`${this.prefix}_${key.replace(/_[^_]+$/, '')}_bucket{le="+Inf"} ${stats.count}`);
      lines.push(`${this.prefix}_${key.replace(/_[^_]+$/, '')}_sum ${stats.sum}`);
      lines.push(`${this.prefix}_${key.replace(/_[^_]+$/, '')}_count ${stats.count}`);
    }
    
    return lines.join('\n');
  }
  
  /**
   * Generate Grafana dashboard
   */
  generateGrafanaDashboard(options = {}) {
    const title = options.title || `${this.serviceName} Metrics Dashboard`;
    const uid = options.uid || this.serviceName.toLowerCase().replace(/\s+/g, '-');
    
    const panels = [];
    let y = 0;
    
    // Latency panel
    panels.push({
      id: 1,
      title: 'Latency (P50, P95, P99)',
      type: 'graph',
      gridPos: { x: 0, y, w: 12, h: 8 },
      targets: [
        {
          expr: `histogram_quantile(0.50, rate(${this.prefix}_*_latency_bucket[5m]))`,
          legendFormat: 'P50',
          refId: 'A'
        },
        {
          expr: `histogram_quantile(0.95, rate(${this.prefix}_*_latency_bucket[5m]))`,
          legendFormat: 'P95',
          refId: 'B'
        },
        {
          expr: `histogram_quantile(0.99, rate(${this.prefix}_*_latency_bucket[5m]))`,
          legendFormat: 'P99',
          refId: 'C'
        }
      ],
      yaxes: [
        { format: 'ms', label: 'Latency' },
        { format: 'short' }
      ]
    });
    y += 8;
    
    // Error rate panel
    panels.push({
      id: 2,
      title: 'Error Rate',
      type: 'graph',
      gridPos: { x: 0, y, w: 12, h: 8 },
      targets: [
        {
          expr: `rate(${this.prefix}_*_errors_total[5m]) / rate(${this.prefix}_*_total[5m]) * 100`,
          legendFormat: '{{operation}}',
          refId: 'A'
        }
      ],
      yaxes: [
        { format: 'percent', label: 'Error Rate %' },
        { format: 'short' }
      ],
      alert: {
        conditions: [
          {
            evaluator: { type: 'gt', params: [5] },
            operator: { type: 'and' },
            query: { params: ['A', '5m', 'now'] },
            reducer: { type: 'avg' },
            type: 'query'
          }
        ],
        message: 'Error rate exceeds 5%',
        name: 'High Error Rate'
      }
    });
    y += 8;
    
    // Request rate panel
    panels.push({
      id: 3,
      title: 'Request Rate',
      type: 'graph',
      gridPos: { x: 0, y, w: 12, h: 8 },
      targets: [
        {
          expr: `rate(${this.prefix}_*_total[5m])`,
          legendFormat: '{{operation}}',
          refId: 'A'
        }
      ],
      yaxes: [
        { format: 'reqps', label: 'Requests/sec' },
        { format: 'short' }
      ]
    });
    y += 8;
    
    // Success rate panel
    panels.push({
      id: 4,
      title: 'Success Rate',
      type: 'gauge',
      gridPos: { x: 0, y, w: 6, h: 6 },
      targets: [
        {
          expr: `rate(${this.prefix}_*_success_total[5m]) / rate(${this.prefix}_*_total[5m]) * 100`,
          legendFormat: 'Success Rate',
          refId: 'A'
        }
      ],
      fieldConfig: {
        defaults: {
          max: 100,
          min: 0,
          unit: 'percent',
          thresholds: {
            mode: 'absolute',
            steps: [
              { color: 'red', value: 0 },
              { color: 'yellow', value: 90 },
              { color: 'green', value: 95 }
            ]
          }
        }
      }
    });
    
    return {
      dashboard: {
        title,
        uid,
        panels,
        schemaVersion: 27,
        version: 1,
        refresh: '30s'
      },
      overwrite: true
    };
  }
  
  /**
   * Get all metrics summary
   */
  getSummary() {
    const summary = {
      serviceName: this.serviceName,
      timestamp: Date.now(),
      counters: {},
      gauges: {},
      histograms: {},
      alerts: {
        rules: Array.from(this.alertRules.keys()),
        firing: this.alertHistory.filter(a => a.state === 'firing').slice(-10)
      }
    };
    
    for (const [key, counter] of this.counters) {
      summary.counters[key] = counter.get();
    }
    
    for (const [key, gauge] of this.gauges) {
      summary.gauges[key] = gauge.get();
    }
    
    for (const [key, histogram] of this.histograms) {
      summary.histograms[key] = histogram.getStats();
    }
    
    return summary;
  }
  
  /**
   * Make key for metric storage
   */
  _makeKey(name, labels = {}) {
    const labelStr = Object.entries(labels)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([k, v]) => `${k}=${v}`)
      .join(',');
    return labelStr ? `${name}{${labelStr}}` : name;
  }
}

/**
 * Anomaly Detector - Detect anomalies in metrics
 */
class AnomalyDetector {
  constructor(options = {}) {
    this.windowSize = options.windowSize || 100;
    this.zScoreThreshold = options.zScoreThreshold || 3;
    this.history = new Map(); // metric -> [values]
  }
  
  /**
   * Add value and check for anomaly
   */
  check(name, value) {
    if (!this.history.has(name)) {
      this.history.set(name, []);
    }
    
    const history = this.history.get(name);
    history.push(value);
    
    if (history.length > this.windowSize) {
      history.shift();
    }
    
    // Need at least 10 points for meaningful detection
    if (history.length < 10) {
      return { anomaly: false, reason: 'insufficient_data' };
    }
    
    // Calculate mean and std dev
    const mean = history.reduce((a, b) => a + b, 0) / history.length;
    const variance = history.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / history.length;
    const stdDev = Math.sqrt(variance);
    
    // Calculate z-score
    const zScore = stdDev > 0 ? Math.abs(value - mean) / stdDev : 0;
    
    return {
      anomaly: zScore > this.zScoreThreshold,
      zScore,
      mean,
      stdDev,
      value,
      threshold: this.zScoreThreshold,
      reason: zScore > this.zScoreThreshold ? 'z_score_exceeded' : 'normal'
    };
  }
  
  /**
   * Get baseline for a metric
   */
  getBaseline(name) {
    const history = this.history.get(name) || [];
    
    if (history.length < 10) {
      return null;
    }
    
    const mean = history.reduce((a, b) => a + b, 0) / history.length;
    const variance = history.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / history.length;
    const stdDev = Math.sqrt(variance);
    
    return {
      mean,
      stdDev,
      min: Math.min(...history),
      max: Math.max(...history),
      count: history.length
    };
  }
}

/**
 * Create metrics collector
 */
function createMetricsCollector(options) {
  return new MetricsCollector(options);
}

/**
 * Create histogram
 */
function createHistogram(options) {
  return new Histogram(options);
}

/**
 * Create counter
 */
function createCounter(name, labels) {
  return new Counter(name, labels);
}

/**
 * Create gauge
 */
function createGauge(name, labels) {
  return new Gauge(name, labels);
}

/**
 * Create alert rule
 */
function createAlertRule(options) {
  return new AlertRule(options);
}

/**
 * Create anomaly detector
 */
function createAnomalyDetector(options) {
  return new AnomalyDetector(options);
}

/**
 * Quick monitor - Create a simple monitoring setup
 */
function quickMonitor(serviceName, operations = []) {
  const collector = createMetricsCollector({ serviceName });
  
  // Add default alert rules
  collector.addAlertRule({
    name: 'high_error_rate',
    metric: 'error_rate',
    condition: 'gt',
    threshold: 0.05,
    duration: 60000,
    severity: 'warning',
    message: 'Error rate exceeds 5%'
  });
  
  collector.addAlertRule({
    name: 'high_p99_latency',
    metric: 'latency_p99',
    condition: 'gt',
    threshold: 1000,
    duration: 60000,
    severity: 'warning',
    message: 'P99 latency exceeds 1000ms'
  });
  
  return collector;
}

module.exports = {
  createMetricsCollector,
  createHistogram,
  createCounter,
  createGauge,
  createAlertRule,
  createAnomalyDetector,
  quickMonitor,
  Histogram,
  Counter,
  Gauge,
  TimeSeriesStore,
  AlertRule,
  MetricsCollector,
  AnomalyDetector
};
