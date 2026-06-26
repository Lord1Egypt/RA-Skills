# 🔍 Google & Baidu Smart Search

**Intelligent Dual Search Engine - Automatically Selects Google or Baidu Based on Query Language**

[![Version 1.0.0](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/leohuang8688/google-baidu-search)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**[English](#-google--baidu-smart-search)** | **[中文](#-google--baidu-智能搜索)**

---

## ✨ Features

- 🤖 **Smart Engine Selection** - Auto-select best engine based on query language
- 🇨🇳 **Chinese Queries** → Automatically use Baidu
- 🌐 **English/International** → Automatically use Google
- 🔍 **Dual Engine Support** - Configure both Google and Baidu
- 📊 **Unified API** - Simple, consistent interface
- 🚀 **Easy Integration** - OpenClaw compatible
- ⚠️ **Fallback Support** - Automatically use available engine if one is unavailable

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

### Environment Variables

```bash
# Google (get from https://console.cloud.google.com/)
export GOOGLE_API_KEY="your_google_api_key"
export GOOGLE_CX="your_search_engine_id"

# Baidu (get from https://ai.baidu.com/)
export BAIDU_API_KEY="your_baidu_api_key"
```

Or use `.env` file:
```bash
# Copy example
cp .env.example .env

# Edit and add your keys
nano .env
```

---

## 📁 Project Structure

```
google-baidu-search/
├── src/
│   └── search.py           # Main search client with smart selection
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
├── SKILL.md                # Skill definition
└── README.md               # This documentation
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

- **GitHub Issues:** https://github.com/leohuang8688/google-baidu-search/issues
- **Google Cloud Docs:** https://cloud.google.com/custom-search/docs
- **Baidu AI Docs:** https://ai.baidu.com/docs

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**PocketAI for Leo** - OpenClaw Community

- GitHub: [@leohuang8688](https://github.com/leohuang8688)
- Contact: claw@pocketai.sg

---

**Happy Searching! 🔍**

---

*Last Updated: 2026-03-19*  
*Version: 1.0.0*

---

---

# 🔍 Google & Baidu 智能搜索

**智能双搜索引擎 - 根据查询语言自动选择 Google 或 Baidu**

[![版本 1.0.0](https://img.shields.io/badge/版本 -1.0.0-green.svg)](https://github.com/leohuang8688/google-baidu-search)
[![许可证 MIT](https://img.shields.io/badge/许可证-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## ✨ 功能特性

- 🤖 **智能引擎选择** - 根据查询语言自动选择最佳引擎
- 🇨🇳 **中文查询** → 自动使用 Baidu
- 🌐 **英文/国际** → 自动使用 Google
- 🔍 **双引擎支持** - 可同时配置 Google 和 Baidu
- 📊 **统一 API** - 简单一致的接口
- 🚀 **易于集成** - OpenClaw 兼容
- ⚠️ **容错支持** - 如果一个引擎不可用，自动使用另一个

---

## 🚀 快速开始

### 安装

```bash
cd ~/.openclaw/workspace/skills/google-baidu-search

# 安装依赖
pip3 install -r requirements.txt
```

### 配置

```bash
# 复制示例 .env 文件
cp .env.example .env

# 编辑 .env 并添加 API 密钥
nano .env
```

### 基本使用

```python
from src.search import search_web

# 自动选择引擎（推荐）
result = search_web("人工智能 2026")  # 自动选择 Baidu
print(result)

result = search_web("AI trends 2026")  # 自动选择 Google
print(result)

# 手动选择引擎
result = search_web("AI trends", engine='google', count=10)
result = search_web("人工智能", engine='baidu', count=10)
result = search_web("AI", engine='both', count=10)
```

### CLI 使用

```bash
# 自动选择引擎（推荐）
python3 src/search.py "人工智能 2026"           # 自动：Baidu
python3 src/search.py "AI trends 2026"          # 自动：Google

# 手动选择引擎
python3 src/search.py "AI trends" google 10     # 强制 Google
python3 src/search.py "人工智能" baidu 10       # 强制 Baidu
python3 src/search.py "AI" both 10              # 搜索两个引擎
```

---

## 🤖 智能引擎选择

### 工作原理

智能搜索引擎根据以下因素自动选择最佳引擎：

1. **语言检测**
   - 中文字符 → Baidu
   - 英文/其他 → Google

2. **关键词检测**
   - 中国相关关键词（中国，北京，上海等）→ Baidu
   - 国际关键词 → Google

### 示例

| 查询 | 自动选择引擎 | 原因 |
|------|-------------|------|
| "人工智能 2026" | Baidu | 包含中文字符 |
| "AI trends 2026" | Google | 英文查询 |
| "北京美食" | Baidu | 中国相关关键词 |
| "New York restaurants" | Google | 国际查询 |
| "中文搜索" | Baidu | 中文关键词 |
| "machine learning" | Google | 英文查询 |

---

## 📖 API 使用

### Python API

```python
from src.search import SmartSearch, search_web

# 方法 1：简单搜索（自动选择）
result = search_web("人工智能 2026")
print(result)

# 方法 2：Smart Search 客户端
searcher = SmartSearch()

# 自动选择引擎
results = searcher.search("人工智能 2026", engine='auto')

# 强制特定引擎
results = searcher.search("AI trends", engine='google')
results = searcher.search("人工智能", engine='baidu')

# 搜索两个引擎
results = searcher.search("AI", engine='both')

# 检查可用引擎
engines = searcher.get_available_engines()
print(f"可用引擎：{engines}")

# 处理结果
for result in results:
    print(f"标题：{result['title']}")
    print(f"链接：{result['url']}")
    print(f"来源：{result['source']}")
    print(f"引擎：{result['engine']}")
    print()
```

---

## ⚙️ 配置指南

### 获取 Google API 凭证

1. **获取 API 密钥：**
   - 访问 https://console.cloud.google.com/
   - 创建新项目或选择现有项目
   - 启用 "Custom Search API"
   - 进入 APIs & Services → Credentials
   - 创建 API 密钥

2. **获取搜索引擎 ID (CX)：**
   - 访问 https://programmablesearchengine.google.com/
   - 点击 "Add" 创建新搜索引擎
   - 配置搜索范围（全网或特定网站）
   - 获取搜索引擎 ID (CX)

### 获取 Baidu API 密钥

1. 访问 https://ai.baidu.com/
2. 注册/登录账号
3. 进入控制台 → 应用管理
4. 创建新应用
5. 获取 API 密钥

### 环境变量

```bash
# Google（从 https://console.cloud.google.com/ 获取）
export GOOGLE_API_KEY="your_google_api_key"
export GOOGLE_CX="your_search_engine_id"

# Baidu（从 https://ai.baidu.com/ 获取）
export BAIDU_API_KEY="your_baidu_api_key"
```

或使用 `.env` 文件：
```bash
# 复制示例
cp .env.example .env

# 编辑并添加密钥
nano .env
```

---

## 📁 项目结构

```
google-baidu-search/
├── src/
│   └── search.py           # 主搜索客户端（智能选择）
├── .env.example            # 环境变量模板
├── requirements.txt        # Python 依赖
├── SKILL.md                # 技能定义
└── README.md               # 本文档
```

---

## 🎯 使用案例

### 1. 新闻搜索

```python
# 中文新闻（自动选择 Baidu）
result = search_web("最新科技新闻 2026")

# 全球新闻（自动选择 Google）
result = search_web("latest tech news 2026")
```

### 2. 研究搜索

```python
# 中文学术（自动选择 Baidu）
result = search_web("机器学习论文")

# 国际学术（自动选择 Google）
result = search_web("machine learning papers")
```

### 3. 产品搜索

```python
# 中文产品（自动选择 Baidu）
result = search_web("智能手机评测")

# 全球产品（自动选择 Google）
result = search_web("smartphone reviews 2026")
```

### 4. 本地搜索

```python
# 中国本地（自动选择 Baidu）
result = search_web("北京美食推荐")

# 国际本地（自动选择 Google）
result = search_web("best restaurants New York")
```

---

## 📝 响应格式

### 搜索结果结构

```json
{
  "title": "页面标题",
  "url": "https://example.com/page",
  "snippet": "页面描述摘要",
  "display_link": "example.com",
  "source": "Google" 或 "Baidu",
  "engine": "google" 或 "baidu"
}
```

### 示例输出

```
🔍 搜索结果：人工智能 2026

引擎：Baidu (自动选择)
可用引擎：google, baidu
找到 10 条结果：

1. **2026 年人工智能发展趋势** [Baidu]
   URL: https://example.com/ai-trends-2026
   人工智能领域在 2026 年将继续快速发展...

2. **AI 技术应用前景** [Baidu]
   URL: https://example.com/ai-applications
   AI 技术在各行业的应用前景广阔...
```

---

## ⚠️ 限制说明

### Google Custom Search
- **API 配额：** 免费层：100 次查询/天
- **结果限制：** 每查询最多 10 条结果
- **API 密钥：** 需要有效的 Google API 密钥
- **搜索引擎：** 需要创建 Custom Search Engine

### Baidu Search
- **API 速率限制：** Baidu API 有速率限制
- **API 密钥：** 需要有效的 Baidu API 密钥
- **中文聚焦：** 最适合中文搜索查询
- **区域限制：** 可能有区域限制

---

## 💰 定价

### Google Custom Search
- **免费层：** 100 次查询/天
- **付费层：** 每 1000 次查询 5 美元
- 适合开发和生产使用

### Baidu Search
- **免费层：** 可用，有限制
- **付费层：** 联系 Baidu 获取定价
- 适合开发和生产使用

---

## 📞 支持

- **GitHub Issues:** https://github.com/leohuang8688/google-baidu-search/issues
- **Google Cloud 文档：** https://cloud.google.com/custom-search/docs
- **Baidu AI 文档：** https://ai.baidu.com/docs

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

---

## 👨‍💻 作者

**PocketAI for Leo** - OpenClaw Community

- GitHub: [@leohuang8688](https://github.com/leohuang8688)
- 联系方式：claw@pocketai.sg

---

**Happy Searching! 🔍**

---

*最后更新：* 2026-03-19  
*版本：* 1.0.0
