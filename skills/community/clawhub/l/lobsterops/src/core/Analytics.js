/**
 * Analytics - Behavioral analytics for AI agent event traces
 *
 * Detects patterns, loops, failure points, and provides
 * performance metrics from agent event data.
 */
class Analytics {
  /**
   * Analyze an array of events and return a full behavioral report
   * @param {Array} events - Events to analyze
   * @returns {Object} - Behavioral analytics report
   */
  static analyze(events) {
    if (!events || events.length === 0) {
      return {
        totalEvents: 0,
        successRate: null,
        eventTypeBreakdown: {},
        agentBreakdown: {},
        performanceMetrics: {},
        loopsDetected: [],
        failurePatterns: [],
      };
    }

    return {
      totalEvents: events.length,
      eventTypeBreakdown: Analytics.eventTypeBreakdown(events),
      agentBreakdown: Analytics.agentBreakdown(events),
      successRate: Analytics.successRate(events),
      performanceMetrics: Analytics.performanceMetrics(events),
      loopsDetected: Analytics.detectLoops(events),
      failurePatterns: Analytics.failurePatterns(events),
      costAnalysis: Analytics.costAnalysis(events),
    };
  }

  /**
   * Break down events by type
   * @param {Array} events
   * @returns {Object} - Count per event type
   */
  static eventTypeBreakdown(events) {
    const breakdown = {};
    for (const event of events) {
      breakdown[event.type] = (breakdown[event.type] || 0) + 1;
    }
    return breakdown;
  }

  /**
   * Break down events by agent
   * @param {Array} events
   * @returns {Object} - Per-agent statistics
   */
  static agentBreakdown(events) {
    const agents = {};
    for (const event of events) {
      const agentId = event.agentId || 'unknown';
      if (!agents[agentId]) {
        agents[agentId] = { eventCount: 0, types: {}, errors: 0 };
      }
      agents[agentId].eventCount++;
      agents[agentId].types[event.type] = (agents[agentId].types[event.type] || 0) + 1;
      if (event.type === 'agent-error') agents[agentId].errors++;
    }
    return agents;
  }

  /**
   * Calculate success rate from tool calls and decisions
   * @param {Array} events
   * @returns {Object} - Success rate metrics
   */
  static successRate(events) {
    const toolCalls = events.filter(e => e.type === 'tool-call');
    const successful = toolCalls.filter(e => e.success === true);
    const failed = toolCalls.filter(e => e.success === false);

    return {
      totalToolCalls: toolCalls.length,
      successful: successful.length,
      failed: failed.length,
      rate: toolCalls.length > 0
        ? Math.round((successful.length / toolCalls.length) * 10000) / 100
        : null,
    };
  }

  /**
   * Calculate performance metrics (latency, cost, throughput)
   * @param {Array} events
   * @returns {Object} - Performance metrics
   */
  static performanceMetrics(events) {
    const durations = events
      .filter(e => typeof e.durationMs === 'number')
      .map(e => e.durationMs);

    if (durations.length === 0) {
      return { avgDurationMs: null, minDurationMs: null, maxDurationMs: null, p95DurationMs: null };
    }

    durations.sort((a, b) => a - b);

    const sum = durations.reduce((a, b) => a + b, 0);
    const p95Index = Math.floor(durations.length * 0.95);

    return {
      avgDurationMs: Math.round(sum / durations.length),
      minDurationMs: durations[0],
      maxDurationMs: durations[durations.length - 1],
      medianDurationMs: durations[Math.floor(durations.length / 2)],
      p95DurationMs: durations[Math.min(p95Index, durations.length - 1)],
      totalMeasured: durations.length,
    };
  }

  /**
   * Detect repeating event patterns that may indicate loops or stuck states
   * @param {Array} events
   * @param {Object} options
   * @param {number} options.minRepetitions - Minimum repetitions to flag (default: 3)
   * @param {number} options.windowSize - Window size to check for patterns (default: 5)
   * @returns {Array} - Detected loop patterns
   */
  static detectLoops(events, options = {}) {
    const minRepetitions = options.minRepetitions || 3;
    const windowSize = options.windowSize || 5;
    const loops = [];

    if (events.length < minRepetitions * 2) return loops;

    // Check for repeating sequences of types
    const types = events.map(e => e.type);

    for (let patternLen = 1; patternLen <= windowSize; patternLen++) {
      for (let i = 0; i <= types.length - patternLen * minRepetitions; i++) {
        const pattern = types.slice(i, i + patternLen);
        let repetitions = 1;

        for (let j = i + patternLen; j <= types.length - patternLen; j += patternLen) {
          const segment = types.slice(j, j + patternLen);
          if (JSON.stringify(segment) === JSON.stringify(pattern)) {
            repetitions++;
          } else {
            break;
          }
        }

        if (repetitions >= minRepetitions) {
          const existing = loops.find(l =>
            JSON.stringify(l.pattern) === JSON.stringify(pattern) && l.startIndex === i
          );
          if (!existing) {
            loops.push({
              pattern,
              repetitions,
              startIndex: i,
              endIndex: i + patternLen * repetitions - 1,
            });
          }
        }
      }
    }

    return loops;
  }

  /**
   * Identify failure patterns and common error sequences
   * @param {Array} events
   * @returns {Array} - Failure patterns
   */
  static failurePatterns(events) {
    const errors = events.filter(e => e.type === 'agent-error');
    if (errors.length === 0) return [];

    // Group errors by type
    const errorGroups = {};
    for (const error of errors) {
      const key = error.errorType || error.errorMessage || 'unknown';
      if (!errorGroups[key]) {
        errorGroups[key] = { type: key, count: 0, occurrences: [] };
      }
      errorGroups[key].count++;
      errorGroups[key].occurrences.push({
        timestamp: error.timestamp,
        agentId: error.agentId,
        severity: error.severity,
        recovered: error.recovered,
      });
    }

    return Object.values(errorGroups).sort((a, b) => b.count - a.count);
  }

  /**
   * Analyze cost data across events
   * @param {Array} events
   * @returns {Object} - Cost analysis
   */
  static costAnalysis(events) {
    const withCost = events.filter(e => typeof e.cost === 'number');
    if (withCost.length === 0) {
      return { totalCost: 0, avgCost: null, maxCost: null, eventCount: 0 };
    }

    const costs = withCost.map(e => e.cost);
    const total = costs.reduce((a, b) => a + b, 0);

    // Group by agent
    const costByAgent = {};
    for (const event of withCost) {
      const agent = event.agentId || 'unknown';
      costByAgent[agent] = (costByAgent[agent] || 0) + event.cost;
    }

    return {
      totalCost: Math.round(total * 10000) / 10000,
      avgCost: Math.round((total / costs.length) * 10000) / 10000,
      maxCost: Math.max(...costs),
      eventCount: withCost.length,
      costByAgent,
    };
  }
}

module.exports = { Analytics };
