# Optimization Rules

## Mandatory Prompt Baseline
当用户发出“优化”指令时，强制执行以下基线（原文详见 `OptimizationDirective.md`）：
1. 深度分析文件目录和文件内容。
2. 文件/文件夹命名使用单独单词或单词组，且每个单词首字母大写。
3. 精简内容、减少重复、加强文件间联系。
4. 允许并执行必要的修改、删减、增加。

## Standard Flow
1. 明确目标与验收标准（缺省时先给默认标准）。
2. 全局扫描并按优先级列问题清单。
3. 执行优化并记录关键改动。
4. 回归验证关键路径与关联点。
5. 使用 `AcceptanceTemplate.md` 输出收尾结果。

## Depth Guardrails
- 禁止只修表面问题，必须检查上下游影响。
- 完成前必须做至少一次相邻功能点回归。
