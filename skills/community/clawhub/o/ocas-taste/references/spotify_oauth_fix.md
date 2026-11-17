# Fix: taste:sync-spotify DEGRADED — missing SPOTIFY_REFRESH_TOKEN

**Detected:** 2026-07-26 (finch:work)
**Cron:** `e0a126b6c9f7` (taste:sync-spotify)
**Root cause:** `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` are set in
`$HERMES_HOME/../indigo/.env`, but `SPOTIFY_REFRESH_TOKEN` is absent.
The refresh token **cannot** be minted headlessly — Spotify's user-data
endpoints (`/me/player/recently-played`) require the OAuth Authorization
Code flow with an interactive browser login. No unattended fix exists.

**Second wiring gap (fixed proactively):** once the operator authorizes, the helper
`spotify_auth_helper.py` writes the token to
`commons/data/ocas-taste/music/spotify_token.json`, but the cron puller
`spotify_history_puller.py` reads `SPOTIFY_REFRESH_TOKEN` from `.env`.
Without a bridge, the cron would stay DEGRADED even after OAuth succeeded.
A bridge script `apply_spotify_token_to_env.py` is provided to copy the
file token into `.env`.

## Manual steps for the operator (one-time)

1. **Run the interactive OAuth helper** in an environment with a browser
   (not the headless cron host):
   ```bash
   cd $HERMES_HOME/../indigo/skills/ocas-taste/scripts
   $HERMES_PY spotify_auth_helper.py
   ```
   It opens the Spotify authorize URL, you log in, the callback writes
   `commons/data/ocas-taste/music/spotify_token.json`.

2. **Bridge the token into `.env`** so the cron puller can read it:
   ```bash
   cd $HERMES_HOME/../indigo/skills/ocas-taste/scripts
   $HERMES_PY apply_spotify_token_to_env.py
   ```

3. **Verify the cron resumes cleanly:**
   ```bash
   hermes cron run e0a126b6c9f7
   ```
   Expect: "Fetched N recently played tracks" / "OK: taste spotify sync complete".

## Notes
- `spotipy` is NOT installed in the venv; the active path is the direct
  Web API puller (`spotify_history_puller.py`), which needs only `requests`.
- Do not "fix" this by retrying the cron — the token will not appear on its own.
- Once `SPOTIFY_REFRESH_TOKEN` is in `.env`, Spotify refresh works non-interactively
  forever (refresh tokens don't expire unless revoked). No further manual steps.
