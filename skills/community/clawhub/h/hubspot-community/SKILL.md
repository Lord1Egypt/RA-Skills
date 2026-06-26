---
name: hubspot-community
description: Research HubSpot Community profiles, boards, unanswered threads, leaderboards, and Community Champion opportunities to identify visibility patterns and produce non-spam participation plans, reply drafts, and scorecards. Use when the user mentions HubSpot Community, Community Champions, Community Champion Opportunities, unanswered HubSpot threads, profile signals, leaderboards, earning visibility, or wants a HubSpot Community playbook or skill.
---

# HubSpot Community

Use this skill when the task is about winning visibility on HubSpot Community through higher-quality participation, not automation.

## Guardrails

- Do not automate posting, liking, upvoting, commenting, or any spammy behavior.
- Prefer public profile, board, and leaderboard pages. If a page needs login, say what is blocked and continue with public sources.
- When Champion guidance is relevant, read [references/champion-opportunities.md](references/champion-opportunities.md).
- If drafting content that may be AI-assisted, note that Champion guidance asks for disclosure and accuracy review before publishing.

## Default workflow

1. Clarify the objective.
   - Common goals: competitor teardown, daily opportunity scan, reply drafting, leaderboard benchmarking, Champion opportunity review.
2. Gather profile signals.
   - Use `https://community.hubspot.com/t5/user/viewprofilepage/user-id/<id>`.
   - Capture member-since date, solutions, replies, upvotes received, ideas, badges, bio, and visible activity.
   - Review the `recent`, `Most Upvotes`, and `Accepted Solutions` tabs.
   - Sample at least 3 recent threads and 3 high-signal contributions.
3. Gather current opportunity sources.
   - Inspect the target boards directly.
   - Use unanswered-thread shortcuts from [references/champion-opportunities.md](references/champion-opportunities.md) instead of relying on flaky board filters.
   - Review the Community Champion Opportunities board when the user cares about points, visibility, or official priorities.
4. Analyze what is working.
   - Look for response speed, board mix, answer structure, follow-up behavior, accepted solutions, and recurring themes.
   - Separate durable patterns from one-off campaign prompts.
5. Produce an actionable output.
   - Default report sections: `Target activity`, `Opportunities today`, `Suggested replies/posts`, and `Progress scorecard`.
   - If access is blocked, add a short `Blocked / data limits` note and give the best next actions.

## What to optimize for

- Prioritize fresh threads with clear business consequences, usually under 48 hours old and with low reply counts.
- Higher quality beats higher volume. Strong replies usually include:
  - direct recommendation
  - rationale or tradeoff
  - concrete implementation steps
  - validation or fallback path
- Focus first on boards where operators need real help, for example CRM, workflows, reporting, sales email, and high-intent marketing questions.
- When benchmarking a strong competitor, note whether they:
  - answer quickly
  - simplify decisions
  - stay in-thread for follow-up
  - convert replies into accepted solutions
  - use signatures or calls to mark the answer as a solution

## HubSpot-specific sources

- Profile pages for signal collection
- Board homepages for recent questions
- Unanswered topic pages from the Champion shortcuts reference
- Community Champion Opportunities board for official visibility and point incentives
- Community leaderboard for benchmarking recognized contributors

## Output patterns

- For competitor analysis: compare board focus, response shape, accepted-solution behavior, and visible brand signals.
- For daily planning: recommend a small number of high-conviction replies and one thought-leadership post, not broad activity quotas.
- For draft generation: write replies that are specific enough to be useful, but never submit them automatically.
