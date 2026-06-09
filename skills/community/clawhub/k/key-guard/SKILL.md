---
name: "# key-guard  A local MCP server that keeps API keys off Claude's servers.  ## Why This Exists  When Claude reads a file containing an API key, the raw key content gets sent to Claude's servers. key-guard prevents this by acting as a local middleman — Claude calls a tool, the tool reads the key and makes the API call locally, and only the result is returned to Claude."
description: "Security guardrail: prevents API keys from being sent to Claude. Triggers when user asks to call an external API, use a key, check credentials, read .env fil..."
category: "other"
source: "ClawHub"
tags: []
platforms: []
author: ""
version: ""
license: ""
installCmd: "hermes skills install clawhub/key-guard"
sourceUrl: "https://clawhub.ai/skills/key-guard"
---

# # key-guard  A local MCP server that keeps API keys off Claude's servers.  ## Why This Exists  When Claude reads a file containing an API key, the raw key content gets sent to Claude's servers. key-guard prevents this by acting as a local middleman — Claude calls a tool, the tool reads the key and makes the API call locally, and only the result is returned to Claude.

> Security guardrail: prevents API keys from being sent to Claude. Triggers when user asks to call an external API, use a key, check credentials, read .env fil...

- **Category:** Other
- **Source:** ClawHub
- **Author:** 
- **Version:** 
- **License:** 
- **Platforms:** All
- **Install Command:** `hermes skills install clawhub/key-guard`
- **Source URL:** [https://clawhub.ai/skills/key-guard](https://clawhub.ai/skills/key-guard)

## Overview


## Installation
To install this skill, run the following command in your terminal:
```bash
hermes skills install clawhub/key-guard
```
