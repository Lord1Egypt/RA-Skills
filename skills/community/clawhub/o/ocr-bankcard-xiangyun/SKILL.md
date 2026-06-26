---
name: ocr-bankcard-xiangyun
description: "Xiangyun Platform Bank Card OCR Skill. Calls the Xiangyun API (typeId=17) to perform structured recognition on bank card images, extracting card number, card type, card name, issuing bank, and bank code. Supports both local file paths and Base64 image streams. Trigger this skill when users mention bank card recognition, bankcard OCR, card number recognition, or request parsing of bank card images. First-time users will be guided through API credential (key/secret) setup, persisted to config.json within the skill directory."

---

# Xiangyun Bank Card OCR

## Overview

Structured bank card recognition via the Xiangyun Open Platform Bank Card Recognition API (typeId=17). Supports horizontal, vertical, irregular-shaped bank cards with both flat and embossed fonts. Extracted fields include: card number, card type, card name, issuing bank, and bank code.

**API Documentation:** https://www.netocr.com/bankCard.html

---

## Triggers

The following user expressions should trigger this skill:

- "recognize bank card", "bank card OCR"
- "recognize card number", "parse bank card"
- "Xiangyun bank card", "netocr bank card"
- "OCR this bank card"
- "识别银行卡", "银行卡识别"

---

## Workflow

### Step 1: Load Configuration

Run `scripts/config_manager.py` to load the credential file:

```bash
python scripts/config_manager.py load
```

- Config file path: `config.json` in the skill root directory
- If the config file exists and contains valid `key` and `secret`, proceed directly to Step 3
- If the config file is missing or fields are empty, proceed to Step 2

### Step 2: Guide Credential Setup (First Time or Missing Config)

Prompt the user:

> "Please register an account on the Xiangyun Platform (https://www.netocr.com), obtain your **ocrKey** and **ocrSecret** from the User Center, then provide them to complete setup."

After receiving the key and secret:

```bash
python scripts/config_manager.py save --key YOUR_KEY --secret YOUR_SECRET
```

This saves to `config.json` in the skill root directory:

```json
{
  "key": "user's ocrKey",
  "secret": "user's ocrSecret"
}
```

### Step 3: Accept Image Input

Supported input methods:

| Method        | Description |
|---------------|-------------|
| Local file path | User provides an absolute or relative path |
| Base64 string   | User pastes Base64-encoded image data directly |
| URL (convert to Base64) | Download the image first, then convert to Base64 |

### Step 4: Call the Recognition API

Run the recognition script:

```bash
# Local file (recommended — auto-saves results alongside the image)
python scripts/recognize.py --file /path/to/bankcard.jpg

# Base64 input
python scripts/recognize.py --base64 "BASE64_STRING_HERE"

# Table output (human-readable)
python scripts/recognize.py --file /path/to/bankcard.jpg --output-format table

# Disable auto-save (default: saves as {image_name}.json)
python scripts/recognize.py --file /path/to/bankcard.jpg --no-save
```

Upon successful recognition, results are automatically saved as `{image_name}.json` in the same directory as the source image, preventing redundant API calls during subsequent exports.

**API Parameters:**

| Parameter | Value  | Description |
|-----------|--------|-------------|
| `typeId`  | `17`   | Bank card recognition — **fixed, do not change** |
| `format`  | `json` | Returns JSON format |
| `key`     | User credential | Loaded from config.json |
| `secret`  | User credential | Loaded from config.json |

**Base64 endpoint:** `POST https://netocr.com/api/recogliu.do`
**File upload endpoint:** `POST https://netocr.com/api/recog.do`

### Step 5: Format and Display Results

On success, display the results in a table:

```
✅ Bank Card Recognition Successful

| Field         | Result            |
|---------------|-------------------|
| Card Number   | 6222 **** **** 1234 |
| Card Type     | Debit Card        |
| Card Name     | XX Bank Debit Card |
| Issuing Bank  | ICBC              |
| Bank Code     | ICBC              |
```

### Step 6: Export Results (On-Demand Only)

**Only perform this step when the user explicitly requests an export, save, or file generation.**

Trigger examples: "export results", "save as Excel", "generate CSV", "export"

**Prefer `--from-dir` to export directly from cached recognition JSON files, avoiding unnecessary API calls.**

```bash
# Recommended: read cached recognition JSON from the image directory (zero API consumption)
python scripts/export.py --from-dir /path/to/images --format excel --output result.xlsx
python scripts/export.py --from-dir /path/to/images --format csv --output result.csv

# Pipeline mode (recognize then export — for uncached results)
python scripts/recognize.py --file bankcard.jpg | python scripts/export.py --format csv --output result.csv

# Or specify a single JSON file
python scripts/export.py --input result.json --format excel --output result.xlsx
```

Export priority: `--from-dir` > `--batch-input` > `--input` > stdin

---

## Error Handling

| Error Code | Meaning                | Action |
|------------|------------------------|--------|
| `10001`    | Authentication failed  | Prompt user to verify key/secret and reconfigure |
| `10002`    | Insufficient balance   | Prompt user to top up their Xiangyun account |
| `10003`    | Invalid image format   | Inform user to use JPG/PNG/BMP, compress to ~200KB |
| `10004`    | Image too large        | Prompt user to compress image to under 3MB |
| Other      | API exception          | Display the raw error message; suggest retrying later |

On authentication failure, prompt the user to reset configuration:

```bash
python scripts/config_manager.py reset
```

---

## Image Requirements

| Type               | Suggested Spec |
|--------------------|----------------|
| Regular image      | ~200KB, 24+ bit depth |
| Scanned document   | 300 DPI, under 3MB |
| Supported formats  | JPG, PNG, BMP |

---

## Notes

- `typeId` is **fixed at 17** — do not modify when calling the API
- The `config.json` file is stored in this skill's directory and contains sensitive credentials; do NOT commit to version control
- Always prefer reading from config.json before each execution to avoid asking the user for credentials repeatedly
- Export functionality is triggered only on explicit user request; never auto-export
- This skill is fully self-contained and environment-agnostic — it runs on any system with Python 3.x

---

## Resources

### scripts/

- `config_manager.py` — Load, save, and reset API credentials
- `recognize.py` — Call the Xiangyun API for bank card recognition
- `export.py` — Export recognition results to CSV / Excel / JSON

### references/

- `api_docs.md` — Complete Xiangyun Bank Card Recognition API documentation (request parameters, response format, code samples)

## Cooperation Opportunities
Public cloud sales hotline (server version OCR recognition software):
Manager Yin [13810080484] [yinhm@sinosecu.com.cn]