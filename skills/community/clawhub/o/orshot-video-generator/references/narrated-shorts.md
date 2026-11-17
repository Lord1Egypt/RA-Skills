# Narrated shorts and captioned clips

Use this path when the video is driven by a voice: a faceless Short with a voiceover per scene and word-by-word captions, a podcast clip, or captions burnt into a talking-head clip. Films do not burn captions in or take a per-render `audioSource` yet, so these videos are pages joined with `videoOptions.combinePages` instead of a `film` block. Everything else in the skill (pacing, pictures, checks, drafts) still applies.

Field shapes: `orshot_get_design_spec` topic `template-json` and https://orshot.com/docs/definitions/template-json.md. Render options: https://orshot.com/docs/video-generation/video-options.md. Captions: https://orshot.com/docs/video-generation/adding-subtitles.md. Per-render clip keys: https://orshot.com/docs/video-generation/video-elements.md.

## Recipes

**Faceless fact reel (9:16, 20 to 40 s).** 5 to 7 pages, one per narration line, each as long as its line plus 1 s.
- Page 1 hook: the claim at t=0, biggest text, a full-bleed clip of the subject. "Octopuses have three hearts" beats "Did you know?".
- Pages 2 to 5: one fact per page, 6 words or fewer on screen, a new clip per page.
- Last page: the payoff and a follow line.
- Fields: `pageN@line`, `pageN@clip`. Voice per page, captions from the same audio.

**Explainer with narration (16:9, 30 to 90 s).** One page per step. Start where the viewer is, then one concrete example worked start to finish. Captions on, with a calm preset such as `minimal`.

**Podcast or quote clip (9:16 or 1:1, 15 to 60 s).** One page: the speaker photo or clip, the show name, the quote or captions, and a `waveform` layer that animates from the page audio track (Waveforms in [Template JSON](https://orshot.com/docs/definitions/template-json.md)). Fields: `quote`, `speaker_name`, `speaker_photo`. Swap the audio per render with `videoOptions.audioSource`; captions come from the same audio.

**Captions on an existing clip (any size).** One page with a full-bleed video field (element `videoOptions.muted: false` so the clip keeps its sound) plus a logo or title bar. Per render: the clip URL in the field and the same URL in `videoOptions.subtitleSource`, with a `captionPreset`. A video URL is transcribed from its own audio.

```json
{
  "templateId": 123,
  "format": "mp4",
  "background": true,
  "modifications": {
    "clip": "https://.../take-07.mp4",
    "title": "3 signs you grind your teeth"
  },
  "videoOptions": { "subtitleSource": "https://.../take-07.mp4", "captionPreset": "bold" }
}
```

Send the same `captionPreset` on every clip so the series looks the same. Orshot captions and frames the clip. It does not cut silences or retakes, so trim the clip first.

## Voice, music and captions

- **Voiceover:** a recorded file as a page audio track. If `orshot_get_audio_authoring_options` is in your tool list, it lists generated voices and limits; if it is not, use a recorded file.
- **Narration budget:** about 2.5 words per second, plus 1 s of headroom per page.
- **Music:** a page audio track with its trim, fade, volume and loop saved in the template, at about 0.08 to 0.18 under a voice. Swap the file per render with `videoOptions.audioSource`; the saved trim, fade and volume stay.
- **How many tracks:** a render is refused when a page has more audio tracks than the plan allows per page (Page audio in [Template JSON](https://orshot.com/docs/definitions/template-json.md)). Voice plus music is two. If the plan allows one, mix them into one file first.
- **Auto captions:** `page.subtitle.source: "auto-audio"` in the template captions the page's first audio track, or pass `videoOptions.subtitleSource` per render. Pick the look with `videoOptions.captionPreset`.

## Build, check, render

1. `orshot_create_template_design` with every page, `videoDuration`, `audioTracks` and `subtitle` where needed, and `includeThumbnails: true`. Read the checks and the free animated preview; fix in one update.
2. Check one still before spending a video render: `orshot_render_template` with `format: "png"`, `includePages: [1]`, `responseType: "base64"` costs one image credit and shows layout, contrast and text fit exactly as the video will.
3. Render with the pages joined:

```json
{
  "templateId": 123,
  "format": "mp4",
  "background": true,
  "modifications": {
    "page1@line": "Octopuses have three hearts",
    "page1@clip": "https://.../octopus.mp4",
    "page2@line": "Two pump blood to the gills",
    "page2@clip": "https://.../gills.mp4"
  },
  "videoOptions": {
    "combinePages": true,
    "pageTransition": "fade",
    "pageTransitionDuration": 0.9,
    "audioSource": [ { "page": 1, "url": "https://.../voice-1.mp3" }, { "page": 2, "url": "https://.../voice-2.mp3" } ],
    "subtitleSource": [ { "page": 1, "url": "https://.../voice-1.mp3" }, { "page": 2, "url": "https://.../voice-2.mp3" } ],
    "captionPreset": "bold"
  }
}
```

Each `audioSource` entry swaps track 0 of its page, so the voice is track 0 and any music is track 1. A string `audioSource` swaps every page's first track.

## A faceless Shorts channel in n8n

One template per channel, one n8n node per step:

1. **Schedule Trigger:** once a day.
2. **Google Sheets:** read the next row marked `todo`. It holds the topic and one clip URL per scene. Stock search is an MCP tool, so fill the clip columns ahead with `orshot_search_stock_media` and `orshot_use_stock_media`, or use the user's brand videos.
3. **LLM node:** write the hook, one on-screen line per scene (6 words or fewer) and the narration per scene, each within its page's narration budget.
4. **Text to speech:** one mp3 per scene from the user's voice service, at a public URL.
5. **HTTP Request:** the render above over REST, with `"response": { "type": "url", "format": "mp4", "mode": "async" }`, a `webhook_url` pointing at an n8n Webhook node and `"metadata": "{{row_number}}"`. The Orshot n8n node lists image and PDF formats, so video goes through an HTTP Request node.
6. **Wait for the result:** the Webhook node, or poll `GET /v1/studio/render-jobs/<id>` until `finished` is true ([Async renders](https://orshot.com/docs/api-reference/async-render-start.md)).
7. **Write back:** the video URL in the row, marked `done`, or post it as a draft: `orshot_publish_social_post` with the video URL and `status: "draft"` over MCP, or `publish` with `"isDraft": true` on a REST render.

Say the cost before switching it on: video is 1 credit per second, so one 30 s short a day is about 900 credits a month.

## Gotchas

1. `trimStart` and `trimEnd` in `videoOptions` trim the output, not the music, and must be sent together. Trim a song on its audio track instead.
2. Templates with `page.subtitle.source: "auto-audio"` need no `subtitleSource`.
3. Over MCP, `easing` takes only the values the schema lists. Any other `cubic-bezier(...)` is rejected.
