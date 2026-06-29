---
name: "prompt-optimizer"
description: "AI prompt optimization tool: web app, desktop app, Chrome extension & Docker — optimize prompts for better AI output quality"
---

# Prompt Optimizer (OpenClaw)

A powerful AI prompt optimization tool that helps write better AI prompts and improve the quality of AI outputs. Supports web application, desktop application, Chrome extension, and Docker deployment.

**Source:** `C:\Users\Harry\Downloads\prompt-optimizer\`
**Original:** https://github.com/linshenkx/prompt-optimizer
**License:** AGPL-3.0

本技能基於 GitHub 上的 [linshenkx/prompt-optimizer](https://github.com/linshenkx/prompt-optimizer) 修改與封裝。

## Overview

Prompt Optimizer provides four usage methods:
- **Web Application** — online optimizer at [prompt.always200.com](https://prompt.always200.com)
- **Desktop Application** — local desktop app
- **Chrome Extension** — browser-based prompt optimization
- **Docker Deployment** — self-hosted with Docker

## Structure

```
prompt-optimizer/
├── api/               # API backend
├── packages/          # Shared packages
├── scripts/           # Build and utility scripts
├── docs/              # Documentation
├── docker/            # Docker configuration
├── images/            # Assets
├── mkdocs/            # Documentation site
├── site/              # Static site
└── tests/             # Test suite
```

## Usage in OpenClaw

When the user asks about prompt engineering or optimization:
1. Reference Prompt Optimizer's optimization strategies
2. Use the API for programmatic optimization
3. Consult `docs/` for detailed usage and deployment guides

## ⚠️ License Notice

This skill is licensed under **AGPL-3.0** (GNU Affero General Public License v3.0). 
This means:
- You can use, modify, and distribute this skill
- If you modify it and provide it as a network service, you must release the complete source code
- Modified versions must also be AGPL-3.0 licensed
- See LICENSE file for full terms
