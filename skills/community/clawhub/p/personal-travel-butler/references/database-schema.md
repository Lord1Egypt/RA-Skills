# Travel Database Schema

Use Markdown files with YAML frontmatter. Store one durable idea per file.

## Directory Map

- `places/`: restaurants, cafes, attractions, shops, hotels, stations, neighborhoods.
- `guides/`:攻略、榜单、路线线索、社媒收藏、文章摘要。
- `trips/`: concrete itineraries, draft plans, past trips, day plans.
- `preferences/`: user preferences, constraints, travel style, dietary notes.
- `assets/`: images and other source files.
- `_inbox/`: raw captures, OCR text, uncertain imports, multi-entity notes.
- `indexes/`: generated or manually refreshed views grouped by city, tag, and source.

## Required Frontmatter

Every atomic entry in `places/`, `guides/`, `trips/`, and `preferences/` must include:

```yaml
id: place-20260614-abc123
type: place
status: active
name: Example name
city: Shanghai
coordinates: null
tags: []
source: []
evidence: []
priority: 3
last_verified: null
created_at: 2026-06-14
updated_at: 2026-06-14
```

## Field Rules

- `id`: stable, unique, lowercase slug prefix plus date and short hash. Never change after creation.
- `type`: one of `place`, `guide`, `trip`, `preference`.
- `status`: one of `inbox`, `active`, `planned`, `visited`, `archived`, `needs-review`.
- `name`: human-readable title.
- `city`: known city or `null` if unknown. Use one city name consistently per entry.
- `coordinates`: `null` or a mapping with `lat` and `lng`.
- `tags`: lowercase-ish descriptive tags. Chinese tags are fine.
- `source`: list of source objects or strings. Prefer objects when details are known.
- `evidence`: list of raw user quotes, asset paths, URLs, or notes supporting the entry.
- `priority`: integer 1-5, where 5 means very important to the user.
- `last_verified`: date when external facts were last checked, or `null`.
- `created_at` / `updated_at`: ISO dates.

## Recommended Source Object

```yaml
source:
  - title: "Original user note"
    url: null
    captured_at: 2026-06-14
    confidence: high
```

Use `confidence: low`, `medium`, or `high`. External facts should include source title or URL when available.

## Place Body Template

```markdown
## Snapshot

- Why it matters:
- Best for:
- Signature items:
- Reservation:
- Hours:
- Budget:

## Notes

- 

## Evidence

- 

## Conflicts / Review

- 
```

## Guide Body Template

```markdown
## Summary


## Extracted Items

- 

## Useful For

- 

## Evidence

- 
```

## Trip Body Template

```markdown
## Intent


## Constraints

- 

## Draft Plan

- 

## Candidates

- 
```

## Preference Body Template

```markdown
## Preference


## Applies To

- 

## Evidence

- 
```
