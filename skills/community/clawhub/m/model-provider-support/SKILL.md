---
name: model-provider-support
description: "Answer official-doc-grounded support questions about Claude, OpenAI/GPT, and Gemini model availability across Bedrock, Vertex AI, Azure, OpenAI, and Gemini API."
---

# Model Provider Support

Use when answering team questions about Claude, GPT/OpenAI, or Gemini API/model support across cloud-hosted providers.

## Rules

- Treat each provider-hosted model as its own product surface.
- Do not infer cloud provider support from first-party model docs, or first-party support from cloud provider docs.
- Cite official provider documentation for the exact surface being discussed.
- If docs conflict or are stale, say so and prefer the hosting provider's current docs for hosted availability.
- Mark unverified capabilities as `unknown_needs_live_check`; do not guess.

## Workflow

1. Identify model family, hosting provider, region, API surface, and capability.
2. Load `references/source-registry.json` and the relevant provider notes.
3. Check `references/capability-taxonomy.md` for status labels.
4. Apply `references/provider-differences.md` before answering.
5. If live docs cannot be reached, cite registry URL and access notes, then answer conservatively.

## Validation

Run `node scripts/check-sources.mjs` after editing registry entries.
