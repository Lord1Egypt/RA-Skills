# Partner EU — Fulfillment 接口目录（合一）

Partner Platform for EU **Fulfillment / 电商履行**：**Buy-Shipping**、**Co-Warehouse**、**Self-Fulfilled Shipments**、**Tracking**、**Self-Delivery POD**（共 **30** 个 `type`；其中 27 个与 US 版 `linkfox-temu-fulfillment-us` 对齐）。

文档根 `menu_code`（浏览器地址栏常见）：`7289390cfd724be4a196f11ebe45a896`。

本 skill 经 `temu_eu_proxy`（`POST /temu/proxy`）调用，默认 **`site=eu`**、**`tokenPurpose=order-shipping`**。

脚本前缀：`eu_buy_shipping_*`、`eu_co_warehouse_*`、`eu_self_fulfilled_*`、`eu_tracking_*`。

> EU Partner 各子菜单 `sub_menu_code` 请在 [partner-eu.temu.com](https://partner-eu.temu.com/documentation) 按 `type` 打开后补全。

## 已接入（30）

| sub_menu_code | type | 脚本 | 参数文档 |
|---------------|------|------|----------|
| — | `bg.logistics.warehouse.list.get` | `eu_buy_shipping_logistics_warehouse_list_get.py` | [apis/bg-logistics-warehouse-list-get.md](./apis/bg-logistics-warehouse-list-get.md) |
| — | `temu.logistics.shiplogisticstype.get` | `eu_buy_shipping_logistics_shiplogisticstype_get.py` | [apis/temu-logistics-shiplogisticstype-get.md](./apis/temu-logistics-shiplogisticstype-get.md) |
| — | `bg.logistics.shippingservices.get` | `eu_buy_shipping_logistics_shippingservices_get.py` | [apis/bg-logistics-shippingservices-get.md](./apis/bg-logistics-shippingservices-get.md) |
| — | `bg.logistics.shipment.create` | `eu_buy_shipping_logistics_shipment_create.py` | [apis/bg-logistics-shipment-create.md](./apis/bg-logistics-shipment-create.md) |
| — | `bg.logistics.shipment.result.get` | `eu_buy_shipping_logistics_shipment_result_get.py` | [apis/bg-logistics-shipment-result-get.md](./apis/bg-logistics-shipment-result-get.md) |
| — | `bg.logistics.shipment.update` | `eu_buy_shipping_logistics_shipment_update.py` | [apis/bg-logistics-shipment-update.md](./apis/bg-logistics-shipment-update.md) |
| — | `bg.logistics.shipment.document.get` | `eu_buy_shipping_logistics_shipment_document_get.py` | [apis/bg-logistics-shipment-document-get.md](./apis/bg-logistics-shipment-document-get.md) |
| — | `bg.order.unshipped.package.get` | `eu_buy_shipping_order_unshipped_package_get.py` | [apis/bg-order-unshipped-package-get.md](./apis/bg-order-unshipped-package-get.md) |
| — | `temu.logistics.label.list.get` | `eu_buy_shipping_logistics_label_list_get.py` | [apis/temu-logistics-label-list-get.md](./apis/temu-logistics-label-list-get.md) |
| — | `bg.logistics.shipped.package.confirm` | `eu_buy_shipping_logistics_shipped_package_confirm.py` | [apis/bg-logistics-shipped-package-confirm.md](./apis/bg-logistics-shipped-package-confirm.md) |
| — | `temu.logistics.candidate.scanform.list.get` | `eu_buy_shipping_logistics_candidate_scanform_list_get.py` | [apis/temu-logistics-candidate-scanform-list-get.md](./apis/temu-logistics-candidate-scanform-list-get.md) |
| — | `temu.logistics.scanform.create` | `eu_buy_shipping_logistics_scanform_create.py` | [apis/temu-logistics-scanform-create.md](./apis/temu-logistics-scanform-create.md) |
| — | `temu.logistics.scanform.get` | `eu_buy_shipping_logistics_scanform_get.py` | [apis/temu-logistics-scanform-get.md](./apis/temu-logistics-scanform-get.md) |
| — | `temu.logistics.scanform.document.get` | `eu_buy_shipping_logistics_scanform_document_get.py` | [apis/temu-logistics-scanform-document-get.md](./apis/temu-logistics-scanform-document-get.md) |
| — | `temu.logistics.shipment.pickup.reservation.create` | `eu_buy_shipping_logistics_shipment_pickup_reservation_create.py` | [apis/temu-logistics-shipment-pickup-reservation-create.md](./apis/temu-logistics-shipment-pickup-reservation-create.md) |
| — | `temu.logistics.shipment.pickup.reservation.result.get` | `eu_buy_shipping_logistics_shipment_pickup_reservation_result_get.py` | [apis/temu-logistics-shipment-pickup-reservation-result-get.md](./apis/temu-logistics-shipment-pickup-reservation-result-get.md) |
| — | `temu.logistics.shipment.pickup.reservation.cancel` | `eu_buy_shipping_logistics_shipment_pickup_reservation_cancel.py` | [apis/temu-logistics-shipment-pickup-reservation-cancel.md](./apis/temu-logistics-shipment-pickup-reservation-cancel.md) |
| — | `bg.cooperativewarehouse.provider.list` | `eu_co_warehouse_cooperativewarehouse_provider_list.py` | [apis/bg-cooperativewarehouse-provider-list.md](./apis/bg-cooperativewarehouse-provider-list.md) |
| — | `bg.cooperativewarehouse.token.authorization` | `eu_co_warehouse_cooperativewarehouse_token_authorization.py` | [apis/bg-cooperativewarehouse-token-authorization.md](./apis/bg-cooperativewarehouse-token-authorization.md) |
| — | `bg.cooperativewarehouse.fulfill.submit` | `eu_co_warehouse_cooperativewarehouse_fulfill_submit.py` | [apis/bg-cooperativewarehouse-fulfill-submit.md](./apis/bg-cooperativewarehouse-fulfill-submit.md) |
| — | `bg.cooperativewarehouse.fulfill.cancel` | `eu_co_warehouse_cooperativewarehouse_fulfill_cancel.py` | [apis/bg-cooperativewarehouse-fulfill-cancel.md](./apis/bg-cooperativewarehouse-fulfill-cancel.md) |
| — | `bg.logistics.companies.get` | `eu_self_fulfilled_logistics_companies_get.py` | [apis/bg-logistics-companies-get.md](./apis/bg-logistics-companies-get.md) |
| — | `bg.logistics.shipment.v2.confirm` | `eu_self_fulfilled_logistics_shipment_v2_confirm.py` | [apis/bg-logistics-shipment-v2-confirm.md](./apis/bg-logistics-shipment-v2-confirm.md) |
| — | `bg.logistics.shipment.v2.get` | `eu_self_fulfilled_logistics_shipment_v2_get.py` | [apis/bg-logistics-shipment-v2-get.md](./apis/bg-logistics-shipment-v2-get.md) |
| — | `bg.logistics.shipment.sub.confirm` | `eu_self_fulfilled_logistics_shipment_sub_confirm.py` | [apis/bg-logistics-shipment-sub-confirm.md](./apis/bg-logistics-shipment-sub-confirm.md) |
| — | `bg.logistics.shipment.shippingtype.update` | `eu_self_fulfilled_logistics_shipment_shippingtype_update.py` | [apis/bg-logistics-shipment-shippingtype-update.md](./apis/bg-logistics-shipment-shippingtype-update.md) |
| — | `temu.track.trackinginfo.get` | `eu_tracking_track_trackinginfo_get.py` | [apis/temu-track-trackinginfo-get.md](./apis/temu-track-trackinginfo-get.md) |
| `e7ada01f9b044cf98adc4e5a6ebcfd62` | `temu.logistics.self.delivery.pod.audit.result.get` | `eu_self_fulfilled_logistics_self_delivery_pod_audit_result_get.py` | [apis/temu-logistics-self-delivery-pod-audit-result-get.md](./apis/temu-logistics-self-delivery-pod-audit-result-get.md) |
| `39dce790742249f39998ee87eb75e5cf` | `temu.logistics.self.delivery.pod.upload` | `eu_self_fulfilled_logistics_self_delivery_pod_upload.py` | [apis/temu-logistics-self-delivery-pod-upload.md](./apis/temu-logistics-self-delivery-pod-upload.md) |
| `b42a002b6a3d42a58aa809cfc1ea14fd` | `temu.logistics.self.delivery.pod.upload.signature.query` | `eu_self_fulfilled_logistics_self_delivery_pod_upload_signature_query.py` | [apis/temu-logistics-self-delivery-pod-upload-signature-query.md](./apis/temu-logistics-self-delivery-pod-upload-signature-query.md) |

## 官方文档 URL

| type | URL |
|------|-----|
| `bg.logistics.warehouse.list.get` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `temu.logistics.shiplogisticstype.get` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `bg.logistics.shippingservices.get` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `bg.logistics.shipment.create` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `bg.logistics.shipment.result.get` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `bg.logistics.shipment.update` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `bg.logistics.shipment.document.get` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `bg.order.unshipped.package.get` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `temu.logistics.label.list.get` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `bg.logistics.shipped.package.confirm` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `temu.logistics.candidate.scanform.list.get` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `temu.logistics.scanform.create` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `temu.logistics.scanform.get` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `temu.logistics.scanform.document.get` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `temu.logistics.shipment.pickup.reservation.create` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `temu.logistics.shipment.pickup.reservation.result.get` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `temu.logistics.shipment.pickup.reservation.cancel` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `bg.cooperativewarehouse.provider.list` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `bg.cooperativewarehouse.token.authorization` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `bg.cooperativewarehouse.fulfill.submit` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `bg.cooperativewarehouse.fulfill.cancel` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `bg.logistics.companies.get` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `bg.logistics.shipment.v2.confirm` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `bg.logistics.shipment.v2.get` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `bg.logistics.shipment.sub.confirm` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `bg.logistics.shipment.shippingtype.update` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `temu.track.trackinginfo.get` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896 |
| `temu.logistics.self.delivery.pod.audit.result.get` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=e7ada01f9b044cf98adc4e5a6ebcfd62 |
| `temu.logistics.self.delivery.pod.upload` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=39dce790742249f39998ee87eb75e5cf |
| `temu.logistics.self.delivery.pod.upload.signature.query` | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=b42a002b6a3d42a58aa809cfc1ea14fd |

## 上游 OpenAPI（EU）

`POST` https://openapi-b-eu.temu.com/openapi/router（经 LinkFox 网关 `site=eu` 转发）

## 通用脚本

| 脚本 | 说明 |
|------|------|
| `temu_eu_proxy.py` | 任意 `type` + `params` |
| `temu_eu_file_download.py` | 加签文件下载 |

## 与其他 Temu skill 的关系

| 能力 | skill |
|------|--------|
| **履约/发货**（本 skill） | **`linkfox-temu-fulfillment-eu`** |
| 订单查询、地址、金额 | `linkfox-temu-order-eu` |
| 取消订单 | `linkfox-temu-cancel-order-eu` |
| 商品管理 | `linkfox-temu-manage-product-eu` |
| 价格 | `linkfox-temu-price-eu` |
| 美国站履约 | `linkfox-temu-fulfillment-us` |

## Token 说明

建议使用 **`tokenPurpose=order-shipping`**。详见 [access-token.md](./access-token.md)。
