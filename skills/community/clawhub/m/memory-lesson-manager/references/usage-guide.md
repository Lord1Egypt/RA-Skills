# Memory Lesson Manager 使用指南

**版本：** 2.0.0  
**最后更新：** 2026-04-06

---

## 快速参考

| 场景 | 操作 |
|------|------|
| 命令/操作失败 | 记录到 `memory/lessons/WARM/errors/ERR-日期 - 哈希.md` |
| 用户纠正错误 | 记录到 `memory/lessons/WARM/corrections/LRN-日期 - 哈希.md` |
| 发现更好方法 | 记录到 `memory/lessons/WARM/best-practices/LRN-日期 - 哈希.md` |
| 技术选型决策 | 记录到 `memory/lessons/WARM/decisions/DEC-日期 - 哈希.md` |
| 项目启动/复盘 | 记录到 `memory/lessons/WARM/projects/PRJ-日期 - 哈希.md` |
| 重复问题≥3 次 | 使用 `extract-skill.sh` 提取为技能 |

**智能推断：**
- ✅ 类型 → 从目录推断（errors/ → ERR）
- ✅ 时间 → 自动生成（ISO-8601）
- ✅ 优先级 → 根据关键词推断（critical/error → P1）

---

## 目录结构

```
workspace/
├── memory/
│   ├── YYYY-MM-DD.md              # 每日日记
│   └── lessons/
│       ├── HOT/                   # 高频使用（≤20 条）
│       ├── WARM/                  # 按需加载（默认）
│       │   ├── errors/            # ERR-*
│       │   ├── corrections/       # LRN-*
│       │   ├── best-practices/    # LRN-*
│       │   ├── feature-requests/  # FEAT-*
│       │   ├── decisions/         # DEC-*
│       │   ├── projects/          # PRJ-*
│       │   └── people/            # PPL-*
│       └── COLD/archive/          # 90 天未用
├── state/
│   ├── session-state.md
│   └── working-buffer.md
└── skills/memory-lesson-manager/
    ├── SKILL.md
    ├── scripts/
    │   ├── init-memory-system.sh
    │   ├── validate-diary.sh
    │   ├── extract-skill.sh
    │   ├── promote-lesson.sh
    │   └── archive-cold.sh
    └── references/
        └── usage-guide.md（本文件）
```

---

## 工具脚本

### init-memory-system.sh

**功能：** 自动创建缺失的记忆文件和目录结构

**用法：**
```bash
# 初始化（首次使用）
./skills/memory-lesson-manager/scripts/init-memory-system.sh

# 预览
./skills/memory-lesson-manager/scripts/init-memory-system.sh --dry-run
```

---

### validate-diary.sh

**功能：** 检查日记质量（反思环节、内容长度等）

**参数：**
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `[日期]` | 检查指定日期 | 今日 |
| `--fix` | 自动修复 | false |
| `--strict` | 严格模式 | false |
| `--all` | 检查本周 | false |

**用法：**
```bash
# 检查今日
./skills/memory-lesson-manager/scripts/validate-diary.sh

# 检查本周
./skills/memory-lesson-manager/scripts/validate-diary.sh --all

# 自动修复
./skills/memory-lesson-manager/scripts/validate-diary.sh --fix
```

---

### extract-skill.sh

**功能：** 将学习条目提取为独立技能

**参数：**
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<名称>` | 技能名称 | - |
| `--dry-run` | 预览 | false |
| `--output-dir` | 输出目录 | ./skills |

**用法：**
```bash
./skills/memory-lesson-manager/scripts/extract-skill.sh git-auth-helper
```

---

### promote-lesson.sh

**功能：** 晋升高频条目到 HOT（7 天内≥3 次使用）

**参数：**
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `[ID]` | 指定条目 | 自动检测 |
| `--dry-run` | 预览 | false |
| `--threshold` | 次数阈值 | 3 |
| `--days` | 天数窗口 | 7 |

**用法：**
```bash
./skills/memory-lesson-manager/scripts/promote-lesson.sh
```

---

### archive-cold.sh

**功能：** 归档 90 天未用条目到 COLD

**参数：**
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--dry-run` | 预览 | false |
| `--days` | 天数阈值 | 90 |
| `--restore ID` | 恢复条目 | - |
| `--list-cold` | 列出归档 | - |

**用法：**
```bash
./skills/memory-lesson-manager/scripts/archive-cold.sh
./skills/memory-lesson-manager/scripts/archive-cold.sh --restore ERR-xxx
```

---

## ID 命名规则

**格式：** `TYPE-YYYYMMDD-XXX`

| 类型 | 前缀 | 目录 |
|------|------|------|
| 错误 | ERR | WARM/errors/ |
| 学习/纠正 | LRN | WARM/corrections/ 或 WARM/best-practices/ |
| 功能请求 | FEAT | WARM/feature-requests/ |
| 决策 | DEC | WARM/decisions/ |
| 项目 | PRJ | WARM/projects/ |
| 人员 | PPL | WARM/people/ |

---

## 状态流转

```
pending → in_progress → resolved → promoted → promoted_to_skill
```

---

## ⚠️ 迁移提示

**首次使用（推荐）：**
1. 备份：`cp -r memory memory-backup-日期`
2. 初始化：`./skills/memory-lesson-manager/scripts/init-memory-system.sh`
3. 新记录使用 WARM/ 结构，现有文件保留原位

**详细迁移指南：** 见 [references/migration-guide.md](references/migration-guide.md)

---

_规范详情：work-specs/docs/memory-system-v2-spec.md_
