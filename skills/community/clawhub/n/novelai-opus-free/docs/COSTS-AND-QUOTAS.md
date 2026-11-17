# Opus Free Enhancement Mode: Costs and Quotas

## Goal

This variant aims to **avoid NovelAI Image Anlas for an active Opus account** while allowing image operations tested as zero Anlas under normal-size parameters.

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
| One text-to-image, img2img, or inpaint request | Allowed only for Opus after an explicit `0 Anlas` estimate |
| Generation with an already encoded Vibe | Allowed for V4/V4.5 within the same zero-cost gate; Vibe encoding itself is blocked |
| Annotation | Allowed as preprocessing |
| Director lineart, sketch, declutter, colorize, and emotion | Allowed for normal-size inputs based on the tested MCP behavior |

## Required conditions for an image

All conditions must hold:

1. The account has an active Opus subscription;
2. The active MCP exposes `estimate_anlas_cost`;
3. The final parameters are sent to the estimator first;
4. The estimator returns an explicit numeric `0 Anlas` result;
5. Exactly one image is generated;
6. The resolution is within the normal range (keep the area at or below a 1024x1024 equivalent);
7. Steps are 28 or fewer;
8. Img2img/inpaint may use a base image or mask only when the exact estimator returns zero; Vibe may use only existing encoded V4/V4.5 references; Director is limited to the five tested tools and excludes background removal;
9. There is no batch, parallel generation, or parallel retry. A transient failure may be retried sequentially up to 3 times after the initial attempt, with the exact same parameters; ambiguous or billing-related failures are not retried automatically.

If any condition is not met, the image tool must not be called. After the first successful gate and balance audit, the same conversation may reuse the verified billing profile indefinitely while billing-affecting parameters remain unchanged. Do not repeat account or estimator calls for a matching request. Invalidate the session lease on a new conversation, OpenClaw/MCP restart, parameter change, tool error, account warning, explicit cost recheck request, or any reported Anlas/Usage Limit discrepancy.

## Explicitly blocked

- new Vibe encoding;
- Precise Reference;
- Director background removal;
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

For new Vibe encoding, background removal, Precise Reference, Enhance, dedicated upscaling, batches, or high-resolution work, use the parent project's advanced `openclaw-novelai` Skill. This mode stops if its post-operation balance audit detects a charge.

## Official references

- [NovelAI Subscription](https://docs.novelai.net/en/subscription/)
- [NovelAI FAQ — Opus Usage Limits](https://docs.novelai.net/en/faq/)
- [Steps & Prompt Guidance](https://docs.novelai.net/en/image/stepsguidance/)
- [NovelAI Image Generation](https://docs.novelai.net/en/image/)
