---
name: "hopola-cutout"
description: "执行商品抠图与去背景并返回透明底图链接。Invoke when user requests cutout/background removal before product-image generation."
---

# Hopola Cutout

## 作用
负责对商品原图执行抠图与去背景，返回可用于商品图二次生成的透明底图或净背景图链接。

## 触发时机
- 用户明确提出“抠图”“去背景”“先抠图再生图”。
- 商品图流程中出现前置抠图失败，需要单独抠图重试。
- 主技能阶段为 `generate-product-image` 且检测到背景复杂。

## 输入
- `image_url`
- `session_uploaded_images`
- `auto_upload_session_images`
- `cutout_mode`
- `output_background`

## 输出
- `cutout_image_url`
- `tool_name_used`
- `fallback_used`
- `cutout_status`
- `error_message`

## 工具优先级
1. `api_v1_sod_c_async`

## 规则
- 若 `image_url` 缺失但存在 `session_uploaded_images`，必须先调用上传子技能自动上传并回填 `image_url`。
- 固定优先调用 `api_v1_sod_c_async`，参数仅使用 `image_url`。
- 若 `api_v1_sod_c_async` 返回 `GATEWAY_ROUTE_DATA_NOT_FOUND`、网络异常或任务失败，仅允许在同工具链内重试。
- 若用户指定 `output_background=transparent`，优先保留主体边缘，不添加场景元素。
- 若多次重试仍失败，返回 `cutout_status=failed` 与错误摘要，不得伪造链接。
- 输出必须显式标注 `tool_name_used` 和 `fallback_used`。

## 默认参数
- `cutout_mode`: `auto`
- `output_background`: `transparent`

## 调用示例
```json
{
  "mode": "stage",
  "stage": "cutout",
  "task_type": "product-image",
  "image_url": "https://example.com/product.png",
  "cutout_mode": "auto",
  "output_background": "transparent",
  "report_format": "markdown"
}
```

## 失败处理
- 工具不可用：记录失败码并切换回退工具。
- 返回空链接：判定失败并提示用户更换原图格式（建议 PNG/JPG，主体清晰、无严重压缩）。
- 鉴权失败：提示检查 `OPENCLOW_KEY`。
