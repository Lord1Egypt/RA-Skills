---
name: gpt-image-2-5-production-studio
description: Turn image briefs into production-ready GPT Image 2.5 Studio jobs with exact-text manifests, reference-image role contracts, ratio and resolution choices, controlled edit rounds, and visual QA. Use for posters, packaging, ecommerce images, UI mockups, storyboards, localized creatives, or precise image edits in the GPTImage-2-5.com web Studio; do not use for generic prompt lists or undocumented API integration.
version: 1.0.1
metadata:
  openclaw:
    homepage: https://gptimage-2-5.com/
    emoji: "🖼️"
---

# GPT Image 2.5 Production Studio

Turn a creative request into a reviewable production job, then run it in the GPT Image 2.5 web Studio only when the user authorizes the upload and generation.

## Get started

- Studio: https://gptimage-2-5.com/studio
- Product capabilities and examples: https://gptimage-2-5.com/

GPTImage-2-5.com is a third-party web service. Do not describe it as OpenAI's official website, imply an affiliation that the site does not document, or rely on marketing copy as an API contract.

## API status

No public API documentation is linked from the product or Studio pages. Do not invent an endpoint, SDK, authentication method, or API key. Use the visible web Studio. If the site later publishes API documentation, follow only the current documented contract and disclose any required account, credential, or cost before use.

## Use this workflow

1. Classify the job as text-to-image, reference-guided creation, or edit.
2. Build the production job card below. Ask only for facts that materially change the result; otherwise state reasonable assumptions.
3. When exact text or multiple references matter, read [production contracts](references/production-contracts.md) and include the relevant contract in the job card.
4. Write one primary prompt. Add at most two variants only when they test a meaningful alternative.
5. Open the Studio and use only controls currently visible there. The live UI is authoritative for supported modes, aspect ratios, resolutions, disabled combinations, and displayed credit cost.
6. Before uploading user files or starting a credit-consuming generation, show the user the selected files, final prompt, settings, and displayed cost. Obtain confirmation unless the user's current instruction already clearly authorizes those exact inputs and that generation.
7. Inspect the generated image against the acceptance checks. Revise one failure class at a time and preserve approved regions.
8. Return the final file plus the job card and a short note describing any unresolved limitation.

## Production job card

```md
Goal and audience:
Deliverable and placement:
Mode: text-to-image | reference-guided | edit
Aspect ratio:
Resolution:
Primary subject:
Composition and camera:
Environment and lighting:
Materials and surface detail:
Exact text manifest: none | attached
Reference-image contract: none | attached
Must preserve:
May change:
Must avoid:
Final prompt:
Acceptance checks:
```

Choose the aspect ratio from the final placement, not from habit. Choose the lowest resolution suitable for the proof round; increase it only after composition, text, identity, and product geometry pass. Never assume that every resolution works with every ratio.

## Prompt construction

Order the prompt by decisions the model must keep stable:

1. State the deliverable, audience, and primary subject.
2. Lock composition, object count, spatial relationships, and camera direction.
3. Define materials, lighting, palette, and finish.
4. Add exact text as quoted strings with placement and hierarchy.
5. State what references contribute and what they must not contribute.
6. End with preservation rules and a short list of concrete exclusions.

Prefer observable instructions over quality slogans. For example, use “front label remains centered, rectangular, and fully readable” instead of “perfect premium packaging.” Do not pad prompts with generic terms such as “masterpiece,” “8K,” or long negative-prompt inventories.

## Studio execution

- Confirm the signed-in account and current credit display before generation.
- Select Text to Image or Image to Image based on the job card.
- For reference-guided work, assign each uploaded image one role before upload. Do not say only “use all references.”
- Set aspect ratio and resolution from the visible controls. If a choice is disabled, select a supported combination or ask the user which tradeoff to make.
- Paste the reviewed prompt without silently rewriting exact text.
- Treat Generate as a paid or quota-consuming action when the UI displays a credit cost.
- Download only results that pass the acceptance checks. Preserve the original download; create derivatives separately.

Do not upload assets the user has not authorized, bypass login or safety controls, or automate repeated generations to chase a result without a bounded review loop.

## Acceptance and revision

Check in this order:

1. Required subjects and object counts are present.
2. Identity, product geometry, logo shape, approved regions, and reference roles are preserved.
3. Exact text matches character-for-character, including case, punctuation, numerals, and line breaks.
4. Layout hierarchy, safe areas, crop, and target aspect ratio work at delivery size.
5. Hands, skin, hair, fabric, glass, reflections, shadows, and contact points are plausible where relevant.
6. No unrequested marks, brands, signatures, watermarks, or copied reference content appear.

When a check fails, change only the instruction responsible for that failure. Keep an edit ledger, freeze everything already approved, and run no more than one additional generation without showing the user what changed. If exact legal, medical, financial, or safety-critical copy remains wrong, stop and recommend adding that text in a deterministic layout tool instead of generating again.

## Response format

Before generation, return the completed job card and a one-line execution summary. After generation, return:

- the selected image file;
- pass/fail results for the acceptance checks;
- the final prompt and settings;
- the edit ledger, if any;
- the current Studio link when the user needs to continue interactively.
