---
name: notion
description: Notion API for creating and managing pages, databases, and blocks. Also includes 想法点子库（💡）持久化 workflow，当用户说"入库"、"记录这个想法"、"这个先记下来"、"持久化这个"时触发。
homepage: https://developers.notion.com
metadata: {"clawdbot":{"emoji":"📝"}}
---

# notion

Use the Notion API to create/read/update pages, databases, and blocks.

## Setup

```bash
mkdir -p ~/.config/notion
echo "ntn_your_key_here" > ~/.config/notion/api_key
```
Integration API key starts with `ntn_` or `secret_`. Share target pages/databases with your integration (click "..." → "Connect to" → your integration name).

## API Version Decision Tree

> **Critical**: Wrong version = silent failures.

| Operation | Version | Why |
|---|---|---|
| Query data source | `2025-09-03` | Newer endpoint |
| Search / Get page | `2025-09-03` | Read operations |
| Create/update pages | `2022-06-28` | More reliable for property writes |
| Create database | `2022-06-28` | 2025-09-03 silently drops custom properties |
| Update database schema | `2022-06-28` | Same reason |

**Always include** `Notion-Version` header. Default in this skill: `2025-09-03`.

## Quick Reference Cheatsheet

```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)

# Search
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "keywords"}'

# Get page
curl -s "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03"

# Query database (newer endpoint, use data_source_id)
curl -s -X POST "https://api.notion.com/v1/data_sources/{data_source_id}/query" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"sorts": [{"property": "创建时间", "direction": "descending"}], "page_size": 20}'

# Create page (use database_id as parent, version 2022-06-28)
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"parent": {"database_id": "xxx"}, "properties": {"Name": {"title": [{"text": {"content": "Title"}}]}}}'

# Update page properties
curl -s -X PATCH "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"Status": {"select": {"name": "Done"}}}}'
```

**Parse response (Python):**
```python
import subprocess, json
result = subprocess.run(['curl', '-s', ...], capture_output=True, text=True)
data = json.loads(result.stdout)
page_id = data.get('id')
error = data.get('message')  # if 'object' == 'error'
```

---

## 💡 想法点子库

**数据库 ID:** `339d8e39-9e68-814b-8fc9-c06adfb3ae00`
**里程碑数据库 ID:** `339d8e39-9e68-8130-932c-ecf46af154b5`
**父页面:** Winnie (`321d8e39-9e68-8037-9c2f-d55fd4e9a54c`)

### 数据库字段

| 字段 | 类型 | 说明 |
|---|---|---|
| 名称 | title | 提纯后的标题，≤20字 |
| 想法摘要 | rich_text | 核心内容摘要 |
| 决策结论 | rich_text | 最终结论或后续行动（暂无填"待定"） |
| 来源 | select | 临时想法 / 项目相关 / 系统讨论 |
| 相关项目 | rich_text | 关联项目，可空 |
| 标签 | multi_select | 自由标签 |
| 状态 | select | 待实现 / 进行中 / **已规划** / **执行中** / 已实现 / 已归档 |
| 规划内容 | rich_text | 想法→计划的推导过程（转为"已规划"时填写） |
| 相关里程碑 | relation | 反向关联里程碑条目 |
| 里程碑数 | number | 关联里程碑计数 |
| 重要性 | select | 高 / 中 / 低 |
| 创建时间 | date | 消息时间戳（ISO 格式） |

### 里程碑数据库字段

| 字段 | 类型 |
|---|---|
| 里程碑标题 | title |
| 所属想法 | relation → 想法点子库 |
| 处理过程 | rich_text |
| 决策记录 | rich_text |
| 产物链接 | url |
| 状态 | select（进行中 / 已完成） |
| 创建时间 | date |

### 入库流程（触发词: "入库"/"记录这个想法"/"持久化这个"）

1. 从消息提取：时间戳 → 标题（≤20字） → 摘要 → 决策结论 → 来源/状态/重要性
2. 组装 JSON（见下方模板）
3. **调用确认脚本**：`python3 ~/.openclaw/skills/notion/scripts/notion-write-idea.py create < idea.json`
4. 脚本展示内容 → 用户输入 `y` 确认 → 才写入 Notion
5. 写入后脚本自动验证并返回 Notion 页面链接

### 入库 API

**不直接调 curl**，统一走脚本确保确认环节：

```bash
cat > /tmp/idea.json << 'EOF'
{
  "名称": "无头服务器网站登录解法",
  "想法摘要": "agent-browser在无头服务器无法登录需验证码网站。解法：Cookie导入、Xvfb虚拟显示器、本地登录导出session。",
  "决策结论": "优先试方案1（Cookie导入），最可行。",
  "来源": "临时想法",
  "相关项目": "agent-browser",
  "标签": ["服务器部署", "Cookie导入"],
  "状态": "待实现",
  "重要性": "中",
  "创建时间": "2026-04-04T22:38:00+08:00"
}
EOF

python3 ~/.openclaw/skills/notion/scripts/notion-write-idea.py create < /tmp/idea.json
```

### 想法→计划 转化流程

**触发词:** "转计划"、"开始规划"、"这是个好想法"

1. 读取想法页面的 `page_id`
2. 展示并确认"规划内容"（想法→计划的推导）
3. 更新想法状态为"已规划"（`规划内容`字段填入推导）
4. 用户确认后才写入

### 创建里程碑（触发词: "添加里程碑"/"新建里程碑"）

```bash
cat > /tmp/milestone.json << 'EOF'
{
  "里程碑标题": "方案1测试：Cookie导入",
  "所属想法ID": "想法页面的page_id",
  "处理过程": "测试EditThisCookie导出Chrome Cookie，导入agent-browser",
  "决策记录": "Cookie导入可行，但B站登录态有效期仅24h，需定期刷新",
  "产物链接": "https://github.com/...",
  "状态": "进行中",
  "创建时间": "2026-04-05T13:00:00+08:00"
}
EOF

python3 ~/.openclaw/skills/notion/scripts/notion-write-milestone.py create < /tmp/milestone.json
```

### 更新状态（触发词）

| 触发词 | 操作 |
|---|---|
| "已完成"/"已实现" | 状态→已实现 |
| "归档"/"不要了" | 状态→已归档 |
| "进行中" | 状态→进行中 |
| "转计划"/"开始规划" | 状态→已规划 + 填写规划内容 |
| "添加里程碑" | 在里程碑库创建条目 |

### 查询所有想法（按时间倒序）

```bash
curl -s -X POST "https://api.notion.com/v1/data_sources/339d8e39-9e68-814b-8fc9-c06adfb3ae00/query" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"sorts": [{"property": "创建时间", "direction": "descending"}], "page_size": 20}'
```

### 查询某想法的里程碑

```bash
curl -s -X POST "https://api.notion.com/v1/data_sources/339d8e39-9e68-8130-932c-ecf46af154b5/query" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"property": "所属想法", "relation": {"contains": "想法page_id"}}}'
```

---

## Operations

### Search pages and data sources

```bash
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "keywords", "filter": {"value": "page", "property": "object"}}'
```

### Get page

```bash
curl -s "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03"
```

### Get page blocks

```bash
curl -s "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03"
```

### Create database

```bash
curl -s -X POST "https://api.notion.com/v1/databases" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"type": "page_id", "page_id": "xxx"},
    "title": [{"text": {"content": "Database Title"}}],
    "properties": {
      "Name": {"title": {}},
      "Status": {"select": {"options": [{"name": "Todo"}, {"name": "Done"}]}},
      "Date": {"date": {}}
    }
  }'
```

### Add blocks to page

```bash
curl -s -X PATCH "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"children": [{"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Text"}}]}}]}'
```

---

## Property Types

| Type | Format |
|---|---|
| Title | `{"title": [{"text": {"content": "..."}}]}` |
| Rich text | `{"rich_text": [{"text": {"content": "..."}}]}` |
| Select | `{"select": {"name": "Option"}}` |
| Multi-select | `{"multi_select": [{"name": "A"}, {"name": "B"}]}` |
| Date | `{"date": {"start": "2024-01-15"}}` |
| Checkbox | `{"checkbox": true}` |
| Number | `{"number": 42}` |
| URL | `{"url": "https://..."}` |
| Relation | `{"relation": [{"id": "page_id"}]}` |

---

## Key Differences (2025-09-03 vs 2022-06-28)

- **Databases → Data Sources**: Query uses `/data_sources/` endpoint; create uses `/databases`
- **Two IDs**: Each database has `database_id` (for creating pages) and `data_source_id` (for querying)
- **Creating databases**: Only `2022-06-28` works reliably — `2025-09-03` silently drops custom properties
- **Creating pages**: Either version works, but `2022-06-28` is more predictable

---

## Error Handling

```python
import subprocess, json

def notion_req(method, endpoint, body=None, version="2025-09-03"):
    key = open("/root/.config/notion/api_key").read().strip()
    cmd = ["curl", "-s", "-X", method,
           f"https://api.notion.com/v1/{endpoint}",
           "-H", f"Authorization: Bearer {key}",
           "-H", f"Notion-Version: {version}",
           "-H", "Content-Type: application/json"]
    if body:
        import json
        cmd += ["-d", json.dumps(body)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(r.stdout)
    if data.get("object") == "error":
        raise Exception(f"Notion API error {data.get('code')}: {data.get('message')}")
    return data
```

Common error codes:
- `object_not_found`: 页面/数据库 ID 不存在或无权访问
- `validation_error`: 属性格式错误，检查 property type 是否匹配
- `restricted_resource`: 页面未分享给 integration
- `rate_limited`: 限速，等 1 秒重试

## Notes

- IDs are UUIDs with or without dashes (both work)
- Rate limit: ~3 req/s，平均值，突发会限速
- API 无法设置数据库视图筛选器（UI 操作）
- 创建数据库时用 `is_inline: true` 可嵌入页面
