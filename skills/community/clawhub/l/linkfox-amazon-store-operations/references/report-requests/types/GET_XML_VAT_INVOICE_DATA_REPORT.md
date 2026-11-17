# `GET_XML_VAT_INVOICE_DATA_REPORT`

> **分类**：8. Invoice Reports  
> **说明**：VAT 发票数据（XML）  
> **可用范围**：仅卖家

## 官方说明（Report type values）

以下内容整理自官方 [Report type values](https://developer-docs.amazon.com/sp-api/docs/report-type-values) 子页 [Invoice Data Reports](https://developer-docs.amazon.com/sp-api/docs/report-type-values-invoice-data#xml-vat-invoice-data-report-vidr)（章节：**XML VAT Invoice Data Report (VIDR)**）。**与专页其它段落冲突时以官方英文文档为准。**

- **受限报告**：未在相邻 Note 中写明，但 **角色** 含 *Restricted*；**仍可能**需 RDT/额外审核，以官方为准
- **角色**：[Tax Invoicing (Restricted)](https://developer-docs.amazon.com/sp-api/docs/roles-in-the-selling-partner-api#tax-invoicing-restricted)
- **可用范围**：已加入 Amazon VAT Calculation Service 并选择自行上传发票的卖家。此报告同时覆盖 Fulfillment by Amazon 与卖家自发货订单。
- **报告输出类型**：XML
- **默认值**：`"pendingInvoices" : "true"`。
- **要点**：提供卖家订单每次发货、退货或退款生成 VAT 发票所需的全部信息。货件在发货后立即纳入此报告。Amazon 建议每日至少定时生成此报告两次。此报告接受以下 `reportOptions` 取值：关于如何使用此报告，参见 [VAT Calculation Service](https://developer-docs.amazon.com/sp-api/docs/vat-calculation-service-guide)。
- **reportOptions（摘录）**：
  - pendingInvoices – 布尔值。为 true 时，报告仅包含发票与贷记单待处理的货件；不含发票已成功上传的货件。包含过去 90 天内下单的货件。为 false，或 `reportOptions` 中未包含 pendingInvoices 时，报告内容由 all 的值决定。示例：`"reportOptions":{"pendingInvoices":"true"}`
  - all – 布尔值。为 true 时，报告包含所指定日期范围内下单的货件，涵盖所有可能的发票状态。必须指定 createReport 操作的 startDate 与 endDate 参数。dataStartTime 与 dataEndTime 必须对应所指定 reportPeriod 内有效的首日与末日。例如 reportPeriod=WEEK 时，dataStartTime 须为周日、dataEndTime 须为周六。允许的最大日期范围为 30 天。为 false，或 `reportOptions` 中未包含 all 时，报告内容由 pendingInvoices 的值决定。示例：`"reportOptions": {"ReportOption=All": "true"}`

- **官方直达**：<https://developer-docs.amazon.com/sp-api/docs/report-type-values-invoice-data#xml-vat-invoice-data-report-vidr>


## 官方 `schemas/reports` JSON Schema

本 `reportType` 在 Amazon 仓库 [https://github.com/amzn/selling-partner-api-models/tree/main/schemas/reports](https://github.com/amzn/selling-partner-api-models/tree/main/schemas/reports) 中**无**与结果格式一一对应的独立 JSON 文件（多为 **Flat File / TSV / XML** 等）。**请求参数、可选日期、`reportOptions`、列定义**以官方为准：

- [https://developer-docs.amazon.com/sp-api/docs/report-type-values](https://developer-docs.amazon.com/sp-api/docs/report-type-values)

## CreateReport 请求体（最小常用）

多数此类报告可按下述最小结构创建（是否支持 `dataStartTime`/`dataEndTime` 及格式以官方文档为准）：

```json
{
  "reportType": "GET_XML_VAT_INVOICE_DATA_REPORT",
  "marketplaceIds": ["ATVPDKIKX0DER"]
}
```

支持日期范围时，可补充例如：

```json
{
  "reportType": "GET_XML_VAT_INVOICE_DATA_REPORT",
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
