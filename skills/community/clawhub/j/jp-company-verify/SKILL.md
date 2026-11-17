---
name: jp-company-verify
description: >-
  Verify Japanese companies against official registries with JPVerify: identify a Japanese company
  from an English or romanized name, postal code, T-number, LEI or securities code with English output;
  corporate number (法人番号) lookup by number or company name, active/closed status, registered address, a company pre-check
  report with risk flags, company profile (capital, employees, website), listing, EDINET filings, Financial Services Agency
  licences and former names. Use when a
  task involves confirming that a Japanese company exists, finding its corporate number, or doing a
  pre-check before onboarding or paying a Japanese counterparty. Paid per call (API key credits or x402).
license: MIT
---

# Japanese company verification / 日本企業の照合

Version 1.3.5 · JPVerify · https://www.jpverify.com

## When to use / いつ使うか

- You only have an English or romanized company name (e.g. from an English invoice, website or vendor form), or a T-number, LEI or stock code, and need to know which Japanese legal entity it is — with the answer in English.
- Find or confirm a Japanese company's 13-digit corporate number (法人番号), legal name, address and whether it is active or closed.
- Run a pre-check on a Japanese counterparty before onboarding or payment.
- Check EDINET disclosure filings of a listed company, or whether an entity holds an FSA registration (e.g. funds-transfer business).

If the starting point is a T-number on an invoice, use `jp-invoice-number-check` instead.

## Connect / 接続

JPVerify is a paid, per-call API. Pick the first option that applies; never guess credentials.

1. **API key (recommended).** If the environment has `JPVERIFY_API_KEY` (a `jpv_live_…` key the user created), send it on every call:
   - HTTP: header `Authorization: Bearer $JPVERIFY_API_KEY` (or `X-API-Key`).
   - MCP: if the JPVerify Claude Code plugin is installed, the `jpverify` MCP server is already configured and uses the key saved in the plugin's settings (`/plugin` → JPVerify → Configure), not `JPVERIFY_API_KEY`. Otherwise: `claude mcp add --transport http jpverify https://api.jpverify.com/mcp --header "Authorization: Bearer $JPVERIFY_API_KEY" --header "X-JPVerify-Client: jp-company-verify/1.3.5"`
   Each successful call is deducted from the user's prepaid USD credits; failed or invalid calls are refunded automatically. Before a large batch, check the balance for free: `GET https://api.jpverify.com/v1/account/balance` with the same header, or the MCP tool `jpverify_balance`.
2. **x402 wallet.** If you have an x402 client with USDC on Base (`eip155:8453`) and the user approved a budget, call without a key: the API answers HTTP 402 with the exact price; sign and retry with `PAYMENT-SIGNATURE`. Pay only within the approved budget.
3. **Neither.** Do not pay and do not invent a key. The MCP server also works without a key for the free tool `jpverify_guide` (`claude mcp add --transport http jpverify https://api.jpverify.com/mcp`); use it to confirm which call fits, then tell the user they can create a free account with starter credit at https://www.jpverify.com/signup?ref=jp-company-verify and set `JPVERIFY_API_KEY`.

Always send `X-JPVerify-Client: jp-company-verify/1.3.5` on HTTP calls. Never print, log or share the API key.

## Workflow / 手順

1. **Start with the strongest identifier.** A corporate number gives an exact match; a name is searched in the registered names — the Japanese name (`トヨタ自動車株式会社`), the registered English name (`Toyota Motor Corporation`, from the NTA, EDINET or GLEIF) or the romanized registered name (`Toyota Jidosha Kabushiki Kaisha`) — and an address (Japanese or romanized) only confirms a match; it cannot find a company on its own.
2. **Only a brand, trade, short or former name, a website or an LEI?** Call `POST /v1/jp/companies/resolve` (MCP `jp_company_resolve`, $0.25) with what you hold: `name` (legal, English or brand name such as "Uniqlo") plus `address` (English or Japanese), `postal_code` or `prefecture`; a `website` or company `email` (only the domain is used); or `t_number`, `corporate_number`, `lei`, `securities_code`. Identifiers return `matched`; a name alone returns `candidates` (show them to the user). `likely_match` needs a strong name match corroborated by the postal code, municipality, website domain or prefecture; it is still not an identifier match. Then use `corporate_number` for the other calls below.
3. **Choose the call.**
   - Identity and status → `POST /v1/jp/companies/verify` (MCP `jp_company_verify`).
   - Pre-check with risk flags and evidence, or the user needs the company's size, website, listing, licences or former names → `POST /v1/jp/companies/report` (includes the verification; do not call both).
   - 2–100 companies → `POST /v1/jp/companies/verify-batch` ($0.008 per company). Tell the user the total first.
   - Disclosure filings → `GET /v1/jp/filings` (needs a corporate number, EDINET code or securities code).
   - FSA licence / registration → `POST /v1/jp/regulated-entities/verify`.
4. **If a name search returns several candidates**, show them (name, address, corporate number) and ask the user which one is meant, then verify by corporate number. Do not pick one yourself.

## Endpoints and prices / エンドポイントと料金

| Endpoint | MCP tool | Price (USD) | Use when | Returns |
|---|---|---|---|---|
| `POST /v1/jp/companies/resolve` | `jp_company_resolve` | $0.25 | You hold an English, brand or romanized Japanese company name, an English address or postal code, a website or e-mail domain, a T-number, corporate number, LEI or securities code and need the Japanese legal entity, in English. | Decision (matched / likely_match / candidates), legally binding Japanese name, kana, English name with source, contract party name, status and qualified-invoice registration. Brand names (au, MOS Burger) find the owner as candidates; listing, Wikidata prominence and gBizINFO employee counts only order candidates. |
| `POST /v1/jp/companies/verify` | `jp_company_verify` | $0.01 | You need a Japanese company or corporate-number lookup. | Corporate number, registered Japanese legal name (legal_name_ja) and address, English name (NTA official, EDINET, or romanized reading) and English address (official or Japan Post romanization) with their sources, active or closed status, and match evidence. |
| `POST /v1/jp/companies/report` | — | $0.10 | You need a Japan company registry pre-check with risk flags. | Registry identity, status, evidence and risk flags, plus a profile (capital, employees, founding date, website, representative), listing and latest EDINET filing, FSA licences and former names, each with its source; the profile falls back to a dated gBizINFO snapshot when the live source is unavailable. Not full KYC/KYB. |
| `POST /v1/jp/companies/verify-batch` | — | $0.008 per item | You need up to 100 Japanese company or corporate-number lookups in one request ($0.008 each). | One result per input with match status and registry evidence. |
| `GET /v1/jp/filings` | — | $0.01 | You need EDINET filing metadata for a Japanese company by corporate number, EDINET code, or security code. | Filing metadata, correction/withdrawal relationships, freshness, and official evidence references; raw files remain internal. |
| `POST /v1/jp/regulated-entities/verify` | — | $0.03 | You need to verify an entity against the covered Japanese FSA financial instruments, funds transfer, or crypto-asset exchange datasets. | Coverage-aware licensing decision, freshness, identity match, license evidence, and review warnings; not a legal unlicensed determination. |

### Request fields / リクエスト項目

| Endpoint | Required fields | Optional fields |
|---|---|---|
| `POST /v1/jp/companies/resolve` | — | `name`, `address`, `postal_code`, `prefecture`, `corporate_number`, `t_number`, `lei`, `securities_code`, `duns`, `max_candidates`, `website`, `email` |
| `POST /v1/jp/companies/verify` | — | `name`, `corporate_number`, `address`, `response_language` |
| `POST /v1/jp/companies/report` | — | `name`, `corporate_number`, `address`, `response_language` |
| `POST /v1/jp/companies/verify-batch` | `items` | `response_language` |
| `GET /v1/jp/filings` | — | `corporate_number`, `edinet_code`, `security_code`, `date_from`, `date_to`, `doc_type_code`, `form_code`, `include_withdrawn`, `limit`, `cursor`, `response_language` |
| `POST /v1/jp/regulated-entities/verify` | — | `corporate_number`, `name`, `address`, `phone`, `categories`, `response_language` |

Where no field is required, send at least one identifier. JPVerify does not read files: send the fields you read. `response_language` is `ja`, `en` or `both` (default `both`).

Japanese descriptions and request examples for every endpoint: [references/endpoints.md](references/endpoints.md), [references/examples.md](references/examples.md).

## Reading results / 結果の読み方

- `/v1/jp/companies/resolve`: `decision` is `matched` (identifier), `likely_match`, `candidates`, `identifier_conflict`, `not_found` or `source_unavailable`. `legal_name_ja` is the legally binding name — use it (or `contract_party_name`) in contracts; `name_en.source` says whether the English name is official (`nta_official_en`, `edinet_en`) or a transliteration. A T-number of an individual returns only its registration status.
- `/v1/jp/companies/verify` and `/v1/jp/companies/report`: a registered English or romanized name gives `match_type` `registered_official_english_name_exact` or `registered_romanized_name_exact` (`_prefix` for a partial name). A Latin-script name that is not a registered name returns `not_found` with risk flag `english_name_not_in_registry_index` and a `next_step` — the company may still exist under a brand; resolve it with `/v1/jp/companies/resolve` (the miss is billed, so start there for brands). `status` is `active`, `closed`, `not_found` or `multiple_matches`; `verified` is true only for a single confident match. `match_type`, `match_score` and `address_match` show how the match was made. `risk_flags` (report) lists items to confirm. The report also returns `profile` (capital, employees, founding date, website, business summary and representative in Japanese — from gBizINFO; the website may come from Wikidata; when the live gBizINFO source is unavailable the profile comes from a dated gBizINFO snapshot with `retrieval: bulk_snapshot` and no representative name), `listing` (securities and EDINET codes, latest filing), `regulated` (FSA licences found by corporate number) and `former_names` (from the NTA change log since `coverage_since`). Each section names its source; empty or `source_unavailable` means no data, not a negative finding. Verify and report also return `source_type` (`official_daily_sync` when the local NTA corporate-number register holds the NTA's newest daily file, published the same afternoon; `public_snapshot` if behind) and `source_sync` (`official_published_through`, `applied_through`, `up_to_date`).
- `/v1/jp/regulated-entities/verify`: `decision` is `verified`, `no_record_within_coverage`, `manual_review`, `out_of_scope` or `stale_source`; `coverage_status` tells whether the requested licence category is covered. "No record within coverage" is not proof that a licence is required or missing.
- `/v1/jp/filings`: an empty list means no EDINET filings matched the identifier — many private companies file nothing there.
- Candidates are ordered by name evidence first; listing, Wikidata prominence and gBizINFO employee counts only break ties between companies with the same name evidence (`signals`: `listed_company`, `wikidata_sitelinks`, `company_size`). They never turn a name into `likely_match` on their own. A brand name (`au`, `MOS Burger`) finds the company that owns the brand (`matched_alias_source: wikidata_brand`) as a candidate only — confirm it with the user. A Japan Post business-specific postal code (e.g. `530-8323` for Daikin Industries' head office) counts as postal evidence when the office name matches the candidate (`{"signal": "postal_code", "result": "match", "via": "business_postal_code"}`). Website and e-mail domains are compared with Wikidata and gBizINFO websites; a domain shared by several companies is ignored.
- English names come in this order: NTA official English name, the company's EDINET English name, its GLEIF (LEI) English legal name, the Wikidata English name, then a rendering of the registered reading: katakana loanwords as English words (Shiseido Creative for 資生堂クリエイティブ, `loanword_rendering`) or else a romanization (`furigana_transliteration`). `name_en_source` is `official`, `edinet`, `gleif`, `wikidata`, `loanword_rendering` or `furigana_transliteration`; the last two are not the company's own English name — say so if you show them. English addresses are official or Japan Post's romanization (`address_en_source`: `official`, `japan_post_romaji`); `localized.address.completeness` is `complete`, `partial` (a building name, unparsed part or town could not be romanized) or `unavailable`. With `response_language=en` a partial English address does not replace `address`, which keeps the full Japanese original — use that for mail or records. The entity lookup reports the same as `address.en_completeness`. Nothing is machine-translated; loanwords come from a dictionary (JMdict) and official English company names. For contracts and legal documents use `legal_name_ja`, the Japanese registered name, which is returned in every `response_language`.

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
  -H "X-JPVerify-Client: jp-company-verify/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"name": "Murata Manufacturing Co., Ltd.", "prefecture": "Kyoto"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/companies/resolve",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jp-company-verify/1.3.5"},
    json={"name": "Murata Manufacturing Co., Ltd.", "prefecture": "Kyoto"},
    timeout=60,
)
print(response.status_code, response.json())
```

x402 (no account):

```bash
# No key: shows the HTTP 402 x402 price; pay with an x402 client and retry with PAYMENT-SIGNATURE.
curl -i -X POST https://api.jpverify.com/v1/jp/companies/resolve \
  -H "X-JPVerify-Client: jp-company-verify/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"name": "Murata Manufacturing Co., Ltd.", "prefecture": "Kyoto"}'
```

Full SDK examples (Python `x402`, JavaScript `@x402/fetch`): https://api.jpverify.com/docs/x402

## Limits and privacy / 制限とプライバシー

- Results are a **public-registry pre-check** with the source and as-of date of the data. They are not KYB, AML or sanctions screening, and not legal, tax or accounting advice. A "not found" does not mean the entity does not exist or is risky.
- If `manual_review_required` is true or a status is ambiguous, show the evidence to the user and let them decide; do not decide on their behalf.
- Only send data the user is entitled to process. JPVerify takes fields, not files; do not send personal details (names, phone numbers, e-mail addresses) that a check does not need.
- Docs: API key https://api.jpverify.com/docs/api-key · x402 https://api.jpverify.com/docs/x402 · terms https://api.jpverify.com/en/terms · privacy https://api.jpverify.com/en/privacy
