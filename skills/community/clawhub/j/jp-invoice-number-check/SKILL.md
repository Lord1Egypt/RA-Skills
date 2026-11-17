---
name: jp-invoice-number-check
description: >-
  Check Japanese qualified-invoice registration numbers (T-numbers, 適格請求書発行事業者登録番号,
  インボイス登録番号) against the National Tax Agency registry with JPVerify, check that a T-number
  belongs to the issuer name (and address) on an invoice and that the issuer was registered — not
  cancelled or expired — on the invoice date, and match an invoice to a supplier's expected T-number or
  corporate number from master data (AP / vendor checks). Use when a task involves verifying a T-number,
  confirming who issued a Japanese invoice and whether its registration covered the invoice date, or
  matching an invoice to supplier master data. Paid per call (API key credits or x402).
license: MIT
---

# Japanese T-number and invoice issuer check / インボイス登録番号と発行者の確認

Version 1.3.5 · JPVerify · https://www.jpverify.com

## When to use / いつ使うか

- You have a T-number (`T` + 13 digits) and need to know whether it is registered and active.
- You have an invoice's issuer name/address and T-number and need to know whether they belong together.
- You have up to 100 T-numbers or received invoices to check at once.
- You have an invoice's date and need to know whether the issuer was registered on that date (not yet registered, or already cancelled or expired).
- You need to know whether an invoice really comes from a supplier in your master data, and you have that supplier's T-number or corporate number stored there.

JPVerify does not read files. If you have an invoice or receipt image or PDF, read it yourself (or with the user's OCR) and send the fields. Ask the user rather than guessing a value you cannot read.

## Connect / 接続

JPVerify is a paid, per-call API. Pick the first option that applies; never guess credentials.

1. **API key (recommended).** If the environment has `JPVERIFY_API_KEY` (a `jpv_live_…` key the user created), send it on every call:
   - HTTP: header `Authorization: Bearer $JPVERIFY_API_KEY` (or `X-API-Key`).
   - MCP: if the JPVerify Claude Code plugin is installed, the `jpverify` MCP server is already configured and uses the key saved in the plugin's settings (`/plugin` → JPVerify → Configure), not `JPVERIFY_API_KEY`. Otherwise: `claude mcp add --transport http jpverify https://api.jpverify.com/mcp --header "Authorization: Bearer $JPVERIFY_API_KEY" --header "X-JPVerify-Client: jp-invoice-number-check/1.3.5"`
   Each successful call is deducted from the user's prepaid USD credits; failed or invalid calls are refunded automatically. Before a large batch, check the balance for free: `GET https://api.jpverify.com/v1/account/balance` with the same header, or the MCP tool `jpverify_balance`.
2. **x402 wallet.** If you have an x402 client with USDC on Base (`eip155:8453`) and the user approved a budget, call without a key: the API answers HTTP 402 with the exact price; sign and retry with `PAYMENT-SIGNATURE`. Pay only within the approved budget.
3. **Neither.** Do not pay and do not invent a key. The MCP server also works without a key for the free tool `jpverify_guide` (`claude mcp add --transport http jpverify https://api.jpverify.com/mcp`); use it to confirm which call fits, then tell the user they can create a free account with starter credit at https://www.jpverify.com/signup?ref=jp-invoice-number-check and set `JPVERIFY_API_KEY`.

Always send `X-JPVerify-Client: jp-invoice-number-check/1.3.5` on HTTP calls. Never print, log or share the API key.

## Workflow / 手順

1. **Normalize the number.** Accept `T1234567890123`, `t1234567890123` or full-width digits; send it as `T` + 13 ASCII digits. If there are not 13 digits, ask the user instead of guessing; a malformed number returns `422` and is not charged.
2. **Choose the call.**
   - Number only → `POST /v1/jp/invoice-registrations/verify` (MCP `jp_invoice_registration_verify`).
   - Number + issuer name (and address, invoice date if known) from an invoice → `POST /v1/jp/invoices/check-issuer` (MCP `jp_invoice_issuer_check`) with `supplier_name`, optional `address` and optional `invoice_date` (YYYY-MM-DD). It also verifies the number, so do not call `/v1/jp/invoice-registrations/verify` too.
   - The user keeps this supplier in master data (vendor master) → add the T-number or corporate number stored there as `expected_registration_number` or `expected_corporate_number`. Take it from the master data, never from the invoice: a forged invoice from another real company is internally consistent, and only the stored number shows it comes from someone else.
   - 2–100 T-numbers only → `POST /v1/jp/invoice-registrations/verify-batch` ($0.008 per number). 2–100 invoices with issuer name, date or master number → `POST /v1/jp/invoices/check-issuer-batch` (`items` of the same fields as the single check, $0.04 per invoice). Tell the user the total first.
3. **Report** the status, the registered name, the registration (and any cancel/expiry) date, and the `data_as_of` date of the registry data.

## Endpoints and prices / エンドポイントと料金

| Endpoint | MCP tool | Price (USD) | Use when | Returns |
|---|---|---|---|---|
| `POST /v1/jp/invoice-registrations/verify` | `jp_invoice_registration_verify` | $0.01 | You already have a Japanese T+13-digit qualified-invoice registration number. | NTA registration status, corporate number, registered name, and relevant dates. |
| `POST /v1/jp/invoices/check-issuer` | `jp_invoice_issuer_check` | $0.05 | You have a T-number and the issuer name from an invoice (address and invoice date optional) and need to know whether they belong together and the issuer was registered on the invoice date. | Registry fields, issuer name and address comparison, registration on the invoice date, supplier master comparison, and one status per check in check_results. |
| `POST /v1/jp/invoice-registrations/verify-batch` | — | $0.008 per item | You need up to 100 Japanese T-number checks in one request ($0.008 each). | One NTA registration result per T-number. |
| `POST /v1/jp/invoices/check-issuer-batch` | — | $0.04 per item | You have up to 100 received invoices and need the issuer check (T-number, issuer name, invoice date, supplier master number) on each in one request ($0.04 each). | One invoice issuer check result per invoice, in input order. |

### Request fields / リクエスト項目

| Endpoint | Required fields | Optional fields |
|---|---|---|
| `POST /v1/jp/invoice-registrations/verify` | `registration_number` | `response_language` |
| `POST /v1/jp/invoices/check-issuer` | `registration_number` | `supplier_name`, `address`, `invoice_date`, `expected_registration_number`, `expected_corporate_number`, `response_language` |
| `POST /v1/jp/invoice-registrations/verify-batch` | `registration_numbers` | `response_language` |
| `POST /v1/jp/invoices/check-issuer-batch` | `items` | `response_language` |

Where no field is required, send at least one identifier. JPVerify does not read files: send the fields you read. `response_language` is `ja`, `en` or `both` (default `both`).

Japanese descriptions and request examples for every endpoint: [references/endpoints.md](references/endpoints.md), [references/examples.md](references/examples.md).

## Reading results / 結果の読み方

- Data currency: `source_type` is `official_daily_sync` when JPVerify's copy of the NTA register holds the NTA's newest published daily file (the NTA publishes a day's changes after 06:00 JST the next business day; JPVerify applies them by 06:30), `public_snapshot` if that sync is behind, or `live_api`. `source_sync` gives `official_published_through`, `applied_through`, `last_checked_at`, `signature_verified` and `up_to_date`. An exact number match has `verification_confidence: high` while up to date, otherwise `medium`; `not_found` stays `medium` because a registration processed today is published only on the next business day.
- `/v1/jp/invoice-registrations/verify`: `status` is `registered`, `registered_until_expiry`, `expired`, `cancelled`, `deleted` or `not_found`; `verdict` is `qualified` only while the registration is valid. `format_valid` / `checksum_valid` false means the number itself is wrong (check for a typo before concluding anything).
- `/v1/jp/invoices/check-issuer`: `check_results` gives one status per check: `registration` (`ok`, `inactive`, `not_found`, `invalid`), `issuer_name` (`ok`, `likely`, `mismatch`, `unverifiable`, `not_evaluated`), `issuer_address` (`ok`, `mismatch`, `not_evaluated`), and with `invoice_date`, `registration_on_date` (`ok`, `not_registered`, `not_found`). `decision` is `verified`, `manual_review` or `not_found`; with `invoice_date` it follows the registration on that date, so an invoice dated before a later cancellation can still be `verified`, and one dated outside the registration period carries risk flag `invoice_date_outside_registration_period`. `company_match` and `address_match` compare the invoice's issuer with the registered record; `risk_flags` lists differences such as `supplier_name_differs_from_registered_legal_name`, `address_mismatch` or `invoice_cancelled`. A trade name differing from the legal name is common — present it as a difference to confirm, not as fraud. The issuer name can be sent in Japanese or English: English is matched word for word with the company's official English name (NTA, EDINET, GLEIF) or with its romanized registered reading, and `check_results.issuer_name.matched_by` says which (`compared_with` shows the value used). `likely` (`matched_by` `katakana_phonetic` or `website_domain`) means the English name sounds like the registered katakana name (Technoarch for テクノアーチ) or matches the company website: the decision is `verified` only when the address or supplier master number also matches, otherwise `manual_review` with risk flag `supplier_name_phonetic_match_only` — sending the address is the easiest way to confirm. `unverifiable` (risk flag `supplier_name_english_unverified`) means an English name could not be confirmed — most Japanese companies have no official English name — not that it is wrong; ask the user to confirm it, or send the Japanese name if the invoice shows one.
- With `expected_registration_number` / `expected_corporate_number`, `check_results.supplier_master` is `ok`, `mismatch` (risk flag `invoice_issuer_differs_from_supplier_master`: the invoice may come from another company) or `not_evaluated` (the T-number belongs to a sole proprietor with no corporate number). Anything but `ok` makes `decision` `manual_review`.
- For individuals (sole proprietors) the registry often does not publish an address, and the published name may differ from the trade name on the invoice; say so instead of treating missing or different fields as a mismatch.

## Errors and spending / エラーと費用

| Response | What to do |
|---|---|
| `200` | Use the result (see "Reading results"). With an API key, `X-JPVerify-Credits-Charged` and `X-JPVerify-Credits-Remaining` show the cost and balance. |
| `401 invalid_api_key` | The key is missing, wrong or revoked. Ask the user to check `JPVERIFY_API_KEY`; do not retry with guesses. |
| `402 insufficient_credits` (API key) | Stop. Nothing was charged. Tell the user to top up at https://www.jpverify.com/account/billing. Do not retry. |
| `402` with x402 payment requirements (no key) | Pay only within the approved budget, using the exact amount in the response. |
| `422` | Invalid input; nothing was charged. Fix the input (the error says which field) and call again once. |
| `5xx` / timeout | Not charged (credits are refunded). Retry once later; then report the failure. |

Spending rules:
- Before a batch call, or any plan that will cost more than **$0.50** in total, state the number of calls and the total price and get the user's go-ahead.
- Do not call the same paid endpoint repeatedly for the same input; reuse the result you already have.
- Prices in the endpoint table are per successful call in USD (the same with an API key or x402).

## Example / 呼び出し例 (`POST /v1/jp/invoice-registrations/verify`)

API key:

```bash
curl -X POST https://api.jpverify.com/v1/jp/invoice-registrations/verify \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jp-invoice-number-check/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"registration_number": "T1013301046627", "response_language": "both"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/invoice-registrations/verify",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jp-invoice-number-check/1.3.5"},
    json={"registration_number": "T1013301046627", "response_language": "both"},
    timeout=60,
)
print(response.status_code, response.json())
```

x402 (no account):

```bash
# No key: shows the HTTP 402 x402 price; pay with an x402 client and retry with PAYMENT-SIGNATURE.
curl -i -X POST https://api.jpverify.com/v1/jp/invoice-registrations/verify \
  -H "X-JPVerify-Client: jp-invoice-number-check/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"registration_number": "T1013301046627", "response_language": "both"}'
```

Full SDK examples (Python `x402`, JavaScript `@x402/fetch`): https://api.jpverify.com/docs/x402

## Limits and privacy / 制限とプライバシー

- Results are a **public-registry pre-check** with the source and as-of date of the data. They are not KYB, AML or sanctions screening, and not legal, tax or accounting advice. A "not found" does not mean the entity does not exist or is risky.
- If `manual_review_required` is true or a status is ambiguous, show the evidence to the user and let them decide; do not decide on their behalf.
- Only send data the user is entitled to process. JPVerify takes fields, not files; do not send personal details (names, phone numbers, e-mail addresses) that a check does not need.
- Docs: API key https://api.jpverify.com/docs/api-key · x402 https://api.jpverify.com/docs/x402 · terms https://api.jpverify.com/en/terms · privacy https://api.jpverify.com/en/privacy
