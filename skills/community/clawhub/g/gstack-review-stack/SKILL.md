---
name: gstack-review-stack
description: Use this skill when Codex needs gstack-style CEO/product, engineering, design, QA, release, or portfolio-shelf-space review. Trigger for requests like "use gstack", "CEO review", "engineering plan review", "design critique", "QA gate", "ship gate", "which products should we keep", or "decide what to publish/unpublish".
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# GStack Review Stack

Use this skill to bring gstack-style review discipline into Codex and ClawHub workflows without copying the full upstream gstack playbooks into context.

This adapter is original guidance inspired by the public MIT-licensed `garrytan/gstack` project. When exact upstream behavior matters, inspect the local or upstream gstack clone and cite the specific file used.

## Start

1. Run `python3 scripts/find_gstack.py --summary` from the skill folder to locate the local gstack clone and list available upstream skill files.
2. Choose the narrowest review mode that matches the user's request.
3. Load only the reference file needed for that mode:
   - Product, portfolio, scope, or slot decisions: `references/review-rubric.md`
   - Release, QA, or "is this ready to ship": `references/ship-and-qa.md`
   - UI/UX plans or visual quality: `references/design-review.md`
4. If the task involves live publishing, store actions, or irreversible changes, make the recommendation first and only execute after explicit user approval.

## Modes

### CEO/Product Review

Use for strategy, portfolio, scope expansion/reduction, product line focus, and "what should we build/keep/kill?"

Default stance: selective expansion with reduction discipline.

Output:
- Current facts and missing facts
- What is not in scope
- Candidate options
- Green/yellow/red classification
- Named tradeoffs
- Recommended decision and explicit next action

### Engineering Review

Use before implementation or release when architecture, data flow, edge cases, permissions, or maintainability are the risk.

Output:
- Critical paths
- Failure modes
- Test coverage map
- Security/privacy risk
- Performance and maintenance risks
- Blocking fixes before release

### Design Review

Use for UI/UX, landing pages, extension side panels, listing assets, screenshots, and flows.

Output:
- 0-10 rating by dimension
- What would make it a 10
- Specific edits, not taste adjectives
- Mobile/responsive and empty/error/loading states
- "AI-slop" flags: generic layouts, vague copy, ornamental visuals, overcomplicated text

### QA And Ship Gate

Use when the user asks to test, publish, deploy, submit, or release.

Output:
- Tests run and results
- User-flow evidence
- Remaining blockers
- Rollback or recovery path
- Clear ship/no-ship recommendation

## Decision Rules

- Prefer real demand over technical novelty.
- Prefer recurring use over one-time curiosity.
- Prefer narrow permissions and simple privacy disclosures.
- Keep scarce slots only for products that beat a named alternative.
- Do not treat total installs as active use; weigh retained weekly users, uninstall rate, impressions, page views, and conversion.
- When evidence is weak, run a bounded test instead of declaring certainty.

## Upstream Use

If `/home/z/Github/gstack` exists, use it as source material for deeper review. Read only the specific upstream `SKILL.md` needed for the current mode.

If it is missing and the user asked to use upstream gstack, fetch or inspect `https://github.com/garrytan/gstack` before proceeding.

Do not paste large upstream sections into outputs. Summarize and cite local file paths or public links.
