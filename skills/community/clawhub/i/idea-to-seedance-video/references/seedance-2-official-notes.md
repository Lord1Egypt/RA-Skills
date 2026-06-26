# Seedance 2.0 Official Notes

These notes are extracted from the user's document: `🎬 即梦 Seedance 2.0 使用手册（全新多模态创作体验）.docx`. Use this file for Seedance 2.0 entry selection, reference syntax, constraints, and prompt design. If the live Seedance UI or a newer user-provided guide differs, follow the newer source.

## Core Model Idea

Seedance 2.0 supports text, image, video, and audio inputs. Treat uploaded assets either as direct use objects or as reference objects. The prompt must clearly say what each asset controls: role/subject, first frame, scene, prop, material, camera language, action rhythm, transition, effect, music, sound, or voice.

The guide emphasizes:

- Image reference: composition, character details, product details, scene details.
- Video reference: camera language, complex action rhythm, transitions, effects, performance, and sound cues.
- Audio reference: rhythm, ambience, music, voice/timbre, sound effect direction.
- Video extension: continue before or after a source video with smooth continuity.
- Video editing: replace, delete, add, or change characters/actions in an existing video.

## Input Limits

- Images: `jpeg`, `png`, `webp`, `bmp`, `tiff`, `gif`; up to 9 images; each under 30 MB.
- Videos: `mp4`, `mov`; up to 3 videos; total reference-video duration 2-15s; each under 50 MB; total pixel count 409600 to 927408.
- Audio: `mp3`, `wav`; up to 3 audio files; total duration no more than 15s; each under 15 MB.
- Text: natural language.
- Output duration: choose 4-15s.
- Mixed-input total limit: up to 12 uploaded files.
- Output sound: Seedance can produce sound effects/music.

## Entry Selection

- Use `首尾帧` when there is only a first-frame image plus prompt, or when the task needs first/last-frame control.
- Use `全能参考` for multimodal combinations of image, video, audio, and text.
- Do not recommend `智能多帧` or `主体参考` for this Seedance 2.0 workflow; the guide says they are not selectable in this context.

## Reference Syntax

Use `@素材名` to name each asset's role. Examples:

```text
@图片1 作为首帧，参考@视频1的打斗动作。
@图片1为角色造型，@图片2为场景，@视频1参考运镜和转场，@音频1用于配乐。
@视频1延长5s，生成时长选择5s。
我要在@视频1和@视频2之间加一个场景，内容为...
```

When there are many assets, keep a small "素材清单" before prompts:

```markdown
- @图片1：主角造型/首帧
- @图片2：场景参考
- @图片3：产品材质参考
- @视频1：运镜/动作节奏参考
- @音频1：配乐/音色参考
```

## Realistic Human Face Restriction

The guide says the platform currently does not support uploading materials containing realistic human faces, including image and video assets. Clear identifiable real-person faces may be blocked before generation. When a user's workflow depends on a realistic face reference, warn them and suggest safer alternatives:

- Use non-realistic illustration, stylized character, silhouette, back view, masked/obscured face, product-only shot, or non-human subject.
- Generate a less realistic character sheet when possible, but warn that very realistic AI-generated faces may still be treated as face material.
- For action/camera references, prefer reference videos without clear human faces.

## Prompt Patterns By Task

### Basic text-to-video

Use when no fixed reference is needed.

```text
[镜头/景别]，[主体]在[场景]中[连续动作]，[镜头运动]，[光线/色彩/风格]，[情绪/声音]，画面自然流畅。
```

### Image-led video

Use when an image locks subject, product, first frame, location, or style.

```text
@图片1作为[首帧/主体/产品/场景/风格参考]，[主体动作]，[镜头运动]，[需要保持的细节]，[情绪/声音/风格]。
```

### Video reference for motion/camera/effects

Use when copying camera language, action, transition, rhythm, or effects.

```text
参考@视频1的[运镜/动作节奏/转场/特效/剪辑节奏]，用@图片1的[主体/产品/角色]在@图片2的[场景]中完成[新故事动作]，保持[质感/光影/节奏]。
```

### Multi-reference composition

Assign every reference a job.

```text
@图片1为主体1造型，@图片2为主体2造型，@图片3为武器/道具，@图片4为场景，参考@视频1的动作节奏和运镜，生成[故事动作]。0-2秒...，3-8秒...，9-15秒...。
```

### Video extension

State direction and extension length. The selected generation length should equal the new segment duration.

```text
将@视频1向后延长6s。0-2秒...，3-5秒...，5-6秒...。保持原视频的主体、光线、镜头方向和情绪连续。
```

### Video editing

Specify the source video, the target change, and what must remain unchanged.

```text
基于@视频1，只修改[角色/动作/发型/道具/剧情]，保持原视频的[场景/运镜/剪辑逻辑/光线]不变。新的故事线为...
```

### Music beat / audio-led video

Specify rhythm target and visual beat mapping.

```text
参考@音频1或@视频1的音乐节奏，在每个重拍切换[服装/场景/产品角度]，画面根据节拍进行卡点，保持[风格]和[主体一致性]。
```

## High-Value Use Cases

- Character/product consistency across shots.
- Product detail, material, logo, and package display.
- High-control camera movement and complex action replication from reference video.
- Creative template imitation: transition, advertisement structure, MV structure, particle effects, transformation effects.
- Narrative completion from comics, storyboard images, treatment screenshots, or scene references.
- Smooth one-take camera paths through multiple locations.
- Existing-video continuation and local story edits.
- Music beat editing and rhythmic fashion/product cuts.
- Emotional performance: expression shifts, meltdown, surprise, fear, comedy exaggeration.

## Practical Prompting Advice

- Write in natural language, but be explicit about "参考" vs "编辑" vs "作为首帧/主体/场景".
- Use time ranges for 8-15s videos: `0-2秒`, `3-6秒`, `7-12秒`, `13-15秒`.
- Keep the main action continuous; describe how one action transitions into the next.
- For one-take shots, explicitly say `全程不要切镜头，一镜到底`.
- For continuity, repeat identity, wardrobe, prop, product, lighting, and scene constraints.
- For product videos, reference side angle, material, logo/text, use case, and final packshot separately.
- For text/logo on products, prefer image references; text can still deform, so warn users to verify.
- For unwanted captions, include `画面中不出现字幕、文字、水印、UI界面`; the comments suggest this may not always be fully controllable, especially in some vertical-video/audio cases.
- Split complex stories into several 4-15s shots instead of asking one prompt to do too much.

## Known Risks From Guide And Comments

Use these as quiet production cautions, not as dramatic disclaimers:

- Realistic face references can be blocked, including some realistic AI-generated faces.
- Video references with clear human faces may fail even when used only for motion or camera.
- Captions/subtitles may appear despite negative wording; plan for post-removal if no-text output is critical.
- Long prompts with many references can confuse asset roles; add a material list.
- Product consistency is generally easier than realistic human identity consistency.
- Prompt compliance, queue time, and review outcomes may vary with account, model choice, platform status, and moderation.
