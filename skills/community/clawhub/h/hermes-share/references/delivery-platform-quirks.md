# Delivery Platform Quirks

Condensed from real delivery attempts — what works and what doesn't.

---

## Telegram Bot Delivery

### Rule: Recipient MUST message the bot first

Telegram Bot API blocks bots from initiating conversations. If `@username` has never messaged the bot, delivery fails silently.

**Symptoms:**
- `cronjob create --deliver telegram:@username` never fires (0/N runs, next_run_at keeps moving)
- `getUpdates` doesn't show the user
- Direct API call returns 403

**Fix:** Get the recipient to send any message to the bot first, THEN deliver. Or use a temp download link.

### cronjob deliver format

```
cronjob create --deliver telegram:@username
```

Only works if the user's chat_id is already known to the bot from a prior interaction.

---

## Upload Services Priority

Tested 2026-05-11 from Hermes gateway (KSA region):

| # | Service | Status | Notes |
|---|---------|--------|-------|
| 1 | **tmpfiles.org** | ✅ Working | `curl -s -F "file=@..." https://tmpfiles.org/api/v1/upload` → returns JSON with URL. Direct download: `https://tmpfiles.org/dl/{id}/file.zip` |
| 2 | **file.io** | ⚠️ Unreliable | Upload may succeed but returns empty response. Not recommended as primary. |
| 3 | **transfer.sh** | ❌ Blocked | `curl: (7) Failed to connect to transfer.sh port 443` from KSA |
| 4 | **0x0.st** | ❌ Disabled | Returns: "uploads disabled because it's been almost nothing but AI botnet spam" |

**Always try tmpfiles.org first.** It's the most reliable from KSA/MENA region.

### tmpfiles.org response format

```json
{"status": "success", "data": {"url": "http://tmpfiles.org/37573330/file.zip"}}
```

Convert to direct download: `https://tmpfiles.org/dl/37573330/file.zip`
