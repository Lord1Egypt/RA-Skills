# Intelligent Orchestration

## Decision Model

Resolve a request in this order:

1. **Explicit resource**: call the named model/application if tenant discovery confirms it and the supplied inputs satisfy its contract.
2. **Explicit operation**: map a phrase such as "对口型", "视频超分", "真人口播混剪", "音色转换", or "生成歌词" to the catalog operation.
3. **Outcome**: construct the smallest DAG that creates the missing input types. Ask only for irreducible inputs or a material choice.
4. **Management/query**: do not turn asset listing, template lookup, social lookup, or task query into a generation workflow.

Before every paid node: discover availability, validate inputs, upload local media, and obtain price when the user is cost-sensitive. After every node: verify `code=1`, extract a documented ID/URL, validate its type, then continue.

## Direct Capability Families

| User outcome | Eligible operations | Required input type |
| --- | --- | --- |
| Generate or edit an image | Image models; `nano_banana/submit`; `dressing_diffusion/submit` | Prompt, optionally reference/model/garment image |
| Generate a video | Video models; Seedance, Happy Horse, Wan, Omni, Grok, Full Video, Seedance Pro | Prompt, optionally reference images/video/audio |
| Generate speech | `voice_tts/tts`, `tts_async`, `tts_live`, `indextts/submit` | Text; IndexTTS additionally requires reference audio |
| Clone a voice | `voice_tts/clone_voice`, `music_generation/voice_clone` | Clear reference audio; choose domain based on the downstream task |
| Convert/copy a voice | `seedsvc/submit` | Reference audio plus source audio |
| Make a talking video | `lipsync/submit` | Audio URL plus source video URL |
| Create an avatar video from image | `image_human/submit` | Portrait image plus driving audio |
| Enhance a video | `flashvsr/submit` | Video URL |
| Add sound effects or dub video | `mmaudio/submit` | Video URL, optional audio/prompt |
| Replace person / transfer action | Corresponding submit API | Source person image(s) plus driving video |
| Remove watermark or resolve social media | `watermark_removal/*` | Public share URL or platform identifiers |
| Make music or derive music assets | `music_generation/*` | Prompt, lyrics, audio URL, audio ID, or persona ID as documented |
| Smart Clip | `smart_clip/*` | Scene-compatible template plus video/audio/material assets |

## Supported Composite Recipes

### Direct Lipsync

```text
local audio/video (if any) -> upload -> lipsync/submit -> platform task poll -> video_url
```

Ask for the missing source video or audio. Do not substitute an image for `video_url`.

### Text To Talking Video

```text
text + existing voice_tts reference_id + source video
-> voice_tts/tts or tts_async
-> audio_url
-> lipsync/submit
-> video_url
```

Use sync TTS for short text; offer async TTS for long text. The TTS result must contain an audio URL before lipsync starts.

### Clone Voice To Talking Video

```text
reference audio -> voice_tts/clone_voice -> clone id
text + clone id -> voice_tts/tts or tts_async -> audio_url
audio_url + source video -> lipsync/submit -> video_url
```

Preflight availability and pricing for all paid nodes. Create the clone once and retain its returned ID; never retry clone creation blindly.

### Avatar Image To Smart-Edited Talking Video

```text
portrait image + driving audio -> image_human/submit -> video_url
smart_clip/template(scene=realMan) -> template choice
video_url + template styleId -> smart_clip/realman_broadcast -> final video_url
```

For a text-led request, place TTS or voice cloning before `image_human`. If several templates match, present template name, cover/demo URL, and price-impacting options for user choice.

### Existing Talking Video To Smart Clip

```text
source video -> smart_clip/template(scene=realMan) -> optional template_detail
-> realman_broadcast(styleId, videoUrl) -> final video_url
```

Use `processRules.resourcePreprocessMethod=roughCut` only when the user requests automatic silence/rough cutting. Use `sliceMerge` only with validated subtitle time ranges.

### Audio Plus Materials To Smart Clip

```text
audio + images/videos -> upload -> template(scene=oralMixCutting)
-> broadcast_mixcut(styleId, audioUrl, materials[].fileUrl) -> final video_url
```

Do not use the unsupported `content + speakerId` branch. Material URLs, audio URLs, background music, and cover URLs must be distinct where the contract requires it.

### News Materials To Smart Clip

```text
title + images/videos -> upload -> template(scene=newsMixCutting)
-> news_mixcut(styleId, title, materials) -> final video_url
```

Ask for a title and template if missing. Honor requested `videoDuration` and ordered/random material composition.

### Generate Then Enhance Or Edit Video

```text
prompt/reference media -> selected video generator -> video_url
-> optional flashvsr -> enhanced video_url
-> optional compatible Smart Clip scene -> final video_url
```

Never assume every video generator output is suitable for every downstream model. Confirm its public reachability, media type, and duration before passing it on.

### Image To Video

```text
prompt -> selected image generator -> image_url
-> selected image-to-video model/app -> video_url
```

Choose only a generator contract that accepts reference images. For first/last-frame requests, select a capability explicitly supporting both fields; do not overload a reference-image-only contract.

### Music Workflows

```text
prompt -> lyrics/style (optional) -> music_generation/create -> audio_id/audio_url
audio_url -> music_generation/upload_audio -> audio_id
audio_id -> persona/vox/wav/mp4/midi/timing as requested
```

Keep music-domain IDs inside `music_generation`. A `voice_tts` clone ID and a music `persona_id` are different resources.

## Non-Combination Rules

- Do not connect a task ID to a media URL field, or a media URL to an ID field.
- Do not use an elastic task ID in generic task polling, or a platform `task_id` in a legacy query endpoint unless the contract states it accepts one.
- Do not invoke social retrieval with a local file; it requires public platform share URLs or identifiers.
- Do not silently add watermark, change resolution, duration, model tier, or Smart Clip template.
- Do not auto-delete Seedance assets. Obtain confirmation immediately before `deleteAsset`.
