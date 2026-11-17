---
name: jpverify
description: >-
  JPVerify: Japan business data for AI agents — verify Japanese companies (法人番号), qualified-invoice
  T-numbers (インボイス), invoice issuers (including registration on the invoice date) and suppliers;
  normalize and validate Japanese addresses; find a Japanese company from its English name; plus JP PINT
  e-invoice validation. Use when a task involves Japanese business documents or data and you need to
  pick the right check. Paid per call (API key credits or x402); a free guide tool is available.
license: MIT
---

# JPVerify — pick the right Japan business check

Version 1.3.5 · JPVerify · https://www.jpverify.com

Use this skill to route a task to the right JPVerify endpoint. For the common tasks, the focused skills have detailed workflows:

| Task | Skill |
|---|---|
| T-number and invoice issuer checks (name, address, registration on the invoice date), issuer vs supplier master | `jp-invoice-number-check` |
| Japanese company from an English name or identifier, corporate number, filings, FSA licences | `jp-company-verify` |
| Japanese address normalization, validation, geocoding, postal codes | `jp-address` |
| Japanese supplier / counterparty pre-check before onboarding or payment | `jp-supplier-due-diligence` |
| JP PINT (Peppol) e-invoice XML validation | `jp-pint-invoice-validation` |

If they are not installed, follow the routing below directly.

## Connect / 接続

JPVerify is a paid, per-call API. Pick the first option that applies; never guess credentials.

1. **API key (recommended).** If the environment has `JPVERIFY_API_KEY` (a `jpv_live_…` key the user created), send it on every call:
   - HTTP: header `Authorization: Bearer $JPVERIFY_API_KEY` (or `X-API-Key`).
   - MCP: if the JPVerify Claude Code plugin is installed, the `jpverify` MCP server is already configured and uses the key saved in the plugin's settings (`/plugin` → JPVerify → Configure), not `JPVERIFY_API_KEY`. Otherwise: `claude mcp add --transport http jpverify https://api.jpverify.com/mcp --header "Authorization: Bearer $JPVERIFY_API_KEY" --header "X-JPVerify-Client: jpverify/1.3.5"`
   Each successful call is deducted from the user's prepaid USD credits; failed or invalid calls are refunded automatically. Before a large batch, check the balance for free: `GET https://api.jpverify.com/v1/account/balance` with the same header, or the MCP tool `jpverify_balance`.
2. **x402 wallet.** If you have an x402 client with USDC on Base (`eip155:8453`) and the user approved a budget, call without a key: the API answers HTTP 402 with the exact price; sign and retry with `PAYMENT-SIGNATURE`. Pay only within the approved budget.
3. **Neither.** Do not pay and do not invent a key. The MCP server also works without a key for the free tool `jpverify_guide` (`claude mcp add --transport http jpverify https://api.jpverify.com/mcp`); use it to confirm which call fits, then tell the user they can create a free account with starter credit at https://www.jpverify.com/signup?ref=jpverify and set `JPVERIFY_API_KEY`.

Always send `X-JPVerify-Client: jpverify/1.3.5` on HTTP calls. Never print, log or share the API key.

## Routing / 使い分け

1. **English company name or an identifier, need the Japanese legal entity in English?** `POST /v1/jp/companies/resolve` (MCP `jp_company_resolve`). Brand names (`au`, `MOS Burger`) return the owning company as a candidate.
2. **Unsure which call fits?** Ask the free MCP tool `jpverify_guide` with the task in plain words, or use the table below.
3. **JPVerify does not read files.** Read invoices, receipts and business cards yourself, then send the fields. Prefer one call that answers the question (e.g. `/v1/jp/invoices/check-issuer` with the issuer name and invoice date instead of separate lookups; `/v1/jp/suppliers/resolve` for a supplier with several identifiers).
4. **Batches:** up to 100 items use the `*-batch` endpoints (priced per item: `companies/verify-batch` and `invoice-registrations/verify-batch` $0.008, `invoices/check-issuer-batch` $0.04); larger jobs (up to 1,000) use `/v1/batch-jobs`, which is x402-only and needs a caller-chosen capability token and an `Idempotency-Key` header. Always confirm the total cost with the user first.

## Endpoints and prices / エンドポイントと料金

### Registry verification / 公的データ照合

| Endpoint | MCP tool | Price (USD) | Use when | Returns |
|---|---|---|---|---|
| `POST /v1/jp/companies/resolve` | `jp_company_resolve` | $0.25 | You hold an English, brand or romanized Japanese company name, an English address or postal code, a website or e-mail domain, a T-number, corporate number, LEI or securities code and need the Japanese legal entity, in English. | Decision (matched / likely_match / candidates), legally binding Japanese name, kana, English name with source, contract party name, status and qualified-invoice registration. Brand names (au, MOS Burger) find the owner as candidates; listing, Wikidata prominence and gBizINFO employee counts only order candidates. |
| `POST /v1/jp/invoice-registrations/verify` | `jp_invoice_registration_verify` | $0.01 | You already have a Japanese T+13-digit qualified-invoice registration number. | NTA registration status, corporate number, registered name, and relevant dates. |
| `POST /v1/jp/invoices/check-issuer` | `jp_invoice_issuer_check` | $0.05 | You have a T-number and the issuer name from an invoice (address and invoice date optional) and need to know whether they belong together and the issuer was registered on the invoice date. | Registry fields, issuer name and address comparison, registration on the invoice date, supplier master comparison, and one status per check in check_results. |
| `POST /v1/jp/invoice-registrations/verify-batch` | — | $0.008 per item | You need up to 100 Japanese T-number checks in one request ($0.008 each). | One NTA registration result per T-number. |
| `POST /v1/jp/invoices/check-issuer-batch` | — | $0.04 per item | You have up to 100 received invoices and need the issuer check (T-number, issuer name, invoice date, supplier master number) on each in one request ($0.04 each). | One invoice issuer check result per invoice, in input order. |
| `POST /v1/jp/companies/verify` | `jp_company_verify` | $0.01 | You need a Japanese company or corporate-number lookup. | Corporate number, registered Japanese legal name (legal_name_ja) and address, English name (NTA official, EDINET, or romanized reading) and English address (official or Japan Post romanization) with their sources, active or closed status, and match evidence. |
| `POST /v1/jp/companies/report` | — | $0.10 | You need a Japan company registry pre-check with risk flags. | Registry identity, status, evidence and risk flags, plus a profile (capital, employees, founding date, website, representative), listing and latest EDINET filing, FSA licences and former names, each with its source; the profile falls back to a dated gBizINFO snapshot when the live source is unavailable. Not full KYC/KYB. |
| `POST /v1/jp/companies/verify-batch` | — | $0.008 per item | You need up to 100 Japanese company or corporate-number lookups in one request ($0.008 each). | One result per input with match status and registry evidence. |
| `POST /v1/jp/suppliers/resolve` | `jp_supplier_resolve` | $0.10 | You need one coverage-aware supplier check combining company, qualified-invoice, and address evidence; optionally includes projected gBizINFO activity evidence when the internal feature flag is enabled. | Independent evidence checks, source versions, and a resolved/ambiguous/not-found/insufficient-coverage status; optional gBizINFO is projected enrichment inside this response, not a standalone source or raw-response resale. Not a legal or KYB determination. |
| `POST /v1/jp/regulated-entities/verify` | — | $0.03 | You need to verify an entity against the covered Japanese FSA financial instruments, funds transfer, or crypto-asset exchange datasets. | Coverage-aware licensing decision, freshness, identity match, license evidence, and review warnings; not a legal unlicensed determination. |
| `GET /v1/jp/filings` | — | $0.01 | You need EDINET filing metadata for a Japanese company by corporate number, EDINET code, or security code. | Filing metadata, correction/withdrawal relationships, freshness, and official evidence references; raw files remain internal. |

### Japanese addresses / 住所

| Endpoint | MCP tool | Price (USD) | Use when | Returns |
|---|---|---|---|---|
| `POST /v1/jp/addresses/normalize` | `jp_address_normalize` | $0.005 | You need Japanese address normalization or standardization, whether or not the input contains a postal code. | Standard written form: normalized components, a unique truncated town completed, an English address from Japan Post romanization, and postal-master consistency and candidates. It does not infer a missing postal code, return coordinates (geocode) or give a final decision (validate). |
| `POST /v1/jp/addresses/parse` | — | $0.002 | You only need the address split into prefecture, city, town, chome, block, lot or house as written (cheapest address call). | Components as written, normalized value, English address and components from Japan Post romanization, unparsed fragments, parser status and confidence. No town completion, postal check, coordinates or decision. |
| `POST /v1/jp/postal-codes/lookup` | — | $0.001 | You need a Japan Post postal-code lookup or reverse lookup from a postal code or administrative address. | Japan Post local-snapshot matches with postal code, prefecture, city, town, kana, Japan Post romanized prefecture/city/town, confidence, source, data version, and candidate count. Business-specific codes of single offices (e.g. 100-8310) return postal_code_type business_specific with the office name and street. |
| `POST /v1/jp/addresses/geocode` | — | $0.005 | You need Japanese forward-geocoding candidates, coordinates, address IDs, or hierarchy levels. The required hierarchy is inferred from the input. | Provider-neutral Jageocoder candidates with normalized address, coordinates, address ID, match level, granularity, confidence, reasons, unmatched tails, and dictionary status. Level 5/6 is oaza/aza, 7 is block, and 8 is building or house node when covered. City-level or town-prefix candidates remain partial; town-level results are not door-number or coordinate accuracy claims. Parcel addresses (番地) match at level 7; a sub-number (枝番) the dictionary lacks stays partial. |
| `POST /v1/jp/addresses/validate` | `jp_address_validate` | $0.005 | You need one evidence-based Japanese address quality decision combining parsed address, postal evidence, and geocoder evidence. | Exact, partial, ambiguous, conflict, or unverified status with accepted hierarchy, confidence signals, validation scope, and reasons. |

### E-invoicing / 電子インボイス

| Endpoint | MCP tool | Price (USD) | Use when | Returns |
|---|---|---|---|---|
| `POST /v1/jp/invoices/validate-pint` | — | $0.02 | You need offline validation of a JP PINT 1.1.3 UBL Invoice before accounting or payment workflow acceptance. | Official document_valid from pinned OASIS UBL 2.1 XSD and OpenPeppol JP PINT 1.1.3 Schematron, plus separate decision/trusted fields and optional NTA registry evidence. |

### Batch / バッチ

| Endpoint | MCP tool | Price (USD) | Use when | Returns |
|---|---|---|---|---|
| `POST /v1/batch-jobs` | — | per item (x402 only) | You need up to 1,000 structured company, invoice, supplier, or Japanese address operations as one durable paid job with progress and downloadable per-item results. | An owner-scoped job ID, exact operation-based price, payment and execution state, progress counts, and stable per-item results with retry metadata; results are released only after settlement. |

### Request fields / リクエスト項目

| Endpoint | Required fields | Optional fields |
|---|---|---|
| `POST /v1/jp/companies/resolve` | — | `name`, `address`, `postal_code`, `prefecture`, `corporate_number`, `t_number`, `lei`, `securities_code`, `duns`, `max_candidates`, `website`, `email` |
| `POST /v1/jp/invoice-registrations/verify` | `registration_number` | `response_language` |
| `POST /v1/jp/invoices/check-issuer` | `registration_number` | `supplier_name`, `address`, `invoice_date`, `expected_registration_number`, `expected_corporate_number`, `response_language` |
| `POST /v1/jp/invoice-registrations/verify-batch` | `registration_numbers` | `response_language` |
| `POST /v1/jp/invoices/check-issuer-batch` | `items` | `response_language` |
| `POST /v1/jp/companies/verify` | — | `name`, `corporate_number`, `address`, `response_language` |
| `POST /v1/jp/companies/report` | — | `name`, `corporate_number`, `address`, `response_language` |
| `POST /v1/jp/companies/verify-batch` | `items` | `response_language` |
| `POST /v1/jp/suppliers/resolve` | — | `name`, `corporate_number`, `address`, `registration_number`, `t_number`, `country_code`, `identifiers`, `response_language` |
| `POST /v1/jp/regulated-entities/verify` | — | `corporate_number`, `name`, `address`, `phone`, `categories`, `response_language` |
| `GET /v1/jp/filings` | — | `corporate_number`, `edinet_code`, `security_code`, `date_from`, `date_to`, `doc_type_code`, `form_code`, `include_withdrawn`, `limit`, `cursor`, `response_language` |
| `POST /v1/jp/addresses/normalize` | `address` | `response_language` |
| `POST /v1/jp/addresses/parse` | `address` | `postal_code`, `response_language`, `parser_profile` |
| `POST /v1/jp/postal-codes/lookup` | — | `postal_code`, `prefecture`, `county`, `city`, `ward`, `town`, `max_results` |
| `POST /v1/jp/addresses/geocode` | — | `address`, `components`, `postal_code`, `max_candidates`, `minimum_acceptable_level`, `provider` |
| `POST /v1/jp/addresses/validate` | — | `address`, `parsed`, `postal_evidence`, `geocode_evidence`, `required_level`, `strict` |
| `POST /v1/jp/invoices/validate-pint` | `xml` | `registry_enhance` |
| `POST /v1/batch-jobs` | `operation` | `items`, `csv_data`, `response_language` |

Where no field is required, send at least one identifier. JPVerify does not read files: send the fields you read. `response_language` is `ja`, `en` or `both` (default `both`).

Japanese descriptions and request examples for every endpoint: [references/endpoints.md](references/endpoints.md), [references/examples.md](references/examples.md).

## Reading results / 結果の読み方

- Every registry result names its `source` and the as-of date of the data. Quote them when you report.
- Most results carry `decision_summary.status`, one vocabulary across endpoints: `verified`, `likely_match`, `candidates`, `not_found`, `manual_review` or `insufficient_coverage`, with machine-readable `reasons`. Act on it the same way everywhere: only `verified` is a confirmed match; `likely_match` and `candidates` need the user's confirmation or an identifier; `manual_review` needs a person; `insufficient_coverage` means no conclusion either way.
- Check `status` / `decision`, `risk_flags` and `manual_review_required` before acting. Ambiguous or multiple matches go back to the user.
- English names: NTA official → EDINET → romanized reading; English addresses: official or Japan Post romanization, with `completeness` (`partial` English never replaces the Japanese `address`). Company and supplier checks search registered Japanese names; start from `/v1/jp/companies/resolve` when you only have an English name. Check `*_source` before relying on one, and use `legal_name_ja` (always returned) on legal documents. Empty means no English source exists, not an error.

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
  -H "X-JPVerify-Client: jpverify/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"name": "Murata Manufacturing Co., Ltd.", "prefecture": "Kyoto"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/companies/resolve",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jpverify/1.3.5"},
    json={"name": "Murata Manufacturing Co., Ltd.", "prefecture": "Kyoto"},
    timeout=60,
)
print(response.status_code, response.json())
```

x402 (no account):

```bash
# No key: shows the HTTP 402 x402 price; pay with an x402 client and retry with PAYMENT-SIGNATURE.
curl -i -X POST https://api.jpverify.com/v1/jp/companies/resolve \
  -H "X-JPVerify-Client: jpverify/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"name": "Murata Manufacturing Co., Ltd.", "prefecture": "Kyoto"}'
```

Full SDK examples (Python `x402`, JavaScript `@x402/fetch`): https://api.jpverify.com/docs/x402

## Limits and privacy / 制限とプライバシー

- Results are a **public-registry pre-check** with the source and as-of date of the data. They are not KYB, AML or sanctions screening, and not legal, tax or accounting advice. A "not found" does not mean the entity does not exist or is risky.
- If `manual_review_required` is true or a status is ambiguous, show the evidence to the user and let them decide; do not decide on their behalf.
- Only send data the user is entitled to process. JPVerify takes fields, not files; do not send personal details (names, phone numbers, e-mail addresses) that a check does not need.
- Docs: API key https://api.jpverify.com/docs/api-key · x402 https://api.jpverify.com/docs/x402 · terms https://api.jpverify.com/en/terms · privacy https://api.jpverify.com/en/privacy
