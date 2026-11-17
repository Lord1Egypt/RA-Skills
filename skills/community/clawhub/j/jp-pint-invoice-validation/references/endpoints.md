# jp-pint-invoice-validation — endpoints

Generated from the live JPVerify catalog. Prices are USD per successful call (the same with an API key or x402).

## English

| Endpoint | MCP tool | Price (USD) | Use when | Returns |
|---|---|---|---|---|
| `POST /v1/jp/invoices/validate-pint` | — | $0.02 | You need offline validation of a JP PINT 1.1.3 UBL Invoice before accounting or payment workflow acceptance. | Official document_valid from pinned OASIS UBL 2.1 XSD and OpenPeppol JP PINT 1.1.3 Schematron, plus separate decision/trusted fields and optional NTA registry evidence. |

## 日本語

| Endpoint | MCP tool | Price (USD) | Use when | Returns |
|---|---|---|---|---|
| `POST /v1/jp/invoices/validate-pint` | — | $0.02 | 会計処理や支払ワークフローに受け入れる前に、JP PINT 1.1.3 UBL請求書をオフライン検証したい場合。 | 固定したOASIS UBL 2.1 XSDとOpenPeppol JP PINT 1.1.3 Schematronによるdocument_valid、分離されたdecision/trusted、任意の国税庁登記根拠を返します。 |
