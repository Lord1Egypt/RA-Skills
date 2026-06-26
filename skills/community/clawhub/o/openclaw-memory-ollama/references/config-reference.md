# OpenClaw 记忆管理系统配置参考

## 配置文件位置

| 配置文件 | 路径 |
|---------|------|
| OpenClaw 主配置 | `~/.openclaw/openclaw.json` |
| cognitive-brain 配置 | `~/.openclaw/workspace-*/skills/cognitive-brain/config.json` |
| Embedding 脚本 | `~/.openclaw/workspace-*/skills/cognitive-brain/scripts/embed.py` |

## cognitive-brain config.json

```json
{
  "provider": "ollama",
  "dimension": 768,
  "model": "nomic-embed-text",
  "ollama": {
    "baseUrl": "http://localhost:11434",
    "apiKey": "ollama-local"
  },
  "brain": {
    "host": "localhost",
    "port": 5432,
    "database": "cognitive_brain",
    "user": "<your-postgres-user>",
    "password": "<your-postgres-password>"
  },
  "redis": {
    "host": "localhost",
    "port": 6379
  }
}
```

### 配置字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| provider | string | Embedding 提供商，可选: ollama, openai |
| dimension | int | 向量维度，nomic-embed-text 为 768 |
| model | string | 模型名称 |
| ollama.baseUrl | string | Ollama API 地址 |
| ollama.apiKey | string | API Key（本地可设为任意值）|
| brain.* | object | PostgreSQL 连接配置 |
| redis.* | object | Redis 连接配置 |

## openclaw.json 配置

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "minimax/MiniMax-M2.7"
      },
      "memorySearch": {
        "provider": "ollama",
        "model": "nomic-embed-text:latest"
      },
      "thinkingDefault": "high"
    }
  }
}
```

### 配置字段说明

| 字段 | 说明 |
|------|------|
| agents.defaults.model.primary | 默认 LLM 模型 |
| agents.defaults.memorySearch.provider | 记忆搜索 provider |
| agents.defaults.memorySearch.model | Embedding 模型 |
| agents.defaults.thinkingDefault | 默认思考级别 |

## 环境变量

```bash
# Ollama 配置
export OLLAMA_API_KEY=ollama-local
export OLLAMA_HOST=localhost:11434

# 可选: 覆盖默认 OpenAI 配置
# export OPENAI_API_KEY=your-key
# export OPENAI_BASE_URL=https://api.openai.com/v1
```

## 数据库表结构

### episodes 表 (情景记忆)

```sql
CREATE TABLE episodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    metadata JSONB DEFAULT '{}',
    embedding向量类型(768) USING embedding::vector(768),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 创建向量索引
CREATE INDEX episodes_embedding_idx ON episodes 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- 创建角色过滤索引
CREATE INDEX episodes_role_idx ON episodes (role);
```

### concepts 表 (概念知识)

```sql
CREATE TABLE concepts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    metadata JSONB DEFAULT '{}',
    embedding向量类型(768) USING embedding::vector(768),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 创建向量索引
CREATE INDEX concepts_embedding_idx ON concepts
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

## Redis 键结构

| 键模式 | 类型 | TTL | 说明 |
|--------|------|-----|------|
| brain:memory:session:* | String | 60分钟 | 会话上下文 |
| brain:sensory:* | String | 30秒 | 感官记忆 |

## cognitive-brain 引用说明

本技能引用 cognitive-brain 技能的以下代码:

1. **brain.js/brain.py** — 核心记忆服务接口
2. **数据库 schema** — episodes 和 concepts 表结构
3. **Redis 缓存逻辑** — 热数据缓存机制

引用来源: cognitive-brain 技能目录
`~/.openclaw/workspace-*/skills/cognitive-brain/`
