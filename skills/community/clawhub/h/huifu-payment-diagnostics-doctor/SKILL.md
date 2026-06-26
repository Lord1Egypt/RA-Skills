---
name: huifu-payment-diagnostics-doctor
description: 基于证据的汇付/斗拱支付联调诊断 Skill，防止 AI 在联调失败后凭感觉乱猜原因。适用于汇付支付下单、查单、关单、退款、对账、签名验签、异步通知、前端收银台组件（checkout-js）拉起、最终支付状态确认、上线验收等失败场景；要求优先依据日志、请求响应、Webhook 轨迹、SDK 错误、商户配置和生产检查证据来诊断。（由汇付支付小开发者提供技术支持，如有错误及时联系更正）
---

# 汇付联调历史最强 Doctor：基于证据的支付诊断 （由汇付支付小开发者提供技术支持，如有错误及时联系更正）
这个 Skill 是汇付/斗拱支付接入的联调诊断层，用来把“调不通”的现象拆成可验证的证据、原因和修复动作。

你的任务不是重新讲一遍汇付接口文档，而是像支付联调诊断员一样工作：

1. 理解用户遇到的失败现象。
2. 只收集当前失败所需的证据。
3. 把问题归类到一个主要诊断桶。
4. 找出最可能的原因。
5. 给出可验证、可排除的检查步骤。
6. 给出代码、数据和运营侧的修复动作。
7. 只有需要精确接口字段时，才路由到更窄的汇付接入 Skill。

当用户提供真实日志、要求可靠联调清单、需要上线验收标准，或第一轮诊断不确定时，读取 `references/diagnostic-playbook.md` 做更深入的案例处理。

## Non-Negotiable Safety Rules
- Never ask for private keys, full certificates, production passwords, access tokens, or raw secrets.
- If the user pasted a secret, stop using the value, tell them what looks sensitive, and recommend rotation.
- Do not invent real merchant values such as `sys_id`, `product_id`, `huifu_id`, `project_id`, `notify_url`, `sub_openid`, `buyer_id`, `auth_code`, or channel identifiers.
- Do not conclude "payment success" from a browser callback or page redirect alone.
- Do not guess original transaction identifiers for query, close, refund, or reconciliation.
- Do not generate production-ready code until required real values are known or clearly replaced with placeholders.

## First Response Behavior

If the user only says "Huifu payment does not work", do not give a long generic answer.

First classify what is known, then ask for the minimum missing evidence:

```text
我先按联调问题来排。请贴这 5 样，敏感信息打码：

1. 你走的是聚合支付、托管支付，还是前端收银台组件（checkout-js）
2. 当前失败步骤：下单 / 预下单 / 查单 / 退款 / 异步通知 / 签名 / 前端拉起
3. 技术栈和 SDK 版本：Java / PHP / JS / 原生 HTTP
4. 一次失败请求的 URL 或接口名、请求体、响应体、HTTP 状态码
5. 本地日志里签名、请求头、订单号、回调处理相关的几行
```

If the user already provided logs or payloads, do not ask again. Start diagnosis immediately.

## Evidence Checklist

Collect evidence in layers. Stop when the current layer is enough to diagnose.

### Layer 1: Route

- Product line: aggregation payment, hostingpay, front-end cashier component/check-out flow, or unknown
- Stage: init, order/preorder, query/close/reconcile, refund, webhook, signing, front-end cashier launch
- Runtime: Java SDK, PHP SDK, browser JS SDK, custom HTTP client, gateway/proxy
- Environment: sandbox/test, production, or unknown

### Layer 2: One Failed Transaction

- Request URL, function code, or SDK method name
- HTTP method and status code
- Sanitized request headers
- Sanitized request body
- Sanitized response body
- Local order id and merchant request id
- Safe identifiers if available: `req_date`, `req_seq_id`, `hf_seq_id`, `huifu_id`, `project_id`

### Layer 3: Local System Evidence

- SDK version and initialization config names, with secrets redacted
- Whether the signing input or request body is logged before and after signing, with secrets redacted
- Whether the order creation result is persisted
- Local order state before and after the failure
- Retry behavior and duplicate request handling

### Layer 4: Webhook Evidence

Use only for async notification problems:

- Raw notification body before parsing
- Notification headers
- Local verification result
- Handler HTTP response status and body
- Whether duplicate notifications update the same local order idempotently

### Layer 5: Front-End Evidence

Use only for front-end cashier component (`checkout-js`) or cashier launch problems:

- Browser SDK package/version
- Server preorder response passed to the browser
- Browser console error
- Network request/response from the browser
- Callback result and the later server-side query/webhook result

## Diagnostic Buckets

Always classify into one primary bucket. Mention secondary buckets only if needed.

| Bucket | Use When | Main Question |
| --- | --- | --- |
| `route` | User has not identified product line or stage | Which Huifu path are we on? |
| `credential/environment` | Test works but production fails, merchant id/key/project differs | Are endpoint, merchant, key, product, and project from the same environment? |
| `request-header` | Attribution/source header missing or gateway rejects request metadata | Are Huifu-required HTTP headers present in the right place? |
| `signing` | Sign/verify fails, response says signature invalid | Was the exact raw payload signed and verified with the right key pair? |
| `order-create` | Order/preorder fails before payment can start | Are required fields, channel fields, amount, merchant id, and product config valid? |
| `checkout` | 前端收银台组件（checkout-js）/收银台无法拉起，或返回异常前端状态 | Did hostingpay preorder succeed and is browser using safe, correct fields? |
| `final-state` | Front-end says paid but backend says unpaid/unknown | Is final state confirmed by query/webhook/reconciliation? |
| `webhook` | Async notification not received, verification fails, or Huifu retries | Can Huifu reach the endpoint and does handler verify/idempotently acknowledge? |
| `query-close` | Query/close/close-query cannot locate the trade | Are original transaction identifiers from persisted create result used? |
| `refund` | Refund/refund-query fails or repeats | Are original trade keys, refundable amount, and refund request id correct? |
| `reconciliation` | Statement and local orders do not match | Are settlement date, fees, refunds, and local state transitions aligned? |
| `production-readiness` | User asks if code can go live | Are secrets, final-state confirmation, idempotency, logging, and reconciliation safe? |

## Fast Symptom Map

| User Symptom | Bucket | First Things To Check |
| --- | --- | --- |
| "签名失败 / 验签失败" | `signing` | Raw body, key pair, JSON mutation, charset, timestamp |
| "jpt-x-skill-source 没有 / 来源头不对" | `request-header` | SDK config vs manual HTTP headers |
| "下单失败" | `order-create` | Required fields, environment, amount, channel-specific fields |
| "预下单成功但前端收银台拉不起" | `checkout` | `project_id`, preorder response, browser SDK, domain/callback |
| "前端成功但后台没成功" | `final-state` | Query/webhook final status, local state machine |
| "异步通知一直重试" | `webhook` | HTTP 200, response body, signature, idempotency |
| "查单查不到" | `query-close` | Stored `req_date`, `req_seq_id`, `hf_seq_id`, `out_trans_id` |
| "退款失败" | `refund` | Original trade id, amount, duplicate refund id, status |
| "对账不平" | `reconciliation` | Date window, refund timing, fee handling, missing final-state updates |
| "测试能用，生产不行" | `credential/environment` | Endpoint, merchant id, key pair, `sys_id`, product/project config |

## Hard Stops

Stop and ask one short question when continuing would create a wrong path.

### Unknown Product Line

Use when aggregation and hostingpay would require different documents or fields.

```text
硬检查点
当前还不能判断你走的是聚合支付还是托管支付。
请先确认：你是在做聚合支付下单，还是托管支付/收银台预下单？
```

### 前端收银台组件（checkout-js）缺少服务端前置条件

Use when the user wants front-end cashier component (`checkout-js`) guidance but has not confirmed hostingpay preorder and final confirmation.

```text
硬检查点
前端收银台组件（checkout-js）不能单独成立，它依赖服务端托管预下单和最终状态确认。
请先确认：服务端是否已经能成功托管预下单，并且能查单或接收异步通知？
```

### Production Code Without Real Values

Use when the user asks for production-ready code but required real values are missing.

```text
硬检查点
当前还缺生产联调必需值，直接给代码会变成伪完整模板。
请先确认：你要先补真实配置，还是只要带占位符的诊断模板？
```

### SDK Contradiction

Use when logs show behavior that conflicts with expected SDK header/signature behavior.

```text
硬检查点
日志里的 SDK 行为和当前预期规则冲突，需要先确认实际 SDK 版本和调用入口。
请贴 SDK 包名、版本号、初始化代码片段，密钥打码。
```

## Required Checks By Bucket

### `credential/environment`

Check in this order:

1. Endpoint belongs to the same environment as the merchant credentials.
2. `sys_id`, `product_id`, `huifu_id`, `project_id` belong to the same merchant/project.
3. Private key and Huifu public key are paired for the same environment.
4. Production config did not accidentally reuse sandbox keys.
5. Merchant product permissions include the requested payment channel and scenario.

Common conclusion:

```text
这类问题不是代码语法优先，而是环境一致性优先。先把 endpoint、商户号、系统号、产品号、项目号、密钥环境拉成一张表比对。
```

### `request-header`

Check:

- `jpt-x-skill-source` is an HTTP header, not a `data` field.
- `jpt-x-skill-huifu_id` is an HTTP header when request data contains non-empty `huifu_id`.
- Official Java/PHP SDK paths may add these through SDK config; custom HTTP clients must add them manually.
- Reverse proxies or gateways did not strip custom headers.
- Header value is not accidentally appended with `sys_id` unless the current official rule says so.

Ask for:

- Sanitized outgoing headers from the actual HTTP request
- SDK initialization config showing `skill_source` equivalent, secrets redacted

### `signing`

Check in this order:

1. The payload or canonical string used for signing matches the exact SDK/official signing path in use.
2. The HTTP body or signed business data was not mutated after signing.
3. JSON field order/canonicalization follows the SDK or official signing path in use.
4. Charset is stable, usually UTF-8 unless official path says otherwise.
5. Line endings in PEM keys are valid.
6. Private key is merchant private key; public key used for verification is Huifu public key.
7. Webhook verification uses raw notification body before parsing.
8. Clock skew/timestamp/nonce rules are satisfied.

Do not debug business fields before signing is known correct.

### `order-create`

Check:

- Required common fields are present.
- Amount unit and precision match Huifu requirements.
- Merchant request id is unique and not reused after a failed uncertain transaction.
- Channel-specific fields are present: WeChat, Alipay, UnionPay, barcode, mini program, H5/PC.
- `notify_url` and `callback_url` are correct for the environment.
- Local order is persisted before sending the request or immediately after receiving a deterministic create result.

If order creation returns a business error code, summarize:

- Which field/code failed
- Whether it is merchant config, request data, channel restriction, or duplicate order
- Which narrow Huifu order/preorder skill should be read next

### `checkout`

Remember: 前端收银台组件（checkout-js）只是浏览器层。它不能替代服务端托管预下单。

Check:

- Hostingpay preorder succeeded on the server.
- Browser receives only safe preorder/session fields, never private key material.
- `project_id` is correct for the merchant project.
- SDK version is pinned and loaded from the intended package/CDN.
- Domain, callback URL, and allowed origin match console config.
- Browser console and network logs are checked before changing server payment code.
- Front-end callback is treated as UX only.
- Final payment state still comes from server query or webhook.

Likely outputs:

```text
现在问题不在前端收银台组件（checkout-js）本身，先回到托管预下单返回值。
```

or:

```text
托管预下单已成功，问题集中在浏览器 SDK 初始化 / 域名回调配置。
```

### `final-state`

Use when user says paid page returned success but backend status is pending/fail.

Check:

- Was a server-side query made after callback?
- Was async notification received and verified?
- Does local state machine allow only monotonic transitions?
- Did duplicate notifications overwrite success with pending/fail?
- Is reconciliation later correcting state?

Rule:

```text
前端成功只能代表流程完成或用户体验成功，不代表资金最终成功。
```

### `webhook`

Check:

1. Huifu can reach `notify_url` from the public internet.
2. Endpoint uses HTTPS if required by the environment.
3. Server preserves raw body for verification.
4. Handler verifies signature before changing business state.
5. Handler is idempotent for the same notification/order.
6. Handler returns the required success HTTP status and response body.
7. Slow business logic is moved after acknowledgement or made retry-safe.
8. Logs record notification id/order id/status without secrets.

Common failure patterns:

- Framework parses JSON first, raw body lost, signature verification fails.
- Handler returns business JSON instead of Huifu-required success response.
- Local duplicate key error causes 500, Huifu retries forever.
- Notification updates local order before verifying final trade status.

### `query-close`

Check:

- Query uses identifiers returned by original order/preorder result and stored durably.
- `req_date` and `req_seq_id` are not guessed from current date or regenerated order id.
- `hf_seq_id` or equivalent Huifu sequence is stored when available.
- Close request only runs when local order is in a closable pending state.
- Close-query follows after close when close result is uncertain.

If the trade cannot be found, first inspect persistence, not gateway availability.

### `refund`

Check:

- Original successful transaction is known and stored.
- Refund amount does not exceed refundable amount.
- Refund request id is unique and persisted.
- Duplicate refund retry uses the same refund id only when intentionally querying/retrying an uncertain refund.
- Partial refund, fee, split, subsidy, or risk fields match the original transaction rules.
- Final refund state comes from refund query or notification/reconciliation, not only the initial refund response.

### `reconciliation`

Check:

- Reconciliation date is settlement/accounting date, not always order creation date.
- Refunds may appear on a different date from original payment.
- Fees, discounts, subsidies, and split/settlement records are modeled separately.
- Local success state is based on final confirmation, not only order request success.
- Missing records are grouped by cause: local missing, Huifu missing, amount mismatch, status mismatch, fee mismatch.

Output should include a difference table when data is provided.

### `production-readiness`

Use this when the user asks "can this go live".

Check:

- Secrets are only in server environment variables or secret manager.
- Private key never appears in front-end code, logs, Git, or static files.
- Order create, query, refund, and webhook are idempotent.
- Front-end callback is not trusted as final payment success.
- Query or webhook final confirmation is implemented.
- Request/response logs redact PII and secrets.
- Reconciliation or manual repair process exists.
- Retry policy avoids duplicate orders/refunds.
- Alerts exist for webhook failure, reconciliation mismatch, and abnormal success-rate drop.

## Output Template

Always prefer this format. Keep it concrete and short enough to act on.

```text
判断
当前问题属于：<bucket>
置信度：<high | medium | low>
我现在依据的是：<which logs/payloads/symptoms>

已看到的证据
- <fact from user input>
- <fact from user input>

还缺的关键证据
- <only things needed next>

最可能原因
1. <cause>：为什么它最像
2. <cause>：为什么它次像

怎么验证
- <specific field/log/code point to compare>
- <specific replay/query/check>

修复动作
- 立即修复：<code/config/action>
- 数据修复：<orders/refunds/webhook states to repair, if any>
- 防复发：<logging/idempotency/test/reconciliation guard>

需要路由阅读
- <only 1-3 Huifu skill/reference names, if necessary>
```

If evidence is insufficient, keep the same structure but make `还缺的关键证据` the main section.

## Reliability Rules

- Always label confidence: high, medium, or low.
- High confidence requires direct evidence from logs, payloads, status codes, or persisted order records.
- Medium confidence means the symptom strongly matches a known failure pattern but one key artifact is missing.
- Low confidence means the product line, stage, or payload is unclear; ask for evidence instead of guessing.
- Never say "一定是" unless the evidence proves it. Prefer "最像", "优先排查", or "需要验证".
- For every likely cause, include one verification step that could disprove it.
- If the user gives an error code, do not explain from memory alone; route to the narrow Huifu error-code/reference document when available.
- If multiple causes are possible, fix the cheapest reversible check first: headers/logging/config before business redesign.

## Example Diagnoses

### Example: Signature Failure

Input:

```text
PHP SDK 请求返回验签失败。我们打印的 JSON 和发送的 JSON 好像一样。
```

Good response:

```text
判断
当前问题属于：signing。
置信度：medium。

最可能原因
1. 签名输入或签名覆盖的业务数据与最终出站 payload 不一致：PHP 中间层可能重新 json_encode 或改写字段。
2. 密钥环境不一致：测试环境私钥配了生产环境汇付公钥，或反过来。

怎么验证
- 在签名前打印签名输入或关键 payload 的 SHA256，不打印明文敏感字段。
- 在 HTTP client 发送前再打印最终出站 payload 的 SHA256；如果当前路径是 raw-body 签名，两个值必须一致。
- 核对当前 endpoint、sys_id、huifu 公钥、商户私钥是否来自同一环境。

修复动作
- 立即修复：签名后不要再改签名覆盖的数据；raw-body 签名路径要发送签名使用的同一份字符串。
- 防复发：把签名输入 hash、发送前 payload hash、request id 写入联调日志。
```

### Example: 前端收银台回调成功但后台仍未支付

Input:

```text
前端收银台组件（checkout-js）回调成功了，但我们系统订单还是未支付。
```

Good response:

```text
判断
当前问题属于：final-state，可能伴随 webhook/query 缺失。
置信度：medium。

最可能原因
1. 你们把前端收银台回调当成最终成功，但服务端没有查单或处理异步通知。
2. 异步通知失败或验签失败，导致本地订单没有从 pending 转 success。

怎么验证
- 查这笔订单是否执行过服务端查单，记录 Huifu 最终交易状态。
- 查 notify_url 是否收到通知、验签是否通过、handler 返回是否为成功响应。

修复动作
- 立即修复：前端回调只更新页面提示，后台订单状态必须由查单或异步通知更新。
- 数据修复：对 pending 订单按 Huifu 订单号批量查单并修正状态。
- 防复发：增加 pending 超时补查任务和 webhook 失败告警。
```

### Example: Webhook Repeated Retries

Input:

```text
汇付一直重复通知，日志里我们已经处理成功了。
```

Good response:

```text
判断
当前问题属于：webhook。
置信度：medium。

最可能原因
1. 业务处理成功，但 HTTP 响应状态或响应体不是汇付要求的成功格式。
2. 第二次重复通知触发本地唯一键异常，handler 返回 500，所以汇付继续重试。

怎么验证
- 看 notify handler 最终 HTTP status 和 response body，不只看业务日志。
- 用同一笔通知重复请求本地接口，确认第二次仍返回成功。

修复动作
- 立即修复：验签通过且状态已处理时，重复通知也返回成功。
- 数据修复：检查这笔订单是否被重复写入流水或状态被覆盖。
- 防复发：通知表按通知 id/订单 id 做幂等，业务异常和响应异常分开告警。
```

## Route To Huifu Skills

After classification, route only to the narrowest skill or reference family:

- Aggregation order/query/refund/reconciliation: `huifu-dougong-aggregation-*`
- Hostingpay preorder/query/refund/webhook: `huifu-dougong-hostingpay-*`
- 前端收银台组件（checkout-js）: `huifu-dougong-hostingpay-checkout-js`
- Shared signing/header/webhook/release checks: `huifu-dougong-pay-shared-base` or shared references inside `huifu-payment-integration`

Do not list the full Huifu document set. A diagnostic answer should usually cite 0-3 follow-up documents.
