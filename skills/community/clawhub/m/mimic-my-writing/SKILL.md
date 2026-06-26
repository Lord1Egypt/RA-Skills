---
name: mimic-my-writing
description: Mimic my writing -- force AI to write like you do. Extract a quantitative voice fingerprint from sample text (sentence burstiness, vocabulary anchors, signature phrases, punctuation rate, quirks) and use it as a hard constraint when drafting. Use when the user asks to write in their voice, write like them, mimic a specific author, sound like a sample, match a writing style from examples, or de-AI a draft against a personal style. Also use when asked to grade how well a draft matches an author's voice.
---

# Mimic My Writing

Force any draft to sound like a specific human by extracting a measurable fingerprint from their samples and writing to those constraints. Stops the model from defaulting to LLM voice.

## Quick start

```bash
# 1. Drop the user's writing samples here (markdown or plain text)
samples/<author-slug>/

# 2. Extract the fingerprint
scripts/analyze_voice.py samples/<author-slug>/
```

The script prints a JSON report. Read it, then draft.

## The fingerprint, in one breath

The analyzer measures **rhythm** (sentence-length burstiness, fragment share), **vocabulary** (TTR, top content words, profanity rate, AI-filler hits), **punctuation** (em-dash, exclaim, semicolon rates), **contractions**, **signature 2- and 3-grams**, **sentence openers**, and **quirks** (all-caps emphasis, rhetorical Q+A, "fuck" as intensifier, etc).

Each metric maps to a concrete writing rule. See `references/fingerprint.md` for the translation table.

## Workflow

1. **Get samples.** Need 2-4 pieces, ~1k+ words total. Ask if not provided. Save under `samples/<author-slug>/`.
2. **Run the analyzer.** `scripts/analyze_voice.py samples/<author-slug>/`. Takes <1 second, stdlib only.
3. **Translate the JSON** using `references/fingerprint.md`. Write out the constraints (sentence rhythm targets, vocab anchors, must-use signature phrases, quirks to preserve).
4. **Draft** against those constraints.
5. **Self-audit** with `references/anti-ai-tells.md` -- rip out LLM defaults (delve, leverage, tricolon stacks, etc).
6. **Deliver.**

Detailed variants (cold mimic, warm mimic, hybrid voice, critique mode, sample organization) live in `references/workflow.md`.

## Non-negotiables

- **Never paraphrase signature phrases.** They're the author's verbal tics. Drop 2-3 of them into any mimic draft verbatim.
- **Match burstiness, don't average it.** If the author swings between 2-word fragments and 30-word runners, do the same. Don't write a uniform-length string of sentences.
- **Match the profanity rate.** Diluting it sanitizes the voice; inflating it caricatures. Within ±50% of the measured rate.
- **Reuse anchor words; do not synonym-cycle.** If the author says "call" 10x, you say "call" -- not "conversation, dialogue, exchange."
- **Honor every quirk** in the `quirks` array. They're flags for hard constraints, not suggestions.

## When to load which reference

- Translating JSON metrics into writing rules → `references/fingerprint.md`
- About to ship a draft, doing the AI-tell sweep → `references/anti-ai-tells.md`
- Edge case (no samples, hybrid topic, critique mode, sample layout) → `references/workflow.md`

## Failure modes to avoid

- **Mimicking the topic, not the voice.** If samples are about sales and the user asks for a poem, the rhythm/vocab quirks still apply. Topic ≠ voice.
- **Surface mimicry only.** Copying a few catchphrases without matching sentence rhythm reads like a bad SNL impression. Stats first, vocab second.
- **Bleeding authors.** If `samples/` has multiple authors, only analyze the requested one's folder. Don't mix fingerprints unless explicitly asked for a fusion.
- **Outdated samples.** If the user provides a new sample, drop it in and re-run the analyzer. Don't trust an old fingerprint from prior session memory.
- **Skipping the script.** Eyeballing samples and "writing in their voice" without the fingerprint is how you end up with delve+leverage soup. Run it every time.

## Example mini-fingerprint readout (Chad)

From `samples/chad/`:

- burstiness 0.82, fragment share 30%, long-sentence share 18% → swing hard between one-liners and 30+ word runs
- TTR 0.48 → moderate vocabulary; repeat anchor nouns
- profanity 7.7/1k words → curse freely; "fuck" as intensifier confirmed
- em-dash 8.7/1k chars → dashes are structural, not ornamental
- ALL-CAPS emphasis confirmed → use it on intensifier words (ENTIRE, MOMENT, NOT)
- Signature phrases: "ask for the money", "you can't", "that's the", "i've seen"
- Rhetorical question + self-answer → confirmed move

A draft that hits those numbers reads like Chad. One that doesn't reads like ChatGPT cosplaying Chad.
