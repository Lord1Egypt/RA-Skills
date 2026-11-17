# `GET_LEDGER_DETAIL_VIEW_DATA`

> **分类**：6.2 FBA Inventory  
> **说明**：库存账本明细  
> **可用范围**：仅卖家

## 官方说明（Report type values）

以下内容整理自官方 [Report type values](https://developer-docs.amazon.com/sp-api/docs/report-type-values) 子页 [Fulfillment by Amazon (FBA) Reports](https://developer-docs.amazon.com/sp-api/docs/report-type-values-fba#inventory-ledger-report---detailed-view)（章节：**Inventory Ledger Report - Detailed View**）。**与专页其它段落冲突时以官方英文文档为准。**

- **受限报告**：按当前小节文本为否（仍以官方为准）
- **角色**：[Amazon Fulfillment](https://developer-docs.amazon.com/sp-api/docs/roles-in-the-selling-partner-api#amazon-fulfillment)
- **请求/调度**：本报告仅支持按需请求。
- **报告输出类型**：制表符分隔的扁平文件
- **要点**：使用库存账本报告 - 明细视图分析库存出入亚马逊运营中心的流转情况，包括已售出、退货、移除/销毁、损坏、丢失和找回的商品。本报告可查看最长 18 个月的库存历史流转记录。本报告接受以下 reportOptions 取值：可向 ReportOptions 传入多个参数，示例如下："reportOptions":{"eventType":"Adjustments", "FNSKU" : "X00001", "MSKU" : "Test"}
- **reportOptions（摘录）**：
  - eventType：按特定仓库事件过滤报告数据。默认为空字符串，返回所有事件。其它可选值：Adjustments CustomerReturns Receipts Shipments VendorReturns WhseTransfers 示例："reportOptions":{"eventType":""} "reportOptions":{"eventType":"Adjustments"}
  - FNSKU：传入 FNSKU 值以查看该 FNSKU 对应的报告数据。
  - MSKU：传入 MSKU 值以查看该 MSKU 所有有效 FNSKU 映射的报告数据。
  - ASIN：传入 ASIN 值以查看该 ASIN 所有有效 FNSKU 映射的报告数据。

- **官方直达**：<https://developer-docs.amazon.com/sp-api/docs/report-type-values-fba#inventory-ledger-report---detailed-view>


## 官方 `schemas/reports` JSON Schema

本 `reportType` 在 Amazon 仓库 [https://github.com/amzn/selling-partner-api-models/tree/main/schemas/reports](https://github.com/amzn/selling-partner-api-models/tree/main/schemas/reports) 中**无**与结果格式一一对应的独立 JSON 文件（多为 **Flat File / TSV / XML** 等）。**请求参数、可选日期、`reportOptions`、列定义**以官方为准：

- [https://developer-docs.amazon.com/sp-api/docs/report-type-values](https://developer-docs.amazon.com/sp-api/docs/report-type-values)

## CreateReport 请求体（最小常用）

多数此类报告可按下述最小结构创建（是否支持 `dataStartTime`/`dataEndTime` 及格式以官方文档为准）：

```json
{
  "reportType": "GET_LEDGER_DETAIL_VIEW_DATA",
  "marketplaceIds": ["ATVPDKIKX0DER"]
}
```

支持日期范围时，可补充例如：

```json
{
  "reportType": "GET_LEDGER_DETAIL_VIEW_DATA",
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
