# Ontology Modeling Decision Guide

## Is this table a business entity?

```
Q1: Do business people mention this concept daily?
  NO  → EXCLUDE (technical: logs, audit, config, sequences)
  YES → Q2

Q2: Does it have an independent lifecycle (create → use → archive)?
  NO  → Likely ENUM (dictionary/lookup) or LINK (association)
  YES → Q3

Q3: Can it exist independently (own PK and business meaning)?
  NO  → Likely sub-table or LINK
  YES → ENTITY
```

## ENUM vs ENTITY

```
>5 business-meaningful attributes?
  NO  → ENUM (e.g., gender table with 3 fields)
  YES → Consider ENTITY (e.g., country table with visa rules, 17 fields)

Referenced by >3 other entities?
  YES → Consider promoting to ENTITY
  NO  → Keep as ENUM
```

## Promote property to ENTITY? (Stanford Ontology 101)

```
Does this field have its own attributes to describe?
  NO  → Keep as property
  YES → continue

Do multiple entities reference this concept?
  NO  → Keep as property (local concern)
  YES → PROMOTE, create review_flag
```

## Cross-system merge

```
Same table name in different systems?
  YES → Auto-merge, keep version with more complete attributes

Similar Chinese name (>80%) AND field overlap (>60%)?
  YES → review_flag type=merge, do NOT auto-merge

Different name but same business concept?
  → review_flag, note shared FKs / similar fields
```

## Subagent Architecture (large projects)

For >100 files, parallelize with Claude Code Task tool:

- **Scanner subagent** (Explore): Run scan_directory.py, recommend batches
- **Extractor subagent(s)** (general-purpose): Process file batches, run extraction scripts, apply rules
- **Merger subagent** (general-purpose): Combine fragments, deduplicate, generate outputs

## Incremental Mode

If extraction interrupted or adding files:
1. Check existing extracted_tables.json
2. Process only new/unprocessed files
3. Merge with existing
4. Re-run Phase 3 on combined data

## Core Types 设计理由与边界定义

8 个 core types 对齐 BFO (Basic Formal Ontology) 的两大范畴：

- **Continuant（持续体）**：在时间中持续存在、可被反复引用的实体
- **Occurrent（发生体）**：占据时间区间、有起止的过程或事件

| Type | BFO 范畴 | 理由 |
|------|----------|------|
| Person | Continuant | 人在时间中持续存在，属性可变但身份不变 |
| Organization | Continuant | 组织持续存在，成员和结构可变 |
| Project | Continuant | 项目是长期存在的工作容器，状态可变 |
| Document | Continuant | 文档是持久化的信息载体，有文件路径 |
| Goal | Continuant | 目标是持续存在的期望状态描述 |
| Note | Continuant | 知识片段一旦创建即持续存在 |
| Task | Occurrent | 任务是有起止的工作过程 |
| Event | Occurrent | 事件是有时间定位的发生 |

### Person
人物实体。同事、客户联系人、行业人物、私人关系人。
- **算**：有姓名的自然人，如 `[per-00001] 张三`、`[per-00009] 李四`
- **不算**：岗位角色（"客户经理"是 Person 的 role 属性，不是独立实体）；团队（归 Organization）
- **与 Organization 的边界**：Person 通过 works_at 关系挂在 Organization 下，不内嵌

### Organization
组织实体。公司、部门、团队、政府机构、行业协会。
- **算**：有独立名称和运作结构的组织体，如 `[org-00002] 蓝天信息技术有限公司`、`[org-00013] 某部委`
- **不算**：临时工作小组（归 Project 的参与者）；一个人的工作室（除非对外有独立品牌）
- **层级处理**：用 subsidiary_of / parent_of 关系表达层级，如星辰集团 → 星辰集团国际 → 蓝天信息

### Project
长期工作容器。有明确目标、多个参与者、跨越一段时间。
- **算**：某战略项目文档体系、某IT系统项目、某AI产品开发，如 `[task-00005]` 对应的整体项目
- **不算**：一次性的具体工作（归 Task）；一场会议（归 Event）
- **与 Task 的边界**：Project 是"装 Task 的容器"。Project 没有单一 assignee，Task 有。Project 的完成取决于其下 Task 的完成。如"某IT系统项目"是 Project，"外派周八到某地"是其下的 Task

### Task
具体可交付的工作项。有明确的执行者、截止时间、完成标准。
- **算**：`[task-00001] 某IT系统项目实施`、`[task-00004] 某系统升级方案`
- **不算**：长期的战略方向（归 Goal）；已经结束的事情的记录（归 Event）
- **与 Event 的边界**：Task 面向未来或进行中，有 status（open/in_progress/done）。Event 面向过去，有 date。"编写升级方案"是 Task，"方案评审会（2025-06-01）"是 Event。Task 完成后不变成 Event——它的 status 变为 done

### Document
有文件路径的信息载体。实际存在于文件系统中的文件。
- **算**：`[doc-00001]` 以上所有有 path 属性的实体，Word/PDF/Excel/MD 文件
- **不算**：从文档中提取的知识片段（归 Note）；没有对应文件的口头信息
- **与 Note 的边界**：Document 有 `path` 属性指向文件系统中的真实文件。Note 是从 Document（或对话、会议）中提取的语义片段，没有独立文件路径。一个 Document 可以产出多个 Note。如 `[doc-00033] 项目需求规格书V2` 是 Document，从中提取的"系统需支持多语言"是 Note

### Event
已发生或已确定时间的事件。时间是必需属性。
- **算**：`[evt-00001] 2020年9月蓝天信息并入星辰集团国际`、`[evt-00013] 赴某地某IT系统项目现场实施`
- **不算**：正在进行且无确定结束时间的工作（归 Task）；周期性例行会议（除非某次会议产生了重要决定）
- **与 Task 的边界**：Event 回答"发生了什么"（what happened），Task 回答"要做什么"（what to do）。Event 有确切 date，Task 有 deadline（可能未定）。Event 是点或短区间，Task 是过程

### Note
非结构化知识片段。洞察、事实、观察、总结。
- **算**：`[note-00002] 业务占比:客户A占45%，客户B占35%，客户C占20%`、`[note-00004] 核心劣势:...`
- **不算**：有可度量结果的目标（归 Goal）；有时间和地点的事件（归 Event）
- **与 Goal 的边界**：Note 是对现状的描述或洞察，Goal 是对未来的期望。"蓝天信息市场占有率本地100%、国内5%"是 Note（现状事实），"将国内份额提升到15%"是 Goal（期望状态）

### Goal
可度量的目标状态。有期望达成的结果和判断标准。
- **算**：`[goal-00001] 巩固提升核心业务`、`[goal-00006] 立足本地市场、辐射周边地区`
- **不算**：模糊的愿景（"成为行业领先"太虚，除非配有量化指标）；具体的执行步骤（归 Task）
- **与 Task 的边界**：Goal 回答"要达到什么状态"，Task 回答"具体怎么做"。Goal 通过 measured_by 关系关联 Task，用 Task 的完成来衡量 Goal 的达成
