# Epic Or Technical Debt Issue Shape

Use this shape for multi-part work that should coordinate several related fixes, child issues, or phased implementation. Epics should describe scope, grouping, priority, and verification, not bury every detail in one undifferentiated list.

## Required Sections

```markdown
# <Epic title>

## Summary

What theme connects the work, why it matters, and what outcome the epic should produce.

## Scope

In scope:
- ...

Out of scope:
- ...

## Findings / Workstreams

### High Priority

1. <Item>
   - Description:
   - Evidence summary:
   - Recommended direction:
   - Child issue candidate: yes/no

### Medium Priority

...

### Low Priority / Follow-up

...

## Dependencies And Sequencing

1. ...
2. ...

## Acceptance Criteria

- [ ] ...

## Child Issues To Create

- [ ] ...
```

## Epic-Specific Rules

1. Group related issues by risk or dependency order.
2. Keep the epic readable; move implementation-heavy details to child issues when needed.
3. Include enough evidence for each high-priority item to justify its inclusion.
4. Distinguish confirmed facts from items needing verification.
5. If the epic spans security, bugs, and tech debt, keep security items' evidence and reasoning intact.

## Recommendation Rules For Epics

1. Use directional recommendations in the epic.
2. Put detailed patch-level recommendations in child issues unless the user wants one comprehensive issue.
3. For rejection/compatibility/default changes, still include reasons and options in the epic because those decisions affect planning.

## Sequencing Example

```markdown
Recommended order:

1. Close externally reachable or privilege-expanding paths first.
2. Restore boundary isolation.
3. Tighten defaults and fail-closed behavior.
4. Add resource limits and rate limits.
5. Add defense-in-depth and supply-chain hardening.
```
