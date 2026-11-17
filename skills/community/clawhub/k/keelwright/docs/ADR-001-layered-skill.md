# ADR-001 — Layered skill: SKILL.md as index, references on demand

**Status:** Accepted (2026-08-30)
**Context:** F46 (SKILL.md layered, 11 598 → 1 606 lines) was marked "mandatory" in
EXECUTION-ROADMAP.md but was implemented cosmetically (empty lines removed, content preserved).
SKILL.md still costs ~17K tokens on every `skill_view(name='keelwright')` call — a real
adoption blocker for Cursor/Claude Code context limits, not just a line-count problem.

## Decision

keelwright ships as a **layered skill**:

1. **`SKILL.md`** = **index** (~150 lines, ~2–3K tokens). Contains:
   - Frontmatter (name/version/license/author/triggers)
   - One-line description + 30-second try
   - Critical safety rules (R1–R12, autonomy dial, circuit-breaker caps) — duplicated
     so they survive even if references aren't loaded
   - `## When to load which reference` map (progressive disclosure)
   - Bootstrap, Web Guard activation, install snippets
   - NO deep explanations; NO risk-glossary table; NO long circuit-breaker philosophy.

2. **`references/*.md`** = **detail modules** (loaded on demand via
   `skill_view(name='keelwright', file_path='references/<module>.md')` or equivalent
   on each runtime). ~8–12 modules, each self-contained, no cross-imports:
   - `references/security-gates.md` — R1–R12 implementations
   - `references/circuit-breaker.md` — caps, file-backed counters
   - `references/phases.md` — build-loop phases P1/P2/P3
   - `references/writing-code.md` — coding discipline (style, R8 slopsquatting)
   - `references/risk-glossary.md` — 28 failure modes
   - `references/web-guard.md` — runtime-agnostic guard activation
   - `references/attack-registry.md` — log schema
   - `references/qa-testing.md` + `qa-trap-catalog.md` — adversarial QA
   - `references/bindings/<runtime>.md` — per-runtime binding
   - `references/stability-and-learning.md` — Phoenix + Autoresearch
   - `references/refactoring-catalog.md` — common refactors

3. **`scripts/build_skill.py`** = **assembly** (B part). Re-assembles a full
   `SKILL.full.md` from index + references for **publications only**
   (skills.sh / ClawHub / askill.sh display whole content; agents load the index).
   This avoids the discoverability hit of publishing a short index on public registries.

4. **Hermes desktop on-demand** (C part, optional later): `skill_view(name, file_path=...)`
   already supports per-module loading. Index points at modules explicitly; we do not
   add a runtime hook (premature complexity). Agents that follow "load when X" already
   get the saving; agents that don't — at least see the critical rules in the index.

## Why this is the right shape

- **Real token savings:** index ~2–3K + on-demand modules ~3–5K each (only when needed).
  Hermes agents see SKILL.md alone at ~2–3K tokens. The 17K cost disappears.
- **Discoverability preserved:** public registries show the full assembled doc, so a
  visitor to skills.sh/ClawHub/askill.sh still sees the whole skill.
- **Runtime-agnostic:** Cursor/Codex/Cline/OpenClaw get the same index; their rules
  files (AGENTS.md / rules/) reference modules by name. Modules are pure markdown,
  no runtime API.
- **Honest about discipline vs enforcement:** critical rules (R1–R12, autonomy, breaker)
  live in the index — they MUST be enforced without a reference load. The rest is
  reference and the agent's discipline.

## What we explicitly reject

- **Auto-loader plugin (variant C from the brainstorm).** Premature. The index already
  makes the right thing easy; a runtime hook would add a point of failure.
- **Per-file semver.** Overkill for a skill releasing every 2–3 months.
- **Fragmenting references into 30+ small files.** Navigation overhead > token savings.
- **Moving public surface into `internal/`.** Violates the skill's own publish-hygiene rule.

## Verification

- Index token budget: ≤ 3K (count after build).
- Module sizes: each ≤ 6K tokens (count after build).
- Build script: idempotent — second run produces identical output (sha256 check).
- Public-registry doc: byte-identical to pre-layered content for any visitor who reads
  everything (modulo link fix-ups and reference-id mapping).
- `references/bindings/<runtime>.md` loadable per runtime (Hermes, Cursor, Codex, Cline, OpenClaw).
