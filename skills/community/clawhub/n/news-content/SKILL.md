---
name: news-content-extractor
description: Input a news URL to efficiently extract the body, title, author, and date using a remote API.
metadata: {"openclaw": {"requires": {"bins": ["node"], "env": ["EASYALPHA_API_KEY", "NEWS_EXTRACTOR_SERVER_URL"]}}}
---

# News Content Extractor (Pro Version)

This is a news content extraction Skill using a client-server architecture.

## Features
- **Zero Local Dependencies**: Uses Node.js for the client, so no complex Python libraries need to be installed locally.
- **Authentication**: Core API calls are protected by `EASYALPHA_API_KEY`.
- **High-Performance Parsing**: Powered by a remote backend service based on `trafilatura`.

## Configuration Requirements

The following environment variables must be set to use this Skill:

1. `EASYALPHA_API_KEY`: Your authentication token. Obtainable from: https://easyalpha.duckdns.org
2. `NEWS_EXTRACTOR_SERVER_URL`: (Optional) The backend server address. Defaults to the production API: https://easyalpha.duckdns.org/api/v1/extract

## Usage

**User**: "Scrape the content of this page: https://www.bbc.com/news/uk-12345678"

**Agent Behavior**:
- Runs `node scripts/extract_news.js https://www.bbc.com/news/uk-12345678`
- The script automatically includes the Token and sends the request to the server.
- Parses and displays the results.
