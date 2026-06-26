---
name: outlook-hack
version: 3.0.0
description: "Your agent reads Outlook email all day. Drafts replies for you. Won't send a single one. Not even if you ask nicely."
metadata:
  {
    "openclaw":
      {
        "emoji": "📧",
        "os": ["linux", "darwin"],
        "requires": { "capabilities": ["browser"] },
        "notes":
          {
            "security": "This skill captures Outlook Web session tokens via browser tab sharing to make direct REST calls to Microsoft's Outlook REST API v2.0. No API keys or admin approval needed. SENDING IS CODE-DISABLED: the fetch script physically blocks /sendmail, /reply, /replyall, /forward. It reads, searches, and creates drafts only. Drafts land in the user's Drafts folder for manual review and sending. Tokens are stored at ~/.openclaw/credentials/outlook-msal.json with 0600 permissions.",
          },
      },
  }
---

# Outlook Hack

**Your AI agent won't email the CEO at 3am.**

Not because there's a setting. Not because there's a policy. Because the code physically cannot send emails. We removed that capability the way you'd remove a chainsaw from a toddler — completely and without negotiation.

## What It Does

- 📧 Read, search, and bulk-fetch emails across all folders
- 📎 Index all attachments (name, type, size) per message
- 📊 Generate digest summaries with top senders, unread counts, full body text
- ✏️ Create email drafts (lands in Drafts folder — never sends)
- 📅 Access calendar events, 👥 Browse contacts

## Quick Start

### 1. Token Extraction (one-time, ~30 seconds)

**Extract from the Teams tab, NOT Outlook.** Classic Outlook no longer exists in most orgs, and new Outlook uses PoP tokens that can't be extracted. The Teams tab provides an MSAL refresh token (90-day, auto-rotating) that powers both this skill and the `teams-hack` skill.

Open **Microsoft Teams** (`teams.cloud.microsoft`) in Chrome with the OpenClaw browser relay attached. Then run this in-browser evaluation:

```javascript
(() => {
  const keys = Object.keys(localStorage).filter(
    (k) => k.includes("refreshtoken") || k.includes("RefreshToken"),
  );
  const parsed = JSON.parse(localStorage.getItem(keys[0]));
  const accountKeys = Object.keys(localStorage).filter((k) => {
    try {
      return JSON.parse(localStorage.getItem(k)).tenantId;
    } catch {
      return false;
    }
  });
  let tenantId = null;
  for (const k of accountKeys) {
    try {
      tenantId = JSON.parse(localStorage.getItem(k)).tenantId;
      break;
    } catch {}
  }
  return { secret: parsed.secret, tenantId };
})();
```

Save the token via the `teams` CLI (NOT the outlook-mail-fetch script):

```bash
teams token store --refresh-token "<secret>" --tenant-id "<tenantId>"
```

### 2. Verify Access

```bash
node {baseDir}/scripts/outlook-mail-fetch.mjs --test
```

### 3. Bulk Fetch

```bash
# Last 6 months (default)
node {baseDir}/scripts/outlook-mail-fetch.mjs --fetch-all

# Custom range
node {baseDir}/scripts/outlook-mail-fetch.mjs --fetch-all --months 12
```

**Output:** `~/.openclaw/workspace/data/outlook-emails/`

- `raw-emails.jsonl` — full email data (subject, from, to, body text, preview)
- `attachments-index.jsonl` — every attachment per message
- `email-summary.md` — readable digest with stats and per-email summaries

## Critical: Teams is the Token Source

| Source                                  | Token Type                      | Extractable?       | Lifetime                |
| --------------------------------------- | ------------------------------- | ------------------ | ----------------------- |
| Teams (`teams.cloud.microsoft`)         | MSAL refresh token              | ✅ Yes             | 90 days, auto-rotates   |
| New Outlook (`outlook.cloud.microsoft`) | PoP token (Proof-of-Possession) | ❌ No              | Crypto-bound to browser |
| Classic Outlook (`outlook.office.com`)  | Bearer access token             | ⚠️ Deprecated/gone | Most orgs migrated      |

**Always extract from the Teams tab.** New Outlook uses Proof-of-Possession tokens that cannot be extracted or replayed. Classic Outlook is deprecated and no longer available in most orgs.

## How It Works (Technical)

1. Share your **Microsoft Teams** tab with OpenClaw via the Browser Relay
2. The agent reads `localStorage` to extract the MSAL refresh token
3. Token is stored and exchanged for a Graph API access token via `teams token store`
4. Both this skill and `teams-hack` share `~/.openclaw/credentials/outlook-msal.json` (0600)
5. The `outlook-mail-fetch.mjs` script uses the Graph API access token for mail operations
6. Refresh token lasts 90 days and auto-rotates on each use

The skill is NOT scraping the page. It speaks Outlook's own REST API, authenticated through your existing browser session.

## Token Lifetime & Refresh

- Refresh token: 90 days, auto-rotates on each use (shared with `teams-hack`)
- Access token: ~1 hour, automatically refreshed by the scripts
- Any cron job using either skill keeps the refresh token alive
- When expired: re-extract from Teams tab (one browser relay session)

## Architecture Notes

- **Zero external dependencies** — pure Node.js (v18+), no npm packages
- **Send-blocked** — the script has no send/reply/forward functions. They don't exist.
- **Rate-limited** — fetches 50 emails per page with automatic pagination
- **Body text cleaned** — HTML stripped, whitespace normalized, truncated to 3000 chars per email

## The Full Stack

Pair with [**whatsapp-ultimate**](https://clawhub.com/globalcaos/whatsapp-ultimate) for messaging and [**jarvis-voice**](https://clawhub.com/globalcaos/jarvis-voice) for voice.

👉 **[Clone it. Fork it. Break it. Make it yours.](https://github.com/globalcaos/tinkerclaw)**
