---
name: pagetranslate-pdf-translator
description: "Use this skill whenever the user wants a PDF translated into another language and returned as a PDF with its pages, tables, fonts and images in place: manuals, contracts, reports, papers, brochures, large PDFs. Uploads the file to PageTranslate, shows the exact price first, and downloads the translated PDF."
version: 0.1.3
author: Caravaca Labs
license: MIT
homepage: https://pagetranslate.ai/pdf-translator
compatibility: Needs network access, curl and a PageTranslate API key in PAGETRANSLATE_API_KEY. Uses the pagetranslate MCP tools when they are installed.
required_environment_variables:
  - name: PAGETRANSLATE_API_KEY
    prompt: "PageTranslate API key"
    help: "Create one at https://pagetranslate.ai/dashboard/api-keys (free account, verified email)"
    required_for: "Uploading documents and downloading translations"
metadata:
  openclaw:
    homepage: https://pagetranslate.ai/pdf-translator
    tags: ["translation", "pdf", "pdf-translator", "translate-pdf", "pagetranslate"]
    requires:
      bins: ["curl"]
      env: ["PAGETRANSLATE_API_KEY"]
    primaryEnv: PAGETRANSLATE_API_KEY
  hermes:
    tags: ["translation", "pdf", "pdf-translator", "translate-pdf", "pagetranslate"]
    category: productivity
    requires_toolsets: ["terminal"]
---

# PageTranslate PDF Translator

Translate a PDF with PageTranslate and get a PDF back: the same pages, tables, fonts and images, in the new language.

[PageTranslate](https://pagetranslate.ai) translates the file itself, not pasted text. For a sentence or a
paragraph, translate it yourself.

## When to use

- The user names a `.pdf` file and a language, or asks to translate a PDF.
- The layout matters: tables, columns, figures, page numbers, headers and footers.
- The PDF is long. One file can have up to 1,000 pages and 100 MB.

## Before you start

- **Target language:** a code such as `es`, `fr`, `de`, `it`, `ja`, `ko`, `ar`, `hi`, `ru`.
  Use `pt-BR` for Brazilian Portuguese, `zh` for Simplified and `zh-TW` for Traditional Chinese.
  The source language is detected. If the user did not name a target language, ask.
- **API key:** the user creates one at https://pagetranslate.ai/dashboard/api-keys (free account, verified
  email) and sets it as `PAGETRANSLATE_API_KEY`.
- **Price:** uploading is free and returns the exact price. Nothing is charged until the user pays.
- **Limits:** PDF, DOCX, EPUB, PNG, JPG, WEBP, TIFF, BMP, GIF. Up to 100 MB and 1,000 PDF pages.

## Steps

Use the `pagetranslate` MCP tools when they are available. Otherwise use curl (next section).

1. **Upload:** `upload_document` with the file's absolute path and the target language. It returns
   `job_id`, `word_count`, `price` and `next_step`.
2. **Tell the user the price and get a yes.** Then:
   - If the response has a `payment_url`, give the user that link. They pay by card in the browser,
     and the translation starts by itself.
   - If the price is `0.00` (covered by the account's word balance), call `start_translation`.
3. **Wait:** call `get_translation` about every 30 seconds until `status` is `completed`. If
   `status` is `failed`, tell the user the reason given.
4. **Download:** `download_translation` with `output_dir` set to the source file's folder. It never
   overwrites a file. Tell the user the saved path.

`list_translations` shows earlier jobs, for example to download one again.

## Without the MCP server

Same steps over HTTPS. Every request carries `Authorization: Bearer $PAGETRANSLATE_API_KEY`.

```bash
API=https://api.pagetranslate.ai/api/v1

# 1. Upload (free). The response has job_id and quote.total_cents.
curl -sS -X POST "$API/upload/" -H "Authorization: Bearer $PAGETRANSLATE_API_KEY" \
  -F "file=@/path/to/file" -F "requested_language=es"

# 2. Start from the account's word balance. A 400 "Insufficient credits" means the user
#    pays by card at https://pagetranslate.ai/dashboard?resume=JOB_ID#upload instead.
curl -sS -X POST "$API/jobs/JOB_ID/translate" -H "Authorization: Bearer $PAGETRANSLATE_API_KEY" \
  -H "Content-Type: application/json" -d '{}'

# 3. Poll until "status" is "completed" ("payment_status" shows whether it was paid).
curl -sS "$API/jobs/JOB_ID" -H "Authorization: Bearer $PAGETRANSLATE_API_KEY"

# 4. Download. -OJ keeps the server's file name; run it in the folder to save into.
curl -sS -OJ "$API/jobs/JOB_ID/download" -H "Authorization: Bearer $PAGETRANSLATE_API_KEY"
```

## PDF notes

- The result is a PDF. Do not extract the text and translate it yourself; that loses the layout.
- A PDF with no selectable text is a scan. PageTranslate reads it with OCR. Scans in Chinese, Japanese, Korean, Arabic, Hebrew, Hindi or Thai are refused; see the scanned PDF guide below.
- The saved file keeps the service's name for it (for example `job-<id>-es.pdf`). Tell the user the path.

## Problems

- **401:** the key is missing or revoked. Ask the user to create a new one.
- **429 on upload:** uploads are rate limited per account. Wait, do not retry in a loop.
- **"Unsupported language code":** use one of the codes above.
- **Stuck at `pending`:** the job is unpaid. Give the user the payment link again.

## Links

- Online version: [PageTranslate PDF translator](https://pagetranslate.ai/pdf-translator)
- Long files: [translate a large PDF](https://pagetranslate.ai/pdf-translator/translate-large-pdf)
- Scans: [how to translate a scanned PDF](https://pagetranslate.ai/faq/how-to-translate-scanned-pdf)
- Language pairs: [Chinese to English PDF converter](https://pagetranslate.ai/pdf-translator/chinese-to-english-pdf-converter)
- Comparison: [DeepL alternative for PDFs](https://pagetranslate.ai/blog/deepl-alternative)
- Source and docs: [GitHub](https://github.com/Caravaca-Labs/pagetranslate-mcp) · [npm](https://www.npmjs.com/package/pagetranslate-mcp) · [PageTranslate](https://pagetranslate.ai)

## Safety

- Uploading sends the file to PageTranslate. Upload only the file the user asked to translate.
- Never print the API key or write it to a file.
- Do not say a translation is running until `payment_status` is `paid`.
- Never pay, or enter card details, for the user. Payment is theirs to make in the browser.
