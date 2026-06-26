---
name: inspiration-material-organizer
description: 将聊天记录、截图文字、链接和随手记等碎片灵感整理为可检索知识库。支持快速收录、智能分类、语义检索和灵感反刍。用户提到灵感整理、素材归档、笔记分类、找不到收藏内容、旧素材回顾时使用。
---

# Inspiration Material Organizer

## 适用场景

当用户提出以下需求时启用：

- 整理分散的灵感素材
- 把截图文字或链接沉淀成卡片
- 给素材自动打标签并分组归档
- 通过关键词或模糊描述找历史素材
- 定期回顾旧素材，防止遗忘

## 默认策略

1. 使用本技能的 Python 脚本作为唯一实现入口。
2. 所有素材落到本地 JSON 知识库，保证可检索和可迁移。
3. 分类使用外部规则文件（稳定、可解释），可直接编辑主题与关键词。
4. 检索使用关键词与简单语义近似（token overlap），避免外部依赖。

## 工作流

复制并跟踪以下清单：

```text
任务进度:
- [ ] 步骤1: 收录素材为标准卡片
- [ ] 步骤2: 自动分类并补充标签
- [ ] 步骤3: 检索验证可用性
- [ ] 步骤4: 反刍输出回顾列表
```

### 步骤1：快速收录

命令：

```bash
python .cursor/skills/inspiration-material-organizer/scripts/organizer.py capture --text "内容" --source "chat"
```

支持输入：

- `--text` 文字内容（聊天片段、随手记、OCR 结果）
- `--url` 链接（可选）
- `--title` 标题（可选，不传则自动生成）
- `--source` 来源：`chat` / `screenshot` / `link` / `note` / `other`

### 步骤2：智能分类

命令：

```bash
python .cursor/skills/inspiration-material-organizer/scripts/organizer.py classify --ids all
```

效果：

- 自动按 `config/topic_rules.json` 分配主题分类
- 自动追加关键词标签
- 按主题写入分组字段

### 步骤3：语义检索

命令：

```bash
python .cursor/skills/inspiration-material-organizer/scripts/organizer.py search --query "我记得有个关于内容选题的方法"
```

输出：

- 按相关性排序的历史素材卡片
- 显示命中原因（标签/关键词）

### 步骤4：灵感反刍

命令：

```bash
python .cursor/skills/inspiration-material-organizer/scripts/organizer.py ruminate --topic 写作 --count 5
```

可选：

- `--date-from YYYY-MM-DD`
- `--date-to YYYY-MM-DD`
- `--topic 主题`
- `--count 数量`

## 数据文件

默认数据库位置：

` .cursor/skills/inspiration-material-organizer/data/inspirations.json `

可通过环境变量覆盖：

`INSPIRATION_DB_PATH`

默认分类规则位置：

` .cursor/skills/inspiration-material-organizer/config/topic_rules.json `

可通过环境变量覆盖：

`INSPIRATION_TOPIC_RULES_PATH`

## 附加资源

- 详细字段说明与分类规则见 [reference.md](reference.md)
- 常见命令与场景示例见 [examples.md](examples.md)
