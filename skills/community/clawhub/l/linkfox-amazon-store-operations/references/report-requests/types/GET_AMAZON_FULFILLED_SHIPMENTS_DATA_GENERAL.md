# `GET_AMAZON_FULFILLED_SHIPMENTS_DATA_GENERAL`

> **分类**：6.1 FBA Shipments
> **说明**：FBA 履约货件（通用）（FBA fulfilled shipments (general)）
> **可用范围**：仅卖家（Seller only）

## 官方说明（Report type values）

以下内容整理自官方 [Report type values](https://developer-docs.amazon.com/sp-api/docs/report-type-values) 子页 [Fulfillment by Amazon (FBA) Reports](https://developer-docs.amazon.com/sp-api/docs/report-type-values-fba#fba-amazon-fulfilled-shipments-report)（章节：**FBA Amazon Fulfilled Shipments Report**）。**与专页其它段落冲突时以官方英文文档为准。**

- **受限报告**：按当前小节文本为否（仍以官方为准）
- **Availability**：FBA sellers
- **Requested/scheduled**：本报告仅可请求（This report can only be requested）。
- **Report output type**：Tab-delimited flat file
- **Roles**：[Pricing](https://developer-docs.amazon.com/sp-api/docs/roles-in-the-selling-partner-api#pricing), [Amazon Fulfillment](https://developer-docs.amazon.com/sp-api/docs/roles-in-the-selling-partner-api#amazon-fulfillment), [Inventory and Order Tracking](https://developer-docs.amazon.com/sp-api/docs/roles-in-the-selling-partner-api#inventory-and-order-tracking)
- **要点**：包含详细的订单/货件/商品信息，含价格、承运商和跟踪数据。单个报告最多可请求一个月的数据。欧洲（EU）、日本和北美（NA）地区内容近实时更新。📘注意：在日本、EU 和 NA，大多数情况下，从履约订单发货到该订单中的商品出现在报告中会有大约一到三小时的延迟；在少数情况下可能延迟最多 24 小时。

- **官方直达**：<https://developer-docs.amazon.com/sp-api/docs/report-type-values-fba#fba-amazon-fulfilled-shipments-report>


## 官方 `schemas/reports` JSON Schema

本 `reportType` 在 Amazon 仓库 [https://github.com/amzn/selling-partner-api-models/tree/main/schemas/reports](https://github.com/amzn/selling-partner-api-models/tree/main/schemas/reports) 中**无**与结果格式一一对应的独立 JSON 文件（多为 **Flat File / TSV / XML** 等）。**请求参数、可选日期、`reportOptions`、列定义**以官方为准：

- [https://developer-docs.amazon.com/sp-api/docs/report-type-values](https://developer-docs.amazon.com/sp-api/docs/report-type-values)

## CreateReport 请求体（最小常用）

多数此类报告可按下述最小结构创建（是否支持 `dataStartTime`/`dataEndTime` 及格式以官方文档为准）：

```json
{
  "reportType": "GET_AMAZON_FULFILLED_SHIPMENTS_DATA_GENERAL",
  "marketplaceIds": ["ATVPDKIKX0DER"]
}
```

支持日期范围时，可补充例如：

```json
{
  "reportType": "GET_AMAZON_FULFILLED_SHIPMENTS_DATA_GENERAL",
  "marketplaceIds": ["ATVPDKIKX0DER"],
  "dataStartTime": "2024-01-01T00:00:00Z",
  "dataEndTime": "2024-01-31T23:59:59Z"
}
```

若官方要求 **`reportOptions`** 或其它字段，必须一并传入（见 Report type values）。

## LinkFox

- `scripts/get_report.py`：JSON 参数与 CreateReport 体字段同名；支持 `reportOptions`、`lastUpdatedDate`。
- 网关与代理：`references/api.md`。

## 另见

- 全类型总表：`references/report-types.md`
- 带 JSON 结果 Schema 的报告：`references/report-requests/README.md`
