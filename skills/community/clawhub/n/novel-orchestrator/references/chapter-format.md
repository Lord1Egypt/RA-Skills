# 章节文件规范

## 命名规则

### 章节文件

格式：`第XXX章.md`

示例：
- `第001章.md`
- `第013章.md`
- `第128章.md`

### 章节元数据

每个章节文件头部必须包含 YAML frontmatter：

```markdown
---
title: "章节标题"
chapter: 1
word_count: 3500
status: draft|review|approved
writer: writer-agent-id
checker: checker-agent-id
created_at: 2026-03-21
updated_at: 2026-03-21
---

正文内容...
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| title | 是 | 章节标题 |
| chapter | 是 | 章节序号 |
| word_count | 是 | 字数（用脚本统计） |
| status | 是 | draft/review/approved |
| writer | 否 | 写作 agent ID |
| checker | 否 | 审稿 agent ID |
| created_at | 是 | 创建日期 |
| updated_at | 是 | 最后修改日期 |

## 存储位置

章节文件统一放在：`agent/writer/chapters/`

## 版本控制

- 初稿：直接写入
- 返修：编辑原文件，更新 `updated_at` 和 `word_count`
- 审稿通过：修改 `status` 为 `approved`
