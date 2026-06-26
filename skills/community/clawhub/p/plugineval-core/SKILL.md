---
name: plugineval-core
slug: plugineval-core
version: 1.0.0
description: Self-contained PluginEval quality evaluation engine. Measures 6 dimensions, detects anti-patterns, assigns badges. No external dependencies.
author: Nova
source: https://github.com/Donmeusi/openclaw-config/tree/main/skills/plugineval-core
tags: quality,evaluation,skills,badges
triggers:
  - "evaluate skill"
  - "check quality"
  - "quality score"
  - "anti-pattern"
  - "skill badge"
---

# PluginEval Core 🔬

Self-contained quality evaluation for AI agent skills. Measures quality across 6 dimensions, detects anti-patterns, assigns quality badges.

## Use When

- Evaluating skill quality before installation
- Checking installed skills for quality issues
- Improving skills to meet quality standards
- Publishing skills to ClawHub with quality badges

## Input / Output

**Input:**
- Skill directory containing SKILL.md
- Optional: --layer1, --layer2, --anti-patterns flags

**Output:**
```json
{
  "skill": "example-skill",
  "score": 87,
  "badge": "Gold",
  "grade": "B+",
  "anti_patterns": []
}
```

## Usage

```bash
# Layer 1: Static Analysis
python3 ~/.openclaw/skills/plugineval-core/scripts/eval.py --layer1 <skill-dir>

# Anti-Pattern Detection
python3 ~/.openclaw/skills/plugineval-core/scripts/eval.py --anti-patterns <skill-dir>

# Full Evaluation
python3 ~/.openclaw/skills/plugineval-core/scripts/eval.py <skill-dir>
```

## Quality Dimensions

| Dimension | Weight | Measures |
|-----------|--------|----------|
| Frontmatter Quality | 35% | Name, description, trigger |
| Orchestration Wiring | 25% | Input/Output, examples |
| Progressive Disclosure | 15% | Conciseness |
| Structural Completeness | 10% | Headings, troubleshooting |
| Token Efficiency | 6% | Directives, duplication |
| Ecosystem Coherence | 2% | Cross-references |

## Quality Badges

| Badge | Score |
|-------|-------|
| Platinum ★★★★★ | ≥90 |
| Gold ★★★★ | ≥80 |
| Silver ★★★ | ≥70 |
| Bronze ★★ | ≥60 |
| Needs Improvement ★ | <60 |

## Anti-Patterns

| Pattern | Penalty |
|---------|---------|
| OVER_CONSTRAINED | 10% |
| EMPTY_DESCRIPTION | 10-50% |
| MISSING_TRIGGER | 15% |
| BLOATED_SKILL | 10% |
| ORPHAN_REFERENCE | 5% |
| DEAD_CROSS_REF | 5% |

## References

- [quality-framework.md](references/quality-framework.md)
- [anti-pattern-catalog.md](references/anti-pattern-catalog.md)

## Examples

```bash
# Evaluate skill
python3 scripts/eval.py --layer1 ~/.openclaw/skills/weather-pollen

# Output:
# [1/6] Frontmatter Quality: 100/100
# [2/6] Orchestration Wiring: 100/100
# ...
# Final: 87 | Badge: Gold ★★★★
```

---

**Version:** 1.0.0 | **License:** MIT
