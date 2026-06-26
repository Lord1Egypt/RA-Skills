---
name: kujiale-3D-model-upload
description: >
  Validates and runs the complete 5-step Kujiale OpenAPI 3D model upload flow:
  STS credentials → OSS upload → trigger model parse → poll parse status → submit model.
  Use this skill whenever you need to upload a 3D model (ZIP file) to the Kujiale/酷家乐
  OpenAPI platform, test the upload pipeline end-to-end, troubleshoot upload failures,
  or integrate model upload into an automation workflow. Triggers on phrases like
  "upload to kujiale", "test kujiale api", "kujiale model upload", "upload 3d model zip",
  "openapi full flow", or "酷家乐3D模型上传".
compatibility:
  python: ">=3.7"
  dependencies:
    - requests
    - oss2
---

## What is this skill

This skill wraps `kujiale_upload.py` — a self-contained Python script that
validates the complete Kujiale OpenAPI 3D model upload pipeline in exactly 5 steps.
The script uses Python `requests` / `oss2` only, and explicitly disables
environment-derived proxy / certificate overrides (`trust_env=False`) because
those settings can cause TLS handshake failures in some Windows environments:

| Step | Method | Endpoint | Description |
|------|--------|----------|-------------|
| 1 | GET | `/v2/commodity/upload/sts` | Obtain OSS STS credentials + `uploadTaskId` |
| 2 | PUT | Alibaba OSS (`oss2`) | Upload ZIP bytes to OSS |
| 3 | POST | `/v2/commodity/upload/create` | Trigger server-side model parsing |
| 4 | GET | `/v2/commodity/upload/status` | Poll parse status until `status == 3` |
| 5 | POST | `/v2/commodity/upload/submit` | Submit parsed model → returns `brandGoodId` |

**Authentication**: `md5(appSecret + appKey + timestamp_ms)`

**API Key**: Apply at [Manycore OpenAPI Console](https://www.manycoreapis.com/openapi/console/keys)

---

## Quick Start

```bash
# 1. Install dependencies
pip install requests oss2

# 2. Copy the example env file and fill in YOUR credentials
cp .env.example .env
# Windows PowerShell:
# Copy-Item .env.example .env

# 3. Set env vars for the current shell session
export KUJIALE_APP_KEY=your_app_key_here
export KUJIALE_APP_SECRET=your_app_secret_here
# Windows PowerShell:
# $env:KUJIALE_APP_KEY="your_app_key_here"
# $env:KUJIALE_APP_SECRET="your_app_secret_here"

# 4. Run a safe local smoke test first
python kujiale_upload.py --dry-run

# 5. Run the real flow
python kujiale_upload.py
```

---

## Prerequisites and Scope

This skill is intended for users who already have:

- A valid Kujiale OpenAPI `appKey` / `appSecret` — **Apply at [Manycore OpenAPI Console](https://www.manycoreapis.com/openapi/console/keys)**
- Permission to call the commodity model upload APIs in their Kujiale tenant
- A `.zip` package that matches Kujiale's 3D model import requirements
- Network access to `openapi.kujiale.com` and the OSS endpoint returned by Step 1

This repository does **not** include:

- Any built-in credentials
- Any guarantee that the generated placeholder ZIP is a production-valid 3D model package
- Any tenant-specific category mapping beyond the sample defaults in `kujiale_upload.py`

The auto-generated ZIP is only for API connectivity and workflow smoke testing.

## Configuration

### Required credentials

You **must** supply your own Kujiale OpenAPI credentials. There are **no built-in defaults**.

| Method | How to set |
|--------|-----------|
| Environment variable **(recommended)** | `export KUJIALE_APP_KEY=xxx` / `export KUJIALE_APP_SECRET=xxx` |
| CLI flag | `--app-key xxx --app-secret xxx` |
| Programmatic dict | `run_skill({"app_key": "xxx", "app_secret": "xxx"})` |

Priority: **explicit CLI/dict value > environment variable**

If credentials are missing, you will see:
```
FAILED: Missing required credentials: app_key (env: KUJIALE_APP_KEY), app_secret (env: KUJIALE_APP_SECRET).
Set environment variables or pass via --app-key / --app-secret.
See .env.example for reference.
```

### All configuration parameters

| Parameter | Env var / dict key | Default | Description |
|-----------|-------------------|---------|-------------|
| `app_key` | `KUJIALE_APP_KEY` | *(required)* | Kujiale OpenAPI appKey |
| `app_secret` | `KUJIALE_APP_SECRET` | *(required)* | Kujiale OpenAPI appSecret |
| `zip_path` | — | *(auto-generated test ZIP)* | Path to the ZIP file to upload |
| `poll_interval` | — | `5.0` | Seconds between status polls |
| `poll_timeout` | — | `300.0` | Max seconds to wait for parse completion |
| `dry_run` | — | `False` | If `True`, skip all network calls and return mock data |

### Transport behavior

- Default path: API calls use `requests`; OSS upload uses `oss2`
- The script creates dedicated sessions with `trust_env=False`
- This prevents inherited proxy / CA bundle environment settings from breaking TLS handshakes
- If you run this skill inside an agent or IDE that sandboxes outbound network access, the real upload path requires unrestricted network access to `openapi.kujiale.com` and the returned OSS endpoint. The script now reports this case explicitly and tells you to rerun with network permissions enabled.

### Built-in Step 5 defaults

`kujiale_upload.py` currently submits with these sample defaults:

- `location = 1`
- `brandCats = ["3FO4K6E984C7"]`

These values are **not universal**. They appear to be business defaults from the original implementation and may be wrong for another tenant or another catalog tree. If your account requires different category metadata, update the script before using the real submit step.

---

## Usage

### CLI

```bash
# Install dependencies
pip install requests oss2

# Run with credentials from environment variables (recommended)
python kujiale_upload.py

# Run with explicit credentials
python kujiale_upload.py \
  --app-key YOUR_APP_KEY \
  --app-secret YOUR_APP_SECRET

# Run with a specific ZIP file
python kujiale_upload.py \
  --app-key YOUR_APP_KEY \
  --app-secret YOUR_APP_SECRET \
  --zip /path/to/your/model.zip

# Dry run — no network calls, no credentials needed
python kujiale_upload.py --dry-run

# Custom polling parameters
python kujiale_upload.py \
  --app-key YOUR_APP_KEY \
  --app-secret YOUR_APP_SECRET \
  --poll-interval 3 \
  --poll-timeout 120
```

### Programmatic (Python)

Import and call `run_skill(params)` directly:

```python
from kujiale_upload import run_skill

# Credentials from environment variables KUJIALE_APP_KEY / KUJIALE_APP_SECRET
summary = run_skill({})
print(summary)
# {
#   "uploadTaskId": "...",
#   "filePath": "...",
#   "previewImg": "...",
#   "brandGoodId": "..."
# }

# Or pass credentials explicitly
summary = run_skill({
  "app_key": "YOUR_APP_KEY",
  "app_secret": "YOUR_APP_SECRET",
})

# With a specific zip and overridden polling
summary = run_skill({
  "app_key": "YOUR_APP_KEY",
  "app_secret": "YOUR_APP_SECRET",
  "zip_path": "/path/to/model.zip",
  "poll_interval": 3.0,
  "poll_timeout": 120.0,
})

# Dry run — no network calls, no credentials needed
mock = run_skill({"dry_run": True})
print(mock)
# {
#   "uploadTaskId": "DRY_RUN_TASK_ID",
#   "filePath": "dry_run/path/test_model_for_api_test.zip",
#   "previewImg": "",
#   "brandGoodId": "DRY_RUN_BRAND_GOOD_ID",
#   "dry_run": True
# }
```

---

## Test / Run

### What to expect on a successful run

```
============================================================
Kujiale OpenAPI Full Flow
appKey=<your_key> zip=test_model_for_api_test.zip
============================================================
[INFO] Created test zip: test_model_for_api_test.zip
[Step 1] GET https://openapi.kujiale.com/v2/commodity/upload/sts file_name=test_model_for_api_test.zip
[Step 1] OK uploadTaskId=1234567890 filePath=kujiale-models/xxx/test_model_for_api_test.zip
[Step 2] OSS PUT endpoint=https://oss-cn-hangzhou.aliyuncs.com bucket=xxx key=... size=212
[Step 2] OK status=200 etag="..."
[Step 3] POST https://openapi.kujiale.com/v2/commodity/upload/create upload_task_id=1234567890
[Step 3] OK m=
[Step 4] Polling status for uploadTaskId=1234567890 (timeout=300.0s)
[Step 4] Attempt 1 status=1
[Step 4] Attempt 2 status=3
[Step 4] OK status=3 (zip parse success, ready to submit) previewImg=https://...
[Step 5] POST https://openapi.kujiale.com/v2/commodity/upload/submit name=test_model_for_api_test uploadTaskId=1234567890
[Step 5] OK brandGoodId=ABCxyz123 successFlag=True

============================================================
ALL STEPS PASSED
{
  "uploadTaskId": "1234567890",
  "filePath": "kujiale-models/xxx/test_model_for_api_test.zip",
  "previewImg": "https://...",
  "brandGoodId": "ABCxyz123"
}
============================================================
```

### Parse status codes (Step 4)

| Status | Meaning |
|--------|---------|
| 0 | Generating |
| 1 | Parsing ZIP |
| 2 | ZIP parse failed → raises RuntimeError |
| 3 | ZIP parse success, ready to submit → **proceed to Step 5** |
| 4 | Submit success |
| 5 | Submit task exception → raises RuntimeError |

### Common failure modes

| Error | Cause | Fix |
|-------|-------|-----|
| `FAILED: Missing required credentials` | No credentials configured | Set `KUJIALE_APP_KEY` / `KUJIALE_APP_SECRET` env vars, or pass via `--app-key` / `--app-secret` |
| `Step 1 error: c=10001` | Invalid appKey/appSecret | Check credentials on Kujiale open platform |
| `FAILED: ZIP file not found: ...` | Invalid `--zip` path | Pass an existing local `.zip` file |
| `FAILED: ZIP file must end with .zip: ...` | Wrong file type | Package the model as `.zip` before upload |
| `Step 4 poll timeout after 300s` | Parse taking too long | Increase `--poll-timeout` |
| `Step 4 FAILED: status=2` | Invalid ZIP format | Ensure ZIP contains valid model files |
| `Step 1 request failed: ...` / `Step 5 request failed: ...` | Network/API connectivity or a local environment override | Check firewall, VPN, DNS, and whether your shell injects custom proxy / CA env vars |
| `outbound network access appears to be blocked by the current runtime or sandbox` | The tool is running in a restricted sandbox/agent session | Re-run the same command with unrestricted network access, or allow the agent/tool to escalate network permissions |
| `Step 2 OSS PUT failed: ...` | OSS connectivity or STS issue | Check returned OSS region/bucket and network reachability |

---

## Dependencies

```
requests>=2.20.0
oss2>=2.14.0
```

Install:

```bash
pip install requests oss2
```

---

## Publishing Checklist

Before publishing externally, verify:

- [ ] No real credentials in any tracked file — run:
  ```bash
  grep -rn "app_key\|app_secret" . --include="*.py" --include="*.json" --include="*.md" | grep -v ".env.example" | grep -v "YOUR_APP"
  ```
  Confirm only placeholder / env-var references remain.
- [ ] `.env` is **not** committed (keep it local only)
- [ ] `.env.example` is committed with placeholder values only
- [ ] Add `.env` to `.gitignore` in the repo that vendors this skill
- [ ] README / SKILL.md directs users to set `KUJIALE_APP_KEY` / `KUJIALE_APP_SECRET`
- [ ] `python kujiale_upload.py --dry-run` succeeds on a clean machine
- [ ] `python kujiale_upload.py` without credentials fails with a single-line `FAILED:` message, not a traceback

---

## Security Notes

- **Credentials are never logged.** The script logs `appKey` (for traceability) but never logs `appSecret` or the computed `sign`.
- `appSecret` flows only through the in-memory `_sign()` function and is never serialised to disk or printed.
- STS tokens returned by Step 1 are temporary (short TTL) and scoped to a single upload — no long-lived secrets are stored.
- If you suspect your `appKey`/`appSecret` have been exposed, rotate them immediately on the [Manycore OpenAPI Console](https://www.manycoreapis.com/openapi/console/keys).

---

## File Tree

```
kujiale-3D-model-upload/
├── SKILL.md           # This file
├── .env.example       # Credential template — copy to .env and fill in your keys
└── kujiale_upload.py  # Main script (CLI + run_skill entrypoint)
```