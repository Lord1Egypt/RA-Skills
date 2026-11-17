---
name: nature-paper-workflow
displayName: "Nature Paper Workflow 论文生产链"
version: 2.0.0
summary: 多学科端到端论文工作流顶层路由 skill，支持 STEM 与经济学双分支。
slug: nature-paper-workflow
description: >-
  论文生产链顶层路由 skill：识别阶段并路由到子 skill。Use when user says
  论文生产链、paper workflow、帮我写论文、帮我投稿、经济学论文、DiD、IV、AER、QJE.
  This skill does NOT execute paper tasks; it routes to sub-skills.
  行为范围：只读子 skill SKILL.md，无网络/subprocess/写入。
author: TRAE SOLO CN
license: MIT
tags: [paper, workflow, router, nature, academic, research, writing, submission, economics, econ]
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    primaryEnv: ""
    envVars: []
---

# 论文生产链 — Paper Workflow Router

## 角色定位

本 skill 是**子母结构的母 skill**（顶层路由），不直接执行任何论文生产任务。它的职责：

1. **Pre-Phase 学科识别**：将任务分流到 STEM 分支（默认）或 Econ 分支（可选）
2. **识别用户当前所处的论文生产阶段**
3. **路由到对应的子 skill**（已安装在 `~/.claude/skills/`）
4. **在工作流状态机中追踪进度**，建议下一步
5. **处理跨阶段 handoff**，避免信息丢失

**铁律**：不要从这个 router 中"凭记忆"执行任何论文任务。永远先识别学科分支，再识别阶段，再路由到子 skill，让子 skill 的 SKILL.md 主导执行。

## 触发条件

### 主触发（显式）
- "论文生产链" / "paper workflow" / "nature workflow"
- "论文工作流" / "论文全流程" / "论文生产"
- "帮我写论文" / "帮我投稿" / "论文下一步该做什么"

### 学科扩展触发（v2.0.0 新增）
- **经济学**："经济学论文" / "DiD" / "IV" / "RDD" / "RCT" / "双重差分" / "工具变量" / "断点回归" / "经济研究" / "管理世界" / "中国工业经济" / "经济学季刊" / "AER" / "QJE" / "JPE" / "Econometrica" / "REStud"

### 阶段触发（自动识别）

详见 [references/trigger-map.md](references/trigger-map.md)。

### 反例（不触发本 skill）
- 用户明确指定子 skill 名（如"用 nature-reader 读这篇"）→ 直接路由到子 skill
- 单一阶段任务且无跨阶段需求 → 直接调子 skill
- 非论文场景（写代码、做 PPT、写报告）→ 不触发

## Pre-Phase 学科识别（v2.0.0 新增）

在主工作流之前执行学科识别，将任务分流到对应分支：

```
用户输入
    │
    ▼
学科信号扫描（关键词 / 文件类型 / 上下文）
    │
    ▼
┌──────────────────────────────────────────┐
│ Econ 信号 ≥2 且 STEM 信号 =0 → Econ 分支│
│ STEM 信号 ≥1 且 Econ 信号 =0 → STEM 分支│
│ 信号冲突 → 问 1 个问题确认              │
│ 无信号 → 默认 STEM 分支                  │
└──────────────────────────────────────────┘
```

详细决策树、信号清单、冲突仲裁规则见 [references/discipline-routing.md](references/discipline-routing.md)。

## 分支工作流

### STEM 分支（默认）— 12 阶段端到端

```
Phase 0: 读论文+调研 → Phase 1: 项目初始化 → Phase 2: 起草+结构
Phase 3: 图+证据     → Phase 4: 统计+数据   → Phase 5: 引用+数据声明
Phase 6: 润色+预检   → Phase 7: 审稿+返修
衍生场景: D1 转 PPT / D2 转专利 / D3 写基金 / D4 实验记录 / D5 会议论文
```

详细状态机图、阶段定义、子 skill 映射见 [references/workflow-map.md](references/workflow-map.md)。

### Econ 分支（可选）— 6 阶段经济学工作流（v2.0.0 新增）

```
E-0: 输入审计 → E-1: 全文起草 → E-2: 表图设计
E-3: 论证逻辑审计 → E-4: 期刊适配 → E-5: 审稿+返修
```

详细阶段定义、子 skill 映射、handoff 产物见 [references/econ-workflow.md](references/econ-workflow.md)。

**前置条件**：Econ 分支需用户独立安装 econ-* 扩展包（5 个子技能，CC BY-NC 4.0 许可）。安装命令见 [references/discipline-routing.md](references/discipline-routing.md#安装校验)。

## 路由协议（每次调用必走 5 步）

### Step 1: Pre-Phase 学科识别
扫描用户输入的学科信号，按决策树分流到 STEM 或 Econ 分支。详细规则见 [references/discipline-routing.md](references/discipline-routing.md)。

### Step 2: 识别阶段
在选定分支内识别当前所处的阶段。识别依据：显式阶段关键词（[trigger-map.md](references/trigger-map.md)）、任务上下文（PDF/草稿/.dta/.do）、进度线索（"投稿前"/"返修"）。如果阶段不明确，**最多问一个问题**就确定，不要连环追问。

### Step 3: 告知用户当前分支 + 阶段 + 路由目标
```
📍 学科分支：STEM / Econ
📍 当前阶段：Phase 2 - 起草与结构 / E-1 - 全文起草
🎯 路由到：nature-writing / econ-write
```

### Step 4: 调用子 skill
读取目标子 skill 的 `SKILL.md`，让它的路由协议主导执行。具体调用方式见 [references/sub-skill-protocol.md](references/sub-skill-protocol.md)。

### Step 5: 建议下一步
子 skill 任务完成后，根据当前分支的状态机建议下一阶段。**不要强制顺序**——用户可以跳过任何阶段。

## 特殊路由规则

### Rule 1: 双子 skill 协同
某些阶段需要两个子 skill 协同：
- **STEM Phase 0b 文献调研**：`nature-academic-search`（检索）+ `academic-researcher`（综述）
- **STEM Phase 4 统计**：`stats-reporting-audit`（审计）+ `nature-statistics`（分析）
- **STEM Phase 5 引用**：`nature-ref-verifier`（核验）+ `nature-citation`（补充）
- **Econ E-5 审稿+返修**：`nature-reviewer`（共享，按经济学视角调整）+ `nature-response`（共享，逐点回复）

### Rule 2: 冲突消解与协同

子 skill 关系分四类，详细映射表见 [manifest.yaml](manifest.yaml) 的 `conflict_resolution` 段：

1. **学科分流（最高优先级）**：章节起草 / 表图设计 / 期刊适配 / 中文润色 → 按学科分支路由
2. **等价冲突（择一使用）**：科研绘图 / 审稿模拟 / 返修回复 / 章节起草 / 论文深读 / 论文转 PPT → 优先已安装版本
3. **互补协同（配合使用）**：引用核验（先内容后格式）/ 润色（先段落后句子）/ 会议论文（独立场景）
4. **跨学科共享（无冲突）**：paper-bootstrap / nature-ref-verifier + citation-verifier / submission-audit / nature-reviewer / nature-response

**判断规则**：
- 期刊投稿：用 `nature-writing` + `nature-polishing`
- 会议论文：用 `conference-paper-writing` + `scientific-prose-style`
- 经济学论文：走 Econ 分支，用 `econ-write` / `cn-top-econ-writing` + `econ-table-figure-design`

### Rule 3: 跨阶段 handoff

当用户从一个阶段跳到另一个阶段时，提醒需要带走的关键产物。详细 handoff 映射：
- STEM 分支：见 [references/workflow-map.md](references/workflow-map.md#跨阶段-handoff-产物)
- Econ 分支：见 [references/econ-workflow.md](references/econ-workflow.md#跨阶段-handoff-产物)

### Rule 4: 中英文场景识别
- **中文场景**（读中文论文、写中文组会 PPT、国知局专利、《经济研究》《管理世界》投稿）：优先中英对照能力的子 skill
- **英文场景**（Nature 系列投稿、英文润色、英文审稿、AER/QJE/JPE 投稿）：所有子 skill 均适用

## 默认假设

- 默认 STEM 分支（未识别到经济学信号时）
- 默认期刊导向（非会议），未明确 venue 时按 Nature 系列处理
- 默认结构先于润色（reverse outline → prose polish）
- 默认证据边界优先（Abstract 不允许比下游证据更强）
- 默认一图一主张（每张主图只承载一个主结论）
- Econ 分支默认按投稿目标选英文/中文子 skill

## 与子 skill 的边界

本 router **不做**：任何具体的论文写作、润色、出图、引用核验、文件创建、代码执行、PDF 解析、数据分析、经济学回归分析。

本 router **只做**：Pre-Phase 学科识别、阶段识别、子 skill 路由、进度追踪与下一步建议、跨阶段 handoff 提醒。

## 权限声明

本 skill 是只读路由器，不直接执行任何任务。权限范围：

| 能力类别 | 是否使用 | 说明 |
|---------|---------|------|
| 网络访问 | ❌ | 不发起任何网络请求（路由器无需联网） |
| 文件读写 | ✅（只读） | 读取 `~/.claude/skills/<sub-skill>/SKILL.md`（仅读，不写） |
| 环境变量 | ❌ | 不读取任何环境变量 |
| subprocess | ❌ | 不调用任何外部命令 |
| 外部 API | ❌ | 不调用任何外部 API |

**用户须知**：本 skill 是路由器，无副作用，不会自动写入任何外部目的地，不会创建或覆盖项目内文件。所有实际任务由子 skill 执行，请参阅各子 skill 的权限声明。

## 安装位置

主 skill：`~/.claude/skills/nature-paper-workflow/`；STEM 子 skill（35 个）：`~/.claude/skills/{nature-*, paper-*, manuscript-optimizer, ...}/`；Econ 子 skill（5 个，可选）：`~/.claude/skills/{econ-write, cn-top-econ-writing, econ-table-figure-design, econ-writing-workflow, econ-writing-workflow-multiagent}/`；共享支持包：`~/.claude/skills/nature-shared/`。完整清单见 [references/skill-map.md](references/skill-map.md)。

## 参考文档

- [references/discipline-routing.md](references/discipline-routing.md) - 学科识别决策树（v2.0.0 新增）
- [references/econ-workflow.md](references/econ-workflow.md) - Econ 分支 E-0~E-5（v2.0.0 新增）
- [references/trigger-map.md](references/trigger-map.md) / [workflow-map.md](references/workflow-map.md) - 触发词表 + STEM 工作流图
- [references/skill-map.md](references/skill-map.md) / [sub-skill-protocol.md](references/sub-skill-protocol.md) - 子 skill 速查表 + 调用协议
- [manifest.yaml](manifest.yaml) - 工作流定义与子技能映射表

## 更新策略

主 skill 更新改 SKILL.md + manifest.yaml；子 skill 更新各自目录；新增子 skill 在 manifest.yaml 注册 + trigger-map.md 加一行；新增学科分支在 references/ 新增 `<discipline>-workflow.md`。
