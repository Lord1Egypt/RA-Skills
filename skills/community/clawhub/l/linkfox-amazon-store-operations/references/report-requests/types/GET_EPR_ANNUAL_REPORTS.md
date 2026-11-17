# `GET_EPR_ANNUAL_REPORTS`

> **分类**：12. Regulatory Compliance Reports
> **说明**：EPR 年度报告
> **可用范围**：仅卖家

## 官方说明（Report type values）

以下内容整理自官方 [Report type values](https://developer-docs.amazon.com/sp-api/docs/report-type-values) 子页 [Regulatory Compliance Reports](https://developer-docs.amazon.com/sp-api/docs/report-type-values-regulatory-compliance#epr-annual-report)（章节：**EPR Annual Report**）。**与专页其它段落冲突时以官方英文文档为准。**

- **受限报告**：按当前小节文本为否（仍以官方为准）
- **Role**：[Product Listing](https://developer-docs.amazon.com/sp-api/docs/roles-in-the-selling-partner-api#product-listing)
- **Availability**：卖家
- **Requested/scheduled**：本报告仅支持请求，不支持定时调度。
- **Report output type**：Comma-separated flat file
- **要点**：包含用于向监管机构申报 EPR 合规情况并缴纳 EPR 费用的数据，按年度汇总。Amazon Extended Producer Responsibility Reports（Amazon EPR Reports，亚马逊生产者责任延伸报告）允许卖家以编程方式获取向监管机构进行 EPR 申报并缴纳 EPR 费用所需的全部数据。Amazon EPR Reports 通过自动生成报告，免去跨多个数据源手动汇总数据和手动商品分类的工作，为卖家节省大量时间。

- **官方直达**：<https://developer-docs.amazon.com/sp-api/docs/report-type-values-regulatory-compliance#epr-annual-report>


## 官方 `schemas/reports` JSON Schema

本 `reportType` 在 Amazon 仓库 [https://github.com/amzn/selling-partner-api-models/tree/main/schemas/reports](https://github.com/amzn/selling-partner-api-models/tree/main/schemas/reports) 中**无**与结果格式一一对应的独立 JSON 文件（多为 **Flat File / TSV / XML** 等）。**请求参数、可选日期、`reportOptions`、列定义**以官方为准：

- [https://developer-docs.amazon.com/sp-api/docs/report-type-values](https://developer-docs.amazon.com/sp-api/docs/report-type-values)

## CreateReport 请求体（最小常用）

多数此类报告可按下述最小结构创建（是否支持 `dataStartTime`/`dataEndTime` 及格式以官方文档为准）：

```json
{
  "reportType": "GET_EPR_ANNUAL_REPORTS",
  "marketplaceIds": ["ATVPDKIKX0DER"]
}
```

支持日期范围时，可补充例如：

```json
{
  "reportType": "GET_EPR_ANNUAL_REPORTS",
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
