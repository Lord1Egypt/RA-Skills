---
name: hallucination-check
description: LLM hallucination detector with dual strategy (UQLM + rule-based fallback). Scores any AI output's confidence and flags potential hallucination risks.
emoji: 🔍
platform: python
license: MIT-0
requires:
  pip: [uqlm]
triggers:
  heartbeat: false
  message: false
---

# Hallucination Check

Detect AI hallucination risks in LLM outputs. Uses UQLM (uncertainty quantification) as primary scorer, with a rule-based fallback when UQLM dependencies aren't available.

## Quick Start

```bash
# Install
pip install uqlm

# Check a text
hallucination-check --input "根据我的分析，这可能是新算法，我不太确定具体参数"
# → 置信度: 65.3%  | 建议: 低置信度，建议重新生成

# JSON output
hallucination-check --input "..." --json

# Check from file
hallucination-check --file response.json --field text
```

## How It Works

```
LLM output → UQLM scorer → confidence 0-1 → threshold check
                                      ↓
                            rule-based keyword flags
                                      ↓
                           output: safe/warn/danger
```

## Dual Strategy

| Mode | When | Accuracy |
|------|------|----------|
| **UQLM** | `pip install uqlm` done | High (semantic entropy + min token prob) |
| **Rule fallback** | UQLM unavailable | Medium (keyword + pattern matching) |

## Thresholds

- `--threshold 0.3` (default): below = high risk
- Flags: vague language, unsourced numbers, contradiction patterns

## For Developers

The core function is `check_text(text, context="")`:
```python
from hallucination_check import check_text
result = check_text("AI生成的内容", context="指令")
print(result["confidence"], result["suggestion"])
```

## Notes

- UQLM needs `transformers<5.0.0` (see pypi for version compat)
- Rule fallback is zero-dependency, works everywhere
- Best used before critical operations (code execution, SQL, external sends)
