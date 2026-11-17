---
name: image-ppt-maker
description: "Create PPT-style images through a human-in-the-loop workflow: clarify presentation requirements including optional top-corner LOGO space, research and draft McKinsey-style master and page-by-page outlines, expand page content, confirm the desired visual style before image prompts, write unified-style image-2 prompts, batch-generate 16:9 slide images, automatically assemble the images into a playable 16:9 HTML slideshow, and finally write oral speaker notes based on the outline and final images. Use for PPT风格图片, PPT图片生成, image-2幻灯片图片, 麦肯锡式分页大纲, 口语化讲稿, 批量生成演示页图片, HTML播放版演示, or presentation image prompt workflows. This skill does not assemble PPTX files."
---

# Image PPT Maker

Help users create a set of PPT-style slide images with image-2. Use a strict review-gated workflow:

1. Confirm requirements.
2. Build a McKinsey-style master outline and page-by-page outline.
3. Expand the outline content.
4. Confirm the desired visual style for the images.
5. Write unified-style image-2 prompts.
6. Batch-generate 16:9 PPT images.
7. Review the generated images with the user and revise affected pages if needed.
8. Assemble the user-approved final images into a playable 16:9 HTML slideshow.
9. Write duration-aware, directly readable oral speaker notes based on the approved outline and final images.

Ask the user whether they want changes only at the review gates listed below. Image prompts are internal execution artifacts, not a review gate. Do not assemble HTML or write final speaker notes until the user explicitly approves the generated images.

## Required References

- Read [workflow.md](references/workflow.md) before starting any task.
- Read [mckinsey-outline.md](references/mckinsey-outline.md) before drafting or revising outlines.
- Read [image-2-prompts.md](references/image-2-prompts.md) before writing prompts or generating images.
- Use [generate-html-player.mjs](scripts/generate-html-player.mjs) only after the user approves final local images for a playable HTML output.

## Core Rules

1. Use the user's language for questions and deliverables unless they specify another deck language.
2. If key information is missing, ask concise questions before outlining: topic, goal, audience, style, duration, slide count, information density, source material, constraints, and whether to reserve a small LOGO area in the upper-left or upper-right corner.
3. Summarize the confirmed brief and ask whether the user has changes before creating the outline.
4. Use McKinsey-style logic: answer first, issue-tree thinking, MECE where practical, one governing thought per slide, and a clear so what.
5. Every page in the outline must include logic notes. Do not create title-only or decorative pages.
6. After the outline is approved, expand each page with richer content, examples, implications, and visual emphasis. Do not output speaker notes yet.
7. Before writing image prompts, ask the user what visual style they prefer and recommend context-aware options such as training style with friendly editorial illustrations, executive report style with restrained illustration accents, illustration-led storytelling with recurring characters and scenes, graphic/chart-heavy, product demo style, or other suitable options.
8. Generate one image per slide, 16:9, with image-2. Do not create final slide images with SVG, HTML, screenshots, local drawing, PowerPoint export, or montage workflows.
9. Treat image generation as a long-running operation. Do not interpret a quiet period, a partial preview, or a tool call with no immediate new image as failure. Keep the generation task alive, wait for its final completion signal, inspect the output directory for newly completed files, and report progress without triggering a duplicate generation. Retry only after an explicit tool failure, confirmed timeout, or confirmed missing/corrupt output after completion.
10. After image generation, present the final image paths or previews and ask the user whether any page needs adjustment. Do not assemble HTML or write final speaker notes until the user explicitly approves the images.
11. After the user approves the images, automatically generate a playable 16:9 HTML slideshow from the final local images.
12. After HTML assembly, write final per-slide speaker notes based on the approved outline and final images. Allocate page-level speaking time to match the confirmed duration, and write a complete, directly readable oral script for each page.
13. This skill does not assemble PPTX files. Stop at generated images, HTML slideshow, prompt records, final speaker notes, and revision notes.
14. Preserve approved work during revisions. Only regenerate the affected downstream artifacts.
15. Do not ask the user to review or approve image prompts. After the page content and visual style are approved, write the prompts and proceed directly to image generation.
16. For every later single-page change, re-run the complete single-page content flow while reusing the approved deck-wide style. Confirm the revised page content before generating that page's image; never regenerate directly from raw feedback.

## Workflow Gates

Do not skip these review points:

- After requirement parsing: ask whether the brief and assumptions need changes.
- After the master outline and page-by-page outline: ask whether the storyline, page count, or logic needs changes.
- After the expanded outline content: ask whether the content depth, examples, or emphasis needs changes.
- Before writing image-2 prompts: ask which visual style the user prefers, offering context-aware recommendations that include concrete illustration directions when illustration is suitable.
- After image generation: present the completed images and ask whether any page needs changes; wait for explicit approval before HTML assembly and final speaker notes.
- After HTML assembly and final speaker notes: ask whether any HTML output or speaker note should be adjusted.

Never create a prompt-review gate. Prompt creation proceeds automatically after the preceding content and style approvals.

If the user requests changes:

- Requirement changes invalidate outline, prompts, and images.
- Outline changes invalidate affected expanded content, prompts, images, HTML, and final speaker notes.
- Visual-style changes invalidate prompts, images, HTML, and final speaker notes.
- Final speaker-note changes do not invalidate prompts, images, or HTML unless the visible slide content or logic changes.
- Style changes invalidate prompts, images, HTML, and final speaker notes according to the affected scope.
- Any single-page content or image change must enter the single-page revision loop in [workflow.md](references/workflow.md): clarify the page request, rebuild the page logic and expanded content, obtain explicit content approval, rebuild the prompt internally without asking for prompt approval, generate only that page, and review the new image.
- Never regenerate a page immediately from user feedback, even when the requested change seems small. Reconfirm the revised page content first. Reuse the existing style lock and do not repeat visual-style confirmation unless the user explicitly asks to change the deck style.
- HTML output must be regenerated if final image filenames, image count, title, or image folder changes.

## Deliverables

When complete, provide:

- confirmed brief;
- master outline and page-by-page outline;
- expanded outline content;
- image-2 prompt set with the shared style lock;
- generated image paths or previews;
- playable 16:9 HTML slideshow path;
- final oral speaker notes based on the outline and generated images;
- concise notes on pages that may need regeneration.
