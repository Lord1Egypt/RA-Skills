# Forge

  <img src="./assets/readme/hero.jpg" width="100%" alt="Forge: skill architect and builder — designs, scopes, builds, and validates new OCAS skills">

Skill design and construction for Hermes Agent. Runs a mandatory eight-phase pipeline: existence gate, research, classify, scope, architecture, plan, build, validate. Default output is the finished installable package.

**Skill name:** `ocas-forge`
**Version:** 3.7.1
**Type:** system
**Layer:** Architecture
**Author:** <agent-name>

---

## 📖 Overview

Builds and repairs agent skill packages. Default output is the finished package.

---

## 🔧 Commands

- `forge.build` — build a complete skill package
- `forge.critique` — review a package and identify defects
- `forge.repair` — fix broken files in an existing package
- `forge.classify` — classify a proposed skill by size class
- `forge.validate` — run structural validation
- `forge.scaffold` — generate a minimal package skeleton
- `forge.consolidate` — merge orphan or duplicate skill into its natural parent
- `forge.sync` — sync local skill changes to the canonical repository via PR
- `forge.verify-update` — check whether a skill is at the latest version
- `forge.audit` — audit skills for compliance, apply fixes, sync to GitHub
- `forge.status` — current build state if multi-step build in progress
- `forge.journal` — write journal for the current run
- `forge.update` — pull latest from GitHub source; preserves journals and data

---

## 📊 Outputs

Packages written to disk. Journals. Validation reports. PRs for sync operations.

---

## 📄 Files

| File | Purpose |
| --- | --- |
| `SKILL.md` | Skill definition with agentskills.io frontmatter |
| `CHANGELOG.md` | Release history |
| `references/` | Pipeline specs, authoring rules, ontology, schemas, workflow plans |
| `scripts/` | Build and validation scripts |
| `templates/` | Package scaffolding and file templates |
| `evals/` | Evaluation suites and metrics |
| `deferred/` | Out-of-scope material pending proper homes |

---

## Changelog

- **v3.7.1 (2026-07-13)** — Audit repair: restored missing manifest fields, fixed frontmatter validation errors, standardized templates/skill.json against schema.
- **v2.7.1 (2026-04-26)** — Version alignment: SKILL.md frontmatter, CHANGELOG.md, and GitHub release tag in sync. No functional change.
- **v2.7.0 (2026-04-18)** — Refactor: folded builder-domain helper skills into Forge's existing structure. SKILL.md shrunk to 343 lines. Added `forge.consolidate`, `forge.sync`, `forge.verify-update`. Moved runtime-harness guidance to `deferred/running-ocas-skills.md`. Moved OAuth/MCP setup content to `deferred/mcp-oauth-setup.md`.
- **v2.6.11 (2026-04-16)** — Authoring rules v2.7.2 -> v2.8.0. Ontology v2.0.1 -> v2.1.1. Active ecosystem updated.
- **v2.6.8 (2026-04-12)** — Fixed missing `{agent_root}/skills/` filesystem write path.
- **v2.6.0 (2026-04-08)** — Adopted agentskills.io open standard. Replaced skill.json hardcoding with {agent_root}/commons/ convention.

---

## 📚 Documentation

Read `SKILL.md` for operational details, schemas, and validation rules.

Read `references/` for detailed specifications and examples.

---

## 📄 License

MIT License — see `LICENSE` for details.