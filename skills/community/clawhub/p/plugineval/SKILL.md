---
name: plugineval
version: 2.0.0
description: PluginEval Quality Evaluation with enhanced UI. Wraps plugineval-core with vetting and reporting features. Requires plugineval-core.
source: https://github.com/Donmeusi/openclaw-config/tree/main/skills/plugineval
requires:
  - plugineval-core
---

# PluginEval 2.0.0 🔬

Enhanced quality evaluation with vetting workflow. This skill wraps `plugineval-core` and adds:
- Combined security + quality checks
- Vetting workflow
- Report generation

## Use When

- Evaluating skills before installation
- Combined security + quality vetting
- Publishing with quality badges

## Dependencies

**Required:** `plugineval-core`

```bash
clawhub install plugineval-core
```

## Input / Output

**Input:** Skill name or path

**Output:** Combined security + quality report

## Quick Start

```bash
# Vetting workflow (Security + Quality)
~/.openclaw/skills/plugineval/scripts/vet.sh weather-pollen

# Or use core directly
python3 ~/.openclaw/skills/plugineval-core/scripts/eval.py --layer1 <skill>
```

## Examples

### Vetting a Skill

```bash
vet-skill weather-pollen

# Output:
# ════════════════════════════════════════════════════
# Skill Vetting: weather-pollen
# ════════════════════════════════════════════════════
#
# [1/3] Security Scan (ClawDefender)
# ─────────────────────────────────────────
#   ✓ Clean
#
# [2/3] Quality Evaluation (PluginEval)
# ─────────────────────────────────────────
#   Final: 81 | Badge: Gold ★★★★
#
# [3/3] Anti-Pattern Detection
# ─────────────────────────────────────────
#   ✓ No anti-patterns
```

## References

- [EXTERNAL.md](EXTERNAL.md) - External dependencies documentation
- `plugineval-core` - Core evaluation engine

## Changelog

### v2.0.0 (2026-04-08)
- Now wraps plugineval-core (separate skill)
- Added dependency management
- Simplified structure
- Platinum badge quality

### v1.3.0 (2026-04-08)
- Version sync fix
- Added source link
- Added EXTERNAL.md documentation

### v1.2.0 (2026-03-31)
- Added Layer 3: Auto-Fix
- Added vet-skill.sh

### v1.0.0 (2026-03-31)
- Initial release

---

**Requires:** plugineval-core | **Version:** 2.0.0
