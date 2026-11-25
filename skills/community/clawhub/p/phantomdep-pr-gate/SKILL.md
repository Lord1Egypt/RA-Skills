---
name: phantomdep-pr-gate
description: Audit only the dependencies a pull request adds — typosquats and lookalike package names, packages that do not exist on npm or PyPI, newborn or barely-downloaded packages, and dependencies added but never imported. Use when asked to check, review or gate a PR's new dependencies in package.json, requirements.txt, pyproject.toml or package-lock.json, when reviewing dependency changes before merging, or when a PR adds a suspicious-looking package name. Not for auditing dependencies a project already has (only added ones are checked), for scanning AI-agent skills (use skillscan), or for checking workflow run: commands (use ci-command-truth).
license: MIT
compatibility: Requires Python 3.11+ and pip. Installing needs network access to GitHub. Auditing is offline by default; live registry lookups happen only with --live.
---

# PhantomDep PR Gate

## What this tool does

PhantomDep compares the dependency manifests at a PR's base and head —
`package.json`, `requirements.txt`, `pyproject.toml`, `package-lock.json`
— and audits only the dependencies the PR adds. Each added dep gets a
verdict from registry evidence (exists, age, weekly downloads), name
similarity to popular packages, and whether the code actually imports
it. Nothing from the PR is installed or executed.

## Install

The `phantomdep` command (standard library only), via pip, pipx or uv:

```bash
pip install git+https://github.com/RakTikoo/phantomdep-pr-gate
# or, isolated:
pipx install git+https://github.com/RakTikoo/phantomdep-pr-gate
# or with uv:
uv tool install git+https://github.com/RakTikoo/phantomdep-pr-gate
```

Not on PyPI — the git URL is the package source. Or use it with no
install at all as a GitHub Action:

```yaml
uses: RakTikoo/phantomdep-pr-gate@v0.3.0
```

Or clone the repo and run the single file directly:

```bash
git clone https://github.com/RakTikoo/phantomdep-pr-gate
cd phantomdep-pr-gate
python3 phantomdep.py --base origin/main --head HEAD --live
```

There is also a pre-commit hook (see the README).

## Run

Audit a PR from git refs (live registry lookups):

```bash
phantomdep --base origin/main --head HEAD --live
```

Or compare two manifest snapshots, offline against registry fixtures:

```bash
phantomdep --base-dir path/to/base --head-dir path/to/head --registry-fixtures path/to/registry-fixtures
```

Add `--json` for a machine-readable report, or `--comment-out file.md`
to write the PR-comment Markdown. A saved unified diff can be audited
with `--diff-file pr.diff --head-dir .`.

## Reading the results

Note the exit policy — it is this tool's own, not the usual pattern:

- `0` — nothing blocks. Warnings may still be present: `NEWBORN`,
  `LOW-DOWNLOADS`, `UNUSED` (added but never imported) and
  `TYPO-LOOKALIKE` are warnings, noted in the output.
- `1` — blocking: at least one added dep is `NOT-FOUND` on its registry
  or a blocking `SUSPECT-TYPO` (a young, low-download lookalike of a
  popular package). Do not merge until it is explained or removed.
- `2` — usage or input error: a manifest that is present but
  unparseable or oversized, invalid TOML, or a bad path. No audit ran.

Each result line names the dep, registry, manifest and section, its
verdicts, and the evidence (exists, age, weekly downloads, imported).
Non-registry specs (`workspace:`, `file:`, `git+`, direct URLs) are
`SKIPPED-NONREGISTRY` — listed separately, never flagged, never
affecting the exit code. The JSON report carries `results`, `notes`,
`exit_code`, `tool` and `version`.

Offline honesty: without `--live` and without `--registry-fixtures`,
every registry field is reported as `unknown` — the tool never guesses
offline, so an offline run cannot prove a dep exists.

## Limits

- Only added dependencies are audited — version bumps of existing deps
  and deps removed by the PR are out of scope.
- `overrides` / pnpm `overrides` in package.json are not parsed.
- Lockfile support covers package-lock.json v2/v3 direct deps only;
  v1 is not read (a note is printed).
- Caps: 100 manifests per comparison and 200 added deps per run;
  beyond the dep cap, deps are `NOT-AUDITED` and the audit is flagged
  incomplete.
- Manifests under fixtures/, examples/ and docs/ are audited like any
  other — scope the scan if a repo keeps fake deps there on purpose.
