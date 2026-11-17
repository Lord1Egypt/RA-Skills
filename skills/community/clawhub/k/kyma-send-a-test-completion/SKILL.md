---
name: send-a-test-completion
description: Run one real, billed chat completion through Kyma API with the user's explicit approval and report back the output and what it cost. Use when the user asks to test a model, check that a model actually answers, compare two models on the same prompt, or says something like "reply with pong via <model>".
---

# Send a test completion through Kyma API

`send_message` is the only billed tool in this plugin. It runs a real completion against a real model and charges the account.

## When to use

- "Test <model>." / "Does <model> actually work?"
- "Ask <model> to reply with pong."
- "Run this prompt through <model A> and <model B> and compare."

## The approval rule

- `send_message` requires `allow=true`. Never pass it without the user's go-ahead in this conversation.
- Ask once, in plain terms: which model, the exact prompt, and roughly what it will cost. Then wait.
- Without an Allow there is no charge and no call. Silence is not approval, and neither is an earlier "yes" to a different prompt or a different model.
- One approval covers one call. A second model, a retry, or a longer prompt needs a fresh ask.

## Steps

1. Confirm the model id with `get_model` if the user gave a friendly name or an alias, so you bill the model they meant.
2. Check the budget first — `get_credits` and `get_spend` — and say the remaining amount out loud. See the check-spend-and-credits skill.
3. Show the user the exact model id and prompt you are about to send, with a cost estimate from `list_pricing` for that model.
4. On their explicit go-ahead, call `send_message` with `allow=true`. Keep `max_tokens` small for a smoke test; a "reply with pong" check does not need a long ceiling.
5. Report the model's reply verbatim, then the actual cost from the response, then the remaining budget.

## Comparing models

Run the same prompt against each model as separate approved calls, with the same `max_tokens`. Put the replies side by side with each one's cost and latency. Do not judge a model on a single short completion — say what the sample does and does not show.

## Do not

- Do not use `send_message` for work the user did not ask to be billed for, such as summarizing, checking a fact, or reformatting something.
- Do not retry a failed call automatically. Report the failure and ask.
- Do not attribute a model's reply to any inference backend. Report the model id that answered and nothing about where it ran.
