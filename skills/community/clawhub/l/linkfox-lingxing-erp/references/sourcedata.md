# 领星源数据接口参考

所有接口均为 POST 请求，域名：`https://openapi.lingxing.com`

通用参数说明：`sid` 为店铺id（来自 SellerLists 接口），`offset`/`length` 用于分页（默认0/1000）。

---

## AllOrders - 查询全量订单

**路径**: `/erp/sc/data/mws_report/allOrders`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| start_date | 是 | string | 开始日期 Y-m-d（左闭） |
| end_date | 是 | string | 结束日期 Y-m-d（右开） |
| date_type | 否 | int | 1下单日期（默认）/2亚马逊订单更新时间 |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: amazon_order_id, merchant_order_id, purchase_date, purchase_date_locale, order_status, shipment_date, last_updated_time

---

## FbaOrders - 查询FBA出库订单

**路径**: `/erp/sc/data/mws_report/fbaOrders`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| start_date | 是 | string | 开始日期 Y-m-d（左闭） |
| end_date | 是 | string | 结束日期 Y-m-d（右开） |
| date_type | 否 | int | 1下单日期（默认）/2配送日期 |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: amazon_order_id, shipment_id, shipment_item_id, amazon_order_item_id, purchase_date, shipment_date, payments_date, reporting_date

---

## RefundOrders - 查询退货订单

**路径**: `/erp/sc/data/mws_report/refundOrders`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| start_date | 是 | string | 开始时间 Y-m-d（左闭右开） |
| end_date | 是 | string | 结束时间 Y-m-d（左闭右开） |
| date_type | 否 | int | 1退货时间（默认）/2更新时间 |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: sid, order_id, local_sku, product_name, sku, asin, fnsku, quantity

---

## Transaction - 查询账务流水

**路径**: `/erp/sc/data/mws_report/transaction`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| event_date | 是 | string | 报表日期 Y-m-d（每月3日后支持查上月数据） |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: sid, report_date_month, date_str, date_locale, settlement_id, is_to_b, report_index

---

## ManageInventory - 查询库存管理快照

**路径**: `/erp/sc/data/mws_report/manageInventory`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: sku, fnsku, asin, product_name, condition, mfn_fulfillable_quantity, afn_listing_exists, afn_fulfillable_quantity, afn_reserved_quantity

---

## DailyInventory - 查询每日库存快照

**路径**: `/erp/sc/data/mws_report/dailyInventory`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id（欧洲传UK店铺，美国传US店铺） |
| event_date | 是 | string | 报表日期 Y-m-d |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: snapshot_date, fnsku, sku, product_name, quantity, fulfillment_center_id, detailed_disposition, country

---

## AfnFulfillableQuantity - 查询FBA可售库存

**路径**: `/erp/sc/data/mws_report/getAfnFulfillableQuantity`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: sid, seller_sku, fnsku, asin, condition_type, country, afn_fulfillable_quantity, gmt_modified

---

## ReservedInventory - 查询预留库存

**路径**: `/erp/sc/data/mws_report/reservedInventory`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: sku, fnsku, asin, product_name, reserved_qty, reserved_customerorders, reserved_fc_transfers, reserved_fc_processing

---

## RemovalLists - 查询移除订单报告

**路径**: `/erp/sc/data/fba_report/removalLists`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| start_date | 是 | string | 开始时间 Y-m-d（闭区间） |
| end_date | 是 | string | 结束时间 Y-m-d（开区间） |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: sid, uuid, order_id, request_date, shipment_date, sku, fnsku, disposition, quantity

---

## RemovalOrderListNew - 查询移除订单列表（新）

**路径**: `/erp/sc/routing/data/order/removalOrderListNew`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| start_date | 是 | string | 开始日期 Y-m-d（左闭） |
| end_date | 是 | string | 结束日期 Y-m-d（右开） |
| search_field_time | 是 | string | 时间类型：last_updated_date/request_date |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: seller_id, sid, region, request_date, order_id, order_type, order_status, last_updated_date

---

## RemovalShipmentList - 查询移除发货列表

**路径**: `/erp/sc/statistic/removalShipment/list`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 是 | string | 开始日期（发货日期，左闭右开） |
| end_date | 是 | string | 结束日期（发货日期，左闭右开） |
| sid | 否 | int | 店铺id（与seller_id二选一） |
| seller_id | 否 | string | 亚马逊店铺id |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: sid, mid, seller_id, seller_account_name, marketplace, order_id, uuid_new

---

## SourceRemovalOrders - 查询源移除订单

**路径**: `/erp/sc/data/mws_report/removalOrders`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| start_date | 是 | string | 更新时间开始 Y-m-d（左闭） |
| end_date | 是 | string | 更新时间结束 Y-m-d（右开） |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: request_date, order_id, order_type, order_status, last_updated_date, sku, fnsku, disposition, quantity

---

## AdjustmentList - 查询库存调整列表

**路径**: `/basicOpen/openapi/mwsReport/adjustmentList`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| offset | 是 | int | 分页偏移量，默认0 |
| length | 是 | int | 分页长度，默认20，上限10000 |
| start_date | 是 | string | 开始日期 Y-m-d（闭区间） |
| end_date | 是 | string | 结束日期 Y-m-d（闭区间） |
| sids | 否 | string | 店铺id，多个以英文逗号分隔 |
| search_field | 否 | string | 搜索字段：asin/msku/fnsku/item_name/transaction_item_id |
| search_value | 否 | string | 搜索值 |

**关键返回字段**: data>>sid, data>>report_date, data>>transaction_item_id, data>>fnsku, data>>msku, data>>asin

---

## getAmazonFulfilledShipmentsList - 查询FBA出货记录

**路径**: `/erp/sc/data/mws_report/getAmazonFulfilledShipmentsList`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| shipment_date_after | 是 | string | 发货时间开始 Y-m-d hh-mm-ss（区间支持7天） |
| shipment_date_before | 是 | string | 发货时间结束 Y-m-d hh-mm-ss |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: sid, amazon_order_id, merchant_order_id, shipment_id, shipment_item_id, purchase_date, shipment_date

---

## getFbaAgeList - 查询FBA库龄列表

**路径**: `/erp/sc/routing/fba/fbaStock/getFbaAgeList`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | string | 店铺id，多个以英文逗号分隔 |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: data>>list>>sid, data>>list>>snapshot_date, data>>list>>sku, data>>list>>fnsku, data>>list>>asin

---

## getFbaInventoryEventDetailList - 查询FBA库存事件明细

**路径**: `/erp/sc/data/mws_report/getFbaInventoryEventDetailList`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| snapshot_date_after | 是 | string | 快照开始日期 Y-m-d（区间支持7天） |
| snapshot_date_before | 是 | string | 快照结束日期 Y-m-d |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: sid, snapshot_date, snapshot_date_locale, transaction_type, fnsku, sku, asin

---

## v1getAmazonFulfilledShipmentsList - 查询FBA出货记录V1

**路径**: `/erp/sc/data/mws_report_v1/getAmazonFulfilledShipmentsList`

**参数**: 与 getAmazonFulfilledShipmentsList 相同

**关键返回字段**: 与 getAmazonFulfilledShipmentsList 相同，数据结构与参数一致

---

## v1getFbaInventoryEventDetailList - 查询FBA库存事件明细V1

**路径**: `/erp/sc/data/mws_report_v1/getFbaInventoryEventDetailList`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| snapshot_date_after | 是 | string | 快照开始日期 Y-m-d（区间支持7天） |
| snapshot_date_before | 是 | string | 快照结束日期 Y-m-d |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认1000，上限10000 |

**关键返回字段**: sid, snapshot_date, snapshot_date_locale, transaction_type, fnsku, msku, asin

---

## fbaExchangeOrderList - 查询FBA换货订单

**路径**: `/erp/sc/routing/data/order/fbaExchangeOrderList`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| start_date | 是 | string | 开始时间 Y-m-d（左闭） |
| end_date | 是 | string | 结束时间 Y-m-d（右开） |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: order_hash, sid, replacement_amazon_order_id, original_amazon_order_id, shipment_date, asin, seller_sku, fulfillment_center_id

---

## fbmReturnOrderList - 查询FBM退货订单

**路径**: `/erp/sc/routing/data/order/fbmReturnOrderList`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| start_date | 是 | string | 开始时间 Y-m-d（左闭） |
| end_date | 是 | string | 结束时间 Y-m-d（右开） |
| date_type | 否 | int | 1退货日期（默认）/2下单日期 |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: id, order_hash, sid, order_id, order_date, return_date, return_status, rma_id

---
