# 领星仓库接口参考

所有接口均为 POST 请求（除标注外），域名：`https://openapi.lingxing.com`

---

## warehouseLists - 查询仓库列表

**路径**: `/erp/sc/data/local_inventory/warehouse`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| keyword | 否 | string | 关键词（仓库名称） |
| wid | 否 | int | 仓库ID |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: wid, warehouse_name, warehouse_type, country_code, status, create_time

---

## warehouseStatement - 查询仓库库存流水

**路径**: `/erp/sc/routing/data/local_inventory/wareHouseStatement`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| wid | 否 | int | 仓库ID |
| sku | 否 | string | SKU |
| start_date | 否 | string | 开始时间，格式 Y-m-d |
| end_date | 否 | string | 结束时间 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: wid, warehouse_name, sku, product_name, statement_type, quantity, create_time, order_sn

---

## warehouseStatementNew - 查询仓库库存流水（新版）

**路径**: `/erp/sc/routing/inventoryLog/WareHouseInventory/wareHouseCenterStatement`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| wid | 否 | int | 仓库ID |
| sku | 否 | string | SKU |
| start_date | 否 | string | 开始时间，格式 Y-m-d |
| end_date | 否 | string | 结束时间 |
| statement_type | 否 | int | 流水类型 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: wid, warehouse_name, sku, product_name, statement_type, quantity, cost, create_time, order_sn

---

## inventoryDetails - 查询库存明细

**路径**: `/erp/sc/routing/data/local_inventory/inventoryDetails`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| wid | 否 | int | 仓库ID |
| sku | 否 | string | SKU |
| search_field | 否 | string | 搜索字段：sku/product_name/spu |
| search_value | 否 | string | 搜索值 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: wid, warehouse_name, sku, product_name, spu, available_quantity, locked_quantity, total_quantity, unit_cost, total_cost

---

## inventoryBinDetails - 查询仓位库存明细

**路径**: `/erp/sc/routing/data/local_inventory/inventoryBinDetails`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| wid | 是 | int | 仓库ID |
| bin_code | 否 | string | 仓位编码 |
| sku | 否 | string | SKU |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: wid, bin_code, bin_type, sku, product_name, available_quantity, locked_quantity

---

## wareHouseBinStatement - 查询仓位库存流水

**路径**: `/erp/sc/routing/data/local_inventory/wareHouseBinStatement`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| wid | 否 | int | 仓库ID |
| bin_code | 否 | string | 仓位编码 |
| sku | 否 | string | SKU |
| start_date | 否 | string | 开始时间，格式 Y-m-d |
| end_date | 否 | string | 结束时间 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: wid, bin_code, sku, product_name, statement_type, quantity, create_time, order_sn

---

## warehouseBin - 查询仓位列表

**路径**: `/erp/sc/routing/data/local_inventory/warehouseBin`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| wid | 是 | int | 仓库ID |
| bin_code | 否 | string | 仓位编码 |
| bin_type | 否 | int | 仓位类型 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: bin_id, bin_code, bin_type, bin_type_name, wid, warehouse_name, status, create_time

---

## fbaStock - 查询FBA库存

**路径**: `/erp/sc/routing/fba/fbaStock/fbaList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| search_field | 否 | string | 搜索字段：seller_sku/asin/fnsku |
| search_value | 否 | string | 搜索值 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: sid, seller_sku, asin, fnsku, condition, afn_fulfillable_quantity, afn_unsellable_quantity, afn_reserved_quantity, afn_inbound_working_quantity, afn_total_quantity

---

## fbaStockV2 - 查询FBA库存明细（V2）

**路径**: `/basicOpen/openapi/storage/fbaWarehouseDetail`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| fnsku | 否 | string | FNSKU，多个逗号分隔 |
| msku | 否 | string | MSKU，多个逗号分隔 |
| asin | 否 | string | ASIN，多个逗号分隔 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: sid, seller_sku, asin, fnsku, fulfillment_center_id, detailed_disposition, quantity, cost

---

## awdWarehouseDetail - 查询AWD仓库库存明细

**路径**: `/basicOpen/openapi/storage/awdWarehouseDetail`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| msku | 否 | string | MSKU，多个逗号分隔 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: sid, seller_sku, asin, sku_quantity, sku_sellable_quantity, sku_unsellable_quantity

---

## getBatchDetailList - 查询批次明细列表

**路径**: `/erp/sc/routing/data/local_inventory/getBatchDetailList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| wid | 否 | int | 仓库ID |
| sku | 否 | string | SKU |
| batch_number | 否 | string | 批次号，多个逗号分隔 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: batch_number, wid, warehouse_name, sku, product_name, quantity, unit_cost, total_cost, production_date, expiry_date

---

## getBatchStatementList - 查询批次流水列表

**路径**: `/erp/sc/routing/data/local_inventory/getBatchStatementList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| statement_type_list | 否 | string | 批次流水主类型ID，多个逗号分隔（19=其他入库，22=采购入库，37=FBA出库，38=FBM出库等） |
| search_field | 否 | string | 搜索字段：sku/msku/fnsku/product_name/order_sn/batch_number等 |
| search_value | 否 | string | 搜索值 |
| wid_list | 否 | string | 仓库ID，多个逗号分隔 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20，上限400 |

**关键返回字段**: batch_number, wid, warehouse_name, sku, product_name, statement_type, quantity, cost, create_time, order_sn

---

## getReceiveGoodRecords - 查询收货记录

**路径**: `/erp/sc/routing/owms/inbound/getReceiveGoodRecords`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| overseas_order_no | 否 | string | 备货单单号（不支持批量） |
| start_date | 否 | string | 收货开始时间，格式 Y-m-d，闭区间 |
| end_date | 否 | string | 收货结束时间，开区间 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认500 |

**关键返回字段**: overseas_order_no, receive_date, wid, warehouse_name, item_list[sku/product_name/quantity_received]

---

## purchaseReceiptOrderList - 查询收货单列表

**路径**: `/erp/sc/routing/deliveryReceipt/PurchaseReceiptOrder/getOrderList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| date_type | 否 | int | 时间类型：1=预计到货，2=收货，3=创建，4=更新 |
| start_date | 否 | string | 开始时间，格式 Y-m-d |
| end_date | 否 | string | 结束时间 |
| order_sns | 否 | string | 收货单号，多个逗号分隔 |
| status | 否 | int | 状态：10=待收货，40=已完成 |
| wid | 否 | string | 仓库ID，多个逗号分隔 |
| order_type | 否 | int | 收货类型：1=采购订单，2=委外订单 |
| qc_status | 否 | string | 质检状态：0=未质检，1=部分质检，2=完成质检 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认200，上限500 |

**关键返回字段**: order_sn, purchase_order_sn, status, wid, warehouse_name, arrive_date, qc_status, item_list[sku/quantity_expected/quantity_received]

---

## receiptOrderQcList - 查询收货质检单列表

**路径**: `/erp/sc/routing/deliveryReceipt/ReceiptOrderQc/getOrderList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| date_type | 否 | int | 时间类型：1=质检，2=收货，3=创建 |
| start_date | 否 | string | 开始时间 |
| end_date | 否 | string | 结束时间 |
| qc_sns | 否 | string | 质检单号，多个逗号分隔 |
| status | 否 | string | 状态：0=待质检，1=已质检，2=已免检，10=已质检撤销，20=已免检撤销 |
| wid | 否 | string | 仓库ID，多个逗号分隔 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认200，上限500 |

**关键返回字段**: qc_sn, receipt_order_sn, status, wid, warehouse_name, qc_date, item_list[sku/quantity_qc/quantity_qualified/quantity_unqualified]

---

## wmsOrderList - 查询WMS出库单列表

**路径**: `/erp/sc/routing/wms/order/wmsOrderList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid_arr | 否 | array | 店铺ID列表 |
| status_arr | 否 | array | 状态：1=物流下单，2=发货中，3=已发货，4=已删除 |
| logistics_status_arr | 否 | array | 物流状态 |
| platform_order_no_arr | 否 | array | 平台单号 |
| order_number_arr | 否 | array | 系统单号 |
| time_type | 否 | string | 时间类型：create_at/delivered_at/stock_delivered_at/update_at |
| start_date | 否 | string | 开始日期，格式 Y-m-d |
| end_date | 否 | string | 结束日期 |
| page | 否 | int | 分页页码，默认1 |
| page_size | 否 | int | 分页长度，默认20，上限200 |

**关键返回字段**: order_number, platform_order_no, sid, status, logistics_status, logistics_type_name, create_time, delivered_time, item_list[sku/quantity]

---

## wmsOrderDetail - 查询WMS出库单详情

**路径**: `/basicOpen/wmsOrder/getWmsOrdersByOrderNumbers`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| isPrintCenter | 是 | int | 是否需要拣货信息：1=是，0=否 |
| orderNumbers | 是 | string | 系统单号，多个逗号分隔 |

**关键返回字段**: order_number, platform_order_no, sid, status, logistics_type_name, create_time, item_list[sku/product_name/quantity/bin_code], packing_list（当isPrintCenter=1时）

---

## overseaWarehouseMatchList - 查询海外仓配对列表

**路径**: `/basicOpen/overseaWarehouseSetting/matchList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| wpId | 是 | int | 三方服务商ID |
| twIds | 否 | string | 三方仓ID，多个逗号分隔 |
| isMatched | 否 | int | 是否配对：0=否，1=是 |
| keyword | 否 | string | 关键词（sku/品名/第三方产品名/产品编码） |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页大小，默认20，上限200 |

**关键返回字段**: local_sku, local_product_name, third_party_sku, third_party_product_name, is_matched, wid

---

## overSeasStockDetail - 查询海外仓备货单详情

**路径**: `/basicOpen/overSeaWarehouse/stockOrder/detail`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| overseas_order_no | 是 | string | 备货单号 |

**关键返回字段**: overseas_order_no, status, create_time, wid, warehouse_name, item_list[sku/product_name/quantity_plan/quantity_received]

---

## getProcessOrderLists - 查询加工/拆分单列表

**路径**: `/erp/sc/routing/inventoryReceipt/StorageProcess/getOrderLists`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| type | 是 | int | 单据类型：1=加工单，2=拆分单 |
| offset | 是 | int | 分页偏移量，默认0 |
| length | 是 | int | 分页长度，默认500 |
| wid | 否 | string | 仓库ID，多个逗号分隔 |
| process_sn | 否 | string | 加工单号，多个逗号分隔 |
| status | 否 | int | 状态：0=待配货，1=待完成，2=已完成 |
| search_field_time | 否 | string | 时间维度：create_time/finish_time/update_time |
| start_date | 否 | string | 开始时间，格式 Y-m-d |
| end_date | 否 | string | 结束时间 |

**关键返回字段**: process_sn, type, status, wid, warehouse_name, create_time, finish_time, input_list[sku/quantity], output_list[sku/quantity]

---

## getStorageAdjustOrderList - 查询库存调整单列表

**路径**: `/erp/sc/routing/inventoryReceipt/StorageAdjustment/getStorageAdjustOrderList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| search_date_type | 否 | int | 时间类型：1=创建，2=调整，3=更新 |
| start_date | 否 | string | 开始日期，格式 Y-m-d |
| end_date | 否 | string | 结束日期 |
| order_sn | 否 | string | 调整单号，多个逗号分隔 |
| adjust_status | 否 | int | 状态：5=待提交，10=待调整，20=已完成，30=已删除，121=待审批，122=已驳回 |
| wid | 否 | string | 仓库ID，多个逗号分隔 |
| type | 否 | int | 调整类型：0=数量，1=换标，2=SKU |
| page | 否 | int | 当前页码，默认1 |
| page_size | 否 | int | 分页条数，默认20 |

**关键返回字段**: order_sn, status, type, wid, warehouse_name, create_time, adjust_time, item_list[sku/quantity_before/quantity_after]

---

## getStorageAllocationList - 查询调拨单列表

**路径**: `/erp/sc/routing/inventoryReceipt/StorageAllocation/getStorageAllocationList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| wid | 否 | string | 出库仓库ID，多个逗号分隔 |
| to_wid | 否 | string | 入库仓库ID，多个逗号分隔 |
| search_date_type | 否 | int | 时间类型：1=创建，2=调拨，3=完成，4=更新 |
| start_date | 否 | string | 开始日期，格式 Y-m-d |
| end_date | 否 | string | 结束日期 |
| page | 否 | int | 当前页码，默认1 |
| page_size | 否 | int | 分页条数，默认15 |

**关键返回字段**: order_sn, status, wid, warehouse_name, to_wid, to_warehouse_name, create_time, allocation_time, item_list[sku/quantity]

---

## returnList - 查询退货单列表

**路径**: `/pb/mp/returns/v2/list`
**令牌桶容量**: 10

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_time | 是 | string | 开始时间，格式 Y-m-d H:i:s |
| end_time | 是 | string | 结束时间 |
| offset | 是 | int | 页码（非偏移量，传1返回第一页） |
| length | 是 | int | 每页记录数 |
| time_type | 否 | string | 时间类型：updateTime=更新时间（默认创建时间） |
| platform_code | 否 | array | 平台code列表 |
| sales_type | 否 | int | 退货类型：1=买家退货，2=物流商退货 |
| status | 否 | array | 状态：-1=异常，1=待提交，2=待审批，3=待收货，4=已作废，5=已完成，6=导入中 |
| store_id | 否 | array | 店铺ID列表 |
| wid | 否 | array | 仓库ID列表 |

**关键返回字段**: return_order_no, platform_order_no, store_id, status, wid, warehouse_name, create_time, item_list[sku/quantity/return_reason]

---

## inboundGetOrders - 查询入库单列表

**路径**: `/erp/sc/routing/storage/inbound/getOrders`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| wid | 否 | int | 仓库ID |
| search_field_time | 否 | string | 时间筛选类型：create_time/opt_time/increment_time |
| start_date | 否 | string | 开始时间，格式 Y-m-d（更新时间支持 Y-m-d H:i:s） |
| end_date | 否 | string | 结束时间 |
| order_sn | 否 | string | 入库单号，多个逗号分隔 |
| inbound_idempotent_code | 否 | string | 客户参考单号，多个逗号分隔 |
| status | 否 | int | 状态：10=待提交，20=待入库，40=已完成，50=已撤销，121=待审批，122=已驳回 |
| type | 否 | int | 入库类型：-1=其他入库（全部自定义），1=其他（非自定义），2=采购入库，3=调拨入库，4=赠品入库，26=退货入库，27=移除入库 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20，上限200 |

**关键返回字段**: order_sn, type, status, wid, warehouse_name, create_time, inbound_time, item_list[sku/quantity_plan/quantity_actual]

---

## outboundGetOrders - 查询出库单列表

**路径**: `/erp/sc/routing/storage/outbound/getOrders`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| wid | 否 | string | 仓库ID |
| search_field_time | 否 | string | 时间筛选：create_time/opt_time/increment_time |
| start_date | 否 | string | 开始时间，格式 Y-m-d（更新时间支持 Y-m-d H:i:s） |
| end_date | 否 | string | 结束时间 |
| order_sn | 否 | string | 出库单号，多个逗号分隔 |
| idempotent_code | 否 | string | 客户参考号，多个逗号分隔 |
| status | 否 | int | 状态：10=待提交，30=待出库，40=已完成，50=已撤销，121=待审批，122=已驳回 |
| type | 否 | int | 出库类型：11=其他，12=FBA，14=退货，15=调拨，16=WFS，17=Temu |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20，上限200 |

**关键返回字段**: order_sn, type, status, wid, warehouse_name, create_time, outbound_time, item_list[sku/quantity_plan/quantity_actual]

---

## removalInboundList - 查询移除入库单列表

**路径**: `/erp/sc/routing/owms/removalInbound/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| status | 否 | int | 状态：1=待提交未提交，2=待提交提交中，3=待提交失败，4=待收货未收货，5=待收货异常，6=已完成，7=已作废 |
| start_date | 否 | string | 发货日期开始，双闭区间 |
| end_date | 否 | string | 发货日期结束 |
| order_no | 否 | array | 移除入库单号列表 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20，上限1000 |

**关键返回字段**: order_no, status, shipment_date, wid, warehouse_name, item_list[fnsku/msku/quantity]

---

## matchSkuList - 查询海外仓SKU配对列表

**路径**: `/erp/sc/routing/owms/inbound/matchSkuList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| wid | 是 | string | 仓库ID，多个逗号分隔 |
| is_matched | 否 | int | 是否配对：0=未配对，1=已配对（空=全部） |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: wid, warehouse_name, local_sku, local_product_name, overseas_sku, is_matched

---

## listInbound - 查询海外仓备货单列表

**路径**: `/erp/sc/routing/owms/inbound/listInbound`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| status | 否 | int | 状态：10=待审核，20=已驳回，30=待配货，40=待发货，50=待收货，51=已撤销，60=已完成 |
| sub_status | 否 | int | 子状态（仅待收货状态）：0=全部，1=未收货，2=部分收货 |
| s_wid | 否 | array | 发货仓库ID |
| r_wid | 否 | array | 收货仓库ID |
| overseas_order_no | 否 | string | 备货单号 |
| date_type | 否 | string | 时间类型：delivery_time/create_time/receive_time/update_time |
| create_time_from | 否 | string | 查询开始日期，格式 Y-m-d |
| create_time_to | 否 | string | 查询结束日期 |
| is_delete | 否 | int | 是否删除：0=未删除（默认），1=已删除，2=全部 |
| page | 否 | int | 当前页码，默认1 |
| page_size | 否 | int | 分页数量，最大50，默认20 |

**关键返回字段**: overseas_order_no, status, s_wid, r_wid, create_time, delivery_time, receive_time, item_list[sku/quantity_plan/quantity_received]

---

## checkGetOrderList - 查询盘点单列表

**路径**: `/erp/sc/routing/inventoryReceipt/InventoryCheck/getOrderList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| wid | 否 | string | 仓库ID，多个逗号分隔 |
| check_type | 否 | string | 盘点类型：1=整仓，2=SKU，3=仓位，4=SKU+仓位 |
| date_field | 否 | string | 时间类型：create_date/check_date |
| start_date | 否 | string | 开始日期，格式 Y-m-d |
| end_date | 否 | string | 结束日期 |
| search_field | 否 | string | 搜索字段：order_sn/create_user/check_user/remark |
| search_value | 否 | string | 搜索值 |
| status | 否 | int | 状态：10=待盘点，20=预锁，30=盘点中，40=已盘点，121=待审核，122=已驳回，123=通过，124=作废 |
| page | 否 | int | 分页页码，默认1 |
| page_size | 否 | int | 分页长度，默认20 |

**关键返回字段**: order_sn, check_type, status, wid, warehouse_name, create_time, check_date, create_user, check_user

---

## checkGetOrderDetail - 查询盘点单详情

**路径**: `/erp/sc/routing/inventoryReceipt/InventoryCheck/getOrderDetail`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| order_sn | 是 | string | 盘点单号 |
| search_field | 否 | string | 搜索字段：sku/fnsku/product_name/whb_code_text/whb_type_text |
| search_value | 否 | string | 搜索值 |
| sort_field | 否 | string | 排序字段：book_inventory/actual_inventory/different_count |
| sort_type | 否 | string | 排序：desc（默认）/asc |
| page | 否 | int | 分页页码，默认1 |
| page_size | 否 | int | 分页长度，默认20 |

**关键返回字段**: order_sn, status, check_type, wid, warehouse_name, product_list[sku/fnsku/product_name/book_inventory/actual_inventory/different_count]

---

## getPackingData - 查询备货单装箱数据 (GET)

**路径**: `/erp/sc/routing/owms/inbound/getPackingData`
**请求方式**: GET
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| overseas_order_no | 是 | string | 备货单号 |

**关键返回字段**: overseas_order_no, box_list[box_no/length/width/height/weight/item_list[sku/quantity]]

---

## qualityInspectionOrderDetail - 查询质检单详情

**路径**: `/basicOpen/qualityInspectionOrder/detail`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| qc_sn | 是 | string | 质检单号 |

**关键返回字段**: qc_sn, status, wid, warehouse_name, create_time, qc_time, item_list[sku/product_name/quantity_qc/quantity_qualified/quantity_unqualified/unqualified_reason]
