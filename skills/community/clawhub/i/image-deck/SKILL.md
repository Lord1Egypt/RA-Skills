---
name: image-deck
description: "image-deck creates slide decks, slides, single slides, PPT, PowerPoint-style presentations, carousel pages, and full-image decks with GPT Image 2 through Codex built-in image_gen. Trigger by default when the user asks to make slides, create slides, generate slides, make a slide, create a slide deck, make a deck, make a PPT, create a PowerPoint, build a presentation, or create a carousel; also trigger for Chinese requests such as 做PPT, 制作PPT, 帮我做PPT, 生成PPT, 做deck, 做slides, or 做演示文稿. Each slide/page is one complete generated raster image, including visible text inside the image itself. Before generation, ask for page count, language, style, and text richness/content density; give recommended choices for page count, style, and text richness, but let the user choose language. Default to information-rich 图文并茂 PPT pages unless the user chooses concise or image-led pages."
---

# image-deck

## English

`image-deck` is used to create PPT, PowerPoint-style presentations, slide decks, and carousel decks where every page is a complete generated image. It uses Codex built-in `image_gen` (GPT Image 2) to generate slides one by one, with each slide's title, labels, and short copy generated inside the same image.

This skill requires Codex built-in `image_gen` (GPT Image 2).

Search keywords: `slide`, `slides`, `slide deck`, `presentation`, `PowerPoint`, `PPT`, `PPTX`, `deck`, `carousel`, `GPT Image 2`, `image generation`, `OpenClaw`, `Codex`.

## Trigger

Use this skill by default when the user asks to make a PPT, PowerPoint-style presentation, slide deck, slides, single slide, deck, or carousel, including requests like "make a PPT", "create a PowerPoint", "build a presentation", "make slides", "create slides", "generate slides", "make a slide", "create a slide deck", "make a deck", "做PPT", "制作PPT", "帮我做PPT", "生成PPT", or "做演示文稿".

If the user explicitly asks for an ordinary editable PPT, a text-overlay workflow, or precise editable tables/charts, use a normal presentation workflow instead.

## Best For

- Every PPT page should be one complete generated image
- Images and text should be generated together in the same image
- Page count, language, style, and text richness/content density should be confirmed before planning; recommend page count, style, and text richness, but let the user choose language
- A slide-by-slide design document should be shown before prompt generation
- Prompts should be shown before generation so the user can review or edit them
- Normal content slides should follow the selected text richness mode: information-rich, balanced, or concise
- After the deck is created, the user can revise one slide or several slides
- After the deck is created, the user can add new generated image slides

## Preview

![image-deck preview](https://raw.githubusercontent.com/tseng71/skills/main/skills/image-deck/assets/preview.jpg)

## Install

ClawHub page:

```text
https://clawhub.ai/tseng71/image-deck
```

GitHub repository / Codex install URL:

```text
https://github.com/tseng71/skills
```

Codex:

```bash
mkdir -p ~/.codex/skills
cp -R skills/image-deck ~/.codex/skills/image-deck
```

Restart Codex after installing.

## 中文说明

这是 `tseng71` 的个人 AI Agent Skills 仓库中的一个 skill。

`image-deck` 用于制作“每一页都是完整生成图片”的 PPT、PowerPoint 风格演示、slide deck 和 carousel deck。它会通过 Codex 内置的 `image_gen`（GPT Image 2）逐页生成，每页的标题、标签和短文案都在同一张生成图里完成。

使用这个 skill 需要可用的 Codex 内置 `image_gen`（GPT Image 2）。

搜索关键词：`slide`、`slides`、`slide deck`、`presentation`、`PowerPoint`、`PPT`、`PPTX`、`deck`、`carousel`、`GPT Image 2`、`image generation`、`OpenClaw`、`Codex`。

## 触发方式

用户说“做 PPT”“制作 PPT”“帮我做一个 PPT”“生成 PPT”“做 slides”“做 deck”“做演示文稿”等，都应默认触发这个 skill。

如果用户明确要求普通可编辑 PPT、后期叠文字流程，或者需要大量精确可编辑表格/图表，再改用普通演示文稿流程。

## 适合使用

- 每一页 PPT 都要是一张完整生成图
- 图片和文字要一起生成在同一张图里
- 制作前先确认页数、语言、风格和内容密度；页数、风格和内容密度给出推荐，语言由用户自己选择
- 生成提示词前先展示 PPT 逐页设计文档
- 生成前先输出提示词，让用户确认或修改
- 普通内容页按用户选择的内容密度生成：文字丰富、平衡或文字简洁
- 制作完成后，用户可以指定修改某一页或几页
- 制作完成后，用户可以继续追加新的图片页

## 安装

ClawHub 页面：

```text
https://clawhub.ai/tseng71/image-deck
```

GitHub 仓库 / Codex 安装地址：

```text
https://github.com/tseng71/skills
```

Codex:

```bash
mkdir -p ~/.codex/skills
cp -R skills/image-deck ~/.codex/skills/image-deck
```

安装后重启 Codex。

## Agent Execution Notes

Use this skill to produce decks where each slide is a complete finished PPT page generated through Codex built-in `image_gen` (GPT Image 2), including the slide's visible text and visual elements inside the same image. Then assemble those images into PPTX/PDF if requested. The core job is consistency control: ask for topic, style, page count, language, and text richness/content density; research the topic when no source document is supplied; build a visual bible; show the slide-by-slide design document and complete prompt groups inline in the chat for one combined review; create one approved master sample through Codex `image_gen` (GPT Image 2); generate each slide through Codex `image_gen` (GPT Image 2) using the same locked system; inspect every result; and regenerate only the slides that drift, fall below the selected text richness mode, or that the user asks to revise.

Use the regular `imagegen` skill as the execution path for Codex built-in `image_gen` (GPT Image 2). This skill supplies the art-direction workflow around that image generation capability.

Do not call the Presentations skill/plugin just because the user asks for a PPT. This skill is not an editable-presentation workflow. During intake, attachment reading, source extraction, outlining, prompt planning, image generation, QA, and prompt revision, do not use Presentations. If a PPTX is needed at the end, prefer a minimal image-to-PPTX assembly path that places the already-generated slide images full-bleed, with no extra visible content.

## Trigger Policy

Prefer this skill for broad deck-making requests, even when the user does not say "image-deck" explicitly:

- English: "make a PPT", "create a PowerPoint", "build a presentation", "make slides", "create slides", "generate slides", "make a slide", "create a slide deck", "make a deck", "make a carousel"
- Chinese: "做PPT", "制作PPT", "帮我做PPT", "做一个ppt", "生成PPT", "做deck", "做slides", "做演示文稿"

Only route away from this skill when the user explicitly asks for a normal editable PPT, editable text boxes, editable charts/tables, or a workflow where images are generated first and text is overlaid later.

## Required Run Order

Follow this order for every new deck request. Do not skip a step because the user said "make a PPT", attached a file, or mentioned this skill by name.

1. **Ask required setup questions** before planning: page count, language, style, text richness/content density, and topic if no source is present.
2. **Read source material or research the topic** before writing the deck plan.
3. **Show a PPT slide-by-slide design document directly in the chat** as the planning preview.
4. **Self-check the complete prompt package internally before showing it**, then show prompt groups directly in the chat, up to 8 slides per group.
5. **Ask for one combined approval only after both the design document and prompt groups are shown.** Do not ask the user to confirm the design document separately and then confirm prompts again.
6. **Only after that single approval**, generate the master sample and then the slide images through Codex `image_gen` (GPT Image 2).

Once prompt groups have been shown to the user, treat them as the visible review package. Do not withdraw, replace, or re-output the entire package because of later self-corrections. If a correction is needed after display, append a short revision note and show only the affected slide prompts or affected group.

If an OpenClaw or other runtime cannot show a structured UI question, ask the questions as plain text in one message and wait for the user's answer. Do not infer missing page count, language, style, or text richness silently, except that page count may be offered as "about 15 slides" for the user to accept or change.

## Non-Negotiable Generation Boundary

When this skill is active, a slide is valid only if the complete slide image came from one of these sources:

- a Codex `image_gen` (GPT Image 2) call made for that specific slide
- a Codex `image_gen` (GPT Image 2) regeneration call made for that specific slide

If Codex built-in `image_gen` (GPT Image 2) is unavailable in the active environment, stop and tell the user that this skill needs Codex `image_gen` (GPT Image 2).

Do not satisfy this skill by rendering slides with HTML/CSS, Python drawing, matplotlib, PowerPoint shapes, screenshots, PDF page renders, stock photos, local templates, or presentation JSX. Those tools may be used only after generation to assemble, crop, inspect, contact-sheet, or export the already-generated slide images.

Do not treat "background generated by an image model plus locally overlaid slide layout" as valid output. There is no hybrid mode in this skill. If the slide needs a title, caption, number, label, chart title, or short bullet, that visible text must be requested in the Codex `image_gen` (GPT Image 2) prompt and must appear inside the generated image itself.

When assembling PPTX/PDF, each slide must contain the generated image as the only visible slide content. Do not add separate text boxes, captions, page numbers, icons, shapes, charts, or labels after generation. If text is missing, wrong, or unreadable, regenerate the slide image instead of overlaying corrected text locally.

Do not invoke Presentations to design, analyze, convert, or recreate slide content for this skill. It is acceptable only as a last-mile packaging/inspection fallback after all images already exist, and only if the simpler image-to-PPTX path is unavailable or the user explicitly asks for that route.

Keep an `image-generation-log.md` with one row per slide:

- slide number
- prompt file or prompt text reference
- Codex `image_gen` (GPT Image 2) call/output path
- QA status
- regeneration notes, if any

## Done Criteria

Before reporting completion:

- Every requested slide image exists at the target aspect ratio.
- Every slide has a generation record showing it came from Codex `image_gen` (GPT Image 2).
- Page count, language, style, and text richness/content density were explicitly asked and answered, or the user had already provided them in the request. Page count, style, and text richness included recommendations; language was left for the user to choose.
- The PPT slide-by-slide design document was displayed directly in the chat before image generation.
- The user had one combined review point for the slide-by-slide design document, visual bible, and complete per-slide prompt groups before image generation, unless they explicitly asked to skip prompt review.
- Prompt groups were displayed directly in the chat, not only attached as files or offered as downloads. Each group contains at most 8 slide prompts and explicitly says the slides are independent image-generation tasks, not a collage or thumbnail wall.
- Every slide's visible text and visual elements match its role as a PPT page and the selected text richness/content density. In information-rich mode, normal content slides should be 图文并茂 and carry a substantial part of the slide's meaning in the image. In balanced mode, normal content slides should still include useful explanatory copy, but with fewer and tighter text blocks. In concise mode, normal content slides may use fewer words and stronger visuals, but should not become empty backgrounds unless the user explicitly asks for visual-only pages. Cover, divider, closing, and visual emphasis slides may use lighter text when appropriate.
- The cover has strict text rules: it contains only the main title and, if needed, one subtitle, unless the user explicitly asks for additional cover text. Do not apply the normal content-slide small-text policy to the cover.
- Unless the user chooses concise, low-text, or image-led pages, normal content slides should not contain only a title plus a few short labels, icons, or item names. They should contain distinct information units where appropriate: a central claim, concrete explanations, evidence, examples, steps, comparisons, cautions, or decisions. The exact form is determined by the topic, audience, slide role, and selected text richness mode; do not hard-code a fixed count.
- For normal content slides, prompts must draft the actual visible copy, not just say "add details" or "include useful text." In information-rich mode, use complete short phrases or compact sentences with concrete information from the source, research, or deck argument. In balanced mode, use fewer but still useful callouts. In concise mode, use short claims, captions, or labels that are intentional and readable rather than filler.
- If a normal content slide's design document or prompt falls below the selected text richness mode, revise it before generation. In concise mode, fewer words are acceptable; do not enrich it into a dense report page unless the user changes the mode or asks for more detail.
- Every slide's visible title, explanatory text, labels, bullets/callouts, and short copy, when used, are inside the generated image itself, not overlaid later.
- The deck has one visual style: the selected PPT style, typography mood, layout quality, graphic language, and overall polish feel related.
- Do not interpret style consistency as copying the same literal background or hero image across the deck.
- Each slide passes readable-title and low-artifact checks at full size and contact-sheet size.
- Do not reject a good slide just because it includes tasteful small supporting text or visual-detail text. Regenerate only when the main message becomes unreadable, the page looks broken, or the visual quality clearly fails.
- If the final deck is assembled, verify that each slide is one full-bleed generated image with no extra visible text/shape objects.

## Workflow

### 1. Intake: ask before generating

Ask exactly these required setup questions before writing final prompts unless the user already supplied the answers. Do not ask them as bare questions. Include your recommended answer for page count, style, and text richness/content density, but do not recommend a language; ask the user to choose the language.

- **Topic/source:** Ask what the deck is about when no attachment, document, notes, outline, link, or other source material is present. If source material exists, confirm whether to use it as the primary source.
- **Style:** Offer a short menu, allow a custom answer, and recommend 2-3 styles based on the topic, source material, audience, and desired tone. Mark the best fit as recommended.
- **Page count:** Recommend a page count based on scope before asking. Default recommendation: about 15 slides for a standard deck; 8-10 for a short overview; 18-20 for a complex research/report deck.
- **Language:** Ask the user to choose Chinese, English, or bilingual. Do not recommend or default the language unless the user already specified it. Do not default to mostly visual unless the user explicitly asks for visual-only pages.
- **Text richness / content density:** Ask how much visible text the PPT pages should contain. Recommend **Information-rich / 文字丰富** by default. Offer:
  - **Information-rich / 文字丰富:** more explanatory in-image copy, suitable for report, analysis, training, policy, strategy, and knowledge decks.
  - **Balanced / 平衡:** enough useful text to explain the slide, but with tighter copy and more visual breathing room; use when the user wants a less dense but still substantive deck.
  - **Concise / 文字简洁:** fewer words, stronger visual focus, short claims/captions/labels; suitable for keynote, teaser, social carousel, or image-led storytelling.

These questions are mandatory in OpenClaw too. If there is no structured question tool, ask in plain text as a compact checklist:

```text
Before I design the deck, please confirm:
1. Page count: I recommend <recommended count> because <short reason>. Use this, or another number?
2. Language: please choose Chinese, English, or bilingual.
3. Style: I recommend <best style> first, with <second style> and <third style> as alternatives. Choose one from the menu below, or describe a custom style.
4. Text richness/content density: I recommend information-rich / 文字丰富 by default, so the deck has enough useful in-image explanation. Choose information-rich, balanced, concise, or describe another preference.
5. Topic/source: if no file or notes were attached, what is the topic?
```

Do not proceed to deck design, prompt writing, or image generation until the required answers are known. If the user replies with only partial answers, ask only for the missing items.

Ask for output format only when the user asks for a deliverable instead of prompt planning.

Offer this style menu by default. Keep it visible enough for the user to choose, but allow a custom reference:

1. **premium editorial:** magazine-like, strong imagery, restrained text, polished presentation rhythm
2. **minimal executive:** clean, spacious, high signal, boardroom-ready
3. **futuristic tech:** luminous interfaces, systems diagrams, dark or high-contrast depth
4. **bold keynote:** high contrast, large type, dramatic visual metaphors
5. **consulting report:** structured business presentation, clear hierarchy, charts/diagrams as supporting visuals
6. **corporate annual report:** formal, stable, institutional, polished report-like pages
7. **flat vector illustration:** clean vector scenes, icons, simple shapes, bright but controlled palette
8. **soft editorial illustration:** elegant illustrated scenes, gentle texture, refined magazine feel
9. **watercolor / ink wash:** soft watercolor texture, hand-painted atmosphere, warmer human tone
10. **hand-drawn sketch note:** marker/sketch style, educational, friendly, annotation-heavy
11. **3D isometric / clay render:** dimensional objects, isometric scenes, tactile product-like visuals
12. **cinematic photo-real:** dramatic lighting, realistic scenes, visual storytelling, low-to-medium text
13. **collage / mixed media:** cutout photos, paper texture, editorial composition, energetic layout
14. **product launch:** polished launch-deck style, product hero visuals, feature sections, crisp claims
15. **Chinese modern / 国风:** restrained Chinese visual motifs, ink texture or modern cultural design
16. **luxury dark / premium brand:** dark background, metallic accents, sparse high-end composition
17. **custom:** user's own reference image, brand guide, or description

If the user asks for 15 pages and does not specify a style, propose two fitting styles from the menu based on the topic instead of asking a long follow-up. If the topic is known but the user gave no page count, include your page-count recommendation in the same question.

### 2. Source and research pass

Before writing the deck spine or image prompts, establish the content basis:

- **With source material:** read and analyze the source. Extract the title/topic, structure, key claims, important facts, examples, figures, evidence, decisions, caveats, and visual opportunities needed for the deck spine. Use the source as the main factual basis. Do not invent missing facts to fill pages.
- **Without source material:** perform topic research before creating the slide plan. Search for current, credible sources; collect the core facts, framing, examples, dates, vocabulary, tensions, implications, and visual material needed for the deck; and save `research-notes.md` with source links and usable takeaways.

Attachment reading rules:

- Do not call Presentations for attachment reading, even if the attachment is PPT/PPTX.
- For PDF, DOCX, PPTX, Markdown, text, or spreadsheet sources, use reliable extraction methods that preserve the information needed for deck planning: plain text extraction, document XML/text extraction, page titles, headings, notes, outline, tables, figures, and important annotations where relevant.
- For long files, create `source-map.md` with sections/pages and usable takeaways, then build the slide spine from that map and the requested page count.
- If the source is too long or extraction is slow, prioritize the sections most relevant to the user's goal and continue with a clear deck-oriented analysis.
- If the user provided an existing PPT/PPTX as source, treat it as content reference only. Do not use its editable layout as the output workflow; the new output still uses full-slide images generated by Codex `image_gen` (GPT Image 2).

For time-sensitive, technical, legal, medical, financial, company, product, market, or news topics, browse current sources before committing to slide claims. Prefer official or primary sources when available.

Keep research deck-oriented:

- topic definition and audience-relevant framing
- key facts, claims, evidence, examples, and caveats needed for the deck
- useful examples, timelines, people, products, market context, or concepts
- visual metaphors or scenes that can become image prompts
- source links for facts that matter

Only after this pass, create the slide list and visual bible.

### 3. Use full PPT page mode only

All visible content must be generated inside each slide image. This includes the title, subtitle, bullet-style callouts, labels, page number, section tag, captions, and any short copy.

Default to 图文并茂的 PPT 页面, not decorative backgrounds. Match text density to the selected content-density mode and slide role:

- **Cover:** must use a cover-style hero visual and only a main title, with at most one subtitle, unless the user explicitly asks for additional cover text. Do not add small supporting text to covers by default.
- **Divider/closing:** may use a strong visual with a title, theme line, or short statement.
- **Normal content slide in information-rich mode:** should contain enough concrete in-image explanatory copy to feel like a useful finished PPT page, not only labels, icon names, or decorative slogans.
- **Normal content slide in balanced mode:** should contain a clear title/claim plus a smaller number of useful callouts, captions, or short explanations, leaving more visual space than information-rich mode.
- **Normal content slide in concise mode:** should use fewer words and a stronger visual focus, with short claims, captions, or labels. Do not force dense copy in this mode, but avoid accidental empty-background slides unless the user asked for visual-only pages.
- **Process/timeline/comparison slide:** should include labeled steps, stages, axes, or comparison captions plus short explanations inside the image.
- **Visual emphasis slide:** may be lighter on text, but only when the deck spine intentionally marks it as visual emphasis.

Keep text concise enough for Codex `image_gen` (GPT Image 2) to render. Prefer readable, useful phrases over long paragraphs. In information-rich and balanced modes, a normal content slide should carry meaningful information in the image itself: the main point plus concrete explanation, evidence, examples, steps, comparisons, cautions, or decision logic as appropriate to the slide. If a content slide falls below the selected content-density mode, regenerate with clearer PPT-page text instructions.

When planning text density, honor the selected mode. If the user has not chosen a mode yet, ask before planning. If the user chooses concise, keep the page intentionally concise instead of silently turning it into an information-rich report page.

If exact long copy, dense tables, detailed charts, or perfect typography are required, explain that this skill is not the right fit and suggest a normal editable PPT workflow instead. Do not switch to local text overlays inside this skill.

### 4. Build and show the PPT slide-by-slide design document

Create a PPT slide-by-slide design document before generating prompts. Display it directly in the chat, not only as a file or attachment. The design document is the user's planning preview and must be shown before prompt groups.

For each slide, include:

- slide number
- slide role, such as cover, chapter, proof, comparison, process, summary
- working slide title or cover title
- page message / communication goal
- visible text plan appropriate to the slide role
- title, central claim, bullets/callouts, labels, captions, or annotations as needed
- content detail plan: what information units will appear, and what each unit adds beyond a label
- visual object, such as scene, diagram, chart metaphor, portrait, product view, map, or timeline
- information density: cover-light, divider-light, concise, balanced, or high, based on slide role and the selected content-density mode

Use this inline format:

```text
PPT Slide-by-Slide Design Document

Slide 1 - Cover
Role:
Visible text:
Visual design:
Notes:

Slide 2 - ...
Role:
Visible text:
Visual design:
Notes:
```

For normal content slides, the "Visible text" field must draft concrete in-image copy. In information-rich mode, it should be substantial and specific to the topic. In balanced mode, it should be tighter but still useful. In concise mode, it may be shorter and more visual, but the short text should still feel intentional and useful rather than generic placeholders.

Do not ask the user to approve this design document as a separate confirmation gate. Show it as the planning preview, then continue to the visual bible and prompt groups. If the user interrupts with changes to page count, language, slide order, text richness, or style at this stage, update the design document and show the revised affected slides inline.

The cover must be planned as a cover, not as a normal inner content page. It should have a title-page composition: cover-suitable hero visual, large main title, and at most one subtitle. Do not plan any other cover text unless the user explicitly asks for it. Chapter/divider pages may use a different rhythm from content pages, while still sharing the same visual system.

When writing prompts, choose whatever background, scene, diagram, or visual metaphor best serves each slide. Keep the selected PPT style consistent, but do not force matching backgrounds or repeated hero scenes.

For image-only decks, avoid dense tables, long paragraphs, exact financial disclosures, and tiny body copy that must be read precisely. Convert complex content into PPT-friendly generated slide text: concise claims, bullets, callouts, captions, labels, and annotations. For content slides, do not over-constrain the model to remove all small text; naturally generated supporting detail text is often useful for making a slide feel rich and complete.

For any deck type, choose the type and amount of detail that best serves the slide. Do not hard-code a fixed text count or fixed detail categories unless the user asks for them.

### 5. Lock the visual bible

Write a reusable visual bible and keep it fixed across all slide prompts. Include:

- aspect ratio and safe margins
- palette with 3-5 named colors
- optional palette and lighting preferences if they are part of the selected style
- typography mood for generated in-image text, not font names unless a known font is required and available
- role system for cover, divider, normal content, comparison/process, and closing slides
- selected text richness/content density and how it changes normal content slides
- grid, title zone, text/callout zone, main visual zone, footer/page marker zone for inner pages
- illustration/photo/render style
- shape language, line weight, texture, depth, and shadow rules
- small-text policy: allow purposeful supporting detail text on content slides when it improves richness and realism; do not apply this to covers unless the user explicitly requests it
- quality target: main message readable, supporting detail text natural, overall page polished and coherent

Read `references/prompt-patterns.md` when writing the visual bible or per-slide prompt template.

### 6. Create prompt files and prompt groups

Each prompt must contain:

1. the fixed visual bible
2. the slide-specific role and message
3. exact allowed visible text to generate inside the image, appropriate to the slide role
4. content detail target for normal content slides, chosen by topic, audience, slide role, and selected text richness/content density
5. exact visible explanatory copy for normal content slides, written as complete short phrases or compact sentences
6. composition instructions
7. negative constraints

Change only the slide-specific block between slides. Keep the rest verbatim unless deliberately iterating the global style.

Create prompt groups for review:

- Group prompts into batches of at most 8 slides, such as slides 1-8 and 9-15.
- Display every prompt group directly in the chat inside fenced code blocks. Do not replace this with attachments, downloads, or "open these files" cards.
- Each group must explicitly state that it contains independent image-generation tasks, not one collage, 4x2 grid, overview image, or thumbnail wall.
- Every group must repeat the locked visual bible or a complete fixed visual-system block, so style remains consistent across groups.
- Every group must state that style consistency does not mean repeating the same literal background or hero image.
- Every group must include role-specific instructions so the cover has only a main title plus optional subtitle and does not look like an inner page. Divider/closing pages should not accidentally become dense content pages.
- Every group must include allowed visible text that matches the selected content-density mode. Information-rich mode should include more concrete explanatory copy; balanced mode should include tighter but useful callouts; concise mode should use fewer words and stronger visuals without drifting into accidental empty-background pages.
- Do not let normal content slide prompts use vague placeholders such as "add detailed text" or "include key points." Write the actual visible text to generate.
- Before showing a prompt group, check every normal content slide against the selected content-density mode. If it is below that mode, revise the prompt before the final combined approval request. Add concrete visible copy, not abstract instructions.
- Finish this self-check before posting the prompt groups. Do not stream or attach a draft prompt package, then retract it and output a new full package because of self-correction.
- The saved prompt files are only a backup/source record. The user-facing review artifact is the inline prompt group text in the conversation.

Also save prompts in a task workspace, usually:

```text
prompts/
├── visual-bible.md
├── 00-master-sample.md
├── 01-slide.md
├── 02-slide.md
└── ...
```

Read `references/prompt-patterns.md` for the per-slide prompt template and regeneration patch patterns.

### 7. Single combined review gate

Before any Codex `image_gen` (GPT Image 2) call, show the user:

- the PPT slide-by-slide design document, or a concise reference to the version shown immediately above
- the locked visual bible
- complete prompt groups in the chat, each covering up to 8 slides and including exact allowed visible text for each slide
- the chosen master-sample slide prompt inside the relevant group or repeated separately if needed

Ask the user once to approve generation or request edits. This is the only confirmation gate after intake. Do not first ask for design-document approval and then ask again for prompt approval. Accept edits at any level:

- global style or palette changes
- text richness/content density changes
- title/text changes for one or more slides
- visual scene changes
- slide count changes
- reordering, removing, or adding slides
- changing one whole prompt group while preserving the locked visual bible
- replacing the cover concept without adding extra cover text or turning it into an inner page
- enriching or simplifying slide text when the design document or prompt does not match the selected content-density mode

Do not call Codex `image_gen` (GPT Image 2) until the combined review package is approved, unless the user explicitly says to proceed without review.

If the user says the prompts are hidden in downloadable files or attachments, correct the workflow by pasting the prompt groups inline in the next response.

When the user modifies prompts after the prompt groups are shown, update the affected prompt group and show the revised group inline again. Keep the locked visual bible unchanged unless the user explicitly changes the global style. If one group changes, check whether the same change should be mirrored in later groups to preserve style consistency.

If the assistant finds its own issue after prompt groups are already visible, do not ask for a second confirmation and do not replace the whole package. Add a concise "Revision note" that states the reason, affected slides, and exact replacement prompts. The original package remains the base except for those replacements.

### 8. Generate a master sample first

After prompt approval, generate one representative slide before the rest. Usually choose slide 2 or 3, not the cover, because content slides reveal whether the system works.

Inspect the sample for:

- visual quality
- title readability
- reusable layout grammar
- enough blank/safe space
- whether it can support the full deck without becoming repetitive

If it fails, adjust the visual bible and affected prompts, ask for approval on the changed prompts, and regenerate the sample. Do not generate the whole deck before the sample is acceptable.

### 9. Generate one slide at a time

The skill itself is an instruction pack for Codex `image_gen` (GPT Image 2) slide generation. When executing the deck in Codex, use the built-in image generation path.

Generate each slide through Codex `image_gen` (GPT Image 2). Use one generation request per slide when slides have distinct content. Only use a multi-image request if the active Codex `image_gen` path supports separate prompts and returns separately trackable outputs.

For visual consistency, use the approved master sample as a style reference when the active image generation path supports reference images. If reference-image use is unavailable, repeat the visual bible exactly and keep prompts structurally identical.

Record every call in `image-generation-log.md`. Inspect every generated slide before assembling. Regenerate failed slides through Codex `image_gen` (GPT Image 2); do not repair failed full-image slides by redrawing them locally or adding text overlays.

### 10. QA and regenerate

Make a contact sheet or otherwise view all slide thumbnails together. Mark each slide:

- **pass:** consistent and readable
- **minor:** acceptable if the deck deadline is tight
- **regen:** must redo

Regenerate a slide when any of these appears:

- illegible or malformed title
- missing visible text that was supposed to be inside the generated image
- cover contains more than a main title and one optional subtitle, or uses an inner-page visual structure
- user or reviewer flags the deck as visually monotonous because too many slides accidentally reuse the same literal background or hero image
- slide is mostly decorative image with too little information for its role and selected content-density mode
- normal content slide looks too empty, like a poster or scenic image with minimal copy, when the user selected information-rich or balanced mode
- normal content slide contains only a title plus icon labels, attraction names, category names, or very short tags without useful explanation
- normal content slide prompt failed to specify concrete visible explanatory copy and instead used vague text-density instructions
- obvious artifact or stray mark that makes the slide look broken or unprofessional
- small supporting text becomes distracting enough to weaken the main slide message
- visual style clearly differs from the sample
- slide is much denser or emptier than neighboring slides
- slide text density conflicts with the selected content-density mode
- wrong aspect ratio, cropped content, broken layout, or unreadable chart
- key subject does not match the slide message

When regenerating, keep the visual bible stable and change only the failure-specific instruction.

If the user complains that the deck looks monotonous or backgrounds are too similar, do not defend it as "consistent." Revise only the affected prompts so those pages use more suitable visuals while preserving the selected PPT style. Do not add a rigid scene taxonomy unless the user asks for one.

### 11. Assemble the deck

If the user wants PPTX:

- create a 16:9 deck
- place each image full-bleed on its own slide
- do not add any visible text boxes, captions, page numbers, shapes, charts, or icons on top of the image
- prefer a minimal image-to-PPTX assembly method, such as a small script or `python-pptx`, instead of the Presentations skill/plugin
- use Presentations only as a last-mile fallback after images are generated, or when the user explicitly asks for that tool
- export PDF if requested
- verify output by rendering/opening previews and confirming every slide is visually complete as a single image

Keep source prompts and working images in a task workspace. Put final images, PPTX, and PDF in the requested output folder.

### 12. Revise or expand after delivery

Support follow-up edits without restarting the deck:

- **Modify one slide:** update that slide's prompt, show the revised prompt inline for approval when the change is non-trivial, keep the visual bible stable, regenerate only that slide through Codex `image_gen` (GPT Image 2), replace the image in the assembled deck, and update `image-generation-log.md`.
- **Modify several slides:** batch the prompt edits for those slide numbers, show the revised mini-group inline, regenerate only those slides through Codex `image_gen` (GPT Image 2), then reassemble.
- **Add new slides:** extend the deck spine, create prompts using the same visual bible and the same prompt-group format, ask for prompt approval for the new slides, generate them through Codex `image_gen` (GPT Image 2), insert them into the deck, and update numbering if the deck uses generated page markers.
- **Change global style:** treat this as a style migration. Regenerate a new master sample first, then regenerate all affected slides after prompt approval.
- **Change text richness/content density:** update the visual bible and affected slide prompts, show the changed prompts inline, then regenerate only the affected slides or all slides if the user wants a full density pass.

Do not repair a delivered deck by adding PPT text boxes or shapes. Any visible change must be made by regenerating the affected full-slide image.

For all post-generation revisions, preserve consistency by reusing:

- the locked visual bible
- the approved master sample as a style reference when supported
- the original aspect ratio, palette, lighting, margins, typography mood, page markers, and role system
- the same prompt-group wording around independent single-slide generation

If a user asks to change one slide in a way that would break the deck's style, state the conflict briefly and offer either a style-consistent revision or a full style migration.

## Practical Rules

- Do not start planning from vague defaults. For every new deck, first confirm page count, language, style, and text richness/content density unless the user already gave them.
- Prefer 12-18 slides for a first pass; 15 is a good default.
- Show the PPT slide-by-slide design document inline before prompt groups. This is required even when source notes or prompt files are also saved, but it is not a separate confirmation gate.
- Default slide design is 图文并茂: each slide should feel like a real PPT page, with text and visuals balanced according to its role and selected content-density mode.
- Show prompts inline in groups of up to 8 slides before generation. This is required even when prompt files are also saved.
- Ask for approval only once, after both the slide-by-slide design document and prompt groups have been shown.
- Complete prompt self-checks before showing the prompt groups. After prompts are visible, do not withdraw and regenerate the full prompt package; append revisions for only the affected slides or groups.
- Keep generated in-image text concise and readable. In information-rich mode, normal content slides need high information density. In balanced mode, they need useful explanatory copy with more breathing room. In concise mode, fewer words are acceptable and expected, but the page should still feel like a finished PPT page rather than an accidental empty background unless the user asks for visual-only pages.
- If a generated normal content slide has too little or too much text for the selected content-density mode, regenerate the affected slide with clearer visible-copy instructions instead of accepting the mismatch as a style choice.
- Prefer recurring page devices: corner number, chapter tag, consistent title position, repeated frame/grid.
- Make cover, divider, inner content, and closing pages visibly role-appropriate while sharing the same palette, typography mood, graphic language, and spacing system.
- Keep the chosen PPT style consistent. Do not reuse the same literal background across many slides unless the user asks for that.
- Use chapter-break slides to reset visual energy while preserving the same style.
- Do not ask the image model to reproduce official logos unless the user provides approved assets or explicitly wants unofficial concepts.
- Do not rely on generated images for exact charts. Use stylized chart-like proof with short generated labels; if exact data labels or editable charts are required, switch to a normal editable PPT workflow outside this skill.

## Handoff Checklist

Report:

- user-selected style, page count, language, and text richness/content density
- topic/source used, and whether a research pass was performed
- that prompt groups were shown inline for review, plus where the backup prompt files are saved
- production mode used, with Codex `image_gen` (GPT Image 2) as the generation path
- number of slide images generated
- where the image-generation log or prompt pack is saved
- final file paths
- what verification was performed
- any residual limitation, especially generated text accuracy inside images
