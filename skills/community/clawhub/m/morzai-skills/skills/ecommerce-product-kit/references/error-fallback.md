# Error Fallback

This guide defines the standard error levels, user-facing guidance, and fallback actions for the Morzai Ecommerce Product Kit. The goal is to keep multi-step ecommerce image generation predictable even when part of the workflow fails.

---

## General principles

- Classify the failure first, then decide whether execution can continue.
- Prefer actionable recovery guidance over raw technical errors.
- Only continue when the prerequisite step has clearly succeeded.
- If the full workflow cannot finish, deliver partial results, current status, or a clear next-step recommendation whenever possible.
- Never expose sensitive values such as full AKs, signed upload URLs, upload tokens, or cookies.

---

## L1: Input and local validation errors

### Definition
The user input is incomplete or the local input does not meet the minimum requirements to start execution.

### Typical cases
- No product image URL or local file path was provided
- The local file does not exist
- The file type is not supported
- The file header check fails
- Required fields such as `product_info`, `platform`, or `market` are missing
- Ratio, language, or platform values are malformed

### User-facing guidance
- Required input is missing, so generation cannot start yet.
- Please provide the product image, selling points, or platform settings and try again.
- The local image format or file contents are invalid. Please provide a JPG, JPEG, PNG, WEBP, or GIF image.

### Agent fallback actions
- Stop execution and do not continue to `style_create` or `render_submit`.
- Explicitly list the missing or invalid fields.
- If only a small amount of information is missing, ask a follow-up question instead of hard-failing immediately.
- If the problem is the local file, request a valid replacement image.

### Can execution continue?
**No.** L1 must be fixed first.

### Minimum deliverable
- A list of missing inputs
- A valid input example
- A clear next step for the user

---

## L2: Credentials and runtime environment errors

### Definition
The runtime environment does not meet the requirements to access the service, or authentication fails.

### Typical cases
- `morzai` CLI is not installed or not available on PATH
- CLI authentication is missing, expired, or unauthorized
- The CLI endpoint is missing or unreachable
- Required runtime commands are unavailable
- Environment configuration prevents requests from being sent correctly

### User-facing guidance
- The current environment is missing required credentials, so Morzai APIs cannot be called.
- Please install and authenticate the `morzai` CLI before running the skill.
- The current CLI credential may be invalid or unauthorized. Please rerun `morzai auth device-login` and verify access.

### Agent fallback actions
- Stop the workflow and do not continue to upload, polling, or rendering.
- State clearly whether the issue is missing CLI setup, expired authentication, or endpoint reachability.
- Provide the minimum required setup step, such as installing the CLI or rerunning device login.
- Never print the real AK or echo sensitive values in logs.

### Can execution continue?
**No.** L2 must be fixed first.

### Minimum deliverable
- A short explanation of the missing or failed environment condition
- The exact configuration action the user needs to take
- A minimal example command the user can rerun

---

## L3: Upload, network, and request failures

### Definition
The local input and environment are valid, but the request chain fails during upload or API communication.

### Typical cases
- Upload failure
- Network timeout
- DNS / TLS / HTTP request failure
- Non-expected HTTP error from the API
- Rate limiting or gateway rejection during the request chain

### User-facing guidance
- The image upload or API request failed before the final generation stage completed.
- This is usually caused by a temporary network issue, service instability, or a failed server-side request.
- You can retry later, or verify that your network and API key are working correctly.

### Agent fallback actions
- Stop the current step and avoid blind repeated retries.
- If the failure happened before upload completed, preserve the validated input parameters so the user can rerun the job later.
- If the server returned an interpretable error, translate it into a user-readable explanation.
- If style generation succeeded but render submission failed, preserve the style summary and explain exactly where the failure occurred.

### Can execution continue?
**Usually no.** Only continue if the failed step is truly independent from the next one, but stopping is the default behavior.

### Minimum deliverable
- The failed step name
- The steps that already succeeded
- Reusable input details or safe task/style metadata when helpful
- The recommended next action

---

## L4: Generation, polling, and response-structure failures

### Definition
The request was accepted, but generation or result parsing did not complete normally.

### Typical cases
- `style_create` returns an unexpected structure
- `style_poll` does not return usable output before timeout
- `render_submit` succeeds but `render_poll` times out
- The service returns an abnormal status that makes completion unclear
- The downloaded result is missing fields, image URLs, or expected schema structure

### User-facing guidance
- The task was submitted, but generation did not complete normally.
- Problems at this level usually happen during style generation, render polling, or response parsing.
- The final result cannot be confirmed as complete yet. Use the returned status to decide whether to retry.

### Agent fallback actions
- Clearly distinguish whether the failure happened in the style stage or render stage.
- Preserve partial outputs when available, such as style options, partial image URLs, or the created batch ID.
- If the issue is only a polling timeout, do not describe it as a confirmed hard failure; describe it as incomplete within the expected wait window.
- If the response shape is abnormal, return a safe summary of the state without exposing sensitive fields.

### Can execution continue?
- If the style stage fails: **No**, do not continue to render.
- If the render stage fails: **No**, do not continue to final download delivery, but partial status can still be delivered.

### Minimum deliverable
- The current workflow stage
- `task_id` / `batch_id` when safe and useful
- Any partial output that was successfully produced
- The recommended retry point

---

## L5: Partial delivery strategy after full-chain failure

### Definition
The full goal was not completed, but some useful intermediate output exists and should still be delivered.

### Deliverable candidates
- Validated platform / market / ratio configuration
- A cleaned selling-point summary
- Generated style options
- Partially downloaded images
- The known output directory path
- A reusable input JSON object for the next rerun

### User-facing guidance
- The full delivery did not complete, but some usable intermediate results are available.
- The current style, parameters, or partial image results have been preserved so you can continue from them later.

### Agent fallback actions
- Deliver reusable assets instead of only stating that the workflow failed.
- If some images downloaded successfully, state how many and where they were saved.
- If only the style phase succeeded, deliver the style summary and recommendation direction.
- If only the input preparation succeeded, deliver the structured input so the user can rerun quickly.

### Can execution continue?
L5 is not an execution stage. It is the final fallback strategy after the intended full workflow did not complete.

### Minimum deliverable
- A clear boundary between what succeeded and what failed
- Reusable intermediate output
- Saved paths or parameter summaries
- The recommended retry action

---

## Agent decision matrix

| Level | Continue execution? | Primary action | Main message to the user |
| :--- | :--- | :--- | :--- |
| L1 | No | Ask follow-up / fix input | What is missing and how to provide it |
| L2 | No | Stop and request environment setup | What configuration is missing |
| L3 | No | Stop the failed request and preserve context | Which request failed and how to retry |
| L4 | No | Preserve intermediate state and explain the broken stage | Where the task stalled and whether partial output exists |
| L5 | Not applicable | Deliver partial results | What succeeded, what failed, and how to continue |

---

## What `SKILL.md` should summarize

`SKILL.md` should at minimum explain:
- L1 = input and local validation problems
- L2 = credentials and runtime environment problems
- L3 = upload, network, and request failures
- L4 = style generation, polling, and response-structure failures
- L5 = partial-delivery strategy when the full chain does not complete

---

## What the script layer should expose

The script should produce structured error fields whenever possible, such as:
- `error_type`
- `message`
- `user_hint`
- `task_id` / `batch_id` / current stage when available

This allows the Agent layer to map failures reliably to the L1-L5 strategy in this reference.
