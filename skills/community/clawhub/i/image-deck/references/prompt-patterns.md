# Prompt Patterns

## Research Notes Template

Create `research-notes.md` before slide prompts when the user supplies only a topic and no source document.

```text
# Research Notes

Topic:
Audience/context:
Language:
Target slide count:
Text richness/content density:

## Sources
- <source title> - <link> - <why it matters>

## Usable Takeaways
1. <fact/claim/example>
2. <fact/claim/example>

## Deck Angle
<one paragraph explaining the narrative direction>

## Visual Prompt Material
- <visual metaphor, scene, object, diagram idea>
- <visual metaphor, scene, object, diagram idea>
```

## Visual Bible Template

```text
Deck format: 16:9 landscape presentation slide, full-bleed image, high-resolution, polished keynote/editorial quality.
Consistency anchor: this slide belongs to the same deck style as the approved master sample. Keep the selected PPT style, typography mood, layout quality, graphic language, and polish consistent. Do not treat consistency as copying the same literal background or hero scene.
Palette: <3-5 colors with roles>.
Background/scene: choose whatever background, scene, diagram, or visual metaphor best serves this slide while staying in the selected PPT style.
Typography mood: readable PPT-style hierarchy: display title or central claim when appropriate, supporting captions/bullets/callouts, highly readable, no tiny body copy.
Text richness/content density: <information-rich / balanced / concise>. Match normal content slides to this choice.
Role system:
- Cover: title-page composition, cover-suitable hero visual, one large main title, at most one subtitle, no other cover text unless the user explicitly asks for it.
- Divider/chapter: section statement and one symbolic visual, lighter text.
- Normal content: title or central claim plus visible text that matches the selected text richness mode. Information-rich mode uses more explanatory copy; balanced mode uses tighter useful callouts; concise mode uses fewer words and a stronger visual focus. Do not accidentally reduce a content page to an empty background unless the user asks for visual-only pages.
- Process/comparison: labeled steps, stages, axes, or comparison captions plus short explanations inside the generated image.
- Closing: summary statement or final takeaway, visually distinct but still in the same system.
Inner-page layout grid: <role-appropriate title/claim zone>, <text/callout zone>, <main visual zone>, <footer/page marker zone>, generous safe margins.
Graphic language: <photo/3D/vector/editorial collage/etc.>, consistent line weight, shape language, shadows, and texture.
Text rule: all visible text must be generated inside this image; do not leave blank title areas for later editing. Match text density to slide role and selected content-density mode. Cover slides have strict text rules: main title plus optional subtitle only, unless the user explicitly asks for additional cover text. Normal content slides should not feel underwritten for the selected mode.
Small-text rule: allow naturally generated supporting detail text on content slides when it improves richness, realism, or editorial/report feel in information-rich or balanced mode. In concise mode, keep supporting text selective and intentional. Do not apply this small-text rule to covers unless the user explicitly asks for it.
Quality target: main message readable, information density appropriate for the selected mode, supporting detail text natural, overall page polished and coherent. Keep style consistent across the deck without forcing the same literal background on every slide.
```

## Prompt Group Template

Show prompt groups directly in the conversation before calling `image_gen`. Use at most 8 slides per group. Do not hide this behind file attachments.

```text
请使用 Codex 内置 image_gen 能力生成这一组 <N> 张独立的 16:9 横版 PPT 完整页面图片。

重要执行规则：
这不是一张包含 <N> 页的总览图，也不是拼图、缩略图墙或多页排版预览。
请把下面的每一页理解为独立的图片生成任务。

执行方式：
- 逐页生成。
- 每次只生成一张图片。
- 每张图片只包含当前指定页的一页完整 PPT。
- 当前页生成完成后，再继续生成下一页。
- 不要把多页合并在同一张画布里。
- 不要生成“多页总览图”。
- 不要生成“幻灯片缩略图排列”。
- 不要在一张图中出现多个页面边框。
- 每张图片都是可直接放入 PPT 的完整单页。

统一视觉系统（本组必须逐条遵守；下一组也必须完全沿用）：
<PASTE THE LOCKED VISUAL BIBLE VERBATIM>

跨组一致性要求：
- 第 1 组、第 2 组及后续所有组都保持同一种 PPT 风格、字体气质、版式质量、图形语言和整体完成度。
- 一致性是“风格一致”，不是“同一张背景反复使用”。不要为了保持一致而复制同一个背景或同一个主视觉。
- 每页可以根据内容自由选择背景、场景、图表、示意图或视觉隐喻，只要不偏离用户选定的 PPT 风格。
- 封面必须像封面，不要像内页：默认只能有主标题，最多再加一个副标题。除非用户明确要求，否则封面不要加入其他小字、说明、标签或注释。封面主视觉必须适合封面，不能是内页那种内容解释图。
- 内页必须像真实 PPT 内容页：标题/中心论点、说明文字、图表/流程/示意/场景等视觉元素要一起生成在图片里。文字多少按用户选择的内容密度执行：文字丰富、平衡或文字简洁。
- 内容页允许自然的小字和补充说明文字：在文字丰富或平衡模式下，如果它们能增强画面丰富度、真实感或报告感，就不要刻意去掉。文字简洁模式下，小字要更克制，只保留对页面有帮助的短说明。这个规则不适用于封面，除非用户明确要求。

第 <N> 页：
Slide role: <cover / divider / normal content / process / comparison / closing>
Allowed visible text only:
- <exact generated text>
Text richness/content density: <information-rich / balanced / concise>
Text detail target: <cover: main title plus optional subtitle only; normal content: match the selected text richness mode; process/comparison: labels plus short explanations when useful>
Core message: <one sentence>
Main visual: <visual scene or diagram>
Composition: <role-specific layout; for cover, use only the main title plus optional subtitle unless the user explicitly asked for more cover text, and explicitly avoid inner-page layout. For content pages, allow naturally generated supporting detail text when it makes the slide richer and more complete. Use visuals that fit this slide rather than copying another slide's background>
Quality target: one complete generated PPT page, readable, matched to the selected text richness mode, cohesive with the same visual system.

第 <N+1> 页：
...
```

For decks longer than 8 slides, repeat this template for the next group. Keep the full visual bible unchanged in every group; do not shorten it to "same style as above" because later groups may be used independently.

## Per-Slide Prompt Template

```text
Use case: productivity-visual
Asset type: complete 16:9 slide image generated by Codex built-in image_gen for a presentation deck.

<PASTE THE LOCKED VISUAL BIBLE VERBATIM>

Slide number: <N>
Slide role: <cover / chapter / proof / comparison / process / summary>
Allowed visible text only:
- <list exact slide text here: title/claim, captions, bullets, callouts, labels, section tag, or page marker as appropriate to this slide role>
Text richness/content density: <information-rich / balanced / concise>
Text detail target: <for normal content slides, match the selected text richness mode: information-rich means more explanatory copy, balanced means tighter useful callouts, concise means fewer words and stronger visual focus; for cover, only main title plus optional subtitle>

Core message: <one sentence>.
Main visual: <describe the concrete scene, diagram, object, or metaphor that best serves this slide>.
Composition: <where generated text belongs, where the main visual goes, how labels/callouts attach to the visual, repeated generated footer/page marker if needed. For cover slides, use only the main title plus optional subtitle unless the user explicitly asked for more cover text. For content slides, allow naturally generated supporting detail text when it makes the slide richer and more complete. Keep style consistent without copying another slide's background>.
Quality target: premium, cohesive with the master sample, readable at presentation size and thumbnail size.
Critical constraint: generate the whole slide as one finished PPT page with the visible text included in the image. Match the selected text richness mode. Do not create blank placeholders for later overlays. In concise mode, fewer words are acceptable, but the page should still look intentional and finished.
```

## Prompt Review Summary Template

Show this before calling `image_gen`:

```text
Single review package:
- Slide-by-slide design document: shown above or included here
- Visual bible: prompts/visual-bible.md
- Master sample: prompts/00-master-sample.md
- Inline prompt groups:
  - Group 1: slides 1-8
  - Group 2: slides 9-<N>
- Backup prompt files: prompts/01-slide.md ... prompts/<N>-slide.md

Please review:
1. Overall style and palette
2. Slide text plan and allowed visible text
3. Main visual for each slide
4. Whether normal content slides match the selected text richness/content density, from information-rich to concise
5. Whether the cover has only a main title plus optional subtitle, and looks like a cover rather than an inner page
6. Whether the pages keep the selected PPT style without copying the same literal background
7. Whether later groups still match the first group's style
8. Any slides to add, remove, reorder, or rewrite

This is the only confirmation before image generation. I will call image_gen after you approve this combined package, unless you tell me to skip prompt review.
```

## Prompt Revision Patterns

Before prompt groups are shown to the user, complete the self-check internally. Do not post a draft prompt package and then withdraw it because of self-correction.

After prompt groups are visible, keep the original package visible as the review base. If the user edits prompts or the assistant catches a small issue before image generation, append a revision note and show only the affected revised slide prompts or affected group. Preserve the visual bible unless the user explicitly changes global style. Do not ask for a second confirmation after the revision; the same single combined review gate still applies.

Revision note template:

```text
修订说明：
- 原因：<为什么需要改>
- 受影响页面：第 <N> 页 / 第 <A>-<B> 页
- 改动范围：只替换下面这些提示词；未列出的页面继续沿用上面的提示词包和同一套视觉系统。
```

For one-slide prompt edits:

```text
已根据你的修改更新第 <N> 页提示词。下面只重贴受影响的提示词，其他页面沿用同一套视觉系统不变。

第 <N> 页：
Slide role: <role>
Allowed visible text only:
- <revised exact generated text>
Core message: <revised message>
Main visual: <revised visual>
Composition: <revised layout, still matching the locked visual bible>
Consistency rule: keep the same palette, lighting, margin, typography mood, page marker, and graphic language as the approved visual bible and other prompt groups.
```

For whole-group edits:

```text
已更新第 <A>-<B> 页这一组提示词。统一视觉系统保持不变；只修改每页内容、文案或主视觉。
如果没有其他修改，我会把这一组作为原提示词包的替换部分，不再单独要求确认这一组。
```

If the user changes global style:

```text
这是全局风格修改，会影响所有页面。需要先更新 visual bible，再重新显示全部 prompt groups。即使这样，也只做一次最终确认，再生成新的 master sample。
```

## Regeneration Patch Patterns

Use a short patch instruction instead of rewriting the whole art direction:

```text
Regenerate slide <N> with the same locked visual bible and same content. Fix only this issue: <issue>.
Keep the title area cleaner, reduce decorative clutter, and preserve the same palette and page marker style as the approved master sample.
```

For text failures:

```text
Regenerate slide <N>. Use the exact main visible text listed below and render it inside the generated image. Make the main text readable as designed PPT text, with hierarchy appropriate to the slide role. Preserve natural supporting detail text when it helps the slide feel rich; keep the result polished and coherent.
```

For cover failures:

```text
Regenerate the cover slide with the same locked visual bible. The cover may contain only the main title and one optional subtitle. Remove every other visible word, label, bullet, caption, page number, date, author line, chart label, logo-like mark, and section tag. Make the main visual feel like a cover hero image, not an inner-page explanatory diagram, chart, dashboard, matrix, process flow, or content-card layout.
```

For underfilled slides in information-rich or balanced mode:

```text
Regenerate slide <N>. The previous version looked underfilled and did not contain enough information for its role. Keep the selected PPT style and main image concept, but make it a complete information-rich 图文并茂 PPT page with concrete, topic-specific in-image text. Do not use only icon labels, item names, or two-word tags.
```

For concise-mode slides that became too dense:

```text
Regenerate slide <N>. Keep the same locked visual bible and main image concept, but switch this slide to the approved concise text mode: fewer words, stronger visual focus, short intentional claims/captions/labels, and no dense report-like text blocks. Keep the page finished and readable as a PPT slide.
```

For style drift:

```text
Regenerate slide <N>. Match the approved deck style more closely: same PPT style, typography mood, layout quality, color discipline, graphic language, and overall polish. Choose the background or visual that best serves this slide; do not copy another slide's background unless requested.
```

For accidental monotony or repeated backgrounds:

```text
Regenerate slide <N> with the same content and selected PPT style. The previous version copied the same literal background or hero image too much. Keep the overall style, typography mood, layout quality, and graphic language, but choose a different visual that better serves this slide.
```

For post-delivery user edits:

```text
Update slide <N> after delivery. Keep the locked visual bible and approved master sample style. Regenerate the entire slide image through Codex built-in image_gen; do not add PPT text boxes or local overlays.
User-requested change: <change>.
Preserve: aspect ratio, palette, lighting, margins, typography mood, page marker style, graphic language, and role-specific layout.
```

For adding slides after delivery:

```text
Add slide <N> using the existing deck's locked visual bible and prompt-group format.
Show the new slide prompt inline for approval before generation.
After approval, generate it as one complete PPT page image through Codex built-in image_gen and insert it into the deck.
```

## Contact-Sheet Review Rubric

Score each slide 1-5:

- consistency with master sample
- title readability
- content/message fit
- visual polish
- thumbnail clarity

Regenerate any slide with a 1-2 in consistency or readability. Regenerate any slide whose main message is unreadable, whose aspect ratio is wrong, or whose artifacts make it look broken.
