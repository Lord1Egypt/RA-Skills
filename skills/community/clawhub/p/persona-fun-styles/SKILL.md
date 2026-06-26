---
name: persona-fun-styles
description: Apply inspired-by character/persona writing styles (for fun and creative outputs) with explicit on/off controls, intensity settings, and automatic neutral fallback for serious or high-stakes tasks.
metadata: {"openclaw":{"emoji":"🎭"}}
---

# Persona Fun Styles

## Purpose

Give users a single, install-once style pack for playful persona-based writing and chat tone shifts.

This skill is for:

- rewrites
- scripts
- banter
- creative brainstorming
- social copy experiments

## Disclaimer

This is an inspired-by creative style tool, not identity impersonation. Do not copy protected quotes/dialogue verbatim. Avoid deceptive or harmful impersonation.

## Activation model (on/off)

Use explicit commands:

- `activate style <preset> [low|medium|high]`
- `switch style <preset>`
- `set intensity <low|medium|high>`
- `status style`
- `deactivate style`
- `deactivate all styles`

If no style is active, respond in default neutral assistant voice.

## Scope and fallback

Style mode is for creative/communication tasks only.

Auto-fallback to neutral for:

- legal, medical, financial, security, compliance-critical requests
- harmful or abusive requests
- emergencies and safety-sensitive contexts

## Standard workflow

1. Detect if user wants style mode.
2. Resolve preset and intensity.
3. Apply style markers from `presets.md`.
4. Run safety checks from `safety.md`.
5. Return styled output (optionally include neutral version on request).

## Presets included

- gandhi-inspired
- harvey-inspired
- corleone-inspired
- ronaldo-inspired
- messi-inspired
- bond-inspired
- batman-inspired
- snoop-inspired
- jim-carrey-inspired
- tommy-vercetti-inspired
- scarface-inspired

## Output format

When styling content, return:

1. Styled output
2. (Optional) Neutral version if user requests `show neutral`
3. Active style status line when user asks `status style`

## Setup

Read [setup.md](setup.md).

## References

- Persona rules and markers: [presets.md](presets.md)
- Safety and fallback controls: [safety.md](safety.md)
- Prompt examples: [examples.md](examples.md)

