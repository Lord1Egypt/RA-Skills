# Provenance, credits & license table

This skill combines several community loop-coding patterns into one engine, plus references to
external CLI tools. It contains **instructions only — no third-party source code**. Referencing a
tool by name and giving its command line is not redistribution, so those tools' licenses do not
This skill is published under **MIT-0** (see `LICENSE`) — free to use,
modify, and redistribute, including commercially, without attribution.

## Content sources (adapted patterns)

Adapted from community loop-coding skills, all published under **MIT-0** (use/modify/redistribute
freely, including commercially, no attribution required — credited here anyway, out of courtesy):

- Ralph loop / ralph-mode — autonomous 3-phase loop (Geoffrey Huntley's Ralph technique lineage)
- execution-loop — Triage, Persistence, Stability (5 failure modes), Autoresearch, Phoenix
- match-loop — Generator ↔ visual Analyst loop
- autoresearch-loop — bounded modify-verify-decide with rollback proof, escalation, lessons
- coding-framework — reuse ladder, `/do` workflow, dependency vetting, auto-review
- vibe-coding-guardrails — machine-enforced safety gates against AI-code risks

Plus widely documented concepts: the Ralph loop (Geoffrey Huntley), Loop Stability Check, and the
Phoenix cross-run learning pattern.

## Design references (structural patterns, not copied text)

The loop design section and audit checklist draw on structural patterns from:

- **Loop Engineering** (maxmilian/loop-engineering, MIT) — 7 principles for designing/reviewing
  autonomous agent loops; specifically the whiteboard-first design process (Principle 0),
  the semi-autonomous escalation boundary (Principle 7), and the review-mode diagnostic
  checklist structure. No text is reproduced; these are adapted concepts in our own wording.

**Refactoring vocabulary** (`refactoring-catalog.md`): the code-smell, technique, and design-pattern
NAMES are established industry terminology, used as facts — not copied text. Sources credited:
Martin Fowler, *Refactoring: Improving the Design of Existing Code* (1999, 2nd ed. 2018, with Kent
Beck, Don Roberts, William Opdyke); Gamma/Helm/Johnson/Vlissides ("Gang of Four"), *Design
Patterns* (1994). All descriptions in the catalog are our own wording. Terminology is not
copyrightable; no book text is reproduced, so no license attaches.

## External tools referenced (not bundled)

| Tool | Purpose | License | How referenced |
|---|---|---|---|
| jscpd | duplication detection | MIT | command line |
| lizard | cyclomatic complexity (17 langs) | MIT | command line |
| scc | LOC + complexity estimate (incl. Dart) | MIT | command line |
| madge | circular-dependency + import-graph (JS/TS) | MIT | command line |
| import-linter | layer/boundary contracts + cycles (Python) | BSD-2 | command line |
| eslint-plugin-boundaries | Clean-Arch layer enforcement (JS/TS) | MIT | command line |
| knip | dead code / unused exports (JS/TS) | ISC | command line |
| vulture | dead code (Python) | MIT | command line |
| dart_code_linter | Dart complexity/metrics (MIT fork of dart_code_metrics) | MIT | binding example |
| Gitleaks | secret scanning | MIT | command line |
| Semgrep | SAST | LGPL 2.1 | command line (not linked/bundled) |
| GuardDog | malicious/hallucinated package detection (R8 slopsquatting) | Apache 2.0 | command line |
| OSV-Scanner | lockfile CVE scanning | Apache 2.0 | command line |
| NVIDIA SkillSpector | third-party skill audit | Apache 2.0 | command line |
| nightshift / agent-guard | destructive-command guard for hook-based runtimes (R12, OPTIONAL) | MIT | mentioned as optional |

**Why this is license-safe to publish:** the skill is Markdown documentation. It does not copy,
embed, link, or distribute any of these tools' code — it tells the user which tool to run. The
user installs each tool themselves under that tool's own license. Even Semgrep's LGPL imposes no
obligation here, because there is no linking or distribution of Semgrep.

**Deliberately avoided:** tools under non-OSI "source-available" licenses with paid tiers for
commercial redistribution, and vendor tools that gate core metrics behind a license key. Every
tool above is OSI-approved permissive (MIT/Apache) except Semgrep (LGPL, referenced only).

## Adapting this skill to your stack

The engine is stack-agnostic. To use it on a non-Flutter stack, copy `bindings/flutter-example.md`
to `bindings/<your-stack>.md`, replace the commands, and keep the engine untouched. Keep any
private data (paths, project names, schedules, product strategy) in your project's own
agent-instructions file — never in the skill.
