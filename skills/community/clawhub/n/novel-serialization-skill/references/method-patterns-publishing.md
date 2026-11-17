# Publishing Workflow Templates

This module provides templates and conventions for publishing serialized novel content via Git and GitHub. These templates ensure consistent, versioned releases that are easy to track and distribute.

---

## 1. Git Tag Format

### Tag Naming Convention
```
v{major}.{minor}.{patch}
```

### Tag Examples
- `v1.0.0` — Major release (complete arc)
- `v1.1.0` — Minor release (new chapter added)
- `v1.1.1` — Patch release (typo fix, continuity correction)
- `chapter-001` — Chapter-specific tag (optional)

### Tag Message Format
```
v{version}: {brief description}

{detailed description of changes}

Changelog: See CHANGELOG.md
```

---

## 2. Release Note Template

```
# Release [Version] - [Date]

## Summary
[Brief summary of this release]

## What's New
### Chapters
- [Chapter X]: [Brief description]

### Improvements
- [Improvement 1]
- [Improvement 2]

## Fixes
- [Fix 1]
- [Fix 2]

## Known Issues
- [Known issue 1]

## Upgrade Notes
[Any notes for readers upgrading from previous version]

## Full Changelog
See [CHANGELOG.md](../CHANGELOG.md) for complete history.
```

---

## 3. Chapter File Naming Convention

### Naming Pattern
```
ch-{chapter_number}-{chapter_title}.md
```

### Examples
- `ch-001-the-beginning.md`
- `ch-042-crossroads.md`
- `ch-100-finale.md`

### Frontmatter Requirements
Every chapter file MUST include YAML frontmatter:

```yaml
---
chapter: {number}
title: "{chapter title}"
pov: {POV character name}
date: YYYY-MM-DD
word_count: {approximate word count}
status: draft|review|published
license: CC-BY-NC-SA-4.0
---
```

**File-header order.** Two rules both claim the top of a chapter file: the YAML frontmatter
above, and spec Section 0.5's requirement that every generated novel file *begin* with the
CC BY-NC-SA 4.0 header block. They are reconciled as follows, and every chapter file uses
this exact order:

1. **YAML frontmatter first, at byte 0** — any content before the opening `---` stops tools
   from parsing it as frontmatter. The `license:` key here is the machine-readable licence
   declaration that the release workflow's licence gate checks.
2. **CC BY-NC-SA 4.0 header block second** — the human-readable block from spec Section 4.3,
   before any narrative prose.

See [example-chapter-draft.md](examples/example-chapter-draft.md) for a worked instance.

### File Structure
```
chapters/
├── ch-001-the-beginning.md
├── ch-002-first-steps.md
├── ch-003-the-call.md
└── ...
```

---

## 4. Publishing Checklist

```
# Publishing Checklist

## Pre-Publish Verification
- [ ] Continuity check passed (see method-patterns-continuity.md)
- [ ] Chapter formatting verified
- [ ] License headers present
- [ ] Word count documented
- [ ] POV character documented
- [ ] Timeline consistency verified
- [ ] Character states updated
- [ ] Unresolved threads logged

## Git Operations
- [ ] All changes committed with descriptive message
- [ ] CHANGELOG.md updated
- [ ] Tag created with proper format
- [ ] Tag message follows convention

## Post-Publish
- [ ] Release notes published
- [ ] Readers notified (if applicable)
- [ ] State files updated
- [ ] Feedback collected
```

---

## 5. Version Bumping Guide

### When to Bump
| Change Type | Version Bump | Example |
|-------------|-------------|---------|
| Major release (complete arc) | MAJOR | v1.0.0 → v2.0.0 |
| New chapter/content added | MINOR | v1.1.0 → v1.2.0 |
| Typo/continuity fix | PATCH | v1.1.1 → v1.1.2 |

### Bumping Process
1. Update version number in relevant files
2. Update CHANGELOG.md with release notes
3. Commit changes: `git commit -m "chore: bump version to vX.Y.Z"`
4. Create tag: `git tag -a vX.Y.Z -m "vX.Y.Z: {description}"`
5. Push to remote: `git push origin vX.Y.Z`

---

## 6. GitHub Release Workflow

### Automated Release Steps
1. **Validate**: Check file formats and naming conventions
2. **Verify**: Run continuity checks and license compliance
3. **Package**: Prepare release assets
4. **Publish**: Create GitHub Release with notes
5. **Notify**: Update readers/community

### Manual Release Steps
1. Ensure all checklist items are complete
2. Update CHANGELOG.md
3. Commit and tag with proper version
4. Push to remote
5. Create GitHub Release with release notes

---

## 7. Three-Stage Review (三审制度)

Before a chapter is promoted from draft to release, it passes a three-stage review with
three distinct roles. The stages flow **one way**; a later stage may overturn an earlier
stage's verdict (recording the reason in the report's 备注 line), but an earlier stage may
never overturn a later one. This mirrors the publishing industry's 三审责任制 and gives the
Skill a real audit trail instead of a single flat gate.

### 7.1 Roles, scope and exit gates

| Stage | `review_all.py --stage` | Role (角色) | Scope | Dimensions run | Exit gate |
|-------|-------------------------|-------------|-------|----------------|-----------|
| 初审 | `first` | 责任编辑 | Mechanical & textual layer | `humanizer`, `scale`, `punctuation` | No `FAIL` → send to 复审; any `FAIL` returns to the **author** |
| 复审 | `second` | 编辑部主任 | Content layer | `continuity`, `rationality` | No `FAIL` → send to 终审; any `FAIL` returns to **初审** |
| 终审 | `final` | 主编 | Full-dimension regression + read-through | all five | No `FAIL` **and** every `WARN` adjudicated → **signed off**, may `promote` |

- **初审 (责任编辑)** catches the machine-detectable layer: AI-tone residue, word-count
  shortfall/overshoot, punctuation and orthography. It does not judge plot or continuity.
- **复审 (编辑部主任)** judges the content layer: cross-chapter consistency (names, ages,
  timeline, title/body parity) and rationality (duplicate paragraphs, dialogue ratio, POV
  drift, unresolved foreshadowing, outline coverage). It may overturn 初审 with a reason.
- **终审 (主编)** re-runs all dimensions as a regression (confirming 初审/复审 fixes landed
  and nothing new broke), reads through, adjudicates every remaining `WARN`
  (keep / revise / record a reason), and signs off. Only a signed 终审 permits `_promote_draft.py`.

### 7.2 Commands

Run from the subproject root. Each stage emits its **own** report with its own signature
block; archive all three — do not overwrite an earlier stage's report with a later one.

```bash
# 初审 — 责任编辑（机械层与文字层）
python "../GitHub Novel Serialization Skill/scripts/review_all.py" --stage first \
    --out .workbuddy/reports/初审_第9批.md

# 复审 — 编辑部主任（内容层）
python "../GitHub Novel Serialization Skill/scripts/review_all.py" --stage second \
    --out .workbuddy/reports/复审_第9批.md

# 终审 — 主编（全维回归 + 通读签发）
python "../GitHub Novel Serialization Skill/scripts/review_all.py" --stage final \
    --out .workbuddy/reports/终审签发_第9批.md
```

Per-chapter or draft scope still works at any stage (`--chapters 031 034`,
`--draft notes-personal/正文草稿.md`). Running **without** `--stage` keeps the legacy
all-in-one sweep (one report, generic sign-off) — fine for a quick full check, but it does
**not** substitute for the three signed stages before promotion.

### 7.3 Verdict semantics per stage

| Stage verdict | Meaning | Action |
|---------------|---------|--------|
| `PASS` | No `FAIL`, no `WARN` | May advance (终审 PASS = sign off, may `promote`) |
| `REVISE` (WARN) | No `FAIL`, but `WARN` present | Human must adjudicate each `WARN` before advancing; 终审 must record each ruling |
| `FAIL` | At least one `FAIL` | **Blocks promotion.** Returns to the previous step (初审 FAIL → author; 复审 FAIL → 初审; 终审 FAIL → 复审) |

### 7.4 Flow rules (non-negotiable)

1. **One-way flow.** Stages run in order 初审 → 复审 → 终审. Later may overturn earlier; earlier may not overturn later.
2. **`FAIL` blocks promotion.** `_promote_draft.py` must not run until 终审 signs off.
3. **`WARN` needs a human.** `WARN` never blocks a stage mechanically, but 终审 adjudicates every `WARN` before signing.
4. **One report per stage.** Three archived reports are the audit trail. Reports go to `.workbuddy/reports/` (subproject convention) or `state/continuity-reports/`.
5. **Re-run after revision.** Any revision restarts from 初审; a sign-off does not carry over to text changed after it.
6. **Role isolation.** The reviewer at each stage proposes a verdict; the human in that role owns the sign-off. A script's `PASS` is a recommendation, not a signature.

### 7.5 Where the stage definitions live

The stage→dimension mapping, role names, exit gates and per-stage signature blocks are
defined once in `scripts/_review_lib.py` (`STAGES`, `STAGE_DIMS`, `signoff()`); both this
document and `SKILL.md` describe them. If they ever disagree, the script is authoritative
for what `review_all.py --stage` actually runs, and this document is authoritative for the
human process around it.

---


## Cross-References

- See [method-patterns-worldbuilding.md](method-patterns-worldbuilding.md) for world-building elements.
- See [method-patterns-character.md](method-patterns-character.md) for character design templates.
- See [method-patterns-chapter.md](method-patterns-chapter.md) for chapter writing templates.
- See [method-patterns-continuity.md](method-patterns-continuity.md) for continuity tracking templates.

---

## License

Licensed under GNU General Public License v3.0 (GPL-3.0). Generated novel content produced using these templates is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0).
