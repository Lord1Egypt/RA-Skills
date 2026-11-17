# Request examples

Use actual authorized API IDs and options. These are payload templates, not
authorization to generate or a frozen model catalogue. Store sensitive JSON
files privately and never add LINK42_API_KEY to their content.

## Conversation and structured tools

Chat payload:
```json
{"model":"TEXT_MODEL","messages":[{"role":"system","content":"Return concise Chinese answers."},{"role":"user","content":"Explain a vector index."}],"max_tokens":1024,"stream":true}
```

When using functions, send supported tools as
`{"type":"function","function":{"name":"lookup_order","description":"Read an owned order","parameters":{"type":"object","properties":{"id":{"type":"string"}},"required":["id"]}}}`.
After a returned call, append the original assistant message with its tool_calls,
then `{"role":"tool","tool_call_id":"ORIGINAL_ID","content":"ACTUAL_RESULT_JSON"}`.
The host must actually authorize/execute lookup_order; this skill does not add it
to the platform. Preserve all native calls, IDs and prior results.

Responses uses `{"model":"TEXT_MODEL","input":[...],"store":false}`;
continue function calls with their original `call_id` and real
`{"type":"function_call_output","call_id":"...","output":"..."}` items.
Anthropic uses messages/max_tokens and native content blocks: append the
assistant's tool_use blocks, then user tool_result blocks with matching
`tool_use_id`. Gemini uses contents/parts and native functionCall/functionResponse
parts. Do not intermix protocol shapes or assume a stored response lifecycle.

## Images and video

An image request can use
`{"model":"IMAGE_MODEL","prompt":"A product photo in the agreed style","size":"2K","n":1}`
only when those options are supported. Reference edits may add a valid supported
`image` reference; use asset-upload for large originals instead of inlining them
in JSON. Preserve the actual generated task/result before requesting animation.

```json
{"model":"VIDEO_MODEL","content":[{"type":"text","text":"Keep the subject consistent; slow camera push."},{"type":"image_url","role":"first_frame","image_url":{"url":"asset://ACTUAL_ASSET_ID"}}],"duration":5,"resolution":"720p","ratio":"adaptive","generate_audio":false}
```

Use last_frame/reference_image/reference_video/reference_audio only when the
current model advertises those modes and limits. `-1` automatic duration needs
smart_duration. Treat output format, watermark, audio and final-frame options as
model-specific, not universal controls.

## Read-only planning

```json
{"operation":"image-create","model":"IMAGE_MODEL","request":{"prompt":"One agreed product image","size":"2K","n":1}}
```

Run `plan --json plan.json`. It returns the resolved request, quote and
`submitted:false`. For concrete independent stages, use
`{"stages":[...PLAN_OBJECTS...],"budget_usd":0.50}` with `workflow-plan`.
Future-stage reference IDs cannot be invented; plan those after obtaining actual
outputs. A successful quote is not upstream availability or final settlement.

## Usage and private uploads

Reserve manually with asset-begin JSON
`{"name":"reference.png","type":"image","content_type":"image/png","size_bytes":12345}` (replace with the actual byte count),
or prefer asset-upload --file /absolute/reference.png --execute for the complete
reservation/PUT/confirmation flow. If completion fails, resume asset-complete
with the same upload ID. Do not send LINK42 keys to signed storage URLs.

Usage filters: `{"group_by":"model","start":"2026-10-01T00:00:00Z","end":"2026-10-02T00:00:00Z"}`;
adapt the dates to the user's period. Score an owned request with
`{"request_id":"ACTUAL_REQUEST_ID","name":"helpful","value":1,"comment":"Verified result"}`.
Not every key enables usage-read; lack of permission is not permission to query
an administrator endpoint.
