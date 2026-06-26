---
name: openclaw-pc-security
description: Local security self-check for your Windows PC and OpenClaw server setup (password protection, port, and exposure), producing a local report.
compatibility: "requests>=2.28"
---

# OpenClaw PC Security

## Description

Security self-check and risk alerting for:
- Windows baseline (version/build, last security update date, support status, patch lag)
- Local OpenClaw CLI version vs latest (optional online check)
- OpenClaw server configuration safety (password protection, default port use, public exposure)
- Optional OpenClaw target checks (authorized use only)

## When to use

Use this skill when you need to:
- Check whether Windows is out of support or significantly behind updates
- Confirm whether OpenClaw is up to date on your machine
- If you deployed OpenClaw on a VPS/personal server, verify the setup is safe (password protection on, avoid default port, restrict exposure)
- Generate a local HTML/JSON report for your own reference (do not upload publicly)

## Input
- Local machine information (Windows version/build, last update date)
- Optional OpenClaw config file path for server-side checks (e.g., config.json)
- Optional target host/IP and ports for OpenClaw probing (authorized environments only)

## Output
- Severity-based findings (Info/Medium/High/Critical)
- HTML/JSON report under `output/`
  - `output/audit_report.html` / `output/audit_report.json`
  - `output/scan_report.html` / `output/scan_report.json`
- Finding types include:
  - `defender_status`, `browser_outdated`, `browser_info`, `windows_support_status`
  - `server_config_not_found`, `server_auth_disabled`, `server_auth_enabled`
  - `server_default_port`, `server_custom_port`, `server_exposed_public`, `server_local_only`
  - `openclaw_outdated`, `openclaw_version_mismatch`, `windows_patch_lag`, `weak_credentials`

## Steps

### 1) Local audit
```bash
python scripts/run_audit.py --npm-view-latest-openclaw --out-dir output
```

Optional: if you know your OpenClaw config file path:
```bash
python scripts/run_audit.py --server-config-path "<path-to-config.json>" --out-dir output
```

### 2) Scan a target (authorized environments only)
```bash
python scripts/run_scan.py <target-ip> --ports 18789,18790,18792 --out-dir output
```

Optional: enable active checks explicitly (disabled by default)
```bash
python scripts/run_scan.py <target-ip> --ports 18789,18790,18792 --enable-cred-check --enable-leak-check --out-dir output
```

## Notes
- The server configuration checks are performed locally and do not send data to external services.
- The HTML report supports CN/EN toggle and Simple/Detailed mode.
- Active network checks must ONLY be used on systems you own or have explicit authorization to test.
- **DO NOT** upload tokens, credentials, or reports (output/) to public repositories.
- Reports are written under `output/` when using the provided scripts.
- If OpenClaw is outdated: after upgrading, some or all functions may be unavailable; assess carefully.
- After the HTML report is generated, print the report path in the chat for the user's reference. Do NOT upload or send the report file unless the user explicitly requests it and provides a secure destination. Reports may contain sensitive information, so always handle them with caution.
