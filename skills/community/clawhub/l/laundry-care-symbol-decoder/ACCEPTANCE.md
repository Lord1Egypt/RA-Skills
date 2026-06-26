# Acceptance Criteria: Laundry Care Symbol Decoder Sheet

## Must Do

- Produce a one-garment or batch care artifact.
- Include garment or batch name, label readability, fabric content, color risk, special features, risk warning, and assumptions.
- Decode visible or user-described symbols into meaning, action, avoid note, and confidence.
- Warn when fabric is delicate, label is unreadable, label is missing, or symbols conflict.
- Recommend conservative care when uncertain.
- Separate batch items when care instructions differ or risk is high.
- Include a professional-care or hold-for-review note for high-risk items.

## Must Not Do

- Do not guarantee that a garment will not shrink, fade, bleed, pill, or change texture.
- Do not treat unreadable symbols as confirmed.
- Do not group garments together when care labels differ.
- Do not ignore delicate fabric, embellishments, glued details, structured garments, or vintage items.
- Do not provide hazardous chemical handling instructions.
- Do not create executable code, package files, credential files, or network-dependent assets.

## Metadata Requirements

- Version is `1.0.0`.
- License is `MIT-0`.
- Language is `en`.
- `hasExecutableCode` is `false`.
- Directory contains exactly `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`.

## Manual Test

Input:

- Garment: black wool sweater
- Label: hand wash symbol, do not bleach, dry flat, low iron; dry cleaning circle is faded and unclear
- Fabric: 100 percent wool
- Goal: wash before storage

Expected result:

- The sheet warns that wool is delicate.
- The faded dry-cleaning symbol is marked as partial or needs confirmation.
- The plan recommends cool hand wash, gentle detergent, no wringing, dry flat, no bleach, low heat only if needed, and professional care if the user is unsure.

## Clean Scan Evidence

- [x] Secrets scan: no API keys, tokens, passwords, or credentials found.
- [x] Executable scan: no scripts, binaries, or executable code present.
- [x] Network scan: no outbound calls, fetch, or API endpoints.
- [x] File audit: only SKILL.md, skill.json, and ACCEPTANCE.md; no temp, logs, or build artifacts.
- [x] Language audit: English only; no CJK or mixed-script content.
- [x] Claims audit: all gate check claims verifiable against file contents.

## Install-First Success Path

- **Input:** User says "Decode the care symbols on this wool sweater tag before I wash it."
- **Steps:**
  1. Agent reads SKILL.md, asks for garment type, fabric content, color risk, label readability, and special features.
  2. Agent decodes each visible symbol into meaning, action, avoid note, and confidence level (clear/partial/unreadable).
  3. Agent produces the Garment Snapshot, Symbol Decoder Sheet, Care Plan, Batch Sorting Notes, and Risk Flags — with conservative recommendations for unclear symbols.
- **Output:** A printable laundry care sheet with decoded symbols, safe wash/dry/iron actions, avoid warnings, delicate-fabric flags, and a professional-care note for high-risk items — based on user-described labels only, with no guarantees about garment outcomes.
