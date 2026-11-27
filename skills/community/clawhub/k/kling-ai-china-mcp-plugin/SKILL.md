---
name: kling-ai-china-mcp-plugin
description: Connect an MCP-compatible AI client to the official Kling AI China MCP for image and video generation, Elements, motion tools, account credits, and task status. Use when a user wants 可灵/Kling AI through the China service.
license: MIT
metadata:
  openclaw:
    emoji: 🎬
---

# Kling AI China MCP Plugin

Connect to the official Kling AI China remote MCP endpoint:

`https://klingai.com/mcp/plugin`

This is a hosted Streamable HTTP MCP service. It is not a local server and does not require an API key. Sign in through the MCP client's native OAuth flow with the user's own China Kling account. Never ask for passwords, access tokens, cookies, or credential files in chat.

## OpenClaw setup

Save the China endpoint in OpenClaw and authorize it in the account holder's browser:

```sh
openclaw mcp set kling-ai '{"url":"https://klingai.com/mcp/plugin","transport":"streamable-http","auth":"oauth"}'
openclaw mcp login kling-ai
openclaw mcp probe kling-ai
```

For other MCP clients, add the same URL as a remote Streamable HTTP server and complete native OAuth sign-in. Keep China and Global endpoints/accounts separate; the Global service is `https://kling.ai/mcp/plugin`.

## Use safely

- After connecting, inspect the live tool list and use `who_am_i` to discover available models, inputs, and limits. Do not guess model names or capabilities.
- Image, video, and motion generation consume credits from the connected China Kling account. Confirm the final generation settings before submitting when the request is ambiguous; do not generate merely to test connectivity.
- For an existing generation, use its returned task ID to query status. Never submit a duplicate because a result is slow or unclear.
- A successful MCP probe verifies connectivity and tool discovery; it does not verify that a generation succeeds or that the account has credits.
