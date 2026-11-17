---
name: life-book-generator
description: Creates paid Life Book full-report Agent tasks, checks async status, and retrieves the generated 18-chapter report through the official Agent API. Use when a user wants to buy or generate a Life Book report from an Agent/Hermes-style chat.
version: 2.0.0
metadata:
  openclaw:
    primaryEnv: LIFE_BOOK_BASE_URL
    requires:
      env:
        - LIFE_BOOK_BASE_URL
      bins:
        - node
    envVars:
      - name: LIFE_BOOK_BASE_URL
        required: true
        description: Base URL of the deployed Life Book site, for example https://www.elife369.site
      - name: LIFE_BOOK_AGENT_API_KEY
        required: false
        description: Private integration key for controlled Agent task creation. Do not expose to end users.
      - name: LIFE_BOOK_TASK_TOKEN
        required: false
        description: Bearer token for an existing Agent report task.
      - name: LIFE_BOOK_TIMEOUT_MS
        required: false
        description: Optional timeout in milliseconds for HTTP requests. Defaults to 15000.
    emoji: "📘"
---

# Life Book Generator

Use this skill to create and deliver Life Book full-report tasks through the official Agent API.

The paid product is only the complete 18-chapter Life Book report:

- `lite`: 标准版, about 30,000 Chinese characters, CNY 69.9
- `pro`: 典藏版, about 100,000 Chinese characters, CNY 699

## What This Skill Can Do

1. Check whether the deployed Life Book service is healthy.
2. Collect and validate a complete `intake@1` payload.
3. Create a full-report Agent task through `/api/agent/report-tasks`.
4. Return payment information when the task is awaiting payment.
5. Submit manual payment confirmation after the user pays by WeChat, Alipay, or EVM.
6. Poll task status without using website cookies.
7. Retrieve the final report through the task bearer token when ready.

## Important Payment Boundary

Do not claim payment has succeeded unless the API returns a paid/queued/processing/ready task.

Current supported paths:

- If `LIFE_BOOK_AGENT_API_KEY` is configured by the platform operator, the skill can create a controlled paid Agent task and the report enters the generation queue.
- If no private key is configured, the task may return `awaiting_payment` plus payment details from the deployed payment provider.
- If the server returns `402 PAYMENT_REQUIRED`, explain that x402 payment verification is required and has not been completed in this chat yet.

Never fabricate OKX.AI, Hermes, x402, or external payment success.

## Required Environment

```bash
export LIFE_BOOK_BASE_URL="https://your-life-book-domain.com"
```

For controlled internal Agent integration:

```bash
export LIFE_BOOK_AGENT_API_KEY="..."
```

For existing tasks:

```bash
export LIFE_BOOK_TASK_TOKEN="lbat_..."
```

## Core Agent Workflow

### 1. Health Check

```bash
node scripts/check-health.mjs
```

Stop if health is not `ok`.

### 2. Collect Intake

Gather a complete payload matching `intake@1`. Use the example only as shape reference:

```bash
cat examples/intake.example.json
```

Verify:

- `displayName`
- `birth.localDate`, `birth.localTime`, `birth.timezone`, `birth.latitude`, `birth.longitude`
- `birth.accuracy`, `birth.dayBoundarySect`, `birth.sex`
- `primaryQuestion`
- `optionalQuestions` with at most 2 items
- full `tradeoffs`
- exactly 2 `lifeEvidence` items
- 2 to 6 `milestones`
- `consent: true`

### 3. Create Full-Report Task

```bash
node scripts/create-report-task.mjs \
  --input-file /absolute/path/to/intake.json \
  --edition lite \
  --idempotency-key user-unique-report-key
```

Use `--edition pro` for 典藏版.

The command returns:

- `task.id`
- `task.status`
- `access.token` when a new task is created
- `payment` details if payment is required
- status/result/stream endpoint URLs

If `access.token` is returned, keep it for later calls. It is returned once.

### 4. Handle Payment State

If `task.status` is `awaiting_payment`:

- Present `payment.manualPayment.options` when provider is `manual_qr`.
- For WeChat or Alipay, show the matching `qrCodeUrl`.
- For EVM, show both the `qrCodeUrl` and `walletAddress`.
- Tell the user generation starts only after the operator confirms receipt.

If HTTP status is `402`:

- Explain that x402 payment is required.
- Do not continue to result polling until payment has been verified by the official API.

### 5. Submit Manual Payment Confirmation

After the user says they have paid with one of the displayed manual channels:

```bash
node scripts/confirm-manual-payment.mjs \
  --task-id <taskId> \
  --task-token <taskToken> \
  --channel alipay
```

Use `--channel wechat` or `--channel evm` when appropriate.

This only marks the order as awaiting operator review. It does not auto-confirm receipt.

### 6. Check Task Status

```bash
node scripts/get-report-task.mjs \
  --task-id <taskId> \
  --task-token <taskToken>
```

### 7. Retrieve Result

```bash
node scripts/get-report-result.mjs \
  --task-id <taskId> \
  --task-token <taskToken>
```

This returns HTTP `202` with `result:null` until ready.

To wait until terminal state:

```bash
node scripts/wait-report-result.mjs \
  --task-id <taskId> \
  --task-token <taskToken> \
  --poll-ms 5000 \
  --max-wait-ms 3600000
```

## Website Checkout Fallback

If the Agent API is unavailable but the website remains healthy, the older website checkout scripts are still available:

- `create-intake.mjs`
- `create-order.mjs`
- `get-order.mjs`

Use them only as a fallback. They hand the user to the official website flow and do not return the full report directly in chat.

## Communication Rules

- Speak Chinese unless the user asks otherwise.
- Use `标准版` for `lite` and `典藏版` for `pro`.
- Be explicit about the current state: awaiting payment, queued, processing, ready, failed, or canceled.
- Never claim Hermes/OKX/x402 installation, listing, payment, or report readiness unless confirmed by real command/API output.
- Treat the official Agent API response as the source of truth.
