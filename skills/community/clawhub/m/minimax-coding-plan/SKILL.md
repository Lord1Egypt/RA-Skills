---
name: minimax-coding-plan
description: MiniMax Coding Plan native web search and image understanding for OpenClaw. Use when the user specifically wants MiniMax-native search or image analysis, or when an active MiniMax plan should handle vision instead of the generic media stack.
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
      },
  }
---

# MiniMax Coding Plan

Use the local wrapper:

```bash
bash {baseDir}/scripts/minimax-plan.sh <tool> [args...]
```

Available tools:

- `web_search --query "..."`
- `understand_image --prompt "..." --image-source /path/to/file-or-url`

Recommended routing:

- Use this skill when the user explicitly wants MiniMax-native search or MiniMax-native image understanding.
- For ordinary web research, `tavily-search` is still the general-purpose default.
- If the main `minimax-portal` text model path is not exposed as a reliable image route in the current OpenClaw setup, use `understand_image`.

Examples:

```bash
bash {baseDir}/scripts/minimax-plan.sh web_search --query "MiniMax M2.5 release note"
bash {baseDir}/scripts/minimax-plan.sh understand_image --prompt "Describe the UI in this screenshot" --image-source /tmp/screen.png
bash {baseDir}/scripts/minimax-plan.sh understand_image --prompt "Extract the visible text" --image-source https://example.com/image.png
```

Notes:

- This wrapper first uses `MINIMAX_API_KEY` when present. Otherwise it looks for an existing `minimax-portal` OAuth profile in `OPENCLAW_AUTH_PROFILES_JSON`, `OPENCLAW_AGENT_DIR`, `OPENCLAW_HOME`, or `~/.openclaw`.
- Output is JSON. For image analysis, read `content` first. If `base_resp.status_code != 0`, explain the MiniMax API error plainly.
- Supported image formats: JPEG, PNG, WebP.
