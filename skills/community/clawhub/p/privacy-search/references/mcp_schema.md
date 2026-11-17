# MCP Server 工具 Schema 文档（V1.7）

本文档描述 privacy-search MCP Server 的工具接口契约，供其他 skill 作者接入参考。

## 运行方式

```bash
# 启动 MCP Server（stdio 模式）
python scripts/mcp_server.py

# 查看工具 schema
python scripts/mcp_server.py --schema

# 协议自测
python scripts/mcp_server.py --test
```

## 工具列表

| 工具名 | 描述 | 主要能力 |
|--------|------|----------|
| `search` | 多引擎并行搜索 | 10 引擎并发、SimHash 去重、多因子排序 |
| `synthesize` | Perplexity 式答案合成 | 抓取正文、LLM 带 citation 生成 |
| `fetch` | 网页正文抓取 | 三层降级提取正文 |

---

## 工具详细 Schema

### 1. search — 多引擎并行搜索

**描述**：同时检索百度、必应、DuckDuckGo、Yandex 等十大搜索引擎，SimHash 去重、多因子加权排序。

**输入参数**：

```json
{
  "query": {
    "type": "string",
    "description": "搜索查询词（必填）"
  },
  "engines": {
    "type": "array",
    "items": { "type": "string" },
    "description": "指定引擎列表。可选值：baidu, bing, sogou, 360, duckduckgo, yandex, startpage, qwant, brave, searxng。留空时按隐私模式自动选择。"
  },
  "num": {
    "type": "integer",
    "description": "每个引擎返回结果数（默认 10，最大 20）",
    "default": 10
  },
  "privacy": {
    "type": "string",
    "enum": ["normal", "strict"],
    "description": "隐私模式：normal（全引擎）或 strict（仅隐私友好引擎）",
    "default": "normal"
  },
  "no_cache": {
    "type": "boolean",
    "description": "跳过缓存，强制重新搜索",
    "default": false
  }
}
```

**响应格式**：

```json
{
  "results": [
    {
      "title": "标题",
      "url": "https://example.com",
      "snippet": "摘要",
      "engine": "baidu",
      "engines": ["baidu", "bing"],
      "rank": 1,
      "score": 8.5
    }
  ],
  "notices": ["提示信息"],
  "from_cache": false,
  "count": 10
}
```

---

### 2. synthesize — Perplexity 式答案合成

**描述**：抓取搜索结果正文，分块编号后调用 LLM 生成带 citation 的答案。每个论断都能追溯到具体来源。无 API Key 时自动降级为抽取式摘要。

**输入参数**：

```json
{
  "query": {
    "type": "string",
    "description": "用户问题（必填）"
  },
  "results": {
    "type": "array",
    "description": "搜索结果数组（可选）。未提供时自动先执行搜索。格式：[{\"title\":\"...\",\"url\":\"...\",\"snippet\":\"...\"}, ...]"
  },
  "max_sources": {
    "type": "integer",
    "description": "最多引用几个来源（默认 5，最大 10）",
    "default": 5
  }
}
```

**响应格式**：

```json
{
  "answer": "这是 LLM 生成的答案 [1][2]。\n\n--- 来源 ---\n[1] https://example.com/1\n[2] https://example.com/2",
  "notices": ["提示信息"]
}
```

---

### 3. fetch — 网页正文抓取

**描述**：从指定 URL 提取正文内容，三层降级：trafilatura → boilerpy3 → 正则 <p> 标签。

**输入参数**：

```json
{
  "url": {
    "type": "string",
    "description": "目标网页 URL（必填）"
  },
  "timeout": {
    "type": "integer",
    "description": "抓取超时（秒），默认 10",
    "default": 10
  }
}
```

**响应格式**：

```json
{
  "url": "https://example.com",
  "text": "正文内容...",
  "success": true,
  "length": 1234
}
```

---

## 超时与降级策略

### 超时配置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `mcp_server.timeout` | 30s | 单次工具调用超时 |
| `mcp_server.max_results` | 10 | search 工具默认最大结果数 |
| `mcp_server.max_sources` | 5 | synthesize 工具默认最大引用来源数 |
| `synthesis.fetch_timeout` | 10s | 单个页面抓取超时 |
| `search.timeout` | 15s | 单个引擎搜索超时 |

### 降级策略

| 场景 | 降级行为 |
|------|----------|
| LLM API Key 未配置 | synthesize 自动降级为抽取式摘要 + 来源列表 |
| LLM 调用失败 | 同上 |
| 页面正文抓取失败 | 降级使用该结果的 snippet |
| 所有页面正文抓取失败 | 降级为抽取式摘要 |
| 搜索引擎限流 | 自动重试 + 指数退避 |
| strict 模式引擎全部失败 | 默认拒绝降级（隐私优先），可配置 `allow_fallback` |

### 错误处理

所有工具调用返回统一的错误格式：

```json
{
  "error": "错误描述"
}
```

---

## 生态桥接示例

### 其他 skill 接入本 MCP Server

根据"章首桥接原则"，其他 skill 可按以下方式探测并调用 privacy-search：

```python
# 1. 探测 privacy-search 是否已安装
import shutil
def is_privacy_search_available() -> bool:
    return shutil.which("python") is not None  # 检查 python 环境

# 2. 调用 MCP Server（stdio 模式）
import subprocess
proc = subprocess.Popen(
    ["python", "scripts/mcp_server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

# 3. 发送 initialize 请求
import json
def send_request(proc, method, params=None):
    msg = {"jsonrpc": "2.0", "id": 1, "method": method}
    if params:
        msg["params"] = params
    body = json.dumps(msg, ensure_ascii=False)
    length = len(body.encode("utf-8"))
    proc.stdin.write(f"Content-Length: {length}\r\n\r\n{body}".encode())
    proc.stdin.flush()
    # 读取响应...
```

### 典型调用场景

| 调用方 | 场景 | 推荐工具 |
|--------|------|----------|
| gov-procurement | 政策资料查询 | `search` + `fetch` |
| contract-review | 法条补充检索 | `search` + `synthesize` |
| 其他 skill | 通用搜索 | `search` |

---

## 接口契约稳定性承诺

1. **版本化 schema**：工具 schema 随 SKILL.md 版本号同步更新
2. **向后兼容**：小版本（1.x）内不删除/重命名工具参数
3. **降级保证**：所有外部依赖（LLM、搜索引擎）都有降级方案
4. **超时可控**：所有网络调用都有可配置的超时

---

## 配置示例

```yaml
# config.yaml
mcp_server:
  enabled: true
  timeout: 30
  max_results: 10
  max_sources: 5

synthesis:
  enabled: true
  api_key: ""  # 留空则强制降级
  provider: auto
  max_sources: 5

search:
  timeout: 15
  num_results: 10
```
