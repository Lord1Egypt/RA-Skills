---
name: ifind
description: |
  Use a local Python wrapper around the official iFinD QuantAPI HTTP endpoints on quantapi.51ifind.com. Use when the user wants iFinD market, macro, fund, code-conversion, calendar, report, or portfolio data through HTTP without downloading third-party binaries. This skill is especially appropriate when a local `ifind_api.py` wrapper or custom iFinD HTTP integration should be reused, and when refresh_token acquisition and secure local storage must be checked before any API call.
---

# iFinD

Use this skill to query iFinD via the local Python wrapper in `scripts/ifind_api.py`.

## Environment preparation

Before first use, verify Python dependencies.

Required runtime dependency:
- `requests`

A pinned dependency file is provided at `scripts/requirements.txt`.

Check quickly with:

```bash
python3 -c "import requests; print(requests.__version__)"
```

If missing, install it before running any API script:

```bash
python3 -m pip install -r scripts/requirements.txt
```

If the environment is externally managed, prefer a virtual environment, but installing `requests` is allowed for this skill when needed.

## First rule: confirm refresh_token before querying

Before any data call:

1. Check token status with:
   `python3 scripts/ifind_token_store.py status`
2. If missing, prefer letting the agent obtain it directly from the official site:
   - open `https://quantapi.51ifind.com`
   - log in with the user's existing session, or ask the user to complete login if interactive approval is needed
   - go to the account information page
   - locate the `refresh_token`
3. Store it only through:
   `python3 scripts/ifind_token_store.py set --token '<TOKEN>'`
4. Only fall back to asking the user to provide the token if the browser path is unavailable or login cannot be completed.

Never ask the user to paste shell commands that would echo the token back into chat. Never print the token after storing it.

## Preferred token acquisition workflow

Prefer this order:

1. Browser login to `https://quantapi.51ifind.com` and read the token from account information
2. iFinD 超级命令客户端 → 工具 → `refresh_token` 查询
3. Ask the user directly only as a fallback

If browser automation is used, keep the flow minimal and do not browse unrelated pages. Once the token is found, store it immediately and stop exposing it in further output.

## Token storage policy

- Storage path: `~/.openclaw/skills/ifind/credentials.json`
- File permission target: owner read/write only (`600` on POSIX)
- The store script writes the file and tightens permissions automatically.
- The request script reads the refresh_token from that file unless `IFIND_REFRESH_TOKEN` is already present in the environment.
- Prefer the stored token over hardcoding tokens into code or notes.

## Quick workflow

### 1. Verify dependencies and token state

Run:

```bash
python3 -c "import requests; print(requests.__version__)"
python3 scripts/ifind_token_store.py status
```

If `requests` is missing, install it first:

```bash
python3 -m pip install -r scripts/requirements.txt
```

If the token is missing, obtain it through the preferred browser workflow and store it first.

### 2. Choose a calling path

- For direct endpoint calls, use `scripts/ifind_request.py endpoint`
- For common market-data work, use `scripts/ifind_request.py preset`
- For Python integration or patching, read `scripts/ifind_api.py`
- For endpoint details and payload shape, read `references/iFind_API_Reference.md`

### 3. Run the query

Examples:

```bash
python3 scripts/ifind_request.py preset realtime \
  --codes '300033.SZ,600000.SH' \
  --indicators 'open,high,low,latest,changeRatio,volume,amount'

python3 scripts/ifind_request.py preset ohlcv \
  --codes '000300.SH' \
  --startdate '2025-01-01' \
  --enddate '2025-03-01'

python3 scripts/ifind_request.py endpoint get_thscode \
  --payload '{"seccode":"300033","functionpara":{"mode":"seccode","sectype":"","market":"","tradestatus":"0","isexact":"0"}}'
```

## Output discipline

When using returned data in analysis:

- state the endpoint used
- include the symbol universe / code list
- include the requested date range or timestamp
- include the returned `perf`, `dataVol`, or other useful metadata when relevant
- if the API returns an error, surface the error code and message rather than guessing

## References

- `references/iFind_API_Reference.md`: local API wrapper reference and examples from the user
- `references/token-and-storage.md`: refresh_token acquisition and storage procedure
- `scripts/ifind_api.py`: local Python wrapper
- `scripts/ifind_request.py`: CLI for endpoint/preset calls
- `scripts/ifind_token_store.py`: token status/set/remove helper
