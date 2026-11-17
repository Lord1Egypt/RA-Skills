# `GET_XML_BROWSE_TREE_DATA`

> **分类**：4. Browse Tree Reports  
> **说明**：浏览树层级（XML 格式）  
> **可用范围**：仅卖家

## 官方说明（Report type values）

以下内容整理自官方 [Report type values](https://developer-docs.amazon.com/sp-api/docs/report-type-values) 子页 [Browse Tree Reports](https://developer-docs.amazon.com/sp-api/docs/report-type-values-browse-tree#browse-tree-report)（章节：**Browse Tree Report**）。**与专页其它段落冲突时以官方英文文档为准。**

- **受限报告**：未在相邻 Note 中写明，但 **角色** 含 *Restricted*；**仍可能**需 RDT/额外审核，以官方为准
- **角色**：[Product Listing](https://developer-docs.amazon.com/sp-api/docs/roles-in-the-selling-partner-api#product-listing), [Pricing](https://developer-docs.amazon.com/sp-api/docs/roles-in-the-selling-partner-api#pricing), [Inventory and Order Tracking](https://developer-docs.amazon.com/sp-api/docs/roles-in-the-selling-partner-api#inventory-and-order-tracking), [Direct to Consumer Shipping (Restricted)](https://developer-docs.amazon.com/sp-api/docs/roles-in-the-selling-partner-api#direct-to-consumer-shipping-restricted)
- **可用范围**：卖家
- **请求/定时**：此报告可请求或定时。
- **报告输出类型**：XML
- **Schema**：[BrowseTreeReport.xsd](https://images-na.ssl-images-amazon.com/images/G/01/mwsportal/doc/en_US/Reports/XSDs/BrowseTreeReport.xsd)
- **要点**：包含任意站点 Amazon 零售网站的浏览树层级信息与节点细化信息。此报告接受以下 `reportOptions` 取值：📘注意：卖家必须已在使用 MarketplaceId 指定的站点完成注册。此外，请求必须发送到与所指定 MarketplaceId 对应的终端节点，否则服务将返回错误。📘注意：若 `reportOptions` 中同时包含 RootNodesOnly 和 BrowseNodeId，RootNodesOnly 优先。📘注意：Amazon 建议在调用 createReport 请求浏览树报告时不要传入 MarketplaceIds 参数。若 MarketplaceIds 参数值与 `reportOptions` 中的 MarketplaceId 值冲突，以 MarketplaceId 值为准。
- **reportOptions（摘录）**：
  - MarketplaceId – 指定要获取浏览树信息的目标站点。若 `reportOptions` 中未包含 MarketplaceId，则报告包含卖家默认站点的浏览树信息。
  - RootNodesOnly – 字符串值，必须为 true 或 false。当 RootNodesOnly 设为 true 时，报告仅包含通过 MarketplaceId 指定站点（若未指定 MarketplaceId 则为默认站点）的根节点。当 RootNodesOnly 设为 false，或未在 `ReportOptions` 中包含 RootNodesOnly 时，报告内容由 BrowseNodeId 的值决定。
  - BrowseNodeId – 指定报告中浏览树层级的顶部节点。若 `ReportOptions` 中未包含 BrowseNodeId，且 RootNodesOnly 为 false 或未包含，则报告包含通过 MarketplaceId 指定站点（若未指定则为卖家默认站点）的完整浏览节点层级。注意：若请求中包含无效的 BrowseNodeId，服务将返回不含数据的报告。

- **官方直达**：<https://developer-docs.amazon.com/sp-api/docs/report-type-values-browse-tree#browse-tree-report>


## 官方 `schemas/reports` JSON Schema

本 `reportType` 在 Amazon 仓库 [https://github.com/amzn/selling-partner-api-models/tree/main/schemas/reports](https://github.com/amzn/selling-partner-api-models/tree/main/schemas/reports) 中**无**与结果格式一一对应的独立 JSON 文件（多为 **Flat File / TSV / XML** 等）。**请求参数、可选日期、`reportOptions`、列定义**以官方为准：

- [https://developer-docs.amazon.com/sp-api/docs/report-type-values](https://developer-docs.amazon.com/sp-api/docs/report-type-values)

## CreateReport 请求体（最小常用）

多数此类报告可按下述最小结构创建（是否支持 `dataStartTime`/`dataEndTime` 及格式以官方文档为准）：

```json
{
  "reportType": "GET_XML_BROWSE_TREE_DATA",
  "marketplaceIds": ["ATVPDKIKX0DER"]
}
```

支持日期范围时，可补充例如：

```json
{
  "reportType": "GET_XML_BROWSE_TREE_DATA",
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
