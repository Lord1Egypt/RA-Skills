# Markdown → Notion Sync Skill

将 Markdown 文件同步到 Notion 数据库页面。支持加粗、斜体、代码、链接、表格、callout、引用、公式等富文本格式，并提供 upsert 语义（同标题先删后插，自动去重）。

---

## ⚙️ 快速配置（使用前必读）

编辑 `scripts/sync.py` 开头的配置区：

```python
# ============ 配置区（修改这里） ============
NOTION_KEY = "your-notion-api-token-here"
DB_ID = "your-database-id-here"
OBSIDIAN_ROOT = "/path/to/your/obsidian/vault"
TARGET_DIRS = ["C-我的日志", "B-知识内容/论文阅读"]  # 要同步的子目录
EXCLUDE = ["README.md", "template.md"]  # 排除的文件
# ===========================================
```

**获取方式：**
- **NOTION_KEY**: Notion Integration → Settings → Integrations → 获取 Internal Integration Token
- **DB_ID**: 创建数据库后，从数据库 URL 复制（`notion.so/workspace/{DB_ID}`）
- **OBSIDIAN_ROOT**: Obsidian 仓库的根目录路径

---

## 📁 文件结构

```
obsidian-notion/
├── SKILL.md          # 本文档
├── scripts/
│   └── sync.py       # 同步脚本（主程序）
└── README.md         # 使用说明（可选）
```

---

## 🗄️ Notion 数据库要求

### 必填属性

数据库需包含以下 5 个属性（名称必须完全一致）：

| 属性名 | 类型 | 说明 |
|--------|------|------|
| 名称 | title | 页面标题 |
| 日期 | date | YYYY-MM-DD 格式 |
| 笔记分类 | select | 单选分类 |
| 主要标签 | multi_select | 多选标签 |
| 整理状态 | select | 单选状态 |

### 属性选项参考

**笔记分类选项：**
- A-任务管理
- B-知识内容/论文阅读
- B-知识内容/我的思考笔记
- B-知识内容/课程学习
- C-我的日志

**主要标签选项：**
- paper/待读、paper/阅读中、paper/已读完
- task/科研、task/论文、task/生活

**整理状态选项：**
- 待整理、已整理、已归档

---

## 📝 Markdown → Notion Block 映射表

### 1. 行内样式（Rich Text）

Notion rich_text 结构（annotations 与 text **同级**，不是嵌套！）：

```json
// 加粗
{"type": "text", "text": {"content": "加粗文字"}, "annotations": {"bold": true}}

// 斜体
{"type": "text", "text": {"content": "斜体文字"}, "annotations": {"italic": true}}

// 行内代码
{"type": "text", "text": {"content": "代码"}, "annotations": {"code": true}}

// 链接
{"type": "text", "text": {"content": "链接"}, "text": {"link": {"url": "https://..."}}}
```

**自动识别规则（正则优先级）：**
```
`**bold**` → bold=true
`*italic*` → italic=true
`` `code` `` → code=true
`$公式$` → code=true
`[文字](url)` → link
```

### 2. 基础块

| Markdown | Notion Block |
|---|---|
| `# 标题` | heading_1 |
| `## 标题` | heading_2 |
| `### 标题` | heading_3 |
| `#### 标题` | heading_4 |
| `##### 文字` | paragraph + bold（非标题块） |
| `---` | divider |
| 普通段落 | paragraph |

### 3. 列表

| Markdown | Notion Block |
|---|---|
| `- 项目` | bulleted_list_item |
| `1. 项目` | numbered_list_item |
| 嵌套列表 | children 内嵌 list_item（最多2层） |

### 4. 代码块

```json
{
  "object": "block",
  "type": "code",
  "code": {
    "rich_text": [{"type": "text", "text": {"content": "code"}}],
    "language": "python"
  }
}
```

**语言标准化映射：** `py`→`python`, `js`→`javascript`, `c++`→`cpp`, `sh`→`bash`, `yml`→`yaml` 等。不在白名单内的语言统一映射为 `plain text`。

### 5. 表格（Notion 原生）

```json
{
  "object": "block",
  "type": "table",
  "table": {
    "table_width": 3,
    "has_column_header": true,
    "has_row_header": false,
    "children": [
      {
        "object": "block",
        "type": "table_row",
        "table_row": {
          "cells": [
            [{"type": "text", "text": {"content": "列1"}}],
            [{"type": "text", "text": {"content": "列2"}}],
            [{"type": "text", "text": {"content": "列3"}}]
          ]
        }
      }
    ]
  }
}
```

### 6. Callout

```json
{
  "object": "block",
  "type": "callout",
  "callout": {
    "rich_text": [...],
    "icon": {"emoji": "💡"},
    "color": "blue_background"
  }
}
```

**Markdown 语法：** `> [!info] 标题` → 多行 callout body

**颜色映射：**
| 类型 | color | emoji |
|---|---|---|
| info | blue_background | ℹ️ |
| tip | green_background | 💡 |
| success | green_background | ✅ |
| warning | yellow_background | ⚠️ |
| danger/error | red_background | 🚨 |
| abstract | purple_background | 📋 |
| note | gray_background | 📝 |

> [!note]
> `[!type]` 标签不会显示在 callout 正文中，只用于确定类型

### 7. 引用

```json
{
  "object": "block",
  "type": "quote",
  "quote": {"rich_text": [...]}
}
```

**Markdown 语法：** `> 引用文字`

### 8. 公式

| Markdown | Notion Block |
|---|---|
| `$$E=mc^2$$` | equation block |
| `$公式$` | code 格式 rich_text |

```json
{"object": "block", "type": "equation", "equation": {"expression": "E=mc^2"}}
```

---

## 🔄 同步策略：Upsert

**同名页面先删后插**，确保数据库中每个标题只有最新版本。

流程：
1. 查询数据库所有页面，构建 title → id 缓存
2. 对每个 Markdown 文件：
   - 如果标题已存在 → 移到垃圾箱（in_trash: true）
   - 创建新页面，填入所有 blocks

---

## 🚀 使用方法

```bash
# 1. 编辑配置
vim scripts/sync.py  # 修改 NOTION_KEY, DB_ID, OBSIDIAN_ROOT

# 2. 运行同步
python3 scripts/sync.py

# 3. 查看结果
# Found 51 files
# Progress: 20/51 | Success: 20 | Failed: 0
# Progress: 40/51 | Success: 38 | Failed: 2
# === DONE ===
# Total: 51, Success: 49, Failed: 2
```

---

## ⚠️ 常见错误处理

| 错误信息 | 原因 | 解决 |
|---|---|---|
| `table_width should be defined` | table 缺 `table_width` | 必须指定列数 |
| `rich_text[...].annotations should be an object` | annotations 嵌套在 text 内 | 修正为同级结构 |
| `language should be one of "abap"...` | 语言不在白名单 | 映射到 `plain text` |
| `body.children.length should be ≤ 100` | 超过 block 限制 | 分批创建 |
| `Can't edit block that is archived` | 页面已在垃圾箱 | 跳过或先恢复 |
| `Invalid URL for link` | 链接格式错误 | 确保以 `http://`/`https://` 开头 |

---

## 📋 预处理规则

1. **清理 frontmatter**：`re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)`
2. **日期验证**：必须是 `YYYY-MM-DD`，否则使用默认值
3. **代码块截断**：单个 rich_text 内容不超过 2000 字符
4. **空文件跳过**：正文 blocks 为空时跳过，不创建页面
5. **HTML 标签清理**：`re.sub(r'<[^>]+>', '', text)`
