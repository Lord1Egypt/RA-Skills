---
name: pi-ppt
description: Generate PPTs using services provided by PI (Presentation Intelligence).
metadata:
  openclaw:
    emoji: "✨"
    requires:
      bins:
        - python3
      env:
        - PIPPT_BASE_URL
        - PIPPT_APP_ID
        - PIPPT_APP_SECRET
    primaryEnv: PIPPT_APP_ID
---

# Pi PPT Generation

## Functionality
1. Generate PPTs using the PI (Presentation Intelligence) API.

## Setup
1.  **API Key:** Ensure the PIPPT_BASE_URL, PIPPT_APP_ID and PIPPT_APP_SECRET environment variables are set with your valid API key. You can obtain API key from the PI website: https://www.pi.inc/  .
2.  **Environment:** The API key should be available in the runtime environment.

## Generate a PPT
Run the following script:
```bash
PIPPT_BASE_URL=xxx PIPPT_APP_ID=xxx PIPPT_APP_SECRET=xxx python3 scripts/generate_pi_ppt.py --content  --language --cards --file
```
Input arguments:
   content(str, required): Topic and description, for example: "Create a PPT introducing Chinese GPU vendors in a formal business style."
   cards(int, optional): Expected number of slides, for example 10. Default is 8. If you generate a PPT from an uploaded document, do not specify cards because the slide count is determined by the document content.
   language(str, required): Target language of the PPT. 'zh' for Chinese, 'en' for English. Default is 'zh'.
   file(str, optional): Path to the document to upload, for example: "/Users/jack/download/weekly_report_20250304.doc". Supported file types: .doc/.docx/.txt/.md/.pdf/.pptx/.ppt. Other file types are not supported. Only one document can be uploaded.

Complete command examples:

**Generate from an uploaded document** (slide count is determined by content, do not pass `--cards`):

```bash
PIPPT_BASE_URL=xxx PIPPT_APP_ID=xxx PIPPT_APP_SECRET=xxx python3 scripts/generate_pi_ppt.py \
  --content "Generate a well-structured business report PPT based on the attached document" \
  --language zh \
  --file "/Users/YourName/Documents/quarterly_review.docx"
```

**Generate from a one-line prompt / topic** (you can specify slide count):

```bash
PIPPT_BASE_URL=xxx PIPPT_APP_ID=xxx PIPPT_APP_SECRET=xxx python3 scripts/generate_pi_ppt.py \
  --content "Create a PPT introducing Chinese GPU vendors in a formal business style" \
  --language zh \
  --cards 10
```
## Notes
- Generating one PPT usually takes about 3-6 minutes. Please remind users to be patient.
