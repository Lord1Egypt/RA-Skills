---
name: news-impact-analyzer
description: Input news text and use an LLM to analyze its impact on stock market sectors and concepts (bullish/bearish/neutral) along with the underlying logic.
metadata: {"openclaw": {"requires": {"bins": ["node"], "env": ["EASYALPHA_API_KEY"]}}}
---

# News Impact Analyzer

This is a Skill designed to assist with stock market investment research and analysis.

## Features
- **Zero Local Dependencies**: The client side is written in pure Node.js and requires no `npm install`.
- **Deep Insights**: Leverages Large Language Models to analyze news content and extract affected sectors and concept trends.
- **Frontend-Backend Separation**: Communication with the LLM is handled by a remote FastAPI-based backend service.

## Configuration Requirements

To use this Skill, you must set the following environment variable:

1. `EASYALPHA_API_KEY`: Your authentication token. You can obtain this by registering an account at `https://easyalpha.duckdns.org`.
2. `NEWS_EXTRACTOR_SERVER_URL`: The backend analysis server address (e.g., `http://localhost:8000`). Default is `https://easyalpha.duckdns.org`.

## Usage Instructions

**User**: "Analyze the impact of this news regarding a breakthrough in AI chips: A certain tech company announced a major breakthrough in computing-in-memory chips, expecting mass production next year..."

**Agent Action**:
- Run `node scripts/analyze_news.js "<news text content>"`
- The script automatically includes the Token and sends a request to the server for analysis.
- It will parse and display the impacted sectors, the bullish/bearish direction, and the logic behind it.
