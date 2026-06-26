---
name: ollama-web-search-cli
description: 使用 Ollama Web Search API 进行网络搜索和网页抓取
version: 1.0.1
author: sunnydou
license: MIT
requirements: [curl, python3]
env:
  - name: OLLAMA_API_KEY
    description: Ollama API Key for web search and fetch endpoints
    required: true
    source: https://ollama.com/settings/keys
credentials:
  - OLLAMA_API_KEY
---

# ollama-web-search Skill

使用 Ollama Web Search API 进行网络搜索和网页抓取。

## 🔧 前置要求

### 1. Ollama API Key
- 访问 https://ollama.com/settings/keys 创建 API Key
- 设置环境变量：`export OLLAMA_API_KEY=your_key_here`

### 2. 依赖工具
- `curl`: HTTP 请求工具 (macOS/Linux 自带)
- `python3`: JSON 解析和转义 (macOS/Linux 自带)

### 3. 依赖检查
```bash
python3 --version  # 检查 Python3
curl --version     # 检查 curl
```

---

## 📋 功能

| 功能 | 命令 | 说明 |
|------|------|------|
| **Web Search** | `search` | 执行网络搜索，返回相关结果 |
| **Web Fetch** | `fetch` | 获取单个网页内容 |

---

## 🛠️ 使用方法

### 方法一：直接执行脚本

**搜索:**
```bash
./ollama-web-search.sh search "AI 最新进展" 5
```

**抓取网页:**
```bash
./ollama-web-search.sh fetch "https://ollama.com"
```

### 方法二：使用 Slash 命令 (推荐)

**搜索:**
```
/ollama-search "AI 最新进展" 5
```

**抓取网页:**
```
/ollama-fetch "https://ollama.com"
```

### 方法三：在对话中使用
```
用 ollama-web-search-cli 搜索 "Ollama 新功能"
抓取 https://docs.ollama.com 页面内容
```

---

## 📊 参数

### Web Search
| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `query` | string | ✅ | - | 搜索查询字符串 |
| `max_results` | number | ❌ | 5 | 最大结果数 (1-10) |

### Web Fetch
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `url` | string | ✅ | 要抓取的网页 URL |

---

## 📤 响应格式

### Web Search
```json
{
  "results": [
    {
      "title": "页面标题",
      "url": "https://example.com",
      "content": "相关内容摘要"
    }
  ]
}
```

### Web Fetch
```json
{
  "title": "页面标题",
  "content": "页面主要内容",
  "links": ["链接 1", "链接 2", ...]
}
```

---

## 🔍 示例

### 搜索示例
```bash
# 基本搜索
./ollama-web-search.sh search "什么是 Ollama" 5

# 技术搜索
./ollama-web-search.sh search "LLM model scheduling" 10

# 新闻搜索
./ollama-web-search.sh search "AI news 2026" 5

# Slash 命令
/ollama-search "Ollama Web Search API" 5
```

### 抓取示例
```bash
# 抓取 Ollama 首页
./ollama-web-search.sh fetch "https://ollama.com"

# 抓取文档
./ollama-web-search.sh fetch "https://docs.ollama.com"

# Slash 命令
/ollama-fetch "https://docs.openclaw.ai"
```

---

## 🔧 API 端点

| API | 端点 | 方法 |
|-----|------|------|
| **Web Search** | `https://ollama.com/api/web_search` | POST |
| **Web Fetch** | `https://ollama.com/api/web_fetch` | POST |

### cURL 示例
```bash
# Web Search
curl -X POST "https://ollama.com/api/web_search" \
  -H "Authorization: Bearer $OLLAMA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"what is ollama","max_results":5}'

# Web Fetch
curl -X POST "https://ollama.com/api/web_fetch" \
  -H "Authorization: Bearer $OLLAMA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://ollama.com"}'
```

---

## ⚠️ 注意事项

- **API Key**: 必须设置 `OLLAMA_API_KEY`
- **账户**: 需要免费 Ollama 账户
- **速率限制**: 参考 Ollama API 文档
- **缓存**: 结果缓存 15 分钟
- **SSRF 保护**: 私有/内部 IP 地址会被阻止
- **错误处理**: 脚本会检查 API Key 和响应状态

---

## 📁 文件结构

```
ollama-search-tool/
├── SKILL.md              # 技能文档
├── README.md             # 快速入门
├── _meta.json            # 元数据
└── ollama-web-search.sh  # 主脚本

slash-commands/
├── ollama-search         # 搜索命令
└── ollama-fetch          # 抓取命令
```

---

## 🔗 相关文档

- [Ollama Web Search API](https://docs.ollama.com/capabilities/web-search)
- [OpenClaw Tools](https://docs.openclaw.ai/tools/web)
- [Ollama API Keys](https://ollama.com/settings/keys)
- [OpenClaw Slash Commands](https://docs.openclaw.ai/tools/slash-commands)
