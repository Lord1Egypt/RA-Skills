---
name: privacy-scan
description: Scan any public web page for GDPR/CCPA/ePrivacy privacy & cookie-consent signals — honest about what static-HTML testing can and cannot catch
metadata:
  openclaw:
    requires:
      bins:
        - curl
homepage: https://privacy-scan.foomworks.workers.dev
license: MIT
---

# Privacy & cookie-consent scan (privacy-scan)

Use this skill when a task needs to **check a web page for privacy / cookie-consent issues**
(GDPR · CCPA/CPRA · ePrivacy) — auditing a site, reviewing your own pages, or flagging risk before a
launch. Give it one publicly reachable URL; get back the observable privacy signals a static-HTML
scan can find — which known third-party trackers are present, whether consent tooling and a
privacy-policy / "Do Not Sell" link exist, cookie attributes, and HTTPS — each with the risk and a
concrete fix, plus an honest summary.

Base URL: `https://privacy-scan.foomworks.workers.dev`

**Honest by design (the bright line).** Static HTML can see that a tracker script is *present*, but
NOT whether it fires *before* the user consents — the behaviour regulators fine for; that needs a
real browser. So this never returns a "compliant" verdict or a score; it flags risk signals and
states on every result what it cannot determine. A clean scan is **not** a determination of
GDPR/CCPA/ePrivacy compliance, and this service never claims otherwise. Charter-clean: honors
`robots.txt`, identifies honestly, read-only GET, never bypasses anti-bot/CAPTCHA/paywalls.

## Use as an MCP server (recommended for agents)
privacy-scan is a remote **MCP server** (Streamable HTTP, JSON-RPC 2.0) — connect your agent and the
tools load natively, no curl required:

- Endpoint: `https://privacy-scan.foomworks.workers.dev/mcp`
- Tools (all free, return data directly):
  - `scan_url_privacy` — scan a URL → findings (regulation, impact, count, how-to-fix) + what was detected + summary + coverage note
  - `scan_url_privacy_preview` — what was detected + summary + top issues only (a quick look before the full report)

Discovery manifests: `GET /.well-known/mcp.json` (MCP descriptor), `GET /openapi.json` (OpenAPI 3.1).

## When to use
- "Check <URL> for GDPR / CCPA / cookie-consent issues"
- "Does <URL> load trackers without a consent banner? Is there a Do-Not-Sell link?"
- "Audit this page's privacy posture — trackers, consent tooling, cookie attributes, HTTPS"

## What it checks (static-HTML signals)
Third-party trackers present with no consent tooling (GDPR/ePrivacy), missing privacy-policy link
(GDPR/CCPA), missing CCPA "Do Not Sell or Share" link when trackers are present, insecure cookie
attributes (Set-Cookie without Secure/SameSite), not-HTTPS / mixed content. It recognises common
trackers (Google Analytics/Tag Manager, Meta Pixel, TikTok, Hotjar, Clarity, LinkedIn, …) and
consent platforms (OneTrust, Cookiebot, Osano, Usercentrics, Didomi, iubenda, …). It does **not**
load the page in a browser, so it cannot confirm pre-consent tracker firing (a deeper, browser-based
scan is on the roadmap).

## Endpoints (all currently free)
- `GET /scan?url=<URL>` — full findings + what was detected + summary + coverage note + disclaimer
- `GET /scan/preview?url=<URL>` — what was detected + summary + top issues only
- `POST /mcp` — MCP server (JSON-RPC 2.0): `scan_url_privacy`, `scan_url_privacy_preview`
- `GET /health` · `GET /policy` · `GET /stats`

## Limits & behavior
- **Static HTML only** — it analyzes the page source; it does not run JavaScript or a browser.
- A disallowed `robots.txt` path is **refused without fetching**; an unconfirmable `robots.txt`
  (5xx/error) is treated conservatively as disallowed.
- Private/loopback/link-local/internal hosts are blocked (SSRF protection); every redirect hop is
  re-validated. Body cap ~2 MB, fetch timeout ~12 s. The service holds no keys and never pays.

## Example
```bash
BASE=https://privacy-scan.foomworks.workers.dev
# REST
curl -s "$BASE/scan?url=https://example.com/"
# MCP (Streamable HTTP, JSON-RPC 2.0)
curl -s -X POST "$BASE/mcp" -H 'content-type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"scan_url_privacy","arguments":{"url":"https://example.com/"}}}'
```
