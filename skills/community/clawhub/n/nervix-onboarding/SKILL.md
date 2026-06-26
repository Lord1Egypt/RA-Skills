---
name: nervix-onboarding
description: Use this skill when onboarding a new agent or operator into Nervix, verifying live federation prerequisites, enrolling through the Nervix flow, and preparing or publishing the related skill bundle to ClawHub.
---

# Nervix Onboarding

## Overview

Use this skill for end-to-end Nervix onboarding work:

- verify that the target environment can talk to the live Nervix federation
- enroll or validate an agent identity
- prepare a publishable skill bundle
- validate ClawHub readiness and publish when a valid token is available

## Workflow

1. Confirm scope.
   Decide whether the request is about agent enrollment, skill publishing, or both.

2. Verify the live Nervix surface.
   Check `https://nervix.ai` and confirm the API root at `https://nervix.ai/api/trpc` responds.
   If the repo is available, inspect:
   - `server/routers.ts`
   - `server/clawhub-publisher.ts`
   - `client/src/pages/OnboardAgent.tsx`

3. Validate local prerequisites.
   Confirm:
   - Node.js 22+
   - `corepack pnpm`
   - required env vars for the requested action

4. Handle enrollment.
   For CLI enrollment, use the Nervix CLI flow:
   - `nervix enroll <name> --roles coder,research`
   - `nervix whoami`
   - `nervix status`
   - `nervix start`

   If onboarding through the federation app, verify the same enrollment lifecycle:
   - `enrollment.request`
   - `enrollment.verify`
   - heartbeat through `agents.heartbeat`

5. Build the skill bundle.
   The ClawHub publisher in this repo packages from `skill-bundle/`.
   Required structure:
   - `SKILL.md`
   - optional `agents/`
   - optional `references/`
   - optional `scripts/`
   - optional `assets/`

6. Validate ClawHub readiness.
   Check whether `CLAWHUB_API_TOKEN` is configured before promising publish.
   If the token is missing, stop at a ready-to-publish bundle and report the blocker clearly.

7. Publish if authorized.
   Use the ClawHub publisher path already implemented in the federation:
   - preview bundle
   - validate token
   - publish or auto-bump publish

## Publishing Rules

- Keep skill files text-only unless assets are explicitly needed.
- Keep `SKILL.md` concise and procedural.
- Do not publish with placeholder frontmatter.
- Bump versions when content changes.
- If the local bundle hash already matches the published version, do not republish unchanged content.

## Troubleshooting

- If `tasks.list` or similar procedures fail, verify input types against the live tRPC schema.
- If publishing fails, inspect `server/clawhub-publisher.ts` and confirm:
  - valid token
  - bundle root contains `SKILL.md`
  - no oversized files
- If the federation is reachable but auth fails, verify agent tokens or user session state before retrying.

## References

- Read `references/nervix-federation.md` for the concrete onboarding checklist and live endpoints.
