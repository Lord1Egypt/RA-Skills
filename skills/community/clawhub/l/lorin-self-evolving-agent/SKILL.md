---
name: self-improving-agent
description: 自我进化智能体 — 自动捕获错误+主动提炼经验+自动生成SKILL，三位一体持续进化。灵感来源：Hermes Agent skill_manage + pskoett self-improving-agent
---

# 自我进化智能体 (Self-Improving Agent)

> **三位一体**：自动捕获错误（Hook） + 主动提炼经验（Skill化） + 遗忘曲线复习（Promote）
> 
> 每一次踩坑都不会白费，每一个经验都会变成可复用的 Skill。

---

## 核心循环

```
工具调用失败/用户纠正/发现新工作流
         ↓
  ┌──────┴──────┐
  ↓             ↓
自动捕获     主动判断
(.learnings)   (Skill化)
  ↓             ↓
  ↓         是否值得固化成Skill？
  ↓             ├─ 否 → 保持原样
  ↓             └─ 是 → 创建/更新 SKILL.md
  ↓                      ↓
  ↓              是否普遍适用？
  ↓             ├─ 否 → 保持为Skill
  ↓             └─ 是 → Promote到 SOUL.md / AGENTS.md / TOOLS.md
  ↓
定期回顾
  ↓
Recurrence-Count ≥ 3 → 系统级规则
```

---

## 第一层：自动捕获（Hook层）

### 触发时机（自动，无需人工判断）

| 场景 | 自动日志 | 目标文件 |
|------|---------|---------|
| 命令失败（exit code ≠ 0） | `error-detector.sh` hook | `.learnings/ERRORS.md` |
| 工具调用异常 | Agent自觉判断 | `.learnings/ERRORS.md` |
| PostToolUse 扫描到错误模式 | hook自动注入 | `.learnings/ERRORS.md` |

### 错误检测模式（自动匹配）

```
error:, Error:, ERROR:, failed, FAILED,
command not found, No such file, Permission denied,
fatal:, Exception, Traceback, npm ERR!,
ModuleNotFoundError, SyntaxError, TypeError,
exit code, non-zero
```

**如果检测到**：自动在输出中注入提醒，建议写入 `.learnings/ERRORS.md`

---

## 第二层：主动提炼（Skill层）

### 触发时机（Agent主动判断）

| 场景 | 日志类型 | 目标 |
|------|---------|------|
| 复杂任务成功（≥5工具调用） | 经验 | → 考虑创建Skill |
| 踩坑后找到正确路径 | 错误+解决 | → 创建Skill记录坑+解法 |
| 用户纠正（"不是这样"） | 纠正 | → 记录纠正内容 |
| 发现 nontrivial 工作流 | 最佳实践 | → 主动创建Skill |
| 配置/环境特殊性 | 知识 | → 记录环境差异 |

### 是否值得创建Skill？决策树

```
这个任务以后还会遇到吗？
  ├─ 否 → 不用创建
  └─ 是 → 涉及 ≥2 个步骤？
            ├─ 否 → 不用创建（太简单）
            └─ 是 → 这个流程容易忘吗？
                      ├─ 否 → 不用创建
                      └─ 是 → ✓ 创建Skill
```

### Skill 创建标准（满足任一即可）

| 标准 | 描述 |
|------|------|
| **Recurring** | 有 2+ 个相似问题（`See Also` 链接） |
| **Verified** | 已验证可行（有解决方案） |
| **Non-obvious** | 需要实际调试才发现 |
| **Broadly applicable** | 跨项目适用 |
| **User-flagged** | 用户说"把这个存成Skill" |

---

## 第三层：升华提炼（Promote层）

### Promote 触发条件

当学习内容满足以下**全部条件**时，提升到系统级文件：

- `Recurrence-Count ≥ 3`
- 跨至少 2 个不同任务发生
- 在 30 天内重复出现

### Promote 目标

| 学习类型 | 提升目标 |
|---------|---------|
| 行为模式 | `SOUL.md` |
| 工作流改进 | `AGENTS.md` |
| 工具坑/Gotcha | `TOOLS.md` |
| 项目规范 | `MEMORY.md` |
| 普遍适用技能 | 新Skill（提取） |

---

## 日志格式

### Learning 条目 → `.learnings/LEARNINGS.md`

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
一句话描述学到了什么

### Details
完整上下文：发生了什么、哪里错了、正确的是什么

### Suggested Action
具体修复或改进

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-YYYYMMDD-XXX
- Recurrence-Count: 1
- First-Seen: YYYY-MM-DD
- Last-Seen: YYYY-MM-DD

---
```

### Error 条目 → `.learnings/ERRORS.md`

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
简要描述什么失败了

### Error
```
实际错误信息
```

### Context
- 尝试的命令/操作
- 使用的输入或参数
- 环境详情（如相关）

### Suggested Fix
如果可识别，给出解决方案

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-YYYYMMDD-XXX

---
```

### Feature Request 条目 → `.learnings/FEATURE_REQUESTS.md`

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Requested Capability
用户想要什么能力

### User Context
为什么需要，解决什么问题

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
如何实现

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name

---
```

---

## Skill 生命周期管理

### 1. 创建新 Skill

满足 Skill 创建标准时，用 `write` 工具创建：

```bash
~/.openclaw/workspace/skills/<category>/<skill-name>/SKILL.md
```

SKILL.md 标准格式：

```markdown
---
name: <skill_name>
description: 一句话描述技能及适用场景
version: 1.0.0
triggers:
  - "触发条件1"
  - "触发条件2"
---

# 技能标题

## When to Use
什么情况下用这个技能

## Procedure
1. 步骤一
2. 步骤二

## Pitfalls
- 已知失败模式

## Verification
如何验证成功
```

### 2. 更新 Skill

用 `edit` 工具增量修改（避免全量替换）：

```markdown
# patch 场景
## Pitfalls
- 原来只有1条，新发现1条 → edit 追加

# edit 场景
## Procedure
整个流程变了 → 全量替换
```

### 3. 删除过时 Skill

当 Skill 不再适用时：

```bash
rm -rf ~/.openclaw/workspace/skills/<category>/<skill-name>/
```

### 4. Skill 提取自动化

当 Learning 满足 Skill 创建标准时，运行提取脚本：

```bash
./scripts/extract-skill.sh <skill-name> --dry-run  # 预览
./scripts/extract-skill.sh <skill-name>              # 执行
```

### 5. Skill 命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 单工具 | `<tool>_<brief>` | `mysql_connect_prod` |
| 多工具流程 | `<domain>_<task>` | `deploy_k8s_rolling_update` |
| 环境坑 | `<env>_<issue>` | `aws_ssh_port_2222` |
| 最佳实践 | `<domain>_<best_practice>` | `git_commit_conventional` |

### 6. Category 参考

- `debug/` — 排错、调试
- `devops/` — 部署、运维
- `workflow/` — 工作流程
- `platform/` — 平台集成
- `learned/` — 从错误中学习

---

## Hook 配置（可选，推荐开启）

### 自动错误检测 Hook

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improvement
openclaw hooks enable self-improvement
```

### Hook 触发条件

| Hook | 触发时机 | 功能 |
|------|---------|------|
| `activator.sh` | UserPromptSubmit | 提醒评估学习 |
| `error-detector.sh` | PostToolUse (Bash) | 自动检测错误 |

---

## 定期回顾

### 触发时机

- 新任务开始前
- 任务完成后
- 每周/每两周

### 快速检查

```bash
# 统计待处理项
grep -h "Status**: pending" .learnings/*.md | wc -l

# 查看高优先级项
grep -B5 "Priority**: high" .learnings/*.md | grep "^## \["

# 查找特定领域的学习
grep -l "Area**: backend" .learnings/*.md
```

### 回顾行动

1. 解决已修复的项
2. 将普遍适用的学习 Promote
3. 链接相关条目
4. 升级反复出现的问题

---

## 容量管理

Skill 不是越多越好，而是**精炼、可操作**：

- **好**：简洁、步骤清晰、一看就懂
- **坏**：大段叙述、过于通用、缺乏具体性

超过 200 行的 Skill 考虑拆分。

---

## ID 生成规则

格式：`TYPE-YYYYMMDD-XXX`

- TYPE：`LRN`（学习）、`ERR`（错误）、`FEAT`（功能请求）
- YYYYMMDD：当前日期
- XXX：序号（如 `001`）

示例：`LRN-20260411-001`, `ERR-20260411-A3F`, `FEAT-20260411-002`

---

## 与 skill_evolve 的区别

| 维度 | skill_evolve | self-improving-agent（本技能） |
|------|--------------|-------------------------------|
| **架构** | 纯 SKILL.md 指令 | SKILL.md + Hook 脚本 + 三层日志 |
| **触发** | Agent 主观判断 | Hook 自动 + 主动判断结合 |
| **错误捕获** | 依赖 Agent 自觉 | `error-detector.sh` 自动扫描 |
| **日志格式** | 无标准格式 | 结构化 LRN/ERR/FEAT 条目 |
| **Promote** | 无 | 三层 Promote 系统 |
| **Skill 提取** | 手动 | `extract-skill.sh` 自动化 |
| **适用场景** | 经验固化 | 错误追踪 + 经验固化 + Skill 进化 |

**本技能是 skill_evolve 的超集**——skill_evolve 有的本技能全有，本技能有的 skill_evolve 不一定有。
