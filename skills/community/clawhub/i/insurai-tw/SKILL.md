---
name: insurai-tw
version: 1.0.6
description: Use for Republic of China (Taiwan) personal insurance tasks through the InsurAI Agent API, including insurance planning interpretation, occupation classification, product recommendation and search, policy review, coverage-gap analysis, metadata lookup, contract or premium document retrieval, and PDF link lookup. Apply the mandatory scope and rejection rules before any API call. For policy images or PDFs, use external OCR/document-processing capability first, then analyze the extracted text with this skill. Requires INSURAI_API_KEY from https://insurai.com.tw. 適用於中華民國（臺灣）保險相關任務，包括保險規劃分析、保單檢視、保障缺口分析、保險商品推薦、商品檢索、文件取得、商品 metadata 查詢與保險個人職業分類表查詢。呼叫 API 前請先套用必要的適用範圍與拒絕規則；若為保單圖片或 PDF，須先由外部 OCR／文件處理能力轉成文字後，再交由本 skill 分析。使用前需先至 https://insurai.com.tw 註冊會員並申請 INSURAI-API-KEY。
---

# InsurAI Taiwan

Use this skill for supported Taiwan personal insurance workflows.

## Before You Use

This skill requires an `INSURAI_API_KEY`. Register at https://insurai.com.tw, sign in, apply for an `INSURAI-API-KEY`, then set `INSURAI_API_KEY`. `INSURAI_AGENT_URL` is optional and defaults to the production endpoint.

使用前請先至 https://insurai.com.tw 註冊會員，登入後申請 `INSURAI-API-KEY`，再設定 `INSURAI_API_KEY`。`INSURAI_AGENT_URL` 可省略，預設使用正式端點。

```bash
export INSURAI_API_KEY=your_api_key_here
# Optional: override the production endpoint.
export INSURAI_AGENT_URL=https://insurai.com.tw/insurai/agent
```

## Security and Capability Boundaries

This skill invokes the bundled Python helper to call the InsurAI Agent API.

Privacy and data handling:

- User inputs for insurance planning and product lookup may include sensitive personal or financial information, such as age, gender, location, occupation, family situation, insurance holdings, health-related context, and coverage needs.
- The helper transmits the minimum fields required for the selected action to `INSURAI_AGENT_URL`.
- For policy images or PDFs, use external OCR or document-processing capability first, then submit only the extracted text and the minimum follow-up inputs needed for analysis.
- Before invoking the API for the first time in a conversation, tell users that their insurance/planning inputs will be sent to the configured InsurAI Agent API endpoint and obtain their consent to continue.
- Minimize submitted data. Do not include national ID numbers, contact details, full policy documents, payment data, medical records, or other unnecessary identifiers unless the user explicitly requests it and the selected action requires it.
- When assisting someone other than the requester, obtain the person's consent before sending their personal insurance or planning information.

Environment variables used:

- `INSURAI_AGENT_URL`: HTTPS API base URL. Defaults to `https://insurai.com.tw/insurai/agent`.
- `INSURAI_API_KEY`: API key sent only as the `X-API-KEY` header to `INSURAI_AGENT_URL`.

Network access:

- The helper sends requests only to `INSURAI_AGENT_URL`.
- The default production endpoint is `https://insurai.com.tw/insurai/agent`.
- `INSURAI_AGENT_URL` must use `https`; non-HTTPS URLs are rejected before any API request.

Data sent to the API:

- User-provided insurance scenarios, occupation keywords, product search terms, insurer filters, age, gender, occupation level, product codes, and document type parameters as required by the selected action.

Boundaries:

- This skill does not enumerate local files.
- This skill does not enumerate environment variables; it reads only `INSURAI_AGENT_URL` and `INSURAI_API_KEY`.
- This skill does not read or upload user files to the InsurAI API. For policy images or PDFs, external OCR or document-processing capability must extract text first, and this skill analyzes only the extracted text plus required follow-up inputs.
- This skill does not print or expose `INSURAI_API_KEY`.
- This skill does not execute `sudo`, install packages, fetch external scripts, or run arbitrary shell commands.

中文摘要：本 skill 僅透過內建 Python helper 呼叫 InsurAI Agent API，只讀取 `INSURAI_AGENT_URL` 與 `INSURAI_API_KEY`，不列舉環境變數、不直接將使用者檔案上傳至 API、不輸出 API key，也不執行 sudo、安裝套件、下載外部腳本或任意 shell 指令。若為保單圖片或 PDF，須先由外部 OCR／文件處理能力轉成文字，再以最小必要資訊交由本 skill 分析。`INSURAI_AGENT_URL` 必須使用 HTTPS；保險查詢資料送出前應告知使用者、取得同意，並採最小化原則。

## Required References

Read references according to the task:

- Read [insurai-rules.md](references/insurai-rules.md) before every request. It defines supported scope, mandatory rejection responses, insurer normalization, value domains, workflow rules, and response behavior.
- Read [insurai-api-spec.md](references/insurai-api-spec.md) when selecting an endpoint or interpreting request and response fields.
- Read [insurai-api-script.md](references/insurai-api-script.md) when invoking or troubleshooting the Python helper.
- Read [policy-review-workflow.md](references/policy-review-workflow.md) for policy review, coverage-gap analysis, cancellation/keep comparisons, or when the user provides an existing policy image, PDF, or product list for evaluation.

Treat `insurai-rules.md` as authoritative for business behavior and `insurai-api-spec.md` as authoritative for the REST contract.

## Execution Order

1. Confirm the request is about supported Taiwan personal insurance.
2. Apply the mandatory direct-rejection rules before any API call.
3. Validate requested insurers against the supported insurer table.
4. Normalize gender, recommendation type, document type, age, occupation level, and insurer identifiers.
5. Check `INSURAI_AGENT_URL` and `INSURAI_API_KEY`.
6. Before the first API call in a conversation, disclose that necessary insurance/planning inputs will be transmitted to `INSURAI_AGENT_URL`, minimize the submitted data, and obtain the user's consent to continue.
7. Run the Python helper from the installed skill root:

```bash
python3 scripts/insurai_api.py <action> [args...]
```

8. Base product-specific claims on API results. Do not invent products, benefits, premiums, underwriting rules, documents, or PDF links.
9. For policy review tasks, first normalize the user's existing policy into product candidates, convert policy short codes to InsurAI `productCode` values via `search`, then use `batch-metadata` or `metadata` before making product-specific claims.
10. For policy review recommendations, compare current coverage against the user's needs, then validate shortlisted products with `document --campaign-type premium` before quoting premiums or plan comparisons.
11. Follow endpoint-specific error handling and stop when the rules require it.

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
- For policy review, do not send policy short codes directly to `metadata`; resolve them to InsurAI `productCode` values first.
- For policy review, do not present keep/cancel/reduce-or-replace conclusions before completing the API lookup and coverage-gap comparison workflow.
- Return full Markdown or a PDF link only when the user asks for it.
- Never continue with general insurance assumptions after an API error that requires stopping.

## Version

Current version: `1.0.6`

## Copyright

Copyright (c) 2026 JRSoft Technology Ltd.

Licensed under the MIT License. See `LICENSE`.
