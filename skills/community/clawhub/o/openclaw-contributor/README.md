# OpenClaw Contributor

[![ClawHub](https://img.shields.io/badge/ClawHub-openclaw--contributor-7A2CF5)](https://clawhub.ai/manjaroblack/openclaw-contributor)
[![GitHub release](https://img.shields.io/github/v/release/manjaroblack/openclaw-contributor-skill?display_name=tag)](https://github.com/manjaroblack/openclaw-contributor-skill/releases)
[![GitHub](https://img.shields.io/badge/GitHub-manjaroblack%2Fopenclaw--contributor--skill-181717?logo=github&logoColor=white)](https://github.com/manjaroblack/openclaw-contributor-skill)

Contribute to the OpenClaw core repository the way the repo actually expects.

This skill helps with upstream OpenClaw work in `openclaw/openclaw` or a fork: scope checks, validation planning, PR prep, AI-assistance disclosure, and maintainer-friendly handoff.

## Install

```bash
clawhub install openclaw-contributor
```

ClawHub page:

- https://clawhub.ai/manjaroblack/openclaw-contributor

GitHub repo:

- https://github.com/manjaroblack/openclaw-contributor-skill

## What it does

- Tells the agent to start with the target repo's `CONTRIBUTING.md`
- Keeps changes focused instead of mixing unrelated work
- Recommends validation commands before opening a PR
- Encourages regression tests where practical
- Generates maintainer-friendly PR bodies and routing hints
- Calls out OpenClaw-specific UI and contribution norms

## Included resources

- `SKILL.md` — main workflow and rules
- `references/contributing-checklist.md` — distilled checklist and validation matrix
- `references/pr-template.md` — PR structure with AI-assistance disclosure
- `references/example-perplexity-check-plan.txt` — example validation planning artifact
- `scripts/recommend_checks.py` — diff-aware validation recommendations
- `scripts/generate_pr_body.py` — draft a PR body from repo context

## Typical usage

Use this when you want an agent to:

- triage an OpenClaw issue
- plan a tight upstream fix
- choose the right validation commands
- prepare an AI-assisted PR without annoying maintainers
- route work to the right subsystem owners

## Example prompts

- "Help me contribute a fix to openclaw/openclaw."
- "Plan the validation steps for this OpenClaw PR."
- "Draft a maintainer-friendly PR body for this OpenClaw change."
- "Figure out which checks I should run before opening this upstream PR."

## Versioning

Published on ClawHub as `openclaw-contributor`.

Use the GitHub releases page for repo-level notes and the ClawHub changelog for published skill version history.
