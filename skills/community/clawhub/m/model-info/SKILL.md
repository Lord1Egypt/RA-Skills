---
name: model-info
description: Get 100% accurate current model details including model name, provider, API endpoint, and session status
version: 1.0.0
author: AutoClaw
---

# Model Info Skill

Provides accurate, real-time information about the currently active AI model.

## Usage

Simply ask: **"model info"** or **"what model"** or **"model status"**

## What it Returns

- **Model Name:** Full model ID (e.g., stepfun-ai/step-3.5-flash)
- **Provider:** Which provider/API it's running on (Nvidia, OpenRouter, etc.)
- **API Key Type:** The API key source
- **Session Status:** Active session info
- **Cost & Tokens:** Current session usage stats
- **Runtime Configuration:** Think mode, elevated status, etc.

## Accuracy

100% accurate - pulls directly from `session_status` command output, the same system that tracks your current runtime.
