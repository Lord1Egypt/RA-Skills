## Render Configuration

### Dynamic Parameters

Override template styles, content, and behavior at render time using dot notation.

#### Style Parameters

Format: `parameterId.property`

```json
{
  "modifications": {
    "title": "Hello World",
    "title.fontSize": "48px",
    "title.color": "#ff0000",
    "title.fontFamily": "Roboto",
    "title.textAlign": "center",
    "logo.borderRadius": "50%",
    "logo.objectFit": "cover"
  }
}
```

**Text properties:** `fontSize`, `fontWeight`, `fontStyle`, `fontFamily`, `lineHeight`, `letterSpacing`, `textAlign`, `verticalAlign`, `textDecoration`, `textTransform`, `color`, `backgroundColor`, `backgroundRadius`, `textStrokeWidth`, `textStrokeColor`, `opacity`, `filter`, `dropShadowX/Y/Blur/Color`

**Image properties:** `objectFit`, `objectPosition`, `borderRadius`, `borderWidth`, `borderColor`, `boxShadowX/Y/Blur/Color`, `opacity`, `filter`

**Shape properties:** `fill`, `stroke`, `strokeWidth`, `borderRadius`, `opacity`

**Position/Size (all elements):** `x`, `y`, `width`, `height`

Property names are **case-insensitive**.

#### Multi-Page Templates

Prefix modifications with page number:
```json
{
  "modifications": {
    "page1@title": "Page 1 Title",
    "page2@title": "Page 2 Title",
    "page1@title.fontSize": "48px"
  }
}
```

#### AI Content Generation (.prompt)

Generate text or images using AI:
```json
{
  "modifications": {
    "headline.prompt": "Write a catchy headline about coffee",
    "background.prompt": "A serene mountain landscape at sunset"
  }
}
```
- `.prompt` on a text element generates copy; on an image element it generates imagery. The underlying AI models are managed by Orshot and may change over time, don't hardcode a specific model. AI modifications consume AI Credits.

#### Interactive Links (.href)

Add clickable links in PDF outputs:
```json
{
  "modifications": {
    "cta_button.href": "https://example.com/signup",
    "logo.href": "https://company.com"
  },
  "response": { "format": "pdf" }
}
```

#### Video Parameters

Control video elements dynamically:
```json
{
  "modifications": {
    "bgVideo": "https://example.com/video.mp4",
    "bgVideo.trimStart": 5,
    "bgVideo.trimEnd": 15,
    "bgVideo.muted": false,
    "bgVideo.loop": true
  },
  "response": { "format": "mp4" }
}
```

### Video Render Example

Render templates with video elements as MP4, WebM, or GIF:

```js
await fetch("https://api.orshot.com/v1/studio/render", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: "Bearer $ORSHOT_API_KEY",
  },
  body: JSON.stringify({
    templateId: 123,
    modifications: {
      videoElement: "https://example.com/custom-video.mp4",
      "videoElement.trimStart": 0,
      "videoElement.trimEnd": 10,
      "videoElement.muted": false,
      "videoElement.loop": true,
    },
    videoOptions: {
      trimStart: 0,
      trimEnd: 20,
      muted: true,
      loop: true,
    },
    response: {
      type: "url",
      format: "mp4",
    },
  }),
});
```

### Render-level `videoOptions` (top level, sibling of `modifications`)

Controls the whole video render, not one element:

```json
{
  "templateId": 123,
  "modifications": { "page1@headline": "Launch day" },
  "videoOptions": {
    "duration": 12,
    "fps": 30,
    "muted": false,
    "combinePages": true,
    "pageTransition": "fade",
    "pageTransitionDuration": 0.5,
    "audioSource": "https://example.com/track.mp3",
    "subtitleSource": "https://example.com/voiceover.mp3",
    "captionPreset": "karaoke"
  },
  "response": { "type": "url", "format": "mp4" }
}
```

- `duration`, `fps` (≤30), `quality`, `muted`, `trimStart`+`trimEnd` (must be paired).
- `combinePages: true` merges a multi-page template into ONE video, with `pageTransition` (42 types, fades, slides, wipes, zooms, blurs and more) and `pageTransitionDuration` (0–2s, default 0.5) between scenes. A string `audioSource` then lays one continuous soundtrack across the combined video, the recipe for multi-scene videos.
- `audioSource` swaps an existing URL audio track at render time while keeping its saved trim/fades/volume/offset/loop. Generated narration changes through `tts.parameterId` instead (see Audio below).
- Captions: `subtitleSource` (a media URL to auto-transcribe, or a `.srt`/`.vtt` used as-is), `captionPreset` (`pill` | `minimal` | `karaoke` | `bold` | `outline` | `neon`), plus fine-grained `subtitleMode` (`phrase`|`word-by-word`), `subtitleWordReveal` (`appear`|`highlight`|`align`), `subtitleSplit` (`word`|`letter`), `subtitleMaxWordsPerLine` or `subtitleMaxCharsPerLine`, and `subtitle*` styling keys. Prefer authored `page.subtitle` with source `"auto-audio"` so captions word-sync automatically.

### Async render jobs (long videos, use this from automations)

A synchronous render holds the HTTP connection for the full render time; video routinely outlives client timeouts (Zapier ~30s, many MCP clients 120s). Add `response.mode: "async"`:

```
POST /v1/studio/render  { ..., "response": { "mode": "async", "format": "mp4" } }
  → 202 with a job object in ~100ms
GET  /v1/studio/render-jobs/:id          → poll the job (queued → processing → succeeded/failed/canceled)
GET  /v1/studio/render-jobs?status=&limit=  → newest-first list
POST /v1/studio/render-jobs/:id/cancel   → cancel while not terminal
```

The job's `result` is byte-identical to the sync response. Pass a `webhook_url` to get the settled job POSTed to you instead of polling. Jobs time out at 15 minutes.

### Page animations & ambient motion (video templates)

Elements animate via a page-level `transitions` object on the element, no video file needed:

```json
{
  "transitions": {
    "enter": { "type": "slideInUp", "duration": 0.5, "easing": "ease-out" },
    "showAt": 0.4,
    "ambient": { "type": "kenBurns", "customValues": { "zoom": 1.12, "panX": 6 } },
    "exit": { "type": "fadeOut", "duration": 0.3 },
    "hideAt": 3.6
  }
}
```

- Three phases: `enter` → `ambient` (plays the element's whole visible life) → `exit`. `showAt`/`hideAt` are siblings of `enter`/`exit`, never nested inside them (the #1 authoring bug).
- Ambient types: `kenBurns` (runs once, stretched across visibility, give every full-bleed photo one), plus looping `pulse`, `float`, `drift`, `wiggle`, `shake`, `slowRotate`, `breathe`. `shake`/`slowRotate` need `easing: "linear"` or the loop seam shows.
- All timing is tunable per render via dot-notation modifications: `"photo.showAt": 2.1`, `"photo.enterType": "scaleIn"`, `"photo.ambientType": "kenBurns"`, etc.

### Audio: soundtracks & AI voiceover (video templates)

Each page carries `audioTracks` (max 10, page-level, mixed into every mp4/webm render):

- **Existing audio**: `{ "url": "https://...", "trimStart": 33.2, "trimEnd": 44.1, "fadeOut": 1, "volume": 1, "loop": false, "offset": 0 }`: trim to the song's best part; `videoOptions.audioSource` swaps the file at render keeping these settings.
- **AI voiceover**: `{ "tts": { "text": "words to speak", "voiceId": "...", "modelId": "flash", "parameterId": "voiceover" } }` instead of `url`. Synthesized when the template is saved (metered voice minutes; identical scripts are cached and free on re-render). Narration length drives the page length, and `page.subtitle` with source `"auto-audio"` gives word-synced captions with no transcription step.
- **Generated ambient/SFX**: `{ "sfx": { "prompt": "warm modern pulse, instrumental, seamless loop", "seconds": 12 }, "volume": 0.12, "loop": true }`.
- `tts.parameterId` makes the SPOKEN TEXT a render parameter: `modifications: { "voiceover": "new words" }` (multi-page: `"page1@voiceover"`) re-voices the video per render; `"voiceover.voiceId"` / `"voiceover.modelId"` tune the voice.
- Budget narration at ~2 words/second plus 1 second of headroom for the page duration.
- Via MCP, call `orshot_get_audio_authoring_options` first, it returns valid voice ids, models and the workspace's voice allowance in one read-only call.

### Smart Resize (one design → any size)

Render a template at a **different canvas size without redesigning it**: the layout is deterministically re-solved to fit (elements re-anchor, backgrounds stretch, groups move together). Set these on the `response` object:

- **`size`**: *replace* the render size. A preset slug (`"instagram-story"`, `"og-image"`, `"youtube-thumbnail"`, …), a `"WIDTHxHEIGHT"` string (`"1080x1920"`), or use `width` + `height` (10–5000px each).
- **`extraSizes`**: *add* the same design at extra sizes in one call. An array (`["1080x1920", "1080x1080"]`) or a named object (`{ story: "1080x1920", square: "1080x1080" }`). Each output gains a nested `extraSizes` array of `{ size, width, height, content }`.

```json
{
  "templateId": 123,
  "modifications": { "title": "Launch Day" },
  "response": {
    "type": "url",
    "format": "png",
    "size": "1200x630",
    "extraSizes": ["1080x1920", "1080x1080"]
  }
}
```

Image formats only (`png`/`jpg`/`webp`/`avif`), up to 50 extra outputs per call. Each extra output is billed like a page (1 credit). Saved sizes from the Studio Smart Resize panel reproduce their approved preview exactly.

### Response Types

| Type     | Description                                     |
| -------- | ----------------------------------------------- |
| `url`    | Returns a hosted URL to the rendered file       |
| `base64` | Returns base64-encoded content as a string      |
| `binary` | Returns binary file content for custom handling |

### Response Formats

| Format | Type  | Notes                                      |
| ------ | ----- | ------------------------------------------ |
| `png`  | Image | Best quality, larger size                  |
| `webp` | Image | Smaller size, good quality                 |
| `jpg`  | Image | Compressed, no transparency                |
| `avif` | Image | Smallest size, modern browsers             |
| `pdf`  | Doc   | Supports multi-page, clickable links, CMYK |
| `mp4`  | Video | H.264, requires video elements in template |
| `webm` | Video | VP9, web-optimized                         |
| `mov`  | Video | QuickTime container                        |
| `mkv`  | Video | Matroska container                         |
| `gif`  | Video | Animated, no audio support                 |

### Render Usage (credits)

Usage is measured in **credits**. 1 credit = 1 image, 1 PDF page, or 1 second of video.

| Output               | Cost                     |
| -------------------- | ------------------------ |
| Image (PNG/JPG/WebP/AVIF) | 1 credit per image  |
| PDF                  | 1 credit per page        |
| Video (MP4/WebM/MOV/MKV/GIF) | 1 credit per second |

Multi-page templates and Smart Resize extra sizes: each output page/size counts as its own credit. AI modifications (`.prompt`) additionally consume AI Credits.

