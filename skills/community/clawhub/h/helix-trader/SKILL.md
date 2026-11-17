---
name: helix-trader
description: Guide users through installing and safely operating the self-hosted Helix Trader crypto bot. Use for local setup, diagnostics, testnet-first configuration, strategy selection, preview, status checks, or stopping the bot. Never request credentials in chat, skip configuration preview, or promise returns.
metadata:
  openclaw:
    requires:
      bins:
        - git
        - python3
    emoji: "🧬"
    homepage: https://github.com/trade-upnow/helix-trader
---

# Helix Trader

Guide users through downloading and operating Helix Trader on their own
computer. The skill does not custody keys, operate a hosted trading account, or
promise returns.

Read the sibling files when relevant:

- `INSTALL.md` for installation and environment checks;
- `TOOLS.md` for runtime commands and MCP tools;
- `EXPERIENCE.md` and `PARAMETERS.md` for strategy explanations;
- `PLAYBOOK.md` for user-facing workflows;
- `SECURITY.md` for credential and execution boundaries.

## Required order

1. Confirm the local runtime is installed; otherwise follow `INSTALL.md`.
2. Run `doctor`, then use read-only status tools.
3. Ask the user to choose OKX or Binance.
4. Ask the user to choose a strategy; recommend the trend strategy without
   silently selecting it.
5. Use testnet by default.
6. Run `preview_bot_config` and display the configuration summary.
7. Start only after the user explicitly confirms the preview.
8. When stopping, default to preserving positions. Require separate explicit
   confirmation before closing positions.

Never request or echo API credentials in chat. Never upload `.env`, logs,
tokens, keys, or user databases. If the runtime tools are unavailable, provide
installation guidance and clearly state that no action was executed.
