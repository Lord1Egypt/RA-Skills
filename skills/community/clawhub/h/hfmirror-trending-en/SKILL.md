---
name: hfmirror-trending-en
version: "1.0.0"
description: Fetches real-time Hugging Face trending data via the public HF-Mirror API and generates structured Markdown reports in English. Suitable for conversational AI agents.
author: shunshiwei
tags:
  - huggingface
  - hf-mirror
  - trending
  - ai
  - english
license: MIT
python: ">=3.6"
dependencies: []
---

# hfmirror_trending_en (Cross-platform Generic Version)

This Skill enables AI agents to autonomously fetch and parse real-time trending data from HF-Mirror (`hf-mirror.com`).

> **Data Source Notice**: This Skill calls `https://hf-mirror.com/api/trending` — a **public, login-free REST API** provided by HF-Mirror. It does not require any tokens or authorization, nor does it involve any authenticated web scraping or bypassing of access controls.

## Use Cases

When a user inquires about recent trending models, datasets, or projects on Hugging Face or its mirror. Examples:
- "What are the trending models lately?"
- "What's hot on Hugging Face right now?"
- "Push today's Hugging Face mirror trending list."
- "Help me parse the trending data from HF-Mirror."

## Agent Workflow

When processing the above commands, AI agents should follow this standard end-to-end logic:

1. **Auto-Fetch and Parse**: The agent should call the processing script located in the Skill's root directory, utilizing its built-in networking capabilities.
   ```bash
   python scripts/summarize.py --fetch [out_path.md]
   ```
   *Note: The script is Python 3 compatible and can be run directly in Windows (PowerShell/CMD), Linux (Shell), or macOS environments.*

2. **Generate Elegant Reports**: The script automatically fetches JSON from `https://hf-mirror.com/api/trending` and generates structured Markdown output in English.

3. **Smart Delivery**: The agent reads the generated file content and presents it as a well-formatted message to the user.

## Core Design (Cross-Platform & Environment Decoupled)

- **Path Agnostic**: Agents can locate `scripts/summarize.py` via relative paths or Skill environment configurations based on their current context.
- **Zero Dependencies**: The script relies solely on Python 3 standard libraries (`json`, `urllib`, `os`, `sys`). It requires no third-party packages, allowing it to run smoothly even in minimal container or CLI environments.
- **Dynamic Fetch**: The built-in `--fetch` argument eliminates the need to manually prepare intermediate files, enabling a seamless one-click transition from API to report.
- **Compliant Access**: Uses a named User-Agent (`hfmirror-trending-en-skill/1.0`) to identify the request source, adhering to public API best practices.

## Core Output Fields Explanation

- **Model ID**: The unique identifier for the model.
- **Downloads & Likes**: Metrics reflecting community popularity.
- **Parameter Size**: Automatically converted (e.g., 7B, 27B) to help users evaluate deployment costs.
- **Pipeline Tag**: Distinction between different AI domains such as ASR, TTS, OCR, etc.
