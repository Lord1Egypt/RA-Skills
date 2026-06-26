---
name: proof-card-forge
description: Generate shareable SVG and Markdown proof cards from a skill audit or release metadata for GitHub READMEs, landing pages, and ClawHub listings.
version: 0.1.0
homepage: https://clawhub.ai/zack-dev-cm/proof-card-forge
license: MIT
user-invocable: true
metadata: {"openclaw":{"skillKey":"proof-card-forge","requires":{"anyBins":["python3","python"]}}}
---

# Proof Card Forge

Use this skill when a builder wants a small trust badge that shows a skill was checked before publish.

## When To Use

- A skill audit JSON exists and needs a clean proof card.
- A GitHub README, landing page, or ClawHub listing needs a visual trust signal.
- A release needs a stable score, grade, status, and install link in one asset.
- A builder wants a proof card without hand-editing SVG.

## Workflow

1. Locate the audit JSON from Skill Package Doctor, or collect the skill name, score, grade, and URL.
2. Run the bundled script:

```bash
python3 scripts/proof_card.py \
  --audit skill-doctor.json \
  --out-svg proof-card.svg \
  --out-md proof-card.md \
  --out-json proof-card.json
```

3. If there is no audit file, pass `--name`, `--score`, `--grade`, and `--url`.
4. If you intentionally replace existing artifacts, add `--force`.
5. Review the generated SVG text, score, and link before sharing.
6. Use the Markdown snippet in GitHub and the raw SVG in landing pages.
7. Keep the card honest: refresh it after every material skill change.
8. Read `references/source-manifest.json` only when you need package provenance.

## Review Rules

- Do not show `publish-ready` unless the latest audit supports it.
- Escape all names, descriptions, and links before rendering SVG or Markdown.
- Keep proof cards small, legible, and embeddable.
- Use plain labels: score, status, grade, version, and checked date.
- Link the card to the skill page, release page, or public audit artifact when available.
- If the score is missing, ask for the audit or mark the status as `unchecked`.
- Refuse accidental overwrites unless the user explicitly chooses `--force`.

## Output

Return:

- proof-card SVG path
- Markdown badge snippet
- JSON summary path when generated
- any missing inputs or honesty warnings
- suggested placement for README, landing page, and listing

## Stop Conditions

Do not create or recommend a proof card when:

- the audit says `do-not-publish`
- the user asks to hide known errors
- the source score or status cannot be verified and the card would imply a completed audit
