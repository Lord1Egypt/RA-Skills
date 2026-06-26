# Known-Good Context

This skill is derived from a working setup previously validated on a remote MeowMusicServer-patched deployment.

## Validated facts from the working setup

- Production-ish project path used during the successful run: `/root/MeowMusicServer_patched/repo`
- Service name used there: `meowmusicserver.service`
- Service port there: `2233`
- The working path included:
  - server-side YouTube search/download
  - MV -> MP3 extraction
  - uploaded/synced YouTube cookies
  - Node 22 + `yt-dlp` + `yt-dlp-ejs` + `ffmpeg`
  - local music upload/listing in the web UI

## Important product intent

This is not a "turn MeowMusic into a YouTube player" skill.

The intended shape is:
- keep old sources valuable
- use YouTube only when old sources miss
- save useful downloads into local/cache space
- make the system progressively more local-first

## Migration stance

When applying this skill to another repo:

- preserve repo-native source resolution if it already works
- add YouTube as the missing-track path, not as a blanket replacement
- prefer adding cookie support and stable MP3 caching first
- only add live-stream endpoints if the product truly needs them
