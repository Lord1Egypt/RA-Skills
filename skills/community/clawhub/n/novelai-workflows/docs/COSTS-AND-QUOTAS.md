# NovelAI Costs and Quotas

> Verified: 2026-09-06. This document describes NovelAI-side Anlas, Opus free-image conditions, and the V5 usage allowance. It is not a pricing contract. Official rules, the client UI, and account state may change; use the current UI or an available cost-estimation tool before generating.

## 1. Three different resources

### Anlas (image credits)

Anlas is NovelAI's main credit system for image generation. The current official subscription documentation says that subscribed users receive unlimited Text and Text to Speech, while other resource-intensive features primarily use Image Anlas.

The Opus subscription includes 10,000 Subscription Anlas per month; Tablet and Scroll include 1,000 each. Subscription Anlas refill with the subscription cycle. Paid Anlas are purchased separately and are normally used after the subscription-side balance is depleted.

### The Opus V5 free-generation allowance

Opus also has a separate, rechargeable Usage Limit for free V5 image generation. It is not Anlas and it is not a fixed number of images granted at midnight every day.

When the free conditions are met, a V5 generation uses this allowance instead of Anlas. Once the allowance is empty, generation can continue by using Subscription Anlas or Paid Anlas.

### OpenClaw and other model costs

Story planning, prompt rewriting, and context assembly may be performed by the text model selected in OpenClaw. If that model comes from OpenAI, Anthropic, DeepSeek, or another metered provider, its charges are separate from NovelAI Anlas. This Skill does not add a separate fee.

## 2. Operations that do not consume NovelAI Anlas

The following operations do not generate an image and therefore do not consume NovelAI Anlas by themselves:

| Operation | Notes |
| --- | --- |
| NovelAI text generation | Unlimited within an active subscription; model access still depends on the tier |
| NovelAI Text to Speech | Unlimited within an active subscription |
| Story-project initialization, context assembly, and chapter planning | Local file operations or text-model calls, not image credits |
| `get_subscription`, `get_user_data` | Read-only account queries |
| `estimate_anlas_cost` | Estimates cost without executing a generation |
| `suggest_tags` | Tag suggestions without image generation |
| Prompts, negative prompts, seeds, tags, and quality tags | No separate fee; they affect the enclosing image request |
| `annotate_image` | A preprocessing step such as ControlNet annotation; a later image generation is still billed by its own rules |

“No Anlas” does not mean “no model cost”: a text provider may be metered, and a free V5 image still uses the separate Usage Limit.

## 2.1 Session billing profiles and transient retries

After a successful account/cost verification, the main Skill may keep a redacted billing profile in memory for the current conversation. It may reuse that profile indefinitely when the operation type, model, dimensions, Steps, image count, sampler/scale/noise, base image, mask, reference, Vibe, and Director operation remain unchanged. A new conversation, restart, parameter change, account warning, tool error, ambiguous processing result, or explicit recheck request invalidates it.

Each user-requested image operation may retry a clearly transient failure up to 3 times after the initial attempt, sequentially and with identical parameters. Do not retry parameter, authentication, billing, account, Usage Limit, or ambiguous failures.

## 3. Opus free-image conditions

An Opus basic free image must satisfy all of these conditions:

1. Use an eligible subscription and model;
2. Generate one image at a time;
3. Stay within the normal resolution range;
4. Use 28 Steps or fewer;
5. Do not use another image as a base image.

The official subscription page also uses the phrase “Normal Sized,” while the FAQ summarizes the rule as normal resolution. Do not infer free billing solely from a UI label such as “Small”; let the current client or cost estimator show `0 Anlas` before executing.

### V4.5 and earlier models

The official documentation says that image models before V5 are not subject to the V5 Usage Limit and can continue to be used without that V5 cap when the usual free conditions are met. Higher resolution, more than 28 Steps, batches, and extra features can still consume Anlas.

### V5

When the free conditions are met, V5 uses the separate Opus Usage Limit. The account UI dynamically shows the remaining percentage, an estimated number of standard-image equivalents, and the refill speed.

Some accounts or periods may show approximately 11% per day, or approximately 190 images per day. This is an example of the current UI refill rate, not a fixed daily grant. The allowance refills continuously, and actual image equivalents depend on resolution, Steps, and current service rules. The official announcement says a completely empty allowance takes about a week to recharge.

## 4. Live results from the reference Opus account

The following results came from real API tests on 2026-09-06 using an active Opus account. Requests used normal dimensions and one image. Subscription Anlas, Paid Anlas, and the V5 Usage Limit were queried before and after each operation. Charged items were repeated with paired pre/post samples using the shared token; no external balance drift was observed during those retests.

| Operation | Observed result | Notes |
| --- | --- | --- |
| Single V5 / V4.5 text-to-image | 0 Anlas | 8 and 28 Steps, normal dimensions |
| V4.5 img2img | 0 Anlas | 8 and 28 Steps, normal dimensions; account-specific evidence |
| V4.5 inpainting | 0 Anlas | 8 and 28 Steps, normal dimensions; account-specific evidence |
| Generation with an already encoded V4/V4.5 Vibe | 0 Anlas | New Vibe encoding is separate and charged |
| `annotate_image` | 0 Anlas | ControlNet preprocessing test |
| Director lineart, sketch, declutter, colorize, emotion | 0 Anlas | Normal-size source image |
| Director background removal | 65 Anlas | Observed account charge |
| Vibe encoding | 2 Anlas | V4+ one-time encoding charge; re-encoding charges again |
| Two images in one request | 8 Anlas | Observed account charge |
| 1536x1024 single image | 12 Anlas | Observed account charge |
| 29-Step single image | 20 Anlas | Observed account charge |
| Dedicated upscale | No image | Current `/ai/upscale` returned 404 |
| Enhance and Precise Reference | Not tested | Not exposed as independent tools by the reference MCP |

These are empirical results for one account, one MCP version, and concrete parameters, not a permanent NovelAI pricing promise. Img2img, inpainting, and the free Director subset were zero in this test, but must still be estimated and followed by a balance audit on every use.

## 5. Operations that consume Anlas or require confirmation

| Skill operation or parameter | Anlas rule |
| --- | --- |
| Basic `generate_image` | Charged for non-Opus accounts or when the free conditions are not met; V5 is also charged after its free allowance is empty |
| Multiple images in one request | Always costs Anlas, even for Opus; more images increase the cost |
| Higher resolution | Normally costs Anlas |
| More than 28 Steps | Normally costs Anlas |
| `image_to_image` with a base image | Zero in the tested Opus parameters; official conditions are more conservative, so require an exact estimate and balance audit |
| Ordinary `inpaint` | Zero in the tested Opus parameters; other sizes, models, or settings may charge |
| Focused Inpainting | The official docs explicitly say that Opus can inpaint regions of large images at zero Anlas; still follow the current tool estimate |
| `enhance` | Runs the image through NovelAI Diffusion again; treat it as another potentially charged image operation |
| `encode_vibe` | V4+ encoding costs 2 Anlas once; re-encoding after changing Information Extracted costs again |
| Vibe generation | The base image request rules still apply; for V4+ each Vibe beyond the first four adds 2 Anlas |
| Precise Reference | The official docs charge an additional 5 Anlas per reference image, per generation; currently V4.5 only |
| `director_tool` | Lineart, sketch, declutter, colorize, and emotion were zero in the test; background removal charged 65, and other operations are not automatically free |
| `annotate_image` | Zero in the ControlNet preprocessing test; a later image generation is still billed by its own rules |
| `upscale_image` | The reference environment's dedicated `/ai/upscale` route currently returns 404 and produces no successful image; if it returns, estimate first |

Multi-character prompts, character positions, seeds, samplers, negative prompts, and ordinary tags do not add a separate fee; their cost belongs to the enclosing image request.

## 6. Variant policies

- `openclaw-novelai-free`: the strictest variant; it allows only the narrowest image path with an explicit zero estimate and does not allow img2img, inpainting, or Director tools.
- `openclaw-novelai-opus-free`: requires active Opus, normal dimensions, one image, 28 Steps or fewer, an explicit zero estimate, and a post-operation balance audit. It allows the tested-free img2img, inpainting, pre-encoded Vibe generation, annotation, and selected Director tools.
- Both variants block Vibe encoding, background removal, Precise Reference, Enhance, dedicated upscaling, batches, high resolution, and more than 28 Steps.

## 7. Safe operating pattern

Before any image output, ask the agent to do this:

```text
First query my NovelAI subscription and balance, then estimate the Anlas cost with the current tool.
Show the model, dimensions, Steps, image count, reference/Vibe count, and estimated cost.
If the estimate is not 0 Anlas, do not execute until I confirm.
```

For a free-condition V5 image:

```text
Use V5 at a normal resolution, 28 Steps, one image, and no base image.
Tell me whether the current estimate is 0 Anlas first; if it is not 0, do not generate.
```

For Vibe, inpainting, Director, Enhance, or batch work, do not say only “try it for free.” Explicitly request a cost estimate first.

## 8. Quick reference

- Text and TTS: no NovelAI Anlas within an active subscription.
- Queries, estimates, tag suggestions, and local records: no Anlas.
- Opus + one image + normal size + no more than 28 Steps: may be 0 Anlas; img2img and inpainting require the current estimate and balance audit.
- V5 at 0 Anlas: it still consumes the separate Usage Limit.
- Batches, higher resolution, more than 28 Steps, Vibe encoding, references, background removal, and second-pass processing: treat as charged or unverified.

## 9. Official references

- [NovelAI Subscription](https://docs.novelai.net/en/subscription/)
- [NovelAI FAQ — Opus Usage Limits](https://docs.novelai.net/en/faq/)
- [NovelAI Image Generation](https://docs.novelai.net/en/image/)
- [Steps & Prompt Guidance](https://docs.novelai.net/en/image/stepsguidance/)
- [Vibe Transfer](https://docs.novelai.net/en/image/vibetransfer/)
- [Inpaint](https://docs.novelai.net/en/image/inpaint/)
- [Precise Reference](https://docs.novelai.net/en/image/precisereference/)
- [Director Tools](https://docs.novelai.net/en/image/directortools/)
- [NovelAI official Usage Limit announcement](https://blog.novelai.net/subscription-updates-usage-limits-2025-88a208d5d9c5)
