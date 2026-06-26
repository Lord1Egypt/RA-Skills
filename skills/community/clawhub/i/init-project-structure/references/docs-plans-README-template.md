# Plans

This directory holds **plan-as-contract** files. Each plan is a pre-work document describing what's about to be built, how we'll know it's done, and which contract docs will need updating.

## Filename format

```
YYYY-MM-DD-<short-slug>.md
```

Examples:
- `2026-04-08-cabin-scoring.md`
- `2026-04-12-stripe-metered-billing.md`
- `2026-04-15-port-weather-cleanup.md`

ISO date prefix is non-negotiable — it makes the directory self-sorting by creation date and doubles as the plan's identifier in recaps. The slug is short, kebab-case, and describes the *thing being built*, not the action ("cabin-scoring", not "implement-cabin-scoring").

## Plan structure

Every plan follows the same template (see `~/.claude/skills/draft-feature-plan/templates/plan.md.template`). Required sections:

- **Frontmatter**: `status`, `created`, `updated`, `slug`
- **Context**: why this work is happening, what problem it solves
- **Approach**: the recommended path (one option, not a menu)
- **Acceptance criteria**: a markdown checkbox list of single-sentence verifiable assertions — this is the contract. Free-form prose criteria are not allowed.
- **Files to be touched**: explicit paths
- **Out of scope**: things people might assume but we're not doing
- **Verification**: how to confirm each criterion (commands, manual steps, screens to check)
- **Linked artifacts**: which `docs/features/<name>.md`, `TECHNICAL-DOCUMENTATION.md` section, and `FUNCTIONAL-SPECIFICATIONS.md` section will need updating when the work is done

## Plan status lifecycle

```
draft → active → completed
                ↘ abandoned
```

| Status | Meaning |
|--------|---------|
| `draft` | Plan is being written, not yet started |
| `active` | Implementation is in progress |
| `completed` | All acceptance criteria met, contract docs updated |
| `abandoned` | Decided not to do this, with a reason in the plan |

The status field lives in YAML frontmatter. To find what's in flight:

```bash
grep -l 'status: active' docs/plans/*.md
```

## How plans connect to recaps

Each session recap references the plan(s) it touched by filename. When a session completes the last acceptance criterion of a plan, the recap also flips the plan's status to `completed`. This creates a bidirectional link:

- From plan → recaps that worked on it: `grep -l '2026-04-08-cabin-scoring' docs/recaps/*.md`
- From recap → plan: read the "Plan link" line at the top of the recap

## Drafting a plan

Use the `draft-feature-plan` skill or the `/plan-feature` slash command. The skill will:

1. Read CLAUDE.md and the relevant `docs/` files for context
2. Ask you for the feature description
3. Draft the plan in the standard template at `docs/plans/YYYY-MM-DD-<slug>.md`
4. Present it for your review before writing

## When NOT to draft a plan

Skip the plan for:
- Typo fixes
- Single-line bug fixes that don't change behavior contract
- Dependency bumps with no behavior change
- Pure refactors that produce no observable change
- Hot fixes where there's no time to plan first (write a retroactive plan after the fix)

For these, go straight to a brief recap noting the change.

## When you ARE drafting a plan

The plan is the contract. Don't start implementation until the plan is approved (by you, the user — Claude shouldn't approve its own plans). The plan can be edited mid-flight as you learn things, but acceptance criteria changes should be deliberate, not silent — note them in the recap.
