# 领星 VC 接口参考

所有接口均为 POST 请求，域名：`https://openapi.lingxing.com`

---

## vcOrderPageList - 查询 VC 订单列表

**路径**: `/basicOpen/platformOrder/vcOrder/pageList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| purchase_order_type | 是 | array | 订单类型：0=DF，1=PO，2=DI |
| vc_store_ids | 否 | array | VC 店铺ID |
| search_field_time | 否 | string | 1=订购时间，2=要求发货时间，3=订单更新时间 |
| start_date | 否 | string | 开始时间，Y-m-d，间隔不超过90天 |
| end_date | 否 | string | 结束时间，Y-m-d |
| search_field | 否 | string | purchase_order_number/asin/local_name/customer_order_number/vendor_product_id |
| search_value | 否 | array | 搜索值 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20，上限200 |

**关键返回字段**: purchase_order_number, customer_order_number, purchase_order_type, purchase_order_process_state, currency_code, focus_party_id, shipment_confirm_status

---

## vcOrderPoDetail - 查询 VC 订单详情（PO）

**路径**: `/basicOpen/platformOrder/vcOrderPo/detail`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| local_po_number | 是 | string | 本地 PO 号（来自 vcOrderPageList 的 local_po_number） |

**关键返回字段**: purchase_order_date, currency_code, delivery_window_start, remark, items[item_name/asin/vendor_product_id/ordered_quantity/unit_cost]

---

## vcOrderDfDetail - 查询 VC 订单详情（DF）

**路径**: `/basicOpen/platformOrder/vcOrderDf/detail`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| vc_store_id | 是 | string | VC 店铺ID |
| purchase_order_number | 是 | string | 订单编号 |

**关键返回字段**: purchase_order_date, related_warehouse_id, is_pslip_required, message_to_customer, remark, items

---

## vcDeliverPageList - 查询 VC 发货单列表

**路径**: `/basicOpen/openapi/getInvoice/page/list`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| shipmentType | 是 | int | 1=DF，2=PO，3=DI |
| sids | 否 | array | 店铺ID |
| wid | 否 | int | 国家ID |
| status | 否 | int | 0=全部，5=待配货，10=待出库，15=已完成，100=已作废 |
| createTimeStartTime | 否 | string | 创建日期开始 |
| createTimeEndTime | 否 | string | 创建日期结束 |
| offset | 否 | int | 偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: list[orderNo, shipmentTime, shipmentType, sourceType], count

---

## vcDeliverDetail - 查询 VC 发货单详情

**路径**: `/basicOpen/openapi/getInvoice/detail`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| orderNo | 是 | string | 发货单号 |

**关键返回字段**: invoice[shippingWid, createUser, estimatedPickupTime, items]

---

## listingManageVcListingPageList - 查询 VC Listing 列表

**路径**: `/basicOpen/listingManage/vcListing/pageList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| vc_store_ids | 否 | array | VC 店铺ID |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20，上限200 |

**关键返回字段**: msku, local_sku, asin, title, status, classification_rank, display_group_rank, reviews_num

---

## platformAuthVcSellerPageList - 查询 VC 店铺列表

**路径**: `/basicOpen/platformAuth/vcSeller/pageList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20，上限200 |

**关键返回字段**: vc_store_id, region_name, seller_name, auth_status

---
