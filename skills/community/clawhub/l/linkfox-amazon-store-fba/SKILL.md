---
name: linkfox-amazon-store-fba
description: 亚马逊 FBA 综合管理技能。用于查询商品入仓资格与 FBA 库存，调整库存，并处理 FBA 入仓计划、装箱、放置、运输、货件、标签、提单以及旧版 MCF 多渠道履约订单、退货和跟踪等跨域流程。用户提到亚马逊 FBA、入仓资格、Inbound Eligibility、FBA 库存摘要、Send to Amazon、Inbound Plan、FBA 货件、旧版 MCF、getItemEligibilityPreview、getInventorySummaries、createInboundPlan、createFulfillmentOrder 时触发。若需求专门涉及 Fulfillment Inbound v2024-03-20 入仓流程，优先使用 linkfox-amazon-store-fulfillment-inbound；涉及 Fulfillment Outbound v2026-07-04 新版 MCF，使用 linkfox-amazon-store-fulfillment-outbound；External Fulfillment 和普通卖家订单不属于此技能。
---

# Amazon 店铺 Fulfillment by Amazon (FBA)

本 skill 与 **`linkfox-amazon-store-auth`** 同属 **Amazon Store** 系列：依赖授权选店（`sellerId`+`region`）；经 **`POST /spApi/developerProxy`** 转发 SP-API（勿传 `amzAccessToken`，除非兼容旧调用）。

覆盖 **方案 A** 模块：

1. **Inbound Eligibility v1**（入仓/混装资格预览）
2. **FBA Inventory v1**（仓内库存）
3. **Fulfillment Inbound v2024-03-20**（现行入仓工作流）+ **v0** 保留查询
4. **Fulfillment Outbound 2020-07-01**（MCF 多渠道履约）

不包含：FBA Small and Light（已弃用）、External Fulfillment（见 `linkfox-amazon-store-external-fulfillment`）、Merchant Fulfillment（MFN）。

## 调用方式

- **统一入口**：`python scripts/fba_api.py '{"api":"<operationId>","sellerId":"...","region":"NA",...}' [--inline]`
- **单接口脚本**：`python scripts/<脚本名>.py '<JSON>' [--inline]`（完整对照见 `references/capabilities.md`）
- **写操作 body**：优先传 **`requestBody`**；也可把业务字段平铺在 JSON 中（脚本会排除 sellerId/region/path/query 后组装 body）
- **Query**：声明字段直接传；或用 **`query`** 对象 / **`queryString`** 覆盖
- **成本约束**：失败/空结果不得自动翻页或连续试探；继续前先说明可能产生额外消耗

**输出策略**：完整响应落盘到 `linkfox/<date>/<session>/data/linkfox-amazon-store-fba-*.json`；>8KB 默认摘要；`--inline` 全量打印。

## 解决认证和算力问题

发生未配置 API Key、401/402、算力不足时，采用 `references/onboarding.md` 引导。

## Prerequisites

1. 依赖 **`linkfox-amazon-store-auth`**：`python scripts/check_auth_dependency.py`（exit 42 → 先装 auth）
2. 应用需具备 **Amazon Fulfillment** 等相关角色（以 Amazon 控制台为准）
3. 网关需放行路径前缀：`fba/`、`inbound/fba/`（遇 **1005** 找后端加白）

## Current Capabilities

共 **70** 个 operation。模块表：

| 模块 | 数量 | 说明 |
|------|------|------|
| eligibility | 1 | getItemEligibilityPreview |
| inventory | 4 | summaries / create / delete / add |
| inbound_v0 | 6 | prep / labels / BOL / shipments / items |
| inbound (2024-03-20) | 45 | InboundPlan 全流程 |
| outbound (2020-07-01) | 14 | MCF 履约 |

**完整 Operation ↔ path ↔ 脚本表**：见 [`references/capabilities.md`](references/capabilities.md)  
**机器可读注册表**：`scripts/_fba_endpoints.py`、`references/operations.json`

## Quick Parameters

### getItemEligibilityPreview

- 必填：`asin`、`program`（`INBOUND`|`COMMINGLING`）
- `program=INBOUND` 时必填 `marketplaceIds`（或 `marketplaceId`，最多 1 个）

```bash
python scripts/get_item_eligibility_preview.py '{"sellerId":"A1...","region":"NA","asin":"B0...","program":"INBOUND","marketplaceId":"ATVPDKIKX0DER"}'
```

### getInventorySummaries

- 必填：`granularityType`（通常 `Marketplace`）、`granularityId`（marketplaceId）、`marketplaceIds`
- 可选：`details`、`sellerSkus`、`startDateTime`、`nextToken`

### Inbound / Outbound 写操作

复杂 schema 请用 **`requestBody`** 按官方模型传完整 JSON；path 参数（如 `inboundPlanId`、`shipmentId`、`sellerFulfillmentOrderId`）与 query 字段并列在入参中。

异步步骤（generate*Options 等）返回后用 **`getInboundOperationStatus`** 轮询（勿擅自高频轮询，先征得用户同意）。

## Scripts

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

# 统一入口
python scripts/fba_api.py '{"api":"getItemEligibilityPreview","sellerId":"A1...","region":"NA","asin":"B0...","program":"INBOUND","marketplaceIds":["ATVPDKIKX0DER"]}'

python scripts/fba_api.py '{"api":"getInventorySummaries","sellerId":"A1...","region":"NA","granularityType":"Marketplace","granularityId":"ATVPDKIKX0DER","marketplaceIds":["ATVPDKIKX0DER"],"details":true}'

python scripts/fba_api.py '{"api":"listInboundPlans","sellerId":"A1...","region":"NA","pageSize":10}'
```

共享模块：`_spapi_fba_common.py`、`_fba_endpoints.py`、`_fba_runner.py`（非独立 CLI）。

## Display Rules

1. 先看 `developerProxy.errcode` / `httpStatus`，再看解析字段 **`payload`**
2. 202/204 可能无 body；以状态码判断成功
3. Inbound 2024 与 v0 的 `getShipments`/`getShipment` 勿混淆：v0 脚本为 `get_shipments_v0.py`；2024 货件为 `get_inbound_shipment.py`
4. 与 **`linkfox-amazon-store-orders`**、**`linkfox-amazon-store-external-fulfillment`** 边界清晰，勿混用

## Important Limitations

- Outbound **2026-07-04** 未纳入本 skill（方案 A）
- Small and Light 已弃用，不实现
- Inbound 状态机复杂，需按官方工作流顺序调用；冲突常见 **409/422**
- 限速因接口而异（Eligibility 约 1 rps），注意 **429**

## Amazon SP-API 接口保护与重试指引

同一店铺连续收到 Amazon SP-API 的 400、403、404 或 429 时，网关会返回 450、453、454 或 459 并短暂冷却。这些自定义状态码不是 Amazon 原生状态，也不表示封号；目的是避免持续异常或高频调用扩大店铺风险。

| 状态与 message | 范围 | 触发与冷却 | 处理 |
|---|---|---|---|
| `450`：`400，请求异常，请优化您的参数` | 店铺+接口 | 60 秒内超过 3 次：5 分钟；10 分钟内超过 4 次：20 分钟 | 停止原参数重试，检查必填字段、marketplace、ID、日期和请求体 |
| `453`：`403，店铺未授权，请先授权` | 店铺全部接口 | 60 秒内超过 2 次：5 分钟；10 分钟内超过 4 次：30 分钟 | 停止该店铺调用，检查授权、权限、店铺归属和区域 |
| `454`：`404，资源不存在，请优化您的参数` | 店铺+接口 | 60 秒内超过 3 次：5 分钟；10 分钟内超过 4 次：30 分钟 | 确认资源 ID、所属店铺/站点、资源状态和接口路径 |
| `459`：`429限流中，请降低频率` | 店铺+接口 | 首次：15 秒；2 分钟内超过 2 次：30 秒；3 分钟内超过 4 次：2 分钟 | 降低并发、分页和轮询频率并逐级退避 |

- 立即停止自动或并发重试，不得通过换脚本或重复创建任务绕过保护；优先遵循 `retryAfter`、`blockedUntil`，没有时按表中时长说明。
- 450/453/454 必须先修正参数、授权或资源标识，冷却后最多谨慎重试一次；再次触发则停止调用。453 期间停止该店铺全部 SP-API。
- 保留已有 `reportId`、`feedId` 等任务 ID；写操作结果不确定时先查询状态，不直接重放。
- 向用户先说明店铺保护，再给原因、处理和等待时间。可回复：“为保护您的亚马逊店铺安全，检测到 Amazon SP-API 连续返回{原因}，当前已进入短暂保护。请先{处理动作}，预计{等待时间}后再试；这不代表封号，也不是套餐或算力限制。”不要只说“LinkFox 限流”或“服务器繁忙”。

## 算力消耗规则

不消耗算力（以网关实际计费为准）。

**Feedback：** `skillName`：`linkfox-amazon-store-fba`

---
*更多跨境 skill：[LinkFox Skills](https://skill.linkfox.com/)*
