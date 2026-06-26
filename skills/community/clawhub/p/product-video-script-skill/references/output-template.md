# Output Template

Use this structure by default. Keep it concise.

## Product Diagnosis

- Category:
- Visible traits:
- Likely buyer/use case:
- Best script angle:
- Risks/uncertainties:
- Campaign context: if requested, name the campaign; otherwise write `无明确活动，按长期通用脚本处理`.

## Direction Options

Only include this section when the user has not chosen a direction.

1. 带货口播 - ...
2. 场景种草 - ...
3. 促销活动 - only if the user wants an event/deal angle
4. 测评对比 - ...
5. 海外 TikTok 风格 - ...
6. 直播间真人带货 - ...
7. 商业广告/TVC - ...

## Research Summary

Use this section when research was performed.

- Sources checked:
- Reusable patterns:
- What to copy structurally:
- What not to copy:

If research was not possible, write: `未联网版本：以下脚本基于通用平台内容规律与产品图分析生成。`

## Recommended Script

- Title:
- Duration:
- Ratio:
- Platform/style:
- Why it fits:

Write the script as a continuous sequence, not a timestamp table. Do not use rows such as `0-2s`, `2-5s`, or numbered clip segments.

- Opening hook:
- Visual flow:
- Voiceover:
- Subtitle / on-screen text policy: none. Do not add subtitles, captions, title cards, price stickers, floating labels, or generated text overlays.
- Closing CTA:

## Full Voiceover

Write the full spoken script in one paragraph.

## Video Handoff Notes

Write concise handoff notes for a later video generation step. These notes are not permission to generate video and are not a replacement prompt. When the user later asks to generate video, preserve the confirmed script as the source of truth and pass these notes as constraints.

Include:
- product reference notes
- for non-TVC directions, explicitly say to use the product image as the reference image and directly generate one complete 15s 9:16 video
- for non-TVC directions, explicitly forbid storyboard images, character design images, separate clips, timestamp-based generation, and storyboard confirmation
- explicitly say to generate sound/voiceover natively inside the video generation request; do not create separate TTS audio or compose audio and video later
- explicitly say no subtitles, no captions, no text overlays, no title cards, no price stickers, no floating labels, and no generated UI text
- camera style
- model/hand/action notes
- overall pacing only, without timestamp segments
- ratio and duration
- voiceover language
- no-text-overlay constraints

## Variants

Optionally provide 2-3 hook or CTA variants.

## Next Actions

Use short user-facing labels. Do not expose backend workflow details in option names.

Mandatory stop rule:
- After outputting a script, stop here and wait for the user's next selection.
- Do not call LibTV or any video generation tool from the same response that writes the script.
- A user selecting a direction means "write a script in this direction"; it is not permission to generate the video.
- Only start video generation after the user explicitly selects `直接生成视频`, `选其中一条去生成视频`, `把这几条全部交给 LibTV 批量生成`, or clearly asks to generate videos.

After a single script, use exactly:

1. 直接生成视频
2. 重写一版（可提要求）
3. 多给几个脚本/创意方向
4. 改成其他视频方向（口播/种草/促销/测评/TikTok/直播/TVC）

If the chosen direction is商业广告/TVC, still write `直接生成视频`; the storyboard-first workflow belongs in the internal video handoff, not the user-facing option text.

For every non-TVC direction, `直接生成视频` means: use the product image as the reference image, then directly generate one complete 15s 9:16 video. Do not expose or create a storyboard-first workflow.

After multiple scripts or creative directions, use exactly:

1. 选其中一条去生成视频
2. 把这几条全部交给 LibTV 批量生成
3. 继续重写更多版本
4. 先优化其中某一条脚本
