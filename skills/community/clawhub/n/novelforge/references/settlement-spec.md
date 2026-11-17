# Settlement specification

Settlement is the single mechanism for updating story state after a chapter
passes both text and engine reviews. All state changes flow through
`novelforgectl settle`.

## Fact types

| type | folder | description |
|---|---|---|
| `character` | `characters/` | Character profile with personality & pressure log |
| `location` | `locations/` | Named place, scene stage |
| `item` | `items/` | Physical or conceptual item, weapon, artifact |
| `faction` | `factions/` | Group, sect, clan, organization |
| `hook` | `hooks/` | Narrative hook or foreshadowing |
| `event` | `timeline/` | Timestamped story event |
| `entity` | `entities/` | General entity (concept, law, species) |

## Character pressure events

When a `character`-type fact includes a `pressure_event` field, the settlement
engine appends the event to the character's `personality.pressure_log` in the
character's Markdown frontmatter (`characters/<id>.md`).

```json
{
  "id": "character.example",
  "type": "character",
  "pressure_event": {
    "event": "被师兄出卖",
    "weight": 0.2,
    "toward": "trust→distrust"
  }
}
```

Rules:

1. `pressure_event.weight` must be a float in range (0, 0.5] for normal events.
2. The `chapter` field is added automatically from the settlement header.
3. Pressure events accumulate across chapters; they are never overwritten by a
   later settlement unless the story-builder explicitly clears them after a
   personality shift.
4. The settlement engine does not evaluate whether the threshold is reached—
   that judgement belongs to the story-builder and hook-inspector agents.

## Idempotency

Re-applying the same settlement (identical `source_hash` and `review_hashes`)
is a no-op. Changing the chapter body after settlement marks the settlement as
`STALE` and requires re-running the review gates.

