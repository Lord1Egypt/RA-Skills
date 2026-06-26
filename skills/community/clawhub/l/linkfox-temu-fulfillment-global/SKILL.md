---
name: linkfox-temu-fulfillment-global
version: 1.0.0
category: product-sourcing
description: Temu 全球站（非 US/EU）电商履行/发货 API（合一）：Buy-Shipping购标面单、合作仓履约、卖家自发货、物流跟踪等23个接口（不含 Scan Form）。当用户提到 Temu Global 发货、购标、Buy-Shipping、合作仓、自发货、tracking、shipment.create、site=global order-shipping 时触发。订单用 linkfox-temu-order-global。Scan Form 请用 linkfox-temu-fulfillment-us。
---

# Temu 全球站 — 电商履行 / 发货（Fulfillment）

本 skill（`linkfox-temu-fulfillment-global`）覆盖 Partner **Global** **Fulfillment** 域 **23** 个已接入 `type`（与 US 版对齐但 **不含** 4 个 Scan Form 接口）。

| 域 | 脚本前缀 | 接口数 |
|----|----------|--------|
| Buy-Shipping | `global_buy_shipping_*` | 13 |
| Co-Warehouse | `global_co_warehouse_*` | 4 |
| Self-Fulfilled | `global_self_fulfilled_*` | 5 |
| Tracking | `global_tracking_*` | 1 |

**未接入（相对 US）**：`temu.logistics.scanform.create`、`temu.logistics.scanform.get`、`temu.logistics.scanform.document.get`、`temu.logistics.candidate.scanform.list.get` — 请用 **`linkfox-temu-fulfillment-us`**（`site=us`）。

详见 [partner-global-catalog.md](./references/partner-global-catalog.md)。美国站请用 **`linkfox-temu-fulfillment-us`**；欧洲站请用 **`linkfox-temu-fulfillment-eu`**。

**网关**：

| 能力 | 方法 | 路径 |
|------|------|------|
| 履约 OpenAPI | POST | `https://tool-gateway.linkfox.com/temu/proxy` |
| 加签文件下载 | POST | `https://tool-gateway.linkfox.com/temu/fileDownload` |

## 相关 skill

| 场景 | skill |
|------|--------|
| 订单列表/详情/地址 | `linkfox-temu-order-global` |
| 取消订单 | `linkfox-temu-cancel-order-global` |
| 商品管理 | `linkfox-temu-manage-product-global` |
| 美国站履约（含 Scan Form） | `linkfox-temu-fulfillment-us` |
| 欧洲站履约 | `linkfox-temu-fulfillment-eu` |
| 退货退款 | `linkfox-temu-returns-refunds-global` |

## 默认参数

| 字段 | 默认 |
|------|------|
| site | `global` |
| managementType | `semi-managed` |
| tokenPurpose | `order-shipping` |

## Scripts（按域）

### Buy-Shipping（`global_buy_shipping_*`）

购标、面单、上门揽收等（**不含 Scan Form**）— 见 [apis/README.md](./references/apis/README.md)。

### Co-Warehouse（`global_co_warehouse_*`）

`bg.cooperativewarehouse.*` — 合作仓授权、提交/取消履约。

### Self-Fulfilled（`global_self_fulfilled_*`）

`bg.logistics.shipment.v2.*`、`shippingtype.update` 等 — 卖家自带运单号。

### Tracking（`global_tracking_*`）

`temu.track.trackinginfo.get`

### 通用

| 脚本 | 说明 |
|------|------|
| `temu_global_proxy.py` | 任意 `type` |
| `temu_global_file_download.py` | 加签文件下载 |

薄封装统一调用 **`_global_fulfillment_script.run_cli`**。

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

# Buy-Shipping 购标
python scripts/global_buy_shipping_logistics_shipment_create.py '{
  "accessToken": "TOKEN",
  "site": "global",
  "tokenPurpose": "order-shipping",
  "request": { }
}'

# 卖家自发货更新跟踪号
python scripts/global_self_fulfilled_logistics_shipment_shippingtype_update.py '{
  "accessToken": "TOKEN",
  "site": "global",
  "tokenPurpose": "order-shipping",
  "request": { "editPackageRequestList": [{ "packageSn": "PKG-1", "trackingNumber": "1Z..." }] }
}'
```

**Feedback：** `skillName`：`linkfox-temu-fulfillment-global`
