# 🔍 Google Web Search Skill

**Google 网页搜索技能 - 使用 Google Custom Search API 进行全球网络搜索**

---

## 📋 Overview

| Property | Value |
|----------|-------|
| **Name** | google-web-search |
| **Version** | 1.0.0 |
| **Author** | PocketAI for Leo |
| **License** | MIT |
| **Category** | Search |
| **Required Env Vars** | `GOOGLE_API_KEY`, `GOOGLE_CX` |

---

## 🔐 Required Environment Variables

**This skill requires the following environment variables:**

| Variable | Description | Required | How to Get |
|----------|-------------|----------|------------|
| `GOOGLE_API_KEY` | Google Custom Search API key | ✅ Yes | https://console.cloud.google.com/ |
| `GOOGLE_CX` | Custom Search Engine ID | ✅ Yes | https://programmablesearchengine.google.com/ |

**Configuration:**
```bash
export GOOGLE_API_KEY="your_google_api_key"
export GOOGLE_CX="your_search_engine_id"
```

---

## ✨ Features

---

## ✨ Features

- 🔍 **Google Web Search** - 使用 Google Custom Search API
- 🌍 **Global Coverage** - 全球搜索覆盖
- 📊 **Customizable Results** - 可定制返回结果数量
- 🚀 **Easy Integration** - 易于集成到 OpenClaw
- 🎯 **High Quality** - 高质量搜索结果

---

## 🚀 Quick Start

### Installation

```bash
cd ~/.openclaw/workspace/skills
# Already installed at: google-web-search/
```

### Configuration

**Option 1: Using .env file (Recommended)**

```bash
# Copy the example .env file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your favorite editor
```

**Option 2: Using environment variables**

```bash
export GOOGLE_API_KEY="your_google_api_key"
export GOOGLE_CX="your_search_engine_id"
```

### Basic Usage

```python
from src.google_search import google_search

# Search with default 10 results
result = google_search("AI trends 2026")
print(result)

# Search with custom result count
result = google_search("electric vehicles", count=5)
print(result)
```

### CLI Usage

```bash
# Search with default 10 results
python3 src/google_search.py "AI trends 2026"

# Search with custom result count
python3 src/google_search.py "electric vehicles" 5
```

---

## 📖 API Usage

### Python API

```python
from src.google_search import GoogleSearch, google_search

# Method 1: Simple search
result = google_search("OpenClaw AI", count=10)
print(result)

# Method 2: Using client
searcher = GoogleSearch(
    api_key="your_api_key",
    cx="your_cx_id"
)
results = searcher.search("OpenClaw", count=10)

for result in results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Snippet: {result['snippet']}")
    print(f"Source: {result['display_link']}\n")
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google Custom Search API key | ✅ Yes |
| `GOOGLE_CX` | Custom Search Engine ID | ✅ Yes |

### Getting Google API Key

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "Custom Search API"
4. Go to APIs & Services → Credentials
5. Create API Key

### Creating Search Engine

1. Visit [Programmable Search Engine](https://programmablesearchengine.google.com/)
2. Click "Add" to create a new search engine
3. Configure search scope (entire web or specific sites)
4. Get the Search Engine ID (CX)

---

## 📁 Project Structure

```
google-web-search/
├── src/
│   └── google_search.py    # Main search client
├── SKILL.md                 # This file
└── README.md                # Documentation
```

---

## 🎯 Use Cases

### 1. News Search

```python
result = google_search("latest tech news 2026")
```

### 2. Research

```python
result = google_search("AI healthcare applications research")
```

### 3. Product Search

```python
result = google_search("smartphone reviews 2026")
```

### 4. Academic Search

```python
result = google_search("machine learning papers site:arxiv.org")
```

---

## 📝 Response Format

### Search Result Structure

```json
{
  "title": "Page Title",
  "url": "https://example.com/page",
  "snippet": "Page description snippet",
  "display_link": "example.com"
}
```

### Example Output

```
🔍 Google Search Results for: AI trends 2026

Found 10 results:

1. **Top AI Trends to Watch in 2026**
   Source: forbes.com
   URL: https://forbes.com/ai-trends-2026
   Artificial intelligence continues to evolve rapidly...

2. **The Future of AI in 2026**
   Source: mit.edu
   URL: https://mit.edu/ai-future-2026
   MIT researchers predict major breakthroughs...
```

---

## ⚠️ Limitations

- **API Quotas:** Free tier: 100 queries/day
- **API Key Required:** Must have valid Google API key
- **Search Engine Required:** Must create Custom Search Engine
- **Results Limit:** Maximum 10 results per query

---

## 💰 Pricing

### Free Tier
- 100 queries per day
- Suitable for development and testing

### Paid Tier
- $5 per 1000 queries
- Suitable for production use

---

## 📞 Support

- **Google Cloud Docs:** https://cloud.google.com/custom-search/docs
- **API Reference:** https://developers.google.com/custom-search/v1/overview

---

## 📄 License

MIT License - See LICENSE file for details.

---

**Happy Searching! 🔍**

---

*Last Updated: 2026-03-17*  
*Version: 1.0.0*  
*Author: PocketAI for Leo*
