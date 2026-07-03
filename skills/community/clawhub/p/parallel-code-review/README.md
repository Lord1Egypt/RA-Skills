# parallel-code-review

[![Category](https://img.shields.io/badge/Category-Development-blue)](https://clawhub.ai/skills?category=development)

Parallel code review — dispatches two subagents to audit **runtime safety** (resource leaks, null paths, race conditions) and **architecture consistency** simultaneously, then merges and deduplicates into a single report. One pass covers two orthogonal bug dimensions.

## Install

```bash
git clone https://github.com/<your-org>/parallel-code-review.git \
  ~/.pi/agent-code/skills/parallel-code-review
```

Or copy `SKILL.md` into a same-named folder under your skills directory.

## Usage

Say `"review"` / `"code review"` / `"审查"` in any skill-aware agent. Defaults to reviewing all commits on the current branch not yet on upstream. Optionally specify a range: `"review origin/main..HEAD"`.

Pipeline: resolve scope → rapid scan → parallel dual-lens review → synthesis.

## Output

```
## Overview
Reviewing feat/my-branch (origin/main..HEAD): 6 commits, 98 files, +7763/-5965.

## Issues
app/manager.py:L90: 🔴 bug: _release_service doesn't null ref, zombie state on retry. Add setattr(... None).
alg/.../service.py:L82: ⚠️ arch: init() missing override annotation on parent method.
alg/utils/contours.py:L307: 🟡 risk: contours_to_mask no empty guard. Add if not contours_list.

## Verdict
Ready to merge? After 🔴 fixes
```

## License

MIT
