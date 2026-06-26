# 领星销售查询接口参考

所有接口均为 POST 请求（除标注外），域名：`https://openapi.lingxing.com`

---

## orderDetail - 查询亚马逊订单详情

**路径**: `/erp/sc/data/mws/orderDetail`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| order_id | 是 | string | 亚马逊订单号，多个用英文逗号分隔，上限200 |

**关键返回字段**: amazon_order_id, sid, order_status, order_total_amount, currency, fulfillment_channel, is_return_order, is_replaced_order, is_replacement_order, purchase_date_local, shipment_date, item_list[seller_sku/asin/order_item_id/quantity_ordered/quantity_shipped/item_price_amount/profit]

---

## refundOrder - 订单退款

**路径**: `/basicOpen/openapi/salesOrder/refundOrder`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | number | 店铺id |
| amazonOrderId | 是 | string | 亚马逊订单ID |
| purchaseDateLocal | 是 | string | 订购时间，格式 Y-m-d H:i:s |
| data | 否 | array | 商品退款列表 |
| data>>orderItemId | 是 | string | 商品行id |
| data>>asin | 是 | string | ASIN |
| data>>sellerSku | 是 | string | MSKU |
| data>>title | 是 | string | 商品名称 |
| data>>quantityOrdered | 是 | number | 下单数量 |
| data>>quantityShipped | 是 | number | 到货数量 |
| data>>reason | 是 | string | 退款原因（CustomerReturn/GeneralAdjustment） |
| data>>itemList | 否 | array | 退款费用项目列表 |
| data>>itemList>>type | 是 | string | 费用类型（Principal/Tax/Shipping等） |
| data>>itemList>>currencyCode | 是 | string | 货币编码 |
| data>>itemList>>returnAmount | 是 | string | 本次申请退款金额 |
| data>>itemRefundTotal | 是 | string | 商品退款合计 |

**关键返回字段**: code=0 表示成功

> **注意**: 写操作，谨慎调用。亚马逊限制：同一订单含多商品时无法仅退某商品。

---

## productList - 查询刊登结果

**路径**: `/listing/publish/openapi/amazon/product/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| record_unique_id | 否 | int | 批次唯一ID |
| sku | 否 | string | SKU |
| store_id | 否 | int | 店铺ID |
| operate_time | 否 | object | 操作时间范围 |
| operate_time>>start | 否 | string | 开始时间 |
| operate_time>>end | 否 | string | 结束时间 |

**关键返回字段**: record_unique_id, store_id, sku, status（0=处理中/1=成功/2=失败）, failure_reason, warning, operate_time, finish_time, operationType（0=刊登新品/1=更新已有商品）

---

## fbmOrderList - 查询亚马逊自发货订单列表

**路径**: `/erp/sc/routing/order/Order/getOrderList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | string | 店铺sid，多个用英文逗号分隔 |
| order_status | 否 | string | 订单状态，多个逗号分隔：2=已发货，3=未付款，4=待审核，5=待发货，6=已取消 |
| page | 否 | int | 页码，默认1 |
| length | 否 | int | 分页长度，默认100 |
| start_time | 否 | string | 订购时间开始，格式 Y-m-d H:i:s |
| end_time | 否 | string | 订购时间结束 |

**关键返回字段**: order_number, status, order_from, country_code, purchase_time, logistics_type_name, logistics_provider_name, wid, warehouse_name, platform_list

---

## fbmOrderDetail - 查询亚马逊自发货订单详情

**路径**: `/erp/sc/routing/order/Order/getOrderDetail`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| order_number | 是 | string | 系统单号 |

**关键返回字段**: order_number, status, platform_list, country_code, purchase_time, logistics_type_name, warehouse_name, item_list[sku/msku/quantity/price]

---

## mcfOrderList - 查询多渠道订单列表

**路径**: `/order/amzod/api/orderList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sids | 否 | array | 店铺ID列表 |
| start_date | 否 | string | 开始日期，格式 Y-m-d |
| end_date | 否 | string | 结束日期 |
| order_status | 否 | string | 订单状态 |
| offset | 是 | int | 分页偏移量（与length同时必填） |
| length | 是 | int | 每页条数（与offset同时必填） |

**关键返回字段**: amazon_order_id, seller_fulfillment_order_id, order_status, sid, purchase_date_local, item_list[asin/msku/quantity]

---

## orderProductInformation - 查询多渠道订单商品信息

**路径**: `/order/amzod/api/orderDetails/productInformation`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| order_info | 是 | array | 订单信息列表，上限200 |
| order_info>>sid | 是 | int | 店铺ID |
| order_info>>seller_fulfillment_order_id | 是 | string | 卖家订单号 |

**关键返回字段**: seller_fulfillment_order_id, item_list[asin/msku/quantity/status]

---

## getPrices - 查询Listing价格

**路径**: `/listing/listing/open/api/listing/getPrices`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| data | 是 | array | 查询列表，上限500 |
| data>>sid | 是 | int | 店铺ID |
| data>>msku | 是 | string | MSKU |

**关键返回字段**: sid, msku, asin, price, landed_price, business_price, quantity_price_type, currency

---

## orderLogisticsInformation - 查询多渠道订单物流信息

**路径**: `/order/amzod/api/orderDetails/logisticsInformation`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| order_info | 是 | array | 订单信息列表，上限200 |
| order_info>>sid | 是 | int | 店铺ID |
| order_info>>seller_fulfillment_order_id | 是 | string | 卖家订单号 |

**关键返回字段**: seller_fulfillment_order_id, tracking_number, carrier_code, shipment_status, estimated_arrival_date

---

## getMerchantShippingGroup - 查询卖家配送模板

**路径**: `/basicOpen/openapi/publish/manage/getMerchantShippingGroup`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |

**关键返回字段**: shipping_group_id, name, type, marketplace_id

---

## getFulfillmentResult - 查询多渠道订单履行结果

**路径**: `/pb/mp/order/getFulfillmentResult`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| order_info | 是 | array | 订单信息列表 |
| order_info>>sid | 是 | int | 店铺ID |
| order_info>>seller_fulfillment_order_id | 是 | string | 卖家订单号 |

**关键返回字段**: seller_fulfillment_order_id, fulfillment_order_status, package_list[tracking_number/carrier_code/shipment_date]

---

## queryProductList - 查询刊登产品列表

**路径**: `/listing/publish/openapi/amazon/product/search`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sku | 否 | string | SKU |
| store_id | 否 | int | 店铺ID |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数 |

**关键返回字段**: record_unique_id, sku, store_id, status, asin, operate_time, finish_time

---

## publishManageCategoryRoot - 查询亚马逊分类根节点

**路径**: `/basicOpen/openapi/publish/manage/categoryRoot`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| marketplace_id | 是 | string | 市场ID |

**关键返回字段**: node_id, name, has_children

---

## publishManageCategoryChildren - 查询亚马逊分类子节点

**路径**: `/basicOpen/openapi/publish/manage/categoryChildren`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| marketplace_id | 是 | string | 市场ID |
| node_id | 是 | string | 父节点ID |

**关键返回字段**: node_id, name, has_children, is_leaf

---

## publishManageGetProductType - 查询亚马逊产品类型

**路径**: `/basicOpen/openapi/publish/manage/getProductType`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| marketplace_id | 是 | string | 市场ID |
| node_id | 否 | string | 分类节点ID |
| keyword | 否 | string | 搜索关键词 |

**关键返回字段**: product_type, display_name

---

## adjustPriceManual - 手动调价

**路径**: `/basicOpen/module/adjustPrice/AdjustPriceManual`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| msku | 是 | string | MSKU |
| price | 是 | number | 调整后价格 |
| currency | 否 | string | 货币代码 |

**关键返回字段**: code=0 表示成功

> **注意**: 写操作，会修改Listing价格，谨慎调用。

---

## afterSaleList - 查询售后单列表

**路径**: `/erp/sc/routing/amzod/order/afterSaleList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 否 | int | 店铺ID |
| start_date | 否 | string | 开始时间，格式 Y-m-d |
| end_date | 否 | string | 结束时间 |
| status | 否 | int | 状态 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: after_sale_no, amazon_order_id, sid, status, type, create_time, item_list[asin/msku/quantity]

---

## fbaFeeDifferenceList - 查询FBA费用差异订单列表

**路径**: `/basicOpen/openapi/sale/fbaFeeDifference/order/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sids | 否 | array | 店铺ID列表 |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: amazon_order_id, sid, actual_fee, expected_fee, fee_difference, dispute_status

---

## fbaFeeDifferenceMskuList - 查询FBA费用差异MSKU列表

**路径**: `/basicOpen/openapi/sale/fbaFeeDifference/msku/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sids | 否 | array | 店铺ID列表 |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: msku, asin, sid, total_difference, order_count

---

## globalTagPageList - 查询全局标签列表

**路径**: `/basicOpen/globalTag/listing/page/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| keyword | 否 | string | 关键词 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: tag_id, tag_name, tag_color, create_time

---

## listingOperateLogPageList - 查询Listing操作日志

**路径**: `/basicOpen/listingManage/listingOperateLog/pageList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 否 | int | 店铺ID |
| asin | 否 | string | ASIN |
| msku | 否 | string | MSKU |
| start_date | 否 | string | 开始时间 |
| end_date | 否 | string | 结束时间 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: log_id, sid, asin, msku, operate_type, operate_content, operate_time, operator

---

## promotionListingList - 查询Listing促销活动列表

**路径**: `/basicOpen/promotion/listingList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| asin | 否 | string | ASIN |
| msku | 否 | string | MSKU |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: asin, msku, promotion_type, promotion_id, start_date, end_date, discount

---

## promotionListingDetailCoupon - 查询Listing优惠券促销详情

**路径**: `/basicOpen/promotion/listingDetailCoupon`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| promotion_id | 是 | string | 促销活动ID |

**关键返回字段**: promotion_id, name, status, start_date, end_date, discount_type, discount_value, asin_list

---

## promotionListingDetailManage - 查询Listing促销（满减）详情

**路径**: `/basicOpen/promotion/listingDetailManage`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| promotion_id | 是 | string | 促销活动ID |

**关键返回字段**: promotion_id, name, status, start_date, end_date, discount_details, asin_list

---

## promotionListingDetailPrimeDiscount - 查询Listing专享折扣详情

**路径**: `/basicOpen/promotion/listingDetailPrimeDiscount`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| promotion_id | 是 | string | 促销活动ID |

**关键返回字段**: promotion_id, name, status, start_date, end_date, discount_value, eligible_asin_list

---

## promotionListingDetailSecKill - 查询Listing秒杀详情

**路径**: `/basicOpen/promotion/listingDetailSecKill`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| promotion_id | 是 | string | 促销活动ID |

**关键返回字段**: promotion_id, name, status, start_date, end_date, discount_value, asin_list

---

## promotionalActivitiesCouponList - 查询优惠券促销活动列表

**路径**: `/basicOpen/promotionalActivities/coupon/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| status | 否 | string | 状态 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: promotion_id, name, status, start_date, end_date, discount_type, claimed_count

---

## promotionalActivitiesManageList - 查询满减促销活动列表

**路径**: `/basicOpen/promotionalActivities/manage/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: promotion_id, name, status, start_date, end_date, discount_type

---

## promotionalActivitiesSecKillList - 查询秒杀活动列表

**路径**: `/basicOpen/promotionalActivities/secKill/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: promotion_id, name, status, start_date, end_date, discount_percent

---

## promotionalActivitiesVipDiscountList - 查询VIP折扣活动列表

**路径**: `/basicOpen/promotionalActivities/vipDiscount/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: promotion_id, name, status, start_date, end_date, discount_value

---

## queryListingRelationTagList - 查询Listing关联标签列表

**路径**: `/basicOpen/listingManage/queryListingRelationTagList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| asin | 否 | string | ASIN |
| msku | 否 | string | MSKU |
| tag_id | 否 | int | 标签ID |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: asin, msku, tag_id, tag_name

---

## promotionCouponAllDetailBatch - 批量查询优惠券促销全量详情

**路径**: `/promotionApi/open/promotion/couponAllDetailBatch`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| promotion_ids | 是 | array | 促销活动ID列表，上限20 |

**关键返回字段**: promotion_id, name, status, start_date, end_date, discount_type, discount_value, asin_list, claimed_count

---

## promotionManagementAllDetailBatch - 批量查询满减促销全量详情

**路径**: `/promotionApi/open/promotion/managementAllDetailBatch`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| promotion_ids | 是 | array | 促销活动ID列表，上限20 |

**关键返回字段**: promotion_id, name, status, start_date, end_date, discount_type, asin_list

---

## promotionPrimeDiscountAllDetailBatch - 批量查询专享折扣全量详情

**路径**: `/promotionApi/open/promotion/primeDiscountAllDetailBatch`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| promotion_ids | 是 | array | 促销活动ID列表，上限20 |

**关键返回字段**: promotion_id, name, status, start_date, end_date, discount_value, eligible_asin_list

---

## promotionSecKillAllDetailBatch - 批量查询秒杀全量详情

**路径**: `/promotionApi/open/promotion/secKillAllDetailBatch`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| promotion_ids | 是 | array | 促销活动ID列表，上限20 |

**关键返回字段**: promotion_id, name, status, start_date, end_date, discount_percent, asin_list
