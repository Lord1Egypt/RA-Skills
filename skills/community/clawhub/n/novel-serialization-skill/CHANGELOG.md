# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0] - 2026-10-17

### Added
- `.refsignore`: the reference-check exemption list, one regex per line with
  the reason next to it. Read by default by `scripts/check_refs.py`, so a local
  run, the pre-commit hook and CI judge the same tree instead of CI carrying a
  private `--ignore` string that nothing else saw.
- `check_refs.py --ignore-file` (default `.refsignore`, `''` disables) and a
  new eighth bucket, `PRIVATE_MISSING`.

### Changed
- `PRIVATE_MISSING` splits "target does not exist" by source: from a release
  file it stays `MISSING`, from a report or working note it becomes
  `PRIVATE_MISSING` and is listed but never gated on. That split is what makes
  the next item possible.
- CI and pre-commit now gate on `NONRELEASE,MISSING` instead of `NONRELEASE`
  alone. The release tree had 21 dangling references, all of them paths this
  repository only *describes* — subproject state files, example manuscripts,
  and the seed file's instructions written from a subproject's point of view.
  Every one is now declared in `.refsignore` with its reason, and a new one
  fails the build instead of being quietly filtered by a CI-only flag.

## [1.3.0] - 2026-10-17

### Added
- `tests/`: regression suite for the shared scripts — 34 tests covering the
  release-only reference rule (`check_refs`), the hygiene scanner
  (`scan_hygiene`), the subproject scaffold (`init_subproject`) and the
  de-AI-tone gate (`humanizer_check`). Run with `pytest`, or via
  `python scripts/dev.py test`.
- `scripts/dev.py`: one entry point for every local gate — `test`, `hygiene`,
  `refs`, `lint`, `scaffold`, `all`. Exits with the first failing gate's code.
- `Makefile`: thin proxy to `scripts/dev.py` for contributors who have make.
  Windows contributors call `scripts/dev.py` directly.
- `pyproject.toml`: project metadata plus `[tool.pytest.ini_options]` and
  `[tool.ruff]`; `requirements-dev.txt` for the development-only dependencies.
- `docs/`: engineering documentation directory with an ADR index
  (`docs/adr/README.md`) and three records — 0001 reports are not released,
  0002 release files reference release files only, 0003 dual-track chapter
  naming. The directory holds decisions, not reports.
- `security.txt` (RFC 9116): machine-readable contact for security tooling,
  mirroring `SECURITY.md`.
- `.github/workflows/codeql.yml`: CodeQL scan (`security-extended`) on push,
  pull request and a weekly schedule.
- `.pre-commit-config.yaml`: `conventional-pre-commit` on the `commit-msg`
  stage, plus local hooks for `check_refs.py` and `pytest`.
- `.gitattributes`: binary markers for image and archive types, and linguist
  overrides (`CITATION.cff` counted as YAML, generated audit reports excluded).

### Changed
- `.github/workflows/ci.yml`: new `tests` job (`pip install -r
  requirements-dev.txt && pytest`); the required-community-files check now also
  asserts `security.txt`, `pyproject.toml`, `requirements-dev.txt`, `Makefile`,
  `docs/README.md`, `docs/adr/README.md` and `tests/conftest.py`.
- `CONTRIBUTING.md`: added a Development Environment section (`requirements-dev.txt`,
  `pre-commit install --hook-type commit-msg`, `python scripts/dev.py all`); step 4 of
  the workflow now names the four gates instead of claiming no validation tooling
  exists; the project-structure tree lists `docs/`, `tests/`, `scripts/` and the
  full `.github/` tree.
- `README.md`: new Development section with the gate table; directory structure
  updated; link to the ADR index from the Subprojects section.

### Fixed
- `SECURITY.md` supported-versions table listed 1.1.x and 1.0.x as supported
  after 1.2.0 shipped. Now 1.3.x supported, 1.2.x security-only, older lines
  unsupported, with a pointer to `security.txt`.
  textual layer) → 复审 (编辑部主任, content layer) → 终审 (主编, full-dimension regression
  + read-through sign-off). One-way flow; a later stage may overturn an earlier verdict with
  a written reason, never the reverse; any `FAIL` blocks `_promote_draft.py` until 终审 signs off.
- `scripts/review_all.py`: new `--stage first|second|final` runs only that stage's dimensions,
  titles the report per stage, prints the next-step flow hint, and emits a per-stage signature
  block. Running without `--stage` keeps the legacy all-in-one behaviour (unchanged).
- `scripts/_review_lib.py`: `STAGES` / `STAGE_DIMS` / `STAGE_KEYS` (single source of truth for
  the stage→dimension mapping, roles and exit gates), plus `stage_label()`, `stage_dims()`,
  `stage_intro()`, `signoff()`; `render()` gained a `stage=` argument that selects the matching
  signature block.
- `references/method-patterns-publishing.md` §7 "Three-Stage Review": roles, dimensions,
  commands, per-stage verdict semantics, flow rules, and where the definitions live.

### Changed
- `SKILL.md` `## Verification Gates`: the flat "Review gate" checklist item became a three-stage
  quick-reference table (stage → role → dimensions → exit gate) plus the checklist; long-form
  rules and commands moved to `references/method-patterns-publishing.md` §7 per the
  "SKILL.md is index + quick-reference only" rule.
- `scripts/README.md` and `SUBPROJECTS.md`: gate wording updated to the three-stage flow
  (per-stage invocation, per-stage archived reports, promotion gated on 终审 sign-off).

### Fixed
- `scripts/_review_lib.py` `emit()`: report write-back now uses `newline='\n'`, matching the
  project's Windows write rule (scripts/README.md "落盘守则"); previously a stage report could
  be written with CRLF and fail `scan_hygiene.py --fail-on crlf`.

## [1.2.0] - 2026-10-07

### Added
- `.gitignore` and `.editorconfig` (were missing from the generated project)
- `LICENSES/CC-BY-NC-SA-4.0.txt` with the official Creative Commons license text
- `README_FOR_AI_Audit_Report.md` recording the post-generation compliance audit
- `CONTRIBUTING.md`: Recognition Policy section (required by spec Section 7.6)
- `references/method-patterns.md`: Style Consistency Rules row in the split index
- `README_FOR_AI_Audit_Report_Round2.md`: content-level re-audit (12 further defects)
- `CONTRIBUTING.md`: Review Process and Markdown linting rules (required by spec Section 7.6)
- `.github/workflows/novel-release.yml`: the licence gate now inspects chapter content for the
  CC BY-NC-SA 4.0 header, and the continuity gate now fails when the module or required
  `state/` files are missing
- `references/method-patterns-publishing.md`: documented the frontmatter-vs-CC-header ordering
- `references/examples/example-chapter-draft.md`: added the mandatory YAML frontmatter
- `README_FOR_AI_Audit_Report_Round3.md`: cross-document consistency audit (6 further defects)
- `scripts/` (shared automation, consumed by novel subprojects): `humanizer_check.py`
  (de-AI-tone gate: AI-tone density, structural/abstract clichés, vague adverbs, emotion labels,
  formulaic patterns, ending-elevation, idiom runs, punctuation density, paragraph-length CV —
  PASS/WARN/FAIL), `_list_hits.py` (lists flagged sentences for manual rewrite),
  `_promote_draft.py` (draft → release sync with pre-write snapshot, word-count diff, zero-diff
  chapter-title check, humanizer gate), `_sync_draft.py` (release → draft write-back, errata only),
  plus `scripts/README.md` documenting invocation conventions
- `SUBPROJECTS.md`: registry of independent novel subprojects (own git repo and remote) —
  currently `-1928` (《奉天1928》) — and the rule that scripts stay in this repo, never copied
  into a subproject as `tools/`
- `README.md`: `scripts/` and `SUBPROJECTS.md` added to the directory structure, plus a
  Subprojects section; `SKILL.md` cross-references both
- `scripts/_promote_draft.py`: project root resolved from the current working directory
  (new `--root` flag) instead of the script's parent directory; `humanizer_check.py` located
  relative to the script's own directory, so the script works from any subproject
- `scripts/`: review-gate script family — `review_all.py` (runs every gate in one pass and emits a
  single review report: verdict table, issue detail, scale overview, TODO list, sign-off block),
  `review_scale.py` (per-chapter word count vs target, pass rate, gap ranking),
  `review_continuity.py` (name variants, character age vs dossier, timeline reversal,
  title/body mismatch, timeline entries, draft-vs-release title parity),
  `review_rationality.py` (duplicate paragraphs, paragraph shape, dialogue ratio, ordinal gaps,
  POV drift, unresolved foreshadowing, outline coverage), `review_punctuation.py` (quote pairing,
  half-width punctuation, straight quotes, traditional-character leaks, stray English, punctuation
  density), plus the shared `_review_lib.py`. All accept `--root`, `--chapters`, `--draft`, `--out`
  and work with both `ch-001-title.md` and `第NNN章 标题.md` naming; thresholds were calibrated
  against real manuscript text to keep false positives low
- `scripts/check_refs.py`: reference integrity check with seven buckets
  (`OK` / `LOCAL` / `TEMPLATE` / `BARE` / `PRIVATE_OK` / `NONRELEASE` / `MISSING`).
  **Release files reference release files only; non-release files may reference anything** —
  a private target referenced from a release file is `NONRELEASE` (defect), the same target
  referenced from a report or working note is `PRIVATE_OK` (allowed). Backtick paths
  resolve from the repository root, real links (a label in `[]` followed by a
  target in `()`) resolve relative to the file —
  the two systems are deliberately kept apart. URL-encoded links (`%20`) and root-absolute
  links (leading `/`) are resolved the way GitHub resolves them. Supports `--root`, `--kind`,
  `--ignore`, `--fail-on`, `--json`, `--out`
- `scripts/scan_hygiene.py`: file hygiene scan — CRLF, mojibake, junk files, empty files,
  missing trailing newline, line budget. `--fix` rewrites CRLF files as LF in place;
  `--allow` declares line-budget exemptions; `--fail-on` selects the blocking checks
- `scripts/init_subproject.py`: subproject scaffold generator — directory skeleton,
  issue forms (chapter claim / errata / creative proposal / hygiene), PR template,
  CODEOWNERS, decision ledger, report index, layered-memory entrance. `--dry-run` and
  `--force` supported; existing files are never overwritten by default
- `references/subproject-playbook.md`: field-tested subproject conventions distilled from
  the `-1928` subproject (288 released chapters, 227 reports, 558+ ledger rulings) —
  directory layout, what replaced `state/`, decision ledger, three-index report rule,
  layered memory, LF write discipline, reference integrity, honest 500-line policy
- Gap analysis of this repository against real subproject use — 19 defects graded
  P0/P1/P2 across three classes (spec vs. practice, script capability, community
  engineering). The report itself is a working artefact and is not committed
- GitHub community engineering files: `.github/CODEOWNERS`, `SUPPORT.md`,
  `GOVERNANCE.md`, `CITATION.cff`, `.github/labels.yml`, `.github/release.yml`,
  `.github/workflows/ci.yml`, `.github/workflows/label-sync.yml`,
  `.github/workflows/stale.yml`, `.github/ISSUE_TEMPLATE/errata.yml`,
  `.github/ISSUE_TEMPLATE/docs.yml`, `.github/PULL_REQUEST_TEMPLATE/content.md`,
  `.markdownlint.json`, `.pre-commit-config.yaml`

### Changed
- `SKILL.md`: chapter naming is now explicitly dual-track — `ch-{number}-{title}.md` is the
  default, subprojects may register their own convention; volume/arc directories recognised;
  `state/` may be replaced by the playbook layout provided one home per state kind is chosen;
  500-line rule now has declared exemptions
- `CONTRIBUTING.md`: 500-line rule gained an explicit exemption table (ledger / log,
  reference table, generated seed) — exemptions must be declared via `scan_hygiene.py --allow`
- `scripts/README.md`: three new scripts catalogued, plus the Windows LF write discipline
  and ready-to-paste invocation examples
- **Reports are no longer committed.** Working reports live in `.workbuddy/reports/`
  and are excluded by `.gitignore`. Release files (`SKILL.md`, `README.md`, `CONTRIBUTING.md`,
  `SUBPROJECTS.md`, `SUPPORT.md`, `CHANGELOG.md`) do not reference them, which is what the
  release-only-references-release rule requires
- `references/glossary.md`: root-absolute example paths (`/CODE_OF_CONDUCT.md`) no longer
  carry a leading slash, so they resolve from the repository root
- `references/method-patterns-publishing.md`: `CHANGELOG.md` link corrected to `../CHANGELOG.md`
- `modules/` restructured to `modules/<name>/SKILL.md` per spec Sections 1 and 5.2
- `references/examples/` created and the three worked examples moved into it
- `.github/ISSUE TEMPLATE` renamed to `.github/ISSUE_TEMPLATE` so GitHub detects the forms
- `.gitattributes` now enforces `eol=lf`, matching `.editorconfig`
- All files normalized to LF line endings with a trailing newline
- Version fields aligned to 1.1.2 (all seven SKILL.md files and the README badge)
- `CODE_OF_CONDUCT.md` / `SECURITY.md`: fabricated contact addresses replaced with the
  spec-mandated placeholders
- `.github/workflows/novel-release.yml`: the chapter-format gate can now actually fail, and
  no longer errors when `chapters/` is absent
- The CC BY-NC-SA 4.0 license header ordering rule (frontmatter at byte 0, then the header,
  then narrative) is now stated identically in all 11 files that state it, instead of only in
  `references/method-patterns-publishing.md`. This closes a contradiction introduced by the
  ordering fix itself: `prompts/02-robustness-checks.md` previously instructed reviewers to
  reject compliant chapter files
- Root `SKILL.md` no longer calls chapter frontmatter optional while the publishing template
  makes it mandatory
- World-building and character sheet paths in the two modules now match the root `SKILL.md`
  conventions instead of contradicting them
- `state/location-states.md` added to the root state inventory, which the continuity-tracker
  module already required
- Chapter filename examples zero-padded to 3 digits everywhere, so lexical sort equals numeric
  sort
- Continuity reports now go to `state/continuity-reports/` instead of the Git-ignored `drafts/`
- Root `SKILL.md` Continuity State table: state-file ownership realigned to the continuity tracker
- All six module SKILL.md files: sibling modules relabelled from "Sub-Skills"/"branch skills"
  to "Related Modules" (peers), and the path column converted to resolving relative links
- `README.md`: architecture diagram rebuilt on a uniform 68-column grid
- `CONTRIBUTING.md`: dual-mode wording corrected so it no longer contradicts itself

### Fixed
- `scripts/humanizer_check.py` and `scripts/review_rationality.py` were stored with CRLF
  line endings, contradicting `.gitattributes` and `.editorconfig`. Both normalised to LF.
  Root cause documented in `scripts/README.md`: `io.open(p, 'w', encoding='utf-8')` defaults
  to `newline=None`, which converts LF back to CRLF on write — always pass `newline='\n'`
- All `[OWNER]` / `[REPO]` / `[YOUR_GITHUB_USERNAME]` placeholders replaced with the real
  owner, so clone and install commands are directly executable
- `README.md` directory structure no longer lists `README_FOR_AI_Audit_Report*.md`; those
  reports are generated on demand and excluded by `.gitignore`
- `SUBPROJECTS.md`: `-1928` status updated (288 chapters released, not 55)
- Broken internal links in `references/method-patterns.md` (raw space + wrong anchor)
  and `prompts/01-implement-method.md` (pointed at the wrong README)
- Three module SKILL.md files referencing example files that do not exist in the spec tree
- `CHANGELOG.md` compare links, which were missing the owner path segment
- Headings rendered as literal text in five files (no preceding blank line)
- `CONTRIBUTING.md`: branch prefix unified to `feat/`, missing TOC entry added
- `CONTRIBUTING.md` no longer tells contributors to run `validate.py` or `tests/` (neither exists)
- `CONTRIBUTING.md`: leftover `feature/` branch prefix unified to `feat/`
- `references/method-patterns-publishing.md`: malformed `poV:` frontmatter key corrected to `pov:`
- `modules/chapter-writing/SKILL.md`: the undefined "continuity state header" term now points at
  the concrete frontmatter defined in the publishing template
- `SECURITY.md`: GitHub's template boilerplate sentence replaced with real content
- `README.md`: directory tree was missing `.gitattributes` and the audit reports
- `references/examples/example-chapter-draft.md`: word-count claim no longer states 4,500 words
  of prose that the file does not contain

## [1.1.2] - 2026-09-14

### Changed
- Updated README FOR AI.md metadata version to 1.1.2
- Updated license policy documentation for clarity
- Improved runtime output language specification

### Fixed
- Corrected file naming convention note in README
- Fixed license header references in prompt templates

## [1.1.1] - 2026-09-10

### Changed
- Refactored module structure for improved modularity
- Updated SKILL.md frontmatter with dual license declarations
- Improved glossary definitions in references/

### Fixed
- Fixed broken cross-references in method-patterns.md
- Corrected module trigger descriptions

## [1.1.0] - 2026-09-05

### Added
- Added `continuity-tracker` module for state tracking and memory persistence
- Added `method-patterns-continuity.md` split module
- Added `example-chapter-draft.md` worked example
- Added GitHub Actions release workflow template
- Added dependabot configuration
- Added FUNDING.yml for community support

### Changed
- Split `method-patterns.md` into sub-modules per the 500-line rule
- Updated project directory structure documentation
- Improved prompt templates with output language instructions

### Fixed
- Fixed continuity state tracking inconsistencies
- Corrected version numbering in YAML frontmatter

## [1.0.0] - 2026-08-28

### Added
- Initial release of GitHub Novel Serialization Skill
- Core SKILL.md index and quick-reference
- `references/method-patterns.md` master template file
- `prompts/` dual-mode prompt templates (implement-method, robustness-checks)
- Functional modules:
  - `worldbuilding/` — World-building sub-skill
  - `character-design/` — Character design sub-skill
  - `chapter-writing/` — Chapter writing sub-skill
  - `continuity-check/` — Continuity & consistency verification sub-skill
  - `publishing-workflow/` — GitHub publishing & release sub-skill
- Example files: worldbuilding, character sheet, chapter draft
- GitHub community health files (ISSUE_TEMPLATE, PULL_REQUEST_TEMPLATE)
- .gitignore and .editorconfig
- Dual licensing: GPL-3.0 + CC BY-NC-SA 4.0
- CODE_OF_CONDUCT.md, CONTRIBUTING.md, SECURITY.md, CHANGELOG.md

---

[Unreleased]: https://github.com/JohnSmithfan/github-novel-serialization-skill/compare/v1.4.0...HEAD
[1.4.0]: https://github.com/JohnSmithfan/github-novel-serialization-skill/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/JohnSmithfan/github-novel-serialization-skill/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/JohnSmithfan/github-novel-serialization-skill/compare/v1.1.2...v1.2.0
[1.1.2]: https://github.com/JohnSmithfan/github-novel-serialization-skill/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/JohnSmithfan/github-novel-serialization-skill/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/JohnSmithfan/github-novel-serialization-skill/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/JohnSmithfan/github-novel-serialization-skill/releases/tag/v1.0.0
