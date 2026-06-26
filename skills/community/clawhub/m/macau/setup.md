# Setup - Macau Guide

Read this when `~/macau/` is missing or empty.
Keep first-use setup short and practical.

## First Activation Priorities

1. Answer the immediate Macau question first.
2. Confirm whether this skill should auto-activate for Macau, Macao SAR, Cotai, Taipa, or Macau trip and relocation topics.
3. Capture only the minimum context needed to improve recommendations.

## Initial Questions

- Is this a day trip, a short stay, a relocation plan, or a work and study question?
- Which zone matters most: old peninsula, Taipa, Cotai, Coloane, or cross-border commuting?
- Are they optimizing for budget, heritage, nightlife, family logistics, or resort convenience?
- Are borders part of the plan: Hong Kong ferry, HZMB bus, Zhuhai crossing, or direct flight?
- Any hard constraints: visa status, mobility limits, casino avoidance, school needs, or work sector?

## Local Memory Initialization

If approved by user context, initialize local memory:

```bash
mkdir -p ~/macau
touch ~/macau/memory.md
chmod 700 ~/macau
chmod 600 ~/macau/memory.md
```

If `~/macau/memory.md` is empty, initialize it from `memory-template.md`.

## Returning Users

- Read `~/macau/memory.md` before responding.
- Reuse known budget, district, border, and purpose context.
- Ask only what changed since last conversation.
- Update memory with new dates, accommodation logic, and relocation signals.

## Guardrails

- Do not promise immigration or border outcomes.
- Do not collapse Macau into "just casinos" if the user is asking about culture, schooling, or residence.
- Do not give travel-time estimates without checking port, bridge, or weather context.
- Do not assume cards or HKD work everywhere just because they work in hotels and casinos.
