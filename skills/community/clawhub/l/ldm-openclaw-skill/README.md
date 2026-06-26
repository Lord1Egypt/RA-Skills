# LDM Deliverability Check for OpenClaw

An OpenClaw skill that helps outbound agents avoid sending cold email that lands in spam.

OpenClaw agents can draft and send outbound messages, but they usually do not know whether a message or sender domain will land in Inbox, Spam, or Promotions before sending. This skill adds a deliverability preflight powered by LDM.

## What It Checks

- Inbox placement across major mailbox providers
- SPF, DKIM, and DMARC signals
- Spam-score and content-risk signals
- Risky links, redirects, and broken URLs
- HTML structure, image/text ratio, and compliance issues

## Default Policy

```text
Always run ldm_check before bulk outbound. If inbox placement is below 70%, stop and report fixes instead of sending.
```

## Install

Copy this folder into your OpenClaw skills directory:

```bash
mkdir -p ~/.openclaw/skills
cp -R ldm-openclaw-skill ~/.openclaw/skills/ldm-deliverability-check
```

Then configure:

```bash
export LDM_API_BASE="https://check.live-direct-marketing.online"
export LDM_API_KEY="your_ldm_api_key"
export LDM_INBOX_THRESHOLD="70"
```

## Use Case

Ask OpenClaw:

```text
Prepare a cold email campaign for 50 manufacturing companies. Before sending, run the LDM deliverability preflight and pause if placement is risky.
```

Expected behavior:

1. OpenClaw drafts the outbound email.
2. The skill runs an LDM pre-send check.
3. If Gmail or Outlook placement is risky, the agent pauses.
4. The agent reports concrete fixes.
5. After changes, the agent rechecks before sending.

## Links

- LDM Inbox Placement Test: https://check.live-direct-marketing.online
- LDM Developer API: https://developers.live-direct-marketing.online
- Live Direct Marketing: https://live-direct-marketing.online

## Status

Early community version. Feedback from OpenClaw users building outbound, recruiting, investor-update, or deal-flow agents is welcome.
