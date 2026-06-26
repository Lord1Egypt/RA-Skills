# 领星财务接口参考

所有接口均为 POST 请求，域名：`https://openapi.lingxing.com`

---

## profitAsin - 查询ASIN利润报表

**路径**: `/erp/sc/routing/finance/ProfitState/profitAsin`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| month | 是 | string | 月份，格式 Y-m |
| sids | 否 | string | 店铺ID，多个逗号分隔 |
| currency_type | 否 | string | 币种：1=CNY，2=USD，3=EUR等 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，上限200 |

**关键返回字段**: sid, asin, parent_asin, seller_sku, month, sales_amount, cost, profit, profit_rate, fba_fee, commission, ad_cost

---

## profitAsinSon - 查询ASIN子变体利润

**路径**: `/erp/sc/routing/finance/ProfitState/profitAsinSon`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| month | 是 | string | 月份，格式 Y-m |
| sids | 否 | string | 店铺ID，多个逗号分隔 |
| asin | 否 | string | 父ASIN |
| version | 否 | int | 版本号 |
| currency_type | 否 | string | 币种 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，上限200 |

**关键返回字段**: sid, asin, seller_sku, month, sales_amount, profit, profit_rate

---

## profitSettlement - 查询结算利润报表

**路径**: `/erp/sc/routing/finance/ProfitState/profitSettlement`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sids | 否 | string | 店铺ID，多个逗号分隔 |
| start_date | 是 | string | 开始日期，格式 Y-m-d |
| end_date | 是 | string | 结束日期 |
| currency_type | 否 | string | 币种 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，上限200 |

**关键返回字段**: sid, amazon_order_id, settlement_id, sales_amount, fba_fee, commission, profit, currency

---

## profitMsku - 查询MSKU利润报表

**路径**: `/erp/sc/routing/finance/ProfitState/profitMsku`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| month | 是 | string | 月份，格式 Y-m |
| sids | 否 | string | 店铺ID，多个逗号分隔 |
| currency_type | 否 | string | 币种 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，上限200 |

**关键返回字段**: sid, seller_sku, asin, month, sales_amount, profit, profit_rate, fba_fee, commission

---

## settlementReport - 查询结算报告

**路径**: `/cost/center/api/settlement/report`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| amazonSellerIds | 否 | array | 亚马逊店铺ID列表 |
| sids | 否 | array | 领星店铺ID列表 |
| timeType | 是 | int | 时间类型：1=结算开始时间，2=结算结束时间 |
| filterBeginDate | 是 | string | 开始日期，格式 Y-m-d |
| filterEndDate | 是 | string | 结束日期 |

**关键返回字段**: settlement_id, sid, start_date, end_date, total_amount, currency

---

## costStream - 查询成本流水

**路径**: `/cost/center/api/cost/stream`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| mskus | 否 | array | MSKU列表 |
| business_types | 是 | array | 业务类型列表 |
| query_type | 是 | int | 查询类型 |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |

**关键返回字段**: msku, business_type, amount, currency, date, remark

---

## orderProfitListMSKU - 查询订单MSKU利润明细

**路径**: `/basicOpen/finance/mreport/OrderProfit`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sids | 否 | string | 店铺ID，多个逗号分隔 |
| startDate | 是 | string | 开始日期，格式 Y-m-d |
| endDate | 是 | string | 结束日期 |
| searchField | 否 | string | 搜索字段：amazon_order_id/seller_sku/asin |
| searchValue | 否 | string | 搜索值 |
| currencyCode | 否 | string | 货币代码 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: amazon_order_id, sid, seller_sku, asin, sales_amount, fba_fee, commission, profit, currency

---

## invoiceList - 查询发票列表

**路径**: `/bd/profit/report/open/report/ads/invoice/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sids | 否 | array | 店铺ID列表 |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: invoice_id, sid, invoice_date, amount, currency, status, campaign_count

---

## invoiceDetail - 查询发票详情

**路径**: `/bd/profit/report/open/report/ads/invoice/detail`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| invoice_id | 是 | string | 发票ID |
| sid | 是 | int | 店铺ID |

**关键返回字段**: invoice_id, sid, invoice_date, amount, currency, status, line_items

---

## invoiceCampaignList - 查询发票广告活动列表

**路径**: `/bd/profit/report/open/report/ads/invoice/campaign/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| invoice_id | 是 | string | 发票ID |
| sid | 是 | int | 店铺ID |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: campaign_id, campaign_name, spend, impressions, clicks

---

## queryReceiptFundsList - 查询收款记录列表

**路径**: `/basicOpen/finance/queryReceiptFundsList`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sids | 否 | string | 店铺ID，多个逗号分隔 |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: receipt_id, sid, amount, currency, receipt_date, status

---

## requestFundsOrderList - 查询付款单列表

**路径**: `/basicOpen/finance/requestFunds/order/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| status | 否 | int | 状态 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: order_id, amount, currency, status, create_time, type

---

## settlementExportUrlGet - 获取结算报告导出URL

**路径**: `/bd/sp/api/open/settlement/export/url/get`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| settlement_id | 是 | string | 结算ID |
| sid | 是 | int | 店铺ID |

**关键返回字段**: url, expires_at

---

## bdAsin - 查询ASIN利润分析报表

**路径**: `/bd/profit/report/open/report/asin/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始日期，格式 Y-m-d |
| endDate | 是 | string | 结束日期 |
| sids | 否 | array | 店铺ID列表 |
| currencyCode | 否 | string | 货币代码 |
| monthlyQuery | 否 | int | 是否按月查询：0=否，1=是 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: asin, sid, sales_amount, ad_cost, fba_fee, commission, profit, profit_rate, currency

---

## bdMsku - 查询MSKU利润分析报表

**路径**: `/bd/profit/report/open/report/msku/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始日期 |
| endDate | 是 | string | 结束日期 |
| sids | 否 | array | 店铺ID列表 |
| currencyCode | 否 | string | 货币代码 |
| monthlyQuery | 否 | int | 是否按月查询 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: seller_sku, asin, sid, sales_amount, profit, profit_rate, currency

---

## bdOrder - 查询订单利润分析报表

**路径**: `/bd/profit/report/open/report/order/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始日期 |
| endDate | 是 | string | 结束日期 |
| sids | 否 | array | 店铺ID列表 |
| currencyCode | 否 | string | 货币代码 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: amazon_order_id, sid, sales_amount, profit, profit_rate, currency, purchase_date

---

## bdParentAsin - 查询父ASIN利润分析报表

**路径**: `/bd/profit/report/open/report/parent/asin/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始日期 |
| endDate | 是 | string | 结束日期 |
| sids | 否 | array | 店铺ID列表 |
| currencyCode | 否 | string | 货币代码 |
| monthlyQuery | 否 | int | 是否按月查询 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: parent_asin, sid, sales_amount, profit, profit_rate, currency

---

## bdSku - 查询SKU利润分析报表

**路径**: `/bd/profit/report/open/report/sku/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始日期 |
| endDate | 是 | string | 结束日期 |
| sids | 否 | array | 店铺ID列表 |
| currencyCode | 否 | string | 货币代码 |
| monthlyQuery | 否 | int | 是否按月查询 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: sku, asin, sid, sales_amount, profit, profit_rate, currency

---

## bdSeller - 查询店铺利润分析报表

**路径**: `/bd/profit/report/open/report/seller/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始日期 |
| endDate | 是 | string | 结束日期 |
| sids | 否 | array | 店铺ID列表 |
| currencyCode | 否 | string | 货币代码 |
| monthlyQuery | 否 | int | 是否按月查询 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: sid, seller_name, sales_amount, profit, profit_rate, currency

---

## bdSellerSummary - 查询店铺利润汇总报表

**路径**: `/bd/profit/report/open/report/seller/summary/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始日期 |
| endDate | 是 | string | 结束日期 |
| sids | 否 | array | 店铺ID列表 |
| currencyCode | 否 | string | 货币代码 |

**关键返回字段**: sid, seller_name, total_sales, total_profit, profit_rate, currency

---

## centerOdsDetailQuery - 查询成本中心ODS明细

**路径**: `/cost/center/ods/detail/query`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| mskus | 否 | array | MSKU列表 |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: msku, cost_type, amount, currency, date, warehouse

---

## feeManagementList - 查询其他费用列表

**路径**: `/bd/fee/management/open/feeManagement/otherFee/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sids | 否 | array | 店铺ID列表 |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| fee_type | 否 | string | 费用类型 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: fee_id, sid, fee_type, fee_name, amount, currency, date

---

## feeManagementType - 查询费用类型列表

**路径**: `/bd/fee/management/open/feeManagement/otherFee/type`
**令牌桶容量**: 1

**参数**: 无

**关键返回字段**: type_id, type_name, type_code

---

## lazadaPayoutList - 查询Lazada打款记录

**路径**: `/basicOpen/finance/lazada/payout/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| store_ids | 否 | array | 店铺ID列表 |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: payout_id, store_id, amount, currency, payout_date, status

---

## lazadaSettlementList - 查询Lazada结算列表

**路径**: `/basicOpen/finance/lazada/settlement/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| store_ids | 否 | array | 店铺ID列表 |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: settlement_id, store_id, amount, currency, start_date, end_date, status

---

## profitReportOrderTranscationList - 查询订单交易利润报表

**路径**: `/basicOpen/finance/profitReport/order/transcation/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sids | 否 | string | 店铺ID，多个逗号分隔 |
| start_date | 是 | string | 开始日期 |
| end_date | 是 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: amazon_order_id, sid, transaction_type, amount, currency, posted_date

---

## receivableReportList - 查询应收账款报表列表

**路径**: `/bd/sp/api/open/monthly/receivable/report/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sids | 否 | array | 店铺ID列表 |
| year_month | 否 | string | 年月，格式 Y-m |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: report_id, sid, year_month, receivable_amount, currency, status

---

## reportListDetail - 查询应收账款报表明细

**路径**: `/bd/sp/api/open/monthly/receivable/report/list/detail`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| report_id | 是 | string | 报表ID |
| sid | 是 | int | 店铺ID |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: settlement_id, amount, currency, start_date, end_date

---

## reportListDetailInfo - 查询应收账款报表明细详情

**路径**: `/bd/sp/api/open/monthly/receivable/report/list/detail/info`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| report_id | 是 | string | 报表ID |
| settlement_id | 是 | string | 结算ID |
| sid | 是 | int | 店铺ID |

**关键返回字段**: settlement_id, transaction_list[type/amount/currency/date]

---

## requestFundsPoolCustomFeeList - 查询资金池自定义费用列表

**路径**: `/basicOpen/finance/requestFundsPool/customFee/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| pool_id | 是 | int | 资金池ID |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: fee_id, pool_id, fee_type, amount, currency, date, remark

---

## requestFundsPoolInboundList - 查询资金池头程费用列表

**路径**: `/basicOpen/finance/requestFundsPool/inbound/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| pool_id | 是 | int | 资金池ID |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: fee_id, pool_id, shipment_no, amount, currency, date

---

## requestFundsPoolLogisticsList - 查询资金池物流费用列表

**路径**: `/basicOpen/finance/requestFundsPool/logistics/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| pool_id | 是 | int | 资金池ID |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: fee_id, pool_id, order_no, amount, currency, date

---

## requestFundsPoolOtherFeeList - 查询资金池其他费用列表

**路径**: `/basicOpen/finance/requestFundsPool/otherFee/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| pool_id | 是 | int | 资金池ID |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: fee_id, pool_id, fee_type, amount, currency, date

---

## requestFundsPoolPrepayList - 查询资金池预付款列表

**路径**: `/basicOpen/finance/requestFundsPool/prepay/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| pool_id | 是 | int | 资金池ID |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: prepay_id, pool_id, amount, currency, date, status

---

## requestFundsPoolPurchaseList - 查询资金池采购费用列表

**路径**: `/basicOpen/finance/requestFundsPool/purchase/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| pool_id | 是 | int | 资金池ID |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: fee_id, pool_id, purchase_order_no, amount, currency, date

---

## settlementSummaryList - 查询结算汇总列表

**路径**: `/bd/sp/api/open/settlement/summary/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sids | 否 | array | 店铺ID列表 |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: settlement_id, sid, start_date, end_date, total_amount, deposit_amount, currency

---

## settlementTransactionList - 查询结算交易明细列表

**路径**: `/bd/sp/api/open/settlement/transaction/detail/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| settlement_id | 是 | string | 结算ID |
| sid | 是 | int | 店铺ID |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: transaction_id, settlement_id, type, amount, currency, posted_date, order_id

---

## shopeeAdjustmentList - 查询Shopee调整列表

**路径**: `/basicOpen/finance/shopee/adjustment/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| store_ids | 否 | array | 店铺ID列表 |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: adjustment_id, store_id, type, amount, currency, date, reason

---

## shopeeIncomeList - 查询Shopee收入列表

**路径**: `/basicOpen/finance/shopee/income/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| store_ids | 否 | array | 店铺ID列表 |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: income_id, store_id, order_id, amount, currency, income_date, type

---

## shopeePayoutList - 查询Shopee打款列表

**路径**: `/basicOpen/finance/shopee/payout/list`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| store_ids | 否 | array | 店铺ID列表 |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 每页条数，默认20 |

**关键返回字段**: payout_id, store_id, amount, currency, payout_date, status

---

## summaryQuery - 查询成本中心ODS汇总

**路径**: `/cost/center/ods/summary/query`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| mskus | 否 | array | MSKU列表 |
| start_date | 否 | string | 开始日期 |
| end_date | 否 | string | 结束日期 |

**关键返回字段**: msku, total_cost, cost_by_type[type/amount/currency]
