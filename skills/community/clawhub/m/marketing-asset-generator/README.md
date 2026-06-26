# Marketing Asset Generator

AI-powered end-to-end marketing asset generation workflow.

## Overview

This skill provides a complete pipeline for marketing teams:

1. **Research** - Search DuckDuckGo for design inspiration and best practices
2. **Create** - Generate high-quality marketing images using Gemini AI
3. **Store** - Automatically upload assets to Feishu Drive
4. **Notify** - Alert the team on Slack with previews and direct links

## Quick Start

```python
from marketing_asset_workflow import MarketingAssetGenerator

generator = MarketingAssetGenerator()
result = generator.run_full_workflow(
    design_prompt="product launch 2024 marketing campaign",
    image_prompt="Modern product launch announcement banner, clean design"
)
```

## Requirements

- Python 3.8+
- Google Gemini API key
- Feishu Open Platform credentials
- Slack Bot token

## License

MIT
