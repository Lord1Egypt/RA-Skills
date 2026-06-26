---
name: predictive-scaler
description: Analyze resource usage patterns and predict future scaling needs using trend analysis and forecasting methods for capacity planning and auto-scaling decisions.
---

# Predictive Scaler

Analyze resource usage patterns and predict future scaling needs.

## When to Use

- Capacity planning and resource forecasting
- Auto-scaling decision support
- Predicting CPU, memory, or request load
- Analyzing bursty traffic patterns
- Generating scaling recommendations

## Usage

```javascript
const scaler = require('./skills/predictive-scaler');

// Basic prediction
const prediction = scaler.predict(cpuHistory, {
  horizon: 60,  // Predict 60 minutes ahead
  scaleUpThreshold: 0.8,
  scaleDownThreshold: 0.3
});

console.log(prediction.recommendation);
// { action: 'scale_up', reason: 'Predicted peak 0.85 exceeds threshold 0.8' }
```

## API

### `predict(data, options)`

Predict future resource usage and generate scaling recommendation.

```javascript
const result = scaler.predict(usageData, {
  horizon: 60,              // Prediction horizon in minutes
  minDataPoints: 5,         // Minimum data points needed
  scaleUpThreshold: 0.8,    // Threshold to recommend scale-up
  scaleDownThreshold: 0.3,  // Threshold to recommend scale-down
  confidenceThreshold: 0.7, // Minimum confidence for recommendations
  smoothingFactor: 0.3,     // Exponential smoothing factor
  windowSize: 10            // Moving average window
});
```

### `predictMulti(resources, options)`

Predict for multiple resources at once.

```javascript
const result = scaler.predictMulti({
  cpu: cpuHistory,
  memory: memoryHistory,
  requests: requestHistory
});

console.log(result.combinedRecommendation);
// { action: 'scale_up', scaleUpCount: 1, scaleDownCount: 0 }
```

### `predictLinear(data, steps)`

Predict using linear regression.

```javascript
const { predictions, confidence } = scaler.predictLinear(data, 10);
```

### `predictExponential(data, steps, factor)`

Predict using exponential smoothing.

```javascript
const { predictions, confidence } = scaler.predictExponential(data, 10, 0.3);
```

### `detectTrend(data)`

Detect trend direction in data.

```javascript
const trend = scaler.detectTrend(data);
// 'increasing' | 'decreasing' | 'stable' | 'volatile'
```

### `detectBurstyPattern(data)`

Detect bursty traffic patterns.

```javascript
const bursty = scaler.detectBurstyPattern(data);
// { isBursty: true, burstFactor: 0.6, spikeRatio: 0.15 }
```

### `calculateCapacityNeeded(current, predicted, targetUtilization)`

Calculate capacity needed to handle predicted load.

```javascript
const capacity = scaler.calculateCapacityNeeded(10, 8.5, 0.7);
// { current: 10, needed: 13, change: 3, changePercent: 30 }
```

### `analyzeScalingHistory(events)`

Analyze historical scaling events.

```javascript
const analysis = scaler.analyzeScalingHistory(scalingEvents);
// { scaleUpFrequency: 0.3, averageInterval: 3600000 }
```

## Output Structure

```javascript
{
  predictions: [0.65, 0.68, 0.72, ...],  // Predicted values
  confidence: 0.85,                       // Prediction confidence
  trend: 'increasing',                    // Trend direction
  bursty: {
    isBursty: false,
    burstFactor: 0.2
  },
  recommendation: {
    action: 'scale_up',                   // 'scale_up' | 'scale_down' | 'maintain'
    reason: 'Predicted peak 0.85 exceeds threshold 0.8',
    current: 0.72,
    predicted: { average: 0.78, max: 0.85, min: 0.70 }
  },
  statistics: {
    mean: 0.65,
    stdDev: 0.1,
    min: 0.45,
    max: 0.82,
    dataPoints: 30
  }
}
```

## Scaling Actions

| Action | Description |
|--------|-------------|
| `scale_up` | Resource predicted to exceed scale-up threshold |
| `scale_down` | Resource predicted below scale-down threshold |
| `maintain` | Resource within normal range |
| `unknown` | Insufficient data or error |

## Examples

### Basic Scaling Prediction

```javascript
const scaler = require('./skills/predictive-scaler');

// CPU usage history (0-1 normalized)
const cpuHistory = [0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.72, 0.75, 0.78];

const prediction = scaler.predict(cpuHistory, {
  horizon: 30,
  scaleUpThreshold: 0.8
});

if (prediction.recommendation.action === 'scale_up') {
  console.log('Scale up recommended:', prediction.recommendation.reason);
}
```

### Multi-Resource Prediction

```javascript
const scaler = require('./skills/predictive-scaler');

const resources = {
  cpu: [0.5, 0.55, 0.6, 0.65, 0.7],
  memory: [0.3, 0.32, 0.35, 0.38, 0.4],
  requests: [100, 120, 150, 180, 200]
};

const result = scaler.predictMulti(resources, { horizon: 60 });

console.log('CPU:', result.resources.cpu.recommendation.action);
console.log('Memory:', result.resources.memory.recommendation.action);
console.log('Combined:', result.combinedRecommendation.action);
```

### Trend Analysis

```javascript
const scaler = require('./skills/predictive-scaler');

const usageData = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6];

const trend = scaler.detectTrend(usageData);
console.log('Trend:', trend); // 'increasing'

const bursty = scaler.detectBurstyPattern(usageData);
console.log('Bursty:', bursty.isBursty); // false
```

### Capacity Planning

```javascript
const scaler = require('./skills/predictive-scaler');

const prediction = scaler.predict(cpuHistory, { horizon: 60 });
const predictedLoad = prediction.predictions[prediction.predictions.length - 1];

const capacity = scaler.calculateCapacityNeeded(
  10,              // Current capacity (instances)
  predictedLoad,   // Predicted load
  0.7              // Target utilization
);

console.log(`Need ${capacity.needed} instances (${capacity.changePercent}% change)`);
```

### Scaling History Analysis

```javascript
const scaler = require('./skills/predictive-scaler');

const scalingEvents = [
  { action: 'scale_up', timestamp: Date.now() - 3600000 },
  { action: 'scale_down', timestamp: Date.now() - 1800000 },
  { action: 'scale_up', timestamp: Date.now() }
];

const analysis = scaler.analyzeScalingHistory(scalingEvents);
console.log('Scale-up frequency:', analysis.scaleUpFrequency);
console.log('Average interval:', analysis.averageInterval, 'ms');
```

## Prediction Methods

### Linear Regression
- Best for: Steady growth/decline patterns
- Output: Trend line with confidence (R²)
- Use when: Data shows clear linear trend

### Exponential Smoothing
- Best for: Recent data more important than old
- Output: Smoothed predictions
- Use when: Recent trends are more relevant

### Combined Prediction
- Default: Weighted average of both methods
- Weights: Based on each method's confidence
- More robust than single method

## Best Practices

1. **Minimum data points**: Use at least 10-15 data points for reliable predictions
2. **Normalize data**: Input should be 0-1 range (CPU%, memory%, etc.)
3. **Set appropriate thresholds**: Scale-up at 80%, scale-down at 30% is typical
4. **Consider bursty patterns**: Lower confidence for highly variable data
5. **Combine with cooldown**: Don't scale too frequently based on predictions
6. **Validate predictions**: Compare predictions with actual values over time

## Notes

- Predictions are statistical estimates, not guarantees
- Confidence decreases with prediction horizon
- Bursty patterns reduce prediction reliability
- Multiple resources can be analyzed together
- Historical scaling events inform future decisions
