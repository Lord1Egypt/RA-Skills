---
name: jtexpress
description: Use J&T Express (极兔速递) for shipment tracking, shipping guidance, service-type comparison, outlet lookup, and delivery-time or fee estimation.
version: 1.0.0
tags: logistics, shipping, economy, jitu, china, tracking
---

# J&T Express (极兔速递)

## Overview

Use this skill to help users with common J&T Express tasks such as tracking shipments, understanding service levels, estimating timing or fees, and preparing to send a parcel.

## Usage Scenarios

### Scenario 1: Track a J&T Express shipment
**User input:** "极兔快递单号 JT1234567890 怎么查不到？"
**Expected output:** Check the tracking number format and guide the user on J&T tracking methods. If the number is recent, explain that tracking may take a few hours to appear in the system. Provide the latest available status (e.g., "包裹已揽收") or suggest retrying after some time.

### Scenario 2: Estimate J&T shipping fee for e-commerce return
**User input:** "我要退货，用极兔寄一个1公斤的包裹从杭州到南京，多少钱？"
**Expected output:** Give a fee estimate for J&T's economy service. Explain that J&T Express is popular for e-commerce returns and typically offers competitive rates for lightweight parcels. Provide a price range and note any minimum charge for the first kg plus per-kg surcharge.

### Scenario 3: Compare J&T vs other economy carriers
**User input:** "极兔和中通、韵达比，哪个便宜？"
**Expected output:** Compare J&T Express with ZTO and Yunda on pricing, coverage, average transit time, and reliability. Note J&T's aggressive pricing strategy and strong presence in e-commerce parcels, but also mention that service quality may vary by region.
### Scenario 4: 极兔寄件查运费
**User input:** "我想从上海寄一袋5公斤的猫粮到长沙，用极兔大概多少钱？比中通便宜吗？"
**Expected output:** 查询极兔速递的标准运费表，估算从上海到长沙5公斤包裹的费用；同时给出拼多多/淘宝等平台寄件（菜鸟裹裹）的比价参考。说明极兔在拼多多订单中的常见运费优势，以及是否有续重优惠。

## Local Persistence

When the local CLI/runtime code is used, this skill may create and persist local data under:

- `~/.openclaw/data/jtexpress/jtexpress.db`
  - stores query history
  - stores shipment-subscription records
  - may store saved address records if those commands are implemented/used
- `~/.openclaw/data/jtexpress/secure/`
  - stores encrypted local files used by the privacy/storage helper
- `~/.openclaw/data/jtexpress/secure/.key`
  - stores a local encryption key file with mode `600`
- `~/.openclaw/data/jtexpress/privacy_export.json`
  - may be created when the user runs privacy export

Only use persistence when it is necessary for the user's requested workflow. If the user asks about privacy, disclose these paths clearly.

## Privacy Controls

The local CLI supports privacy operations:

- `privacy info` — show local storage paths and stored-file info
- `privacy clear` — clear local SQLite history/subscription data and encrypted local files
- `privacy export` — export local storage metadata to `privacy_export.json`

## Workflow

1. Determine the user's goal:
   - track an existing shipment
   - estimate fee or delivery time
   - compare service types
   - find a nearby outlet or pickup point
   - prepare shipment details
   - review or clear local history/subscriptions/privacy data
2. Ask for only the missing essentials, such as tracking number, route, package size, or urgency.
3. Give the most practical answer first.
4. If exact fee or timing cannot be confirmed, provide a cautious estimate and state assumptions.
5. If the task uses local runtime features that persist data, mention that local history/subscription/privacy files may be created under `~/.openclaw/data/jtexpress/`.
6. Do not claim to complete real shipping actions unless live tools are available and confirmed.
