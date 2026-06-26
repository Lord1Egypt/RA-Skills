---
name: idea-to-seedance-video
description: Convert a user's raw creative idea, synopsis, scene concept, brand story, short-video idea, or Chinese-language creative brief into a polished director/screenwriter treatment, complete script, shot breakdown, and Seedance 2.0-ready AI video prompts. Use when the user asks for script polishing, film/advertising/MV/short-drama story development, storyboard planning, text-to-video prompts, image-to-video prompts, first/last-frame prompts, omni-reference prompts using images/videos/audio, video extension/editing prompts, or image-generation prompts for video production.
---

# Idea To Seedance Video

## Output Language

Respond in the user's language. Default to Chinese when the user's creative brief is Chinese. Keep technical labels such as `Seedance 2.0`, `Text-to-Video`, `Image-to-Video`, `首尾帧`, and `全能参考` when useful.

## Core Workflow

1. Extract the creative intent: genre, theme, audience, duration, platform, tone, protagonist, conflict, emotional arc, visual style, required product/brand/message, and constraints.
2. Ask only for missing information that materially changes the result. If the user provides little detail, make tasteful assumptions and state them briefly before writing.
3. Rewrite the idea as a director/screenwriter treatment:
   - Logline
   - Theme and emotional hook
   - World and visual style
   - Character setup
   - Three-act or beginning-middle-end structure
   - Key dramatic beats
4. Produce a complete script appropriate to the requested format:
   - For narrative film/short drama: scene headings, action, dialogue, emotional subtext, transitions.
   - For ads/social videos: hook, visual beat, product/message beat, CTA if appropriate.
   - For music/fashion/atmospheric pieces: visual progression, rhythm, movement, camera, mood.
5. Break the script into shots. For each shot, decide the Seedance generation method and Seedance entry:
   - `Text-to-Video` when the shot can be described clearly without fixed identity, exact object continuity, or strict starting/ending frames.
   - `Text-to-Image + Image-to-Video` when character/product/scene design must be locked before motion.
   - `首尾帧 / First-Last Frame` when the shot must transform from one precise state to another, preserve composition across a planned transition, or match a designed ending.
   - `全能参考 / Omni Reference` when the shot needs multimodal references: images, videos, audio, text, camera language, action rhythm, effects, music, or editing.
6. Generate production-ready prompts. Include image prompts when images are needed, then video prompts for Seedance 2.0.
7. Add a concise production note: continuity risks, recommended image tool, aspect ratio, duration, and suggested iteration order.

## Script Standards

Write like a professional director and screenwriter:

- Replace vague ideas with playable actions, visual conflict, and concrete cinematic details.
- Build an emotional arc, not just a sequence of pretty shots.
- Use subtext in dialogue; avoid explaining what the image already shows.
- Give characters specific wants, obstacles, and behavioral texture.
- Keep scenes shootable: concrete locations, visible actions, motivated camera movement, and clear transitions.
- Maintain continuity of character identity, wardrobe, props, lighting, time of day, and spatial geography.
- If the user's idea is weak or scattered, preserve the core spark while restructuring it into a coherent piece.

## Seedance 2.0 Prompt Standards

Seedance prompts should be direct, visual, and motion-aware. Prefer one shot per prompt.

When a task needs exact Seedance 2.0 limits, modes, entry selection, or reference syntax, read `references/seedance-2-official-notes.md`. Treat newer user-provided Seedance docs or visible UI options as authoritative if they differ.

### Prompt Structure

Use this structure unless the user requests another format:

```text
主体/角色 + 场景/时间 + 动作/事件 + 镜头运动 + 景别/构图 + 光线/色彩 + 风格/质感 + 情绪 + 技术约束
```

For English prompts, use:

```text
Subject + setting/time + action + camera movement + framing/composition + lighting/color + style/texture + mood + constraints
```

### Include

- Subject identity: age, appearance, wardrobe, object/product details.
- Scene specifics: place, era, time, weather, set dressing.
- Action and motion: what changes during the clip; use clear verbs.
- Camera: static, handheld, dolly-in, tracking, orbit, crane, push-in, pull-back, pan, tilt, close-up, wide shot.
- Composition: foreground/background, depth, lens feeling, angle.
- Lighting and color: natural light, neon, candlelight, cool moonlight, warm practicals, high contrast, soft diffusion.
- Style: cinematic realism, luxury commercial, documentary, anime, watercolor, claymation, noir, etc.
- Duration/aspect ratio if known.
- Negative constraints: no text, no watermark, no distorted hands, no extra limbs, no identity drift, no logo deformation, no flicker.

### Avoid

- Abstract instructions with no visible action.
- Multiple unrelated events in one short prompt.
- Contradictory camera directions.
- Overloaded style piles that fight each other.
- Long dialogue inside video prompts. Put dialogue in the script; keep video prompts visual.
- Asking the model to preserve exact text unless a reference image has already locked it.

## Generation Method Decision Guide

Use this table when choosing a method:

| Need | Recommended method | Reason |
|---|---|---|
| Fast ideation, broad atmosphere, simple subject | Text-to-Video | Best for exploratory shots without strict continuity. |
| Only a first frame image plus prompt | 首尾帧入口 | The official guide says this can use the first/last-frame entry. |
| First frame and last frame are both designed | 首尾帧入口 | Best for planned reveal, transformation, or exact ending. |
| Same protagonist/product across many shots | Text-to-Image + Image-to-Video or 全能参考 | Lock design first, then animate; use references for continuity. |
| Product packshot must stay accurate | 全能参考 with product images | Reference images protect shape, color, logo, and materials. |
| Shot uses several reference inputs: character, product, location, style | 全能参考 | Use `@素材名` to specify each image's role. |
| Shot must imitate camera movement, action rhythm, transitions, effects, or music | 全能参考 with video/audio | Reference video/audio carries motion, editing, and sound. |
| Extend an existing video | 全能参考 with source video | Choose the generation duration as the newly extended segment length. |
| Edit an existing video: replace, add, delete, or change character/action | 全能参考 with source video | Specify the original video and the exact change. |
| Complex narrative scene with dialogue | Split into multiple short shots | Seedance prompts should stay visual and concise. |

## Seedance 2.0 Official Constraints

Apply these constraints from the provided Seedance 2.0 guide:

- Images: `jpeg`, `png`, `webp`, `bmp`, `tiff`, `gif`; up to 9 images; each under 30 MB.
- Videos: `mp4`, `mov`; up to 3 videos; total reference-video duration 2-15s; each under 50 MB; total pixel range 409600 to 927408.
- Audio: `mp3`, `wav`; up to 3 audio files; total duration up to 15s; each under 15 MB.
- Mixed multimodal upload limit: up to 12 files total.
- Generated video duration: choose 4-15s.
- Current entries: use `首尾帧` for first-frame/last-frame style work; use `全能参考` for multimodal references. Do not recommend `智能多帧` or `主体参考` for Seedance 2.0 when following this guide.
- Use `@素材名` in prompts to assign roles, such as `@图片1 作为首帧`, `@视频1 参考运镜和动作节奏`, `@音频1 用于配乐`.
- Do not ask the user to upload realistic identifiable human-face images or videos; the guide says these are currently blocked by compliance checks.

## Image Prompt Guidance

When the chosen method uses images, provide a separate image-generation prompt before the Seedance video prompt.

Recommend tools by need:

- `GPT-Image` or `ChatGPT image generation`: best for prompt adherence, character/product concept images, first/last frames, storyboard frames, and iterative art direction.
- `Midjourney`: best for high-aesthetic moodboards, fashion/editorial looks, cinematic stills, and stylized visual exploration.
- `Flux`/`Stable Diffusion`: best when the user needs local control, LoRA/IP-Adapter/ControlNet workflows, batch variations, or consistent custom characters.

Image prompts should specify:

- Exact frame purpose: character reference, product reference, location plate, first frame, last frame, or style reference.
- Aspect ratio matching final video.
- Character/product continuity details.
- Composition and camera angle.
- Lighting and color.
- Style and realism level.
- Negative constraints: no text unless required, no watermark, no extra fingers, no warped logo, no duplicate face.

## Output Format

Use this default structure:

```markdown
## 创意升级
- 核心概念：
- 类型与基调：
- 主题：
- 受众/平台：
- 视觉关键词：

## 导演阐述
...

## 完整剧本
### 场景 1：...
...

## 分镜与 Seedance 2.0 方案
| 镜头 | 内容 | 入口/生成方式 | 素材准备与@引用 | 画面/图片提示词 | Seedance 2.0 视频提示词 | 避坑提示 | 参数建议 |
|---|---|---|---|---|---|---|---|

## 制作建议
- 先生成/锁定：
- 再生成视频：
- 连贯性注意：
- 可替代方案：
```

For long scripts, group shots by sequence instead of using one huge table. Keep each video prompt separately copyable.

## Quality Checklist

Before finalizing, verify:

- The rewritten story preserves the user's original creative spark.
- The script has conflict, progression, and an ending.
- Each shot has one primary visible action.
- Generation method choices are justified by continuity/control needs.
- Any required image prompt appears before the video prompt that depends on it.
- Seedance entry choice is explicit: `首尾帧` or `全能参考` when references are involved.
- Referenced assets are named with `@图片1`, `@视频1`, `@音频1`, and each asset's purpose is unambiguous.
- Prompts include camera, motion, lighting, composition, style, and negative constraints.
- Character/product continuity details repeat where needed.
- Generated durations stay within 4-15s unless the user's active UI says otherwise.
- Reference assets respect count, format, size, and realistic-face restrictions from the guide.
- The output is practical for a user to copy into Seedance 2.0.

## If Seedance Tutorial Details Are Provided

If the user pastes Seedance 2.0 documentation, screenshots, parameter lists, or private tutorial text, treat that content as authoritative for the current task. Extract only the relevant operating rules, update prompt structure and parameter recommendations accordingly, and avoid claiming details that are not present in the provided tutorial.
