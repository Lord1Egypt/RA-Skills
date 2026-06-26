---
name: idea-validator
description: Startup idea validation skill. Helps indie developers validate product ideas, analyze competitive landscapes, and assess market saturation.
---

# Idea Validator

## Overview

Helps indie developers validate the uniqueness and market potential of product ideas through a multi-dimensional evaluation framework.

## Use Cases

Use when users mention "idea validation," "competitor analysis," "validate startup idea," "analyze market space," "startup idea evaluation," or "idea validation."

## Core Capabilities

| Capability | Description |
|------------|-------------|
| Multi-dimensional Startup Idea Evaluation | Comprehensive assessment of market / competition / technology / business model |
| User Persona and Needs Validation | Target user persona construction and pain point analysis |
| MVP Roadmap Generation | Define core features and plan product iteration path |

## Command List

| Command | Description |
|---------|-------------|
| `python scripts/idea_validator.py validate --idea "<product description>"` | Validate startup idea |
| `python scripts/idea_validator.py compete --market "<category>"` | Competitor analysis |
| `python scripts/idea_validator.py mvp --idea "<product description>"` | Generate MVP plan |

## Usage Workflow

### Validate Startup Idea

When the user says "validate [product name] startup idea," execute:

```bash
python3 scripts/idea_validator.py validate --idea "<product description>"
```

### Competitor Analysis

When the user says "analyze [category] competitive landscape," execute:

```bash
python3 scripts/idea_validator.py compete --market "<category>"
```

### Generate MVP Plan

When the user says "generate MVP feature plan," execute:

```bash
python3 scripts/idea_validator.py mvp --idea "<product description>"
```

## Output Format

All commands output a unified Markdown format report containing:

- **Key Findings** — 3-5 key insights
- **Data Overview** — Key metrics table (with ratings)
- **Detailed Analysis** — Multi-dimensional in-depth analysis
- **Actionable Recommendations** — List of suggestions categorized by priority

## References

See `references/references.md` for details, including links to Y Combinator startup methodology, community discussions, and Chinese resources.

## Notes

- Do not fabricate data; mark missing data fields as "Data Unavailable"
- All analysis is based on publicly available information; AI is for reference only
- It is recommended to combine with human judgment
- Install dependencies before first use: `pip install requests`