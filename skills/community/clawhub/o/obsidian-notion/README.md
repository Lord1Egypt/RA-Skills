# Markdown → Notion（Obsidian 版）（通用版）

将 Obsidian Markdown 笔记同步到 Notion 数据库，支持富文本、表格、callout、引用、公式等格式。

## 文件结构

```
markdown-to-notion/
├── SKILL.md      # 完整规范文档（block 映射表 + API 示例）
├── scripts/
│   └── sync.py  # 同步脚本
└── README.md     # 本文件
```

## 快速开始

### 1. 配置

编辑 `scripts/sync.py` 开头的 `CONFIG` 字典：

```python
CONFIG = {
    "NOTION_KEY": "ntn_xxxxxxxxxxxx",     # 你的 Notion API Token
    "DB_ID": "xxxxxxxx-xxxx-xxxx",        # 你的数据库 ID
    "OBSIDIAN_ROOT": "/path/to/vault",    # Obsidian 仓库路径
    "TARGET_DIRS": ["日记", "笔记"],       # 要同步的子目录
    "EXCLUDE": ["README.md"],
    "PROPERTY_MAP": {
        "title": "名称",
        "date": "日期",
        "category": "分类",
        "tags": "标签",
        "status": "状态"
    },
    "DEFAULT_DATE": "2026-01-01",
    "DEFAULT_CATEGORY": "未分类",
    "DEFAULT_STATUS": "已整理",
}
```

### 2. 运行

```bash
python3 scripts/sync.py
```

### 3. 输出示例

```
Found 51 files
Querying existing pages...
Found 0 existing pages
Progress: 20/51 | Success: 20 | Failed: 0 | Empty: 0
Progress: 40/51 | Success: 38 | Failed: 2 | Empty: 0
=== DONE ===
Total: 51, Success: 49, Failed: 2, Empty: 2
```

## 数据库要求

数据库需包含以下属性（通过 `PROPERTY_MAP` 映射）：

| 属性 | 类型 | 说明 |
|------|------|------|
| 名称 | title | 笔记标题 |
| 日期 | date | YYYY-MM-DD |
| 分类 | select | 分类 |
| 标签 | multi_select | 多选标签 |
| 状态 | select | 整理状态 |

## 支持的 Markdown 格式

| 语法 | Notion |
|------|--------|
| `**bold**` | 加粗 |
| `*italic*` | 斜体 |
| `` `code` `` | 行内代码 |
| `$公式$` | 行内公式（代码格式） |
| `$$公式$$` | 独立公式块 |
| `# ## ### ####` | h1~h4 |
| `##### 文字` | 加粗段落 |
| `- item` | 无序列表 |
| `1. item` | 有序列表 |
| `> text` | 引用块 |
| `> [!info] text` | Callout |
| `---` | 分隔线 |
| ` ```code``` ` | 代码块 |
| 表格 | 原生表格 block |

## 同步策略

**Upsert**（同名先删后插）：每次运行，同名笔记会先删除旧版再插入新版，数据库始终只有最新内容。
