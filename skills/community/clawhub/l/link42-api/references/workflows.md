# Capability map and workflows

## Choose by the requested outcome

| Outcome | Transport/operation | What must be verified |
|---|---|---|
| Writing, translation, analysis, code, structured JSON | chat / responses / messages / gemini | Authorized text model, context/output limits, reasoning/JSON support |
| Multi-turn conversation | Native messages/input history | Preserve roles, previous outputs, tool IDs and reasoning blocks; trim only with consent/clear disclosure |
| Image/video understanding | Vision-capable text transport | Supported input parts and URLs/inline limits; generation support is not understanding support |
| Tool/function calling | Native tools and tool results | Model advertises tools; execute only host tools within user intent; return results with original IDs |
| Embeddings/retrieval | embeddings | An enabled embedding model, dimensions/encoding; retrieval needs the host's index, not an invented platform database |
| Text-to-image, image sets | image / image-create | Model sizes, pixel range, count/sequential policy and total expected cost |
| Reference-image edit | image-edit or generation with image references | Reference format/limits and model editing support; JSON only, no multipart/mask promise |
| Text-to-video | video-create | Duration/resolution/ratio/audio/output format from video_options |
| First/last-frame video | video-create with image_url roles | Correct first_frame/last_frame roles; some first-frame models require adaptive ratio |
| Multimodal reference video | image/video/audio reference roles | Per-type and total count/duration limits; sound/reference modes vary by model |
| Video editing/extension | Supported reference_video/edit/extend roles | Existing source, actual mode contract and authorization; do not invent endpoint names |
| Private reference upload | asset-begin / asset-upload / asset-complete | Owner/type/size/quota; storage PUT carries no LINK42 authorization header |
| Resume/cancel tasks | image-get/wait, video-get/list/wait/cancel | Existing ID/ownership, bounded timeout; cancellation only on request |
| Cost reporting and evaluation | usage-report/logs/csv, score | Key usage-read permission; account-wide reporting can reveal other keys' spend, exports stay private |
| Planning/diagnostics | discover / doctor / estimate / plan / workflow-plan | Read-only scope/quote checks; not provider execution/health proof |

## Writing, vision and structured output

Carry the user's language, requested format and relevant conversation context.
Use the selected protocol's supported JSON schema/format when available, then
validate the returned object. Do not invent missing data or describe unexecuted
tools as finished. For understanding, use supported text/image/video content
parts; a PDF/file must be read/extracted by an authorized host tool unless the
chosen route explicitly supports that native file input. Keep private documents
and signed URLs out of public logs.

## Tool-driven work

Treat tool calls as requests, not execution authority. Compare each request with
the user's task and the host's permissions. Preserve native call IDs and append
the actual result in the protocol's format. Do not drop sibling tool calls or
replay already-executed mutations after a model/transport error. Stop on missing
authority or repeated non-actionable failures; ask for the missing input. A model
request for browser searches or filesystem execution requires a real permitted
host tool—LINK42 does not manufacture hosted browsing/code execution.

## Image → video creative chain

1. Establish subject/style, target ratio, duration, outputs and overall budget.
2. Discover and select text/image/video models separately; capabilities differ.
3. Plan and quote the first concrete stage. Preserve reference identity in its
   prompt rather than inventing uploaded assets or completed images.
4. Create only the authorized stage, persist IDs and stable idempotency key, and
   wait/query the same task. Inspect the actual result and storage status.
5. For the next stage, use the actual owned asset/result in supported roles,
   re-check options and cost. Future-stage budgets are estimates until real
   inputs exist. The key's server-side budget is the hard protection.
6. Return actual results, request/task IDs and billing state. Local timeout keeps
   the task recoverable; expiring media is re-queried, not regenerated.

Image batches depend on the model's count/sequential policy. Multiple videos are
separate paid tasks with separate stable keys; do not assume `n`. Do not process
a whole folder or retry paid submissions without corresponding user scope.

## Transport and failure diagnosis

CLI `--request-options private-options.json` accepts SDK `timeout`, `headers`
and `request_id` without exposing command-line secrets. Use cost tags such as
`X-OneRelay-Tags: project:poster,env:test` or supported organization context;
never override Authorization/X-API-Key/Host or weaken TLS. Paid operations force
zero automatic retries. Budget-protected operations lacking a supported quote
fail closed; use server-side key budgets and explicit scope instead of claiming
an unverified cost cap. Scope/token/IP/account availability and provider health
are separate. `doctor` establishes discovery, not that every upstream will run.

No customer key grants administrator settings, other users' data, wallet
recharges/refunds or reseller assignment. Audio API, Realtime, Batch, multipart
image edits and hosted tools remain outside the current implementation, even if
a video can contain sound or a host can execute its own tools.
