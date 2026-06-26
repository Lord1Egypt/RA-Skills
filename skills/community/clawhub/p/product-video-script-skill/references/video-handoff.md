# Video Handoff

Use this when scripts are handed to a video generation skill/tool.

Entry condition:
- Use this file only after the user explicitly asks to generate video.
- Do not use this file immediately after the user merely selects a script direction.
- Script approval/selection and storyboard approval are different. A script must be shown first; storyboard review can be skipped only inside the video-generation phase.
- Preserve the confirmed script as the source of truth. Do not rewrite, expand, translate, or optimize it into a new creative prompt during handoff.

Default audio route:
- Generate native audio/voiceover inside the video generation request.
- Put the full voiceover and audio direction directly in the video prompt.
- Do not create separate TTS audio.
- Do not create a silent video and compose it with audio later.
- Do not use a `video + TTS + compose` workflow unless the user explicitly requests separate voiceover production.
- The final deliverable must be one complete video with audible sound/voiceover.

Default visual text route:
- Do not add subtitles, captions, karaoke captions, title cards, price stickers, promotional text, floating labels, lower thirds, UI panels, or generated text overlays.
- Do not burn the voiceover into the video as subtitles.
- Product packaging text and logos already present in the reference image may remain, but do not invent new text.
- Put all selling points in the voiceover and visual demonstration, not on-screen text.

## Single Video Handoff

Use this for all non-TVC directions, including 带货口播, 场景种草, 促销活动, 测评对比, 海外 TikTok 风格, and 直播间真人带货.

Core rule:
- Use the product image as the reference image.
- Directly submit one complete video generation task for the full 15s video.
- Generate the video with native audio/voiceover directly.
- Do not generate storyboard images, character design images, or separate video clips.
- Do not split the script into timestamp segments, shot segments, or clip segments.
- Do not generate separate TTS audio or use later audio-video composition.
- Do not add a storyboard review/confirmation step.

Include:
- first sentence with fixed generation target: `请基于这张产品参考图，直接生成一条15秒、9:16竖屏、带声音/口播、无字幕、无屏幕文字的完整短视频。`
- title
- selected direction
- duration and ratio
- reference image URLs or local paths
- context isolation line
- product appearance constraints
- continuous visual flow, without timestamps or clip segments
- full voiceover
- native audio instruction
- no-subtitles/no-text-overlay instruction
- avoid list
- success criteria

Required non-TVC constraint line:

`不要先生成分镜图、角色设计图或分段视频，也不要等待用户确认分镜。不要按镜头、时间段或脚本段落拆成多个视频片段，不要多段生成后合并。请一次性直接输出完整成片。`

Required audio constraint line:

`请在视频生成时直接生成声音/口播，不要单独生成TTS音频，不要先生成无声视频再后期合成。最终交付必须是一条带声音的完整视频。`

Required no-text constraint line:

`不要添加任何字幕、口播字幕、屏幕文字、标题卡、价格贴片、促销文字、漂浮标签或生成式文字。画面里只保留产品本身已有的包装文字/Logo，不额外生成新文字。`

## Batch Video Handoff

For multiple videos, create one manifest item per video. Keep each item self-contained so a downstream video skill can submit separate tasks without reading prior items.

For LibTV, one script equals one video task. Do not merge multiple scripts into one prompt or ask LibTV to choose among concepts.

If prior tasks in the same agent/session used another product, create or switch to a clean video-tool project/canvas before uploading the new product reference image. For LibTV, call `change_project.py`, then upload the product image, then submit the generation task. If prior tasks used another campaign or language, recommend a clean project/session before generation.

Template:

```markdown
## Batch Manifest

### Video 1: <title>
- Context isolation: This is a new standalone product task. Do not inherit any previous product, campaign, 618, 双11, price, or activity context unless repeated in this prompt.
- Direction:
- Duration:
- Ratio:
- Reference image:
- Product constraints:
- Voiceover:
- Continuous visual flow:
- Subtitle / on-screen text policy: none. Do not add subtitles, captions, title cards, price stickers, floating labels, or generated text overlays.
- Avoid:
- Success criteria:

### Video 2: <title>
...
```

## Generation Strategy

- Treat each script variant as a separate video task.
- For LibTV, submit scripts sequentially or as separate tasks; do not pack multiple scripts into one prompt.
- Each video task must generate one complete 15s video. Do not split a single script into several clip tasks or merge generated clips afterward.
- Require a new project/canvas when changing products. For LibTV, call `change_project.py` before uploading the new product reference image.
- Prefer a new session when changing language, platform, or removing a previously used campaign context.
- If the tool has unknown concurrency limits, avoid promising a batch size. Say that batching means preparing multiple self-contained tasks, not guaranteeing simultaneous execution.
- For AI video tools that often garble text, use no text. Put detailed selling points in voiceover.
- Every video task must explicitly forbid subtitles, captions, title cards, price stickers, floating labels, and generated text overlays.
- For sound/voiceover, use native audio in the video generation request. Do not split into separate TTS and later composition.
- For product-reference fidelity, include exact visible traits from the product image in every item.
- If campaign language is not wanted, repeat the avoid list in every item: no 618, no 双11, no限时促销, no价格贴片, no shopping festival language.

## Commercial/TVC Storyboard-First Handoff

Use this only when the selected direction is `商业广告/TVC`. Do not use this workflow for 带货口播, 场景种草, 促销活动, 测评对比, 海外 TikTok 风格, or 直播间真人带货.

Workflow:
1. Generate 5 key 9:16 storyboard images.
2. Check that each storyboard preserves product identity and has no unwanted text. This is an internal check, not a required user confirmation step.
3. Use the 5 storyboard images together as reference images for one complete 15s 9:16 video.
4. Continue from storyboard images to final video automatically unless the user explicitly asked to review/approve storyboard images first.

Storyboard slots:
- Frame 1: hero product establishing shot
- Frame 2: lifestyle/user scene
- Frame 3: product texture/detail/macro
- Frame 4: emotional payoff or use result
- Frame 5: final product/brand end frame

Handoff prompt must include:
- first sentence with fixed generation target: `请生成一条15秒、9:16竖屏、带声音/口播、无字幕、无屏幕文字的商业广告/TVC视频。`
- original product image
- 5 storyboard descriptions
- instruction to create storyboard images first
- instruction to use all storyboard images together as references for final video
- instruction to continue to final video automatically after storyboard images unless the user explicitly requested storyboard approval
- instruction to generate native audio/voiceover inside the final video request, not as separate TTS plus composition
- no subtitles, no captions, no title cards, no price stickers, no floating labels, and no generated text overlays
- full voiceover or music direction

## Commercial/TVC Batch Execution

When the user chooses to generate multiple TVC scripts, keep the user-facing action as `把这几条全部交给 LibTV 批量生成`, but execute internally as a serial batch.

Rules:
- Use unique IDs: `TVC-01`, `TVC-02`, `TVC-03`.
- Submit only one TVC storyboard-first job at a time.
- The first sentence of every submitted TVC prompt must include: `15秒、9:16竖屏、带声音/口播`.
- Every submitted TVC prompt must require native audio/voiceover in the final video and must not request separate TTS plus composition.
- Every submitted TVC prompt must forbid subtitles, captions, title cards, price stickers, floating labels, and generated text overlays.
- Wait until that TVC has final video URL(s), or reaches a clear failure/timeout state, before submitting the next.
- Prefer a new video-tool session for each TVC when the tool is conversational or likely to merge multiple tasks.
- Record results before moving on: storyboard status, final video URL, failure reason, or timeout.
- Do not pack several TVC concepts into one prompt.

Timeout guidance:
- If storyboard images are created but final video is not complete after a reasonable wait, report that state and continue only if the user asked for continued autonomous batching.
- If the tool asks for confirmation because it sees multiple tasks, confirm only for the current TVC, not the whole batch.

## Parameter Loss Check

If a generated video returns with the wrong duration, ratio, or no sound, first inspect the actual message sent to the video tool. The script output may contain the correct values, but the handoff prompt must also explicitly include:
- 15秒
- 9:16竖屏
- 带声音/口播
- 直接生成声音/口播，不要单独TTS或后期合成
- 无字幕、无屏幕文字、无文字贴片

If any of these are missing from the actual handoff prompt, regenerate with a corrected prompt before changing the creative script.

## Regeneration Strategy

When the user is unhappy with a script, ask for the failure type only if it is unclear:
- hook weak
- too salesy
- not native to platform
- product selling points inaccurate
- too generic
- tone mismatch
- needs more drama/funniness/premium feeling

Then regenerate with one of these changes:
- new hook, same structure
- same hook, different scenario
- different direction
- more restrained text overlay
- more product close-ups
- stronger CTA
