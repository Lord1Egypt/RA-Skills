---
name: openclaw-weixin-setup
description: Install and connect the WeChat (微信) channel plugin for OpenClaw. Use when the user asks to set up WeChat, connect WeChat, install the WeChat plugin, scan WeChat QR code, or link their WeChat account to OpenClaw. Triggers on phrases like "connect WeChat", "install WeChat plugin", "微信插件", "连接微信", "微信扫码".
---

# OpenClaw WeChat (微信) Plugin Setup

Install and connect WeChat as a messaging channel for OpenClaw.

## Prerequisites

- OpenClaw installed and running (`openclaw` CLI available)
- A WeChat account on a mobile device for QR code scanning

## Setup Workflow

### Step 1: Install the plugin

```bash
npx -y @tencent-weixin/openclaw-weixin-cli@latest install
```

This command will:
1. Detect the local OpenClaw installation
2. Download and install the `@tencent-weixin/openclaw-weixin` plugin
3. Enable the plugin in OpenClaw config
4. Start the WeChat QR code login flow
5. Display a terminal QR code for scanning

### Step 2: Scan the QR code

The CLI prints an ASCII QR code in the terminal. The user must scan it with their WeChat mobile app to authorize the connection.

**Important:** The QR code renders correctly only in a **monospace terminal**. It will appear garbled in chat interfaces (webchat, Feishu, etc.) due to proportional fonts. If the user cannot see the QR code clearly:
- Instruct them to run the command directly in their terminal (Terminal.app, iTerm2, etc.)
- Or use `openclaw channels login --channel openclaw-weixin` after plugin is installed

### Step 3: Verify connection

After scanning, verify the connection:

```bash
openclaw status 2>/dev/null | grep -i "openclaw-weixin"
```

Expected output should show `openclaw-weixin │ ON │ OK`.

### Step 4: Restart gateway (if needed)

If the plugin was installed but the gateway wasn't restarted:

```bash
openclaw gateway restart
```

## Adding More WeChat Accounts

```bash
openclaw channels login --channel openclaw-weixin
```

Each scan creates a new account entry. Multiple WeChat accounts can be online simultaneously.

## Context Isolation (Optional)

To isolate conversation context per WeChat account:

```bash
openclaw config set agents.mode per-channel-per-peer
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| QR code garbled in chat | Run the command in a real terminal |
| QR code expired | Re-run `openclaw channels login --channel openclaw-weixin` |
| Plugin not loading | Check `openclaw status`, ensure `plugins.entries.openclaw-weixin.enabled` is `true` |
| "No install record" warning | Non-critical; plugin still functions if files exist locally |
| Connection dropped | Re-run login command to re-authenticate |
