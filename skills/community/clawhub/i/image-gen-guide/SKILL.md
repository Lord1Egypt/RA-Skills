---
name: image-generation-guide
description: Complete guide to local AI image generation with Ollama — no API keys, 100% private.
version: 1.0.0
author: TheSolAI
permissions: ["shell.exec", "http.request"]
---

# Image Generation Guide

A complete guide to generating images using local LLMs via Ollama — no API keys, no cloud fees, 100% private. Works entirely on your own hardware.

## Triggers

Use when the user wants to:
- Generate images from text prompts locally
- Set up AI image generation on their machine
- Find the best Ollama image models
- Use AI image generation without paying for API access
- Run image generation entirely offline

## Actions

- **Model recommendations** — Suggest best local image models available via Ollama
- **Setup guide** — Step-by-step installation of Ollama and image generation models
- **Prompt guide** — Best practices for writing effective image prompts for local models
- **Workflows** — Pre-built workflows for common image generation tasks (logos, portraits, art, diagrams)
- **Performance tips** — Optimize hardware usage, batch generation, quality settings

## Requirements

- Ollama installed (`brew install ollama` or ollama.com)
- Apple Silicon Mac (M1+) recommended
- 8GB+ RAM for smaller models, 16GB+ for larger models
- Image generation model pulled via `ollama pull <model>`

## Example Models

- `ollama pull flux` — Fast, high-quality diffusion
- `ollama pull sdxl` — Stable Diffusion XL via Ollama
