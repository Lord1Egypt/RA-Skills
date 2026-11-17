# Pinterest Rules

Use this file for Pinterest platform-level routing boundaries. Use module files for scenario-specific workflows.

## Entity Scope

users, profiles, boards, pins, followers, and following relationships

## Scenario Module Routing

- Use `pinterest-profile-rules.md` for user search and profile information.
- Use `pinterest-content-rules.md` for boards and pins.
- Use `pinterest-network-rules.md` for followers and following.

## Identifier Discipline

- Resolve the target user before board, pin, follower, or following workflows.
- Keep board and pin identifiers separate when a downstream endpoint requires one or the other.

## Output Guidance

- For profile reports, separate user metadata, board inventory, pin evidence, and social graph context.
- For graph work, state whether results are followers or following.
