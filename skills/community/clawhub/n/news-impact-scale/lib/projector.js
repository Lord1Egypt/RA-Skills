/**
 * projector.js — Build prev/current/future timeline for each affected system.
 * Grounded in historical benchmark data.
 */

const TREND_MAP = {
  fast:     '🟢 Improving — fast recovery expected',
  moderate: '🟢 Improving — gradual recovery underway',
  slow:     '🟡 Stable — long-term recovery expected',
  stalled:  '🔴 Worsening — stalled recovery or compound risks',
  unknown:  '🟡 Stable — insufficient data to determine trend',
};

function projectSystem(system, benchmarkCases, eventType) {
  if (!benchmarkCases || benchmarkCases.length === 0) {
    return {
      previousState:  'Normal operational state prior to event',
      currentState:   'Disrupted',
      futureState:    'Cannot project — no comparable historical data available',
      confidence:     'Low',
      benchmarkSource: 'No precedent found; projection based on general patterns only',
      trend:          TREND_MAP.unknown,
    };
  }

  const best  = benchmarkCases[0]; // most recent/relevant case
  const count = benchmarkCases.length;
  const confidence = count >= 3 ? 'High' : 'Medium';

  return {
    previousState:  best.previousState || 'Normal operational state',
    currentState:   'Disrupted as of event date',
    futureState:    best.futureState || best.recoveryDescription || `System expected to recover within ${best.recoveryDays || 'an unknown'} day(s)`,
    confidence,
    benchmarkSource: `Based on ${count} similar event(s) in this location: ${best.description || best.event} (${best.year || 'recent'})`,
    trend: TREND_MAP[best.recoverySpeed] || TREND_MAP.moderate,
  };
}

function projectAll(affectedSystems, benchmarkCases, eventType) {
  return affectedSystems.map(system => ({
    system,
    ...projectSystem(system, benchmarkCases, eventType),
  }));
}

module.exports = { projectAll };
