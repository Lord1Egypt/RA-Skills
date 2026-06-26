---
name: pattern-pindata-hygiene
description: Why pinData must never be in template files.
user-invocable: false
---

# Pattern: pinData hygiene

`pinData` is n8n's UI mechanism for "pinning" a node's output during interactive testing. It carries the test data tied to the live UI session.

## Rule

Templates MUST NOT include `pinData`. It contains test data that breaks reproducibility across envs and balloons template size.

## Enforcement

- `dehydrate.py` strips `pinData` on resync (in the `_METADATA_FIELDS` set in `helpers/dehydrate.py`).
- `validate.py --source template` rejects templates with non-empty `pinData`.

## When pinData appears

It usually shows up when someone exports a workflow from the UI manually instead of using `resync`. If you `dehydrate-workflow.md` from a raw UI export, the strip step removes it automatically.

## In dev: leave it in the UI

`pinData` is fine in the live n8n UI — it just shouldn't make it into the version-controlled template. Resync round-trips strip it cleanly.
