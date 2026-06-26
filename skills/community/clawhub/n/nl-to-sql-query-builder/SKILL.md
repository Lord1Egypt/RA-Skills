# NL-to-SQL Query Builder Skill for OpenClaw

## Overview
Production-grade natural language to SQL system based on battle-tested patterns from serving 100+ daily users across 10+ business domains.

## What's Inside

### Core Scripts
1. `query_classifier.py` - Classify query intent (metric, list, comparison, trend)
2. `schema_context_builder.py` - Generate rich schema context from database metadata
3. `confidence_scorer.py` - Calculate confidence based on schema match, ambiguity, edge cases
4. `disambiguation_ui.py` - Flask components for user clarification
5. `fallback_handler.py` - Route low-confidence queries to human review
6. `audit_logger.py` - Track all queries and interpretations

### Features
- **Multi-domain support**: Tested across 10+ industries
- **Confidence thresholds**: 85% auto-execute, 60% clarify, below 60% human review
- **Disambiguation flow**: Interactive UI for clarifying ambiguous queries
- **Error recovery**: Automatic retry with modified prompts
- **Full audit trail**: Compliance-ready logging

## Quick Start
```bash
pip install -r requirements.txt
python schema_context_builder.py --db-url your_db --output schema.json
python query_classifier.py --query "Show me sales by category" --schema schema.json
```

## Pricing
$149 one-time (lifetime updates included)

## Requirements
- Python 3.10+
- OpenClaw agent framework
- Database with metadata access

---
Built by: Abhi (100+ daily users production system)
