---
name: proflow
description: 项目全流程标准化交付技能。深度整合 openspec 与 superpowers，覆盖从需求脑暴到规格文档的完整开发周期。核心能力：智能功能规模评估（fix/小功能自动跳过脑暴直达代码）、全局唯一需求ID注入与防重、标准化文档命名与归档、全流程阶段追踪与回退。支持 proflow full/brainstorm/plan/execute/spec/status/reset 命令。触发条件：用户提及 proflow、项目全流程、标准项目流程、一键全自动项目文档、需求脑暴与执行计划等。
---

# Proflow 项目标准化全流程

## 概述

执行团队标准项目流程，覆盖脑暴、计划、执行、标准化文档四个阶段。强制统一目录规范、自动生成唯一需求ID、标准化文件名格式。

## 可用命令

- `proflow full` — 一键全自动完整流程（脑暴→计划→执行→文档）
- `proflow brainstorm` — 阶段1：需求脑暴发散
- `proflow plan` — 阶段2：生成执行计划
- `proflow execute` — 阶段3：自动化落地执行
- `proflow spec` — 阶段4：生成全量标准化规格文档
- `proflow status` — 查看当前项目执行状态
- `proflow reset [stage]` — 重置指定阶段状态（支持回退重跑）

## 前置准备

### 前置依赖检查（强制）
使用本技能前必须确保已安装：
1. `openspec` 技能
2. `superpowers` 技能
任一缺失将直接提示并退出，不执行后续逻辑。

### 初始化步骤（强制）
执行任何阶段命令前，运行以下初始化步骤：

1. **解析需求ID**：
   - 优先读取用户传入的 `--id` 参数
   - 其次尝试从提示词中提取需求编号（如 `2345`、`25` 等格式）
   - 若以上均未获取到，使用当前时间的 `hhmmss`（6位数字，如 `143052`）作为唯一编号
   - 使用 `scripts/id_manager.py` 扫描 `docs/` 目录校验全局唯一性，自动去重（不再限制数值大小）
2. **功能规模判断**：
   - 根据用户提示词智能判断功能规模，分为四类：`fix`、`小功能`、`中等功能`、`大功能`
   - 判断规则（优先级从高到低）：
     - 提示词中明确出现 "fix"、"bugfix"、"修复" → 判定为 `fix`
     - 提示词中涉及 "字段修改"、"表结构变更"、"数据库迁移"、"接口协议变更"、"核心架构调整" → 无论描述长短，**强制判定为 `大功能`**，必须按完整步骤执行
     - 仅涉及单点改动、文案替换、简单样式调整、单一配置项变更 → 判定为 `小功能`
     - 涉及 2~3 个模块联动、新增中等复杂度页面或接口 → 判定为 `中等功能`
     - 涉及系统级重构、多模块大规模改造、全新功能模块 → 判定为 `大功能`
   - 若判定为 `fix` 或 `小功能`，**跳过后续所有阶段流程**，直接定位代码并进行修改
   - 若判定为 `中等功能` 或 `大功能`，继续执行以下步骤
3. 使用 `scripts/file_naming.py` 确认文件名格式：`cr-{id}-{slug}-{YYYYMMDD}`
4. 使用 `scripts/log_manager.py` 初始化日志文件到 `docs/logs/`

## 全流程（full）

按顺序执行以下阶段，每个阶段前检查状态标记，已完成的阶段自动跳过：

### 1. 脑暴阶段
- 检查状态 `.opencode/status/proflow/brainstorm.done`，如果判断文件夹不存在，请创建并添加gitignore忽略文件.opencode/status/ 目录，并创建 .gitignore 文件忽略该文件夹
- 若未完成：调用 `superpowers brainstorming` skill 梳理项目核心需求与业务边界
- 将结果保存到 `docs/brainstorm/cr-{id}-brainstorm-{YYYYMMDD}.md`
- 标记状态完成，并记录日志

### 2. 计划阶段
- 检查状态 `.opencode/status/proflow/plan.done`
- 若未完成：确保脑暴阶段已完成；调用 `superpowers writing-plans` skill 生成执行计划
- 将结果保存到 `docs/plans/cr-{id}-execution-plan-{YYYYMMDD}.md`
- 标记状态完成，并记录日志

### 3. 执行阶段
- 检查状态 `.opencode/status/proflow/execute.done`
- 若未完成：确保计划阶段已完成；调用 `superpowers executing-plans` skill 或 `superpowers subagent-driven-development` skill 按步骤执行
- 将执行记录保存到 `docs/execute/cr-{id}-execute-record-{YYYYMMDD}.md`
- 标记状态完成，并记录日志

### 4. 文档阶段
- 检查状态 `.opencode/status/proflow/spec.done`
- 若未完成：确保执行阶段已完成
- 调用 `openspec` skill 按需生成项目规格文档：
- 依次生成以下文档并保存：
  - PRD: `docs/spec/prd/cr-{id}-prd-{YYYYMMDD}.md`
  - 架构设计: `docs/spec/architecture/cr-{id}-architecture-{YYYYMMDD}.md`
  - API 规范: `docs/spec/api/cr-{id}-api-spec-{YYYYMMDD}.md`（如果是前端功能，不需要生成这个文件）
  - 数据库设计: `docs/spec/database/cr-{id}-database-design-{YYYYMMDD}.md`（如果是前端功能，不需要生成这个文件）
- 标记状态完成，并记录日志

## 单阶段执行

### brainstorm
执行脑暴阶段并保存结果。流程同上阶段1。

### plan
依赖脑暴阶段已完成，生成执行计划并保存。流程同上阶段2。

### execute
依赖计划阶段已完成，按步骤执行并记录。流程同上阶段3。

### spec
依赖执行阶段已完成，生成全量规格文档。流程同上阶段4。

## 辅助命令

### status
运行 `scripts/status_manager.py list` 查看各阶段完成状态，并显示最新日志摘要。

### reset [stage]
运行 `scripts/status_manager.py reset [stage]` 清除指定阶段的状态标记，记录回退日志。支持的 stage 值：`brainstorm`、`plan`、`execute`、`spec`。

## 输出规范（强制）

1. 所有输出自动归档到 `docs/brainstorm/`、`docs/plans/`、`docs/execute/`、`docs/spec/`、`docs/logs/`
2. 禁止生成 `docs/superpowers/` 目录，禁止非标文件名
3. 需求ID全局唯一，自动扫描去重，支持 `--id` 自定义；未指定时默认按 `hhmmss` 生成
4. 文件名强制格式：`cr-{id}-{slug}-{YYYYMMDD}.md`
5. 状态文件禁止手动删除，异常自动触发回退提示与日志记录

## Scripts

- `scripts/id_manager.py` — 文档扫描、ID 生成与去重
- `scripts/status_manager.py` — 状态标记管理
- `scripts/log_manager.py` — 日志记录与查询
- `scripts/file_naming.py` — 标准化文件名生成