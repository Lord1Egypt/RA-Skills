---
name: makernice-setup
description: First-run guide for the Makernice video and image tools. Use when the user has just connected Makernice, asks how it works, wants to check their balance and spending limits, or wants to make a first low-cost test video.
---

# Makernice setup

Help the user confirm the connection works, understand their balance and limits, and make one low-cost test video. Reply in the user's language. All prices are in USD.

## 1. Check the connection

Call `get_balance`.

- If the Makernice tools are not available, the connection is not set up yet. Tell the user to add the Makernice server (in Claude Code: run `/mcp`, choose `makernice`, then approve the connection on the Makernice page that opens in the browser). Stop here until it is connected.
- If the client reports that the connection is no longer valid (for example after it was removed on Makernice), ask the user to connect again the same way.

## 2. Explain balance and limits

Summarize the `get_balance` result in plain words:

| Field | What to tell the user |
|---|---|
| `available_usd` | Money that can be spent now. |
| `held_usd` | Money reserved by jobs still running. It is charged when a job succeeds and released if it fails or is canceled. |
| `spent_today_usd`, `daily_limit_usd`, `daily_remaining_usd` | Account spending today and the daily cap. The day resets at 00:00 UTC. |
| `per_job_limit_usd` | The most a single job may cost through this connection. More expensive jobs are refused. |
| `connection_spend_limit_usd`, `connection_spent_usd` | Total cap for this connection (null means no cap) and how much it has used. |
| `connection_daily_limit_usd`, `connection_spent_today_usd` | Daily cap for this connection (null means no cap) and how much it has used today. The day resets at 00:00 UTC. |

Failed jobs are not charged. If a finished output is blocked by the safety review for a policy violation, the job is still charged.

## 3. Find the lowest-cost test video

Do not quote prices from memory; prices change. Work them out:

1. Call `list_models` and look at video models with a `t2v` mode. For each, take the lowest `unit_price_usd`: when `unit` is `second`, multiply it by the model's minimum duration from `durations`; when `unit` is `request`, it is already the price of one job.
2. Pick the two or three lowest results and call `estimate_cost` for each with the exact parameters you would send, for example:

   ```json estimate_cost
   {"input": {"model": "<model id from list_models>", "mode": "t2v", "prompt": "A paper boat drifting on a calm lake at sunrise, gentle ripples, soft light", "duration": 5, "resolution": "720p"}}
   ```

3. Recommend the option with the lowest `amount_usd`. Show the user the model, resolution, duration and the exact `amount_usd`. If they only want to see that everything works, mention that a single image (a `t2i` mode) usually costs less than a video; check it with `estimate_cost` as well.

The test can only run if the price is within `available_usd`, `daily_remaining_usd` and `per_job_limit_usd`, and within what is left of `connection_spend_limit_usd` and `connection_daily_limit_usd` when they are not null. If not, explain which limit stops it. If the `get_topup_link` tool is available and the user asks how to add balance, give them the link it returns; mention it once and do not repeat it.

## 4. Run the test after the user agrees

Only call `generate` after the user has seen the price and said yes. If the user already set a budget and told you to go ahead, you may start without asking again as long as `amount_usd` is within that budget; still use `amount_usd`, not the budget, as `max_cost_usd`.

- `max_cost_usd`: required. Use the `amount_usd` the user approved, exactly as returned by `estimate_cost`. The job is refused if the price is higher.
- `request_id`: required and unique for every new job, printable ASCII with no spaces, at most 64 characters, for example `setup-test-boat-1`. A used id can never be reused for a different job.
- If `generate` fails with a network error, a timeout, a system error or "Too many requests", wait a few seconds and retry with the same `input`, the same `max_cost_usd` and the same `request_id`. The same id returns the same job and is never charged twice. Do not invent a new id for a retry.

```json generate
{"input": {"model": "<model id>", "mode": "t2v", "prompt": "A paper boat drifting on a calm lake at sunrise, gentle ripples, soft light", "duration": 5, "resolution": "720p"}, "max_cost_usd": "<amount_usd from estimate_cost>", "request_id": "setup-test-boat-1"}
```

Then wait for the result with `check_job`, passing `job_id` and `wait_s` set to 55. If it returns while the job is still running, follow `next_step` and call `check_job` again with `wait_s` 55. Do not poll in a tight loop with `wait_s` 0.

When the job succeeds, give the user the result link from `outputs` and the `console_url`. Links expire after 24 hours; calling `check_job` again returns fresh links. If an output has `state` `blocked` and no `url`, the safety review hid the result after it was generated; that job is still charged, and the user can contact Makernice to have it reviewed. If the job fails, tell the user the reason from `error` and that the held amount was released.

## Handling refusals

- **Price above `max_cost_usd`**: the price went above what the user approved. Show the new price and ask before retrying with a new `max_cost_usd` and a new `request_id`.
- **Above the per-job limit**: choose a cheaper option, or the user can raise the per-job limit on Makernice.
- Daily limit reached: the day resets at 00:00 UTC.
- To stop a job that is still queued, call `cancel_job` with its `job_id`; the held amount is released in full. Jobs that already started cannot be canceled.
