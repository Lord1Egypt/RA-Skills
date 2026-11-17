---
name: trend-remix
description: Turn the user's photos into a video using a Makernice trend template, a preset effect with a fixed model, motion and length. Use when the user wants a trending effect, a viral-style clip from a photo, or asks what templates are available.
---

# Trend remix

Apply a trend template to the user's own photos. Reply in the user's language. All prices are in USD.

## 1. Show the templates

Call `list_trends`. For each template you get its `id`, `duration_s`, the price per resolution in `prices`, the allowed `aspect_ratios`, and how many photos it needs in `images` (`min` to `max`). Templates do not include their prompt.

Show a short list (id, length, price at the default resolution, photos needed) and let the user choose. If they describe an effect, suggest the closest matching ids.

## 2. Get the photos

- Ask for public `https` links to the photos, between `images.min` and `images.max` of them. Local files and private links do not work; the user has to host the images at a public https URL first.
- Only use photos of the user or of adults who have agreed to it. Do not use photos of minors or of people who have not agreed.
- Clear, well-lit photos with the face or subject fully visible work best.

## 3. Options

- `resolution`: one of the resolutions in the template's `prices`. Leave it out for the default.
- `aspect_ratio`: one of the template's `aspect_ratios`. Leave it out to keep the template's original framing.
- `prompt`: optional. It replaces the template's preset prompt, so the result can drift away from the template's look. Only add it when the user asks for a change.

## 4. Check the price

Call `estimate_cost` with the exact request and show the user the `amount_usd`:

```json estimate_cost
{"input": {"template": "<template id from list_trends>", "images": ["https://example.com/photo.jpg"], "resolution": "720p"}}
```

## 5. Generate after the user agrees

Only call `generate` after the user has seen the price and said yes. If the user already set a budget and told you to go ahead, you may start without asking again as long as `amount_usd` is within that budget; still use `amount_usd`, not the budget, as `max_cost_usd`.

- `max_cost_usd`: required. Use the approved `amount_usd` from `estimate_cost`, exactly as returned. The job is refused if the price is higher.
- `request_id`: required and unique for every new job, printable ASCII with no spaces, at most 64 characters, for example `trend-<template id>-1`. A used id can never be reused for a different job.
- If `generate` fails with a network error, a timeout, a system error or "Too many requests", wait a few seconds and retry with the same `input`, the same `max_cost_usd` and the same `request_id`. The same id returns the same job and is never charged twice.

```json generate
{"input": {"template": "<template id from list_trends>", "images": ["https://example.com/photo.jpg"], "resolution": "720p"}, "max_cost_usd": "<amount_usd from estimate_cost>", "request_id": "trend-remix-1"}
```

Wait with `check_job`, passing `job_id` and `wait_s` set to 55; if the job is still running, follow `next_step` and call again with `wait_s` 55. After generating, jobs go through a short safety review before the result is available. Do not poll in a tight loop.

On success, give the result link from `outputs` and the `console_url`. Links expire after 24 hours; `check_job` returns fresh ones. If an output has `state` `blocked` and no `url`, the safety review hid the result after it was generated; that job is still charged, and the user can contact Makernice to have it reviewed. Jobs that fail, including ones whose photos or prompt are refused before generating, are not charged; tell the user the reason from `error`.

## Handling refusals

- The photo link cannot be fetched or is not an image: ask for another public https link.
- **Price above `max_cost_usd`**: show the new price and ask before retrying with a new `max_cost_usd` and a new `request_id`.
- **Above the per-job limit**: suggest a lower resolution, or the user can raise the per-job limit on Makernice.
- Not enough balance or daily limit reached: call `get_balance` and explain. If the `get_topup_link` tool is available and the user asks how to add balance, give the link once.
- Changed their mind while the job is queued: `cancel_job` with its `job_id` releases the held amount in full.
