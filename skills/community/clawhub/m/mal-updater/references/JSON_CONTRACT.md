# Crunchyroll snapshot JSON contract

The live Crunchyroll fetch path produces a single normalized JSON snapshot.
The rest of the Python application owns validation, persistence, mapping, sync policy, and review-queue generation.

## Contract boundary

Current producer shape:

```bash
PYTHONPATH=src python3 -m mal_updater.cli crunchyroll-fetch-snapshot --out path/to/snapshot.json
```

- output JSON matches `references/contracts/crunchyroll_snapshot.schema.json`
- the snapshot is normalized provider data, not direct MAL mutation intent
- any future producer must emit the same contract if it wants to plug into the existing ingestion path

## Contract versioning

- Current version: `1.0`
- Any breaking change requires a new contract version string and coordinated validation/ingestion updates.

## Snapshot semantics

- `series`: deduplicated per-provider series/season records known from Crunchyroll data
- `progress`: per-episode playback observations with timestamps, completion ratio, and raw timing needed for conservative completion inference
- `watchlist`: explicit watchlist/library entries if Crunchyroll exposes them
- `raw`: optional provider-specific passthrough/debug object

## Required safety expectations

- Secrets must never be written into the snapshot.
- Missing/unknown fields must be treated as incomplete data, not proof of absence.
- MAL mutations must only be inferred from normalized persisted state, never directly from raw passthrough blobs.
- `playback_position_ms`, `duration_ms`, `episode_number`, and `last_watched_at` are part of the conservative completion policy; do not drop them if credits-skipped behavior still matters.

## Example payload

```json
{
  "contract_version": "1.0",
  "generated_at": "2026-03-14T18:00:00Z",
  "provider": "crunchyroll",
  "account_id_hint": null,
  "series": [
    {
      "provider_series_id": "series-123",
      "title": "Example Show",
      "season_title": "Example Show Season 1",
      "season_number": 1
    }
  ],
  "progress": [
    {
      "provider_episode_id": "episode-456",
      "provider_series_id": "series-123",
      "episode_number": 3,
      "episode_title": "Example Episode",
      "playback_position_ms": 1300000,
      "duration_ms": 1440000,
      "completion_ratio": 0.95,
      "last_watched_at": "2026-03-14T17:55:00Z",
      "audio_locale": "en-US",
      "subtitle_locale": null,
      "rating": null
    }
  ],
  "watchlist": [
    {
      "provider_series_id": "series-123",
      "added_at": "2026-03-10T12:00:00Z",
      "status": "watching"
    }
  ],
  "raw": {}
}
```