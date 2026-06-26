---
name: jdl-express
description: Use JD Logistics (京东快递) for shipment tracking, shipping guidance, service-type comparison, outlet lookup, and delivery-time or fee estimation.
version: 1.0.0
tags: logistics, shipping, jd, ecommerce, same-day-delivery, china
---

# JD Logistics (京东快递)

## Overview

Use this skill to help users with common JD Logistics tasks such as tracking shipments, understanding service levels, estimating timing or fees, and preparing to send a parcel.

## Usage Scenarios

### Scenario 1: Track a JD Logistics shipment
**User input:** "京东快递单号 JDK123456789 到哪里了？"
**Expected output:** Return the current tracking status showing the latest scan event (e.g., "快件已到达北京通州分拣中心"), the estimated delivery time window, and pickup instructions if applicable. For JD same-day or next-day services, highlight the SLA status (e.g., "预计今日达").

### Scenario 2: Compare JD Express service types
**User input:** "京东快递的京尊达、特快送和特惠送有什么区别？"
**Expected output:** Explain the differences between JD Logistics service tiers: 京尊达 (premium, dedicated driver), 特快送 (express, 1-3 day), 特惠送 (economy, 3-5 day). Include typical pricing differences, coverage scope, and which service is best for time-sensitive vs budget-conscious shipments.

### Scenario 3: Estimate JD delivery time
**User input:** "从上海发到深圳，京东快递多久能到？"
**Expected output:** Provide estimated delivery time based on route and service type, noting JD's advantage in city-to-city routes with their own logistics network. Give a realistic range (e.g., "特快送约1-2天，特惠送约2-4天") and factor in weather or holiday effects if applicable.
### Scenario 4: 京东快递退货上门取件
**User input:** "我在京东买了个手机壳不合适要退货，约了京东快递明天上门，但我忘了把取件码放哪了，怎么办？"
**Expected output:** 引导用户在京东App订单详情或京东快递小程序中找到取件码/上门取件编号；如果找不到，提供重新获取取件码的路径（联系京东客服或查看退换货进度）。同时提示用户准备好包裹（原包装+退换货单）并了解快递员上门时间范围。

## Local Persistence

When the local CLI/runtime code is used, this skill may create and persist local data under:

- `~/.openclaw/data/jdl-express/jdlexpress.db`
  - stores query history
  - stores shipment-subscription records
  - may store saved address records if those commands are implemented/used
- `~/.openclaw/data/jdl-express/secure/`
  - stores encrypted local files used by the privacy/storage helper
- `~/.openclaw/data/jdl-express/secure/.key`
  - stores a local encryption key file with mode `600`
- `~/.openclaw/data/jdl-express/privacy_export.json`
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
5. If the task uses local runtime features that persist data, mention that local history/subscription/privacy files may be created under `~/.openclaw/data/jdl-express/`.
6. Do not claim to complete real shipping actions unless live tools are available and confirmed.
