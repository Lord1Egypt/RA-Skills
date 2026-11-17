---
name: pontx-amazon-sqs
description: Integrate Amazon SQS safely through Pontx. Use for queue discovery, direct SDK or CLI setup, consumer reliability, FIFO or standard queue decisions, visibility timeouts, DLQs, polling, and explicitly approved queue mutations.
---

# Amazon SQS

Use this skill for Amazon SQS integration and queue-safety decisions. Resolve
the live Endpoint, request, Schema, credential, and package details instead of
copying them into an application:

```bash
pontx-hub search "Amazon SQS <capability>" --type endpoint --json
pontx-hub show <returned-resource-id>
pontx-hub sdk amazon-sqs
```

Use `@pontx/amazon-sqs` for application code. Use `pontx-amazon-sqs` only for
an explicitly requested local script. Do not treat Hub discovery as an
execution path; configure the caller-owned AWS credentials and Region outside
source, shell history, inputs, logs, and chat.

## Choose queue and consumer semantics first

Amazon SQS standard queues use at-least-once delivery and best-effort ordering.
Make processing idempotent before retrying an ambiguous receive, send, delete,
or change. FIFO queues preserve message order and support exactly-once
processing. Confirm whether strict ordering is required and inspect the live
contract for the applicable FIFO grouping fields rather than inferring them.

Receiving a message makes it temporarily invisible to other consumers. If a
consumer does not delete a received message before its visibility timeout
expires, SQS can make it visible for another processing attempt. Choose a
timeout that matches the work, extend it deliberately when the current
contract permits, and delete only after durable processing succeeds.

Configure a dead-letter queue with a redrive policy to isolate messages that
are not processed successfully. Investigate the failure and retry policy before
moving messages back; do not purge a production queue to make an incident look
resolved.

Long polling reduces empty `ReceiveMessage` responses and can reduce cost. Use
the current Endpoint contract to set its wait behavior deliberately, then
measure application latency and queue metrics rather than assuming one polling
choice fits every workload.

## Preview every direct call

List the current locally supported actions and preview the exact input before
calling AWS:

```bash
pnpm exec pontx-amazon-sqs list apis
pnpm exec pontx-amazon-sqs preview <Action> --input '<verified-json>'
```

For every local CLI action, show the redacted preview and expected effect, then
obtain explicit approval for the unchanged input. Only then use the
confirmation token emitted by that preview:

```bash
pnpm exec pontx-amazon-sqs call <Action> --input '<same-json>' \
  --confirm '<preview-confirmation-token>' --region "$AWS_REGION"
```

If the action, queue, message receipt handle, body, region, or input changes,
discard the token and create a new preview. Do not reveal credentials, message
bodies, receipt handles, or confirmation tokens in code examples, diagnostics,
or chat.

## Few-shot workflows

### Scenario 1: Read queue topology

**User:** "Show the queues in our development Region, but do not change
anything."

**Approach:** Discover the current list Endpoint and SDK guidance, use a local
preview with an empty or live-contract-derived input, and ask for approval
before a direct AWS call. Return only the requested queue identifiers and keep
credentials out of output.

### Scenario 2: Build a reliable worker

**User:** "Write a consumer for our task queue."

**Approach:** Resolve the current receive/delete contract, decide standard or
FIFO semantics first, make handling idempotent, set the visibility timeout for
the work, delete only after durable success, and include DLQ and long-polling
decisions. Generate `@pontx/amazon-sqs` code only after the live SDK contract
is confirmed.

### Scenario 3: Send a production message

**User:** "Send this job to the production queue now."

**Approach:** Resolve the exact target and message requirements, create a
redacted local preview, explain the stateful effect, and stop for explicit
approval. Invoke the direct CLI only with the unchanged preview token and the
caller-owned AWS configuration.
