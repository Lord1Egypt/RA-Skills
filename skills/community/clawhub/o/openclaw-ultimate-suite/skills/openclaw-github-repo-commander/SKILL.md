---
name: github-repo-commander
homepage: https://github.com/wd041216-bit/openclaw-github-repo-commander
description: Orchestrate GitHub repository cleanup, README polish, presentation upgrades, discoverability improvements, privacy checks, model-agnostic refactors, and awesome-list PR prep in one unified workflow.
---

# GitHub Repo Commander

Use this skill when a GitHub repository should be improved as a whole, not just in one narrow dimension.

This skill now subsumes the old split between:

- GitHub presentation polish
- README and first-screen cleanup
- discoverability and metadata work
- privacy and open-source readiness checks
- model-agnostic compatibility cleanup
- curated-list / awesome-list submission prep

It adds the missing governance layer:

- privacy and open-source readiness checks
- local path / token leak scanning
- skill metadata compliance checks
- model-agnostic refactor guidance
- awesome-list / curated-list contribution prep

It also covers the presentation layer directly:

- repo description clarity
- README hero and first-screen quality
- screenshots, demos, and visual hierarchy
- topics, homepage, and GitHub metadata
- repo packaging for portfolio or community discovery
- bilingual documentation hygiene for public-facing repos
- upgrade-note discipline so visible capability changes are documented

## What this skill is for

Use it when the user wants to:

- audit a repo before open-sourcing
- make a repo cleaner and more presentable on GitHub
- improve README, visual hierarchy, and project packaging
- improve discoverability and recommendation readiness
- merge improvements from another fork or branch without losing structure
- remove model-specific assumptions from prompts or scripts
- prepare a repo or skill for submission to an awesome-list
- upgrade an existing GitHub workflow skill into something more complete

## Commanding workflow

1. Inspect the repo with `gh` when the remote exists.
2. Run the privacy/compliance audit script.
3. Fix critical open-source blockers first:
   - tokens
   - `.env`
   - local machine paths
   - accidental personal data
4. Then improve packaging and discoverability:
   - repo description
   - README first screen
   - bilingual README coverage when the repo serves both Chinese and international readers
   - screenshots / demo / topics
   - visual hierarchy
   - social preview / portfolio positioning when relevant
5. If the repo changed in a user-visible way, update the public docs at the same time:
   - `README.md`
   - `README.zh-CN.md` when the repo uses a Chinese doc track
   - `CHANGELOG.md` or release notes for meaningful upgrades
6. If the repo is skill-like, verify:
   - `SKILL.md` frontmatter
   - `skill.json`
   - `_meta.json` when required by the target ecosystem
7. If the repo is too model-specific, refactor toward model-agnostic behavior:
   - generic instructions
   - explicit capability assumptions
   - graceful degradation for smaller or local models
8. If the target is an awesome-list:
   - normalize repository URL
   - verify alphabetical placement
   - update counters or section summaries if needed

## Built-in audit script

Run:

```bash
python3 ./scripts/repo_commander_audit.py /path/to/repo
```

Useful flags:

```bash
python3 ./scripts/repo_commander_audit.py /path/to/repo --json
python3 ./scripts/repo_commander_audit.py /path/to/repo --strict
```

The script checks for:

- `.env`, secrets, token-like strings
- leaked local paths with personal usernames or machine-specific home directories
- missing skill metadata files
- obviously model-specific wording
- README presence and basic packaging issues
- bilingual README coverage and cross-link expectations
- changelog / upgrade-note presence for public package-style repos

## How to combine it

Use together with:

- `github` for live repo inspection and metadata updates
- `readme-generator` when the README needs a serious rewrite
- `ai-discoverability-audit` when visibility and recommendation presence matter
- `frontend-design` and `ui-ux-pro-max` when a repo needs stronger visual taste

`github-repo-polish` can still exist as a narrower legacy skill, but this skill should be the main front door for GitHub work.

## Commander rules

- Fix safety and privacy problems before beautifying the repo
- Once safety is acceptable, actively improve the repo's presentation instead of stopping at compliance
- If the upgrade changes visible behavior, update the docs in the same pass instead of treating docs as optional follow-up
- Prefer a bilingual README policy for repos that are actively shared with both Chinese-speaking and international users
- Keep open-source repos free of local deployment details
- Prefer human-readable GitHub positioning over keyword stuffing
- Keep PR fixes focused and easy to review
- Treat model-agnostic design as compatibility work, not branding language

## Output expectations

When you use this skill well, the result should usually include:

- critical findings first
- a proposed remediation plan
- concrete README / metadata / discoverability changes
- any metadata / README / topic updates
- if relevant, a PR-ready awesome-list entry or ordering note
