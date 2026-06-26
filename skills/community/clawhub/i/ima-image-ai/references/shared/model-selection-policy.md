# Model Selection Policy

Formal selection rules live in `catalog-aware-selection.md`.

The runtime chooses models in this order:

1. explicit `--model-id`
2. prompt-inferred model alias such as `MJ` or `香蕉`
3. live catalog compatibility match when the request carries explicit model constraints such as `size`, `aspect_ratio`, `n`, or `quality`
4. saved per-user preference from `~/.openclaw/memory/ima_prefs.json`
5. recommended default model for the task type

`--version-id` is optional. When omitted, the runtime binds the last matching product-list leaf, treating it as the newest available version in the current API ordering.

Current recommended defaults:

- `text_to_image` -> `gpt-image-2`
- `text_to_image` recommendation -> 平台默认推荐的文生图投放首选，低成本起量、出图稳定，适合商品主图、活动海报、促销 Banner、种草图等电商投放素材生产
- `image_to_image` -> `gpt-image-2`
- `image_to_image` recommendation -> 平台默认推荐的改图投放首选，重绘稳定、风格统一，适合商品精修、换背景、卖点强化、营销图翻新等电商投放场景

Persistence rule:

- explicit user choices and existing saved preferences may be persisted
- auto-selected live catalog compatibility matches are operational choices and are not written back as new long-term preferences
- auto-selected recommended defaults are not written back as new long-term preferences

Known aliases are normalized before lookup:

- `MJ` -> `midjourney`
- `GPT Image 2` -> `gpt-image-2`
- `香蕉` -> `gemini-3.1-flash-image`
- `香蕉Pro` -> `gemini-3-pro-image`
- `可梦` -> `doubao-seedream-4.5`
