# Artifact Format — 04-build-notes.md

Output of Phase 4. One entry appended **per slide**, written before the slide's HTML is written.
The note and the HTML for each slide are produced together — do not batch all notes first.

```markdown
# Build Notes — <slug>

## Slide <N> — <job>

**Layout:** <one sentence — must be writable before any HTML is written; if you can't write it, the job isn't clear>
**Because:** <content shape from 02-slide-plan.md — copy the exact phrase from the Content shape column>
**Headline strategy (optional):** <only when using a compressed headline, support line, non-default tier, or poster-style exception — format: "[display headline]" — Tier: hero-xl | hero-lg | section-md | compact-md — Support line: [text or none]>

## Slide <N+1> — <job>

**Layout:** ...
**Because:** ...
**Headline strategy (optional):** ...
```

**The "Because" field must reference the Content shape from the slide plan, not a re-invented description.**
If the Content shape in the plan says "演进时间线" and you implement a card grid instead, that is a plan deviation — either update the plan or implement the timeline.
