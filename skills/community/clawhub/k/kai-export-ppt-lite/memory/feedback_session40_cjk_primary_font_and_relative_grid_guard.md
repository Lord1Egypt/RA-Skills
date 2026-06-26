# Session 40：CJK 文本不能只设 ea_font，grid/flex wrapper 要有 local-origin 守卫

## 1. 背景

继续收 `data-story` 的低分页时，确认了两个通用问题：

1. `P2 / P4 / P6` 的中文正文、卡片标题虽然已经有 `ea_font`
   - 但 `run.font.name` 仍然是 Latin font（之前是 `Helvetica Neue`）
   - 如果预览/渲染链优先吃 Latin font，整页视觉就会比 source 小一号

2. 像 `feat-grid / solution-grid` 这种 slide 内部的 grid wrapper，
   需要有明确的 local-origin 回归测试守住
   - 否则 children 一旦重新带回“页级绝对坐标思维”，很容易在右侧列出现几何漂移

## 2. 修复 A：CJK 文本的主字体也切到稳定 CJK font

### 根因

之前 `map_font()` 的策略是：

- pure Latin：走 Latin-safe font
- 含中文：仍然返回 `(latin_font, ea_font)`

这意味着：

- `ea_font` 是中文字体
- 但 `run.font.name` 还是 Latin font

在某些渲染/预览链里，这会导致中文整体看起来比 source 小一号。

### 修法

`map_font()` 现在改成：

- **pure Latin**：继续保持 Latin-safe 路径
- **contains CJK**：直接返回 `(ea_font, ea_font)`

也就是：

- `run.font.name`
- `a:ea`
- `a:cs`

三者都统一到稳定 CJK font。

### 当前验证

重导出后直接核 PPT 实体：

- `P2`：`用户认为 AI 生成内容缺乏独特美学` → `Hiragino Sans GB`
- `P4`：`数据报告 / KPI 看板` → `Hiragino Sans GB`
- `P6`：`精确视口适配` / `每页 = 一个视口，移动端自动缩放` → `Hiragino Sans GB`

并同步更新了测试：

- `test_map_font_prefers_office_safe_font_in_mixed_cjk_stack()`
- `test_map_font_prefers_stable_ppt_font_over_platform_stack_order()`
- `test_map_font_platform_only_cjk_stack_falls_back_to_office_safe_font()`

## 3. 修复 B：给 data-story feature grid 增加 local-origin 回归守卫

这轮还补了一条专门的回归测试：

- `test_data_story_feature_grid_children_stay_within_local_container_width()`

目的不是宣称 `P6` 已彻底解决，而是先把“feature grid 的 children 必须按 local container 宽度约束”固定成测试门槛，避免后面继续调 solver 时把相对坐标链弄回去。

## 4. 当前验证状态

- `python3 scripts/test-export.py`：通过
- `python3 scripts/export-sandbox-pptx.py demo/data-story-zh.html demo/data-story-output.pptx`：通过

## 5. 不要再犯

1. 对中文文本，只设置 `ea_font` 不够；如果最终 `run.font.name` 还是 Latin font，视觉仍可能明显偏小。
2. `grid/flex wrapper` 的 local-origin 不能只靠肉眼记忆，必须留一条回归测试盯住。
3. 当视觉问题是“整体比 source 小一号”，优先先查字体主链，再去抠 gap / min-height。
