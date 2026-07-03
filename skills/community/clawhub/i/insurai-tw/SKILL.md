---
name: insurai-tw
version: 1.0.3
description: Use for Republic of China (Taiwan) personal insurance tasks through the InsurAI Agent API, including insurance planning interpretation, occupation classification, product recommendation and search, metadata lookup, contract or premium document retrieval, and PDF link lookup. Apply the mandatory scope and rejection rules before any API call. 適用於中華民國（臺灣）保險相關任務，包括保險規劃分析、保險商品推薦、商品檢索、文件取得、商品 metadata 查詢與保險個人職業分類表查詢。
---

# InsurAI Taiwan

Use this skill for supported Taiwan personal insurance workflows.

## Required References

Read references according to the task:

- Read [insurai-rules.md](references/insurai-rules.md) before every request. It defines supported scope, mandatory rejection responses, insurer normalization, value domains, workflow rules, and response behavior.
- Read [insurai-api-spec.md](references/insurai-api-spec.md) when selecting an endpoint or interpreting request and response fields.
- Read [insurai-api-script.md](references/insurai-api-script.md) when invoking or troubleshooting the Python helper.

Treat `insurai-rules.md` as authoritative for business behavior and `insurai-api-spec.md` as authoritative for the REST contract.

## Execution Order

1. Confirm the request is about supported Taiwan personal insurance.
2. Apply the mandatory direct-rejection rules before any API call.
3. Validate requested insurers against the supported insurer table.
4. Normalize gender, recommendation type, document type, age, occupation level, and insurer identifiers.
5. Check `INSURAI_AGENT_URL`, `INSURAI_API_KEY`, and TLS verification settings.
6. Run the Python helper from the installed skill root:

```bash
python3 scripts/insurai_api.py <action> [args...]
```

7. Base product-specific claims on API results. Do not invent products, benefits, premiums, underwriting rules, documents, or PDF links.
8. Follow endpoint-specific error handling and stop when the rules require it.

## API Actions

| Task                         | Action               |
| ---------------------------- | -------------------- |
| Insurance planning           | `plan_interpret`     |
| Occupation lookup            | `occupations_search` |
| Product recommendation       | `recommend`          |
| Product search               | `search`             |
| Product metadata             | `metadata`           |
| Batch metadata               | `batch-metadata`     |
| Contract or premium document | `document`           |
| PDF link                     | `pdf_link`           |

Use `--insurers` for insurer names or codes and `--protection` for one or more protection names. Search defaults to available products; use `--no-available-product` only when discontinued products are required.

## Response Discipline

- Summarize relevant API fields instead of dumping raw JSON.
- For planning failures with `success=false`, report only the documented reason or code and stop.
- Determine product coverage from `mainBenefits`, not solely from product names or broad contract types.
- Treat `productCodes` as the recommendation result key and handle `supplementaryRiders` as an array that may be empty.
- Treat metadata responses as JSON objects, not JSON strings.
- When metadata includes `officialRiderContracts`, interpret it as the main policy's officially supported rider contract list.
- When metadata includes `eligibleMainContracts`, interpret it as the list of main contracts that can pair with the current non-main product.
- Expect metadata to include `officialRiderContracts` or `eligibleMainContracts` depending on whether the current product is main or non-main.
- Use `officialRiderContracts` and `eligibleMainContracts` as authoritative pairing data; do not infer main-rider compatibility from product names alone.
- Return full Markdown or a PDF link only when the user asks for it.
- Never continue with general insurance assumptions after an API error that requires stopping.

## Version

Current version: `1.0.3`

## Copyright

Copyright (c) 2026 JRSoft Technology Ltd.

Licensed under the MIT License. See `LICENSE`.
