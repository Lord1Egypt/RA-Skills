---
name: tutorial-website-builder
description: Create reusable paged HTML tutorial guides from operation workflows, screenshots, videos, links, reference images, and step-by-step documentation. Use when the user asks to extract a reusable UI style prompt from a reference image, choose a saved style prompt, or turn a software installation guide, tool setup process, knowledge-base tutorial, AI workflow explanation, brand walkthrough, product tutorial, or other procedural content into a single-file HTML page with configurable style systems, media in images/videos directories, pagination, captions, lightbox preview, and responsive tutorial layout.
---

# Tutorial Website Builder

## Overview

Use this skill for two related workflows:

1. Extract a reusable UI style prompt from a user-provided reference image.
2. Generate a single-file paged HTML tutorial using a selected UI style prompt.

The expected HTML output is an immediately usable tutorial page, not a marketing landing page. The first screen must enter the tutorial content directly.

## Workflow A: Extract Style From Image

When the user provides a reference image and asks to create, extract, save, or package a style:

1. Read `references/style-extraction-schema.md`.
2. Analyze only the visual language of the image: layout, typography, color, components, spacing, media treatment, illustration logic, interaction mood, and responsive implications.
3. Fill the schema fields with concrete reusable defaults. Do not merely describe the image; convert what you see into a style system another agent can apply to a webpage.
4. Name the style by its visual language, using lowercase hyphen-case English for the file name.
5. Save the reusable prompt as `references/styles/<style-name>.md`.
6. If the image contains protected logos, characters, private UI, or copyrighted artwork, extract the general visual system only. Do not instruct future pages to copy exact proprietary elements.
7. Report the created style file path and the human-readable style name.

Do not generate the tutorial HTML in this workflow unless the user also asks for it.

## Workflow B: Generate Tutorial HTML

When the user asks to generate or modify a tutorial HTML:

1. Identify available style prompts:
   - `references/default-ui-system.md`
   - every `*.md` file in `references/styles/`
2. If the user has not specified a style, ask which style prompt to use. Keep the question concise and include the default option.
3. Read the selected style prompt before designing the HTML.
4. Also read `references/production-guide.md`.
5. Always apply the three bottom-level logic rules below, even if the selected style prompt does not mention them.
6. Generate or edit the HTML according to the selected style, tutorial content, and media available in the project.

Default media folders remain:

```text
tutorial.html
images/
  image_01.png
  image_02.png
videos/
  video_01.mp4
```

The user may confirm or adjust actual image/video placement later in the conversation. Do not require that confirmation before producing a scaffold when the user asks for one.

## Required Bottom-Level Logic

These rules override individual style prompts and component convenience.

### 1. No Card-Inside-Card Composition

Never build the page by stacking many cards inside other cards. Use one primary page/container surface, then create hierarchy with grid, typography, borders, divider lines, labels, media frames, verification blocks, and whitespace.

Avoid repeated nested rounded rectangles such as `card > card > panel > media card`.

### 2. Meaningful Graphics Only

Do not add graphics by default. Any illustration, icon, shape, branch, leaf, animal, smoke, stream, hill, background mark, or decorative object must have a clear purpose:

- Aesthetic framing.
- Topic symbolism.
- Section rhythm.
- Directional guidance.
- State feedback.
- Media annotation.
- Brand mood reinforcement.

If the graphic cannot be explained, omit it. If graphics make the page busy or weaken the focal point, remove them.

### 3. Tutorial Readability First

Layout styles can be diverse, but the page is a tutorial first. Every page must make these items easy to find:

- Current step.
- Current action.
- Why the step matters.
- Media that verifies the action.
- Observable success condition.

Do not use visual variation that makes reading order ambiguous, separates media from its explanation, hides verification standards, creates long scanning paths, or turns the tutorial into a decorative poster.

## User Configuration

Before generating the final HTML, ask whether any selected style defaults should be changed. Keep the question concise:

```text
默认使用所选风格提示词。是否需要修改主色、字体、圆角、间距、导航、媒体样式、插图风格或动效？如果不需要，我将按默认值生成。
```

If the user does not specify changes, proceed with the selected style defaults. Do not repeatedly ask configuration questions.

When the user provides overrides, update only the relevant tokens or component rules while preserving the rest of the selected style.

## Tutorial Content Rules

1. Inventory the user-provided material:
   - Steps or rough workflow text.
   - Screenshots in `images/`, preferably named `image_01.png`, `image_02.png`, etc.
   - Videos in `videos/`, preferably named `video_01.mp4`, `video_02.mp4`, etc.
   - Official sites, source articles, tool pages, documentation links, or other external references.
2. Split the tutorial by the real execution order. Each page must cover one action or one tightly related group of actions.
3. For each page, write only the current step:
   - What the user is trying to accomplish.
   - What to do now.
   - What visible result means the step is complete.
4. Attach media after the explanation so the image or video verifies the operation, rather than replacing the instructions.
5. Number all figures globally by appearance order: `图 1`, `图 2`, `图 3`. Do not reset numbering per step.
6. Embed links directly in the body text with `target="_blank"` and `rel="noopener noreferrer"`.

## Output Requirements

- Create a single HTML file unless the user explicitly asks for a framework project.
- Use `assets/newspaper-tutorial-template.html` as a structural starting point when useful, but restyle it according to the selected style prompt.
- Keep all style choices in CSS custom properties or equivalent design tokens.
- Keep exactly one navigation area near the top: current page indicator plus previous/next buttons.
- Use `data-step` sections and a single `totalSteps` value in JavaScript.
- Derive Chinese page numerals from the step count.
- Support clickable image enlargement. Videos should remain playable inline.
- Make mobile layout single-column with large enough navigation buttons.

## Quality Gate

Before delivery, check:

- The selected style prompt is applied consistently.
- The three bottom-level logic rules are applied.
- Previous/next buttons correctly disable on first and last pages.
- Only one navigation area exists.
- Current page indicator and total page count match the number of step sections.
- Figure numbers increase globally in display order.
- Every `src` path points to the correct `images/` or `videos/` directory.
- Every image has useful `alt` text and every media item has a concise caption.
- Links open in a new tab and use `rel="noopener noreferrer"`.
- The page works when opened as a local HTML file.
- Mobile width does not create horizontal scrolling, clipped buttons, or text overlap.
