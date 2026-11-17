---
name: cost-planner
description: Plan which Makernice models, resolutions and durations fit a budget before generating anything. Use when the user gives a budget in USD, asks how many videos or images they can make, or wants to compare the price of options. Planning never creates jobs or charges anything.
---

# Cost planner

Build a plan that fits the user's budget. Reply in the user's language. All prices are in USD.

Planning only reads prices: use `list_models` to see the options and `estimate_cost` for every price you show. Do not call `generate` while planning.

## 1. Understand the goal

Ask only for what is missing:

- Total budget in USD.
- What they need: how many clips or images, how long each clip is, and where it will be used (this decides the resolution).
- Must-haves: a specific model, a minimum resolution, starting from a photo (`i2v`) or from text (`t2v`).

## 2. Shortlist options

Call `list_models`. Each mode lists its `prices` with `resolution`, `unit` (`second` or `request`) and `unit_price_usd`. Use these only to shortlist; for a candidate model, call `list_models` with `model` to see its allowed `durations` and `aspect_ratios`.

Shortlist a few combinations across price levels, for example a low-cost draft option, a balanced option and a high-quality option.

## 3. Price every line with estimate_cost

Call `estimate_cost` once per distinct combination, with the exact parameters that would be sent later:

```json estimate_cost
{"input": {"model": "<model id from list_models>", "mode": "t2v", "prompt": "Placeholder prompt for pricing", "duration": 5, "resolution": "720p"}}
```

The `amount_usd` it returns is the price per job. Never compute prices from memory or from older answers; `price_version` tells you which price list was used. Add up totals exactly from the returned amounts.

## 4. Present the plan

Show a table:

| Option | Model | Mode | Resolution | Duration | Price per job | Jobs | Total | Left over |
|---|---|---|---|---|---|---|---|---|

Then recommend one option in a sentence. Useful patterns:

- Draft at `720p`, then make only the chosen clips at `1080p`.
- Several short clips usually cost less than one long clip and are easier to redo.
- Leave some budget for one or two retakes; failed jobs are not charged, but clips the user does not like are, and so are outputs the safety review blocks.

If the user plans to run it, mention that each job must also fit the per-job limit and daily limit shown by `get_balance`.

## 5. If the user decides to run the plan

Before each job, call `estimate_cost` again with the final prompt and parameters, and get the user's yes on that price (or check it is within the budget the user already approved).

- `max_cost_usd`: required on every `generate` call. Use the approved `amount_usd`, exactly as returned. The job is refused if the price is higher.
- `request_id`: required and unique for every new job, printable ASCII with no spaces, at most 64 characters, for example `plan-clip-1`, `plan-clip-2`. A used id can never be reused for a different job.
- If `generate` fails with a network error, a timeout, a system error or "Too many requests", wait a few seconds and retry with the same `input`, the same `max_cost_usd` and the same `request_id`. The same id returns the same job and is never charged twice.

```json generate
{"input": {"model": "<model id>", "mode": "t2v", "prompt": "<final prompt>", "duration": 5, "resolution": "720p"}, "max_cost_usd": "<amount_usd from estimate_cost>", "request_id": "plan-clip-1"}
```

Wait for each job with `check_job`, passing `job_id` and `wait_s` set to 55; if it is still running, follow `next_step` and call again with `wait_s` 55. Keep a running total of `amount_usd` for the jobs that succeeded and compare it with the budget after each one. Succeeded jobs are charged even when the safety review hides an output (`state` `blocked`); failed or canceled jobs are not.
