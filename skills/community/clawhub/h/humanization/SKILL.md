---
name: humanization
description: Check an essay's AI score on ZeroGPT and automatically rewrite it to bring the score below 70%, while preserving meaning and maintaining a professional, academic tone suitable for a learning journal.
metadata:
  display-name: Humanization
  enabled: "true"
  version: "1.0"
---

# Humanization

## When to Use

Activate when the user wants to:
- Check whether an essay will be flagged as AI-generated
- Reduce the AI-detection score of a piece of writing
- "Humanize" text for academic or journal submission
- Pass AI detection tools (ZeroGPT, GPTZero, etc.)

## Overview

This skill feeds an essay to **zerogpt.com**, reads the AI percentage score, and iteratively rewrites the essay until the score drops below **70%**. All rewrites preserve the original meaning and maintain a professional, academic tone appropriate for a learning journal — no casual language, no first-person storytelling, no informal phrasing.

---

## Steps

### Phase 1 — Get the Essay

1. If the user has pasted the essay directly in chat, use that text.
2. If the user references a file, use `filesystem_read` to load it.
3. Store the essay text as the **working draft**.

---

### Phase 2 — Check AI Score on ZeroGPT

1. Navigate to `https://www.zerogpt.com` using `navigate_page` on the current tab **or** a background tab if the user is on a page they want to keep.
2. Take a `take_snapshot` to locate the text input area.
3. Clear any existing content in the textarea, then `fill` it with the working draft.
4. Click the **Detect Text** (or equivalent submit) button.
5. Wait for the result to appear — use `take_snapshot` or `get_page_content` to read the AI percentage score.
6. Extract the numeric score (e.g. "82% AI-generated" → `82`).
7. Report the score to the user: _"ZeroGPT score: **82%** — above the 70% threshold. Beginning rewrite..."_

**If the score is already below 70%**, skip to Phase 4 (report success).

---

### Phase 3 — Rewrite Loop (score ≥ 70%)

Repeat the following loop up to **5 iterations**. Stop as soon as the score drops below 70%.

#### 3a. Rewrite the Essay

Apply the humanization strategies below to produce a revised draft. **Do not apply all strategies at once** — make targeted, incremental changes each round so the meaning is never distorted.

#### Humanization Strategies (apply progressively)

**Round 1 — Sentence-level variation**
- Break up long, uniform sentences into shorter ones, or combine short choppy ones into longer compound sentences.
- Vary sentence openings — avoid starting multiple sentences with the same word or structure.
- Replace overly smooth transitional phrases ("Furthermore,", "Additionally,", "In conclusion,") with more varied connectives or restructured paragraphs.

**Round 2 — Vocabulary naturalisation**
- Replace high-frequency AI vocabulary: "delve", "crucial", "leverage", "utilize", "it is important to note", "in the realm of", "showcasing", "underscoring", "shed light on", "tapestry", "landscape" → use plainer or more specific alternatives.
- Introduce minor lexical variety: synonyms, discipline-specific terminology, or concrete examples where the original was abstract.

**Round 3 — Structural reordering**
- Reorder supporting points within paragraphs (flip the order of two sub-arguments).
- Split one dense paragraph into two, or merge two thin paragraphs into one.
- Move a concluding sentence to the opening of its paragraph as a topic sentence (or vice versa).

**Round 4 — Hedging and epistemic language**
- Add appropriate academic hedging where claims are overly definitive: "suggests", "appears to", "may indicate", "tends to", rather than absolute assertions.
- Insert a brief acknowledgement of complexity or nuance where the text is too clean and declarative.

**Round 5 — Rhythm and voice refinement**
- Introduce one or two concrete, grounded examples or observations (e.g. referencing a specific course concept, a real scenario encountered, or a specific skill practised) to anchor abstract statements.
- Vary paragraph length — ensure not all paragraphs are the same number of sentences.

#### Tone Guardrails (must follow on every round)
- ❌ Do NOT use casual language ("kinda", "pretty much", "a lot", "stuff")
- ❌ Do NOT add personal anecdotes or first-person emotional statements unless already present in the original
- ❌ Do NOT change technical terms, defined concepts, or proper nouns
- ❌ Do NOT alter the core argument, thesis, or conclusions
- ✅ DO keep an academic, reflective register appropriate for a learning journal
- ✅ DO preserve all citations, references, and section headings if present

#### 3b. Re-check on ZeroGPT

1. Clear the ZeroGPT textarea.
2. `fill` it with the new draft.
3. Click **Detect Text** again and read the new score.
4. Report progress: _"Round 2 rewrite: ZeroGPT score now **61%** ✅ — below threshold."_

#### 3c. Decide

- If score < 70% → exit loop, proceed to Phase 4.
- If score ≥ 70% → apply next round of strategies, repeat.
- If 5 rounds are exhausted and score is still ≥ 70% → proceed to Phase 4 with the lowest-scoring draft and report the limitation.

---

### Phase 4 — Deliver Results

1. Present the **final rewritten essay** in full in the chat (or offer to save it to a file if it is long).
2. Show a summary table:

```
| Round | AI Score | Status        |
|-------|----------|---------------|
| 0     | 82%      | ❌ Too high   |
| 1     | 74%      | ❌ Too high   |
| 2     | 61%      | ✅ Passed     |
```

3. If the final score is still ≥ 70% after 5 rounds, be transparent:
   > "After 5 rewrite rounds, the lowest score achieved was **XX%**. The essay has been improved but further manual editing may be needed. The best version is provided below."

4. Optionally offer to save the result: "Would you like me to save the humanized essay to a file?"

---

## Error Handling

- **ZeroGPT is slow to load**: Wait and retry `take_snapshot` up to 3 times before reporting a timeout.
- **Score not found on page**: Use `get_page_content` to search for percentage text; fall back to `evaluate_script` to extract it from the DOM.
- **ZeroGPT blocks paste/fill**: Try `evaluate_script` to set the textarea value directly, then trigger an input event:
  ```js
  const ta = document.querySelector('textarea');
  const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
  nativeInputValueSetter.call(ta, `ESSAY_TEXT`);
  ta.dispatchEvent(new Event('input', { bubbles: true }));
  ```
- **Essay is very long (>3000 words)**: Warn the user that ZeroGPT has input limits. Offer to check the essay in sections and report an average score.

---

## Notes

- This skill works entirely through browser automation — no external APIs required.
- ZeroGPT's scoring can vary slightly between submissions; a score of 68–72% near the threshold may fluctuate. If the score is within 5% of the threshold, flag this to the user.
- The goal is to make the writing sound like a thoughtful human student wrote it — not to strip all structure, but to break the statistical patterns that AI detectors look for.
