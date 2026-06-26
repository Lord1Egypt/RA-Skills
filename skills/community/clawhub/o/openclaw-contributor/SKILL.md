---
name: openclaw-contributor
description: Contribute to the OpenClaw core repository using the repo's own CONTRIBUTING.md rules. Use when working in `openclaw/openclaw` or a fork to triage issues, plan a focused fix, choose the right validation commands, prepare AI-assisted PRs, route changes to the right subsystem maintainers, or avoid breaking OpenClaw contribution norms.
---

# OpenClaw contributor

Contribute to OpenClaw the way the repo expects.

Start by reading the repo-root `CONTRIBUTING.md` in the target checkout. Treat it as the source of truth over generic PR habits.

## Workflow

1. Confirm scope.
   - Small bugfixes and focused docs fixes can go straight to a PR.
   - New features, large refactors, or architecture changes should start with a GitHub Discussion or Discord conversation first.
2. Inspect the changed area before editing.
   - Read nearby implementation and tests.
   - Look for existing branch/work in `upstream/*` before duplicating effort.
3. Generate a validation plan.
   - Run `scripts/recommend_checks.py --repo <openclaw-repo>`.
   - Use its output to choose validation commands and maintainer routing hints.
4. Keep the patch tight.
   - One logical change per PR.
   - Add or update regression tests with the fix when possible.
   - Avoid mixing runtime fixes, refactors, docs, and feature work in one branch.
5. Validate before opening the PR.
   - Default expectation from OpenClaw is:
     - `pnpm build`
     - `pnpm check`
     - `pnpm test`
   - For docs-only or subsystem-specific work, use the slimmer commands recommended by `scripts/recommend_checks.py`.
6. Prepare the PR for maintainers.
   - Explain what changed and why.
   - Mark AI-assisted work in the PR title or description.
   - State testing level clearly.
   - Include screenshots for UI or visual changes.
   - Optionally generate a draft with `scripts/generate_pr_body.py`.

## Non-negotiables

- Follow `CONTRIBUTING.md`, not generic habits.
- Keep PRs focused.
- Prefer source-level fixes over patching built artifacts.
- Add tests for regressions when practical.
- Be transparent about AI assistance.
- For UI changes, preserve Control UI legacy decorator style unless the build tooling is intentionally being changed too.

## Use bundled resources

- `references/contributing-checklist.md`
  - Read when you need the distilled OpenClaw-specific PR checklist, maintainer hints, or validation command matrix.
- `references/pr-template.md`
  - Read when you need a maintainer-friendly OpenClaw PR structure with AI-assistance disclosure and validation sections.
- `scripts/recommend_checks.py`
  - Run in an OpenClaw checkout to derive recommended validation commands and maintainer hints from the actual diff.
  - Example:
    - `python3 skills/openclaw-contributor/scripts/recommend_checks.py --repo /path/to/openclaw`
    - `python3 skills/openclaw-contributor/scripts/recommend_checks.py --repo /path/to/openclaw --base upstream/main --json`
- `scripts/generate_pr_body.py`
  - Generate a PR-body draft using the diff-aware recommendations.
  - Example:
    - `python3 skills/openclaw-contributor/scripts/generate_pr_body.py --repo /path/to/openclaw --title "fix(web-search): honor OpenRouter-backed Perplexity runtime path" --summary "Honor OpenRouter-backed Perplexity config in runtime web_search path" --why "Current runtime ignores configured baseUrl and sends OpenRouter keys to Perplexity direct"`

## Related skills

If they are available locally, use them alongside this skill:

- `github` for GH CLI operations
- `Pull Request` before opening the PR
- `code-review` before final submission or while addressing review comments

## Output standard

When asked to contribute upstream, finish with:

- branch name
- files changed
- validation run (or what remains and why)
- PR/discussion recommendation
- any maintainer/subsystem routing hints
