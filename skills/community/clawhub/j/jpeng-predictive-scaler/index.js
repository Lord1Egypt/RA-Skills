/**
 * Predictive Scaler - Analyze resource usage and predict scaling needs
 * 
 * Features:
 * - Historical data analysis
 * - Trend detection (moving average, linear regression)
 * - Scaling recommendations with confidence levels
 * - Support for scale-up and scale-down predictions
 * - Configurable prediction horizons
 * 
 * Usage:
 *   const scaler = require('./skills/predictive-scaler');
 *   const prediction = scaler.predict(usageHistory, { horizon: 60 });
 *   console.log(prediction.recommendation);
 */

/**
 * Scaling actions
 */
const ScalingAction = {
  SCALE_UP: 'scale_up',
  SCALE_DOWN: 'scale_down',
  MAINTAIN: 'maintain',
  UNKNOWN: 'unknown'
};

/**
 * Default options
 */
const DEFAULT_OPTIONS = {
  horizon: 60,           // Prediction horizon in minutes
  minDataPoints: 5,      // Minimum data points for prediction
  scaleUpThreshold: 0.8, // CPU/Memory threshold to recommend scale-up
  scaleDownThreshold: 0.3, // CPU/Memory threshold to recommend scale-down
  confidenceThreshold: 0.7, // Minimum confidence for recommendations
  smoothingFactor: 0.3,  // Exponential smoothing factor
  windowSize: 10         // Moving average window size
};

/**
 * Calculate simple moving average
 */
function movingAverage(data, windowSize = DEFAULT_OPTIONS.windowSize) {
  if (data.length < windowSize) {
    return data.reduce((a, b) => a + b, 0) / data.length;
  }
  
  const window = data.slice(-windowSize);
  return window.reduce((a, b) => a + b, 0) / windowSize;
}

/**
 * Calculate exponential moving average
 */
function exponentialMovingAverage(data, factor = DEFAULT_OPTIONS.smoothingFactor) {
  if (data.length === 0) return 0;
  
  let ema = data[0];
  for (let i = 1; i < data.length; i++) {
    ema = factor * data[i] + (1 - factor) * ema;
  }
  return ema;
}

/**
 * Calculate linear regression
 */
function linearRegression(data) {
  const n = data.length;
  if (n < 2) return { slope: 0, intercept: data[0] || 0, r2: 0 };
  
  let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0, sumY2 = 0;
  
  for (let i = 0; i < n; i++) {
    sumX += i;
    sumY += data[i];
    sumXY += i * data[i];
    sumX2 += i * i;
    sumY2 += data[i] * data[i];
  }
  
  const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
  const intercept = (sumY - slope * sumX) / n;
  
  // Calculate R-squared
  const yMean = sumY / n;
  let ssTotal = 0, ssResidual = 0;
  
  for (let i = 0; i < n; i++) {
    const predicted = slope * i + intercept;
    ssTotal += Math.pow(data[i] - yMean, 2);
    ssResidual += Math.pow(data[i] - predicted, 2);
  }
  
  const r2 = ssTotal > 0 ? 1 - (ssResidual / ssTotal) : 0;
  
  return { slope, intercept, r2 };
}

/**
 * Predict future values using linear regression
 */
function predictLinear(data, steps) {
  const { slope, intercept, r2 } = linearRegression(data);
  const predictions = [];
  
  for (let i = 0; i < steps; i++) {
    predictions.push(intercept + slope * (data.length + i));
  }
  
  return { predictions, confidence: Math.max(0, Math.min(1, r2)) };
}

/**
 * Predict future values using exponential smoothing
 */
function predictExponential(data, steps, factor = DEFAULT_OPTIONS.smoothingFactor) {
  const ema = exponentialMovingAverage(data, factor);
  
  // Simple prediction: assume trend continues
  const trend = data.length > 1 ? (data[data.length - 1] - data[data.length - 2]) : 0;
  
  const predictions = [];
  for (let i = 0; i < steps; i++) {
    predictions.push(ema + trend * (i + 1));
  }
  
  // Confidence based on data consistency
  const variance = calculateVariance(data);
  const consistency = 1 / (1 + variance);
  
  return { predictions, confidence: consistency };
}

/**
 * Calculate variance
 */
function calculateVariance(data) {
  if (data.length === 0) return 0;
  
  const mean = data.reduce((a, b) => a + b, 0) / data.length;
  const squaredDiffs = data.map(x => Math.pow(x - mean, 2));
  return squaredDiffs.reduce((a, b) => a + b, 0) / data.length;
}

/**
 * Calculate standard deviation
 */
function calculateStdDev(data) {
  return Math.sqrt(calculateVariance(data));
}

/**
 * Detect trend direction
 */
function detectTrend(data) {
  if (data.length < 3) return 'stable';
  
  const { slope, r2 } = linearRegression(data);
  const threshold = 0.01; // 1% change per data point
  
  if (r2 < 0.3) return 'volatile';
  
  if (slope > threshold) return 'increasing';
  if (slope < -threshold) return 'decreasing';
  return 'stable';
}

/**
 * Detect bursty patterns
 */
function detectBurstyPattern(data) {
  if (data.length < 5) return { isBursty: false, burstFactor: 0 };
  
  const mean = data.reduce((a, b) => a + b, 0) / data.length;
  const stdDev = calculateStdDev(data);
  const coefficientOfVariation = mean > 0 ? stdDev / mean : 0;
  
  // Check for sudden spikes
  const spikes = data.filter(x => x > mean + 2 * stdDev).length;
  const spikeRatio = spikes / data.length;
  
  return {
    isBursty: coefficientOfVariation > 0.5 || spikeRatio > 0.1,
    burstFactor: coefficientOfVariation,
    spikeRatio,
    mean,
    stdDev
  };
}

/**
 * Generate scaling recommendation
 */
function generateRecommendation(current, predicted, options) {
  const { scaleUpThreshold, scaleDownThreshold, confidenceThreshold } = options;
  
  const avgPredicted = predicted.reduce((a, b) => a + b, 0) / predicted.length;
  const maxPredicted = Math.max(...predicted);
  const minPredicted = Math.min(...predicted);
  
  // Determine action
  let action = ScalingAction.MAINTAIN;
  let reason = '';
  
  if (maxPredicted > scaleUpThreshold) {
    action = ScalingAction.SCALE_UP;
    reason = `Predicted peak ${maxPredicted.toFixed(2)} exceeds threshold ${scaleUpThreshold}`;
  } else if (minPredicted < scaleDownThreshold && avgPredicted < scaleDownThreshold) {
    action = ScalingAction.SCALE_DOWN;
    reason = `Predicted average ${avgPredicted.toFixed(2)} below threshold ${scaleDownThreshold}`;
  } else {
    reason = `Predicted values within normal range (${minPredicted.toFixed(2)} - ${maxPredicted.toFixed(2)})`;
  }
  
  return {
    action,
    reason,
    current,
    predicted: {
      average: avgPredicted,
      max: maxPredicted,
      min: minPredicted
    },
    thresholds: {
      scaleUp: scaleUpThreshold,
      scaleDown: scaleDownThreshold
    }
  };
}

/**
 * Main prediction function
 */
function predict(data, options = {}) {
  const opts = { ...DEFAULT_OPTIONS, ...options };
  
  // Validate input
  if (!data || !Array.isArray(data) || data.length === 0) {
    return {
      error: 'Invalid input: data must be a non-empty array',
      recommendation: {
        action: ScalingAction.UNKNOWN,
        reason: 'Insufficient data for prediction'
      }
    };
  }
  
  // Normalize data to 0-1 range if needed
  const normalizedData = data.map(x => Math.max(0, Math.min(1, x)));
  
  // Check minimum data points
  if (normalizedData.length < opts.minDataPoints) {
    return {
      error: `Insufficient data: need at least ${opts.minDataPoints} points, got ${normalizedData.length}`,
      recommendation: {
        action: ScalingAction.UNKNOWN,
        reason: 'Need more historical data'
      }
    };
  }
  
  // Calculate predictions using multiple methods
  const linearResult = predictLinear(normalizedData, opts.horizon);
  const expResult = predictExponential(normalizedData, opts.horizon, opts.smoothingFactor);
  
  // Combine predictions (weighted average)
  const combinedPredictions = linearResult.predictions.map((val, i) => {
    const expVal = expResult.predictions[i] || val;
    const linearWeight = linearResult.confidence;
    const expWeight = expResult.confidence;
    const totalWeight = linearWeight + expWeight;
    
    return totalWeight > 0 ? (val * linearWeight + expVal * expWeight) / totalWeight : (val + expVal) / 2;
  });
  
  // Overall confidence
  const confidence = (linearResult.confidence + expResult.confidence) / 2;
  
  // Detect patterns
  const trend = detectTrend(normalizedData);
  const bursty = detectBurstyPattern(normalizedData);
  
  // Generate recommendation
  const current = normalizedData[normalizedData.length - 1];
  const recommendation = generateRecommendation(current, combinedPredictions, opts);
  
  // Adjust confidence based on patterns
  let adjustedConfidence = confidence;
  if (bursty.isBursty) {
    adjustedConfidence *= 0.7; // Lower confidence for bursty patterns
    recommendation.note = 'Bursty pattern detected - predictions may be less reliable';
  }
  
  // Check if confidence is too low
  if (adjustedConfidence < opts.confidenceThreshold) {
    recommendation.action = ScalingAction.MAINTAIN;
    recommendation.reason += ' (Low confidence prediction)';
  }
  
  return {
    predictions: combinedPredictions,
    confidence: adjustedConfidence,
    trend,
    bursty,
    recommendation,
    methods: {
      linear: linearResult,
      exponential: expResult
    },
    statistics: {
      mean: normalizedData.reduce((a, b) => a + b, 0) / normalizedData.length,
      stdDev: calculateStdDev(normalizedData),
      min: Math.min(...normalizedData),
      max: Math.max(...normalizedData),
      dataPoints: normalizedData.length
    }
  };
}

/**
 * Predict for multiple resources
 */
function predictMulti(resources, options = {}) {
  const results = {};
  
  for (const [name, data] of Object.entries(resources)) {
    results[name] = predict(data, options);
  }
  
  // Generate combined recommendation
  const actions = Object.values(results).map(r => r.recommendation?.action);
  const scaleUpCount = actions.filter(a => a === ScalingAction.SCALE_UP).length;
  const scaleDownCount = actions.filter(a => a === ScalingAction.SCALE_DOWN).length;
  
  let combinedAction = ScalingAction.MAINTAIN;
  if (scaleUpCount > 0) {
    combinedAction = ScalingAction.SCALE_UP;
  } else if (scaleDownCount === actions.length) {
    combinedAction = ScalingAction.SCALE_DOWN;
  }
  
  return {
    resources: results,
    combinedRecommendation: {
      action: combinedAction,
      scaleUpCount,
      scaleDownCount,
      maintainCount: actions.filter(a => a === ScalingAction.MAINTAIN).length
    }
  };
}

/**
 * Calculate capacity needed
 */
function calculateCapacityNeeded(currentCapacity, predictedLoad, targetUtilization = 0.7) {
  if (targetUtilization <= 0) targetUtilization = 0.7;
  
  const neededCapacity = predictedLoad / targetUtilization;
  const change = neededCapacity - currentCapacity;
  const changePercent = currentCapacity > 0 ? (change / currentCapacity) * 100 : 0;
  
  return {
    current: currentCapacity,
    needed: Math.ceil(neededCapacity),
    change: Math.round(change * 100) / 100,
    changePercent: Math.round(changePercent * 100) / 100,
    action: change > 0 ? ScalingAction.SCALE_UP : (change < 0 ? ScalingAction.SCALE_DOWN : ScalingAction.MAINTAIN)
  };
}

/**
 * Analyze scaling history
 */
function analyzeScalingHistory(events) {
  if (!events || events.length === 0) {
    return { averageInterval: 0, scaleUpFrequency: 0, scaleDownFrequency: 0 };
  }
  
  const scaleUps = events.filter(e => e.action === ScalingAction.SCALE_UP);
  const scaleDowns = events.filter(e => e.action === ScalingAction.SCALE_DOWN);
  
  // Calculate average time between events
  const intervals = [];
  for (let i = 1; i < events.length; i++) {
    if (events[i].timestamp && events[i-1].timestamp) {
      intervals.push(events[i].timestamp - events[i-1].timestamp);
    }
  }
  
  const averageInterval = intervals.length > 0 
    ? intervals.reduce((a, b) => a + b, 0) / intervals.length 
    : 0;
  
  return {
    totalEvents: events.length,
    scaleUpCount: scaleUps.length,
    scaleDownCount: scaleDowns.length,
    scaleUpFrequency: events.length > 0 ? scaleUps.length / events.length : 0,
    scaleDownFrequency: events.length > 0 ? scaleDowns.length / events.length : 0,
    averageInterval,
    lastEvent: events[events.length - 1]
  };
}

/**
 * Get prediction statistics
 */
function getPredictionStats(result) {
  if (!result || result.error) {
    return null;
  }
  
  return {
    confidence: result.confidence,
    trend: result.trend,
    isBursty: result.bursty?.isBursty || false,
    action: result.recommendation?.action,
    predictedRange: {
      min: Math.min(...result.predictions),
      max: Math.max(...result.predictions)
    },
    dataPoints: result.statistics?.dataPoints
  };
}

module.exports = {
  predict,
  predictMulti,
  predictLinear,
  predictExponential,
  movingAverage,
  exponentialMovingAverage,
  linearRegression,
  detectTrend,
  detectBurstyPattern,
  generateRecommendation,
  calculateCapacityNeeded,
  analyzeScalingHistory,
  getPredictionStats,
  calculateVariance,
  calculateStdDev,
  ScalingAction,
  DEFAULT_OPTIONS
};
