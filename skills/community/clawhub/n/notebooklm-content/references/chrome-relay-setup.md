# Chrome Relay Setup Guide

Complete setup instructions for OpenClaw Browser Relay.

## Installation

1. Install OpenClaw Browser Relay extension in Chrome
2. Open extension settings
3. Configure:
   - Port: 18792
   - Gateway token: from ~/.openclaw/openclaw.json -> gateway.auth.token

## Get Token

```bash
cat ~/.openclaw/openclaw.json | grep -A5 auth
```

**IMPORTANT:** Never paste the token in chat!

## Usage

1. Open target website in Chrome (e.g., NotebookLM)
2. Click Browser Relay extension icon
3. Enable relay for that tab
4. Tab is now controllable via OpenClaw

## Verification

```bash
openclaw browser status --browser-profile chrome-relay --json
```

Should show connected with tabs listed.

## Troubleshooting

- **No tabs found:** Enable relay on a tab first
- **Auth failed:** Check token is correct
- **Gateway error:** Run `openclaw gateway restart`
