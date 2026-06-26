# Corvus Curiosity Engine

## Overview

The curiosity engine drives Corvus's exploration of the knowledge graph. It determines which regions of the graph to investigate and generates hypotheses for testing.

## Drives

### Novelty

Prioritize graph regions that recently appeared or changed. New entities, new relationships, and recently modified nodes score higher.

Scoring: recency-weighted count of new or modified nodes in the region.

### Uncertainty

Prioritize entities with many signals but incomplete understanding. High signal count combined with low pattern confidence indicates areas worth exploring.

Scoring: signal_count × (1 - max_pattern_confidence) for entities in the region.

### Prediction Error

Prioritize patterns where predicted outcomes diverge from observed events. Failed predictions indicate the model needs updating.

Scoring: magnitude of prediction error × prediction confidence.

## Hypothesis Generation

Each drive produces candidate hypotheses:

1. Drive selects a high-priority graph region
2. Corvus examines the region's entities, relationships, and signals
3. Corvus formulates one or more hypotheses about patterns or relationships
4. Each hypothesis is assigned an initial confidence based on available evidence

## Hypothesis Testing

Hypotheses are tested through:

1. Additional graph queries to find supporting or contradicting evidence
2. Temporal analysis to check consistency
3. Cross-domain checks to find corroboration
4. Falsification attempts to find counter-evidence

Hypotheses that survive testing are promoted to pattern validation.

## Priority Scoring

The overall priority of a graph region combines all three drives:

```
priority = (novelty_weight × novelty_score) +
           (uncertainty_weight × uncertainty_score) +
           (prediction_error_weight × prediction_error_score)
```

Weights are configurable in `~/openclaw/data/ocas-corvus/config.json`.
