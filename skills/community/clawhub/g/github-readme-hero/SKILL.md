---
name: github-readme-hero
description: Turn ordinary GitHub README pages, skill landing pages, or Markdown intros into cover-like hero layouts with centered titles, quote-led openings, restrained badges, horizontal navigation, and preserved original voice. Use when the user wants a GitHub README to feel like a designed front page without losing its strongest original introduction, especially for Chinese-first or bilingual repositories that need stronger presentation.
---

# GitHub-README Hero.skill

A weak README explains itself. A strong README arrives with presence.

This skill exists for pages that already have a voice, a strong sentence, or a real idea, but still look like raw Markdown instead of a deliberate front page.

Use this skill when the user wants a README, skill page, or landing-style Markdown document to feel more like a designed front page:
- GitHub README beautification
- ClawHub skill page polish
- hero-section redesign
- quote + badge + navigation layout
- preserving a strong original intro while improving presentation
- upgrading the front page of a Chinese-first README
- making a skill page feel more like a product showcase
- preserving the strongest original line while redesigning only the first screen

Do not use this skill for generic copywriting, long-form documentation editing, or full website implementation unless the user specifically wants the document itself restyled.

## Core Promise

Do not delete the soul of the page.

Your job is not to replace the author's best line with decorative polish. Your job is to:
1. identify the best existing line, quote, or paragraph
2. elevate it into a stronger first screen
3. preserve the original substance underneath
4. make the page feel intentional, clean, and memorable

This skill should sharpen the entrance, not erase the voice.

## Default Workflow

### 1. Read the top of the document first

Inspect the first 30-80 lines before editing.

Look for:
- the strongest quote-worthy sentence
- the real title
- whether the page is bilingual
- whether the page already has useful sections worth linking to
- whether the current top is dry, cluttered, or visually weak

### 2. Decide the hero structure

Prefer this top-level structure when suitable:

```md
<div align="center">

# Title

> Strong quote or distilled line

![badge](...)
![badge](...)

<p align="center">
  horizontal navigation
</p>

<p align="center">
  short subtitle or two-line promise
</p>

</div>

---
```

Use it only if it improves the page. Do not force it onto documents that need a plain technical opening.

### 3. Preserve the original introduction

After the hero block:
- keep the original opening material if it has literary force or brand value
- trim only duplication introduced by the new hero
- do not flatten expressive copy into bland product language

If the author already wrote a powerful intro, keep it alive.

### 4. Add badges with restraint

Badges should signal structure, not become confetti.

Good uses:
- bilingual
- mode or category
- platform
- output style
- standard / workflow type

Bad uses:
- five badges that all say the same thing
- random rainbow clutter
- fake technical authority

Default range: 3-5 badges.

Prefer `flat-square` style unless the repo already uses something else.

### 5. Make navigation horizontal and useful

If the page is long enough to justify navigation:
- add a centered horizontal link row near the top
- link only to real high-value sections
- create stable anchor ids when necessary

Good examples:
- Chinese / English
- Install
- Usage
- Examples
- Prompt
- Output

Do not add navigation if the document is too short to need it.

### 6. Use renderer-safe HTML only

Prefer Markdown plus minimal HTML that renders well in GitHub-like surfaces:
- `<div align="center">`
- `<p align="center">`
- `<br />`
- `<a id="..."></a>`

Avoid:
- inline CSS
- scripts
- complex tables for decoration
- fragile HTML tricks that break on GitHub or ClawHub

### 7. Respect bilingual logic

If the page is bilingual:
- keep the language order the user wants
- keep heading patterns consistent
- do not mix languages randomly inside one line unless the document already uses that style intentionally

If the user wants Chinese-first, keep Chinese-first.
If the user wants English-first, keep English-first.

For Chinese-facing pages:
- prefer Chinese-first copy and navigation labels unless the user explicitly wants English-first
- preserve literary Chinese phrasing when it carries brand value
- do not flatten vivid Chinese introductions into stiff product prose
- keep the page readable to Chinese users before making it impressive to everyone else

## Editing Principles

- Favor visual hierarchy over more words
- Favor one strong quote over three weak slogans
- Favor one clean hero over many decorative gimmicks
- Preserve the strongest original copy
- Keep the first screen readable in raw Markdown and rendered view
- Make the page look designed, not overdesigned

## Output Rules

When you edit:
- keep the page functional as Markdown
- keep links and anchors valid
- keep section order logical
- keep existing meaning intact unless the user asks for copy changes
- explain briefly what you changed and why

If the user asks for a specific style reference:
- mirror the layout principles
- do not plagiarize exact wording
- adapt the style to the user's own content and voice

## Typical Requests That Should Trigger This Skill

- "Make my README look like a landing page"
- "Why does their README look so much better than mine?"
- "Add a centered title, badges, and navigation"
- "Keep my intro, but make the top prettier"
- "Turn this skill page into a poster-style cover"
- "Make this GitHub / ClawHub page feel more premium"
- "Rework my GitHub README into this kind of front-page layout"
- "Keep the original introduction, but make the top feel more premium"
- "Use this screenshot as the reference and turn my skill page into a showcase-style page"
