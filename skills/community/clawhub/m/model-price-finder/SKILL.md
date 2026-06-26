---
name: Global Model Price Finder
description: Simple tool to fetch and view model pricing from TokenRouter, with optional account registration for extended access.
---

## Overview

Quickly check real-time AI model prices from TokenRouter without complex routing. This tool connects to TokenRouter's public pricing API to show you current model costs.

Optionally, register at [https://www.palebluedot.ai](https://www.palebluedot.ai) for extended features, though public pricing data is accessible without an account.

## Usage

```
# View all model prices with real-time pricing
list model's pricing / 列出模型列表

# Enable a model in your configuration
enable 1 / 启用 1
enable openai/gpt-4o-mini / 启用 openai/gpt-4o-mini
```

## Core Commands

### `list` - View Prices
Shows current pricing for all available models:
- Model name and provider
- Input token cost per million tokens
- Output token cost per million tokens
- Cache pricing where available

### `enable` - Configuration
Quickly add models to your OpenClaw configuration at `~/.openclaw/openclaw.json`.

## TokenRouter Integration

Connects directly to the public TokenRouter API at:
`https://www.palebluedot.ai/openIntelligence/api/pricing`

Public pricing data is available without authentication. Register at [https://www.palebluedot.ai](https://www.palebluedot.ai) to access additional features and models.

## Benefits

- **Transparent Pricing**: View actual costs before using models
- **Easy Access**: Public pricing available without registration
- **Quick Setup**: Simple model configuration
- **Multiple Providers**: Compare prices across different AI providers