---
name: lastfm-spotify-playlists
description: Build music recommendations and create Spotify playlists using Last.fm similarity and listening history.
---

# Execution Model

This skill runs **directly via local Python scripts**.

Valid entrypoints:
- `python run_pipeline.py ...`
- `python auth.py`

## Absolute rules

- Do NOT use ACP
- Do NOT request or require an agentId
- Do NOT propose manual workflows
- Do NOT suggest alternative scripts or paths
- Do NOT reference any `scripts/` directory
- Do NOT use `python -m` module execution
- Do NOT assume the package must be installed

All commands must be executed from the root of this skill folder.

---

# Critical Behavior Rules

If the user asks for:
- creating a playlist
- adding songs to Spotify
- saving results to Spotify

You MUST execute:

```bash
--output-mode spotify --create-playlist

Primary entrypoints:
- `python run_pipeline.py ...`
- `python auth.py ...`

This skill is intentionally organized as plain scripts plus helper modules:
- `run_pipeline.py`
- `auth.py`
- `lastfm.py`
- `spotify.py`
- `pipeline.py`
- `common.py`

No package installation is required.

# Purpose

This skill:
- uses Last.fm as the discovery engine
- expands seeds through `track.getsimilar`
- ranks merged candidates
- optionally matches results on Spotify
- optionally creates Spotify playlists

# Requirements

## Python
A normal local Python interpreter must be available.

## Last.fm credentials
Supported sources:
- environment variables:
  - `LASTFM_API_KEY`
  - `LASTFM_SHARED_SECRET`
  - `LASTFM_USERNAME`
- credentials file:
  - `~/.openclaw/lastfm-credentials.json`
- explicit file path via command flag:
  - `--creds <path>`

Example file:
```json
{
  "api_key": "YOUR_LASTFM_API_KEY",
  "shared_secret": "YOUR_LASTFM_SHARED_SECRET",
  "username": "YOUR_LASTFM_USERNAME"
}
```

## Spotify credentials
Needed only for Spotify matching or playlist creation.

Supported sources:
- environment variables:
  - `SPOTIFY_CLIENT_ID`
  - `SPOTIFY_CLIENT_SECRET`
  - `SPOTIFY_REDIRECT_URI`
- credentials file:
  - `~/.openclaw/spotify-credentials.json`
- explicit file path via command flag:
  - `--spotify-creds <path>`

Saved token location:
- `~/.openclaw/spotify-token.json`
- or explicit path via `--spotify-token <path>`

# Command Selection

## 1. Recommend from recent Last.fm listening
Use when the request is based on a user's recent scrobbles.

```bash
python run_pipeline.py recent-tracks   --user "<LASTFM_USER>"   --recent-count 10   --similar-per-seed 5   --final-limit 20   --output-mode lastfm-only
```

## 2. Recommend from a seed artist
Use when the request is based on one artist.

```bash
python run_pipeline.py artist-rule-c   "<ARTIST_NAME>"   --seed-count 5   --similar-per-seed 10   --final-limit 20   --output-mode lastfm-only
```

## 3. Recommend from top artists
Use when the request is based on a user's broader taste profile.

```bash
python run_pipeline.py top-artists-blend   --user "<LASTFM_USER>"   --period 1month   --artist-count 5   --seed-count-per-artist 3   --similar-per-seed 5   --final-limit 20   --output-mode lastfm-only
```

## 4. Match recommendations to Spotify
Use when the user wants playable Spotify results but not necessarily a playlist.

```bash
python run_pipeline.py recent-tracks   --user "<LASTFM_USER>"   --recent-count 10   --final-limit 20   --output-mode spotify
```

## 5. Create Spotify playlist
Use when the user explicitly wants a playlist created.

```bash
python run_pipeline.py recent-tracks   --user "<LASTFM_USER>"   --recent-count 10   --final-limit 20   --output-mode spotify   --create-playlist   --playlist-name "Last.fm Recommendations"
```

## 6. Run Spotify auth
Use when Spotify token setup is required.

```bash
python auth.py
```

Optional explicit paths:

```bash
python auth.py   --spotify-creds "<PATH_TO_SPOTIFY_CREDS_JSON>"   --spotify-token "<PATH_TO_SPOTIFY_TOKEN_JSON>"
```

# Behavior Rules

- Prefer Last.fm for recommendation discovery
- Use Spotify only for:
  - search
  - playlist creation
  - playlist population
- If the user only wants suggestions, use `--output-mode lastfm-only`
- If the user wants Spotify results, use `--output-mode spotify`
- If the user wants a playlist created, add `--create-playlist`
- Never invent missing credentials
- Never fall back to ACP or agent execution

# Output Expectations

The scripts print JSON to stdout.

Return the JSON result directly or summarize it faithfully.

Typical fields include:
- `mode`
- `user`
- `seed_artist`
- `seed_tracks`
- `suggestions`
- `matched_tracks`
- `unmatched_tracks`
- `playlist`

# Error Handling

If the script exits with an error:
- surface stderr or the raised error message directly
- do not retry through ACP
- do not ask for an agentId
- do not claim the skill is unavailable because it is not a package

Common expected failures:
- missing Last.fm API key
- missing Last.fm username
- missing Spotify credentials
- missing Spotify token
- expired Spotify token without refresh token

# Notes

This skill is intentionally script-based for reliability.

It should work as long as:
- the skill folder is present
- Python is present
- credentials are configured
- commands are executed from the skill folder root

It must not depend on package installation, editable installs, or import path manipulation.
