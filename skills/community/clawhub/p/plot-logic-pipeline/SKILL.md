---
name: plot-logic-pipeline
description: Systematically analyze scientific papers by mapping figures to discussions, identifying logical flow, and tracking evidence sources. Figures are the backbone of a paper's argument — this skill teaches agents to trace the logic chain from figure inventory through evidence classification to complete argument reconstruction.
version: 1.0.0
homepage: https://github.com/Larry-of-cosmotim/plot-logic-pipeline
metadata:
  openclaw:
    emoji: 🔬
---

# Plot-Logic-Pipeline

Systematically deconstruct scientific papers by following the figure-discussion logical backbone.

## When to Use

- Analyzing a research paper's argument structure
- Reviewing manuscripts before submission
- Understanding how figures support claims in technical papers
- Mapping evidence sources (literature vs. new measurements)
- Identifying logical gaps or unsupported claims

## Core Principle

**Figures are the bare bones of a paper's logic flow.** Each figure corresponds to a discussion that either:
- **Sets up** the next key finding (preparation)
- **States** the key finding (conclusion)

Complete understanding requires analyzing every figure-discussion pair and tracking evidence sources.

## Analysis Framework

### Step 1: Figure Inventory

Create a complete inventory of all figures in the paper:

```
Figure 1: [Brief description]
Figure 2: [Brief description]
...
Figure N: [Brief description]
```

### Step 2: Figure-Discussion Mapping

For each figure, identify its corresponding discussion section and analyze:

```
Figure X: [Description]
├── Location: [Section/page where discussed]
├── Discussion Type: [Setup / Statement]
├── Main Claim: [Key finding or point]
└── Evidence Source:
    ├── Previous Study: [Citation(s) if supported by literature]
    ├── This Paper: [Analysis method if new measurement/calculation]
    └── Support Level: [Strong / Partial / Contradictory / Missing]
```

### Step 3: Logic Flow Reconstruction

Map how figures build upon each other:

```
Paper Logic Flow:
Figure 1 → Figure 2 → Figure 3 → ... → Conclusion
  ↓            ↓            ↓
[Setup]   [Key Finding 1]  [Key Finding 2]
```

### Step 4: Evidence Assessment

Evaluate the strength of the paper's argument:
- Are all major claims supported by figures?
- Are evidence sources properly attributed?
- Are there logical gaps between figures?
- Do setup discussions adequately prepare for key findings?

## Evidence Classification

### Previous Study Support
- **Direct citation**: Specific reference supporting the claim
- **Literature consensus**: Multiple citations building consensus
- **Comparative reference**: Contrasting with previous work

### This Paper's Contributions
- **New experimental data**: Novel measurements with method specified
- **Novel calculations**: Computational work or modeling
- **Reanalysis**: New interpretation of existing data

### Combined Evidence
- **Validation**: New data confirms previous studies
- **Extension**: New data builds upon previous work
- **Contradiction**: New data challenges previous findings

## Analysis Templates

See [TEMPLATES.md](references/TEMPLATES.md) for detailed templates including:
- Basic figure-discussion analysis
- Complete paper analysis workflow
- Materials science specific templates
- Quality assurance checklist

## Quality Checks

Before concluding analysis:
- ✅ All figures mapped to discussions
- ✅ Evidence sources identified for major claims
- ✅ Logic flow clearly traced from introduction to conclusion
- ✅ Setup vs. statement discussions distinguished
- ✅ Contradictions or gaps noted and flagged

## Common Pitfalls

- **Skipping "obvious" figures**: Even simple schematics contribute to logic flow
- **Missing evidence attribution**: Always identify if claims come from citations or new work
- **Ignoring setup discussions**: These are crucial for understanding logical progression
- **Overlooking figure details**: Axis labels, error bars, and annotations often contain key information
- **Conflating correlation with causation**: Note when figures show correlation vs. when claims assert causation

## Rules

1. **Every figure gets analyzed** — no skipping, even if it seems straightforward
2. **Always classify evidence** — distinguish previous work from new contributions
3. **Trace the logic chain** — show how each figure builds on the previous one
4. **Flag gaps honestly** — note missing evidence or weak logical connections
5. **Separate observation from interpretation** — what the figure shows vs. what the authors claim
