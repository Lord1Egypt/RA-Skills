---
name: "hopola-generate-3d"
description: "调用 Gateway MCP 生成3D模型。Invoke when user asks for 3D assets and model links in the final report."
---

# Hopola Generate 3D

## 作用
完成 3D 资产生成，支持文生 3D 与单图生 3D，输出模型链接与格式信息。

## 触发时机
- 用户需要 3D 模型。
- 主技能 `task_type=3d` 或阶段 `generate-3d`。

## 输入
- `model3d_prompt`
- `model3d_image_url`
- `model3d_task_type`
- `model3d_quality`
- `model3d_format`

## 输出
- `model3d_urls`
- `tool_name_used`
- `fallback_used`

## 规则
- 默认优先 `3d_hy_image_generate`，支持文生 3D 与图生 3D。
- 当存在 `model3d_image_url` 时，优先走 `fal_tripo_image_to_3d` 单图生 3D。
- 固定工具不可用时按关键词自动发现 3D 工具。
- 报告中需标注模型格式与获取方式。
