# 领星采购接口参考

所有接口均为 POST 请求，域名：`https://openapi.lingxing.com`

---

## purchaseOrderList - 查询采购订单列表

**路径**: `/erp/sc/routing/data/local_inventory/purchaseOrderList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 否 | string | 开始日期，格式 Y-m-d |
| end_date | 否 | string | 结束日期 |
| date_type | 否 | int | 时间类型：1=创建时间，2=预计到货时间 |
| status | 否 | int | 状态：1=待提交，2=待审核，3=待收货，4=部分收货，5=已完成，6=已作废 |
| purchase_plan_sn | 否 | string | 采购计划号 |
| order_sn | 否 | string | 采购单号，多个逗号分隔 |
| wid | 否 | int | 仓库ID |
| buyer_id | 否 | int | 采购员ID |
| supplier_id | 否 | int | 供应商ID |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: order_sn, status, create_time, estimated_arrival_date, supplier_name, wid, warehouse_name, total_amount, currency, item_list[sku/product_name/quantity/price]

---

## supplier - 查询供应商列表

**路径**: `/erp/sc/data/local_inventory/supplier`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| keyword | 否 | string | 关键词（供应商名称/编码） |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: supplier_id, supplier_name, supplier_code, contact_name, phone, email, status, create_time

---

## changeOrderList - 查询采购变更单列表

**路径**: `/erp/sc/routing/purchase/purchaseChangeOrder/changeOrderList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 否 | string | 开始日期，格式 Y-m-d |
| end_date | 否 | string | 结束日期 |
| status | 否 | int | 状态：1=待审核，2=已通过，3=已驳回 |
| order_sn | 否 | string | 采购单号 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: change_order_sn, purchase_order_sn, status, create_time, change_type, change_content, operator

---

## getOrders - 查询委外采购订单列表

**路径**: `/erp/sc/routing/purchase/purchaseOutsourceOrder/getOrders`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 否 | string | 开始日期，格式 Y-m-d |
| end_date | 否 | string | 结束日期 |
| status | 否 | int | 状态 |
| order_sn | 否 | string | 委外单号，多个逗号分隔 |
| wid | 否 | int | 仓库ID |
| supplier_id | 否 | int | 供应商ID |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: order_sn, status, create_time, supplier_name, wid, warehouse_name, total_amount, currency, item_list[sku/product_name/quantity/price]

---

## getPurchasePlans - 查询采购计划列表

**路径**: `/erp/sc/routing/data/local_inventory/getPurchasePlans`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 否 | string | 开始日期，格式 Y-m-d |
| end_date | 否 | string | 结束日期 |
| status | 否 | int | 状态：1=待提交，2=待审核，3=采购中，4=已完成，5=已作废 |
| plan_sn | 否 | string | 计划单号，多个逗号分隔 |
| buyer_id | 否 | int | 采购员ID |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: plan_sn, status, create_time, buyer_name, total_sku_count, total_quantity, item_list[sku/product_name/plan_quantity/purchase_quantity]

---

## getPurchaseReturnOrderList - 查询采购退货单列表

**路径**: `/erp/sc/routing/purchase/purchase_return_order/getPurchaseReturnOrderList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 否 | string | 开始日期，格式 Y-m-d |
| end_date | 否 | string | 结束日期 |
| status | 否 | int | 状态 |
| order_sn | 否 | string | 退货单号，多个逗号分隔 |
| supplier_id | 否 | int | 供应商ID |
| wid | 否 | int | 仓库ID |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: return_order_sn, purchase_order_sn, status, create_time, supplier_name, wid, warehouse_name, total_amount, currency, item_list[sku/product_name/return_quantity/price]

---

## purchaserLists - 查询采购员列表

**路径**: `/erp/sc/routing/data/purchaser/lists`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| keyword | 否 | string | 关键词（采购员名称） |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: buyer_id, buyer_name, email, status
