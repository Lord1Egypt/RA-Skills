---
name: github-release-analyzer
version: 0.0.4
description: Analyze GitHub repository releases and summarize release notes. Use when the user asks to analyze, summarize, review, or track the latest release or recent releases for a GitHub repo, including phrases like "分析最新 release", "latest release", "release 更新了什么", "汇总仓库 release", or requests to build a cron that tracks GitHub releases. Supports manual one-off analysis and cron-driven incremental tracking.
metadata:
  {"openclaw":{"emoji":"📦","requires":{"bins":["python3"]}}}
---

# GitHub Release Analyzer

Use this skill as a fixed pipeline:

```text
prepare -> summarize -> render -> deliver -> commit
```

Only `summarize` is free-form. `prepare`, `render`, and `commit` are deterministic script steps.

## Inputs

- Repo input: `https://github.com/<owner>/<repo>` or `<owner>/<repo>`
- Default `stateKey`: `{owner}__{repo}`
- Default template: `default`
- Default behavior:
  - manual: latest formal release only, no state read/write
  - cron: formal releases only, first run selects latest only, later runs select unprocessed only

## Workflow

1. Read `references/execution-modes.md` and choose `manual` or `cron`.
2. Run:

```bash
python3 skills/github-release-analyzer/scripts/run.py prepare --repo <repo> --mode <manual|cron>
```

Useful flags:

- `--state-key <key>`
- `--limit <n>`
- `--include-prerelease`
- `--output-template default`
- `--initial-cron-behavior latest-only`

3. If `status=has_updates`, read `references/summary-contract.md` and produce one summary string per selected release.
   Keep the summary language aligned with the primary language of the invocation instruction.

4. Render the final message:

```bash
python3 skills/github-release-analyzer/scripts/run.py render --repo <repo> --mode <manual|cron> < payload.json
```

When building the `render` payload, preserve the release fields required by `render`, especially `tag_name`, `published_at`, and `html_url`.

5. In cron mode, after successful delivery, commit state:

```bash
python3 skills/github-release-analyzer/scripts/run.py commit \
  --repo <repo> \
  --mode cron \
  --processed-tags <comma-separated-tags> \
  --latest-release-id <id> \
  --latest-published-at <iso8601>
```

## Rules

- Treat `prepare` output as the source of truth for selection, ordering, first-run behavior, repo normalization, and state path.
- The output language must follow the primary language of the invocation instruction.
- The final outgoing message must come from `render`.
- In cron mode:
  - if `status=no_update` or `status=no_release`, reply with `NO_REPLY`
  - if `status=has_updates`, emit only the final rendered message
- Update processed state only after successful delivery.

## Hard prohibitions

- Do not skip `prepare`.
- Do not bypass `render`.
- Do not reorder or silently drop releases selected by `prepare`.
- Do not call `commit` in manual mode.
- Do not call `commit` before delivery succeeds in cron mode.
- Do not replace the summary contract with ad hoc prose outside the required `summaries[]` string-array shape.
- In cron mode, when `status=no_update` or `status=no_release`, reply exactly `NO_REPLY`.
- In cron mode, do not emit progress chatter, intermediate JSON, step labels, or workflow narration.

## Files to read

- `references/execution-modes.md`
- `references/summary-contract.md`
- `references/templates.md`
- `references/state-format.md`
