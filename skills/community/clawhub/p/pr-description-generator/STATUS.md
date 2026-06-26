# pr-description-generator — Status

**Status:** Ready
**Price:** $49
**Created:** 2026-03-30

## What It Does
Auto-generates PR descriptions from git diffs. Parses conventional commits, categorizes changes, rates impact, generates reviewer hints and test checklists. 3 templates (minimal/standard/detailed), markdown or JSON output. Pure Python + git CLI.

## Components
- `scripts/generate_pr_description.py` — main generator
- Tested on real git repository with conventional commits

## Next Steps
- [x] Published to ClawHub (after April 11)
- [ ] Add --gh-create flag to directly create PR via gh CLI
- [ ] Support Jira ticket extraction from branch names
