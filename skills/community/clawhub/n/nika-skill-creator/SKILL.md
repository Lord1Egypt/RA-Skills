---
name: nika-skill-creator
description: Create or update Nika platform skills (main doc + sub docs) that follow Nika constraints (two-level docs, @sub-doc references, no path/extension references). Use when user asks to make a Nika skill, refactor an existing one to Nika format, or validate a Nika skill draft; also useful to output documents that can be pasted into Nika.
---

# Nika Skill Creator

本技能用于在本仓库内创建/更新符合 Nika 平台约束的技能文档，并提供可复制到 Nika 的主文档与子文档内容。

重要核心：
- 本技能生成的“目标技能文档内容”必须遵循 Nika 约束（见 [nika-spec](references/nika-spec.md)）。

## 快速开始

1. 生成一个目标技能骨架（主文档 + 子文档占位）：

```bash
python3 scripts/init_nika_skill.py "你的目标技能中文名"
```

2. 校验目标技能是否满足 Nika 约束与本仓库约定：

```bash
python3 scripts/validate_nika_skill.py "skills/你的目标技能中文名"
```

## 工作流（创建/更新目标技能）

### 1) 需求澄清（先定边界）

收集并锁定：
- 目标技能用途（一句话）
- 典型触发语 3-5 条（用户会怎么说）
- 目标用户（作家/编辑/通用）
- 技能类型（写作类/工具类）
- 是否需要拆子文档：当存在可复用的长流程、清单、模板、示例时，拆到子文档

### 2) 输入契约（必要输入清单）

目标技能必须明确“必要输入内容、形式”：
- 每一项输入都要标注文件类型：设定文件 / 章节文件 / 笔记文件
- 推荐的文件名或命名模式（避免依赖用户随意命名）
- 最低内容要求（缺什么就无法执行）

模板见：[main-doc-template](references/main-doc-template.md)

### 3) 输入获取策略（先查找，找不到再问）

目标技能必须按固定优先级获取输入：
1. 优先使用对话里用户已提供或已引用的内容
2. 否则按“文件类型 + 文件名/命名模式”在设定/章节/笔记中查找
3. 找不到再向用户提问，并一次只问关键缺口

约束与注意事项见：[nika-spec](references/nika-spec.md)

### 4) 交付物契约（持久 + 临时）

目标技能必须同时定义两类交付物：
- 持久交付：要写入哪些设定文件/章节文件，文件名规则是什么，内容结构模板是什么
- 临时交付：屏幕输出哪些内容（摘要、检查结果、下一步指引、可选建议）

模板见：[main-doc-template](references/main-doc-template.md)

### 5) 子文档拆分（渐进式加载）

目标技能的主文档只保留：
- 导航与总流程
- 输入/输出契约
- 子文档索引（目标技能在 Nika 中用 `@子文档名` 引用）

子文档只放可复用的细节：
- 步骤、清单、模板、示例

子文档模板见：[sub-doc-template](references/sub-doc-template.md)

### 6) 生成与交付（仓库落盘 + 屏幕摘要）

默认交付行为：
- 在仓库中生成/更新目标技能目录与文档
- 在对话中输出：目标技能概要、子文档清单、校验结果摘要（参考 [validation-checklist](references/validation-checklist.md) 的检查维度）

### 7) 校验与迭代

完成后运行校验脚本，并把结果作为“屏幕输出交付”的一部分：

```bash
python3 scripts/validate_nika_skill.py "skills/目标技能中文名"
```

如果失败：根据错误定位修订主文档/子文档，再重复校验。

## 参考索引

- [nika-spec](references/nika-spec.md)：Nika 平台约束（目标技能必须遵循）
- [main-doc-template](references/main-doc-template.md)：目标技能主文档骨架模板
- [sub-doc-template](references/sub-doc-template.md)：目标技能子文档模板
- [validation-checklist](references/validation-checklist.md)：人工校验清单（与脚本校验对齐）
