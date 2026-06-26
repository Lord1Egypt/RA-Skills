---
name: evolution-predictor
description: Predict optimal next evolution actions based on history analysis, including stagnation detection, innovation gap measurement, and skill recommendations. Use when you need to determine what the next evolution cycle should focus on.
---

# Evolution Predictor

Predict optimal next evolution actions based on history analysis.

## When to Use

- Determining next evolution focus
- Need to break stagnation cycles
- Planning innovation strategy
- Want proactive evolution guidance

## Quick Start

```javascript
const predictor = require('./skills/evolution-predictor');

// Get prediction for next action
const prediction = predictor.predictNextAction();
console.log(predictor.formatReport(prediction));

// Get recommended skill to create
const skill = predictor.getRecommendedSkill();
console.log('Recommended:', skill.name);
```

## API

### `predictNextAction(options)`
Analyze evolution history and predict optimal next action.

Returns:
- `prediction`: Action recommendation with category, priority, description
- `confidence`: Prediction confidence (0-1)
- `reasoning`: List of reasons for the prediction
- `metrics`: Success rate, stagnation level, innovation gap

### `getRecommendedSkill()`
Get a specific skill recommendation based on prediction.

### `formatReport(prediction)`
Generate human-readable prediction report.

## Prediction Categories

### `force_innovate` (Critical)
When stagnation level > 60%
- Break stagnation cycles
- Create novel skills
- Implement cross-skill orchestration

### `prioritize_innovate` (High)
When innovation gap > 70%
- Increase innovation rate
- Fill capability gaps
- Address user feature requests

### `explore_new_domains` (Medium)
When success rate > 90%
- Expand capabilities
- Add integrations
- Improve user experience

### `stabilize` (Normal)
Normal operation mode
- Continue current pattern
- Monitor for patterns
- Optimize existing skills

## Metrics

- **Success Rate**: Percentage of recent successful cycles
- **Stagnation Level**: Based on stagnation signal frequency
- **Innovation Gap**: How much the system has been optimizing vs innovating

## Example Output

```
🔮 Evolution Predictor
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Metrics:
  Success Rate: 98%
  Stagnation Level: 85%
  Innovation Gap: 75%

🎯 Prediction:
  Action: force_innovate
  Category: break_stagnation
  Priority: critical
  Description: Force innovation to break stagnation cycle
  Confidence: 85%

💡 Suggested Skills:
  1. Create a novel skill that addresses an unmet need
  2. Implement cross-skill orchestration
  3. Add predictive capabilities
```
