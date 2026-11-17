---
name: product-video
description: Plan and generate short product and e-commerce videos with Makernice, such as product showcases, ad clips and marketplace listing videos. Covers choosing a mode, writing the prompt, picking aspect ratio and resolution, checking the price and running the job.
---

# Product video

Turn a product (ideally with a photo) into a short video clip. Reply in the user's language. All prices are in USD.

## 1. Collect the brief

Ask only for what is missing:

- **Product**: what it is, material, color, size, the one feature to show.
- **Product photo**: a public `https` link to a clean photo. Local files and private links do not work; the user has to host the image at a public https URL first.
- **Where it will be used**: this sets the aspect ratio.
  - TikTok, Reels, Shorts, stories: `9:16`
  - Website hero, YouTube, landing page: `16:9`
  - Marketplace listing, feed post: `1:1` (if the model offers it)
- **Length and budget**: most clips are 5 to 10 seconds. For a longer video, plan several short clips instead of one long one.

## 2. Pick model and mode

Call `list_models`, then call it again with `model` set to a candidate id to see its `modes`, `aspect_ratios`, `durations`, `options` and `max_prompt_chars`.

- **Photo available**: use an `i2v` mode with the photo as `image_url`. This keeps the real product's shape, label and color.
- **Several reference photos** (product from different angles): use an `r2v` mode if the model has one, with `reference_images`, within `max_references`.
- **No photo**: use a `t2v` mode and describe the product precisely.
- If a model lists `negative_prompt` in `options`, you may use it for things like "distorted label, extra parts, blurry".

## 3. Write the prompt

One clip, one shot. Build the prompt in this order:

1. **Subject**: the exact product, with material and color ("a matte black ceramic coffee mug with a cork base").
2. **Action or camera move**: one move only, for example slow push-in, smooth 360-degree orbit, top-down reveal, macro pan across the texture, hand picking it up.
3. **Setting and light**: surface, background, lighting ("on a light oak table, soft morning window light, shallow depth of field").
4. **Style and pace**: "clean commercial look, calm pacing".

Tips:

- Do not ask the model to render words, prices or logos as text; they often come out garbled. Add text later in an editor.
- With `i2v`, describe the motion and scene, not the product's look again; the photo already defines it.
- Stay under `max_prompt_chars`.

Example:

> A matte black ceramic coffee mug with a cork base on a light oak table, steam rising, the camera slowly pushes in, soft morning window light, shallow depth of field, clean commercial look, calm pacing.

## 4. Resolution and price

- Draft at `720p` first to check motion and framing; it costs less. Make the final at `1080p` for website, ads or large screens. `720p` is often enough for phone feeds.
- Call `estimate_cost` for the draft and the final options and show the user both prices before anything runs:

  ```json estimate_cost
  {"input": {"model": "<model id>", "mode": "i2v", "prompt": "A matte black ceramic coffee mug on a light oak table, steam rising, the camera slowly pushes in, soft morning light", "image_url": "https://example.com/mug.jpg", "duration": 5, "resolution": "720p", "aspect_ratio": "9:16"}}
  ```

## 5. Generate after the user agrees

Only call `generate` after the user has seen the price and said yes. If the user already set a budget and told you to go ahead, you may start without asking again as long as `amount_usd` is within that budget; still use `amount_usd`, not the budget, as `max_cost_usd`.

- `max_cost_usd`: required. Use the approved `amount_usd` from `estimate_cost`, exactly as returned. The job is refused if the price is higher.
- `request_id`: required and unique for every new job, printable ASCII with no spaces, at most 64 characters, for example `mug-orbit-720p-1`. A used id can never be reused for a different job.
- If `generate` fails with a network error, a timeout, a system error or "Too many requests", wait a few seconds and retry with the same `input`, the same `max_cost_usd` and the same `request_id`. The same id returns the same job and is never charged twice.

```json generate
{"input": {"model": "<model id>", "mode": "i2v", "prompt": "A matte black ceramic coffee mug on a light oak table, steam rising, the camera slowly pushes in, soft morning light", "image_url": "https://example.com/mug.jpg", "duration": 5, "resolution": "720p", "aspect_ratio": "9:16"}, "max_cost_usd": "<amount_usd from estimate_cost>", "request_id": "mug-orbit-720p-1"}
```

Wait with `check_job`, passing `job_id` and `wait_s` set to 55; if the job is still running, follow `next_step` and call again with `wait_s` 55. Do not poll in a tight loop.

On success, give the result link from `outputs` and the `console_url`. Links expire after 24 hours; `check_job` returns fresh ones. If an output has `state` `blocked` and no `url`, the safety review hid the result after it was generated; that job is still charged, and the user can contact Makernice to have it reviewed. Failed jobs are not charged; tell the user the reason from `error`.

For a multi-clip video, run one job per clip, each with its own `estimate_cost`, `max_cost_usd` and new `request_id`, and give the user the running total.

## Handling refusals

- **Price above `max_cost_usd`**: show the new price and ask before retrying with a new `max_cost_usd` and a new `request_id`.
- **Above the per-job limit**: suggest `720p` or a shorter duration, or the user can raise the per-job limit on Makernice.
- Not enough balance or daily limit reached: call `get_balance` and explain. If the `get_topup_link` tool is available and the user asks how to add balance, give the link once.
- Wrong settings on a queued job: `cancel_job` with its `job_id` releases the held amount in full.
