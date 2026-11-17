# Narrative Engine contract

Novel Core treats every writing method as a state-aware plug-in. An engine is
not a voice mandate and it cannot change the Core state machine.

## Required files

```text
engines/<engine-id>/
├── engine.json
├── cards/*.json
├── applicability.md
├── limits.md
└── manifest.json
```

`engine.json` must contain:

```json
{
  "id": "lowercase-slug",
  "version": 1,
  "kind": "narrative-engine",
  "card_files": ["cards/models.json", "cards/techniques.json"],
  "activation": "phase-and-state",
  "language_imitation": false
}
```

Each card must have a unique uppercase `id`, a `kind`, a `name`, a `when`
predicate, a `hardness` value (`required`, `recommended`, or `optional`), and a
short `prompt`. Predicate fields `phase`, `scene_types`, and `requires` are
string lists when present; card-level `requires` is also a string list.
Predicates may inspect declared project and chapter state only. `manifest.json`
must use schema `1` and match every engine and card file hash.

## Activation protocol

1. Validate the engine and its manifest before a project can install it.
2. Read the project profile and the current chapter state.
3. Select cards whose phase, scene type, and required state fields match.
4. Write the selected card IDs and source hashes into an engine snapshot.
5. Pass that snapshot to the writing and review agents.

`engine install` may accept a source tree before its manifest exists; it writes
and verifies the manifest in an isolated staging directory before activation.

An unmatched card is omitted. A card marked `required` is only a requirement
after its predicate matches; it is never a global rule.

## Extension boundary

Users may add engines without changing Novel Core. Core validates the file
contract, path safety, hashes, and output shape. It does not judge an engine's
literary taste. Style detectors are separate, advisory by default, and may be
promoted to project gates explicitly.
