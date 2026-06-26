---
name: openclaw-continuous-work
description: 全面优化 OpenClaw 对话体验并强化任务闭环执行。Use when user asks to 优化, 工作, 项目, 持续工作, 不要停, 继续做, 继续工作, 或希望助手接收指令后持续推进直到完成。Also use when the user asks for complete optimization tasks rather than partial fixes.
---

# OpenClaw Continuous Work

## Goal
- 连续推进：接到指令后持续执行直到完成。
- 优化闭环：优化任务必须全链路落地并回归验证。
- 稳定反馈：里程碑 + 时间触发进度汇报，避免沉默或刷屏。

## Rule Map
- 规则总览（自动索引）：`References/ReferenceMap.md`
- 模块化规范：`References/ModuleSystem.md`
- 模块加载顺序配置：`References/ModuleOrder.json`

## Core Modules
- 通用连续执行规则：`References/GeneralRules.md`
- 持续执行强约束：`References/ContinuousExecutionDirective.md`
- 优化任务专项规则：`References/OptimizationRules.md`
- 优化指令原文基线：`References/OptimizationDirective.md`
- 汇报模板：`References/ReportingTemplate.md`
- 优化清单：`References/OptimizationChecklist.md`
- 验收模板：`References/AcceptanceTemplate.md`
- 质量评分：`References/QualityRubric.md`

## Scripts
- 一键优化流水线：`Scripts/RunOptimizationPipeline.py`
  - 用法：`python Scripts/RunOptimizationPipeline.py <target_path>`
  - 作用：串联执行命名巡检、内容/链接巡检、索引重建并输出汇总结果。
- 命名规范巡检：`Scripts/NamingAudit.py`
  - 用法：`python Scripts/NamingAudit.py <target_path> --json`
  - 作用：扫描命名不符合“单词首字母大写”规则的文件/文件夹并给出建议。
- 模块顺序校验：`Scripts/ValidateModuleOrder.py`
  - 用法：`python Scripts/ValidateModuleOrder.py`
  - 作用：校验 `References/ModuleOrder.json`（缺失模块、重复项、冲突项），输出 `ModuleOrderReport.md/json`。
- 模块索引重建：`Scripts/BuildReferenceMap.py`
  - 用法：`python Scripts/BuildReferenceMap.py`
  - 作用：自动重建 `References/ReferenceMap.md`，让新增 MD 模块即时纳入索引。
- 模块依赖图构建：`Scripts/BuildModuleGraph.py`
  - 用法：`python Scripts/BuildModuleGraph.py`
  - 作用：自动生成 `References/ModuleGraph.md` 与 `References/ModuleGraph.json`。
- 规则冲突巡检：`Scripts/DetectRuleConflicts.py`
  - 用法：`python Scripts/DetectRuleConflicts.py`
  - 作用：自动生成 `References/ConflictReport.md` 与 `References/ConflictReport.json`。
- 内容去重与链接巡检：`Scripts/ContentLinkAudit.py`
  - 用法：`python Scripts/ContentLinkAudit.py <target_path> --json`
  - 作用：检测重复段落与失效 Markdown 链接，支持持续精简与联动。
- 编码规范化：`Scripts/NormalizeEncoding.py`
  - 用法：`python Scripts/NormalizeEncoding.py`
  - 作用：统一文本文件为 UTF-8（无 BOM）+ LF，降低写入与解析报错风险。

## Maintainer Notes
- 新增场景优先写入 `References/`，保持本文件精简。
- 优先扩展：触发词、失败升级策略、完成判定与验收模板。
