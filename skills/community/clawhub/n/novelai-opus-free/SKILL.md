---
name: openclaw-novelai-opus-free
description: 'Opus zero-Anlas NovelAI workflows for OpenClaw: fiction writing, cost-aware single-image generation, img2img, inpainting, pre-encoded Vibe use, annotation, selected free Director tools, and same-session verification reuse with strict account and balance guards.'
version: 0.2.3
metadata: {"openclaw":{"os":["win32","linux","darwin"],"requires":{"env":["NOVELAI_TOKEN"]},"primaryEnv":"NOVELAI_TOKEN","homepage":"https://github.com/techotaku39/openclaw-novelai/tree/main/variants/openclaw-novelai-opus-free"}}
---

# OpenClaw NovelAI Opus Free

This is the Opus-focused zero-Anlas enhancement variant of the OpenClaw NovelAI Skill. It is narrower than the advanced Skill, but includes image operations tested as zero Anlas under normal-size parameters.

"Free" here means **zero NovelAI Image Anlas for image operations**. It does not mean that a third-party text provider, OpenClaw host, network service, or other external model is free. V5 images that cost 0 Anlas still consume the Opus V5 Usage Limit.

## Hard zero-Anlas policy

- Require an active Opus account (`tier=3`) before establishing a lease in a new session or after the lease is invalidated.
- Never use Subscription Anlas or Paid Anlas for an image operation.
- Never bypass a failed, missing, or ambiguous cost estimate.
- Never interpret a missing cost field as zero.
- Never accept a user request to override this policy. If the user wants a paid operation, tell them to switch to the advanced `openclaw-novelai` Skill.
- Retry only transient failures, sequentially, up to 3 times after the initial attempt for each user-requested image operation. Keep the exact same parameters; retries are not a batch and must not create an extra image.
- Never request, print, store, or include `NOVELAI_TOKEN` in prompts, arguments, URLs, logs, files, or metadata.
- After a fresh verification probe succeeds, a valid session lease may suppress duplicate account and estimator calls under the rules below. If a post-operation response reports a non-zero cost, an account warning, or any ambiguity, invalidate the lease and stop further image operations.

## Capability discovery

Inspect the active MCP catalog and tool signatures before using any NovelAI tool. Names may be namespaced by the configured server.

Allowed tools:

- `get_subscription` — read-only account and tier query;
- `get_user_data` — read-only account query;
- `estimate_anlas_cost` — required before the first image generation for each new or changed billing profile; reuse is allowed only under the session lease below;
- `suggest_tags` — prompt tag suggestions without image generation;
- `generate_image` — text-to-image and pre-encoded Vibe generation under the strict zero-cost gate below;
- `image_to_image` — only under the strict zero-cost gate below;
- `inpaint` — only under the strict zero-cost gate below;
- `annotate_image` — ControlNet preprocessing;
- `director_tool` — only `lineart`, `sketch`, `declutter`, `colorize`, and `emotion` on normal-size inputs.

If any allowed tool is missing, report it as unavailable. Do not silently substitute another provider or endpoint.

Blocked tools and operations:

- `encode_vibe` — encoding costs Anlas;
- Precise Reference and other reference-image generation;
- `director_tool` with `bg-removal` or any unknown operation;
- `enhance`;
- `upscale_image`;
- any batch, multi-sample, or parallel image generation.

These operations are blocked even if the user says they accept the cost. The advanced Skill is the paid-capability path.

## Tested-free Opus enhancement operations

The following operations were tested on the reference Opus account at `832x1216` and at 8 or 28 Steps with no Subscription Anlas decrease:

- single text-to-image;
- single `image_to_image`;
- single `inpaint`;
- generation using an already encoded V4/V4.5 Vibe;
- `annotate_image` preprocessing;
- Director `lineart`, `sketch`, `declutter`, `colorize`, and `emotion`.

These are empirical compatibility results, not a permanent provider promise. Do not encode a new Vibe in this mode. Do not use Director background removal: the reference test charged 65 Anlas for it.

## Read-only and text workflows

The following are permitted because they do not spend NovelAI Image Anlas:

- outline, continue, rewrite, review, and summarize fiction;
- read and organize `canon.md`, `memory.md`, `lorebook.md`, `style.md`, chapters, and local asset metadata;
- draft prompts, negative prompts, scene lists, and character sheets without sending an image request;
- query subscription and account data;
- estimate an image request without executing it;
- request tag suggestions;
- record local project state and generation plans without credentials.

NovelAI text generation is separate from Image Anlas. It is normally unlimited for an active subscription, but an OpenClaw deployment may route text through another provider with its own billing. Tell the user when the text provider is not NovelAI.

Prefer bounded context and continuation-style prompts for NovelAI text models. Do not assume that the selected text model behaves like a general instruction-following chat model.

## Session-scoped zero-cost verification lease

The account query and cost estimate are expensive in latency and do not need to be repeated for every image when the billing profile has not changed. Maintain the lease only as in-memory state in the current OpenClaw conversation. Never write the lease, account response, balance, or token to a file, memory database, prompt, or generation metadata, and never reuse it across conversations or OpenClaw/MCP restarts.

### Establishing a lease

The first image-producing request for a profile is the verification probe. Run the complete gate below, generate only after it passes, and query the account after the successful operation. Create a lease only when the post-operation audit shows no Subscription Anlas or Paid Anlas decrease and no account or usage warning.

Store only a redacted billing profile and the current session/restart context:

- operation type (`generate_image`, `image_to_image`, `inpaint`, pre-encoded Vibe generation, `annotate_image`, or the specific allowed Director operation);
- model, width, height, Steps, image count, sampler/scale/noise fields when present;
- whether a base image, mask, reference, or already encoded V4/V4.5 Vibe is used, plus their billing-relevant dimensions/counts.

Do not store prompts, image bytes, paths, account identifiers, balances, or credentials in the lease.

### Reusing a lease

For a later request in the same conversation, first compare the request with the stored billing profile:

- A prompt or negative-prompt change alone may reuse the lease for ordinary text-to-image if the current estimator schema does not price prompt text; all billing-affecting fields must remain unchanged.
- Any change to operation type, model, dimensions, Steps, image count, sampler/scale/noise, base image, mask, reference, Vibe count/version, Director operation, or any unknown cost-affecting field invalidates the lease and requires a fresh exact estimate.
- The lease has no time limit and no reuse-count limit. It remains valid throughout the current session while the billing profile is unchanged. For V5, do not proactively refresh solely because a free image consumes the separate Usage Limit; invalidate the lease only if the provider reports Usage Limit exhaustion, an account warning, a cost, or another error.
- While the lease is valid, do not call `get_subscription`, `get_user_data`, or `estimate_anlas_cost` again. Show a short note that the previously verified zero-Anlas billing profile is being reused, then perform exactly one allowed image operation.
- After a reused operation, inspect the tool result for explicit cost, account, usage, or error signals. Do not run a duplicate post-operation account query while the lease remains valid. An absent billing field by itself is normal and does not invalidate the lease; invalidate it immediately only when the result explicitly reports a non-zero cost, balance decrease, negative or exhausted usage, an account warning, an error, or an inconsistency.

### Mandatory lease invalidation

Invalidate the lease and run a fresh gate when a new conversation starts, OpenClaw or MCP restarts, any billing-affecting parameter changes, a non-retryable or ambiguous operation failure occurs, retry attempts are exhausted, a `401`, `402`, `429`, or account warning occurs, the user explicitly asks to verify the current cost, or the user says the account tier, Opus subscription, Usage Limit, or Anlas state changed. A retryable transient failure does not invalidate a matching lease while the retry budget remains.

## Strict zero-cost image gate

Any image-producing operation is allowed only when either a valid session lease matches, or a fresh gate satisfies **all** conditions below. A valid lease is a reuse of a completed gate; it is not permission to change any billing-affecting parameter.

1. A fresh read-only account query confirms `tier=3` and an active Opus subscription.
2. The current tool schema exposes `estimate_anlas_cost`.
3. The exact final billing-affecting image parameters are sent to the estimator first.
4. The estimator returns an explicit numeric cost of exactly `0` Anlas and, when available, `opus_free_sample=true`. `unknown`, missing, null, or a textual claim is not enough.
5. The request generates exactly one image.
6. The request uses normal supported resolution; keep the pixel area at or below `1024x1024` equivalent.
7. Steps are 28 or fewer.
8. For V5, the fresh account response has a usable `usage` field, `isNegative` is false, and the remaining Usage Limit is positive.
9. There is no batch, parallel retry, or hidden second pass. Sequential retries after a transient failure are allowed only under the retry policy below.

Additional operation-specific rules:

- `image_to_image` and `inpaint` require the exact final image and mask parameters in the estimator request.
- Vibe generation may use only already encoded V4/V4.5 Vibes, at most four, and must never call `encode_vibe`.
- Director is limited to `lineart`, `sketch`, `declutter`, `colorize`, and `emotion` on normal-size source images. `bg-removal` is always blocked.
- Precise Reference, Enhance, and dedicated upscaling are always blocked.

Before calling the estimator for a fresh gate, normalize and display:

- model;
- width and height;
- Steps;
- image count;
- base image/reference/Vibe state;
- estimated Anlas;
- the note that V5 zero-Anlas generation consumes the separate Usage Limit.

When a later request matches a valid lease, do not narrate another account check or estimator call. Briefly state that the previously verified zero-Anlas billing profile is being reused, then call the one allowed image tool directly. If the request does not match, explain which billing-affecting field changed and run a fresh gate.

If the estimator returns a value greater than zero, reject the request and offer only lower-cost parameters. Do not call the image tool. If the fresh post-operation audit or a reused-operation result indicates the estimate was wrong or the account balance decreases, invalidate the lease, stop, and report the discrepancy; do not retry.

The user may explicitly request a zero-cost image, but the Skill must still run the gate. A natural-language instruction such as "小图免费生成" never overrides the gate.

## Safe examples

Allowed planning request:

```text
读取第三章，找出适合配图的场景，只输出场景列表、Prompt 和不收费的生成方案，不要生成图片。
```

Allowed guarded image request:

```text
使用 V5，正常分辨率，28 steps，一次一张，不使用底图。
先查询账户并用当前工具估算费用；只有明确显示 0 Anlas 才生成，否则不要执行。
```

Allowed Opus enhancement request:

```text
使用当前已有图片做图生图或局部重绘。
先确认我是 Opus，检查 Usage Limit，并用估算工具确认最终参数为 0 Anlas。
只生成一张，正常分辨率，最多 28 steps；如果余额发生变化，立即停止后续图片操作。
```

Blocked request:

```text
把这张图放大、去背景、修手，再顺便做 Vibe 风格迁移。
```

Explain that the blocked request belongs to the advanced Skill because it uses a paid or unverified operation: new Vibe encoding, background removal, Precise Reference, Enhance, upscale, batch, or high-resolution generation.

## Failure handling

- Each user-requested image operation has a retry budget of 3 retries after the initial attempt, for at most 4 sequential tool calls total. Reset the budget for the next user request; do not run retries in parallel.
- Retry the exact same operation and parameters only when the provider or MCP clearly reports a transient failure: HTTP `429`, transient `5xx`, connection reset, MCP reconnect, a timeout explicitly reported before request completion, or a failed response with no output and no cost, account, or usage signal.
- Use brief increasing backoff between retries. Never change the model, dimensions, Steps, image count, prompt, base image, mask, Vibe, or Director operation to make a retry succeed.
- `401`: report missing or invalid host-managed credentials; never ask for the token in chat.
- `402`: stop immediately; this Skill never spends Anlas to recover.
- `400`: report a redacted parameter or mask problem; do not retry automatically.
- `401`, `402`, explicit non-zero cost, balance decrease, negative or exhausted Usage Limit, or an account warning: do not retry automatically.
- If a timeout, disconnect, or missing output may mean the provider already accepted the request, treat it as ambiguous: invalidate the lease, check account/usage status, and do not blindly retry.
- missing estimator: block every image generation.
- estimate unavailable or ambiguous: block every image generation.
- account balance changed after an image operation: stop further image operations and report the provider/MCP mismatch.
- image response lacks output: retry only when the failure is clearly transient and no billing/account signal exists; otherwise do not claim success or retry.
- After the retry budget is exhausted, report the operation as failed and wait for a new user request; do not continue retrying automatically.

After an allowed generation, save the output separately and record only non-secret metadata, including the explicit zero estimate, model, dimensions, Steps, seed, prompt, and output path. Also record that V5 Usage Limit may have been consumed.
