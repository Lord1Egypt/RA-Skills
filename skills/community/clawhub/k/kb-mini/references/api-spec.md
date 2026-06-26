# API 接口规范

## 1. 概述

所有接口通过 `kb` 命令行工具调用：

```bash
kb <command> [options]
```

## 2. store - 存入单条

### 2.1 用法

```bash
kb store [options]
```

### 2.2 参数

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--title`, `-t` | 是 | 标题 | `"OpenClaw Hooks"` |
| `--content`, `-c` | 是 | 内容 | `"配置说明..."` |
| `--topic-key` | 否 | 主题 key，默认自动生成 | `openclaw-hooks` |
| `--tags` | 否 | 标签，逗号分隔 | `openclaw,hooks` |
| `--source` | 否 | 来源，默认 manual | `rss/github/huggingface/manual` |
| `--level` | 否 | 层级，默认 2 | `0/1/2` |
| `--metadata` | 否 | 扩展 JSON | `'{"url":"..."}'` |

### 2.3 示例

```bash
kb store \
  --title "OpenClaw Hooks 配置" \
  --content "OpenClaw 支持 before_agent_start 和 after_turn..." \
  --tags "openclaw,hooks" \
  --source "manual" \
  --level 2
```

### 2.4 输出

**成功**：
```json
{
  "status": "ok",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "topic_key": "openclaw-hooks",
  "action": "insert"  // insert 或 update
}
```

**失败**：
```json
{
  "status": "error",
  "error": "Missing required argument: --title"
}
```

## 3. search - 检索

### 3.1 用法

```bash
kb search [options]
```

### 3.2 参数

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--query`, `-q` | 是 | 搜索关键词 | `openclaw hooks` |
| `--limit` | 否 | 返回数量，默认 5 | `10` |
| `--level` | 否 | 加载层级 | `0/1/2` |
| `--source` | 否 | 按来源过滤 | `rss/github/huggingface` |
| `--since` | 否 | 过滤时间 | `7d/30d/90d` |
| `--time-decay` | 否 | 时间衰减因子 | `0.1` |
| `--format` | 否 | 输出格式，默认 json | `json/text/compact` |

### 3.3 示例

```bash
# 基础搜索
kb search --query "openclaw hooks"

# 带过滤
kb search --query "openclaw" --source github --since 7d --limit 10

# 简洁输出
kb search --query "openclaw" --format compact
```

### 3.4 输出

**JSON 格式（默认）**：
```json
{
  "results": [
    {
      "topic_key": "openclaw-hooks",
      "title": "OpenClaw Hooks 配置指南",
      "level": "L1",
      "summary": "OpenClaw 支持 before_agent_start...",
      "relevance_score": 0.85,
      "source": "manual",
      "tags": ["openclaw", "hooks"],
      "updated_at": "2026-03-22T10:00:00Z"
    }
  ],
  "total_hits": 12,
  "query_time_ms": 45
}
```

**Text 格式**：
```
1. OpenClaw Hooks 配置指南 (0.85)
   摘要: OpenClaw 支持 before_agent_start...
   来源: manual | 更新: 2026-03-22
   
2. OpenClaw before_agent_start Hook (0.72)
   摘要: 在 Agent 启动前执行...
   来源: github | 更新: 2026-03-21
```

**Compact 格式**：
```
[0.85] OpenClaw Hooks 配置指南 - manual - 2026-03-22
[0.72] OpenClaw before_agent_start Hook - github - 2026-03-21
```

## 4. retrieve - 按 topic_key 取

### 4.1 用法

```bash
kb retrieve [options]
```

### 4.2 参数

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--topic-key`, `-k` | 是 | 主题 key | `openclaw-hooks` |
| `--level` | 否 | 加载层级，默认 2 | `0/1/2` |

### 4.3 示例

```bash
kb retrieve --topic-key "openclaw-hooks"
```

### 4.4 输出

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "topic_key": "openclaw-hooks",
  "title": "OpenClaw Hooks 配置指南",
  "content": "完整内容...",
  "source": "manual",
  "tags": ["openclaw", "hooks"],
  "level": "L2",
  "created_at": "2026-03-20T10:00:00Z",
  "updated_at": "2026-03-22T10:00:00Z"
}
```

## 5. batch_store - 批量存入

### 5.1 用法

```bash
kb batch_store [options]
```

### 5.2 参数

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--file`, `-f` | 是 | JSONL 文件路径 | `/path/to/entries.jsonl` |
| `--source` | 否 | 默认来源 | `rss` |

### 5.3 文件格式

JSONL（每行一个 JSON）：
```jsonl
{"title": "Title 1", "content": "Content 1", "tags": "tag1,tag2"}
{"title": "Title 2", "content": "Content 2", "tags": "tag3"}
```

### 5.4 示例

```bash
kb batch_store --file "/tmp/entries.jsonl" --source "rss"
```

### 5.5 输出

```json
{
  "status": "ok",
  "processed": 100,
  "inserted": 95,
  "updated": 5,
  "errors": 0
}
```

## 6. config - 配置管理

### 6.1 用法

```bash
kb config [subcommand]
```

### 6.2 子命令

| 子命令 | 说明 |
|--------|------|
| `kb config show` | 显示当前配置 |
| `kb config set <key> <value>` | 设置配置 |
| `kb config mode [private/shared]` | 切换 KB 模式 |

### 6.3 示例

```bash
# 显示配置
kb config show

# 切换到共享 KB
kb config mode shared

# 设置默认加载层级
kb config set default_level 1
```

### 6.4 输出

```json
{
  "kb_mode": "private",
  "db_path": "/Users/thomas/.openclaw/agents/coding-research-partner/knowledge.db",
  "fts_weight_title": 2.0,
  "fts_weight_content": 1.0,
  "default_level": 2,
  "time_decay_lambda": 0.1
}
```

## 7. recall - Hook 自动检索（内部接口）

### 7.1 用法

```bash
kb recall --context "<对话上下文>"
```

### 7.2 参数

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--context` | 是 | 对话上下文 | `"用户问如何配置 hooks"` |
| `--limit` | 否 | 返回数量，默认 3 | `5` |

### 7.3 用途

供 `before_agent_start` hook 调用，无需用户显式触发。

### 7.4 输出

```json
{
  "injected_context": "相关知识：\n1. OpenClaw Hooks 配置指南\n2. before_agent_start 用法\n...",
  "entries_used": 3
}
```

## 8. capture - Hook 自动捕获（内部接口）

### 8.1 用法

```bash
kb capture --turn "<对话内容>"
```

### 8.2 参数

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--turn` | 是 | 对话内容 | `"用户问... Agent 回复..."` |
| `--threshold` | 否 | 捕获阈值，默认 0.7 | `0.8` |

### 8.3 用途

供 `after_turn` hook 调用，自动判断是否值得记忆。

### 8.4 输出

```json
{
  "captured": true,
  "topic_key": "openclaw-hooks-001",
  "decision": "值得记忆：新决策"
}
```

## 9. 错误码

| 错误码 | 说明 |
|--------|------|
| `E001` | 缺少必填参数 |
| `E002` | 数据库初始化失败 |
| `E003` | FTS 查询失败 |
| `E004` | 文件读取失败 |
| `E005` | JSON 解析失败 |
| `E006` | 配置错误 |

## 10. 退出码

| 退出码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1 | 一般错误 |
| 2 | 使用错误（参数错误）|
| 3 | 系统错误（数据库等）|
