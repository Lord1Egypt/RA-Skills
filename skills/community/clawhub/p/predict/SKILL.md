---
name: predict
description: Prediction and forecasting system for trends, outcomes, and risks. Use when user mentions predictions, forecasts, trends, scenarios, or future outcomes. Analyzes patterns, builds forecasting models, evaluates probabilities, generates scenarios, and assesses risks. Combines data analysis with informed judgment for realistic predictions.
---

# Predict

Prediction system. See patterns, forecast outcomes, manage uncertainty.

## Critical Privacy & Safety

### Data Storage (CRITICAL)
- **All prediction data stored locally only**: `memory/predict/`
- **No external prediction APIs** with data sharing
- **Scenario analyses** remain private
- **Risk assessments** confidential
- User controls all data retention and deletion

### Important Note
Predictions are inherently uncertain. This skill provides structured analysis but does not guarantee outcomes. Always maintain appropriate uncertainty and update predictions as new information emerges.

### Data Structure
Prediction data stored locally:
- `memory/predict/models.json` - Prediction models and frameworks
- `memory/predict/scenarios.json` - Scenario analyses
- `memory/predict/forecasts.json` - Forecast records
- `memory/predict/accuracy.json` - Prediction accuracy tracking

## Core Workflows

### Forecast Trend
```
User: "Forecast sales for next quarter based on current data"
→ Use scripts/forecast_trend.py --metric "sales" --period Q2 --data "historical.csv"
→ Build forecast with confidence intervals and key assumptions
```

### Generate Scenarios
```
User: "What are possible scenarios for this project?"
→ Use scripts/generate_scenarios.py --project "X" --factors "budget,timeline,resources"
→ Create best-case, worst-case, and most-likely scenarios
```

### Assess Risk
```
User: "Assess risks for this business decision"
→ Use scripts/assess_risk.py --decision "expansion" --factors "market,competition,capital"
→ Identify risks, evaluate probabilities, develop mitigation strategies
```

### Evaluate Probability
```
User: "What's the probability of success?"
→ Use scripts/evaluate_probability.py --outcome "success" --factors "team,market,timing"
→ Calculate probability with explicit reasoning and confidence levels
```

## Module Reference
- **Trend Analysis**: See [references/trends.md](references/trends.md)
- **Forecasting Methods**: See [references/forecasting.md](references/forecasting.md)
- **Scenario Planning**: See [references/scenarios.md](references/scenarios.md)
- **Risk Assessment**: See [references/risk.md](references/risk.md)
- **Probability Evaluation**: See [references/probability.md](references/probability.md)

## Scripts Reference
| Script | Purpose |
|--------|---------|
| `forecast_trend.py` | Forecast future trends |
| `generate_scenarios.py` | Generate future scenarios |
| `assess_risk.py` | Assess decision risks |
| `evaluate_probability.py` | Evaluate outcome probabilities |
| `track_accuracy.py` | Track prediction accuracy |
| `build_model.py` | Build prediction models |
