# Module System

## Purpose
使该 Skill 支持“随时新增 MD 模块文件”，且无需改动核心规则入口。

## Module Convention
- 所有可扩展模块放在 `References/` 目录。
- 文件命名遵循首字母大写规范（例如：`RiskControl.md`、`DeliveryPolicy.md`）。
- 每个模块建议包含：
  - `# <Title>`
  - `## Purpose`
  - `## Rules` 或 `## Checklist`
  - （可选）`## Examples`

## Loading Rule
- 核心入口从 `ReferenceMap.md` 读取。
- 模块优先级与排除列表由 `ModuleOrder.json` 配置。
- 新增模块后，运行 `python Scripts/BuildReferenceMap.py` 自动更新索引。

## User Workflow (Add New MD Anytime)
1. 在 `References/` 新建模块 MD 文件（可复制 `ModuleTemplate.md` 起步）。
2. 填写模块规则内容。
3. （可选）调整 `ModuleOrder.json` 的 priority/exclude。
4. 运行：`python Scripts/ValidateModuleOrder.py`
5. 运行：`python Scripts/BuildReferenceMap.py`
6. 运行：`python Scripts/BuildModuleGraph.py`
7. 运行：`python Scripts/DetectRuleConflicts.py`
8. 可选运行质量巡检：`python Scripts/ContentLinkAudit.py . --json`
9. 提交并推送。

## Notes
- 不改动 `SKILL.md` 主结构，除非入口逻辑变化。
- 模块间如有依赖，在模块内写 `See also: <OtherModule.md>`。
