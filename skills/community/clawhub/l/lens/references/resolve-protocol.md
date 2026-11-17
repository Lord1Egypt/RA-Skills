# Resolve Protocol

This protocol defines the logic for handling contradictions, privacy boundaries, and behavioral drift within the LENS.

## 1. Conflict Resolution (Truth Evolution)
- **Rule:** New interaction data takes precedence over existing Node data if a direct contradiction exists.
- **Action:**
  - **Placeholder Replacement:** If the existing entry is an uncalibrated `[Pending Input]` template string, overwrite it directly in place. Never archive `[Pending Input]` placeholders.
  - **Real Data Evolution:** When replacing previously populated factual milestones in `~/.lens/AXIOM.yaml` (such as a job change, relocation, or hardware replacement), preserve the prior milestone inside `timeline` or `history`. In `~/.lens/ETHOS.yaml` and `~/.lens/MODUS.yaml`, refine heuristics and phrasing directly in place without spawning `historical` or `legacy` sub-keys.
  - **Validation:** If the conflict is high-impact (e.g., a core philosophical shift), use [prompts/interview.md](../prompts/interview.md) to seek surgical clarification.

## 2. Privacy Redlines (Exfiltration Protection)
- **Rule:** AXIOM data is for internal calibration only unless explicitly cleared for public manifestation.
- **Redline Items:** Biometric data, specific geolocational addresses, private financial assets, and medical constraints must never be included in external or public-facing drafts (emails, posts, replies, shared documents).
- **Masking:** Use abstractions when these topics are relevant (e.g., "home" or "local timezone" instead of a specific street address).

## 3. Drift & Contextual Deviation
- **Rule:** Distinguish between "Core Identity" and "Contextual Noise."
- **Detection:** If the subject's linguistic style or decision-logic deviates significantly from MODUS/ETHOS, analyze the context (e.g., high-stress troubleshooting, humor, or rapid bot commands).
- **Weighting:** Contextual noise should be weighted lower during distillation. Only persistent patterns trigger a Node update.

## 4. Structural Integrity & Specificity Preservation (Anti-Platitude Rule)
- **Rule:** Refinement must never result in net information loss or generic abstraction drift.
- **Action:** Never flatten sharp, concrete personal rules, trade-off heuristics, or named anchors into vague platitudes during distillation (e.g., never compress *"Simplicity is the ultimate secret; locality is logic"* into *"Values clean code"*). Only modify an already-calibrated key when new evidence sharpens or genuinely updates it.
