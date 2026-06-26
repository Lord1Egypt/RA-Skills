---
name: google-gemini-media
description: Use the SkillBoss API Hub (image generation, video generation, TTS speech and audio understanding) to deliver end-to-end multimodal media workflows and code templates for "generation + understanding".
license: MIT
requires.env: [SKILLBOSS_API_KEY]
---

# Multimodal Media (Image/Video/Speech) Skill — powered by SkillBoss API Hub

## 1. Goals and scope

This Skill consolidates six multimodal media capabilities into reusable workflows and implementation templates, all routed through SkillBoss API Hub (`https://api.skillbossai.com/v1/pilot`):

- Image generation (text-to-image, image editing, multi-turn iteration)
- Image understanding (caption/VQA/classification/comparison, multi-image prompts)
- Video generation (text-to-video, aspect ratio/resolution control, reference-image guidance)
- Video understanding (summaries, Q&A, timestamped evidence)
- Speech generation (TTS: single-speaker and multi-speaker; controllable style/accent/pace/tone)
- Audio understanding (description, transcription, time-range transcription)

> Convention: All API calls go through SkillBoss API Hub `/v1/pilot`, which automatically routes to the optimal underlying model. Authentication uses a single `SKILLBOSS_API_KEY`.

---

## 2. Quick routing (decide which capability to use)

1) **Do you need to produce images?**
- Need to generate images from scratch or edit based on an image -> use **Image generation** (see Section 5)

2) **Do you need to understand images?**
- Need recognition, description, Q&A, comparison, or info extraction -> use **Image understanding** (see Section 6)

3) **Do you need to produce video?**
- Need to generate a short video (optionally with native audio) -> use **Video generation** (see Section 7)

4) **Do you need to understand video?**
- Need summaries/Q&A/segment extraction with timestamps -> use **Video understanding** (see Section 8)

5) **Do you need to read text aloud?**
- Need controllable narration, podcast/audiobook style, etc. -> use **Speech generation (TTS)** (see Section 9)

6) **Do you need to understand audio?**
- Need audio descriptions, transcription, time-range transcription -> use **Audio understanding** (see Section 10)

---

## 3. Unified engineering constraints and I/O spec (must read)

### 3.0 Prerequisites (dependencies and tools)

- Node.js 18+ (match your project version)
- No additional SDK required — all calls use standard `fetch` (built-in to Node 18+):
```bash
# No extra install needed for Node.js 18+
# For older environments you can use: npm install node-fetch
```

### 3.1 Authentication and environment variables

- Put your API key in `SKILLBOSS_API_KEY`
- All requests use `Authorization: Bearer $SKILLBOSS_API_KEY`

### 3.2 Shared helper function

All examples below use this shared `pilot()` helper:

```js
const SKILLBOSS_API_KEY = process.env.SKILLBOSS_API_KEY;
const API_BASE = "https://api.skillbossai.com/v1";

async function pilot(body) {
  const r = await fetch(`${API_BASE}/pilot`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${SKILLBOSS_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  return r.json();
}
```

### 3.3 Unified handling of binary media outputs

- **Images**: returned as `result.image_url` (URL) or `result.images[0].url` in the response.
- **Speech (TTS)**: returned as `result.audio_url`.
- **Video**: returned as `result.video_url`; long-running tasks may require polling.

---

## 4. Model selection

> SkillBoss API Hub `/v1/pilot` automatically routes to the optimal underlying model. Use `prefer` to control the trade-off:
> - `"quality"` — best output quality
> - `"price"` — lowest cost
> - `"balanced"` — balanced quality/cost (default)

No need to specify model names manually. The hub selects the best available model for the requested capability.

---

## 5. Image generation

### 5.1 Text-to-Image

**Node.js minimal template**
```js
import * as fs from "node:fs";

const SKILLBOSS_API_KEY = process.env.SKILLBOSS_API_KEY;
const API_BASE = "https://api.skillbossai.com/v1";

async function pilot(body) {
  const r = await fetch(`${API_BASE}/pilot`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${SKILLBOSS_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  return r.json();
}

const result = await pilot({
  type: "image",
  inputs: {
    prompt: "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme",
  },
  prefer: "quality",
});

const imageUrl = result["result"]["image_url"];
console.log("Image URL:", imageUrl);

// Download and save the image
const imgResponse = await fetch(imageUrl);
const buffer = Buffer.from(await imgResponse.arrayBuffer());
fs.writeFileSync("out.png", buffer);
```

**REST (curl) minimal template**
```bash
curl -s -X POST "https://api.skillbossai.com/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "image",
    "inputs": {
      "prompt": "Create a picture of a nano banana dish in a fancy restaurant",
      "aspect_ratio": "16:9"
    },
    "prefer": "quality"
  }'
# Image URL is at: .result.image_url
```

### 5.2 Text-and-Image-to-Image (editing)

Use case: given an image, **add/remove/modify elements**, change style, color grading, etc.

**Node.js minimal template**
```js
import * as fs from "node:fs";

const SKILLBOSS_API_KEY = process.env.SKILLBOSS_API_KEY;
const API_BASE = "https://api.skillbossai.com/v1";

async function pilot(body) {
  const r = await fetch(`${API_BASE}/pilot`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${SKILLBOSS_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  return r.json();
}

const imageBase64 = fs.readFileSync("input.png").toString("base64");

const result = await pilot({
  type: "image",
  inputs: {
    prompt: "Add a nano banana on the table, keep lighting consistent, cinematic tone.",
    image_data: imageBase64,
    image_mime_type: "image/png",
  },
  prefer: "quality",
});

const imageUrl = result["result"]["image_url"];
const imgResponse = await fetch(imageUrl);
const buffer = Buffer.from(await imgResponse.arrayBuffer());
fs.writeFileSync("edited.png", buffer);
```

### 5.3 Multi-turn image iteration

Best practice: use multiple sequential calls with the previous output fed back as `image_data` for continuous iteration (e.g., generate first, then "only edit a specific region/element", then "make variants in the same style").

### 5.4 Image generation controls

Pass these in the `inputs` object:
- `aspect_ratio`: e.g. `"16:9"`, `"1:1"`
- `size`: e.g. `"1024x1024"`, `"1024x576"` (16:9)

---

## 6. Image understanding

### 6.1 Two ways to provide input images

- **Inline image data**: suitable for small files (Base64 encoded).
- **Image URL**: pass the URL directly if the image is publicly accessible.

### 6.2 Inline images minimal template
```js
import * as fs from "node:fs";

const SKILLBOSS_API_KEY = process.env.SKILLBOSS_API_KEY;
const API_BASE = "https://api.skillbossai.com/v1";

async function pilot(body) {
  const r = await fetch(`${API_BASE}/pilot`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${SKILLBOSS_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  return r.json();
}

const imageBase64 = fs.readFileSync("image.jpg").toString("base64");

const result = await pilot({
  type: "chat",
  inputs: {
    messages: [
      {
        role: "user",
        content: [
          {
            type: "image_url",
            image_url: { url: `data:image/jpeg;base64,${imageBase64}` },
          },
          {
            type: "text",
            text: "Caption this image, and list any visible brands.",
          },
        ],
      },
    ],
  },
  prefer: "balanced",
});

const text = result["result"]["choices"][0]["message"]["content"];
console.log(text);
```

### 6.3 Image URL reference minimal template
```js
const SKILLBOSS_API_KEY = process.env.SKILLBOSS_API_KEY;
const API_BASE = "https://api.skillbossai.com/v1";

async function pilot(body) {
  const r = await fetch(`${API_BASE}/pilot`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${SKILLBOSS_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  return r.json();
}

const result = await pilot({
  type: "chat",
  inputs: {
    messages: [
      {
        role: "user",
        content: [
          {
            type: "image_url",
            image_url: { url: "https://example.com/image.jpg" },
          },
          { type: "text", text: "Caption this image." },
        ],
      },
    ],
  },
  prefer: "balanced",
});

const text = result["result"]["choices"][0]["message"]["content"];
console.log(text);
```

### 6.4 Multi-image prompts

Append multiple images as multiple entries in the `content` array; you can mix URLs and inline Base64 bytes.

---

## 7. Video generation

### 7.1 Core features (must know)
- Generates high-fidelity short video (default ~8 seconds), supporting native audio generation (dialogue, ambience, SFX).
- Supports aspect ratio (16:9 / 9:16), resolution control, and first/last frame guidance via `inputs`.

### 7.2 Node.js minimal template
```js
import * as fs from "node:fs";

const SKILLBOSS_API_KEY = process.env.SKILLBOSS_API_KEY;
const API_BASE = "https://api.skillbossai.com/v1";

async function pilot(body) {
  const r = await fetch(`${API_BASE}/pilot`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${SKILLBOSS_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  return r.json();
}

const result = await pilot({
  type: "video",
  inputs: {
    prompt: "A cinematic shot of a cat astronaut walking on the moon. Include subtle wind ambience.",
    duration: 8,
    aspect_ratio: "16:9",
    resolution: "1080p",
  },
  prefer: "quality",
});

const videoUrl = result["result"]["video_url"];
console.log("Video URL:", videoUrl);

// Download and save
const videoResponse = await fetch(videoUrl);
const buffer = Buffer.from(await videoResponse.arrayBuffer());
fs.writeFileSync("out.mp4", buffer);
```

### 7.3 Common controls

Pass these in the `inputs` object:
- `aspect_ratio`: `"16:9"` or `"9:16"`
- `resolution`: `"720p" | "1080p" | "4k"`
- `duration`: duration in seconds (default 8)
- When writing prompts: put dialogue in quotes; explicitly call out SFX and ambience; use cinematography language.

### 7.4 Important limits (engineering fallback needed)

- Latency can vary from seconds to minutes; implement timeouts and retries.
- Download the video promptly after generation.

**Retry with timeout pseudocode**
```js
const deadline = Date.now() + 300_000; // 5 min
let result = null;
while (Date.now() < deadline) {
  try {
    result = await pilot({
      type: "video",
      inputs: { prompt: "...", duration: 8 },
      prefer: "quality",
    });
    if (result["result"]["video_url"]) break;
  } catch (e) {
    await new Promise((resolve) => setTimeout(resolve, 5000));
  }
}
if (!result) throw new Error("video generation timed out");
const videoUrl = result["result"]["video_url"];
```

---

## 8. Video understanding

### 8.1 Video input options
- **Video URL**: for publicly accessible videos.
- **Base64 inline**: for smaller files.
- **YouTube URL**: can analyze public videos by passing the URL in the message.

### 8.2 Video URL minimal template
```js
const SKILLBOSS_API_KEY = process.env.SKILLBOSS_API_KEY;
const API_BASE = "https://api.skillbossai.com/v1";

async function pilot(body) {
  const r = await fetch(`${API_BASE}/pilot`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${SKILLBOSS_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  return r.json();
}

const result = await pilot({
  type: "chat",
  inputs: {
    messages: [
      {
        role: "user",
        content: [
          {
            type: "video_url",
            video_url: { url: "https://example.com/sample.mp4" },
          },
          {
            type: "text",
            text: "Summarize this video. Provide timestamps for key events.",
          },
        ],
      },
    ],
  },
  prefer: "balanced",
});

const text = result["result"]["choices"][0]["message"]["content"];
console.log(text);
```

### 8.3 Timestamp prompting strategy
- Ask for segmented bullets with "(mm:ss)" timestamps.
- Require "evidence with specific time ranges" and include downstream structured extraction (JSON) in the same prompt if needed.

---

## 9. Speech generation (Text-to-Speech, TTS)

### 9.1 Positioning
- For "precise reading + controllable style" (podcasts, audiobooks, ad voiceover, etc.).
- SkillBoss API Hub auto-routes to the best TTS model for the given inputs.

### 9.2 Single-speaker TTS minimal template
```js
import * as fs from "node:fs";

const SKILLBOSS_API_KEY = process.env.SKILLBOSS_API_KEY;
const API_BASE = "https://api.skillbossai.com/v1";

async function pilot(body) {
  const r = await fetch(`${API_BASE}/pilot`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${SKILLBOSS_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  return r.json();
}

const result = await pilot({
  type: "tts",
  inputs: {
    text: "Say cheerfully: Have a wonderful day!",
    voice: "Kore",
  },
  prefer: "balanced",
});

const audioUrl = result["result"]["audio_url"];
console.log("Audio URL:", audioUrl);

// Download and save
const audioResponse = await fetch(audioUrl);
const buffer = Buffer.from(await audioResponse.arrayBuffer());
fs.writeFileSync("out.mp3", buffer);
```

### 9.3 Multi-speaker TTS
Pass multiple text segments with speaker labels in the `text` field, using a structured format like `"[Speaker1]: Hello\n[Speaker2]: Hi there"`.

### 9.4 Voice options and language
- The `voice` field supports named voices (e.g., `"alloy"`, `"Kore"`, `"Zephyr"`, `"Puck"`).
- Auto-detects input language; supports 24+ languages.

### 9.5 "Director notes" (strongly recommended for high-quality voice)
Prefix the text with style directions, e.g.: `"Speak in a calm, professional tone: [your content here]"`.

---

## 10. Audio understanding

### 10.1 Typical tasks
- Describe audio content (including non-speech like birds, alarms, etc.)
- Generate transcripts
- Transcribe specific time ranges
- Estimate token/cost for long audio

### 10.2 Audio transcription (STT) minimal template
```js
import * as fs from "node:fs";
import { Buffer } from "node:buffer";

const SKILLBOSS_API_KEY = process.env.SKILLBOSS_API_KEY;
const API_BASE = "https://api.skillbossai.com/v1";

async function pilot(body) {
  const r = await fetch(`${API_BASE}/pilot`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${SKILLBOSS_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  return r.json();
}

const audioB64 = fs.readFileSync("sample.mp3").toString("base64");

const result = await pilot({
  type: "stt",
  inputs: {
    audio_data: audioB64,
    filename: "sample.mp3",
  },
});

const transcript = result["result"]["text"];
console.log(transcript);
```

### 10.3 Audio description via chat (for non-transcription tasks)
```js
const audioB64 = fs.readFileSync("sample.mp3").toString("base64");

const result = await pilot({
  type: "chat",
  inputs: {
    messages: [
      {
        role: "user",
        content: [
          {
            type: "audio_url",
            audio_url: { url: `data:audio/mp3;base64,${audioB64}` },
          },
          { type: "text", text: "Describe this audio clip." },
        ],
      },
    ],
  },
  prefer: "balanced",
});

const text = result["result"]["choices"][0]["message"]["content"];
console.log(text);
```

### 10.4 Key limits and engineering tips
- Supports common formats: WAV/MP3/AIFF/AAC/OGG/FLAC.
- If the audio file is large, upload it to a publicly accessible URL first and pass the URL instead of Base64.
- For very long audio, consider splitting into segments.

---

## 11. End-to-end examples (composition)

### Example A: Image generation -> validation via understanding
1) Generate product images via `type: "image"` (specify negative space and consistent lighting in the prompt).
2) Use `type: "chat"` with image understanding for self-check: verify text clarity, brand spelling, and unsafe elements.
3) If not satisfied, feed the generated image into editing and iterate.

### Example B: Video generation -> video understanding -> narration script
1) Generate a short video with `type: "video"` (include dialogue or SFX in the prompt).
2) Download and save the video.
3) Use `type: "chat"` with video to produce a storyboard + timestamps + narration copy; then feed the copy to `type: "tts"`.

### Example C: Audio understanding -> transcription -> TTS redub
1) Upload meeting audio and transcribe with `type: "stt"`.
2) Use `type: "chat"` to summarize or extract specific time ranges.
3) Use `type: "tts"` to generate a "broadcast" version of the summary.

---

## 12. Compliance and risk (must follow)

- Ensure you have the necessary rights to upload images/video/audio; do not generate infringing, deceptive, harassing, or harmful content.
- Production systems must implement timeouts, retries, failure fallbacks, and human review/post-processing for generated content.

---

## 13. Quick reference (Checklist)

- [ ] Set `SKILLBOSS_API_KEY` environment variable.
- [ ] Pick the right `type`: `"image"` for image generation, `"chat"` for understanding tasks, `"video"` for video generation, `"tts"` for speech, `"stt"` for transcription.
- [ ] Use `prefer: "quality"` for best results, `"balanced"` for cost efficiency.
- [ ] Parse responses correctly: images → `result.image_url`; audio → `result.audio_url`; video → `result.video_url`; chat → `result.choices[0].message.content`; stt → `result.text`.
- [ ] For video generation: set `aspect_ratio` / `resolution`, and download promptly.
- [ ] For TTS: pass `voice` name in inputs; use director-style prefix for tone control.
- [ ] For large audio/video files: encode to Base64 or host at a URL first.
