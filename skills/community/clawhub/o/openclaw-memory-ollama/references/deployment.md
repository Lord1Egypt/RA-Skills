# OpenClaw 记忆管理系统部署实施指南

## 环境要求

### 必需组件

1. **OpenClaw** — AI 助手框架
2. **Ollama** — 本地 LLM 和 Embedding 服务
   - 模型: `nomic-embed-text` (274MB, 768维)
3. **PostgreSQL** — 向量存储数据库
   - 需安装 pgvector 扩展
4. **Redis** — 热缓存
5. **cognitive-brain 技能** — 已安装

### 验证环境

```bash
# 验证 Ollama
ollama list
ollama show nomic-embed-text

# 验证 PostgreSQL
psql -h localhost -p 5432 -U postgres -d cognitive_brain -c "\dt"

# 验证 Redis
redis-cli ping
```

## 部署步骤

### Step 1: 安装和配置 Ollama

```bash
# 安装 Ollama (macOS)
brew install ollama

# 启动 Ollama
ollama serve

# 拉取 Embedding 模型
ollama pull nomic-embed-text

# 验证
ollama list
```

### Step 2: 配置 cognitive-brain

编辑 `~/.openclaw/workspace-*/skills/cognitive-brain/config.json`:

```json
{
  "provider": "ollama",
  "dimension": 768,
  "model": "nomic-embed-text",
  "ollama": {
    "baseUrl": "http://localhost:11434",
    "apiKey": "ollama-local"
  }
}
```

### Step 3: 配置 Embedding 脚本

编辑 `scripts/embed.py`，使用 Ollama API 替代 sentence-transformers:

```python
import urllib.request
import json

def embed_text(text):
    """使用 Ollama API 生成 embedding 向量"""
    url = "http://localhost:11434/api/embeddings"
    payload = {
        "model": "nomic-embed-text",
        "prompt": text
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read())
        return result["embedding"]
```

### Step 4: 配置 OpenClaw

编辑 `~/.openclaw/openclaw.json`:

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "provider": "ollama",
        "model": "nomic-embed-text:latest"
      }
    }
  }
}
```

### Step 5: 设置环境变量

```bash
export OLLAMA_API_KEY=ollama-local
export OLLAMA_HOST=localhost:11434
```

### Step 6: 重启 Gateway

```bash
openclaw gateway restart
```

## 验证测试

### 验证 Embedding 服务

```bash
cd ~/.openclaw/workspace-*/skills/cognitive-brain
python3 scripts/embed.py --warmup
```

预期输出: `{"status": "warmed_up", "model": "nomic-embed-text"}`

### 验证记忆写入

```
# 在 AI 对话中说 "记住我今天开了重要的会议"
# 然后检查 brain episodes
```

### 验证记忆检索

```
# 问 "我今天开了什么会议？"
# 应该在上下文看到相关记忆
```

## 性能指标

| 指标 | 数值 |
|------|------|
| Embedding 生成 | <100ms |
| 语义搜索延迟 | ~40ms |
| 向量维度 | 768 |
| Episodes 覆盖 | 13/13 |

## 故障排查

### Embedding 服务无响应

1. 检查 Ollama 是否运行: `ollama serve`
2. 检查模型是否已拉取: `ollama list`
3. 检查 API 端口: `curl localhost:11434/api/tags`

### 记忆检索失败

1. 检查 PostgreSQL 连接: `psql -h localhost -p 5432 -U postgres -d cognitive_brain`
2. 检查 Redis 连接: `redis-cli ping`
3. 检查 cognitive-brain 配置: `cat config.json`

### 性能问题

1. 检查内存使用: `top` 或 `htop`
2. 检查 Ollama 模型加载: `ollama ps`
3. 检查 PostgreSQL 索引: `SELECT * FROM pg_indexes WHERE tablename = 'episodes'`
