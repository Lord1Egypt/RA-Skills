---
name: "hopola-logo-design"
description: "封装 Logo 设计问询与出图策略。Invoke when user needs brand logo concepts, style-aligned variants, and delivery-ready logo drafts."
---

# Hopola Logo Design

## 作用
负责品牌 Logo 方案问询、提示词构建与多版本出图，输出可选方向与落地建议。

## 触发时机
- 用户需要新品牌 Logo。
- 用户要对现有 Logo 做风格重做。
- 主技能 `task_type=logo` 或阶段 `generate-logo`。

## 输入
- `brand_name`
- `brand_slogan`
- `brand_industry`
- `brand_keywords`
- `logo_style`
- `logo_ratio`
- `logo_color_palette`
- `logo_usage_scenarios`

## 输出
- `logo_image_urls`
- `logo_concept_summary`
- `tool_name_used`
- `fallback_used`

## 规则
- 默认优先 `aiflow_nougat_create`。
- 问询至少覆盖行业、受众、风格、配色、应用场景、禁忌元素。
- 首轮输出至少 3 个不同方向，并给每个方向命名。
- 仅当用户明确要求“只要文案方案”时才可纯文本返回；默认必须实际调用生图工具并返回图片链接。
- 若未拿到图片链接，不得宣称已完成 logo 设计。
- 固定工具不可用时回退 `text2image_create_hydra_hoppa`。
