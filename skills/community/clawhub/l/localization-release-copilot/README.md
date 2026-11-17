# Localization Release Copilot

> Shadow-mode copilot for localization / translation release operations.

[![ClawHub](https://img.shields.io/badge/ClawHub-localization--release--copilot-blue)](https://clawhub.com)
[![GitHub](https://img.shields.io/badge/GitHub-haiyangchenbj%2Flocalization--release--copilot-lightgrey)](https://github.com/haiyangchenbj/localization-release-copilot)

## What it does

Given a **source draft** and its **target-language version(s)**, it acts as a shadow
reviewer that catches release-breaking drift *before* publish:

- **Terminology lock** — enforces a glossary of mandatory terms across releases.
- **Number integrity** — locale-aware: `8.3亿` ≈ `830M`, `117亿` ≈ `€11.7B` are matches, not errors.
- **Proper-noun check** — product names, orgs, people, frameworks must survive translation.
- **Attribution preservation** — `(Org, Year)` citations in the source must stay in the target.
- **Structure-loss flagging** — only claim-level drops, not legitimate condensation.
- **Reviewable preview** — a PR-style diff a human can approve in one pass.

It **never rewrites** the translation. Review-only by design.

## When to use

- You have a finished source (ZH article / paper / docs / release note) and a translation into another language, and want a pre-publish consistency pass.
- You publish the same content in multiple languages (WeChat ZH → LinkedIn EN / Substack EN; docs ZH → EN) and want to confirm the target didn't silently drop a number, a proper noun, or a source citation.
- You maintain a glossary and need every release to respect locked terms.
- You want a reviewable preview of what changed between source and target.
- You suspect "the English version reads fine but lost the data" — this skill is built to catch exactly that.

## When NOT to use

- Single-language copyedit → `claim-to-source-auditor` (or any dedicated compliance-review skill).
- Consistency across different materials on the same topic → `cross-material-consistency-auditor`.
- Topic selection → `editorial-topic-portfolio`.
- Machine translation generation (this skill reviews, it does not translate).

## Quick start

```bash
python scripts/locale_aware_diff.py \
  --source path/to/source.zh.md \
  --targets path/to/target.en.md \
  --labels LinkedIn \
  --output 01-extracted-claims.json
```

Then run the LLM diff-matrix + preview step per `SKILL.md`.

## Scope

| Supported (v1.0.0) | Pending (needs real samples) |
|---|---|
| Editorial long-form ZH↔EN localization | SaaS `.po` / i18n locale-file diff |
| Glossary-compliant review | Placeholder / plural checks |
| Multi-target (LinkedIn / Substack / docs) | Translation-memory integration |

## License

Internal use. Remove personal context before any public release.
