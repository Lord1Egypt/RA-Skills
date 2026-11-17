---
name: jp-supplier-due-diligence
description: >-
  Run a pre-payment supplier and counterparty check with JPVerify: combine Japanese corporate-number,
  qualified-invoice (T-number) and address evidence for a supplier, add FSA licence and EDINET checks
  when relevant. Covers Japanese suppliers only. Use when a task involves onboarding a vendor, approving an
  invoice for payment, checking a vendor master in bulk, or deciding whether a counterparty needs
  manual review. Paid per call.
license: MIT
---

# Supplier and counterparty pre-check / 取引先の事前確認

Version 1.3.5 · JPVerify · https://www.jpverify.com

A workflow skill: it chains several JPVerify checks into one evidence summary for a human decision. It does **not** approve payments or vendors by itself.

## When to use / いつ使うか

- Onboarding a Japanese supplier, or approving a Japanese invoice for payment.
- Preparing an evidence summary for accounts payable, procurement or compliance review.

## Connect / 接続

JPVerify is a paid, per-call API. Pick the first option that applies; never guess credentials.

1. **API key (recommended).** If the environment has `JPVERIFY_API_KEY` (a `jpv_live_…` key the user created), send it on every call:
   - HTTP: header `Authorization: Bearer $JPVERIFY_API_KEY` (or `X-API-Key`).
   - MCP: if the JPVerify Claude Code plugin is installed, the `jpverify` MCP server is already configured and uses the key saved in the plugin's settings (`/plugin` → JPVerify → Configure), not `JPVERIFY_API_KEY`. Otherwise: `claude mcp add --transport http jpverify https://api.jpverify.com/mcp --header "Authorization: Bearer $JPVERIFY_API_KEY" --header "X-JPVerify-Client: jp-supplier-due-diligence/1.3.5"`
   Each successful call is deducted from the user's prepaid USD credits; failed or invalid calls are refunded automatically. Before a large batch, check the balance for free: `GET https://api.jpverify.com/v1/account/balance` with the same header, or the MCP tool `jpverify_balance`.
2. **x402 wallet.** If you have an x402 client with USDC on Base (`eip155:8453`) and the user approved a budget, call without a key: the API answers HTTP 402 with the exact price; sign and retry with `PAYMENT-SIGNATURE`. Pay only within the approved budget.
3. **Neither.** Do not pay and do not invent a key. The MCP server also works without a key for the free tool `jpverify_guide` (`claude mcp add --transport http jpverify https://api.jpverify.com/mcp`); use it to confirm which call fits, then tell the user they can create a free account with starter credit at https://www.jpverify.com/signup?ref=jp-supplier-due-diligence and set `JPVERIFY_API_KEY`.

Always send `X-JPVerify-Client: jp-supplier-due-diligence/1.3.5` on HTTP calls. Never print, log or share the API key.

## Workflow / 手順

Collect what you know first: legal name, address, corporate number (法人番号), T-number, or the English name and postal code. Ask the user for missing identifiers rather than guessing them.

**Japanese supplier** (typical cost $0.10–$0.20; $0.25 more if you start from an English name):
0. Only an English or romanized name? `POST /v1/jp/companies/resolve` (MCP `jp_company_resolve`) with the name and the postal code or prefecture first, confirm the candidate with the user, then continue with its `corporate_number`.
1. `POST /v1/jp/suppliers/resolve` (MCP `jp_supplier_resolve`) with every identifier you have — one call combines corporate-number, T-number and address evidence. Its `name` is matched against registered Japanese names only; an English name that misses returns reason `english_name_not_in_registry_index` (step 0 first). Each matched check gives `address_en_completeness`; treat `partial` English as display only and keep the Japanese `address`. Stop here if `decision` is `verified` and the user only needs identity.
2. If an invoice is involved and its issuer details differ from the supplier record: `POST /v1/jp/invoices/check-issuer`.
3. Only when relevant to the business: `POST /v1/jp/regulated-entities/verify` (licensed financial businesses) and `GET /v1/jp/filings` (listed companies).

**Many suppliers:** up to 100 per call with the `*-batch` endpoints (priced per item), or up to 1,000 in one x402 batch job (`/v1/batch-jobs`, operation `supplier_resolve`). State the count and total price and get approval first.

## Endpoints and prices / エンドポイントと料金

| Endpoint | MCP tool | Price (USD) | Use when | Returns |
|---|---|---|---|---|
| `POST /v1/jp/companies/resolve` | `jp_company_resolve` | $0.25 | You hold an English, brand or romanized Japanese company name, an English address or postal code, a website or e-mail domain, a T-number, corporate number, LEI or securities code and need the Japanese legal entity, in English. | Decision (matched / likely_match / candidates), legally binding Japanese name, kana, English name with source, contract party name, status and qualified-invoice registration. Brand names (au, MOS Burger) find the owner as candidates; listing, Wikidata prominence and gBizINFO employee counts only order candidates. |
| `POST /v1/jp/suppliers/resolve` | `jp_supplier_resolve` | $0.10 | You need one coverage-aware supplier check combining company, qualified-invoice, and address evidence; optionally includes projected gBizINFO activity evidence when the internal feature flag is enabled. | Independent evidence checks, source versions, and a resolved/ambiguous/not-found/insufficient-coverage status; optional gBizINFO is projected enrichment inside this response, not a standalone source or raw-response resale. Not a legal or KYB determination. |
| `POST /v1/jp/invoices/check-issuer` | `jp_invoice_issuer_check` | $0.05 | You have a T-number and the issuer name from an invoice (address and invoice date optional) and need to know whether they belong together and the issuer was registered on the invoice date. | Registry fields, issuer name and address comparison, registration on the invoice date, supplier master comparison, and one status per check in check_results. |
| `POST /v1/jp/regulated-entities/verify` | — | $0.03 | You need to verify an entity against the covered Japanese FSA financial instruments, funds transfer, or crypto-asset exchange datasets. | Coverage-aware licensing decision, freshness, identity match, license evidence, and review warnings; not a legal unlicensed determination. |
| `GET /v1/jp/filings` | — | $0.01 | You need EDINET filing metadata for a Japanese company by corporate number, EDINET code, or security code. | Filing metadata, correction/withdrawal relationships, freshness, and official evidence references; raw files remain internal. |

### Request fields / リクエスト項目

| Endpoint | Required fields | Optional fields |
|---|---|---|
| `POST /v1/jp/companies/resolve` | — | `name`, `address`, `postal_code`, `prefecture`, `corporate_number`, `t_number`, `lei`, `securities_code`, `duns`, `max_candidates`, `website`, `email` |
| `POST /v1/jp/suppliers/resolve` | — | `name`, `corporate_number`, `address`, `registration_number`, `t_number`, `country_code`, `identifiers`, `response_language` |
| `POST /v1/jp/invoices/check-issuer` | `registration_number` | `supplier_name`, `address`, `invoice_date`, `expected_registration_number`, `expected_corporate_number`, `response_language` |
| `POST /v1/jp/regulated-entities/verify` | — | `corporate_number`, `name`, `address`, `phone`, `categories`, `response_language` |
| `GET /v1/jp/filings` | — | `corporate_number`, `edinet_code`, `security_code`, `date_from`, `date_to`, `doc_type_code`, `form_code`, `include_withdrawn`, `limit`, `cursor`, `response_language` |

Where no field is required, send at least one identifier. JPVerify does not read files: send the fields you read. `response_language` is `ja`, `en` or `both` (default `both`).

Japanese descriptions and request examples for every endpoint: [references/endpoints.md](references/endpoints.md), [references/examples.md](references/examples.md).

## Summarize for the user / 報告のしかた

Report one block per counterparty:
- **Decision signal**: `verified` / `likely_match` → identity confirmed by public data; `ambiguous`, `manual_review`, `not_found_within_coverage`, `insufficient_coverage` → needs a human.
- **Evidence**: which identifiers matched, the registry names and addresses, `risk_flags` / `conflicts`, and each source with its as-of date (`source_versions`, `source_freshness`).
- **Next actions**: use the response's `next_actions` when present (e.g. ask the supplier for a T-number).

Never state that a supplier is "safe", "approved" or "fraudulent". Say what the public data shows and what is missing.

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

## Example / 呼び出し例 (`POST /v1/jp/companies/resolve`)

API key:

```bash
curl -X POST https://api.jpverify.com/v1/jp/companies/resolve \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jp-supplier-due-diligence/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"name": "Murata Manufacturing Co., Ltd.", "prefecture": "Kyoto"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/companies/resolve",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jp-supplier-due-diligence/1.3.5"},
    json={"name": "Murata Manufacturing Co., Ltd.", "prefecture": "Kyoto"},
    timeout=60,
)
print(response.status_code, response.json())
```

x402 (no account):

```bash
# No key: shows the HTTP 402 x402 price; pay with an x402 client and retry with PAYMENT-SIGNATURE.
curl -i -X POST https://api.jpverify.com/v1/jp/companies/resolve \
  -H "X-JPVerify-Client: jp-supplier-due-diligence/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"name": "Murata Manufacturing Co., Ltd.", "prefecture": "Kyoto"}'
```

Full SDK examples (Python `x402`, JavaScript `@x402/fetch`): https://api.jpverify.com/docs/x402

## Limits and privacy / 制限とプライバシー

- Results are a **public-registry pre-check** with the source and as-of date of the data. They are not KYB, AML or sanctions screening, and not legal, tax or accounting advice. A "not found" does not mean the entity does not exist or is risky.
- If `manual_review_required` is true or a status is ambiguous, show the evidence to the user and let them decide; do not decide on their behalf.
- Only send data the user is entitled to process. JPVerify takes fields, not files; do not send personal details (names, phone numbers, e-mail addresses) that a check does not need.
- Docs: API key https://api.jpverify.com/docs/api-key · x402 https://api.jpverify.com/docs/x402 · terms https://api.jpverify.com/en/terms · privacy https://api.jpverify.com/en/privacy
