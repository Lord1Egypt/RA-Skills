---
name: linkfox-temu-fulfillment-us
version: 1.0.0
category: product-sourcing
description: Temu 美国站电商履行/发货 API（合一）：Buy-Shipping购标面单、合作仓履约、卖家自发货、物流跟踪等27+接口。当用户提到 Temu US 发货、购标、Buy-Shipping、合作仓、自发货、tracking、scanform、shipment.create、order-shipping 时触发。订单用 linkfox-temu-order-us。
---

# Temu 美国站 — 电商履行 / 发货（Fulfillment）

本 skill（`linkfox-temu-fulfillment-us`）合并原 **Buy-Shipping**、**Co-Warehouse**、**Self-Fulfilled Shipments**、**Tracking** 四个 skill，覆盖 Partner US **Fulfillment** 域 **27** 个已接入 `type`。

| 域 | 脚本前缀 | 接口数 |
|----|----------|--------|
| Buy-Shipping | `us_buy_shipping_*` | 17 |
| Co-Warehouse | `us_co_warehouse_*` | 4 |
| Self-Fulfilled | `us_self_fulfilled_*` | 5 |
| Tracking | `us_tracking_*` | 1 |

详见 [partner-us-catalog.md](./references/partner-us-catalog.md)。

**网关**：

| 能力 | 方法 | 路径 |
|------|------|------|
| 履约 OpenAPI | POST | `https://tool-gateway.linkfox.com/temu/proxy` |
| 加签文件下载 | POST | `https://tool-gateway.linkfox.com/temu/fileDownload` |

## 相关 skill

| 场景 | skill |
|------|--------|
| 订单列表/详情/地址 | `linkfox-temu-order-us` |
| 取消订单 | `linkfox-temu-cancel-order-us` |
| 商品管理 | `linkfox-temu-manage-product-us` |
| 退货退款 | `linkfox-temu-returns-refunds-us` |
| 全球站履约 | `linkfox-temu-fulfillment-global`（无 Scan Form） |

## 默认参数

| 字段 | 默认 |
|------|------|
| site | `us` |
| managementType | `semi-managed` |
| tokenPurpose | `order-shipping` |

## Scripts（按域）

### Buy-Shipping（`us_buy_shipping_*`）

购标、面单、Scan Form、上门揽收等 — 见 [apis/README.md](./references/apis/README.md#buy-shipping购标面单scan-form)。

### Co-Warehouse（`us_co_warehouse_*`）

`bg.cooperativewarehouse.*` — 合作仓授权、提交/取消履约。

### Self-Fulfilled（`us_self_fulfilled_*`）

`bg.logistics.shipment.v2.*`、`shippingtype.update` 等 — 卖家自带运单号。

### Tracking（`us_tracking_*`）

`temu.track.trackinginfo.get`

### 通用

| 脚本 | 说明 |
|------|------|
| `temu_us_proxy.py` | 任意 `type` |
| `temu_us_file_download.py` | 加签文件下载 |

薄封装统一调用 **`_us_fulfillment_script.run_cli`**。

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

# Buy-Shipping 购标
python scripts/us_buy_shipping_logistics_shipment_create.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": { }
}'

# 卖家自发货更新跟踪号
python scripts/us_self_fulfilled_logistics_shipment_shippingtype_update.py '{
  "accessToken": "TOKEN",
  "request": { "editPackageRequestList": [{ "packageSn": "PKG-1", "trackingNumber": "1Z..." }] }
}'
```

**Feedback：** `skillName`：`linkfox-temu-fulfillment-us`
