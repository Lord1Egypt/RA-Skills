# 领星FBA接口参考

所有接口均为 POST 请求，域名：`https://openapi.lingxing.com`

---

## fbaShipmentList - 查询FBA发货单列表

**路径**: `/erp/sc/data/fba_report/shipmentList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| start_date | 否 | string | 开始日期，格式 Y-m-d |
| end_date | 否 | string | 结束日期 |
| status | 否 | string | 发货单状态 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: sid, shipment_id, shipment_name, status, destination_fulfillment_center_id, label_prep_type, create_date, item_list[seller_sku/fnsku/asin/quantity_shipped]

---

## fbaReceivedInventory - 查询FBA已收货库存

**路径**: `/erp/sc/data/fba_report/receivedInventory`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| start_date | 否 | string | 开始日期，格式 Y-m-d |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: sid, shipment_id, fnsku, asin, seller_sku, quantity_shipped, quantity_received, quantity_in_case

---

## shipmentPlanLists - 查询FBA发货计划列表

**路径**: `/erp/sc/data/fba_report/shipmentPlanLists`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| start_date | 否 | string | 开始日期，格式 Y-m-d |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: sid, plan_id, plan_name, status, create_date, item_list[seller_sku/asin/quantity]

---

## getFbaProductList - 查询FBA产品列表

**路径**: `/erp/sc/routing/fba/shipment/getFbaProductList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| search_field | 否 | string | 搜索字段：seller_sku/asin/fnsku |
| search_value | 否 | string | 搜索值 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: sid, seller_sku, asin, fnsku, product_name, local_sku, condition, prep_type

---

## getInboundShipmentList - 查询FBA入库发货单列表

**路径**: `/erp/sc/routing/storage/shipment/getInboundShipmentList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| start_date | 否 | string | 开始日期，格式 Y-m-d |
| end_date | 否 | string | 结束日期 |
| status | 否 | string | 发货单状态 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: sid, shipment_id, shipment_name, status, fulfillment_center_id, create_date, total_quantity

---

## getInboundShipmentListMwsDetailList - 查询FBA入库发货单商品明细列表

**路径**: `/erp/sc/routing/storage/shipment/getInboundShipmentListMwsDetailList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| shipment_id | 是 | string | 发货单ID |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: shipment_id, seller_sku, fnsku, asin, quantity_shipped, quantity_received, quantity_in_case

---

## shipFromAddressList - 查询FBA发货地址列表

**路径**: `/erp/sc/routing/fba/shipment/shipFromAddressList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |

**关键返回字段**: address_id, name, address_line1, city, state_or_province_code, country_code, postal_code

---

## boxInfo - 查询FBA箱规信息

**路径**: `/erp/sc/routing/fba/shipment/boxInfo`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| shipment_id | 是 | string | 发货单ID |

**关键返回字段**: shipment_id, box_list[box_no/length/width/height/weight/quantity/item_list]

---

## getHeadLogisticsFeeTypes - 查询头程费用类型

**路径**: `/erp/sc/routing/fba/shipment/getHeadLogisticsFeeTypes`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 否 | int | 店铺ID |

**关键返回字段**: fee_type_id, fee_type_name, currency

---

## getSeaTrackSupplierCarriers - 查询海运跟踪供应商承运商

**路径**: `/erp/sc/routing/fba/shipment/getSeaTrackSupplierCarriers`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| supplier_id | 否 | int | 供应商ID |

**关键返回字段**: carrier_id, carrier_name, supplier_id

---

## querySTATaskList - 查询STA入库计划列表

**路径**: `/amzStaServer/openapi/inbound-plan/page`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| status | 否 | string | 计划状态 |
| start_date | 否 | string | 开始日期，格式 Y-m-d |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: inbound_plan_id, sid, status, create_date, total_boxes, total_quantity, marketplace_id

---

## staTaskDetail - 查询STA入库计划详情

**路径**: `/amzStaServer/openapi/inbound-plan/detail`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| inbound_plan_id | 是 | string | 入库计划ID |
| sid | 是 | int | 店铺ID |

**关键返回字段**: inbound_plan_id, status, marketplace_id, shipment_list[shipment_id/status/destination/quantity], item_list[seller_sku/fnsku/asin/quantity]

---

## getInboundShipmentListMwsDetail - 查询FBA入库发货单商品明细

**路径**: `/erp/sc/routing/storage/shipment/getInboundShipmentListMwsDetail`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| shipment_id | 是 | string | 发货单ID |

**关键返回字段**: shipment_id, seller_sku, fnsku, asin, quantity_shipped, quantity_received, prep_detail_list
