---
name: marketing-asset-generator
description: AI-powered marketing asset generation workflow. Combines DuckDuckGo design inspiration search, Gemini Nano Banana Pro image generation, Feishu Drive cloud storage, and Slack team notifications.
tags: ['marketing', 'image-generation', 'gemini', 'feishu', 'slack', 'automation', 'workflow']
version: 1.0.0
author: OpenClaw
license: MIT
repository: https://github.com/openclaw/openclaw
homepage: https://clawhub.com
metadata:
  {
    openclaw:
      {
        requires:
          {
            envs:
              [
                "GEMINI_API_KEY",
                "FEISHU_APP_ID",
                "FEISHU_APP_SECRET",
                "FEISHU_TARGET_FOLDER_TOKEN",
                "SLACK_BOT_TOKEN",
                "SLACK_TARGET_CHANNEL_ID",
                "MARKETING_TEAM_SLACK_MENTIONS",
              ],
            pip:
              [
                "python-dotenv",
                "duckduckgo-search",
                "google-genai",
                "requests",
                "requests-toolbelt",
                "slack-sdk",
              ],
            bins: ["python3"],
          },
        examples:
          [
            {
              name: "Generate summer sale banner",
              prompt: "Generate a summer sale marketing banner and notify the team",
            },
            {
              name: "Product launch campaign",
              prompt: "Create marketing assets for new product launch with inspiration search",
            },
          ],
      },
  }
---

# Marketing Asset Generator Skill

AI-powered end-to-end marketing asset generation workflow for OpenClaw agents.

## Features

- 🔍 **Design Inspiration Search** - DuckDuckGo image and text search for reference materials
- 🎨 **AI Image Generation** - Powered by Google Gemini 3 Pro Image (Nano Banana Pro)
- ☁️ **Cloud Storage** - Automatic upload to Feishu Drive
- 💬 **Team Notifications** - Slack integration with previews and direct links
- ⚡ **Complete Workflow** - Single command to run research → generate → store → notify

## Installation

```bash
clawhub install marketing-asset-generator
```

## Configuration

Set these environment variables in your `.env` file:

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | ✅ |
| `FEISHU_APP_ID` | Feishu Open Platform App ID | ✅ |
| `FEISHU_APP_SECRET` | Feishu Open Platform App Secret | ✅ |
| `FEISHU_TARGET_FOLDER_TOKEN` | Feishu Drive folder token for uploads | ✅ |
| `SLACK_BOT_TOKEN` | Slack Bot OAuth token | ✅ |
| `SLACK_TARGET_CHANNEL_ID` | Slack channel ID for notifications | ✅ |
| `MARKETING_TEAM_SLACK_MENTIONS` | User/team mentions (e.g., `@here` or `<@U12345>`) | ❌ |

## Usage

### Python API

```python
from marketing_asset_workflow import MarketingAssetGenerator

generator = MarketingAssetGenerator()
result = generator.run_full_workflow(
    design_prompt="summer sale 2024 marketing campaign design",
    image_prompt="Vibrant summer sale marketing banner with tropical elements, 50% off text, bright colors, modern design, 16:9 aspect ratio"
)
```

### Individual Methods

```python
# Search for design inspiration
inspiration = generator.search_design_inspiration("B2B SaaS landing page design")

# Generate marketing image
files = generator.generate_marketing_image(
    prompt="Professional B2B SaaS hero banner, blue color scheme, clean design",
    aspect_ratio="16:9",
    image_size="2K"
)

# Upload to Feishu Drive
links = [generator.upload_to_feishu_drive(f) for f in files]

# Notify Slack
generator.send_slack_notification(files, links, inspiration)
```

## Image Configuration Options

| Parameter | Values |
|-----------|--------|
| `aspect_ratio` | `1:1`, `16:9`, `9:16`, `4:3`, `3:4` |
| `image_size` | `512`, `1K`, `2K`, `4K` |

## ClawFlow Integration

This skill can be used with ClawFlow to create automated marketing pipelines:

- Scheduled campaign asset generation
- Event-triggered asset creation
- Multi-language marketing localization
- A/B test variant generation

## Support

For issues and feature requests, visit [clawhub.com](https://clawhub.com)
