# Notion Pro — 完整 Notion API 技能 (OpenClaw)

[English](./SKILL.md) | **中文**

一个生产级 Notion API 技能，内置 Python CLI 工具。不同于仅提供命令语法的基础 Notion 技能，本技能包含 **Agent 操作策略**、**自动翻页**、**递归块获取**、**429 限速自动重试** 以及完整的 API 参考 — AI Agent 高效操作 Notion 所需的一切。

## 独特优势

| 能力 | 本技能 | 基础技能 |
|---|---|---|
| Agent 操作策略（5 步工作流） | ✅ | ❌ |
| 递归块获取（`--recursive`，5 层） | ✅ | ❌ |
| 自动翻页（`--all`） | ✅ | ❌ |
| 429 限速自动重试（Retry-After） | ✅ | ❌ |
| 指定位置插入（`--after`） | ✅ | ❌ |
| API 限制速查表 | ✅ 完整 | 部分 |
| 4 种操作模式 SOP | ✅ | ❌ |
| 零依赖（仅标准库） | ✅ Python 3 | Node.js / curl |

## 配置

1. 创建 [Notion Integration](https://www.notion.so/profile/integrations) 并复制 API Key
2. 通过以下 **任一** 方式配置 Key：
   - 环境变量：`export NOTION_API_KEY="ntn_xxxxx"`
   - OpenClaw 配置：`openclaw.json` → `skills.entries.notion-pro.apiKey`
3. 将目标页面/数据库共享给你的集成（点击 "..." → "Connect to" → 你的集成名称）
4. 如果通过搜索找不到页面/数据库，说明它还没有共享给集成

## 工具：notion_api.py

**所有 Notion 操作必须通过此脚本执行**，不要直接用 curl。

```bash
python3 <SKILL_DIR>/scripts/notion_api.py <command> [options]
```

---

## 操作策略（Agent 必读）

### 任务规划流程

执行 Notion 任务时遵循此顺序：

1. **Discover** — 用 `search` 找到目标页面/数据库的 ID
2. **Inspect** — 用 `get-page` 或 `get-blocks` 了解当前结构
3. **Plan** — 确定需要的操作序列（创建/更新/追加/删除）
4. **Execute** — 分批执行，每批 ≤50 blocks（留安全余量）
5. **Verify** — 关键操作后用 `get-blocks` 验证结果

### 读取策略

- **先搜后读**：不要猜测 ID，用 search 找到确切的页面/数据库
- **递归读取嵌套内容**：`get-blocks` 只返回直接子块。如果某个 block 的 `has_children: true`，**必须用该 block 的 ID 再次调用 `get-blocks`** 来获取嵌套内容。或使用 `--recursive` 自动遍历。
- **分页处理**：如果返回 `has_more: true`，需要多次调用。使用 `--all` 可自动翻页。

### 写入策略

- **长文拆段**：单个 rich_text 块的 `text.content` 上限 **2000 字符**。超长内容必须拆成多个段落块
- **批量写入**：一次 `append-blocks` 调用最多 **100 个块元素**。超过时分多次调用
- **替换内容 = 删除 + 追加**：Notion API **没有**"替换块内容"的端点。要替换某段内容，先用 `delete-block` 删旧块，再用 `append-blocks` 在正确位置追加新块
- **插入位置**：`append-blocks` 默认追加到末尾。如需在特定位置插入，使用 `--after` 参数指定前一个块的 ID

### 数据库写入策略

- **Schema-First**：创建页面前，先用 `get-page` 或 `query-database` 查看数据库的 property schema，确保 properties JSON 格式匹配
- **Title 必填**：每个数据库必须有且仅有一个 `title` 类型属性，创建页面时必须提供
- **属性名精确匹配**：property 名称区分大小写和空格

---

## API 限制速查

| 限制项 | 数值 |
|---|---|
| 速率限制 | **3 请求/秒**（平均），超限返回 429 |
| 请求 payload 最大 | **500 KB** |
| 单次 payload 最大块数 | **1000 个块** |
| 单个数组（blocks/rich_text）最大元素 | **100 个** |
| rich_text `text.content` | **2000 字符** |
| rich_text `text.link.url` | **2000 字符** |
| URL 属性 | **2000 字符** |
| multi_select 选项 | **100 个** |
| relation 关联页面 | **100 个** |
| 数据库 schema 建议大小 | **≤ 50 KB** |
| 分页默认/最大 page_size | **100** |

**429 处理**：遇到速率限制时，脚本自动读取 `Retry-After` header 等待后重试（最多 3 次）。手动批量操作之间加 300-500ms 间隔。

---

## 命令参考

### 搜索

```bash
python3 scripts/notion_api.py search --query "关键词"
python3 scripts/notion_api.py search --query "关键词" --filter page
python3 scripts/notion_api.py search --query "关键词" --filter database --page-size 20

# 翻页（用上次返回的 next_cursor）
python3 scripts/notion_api.py search --query "关键词" --start-cursor "xxx"

# 自动获取全部结果（自动翻页，注意大量数据耗时较长）
python3 scripts/notion_api.py search --query "关键词" --all
```

### 读取页面

```bash
# 获取页面元数据（properties、parent、URL 等）
python3 scripts/notion_api.py get-page --page-id "xxx-xxx"

# 获取页面内容（blocks）— 注意检查 has_children 递归获取嵌套块
python3 scripts/notion_api.py get-blocks --block-id "xxx-xxx"

# 递归获取完整页面（自动展开所有嵌套块，最大深度 5 层）
python3 scripts/notion_api.py get-blocks --block-id "xxx-xxx" --recursive

# 翻页
python3 scripts/notion_api.py get-blocks --block-id "xxx-xxx" --start-cursor "xxx"
```

### 查询数据库

```bash
# 获取所有行
python3 scripts/notion_api.py query-database --database-id "xxx"

# 带过滤
python3 scripts/notion_api.py query-database \
  --database-id "xxx" \
  --filter '{"property": "Status", "select": {"equals": "Active"}}'

# 带排序
python3 scripts/notion_api.py query-database \
  --database-id "xxx" \
  --sorts '[{"property": "Date", "direction": "descending"}]'

# 复合过滤（AND/OR）
python3 scripts/notion_api.py query-database \
  --database-id "xxx" \
  --filter '{"and": [{"property": "Status", "select": {"equals": "Active"}}, {"property": "Priority", "select": {"equals": "High"}}]}'

# 翻页
python3 scripts/notion_api.py query-database --database-id "xxx" --start-cursor "xxx"

# 自动获取全部结果
python3 scripts/notion_api.py query-database --database-id "xxx" --all
```

### 创建页面

```bash
# 在数据库中创建（注意 properties 必须匹配 schema）
python3 scripts/notion_api.py create-page \
  --parent-id "database_id" \
  --parent-type database \
  --properties '{"Name": {"title": [{"text": {"content": "新条目"}}]}}'

# 在页面下创建子页面（带内容）
python3 scripts/notion_api.py create-page \
  --parent-id "page_id" \
  --parent-type page \
  --properties '{"title": {"title": [{"text": {"content": "子页面标题"}}]}}' \
  --children '[{"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Hello"}}]}}]'
```

### 更新页面属性

```bash
python3 scripts/notion_api.py update-page \
  --page-id "xxx" \
  --properties '{"Status": {"select": {"name": "Done"}}}'
```

### 追加内容块

```bash
# 追加到末尾（默认）
python3 scripts/notion_api.py append-blocks \
  --block-id "page_id" \
  --children '[{"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "标题"}}]}}, {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "正文内容"}}]}}]'

# 在指定块之后插入
python3 scripts/notion_api.py append-blocks \
  --block-id "page_id" \
  --after "target_block_id" \
  --children '[{"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "插入到指定位置"}}]}}]'
```

### 删除块

```bash
python3 scripts/notion_api.py delete-block --block-id "block_id"
```

---

## Block 类型参考

### 常用 block（可创建）

```json
// 段落
{"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "文本"}}]}}

// 标题
{"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": "一级标题"}}]}}
{"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "二级标题"}}]}}
{"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"text": {"content": "三级标题"}}]}}

// 可切换标题（点击展开/折叠子内容）
{"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "标题"}}], "is_toggleable": true}}

// 列表
{"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "项目"}}]}}
{"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"text": {"content": "项目"}}]}}

// 待办
{"object": "block", "type": "to_do", "to_do": {"rich_text": [{"text": {"content": "任务"}}], "checked": false}}

// 引用
{"object": "block", "type": "quote", "quote": {"rich_text": [{"text": {"content": "引文"}}]}}

// 标注（callout）
{"object": "block", "type": "callout", "callout": {"rich_text": [{"text": {"content": "重要提示"}}], "icon": {"type": "emoji", "emoji": "⚠️"}}}

// 代码
{"object": "block", "type": "code", "code": {"rich_text": [{"text": {"content": "print('hello')"}}], "language": "python"}}

// 分割线
{"object": "block", "type": "divider", "divider": {}}

// Toggle（可展开）
{"object": "block", "type": "toggle", "toggle": {"rich_text": [{"text": {"content": "可展开标题"}}]}}

// 书签
{"object": "block", "type": "bookmark", "bookmark": {"url": "https://example.com"}}

// 公式
{"object": "block", "type": "equation", "equation": {"expression": "E = mc^2"}}
```

### 支持嵌套子块的类型

以下块类型可以包含子块（通过 `append-blocks` 向其追加子内容）：
- paragraph, bulleted_list_item, numbered_list_item, to_do
- quote, callout, toggle
- heading_1/2/3（仅当 `is_toggleable: true` 时）
- column, synced_block, table

### 不支持通过 API 创建/修改的类型

- `link_preview` — 只读
- `meeting_notes` / `transcription` — 只读
- `synced_block` — 不支持更新内容
- `template` — 已废弃创建功能
- `table` 的 `table_width` — 创建后不可修改

---

## Rich Text 高级格式

```json
// 加粗 + 斜体
{"text": {"content": "重点"}, "annotations": {"bold": true, "italic": true}}

// 代码样式
{"text": {"content": "variable"}, "annotations": {"code": true}}

// 带链接
{"text": {"content": "点击这里", "link": {"url": "https://example.com"}}}

// 颜色（文字/背景）
{"text": {"content": "彩色"}, "annotations": {"color": "red"}}
// 可用颜色: default, gray, brown, orange, yellow, green, blue, purple, pink, red
// 背景色: gray_background, brown_background, ..., red_background

// 提及页面
{"type": "mention", "mention": {"type": "page", "page": {"id": "page-id"}}}

// 提及日期
{"type": "mention", "mention": {"type": "date", "date": {"start": "2026-03-22"}}}
```

---

## Property 类型参考

```json
{"title": [{"text": {"content": "..."}}]}           // Title（必填，每库唯一）
{"rich_text": [{"text": {"content": "..."}}]}        // Rich text
{"select": {"name": "Option"}}                        // Select
{"multi_select": [{"name": "A"}, {"name": "B"}]}     // Multi-select
{"date": {"start": "2026-01-15"}}                     // Date
{"date": {"start": "2026-01-15", "end": "2026-01-20"}} // Date range
{"checkbox": true}                                     // Checkbox
{"number": 42}                                         // Number
{"url": "https://..."}                                 // URL
{"email": "a@b.com"}                                   // Email
{"phone_number": "+86-138-xxxx-xxxx"}                  // Phone
{"relation": [{"id": "page_id"}]}                     // Relation
{"status": {"name": "In Progress"}}                   // Status
{"people": [{"id": "user_id"}]}                       // People
```

**只读属性**（API 不可写）: `formula`, `rollup`, `created_time`, `created_by`, `last_edited_time`, `last_edited_by`, `unique_id`

---

## 常见操作模式

### 模式 1: 知识库批量填充

场景：向 Notion 知识库（数据库）批量写入内容

```
1. search → 找到数据库 ID
2. query-database → 获取 schema 和已有条目（避免重复）
3. 对每个条目:
   a. create-page → 创建页面（properties 匹配 schema）
   b. append-blocks → 分批追加内容（每批 ≤50 块）
   c. 批次间 sleep 300ms 避免 429
4. 完成后 query-database 验证条目数
```

### 模式 2: 页面内容更新

场景：替换或补充已有页面的部分内容

```
1. get-blocks → 读取当前所有块及 ID
2. 找到需要替换的块 ID 范围
3. delete-block → 逐个删除旧块
4. append-blocks → 在正确位置追加新内容
注意: 没有"替换块"API，只能删后追加
```

### 模式 3: 递归读取完整页面

场景：获取包含嵌套 toggle/list 的完整页面内容

```
# 推荐: 一条命令递归展开（最大深度 5 层）
get-blocks --block-id <page_id> --recursive

# 手动逐层（如果只需要特定子树）:
1. get-blocks --block-id <page_id> → 获取顶层块
2. 对返回结果中 has_children: true 的块:
   get-blocks --block-id <block_id> → 获取子块
3. 递归直到所有层级读完
注意: --recursive 会自动处理分页和速率限制（350ms 间隔）
```

### 模式 4: 数据库条件查询 + 批量更新

场景：筛选特定条目并批量修改属性

```
1. query-database --filter '...' → 获取匹配的页面 ID 列表
2. 对每个页面 ID:
   update-page --page-id <id> --properties '{"Status": {"select": {"name": "Done"}}}'
3. 批次间 sleep 300ms
```

---

## API 版本注意事项 (2025-09-03)

- **Databases → Data Sources**：查询使用 `/data_sources/` 端点。脚本自动处理两种端点。
- **两个 ID**：每个数据库有 `database_id` 和 `data_source_id`
  - `database_id`：创建页面时用 (`parent: {"database_id": "..."}`)
  - `data_source_id`：查询时用 — 脚本自动处理两者
- **速率限制**：~3 请求/秒平均
- **Linked Databases**：API 不支持操作关联数据库的数据源，必须找到原始数据源
- **Wiki Databases**：只能在 Notion UI 中创建，API 可读但有限

---

## ⚠️ 重要提醒

- **绝不混淆 Notion 和飞书**。Notion → `api.notion.com`; 飞书 → `open.feishu.cn`。它们是完全不同的平台。
- 用户说"知识库"时默认指 Notion（除非上下文明确提到飞书）。
- **空字符串无效**：要清空属性值，用 `null` 而非 `""`。
- **ID 格式宽松**：API 接受带或不带连字符的 UUID。
- **分页注意**：search 和 query-database 默认最多返回 100 条。如果数据量大，必须通过 `start_cursor` 翻页或使用 `--all`。
