# 记忆文件模板

## 用途

记忆文件用于在长篇创作过程中追踪和管理项目状态，确保创作的连贯性和一致性。

## 文件结构

```
memory/
├── memory.json                    # 主记忆文件（当前状态）
├── style-dna.json                # 风格DNA
├── active/                       # 活跃记忆
│   ├── current-plot.json        # 当前剧情状态
│   ├── active-characters.json   # 活跃人物状态
│   └── unresolved-foreshadowing.json  # 未解决伏笔
└── archive/                      # 归档记忆
    └── chapter-XX-summary.json   # 各章节摘要归档
```

## 主记忆文件字段说明

| 字段 | 说明 |
|------|------|
| project_id | 项目ID |
| project_name | 项目名称 |
| current_chapter | 当前章节号 |
| last_updated | 最后更新时间 |
| current_arc | 当前段落信息 |
| active_characters | 活跃人物状态列表 |
| unresolved_foreshadowing | 未解决的伏笔列表 |
| recent_events | 最近事件摘要 |
| style_notes | 风格备注 |
| author_notes | 作者备注 |

## 使用规范

1. 每完成一章，必须更新 `memory.json`
2. 每完成一章，创建章节摘要归档
3. 每5-10章，进行记忆压缩
4. 发现风格漂移时，更新 `style_notes`
