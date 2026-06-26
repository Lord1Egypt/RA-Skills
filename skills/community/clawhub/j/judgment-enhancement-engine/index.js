/**
 * Judgment Enhancement Engine — pure Node.js info module
 * Pure Python engine. This file provides metadata only.
 */
const path = require('path');

function info() {
  return {
    name: 'judgment-enhancement-engine',
    version: '1.1',
    description: 'AI Agent judgment enhancement via lookahead simulation, risk-adjusted utility, historical reflection',
    language: 'Python 3',
    dependencies: 'none (stdlib only)',
    features: [
      'Monte Carlo lookahead with depth/breadth control',
      'Risk-adjusted utility (VaR95-aware)',
      'Greedy rollout / uniform sampling dual mode',
      'Historical outcome reflection with negative correction',
      'Configurable risk tolerance (0=averse, 1=neutral)',
      'Timeout protection (max_compute_time_sec)',
      'State-action history with automatic pruning'
    ],
    usage: `from engine import JudgmentEnhancementEngine, JudgmentResult
engine = JudgmentEnhancementEngine(world_model, objective, ...)
result = engine.enhance_judgment(state)`,
    run: 'python engine.py',
    test: 'python scripts/test-basic.py'
  };
}

module.exports = { info };
