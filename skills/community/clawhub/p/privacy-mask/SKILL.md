---
name: privacy-mask
description: >-
  Mask, redact, anonymize and censor sensitive information (PII) in
  screenshots and images — phone numbers, emails, IDs, API keys, crypto
  wallets, credit cards, passwords, and more. Uses OCR (Tesseract +
  RapidOCR) with 47 regex rules and optional NER (GLiNER) to detect private
  data and applies blur/fill redaction overlays. Supports GDPR and
  compliance workflows, secret detection, and data loss prevention (DLP).
  All processing runs 100% locally and offline — no data leaves your machine.
version: 0.3.5
license: MIT
compatibility: Requires tesseract OCR, Python 3.10+, and pre-installed privacy-mask CLI.
metadata:
  author: wuhao
  openclaw:
    requires:
      bins:
        - tesseract
        - python3
        - privacy-mask
    emoji: "\U0001F6E1"
    homepage: https://github.com/fullstackcrew-alpha/privacy-mask
  permissions:
    - id: local-file-read
      description: >-
        Reads image files provided by the user to perform OCR-based
        sensitive information detection. No files are copied or transmitted.
      scope: local
      optional: false
    - id: local-file-write
      description: >-
        Writes masked output images to the local filesystem (same directory
        as input, with _masked suffix, or user-specified path).
      scope: local
      optional: false
  hooks:
    - event: UserPromptSubmit
      description: >-
        Intercepts images in Claude's local image cache and applies
        privacy masking (blur/fill redaction) in-place before they are
        sent to the API. Runs entirely locally with no network calls.
        Requires the privacy-mask CLI to be installed.
      command: scripts/mask-images.sh
      timeout: 30000
---

# Privacy Mask

Detect and mask sensitive information in images locally before they leave your machine.

## Prerequisites

This skill requires the `privacy-mask` CLI to be pre-installed on the system.
If it is not available, inform the user that they need to install it first:

1. Install via pip: `pip install privacy-mask`
2. Ensure Tesseract OCR is installed: `brew install tesseract` (macOS) or `apt install tesseract-ocr` (Linux)
3. Verify installation: `privacy-mask --version`
4. (Optional) Install NER support: `pip install privacy-mask[ner]`

## When to use

- User sends a screenshot or image file (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff`) that may contain private data
- User mentions privacy, masking, redacting, or anonymizing
- You need to analyze an image but want to redact sensitive info first
- IF the user shares a screenshot for debugging, THEN run `privacy-mask mask <path> --dry-run` first to check for PII
- IF detections are found, THEN mask the image before proceeding with analysis

## Usage

Mask an image:
```bash
privacy-mask mask /path/to/screenshot.png
privacy-mask mask /path/to/screenshot.png --in-place
privacy-mask mask /path/to/screenshot.png --dry-run   # detect only, no masking
privacy-mask mask /path/to/screenshot.png --detection-engine regex  # regex only, skip NER
privacy-mask mask /path/to/screenshot.png --config /path/to/custom-config.json
```

Output is JSON:
```json
{
  "status": "success",
  "detections": [{"label": "PHONE_CN", "text": "***", "bbox": [10, 20, 100, 30]}],
  "summary": "Masked 1 regions: 1 PHONE_CN"
}
```

### Example workflow

1. User provides a screenshot: `~/Desktop/error-screenshot.png`
2. Run detection: `privacy-mask mask ~/Desktop/error-screenshot.png --dry-run`
3. IF detections found, mask the image: `privacy-mask mask ~/Desktop/error-screenshot.png`
4. The masked output is saved as `~/Desktop/error-screenshot_masked.png`
5. Use the masked image for further analysis

## What it detects

- **IDs**: Chinese ID card, passport, HK/TW ID, US SSN, UK NINO, Canadian SIN, Indian Aadhaar/PAN, Korean RRN, Singapore NRIC, Malaysian IC
- **Phone**: Chinese mobile/landline, US phone, international (+prefix)
- **Financial**: Bank card, Amex, IBAN, SWIFT/BIC
- **Developer keys**: AWS, GitHub, Slack, Google, Stripe tokens, JWT, connection strings, API keys, SSH/PEM keys
- **Crypto**: Bitcoin, Ethereum wallet addresses
- **Other**: Email, birthday, IP/IPv6, MAC, UUID, license plate, MRZ, URL auth tokens
- **NER** (optional): Person names, street addresses, organizations, dates of birth, medical conditions

## Constraints

- Do NOT send unmasked images to any external API or cloud service
- Do NOT skip masking when detections are found — always mask before sharing
- Do NOT modify the original image unless `--in-place` is explicitly requested
- Avoid running on very large images (>10MB) without warning the user about processing time

## Anti-patterns

- **Don't assume images are safe** — always run detection even if the image "looks clean"
- **Don't use `--in-place` by default** — preserve the original unless the user asks otherwise
- **Don't ignore dry-run results** — if `--dry-run` finds PII, the image must be masked before use
- **Don't hardcode config paths** — use the bundled default or let the user specify `--config`

## Important

- All processing is **local and offline** — no data leaves the machine
- Configure rules in the bundled `config.json` or pass `--config` for custom rules
