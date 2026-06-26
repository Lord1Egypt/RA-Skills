# 领星统计报表接口参考

所有接口均为 POST 请求（除标注外），域名：`https://openapi.lingxing.com`

---

## amazonReportExportTask - 下载亚马逊报告

**路径**: `/basicOpen/report/amazonReportExportTask`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| region | 是 | string | 店铺所在地区：na=北美，eu=欧洲，fe=远东 |
| seller_id | 是 | string | 亚马逊店铺ID |
| report_document_id | 是 | string | 报告文档ID（由reportQueryReportExportTask获取） |

**关键返回字段**: url（亚马逊报告下载链接）, report_document_id

---

## asinDailyLists - 查询ASIN每日数据

**路径**: `/erp/sc/data/sales_report/asinDailyLists`
**令牌桶容量**: 5

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| event_date | 是 | string | 报表日期（站点时间），格式 Y-m-d |
| asin_type | 否 | int | 查询维度：1=asin（默认），2=msku |
| type | 否 | int | 类型：1=销售额（默认），2=销量，3=订单量 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: sid, r_date, currency_code, seller_sku, asin, sessions, unit_session_percentage, units_ordered, ordered_product_sales, total_order_items

---

## asinList - 查询ASIN销售统计

**路径**: `/erp/sc/data/sales_report/asinList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| start_date | 是 | string | 开始日期，格式 Y-m-d，闭区间 |
| end_date | 是 | string | 结束日期，开区间 |
| asin_type | 否 | int | 产品表现维度：0=asin（默认），1=父asin |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: sid, asin, price, sessions, units_ordered, ordered_product_sales, conversion_rate, buy_box_percentage

---

## asinListNew - 查询ASIN销售统计（新版）

**路径**: `/bd/productPerformance/openApi/asinList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | object | 店铺ID（单店铺传字符串，多店铺传数组），上限200 |
| start_date | 是 | string | 开始日期，格式 YYYY-MM-DD，双闭区间，最长92天 |
| end_date | 是 | string | 结束日期 |
| offset | 是 | int | 分页偏移量 |
| length | 是 | int | 分页长度，最大10000 |
| sort_field | 是 | string | 排序字段（volume/order_items/amount等） |
| sort_type | 是 | string | 排序方式：desc/asc |
| summary_field | 是 | string | 汇总行维度：asin/parent_asin/msku/sku |
| search_field | 否 | string | 搜索字段：asin/parent_asin/msku/local_sku/item_name |
| search_value | 否 | array | 搜索值，最多50个 |
| mid | 否 | int | 站点ID |
| currency_code | 否 | string | 货币类型，支持USD/CNY |
| extend_search | 否 | array | 表头筛选条件 |

**关键返回字段**: list[parent_asins/asin/msku/volume/order_items/amount/b2b_volume/promotion_volume/avg_volume]

---

## fbaStorageFeeLongTerm - 查询FBA长期仓储费

**路径**: `/erp/sc/data/fba_report/storageFeeLongTerm`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| start_date | 是 | string | 收费日期，左闭区间，格式 Y-m-d |
| end_date | 是 | string | 收费日期，右开区间 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: sid, snapshot_date, sku, fnsku, asin, condition, quantity_charged_12_mo_long_term_storage_fee, per_unit_volume, currency, 12_mo_long_term_storage_fee

---

## fbaStorageFeeMonth - 查询FBA月度仓储费

**路径**: `/erp/sc/data/fba_report/storageFeeMonth`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| month | 是 | string | 收费月份，格式 Y-m |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: sid, asin, fnsku, product_name, fulfillment_center, country, longest_side, median_side, shortest_side, weight, item_volume, storage_utilization_ratio, quantity_charged, estimated_monthly_storage_fee, currency

---

## fbaStockAggregateListNew - 查询FBA库存汇总（新版）

**路径**: `/cost/center/openApi/fba/gather/query`
**令牌桶容量**: 10

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| seller_id | 是 | array | 亚马逊店铺ID列表 |
| start_date | 是 | string | 统计起始月份，格式 Y-m |
| end_date | 是 | string | 统计结束月份，格式 Y-m |
| offset | 是 | int | 分页偏移量，默认0 |
| length | 是 | int | 分页长度，默认15 |

**关键返回字段**: current, size, total, start_date, end_date, list[seller_id/asin/fnsku/quantity/cost]

---

## fbaStockDetailListNew - 查询FBA库存明细（新版）

**路径**: `/cost/center/openApi/fba/detail/query`
**令牌桶容量**: 10

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| seller_id | 是 | array | 亚马逊店铺ID列表 |
| start_date | 是 | string | 开始日期，格式 Y-m |
| end_date | 是 | string | 结束日期，格式 Y-m |
| offset | 是 | int | 分页偏移量，默认0 |
| length | 是 | int | 分页长度，默认15，最大2100 |

**关键返回字段**: total, start_date, end_date, day_interval, amount_type, list[seller_id/msku/asin/quantity/cost]

---

## fbaStockReportList - 查询FBA库存报表列表

**路径**: `/erp/sc/routing/fba/fbaStockReport/getList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_month | 否 | string | 开始月份，格式 Y-m，默认当前月 |
| end_month | 否 | string | 截止月份，默认当前月 |
| seller_id | 否 | string | 亚马逊店铺ID |
| dimention | 否 | int | 数据维度：1=汇总，2=明细（默认） |
| attribute | 否 | int | 可售状态：0=不可售，1=可售，2=全部（默认）|
| offset | 否 | int | 分页偏移量（明细维度生效），默认0 |
| length | 否 | int | 分页长度（明细维度生效），默认20，上限5000 |

**关键返回字段**: ware_house_name, asin, sku, fnsku, sku_name, quantity, unit_cost, total_cost

---

## localAggregateList - 查询本地仓库存汇总

**路径**: `/erp/sc/routing/inventoryLog/WareHouseReport/getLocalWareHouseSummaryList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 是 | string | 开始时间，格式 Y-m-d |
| end_date | 是 | string | 结束时间 |
| sys_wid | 否 | int | 仓库ID，多个逗号分隔 |

**关键返回字段**: sys_wid, ware_house_name, day_early_count, day_early_cost, purchase_in_count, fba_out_count, fbm_out_count, allocation_in_count, allocation_out_count, day_end_count

---

## localAggregateListNew - 查询本地仓库存汇总（新版）

**路径**: `/inventory/center/openapi/storageReport/local/aggregate/list`
**令牌桶容量**: 3

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 是 | string | 开始时间，格式 Y-m-d |
| end_date | 是 | string | 结束时间 |
| sys_wid | 否 | int | 仓库ID，多个逗号分隔 |

**关键返回字段**: sys_wid, ware_house_name, product_count, allocation_in_cost, allocation_in_count, purchase_in_count, purchase_in_cost, day_end_count, day_end_cost

---

## localDetailList - 查询本地仓库存明细

**路径**: `/erp/sc/routing/inventoryLog/WareHouseReport/getLocalWareHouseDetailList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 是 | string | 开始时间，格式 Y-m-d |
| end_date | 是 | string | 结束时间 |
| sys_wid | 否 | int | 仓库ID，多个逗号分隔 |
| offset | 是 | int | 分页偏移量，默认0 |
| length | 是 | int | 分页长度，默认15 |

**关键返回字段**: spu, spu_name, sku, product_name, fnsku, sys_wid, ware_house_name, day_early_count, purchase_in_count, day_end_count, unit_cost, total_cost

---

## localDetailListNew - 查询本地仓库存明细（新版）

**路径**: `/inventory/center/openapi/storageReport/local/detail/page`
**令牌桶容量**: 3

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 是 | string | 开始时间，格式 Y-m-d |
| end_date | 是 | string | 结束时间 |
| sys_wid | 否 | string | 仓库ID，多个逗号分隔 |
| offset | 是 | int | 分页页码，默认1 |
| length | 是 | int | 分页长度，默认15 |

**关键返回字段**: sku, product_name, sys_wid, ware_house_name, day_early_count, purchase_in_count, day_end_count, unit_cost, total_cost

---

## monthRefund - 查询月度退款统计

**路径**: `/erp/sc/routing/finance/Refund/profitMonthRefund`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| start_date | 是 | string | 起始日期，格式 Y-m-d |
| end_date | 是 | string | 结束日期 |
| asin_type | 是 | string | 1=asin，2=父asin |
| offset | 是 | int | 分页偏移量 |
| length | 是 | int | 分页条数，上限200 |
| sort_field | 否 | string | 排序字段 |
| sort_type | 否 | string | 排序：desc/asc |

**关键返回字段**: asin, sid, month, refund_amount, refund_quantity, refund_rate, refund_reason_list

---

## overseasAggregateList - 查询海外仓库存汇总

**路径**: `/erp/sc/routing/inventoryLog/WareHouseReport/getOverSeaSummaryList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 是 | string | 开始时间，格式 Y-m-d |
| end_date | 是 | string | 结束时间 |
| sys_wid | 否 | int | 仓库ID，多个逗号分隔 |

**关键返回字段**: sys_wid, ware_house_name, day_early_count, purchase_in_count, day_end_count, unit_cost, total_cost

---

## overseasAggregateListNew - 查询海外仓库存汇总（新版）

**路径**: `/inventory/center/openapi/storageReport/overseas/aggregate/list`
**令牌桶容量**: 3

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 是 | string | 开始时间，格式 Y-m-d |
| end_date | 是 | string | 结束时间 |
| sys_wid | 否 | string | 仓库ID，多个逗号分隔 |

**关键返回字段**: sys_wid, ware_house_name, product_count, day_early_count, purchase_in_count, day_end_count, day_end_cost

---

## overseasDetailList - 查询海外仓库存明细

**路径**: `/erp/sc/routing/inventoryLog/WareHouseReport/getOverSeaDetailList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 是 | string | 开始时间，格式 Y-m-d |
| end_date | 是 | string | 结束时间 |
| sys_wid | 否 | int | 仓库ID，多个逗号分隔 |
| offset | 是 | int | 分页偏移量，默认0 |
| length | 是 | int | 每页条数，默认15 |

**关键返回字段**: sku, product_name, sys_wid, ware_house_name, day_early_count, purchase_in_count, day_end_count, unit_cost

---

## overseasDetailListNew - 查询海外仓库存明细（新版）

**路径**: `/inventory/center/openapi/storageReport/overseas/detail/page`
**令牌桶容量**: 3

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 是 | string | 开始时间，格式 Y-m-d |
| end_date | 是 | string | 结束时间 |
| sys_wid | 否 | string | 仓库ID，多个逗号分隔 |
| offset | 是 | int | 页码，默认1 |
| length | 是 | int | 分页长度，默认15 |

**关键返回字段**: sku, product_name, sys_wid, ware_house_name, day_early_count, day_end_count, unit_cost, total_cost

---

## platformStatisticsSaleStatPageListV2 - 查询平台销售统计（V2）

**路径**: `/basicOpen/platformStatisticsV2/saleStat/pageList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 是 | string | 开始日期，格式 Y-m-d，最长90天 |
| end_date | 是 | string | 结束日期 |
| result_type | 是 | string | 汇总类型：1=销量，2=订单量，3=销售额 |
| date_unit | 是 | string | 时间指标：1=年，2=月，3=周，4=日 |
| data_type | 是 | string | 统计维度：1=ASIN，2=父体，3=MSKU，4=SKU，5=SPU，6=店铺 |
| sids | 否 | array | 店铺ID列表 |
| page | 否 | int | 分页页码，默认1 |
| length | 否 | int | 分页大小，默认20 |

**关键返回字段**: list[date/value/sid/asin/msku/sku]

---

## profitMsku - 查询MSKU利润统计

**路径**: `/erp/sc/routing/finance/ProfitStatis/profitMsku`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 是 | string | 起始日期，格式 Y-m-d |
| end_date | 是 | string | 结束日期 |
| offset | 是 | int | 分页偏移量 |
| length | 是 | int | 分页长度，上限200 |
| sids | 否 | string | 店铺ID，逗号分隔 |
| currency_type | 否 | string | 币种（1=CNY，2=USD等） |
| sort_field | 否 | string | 排序字段 |
| sort_type | 否 | string | 排序：desc/asc |

**关键返回字段**: seller_sku, asin, sid, sales_amount, profit, profit_rate, fba_fee, commission, ad_cost

---

## purchaseReportBuyerList - 查询采购报表（买家维度）

**路径**: `/basicOpen/report/purchase/buyer/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 否 | string | 开始日期，闭区间，格式 Y-m-d，最长90天 |
| end_date | 否 | string | 结束日期 |
| time_type | 否 | int | 时间类型：1=下单时间，2=到货时间 |
| product_type | 否 | array | 产品类型：1=普通，2=组合，3=辅料 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20，上限200 |

**关键返回字段**: buyer_id, buyer_name, total_amount, purchase_count, product_count, currency

---

## purchaseReportProductList - 查询采购报表（产品维度）

**路径**: `/basicOpen/report/purchase/product/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 否 | string | 开始日期，闭区间，格式 Y-m-d，最长90天 |
| end_date | 否 | string | 结束日期 |
| time_type | 否 | int | 时间类型：1=下单时间，2=到货时间 |
| sids | 否 | string | 店铺ID，多个逗号分隔 |
| search_field | 否 | string | 搜索字段：product_name/sku/msku/fnsku/spu_name/spu |
| search_value | 否 | string | 搜索值 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20，上限200 |

**关键返回字段**: sku, product_name, total_quantity, total_amount, supplier_count, currency

---

## purchaseReportSupplierList - 查询采购报表（供应商维度）

**路径**: `/basicOpen/report/purchase/supplier/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 否 | string | 开始日期，闭区间，格式 Y-m-d，最长90天 |
| end_date | 否 | string | 结束日期 |
| time_type | 否 | int | 时间类型：1=下单时间，2=到货时间 |
| search_field | 否 | string | 搜索字段：order_no=单据号 |
| search_value | 否 | string | 搜索值 |
| product_type | 否 | array | 产品类型：1=普通，2=组合，3=辅料 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20，上限200 |

**关键返回字段**: supplier_id, supplier_name, total_amount, purchase_count, product_count, currency

---

## reimbursementList - 查询亚马逊赔偿列表

**路径**: `/basicOpen/openapi/mwsReport/reimbursementList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sids | 否 | string | 店铺ID，多个逗号分隔 |
| start_date | 否 | string | 批准日期开始，格式 Y-m-d，最长90天 |
| end_date | 否 | string | 批准日期结束 |
| search_field | 否 | string | 搜索字段：reimbursement_id/amazon_order_id/asin/msku/fnsku/item_name |
| search_value | 否 | string | 搜索值 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20，上限200 |

**关键返回字段**: reimbursement_id, sid, amazon_order_id, asin, msku, fnsku, quantity_reimbursed, amount_total, currency, approval_date

---

## returnOrderAnalysisLists - 查询退货分析列表

**路径**: `/basicOpen/salesAnalysis/returnOrder/analysisLists`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始日期，格式 yyyy-MM-dd，最长366天 |
| endDate | 是 | string | 结束日期 |
| asinType | 是 | string | 维度类型：msku/asin/parentAsin/sku/spu |
| dateType | 是 | int | 时间类型：0=退货时间，1=下单时间 |
| offset | 是 | int | 分页偏移量 |
| length | 是 | int | 分页长度 |
| mids | 否 | array | 国家ID列表 |
| storeId | 否 | array | 店铺ID列表 |
| searchField | 否 | string | 搜索字段：msku/asin/parentAsin/localSku/localName/spu/spuName |
| searchValue | 否 | array | 搜索值列表 |
| sortField | 否 | string | 排序字段 |
| sortType | 否 | string | 排序：ASC/DESC |

**关键返回字段**: asin/msku/sku, cur_return_goods_count, return_goods_count_ratio, cur_volume, cur_return_goods_volume_ratio

---

## storeSales - 查询店铺销售报表

**路径**: `/erp/sc/data/sales_report/sales`
**令牌桶容量**: 5

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| start_date | 是 | string | 报表时间，格式 Y-m-d，闭区间 |
| end_date | 是 | string | 报表时间，闭区间 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认1000 |

**关键返回字段**: sid, date, ordered_product_sales, units_ordered, total_order_items, sessions, buy_box_percentage, unit_session_percentage, currency

---

## operateLogList - 查询Listing操作日志

**路径**: `/basicOpen/operateManage/operateLog/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sids | 是 | array | 店铺ID列表 |
| search_field | 是 | string | 搜索类型：asin/parent_asin/msku |
| search_value | 是 | string | 搜索值 |
| date_type | 是 | string | 时间类型：1=日，2=周，3=月 |
| start_date | 是 | string | 开始时间，格式 Y-m-d，闭区间 |
| end_date | 是 | string | 结束时间，闭区间 |

**关键返回字段**: asin/msku, date, operate_type, operate_content, sessions_change, sales_change

---

## operateLogV2List - 查询Listing操作日志（V2）

**路径**: `/basicOpen/operateManage/operateLog/list/v2`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 是 | string | 开始时间，格式 yyyy-mm-dd |
| end_date | 是 | string | 结束时间 |
| summary_type | 是 | string | 日志维度：asin/parent_asin/msku |
| sids | 否 | array | 店铺ID列表 |
| mids | 否 | array | 国家列表 |
| search_field | 否 | string | 搜索条件：asin/parent_asin/msku |
| search_value | 否 | array | 搜索值 |
| offset | 否 | number | 分页偏移量，默认20 |
| length | 否 | number | 分页长度，默认200 |

**关键返回字段**: asin/msku/parent_asin, date, operate_type, operate_content, before_value, after_value

---

## performanceTrendByHour - 查询产品按小时表现趋势

**路径**: `/basicOpen/salesAnalysis/productPerformance/performanceTrendByHour`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sids | 是 | string | 店铺ID，多个逗号分隔，上限200 |
| date_start | 是 | string | 开始时间，格式 Y-m-d，闭区间 |
| date_end | 是 | string | 结束时间，闭区间 |
| summary_field | 是 | string | 查询维度：parent_asin/asin/msku/sku/spu |
| summary_field_value | 是 | string | 查询维度值 |

**关键返回字段**: hour, sessions, units_ordered, ordered_product_sales, conversion_rate

---

## reportCreateReportExportTask - 创建报告导出任务

**路径**: `/basicOpen/report/create/reportExportTask`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| seller_id | 是 | string | 亚马逊店铺ID |
| report_type | 是 | string | 亚马逊报表类型 |
| marketplace_ids | 是 | array | 亚马逊市场ID列表 |
| region | 是 | string | 店铺所在地区：na/eu/fe |
| data_start_time | 否 | string | 报表请求开始时间，格式 YYYY-MM-DDTHH:MM:SSZ |
| data_end_time | 否 | string | 报表请求结束时间 |

**关键返回字段**: task_id（用于后续查询报告状态）

---

## reportQueryReportExportTask - 查询报告导出任务结果

**路径**: `/basicOpen/report/query/reportExportTask`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| seller_id | 是 | string | 亚马逊店铺ID |
| task_id | 是 | string | 任务ID（由reportCreateReportExportTask获取） |
| region | 是 | string | 店铺所在地区：na/eu/fe |

**关键返回字段**: report_document_id, progress_status（IN_PROGRESS/CANCELLED/DONE/FATAL/IN_QUEUE/UNKNOWN）, url（报表下载地址，有效期5min）, compression_algorithm

---

## statisticsOpenASIN - 查询ASIN统计数据（实时）

**路径**: `/bd/profit/statistics/open/asin/list`
**令牌桶容量**: 10

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始时间，双闭区间，最长7天 |
| endDate | 是 | string | 结束时间 |
| sids | 否 | array | 店铺ID列表 |
| mids | 否 | array | 站点ID列表 |
| searchField | 否 | string | 搜索类型：asin |
| searchValue | 否 | array | 搜索值 |
| currencyCode | 否 | string | 货币代码 |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，上限10000 |

**关键返回字段**: asin, sid, units_ordered, ordered_product_sales, sessions, conversion_rate, buy_box_percentage, profit, ad_cost

---

## statisticsOpenMSKU - 查询MSKU统计数据（实时）

**路径**: `/bd/profit/statistics/open/msku/list`
**令牌桶容量**: 10

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始时间，双闭区间，最长7天 |
| endDate | 是 | string | 结束时间 |
| sids | 否 | array | 店铺ID列表 |
| mids | 否 | array | 站点ID列表 |
| searchField | 否 | string | 搜索类型：msku |
| searchValue | 否 | array | 搜索值 |
| currencyCode | 否 | string | 货币代码 |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，上限10000 |

**关键返回字段**: seller_sku, asin, sid, units_ordered, ordered_product_sales, profit, ad_cost, currency

---

## statisticsOpenParent - 查询父ASIN统计数据（实时）

**路径**: `/bd/profit/statistics/open/parent/asin/list`
**令牌桶容量**: 10

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始时间，双闭区间，最长7天 |
| endDate | 是 | string | 结束时间 |
| sids | 否 | array | 店铺ID列表 |
| mids | 否 | array | 站点ID列表 |
| searchField | 否 | string | 搜索类型：parent_asin |
| searchValue | 否 | array | 搜索值 |
| currencyCode | 否 | string | 货币代码 |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，上限10000 |

**关键返回字段**: parent_asin, sid, units_ordered, ordered_product_sales, profit, ad_cost, child_asin_count

---

## statisticsOpenSeller - 查询店铺统计数据（实时）

**路径**: `/bd/profit/statistics/open/seller/list`
**令牌桶容量**: 10

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始时间，双闭区间，最长7天 |
| endDate | 是 | string | 结束时间 |
| sids | 否 | array | 店铺ID列表 |
| mids | 否 | array | 站点ID列表 |
| currencyCode | 否 | string | 货币代码 |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，上限10000 |

**关键返回字段**: sid, seller_name, units_ordered, ordered_product_sales, profit, profit_rate, ad_cost, currency
