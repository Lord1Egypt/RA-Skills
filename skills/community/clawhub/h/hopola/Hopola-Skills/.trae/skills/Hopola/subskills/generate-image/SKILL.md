---
name: "hopola-generate-image"
description: "调用 Gateway MCP 生成图片。Invoke when user needs text-to-image output with fixed tool priority and discovery fallback."
---

# Hopola Generate Image

## 作用
完成文生图任务，执行固定工具名优先、自动发现回退策略。

## 触发时机
- 用户明确要求生成图片。
- 主技能 `task_type=image` 或阶段 `generate-image`。

## 输入
- `image_prompt`
- `image_ratio`
- `image_quality`
- `image_resolution`

## 输出
- `image_urls`
- `tool_name_used`
- `fallback_used`

## 规则
- 先尝试 `preferred_tool_name`。
- 工具不可用时，从 MCP 工具列表按关键词匹配回退。
- 仅返回可公开访问的结果链接。
