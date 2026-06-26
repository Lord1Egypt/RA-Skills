# Huifu Payment Diagnostic Playbook

Use this reference when a user needs a more reliable and detailed Huifu/DouGong troubleshooting process.

The goal is to make another AI behave consistently: collect evidence, classify the issue, verify causes, and produce an actionable fix without inventing facts.

## Core Principle

Payment diagnosis is evidence work. Never jump directly from symptom to fix.

Every answer should connect:

```text
symptom -> evidence -> bucket -> likely cause -> verification -> fix -> prevention
```

Bad:

```text
签名失败一般是密钥错，你换一下密钥。
```

Good:

```text
这更像 signing。先确认当前 SDK/官方签名口径下参与签名的原文或规范串，再比对签名前后关键 payload/hash 是否一致；如果不一致，说明签名后内容被重序列化或改写。若一致，再核对 endpoint、商户私钥、汇付公钥是否来自同一环境。
```

## Standard Evidence Package

Ask for a standard evidence package when the diagnosis is uncertain.

```text
请贴一个标准联调证据包，敏感值打码：

1. 产品线：聚合支付 / 托管支付 / 前端收银台组件（checkout-js）
2. 当前步骤：初始化 / 下单或预下单 / 查单 / 关单 / 退款 / 对账 / 异步通知 / 前端拉起
3. 技术栈和 SDK 版本
4. 环境：测试 / 生产
5. 接口名、URL 或 SDK 方法
6. HTTP 状态码、响应码、响应信息
7. 请求头，至少保留 header 名和值是否为空
8. 请求体，密钥、手机号、证件号、token 打码
9. 本地订单号、`req_date`、`req_seq_id`、`hf_seq_id`、`huifu_id`、`project_id`，没有就写没有
10. 本地日志：签名前、发送前、响应后、落库后、回调处理后的关键几行
```

If webhook is involved, add:

```text
11. notify_url
12. 原始通知 body，不要贴解析后的重组 JSON
13. 通知 headers
14. 验签结果
15. handler 最终 HTTP status 和 response body
16. 重复通知第二次进入时的处理结果
```

If front-end cashier component (`checkout-js`) is involved, add:

```text
17. 服务端托管预下单是否成功
18. 传给浏览器的预下单结果字段，敏感值打码
19. JS SDK 版本
20. 浏览器 console 错误
21. 浏览器 network 失败请求
22. 前端 callback 结果和后端查单/异步通知结果
```

## Confidence Labels

Every diagnosis should include confidence.

### High Confidence

Use high confidence only when at least one direct proof exists:

- Actual response code/message points to a specific field or signing error.
- Request headers show a required header is missing.
- Signed payload/canonical string differs from the final sent payload under the current SDK/official signing path.
- Webhook handler returns non-200 or wrong success body.
- Query uses regenerated identifiers instead of persisted original identifiers.
- Browser console/network error directly identifies front-end cashier domain, SDK, or parameter issue.

### Medium Confidence

Use medium confidence when the symptom matches a strong pattern but one artifact is missing:

- front-end cashier callback succeeded but local order stayed pending, without webhook/query logs.
- Huifu retries notification, but final HTTP response body is not shown.
- Production fails but environment table is incomplete.
- Refund fails, but original transaction and refund request ids are not fully shown.

### Low Confidence

Use low confidence when route or evidence is incomplete:

- Product line unknown.
- Only screenshot/error summary is provided.
- No request/response payload.
- No SDK version.
- No order identifiers.

Low confidence answer should mostly ask for the next evidence, not provide a final fix.

## Decision Tree

Use this tree before deep analysis.

```text
1. Is the product line known?
   no -> hard checkpoint
   yes -> continue

2. Is the failure before Huifu accepts the request?
   yes -> check credential/environment, request-header, signing, order-create
   no -> continue

3. Is the failure in browser/cashier?
   yes -> check front-end cashier component and final-state
   no -> continue

4. Is the failure after payment action?
   yes -> check final-state, webhook, query-close, reconciliation
   no -> continue

5. Is it a refund or post-payment operation?
   yes -> check refund, query-close, reconciliation

6. Is the user asking whether this can go live?
   yes -> check production-readiness
```

## Error Code Handling

When a user gives an error code:

1. Preserve the exact code and message in the answer.
2. Do not paraphrase the code into a fake official meaning unless the relevant Huifu reference is loaded.
3. Classify whether it is:
   - transport error
   - authentication/signing error
   - request validation error
   - merchant configuration error
   - channel/business rule error
   - duplicate/uncertain transaction error
   - system/transient error
4. Ask for response body fields around the code if incomplete.
5. Route to the narrow reference:
   - aggregation order errors
   - aggregation query/close errors
   - aggregation refund errors
   - hostingpay preorder errors
   - hostingpay query/refund errors
   - shared signing/webhook references

Output pattern:

```text
错误码判断
你贴的错误码是：<code>，原始提示是：<message>。
我先不把它强行翻译成官方含义；当前证据显示它更像 <bucket>。
下一步要看 <reference> 或补 <field/log> 来确认。
```

## Logging Requirements

Recommend these logs during联调. Logs must redact secrets.

### Outbound Request Log

Required fields:

- `trace_id`
- `local_order_id`
- `product_line`
- `stage`
- `env`
- `sdk_name`
- `sdk_version`
- `api_name` or `func_code`
- `req_date`
- `req_seq_id`
- `huifu_id`
- `project_id`
- signed payload/canonical string hash before signing
- final outbound payload hash before sending, when applicable
- header names present, not secret values
- HTTP status
- Huifu response code/message
- `hf_seq_id` if returned
- latency

Never log:

- private key
- full certificate
- bearer token
- full card number
- full identity number
- raw password

### Webhook Log

Required fields:

- `trace_id`
- notification id if provided
- local matched order id
- raw body hash
- signature verification result
- parsed Huifu trade status
- local old status
- local new status
- idempotency result: first processed / duplicate ignored / duplicate returned success
- final HTTP status
- final response body category
- processing latency

### State Transition Log

Required fields:

- order id
- old local state
- new local state
- source: create response / query / webhook / reconciliation / manual repair
- reason
- operator or system job
- related Huifu sequence id

## Recommended Local Order State Machine

Use this model when diagnosing final-state, webhook, and reconciliation issues.

```text
created
  -> paying
  -> success
  -> failed
  -> closed

success
  -> refunding
  -> partially_refunded
  -> refunded

any uncertain state
  -> needs_query
  -> repaired_by_query
  -> repaired_by_reconciliation
```

Rules:

- `success` should not be overwritten by a later `pending` notification.
- Duplicate webhook should be idempotent and return success after verification.
- Unknown create/refund result should move to `needs_query`, not immediate failure.
- Manual repair should record source and operator.
- Reconciliation can correct local state but should not hide the original failure reason.

## Bucket Playbooks

### Signing Playbook

Ask:

- Which SDK or raw HTTP path?
- Which environment?
- Is this request signing or webhook verification?
- Is raw body available?
- Is the signed payload/canonical string consistent with the final outbound payload under this SDK path?

Verify:

1. Same environment key pair.
2. Same signed payload/canonical string according to the SDK/official signing path.
3. No JSON reserialization or business data mutation after signing.
4. No proxy/middleware body mutation.
5. Correct Huifu public key for webhook/response verification.
6. Correct merchant private key for request signing.

Most useful proof:

```text
signed_payload_sha256 == final_payload_sha256
```

If not equal under a raw-body signing path, the bug is local request construction. If the SDK signs a canonical string, compare the canonical string and the data fields it covers instead of assuming raw-body signing.

### Request Header Playbook

Ask:

- Are you using official SDK or custom HTTP?
- Show actual outgoing headers after SDK/proxy.
- Is `skill_source` configured?
- Does request data include `huifu_id`?

Verify:

- `jpt-x-skill-source` exists as HTTP header when configured.
- `jpt-x-skill-huifu_id` exists as HTTP header when non-empty `huifu_id` exists.
- Headers are not inside JSON `data`.
- Proxy keeps custom headers.

Fix:

- Official SDK: configure the SDK source field correctly.
- Custom HTTP: add required headers in HTTP layer.
- Gateway/proxy: allowlist these headers.

### Environment Playbook

Ask for an environment table:

```text
endpoint:
sys_id:
product_id:
huifu_id:
project_id:
merchant private key env:
Huifu public key env:
SDK version:
```

Verify all values belong to the same environment and merchant.

Common fixes:

- Replace sandbox public key in production config.
- Use production endpoint with production merchant id.
- Confirm product/channel permission was opened for this merchant/project.

### Webhook Playbook

Ask:

- Did Huifu reach the endpoint?
- What did handler return?
- Was verification done on raw body?
- What happens on duplicate notification?

Verify with a local replay if possible:

```text
first webhook call -> verify ok -> update state -> return success
second same call -> verify ok -> no duplicate side effect -> return success
```

Fix:

- Preserve raw body.
- Make handler idempotent.
- Return exact success status/body expected by current Huifu spec.
- Move slow side effects behind a queue or make them retry-safe.

### 前端收银台组件（checkout-js）Playbook

Ask:

- Did hostingpay preorder succeed?
- What exact fields are passed to browser?
- What browser SDK version?
- Browser console/network error?
- What server-side query/webhook says after callback?

Classify:

- Preorder failed -> not front-end cashier component issue.
- Preorder succeeded, browser fails -> SDK/domain/callback/field issue.
- Browser callback succeeds, backend pending -> final-state issue.

Fix:

- Do not expose secrets to browser.
- Pin SDK version.
- Align domain and callback config.
- Always confirm final state on server.

### Refund Playbook

Ask:

- Original successful payment identifiers.
- Refund request id.
- Refund amount and refundable amount.
- Whether this is first refund, retry, or refund query.
- Whether partial refund/split/subsidy is involved.

Verify:

- Original trade exists and is success.
- Refund id uniqueness is intentional.
- Amount is valid.
- Retry does not create a second refund.

Fix:

- Persist refund order before calling Huifu.
- Put uncertain refund into `needs_query`.
- Use refund query to resolve final status.

### Reconciliation Playbook

Ask:

- Statement date and type.
- Local order export for same business window.
- Whether refunds/fees/splits are included.

Classify differences:

```text
Huifu success, local missing
local success, Huifu missing
amount mismatch
status mismatch
fee mismatch
refund timing mismatch
duplicate local order
```

Fix:

- Generate difference table.
- Repair local status from confirmed Huifu source.
- Create recurring reconciliation job and alert threshold.

## Production Acceptance Checklist

Use this when the user asks whether the integration is reliable enough to上线.

Must pass:

- No private key or token in front-end code.
- No private key or token in repository.
- Secrets loaded from environment or secret manager.
- Request signing logs include hashes, not secrets.
- Order create is idempotent.
- Webhook is idempotent.
- Refund is idempotent.
- Front-end callback is not final success.
- Query or webhook final confirmation exists.
- Pending orders have scheduled补查.
- Reconciliation process exists.
- Duplicate notification returns success after safe verification.
- Unknown gateway result moves to query, not immediate fail.
- Alerts exist for webhook failure, high signing failure, success-rate drop, reconciliation mismatch.
- Manual repair leaves audit trail.

Do not say production ready if any of these are missing:

- final state confirmation
- webhook idempotency
- secret isolation
- refund idempotency
- basic reconciliation or repair plan

## Anti-Patterns

Call these out explicitly when seen:

- Trusting front-end cashier/browser callback as paid.
- Writing private key into JavaScript.
- Logging full request with identity/card/token/private key values.
- Regenerating `req_seq_id` for query/refund instead of using stored original id.
- Treating webhook duplicate as an error.
- Returning 500 after business duplicate-key exception even though order was already processed.
- Marking payment failed immediately after timeout instead of querying.
- Retrying refund with a new refund id after uncertain response.
- Mixing sandbox endpoint with production keys.
- Putting Huifu-required headers inside JSON body.
- Debugging business fields before proving signing input consistency.

## Final Answer Quality Bar

Before answering, check:

- Did I classify the bucket?
- Did I cite user-provided evidence?
- Did I label confidence?
- Did I give a verification step for each likely cause?
- Did I separate immediate fix, data repair, and prevention?
- Did I avoid asking for secrets?
- Did I avoid pretending front-end callback is final success?
- Did I route to only the necessary Huifu skill/reference?

If any answer is mostly generic advice, rewrite it with fields, logs, state transitions, or verification commands.
