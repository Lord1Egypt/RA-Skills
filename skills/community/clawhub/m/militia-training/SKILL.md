---
name: militia-military-training
description: |
  Militia Military Training Assistant based on the classic Militia Military Training Manual.
  Covers anti-aircraft defense, NBC (nuclear-biological-chemical), shooting, combat tactics, combat service support.
  Trigger: anti-aircraft defense, NBC defense, shooting training, combat tactics, field survival, sentry duty, reconnaissance.
  Keywords: militia, anti-aircraft, NBC, shooting, combat, military training
license: MIT
metadata:
  openclaw:
    emoji: "[SHIELD]"
    category: education
    tags: [military, defense, shooting, NBC, combat, survival]
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

# Militia Military Training Assistant

Combat skills trainer based on the classic Militia Military Training Manual.

## MANDATORY DISCLAIMER

This skill provides general knowledge for educational reference only. For professional military training and certification, contact official military training institutions. Observe all applicable laws and regulations.

## Core Modules

| Module | File | Description |
|--------|------|-------------|
| Anti-Air Defense | references/air-defense.md | Aircraft identification, AAA operations |
| Shooting | references/shooting.md | Firing techniques, marksmanship |
| Combat Tactics | references/combat-tactics.md | Attack, defense, patrol |
| Combat Service | references/combat-service.md | Logistics, medical, signal |

## Quick Reference

### Aircraft Identification
| Type | Speed | Altitude | Sound | Threat |
|------|-------|----------|-------|--------|
| Fighter | Fast | Low-High | High pitch whine | HIGH |
| Bomber | Medium | Medium-High | Deep roar | HIGH |
| Helicopter | Slow | Low | Thump-thump | MEDIUM |
| UAV | Variable | Variable | Minimal | MEDIUM |
| Civilian | Regular | Varies | Jet noise | LOW |

### Shooting Fundamentals
| Element | Key Point |
|---------|-----------|
| Stance | Stable, balanced, squared to target |
| Grip | Firm but not white-knuckle |
| Breath | Natural pause at mid-exhale |
| Alignment | Front sight centered in rear notch |
| Trigger | Smooth, continuous pull |
| Follow-through | Hold position after shot |

## Safety Rules
1. Treat every weapon as loaded
2. Never point at anything you do not intend to destroy
3. Keep finger off trigger until ready to fire
4. Identify target and what is beyond it
5. Maintain situational awareness at all times

## File Structure
- SKILL.md (this file)
- references/method-patterns.md
- prompts/01-implement-method.md
- prompts/02-robustness-checks.md

## Changelog
- v2.0.0 (2026-04-26): Rewritten in English. Index-only SKILL.md. Prompts folder added.
- v1.0.0 (2026-04-14): Initial version
