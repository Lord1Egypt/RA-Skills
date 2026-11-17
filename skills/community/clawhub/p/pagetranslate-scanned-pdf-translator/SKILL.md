---
name: pagetranslate-scanned-pdf-translator
description: "Use this skill whenever the user wants a scanned PDF, a photographed page or an image of text (PNG, JPG, WEBP, TIFF) translated. PageTranslate reads the scan with OCR, translates it and puts the translation back on the page, so the result is still a PDF or image, not loose text."
version: 0.1.3
author: Caravaca Labs
license: MIT
homepage: https://pagetranslate.ai/faq/how-to-translate-scanned-pdf
compatibility: Needs network access, curl and a PageTranslate API key in PAGETRANSLATE_API_KEY. Uses the pagetranslate MCP tools when they are installed.
required_environment_variables:
  - name: PAGETRANSLATE_API_KEY
    prompt: "PageTranslate API key"
    help: "Create one at https://pagetranslate.ai/dashboard/api-keys (free account, verified email)"
    required_for: "Uploading documents and downloading translations"
metadata:
  openclaw:
    homepage: https://pagetranslate.ai/faq/how-to-translate-scanned-pdf
    tags: ["translation", "ocr", "scanned-pdf", "image-translation", "pagetranslate"]
    requires:
      bins: ["curl"]
      env: ["PAGETRANSLATE_API_KEY"]
    primaryEnv: PAGETRANSLATE_API_KEY
  hermes:
    tags: ["translation", "ocr", "scanned-pdf", "image-translation", "pagetranslate"]
    category: productivity
    requires_toolsets: ["terminal"]
---

# PageTranslate Scanned PDF Translator

Translate a scanned PDF or a photo of a page. PageTranslate reads it with OCR, translates it, and puts the translation back on the page.

[PageTranslate](https://pagetranslate.ai) translates the file itself, not pasted text. For a sentence or a
paragraph, translate it yourself.

## When to use

- The PDF has no selectable text: a scan, a fax, a photographed book or form.
- The file is an image of text: PNG, JPG, WEBP, TIFF, BMP or GIF.
- You tried to read the PDF's text and got nothing, or only fragments.

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

## Scan notes

- A scan's price comes from a sample of its pages. That price is locked: it is what the user pays.
- Scans in Latin-script languages (English, Spanish, French, German, Portuguese and so on) work. A scan in Chinese, Japanese, Korean, Arabic, Hebrew, Hindi or Thai, or one too faint to read, is refused with a message. Do not retry it.
- For a refused Chinese, Japanese or Korean scan, the fix is an OCR tool that adds a text layer to the PDF. Then upload that PDF.
- A scan takes longer than a text PDF, because OCR runs first. Keep polling; do not upload it again.

## Problems

- **401:** the key is missing or revoked. Ask the user to create a new one.
- **429 on upload:** uploads are rate limited per account. Wait, do not retry in a loop.
- **"Unsupported language code":** use one of the codes above.
- **Stuck at `pending`:** the job is unpaid. Give the user the payment link again.

## Links

- Guide: [how to translate a scanned PDF](https://pagetranslate.ai/faq/how-to-translate-scanned-pdf)
- Online version: [PageTranslate PDF translator](https://pagetranslate.ai/pdf-translator)
- Making scans: [how to turn a scanned document into a PDF](https://pagetranslate.ai/blog/how-to-turn-a-scanned-document-into-a-pdf)
- Text layers: [how to make a PDF file searchable](https://pagetranslate.ai/blog/how-to-make-a-pdf-file-searchable)
- Many files: [batch OCR for PDFs](https://pagetranslate.ai/blog/batch-ocr-pdf)
- Source and docs: [GitHub](https://github.com/Caravaca-Labs/pagetranslate-mcp) · [npm](https://www.npmjs.com/package/pagetranslate-mcp) · [PageTranslate](https://pagetranslate.ai)

## Safety

- Uploading sends the file to PageTranslate. Upload only the file the user asked to translate.
- Never print the API key or write it to a file.
- Do not say a translation is running until `payment_status` is `paid`.
- Never pay, or enter card details, for the user. Payment is theirs to make in the browser.
