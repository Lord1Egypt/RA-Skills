---
name: paper-management-system
description: 文献管理系统 - 自动化PDF文献索引、搜索、AI提炼工具。当用户需要管理PDF文献、自动索引、搜索文献、提取元数据时激活。
metadata:
  {
    "openclaw": {
      "emoji": "📚",
      "tags": ["pdf", "papers", "research", "academic", "indexing"]
    }
  }
---

# Paper Management System

文献管理系统 - 自动化 PDF 文献管理工具（v2.0）

## 功能特性

- 自动索引：扫描 PDF，提取元数据
- 智能搜索：按关键词/年份/作者搜索
- AI 提炼：生成结构化摘要
- 自动重命名：`作者_年份_关键词.pdf`
- 增量处理 + Hash 去重
- 飞书通知（需 feishu-relay）

## 所需环境变量

| 变量名 | 必须 | 说明 |
|--------|------|------|
| `PAPERMGR_PAPERS_DIR` | 否 | PDF 存储目录（默认 `./papers`） |
| `PAPERMGR_DOWNLOADS_DIR` | 否 | 下载目录（默认 `./downloads`） |
| `PAPERMGR_DATABASE_PATH` | 否 | 数据库路径（默认 `./data/index.db`） |
| `PAPERMGR_AI_ENABLED` | 否 | 启用 AI（默认 false） |
| `OPENAI_API_KEY` | 否 | OpenAI API Key |

## 调用方式

### 自动（cron）

```bash
*/30 * * * * /path/to/scripts/auto_index.sh
```

### 手动

```bash
python3 scripts/paper_manager.py index    # 索引
python3 scripts/paper_manager.py rename   # 重命名
python3 scripts/paper_manager.py search <关键词>  # 搜索
python3 scripts/paper_manager.py status   # 状态
```

## 输入

- PDF 文件（放入 `downloads/` 或 `papers/` 目录）

## 输出

- SQLite 数据库（`data/index.db`）
- 重命名后的 PDF 文件
- AI 摘要（`ai_summary` 字段，可选）
- 飞书通知（可选）

## 发布信息

- 版本：v2.0.0
- 许可证：MIT
- GitHub：https://github.com/crayfish-ai/paper-management-system
