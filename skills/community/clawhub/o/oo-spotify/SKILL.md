---
name: oo-spotify
description: "Spotify (spotify.com). Use this skill for ANY Spotify request — reading, creating, updating, and deleting data. Whenever a task involves Spotify, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Spotify"
  author: "OOMOL"
  version: "1.0.1"
  services: ["spotify"]
  icon: "https://static.oomol.com/logo/third-party/spotify.svg"
---

# Spotify

Operate **Spotify** through your OOMOL-connected account. This skill calls the `spotify` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Spotify. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "spotify" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "spotify" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_item_to_playback_queue` — Add a Spotify track or episode to the end of the playback queue. [write]
- `add_items_to_playlist` — Add tracks or episodes to a Spotify playlist in the requested order. [write]
- `change_playlist_details` — Update Spotify playlist metadata such as name, description, visibility, or collaborative state. [write]
- `check_saved_albums` — Check whether the current authenticated Spotify user has saved the given albums.
- `check_saved_audiobooks` — Check whether the current authenticated Spotify user has saved the given audiobooks.
- `check_saved_episodes` — Check whether the current authenticated Spotify user has saved the given episodes.
- `check_saved_shows` — Check whether the current authenticated Spotify user has saved the given shows.
- `check_saved_tracks` — Check whether the current authenticated Spotify user has saved the given tracks.
- `check_user_follows_artists_or_users` — Check whether the current authenticated Spotify user follows the given artists or users.
- `check_users_follow_playlist` — Check whether the given Spotify users follow a playlist. [write]
- `create_playlist` — Create a Spotify playlist for a user account owned by the authenticated user. [write]
- `follow_artists_or_users` — Follow one or more Spotify artists or users on behalf of the authenticated user. [write]
- `follow_playlist` — Follow a Spotify playlist on behalf of the authenticated user. [write]
- `get_album` — Get a Spotify album by its album ID.
- `get_album_tracks` — Get the tracks for a Spotify album by its album ID.
- `get_artist` — Get a Spotify artist by its artist ID.
- `get_artist_albums` — Get Spotify albums for an artist by the artist ID.
- `get_artist_related_artists` — Get related Spotify artists for an artist ID.
- `get_artist_top_tracks` — Get top Spotify tracks for an artist ID in a given market.
- `get_audiobook` — Get a Spotify audiobook by its audiobook ID.
- `get_audiobook_chapters` — Get Spotify chapters for an audiobook ID.
- `get_available_devices` — Get available Spotify playback devices for the current authenticated user.
- `get_available_genre_seeds` — Get the genre seeds supported by Spotify recommendations.
- `get_available_markets` — Get the markets supported by Spotify catalog APIs.
- `get_browse_categories` — Get Spotify browse categories for a market and locale.
- `get_browse_category` — Get a Spotify browse category by category ID.
- `get_category_playlists` — Get Spotify playlists for a browse category ID.
- `get_chapter` — Get a Spotify chapter by its chapter ID.
- `get_current_user_playlists` — Get playlists for the current authenticated Spotify user.
- `get_current_user_profile` — Get the current authenticated Spotify user's profile details.
- `get_currently_playing_track` — Get the currently playing Spotify item for the authenticated user.
- `get_episode` — Get a Spotify episode by its episode ID.
- `get_featured_playlists` — Get Spotify featured playlists for a market and locale.
- `get_followed_artists` — Get artists followed by the current authenticated Spotify user.
- `get_new_releases` — Get Spotify new release albums for a market.
- `get_playback_state` — Get the current Spotify playback state for the authenticated user.
- `get_playlist` — Get metadata for a Spotify playlist by its playlist ID.
- `get_playlist_cover_image` — Get Spotify cover images for a playlist ID.
- `get_playlist_items` — Get playlist items for a Spotify playlist by its playlist ID.
- `get_recently_played_tracks` — Get recently played Spotify tracks for the authenticated user.
- `get_recommendations` — Get Spotify track recommendations from seed artists, tracks, or genres.
- `get_several_albums` — Get multiple Spotify albums by album ID.
- `get_several_artists` — Get multiple Spotify artists by artist ID.
- `get_several_audiobooks` — Get multiple Spotify audiobooks by audiobook ID.
- `get_several_chapters` — Get multiple Spotify chapters by chapter ID.
- `get_several_episodes` — Get multiple Spotify episodes by episode ID.
- `get_several_shows` — Get multiple Spotify shows by show ID.
- `get_several_track_audio_features` — Get Spotify audio features for multiple track IDs.
- `get_several_tracks` — Get multiple Spotify tracks by track ID.
- `get_show` — Get a Spotify show by its show ID.
- `get_show_episodes` — Get Spotify episodes for a show ID.
- `get_track` — Get a Spotify track by its track ID.
- `get_track_audio_analysis` — Get Spotify audio analysis for a track ID.
- `get_track_audio_features` — Get Spotify audio features for a track ID.
- `get_user_playlists` — Get playlists visible for a Spotify user ID.
- `get_user_profile` — Get a Spotify user profile by Spotify user ID.
- `get_user_queue` — Get the current Spotify queue for the authenticated user.
- `get_user_saved_albums` — Get albums saved by the current authenticated Spotify user.
- `get_user_saved_audiobooks` — Get audiobooks saved by the current authenticated Spotify user.
- `get_user_saved_episodes` — Get episodes saved by the current authenticated Spotify user.
- `get_user_saved_shows` — Get shows saved by the current authenticated Spotify user.
- `get_user_saved_tracks` — Get tracks saved by the current authenticated Spotify user.
- `get_user_top_artists` — Get the current Spotify user's top artists for a selected affinity time range.
- `get_user_top_tracks` — Get the current Spotify user's top tracks for a selected affinity time range.
- `pause_playback` — Pause Spotify playback on the targeted device or current active device. [write]
- `remove_playlist_items` — Remove tracks or episodes from a Spotify playlist. [destructive]
- `remove_user_s_saved_audiobooks` — Remove one or more Spotify audiobooks from the authenticated user's library. [destructive]
- `remove_user_s_saved_episodes` — Remove one or more Spotify episodes from the authenticated user's library. [destructive]
- `remove_user_s_saved_shows` — Remove one or more Spotify shows from the authenticated user's library. [destructive]
- `remove_user_s_saved_tracks` — Remove one or more Spotify tracks from the authenticated user's library. [destructive]
- `remove_users_saved_albums` — Remove one or more Spotify albums from the authenticated user's library. [destructive]
- `save_albums_for_current_user` — Save one or more Spotify albums to the authenticated user's library. [write]
- `save_audiobooks_for_current_user` — Save one or more Spotify audiobooks to the authenticated user's library. [write]
- `save_episodes_for_current_user` — Save one or more Spotify episodes to the authenticated user's library. [write]
- `save_shows_for_current_user` — Save one or more Spotify shows to the authenticated user's library. [write]
- `save_tracks_for_current_user` — Save one or more Spotify tracks to the authenticated user's library. [write]
- `search_items` — Search Spotify catalog content across one or more resource types with a keyword query.
- `seek_to_position` — Seek the currently playing Spotify item to the given playback position. [write]
- `set_playback_volume` — Set Spotify playback volume for the targeted playback device. [write]
- `set_repeat_mode` — Set Spotify repeat mode for the targeted playback device. [write]
- `skip_to_next` — Skip to the next item in the Spotify playback queue. [write]
- `skip_to_previous` — Skip to the previous item in the Spotify playback queue. [write]
- `start_resume_playback` — Start a new Spotify playback context or resume playback on the targeted device. [write]
- `toggle_playback_shuffle` — Enable or disable Spotify playback shuffle on the targeted device. [write]
- `transfer_playback` — Transfer Spotify playback to another available device. [write]
- `unfollow_artists_or_users` — Unfollow one or more Spotify artists or users on behalf of the authenticated user. [write]
- `unfollow_playlist` — Unfollow a Spotify playlist on behalf of the authenticated user. [write]
- `update_playlist_items` — Replace all items in a Spotify playlist or reorder an existing range of items. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Spotify state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Spotify is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=spotify
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Spotify homepage: https://spotify.com
