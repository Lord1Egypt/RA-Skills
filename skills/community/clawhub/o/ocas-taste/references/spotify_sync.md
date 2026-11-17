# Spotify Sync (`taste.sync.spotify`)

Music playback history is stored as standard ConsumptionSignal records in `signals.jsonl` with `domain: "music"` and `source: "play"`.

## Auth requirements

The sync uses `scripts/spotify_history_puller.py` which calls the Spotify Web API directly. It requires three environment variables (set in `~/.hermes/.env`):

| Variable | Required | Notes |
|---|---|---|
| `SPOTIFY_CLIENT_ID` | Yes | From Spotify Developer Dashboard |
| `SPOTIFY_CLIENT_SECRET` | Yes | From Spotify Developer Dashboard |
| `SPOTIFY_REFRESH_TOKEN` | Yes | Obtained via OAuth Authorization Code flow (interactive) |

**⚠️ CRITICAL:** The `SPOTIFY_REFRESH_TOKEN` cannot be obtained from the Client Credentials flow. It requires the user to complete the interactive OAuth Authorization Code flow once. Without it, `/me/player/recently-played` returns 403. See `references/api_auth.md` for the re-auth procedure.

**Pre-flight check:** Before running the sync, verify all three env vars are set:
```bash
python3 -c "import os; missing=[v for v in ['SPOTIFY_CLIENT_ID','SPOTIFY_CLIENT_SECRET','SPOTIFY_REFRESH_TOKEN'] if not os.getenv(v)]; print('OK' if not missing else f'Missing: {missing}')"
```

## Procedure

1. **Verify auth:** Confirm all three env vars are present (see above). If `SPOTIFY_REFRESH_TOKEN` is missing, stop and report — do not attempt the API call.
2. **Pull recently played tracks:**
   ```bash
   python3 {skill_root}/scripts/spotify_history_puller.py
   ```
   Outputs JSON array of `{id, name, artist, album, played_at, duration_ms}`.
3. **Deduplicate:** Skip tracks where `dedup_key = "{track_id}:{played_at[:10]}"` already exists in `signals.jsonl`.
4. **Create ConsumptionSignals** (`strength: 0.60`) and ItemRecords per new track:
   - `domain: "music"`, `source: "play"`, `signal_type: "consumed"`
   - ItemRecord: `type: "music"`, `name: "{track_name}"`, `metadata: {artist, album, spotify_id}`
5. **Persist:** Append to `signals.jsonl` and `items.jsonl`.
6. **Update checkpoint:** Write `music/spotify_sync_checkpoint.json` with `last_sync`, `last_sync_status: "ok"`, track count.
7. **Write journal.**

## Cron behavior

- Runs as a scheduled cron job (no user present).
- If auth fails, the script exits with a non-zero code and a diagnostic stderr message naming the missing credential(s).
- The checkpoint file records `last_sync_status: "failed"` with `failure_reason` and `action_required`.
- **Do not retry** on auth failure — the token will not magically appear.

## Data store paths

- Signals: `{agent_root}/commons/data/ocas-taste/signals/signals.jsonl`
- Items: `{agent_root}/commons/data/ocas-taste/items/items.jsonl`
- Checkpoint: `{agent_root}/commons/data/ocas-taste/music/spotify_sync_checkpoint.json`
- Journals: `{agent_root}/commons/journals/ocas-taste/YYYY-MM-DD/`

## Edge cases

- **No new tracks since last sync:** Checkpoint still updates with `last_sync` timestamp. Journal records 0 new signals.
- **Spotify API rate limit (429):** Back off and retry once. If it fails again, record in checkpoint and journal.
- **Duplicate tracks across runs:** The dedup key `{track_id}:{played_at[:10]}` prevents double-counting the same play on the same day.