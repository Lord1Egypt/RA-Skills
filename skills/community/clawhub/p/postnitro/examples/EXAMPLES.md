# PostNitro CLI — Skill Examples

Ready-to-use files for the `postnitro` skill. Authenticate first
(`postnitro auth set-key pn-...` or `export POSTNITRO_API_KEY=pn-...`).

## Files

| File | What it is | Use with |
|------|------------|----------|
| [import-default.json](import-default.json) | Basic 4-slide import (starting / body / body / ending) | `carousel import` |
| [import-infographics.json](import-infographics.json) | Import with `grid` and `cycle` infographic body slides | `carousel import` |
| [import-video.json](import-video.json) | 4-scene video import — background image, inline image, and an infographic scene (same slide array as a carousel) | `video import` |
| [schedule-post.json](schedule-post.json) | A full `schedule` body (designId + accounts + caption + LinkedIn settings) | `schedule create --file` |

## Import a carousel

```bash
# From a file
postnitro carousel import --file examples/import-default.json --wait

# With infographic slides
postnitro carousel import --file examples/import-infographics.json --wait

# Same JSON inline (overrides --file)
postnitro carousel import --slides "$(cat examples/import-default.json)" --wait
```

## Import a video

Scenes use the same slide array as a carousel — one slide per scene. `--video-duration` is
required when you want the rendered MP4 back.

```bash
# Rendered MP4, silent
postnitro video import --file examples/import-video.json \
  --response-type MP4 --video-duration 30 --wait

# With an audio track (IDs come from `postnitro audio list`, never a URL)
AUDIO=$(postnitro audio list | jq -r '.audios[0].id')
postnitro video import --file examples/import-video.json \
  --response-type MP4 --video-duration 30 --audio-id "$AUDIO" --wait

# Design only — no render; set the duration later in the video maker
postnitro video import --file examples/import-video.json --wait
```

A scene holds anything a carousel slide does — `image`, `background_image`, and
`layoutType: "infographic"` all work, which is why this example uses one of each.

**Want actual motion?** Point an `image` or `background_image` at a **`.gif`** (or use a
template whose elements carry animations). The API renders those through its enhanced
video pipeline, which captures the movement; without a GIF or animations you get a
static scene-by-scene video. Expect the enhanced render to take longer than the
15-45s a plain one does.

## Generate with AI (no JSON file needed — flags only)

```bash
postnitro carousel generate --context "5 LinkedIn growth tips" --type text --wait
postnitro carousel generate --context "https://yourblog.com/post" --type article --wait
postnitro carousel generate --context "https://x.com/user/status/123" --type x --wait

# A video instead — each AI-written slide becomes a scene
postnitro video generate --context "3 habits that make remote teams faster" \
  --response-type MP4 --video-duration 30 --wait
```

## Schedule a finished design

Edit `schedule-post.json` (set a real `designId` from the import/generate output and a real
`socialAccountId` from `postnitro social list`), then:

```bash
postnitro schedule create --file examples/schedule-post.json
```

Inline flags override any field in the file, e.g. change the time without editing the file:

```bash
postnitro schedule create --file examples/schedule-post.json --scheduled-at "2027-01-15T09:00:00Z"
```

## End-to-end (capture designId → schedule)

```bash
DID=$(postnitro carousel import --file examples/import-infographics.json --wait | jq -r .designId)
LINKEDIN=$(postnitro social list | jq -r 'first(.accounts[] | select(.platform=="linkedin").id)')
postnitro schedule create --status SCHEDULED --scheduled-at "2026-12-31T13:00:00Z" \
  --design-id "$DID" --selected-accounts "[\"$LINKEDIN\"]" \
  --linkedin-post-settings '{"postType":"document","postTitle":"Remote Work, Done Right"}' \
  --post-content '{"common":"New carousel 🚀 #remotework"}'
```

## Audio tracks

```bash
postnitro audio list                    # ids for --audio-id / postSettings.audioId
postnitro audio delete <audioId> --yes  # destructive; refused while a scheduled post uses it
```

Uploading audio happens in the PostNitro app — the CLI lists and deletes only. An empty
`audios` array means there's nothing uploaded yet; create the video without `--audio-id`.

## What's scheduled on one account

```bash
LINKEDIN=$(postnitro social list | jq -r 'first(.accounts[] | select(.platform=="linkedin").id)')
postnitro schedule list --from 2026-09-01 --to 2026-09-30 --accounts "$LINKEDIN"
```

See [../references/cli-reference.md](../references/cli-reference.md) for the full command and schema reference.
