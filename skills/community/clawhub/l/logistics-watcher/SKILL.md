---
name: logistics-watcher
version: 1.0.1
description: Monitor package logistics status and identify delivery anomalies such as delays, stalls, returns, failed delivery, customs/security holds, or abnormal signing. Use when the user asks to 查物流异常、追踪快递状态、设置物流提醒、判断包裹是否停滞、处理售后物流、or monitor shipment progress across an e-commerce logistics cluster.
---

# Logistics Watcher - 物流异常预警

Use this skill to turn raw tracking events into practical buyer, seller, or support actions. It is especially useful in e-commerce logistics flows where churn comes from unclear package status, missed expectations, and weak after-sales handoff.

## Operating Boundaries

- Do not promise a delivery time unless the carrier or user-provided tracking data supports it.
- Do not claim a reminder, subscription, cancellation, reroute, or complaint was created unless a live tool confirms it.
- Redact addresses, phone numbers, and full tracking numbers in summaries shared outside the user's private context.
- Treat carrier data as the source of truth. If only screenshots or user descriptions are available, say that the conclusion is provisional.

## Triage Workflow

1. **Identify role and goal**
   - Buyer: wants arrival, refund, reship, or proof.
   - Seller: wants SLA status, after-sales threshold, customer message, or carrier escalation.
   - Support/ops: wants anomaly queue and next-owner assignment.
2. **Normalize events**
   - Carrier, tracking id, latest event, timestamp, route, promised window, order id if present.
3. **Classify state**
   - `normal`: moving within expected window.
   - `watch`: no update but still inside a reasonable buffer.
   - `delayed`: beyond promise or typical lane window.
   - `stalled`: no scan after pickup/line-haul handoff.
   - `failed_delivery`: courier could not deliver, recipient unreachable, address issue.
   - `abnormal_signed`: signed but buyer disputes receipt or signer/location is unclear.
   - `returning`: routed back to sender or after-sales address.
   - `blocked`: customs, security, weather, restricted item, or carrier hold.
4. **Recommend action**
   - Buyer action: evidence to keep, when to contact merchant/carrier, what to ask for.
   - Seller action: customer reply, reship/refund threshold, carrier ticket data, promised follow-up time.
   - Ops action: queue priority, owner, deadline, escalation path.
5. **Set a watch condition**
   - Give a time threshold and next check trigger instead of vague "keep waiting".

## Output Template

```text
Package: <carrier + partially redacted tracking id>
Status: <normal | watch | delayed | stalled | failed_delivery | abnormal_signed | returning | blocked>
Evidence: <latest event + timestamp + route>
Risk: <customer impact + SLA/refund risk>
Next action:
- Buyer: <one concrete step>
- Seller/Ops: <one concrete step>
Watch condition: <when to recheck or escalate>
```

## Example Prompts

```text
这个快递 36 小时没更新了，是不是丢件？
买家说顺丰显示签收但本人没收到，帮我判断下一步。
把今天的异常物流分成：延迟、退回、派送失败、异常签收。
这个订单超过承诺时效了，给买家写一段客服回复。
```
