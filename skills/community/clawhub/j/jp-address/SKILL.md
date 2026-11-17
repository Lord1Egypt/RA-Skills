---
name: jp-address
description: >-
  Normalize, parse, validate and geocode Japanese addresses (住所の正規化・解析・検証) with JPVerify,
  and look up Japanese postal codes (郵便番号) — down to 丁目, block and building level, with the
  evidence behind each match. Use when a task involves cleaning or standardizing a Japanese address,
  checking that an address exists at a required precision, splitting it into components, finding
  coordinates, or finding the area for a postal code. Paid per call (API key credits or x402).
license: MIT
---

# Japanese addresses / 日本の住所

Version 1.3.5 · JPVerify · https://www.jpverify.com

## When to use / いつ使うか

- Clean up or standardize a Japanese address (full-width/half-width digits, 丁目・番・号 notation, kanji numerals).
- Split an address into prefecture, city, ward, town, 丁目, block, lot and building.
- Check that an address exists at a required precision before shipping, onboarding or storing it.
- Get coordinates, or the areas that belong to a postal code.

## Connect / 接続

JPVerify is a paid, per-call API. Pick the first option that applies; never guess credentials.

1. **API key (recommended).** If the environment has `JPVERIFY_API_KEY` (a `jpv_live_…` key the user created), send it on every call:
   - HTTP: header `Authorization: Bearer $JPVERIFY_API_KEY` (or `X-API-Key`).
   - MCP: if the JPVerify Claude Code plugin is installed, the `jpverify` MCP server is already configured and uses the key saved in the plugin's settings (`/plugin` → JPVerify → Configure), not `JPVERIFY_API_KEY`. Otherwise: `claude mcp add --transport http jpverify https://api.jpverify.com/mcp --header "Authorization: Bearer $JPVERIFY_API_KEY" --header "X-JPVerify-Client: jp-address/1.3.5"`
   Each successful call is deducted from the user's prepaid USD credits; failed or invalid calls are refunded automatically. Before a large batch, check the balance for free: `GET https://api.jpverify.com/v1/account/balance` with the same header, or the MCP tool `jpverify_balance`.
2. **x402 wallet.** If you have an x402 client with USDC on Base (`eip155:8453`) and the user approved a budget, call without a key: the API answers HTTP 402 with the exact price; sign and retry with `PAYMENT-SIGNATURE`. Pay only within the approved budget.
3. **Neither.** Do not pay and do not invent a key. The MCP server also works without a key for the free tool `jpverify_guide` (`claude mcp add --transport http jpverify https://api.jpverify.com/mcp`); use it to confirm which call fits, then tell the user they can create a free account with starter credit at https://www.jpverify.com/signup?ref=jp-address and set `JPVERIFY_API_KEY`.

Always send `X-JPVerify-Client: jp-address/1.3.5` on HTTP calls. Never print, log or share the API key.

## Workflow / 手順

1. **Pick the cheapest call that answers the question.**
   - Postal code → areas: `POST /v1/jp/postal-codes/lookup` (cheapest). Business-specific codes of large offices (事業所個別郵便番号, e.g. 100-8310) are found too.
   - Standard written form (components, completed town, Japan Post English, postal-master consistency): `POST /v1/jp/addresses/normalize` (MCP `jp_address_normalize`). This is the default. It returns no coordinates and no final decision.
   - Split as written only, cheapest ($0.002): `POST /v1/jp/addresses/parse`. Nothing is completed, checked or geocoded.
   - Coordinates / candidates: `POST /v1/jp/addresses/geocode` (the only call that returns coordinates).
   - A decision on whether the address is real at the level you need: `POST /v1/jp/addresses/validate` (the only call that decides).
   - "Is this address good enough?": `POST /v1/jp/addresses/validate` (MCP `jp_address_validate`) with `required_level` (5/6 = 大字・字, 7 = block/街区, 8 = building/house) and `strict` when every supplied piece of evidence must agree.
2. **Send the address as written**: Japanese, or romanized if that is all you have (`1-9-1 Marunouchi, Chiyoda-ku, Tokyo`; `postal-lookup` and geocode `components` also take `Tokyo` / `Chiyoda-ku` / `Marunouchi`). Romanized input is read back via Japan Post romaji; `romanized_input.status` is `matched`, `ambiguous` (with candidates) or `not_found`, and nothing is guessed. Do not translate a Japanese address into English first. You can pass the output of `parse`/`postal-lookup`/`geocode` to `validate` as `parsed`, `postal_evidence` or `geocode_evidence` instead of calling again.
3. **Many addresses?** Up to 1,000 normalizations run as one x402 batch job (`/v1/batch-jobs`, operation `address_normalize`); confirm the total cost with the user first.

## Endpoints and prices / エンドポイントと料金

| Endpoint | MCP tool | Price (USD) | Use when | Returns |
|---|---|---|---|---|
| `POST /v1/jp/addresses/normalize` | `jp_address_normalize` | $0.005 | You need Japanese address normalization or standardization, whether or not the input contains a postal code. | Standard written form: normalized components, a unique truncated town completed, an English address from Japan Post romanization, and postal-master consistency and candidates. It does not infer a missing postal code, return coordinates (geocode) or give a final decision (validate). |
| `POST /v1/jp/addresses/validate` | `jp_address_validate` | $0.005 | You need one evidence-based Japanese address quality decision combining parsed address, postal evidence, and geocoder evidence. | Exact, partial, ambiguous, conflict, or unverified status with accepted hierarchy, confidence signals, validation scope, and reasons. |
| `POST /v1/jp/addresses/parse` | — | $0.002 | You only need the address split into prefecture, city, town, chome, block, lot or house as written (cheapest address call). | Components as written, normalized value, English address and components from Japan Post romanization, unparsed fragments, parser status and confidence. No town completion, postal check, coordinates or decision. |
| `POST /v1/jp/addresses/geocode` | — | $0.005 | You need Japanese forward-geocoding candidates, coordinates, address IDs, or hierarchy levels. The required hierarchy is inferred from the input. | Provider-neutral Jageocoder candidates with normalized address, coordinates, address ID, match level, granularity, confidence, reasons, unmatched tails, and dictionary status. Level 5/6 is oaza/aza, 7 is block, and 8 is building or house node when covered. City-level or town-prefix candidates remain partial; town-level results are not door-number or coordinate accuracy claims. Parcel addresses (番地) match at level 7; a sub-number (枝番) the dictionary lacks stays partial. |
| `POST /v1/jp/postal-codes/lookup` | — | $0.001 | You need a Japan Post postal-code lookup or reverse lookup from a postal code or administrative address. | Japan Post local-snapshot matches with postal code, prefecture, city, town, kana, Japan Post romanized prefecture/city/town, confidence, source, data version, and candidate count. Business-specific codes of single offices (e.g. 100-8310) return postal_code_type business_specific with the office name and street. |

### Request fields / リクエスト項目

| Endpoint | Required fields | Optional fields |
|---|---|---|
| `POST /v1/jp/addresses/normalize` | `address` | `response_language` |
| `POST /v1/jp/addresses/validate` | — | `address`, `parsed`, `postal_evidence`, `geocode_evidence`, `required_level`, `strict` |
| `POST /v1/jp/addresses/parse` | `address` | `postal_code`, `response_language`, `parser_profile` |
| `POST /v1/jp/addresses/geocode` | — | `address`, `components`, `postal_code`, `max_candidates`, `minimum_acceptable_level`, `provider` |
| `POST /v1/jp/postal-codes/lookup` | — | `postal_code`, `prefecture`, `county`, `city`, `ward`, `town`, `max_results` |

Where no field is required, send at least one identifier. JPVerify does not read files: send the fields you read. `response_language` is `ja`, `en` or `both` (default `both`).

Japanese descriptions and request examples for every endpoint: [references/endpoints.md](references/endpoints.md), [references/examples.md](references/examples.md).

## Reading results / 結果の読み方

- `validate`: `address_validated` is true only when the address reaches `requested_level`. `match_status` is `exact`, `normalized_exact`, `partial`, `ambiguous`, `conflict`, `not_found` or `unverified`; `reasons` explains why. `partial` usually means the address is real but less precise than requested (e.g. no house number).
- `geocode`: `verified_level` and `precision_satisfied` tell how deep the match went; `normalize`: `match_level` is the depth read from the address; `candidate_count` above 1 means the address is ambiguous — show the candidates instead of choosing one.
- A missing postal code is **not** inferred by `normalize`; use `postal-lookup` if the user needs it.
- Business-specific postal codes: a `postal-lookup` match has `postal_code_type` `area` or `business_specific`; a business code also returns the office's `business_name`, `street` and `business_kind` (`office` or `po_box`). `normalize` and `validate` accept a business code that matches its address and still report a conflict when it does not. Reverse lookup by address never returns a business code — a business code belongs to one office, not to the area.
- Parcel addresses (地番, e.g. `大字柏倉2462番地`) match at level 7. A sub-number (枝番, the `19` in `5番地19`) that the registry dictionary does not hold stays `partial` with the unmatched part in `unmatched_tail` — the parcel exists, the sub-number was not confirmed.
- `warnings` may include `duplicate_spelling_candidates_merged`: the dictionary holds one house under two spellings at the same point (e.g. 南十二条 / 南１２条), returned once.
- `normalized_en` uses Japan Post's official romanization (KEN_ALL_ROME), e.g. `1-9-1 Marunochi, Chiyoda-ku, Tokyo 100-0005`, with `normalized_en_source: japan_post_romaji` and a `normalized_en_confidence`. Japan Post's spelling is kept as published (no long-vowel marks), and building names are not translated. `/v1/jp/addresses/parse` also returns `components_en`, and each `/v1/jp/postal-codes/lookup` match returns `prefecture_en`, `city_en` and `town_en`. Nothing is machine-translated.
- `normalized_en_common` gives the spelling people usually write where Japan Post's differs (丸の内: Marunouchi rather than Japan Post's Marunochi); use it for display and keep `normalized_en` for matching Japan Post data.

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

## Example / 呼び出し例 (`POST /v1/jp/addresses/normalize`)

API key:

```bash
curl -X POST https://api.jpverify.com/v1/jp/addresses/normalize \
  -H "Authorization: Bearer $JPVERIFY_API_KEY" \
  -H "X-JPVerify-Client: jp-address/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"address": "東京都新宿区西新宿2丁目8番1号", "response_language": "both"}'
```

```python
import os, requests

response = requests.post(
    "https://api.jpverify.com/v1/jp/addresses/normalize",
    headers={"Authorization": f"Bearer {os.environ['JPVERIFY_API_KEY']}",
             "X-JPVerify-Client": "jp-address/1.3.5"},
    json={"address": "東京都新宿区西新宿2丁目8番1号", "response_language": "both"},
    timeout=60,
)
print(response.status_code, response.json())
```

x402 (no account):

```bash
# No key: shows the HTTP 402 x402 price; pay with an x402 client and retry with PAYMENT-SIGNATURE.
curl -i -X POST https://api.jpverify.com/v1/jp/addresses/normalize \
  -H "X-JPVerify-Client: jp-address/1.3.5" \
  -H "Content-Type: application/json" \
  -d '{"address": "東京都新宿区西新宿2丁目8番1号", "response_language": "both"}'
```

Full SDK examples (Python `x402`, JavaScript `@x402/fetch`): https://api.jpverify.com/docs/x402

## Limits and privacy / 制限とプライバシー

- Results are a **public-registry pre-check** with the source and as-of date of the data. They are not KYB, AML or sanctions screening, and not legal, tax or accounting advice. A "not found" does not mean the entity does not exist or is risky.
- If `manual_review_required` is true or a status is ambiguous, show the evidence to the user and let them decide; do not decide on their behalf.
- Only send data the user is entitled to process. JPVerify takes fields, not files; do not send personal details (names, phone numbers, e-mail addresses) that a check does not need.
- Docs: API key https://api.jpverify.com/docs/api-key · x402 https://api.jpverify.com/docs/x402 · terms https://api.jpverify.com/en/terms · privacy https://api.jpverify.com/en/privacy
