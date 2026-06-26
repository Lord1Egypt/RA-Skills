# linkedin-carousel-factory

## Description
Generate a complete 10-slide LinkedIn carousel JSON for .NET developers. Takes a topic and produces a structured, hook-driven carousel ready for Claude Code ACP punch-up before publishing.

## Use when
- OpenClaw trend scout has approved a weekly .NET carousel topic
- Lam requests a new carousel on a specific topic
- Engine 3 content pipeline triggers Sunday 9pm

## Input format
```
Topic: [topic]
Audience: mid-to-senior .NET developers
Goal: [educate | provoke | warn | showcase]
Hook angle: [optional — if blank, agent picks strongest]
```

## Output format
Return a JSON object with exactly 10 slides:
```json
{
  "topic": "...",
  "hook": "...",
  "slides": [
    { "slide": 1, "type": "hook", "headline": "...", "body": "...", "code": null },
    { "slide": 2, "type": "problem", "headline": "...", "body": "...", "code": null },
    { "slide": 3, "type": "content", "headline": "...", "body": "...", "code": "..." },
    ...
    { "slide": 10, "type": "cta", "headline": "...", "body": "...", "code": null }
  ]
}
```

Slide types: `hook`, `problem`, `content`, `comparison`, `warning`, `tip`, `cta`

## Slide rules
- **Slide 1 (hook):** Pattern interrupt. Must make a mid-senior .NET dev stop scrolling. Question, counterintuitive claim, or "here's what everyone gets wrong". Under 12 words.
- **Slides 2–8 (content):** Each slide = one idea. Headline under 8 words. Body under 40 words. Code snippets: .NET 8+, syntactically correct, no placeholder comments.
- **Slide 9 (comparison or warning):** Before/after or common mistake. Make the right way obvious.
- **Slide 10 (CTA):** Ask for one specific action — follow, comment with X, save for later. Not "like and subscribe."

## Voice rules
- Audience: sceptical, experienced. Do not talk down to them.
- No AI phrases: "it's important to note", "leveraging", "game-changer", "delve", "in today's world"
- Concrete > abstract. Show the code, not the concept.

## Write output to
`~/Documents/Obsidian/ClawBrain/skills/draft/carousel-[topic-slug]-[date].json`

## After generation
Post to Discord `#✅-tasks`: "Carousel draft ready: [topic]. Review in vault → skills/draft/"
Wait for Claude Code ACP punch-up before sending to Lam for approval.

## Self-improvement instructions
After Lam approves a carousel: note what hook angle worked in `memory/what_works.md` under "Engine 3 — Content".
After Lam revises: note what was changed and why.
