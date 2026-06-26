# Fulfillment — 接口文档索引（Global）

每个 `type` 单独一份文档，经 `POST /temu/proxy` 调用（`site=global`）。

> 全球站不含 Scan Form 四类接口，见 [partner-global-catalog.md](./partner-global-catalog.md)。

## Buy-Shipping（购标/面单，13）

| type | 文档 |
|------|------|
| `bg.logistics.warehouse.list.get` | [bg-logistics-warehouse-list-get.md](./bg-logistics-warehouse-list-get.md) |
| `temu.logistics.shiplogisticstype.get` | [temu-logistics-shiplogisticstype-get.md](./temu-logistics-shiplogisticstype-get.md) |
| `bg.logistics.shippingservices.get` | [bg-logistics-shippingservices-get.md](./bg-logistics-shippingservices-get.md) |
| `bg.logistics.shipment.create` | [bg-logistics-shipment-create.md](./bg-logistics-shipment-create.md) |
| `bg.logistics.shipment.result.get` | [bg-logistics-shipment-result-get.md](./bg-logistics-shipment-result-get.md) |
| `bg.logistics.shipment.update` | [bg-logistics-shipment-update.md](./bg-logistics-shipment-update.md) |
| `bg.logistics.shipment.document.get` | [bg-logistics-shipment-document-get.md](./bg-logistics-shipment-document-get.md) |
| `bg.order.unshipped.package.get` | [bg-order-unshipped-package-get.md](./bg-order-unshipped-package-get.md) |
| `temu.logistics.label.list.get` | [temu-logistics-label-list-get.md](./temu-logistics-label-list-get.md) |
| `bg.logistics.shipped.package.confirm` | [bg-logistics-shipped-package-confirm.md](./bg-logistics-shipped-package-confirm.md) |
| `temu.logistics.shipment.pickup.reservation.create` | [temu-logistics-shipment-pickup-reservation-create.md](./temu-logistics-shipment-pickup-reservation-create.md) |
| `temu.logistics.shipment.pickup.reservation.result.get` | [temu-logistics-shipment-pickup-reservation-result-get.md](./temu-logistics-shipment-pickup-reservation-result-get.md) |
| `temu.logistics.shipment.pickup.reservation.cancel` | [temu-logistics-shipment-pickup-reservation-cancel.md](./temu-logistics-shipment-pickup-reservation-cancel.md) |

## Co-Warehouse（合作仓，4）

| type | 文档 |
|------|------|
| `bg.cooperativewarehouse.provider.list` | [bg-cooperativewarehouse-provider-list.md](./bg-cooperativewarehouse-provider-list.md) |
| `bg.cooperativewarehouse.token.authorization` | [bg-cooperativewarehouse-token-authorization.md](./bg-cooperativewarehouse-token-authorization.md) |
| `bg.cooperativewarehouse.fulfill.submit` | [bg-cooperativewarehouse-fulfill-submit.md](./bg-cooperativewarehouse-fulfill-submit.md) |
| `bg.cooperativewarehouse.fulfill.cancel` | [bg-cooperativewarehouse-fulfill-cancel.md](./bg-cooperativewarehouse-fulfill-cancel.md) |

## Self-Fulfilled Shipments（卖家自发货，5）

| type | 文档 |
|------|------|
| `bg.logistics.companies.get` | [bg-logistics-companies-get.md](./bg-logistics-companies-get.md) |
| `bg.logistics.shipment.v2.confirm` | [bg-logistics-shipment-v2-confirm.md](./bg-logistics-shipment-v2-confirm.md) |
| `bg.logistics.shipment.v2.get` | [bg-logistics-shipment-v2-get.md](./bg-logistics-shipment-v2-get.md) |
| `bg.logistics.shipment.sub.confirm` | [bg-logistics-shipment-sub-confirm.md](./bg-logistics-shipment-sub-confirm.md) |
| `bg.logistics.shipment.shippingtype.update` | [bg-logistics-shipment-shippingtype-update.md](./bg-logistics-shipment-shippingtype-update.md) |

## Tracking（物流跟踪，1）

| type | 文档 |
|------|------|
| `temu.track.trackinginfo.get` | [temu-track-trackinginfo-get.md](./temu-track-trackinginfo-get.md) |
