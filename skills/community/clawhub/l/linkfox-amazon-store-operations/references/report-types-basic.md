# Amazon Store 报告类型参考

本文档介绍 Amazon Selling Partner API 中可用的常见报告类型。

## 报告分类

Amazon Store 报告按以下主要类别组织：

### 1. Inventory Reports（库存报告）

跟踪库存状态、Listing 与库存水平。

| Report Type | 说明 | 更新频率 |
|-------------|-------------|------------------|
| `GET_MERCHANT_LISTINGS_ALL_DATA` | 在售 Listing 报告，含 SKU、ASIN、价格、数量 | 近实时 |
| `GET_MERCHANT_LISTINGS_DATA` | 制表符分隔的平面文件格式的在售 Listing | 近实时 |
| `GET_MERCHANT_LISTINGS_INACTIVE_DATA` | 非在售（停用）Listing 报告 | 近实时 |
| `GET_MERCHANT_CANCELLED_LISTINGS_DATA` | 已取消的 Listing | 近实时 |
| `GET_FLAT_FILE_OPEN_LISTINGS_DATA` | 在售 Listing 报告（SKU、价格、数量） | 近实时 |
| `GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA` | FBA 库存管理报告 | 近实时 |
| `GET_FBA_INVENTORY_AGED_DATA` | FBA 库存库龄报告 | 每日 |
| `GET_FBA_INVENTORY_PLANNING_DATA` | FBA 库存规划报告 | 每日 |

**常见用途：**
- 监控当前库存水平
- 识别停用或滞留库存
- 规划库存补货
- 校验 Listing 准确性

### 2. Order Reports（订单报告）

获取订单数据以供处理与分析。

| Report Type | 说明 | 更新频率 |
|-------------|-------------|------------------|
| `GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL` | 按下单日期排列的全部订单（通用格式） | 近实时 |
| `GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_GENERAL` | 按最后更新日期排列的全部订单 | 近实时 |
| `GET_XML_ALL_ORDERS_DATA_BY_ORDER_DATE` | XML 格式的全部订单 | 近实时 |
| `GET_FLAT_FILE_ARCHIVED_ORDERS_DATA_BY_ORDER_DATE` | 归档订单数据 | 历史 |
| `GET_FLAT_FILE_ACTIONABLE_ORDER_DATA` | 需要处理的待操作订单 | 近实时 |
| `GET_ORDER_REPORT_DATA_SHIPPING` | 含配送信息的订单 | 近实时 |

**常见用途：**
- 将订单导出至 ERP/WMS 系统
- 跟踪订单履约状态
- 分析订单模式
- 生成发货标签

### 3. Financial Reports（财务报告）

获取结算与财务交易数据。

| Report Type | 说明 | 更新频率 |
|-------------|-------------|------------------|
| `GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE` | 结算报告 v2（平面文件） | 每 14 天 |
| `GET_V2_SETTLEMENT_REPORT_DATA_XML` | 结算报告 v2（XML 格式） | 每 14 天 |
| `GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2` | 增强版结算报告 | 每 14 天 |

**常见用途：**
- 对账 Amazon 付款
- 跟踪费用与退款
- 生成财务报表
- 与财务系统对接

### 4. Sales Reports（销售报告）

分析销售表现与流量指标。

| Report Type | 说明 | 更新频率 |
|-------------|-------------|------------------|
| `GET_SALES_AND_TRAFFIC_REPORT` | 按日期统计的销售与流量 | 每日 |
| `GET_FLAT_FILE_SALES_TAX_DATA` | 销售税征收数据 | 近实时 |

**常见用途：**
- 跟踪每日销售指标
- 监控流量与转化率
- 分析销售趋势
- 税务申报

### 5. FBA（Fulfillment by Amazon）报告

管理 FBA 库存与货件。

| Report Type | 说明 | 更新频率 |
|-------------|-------------|------------------|
| `GET_AMAZON_FULFILLED_SHIPMENTS_DATA_GENERAL` | FBA 配送的货件 | 近实时 |
| `GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_SALES_DATA` | FBA 客户货件销售 | 每日 |
| `GET_FBA_FULFILLMENT_REMOVAL_ORDER_DETAIL_DATA` | FBA 移除订单明细 | 每日 |
| `GET_FBA_FULFILLMENT_REMOVAL_SHIPMENT_DETAIL_DATA` | FBA 移除货件明细 | 每日 |
| `GET_FBA_STORAGE_FEE_CHARGES_DATA` | FBA 仓储费 | 每月 |
| `GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA` | 预估 FBA 费用 | 按需 |

**常见用途：**
- 跟踪 FBA 货件
- 监控仓储费
- 处理移除订单
- 分析履约成本

### 6. Returns Reports（退货报告）

跟踪客户退货与退款。

| Report Type | 说明 | 更新频率 |
|-------------|-------------|------------------|
| `GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE` | 按退货日期统计的退货数据 | 每日 |
| `GET_XML_RETURNS_DATA_BY_RETURN_DATE` | XML 格式的退货数据 | 每日 |
| `GET_FLAT_FILE_ALL_RETURNS_DATA_BY_RETURN_DATE` | 全部退货数据 | 每日 |
| `GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA` | FBA 客户退货 | 每日 |

**常见用途：**
- 处理退货请求
- 跟踪退货率
- 分析退货原因
- 管理退款

### 7. Performance Reports（绩效报告）

监控卖家绩效指标。

| Report Type | 说明 | 更新频率 |
|-------------|-------------|------------------|
| `GET_V1_SELLER_PERFORMANCE_REPORT` | 卖家绩效指标 | 每日 |
| `GET_FLAT_FILE_FEEDBACK_DATA` | 客户反馈 | 每日 |

**常见用途：**
- 监控账户健康度
- 跟踪客户满意度
- 识别绩效问题
- 回复反馈

## 报告请求工作流

### 创建报告

1. **请求报告**
   - 接口：`POST /reports/2021-06-30/reports`
   - 指定 `reportType`、`marketplaceIds` 及可选的日期范围
   - 响应中返回 `reportId`

2. **检查报告状态**
   - 接口：`GET /reports/2021-06-30/reports/{reportId}`
   - 状态值：`IN_QUEUE`、`IN_PROGRESS`、`DONE`、`CANCELLED`、`FATAL`

3. **下载报告文档**
   - 状态为 `DONE` 时，获取 `reportDocumentId`
   - 接口：`GET /reports/2021-06-30/documents/{reportDocumentId}`
   - 获取下载链接并按需解密

### 获取已有报告

- 接口：`GET /reports/2021-06-30/reports`
- 按 `reportTypes`、`processingStatuses`、`marketplaceIds` 过滤
- 按日期范围过滤：`createdSince`、`createdUntil`

## 常用参数

| 参数 | 说明 | 必填 | 示例 |
|-----------|-------------|----------|---------|
| `reportType` | 要生成的报告类型 | 是 | `GET_MERCHANT_LISTINGS_ALL_DATA` |
| `marketplaceIds` | 目标站点 | 是 | `["ATVPDKIKX0DER"]`（美国） |
| `dataStartTime` | 数据范围起始日期 | 否 | `2024-01-01T00:00:00Z` |
| `dataEndTime` | 数据范围结束日期 | 否 | `2024-01-31T23:59:59Z` |

## 站点 ID（Marketplace IDs）

| 区域 | 国家 | Marketplace ID |
|--------|---------|----------------|
| NA | 美国 | ATVPDKIKX0DER |
| NA | 加拿大 | A2EUQ1WTGCTBG2 |
| NA | 墨西哥 | A1AM78C64UM0Y8 |
| EU | 英国 | A1F83G8C2ARO7P |
| EU | 德国 | A1PA6795UKMFR9 |
| EU | 法国 | A13V1IB3VIYZZH |
| EU | 意大利 | APJ6JRA9NG5V4 |
| EU | 西班牙 | A1RKKUPIHCS9HS |
| FE | 日本 | A1VC38T7YXB528 |
| FE | 澳大利亚 | A39IBJ37TRP1C6 |
| FE | 新加坡 | A19VAU5U5O7RUS |
| FE | 印度 | A21TJRUUN4KGV |

## 最佳实践

1. **请求频率**
   - 遵守速率限制：通常为 0.0222 次请求/秒（每 45 秒 1 次请求）
   - 合理使用突发容量
   - 在非高峰时段调度周期性报告

2. **日期范围**
   - 保持合理的日期范围（通常 1-90 天）
   - 部分报告可能有最大日期范围限制
   - 使用 `dataStartTime` 和 `dataEndTime` 缩小结果范围

3. **错误处理**
   - 下载前先检查报告状态
   - 妥善处理 `FATAL` 状态报告
   - 对失败请求使用指数退避重试

4. **数据处理**
   - 报告通常为 TSV（制表符分隔值）格式
   - 高效处理大文件（流式处理）
   - 处理前先校验数据

## 示例：请求库存报告

```json
POST /reports/2021-06-30/reports
{
  "reportType": "GET_MERCHANT_LISTINGS_ALL_DATA",
  "marketplaceIds": ["ATVPDKIKX0DER"]
}
```

## 示例：获取报告列表

```
GET /reports/2021-06-30/reports?reportTypes=GET_MERCHANT_LISTINGS_ALL_DATA&marketplaceIds=ATVPDKIKX0DER
```

## 其他资源

- 官方文档：https://developer-docs.amazon.com/sp-api/docs/reports-api-v2021-06-30-reference
- 报告类型值：https://developer-docs.amazon.com/sp-api/docs/report-type-values
- Reports API 用例指南：https://developer-docs.amazon.com/sp-api/docs/reports-api-v2021-06-30-use-case-guide

---

**注意**：报告的可用性与更新频率可能因站点和卖家账户类型而异。请始终以 Amazon Selling Partner API 官方文档为准获取最新信息。
