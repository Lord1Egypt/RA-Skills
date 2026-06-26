---
name: add-queue-publish-to-workflow
description: Insert a producer-side XADD into a workflow — appends a Queue Publish Execute Workflow node after the trigger.
user-invocable: false
---

# add-queue-publish-to-workflow

## When

A workflow needs to emit a durable message to a Redis Stream that another workflow (the consumer) will drain at its own pace, with backpressure + retry + optional DLQ. You're the producer side.

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/add_queue_publish_to_workflow.py \
  --workflow-key <wf> \
  --stream-expression "={{ 'orders' }}" \
  [--max-len 10000] \
  [--approximate | --no-approximate] \
  [--insertion-point auto|after-trigger|before-terminal|after-named-node:<name>|before-named-node:<name>]
```

## What it does to your template

Edits `<workspace>/n8n-workflows-template/<wf>.template.json`, splicing one `Execute Workflow` node named `Queue Publish` immediately after the trigger:

```
Trigger ──► Queue Publish ──► <your existing main flow>
```

- `Queue Publish` calls the `queue_publish` sub-workflow with `{ stream, payload, max_len, approximate }`. The whole input item is forwarded as `payload: ={{ $json }}`; the primitive JSON.stringifies it into a single Stream field.
- Downstream nodes are shifted right by 220 px.

Refuses if the queue primitives aren't yet in the workspace — run [`create-queue.md`](create-queue.md) first.

## Flag reference

### `--stream-expression "<n8n-expression>"`

The Redis Stream name. **Always use the canonical `={{ <expression> }}` form** for dynamic values — bare `=<expr>` (without `{{ }}`) is treated as a literal string, the helper auto-wraps with a deprecation warning.

For static streams: `={{ "orders" }}` or simply `orders` (the helper wraps it). For dynamic per-tenant: `={{ "orders-" + $json.tenantId }}`.

### `--max-len <int>`

Optional cap on stream length. When set, every XADD includes `MAXLEN ~ <n>` (approximate trimming, the cheap variant). With `--no-approximate`, uses exact `MAXLEN <n>`. Default: no cap (unbounded — operator must size DLQ retention separately).

### `--insertion-point`

Controls where in the existing workflow the Queue Publish node is spliced. Five modes:

- **`auto`** (default, aliases `after-trigger`) — splices Queue Publish immediately after the trigger. Best when you want every incoming item published verbatim with no preprocessing.
- **`after-trigger`** — same as `auto`.
- **`before-terminal`** — splices Queue Publish before the workflow's single terminal node. Errors out if there are multiple terminals (use `before-named-node:<name>` to disambiguate). Useful when the workflow does preprocessing/enrichment and you only want to publish the final value.
- **`after-named-node:<node-name>`** — splices Queue Publish immediately after the named node. The named node's first main output is rewired through Publish to its previous downstream. Use this when you want to publish a specific intermediate value (e.g. right after a "validate" or "transform" step).
- **`before-named-node:<node-name>`** — splices Queue Publish so all inbound edges to the named node flow through Publish first. Use when you want to capture the value about to enter a specific node.

The named-node modes are name-exact (n8n enforces unique node names); error cleanly if the name doesn't exist. Position math shifts the anchor's downstream right by 220 px; run [`tidy-workflow.md`](tidy-workflow.md) afterward if you want auto-layout cleanup.

## Worked example

```bash
# 1. Make sure queue primitives are in the workspace.
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/create_queue.py

# 2. Wrap a webhook receiver to publish into 'orders'.
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/add_queue_publish_to_workflow.py \
  --workflow-key order_intake \
  --stream-expression "={{ 'orders' }}" \
  --max-len 10000
```

The result on the wire:

```
Webhook → Queue Publish (stream=orders, payload=<full webhook json>, max_len=10000)
       → ... your existing nodes ...
```

The publish output (`{stream, message_id, published:true}`) becomes available downstream as `={{ $('Queue Publish').first().json.message_id }}` if you need to confirm the XID.

## Caveats

- **Not idempotent.** Each XADD creates a new XID; caller-retry produces duplicates. The consumer must dedupe at the application layer if exactly-once is required.
- **`payload` ends up JSON-stringified into a single Stream field** named `payload`, plus an `enqueued_at` field. Re-parse on the consumer side via `JSON.parse`.
- For static stream names, the static literal is auto-appended to every `<env>.yml.queueScopes`. For dynamic streams, you'll see a NOTE on stderr — manual `queueScopes` maintenance is required for the error handler to know about the stream.
