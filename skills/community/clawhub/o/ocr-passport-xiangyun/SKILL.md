---
name: ocr-passport-xiangyun
description: "Xiangyun Platform Passport OCR Skill. Calls the Xiangyun API to perform structured recognition of passports from images, extracting fields such as passport number, name, sex, date of birth, date of issue, expiry date, issuing authority, nationality, and more. Supports both Base64 image stream and local file input. Trigger: use when the user mentions passport recognition, passport OCR, extracting passport information, or parsing passport images. On first use, guide the user to configure API credentials (key / secret), which are persisted to config.json in the skill directory."
---

# Xiangyun Passport OCR

## Overview

Leverages the Xiangyun Open Platform ID Document Recognition API to parse passport images structurally, supporting both Chinese and international passports. Recognized fields include: passport number, name, name (pinyin), sex, date of birth, place of birth, date of issue, expiry date, issuing authority, nationality, and more.

**Product page:** https://www.netocr.com/products.html

---

## Triggers

The following user expressions should trigger this skill:

- "passport OCR", "passport recognition", "recognize passport"
- "extract passport info", "parse passport", "scan passport"
- "read passport", "passport data extraction"
- "Xiangyun passport", "netocr passport"
- "OCR this passport", "identify passport"

---

## Workflow

### Step 1: Load Configuration

Invoke `scripts/config_manager.py` to read the configuration:

```bash
python scripts/config_manager.py load
```

- Config file location: `config.json` in the skill root directory
- If the config file exists and contains valid `key` and `secret`, skip to Step 3
- If the config file is missing or fields are empty, proceed to Step 2

### Step 2: First-Time Setup (on missing config)

Inform the user:

> "Please sign up on the Xiangyun Platform (https://www.netocr.com), navigate to your account dashboard to obtain your **ocrKey** and **ocrSecret**, then provide them to me to complete the setup."

Once the key and secret are received:

```bash
python scripts/config_manager.py save --key YOUR_KEY --secret YOUR_SECRET
```

This saves the credentials to `config.json` in the skill root:

```json
{
  "key": "user's ocrKey",
  "secret": "user's ocrSecret"
}
```

### Step 3: Accept Image Input

Supported input methods:

| Method           | Description                                     |
|------------------|-------------------------------------------------|
| Local file path  | User provides an absolute or relative path      |
| Base64 string    | User pastes Base64-encoded data directly        |
| URL (→ Base64)   | Download image first, then convert to Base64    |

### Step 4: Call Recognition API

Run the recognition script:

```bash
# Local file (recommended — auto-saves results alongside the image)
python scripts/recognize.py --file /path/to/passport.jpg

# Base64 input
python scripts/recognize.py --base64 "BASE64_STRING_HERE"

# Human-readable table output
python scripts/recognize.py --file /path/to/passport.jpg --output-format table

# Disable auto-save (default: saves as {image_name}.json)
python scripts/recognize.py --file /path/to/passport.jpg --no-save
```

On success, results are automatically saved as `{image_name}.json` next to the source image, avoiding repeated API calls for later exports.

**API parameters:**

| Parameter | Value        | Description                              |
|-----------|-------------|------------------------------------------|
| `typeId`  | `13`         | Fixed value for passport recognition — **do not change** |
| `format`  | `json`       | Return JSON format                       |
| `key`     | User credential | Loaded from config.json               |
| `secret`  | User credential | Loaded from config.json               |

**Base64 endpoint:** `POST https://netocr.com/api/recogliu.do`
**File upload endpoint:** `POST https://netocr.com/api/recog.do`

### Step 5: Format & Display Results

On success, display results as a table:

```
✅ Passport recognition successful

| Field              | Value                    |
|--------------------|--------------------------|
| Passport Number    | E12345678                |
| Name               | ZHANG SAN                |
| Pinyin             | ZHANG SAN                |
| Sex                | Male                     |
| Date of Birth      | 1990-01-01               |
| Place of Birth     | Beijing                  |
| Date of Issue      | 2020-06-01               |
| Expiry Date        | 2030-06-01               |
| Issuing Authority  | NIA                      |
| Nationality        | China                    |
```

### Step 6: Export Results (on-demand only)

**Only perform this step when the user explicitly requests exporting, saving, or generating a file.**

Trigger examples: "export results", "save as Excel", "generate CSV", "export"

**Prefer `--from-dir` to export directly from cached JSON results — zero API consumption.**

```bash
# Recommended: read cached JSON results from image directory (no API calls)
python scripts/export.py --from-dir /path/to/images --format excel --output result.xlsx
python scripts/export.py --from-dir /path/to/images --format csv --output result.csv

# Pipe mode (recognize then export — for uncached results)
python scripts/recognize.py --file passport.jpg | python scripts/export.py --format csv --output result.csv

# Specific JSON file
python scripts/export.py --input result.json --format excel --output result.xlsx
```

Export priority: `--from-dir` > `--batch-input` > `--input` > stdin

---

## Error Handling

| Error Code         | Meaning                                              | Action                                           |
|--------------------|------------------------------------------------------|--------------------------------------------------|
| `-1`               | Recognition failed (poor image quality / no passport detected) | Ask user for a clearer passport image            |
| `-2`               | Parameter error                                      | Check request parameters                         |
| `-3`               | Insufficient service quota                           | Advise user to top up on Xiangyun Platform       |
| `-4`               | Authentication failed                                | Prompt user to verify key/secret and reconfigure |
| `-5`               | Insufficient balance                                 | Advise user to top up their Xiangyun account     |
| `CONFIG_MISSING`   | Credentials not configured                           | Guide user through first-time setup              |

On authentication failure, prompt the user to reset:

```bash
python scripts/config_manager.py reset
```

---

## Image Requirements

| Type          | Recommended Specs                                    |
|---------------|------------------------------------------------------|
| Photo         | ~200 KB, 24-bit color depth or higher               |
| Scanned       | 300 DPI, file size < 3 MB                            |
| Format        | JPG, PNG, BMP                                        |

- Place the passport flat and avoid glare or obstructions
- Ensure text is legible with adequate contrast

---

## Important Notes

- `typeId` is **fixed at 13** — do not modify when calling the API
- `config.json` is stored in the skill directory and contains sensitive credentials; do not commit to version control
- Always read config.json before each run to avoid repeatedly asking for credentials
- Recognition results are auto-cached as `{image_name}.json` alongside the source image; exports read from cache without additional API calls
- File export is only triggered on explicit user request — never auto-export
- This skill is fully self-contained and runs on any platform with Python 3.x; no host-specific dependencies

---

## Resources

### scripts/

- `config_manager.py` — Read, write, and reset configuration files
- `recognize.py` — Call the Xiangyun API to perform passport OCR
- `export.py` — Export recognition results to CSV / Excel / JSON

### references/

- `api_docs.md` — Complete Xiangyun Passport Recognition API reference (request parameters, response format, sample code)

## Cooperation Opportunities

Public cloud sales hotline (server version OCR recognition software):
Manager Yin [13810080484] [yinhm@sinosecu.com.cn]