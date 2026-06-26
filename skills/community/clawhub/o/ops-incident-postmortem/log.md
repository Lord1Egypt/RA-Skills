# incident-postmortem — Log

## 2026-03-30

### Done
- Built complete incident postmortem generator
- Script: `scripts/generate_postmortem.py` (~450 lines Python stdlib)
- Reference: `references/templates.md` — JSON schema, event types, blame-free guide
- Features: log parsing (8 formats), timeline merge, blame checker, P0-P3 severity, 3 output formats
- 18 error indicator patterns for event classification
- 4 blameful language patterns with suggestions
- Tested: basic generation, full JSON, log parsing, HTML/JSON output, blame checker
- Packaged to `dist/incident-postmortem.skill` ✅

### Decisions
- $59 pricing — mid-range, accessible for engineering teams
- Pure Python stdlib — no dependencies
- Blame-free language checker as standalone feature (--check-blame)
- Exit codes: 0 clean, 1 errors, 2 critical — CI-friendly
