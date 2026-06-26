---
name: linkfox-temu-fulfillment-eu
version: 1.0.0
category: product-sourcing
description: Temu 欧洲站电商履行/发货 API（合一）：Buy-Shipping购标面单、合作仓履约、卖家自发货、物流跟踪、自配送POD上传与审核等30个接口。当用户提到 Temu EU 发货、购标、POD、proof of delivery、self delivery pod、合作仓、自发货、tracking、order-shipping 时触发。订单用 linkfox-temu-order-eu。
---

# Temu 欧洲站 — 电商履行 / 发货（Fulfillment）

本 skill（`linkfox-temu-fulfillment-eu`）合并原 **Buy-Shipping**、**Co-Warehouse**、**Self-Fulfilled Shipments**、**Tracking** 四个 skill，覆盖 Partner EU **Fulfillment** 域 **30** 个已接入 `type`。

| 域 | 脚本前缀 | 接口数 |
|----|----------|--------|
| Buy-Shipping | `eu_buy_shipping_*` | 17 |
| Co-Warehouse | `eu_co_warehouse_*` | 4 |
| Self-Fulfilled | `eu_self_fulfilled_*` | 5 |
| Tracking | `eu_tracking_*` | 1 |
| Self-Delivery POD | `eu_self_fulfilled_*pod*` | 3 |

详见 [partner-eu-catalog.md](./references/partner-eu-catalog.md)。

**网关**：

| 能力 | 方法 | 路径 |
|------|------|------|
| 履约 OpenAPI | POST | `https://tool-gateway.linkfox.com/temu/proxy` |
| 加签文件下载 | POST | `https://tool-gateway.linkfox.com/temu/fileDownload` |

## 相关 skill

| 场景 | skill |
|------|--------|
| 订单列表/详情/地址 | `linkfox-temu-order-eu` |
| 取消订单 | `linkfox-temu-cancel-order-eu` |
| 商品管理 | `linkfox-temu-manage-product-eu` |
| 退货退款 | `linkfox-temu-returns-refunds-eu` |
| 美国站履约/发货 | `linkfox-temu-fulfillment-us` |
| 全球站履约 | `linkfox-temu-fulfillment-global`（无 Scan Form） |

## 默认参数

| 字段 | 默认 |
|------|------|
| site | `eu` |
| managementType | `semi-managed` |
| tokenPurpose | `order-shipping` |

## Scripts（按域）

### Buy-Shipping（`eu_buy_shipping_*`）

购标、面单、Scan Form、上门揽收等 — 见 [apis/README.md](./references/apis/README.md#buy-shipping购标面单scan-form)。

### Co-Warehouse（`eu_co_warehouse_*`）

`bg.cooperativewarehouse.*` — 合作仓授权、提交/取消履约。

### Self-Fulfilled（`eu_self_fulfilled_*`）

`bg.logistics.shipment.v2.*`、`shippingtype.update` 等 — 卖家自带运单号。

### Tracking（`eu_tracking_*`）

`temu.track.trackinginfo.get`

### Self-Delivery POD（`eu_self_fulfilled_*pod*`）

- `temu.logistics.self.delivery.pod.upload.signature.query`
- `temu.logistics.self.delivery.pod.upload`
- `temu.logistics.self.delivery.pod.audit.result.get`

### 通用

| 脚本 | 说明 |
|------|------|
| `temu_eu_proxy.py` | 任意 `type` |
| `temu_eu_file_download.py` | 加签文件下载 |

薄封装统一调用 **`_eu_fulfillment_script.run_cli`**。

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

# Buy-Shipping 购标
python scripts/eu_buy_shipping_logistics_shipment_create.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": { }
}'

# 卖家自发货更新跟踪号
python scripts/eu_self_fulfilled_logistics_shipment_shippingtype_update.py '{
  "accessToken": "TOKEN",
  "request": { "editPackageRequestList": [{ "packageSn": "PKG-1", "trackingNumber": "1Z..." }] }
}'
```

**Feedback：** `skillName`：`linkfox-temu-fulfillment-eu`
