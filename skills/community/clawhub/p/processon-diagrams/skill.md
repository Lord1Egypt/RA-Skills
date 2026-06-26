---
name: "processon-diagrams"
description: "已废弃的兼容别名，现已更名为 `processon-diagramgen`。This skill has been renamed and should no longer be used as the primary ProcessOn diagram skill. If `processon-diagrams` is mentioned or triggered, tell the user it has been renamed to `processon-diagramgen` and follow the `processon-diagramgen` workflow instead."
icon: "📊"
author: "ProcessOn"
version: "2.0.6"
tags:
  - "diagram"
  - "architecture"
  - "flowchart"
  - "processon"
  - "visualization"
dependencies:
  bins:
    - python3
---

# Deprecated: processon-diagrams

`processon-diagrams` has been renamed to `processon-diagramgen`.

`processon-diagrams` 已废弃，当前正式名称为 `processon-diagramgen`。

## Migration Rule

- If the user mentions `processon-diagrams`, explicitly say it is deprecated and has been replaced by `processon-diagramgen`.
- 如果用户提到 `processon-diagrams`，要明确告知它已经废弃，并已更名为 `processon-diagramgen`。
- Do not use this file as the primary workflow definition anymore.
- 不要再把这个文件当作主工作流定义使用。
- Follow the workflow in `processon-diagramgen` instead.
- 应改为遵循 `processon-diagramgen` 中定义的工作流。
- Keep this file only for backward compatibility and migration guidance.
- 保留这个文件仅用于兼容旧名称和提供迁移说明。

## Suggested Wording

You can say:

> `processon-diagrams` 已废弃，已更名为 `processon-diagramgen`。我将按 `processon-diagramgen` 的流程继续处理你的请求。
