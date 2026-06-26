---
name: api
description: >
  Use this skill whenever the user wants to integrate Nudgen from application
  code, backend services, webhooks, or server-side automation. This includes
  Nudgen API authentication with Personal Access Tokens (PATs), contacts,
  campaigns, stats, teams, brand configs, and affiliate/referral endpoints.
  Trigger on phrases like "Nudgen API", "send request to /api/v1", "Bearer
  PAT", "create contact in backend", "switch team via API", or any request to
  integrate Nudgen in code instead of shell-only CLI usage.
metadata:
  version: 1.0.0
---

# Nudgen API Skill

This skill supports Nudgen backend integration workflows from application code. Use it for request design, endpoint selection, and implementation guidance.

## When To Use

Use this skill when the user needs to:

- integrate with Nudgen APIs from server-side code
- authenticate requests with `Authorization: Bearer <PAT>`
- manage contacts, campaigns, teams, brand configs, and stats
- read affiliate/referral analytics and payout data
- troubleshoot Nudgen API behavior in app code

If the user is operating only from shell commands, use the separate `cli` skill.

## When Not To Use

Do not use this skill when the task is:

- purely CLI command execution without application code changes
- high-level email strategy or deliverability planning
- generic frontend/UI work unrelated to Nudgen API integration

## Working Style

When this skill is active:

1. Prefer server-side integration patterns and avoid client-side secret exposure.
2. Use the current API base URL and endpoint shapes verified from repo sources.
3. Keep requests scoped to team context when behavior is team-bound.
4. Handle non-200 responses explicitly with actionable error handling.
5. If behavior in docs conflicts with source code, treat local source as truth.
6. If the task is terminal usage only, route to the `cli` skill.
7. Include at least one verification request in proposed integration flows.

## API Surface Focus

Current commonly used endpoints in Nudgen CLI integration:

- `/api/v1/user/me`
- `/api/v1/campaigns`
- `/api/v1/contacts`
- `/api/v1/contacts/add`
- `/api/v1/dashboard/overview`
- `/api/v1/teams`
- `/api/v1/teams/switch`
- `/api/v1/brand`
- `/api/v1/affiliate/me`
- `/api/v1/affiliate/analytics`
- `/api/v1/affiliate/payouts`

## Category Routing

- Auth, base URL, endpoint behavior, request patterns, and error handling:
  Read `references/http-api.md`

## Output Checklist

Aim to leave the user with:

- the right endpoint(s) and method(s)
- request/response shape guidance for the specific task
- team-scope and auth caveats that affect correctness
- a concrete validation step (for example `/user/me`, list reads, or a small create/update test)
