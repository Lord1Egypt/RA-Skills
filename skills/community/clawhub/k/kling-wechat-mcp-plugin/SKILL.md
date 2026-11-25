---
name: kling-wechat-mcp-plugin
description: Connect Kling AI's official MCP to OpenClaw and use it through Tencent's Weixin channel. Use when configuring or troubleshooting the WeChat → OpenClaw → Kling MCP path.
metadata:
  short-description: Use Kling MCP from WeChat through OpenClaw
---

# Kling MCP through WeChat and OpenClaw

This is a bridge, not a native WeChat MCP client:

`WeChat DM → Tencent-maintained OpenClaw Weixin channel → OpenClaw agent → Kling official MCP`

The Global and China Kling MCP endpoints use OAuth. OpenClaw supports remote Streamable HTTP MCP with OAuth.

## Set up the Weixin channel

1. Check that OpenClaw is installed and updated. Use OpenClaw `2026.5.12` or newer with Node.js `22.13.0` or newer for the Tencent plugin's current peer requirement.
2. Install Tencent's channel plugin:

   ```sh
   openclaw plugins install "@tencent-weixin/openclaw-weixin"
   openclaw config set plugins.entries.openclaw-weixin.enabled true
   openclaw gateway restart
   ```

3. On the machine running the Gateway, start Weixin login:

   ```sh
   openclaw channels login --channel openclaw-weixin
   ```

   The account holder scans and confirms the QR code themselves. Never request or copy session credentials. Use the channel's pairing/allowlist controls before accepting messages from other senders.

## Connect Kling MCP

Use the endpoint for the user's Kling account region. Global and China accounts, credits, and tasks are separate; configure one region per OpenClaw instance.

Global:

```sh
openclaw mcp add kling-ai \
  --url https://kling.ai/mcp/plugin \
  --transport streamable-http \
  --auth oauth \
  --header X-Kling-Integration=Plugin-OpenClaw \
  --connect-timeout 30 \
  --timeout 60 \
  --no-probe
```

China:

```sh
openclaw mcp add kling-ai \
  --url https://klingai.com/mcp/plugin \
  --transport streamable-http \
  --auth oauth \
  --header X-Kling-Integration=Plugin-OpenClaw \
  --connect-timeout 30 \
  --timeout 60 \
  --no-probe
```

Then authorize in a browser and inspect the tools:

```sh
openclaw mcp login kling-ai
openclaw mcp status --verbose
openclaw mcp probe kling-ai
```

Do not paste OAuth tokens into config files or chat. If the user already has a `kling-ai` MCP entry, inspect its region before changing it; do not overwrite an existing account setup without explicit direction.

## Verify without spending credits

- Confirm OAuth status and that the MCP probe discovers Kling tools.
- If the conversation agent offers a read-only identity or account-credit query, use it only when the user asks to verify account access.
- Do not call image/video generation, upload, task creation, or other credit-consuming actions as a test. Explain that real generations use the user's Kling credits and wait for an explicit generation request.
- A successful MCP probe verifies OAuth connectivity and tool discovery. It does not by itself verify that WeChat messages reach the agent.
- To verify the full route, the account holder must send a DM to the paired Weixin bot. Start with a non-generating request such as asking for the available Kling tools; report clearly whether the DM round trip was tested.

## Troubleshoot

- OAuth not authorized: run `openclaw mcp login kling-ai` and complete the browser flow as the account holder.
- No Kling tools: run `openclaw mcp probe kling-ai`, confirm the endpoint region, then restart the Gateway and start a new conversation.
- Weixin not connected: check `openclaw channels status --probe`; verify the channel plugin is enabled and that the QR login was completed on the Gateway host.
- Unknown sender cannot message the agent: inspect the OpenClaw pairing/allowlist configuration and have the account owner approve the sender.

## Official references

- Tencent-maintained Weixin channel plugin: https://github.com/Tencent/openclaw-weixin
- OpenClaw WeChat channel guide: https://docs.openclaw.ai/zh-CN/channels/wechat
- OpenClaw MCP connection guide: https://docs.openclaw.ai/tools/mcp
- OpenClaw MCP configuration reference: https://docs.openclaw.ai/gateway/config-extensions
- Kling Global MCP: https://kling.ai/mcp/plugin
- Kling China MCP: https://klingai.com/mcp/plugin
- Kling OpenClaw Global plugin: https://hub.openclaw.ai/klingai-dev/plugins/kling-ai-global-openclaw
