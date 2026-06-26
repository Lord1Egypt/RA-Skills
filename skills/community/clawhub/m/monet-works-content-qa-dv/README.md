# Content QA Remediation

Automated QA remediation pipeline for financial content that detects and fixes common issues.

## Description

Content QA Remediation is a two-mode pipeline for fixing content quality issues in financial writing. It can process QA verdict JSON (with REVISE issues) or raw content directly. The skill detects and repairs banned phrases, missing disclaimers, missing CTAs, and excessive length. It outputs fixed content to stdout and a structured change-report JSON to stderr for auditing.

## Key Features

- **Two operation modes** - QA verdict pipeline (preferred) or standalone content fixer
- **Automated fixes** - Banned phrases, disclaimers, CTAs, length trimming
- **Human-judgment flagging** - Tone, strategy, NDA, facts left for editorial review
- **Structured reporting** - JSON change report with before/after diffs
- **Exit code signals** - 0 = all fixed, 1 = partial (manual review needed), 2 = error
- **Template library** - Disclaimer, CTA, and phrase alternative templates
- **Financial content focus** - Designed for investment/trading content compliance

## Quick Start

```bash
# Install dependencies
pip install openai  # or anthropic, depending on LLM provider

# Mode 1: Fix content using QA verdict JSON (recommended)
python3 scripts/auto-remediate.py \
  --content draft.md \
  --verdict verdict.json \
  --type financial > fixed.md 2>report.json

# Mode 2: Standalone content fix (no verdict)
python3 scripts/remediate-content.py \
  --content draft.md \
  --type financial > fixed.md 2>report.json

# Shell wrapper (handles output routing automatically)
bash scripts/remediate.sh \
  --content draft.md \
  --verdict verdict.json \
  --type financial \
  --output-content fixed.md \
  --output-report report.json
```

**Example Output (report.json):**
```json
{
  "status": "partial",
  "fixed_count": 3,
  "remaining_count": 1,
  "changes": [
    {
      "type": "banned_phrase",
      "original": "guaranteed returns",
      "replacement": "historically strong performance",
      "auto_fixed": true
    },
    {
      "type": "missing_disclaimer",
      "added": "This is not investment advice. Past performance...",
      "auto_fixed": true
    },
    {
      "type": "tone_issue",
      "reason": "Overly promotional language requires editorial judgment",
      "auto_fixed": false
    }
  ]
}
```

## What It Does NOT Do

- Does NOT replace human editorial judgment for tone, strategy, or facts
- Does NOT verify factual accuracy or data citations
- Does NOT handle non-financial content types well (optimized for trading/investing)
- Does NOT guarantee regulatory compliance (consult legal counsel)
- Does NOT work without LLM access for phrase substitutions

## Requirements

- Python 3.8+
- openai or anthropic library (for LLM-powered phrase substitution)
- Template files: disclaimer-templates.json, banned-phrase-alternatives.json, cta-templates.json

## License

MIT
