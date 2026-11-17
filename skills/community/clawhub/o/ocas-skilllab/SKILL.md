---
name: ocas-skilllab
license: MIT
description: >
  Skill library maintenance: audit, merge, rename, delete, consolidate, publish,
  sanitize, and critique skills. Interactive menu via clarify tool.
  Scans ALL profile directories recursively — never hardcodes a single path.
  Use when the user asks to clean up the skill library, merge
  overlapping skills, rename skills to follow naming conventions, delete auto-generated
  or stale skills, audit skills for authorship, publish skills to external registries,
  sanitize skills for security scanner compliance, score skills against the 10-dimension
  rubric, generate improvement plans, or run autonomous library grinding (10khr).
  Also covers frontmatter conventions
  and how to identify skills by type (ocas-*, util-*, protected, auto-generated).
  NOT for: building or debugging a skill's own scripts (that is not a library task),
  running code autofix on skill source, or writing arbitrary code unrelated to the skill library.
metadata:
  author: Indigo Karasu (indigokarasu)
  version: "3.7.0"
  merged-from: ocas-critique
  hermes:
    category: software-development
    tags:
      - skill-maintenance
      - audit
      - critique
      - library-hygiene

source: https://github.com/<agent-handle>/skilllab
includes:
  - references/**
  - scripts/**

triggers:
  - skilllab
  - audit skills
  - clean up skills
  - merge skills
  - rename skill
  - delete skill
  - skill library
  - consolidate skills
  - frontmatter check
  - publish skill
  - sanitize skill
  - skill has secrets
  - security scan
  - credential refactor
  - remove inline credential references
  - critique skill
  - score skill
  - evaluate skill
  - skill review
  - skill scoring
  - rubric evaluation
  - 10khr
  - grind
  - improve skill
  - cross-profile skills
  - koda skills
  - secret scan
  - scan skill for secrets
  - credential leak
---

# skilllab

Skill library maintenance: audit, merge, rename, delete, consolidate, publish, sanitize.

The library should hold class-level umbrellas, not micro-skills — prefer one broad skill with labeled subsections over five narrow siblings.

**Read `references/support-file-map.md` first** — full 60+ entry index with per-task "When to read" pointers.

## Interactive Menu

When invoked interactively, present a menu using the `clarify` tool: Audit, Critique, Merge, Rename, Delete, Publish, Sanitize, Hygiene, Exit. Pattern: `references/interactive-menu.md`.

## 1. Skill Taxonomy

- `ocas-*` — OCAS family, authored by <agent-name>. `util-*` — utility skills, same author.
- No prefix — base/generic; may have external authors.
- **Conventions:** never rename to `ocas-*`/`util-*` unless asked; discover via recursive glob across ALL profiles (why: flat scans silently miss whole profiles); protected = bundled/hub-installed (DO NOT edit); auto-generated (`metadata.hermes.generated_by`) = DELETE; author lives in BOTH `author:` and `metadata.author:`.

## 2. Audit Procedure

Checklist:
- [ ] Auto-generated skills (`generated_by`) flagged
- [ ] Author coverage via YAML parser (never grep — false-positives on "authorization")
- [ ] YAML errors (unescaped markdown, bare `---`)
- [ ] Empty profile stubs; SOUL repo install gap
- [ ] Orphaned reference files; support file map completeness
- [ ] Secret gate CLEAN (`bash scripts/secret-scan.sh <dir>` → exit 0)
- [ ] Public prose: banned taglines, deprecated tools, session-log leaks, reference-file PII (rules: `references/sanitize-public-prose-rules.md`; scrub: `references/skill-sanitize-checklist.md`). Why: references must abstract to reusable knowledge — session filenames and contacts leak private context publicly.

## 3. Critique Procedure

## Critique Workflow

### When to Use

Reviewing/critiquing/auditing a skill; iterating toward a target score; pre-publish quality gate; batch library audits; autonomous 10khr grinding.

Score against the 10-dimension rubric (`references/critique-rubric.md`), fix to 50/50.

**Local eval runner (skillgrade):** Integrate the `skillgrade` CLI tooling for **local, offline evaluation** of a skill's `eval.yaml` suite (`references/evals/eval.yaml`) prior to submitting variants. Run `skillgrade` against the local suite to validate behavior against the challenger variant before it is proposed to Monitor/Fellow — this is the gate between a candidate patch and a formal `ocas-fellow` benchmark. If a skill lacks `references/evals/eval.yaml`, note its absence in the critique rather than skipping evaluation entirely. See `spec-ocas-skill-improvements.md` §1.

Example score row: `| D6 | 3 | rules lack "why" |` — gap named.

| Command | What it does |
|---------|-------------|
| `critique.assess <path>` | Score only |
| `critique.plan <path>` | Score + improvement plan |
| `critique.run <path>` | Score → fix → verify |
| `critique.iterate <path>` | Fix-verify loop until 50/50 |
| `critique.batch [paths]` | Ranked table of multiple skills |
| `critique.perfect <skill>` | Grind one skill to 50/50 |
| `critique.10khr` | Autonomous library grinding |

Critique checklist:
- [ ] Phase 1 Read: full SKILL.md + references + scripts; flag >500 lines; hunt phantom refs AND contradictions (align to authoritative section); check prohibitions for rules encoding failed attempts
- [ ] Phase 2 Score: code ratio first (`python3 scripts/critique_code_ratio.py <path>/SKILL.md`, target <20%); score D1–D10; print table (bands A=40–50 … F=0–9)
- [ ] Phase 3 Categorize each ≤3 dimension issue Critical / Major / Minor (`references/critique-issue-categorization.md`)
- [ ] Phase 4 Plan: Location / Current state / Fix / Impact per issue (`references/critique-improvement-plan-template.md`)
- [ ] Phase 5 Execute Critical→Major→Minor; verify syntax after each edit. For 3+ section extractions use one full-file rewrite (why: sequential patches drift anchors and duplicate headers). Replace absolute paths in moved blocks with `{agent_root}/`.
- [ ] Phase 6 Verify: re-read, re-score, before/after table (`references/critique-audit-checklist.md`)
- [ ] Phase 7 Close every 4/5 and 3/5 gap — apply the rubric's "5" criteria as concrete targets. A 48/50 is NOT done.

Reject rationalizations ("come back later", "skip minors", "good enough"). Marker: `<critique-complete>`.

### 10khr Mode

- [ ] Run `python3 scripts/10khr_cron_verify.py` FIRST in any autonomous pass — its output is authoritative for what to grind (do NOT also import the runner and re-walk mtimes by hand)
- [ ] Assess ALL skills recursively across all profiles before fixing any
- [ ] Grind the single lowest-scoring eligible skill **to 50/50**, re-assess, repeat

Rules:
- **Heuristic is ranking-only.** Its magnitude and direction vs a manual rubric score are unpredictable; never trust its number.
- **Skip rule:** if a skill's SKILL.md is unmodified since `last_run` AND heuristic ≥44, skip it. All unmodified ≥44 ⇒ stop.
- **Scope:** 10khr critiques SKILL.md + references + scripts as a documentation package — it does NOT mean running autofix on script source.
- **Never run `--report-only` when you need the skip rule intact** (why: it rewrites `last_run` to now, making every skill read as modified). Import the module and call `run_full_assessment()` without `save_state` instead.
- Dated narratives behind every rule: `references/skilllab-pitfalls.md` ("Extracted" appendix) + `references/critique-10khr-grind-pitfalls.md`; cron constraints: `references/cron-grind-resilience.md`. When to read: any grind misbehavior.

### Error Handling

| Failure | Symptom | Handling |
|---------|---------|----------|
| Frontmatter won't parse after an edit | `yaml.safe_load` ScannerError; runner drops D1→1, D2→3 | A programmatic slice consumed the closing `---`. Re-insert it at the boundary; validate with `yaml.safe_load(content.split('---')[1])`; re-run the scorer. |
| Degraded read mode | `read_file`/`skill_view` fail cluster-wide | Switch reads to `terminal()` (`cat`/`sed -n`/`grep -n`); writes still work. Do NOT abort. |
| Script `--help` crashes | exits non-zero | Move the help guard BEFORE any module-level side effect (argv read, top-level I/O, dependency import). Verify by execution, not `ast.parse`. |
| Duplicate header after extraction | same `### Heading` twice | Run `grep -nE '^#{2,3} ' SKILL.md`; collapse twins. |
| State claims 50/50 but disk says otherwise | state file vs on-disk mismatch | Re-score the actual files; status ≠ evidence. |
| Bulk edit corrupts many scripts | several scripts stop parsing | Recover `git checkout -- .` per repo. NEVER `git clean -fd` (deletes untracked work). Fix one file at a time, verifying after each. |

## 4. Merge / Consolidate

Right test: would a maintainer write N skills or one skill with N labeled sections? If the latter, merge.

Steps when absorbing B into A:
- [ ] Copy B's support files into A's dirs; append B's content as a labeled section
- [ ] Add `metadata.merged-from: <B>` + B's triggers to A
- [ ] Archive B to `$HERMES_HOME/../indigo/skills/.archive/<B>/`
- [ ] Update all external references (crons, memory, other skills)

Package integrity: never flatten only SKILL.md while leaving support files behind. Parallel-copy dedupe: 7-step superset-verified procedure in `references/merge-parallel-copy-dedupe.md` — read before ANY cross-tree dedupe; never delete a tree until its Step-3 check reports 0 missing files (why: trees diverge silently; blind deletion destroys data).

## 5. Rename

```bash
mv $HERMES_HOME/../indigo/skills/<old-name> $HERMES_HOME/../indigo/skills/<new-name>
```

Update checklist (missing any causes stale refs):
- [ ] In-skill: `name:` frontmatter, heading, self-references, support file map
- [ ] Caches: `.skills_prompt_snapshot.json` + `.usage.json` keys renamed (snippets: `references/rename-cache-updates.md`) — why: stale keys persist in the system prompt until refresh
- [ ] grep old name across skills dir + profile md files; update crons, memories, SOUL/AGENT/USER.md, sibling "When NOT to Use" sections
- [ ] Restart the gateway — clears the injected index/autocomplete; directory/frontmatter names must match 

New skill: create dir → delete `.skills_prompt_snapshot.json` (regenerates; else never indexed) → sibling relationships → cron if scheduled → gateway restart.

## 6. Publish

**Read `source:` BEFORE any repo operation** — monorepo target ⇒ sync the subdir, never create a standalone repo (why: orphan repos the `source:` field doesn't reference).

Workflow: check `source:` → spec compliance (`references/skill-publish-spec-compliance-checklist.md`; agentskills.io requires `name` + keyword-rich `description`; strip Hermes-only extensions) → sanitize PII → standalone only: repo create + LICENSE/README/.gitignore → push → public.

GitHub mechanics:
- Push recipe: `references/skill-publish-github-push-recipe.md`; bulk sync: `references/skill-publish-github-sync-existing-skills.md`
- One authenticated GitHub account ⇒ use it; do not ask which (wasted round-trip)
- If HTTPS push fails on credentials: run `gh auth setup-git` once, retry (why: git isn't using the gh token by default)
- Daily sync: ONE cron `skill-sync-all` (04:00) running `skill-sync-all.sh` (indigo automation dir), superseding the paused `ocas-skilllab-sync` + `monorepo-skill-sync`. Discovers ocas/util/eng skills by rule (`references/skill-sync-discovery.md`); idempotent; sets agent identity.
- Sync gates use `--working-tree` secret-scan mode (full history false-blocks pushes over old committed prose); full mode only for pre-publish audits

Share to Nous optional-skills: full procedure (config-policy gate, category table, prerequisites) in `references/skilllab-share-procedure.md` — When to read: immediately before preparing any submission.

## 7. Secret Scan Gate

Policy: no secrets in local/remote skills except the private backup repo — and even there, secrets belong in env files, not skills. A skill is NOT committable until `bash scripts/secret-scan.sh <dir>` exits 0.

```bash
bash scripts/secret-scan.sh <dir>                        # tree + .git/config + ALL history
bash scripts/secret-scan.sh --working-tree <dir>         # skip history (sync gates)
```

Remediation (history rewrite, rotation): `references/secret-history-rewrite.md` — read when the gate exits 1 on a real secret. False positives = example credential-shaped text: redact or move to a reference. **Output is masked — never grep for the masked string; search the real substring via Python `str.replace()` (why: sed/perl metacharacters silently no-op).**

## 8. Frontmatter Standards

Minimum: `name`, `description`, `license` (right after name), `includes:` if support dirs exist, `triggers:` for discoverability. Nest `metadata.hermes` properly (`metadata:\n  hermes:\n    category:`) — a literal top-level `metadata.hermes:` key still scores D1=4. Full reference: `references/skilllab-frontmatter-standards.md`.

## 9. Pitfalls (Top Rules)

Full list (60+, plus extracted dated narratives): `references/skilllab-pitfalls.md`.


- **50/50 means 50/50** — stopping at 45–48 is the #1 failure mode; close every gap.
- **D5 wants `- [ ]` checklists** for any 3+ step procedure; numbered steps don't count.
- **D6 wants a "why" on every rigid rule** so agents can adapt to edge cases.
- **All scripts need executable `--help`** exiting 0; guard must precede module-level side effects; bash guards define every downstream variable under `set -u`. Pattern: `references/critique-10khr-d9-help-injection.md`.
- **Read the FULL skill before acting** — name/description guesses produce wrong moves.
- **Verify superset before deleting parallel trees**; back up to `_backup_<date>/` first. List skills from the filesystem, tersely — never from memory.
- **Edit the LIVE profile skill**, not the indigo-repo backup copy.
- **Re-validate frontmatter after any patch** (leading whitespace breaks YAML).
- **Recursive discovery everywhere** — never `os.listdir()` or flat globs.
- **Cross-profile writes need `cross_profile=True`** after confirming the owning profile.
- **Bulk edits: one file at a time**, verify after each; recover corruption with `git checkout -- .`, never `git clean -fd`.

## 10. External Tool Evaluation & Retired Capabilities

New external tool systems follow `references/tool-integration-pattern.md` (docs → map to existing skills → delegate → build new only at 24+ commands; pitfall: over-integration).

Retire a capability: grep old name → classify refs (prose→replace, section→remove, logs→leave) → rename support files + cache keys → re-grep to confirm zero refs (excluding `.archive/`).
