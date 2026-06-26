---
name: instaparser-api
description: Use the Instaparser API to parse articles, PDFs, and generate summaries from URLs. Trigger when users want to extract content from web pages, parse PDF documents, or summarize articles using the Instaparser service.
metadata:
  openclaw:
    requires:
      env:
       - INSTAPARSER_API_KEY
    primaryEnv: INSTAPARSER_API_KEY
---

# Instaparser API Skill

Use this skill when the user wants to interact with the Instaparser API to parse articles, PDFs, or generate summaries.

## Requirements

- **Network access:** This skill makes HTTPS requests to `https://www.instaparser.com/api/`. The user must grant network access when prompted.
- **API key:** All requests require an Instaparser API key set as the `INSTAPARSER_API_KEY` environment variable.

### Getting an API key

1. Go to [https://www.instaparser.com](https://www.instaparser.com) and create an account.
2. After signing in, navigate to the API section of your dashboard to generate an API key.
3. Set the key in your environment:
   ```bash
   export INSTAPARSER_API_KEY="your_api_key_here"
   ```
4. The free Trial plan includes a limited number of monthly credits. Paid plans are available for higher usage.

## Authentication

All API requests require a Bearer token. The API key should be provided via the `INSTAPARSER_API_KEY` environment variable, or the user can provide it directly.

```
Authorization: Bearer $INSTAPARSER_API_KEY
```

## API Endpoints

### Article API

**POST** `https://www.instaparser.com/api/1/article`

Parse an article from a URL and extract its title, author, body content, images, and more. Uses **1 credit** per call.

**Request body (JSON):**

| Parameter   | Type   | Required | Description |
|-------------|--------|----------|-------------|
| `url`       | string | Yes      | URL of the article to parse |
| `content`   | string | No       | Raw HTML content to parse instead of fetching from `url` |
| `output`    | string | No       | `"html"` (default) or `"text"` |
| `use_cache` | bool   | No       | Whether to use cache. Defaults to `true` |

**Example:**

```bash
curl -X POST https://www.instaparser.com/api/1/article \
  -H "Authorization: Bearer $INSTAPARSER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/article", "output": "text"}'
```

**Response fields:**

| Field         | Description |
|---------------|-------------|
| `url`         | Canonical URL |
| `title`       | Article title |
| `site_name`   | Website name |
| `author`      | Author name |
| `date`        | Published date (UNIX timestamp) |
| `description` | Article description |
| `thumbnail`   | Thumbnail image URL |
| `html`        | HTML body (when output is `"html"`) |
| `text`        | Plain text body (when output is `"text"`) |
| `words`       | Word count |
| `is_rtl`      | `true` if Arabic or Hebrew |
| `images`      | Array of image URLs |
| `videos`      | Array of video URLs |

---

### PDF API

Parse PDFs from a URL (GET) or by uploading a file (POST). Uses **5 credits per page**.

#### Parse from URL

**GET** `https://www.instaparser.com/api/1/pdf`

| Parameter   | Type   | Required | Description |
|-------------|--------|----------|-------------|
| `url`       | string | Yes      | URL of the PDF to parse |
| `output`    | string | No       | `"html"` (default) or `"text"` |
| `use_cache` | bool   | No       | Whether to use cache. Defaults to `true` |

```bash
curl "https://www.instaparser.com/api/1/pdf?url=https://example.com/report.pdf&output=text" \
  -H "Authorization: Bearer $INSTAPARSER_API_KEY"
```

#### Upload a file

**POST** `https://www.instaparser.com/api/1/pdf`

Send as multipart form-data with a `file` field.

```bash
curl -X POST https://www.instaparser.com/api/1/pdf \
  -H "Authorization: Bearer $INSTAPARSER_API_KEY" \
  -F "file=@report.pdf" \
  -F "output=text"
```

**Response fields:** Same as Article API.

---

### Summary API

**POST** `https://www.instaparser.com/api/1/summary`

Generate an AI-powered summary with key sentences. Uses **10 credits** per call.

**Request body (JSON):**

| Parameter   | Type   | Required | Description |
|-------------|--------|----------|-------------|
| `url`       | string | Yes      | URL of the article to summarize |
| `content`   | string | No       | HTML content to parse instead of fetching from URL |
| `use_cache` | bool   | No       | Whether to use cache. Defaults to `true` |
| `stream`    | bool   | No       | Stream the response. Defaults to `false` |

```bash
curl -X POST https://www.instaparser.com/api/1/summary \
  -H "Authorization: Bearer $INSTAPARSER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/article"}'
```

**Response fields:**

| Field            | Description |
|------------------|-------------|
| `key_sentences`  | Array of key sentences extracted from the article |
| `summary`        | Concise summary of the article |

---

## Status Codes

| Code | Reason |
|------|--------|
| 200  | Success |
| 400  | Parameter missing or malformed |
| 401  | API key is invalid |
| 403  | Account suspended (payment error) |
| 409  | Exceeded monthly credits (Trial plan only) |
| 412  | Upstream parsing error |
| 429  | Rate limit exceeded |

## SDK Usage

**Python:**
```python
from instaparser import InstaparserClient

client = InstaparserClient(api_key="YOUR_API_KEY")

# Article
article = client.Article(url="https://example.com/article", output="text")

# PDF
pdf = client.PDF(url="https://example.com/report.pdf")

# Summary
summary = client.Summary(url="https://example.com/article")
```

**JavaScript:**
```javascript
import { InstaparserClient } from 'instaparser-api';

const client = new InstaparserClient({ apiKey: 'YOUR_API_KEY' });

// Article
const article = await client.article({ url: 'https://example.com/article', output: 'text' });

// PDF
const pdf = await client.pdf({ url: 'https://example.com/report.pdf' });

// Summary
const summary = await client.summary({ url: 'https://example.com/article' });
```

## Instructions

When the user asks to parse an article, PDF, or generate a summary:

1. Check if `INSTAPARSER_API_KEY` is set in the environment. If not, ask the user for their API key.
2. Use `curl` via the Bash tool to make the API request.
3. For article parsing, default to `output: "text"` unless the user specifically wants HTML.
4. For PDF parsing from a local file, use the multipart form-data POST method.
5. For PDF parsing from a URL, use the GET method with query parameters.
6. Present the results clearly — show title, author, word count, and the extracted content.
7. For summaries, display both the overview/summary and the key sentences.
