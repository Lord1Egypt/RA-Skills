# 🔍 Google & Baidu Smart Search

**智能双搜索引擎 - 自动选择最佳搜索引擎**

[![Version 1.0.0](https://img.shields.io/badge/version-1.0.0-green.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## 🔐 Required Environment Variables

⚠️ **This skill requires at least one search engine:**

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google Custom Search API key | ⚠️ Optional* |
| `GOOGLE_CX` | Google Custom Search Engine ID | ⚠️ Optional* |
| `BAIDU_API_KEY` | Baidu Search API key | ⚠️ Optional* |

*At least one search engine must be configured. Recommended: configure both for best results.

**Setup:**
```bash
# Google (get from https://console.cloud.google.com/)
export GOOGLE_API_KEY="your_google_api_key"
export GOOGLE_CX="your_search_engine_id"

# Baidu (get from https://ai.baidu.com/)
export BAIDU_API_KEY="your_baidu_api_key"

# Or use .env file
cp .env.example .env
# Edit .env and add your API keys
```

---

## ✨ Features

- 🤖 **Smart Engine Selection** - Auto-select best engine based on query
- 🇨🇳 **Chinese Queries** → Use Baidu automatically
- 🌐 **English/International** → Use Google automatically
- 🔍 **Dual Engine Support** - Configure both Google and Baidu
- 📊 **Unified API** - Simple, consistent interface
- 🚀 **Easy Integration** - OpenClaw compatible

---

## 🚀 Quick Start

### Installation

```bash
cd ~/.openclaw/workspace/skills/google-baidu-search

# Install dependencies
pip3 install -r requirements.txt
```

### Configuration

```bash
# Copy example .env file
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

### Basic Usage

```python
from src.search import search_web

# Auto-select engine (recommended)
result = search_web("人工智能 2026")  # Auto-selects Baidu
print(result)

result = search_web("AI trends 2026")  # Auto-selects Google
print(result)

# Manual engine selection
result = search_web("AI trends", engine='google', count=10)
result = search_web("人工智能", engine='baidu', count=10)
result = search_web("AI", engine='both', count=10)
```

### CLI Usage

```bash
# Auto-select engine (recommended)
python3 src/search.py "人工智能 2026"           # Auto: Baidu
python3 src/search.py "AI trends 2026"          # Auto: Google

# Manual engine selection
python3 src/search.py "AI trends" google 10     # Force Google
python3 src/search.py "人工智能" baidu 10       # Force Baidu
python3 src/search.py "AI" both 10              # Search both
```

---

## 🤖 Smart Engine Selection

### How It Works

The smart search engine automatically selects the best search engine based on:

1. **Language Detection**
   - Chinese characters → Baidu
   - English/Other → Google

2. **Keyword Detection**
   - China-related keywords (中国，北京，上海，etc.) → Baidu
   - International keywords → Google

### Examples

| Query | Auto-Selected Engine | Reason |
|-------|---------------------|--------|
| "人工智能 2026" | Baidu | Contains Chinese characters |
| "AI trends 2026" | Google | English query |
| "北京美食" | Baidu | China-related keyword |
| "New York restaurants" | Google | International query |
| "中文搜索" | Baidu | Chinese keyword |
| "machine learning" | Google | English query |

---

## 📖 API Usage

### Python API

```python
from src.search import SmartSearch, search_web

# Method 1: Simple search (auto-select)
result = search_web("人工智能 2026")
print(result)

# Method 2: Smart Search client
searcher = SmartSearch()

# Auto-select engine
results = searcher.search("人工智能 2026", engine='auto')

# Force specific engine
results = searcher.search("AI trends", engine='google')
results = searcher.search("人工智能", engine='baidu')

# Search both engines
results = searcher.search("AI", engine='both')

# Check available engines
engines = searcher.get_available_engines()
print(f"Available engines: {engines}")

# Process results
for result in results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Source: {result['source']}")
    print(f"Engine: {result['engine']}")
    print()
```

---

## ⚙️ Configuration

### Get Google API Credentials

1. **Get API Key:**
   - Visit https://console.cloud.google.com/
   - Create a new project or select existing
   - Enable "Custom Search API"
   - Go to APIs & Services → Credentials
   - Create API Key

2. **Get Search Engine ID (CX):**
   - Visit https://programmablesearchengine.google.com/
   - Click "Add" to create a new search engine
   - Configure search scope (entire web or specific sites)
   - Get the Search Engine ID (CX)

### Get Baidu API Key

1. Visit https://ai.baidu.com/
2. Create an account or login
3. Go to Console → Applications
4. Create a new application
5. Get your API Key

---

## 📁 Project Structure

```
google-baidu-search/
├── src/
│   └── search.py           # Main search client with smart selection
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
├── SKILL.md                # This file
└── README.md               # Documentation
```

---

## 🎯 Use Cases

### 1. News Search

```python
# Chinese news (auto-selects Baidu)
result = search_web("最新科技新闻 2026")

# Global news (auto-selects Google)
result = search_web("latest tech news 2026")
```

### 2. Research

```python
# Chinese academic (auto-selects Baidu)
result = search_web("机器学习论文")

# International academic (auto-selects Google)
result = search_web("machine learning papers")
```

### 3. Product Search

```python
# Chinese products (auto-selects Baidu)
result = search_web("智能手机评测")

# Global products (auto-selects Google)
result = search_web("smartphone reviews 2026")
```

### 4. Local Search

```python
# China local (auto-selects Baidu)
result = search_web("北京美食推荐")

# International local (auto-selects Google)
result = search_web("best restaurants New York")
```

---

## 📝 Response Format

### Search Result Structure

```json
{
  "title": "Page Title",
  "url": "https://example.com/page",
  "snippet": "Page description snippet",
  "display_link": "example.com",
  "source": "Google" or "Baidu",
  "engine": "google" or "baidu"
}
```

### Example Output

```
🔍 Search Results for: 人工智能 2026

Engine: Baidu (Auto-selected)
Available engines: google, baidu
Found 10 results:

1. **2026 年人工智能发展趋势** [Baidu]
   URL: https://example.com/ai-trends-2026
   人工智能领域在 2026 年将继续快速发展...

2. **AI 技术应用前景** [Baidu]
   URL: https://example.com/ai-applications
   AI 技术在各行业的应用前景广阔...
```

---

## ⚠️ Limitations

### Google Custom Search
- **API Quotas:** Free tier: 100 queries/day
- **Results Limit:** Maximum 10 results per query
- **API Key Required:** Must have valid Google API key
- **Search Engine Required:** Must create Custom Search Engine

### Baidu Search
- **API Rate Limits:** Baidu API has rate limits
- **API Key Required:** Must have valid Baidu API key
- **Chinese Focus:** Best for Chinese language queries
- **Regional Restrictions:** May have regional restrictions

---

## 💰 Pricing

### Google Custom Search
- **Free Tier:** 100 queries/day
- **Paid Tier:** $5 per 1000 queries
- Suitable for development and production use

### Baidu Search
- **Free Tier:** Available with limits
- **Paid Tier:** Contact Baidu for pricing
- Suitable for development and production use

---

## 📞 Support

- **Google Cloud Docs:** https://cloud.google.com/custom-search/docs
- **Baidu AI Docs:** https://ai.baidu.com/docs
- **API Reference:** See documentation

---

## 📄 License

MIT License - See LICENSE file for details.

---

**Happy Searching! 🔍**

---

*Last Updated: 2026-03-19*  
*Version: 1.0.0*  
*Author: PocketAI for Leo*  
*Contact: claw@pocketai.sg*
