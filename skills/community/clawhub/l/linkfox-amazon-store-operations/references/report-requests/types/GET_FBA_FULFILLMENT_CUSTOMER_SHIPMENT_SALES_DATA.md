# `GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_SALES_DATA`

> **分类**：6.1 FBA Shipments
> **说明**：FBA 买家配送销售
> **可用范围**：仅卖家

## 官方说明（Report type values）

以下内容整理自官方 [Report type values](https://developer-docs.amazon.com/sp-api/docs/report-type-values) 子页 [Fulfillment by Amazon (FBA) Reports](https://developer-docs.amazon.com/sp-api/docs/report-type-values-fba#fba-customer-shipment-sales-report)（章节：**FBA Customer Shipment Sales Report**）。**与专页其它段落冲突时以官方英文文档为准。**

- **受限报告**：按当前小节文本为否（仍以官方为准）
- **Role**：[Amazon Fulfillment](https://developer-docs.amazon.com/sp-api/docs/roles-in-the-selling-partner-api#amazon-fulfillment)
- **Availability**：FBA 卖家
- **Requested/scheduled**：本报告仅支持请求，不支持定时调度。
- **Report output type**：Tab-delimited flat file
- **要点**：包含已配送的 FBA 买家订单的商品级精简数据，包括价格、数量与配送目的地。内容在欧洲（EU）、日本与北美（NA）近实时更新。📘注意：在日本、EU 与 NA，大多数情况下，从配送订单发货到订单中的商品出现在报告中会有约 1 至 3 小时的延迟；少数情况下延迟最长可达 24 小时。

- **官方直达**：<https://developer-docs.amazon.com/sp-api/docs/report-type-values-fba#fba-customer-shipment-sales-report>


## 官方 `schemas/reports` JSON Schema

本 `reportType` 在 Amazon 仓库 [https://github.com/amzn/selling-partner-api-models/tree/main/schemas/reports](https://github.com/amzn/selling-partner-api-models/tree/main/schemas/reports) 中**无**与结果格式一一对应的独立 JSON 文件（多为 **Flat File / TSV / XML** 等）。**请求参数、可选日期、`reportOptions`、列定义**以官方为准：

- [https://developer-docs.amazon.com/sp-api/docs/report-type-values](https://developer-docs.amazon.com/sp-api/docs/report-type-values)

## CreateReport 请求体（最小常用）

多数此类报告可按下述最小结构创建（是否支持 `dataStartTime`/`dataEndTime` 及格式以官方文档为准）：

```json
{
  "reportType": "GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_SALES_DATA",
  "marketplaceIds": ["ATVPDKIKX0DER"]
}
```

支持日期范围时，可补充例如：

```json
{
  "reportType": "GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_SALES_DATA",
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
