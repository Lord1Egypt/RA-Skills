---
name: minimax-token-plan-tool
description: A lightweight MiniMax Token Plan Tool skill that directly calls official MCP APIs using pure JavaScript. No external MCP servers. No subprocess invocation. Designed for minimal overhead and fast integration within OpenClaw.
metadata: {"openclaw":{"emoji":"\ud83e\ude99","requires":{"bins":["node"],"env":["MINIMAX_API_KEY", "MINIMAX_API_HOST"]},"primaryEnv":"MINIMAX_API_KEY"}}
---

# MiniMax Token Plan Tool

> Requires a **Token Plan API Key**
> Subscribe at: [MInimax Token Plan (China Mainland)](https://platform.minimaxi.com/subscribe/token-plan) or [MInimax Token Plan (Global)](https://platform.minimax.io/subscribe/token-plan)

A lightweight MiniMax Token Plan Tool skill that directly calls official APIs using pure JavaScript. No external MCP servers. 

Designed for minimal overhead and fast integration within OpenClaw.

---

## Features

This skill provides three native capabilities of MiniMax Token Plan:

### 1. `minimax_web_search`

Web search powered by MiniMax Token Plan API.

### 2. `minimax_understand_image`

Vision-language image understanding via MiniMax VLM.


### 3. `minimax_token_plan_remains`

Query remaining Token Plan usage and quota information.

---

## Architecture

* Pure JavaScript implementation
* Direct HTTPS API calls
* No MCP server runtime required
* No external tool dependency
* Minimal resource usage

---

## Configuration

Default recommendation: put `MINIMAX_API_KEY` and `MINIMAX_API_HOST` in `~/.openclaw/.env`.

```bash
# ~/.openclaw/.env
MINIMAX_API_KEY="sk-your-key"

# China Mainland
MINIMAX_API_HOST="https://api.minimaxi.com"

# or Global
MINIMAX_API_HOST="https://api.minimax.io"
```

OpenClaw can load these values as the default environment for this Skill.
If you update `~/.openclaw/.env`, restart OpenClaw or the gateway process if the new values are not picked up immediately.
Only these two official hosts are supported.

Use a matching Token Plan key for the selected host:

* China Mainland tokens: [platform.minimaxi.com](https://platform.minimaxi.com)
* Global tokens: [platform.minimax.io](https://platform.minimax.io)

### Optional API Host

```bash
# China Mainland
export MINIMAX_API_HOST="https://api.minimaxi.com"

# or Global
export MINIMAX_API_HOST="https://api.minimax.io"
```

Only `https://api.minimaxi.com` and `https://api.minimax.io` are accepted.
If `MINIMAX_API_HOST` is not set, the script defaults to `https://api.minimaxi.com`.

---

# Tool Discovery

Execute `minimax_token_plan_tool.js` with environment variable `MINIMAX_API_KEY` and optional `MINIMAX_API_HOST` to dynamically register these tools:

```
node minimax_token_plan_tool.js tools
```

Output format:

```
{
  "tools": [
    {
      "name": "minimax_web_search",
      "description": "...",
      "inputSchema": { ... }
    },
    {
      "name": "minimax_understand_image",
      "description": "...",
      "inputSchema": { ... }
    },
    {
      "name": "minimax_token_plan_remains",
      "description": "...",
      "inputSchema": { ... }
    }
  ]
}
```

---

# Tool 1 - minimax_web_search

## Purpose

Real-time web search using MiniMax Token Plan search API.

## CLI Invocation

```
node minimax_token_plan_tool.js web_search "<query>"
```

Example:

```
node minimax_token_plan_tool.js web_search "OpenAI GPT-5 release date"
```

## Input Schema

```
{
  "query": "string"
}
```

## Output Format

Success:

```
{
  "success": true,
  "query": "...",
  "results": [
    {
      "title": "...",
      "link": "...",
      "snippet": "...",
      "date": "..."
    }
  ],
  "related_searches": []
}
```

Error:

```
{
  "error": "error message"
}
```

# Tool 2 - minimax_understand_image

## Purpose

Image understanding using MiniMax Token Plan VLM API.
Only mainstream image formats are supported (for example: JPEG/JPG, PNG, WebP, and GIF).

Supports:

* HTTP / HTTPS image URLs
* Local file paths
* `@localfile.jpg` shorthand

Local files are automatically converted to base64 data URLs.
Remote image URLs are fetched by this tool and then converted to data URLs before being sent to the MiniMax API.
Remote image fetching is restricted to public HTTP/HTTPS targets and rejects localhost, private-network addresses, unsupported ports, and excessive redirects.

## Security Notice

This tool requires outbound network access.
If a local image is provided, its content is transmitted to the remote MiniMax API for processing, which introduces a potential risk of local image data leakage.
Do not submit sensitive, private, or regulated images unless you fully accept this risk.

## CLI Invocation

```
node minimax_token_plan_tool.js understand_image <image_source> "<prompt>"
```

Examples:

Remote image:

```
node minimax_token_plan_tool.js understand_image https://example.com/image.jpg "Describe this image"
```

Local image:

```
node minimax_token_plan_tool.js understand_image ./photo.png "What objects are visible?"
```

With @ prefix:

```
node minimax_token_plan_tool.js understand_image @photo.png "Summarize the scene"
```

## Input Schema

```
{
  "image_source": "string",
  "prompt": "string"
}
```

## Output Format

Success:

```
{
  "success": true,
  "prompt": "...",
  "image_source": "...",
  "analysis": "model response"
}
```

Error:

```
{
  "error": "error message"
}
```

# Tool 3 - minimax_token_plan_remains

## Purpose

Query remaining Token Plan usage through the MiniMax open platform remains endpoint.

## CLI Invocation

```
node minimax_token_plan_tool.js remains
```

## Input Schema

```
{}
```

## Output Format

Success:

```
{
  "success": true,
  "remains": {
    "...": "provider response"
  }
}
```

Error:

```
{
  "error": "error message"
}
```
**Note**:
- All times are in UTC+0. Convert them based on the user's local region.
- For all models, `MiniMax-M*` uses a 5-hour period. Other generative models use a 1-day period.
- `remains_time` and `weekly_remains_time` are formatted as `DD:HH:MM:SS`.
- `*_quota = 0` means the current Token Plan subscription does not include that model.

---

## Official Recommendation

This Skill is a lightweight JavaScript implementation built on top of the official MiniMax APIs.
For best compatibility and long-term support, the official MCP is recommended:
[MiniMax-Coding-Plan-MCP](https://github.com/MiniMax-AI/MiniMax-Coding-Plan-MCP/).

For speech synthesis, image generation, and video generation, the official Skill is recommended:
[Minimax-Multimodal-Toolkit](https://clawhub.ai/minimax-ai-dev/minimax-multimodal).
