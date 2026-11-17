# `FBA_BULK_INVOICE`

> **分类**：12. Regulatory Compliance Reports
> **说明**：FBA 批量发票（FBA bulk invoice）
> **可用范围**：仅卖家（Seller only）

## 官方说明（Report type values）

以下内容整理自官方 [Report type values](https://developer-docs.amazon.com/sp-api/docs/report-type-values) 子页 [Regulatory Compliance Reports](https://developer-docs.amazon.com/sp-api/docs/report-type-values-regulatory-compliance#fba-bulk-invoice)（章节：**FBA Bulk Invoice**）。**与专页其它段落冲突时以官方英文文档为准。**

- **受限报告**：未在相邻 Note 中写明，但 **Role** 含 *Restricted*；**仍可能**需 RDT/额外审核，以官方为准
- **Role**：[Tax Invoicing (Restricted)](https://developer-docs.amazon.com/sp-api/docs/roles-in-the-selling-partner-api#tax-invoicing-restricted)
- **Availability**：Sellers
- **Requested/scheduled**：本报告仅可请求（This report can only be requested）。
- **要点**：提供卖家在给定日期范围内的发票。这些发票包含由卖家履约的客户订单。本报告类型支持以下 report options：单个 report option 值限制为 200 个字符。invoiceTypes 的 `TRANSPORTER_COPY` 和 `CUSTOMER_COPY` 仅在 transactionType 为 `MCF_SHIPMENT` 时可用。对于其他 transactionTypes，`SELLER_COPY` 是唯一有效的 invoiceType。`MCF_SHIPMENT` 同样支持 `SELLER_COPY` 作为有效 invoiceType。orderIds 和 shipmentId 为互斥字段，请求中只能提供其中一个；若两个字段都给出则请求会失败。若两个字段均未设置、或 report options 字段本身缺失，则请求会返回所请求日期范围内的所有相关发票（`SHIPMENT` 和 `MCF_SHIPMENT` 事务类型）。
- **reportOptions（摘录）**：
  - orderIds：由逗号分隔的订单 ID 列表组成的单个字符串，用于过滤。示例：406-8193317-8698708, 408-0804227-3381000。
  - shipmentIds：由逗号分隔的货件 ID 列表组成的单个字符串，用于过滤。示例：64119752218302, 264552989124123。
  - transactionTypes：由逗号分隔的事务类型列表组成的单个字符串，用于过滤。可能的 transactionTypes 为 SHIPMENT、REFUND、CANCEL、EINVOICE_CANCEL、FC_TRANSFER、FC_TRANSFER_CANCEL、FC_REMOVAL、FC_REMOVAL_CANCEL、MCF_SHIPMENT、MCF_CANCEL 和 MCF_REFUND。
  - invoiceTypes：由逗号分隔的发票类型列表组成的单个字符串，用于过滤。可能的 invoiceTypes 包括 CUSTOMER_COPY、SELLER_COPY 和 TRANSPORTER_COPY。

- **官方直达**：<https://developer-docs.amazon.com/sp-api/docs/report-type-values-regulatory-compliance#fba-bulk-invoice>


## 官方 `schemas/reports` JSON Schema

本 `reportType` 在 Amazon 仓库 [https://github.com/amzn/selling-partner-api-models/tree/main/schemas/reports](https://github.com/amzn/selling-partner-api-models/tree/main/schemas/reports) 中**无**与结果格式一一对应的独立 JSON 文件（多为 **Flat File / TSV / XML** 等）。**请求参数、可选日期、`reportOptions`、列定义**以官方为准：

- [https://developer-docs.amazon.com/sp-api/docs/report-type-values](https://developer-docs.amazon.com/sp-api/docs/report-type-values)

## CreateReport 请求体（最小常用）

多数此类报告可按下述最小结构创建（是否支持 `dataStartTime`/`dataEndTime` 及格式以官方文档为准）：

```json
{
  "reportType": "FBA_BULK_INVOICE",
  "marketplaceIds": ["ATVPDKIKX0DER"]
}
```

支持日期范围时，可补充例如：

```json
{
  "reportType": "FBA_BULK_INVOICE",
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
