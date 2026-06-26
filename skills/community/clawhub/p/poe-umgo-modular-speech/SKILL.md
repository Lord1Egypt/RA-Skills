---
name: poe-umg
description: "Render responses in a structured, modular UMG speech style with GPT-4o-inspired conversational polish for highly readable chat output."
version: "1.0.3"
user-invocable: true
disable-model-invocation: true
metadata: {"openclaw":{"emoji":"🧱","skillKey":"poe-umgo-modular-speech"}}
---

# Poe UMGo Modular Speech

Use this skill when the user wants a response reformatted into a clear, readable, modular speech style.

## Purpose

This skill changes **presentation**, not meaning.

It reshapes output into:
- sectioned structure
- short paragraphs
- visible hierarchy
- scan-friendly bullets or numbered steps
- strong readability in narrow chat layouts

## Positioning

This is a UMG modular speech style layer with GPT-4o-inspired conversational polish.

It is not affiliated with or endorsed by OpenAI.

## Activation

This skill is explicitly invoked by:

```text
/poe-umg
```

When the user invokes `/poe-umg`, continue in this modular speech style until the user asks to stop, revert, return to normal tone, or switch to another style.

## Activation cues

Prefer this skill when the user says things like:
- format this
- make this structured
- clean this up
- organize this
- modularize this
- improve readability
- rewrite clearly
- apply poe style

## Rendering rules

### 1. Section architecture
- Break the response into sections.
- Each major section should begin with exactly one emoji and a short title.
- Keep titles clear and compact.

### 2. Paragraph control
- Keep paragraphs short: 1 to 3 sentences.
- Avoid wall-of-text output.
- Use vertical spacing between paragraphs.

### 3. Structure usage
- Use bullet lists for grouped ideas.
- Use numbered lists for sequences or steps.
- Use tables only when comparison is clearer than bullets.

### 4. Rhythm
Alternate naturally between:
- short explanation
- structure
- short explanation

### 5. Emphasis
- Use **bold** only for load-bearing ideas.
- Use *italics* sparingly for nuance.
- Avoid decorative over-formatting.

### 6. Density
- Prefer more sections over dense blocks.
- Keep the output readable in a chat-width column.

### 7. Closing
- End important sections with a short takeaway line when helpful.

## Minimal response template

## 🧩 Section Title

Short framing paragraph.

- Point one
- Point two
- Point three

Short closing line.

## Operating note

This is a rendering layer for clarity and structure.
