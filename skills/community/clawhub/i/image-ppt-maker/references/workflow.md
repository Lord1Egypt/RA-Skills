# Workflow

Follow this workflow exactly. Pause only at the designated review gates. Image-prompt creation is not a review gate.

## 1. Confirm requirements

Parse the user's request and collect missing key details:

- topic and background;
- presentation goal: what the audience should understand, believe, decide, or do;
- audience: executives, customers, internal team, review panel, investors, or another group;
- duration and approximate slide count; use the duration as the total speaking-time budget for the final script;
- information density: high, medium, or low;
- preferred visual style or reference material;
- source material, facts, data, cases, and constraints;
- output language and tone;
- whether to reserve a small LOGO area in the upper-left or upper-right corner, or no LOGO area;
- any content that must not be invented.

If the user is unsure, recommend practical defaults:

- duration: 10 minutes;
- slide count: 8-12 pages;
- information density: medium;
- style: clean McKinsey-style consulting deck with restrained color, strong hierarchy, and chart-like logic.
- LOGO area: no reserved LOGO area unless the user asks; if they want it, recommend a small upper-right area for corporate decks and upper-left for brand-led decks.

Then summarize the brief, including the LOGO-space decision, and ask: "以上需求和假设是否需要修改？确认后我会生成总纲和分页大纲。"

## 2. Research and outline

Use the user's source material first. If internet research is requested or required for current facts, browse and cite sources in the final summary.

Create:

- master outline: core answer, main logic chain, issue tree, and section flow;
- page-by-page outline: one page per slide, with complete logic notes and a suggested speaking-time allocation. Allocate the total speaking time across pages according to message importance and complexity; keep the sum aligned with the confirmed duration.

Ask: "这个总纲和分页大纲是否需要调整？确认后我会拓展每页内容。"

## 3. Expand outline content

After the user approves the master outline and page-by-page outline, expand the content before prompt writing.

For each slide, produce:

- expanded content: richer explanation of the page's message, evidence, implications, and examples;
- example ideas: practical examples, analogies, or mini-scenarios that make the point concrete;
- visual emphasis: what the generated image should make most obvious;
- speaking hints: brief notes that may help final speaker-note writing later, but do not output the final talk track yet.

Do not output the final speaker notes in this stage. Final notes must be written after image generation and HTML assembly, using the approved outline and the final generated images.

Ask: "拓展后的内容、例子和视觉重点是否需要调整？确认后我会先和你确认图片风格，再生成每页的 image-2 提示词。"

## 4. Confirm visual style

Before writing image-2 prompts, ask the user what visual style they want. Recommend options based on the context instead of using a fixed list.

Common options include:

- 培训风：更亲和，结构清楚，适合课程、工作坊、内部分享；
- 汇报风：更克制、专业、结论先行，适合管理层汇报和项目汇报；
- 培训插画风：在清晰的咨询式结构中加入友好人物、课堂/工作场景、轻量叙事插画和统一笔触，适合课程、工作坊、内部分享；
- 插画叙事风：用连续出现的角色、场景和视觉隐喻讲清问题变化，搭配少量结构化图形，适合传播、培训、文化和用户故事类主题；
- 汇报插画风：保持结论先行和克制留白，用少量高质量场景插画解释复杂概念，适合管理层汇报中需要提升亲和力的主题；
- 多图形：更多框架图、流程图、矩阵、图表，适合战略、经营、方案类主题；
- 科技感：更适合 AI、数字化、产品技术主题；
- 品牌简洁风：留白更多，适合客户沟通、品牌展示、对外路演。

Recommend 2-4 options that fit the user's topic, audience, duration, and information density, then ask: "你更倾向哪种图片风格？确认后我会把这个风格锁定到整套 image-2 提示词中。"

## 5. Write image-2 prompts

Before writing per-page prompts, define one deck-wide style lock. Apply it to every prompt.

For each slide, write one self-contained image-2 prompt that includes:

- shared style lock;
- single-slide 16:9 instruction;
- LOGO-space instruction if the user requested one;
- page logic;
- expanded content and speaker-note intent where useful;
- the thought and content this page should express, including recommended title, key messages, labels, and emphasis;
- composition and visual structure;
- negative constraints.

Do not show the prompt set for approval and do not ask whether the prompts need changes. Once the approved page content and style lock are available, proceed directly to batch image generation.

## 6. Batch-generate images

Generate exactly one 16:9 image per slide with image-2.

Generation may take many minutes. When generating several pages in parallel or in a batch:

- announce that the operation is long-running and that no immediate new preview does not mean generation failed;
- keep the original generation task running and wait for its final return/completion signal;
- monitor completed files or returned images without launching a second batch;
- preserve already completed pages and report the current count when progress is available;
- retry only after explicit failure, confirmed timeout, or confirmed missing/corrupt output after the task has ended.

Never claim that a batch failed merely because it has been quiet for a while. Never start a duplicate batch while the original task may still be producing images.

Use ordered filenames when files can be saved locally:

```text
images/slide-01.png
images/slide-02.png
images/slide-03.png
```

If local saving is not supported by the active image tool, explain the limitation and provide the generated previews or prompt set.

The ordered filename is for storage and HTML sequencing only. It must never be rendered inside the slide image. Do not put slide numbers, page numbers, sequence labels, numeric badges, or file names in the title, footer, corner, diagram, timeline, or any other visible area unless the user explicitly requires a number as part of the page content.

After all images are complete, present their paths or previews for a dedicated image review. Ask: "图片已生成。是否有页面需要修改？确认最终图片后，我会组装 HTML 播放器并生成逐页讲稿。"

Do not assemble HTML or write final speaker notes until the user explicitly approves the images. If the user requests image changes, regenerate only the affected pages where possible, then return to this image-review gate.

## 7. Automatically assemble playable HTML slideshow

After the user approves the final local slide images, automatically:

- create an output folder with `index.html` and `assets/`;
- copy or reference the final slide images in order as `assets/slide-01.png`, `assets/slide-02.png`, etc.;
- generate a full-viewport 16:9 player modeled after `C:\project\img-ppt\ai-course-html\index.html`;
- include previous/next buttons, click zones, keyboard navigation, progress display, and fullscreen support;
- keep each image inside a 16:9 frame with `object-fit: contain`;
- do not alter the slide images while assembling the HTML.

Use `scripts/generate-html-player.mjs` when local image files are available. If images are not local files, explain that HTML assembly requires local image files and ask the user to provide them.

## 8. Write final speaker notes

After final images and HTML are ready, write the final speaker notes page by page. Use:

- the confirmed brief;
- the master outline and page-by-page outline;
- expanded content and examples;
- the final generated slide images and what each image visually emphasizes.

Treat the confirmed presentation duration as a delivery constraint. Before writing, allocate target speaking time to every slide and ensure the total matches the requested duration, allowing only a small buffer for natural pauses and page transitions. Give substantive pages more time than title, agenda, or closing pages.

For every slide, provide:

- `pageNumber`;
- `imagePath`;
- `targetDuration`: planned spoken time for the page;
- `talkTrack`: a complete, directly readable oral script, not an outline or speaking hints;
- `exampleLines`: examples, analogies, or mini-scenarios woven into the script where they improve clarity;
- `transition`: a conversational bridge to the next page.

Speaker notes should sound like a person presenting to the target audience. Write enough natural spoken content to fill each page's target duration at a normal pace: approximately 180-240 Chinese characters per minute for Chinese, or 120-150 words per minute for English; adapt for the target language and the user's requested pace. Use short sentences, warm phrasing, and concrete examples. Include natural pauses, emphasis, and transitions where useful. Avoid report-style prose, slogans, stiff corporate language, terse bullet-point notes, and mechanically reading every visible word on the slide.

Ask at the end: "已生成图片、HTML 播放器和逐页讲稿。是否有页面、HTML 播放效果或讲稿需要调整？"

## Revision handling

### Mandatory single-page revision loop

Whenever the user requests any later change to one page, run this loop every time, including for small copy, layout, emphasis, example, data, or image corrections:

1. Identify the target page and clarify the requested outcome, required facts, constraints, and unchanged elements. Ask only for missing information.
2. Reuse the approved deck brief, LOGO decision, surrounding storyline, and complete deck-wide style lock. Do not repeat visual-style confirmation unless the user explicitly requests a style change.
3. Rebuild that page's page-by-page outline fields: conclusion-style title, key question, governing thought, supporting logic, visual idea, so what, transition, and speaking-time allocation.
4. Rebuild that page's expanded content, examples, labels, visual emphasis, and any factual constraints.
5. Present the consolidated revised page content to the user and ask: "这页修改后的逻辑、内容和视觉重点是否确认？确认后我会直接生成该页图片。"
6. Only after explicit content approval, rebuild the page's image prompt internally with the existing style lock. Do not show or ask the user to approve the prompt.
7. Generate only the affected page image, preserve all other approved images, and present the new image for review.
8. If the user requests another change to that page, restart this loop before generating again. Do not patch or regenerate the image directly from the latest feedback.
9. After the revised image is approved, regenerate the HTML and affected final speaker notes if those downstream artifacts already exist.

- Requirement edits require revising the outline, prompts, and images.
- Outline edits require revising affected expanded content, prompts, images, HTML, and final speaker notes.
- Final speaker-note edits require revising prompts only if visible text, page logic, or visual emphasis changes.
- Style edits require revising all prompts, images, HTML, and final speaker notes unless the user limits the change to specific pages.
- Internal prompt edits require regenerating affected images, but prompts never require user approval.
- Image feedback should be applied through the mandatory single-page revision loop, followed by another explicit image review before HTML assembly and final speaker-note writing.
- HTML output must be regenerated after any final image change.

This skill stops at PPT-style images, playable HTML, and final speaker notes. Do not assemble a PPTX.
