---
name: laundry-care-symbol-decoder
description: "Decode clothing care symbols into a one-garment or batch care sheet with symbol meanings, actions, avoid notes, delicate-fabric warnings, and label-readability flags."
version: "1.0.0"
type: prompt-flow
tags:
  - laundry
  - clothing-care
  - home-admin
  - symbols
  - garment-care
author: Golden Bean / coder
---

# Laundry Care Symbol Decoder Sheet

## Purpose

Help the user turn a clothing tag or a batch of garment labels into a practical care sheet before washing, drying, ironing, bleaching, or dry cleaning. The deliverable is a printable sheet with each symbol, its meaning, the recommended action, and what to avoid.

This is a prompt-only home care workflow. It supports everyday garment care decisions, but the label and fabric details remain the authority. If the label is unreadable, partly cut off, contradictory, or the fabric is delicate, warn the user and recommend the gentlest safe option or professional cleaning.

## Use This Skill When

Use this skill when the user wants to:

- Understand laundry symbols on one garment tag.
- Build a care sheet for a small batch of similar garments.
- Decide whether to machine wash, hand wash, air dry, tumble dry, iron, bleach, or dry clean.
- Record fabric content, color risk, embellishments, and special care notes.
- Avoid shrinking, fading, pilling, melting, dye transfer, or damage to delicate materials.

Do not use this skill when the user asks for industrial textile processing, chemical stain removal involving hazardous substances, or a guarantee that an expensive garment will be safe. Recommend professional care for high-risk items.

## Best Inputs

Ask for only the details needed to make the sheet useful:

- A clear photo or user description of the care label symbols.
- Garment type: sweater, shirt, coat, dress, jeans, scarf, bedding, towel, uniform, or other.
- Fabric content from the label, if visible.
- Color and dye risk: dark, bright, white, mixed, new, vintage, or unknown.
- Special features: wool, silk, cashmere, leather, suede, lace, sequins, beading, print, coating, elastic, waterproofing, pleats, lining, padding, or glued details.
- User goal: wash now, store safely, travel packing, batch laundry, stain triage, or care archive.
- Whether the label is readable, missing, cut off, faded, or translated from another source.

If the label is not available, create a cautious care plan from fabric and garment details, clearly marked as label-missing guidance.

## Symbol Reading Guide

Use this common symbol map as a starting point, then defer to the actual label and user context:

| Symbol family | Common meaning | Cautious action |
|---|---|---|
| Washtub | Wash method and temperature | Follow dots or number; choose cold if uncertain |
| Hand in tub | Hand wash | Use cool water, gentle detergent, no wringing |
| Crossed washtub | Do not wash | Avoid water cleaning; consider professional care |
| Triangle | Bleach guidance | Empty triangle allows bleach; crossed triangle means no bleach |
| Square with circle | Tumble dry guidance | Follow dots for heat; use low heat if uncertain |
| Crossed square with circle | Do not tumble dry | Air dry flat or hang according to garment structure |
| Square with line | Natural drying method | Line dry, drip dry, or dry flat as indicated |
| Iron | Ironing guidance | Follow dots for heat; protect prints and delicate fabrics |
| Crossed iron | Do not iron | Use steaming only if fabric allows, or skip heat |
| Circle | Professional dry cleaning | Follow letters if visible; ask cleaner if unsure |
| Crossed circle | Do not dry clean | Avoid solvent cleaning |

## Workflow

1. **Identify the garment or batch.** Name each item or group similar items together only when the care labels match.
2. **Assess label readability.** Mark the label as clear, partial, faded, contradictory, missing, or unreadable.
3. **Record fabric and risk factors.** Flag wool, silk, cashmere, rayon, viscose, acetate, leather, suede, lace, beading, sequins, glued trim, waterproof coatings, bright dyes, and vintage fabric as delicate or higher risk.
4. **Decode each symbol.** Translate each visible symbol into plain English. If a symbol is unclear, mark it as `Unreadable or needs confirmation`.
5. **Choose the safest action.** Convert symbols into a care plan: wash method, water temperature, detergent, drying method, ironing level, bleach decision, and professional care note.
6. **Add avoid notes.** Include practical warnings such as no bleach, no tumble heat, no wringing, no direct sun, no soaking, no steam, no high iron, or wash separately.
7. **Create a batch plan.** For multiple garments, group only by matching care action. Put uncertain or delicate items in a separate gentle-care pile.
8. **Add a first-wash caution.** For new, dark, bright, or unknown dyes, recommend washing separately or testing colorfastness.
9. **Escalate high-risk items.** Recommend professional cleaning when fabric is delicate, label is unreadable, garment is expensive, structured, embellished, vintage, or sentimentally important.
10. **Deliver the sheet.** Return a printable artifact for the laundry area or clothing archive.

## Output Format

Return the artifact in this order:

### 1. Garment or Batch Snapshot

| Field | Detail |
|---|---|
| Garment or batch name | |
| Label readability | |
| Fabric content | |
| Color or dye risk | |
| Special features | |
| Delicate or high-risk warning | |
| Assumptions | |

### 2. Symbol Decoder Sheet

| Item | Symbol description | Meaning | Action | Avoid | Confidence |
|---|---|---|---|---|---|
| | | | | | |

Confidence options:

- Clear label
- Partial label
- User-described symbol
- Unreadable or needs confirmation
- Label missing

### 3. Care Plan

Include:

- Wash:
- Water temperature:
- Detergent:
- Bleach:
- Dry:
- Iron or steam:
- Professional care:
- First-wash caution:

### 4. Batch Sorting Notes

If there is more than one garment, group by:

- Safe to wash together:
- Wash separately:
- Hand wash or delicate cycle:
- Air dry only:
- Professional care or hold for review:

### 5. Risk Flags

List any of the following when present:

- Delicate fabric
- Unreadable or missing label
- Conflicting symbols
- Heat-sensitive material
- Color bleed risk
- Embellishment or glued detail risk
- Structured garment risk
- Vintage or sentimental item

## Message Style

- Be calm, practical, and conservative.
- Use plain English, not only symbol jargon.
- Prefer gentler care when the label is unclear.
- Make warnings visible before the care plan.
- Do not promise that a garment will not shrink, fade, or change texture.

## Safety Boundary

Warn clearly when fabric is delicate or the label is unreadable. The safest answer may be to pause, separate the garment, and seek professional cleaning advice. Do not treat uncertain symbols as confirmed.

## Example Prompts

- "Decode the care symbols on this wool sweater tag before I wash it."
- "Build a care sheet for these five new shirts so I know which ones can go together."
- "The label on this vintage dress is faded — give me the safest care plan from what I can read."
