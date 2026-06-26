# Ollama Web Search Skill

使用 Ollama Web Search API 进行网络搜索和网页抓取。

## 🚀 快速开始

### 1️⃣ 设置 API Key

```bash
export OLLAMA_API_KEY=your_key_here
```

获取 API Key: https://ollama.com/settings/keys

### 2️⃣ 获取 API Key
访问 https://ollama.com/settings/keys 创建你的免费 API Key

### 3️⃣ 依赖检查
```bash
python3 --version  # ✅ macOS 自带
curl --version     # ✅ macOS 自带
```

### 4️⃣ 测试

**搜索:**
```bash
cd ollama-web-search-cli
./ollama-web-search.sh search "AI news" 5
```

**抓取:**
```bash
./ollama-web-search.sh fetch "https://ollama.com"
```

---

## 🎯 在 OpenClaw 中使用

### Slash 命令 (推荐)

**搜索:**
```
/ollama-search "查询主题" [结果数量]
示例：/ollama-search "最新 AI 进展" 5
```

**抓取:**
```
/ollama-fetch "URL"
示例：/ollama-fetch "https://docs.ollama.com"
```

### 直接调用
```
/exec /path/to/ollama-web-search.sh search "查询主题" 5
/exec /path/to/ollama-web-search.sh fetch "URL"
```

### 对话中使用
```
用 ollama-web-search 搜索 "最新 AI 进展"
抓取 https://docs.ollama.com 页面内容
```

---

## 📊 输出示例

### 搜索输出
```
🔍 搜索：AI news (最多 5 个结果)

📄 OpenAI Announces New Model
🔗 https://example.com/article1
📝 OpenAI today announced a new language model with improved...

📄 Google DeepMind Research Update
🔗 https://example.com/article2
📝 Researchers at DeepMind have published new findings...

✅ 搜索完成
```

### 抓取输出
```
📡 抓取：https://ollama.com

📄 标题：Ollama - Get up and running with large language models

📝 内容:
Ollama is a lightweight, extensible framework for building and running LLMs...
[更多内容]

🔗 页面链接 (前 10 个):
https://ollama.com/download
https://ollama.com/blog
...

✅ 抓取完成
```

---

## 🔧 故障排除

### 错误：未设置 OLLAMA_API_KEY
```
❌ 错误：OLLAMA_API_KEY 环境变量未设置
```
**解决**: 设置环境变量 `export OLLAMA_API_KEY=your_key_here`

### 错误：请求失败
```
❌ 请求失败
```
**解决**: 检查网络连接和 API Key 有效性

### 测试 API Key
```bash
curl -X POST "https://ollama.com/api/web_search" \
  -H "Authorization: Bearer $OLLAMA_API_KEY" \
  -d '{"query":"test"}'
```

### 依赖检查
```bash
# 检查 curl 和 jq
which curl && which jq || echo "需要安装：brew install curl jq"
```

---

## 📁 文件结构

```
ollama-web-search-cli/
├── SKILL.md              # 技能文档
├── README.md             # 快速入门
└── ollama-web-search.sh  # 主脚本
```

---

## 🔗 相关链接

- [Ollama Web Search API](https://docs.ollama.com/capabilities/web-search)
- [Ollama API Keys](https://ollama.com/settings/keys)
- [OpenClaw Slash Commands](https://docs.openclaw.ai/tools/slash-commands)

## 许可证

MIT License
