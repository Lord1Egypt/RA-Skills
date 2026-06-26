---
name: product-video-script-no-subtitles-tiktok-ugc
description: Generate ecommerce product video scripts from one or more product images and optional selling points, with video handoff notes that forbid subtitles, captions, text overlays, titles, and price stickers by default. This variant makes the 海外 TikTok 风格 direction default to UGC-style seeding ads with conflict hooks, product-as-rescue positioning, fast visual feedback, and validation endings. Use when the user wants带货视频脚本, 产品视频脚本, 短视频脚本, 无字幕产品视频, TikTok/抖音/小红书/直播间/618/双11 product content ideas, or wants to choose directions such as带货口播、场景种草、促销活动、测评对比、海外 TikTok 风格、直播间带货、商业广告/TVC before producing scripts.
---

# Product Video Script - No Subtitles

Turn product images and optional selling points into platform-ready short-video scripts and video handoff notes.

Default text policy: generated videos must have no subtitles, no captions, no text overlays, no title cards, no price stickers, no floating labels, and no generated UI text. Put selling points in voiceover and visuals instead of on-screen text.

## Core Rule

Use **research-enhanced generation when possible**, but never make research a hard dependency.

- If the user asks for recent, trending, top-liked, platform-specific, or competitor-based scripts and the agent has browsing/search tools, research first and cite sources.
- If browsing/search is unavailable, blocked, or the user wants speed, use the fallback playbooks in `references/direction-playbook.md` and clearly label the result as `未联网版本`.
- Do not invent exact rankings, likes, creator names, or video URLs. Say when exact metrics could not be verified.

## Workflow

State boundary:
- Selecting a direction only authorizes script writing. It is not permission to generate a video.
- After writing any script, stop and show `Next Actions`. Do not call LibTV or any video generation tool yet.
- Enter video generation only after the user explicitly selects `直接生成视频`, `选其中一条去生成视频`, `把这几条全部交给 LibTV 批量生成`, or otherwise clearly asks to generate videos.

1. **Read the product input**
   - Inspect all provided images when image understanding is available.
   - Extract visible product category, appearance, use scene, likely audience, giftability, price/activity clues, and visual risks.
   - Incorporate user-provided selling points. If selling points conflict with the image, mention the uncertainty.
   - Campaign language is opt-in, not forbidden. Use 618, 双11, Black Friday, Christmas, summer, back-to-school, discounts, limited-time offers, or similar campaign framing only when the user explicitly requests it, selects a promotion direction, or the product image clearly contains that campaign. Otherwise keep the script evergreen.

2. **Offer directions if the user has not chosen one**
   Present 5-7 concise choices and wait for the user:
   - 带货口播
   - 场景种草
   - 促销活动（only when the user wants a campaign/deal angle）
   - 测评对比
   - 海外 TikTok 风格
   - 直播间真人带货
   - 商业广告/TVC

3. **Research or fallback**
   - For research mode, search the chosen category + platform + time window + commerce intent.
   - Summarize reusable patterns: hook, pacing, camera style, proof, offer, CTA.
   - For fallback mode, read `references/direction-playbook.md`.

4. **Write the script**
   Use `references/output-template.md` unless the user requests another format.
   Default duration is 15 seconds and default ratio is 9:16 when not specified.
   Include:
   - concept title
   - why this direction fits the product
   - continuous script structure without timestamp tables
   - voiceover
   - continuous visual flow
   - no-subtitle/no-text-overlay policy
   - visual/reference notes
   - optional video handoff notes

5. **Offer next actions**
   After delivering a script, always stop and show next actions:
   - After one script, use the single-script next actions from `references/output-template.md`.
   - After multiple scripts, use the multi-script next actions from `references/output-template.md`.
   - For `商业广告/TVC`, use storyboard-first as the internal video handoff workflow, but keep the user-facing action as `直接生成视频`.
   - For every non-TVC direction, `直接生成视频` means: use the product image as a reference image and directly submit one complete 15s 9:16 video task. Do not create storyboard images, character design images, separate video clips, or a storyboard-confirmation checkpoint.
   - Do not execute any video generation action in this step unless the user's current message already explicitly asks to generate the video, not merely choose a direction.

6. **Quality checks**
   - Hook appears in the first 1-3 seconds.
   - Each claim is supportable from visible product traits or user-provided selling points.
   - Campaign context is explicit. If requested, use it confidently; if not requested, keep the script evergreen and do not add shopping-festival language.
   - Do not plan subtitles, captions, title cards, price stickers, or any generated text overlay.
   - Avoid dense subtitles, tiny price tables, and complex text overlays when the next step is AI video generation. In this no-subtitles variant, the default is no on-screen text at all.
   - Keep platform tone natural: TikTok should feel like UGC seeding content, with emotional urgency, fast visual feedback, a product-rescue moment, and a believable validation ending; commercial ads can be more polished.

## When Coordinating With Video Skills

Only coordinate with a video skill/tool after the user explicitly asks to generate video. A direction choice such as `1`, `场景种草`, or `TVC` means "write the script in this direction"; it does not mean "start LibTV generation".

If the user asks to generate the video after the script, pass the confirmed script and reference-image notes to the video generation skill/tool. Preserve the selected script as the source of truth. Do not rewrite, expand, or optimize it into a new prompt during handoff. When image-to-video tools have trouble with text, use a no-text version and rely on voiceover.

Default audio route: when the user wants sound or voiceover, ask the video model/LibTV to generate one complete video with native audio/voiceover directly. Do not create separate TTS audio, do not create a silent video, and do not use a later audio-video compose workflow unless the user explicitly requests separate voiceover production.

When handing off any non-TVC script to a video generation skill/tool, use the product image as the reference image and directly generate the finished video. The first sentence must explicitly state the fixed generation target unless the user explicitly requests a different duration, ratio, or audio mode: `请基于这张产品参考图，直接生成一条15秒、9:16竖屏、带声音/口播的完整短视频。` Do not rely on the earlier script table to carry duration, ratio, audio settings, or reference-image use.

For every video handoff, add this explicit no-text constraint: `不要添加任何字幕、口播字幕、屏幕文字、标题卡、价格贴片、促销文字、漂浮标签或生成式文字。画面里只保留产品本身已有的包装文字/Logo，不额外生成新文字。`

For non-TVC handoff prompts, add this explicit constraint: `不要先生成分镜图、角色设计图或分段视频，也不要等待用户确认分镜。不要按镜头、时间段或脚本段落拆成多个视频片段，不要多段生成后合并。请一次性直接输出完整成片。`

When the product changes from prior work, require a clean video-tool project/canvas before uploading the new product reference image. For LibTV, this means calling `change_project.py` first, then `upload_file.py`, then `create_session.py`. When only platform, campaign context, or language changes, recommend a clean project/session. Add an explicit isolation line to the handoff prompt: `This is a new standalone product task. Do not inherit any previous product, campaign, 618, 双11, price, or activity context unless repeated in this prompt.`

For multiple scripts, do not merge all scripts into one generation request. Create a numbered batch manifest: each item must include concept title, duration, ratio, reference image, full voiceover, shot plan, text-overlay limits, and success criteria. For LibTV, each script must be submitted as a separate video task. Do not pack several scripts into one prompt.

For multiple `商业广告/TVC` scripts, use serial batch execution by default: submit one TVC, wait for its storyboard images and final video to complete, record the result, then submit the next TVC. Do not submit multiple storyboard-first TVC jobs into the same video-tool session at once.

For `商业广告/TVC` only, use a storyboard-first handoff by default: generate 5 key 9:16 storyboard images first, then use those storyboard images together as reference images for one complete video. After storyboard images are generated, continue to final video automatically unless the user explicitly asked to review/approve storyboards first. See `references/video-handoff.md`.

## References

- Use `references/direction-playbook.md` for direction-specific structures when research is unavailable or when you need a baseline.
- Use `references/output-template.md` for the default script output format.
- Use `references/research-guide.md` for safe research behavior and source handling.
- Use `references/video-handoff.md` when the user wants to generate one or many videos from the scripts.
