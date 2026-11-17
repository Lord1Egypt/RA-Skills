---
name: linkfox-amazon-store-fba
description: 亚马逊店铺 Fulfillment by Amazon（FBA）系列（与 linkfox-amazon-store-auth 同系列），经 /spApi/developerProxy 调用 SP-API：FBA Inbound Eligibility（getItemEligibilityPreview）、FBA Inventory（getInventorySummaries/createInventoryItem/deleteInventoryItem/addInventory）、Fulfillment Inbound v2024-03-20（InboundPlan/装箱/放置/运输/货件等）与 v0（prepInstructions/labels/BOL/shipments）、Fulfillment Outbound 2020-07-01（MCF 履约单/预览/退货/tracking/features）。当用户提到 FBA、入仓资格、Inbound Eligibility、FBA 库存摘要、Send to Amazon、Inbound Plan、FBA 货件、MCF、多渠道履约、getItemEligibilityPreview、getInventorySummaries、createInboundPlan、createFulfillmentOrder 时触发。与 External Fulfillment / 普通 Orders 不同。
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

## 解决认证和积分问题

发生未配置 API Key、401/402、积分不足时，采用 `references/onboarding.md` 引导。

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

## 积分消耗规则

不消耗积分（以网关实际计费为准）。

**Feedback：** `skillName`：`linkfox-amazon-store-fba`

---
*更多跨境 skill：[LinkFox Skills](https://skill.linkfox.com/)*


---

# linkfox-amazon-store-fba — API 与网关说明

## 1. 调用链

`POST ${LINKFOX_TOOL_GATEWAY}/spApi/developerProxy`

| 字段 | 说明 |
|------|------|
| region | NA / EU / FE |
| path | SP-API 相对路径，无前导 `/` |
| method | GET / POST / PUT / DELETE / PATCH |
| sellerId | 店铺 ID（网关解析 token） |
| queryString | 可选 |
| body + contentType | 写操作 |

环境变量：`LINKFOX_AGENT_API_KEY`（或 `LINKFOXAGENT_API_KEY`）、可选 `LINKFOX_TOOL_GATEWAY`。

## 2. 通用 JSON 入参

| 字段 | 必填 | 说明 |
|------|------|------|
| sellerId / region | 是 | |
| api / operation | 用 `fba_api.py` 时必填 | Amazon operationId |
| requestBody | 写操作推荐 | 官方 body |
| query | 否 | 额外 query 对象 |
| queryString | 否 | 原始查询串（覆盖） |
| skipDepCheck | 否 | 跳过 auth skill 探测 |
| marketplaceId | 否 | 自动提升为 marketplaceIds |

路径模板参数（如 `inboundPlanId`、`shipmentId`、`sellerSku`）直接写在同级 JSON。

## 3. 模块索引

完整表见 [`capabilities.md`](capabilities.md)，机器可读见 [`operations.json`](operations.json)。

### 3.1 Eligibility

- `getItemEligibilityPreview`：`asin` + `program`；INBOUND 需 marketplaceIds

### 3.2 Inventory

- `getInventorySummaries`：granularityType + granularityId + marketplaceIds
- `createInventoryItem` / `addInventory`：marketplaceId + requestBody
- `deleteInventoryItem`：sellerSku + marketplaceId

### 3.3 Inbound v0

- prepInstructions / labels / billOfLading / shipments / shipmentItems

### 3.4 Inbound 2024-03-20

- InboundPlan CRUD 与状态机：packing → placement → transportation → shipment
- 异步：`getInboundOperationStatus`
- items：compliance / labels / prepDetails

### 3.5 Outbound 2020-07-01

- preview / deliveryOffers / fulfillmentOrders CRUD / return / tracking / features

## 4. 官方入口

- [getItemEligibilityPreview](https://developer-docs.amazon.com/sp-api/reference/getitemeligibilitypreview)
- [FBA Inventory v1](https://developer-docs.amazon.com/sp-api/reference/fba-inventory-v1)
- [Fulfillment Inbound v2024-03-20](https://developer-docs.amazon.com/sp-api/reference/fulfillment-inbound-v2024-03-20)
- [Fulfillment Inbound v0](https://developer-docs.amazon.com/sp-api/reference/fulfillment-inbound-v0)
- [Fulfillment Outbound 2020-07-01](https://developer-docs.amazon.com/sp-api/reference/fulfillment-outbound-2020-07-01)

## 5. 错误处理

| 现象 | 处理 |
|------|------|
| 401/402 / 积分 | onboarding.md |
| 1005 | 放行 `fba/`、`inbound/fba/` |
| 403 | 角色/权限 |
| 409/422 | 状态机或参数问题 |
| 429 | 降速，先征得用户同意 |

## 6. Feedback

`skillName`：`linkfox-amazon-store-fba`


---

### eligibility (1)

| Operation | Method | path | 脚本 |
|-----------|--------|------|------|
| getItemEligibilityPreview | GET | `fba/inbound/v1/eligibility/itemPreview` | `get_item_eligibility_preview.py` |

### inventory (4)

| Operation | Method | path | 脚本 |
|-----------|--------|------|------|
| getInventorySummaries | GET | `fba/inventory/v1/summaries` | `get_inventory_summaries.py` |
| createInventoryItem | POST | `fba/inventory/v1/items` | `create_inventory_item.py` |
| deleteInventoryItem | DELETE | `fba/inventory/v1/items/{sellerSku}` | `delete_inventory_item.py` |
| addInventory | POST | `fba/inventory/v1/items/inventory` | `add_inventory.py` |

### inbound_v0 (6)

| Operation | Method | path | 脚本 |
|-----------|--------|------|------|
| getPrepInstructions | GET | `fba/inbound/v0/prepInstructions` | `get_prep_instructions.py` |
| getLabels | GET | `fba/inbound/v0/shipments/{shipmentId}/labels` | `get_labels_v0.py` |
| getBillOfLading | GET | `fba/inbound/v0/shipments/{shipmentId}/billOfLading` | `get_bill_of_lading.py` |
| getShipments | GET | `fba/inbound/v0/shipments` | `get_shipments_v0.py` |
| getShipmentItemsByShipmentId | GET | `fba/inbound/v0/shipments/{shipmentId}/items` | `get_shipment_items_by_shipment_id.py` |
| getShipmentItems | GET | `fba/inbound/v0/shipmentItems` | `get_shipment_items.py` |

### inbound (45)

| Operation | Method | path | 脚本 |
|-----------|--------|------|------|
| listInboundPlans | GET | `inbound/fba/2024-03-20/inboundPlans` | `list_inbound_plans.py` |
| createInboundPlan | POST | `inbound/fba/2024-03-20/inboundPlans` | `create_inbound_plan.py` |
| getInboundPlan | GET | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}` | `get_inbound_plan.py` |
| listInboundPlanBoxes | GET | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/boxes` | `list_inbound_plan_boxes.py` |
| cancelInboundPlan | PUT | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/cancellation` | `cancel_inbound_plan.py` |
| listInboundPlanItems | GET | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/items` | `list_inbound_plan_items.py` |
| updateInboundPlanName | PUT | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/name` | `update_inbound_plan_name.py` |
| listPackingGroupBoxes | GET | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/packingGroups/{packingGroupId}/boxes` | `list_packing_group_boxes.py` |
| listPackingGroupItems | GET | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/packingGroups/{packingGroupId}/items` | `list_packing_group_items.py` |
| setPackingInformation | POST | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/packingInformation` | `set_packing_information.py` |
| listPackingOptions | GET | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/packingOptions` | `list_packing_options.py` |
| generatePackingOptions | POST | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/packingOptions` | `generate_packing_options.py` |
| confirmPackingOption | POST | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/packingOptions/{packingOptionId}/confirmation` | `confirm_packing_option.py` |
| listInboundPlanPallets | GET | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/pallets` | `list_inbound_plan_pallets.py` |
| listPlacementOptions | GET | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/placementOptions` | `list_placement_options.py` |
| generatePlacementOptions | POST | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/placementOptions` | `generate_placement_options.py` |
| confirmPlacementOption | POST | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/placementOptions/{placementOptionId}/confirmation` | `confirm_placement_option.py` |
| getShipment | GET | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/shipments/{shipmentId}` | `get_inbound_shipment.py` |
| listShipmentBoxes | GET | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/boxes` | `list_shipment_boxes.py` |
| listShipmentContentUpdatePreviews | GET | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/contentUpdatePreviews` | `list_shipment_content_update_previews.py` |
| generateShipmentContentUpdatePreviews | POST | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/contentUpdatePreviews` | `generate_shipment_content_update_previews.py` |
| getShipmentContentUpdatePreview | GET | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/contentUpdatePreviews/{contentUpdatePreviewId}` | `get_shipment_content_update_preview.py` |
| confirmShipmentContentUpdatePreview | POST | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/contentUpdatePreviews/{contentUpdatePreviewId}/confirmation` | `confirm_shipment_content_update_preview.py` |
| getDeliveryChallanDocument | GET | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/deliveryChallanDocument` | `get_delivery_challan_document.py` |
| listDeliveryWindowOptions | GET | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/deliveryWindowOptions` | `list_delivery_window_options.py` |
| generateDeliveryWindowOptions | POST | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/deliveryWindowOptions` | `generate_delivery_window_options.py` |
| confirmDeliveryWindowOptions | POST | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/deliveryWindowOptions/{deliveryWindowOptionId}/confirmation` | `confirm_delivery_window_options.py` |
| listShipmentItems | GET | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/items` | `list_shipment_items.py` |
| updateShipmentName | PUT | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/name` | `update_shipment_name.py` |
| listShipmentPallets | GET | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/pallets` | `list_shipment_pallets.py` |
| cancelSelfShipAppointment | PUT | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/selfShipAppointmentCancellation` | `cancel_self_ship_appointment.py` |
| getSelfShipAppointmentSlots | GET | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/selfShipAppointmentSlots` | `get_self_ship_appointment_slots.py` |
| generateSelfShipAppointmentSlots | POST | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/selfShipAppointmentSlots` | `generate_self_ship_appointment_slots.py` |
| scheduleSelfShipAppointment | POST | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/selfShipAppointmentSlots/{slotId}/schedule` | `schedule_self_ship_appointment.py` |
| updateShipmentSourceAddress | PUT | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/sourceAddress` | `update_shipment_source_address.py` |
| updateShipmentTrackingDetails | PUT | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/shipments/{shipmentId}/trackingDetails` | `update_shipment_tracking_details.py` |
| listTransportationOptions | GET | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/transportationOptions` | `list_transportation_options.py` |
| generateTransportationOptions | POST | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/transportationOptions` | `generate_transportation_options.py` |
| confirmTransportationOptions | POST | `inbound/fba/2024-03-20/inboundPlans/{inboundPlanId}/transportationOptions/confirmation` | `confirm_transportation_options.py` |
| listItemComplianceDetails | GET | `inbound/fba/2024-03-20/items/compliance` | `list_item_compliance_details.py` |
| updateItemComplianceDetails | PUT | `inbound/fba/2024-03-20/items/compliance` | `update_item_compliance_details.py` |
| createMarketplaceItemLabels | POST | `inbound/fba/2024-03-20/items/labels` | `create_marketplace_item_labels.py` |
| listPrepDetails | GET | `inbound/fba/2024-03-20/items/prepDetails` | `list_prep_details.py` |
| setPrepDetails | POST | `inbound/fba/2024-03-20/items/prepDetails` | `set_prep_details.py` |
| getInboundOperationStatus | GET | `inbound/fba/2024-03-20/operations/{operationId}` | `get_inbound_operation_status.py` |

### outbound (14)

| Operation | Method | path | 脚本 |
|-----------|--------|------|------|
| getFulfillmentPreview | POST | `fba/outbound/2020-07-01/fulfillmentOrders/preview` | `get_fulfillment_preview.py` |
| deliveryOffers | POST | `fba/outbound/2020-07-01/deliveryOffers` | `delivery_offers.py` |
| listAllFulfillmentOrders | GET | `fba/outbound/2020-07-01/fulfillmentOrders` | `list_all_fulfillment_orders.py` |
| createFulfillmentOrder | POST | `fba/outbound/2020-07-01/fulfillmentOrders` | `create_fulfillment_order.py` |
| getPackageTrackingDetails | GET | `fba/outbound/2020-07-01/tracking` | `get_package_tracking_details.py` |
| listReturnReasonCodes | GET | `fba/outbound/2020-07-01/returnReasonCodes` | `list_return_reason_codes.py` |
| createFulfillmentReturn | PUT | `fba/outbound/2020-07-01/fulfillmentOrders/{sellerFulfillmentOrderId}/return` | `create_fulfillment_return.py` |
| getFulfillmentOrder | GET | `fba/outbound/2020-07-01/fulfillmentOrders/{sellerFulfillmentOrderId}` | `get_fulfillment_order.py` |
| updateFulfillmentOrder | PUT | `fba/outbound/2020-07-01/fulfillmentOrders/{sellerFulfillmentOrderId}` | `update_fulfillment_order.py` |
| cancelFulfillmentOrder | PUT | `fba/outbound/2020-07-01/fulfillmentOrders/{sellerFulfillmentOrderId}/cancel` | `cancel_fulfillment_order.py` |
| submitFulfillmentOrderStatusUpdate | PUT | `fba/outbound/2020-07-01/fulfillmentOrders/{sellerFulfillmentOrderId}/status` | `submit_fulfillment_order_status_update.py` |
| getFeatures | GET | `fba/outbound/2020-07-01/features` | `get_features.py` |
| getFeatureInventory | GET | `fba/outbound/2020-07-01/features/inventory/{featureName}` | `get_feature_inventory.py` |
| getFeatureSKU | GET | `fba/outbound/2020-07-01/features/inventory/{featureName}/{sellerSku}` | `get_feature_sku.py` |

