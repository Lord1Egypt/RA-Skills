# jp-invoice-number-check — endpoints

Generated from the live JPVerify catalog. Prices are USD per successful call (the same with an API key or x402).

## English

| Endpoint | MCP tool | Price (USD) | Use when | Returns |
|---|---|---|---|---|
| `POST /v1/jp/invoice-registrations/verify` | `jp_invoice_registration_verify` | $0.01 | You already have a Japanese T+13-digit qualified-invoice registration number. | NTA registration status, corporate number, registered name, and relevant dates. |
| `POST /v1/jp/invoices/check-issuer` | `jp_invoice_issuer_check` | $0.05 | You have a T-number and the issuer name from an invoice (address and invoice date optional) and need to know whether they belong together and the issuer was registered on the invoice date. | Registry fields, issuer name and address comparison, registration on the invoice date, supplier master comparison, and one status per check in check_results. |
| `POST /v1/jp/invoice-registrations/verify-batch` | — | $0.008 per item | You need up to 100 Japanese T-number checks in one request ($0.008 each). | One NTA registration result per T-number. |
| `POST /v1/jp/invoices/check-issuer-batch` | — | $0.04 per item | You have up to 100 received invoices and need the issuer check (T-number, issuer name, invoice date, supplier master number) on each in one request ($0.04 each). | One invoice issuer check result per invoice, in input order. |

## 日本語

| Endpoint | MCP tool | Price (USD) | Use when | Returns |
|---|---|---|---|---|
| `POST /v1/jp/invoice-registrations/verify` | `jp_invoice_registration_verify` | $0.01 | 日本のT+13桁インボイス登録番号が既にある場合。 | 国税庁の登録状態、法人番号、登録名、関連日付を返します。 |
| `POST /v1/jp/invoices/check-issuer` | `jp_invoice_issuer_check` | $0.05 | 請求書のT番号と発行者名（住所・日付は任意）が一致するか、請求書の日付時点で登録済みかを確認したい場合。 | 国税庁の登録情報、発行者名・住所の比較結果、請求書日付時点の登録状況、確認項目ごとの結果を返します。 |
| `POST /v1/jp/invoice-registrations/verify-batch` | — | $0.008 per item | 最大100件の日本のT番号を1回のリクエストで検証したい場合（1件$0.008）。 | T番号ごとの国税庁登録結果を返します。 |
| `POST /v1/jp/invoices/check-issuer-batch` | — | $0.04 per item | 受け取った最大100件の請求書について、発行者確認（T番号・発行者名・日付・仕入先マスター番号）を1回で行いたい場合（1件$0.04）。 | 請求書ごとの発行者確認結果を入力順に返します。 |
