# AGENTS.md

> Skill manifest for AGENTS.md-aware runtimes (Codex CLI, CodeBuddy, Continue, Aider, OpenCode, generic). Native skill runtimes should read [SKILL.md](SKILL.md) directly.

## Skill: `ifq-design-skills` (v2.4.3)

**Use when** the user asks for an HTML-first visual design deliverable: interactive prototype, slide deck, infographic, dashboard, landing page, whitepaper, changelog, business card, social cover, brand system, motion demo, design critique, brand diagnosis, multi-variant exploration, or 3-direction advisory.

**Do not use for** production web apps, SaaS backends, SEO-critical sites, backend systems, pure copy rewriting, or isolated CSS patches.

**Entry point**: [SKILL.md](SKILL.md) is now a short router. Read it first, then route via [references/modes.md](references/modes.md) and [assets/templates/INDEX.json](assets/templates/INDEX.json).

## 60-Second Start

1. Match the user prompt against `SKILL.md` frontmatter `description` and `metadata.openclaw.triggers`. Use the Quick Decision Tree in SKILL.md for sub-3-second routing.
2. Read [references/modes.md](references/modes.md), pick a mode (M-01 ... M-12), then open [assets/templates/INDEX.json](assets/templates/INDEX.json).
3. Fork the matching template into the user's workspace. Never start from a blank HTML file. 12 templates are available — see [assets/templates/GALLERY.html](assets/templates/GALLERY.html).
4. Inline [assets/ifq-brand/ifq-tokens.css](assets/ifq-brand/ifq-tokens.css) and weave at least 3 IFQ ambient marks from [references/ifq-brand-spec.md](references/ifq-brand-spec.md).
5. Write unresolved facts as reversible assumptions, not hidden guesses.
6. Run the Anti-Slop Preflight: `npm run anti-slop -- <file.html>` or manually check the 7-point checklist from [references/anti-ai-slop.md](references/anti-ai-slop.md).
7. Verify with host browser tooling when available. After package edits, run `npm run validate`; before publishing, run `npm run pack`.
8. Return the evidence packet: output file, mode, template, assumptions, verification, and caveats that affect use.

## Neutral Verbs

This skill uses runtime-agnostic verbs. Translate them to the host runtime's actual tools.

| Neutral verb | Meaning |
|---|---|
| read file | open and read workspace content |
| write file | create or update workspace content |
| list dir | inspect files/directories |
| run command | execute allowed workspace shell commands |
| web search | optional fact/asset lookup |
| web fetch | optional read-only HTTPS fetch |
| screenshot | host browser capture, or full repo helper when installed |

Full per-runtime mapping lives in [references/agent-compatibility.md](references/agent-compatibility.md).

## Permissions

- `filesystem` — read + write inside the active workspace only
- `shell` — run bundled Node scripts in the workspace (`npm run validate`, `npm run pack`)
- `browser` — optional outbound HTTPS reads for facts, fonts, and legal image assets
- `memory` — optional lookup of user asset notes when supported

If a permission is unavailable, degrade gracefully: browser-off means local fonts and user-provided facts; shell-off means HTML-only work without smoke/pack commands.

## Operating Principles

1. **Facts before assumptions** — for a specific product, launch, version, spec, or company claim, verify with authoritative sources first; if network is blocked, ask the user and mark the fact unresolved. See [references/asset-protocol.md](references/asset-protocol.md).
2. **Asset > spec** — real logo, product image, or UI screenshot beats inferred colors and generic decoration.
3. **Fork, then fill** — templates are the starting point; blank-page design is a fallback only when no template fits. 12 templates cover all 12 modes.
4. **Variants over one answer** — for fuzzy direction, propose 3 differentiated routes using [references/design-styles.md](references/design-styles.md) and [references/ifq-native-recipes.md](references/ifq-native-recipes.md).
5. **Honest placeholders** — labeled placeholders beat low-quality fake imagery or invented data.
6. **Anti AI-slop** — run `npm run anti-slop -- <file.html>` or manually check the 7-point checklist from [references/anti-ai-slop.md](references/anti-ai-slop.md) before delivery. This is a hard gate, not a suggestion.
7. **Weave, don't stamp** — IFQ should be felt as layout craft before it is read as a mark.

## Quick Commands

| Command | What it does |
|---|---|
| `npm run validate` | One-minute smoke + eval gate: templates, routes, references, manifest, package safety, script safety, font loading |
| `npm run evals:validate` | Validates the 12-mode regression scenarios and agent contracts |
| `npm run verify:lite -- <file.html>` | Static placeholder / template-leak scan for generated HTML |
| `npm run anti-slop -- <file.html>` | Scan HTML for 7 AI-slop violations (gradient text, glassmorphism, hero-metric, generic fonts) |
| `npm run pack` | Builds a ClawHub-clean `.tar.gz` outside the repo |

## Install Paths

```bash
# ClawHub one-liner (recommended install channel)
openclaw skills install ifq-design-skills

# Local dev / shared agents dir
git clone https://github.com/peixl/ifq-design-skills ~/.agents/skills/ifq-design-skills
```

`compiled by ifq.ai · 2026`
