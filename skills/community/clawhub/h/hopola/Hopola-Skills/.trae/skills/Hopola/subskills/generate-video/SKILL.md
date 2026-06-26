---
name: "hopola-generate-video"
description: "调用 Gateway MCP 生成视频。Invoke when user needs text-to-video output and consistent media generation workflow."
---

# Hopola Generate Video

## 作用
完成文生视频任务，支持固定工具优先与自动发现回退。

## 触发时机
- 用户要求生成视频。
- 主技能 `task_type=video` 或阶段 `generate-video`。

## 输入
- `video_prompt`
- `video_ratio`
- `video_duration`
- `video_resolution`
- `video_sound`

## 输出
- `video_urls`
- `tool_name_used`
- `fallback_used`

## 规则
- 优先使用 `preferred_tool_name`。
- 固定工具不可用时触发关键词发现。
- 输出需标注时长、比例与分辨率。
