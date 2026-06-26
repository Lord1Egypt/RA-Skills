---
name: Plant Identifier
slug: plant-identifier
version: 1.0.0
homepage: https://clawic.com/skills/plant-identifier
description: "Identify plants from photos using trait-based analysis, ranked species candidates, follow-up capture guidance, and a reusable local log."
changelog: "Initial release with ranked plant identification, trait-based follow-up, and optional local observation memory."
metadata: {"clawdbot":{"emoji":"P","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/plant-identifier/"]}}
---

## When to Use

Use when the user wants to identify a plant from one or more photos, narrow down similar species, log a recurring houseplant or wild observation, or organize what to photograph next.

## Architecture

Memory lives in `~/plant-identifier/`. If `~/plant-identifier/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/plant-identifier/
├── memory.md
├── observations/
│   └── YYYY-MM/
│       └── {entry-id}.md
└── exports/
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Plant evidence checklist | `evidence-guide.md` |

## Scope

This skill ONLY:
- identifies plants from visible traits in user-supplied images
- returns ranked candidates with explicit uncertainty
- asks for the next best photo when the signal is incomplete
- stores local observation notes only if the user approves

This skill NEVER:
- declare a plant safe to eat, touch, burn, or medicate from chat alone
- guarantee species-level certainty when the plant lacks flowers, fruit, bark, or leaf details
- upload images or plant data to external services

## Security & Privacy

**Data stored locally if approved by the user:**
- activation and response preferences in `~/plant-identifier/memory.md`
- one note per saved observation in `~/plant-identifier/observations/`

**This skill does NOT:**
- make network requests
- give safety-critical edible or medicinal clearance
- write local files without user approval

## Core Rules

### 1. Start with image quality and plant completeness
- Check whether the image shows the whole plant, leaves, flower, fruit, stem, or bark.
- If the subject is distant, cropped, wilted, or mixed with other plants, ask for the most useful missing view first.

### 2. Return ranked candidates with evidence and uncertainty
- Give one to three candidates with confidence bands: High 85-95, Medium 60-84, Low 35-59.
- For each candidate, say which visible traits support it and which missing traits keep it tentative.
- If the evidence only supports genus or family level, say so directly.

### 3. Use plant evidence in a fixed order
- Open `evidence-guide.md` before deciding.
- Work from growth habit, leaf arrangement, margin, venation, flower structure, fruit or seed, stem or bark, then habitat context.
- Avoid jumping straight to flower color, which is often too generic by itself.

### 4. Ask for the next best plant photo, not more photos in general
- Prefer whole-plant shot, leaf top and underside, node or stem view, flower front and side, fruit, and bark if relevant.
- Explain which missing trait would separate candidate A from candidate B.

### 5. Separate identification from safety claims
- Plant identification can narrow likely species without proving edibility, toxicity, or medical use.
- If the user asks whether it is safe to eat, touch, or use medicinally, keep the answer conservative and provisional.

### 6. Keep memory around repeated observations, not noise
- Save only durable preferences and approved observation notes.
- One saved entry should record date, location context, best match, confidence, and what evidence was missing.
- Do not write files unless the user approves local storage.

### 7. Say what could change the answer
- Call out missing flowers, missing fruit, juvenile growth, pruning, indoor stress, and hybrid cultivars when they weaken certainty.
- Update the shortlist immediately if a better plant part is shown later.

## Common Traps

- Guessing species from leaf color alone -> many unrelated plants share the same color.
- Treating houseplant stress damage as a species marker -> environment gets mistaken for identity.
- Ignoring the leaf underside, stem nodes, or bark -> key differentiators stay hidden.
- Turning a tentative ID into edibility advice -> that creates avoidable safety risk.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `image` - inspect and optimize plant photos before identification
- `photos` - organize photo sets across repeated observations
- `plants` - broader plant care context once the plant is identified
- `photography` - improve close-up capture, lighting, and color reliability

## Feedback

- If useful: `clawhub star plant-identifier`
- Stay updated: `clawhub sync`
