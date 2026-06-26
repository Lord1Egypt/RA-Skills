---
name: "longform-blog-writer"
description: "Writes publication-ready longform blog posts with strong structure, accurate definitions, and balanced critique. Use when user asks to draft an article/newsletter/essay, or wants a deep, polished blog post (not a quick answer)."
---

# Longform Blog Writer

Write a longform blog post that is coherent, well-structured, and intellectually honest. Optimize for clarity, narrative flow, and usefulness to the target reader.

**Language:** Respond in the same language the user writes in. If mixed, default to English.

---

## When to Use

Use this skill when the user asks to:
- write a blog post / longform article / newsletter / essay
- turn notes into a publishable post
- produce a structured, high-quality draft with sections, examples, and references

Do not use this skill when the user only wants a short explanation or a one-paragraph summary.

---

## Workflow

### Step 1: Intake (ask in one message)

Ask for:
1. Topic + angle (what is the main claim or question?)
2. Target reader (beginner / practitioner / researcher / general public)
3. Tone (neutral / opinionated / playful / academic-lite)
4. Desired length (short / standard / long)
5. Any constraints (company blog style, SEO keywords, “no hype”, etc.)
6. Sources (links, papers, docs) and what must be cited

If the user does not specify, assume: practitioner audience, neutral tone, standard length.

### Step 2: Propose an outline

Return a tight outline first. Do not draft the full article until the outline is accepted (unless the user explicitly says “just write it”).

### Step 3: Draft (longform)

Write the full article following the structure below. Use short paragraphs, clear headings, and concrete examples.

### Step 4: Revise

Do one editing pass with:
- clearer topic sentences per section
- removal of filler
- consistency of terminology
- stronger transitions between sections

---

## Article Structure (default)

Always use this backbone unless the user requests a different format:

1. Title
2. Hook (why care?)
3. Context / background
4. Core idea (the main claim)
5. Deep dive (how it works / why it’s true)
6. Trade-offs / limitations / failure cases
7. Practical takeaways (what to do next)
8. References / further reading
9. Optional: Glossary (for long or technical posts)

---

## Types (choose one)

Pick the best type based on the topic; if unclear, ask the user to choose:

1. **Technical tutorial** (programming / tooling)
2. **Research explainer** (paper walkthrough or field overview)
3. **Math concept** (conceptual + minimal essential equations)
4. **Book review** (critical and comparative)
5. **Science communication** (non-specialist, no hype)

### Type-specific requirements

**Technical tutorial**
- Include runnable code snippets.
- Include a “Best practices” section and an “Anti-patterns” section.

**Research explainer**
- Clearly separate: established consensus vs. open questions vs. debate.
- Cite primary sources; do not invent citations.

**Math concept**
- Explain intuition first, then introduce equations sparingly.
- Define symbols and interpret every equation in plain language.

**Book review**
- Include strengths + weaknesses, and compare to at least 2 related works.

**Science communication**
- Explain like to an intelligent non-specialist.
- Prefer analogies and visual descriptions; minimize formulas.

---

## Concept Decoder Integration

Invoke the `concept-decoder` skill when:
- a key concept needs more than two sentences to define well
- the concept is central and non-trivial
- the target reader is non-specialist and the term would be opaque

Embed the result as a short “Concept Spotlight” block, then continue the article.

---

## Citations and Factuality

- Do not fabricate names, dates, statistics, or citations.
- If a claim is uncertain or contested, label it clearly.
- Prefer primary sources (papers, official docs, standards) over secondary commentary.
- If real-time verification is required, explicitly tell the user what to verify before publishing.

---

## Input/Output

### Input
- Topic + optional notes, audience, tone, and desired length.
- Optional: source links or documents to cite.

### Output
- A publishable blog post in Markdown, following the selected type requirements.
- If needed, invokes `concept-decoder` for deep concept explanations and embeds them cleanly.
