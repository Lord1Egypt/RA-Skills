# Mopidy-Iris / Mopidy API Notes

These notes are for adapting the skill to a specific Mopidy setup.

## Endpoint

Expected JSON-RPC endpoint shape:
- `https://your-host.example.com/mopidy/rpc`

Notes:
- Iris is the web UI, but control should use Mopidy's JSON-RPC API.
- The available library backend may vary by installation.
- Confirm core methods against the target server before assuming backend-specific behavior.

## Commonly Useful Methods

- `core.playback.get_current_track`
- `core.playback.get_state`
- `core.tracklist.get_tl_tracks`
- `core.tracklist.add`
- `core.tracklist.clear`
- `core.playlists.as_list`
- `core.playlists.lookup`
- `core.library.search`
- `core.playback.play`
- `core.playback.pause`
- `core.playback.next`
- `core.playback.previous`

## URI Notes

URI schemes vary by backend. Examples might look like:
- track example: `backend:song:...`
- album example: `backend:album:...`
- playlist example: `backend:playlist:...`

Do not hardcode a specific backend in the skill instructions unless the skill is intentionally backend-specific.

## Queueing Pattern

Typical add-to-queue pattern:
- call `core.tracklist.add` with `uris: [<track-or-album-uri>]`

## Playlist Note

To add playlist contents to queue:
1. look up the playlist with `core.playlists.lookup`
2. extract track URIs
3. add them via `core.tracklist.add`

Do not assume a backend-specific shortcut unless tested.
