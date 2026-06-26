---
name: kuaishou-genius-actual
description: Use this skill whenever the user asks to analyze, verify, debug, reverse-engineer, or automate Kuaishou Genius「预算/预测/实际」页面 data flow (especially management-yearly/actual). Trigger on requests about Network 抓包, API mapping, endpoint calls, auth/session reuse, payload reconstruction, or script-based API probing for genius.corp.kuaishou.com/budget-portal.
---

# Kuaishou Genius Actual API Skill

## Overview

This skill helps an agent quickly move from **Genius 页面操作** to **可复用的接口调用地图与脚本化验证** for the `management-yearly/actual` workflow.

Use it when the goal is to identify core backend endpoints, validate request dependencies, and build repeatable checks for Genius Actual data retrieval.

## Quick Start

1. Ensure login/session is valid for `genius.corp.kuaishou.com`.
2. Capture network around page reload and key filter actions.
3. Focus on `/budget-portal/api/*` requests; ignore static assets and telemetry unless debugging auth/risk.
4. Run script-based endpoint probe/client:

```bash
cd scripts
bash genius_api_probe.sh \
  --base-url "https://genius.corp.kuaishou.com" \
  --cookie "accessproxy_session=<YOUR_COOKIE>" \
  --year 2026

python3 genius_client.py \
  --cookie "accessproxy_session=<YOUR_COOKIE>" \
  workflow --year 2026
```

5. Output a concise report with:
   - reachable endpoints
   - required params/payload hints
   - dependency order
   - known blockers/limitations

## Supported Capabilities

1. **Core API extraction**
   - Identify actual business endpoints used by `management-yearly/actual`.

2. **API map generation**
   - Build endpoint catalog: method, path, purpose, required params/body.

3. **Workflow reconstruction**
   - Reconstruct request order from page load to ledger detail fetch.

4. **Scripted probing**
   - Use `scripts/genius_api_probe.sh` to quickly verify endpoint reachability and baseline responses.

5. **Troubleshooting focus**
   - Distinguish business API failures from:
     - SSO/session expiration
     - fingerprint/risk controls
     - telemetry noise

## API Map (Core Business)

Base domain:
- `https://genius.corp.kuaishou.com`

Core endpoints observed in Actual flow:

- `GET /budget-portal/api/authority/user`
  - Purpose: fetch user auth context.

- `GET /budget-portal/api/authority/org/tree`
  - Purpose: org tree for selectors/permissions scope.

- `GET /budget-portal/api/horse-race-lamp/query?tabCode=management-yearly%2Factual`
  - Purpose: tab-level notification/meta.

- `GET /budget-portal/api/description/act-latest-update-date`
  - Purpose: latest actual update metadata.

- `GET /budget-portal/api/annual-actual/versions?year=<YEAR>`
  - Purpose: available versions for selected year.

- `POST /budget-portal/api/actual-ledger/detail`
  - Purpose: ledger detail dataset.
  - Notes: requires JSON body shaped by current filters.

- `POST /budget-portal/api/actual-ledger/products`
  - Purpose: product/metric dimension data for current view.
  - Notes: requires JSON body shaped by current filters.

Non-core but commonly seen (usually ignore unless diagnosing):
- `log-sdk.ksapisrv.com/*` telemetry
- `mobile-device-info.corp.kuaishou.com/*` device/risk
- `h5-fingerprint.corp.kuaishou.com/*` fingerprint

## Workflow

### 1) Session check
- Confirm not redirected to SSO login.
- Verify `accessproxy_session` works for `genius.corp.kuaishou.com`.

### 2) Capture
- Reload target page:
  - `https://genius.corp.kuaishou.com/management-yearly/actual`
- Capture all XHR/fetch.

### 3) Filter to business APIs
- Keep only `/budget-portal/api/` requests.
- Group by: authority → metadata → versions → ledger POSTs.

### 4) Rebuild minimal call chain
- Start with GET chain (auth/org/version).
- Then reproduce POST ledger calls with realistic payload.

### 5) Validate by script
- Run `genius_api_probe.sh` with cookie + year.
- Record HTTP code + brief body snippet.

### 6) Report
Always output:
- API list (method/path/purpose)
- call order
- required parameters/body fields (known/unknown)
- current blockers and next action

## Script Usage

Script paths:
- `scripts/genius_api_probe.sh`
- `scripts/genius_client.py`

What they do:
- `genius_api_probe.sh`: probes key GET APIs and sends placeholder POSTs for quick triage
- `genius_client.py`: structured client for core APIs (single endpoint or full workflow), supports custom JSON payload files

Required inputs:
- `--base-url` (default `https://genius.corp.kuaishou.com`)
- `--cookie` (must include valid `accessproxy_session=...`)

Optional:
- `--year` (default `2026`)

## Known Limitations

1. **SSO/session coupling**
   - Without valid session cookie, requests fall back to SSO and API probing is invalid.

2. **Risk/fingerprint controls**
   - Some environments may require device/fingerprint side requests; replay outside browser may fail.

3. **POST body incompleteness**
   - `actual-ledger/detail` and `actual-ledger/products` need accurate business payload fields from live capture.

4. **Environment drift**
   - static bundle versions and backend schema may change; always re-capture when results diverge.

5. **Permission scope**
   - org tree and ledger visibility depend on account permissions; data differences are expected across users.
