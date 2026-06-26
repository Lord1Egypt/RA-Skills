---
name: memory-lesson-manager
description: 结构化学习记录与技能提取工具（V2.0）。用于记录错误/纠正/决策/项目/人员，支持 HOT/WARM/COLD 三层自动分层、状态恢复、技能提取。触发词：记录学习、提取技能、创建学习条目、晋升学习、归档条目。
metadata:
  version: 2.0.0
  created: 2026-04-05
  updated: 2026-04-06
  source: LRN-20260405-001
  spec: work-specs/docs/memory-system-v2-spec.md
---

# Memory Lesson Manager

结构化学习记录与技能提取系统。

## 快速参考

| 场景 | 操作 |
|------|------|
| 命令/操作失败 | 记录到 `memory/lessons/WARM/errors/ERR-*.md` |
| 用户纠正错误 | 记录到 `memory/lessons/WARM/corrections/LRN-*.md` |
| 发现更好方法 | 记录到 `memory/lessons/WARM/best-practices/LRN-*.md` |
| 技术选型决策 | 记录到 `memory/lessons/WARM/decisions/DEC-*.md` |
| 项目启动/复盘 | 记录到 `memory/lessons/WARM/projects/PRJ-*.md` |
| 重复问题≥3 次 | 使用 `extract-skill.sh` 提取为技能 |
| 7 天内使用≥3 次 | 使用 `promote-lesson.sh` 晋升到 HOT |
| 90 天未使用 | 使用 `archive-cold.sh` 归档到 COLD |

## 目录结构

```
workspace/
├── memory/
│   ├── YYYY-MM-DD.md              # 每日日记
│   ├── lessons/                   # 学习条目（三层结构）
│   │   ├── HOT/                   # 高频使用（≤20 条）
│   │   ├── WARM/                  # 按需加载（默认）
│   │   └── COLD/archive/          # 90 天未用
│   └── templates/                 # 模板文件（9 个）
├── state/                          # 状态文件（2 个）
│   ├── session-state.md
│   └── working-buffer.md
└── skills/memory-lesson-manager/
    ├── SKILL.md                   # 技能主文件
    ├── scripts/                   # 5 个工具脚本
    └── references/                # 详细文档
```

## 工具脚本

| 脚本 | 用途 |
|------|------|
| `init-memory-system.sh` | 初始化记忆系统 |
| `validate-diary.sh` | 日记质量检查 |
| `search-lessons.sh` | **语义搜索**（新增） |
| `link-diary-lessons.sh` | **自动关联日记**（新增） |
| `extract-skill.sh` | 技能提取 |
| `promote-lesson.sh` | 晋升到 HOT（引用次数≥2） |
| `archive-cold.sh` | 归档到 COLD（遗忘曲线） |

**详细文档：**
- [references/usage-guide.md](references/usage-guide.md) - 完整使用指南
- [references/usage-examples.md](references/usage-examples.md) - 使用示例
- [references/migration-guide.md](references/migration-guide.md) - 迁移指南

## ID 命名

**格式：** `TYPE-YYYYMMDD-XXXX`（日期 +4 位随机哈希）

**示例：**
- `ERR-20260406-a3f7` — 错误
- `LRN-20260406-b2c1` — 学习/纠正
- `DEC-20260406-d4e8` — 决策
- `PRJ-20260406-f5a9` — 项目
- `PPL-20260406-c6b2` — 人员

**优势：**
- ✅ 并发安全，无需查重
- ✅ 更短，易读
- ✅ 仍可按日期排序

## 状态流转

**显式状态（2 种）：**
- `active` — 活跃中（默认）
- `archived` — 已归档

**隐式状态（看文件位置）：**
- `HOT/` — 高频使用
- `WARM/` — 正常使用
- `COLD/` — 低频使用

## ⚠️ 迁移提示

**首次使用：**
1. 备份：`cp -r memory memory-backup-日期`
2. 初始化：`./skills/memory-lesson-manager/scripts/init-memory-system.sh`
3. 新记录用 WARM/，现有文件保留原位

**详细指南：** [references/migration-guide.md](references/migration-guide.md)

---

_详细文档：references/usage-guide.md_
