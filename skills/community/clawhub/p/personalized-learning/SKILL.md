---
name: personalized-learning
description: Use this skill whenever the user wants to systematically learn a topic, asks for a study path, curriculum, lesson outline, tutorial-style walkthrough, concept primer, chapter-by-chapter explanation, or a readable knowledge page. Also use it when the user wants an explorable learning HTML page, even if they do not explicitly say "teach me" or "make a course." The skill infers the learner's background, plans a progressive outline, expands every section into audience-appropriate teaching content with visuals, and by default packages the result as a single self-contained HTML page with left-side navigation and right-side lesson content that should be delivered to the user as an HTML file.
---

# Personalized Learning

## Purpose
- Turn a learning request into a structured teaching deliverable.
- Support topic scoping, outline design, section writing, instructional visuals, and final packaging.
- Use this skill for systematic learning tasks, not for unrelated coding work, casual chat, or simple copy edits.

## Preparation
- Read [references/html-template.html](references/html-template.html) before writing so the structure and styling stay aligned with the intended page layout.
- Infer the learner's background conservatively from context when it is not stated. Prefer clarity over unnecessary density.

## Workflow

### 1. Understand the learning request
- Identify the topic, learning goal, learner background, likely use case, and tone.
- If the learner profile is ambiguous, choose the simplest framing that still respects the topic.

### 2. Plan the outline internally
Create a short internal outline and do not show it separately unless the user asks for it.
- One clear overall title
- Up to 10 section titles in a logical progression

Outline rules:
- Keep titles focused on the knowledge itself.
- Avoid filler such as "Chapter 1," "Study Plan," or other low-information labels.
- Make each section distinct and order them so understanding builds step by step.

### 3. Write every section completely
Every outline section must have a matching full section in the final output.

Each section should include:
- the core concept, mechanism, or principle
- at least one explanatory visual using `svg` or `canvas`
- an example, analogy, or realistic scenario
- a common mistake, edge case, or misconception
- a short wrap-up that connects naturally to the next section when helpful

Writing rules:
- Stay within the boundary of the current section title.
- Adjust terminology, pacing, and examples to the learner's background.
- Use plain, natural language and break difficult ideas into smaller steps.

### 4. Design instructional visuals
- Use visuals to explain relationships, structure, flow, timelines, or state changes.
- Prefer `svg` for static diagrams.
- Use `canvas` only when motion or step-by-step change genuinely improves understanding.
- Keep labels concise and let the visual do most of the explanatory work.
- Inline all styles, scripts, graphics, and animation logic when producing HTML so the result remains self-contained.

### 5. Assemble the final deliverable
- Default to one complete HTML document that follows the template structure.
- If the user explicitly requests another output format, keep the same teaching workflow but adapt the final packaging to that format.
- Ensure the navigation and body stay perfectly aligned: every planned section appears in both places with full content.
- When the final format is HTML, save it as an actual `.html` file and provide that file to the user.

For HTML output:
- Left side: clickable outline navigation with current-section highlighting
- Right side: full lesson content for every planned section, including headings, prose, and visuals

## Output Rules
- Return only the final deliverable, without conversational framing such as "Here is your page" or "I will generate."
- If the output is HTML, make sure the user receives the generated `.html` file rather than only a pasted code block.
- Keep the result suitable for long-form reading and visually restrained.
- Make sure no section from the outline is missing from the final content.

## Resource
- HTML template: [references/html-template.html](references/html-template.html)
