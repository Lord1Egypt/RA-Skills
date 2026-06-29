# glic-check

> Systematic, multi-dimension quality check for skills, code, configs, and docs.

GLIC and UGLIC are short checklists you can run against any change to catch
the issues that matter — syntax breaks, logic gaps, doc/code drift, scope
leaks, and (in UGLIC) user-experience pitfalls.

## What you get

| Mode | Dimensions | When to use |
|------|------------|-------------|
| **GLIC** | G + L + I + C (4) | Pure code/config quality review |
| **UGLIC** | U + G + L + I + C (5) | Anything users (humans or agents) interact with — skills, CLIs, docs |

**G — Grammar** — syntax, naming, formatting
**L — Logic** — control flow, edge cases, implicit dependencies
**I — Integrity** — completeness, doc/code alignment, boundaries
**C — Containment** — side effects, security, backward compatibility
**U — Usability & UX** (UGLIC only) — Agent executability + Human usability

## Quick start

The skill is invoked by an LLM agent (Claude Code, Cursor, OpenClaw, etc.).
Once installed, just ask:

```
"GLIC check this change"
"UGLIC this skill"
"do a glic on src/render.py"
"audit my-skill with uglic"
```

The agent will:

1. Detect the mode (GLIC vs UGLIC).
2. Read all in-scope files.
3. Run each dimension's checklist.
4. Produce a report with citations (`file:line` for every finding).
5. Tag each finding `❌ ERR` / `⚠️ WARN` / `ℹ️ INFO`.
6. Ask before fixing anything.

## Severity rules

| Tag | Meaning |
|-----|---------|
| ❌ **ERR** | Functional impact, security risk, doc misaligns with code, or user fundamentally cannot complete the core task. **Must fix.** |
| ⚠️ **WARN** | Maintainability, consistency, future risk, or user friction. **Should fix.** |
| ℹ️ **INFO** | Style preference, minor optimization. **Optional.** |

Escalation rules (enforced for every check):
- Same issue × 3+ → escalate to ERR
- Could fail silently → always ERR
- Missing doc for a public parameter → always ERR

## Why this, not "just review my code"

| Without GLIC | With GLIC |
|--------------|-----------|
| Agent reviews one thing at a time, may miss a dimension | Agent runs all dimensions deterministically |
| Findings often vague ("looks off here") | Every finding must cite `file:line` |
| No severity discipline | ERR vs WARN vs INFO with explicit escalation rules |
| Skills/CLIs reviewed only as code | UGLIC adds the user-experience lens (skills, CLIs, docs) |

## Part of build-better-skills

This skill is part of the
[build-better-skills](https://github.com/Songhonglei/build-better-skills)
suite — open-source skills that help you build better skills, end-to-end:

| Stage | Skill | Status |
|-------|-------|--------|
| Creation | `skill-creator` | 🚧 Not yet released |
| **Audit** | **`glic-check`** | ✅ **v1.0.0** |
| Testing | `skill-regression` | 🚧 Not yet released |
| Release | `skill-release` | 🚧 Not yet released |
| Sediment | `skill-sediment` | 🚧 Not yet released |

Only `glic-check` is installable today. The other entries are roadmap
placeholders — they will appear in the suite repo as they are open-sourced.

## Files

```
glic-check/
├── SKILL.md            ← agent entry point + workflow
├── README.md           ← this file
├── LICENSE             ← MIT
├── .gitignore
├── scripts/
│   └── grep_antipatterns.sh  ← optional half-auto pre-scan helper
└── references/
    ├── dimensions.md   ← detailed sub-check criteria per dimension
    ├── output-format.md ← report template (GLIC + UGLIC variants)
    └── examples.md     ← 5 worked examples (small → large → high-density)
```

## Changelog

### v1.0.1 (2026-06-21)

Self-check + three-tier sample validation pass found 6 real gaps in v1.0.0;
all fixed in this patch.

- ✨ **U-Agent**: Added explicit "SKILL.md length budget" sub-check (WARN > 500 lines, ERR > 800)
- ✨ **U-Agent**: Added "progressive read hint" sub-check (long SKILL.md should tell agent when to lazy-load each reference)
- ✨ **I-Skill**: Added "cross-section references resolve correctly" sub-check (broken `see Step X.Y` is a silent failure)
- ✨ **I-Skill**: Added "no build/runtime artifacts committed" sub-check (sign.key, __skill_meta__.json, .install-source.json, etc.)
- ✨ **I-Skill**: Added "frontmatter field discipline" sub-check (only `name` + `description`, others break strict YAML parsers)
- ✨ **SKILL.md Step 2**: Read-target guidance now distinguishes small vs large targets (structural scan first, then deep-read)
- ✨ **SKILL.md severity escalation**: Clarified "3× WARN → ERR only within the same check, not across separate targets"
- ✨ **NEW: `scripts/grep_antipatterns.sh`** — half-auto pre-scan that surfaces vague directives, SKILL.md length, frontmatter extras, artifact files, and section-reference candidates
- ✨ **Example 5**: New worked example for large skill with 18 findings (3 ERR / 13 WARN / 2 INFO) — sets honest expectation that complex skills produce more findings

### v1.0.0 (2026-06-21)

- Initial open-source release
- GLIC (4-dim) + UGLIC (5-dim) modes
- 4 worked examples, per-target checklists (code/skill/config/doc)
- Severity rules with explicit escalation (silent-failure = ERR, 3× WARN → ERR, missing public-param doc = ERR)

## License

MIT — see [LICENSE](./LICENSE).

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
