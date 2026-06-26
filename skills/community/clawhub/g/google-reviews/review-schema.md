# Review Schema - Google Reviews

Normalize all inputs into this canonical shape.

## Required Fields

| Field | Type | Notes |
|------|------|-------|
| source | string | `gbp`, `shopping`, `manual` |
| brand | string | Stable brand key |
| entity_id | string | Location, product, or merchant ID |
| review_id | string | Source-native review ID |
| rating | number | 1-5 normalized |
| review_time | string | ISO-8601 timestamp |
| text | string | Raw review text when available |
| language | string | ISO language code |
| author_label | string | Public display label if provided |

## Derived Fields

| Field | Type | Purpose |
|------|------|---------|
| sentiment | string | `positive`, `neutral`, `negative`, `mixed` |
| themes | array | Complaint/praise categories |
| urgency | string | `low`, `medium`, `high` based on policy |
| is_new | boolean | New since previous snapshot |
| is_edited | boolean | Text or rating changed since last snapshot |

## Dedup Key

Use `source + entity_id + review_id` as the unique key.

If two records share the dedup key, keep the newest by `review_time` and preserve previous versions in history logs.
