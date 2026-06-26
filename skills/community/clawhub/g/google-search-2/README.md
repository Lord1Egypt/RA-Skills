# 🔍 Google Web Search

**Google 网页搜索技能 - 使用 Google Custom Search API 进行全球网络搜索**

[![Version 1.0.0](https://img.shields.io/badge/version-1.0.0-green.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## 🔐 Required Environment Variables

⚠️ **This skill requires API credentials:**

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google Custom Search API key | ✅ Yes |
| `GOOGLE_CX` | Custom Search Engine ID | ✅ Yes |

**Setup:**
```bash
export GOOGLE_API_KEY="your_google_api_key"
export GOOGLE_CX="your_search_engine_id"
```

**Get API Key:** https://console.cloud.google.com/  
**Get CX:** https://programmablesearchengine.google.com/

---

## ✨ Features

- 🔍 **Google Web Search** - Google Custom Search API
- 🌍 **Global Coverage** - 全球搜索
- 📊 **Customizable** - 可定制结果数量
- 🚀 **Easy Integration** - 易于集成

---

## 🚀 Installation

### 1. Clone or Create

```bash
cd ~/.openclaw/workspace/skills
# Already created at: google-web-search/
```

### 2. Install Dependencies

```bash
cd google-web-search
pip3 install -r requirements.txt
```

### 3. Configure API Keys

```bash
# Get API keys from Google Cloud
export GOOGLE_API_KEY="your_api_key"
export GOOGLE_CX="your_search_engine_id"
```

---

## 📖 Usage

### Python API

```python
from src.google_search import google_search

# Search
result = google_search("AI trends 2026", count=10)
print(result)
```

### CLI

```bash
python3 src/google_search.py "AI trends 2026" 10
```

---

## ⚙️ Configuration

### Get Google API Key

1. Visit https://console.cloud.google.com/
2. Create project
3. Enable Custom Search API
4. Create API Key

### Get Search Engine ID

1. Visit https://programmablesearchengine.google.com/
2. Create search engine
3. Get Search Engine ID (CX)

---

## 📁 Structure

```
google-web-search/
├── src/
│   └── google_search.py
├── requirements.txt
├── SKILL.md
└── README.md
```

---

## 📄 License

MIT License

---

**Happy Searching! 🔍**
