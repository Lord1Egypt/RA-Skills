---
name: agent-metrics-monitor
description: Provides monitoring and alerting for agent abnormal behavior metrics with Prometheus and Grafana support, including P99 latency, error rates, anomaly detection, and custom alert rules.
---

# Agent Metrics Monitor

Monitor and alert agent abnormal behavior metrics with Prometheus and Grafana support.

## When to Use

- Monitoring agent operation latencies (P50, P95, P99)
- Tracking error rates and success rates
- Detecting anomalies in agent behavior
- Generating Prometheus-compatible metrics
- Creating Grafana dashboard configurations
- Setting up alert rules for abnormal behavior

## Usage

```javascript
const monitor = require('./skills/agent-metrics-monitor');

// Create metrics collector
const collector = monitor.createMetricsCollector({ serviceName: 'my-agent' });

// Record latency
collector.recordLatency('tool_call', 150);
collector.recordLatency('tool_call', 250);

// Record errors and successes
collector.recordError('tool_call', 'timeout');
collector.recordSuccess('tool_call');

// Get error rate
console.log('Error rate:', collector.getErrorRate('tool_call'));

// Export Prometheus format
console.log(collector.exportPrometheus());

// Generate Grafana dashboard
const dashboard = collector.generateGrafanaDashboard({ title: 'My Agent' });
```

## API

### `createMetricsCollector(options)`

Create a metrics collector instance.

```javascript
const collector = monitor.createMetricsCollector({
  serviceName: 'my-agent',
  prefix: 'agent',
  timeSeries: {
    maxPoints: 10000,
    retentionMs: 86400000 // 24 hours
  }
});
```

### `createHistogram(options)`

Create a histogram for latency tracking.

```javascript
const hist = monitor.createHistogram({
  buckets: [1, 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000],
  maxValues: 10000
});

hist.observe(150);
console.log('P99:', hist.p99());
console.log('P95:', hist.p95());
console.log('P50:', hist.p50());
```

### `createCounter(name, labels)`

Create a counter for tracking occurrences.

```javascript
const counter = monitor.createCounter('requests_total', { service: 'api' });
counter.inc();
counter.inc(5);
console.log(counter.get()); // 6
```

### `createGauge(name, labels)`

Create a gauge for point-in-time values.

```javascript
const gauge = monitor.createGauge('active_connections', { host: 'localhost' });
gauge.set(10);
gauge.inc();
gauge.dec();
console.log(gauge.get()); // 10
```

### `createAlertRule(options)`

Create an alert rule.

```javascript
const rule = monitor.createAlertRule({
  name: 'high_error_rate',
  metric: 'error_rate',
  condition: 'gt', // 'gt', 'lt', 'eq', 'gte', 'lte'
  threshold: 0.05,
  duration: 60000, // 1 minute
  severity: 'warning', // 'info', 'warning', 'critical'
  message: 'Error rate exceeds 5%'
});
```

### `createAnomalyDetector(options)`

Create an anomaly detector.

```javascript
const detector = monitor.createAnomalyDetector({
  windowSize: 100,
  zScoreThreshold: 3
});

const result = detector.check('latency', 500);
console.log(result.anomaly); // true/false
console.log(result.zScore); // z-score value
```

### `quickMonitor(serviceName, operations)`

Create a simple monitoring setup with default alert rules.

```javascript
const collector = monitor.quickMonitor('my-agent');
// Pre-configured with high_error_rate and high_p99_latency alerts
```

## Classes

### Histogram

Track latency percentiles.

```javascript
const hist = new monitor.Histogram({ buckets: [10, 50, 100, 500, 1000] });

hist.observe(150);
hist.observe(250);
hist.observe(350);

const stats = hist.getStats();
// {
//   count: 3,
//   sum: 750,
//   mean: 250,
//   p50: 250,
//   p95: 350,
//   p99: 350,
//   buckets: [...]
// }
```

### Counter

Monotonically increasing value.

```javascript
const counter = new monitor.Counter('requests', { service: 'api' });
counter.inc();
counter.inc(10);
console.log(counter.get()); // 11
counter.reset();
console.log(counter.get()); // 0
```

### Gauge

Point-in-time value.

```javascript
const gauge = new monitor.Gauge('temperature');
gauge.set(25);
gauge.inc(2);
gauge.dec(1);
console.log(gauge.get()); // 26
```

### AlertRule

Define alert conditions.

```javascript
const rule = new monitor.AlertRule({
  name: 'high_latency',
  metric: 'latency_p99',
  condition: 'gt',
  threshold: 1000,
  duration: 60000,
  severity: 'warning',
  message: 'P99 latency exceeds 1 second'
});

const result = rule.evaluate(1500);
// {
//   name: 'high_latency',
//   state: 'firing', // 'inactive', 'pending', 'firing'
//   value: 1500,
//   threshold: 1000,
//   severity: 'warning',
//   message: 'P99 latency exceeds 1 second'
// }
```

### MetricsCollector

Collect and aggregate metrics.

```javascript
const collector = new monitor.MetricsCollector({ serviceName: 'agent' });

// Record operations
collector.recordLatency('tool_call', 150);
collector.recordError('tool_call', 'timeout');
collector.recordSuccess('tool_call');

// Get rates
const errorRate = collector.getErrorRate('tool_call');
const successRate = collector.getSuccessRate('tool_call');

// Add alert rules
collector.addAlertRule({
  name: 'high_error_rate',
  metric: 'tool_call_errors_total',
  condition: 'gt',
  threshold: 10,
  severity: 'warning'
});

// Evaluate alerts
const alerts = collector.evaluateAlerts();

// Export Prometheus format
const prometheus = collector.exportPrometheus();

// Generate Grafana dashboard
const dashboard = collector.generateGrafanaDashboard();

// Get summary
const summary = collector.getSummary();
```

### AnomalyDetector

Detect anomalies using z-score.

```javascript
const detector = new monitor.AnomalyDetector({
  windowSize: 100,
  zScoreThreshold: 3
});

// Feed values
for (let i = 0; i < 50; i++) {
  detector.check('latency', 100 + Math.random() * 50);
}

// Check for anomaly
const result = detector.check('latency', 500); // Unusual value
console.log(result.anomaly); // true if z-score > 3

// Get baseline
const baseline = detector.getBaseline('latency');
// { mean: 125, stdDev: 14.4, min: 100, max: 150, count: 51 }
```

## Example: Complete Monitoring Setup

```javascript
const monitor = require('./skills/agent-metrics-monitor');

// Create collector
const collector = monitor.createMetricsCollector({
  serviceName: 'production-agent',
  prefix: 'agent'
});

// Add alert rules
collector.addAlertRule({
  name: 'high_p99_latency',
  metric: 'tool_call_latency',
  condition: 'gt',
  threshold: 2000,
  duration: 60000,
  severity: 'critical',
  message: 'P99 latency exceeds 2 seconds'
});

collector.addAlertRule({
  name: 'high_error_rate',
  metric: 'tool_call_errors_total',
  condition: 'gt',
  threshold: 100,
  duration: 300000, // 5 minutes
  severity: 'warning',
  message: 'More than 100 errors in 5 minutes'
});

// Simulate operations
const operations = ['tool_call', 'llm_request', 'memory_access'];

for (let i = 0; i < 100; i++) {
  const op = operations[i % 3];
  const latency = 50 + Math.random() * 200;
  
  collector.recordLatency(op, latency);
  
  if (Math.random() < 0.05) {
    collector.recordError(op, 'timeout');
  } else {
    collector.recordSuccess(op);
  }
}

// Get metrics
console.log('Tool call error rate:', collector.getErrorRate('tool_call'));
console.log('LLM request P99:', collector.histogram('llm_request_latency').p99());

// Evaluate alerts
const alerts = collector.evaluateAlerts();
for (const alert of alerts) {
  if (alert.state === 'firing') {
    console.log(`ALERT: ${alert.name} - ${alert.message}`);
  }
}

// Export Prometheus format
console.log('\n--- Prometheus Metrics ---');
console.log(collector.exportPrometheus());

// Generate Grafana dashboard
const dashboard = collector.generateGrafanaDashboard({
  title: 'Production Agent Dashboard'
});
console.log('\n--- Grafana Dashboard ---');
console.log(JSON.stringify(dashboard, null, 2));
```

## Example: Anomaly Detection

```javascript
const monitor = require('./skills/agent-metrics-monitor');

const collector = monitor.createMetricsCollector({ serviceName: 'agent' });
const detector = monitor.createAnomalyDetector({ zScoreThreshold: 2.5 });

// Train with normal values
console.log('Training with normal values...');
for (let i = 0; i < 100; i++) {
  const latency = 100 + Math.random() * 50; // 100-150ms
  collector.recordLatency('api_call', latency);
  detector.check('api_call_latency', latency);
}

// Get baseline
const baseline = detector.getBaseline('api_call_latency');
console.log('Baseline:', baseline);

// Test with anomalies
console.log('\nTesting for anomalies...');
const testValues = [120, 135, 500, 1000, 125];

for (const value of testValues) {
  const result = detector.check('api_call_latency', value);
  console.log(`Value: ${value}ms, Anomaly: ${result.anomaly}, Z-Score: ${result.zScore?.toFixed(2)}`);
}
```

## Example: Prometheus Export

```javascript
const monitor = require('./skills/agent-metrics-monitor');

const collector = monitor.createMetricsCollector({
  serviceName: 'my-agent',
  prefix: 'agent'
});

// Record some metrics
collector.recordLatency('tool_call', 150);
collector.recordLatency('tool_call', 250);
collector.recordError('tool_call', 'timeout');
collector.recordSuccess('tool_call');

const gauge = collector.gauge('active_sessions', { region: 'us-east' });
gauge.set(42);

// Export Prometheus format
const prometheus = collector.exportPrometheus();
console.log(prometheus);

// Output:
// # TYPE agent_tool_call_errors_total counter
// agent_tool_call_errors_total{error_type="timeout"} 1
// # TYPE agent_tool_call_success_total counter
// agent_tool_call_success_total 1
// # TYPE agent_tool_call_total counter
// agent_tool_call_total 2
// # TYPE agent_active_sessions gauge
// agent_active_sessions{region="us-east"} 42
// # TYPE agent_tool_call_latency histogram
// agent_tool_call_latency_bucket{le="1"} 0
// ...
```

## Example: Grafana Dashboard Generation

```javascript
const monitor = require('./skills/agent-metrics-monitor');

const collector = monitor.createMetricsCollector({ serviceName: 'api-agent' });

// Generate dashboard configuration
const dashboard = collector.generateGrafanaDashboard({
  title: 'API Agent Metrics',
  uid: 'api-agent-metrics'
});

// Save to file for Grafana provisioning
const fs = require('fs');
fs.writeFileSync('grafana-dashboard.json', JSON.stringify(dashboard, null, 2));

console.log('Dashboard generated with panels:');
for (const panel of dashboard.dashboard.panels) {
  console.log(`  - ${panel.title} (${panel.type})`);
}
```

## Alert Rule Conditions

- `gt` - Greater than
- `lt` - Less than
- `eq` - Equal to
- `gte` - Greater than or equal
- `lte` - Less than or equal

## Alert Severities

- `info` - Informational
- `warning` - Warning condition
- `critical` - Critical condition requiring immediate attention

## Notes

- Histograms use bucket-based storage for Prometheus compatibility
- Percentiles are calculated from stored values for accuracy
- Time series data has configurable retention
- Anomaly detection uses z-score method
- Grafana dashboards are generated in JSON format for provisioning
- Prometheus export follows standard exposition format
