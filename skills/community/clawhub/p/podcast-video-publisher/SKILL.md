---
name: "Podcast Video Publisher"
description: "Render podcast episodes as 1080p art-slideshow MP4s and publish them to a YouTube Podcasts playlist: covers/thumbnails generated from your art, resumable batch upload, playlist ordering, retiring old versions. Use when releasing podcast episodes to YouTube, batch-upgrading existing episode videos, rebuilding a podcast playlist, or debugging YouTube API upload/thumbnail/playlist failures."
---

# Podcast Video Publisher

Turn a folder of podcast audio + a folder of artwork into a complete,
correctly-ordered YouTube Podcasts section. Battle-tested by shipping a
12-episode season in one day (Ghost Signals with Kannaka — canonical
home: https://github.com/NickFlach/kannaka-radio).

## What This Skill Does

1. **Render** — `scripts/podcast-slideshow.py` builds a 1920×1080 MP4 per
   episode: art slides (~45 s each, blur-filled background, sharp center
   panel, dip-to-black fades) plus a generated cover card (hero art +
   episode title) that doubles as the thumbnail. Video is padded then
   muxed `-shortest`, so A/V drift is 0.00 s by construction.
2. **Publish** — `scripts/podcast-upload-batch.js` runs resumable phases:
   `upload → thumbs → playlist → order → retire → verify`, with all
   progress in a state file so any failure (quota, rate limit, network)
   resumes exactly where it stopped.
3. **Self-heal** — `scripts/podcast-finisher.js` is a long-running watcher
   that retries rate-limited thumbnails (2 h cadence) and applies playlist
   positions the moment position updates become possible.

All six scripts in `scripts/` are self-contained (Node stdlib + ffmpeg +
Pillow only — no npm install).

## Setup

1. Drop the `scripts/` folder into your project root (`<project>/scripts/`).
   The scripts treat the parent of `scripts/` as the project root.
2. Install prerequisites: ffmpeg + ffprobe on PATH, Python 3 with Pillow,
   Node 18+.
3. Create YouTube OAuth credentials: `node scripts/youtube-grant.js`
   (prompts for an OAuth client id/secret from Google Cloud Console with
   the full `youtube` scope). Writes `<project>/.youtube.json` —
   **never commit this file**.
4. Set `PODCAST_PLAYLIST` in `scripts/podcast-upload-batch.js` and
   `scripts/podcast-finisher.js` to your podcast playlist ID.
5. Fonts: cover cards default to Segoe UI (`C:/Windows/Fonts/`) — edit
   `FONT_BOLD`/`FONT_REG` in `podcast-slideshow.py` on Linux/macOS.

## Project Layout

```
<project>/
├── .youtube.json                     # OAuth creds (gitignore!)
├── scripts/                          # this skill's scripts
└── workspace/podcasts/
    ├── episodes.json                 # [{num, title, audio}, ...]
    ├── metadata.json                 # [{num, title, description, tags,
    │                                 #   video, cover, oldVideoId?}, ...]
    ├── art/                          # square images ≥1024px
    │   └── manifest.json             # [{file, title}, ...]
    ├── renders/                      # output MP4s + cover PNGs
    └── upload-state.json             # created by the pipeline (gitignore)
```

## Quick Start

```bash
python scripts/podcast-slideshow.py --all      # render (idempotent)
node scripts/podcast-upload-batch.js           # publish, re-run to resume
node scripts/podcast-finisher.js               # only if thumbs/order pending
```

## Phase Reference (`podcast-upload-batch.js`)

| Phase | What it does | Quota |
|-------|--------------|-------|
| `upload` | `videos.insert` per episode, missing-episodes first | 1600/video |
| `thumbs` | `thumbnails.set` with the rendered cover | ~50 |
| `playlist` | remove stale items, insert episodes into the podcast playlist | 50/item |
| `order` | `playlistItems.update` explicit positions 1→N | 50/item |
| `retire` | unlist each replaced video + prepend an "upgraded edition" pointer to its description (old links keep working) | 50/video |
| `verify` | read back playlist order + processing status of every upload | ~1 |

Run one phase with `--phase <name>`. Delete an entry from
`upload-state.json` to force a redo of just that item.

## YouTube Gotchas (all hit in production — trust these)

1. **Uploads can silently vanish.** `videos.insert` may return 200 + a
   video ID and the video is simply gone minutes later — no error, no
   `rejectionReason`. Always re-verify IDs with `videos.list` before
   playlist adds (which otherwise fail "Video not found"), and keep
   uploads resumable per-item. Re-uploading the identical file works.
2. **Thumbnails: 2 MB hard limit + long rate-limit.** 1080p PNGs blow the
   2,097,152-byte cap (`413`) — save covers as JPEG quality ~88. After
   ~10 rapid sets you get `429 "too many thumbnails recently"` and the
   cooldown outlasts 40+ minutes — hence the finisher's 2 h retry cadence.
3. **Podcast playlists force publish-date ordering.** Display order is
   exactly `publishedAt DESC`; insert order is irrelevant, delete +
   re-insert changes nothing, and `playlistItems.update` with a position
   fails with *"Playlist sort type need to be MANUAL to support
   position"*. `publishedAt` is immutable (a private→public round-trip
   does NOT reset it) and the sort setting is not in the Data API. Fix:
   flip the playlist to **Manual** ordering in YouTube Studio (one click,
   owner only), then run `--phase order`. Or upload in episode order in
   the first place.
4. **Daily quota is not always 10k.** A 13-upload day (~21k nominal
   units) cleared fine. Don't pre-abort on quota math, but assume any
   phase can die mid-run — that's what the state file is for.

## Design Notes

- Cover cards are drawn with Pillow (hero art right, blurred/darkened
  art as backdrop, kicker + wrapped title + footer left) — consistent
  branding and readable at thumbnail size.
- Slides render as independent per-slide MP4 segments (parallel,
  resumable) joined with the concat demuxer; audio is muxed once at the
  end, so chapter timestamps in descriptions stay valid.
- Descriptions: keep every factual claim traceable to the episode audio
  (transcribe with faster-whisper if needed), and scrub anything private
  before publishing — no server names, IPs, file paths, or credentials.
