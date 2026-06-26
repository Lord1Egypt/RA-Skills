# Fulfillment — 接口文档索引（EU）

每个 `type` 单独一份文档，经 `POST /temu/proxy` 调用。

## Buy-Shipping（购标/面单/Scan Form）

每个 `type` 单独一份文档，经 `POST /temu/proxy` 调用。网关与鉴权见 [../api.md](../api.md)；目录与 `sub_menu_code` 见 [../partner-eu-catalog.md](../partner-eu-catalog.md)。

## 仓库 / 物流基础

| type | 文档 |
|------|------|
| `bg.logistics.warehouse.list.get` | [bg-logistics-warehouse-list-get.md](./bg-logistics-warehouse-list-get.md) |

## 查价 / 购标 / 面单

| type | 文档 |
|------|------|
| `bg.logistics.shippingservices.get` | [bg-logistics-shippingservices-get.md](./bg-logistics-shippingservices-get.md) |
| `bg.logistics.shipment.create` | [bg-logistics-shipment-create.md](./bg-logistics-shipment-create.md) |
| `bg.logistics.shipment.result.get` | [bg-logistics-shipment-result-get.md](./bg-logistics-shipment-result-get.md) |
| `bg.logistics.shipment.update` | [bg-logistics-shipment-update.md](./bg-logistics-shipment-update.md) |
| `bg.logistics.shipment.document.get` | [bg-logistics-shipment-document-get.md](./bg-logistics-shipment-document-get.md) |
| `temu.logistics.shiplogisticstype.get` | [temu-logistics-shiplogisticstype-get.md](./temu-logistics-shiplogisticstype-get.md) |
| `temu.logistics.label.list.get` | [temu-logistics-label-list-get.md](./temu-logistics-label-list-get.md) |
| `temu.logistics.candidate.scanform.list.get` | [temu-logistics-candidate-scanform-list-get.md](./temu-logistics-candidate-scanform-list-get.md) |
| `temu.logistics.scanform.create` | [temu-logistics-scanform-create.md](./temu-logistics-scanform-create.md) |
| `temu.logistics.scanform.document.get` | [temu-logistics-scanform-document-get.md](./temu-logistics-scanform-document-get.md) |
| `temu.logistics.scanform.get` | [temu-logistics-scanform-get.md](./temu-logistics-scanform-get.md) |

## 订单 / 未发货包裹 / 确认发货

| type | 文档 |
|------|------|
| `bg.order.unshipped.package.get` | [bg-order-unshipped-package-get.md](./bg-order-unshipped-package-get.md) |
| `bg.logistics.shipped.package.confirm` | [bg-logistics-shipped-package-confirm.md](./bg-logistics-shipped-package-confirm.md) |

## 上门揽收预约（Pickup Reservation）

| type | 文档 |
|------|------|
| `temu.logistics.shipment.pickup.reservation.create` | [temu-logistics-shipment-pickup-reservation-create.md](./temu-logistics-shipment-pickup-reservation-create.md) |
| `temu.logistics.shipment.pickup.reservation.result.get` | [temu-logistics-shipment-pickup-reservation-result-get.md](./temu-logistics-shipment-pickup-reservation-result-get.md) |
| `temu.logistics.shipment.pickup.reservation.cancel` | [temu-logistics-shipment-pickup-reservation-cancel.md](./temu-logistics-shipment-pickup-reservation-cancel.md) |

## 取消 / 改单（待补充）

| type | 文档 |
|------|------|
| _待用户提供 Partner 文档_ | — |

## 其他（待补充）

| type | 文档 |
|------|------|
| _待用户提供 Partner 文档_ | — |

## Co-Warehouse（合作仓履约）

每个 `type` 单独一份文档，经 `POST /temu/proxy` 调用。网关与鉴权见 [../api.md](../api.md)；目录与 `sub_menu_code` 见 [../partner-eu-catalog.md](../partner-eu-catalog.md)。

> **Semi-managed only**：本 skill 仅适用于半托管（`managementType=semi-managed`）合作仓履约场景。

## 合作仓服务商 / 授权

| type | 文档 |
|------|------|
| `bg.cooperativewarehouse.provider.list` | [bg-cooperativewarehouse-provider-list.md](./bg-cooperativewarehouse-provider-list.md) |
| `bg.cooperativewarehouse.token.authorization` | [bg-cooperativewarehouse-token-authorization.md](./bg-cooperativewarehouse-token-authorization.md) |

## 合作仓履约

| type | 文档 |
|------|------|
| `bg.cooperativewarehouse.fulfill.submit` | [bg-cooperativewarehouse-fulfill-submit.md](./bg-cooperativewarehouse-fulfill-submit.md) |
| `bg.cooperativewarehouse.fulfill.cancel` | [bg-cooperativewarehouse-fulfill-cancel.md](./bg-cooperativewarehouse-fulfill-cancel.md) |
| `bg.cooperativewarehouse.fulfill.query` | _待接入_ |

## SKU 关系

| type | 文档 |
|------|------|
| `temu.cooperativewarehouse.skurelationship.create` | _待接入_ |
| `temu.cooperativewarehouse.skurelationship.get` | _待接入_ |

## Self-Fulfilled Shipments（卖家自发货）

每个 `type` 单独一份文档，经 `POST /temu/proxy` 调用。网关与鉴权见 [../api.md](../api.md)；目录与 `sub_menu_code` 见 [../partner-eu-catalog.md](../partner-eu-catalog.md)。

## 发货 / 确认发货

| type | 文档 |
|------|------|
| `bg.logistics.shipment.v2.confirm` | [bg-logistics-shipment-v2-confirm.md](./bg-logistics-shipment-v2-confirm.md) |
| `bg.logistics.shipment.sub.confirm` | [bg-logistics-shipment-sub-confirm.md](./bg-logistics-shipment-sub-confirm.md) |
| `bg.logistics.shipment.shippingtype.update` | [bg-logistics-shipment-shippingtype-update.md](./bg-logistics-shipment-shippingtype-update.md) |

## 物流 / 面单 / 包裹

| type | 文档 |
|------|------|
| `bg.logistics.companies.get` | [bg-logistics-companies-get.md](./bg-logistics-companies-get.md) |
| `bg.logistics.shipment.v2.get` | [bg-logistics-shipment-v2-get.md](./bg-logistics-shipment-v2-get.md) |

## 其他（待补充）

| type | 文档 |
|------|------|
| _待用户提供 Partner 文档_ | — |

## Tracking（物流跟踪）

每个 `type` 单独一份文档，经 `POST /temu/proxy` 调用。网关与鉴权见 [../api.md](../api.md)；目录与 `sub_menu_code` 见 [../partner-eu-catalog.md](../partner-eu-catalog.md)。

## 物流跟踪

| type | 文档 |
|------|------|
| `temu.track.trackinginfo.get` | [temu-track-trackinginfo-get.md](./temu-track-trackinginfo-get.md) |

## 其他（待补充）

| type | 文档 |
|------|------|
| _待用户提供 Partner 文档_ | — |

## Self-Delivery POD（EU）

| type | 文档 |
|------|------|
| `temu.logistics.self.delivery.pod.audit.result.get` | [temu-logistics-self-delivery-pod-audit-result-get.md](./temu-logistics-self-delivery-pod-audit-result-get.md) |
| `temu.logistics.self.delivery.pod.upload` | [temu-logistics-self-delivery-pod-upload.md](./temu-logistics-self-delivery-pod-upload.md) |
| `temu.logistics.self.delivery.pod.upload.signature.query` | [temu-logistics-self-delivery-pod-upload-signature-query.md](./temu-logistics-self-delivery-pod-upload-signature-query.md) |
