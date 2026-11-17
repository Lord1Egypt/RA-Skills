# Zero-Anlas Mode: Costs and Quotas

## Goal

This variant aims to **avoid NovelAI Image Anlas**.

It does not promise that every service is free, nor does it provide unlimited images. It only allows image requests that the current tool explicitly estimates at `0 Anlas`.

## Allowed operations

| Operation | Policy |
| --- | --- |
| Fiction outline, continuation, rewrite, review, and summary | Allowed; no image credits |
| Local story-file reading and organization | Allowed |
| Account and subscription queries | Allowed; read-only |
| Anlas cost estimation | Allowed; estimate only |
| Tag suggestions | Allowed; no image generation |
| Prompt, negative prompt, seed, and scene planning | Allowed; preparation only |
| One image generation | Allowed only after an explicit `0 Anlas` estimate |

## Required conditions for an image

All conditions must hold:

1. The account has Opus or another explicitly documented free-image entitlement;
2. The active MCP exposes `estimate_anlas_cost`;
3. The final parameters are sent to the estimator first;
4. The estimator returns an explicit numeric `0 Anlas` result;
5. Exactly one image is generated;
6. The resolution is within the normal range;
7. Steps are 28 or fewer;
8. There is no base image, mask, reference image, Vibe, Precise Reference, Director, Enhance, or upscale operation;
9. There is no batch, parallel generation, or parallel retry. After the first successful gate, the same conversation may reuse the verified billing profile indefinitely while billing-affecting parameters remain unchanged. A transient failure may be retried sequentially up to 3 times after the initial attempt; ambiguous or billing-related failures are not retried automatically.

If any condition is not met, the image tool must not be called.

## Explicitly blocked

- img2img;
- ordinary inpainting and outpainting;
- Vibe encoding and Vibe generation;
- Precise Reference;
- Director tools;
- Enhance;
- dedicated upscaling;
- multiple images, multiple samples, or parallel generation;
- any paid fallback.

## V5 special case

Even when a V5 request estimates at `0 Anlas`, it consumes the separate Opus Usage Limit. That allowance recharges over time; it is not unlimited and is not a fixed daily image grant.

## Recommended request

```text
First query my NovelAI account and inspect the current tool schema.
Use V5, normal resolution, 28 Steps, one image, and no base image.
Estimate the cost first; generate only if the explicit result is 0 Anlas.
```

## Use the advanced variant for paid features

For img2img, inpainting, Vibe, Director, references, batches, or high-resolution work, use the parent project's advanced `openclaw-novelai` Skill. This zero-Anlas variant never spends credits to finish a request.

## Official references

- [NovelAI Subscription](https://docs.novelai.net/en/subscription/)
- [NovelAI FAQ — Opus Usage Limits](https://docs.novelai.net/en/faq/)
- [Steps & Prompt Guidance](https://docs.novelai.net/en/image/stepsguidance/)
- [NovelAI Image Generation](https://docs.novelai.net/en/image/)
