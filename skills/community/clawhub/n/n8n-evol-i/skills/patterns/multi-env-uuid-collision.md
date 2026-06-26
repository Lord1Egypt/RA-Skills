---
name: pattern-multi-env-uuid-collision
description: Why each env needs fresh UUIDs and how the harness mints them.
user-invocable: false
---

# Pattern: multi-env UUID collision

n8n requires every node id within a workflow to be globally unique within its instance. If you copy a workflow's JSON between two n8n instances (e.g. dev → prod) without changing UUIDs, you can get cross-workflow collisions where one workflow's node id accidentally collides with another's.

## Solution

Templates use the `{{@uuid:<identifier>}}` placeholder. Each `<identifier>` resolves to the same UUID within a single hydration run, but a fresh UUID on every hydration. So:

- `dev` hydration produces UUID `aaa-...`
- `prod` hydration produces UUID `bbb-...`
- `dev` re-hydration produces UUID `ccc-...` (different again — but the template stays the same)

This is fine because n8n only cares about uniqueness within an instance. Each env's instance has its own UUIDs, and resync preserves them via name-based lookup.

## When you add a node

Use `{{@uuid:<some-distinct-name>}}` for the new node's `id` field. The identifier just has to be unique within the template (e.g. `webhook-2`, `set-after-merge`).

## Resync preserves UUIDs

When you `resync`, the dehydrate pipeline restores UUID placeholders by **node name** lookup against the existing template. So if you renamed a node in the n8n UI without resyncing, the lookup might miss and you'll see a new UUID slot in the template — not a problem (n8n just needs uniqueness), but worth understanding.

## Position recalculation when adding mid-flow

When inserting nodes mid-flow (e.g. via `add-lock-to-workflow.md`), shift downstream nodes 220px right per inserted node so the canvas stays legible. See `skills/patterns/position-recalculation.md`.
