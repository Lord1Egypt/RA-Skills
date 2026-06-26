---
name: military-civilian-talent
description: |
  Military-Civilian Dual-Use Talent Assistant based on the classic Military-Civilian Dual-Use Talent Handbook.
  Covers agriculture, machinery, construction, electrical, photography, seal-carving, cooking, accounting, management, and military knowledge.
  Trigger: agricultural knowledge, tractor maintenance, construction skills, electrical repair, photography, seal carving, cooking skills, accounting knowledge, rural business, military topics.
  Keywords: military-civilian, farm, tractor, construction, electrical, rural
license: MIT
metadata:
  openclaw:
    emoji: '[SKILL_DIR]'
    category: education
    tags: [agriculture, machinery, construction, electrical, photography, cooking, management]
  schema:
    version: 1.0
    language: en
    dependencies: []
    quality:
      idempotent: true
      deterministic: true
      side_effects: []
    harness:
      level: L1-L6
      complexity: low
---

# Military-Civilian Dual-Use Talent Assistant

Comprehensive skills trainer based on the classic Military-Civilian Dual-Use Talent Handbook.

## Disclaimer

Reference information only. For professional construction, electrical, medical, or agricultural advice, consult licensed professionals. Observe all safety regulations.

## Core Modules

| Module | File | Description |
|--------|------|-------------|
| Agriculture | references/agriculture.md | Soil, seeds, fertilizers, planting |
| Military Knowledge | references/military.md | Strategic knowledge, survival |
| Machinery | references/machinery.md | Tractor, diesel engine, water pump |
| Cooking | references/cooking.md | Cooking techniques, food preservation |
| Rural Business | references/rural-business.md | Farm sideline businesses |

## Quick Reference

### Tractor Maintenance Schedule
| Level | Interval | Tasks |
|-------|----------|-------|
| Pre-operation | Before each use | Check oil, coolant, fuel, tire pressure |
| Class A | 50h | Change oil, clean filter |
| Class B | 250h | Adjust valve clearance, check injectors |
| Class C | 500h | Full inspection, replace wear parts |

### Agricultural Calendar
| Season | Key Activities |
|--------|---------------|
| Spring (Mar-May) | Land prep, sowing, seedling management |
| Summer (Jun-Aug) | Irrigation, weeding, pest control |
| Autumn (Sep-Nov) | Harvesting, drying, storage |
| Winter (Dec-Feb) | Land renovation, equipment maintenance |

## Safety Priority
1. Lockout/tagout for electrical work
2. Proper ventilation for fuel/chemicals
3. Fire extinguisher accessible for flammable operations
4. PPE: gloves, goggles, protective footwear

## File Structure
- SKILL.md (this file)
- references/method-patterns.md
- prompts/01-implement-method.md
- prompts/02-robustness-checks.md

## Changelog
- v2.0.0 (2026-04-26): Rewritten in English. Index-only SKILL.md. Prompts folder added.
- v1.0.0 (2026-04-14): Initial version
