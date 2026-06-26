---
name: "Listen"
description: "Improve transcription accuracy over time. Learn corrections, configure STT."
metadata: {"clawdbot":{"emoji":"👂","os":["linux","darwin","win32"]}}
---

## Active Listening

This skill auto-evolves. Track transcription errors and learn corrections.

**Rules:**
- Detect when transcribed text seems off (wrong context, garbled names)
- Learn from user corrections
- Confirm patterns after 2+ occurrences
- Keep entries ultra-compact
- Check `config.md` for OpenClaw STT setup, `criteria.md` for format

---

### Corrections
<!-- Mistranscriptions learned. Format: wrong → right (confidence) -->

### Patterns  
<!-- Recurring issues. Format: "pattern" -->

### Context
<!-- Domain-specific terms that get mangled. Format: "term" -->

### Never
<!-- False positives to ignore -->

---
*Empty sections = no corrections yet. Learn as you go.*
