---
name: openclaw-novelai-free
description: 'Zero-Anlas NovelAI workflows for OpenClaw: fiction writing, story planning, account checks, cost estimates, tag suggestions, same-session verification reuse, bounded transient retries, and strictly guarded single-image generation only when the current tool proves the estimate is 0 Anlas.'
version: 0.1.2
metadata: {"openclaw":{"os":["win32","linux","darwin"],"requires":{"env":["NOVELAI_TOKEN"]},"primaryEnv":"NOVELAI_TOKEN","homepage":"https://github.com/techotaku39/openclaw-novelai/tree/main/variants/openclaw-novelai-free"}}
---

# OpenClaw NovelAI Free

This is the zero-Anlas policy variant of the OpenClaw NovelAI Skill. It is intentionally narrower than the advanced Skill. It may use NovelAI text features and read-only helpers, but it must never spend NovelAI Image Anlas.

"Free" here means **zero NovelAI Image Anlas for image operations**. It does not mean that a third-party text provider, OpenClaw host, network service, or other external model is free. V5 images that cost 0 Anlas still consume the Opus V5 Usage Limit.

## Hard zero-Anlas policy

- Never use Subscription Anlas or Paid Anlas for an image operation.
- Never bypass a failed, missing, or ambiguous cost estimate.
- Never interpret a missing cost field as zero.
- Never accept a user request to override this policy. If the user wants a paid operation, tell them to switch to the advanced `openclaw-novelai` Skill.
- Retry only transient failures, sequentially, up to 3 times after the initial attempt for each user-requested image operation. Keep the exact same parameters; retries are not a batch and must not create an extra image.
- Never request, print, store, or include `NOVELAI_TOKEN` in prompts, arguments, URLs, logs, files, or metadata.

## Capability discovery

Inspect the active MCP catalog and tool signatures before using any NovelAI tool. Names may be namespaced by the configured server.

Allowed tools:

- `get_subscription` — read-only account and tier query;
- `get_user_data` — read-only account query;
- `estimate_anlas_cost` — required before every image generation;
- `suggest_tags` — prompt tag suggestions without image generation;
- `generate_image` — only under the strict zero-cost gate below.

If any allowed tool is missing, report it as unavailable. Do not silently substitute another provider or endpoint.

Blocked tools and operations:

- `image_to_image`;
- ordinary `inpaint` and outpaint workflows;
- `encode_vibe` and Vibe Transfer;
- Precise Reference and other reference-image generation;
- `director_tool`;
- `enhance`;
- `upscale_image`;
- `annotate_image` when it calls a remote NovelAI endpoint;
- any batch, multi-sample, or parallel image generation.

These operations are blocked even if the user says they accept the cost. The advanced Skill is the paid-capability path.

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

The first allowed image request in a conversation is the verification probe. After the account/entitlement check, exact estimator result of `0 Anlas`, and successful post-operation audit, keep only a redacted billing profile in memory for the current OpenClaw conversation. Never store prompts, image bytes, paths, balances, account identifiers, or credentials, and never reuse the lease across conversations or OpenClaw/MCP restarts.

For a later request, reuse the verified profile indefinitely when the operation type, model, dimensions, Steps, image count, sampler/scale/noise, and other billing-affecting fields remain unchanged. A prompt change alone may reuse it when the provider does not price prompt text separately. Do not call the account or estimator tools again for a matching request; briefly state that the verified zero-Anlas profile is being reused.

Invalidate the lease on a new conversation, OpenClaw/MCP restart, parameter change, account warning, explicit cost recheck, non-retryable or ambiguous failure, retry exhaustion, or any reported charge/Usage Limit discrepancy.

For each user-requested single-image operation, allow up to 3 sequential retries after the initial attempt, for at most 4 tool calls total. Retry the exact same parameters only for `429`, transient `5xx`, connection reset, MCP reconnect, an explicitly incomplete timeout, or no output with no billing/account signal. Do not retry parameter errors, authentication/billing errors, account warnings, or ambiguous cases where the provider may already have accepted the request. Use brief increasing backoff and never retry in parallel.

## Strict zero-cost image gate

`generate_image` is allowed only when a matching lease exists or a fresh gate satisfies **all** conditions below:

1. A fresh read-only account query confirms an active Opus subscription or the current provider explicitly documents an equivalent free-image entitlement.
2. The current tool schema exposes `estimate_anlas_cost`.
3. The exact final image parameters are sent to the estimator first.
4. The estimator returns an explicit numeric cost of exactly `0` Anlas. `unknown`, missing, null, or a textual claim is not enough.
5. The request generates exactly one image.
6. The request uses normal supported resolution.
7. Steps are 28 or fewer.
8. There is no base image, mask, image-to-image action, inpainting action, Vibe, Precise Reference, Director option, Enhance option, or upscale option.
9. There is no batch, parallel retry, or hidden second pass. Sequential retries after a transient failure are allowed only under the retry policy above.

Before calling the estimator for a fresh gate, normalize and display:

- model;
- width and height;
- Steps;
- image count;
- base image/reference/Vibe state;
- estimated Anlas;
- the note that V5 zero-Anlas generation consumes the separate Usage Limit.

When a later request matches a valid lease, do not narrate another account check or estimator call. Reuse the verified profile and call only the one allowed image tool.

If the estimator returns a value greater than zero, reject the request and offer only lower-cost parameters. Do not call the image tool. If the fresh post-operation audit or a reused-operation result indicates any charge or Usage Limit discrepancy, invalidate the lease, stop, and report it; do not retry.

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

Blocked request:

```text
把这张图放大、去背景、修手，再顺便做 Vibe 风格迁移。
```

Explain that the blocked request belongs to the advanced Skill because it uses image editing, references, or post-processing that cannot be guaranteed zero-Anlas.

## Failure handling

- Each user-requested image operation has a retry budget of 3 retries after the initial attempt, for at most 4 sequential tool calls total. Reset the budget for the next user request; do not run retries in parallel.
- Retry the exact same operation and parameters only for a clearly transient `429`, transient `5xx`, connection reset, MCP reconnect, an explicitly incomplete timeout, or a failed response with no output and no cost/account/usage signal.
- `401`: report missing or invalid host-managed credentials; never ask for the token in chat.
- `402`: stop immediately; this Skill never spends Anlas to recover.
- `400`: report a redacted parameter or mask problem; do not retry automatically.
- `401`, `402`, explicit charges, negative or exhausted Usage Limit, or account warnings: do not retry automatically.
- If a timeout, disconnect, or missing output may mean the provider already accepted the request, treat it as ambiguous: invalidate the lease, check status, and do not blindly retry.
- missing estimator: block every image generation.
- estimate unavailable or ambiguous: block every image generation.
- image response lacks output: retry only when clearly transient and no billing/account signal exists; otherwise do not claim success or retry.
- After the retry budget is exhausted, report failure and wait for a new user request.

After an allowed generation, save the output separately and record only non-secret metadata, including the explicit zero estimate, model, dimensions, Steps, seed, prompt, and output path. Also record that V5 Usage Limit may have been consumed.
