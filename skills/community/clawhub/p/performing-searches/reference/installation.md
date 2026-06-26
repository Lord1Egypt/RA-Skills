# 安装指南

augmented-search 与 SearXNG 的完整安装指南。

## 概览

```
┌─────────────────────────────────────────────────────────────┐
│                       安装流程                               │
│                                                              │
│   ┌──────────────┐                                           │
│   │ 检测 Docker  │                                           │
│   └──────┬───────┘                                           │
│          │                                                   │
│    ┌─────┴─────┐                                             │
│    ▼           ▼                                             │
│  有 Docker   无 Docker                                       │
│    │           │                                             │
│    ▼           ▼                                             │
│  方案 A      方案 B                                          │
│  (完整安装)  (npm + 已有 SearXNG)                            │
│                  │                                           │
│                  ▼                                           │
│              无 SearXNG？                                    │
│              使用公共实例                                    │
│              （不推荐）                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 方案 A：Docker 完整安装（推荐）

适用场景：已安装 Docker 的用户。

### 步骤 1：创建目录

```bash
mkdir -p ~/augmented-search && cd ~/augmented-search
```

### 步骤 2：创建 docker-compose.yml

```yaml
services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    ports:
      - "8080:8080"
    volumes:
      - ./searxng:/etc/searxng:rw
    environment:
      - SEARXNG_BASE_URL=http://localhost:8080/
    restart: unless-stopped

  augmented-search:
    image: ghcr.io/sebrinass/mcp-augmented-search:latest
    container_name: augmented-search
    ports:
      - "3000:3000"
    environment:
      - SEARXNG_URL=http://searxng:8080
    depends_on:
      - searxng
    restart: unless-stopped
```

### 步骤 3：启动服务

```bash
docker compose up -d
```

### 步骤 4：验证

```bash
curl http://localhost:8080/search?q=test
curl http://localhost:3000/health
```

---

## 方案 B：npm + 已有 SearXNG

适用场景：已有 SearXNG 实例，无 Docker。

### 前置条件

- Node.js >= 20
- 运行中的 SearXNG 实例

### 步骤 1：安装

```bash
npm install -g augmented-search
```

### 步骤 2：配置环境变量

```bash
# Linux/Mac
export SEARXNG_URL="http://your-searxng:8080"

# Windows PowerShell
$env:SEARXNG_URL = "http://your-searxng:8080"
```

### 步骤 3：运行

```bash
augmented-search
```

### 步骤 4：验证

```bash
curl http://localhost:3000/health
```

---

## 使用公共 SearXNG（不推荐）

⚠️ 隐私警告：公共实例可以看到你的搜索查询。

可用实例：
- https://searx.be
- https://search.bus-hit.me
- https://search.rowie.at
- https://searx.fmac.xyz

```bash
SEARXNG_URL="https://searx.be" augmented-search
```

---

## SearXNG 配置

### 必要配置

创建 `./searxng/settings.yml`（Docker）或编辑 `/etc/searxng/settings.yml`：

```yaml
use_default_settings: true  # 启用所有默认搜索引擎

server:
  port: 8080
  bind_address: "0.0.0.0"
  secret_key: "修改为随机字符串"  # 必须修改！
  limiter: false
  image_proxy: false

search:
  default_lang: "zh-CN"
  safe_search: 0
  formats:
    - html
    - json  # 必须启用！

hostnames:
  remove:  # 可选：过滤视频网站
    - '(.*\.)?youtube\.com$'
    - '(.*\.)?youtu\.be$'
    - '(.*\.)?bilibili\.com$'
    - '(.*\.)?douyin\.com$'

outgoing:  # 建议配置
  request_timeout: 5.0
  max_request_timeout: 15.0  # 纯文本 10-15s，嵌入模型 30-60s
```

### 生成密钥

```bash
# Linux/Mac
openssl rand -hex 32

# Python
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## 混合检索配置（可选）

启用基于 Embedding 的重排序，提升搜索相关性。

### 使用 Ollama（本地）

```bash
# 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 拉取嵌入模型
ollama pull nomic-embed-text

# 配置
export EMBEDDING_BASE_URL="http://localhost:11434"
export EMBEDDING_MODEL="nomic-embed-text"
```

### 使用 OpenAI（云端）

```bash
export EMBEDDING_API_KEY="sk-..."
export EMBEDDING_BASE_URL="https://api.openai.com/v1"
export EMBEDDING_MODEL="text-embedding-3-small"
```

### 使用 Jina（云端）

```bash
export EMBEDDING_API_KEY="jina_..."
export EMBEDDING_BASE_URL="https://api.jina.ai/v1"
export EMBEDDING_MODEL="jina-embeddings-v2-base-en"
```

---

## OpenClaw 集成

OpenClaw 使用 `mcporter` 作为 MCP 客户端。

### HTTP 模式（推荐）

1. 启动 augmented-search HTTP 服务：

```bash
export MCP_HTTP_PORT=3000
export SEARXNG_URL=http://localhost:8080
augmented-search
```

2. 配置 mcporter，添加到 `./config/mcporter.json`：

```json
{
  "servers": {
    "augmented-search": {
      "url": "http://localhost:3000/mcp"
    }
  }
}
```

### stdio 模式

```bash
# 使用 npx
mcporter call --stdio "npx augmented-search" search ...

# 使用 Docker
mcporter call --stdio "docker run -i --rm -e SEARXNG_URL ghcr.io/sebrinass/mcp-augmented-search:latest" search ...
```

**工具使用示例请参阅 [SKILL.md](../SKILL.md#工具使用示例)**

---

## 常见问题

### SearXNG 无响应

```bash
# 查看容器日志
docker logs searxng

# 常见问题：
# 1. 端口 8080 已被占用
# 2. secret_key 未修改
# 3. 卷权限问题
```

### augmented-search 连接失败

```bash
# 检查 SearXNG 地址是否正确
curl $SEARXNG_URL/search?q=test

# Docker 内部：使用容器名
SEARXNG_URL=http://searxng:8080

# 宿主机：使用 host.docker.internal
SEARXNG_URL=http://host.docker.internal:8080
```

### 首次搜索慢

- 首次请求会触发模型加载
- 后续请求会变快

### 超时错误

在 SearXNG `settings.yml` 中增加超时：

```yaml
outgoing:
  request_timeout: 5.0
  max_request_timeout: 15.0
```

**重要**：SearXNG 超时必须小于 augmented-search search工具 超时 5-10 秒（嵌入模型需要视情况增加），否则可能导致结果返回为空。

MCP 超时配置（augmented-search 环境变量）：
```bash
SEARCH_TIMEOUT_MS=30000  # 默认 30 秒
```

---

## 下一步

- 配置 [SearXNG 搜索引擎](https://docs.searxng.org/admin/engines/)
- 生产环境设置 [Redis 缓存](https://docs.searxng.org/admin/settings/#redis)
- 检查 [安全设置](https://docs.searxng.org/admin/settings/#server)
