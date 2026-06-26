# Rename Playbook

Use this when the work touches an existing name that already appears in production, docs, code, analytics, contracts, or user habits.

## Rename Questions

Answer these before approving a rename:
- What breaks if the old name disappears today?
- Which systems depend on the old string literally?
- Is the rename public, internal, or both?
- Do users need a bridge period with aliases?
- What is the rollback plan if confusion spikes?

## Migration Layers

| Layer | Check |
|-------|-------|
| Product UI | labels, menus, tooltips, settings, empty states |
| Documentation | headings, screenshots, examples, glossary |
| Code and API | routes, schema fields, enums, SDK methods, env vars |
| Analytics | event names, dashboards, historical joins |
| Operations | support macros, training, tickets, incident playbooks |
| External market | changelog, release notes, customer comms, SEO impact |

## Safe Rename Sequence

1. Name the target state clearly
2. Inventory all old-name dependencies
3. Decide whether aliases are temporary, permanent, or impossible
4. Update the highest-confusion surfaces first
5. Communicate the change where users will trip over it
6. Track whether the new name is actually being adopted

## Alias Rules

- Keep aliases when breaking them would create avoidable support load
- Remove aliases when they keep the old name alive indefinitely without value
- If both names coexist, define which one is canonical in docs and interfaces

## Recommendation Format

For rename decisions, end with:
- winner
- alias policy
- blast radius
- migration owner
- success signal
- rollback trigger
