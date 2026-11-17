# CSAPI Quota Integration — Multi-Account

## Purpose

Google Custom Search API (CSAPI) is a fallback search tier in Sift, used when free web search returns insufficient results.

## Prerequisites (ALL required)

1. **OAuth scope** `https://www.googleapis.com/auth/cse` on the workspace-mcp token for each account.
2. **`GOOGLE_PSE_API_KEY`** — GCP Console API key. **Must be set manually** (agent cannot write it — credential sanitizer).
3. **`GOOGLE_PSE_ENGINE_ID`** — Custom Search Engine ID (`cx` from Programmable Search Engine settings). **Must be set manually**.
4. Optional: `GOOGLE_PSE_API_KEY_INDIGO` — separate key for the the agent account (separate 1,000 queries/month quota).

⚠️ If `search_custom` fails with "GOOGLE_PSE_API_KEY environment variable not set" or "GOOGLE_PSE_ENGINE_ID environment variable not set", the owner must add these to config.yaml. The agent cannot write them through any tool.

## Multi-Account

Two accounts are configured. The `gsearch/search_tools.py` has been patched to auto-select the API key based on `user_google_email`:
- `<user-google-email>` → uses `GOOGLE_PSE_API_KEY`
- `<third-party-or-user-email>` → uses `GOOGLE_PSE_API_KEY_INDIGO` (falls back to `GOOGLE_PSE_API_KEY` if not set)

## Quota

- **Free tier**: 1,000 queries/month **per account**
- **Tracking script**: `scripts/csapi_quota.py`
- **State file**: `~/.hermes/commons/data/ocas-sift/csapi_quota.json`
- Auto-resets on calendar month boundary

## Commands

```bash
# Check if quota available (exit 0 = yes, 1 = exhausted)
python3 ~/.hermes/skills/ocas-sift/scripts/csapi_quota.py check

# After a successful CSAPI search call, record usage
python3 ~/.hermes/skills/ocas-sift/scripts/csapi_quota.py increment

# View full quota state as JSON
python3 ~/.hermes/skills/ocas-sift/scripts/csapi_quota.py status

# Print queries remaining this month
python3 ~/.hermes/skills/ocas-sift/scripts/csapi_quota.py remaining
```

## Integration Pattern in Sift

Before calling `mcp_google_workspace_search_custom`:

1. Run `python3 ~/.hermes/skills/ocas-sift/scripts/csapi_quota.py check`
2. If exit code 0 (quota available): execute the search, then run `increment`
3. If exit code 1 (exhausted): skip CSAPI, log `degraded: csapi_quota`, do not retry until next month

## Open Web Search

CSAPI does full open web search when `site_search` is omitted. This makes it a complete replacement for the disabled Playwright-based `google-search` MCP.

## Why CSAPI Instead of Browser Scraping

The Playwright-based `google-search` MCP has been disabled. Google permanently blocks datacenter/VPS IPs via CAPTCHA when using browser automation. CSAPI uses authenticated API calls instead, which work reliably from any IP.

## See Also

- `google-workspace-auth/references/csapi-setup.md` — How CSAPI works, prerequisites, and troubleshooting
- `search_tiers.md` — Full search tier chain and provider details
- `research-workflow.md` — Cloud environment fallback workflow
