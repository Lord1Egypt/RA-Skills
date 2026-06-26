# Session 29：Exporter 通用化设计方案 + Claude 对抗性评审

日期：2026-04-21

## 背景

在 Session 28 结束时，`demo/blue-sky-zh.html -> output.pptx` 的导出基线稳定在：

- overall = 8.4/10
- overflow = 0
- overlap = 0
- card containment = 0
- total actionable = 10

这说明“基础布局正确性”已经基本收敛，剩余问题更像结构语义没有被 exporter 正确建模：

- Slide 4 / 10：mixed inline 还不是稳定的 grouped inline
- Slide 7 / 8：展示型 row 结构仍和 data table 共用路径
- Slide 3 / 6 / 7 / 8 / 10：card/container 还残留旧 `_card_group` / fallback 语义

因此 Session 29 决定先停下继续提分，先重写方案，并让 Claude 做对抗性评审。

## 本轮文档

- `docs/session29-exporter-generalization-plan.md`
- `docs/session29-claude-adversarial-review.md`

## Claude 评审结论

Claude 结论：**需要先改方案**。

不是方向错误，而是原方案里仍有几处会让 exporter 再次过拟合或出现双重模型：

1. `compound_inline_group` 不能成为第二套 IR
   - 应退回为 `inline_fragments v2 grouped mode`
   - 保持 `extract_inline_fragments()` 为唯一入口
2. `presentation_rows` 不能靠“两列 table”来判断
   - 必须改成语义密度分类
3. corpus 太窄
   - 不能继续只围绕 Blue Sky
4. grouped inline / `presentation_rows` 之前，必须先补 `flow_box` 最小承载升级
5. `_card_group` 与 `flow_box` 的互斥要写成显式迁移契约
6. `total actionable` 与 `GOLDEN_FIRST_Y` 的替代锚点要明确定义

## 已采纳到方案的修改

1. `compound_inline_group` 改写为 `inline_fragments v2 grouped mode`
2. grouped fragments 首轮支持：
   - `text`
   - `code`
   - `kbd`
   - `badge/pill`
   - `link`
   - `separator`
   - `icon`
3. `presentation_rows` 改为语义密度分类：
   - 位于可见 card 内
   - 无 `thead/th`
   - 无复杂 span
   - `kbd/code/pill` 片段占比高
   - 行高视觉一致
4. corpus 扩为：
   - `references/blue-sky-starter.html`
   - `demos/blue-sky-zh.html`
   - `demos/slide-creator-intro.html`
   - 手写 HTML fixture
   - `demos/swiss-modern-zh.html`
5. 实施顺序重排为：
   - 先补 fixture/corpus + eval 门槛
   - 再做 `flow_box` 最小承载升级
   - 再做 grouped inline
   - 再做 `presentation_rows`
   - 再做完整 `flow_box_v2`
   - 最后退役 hardcode
6. 显式迁移契约：
   - 进入 `flow_box` 的子元素统一打 `_in_flow_box=True`
   - 同时清空 `_card_group`
   - layout/render loop 禁止这些元素走旧 `card_group` 路径
7. `GOLDEN_FIRST_Y` 的替代锚点明确为 `paddingTop + content_top`

## 本轮状态

- 本轮没有继续修改 `scripts/export-sandbox-pptx.py`
- 当前实现基线仍保持在 Session 28 Phase 3 的 `8.4/10`
- 但 Session 29 Phase 1 已落地：
  - 新增手写 fixture：`tests/fixtures/export-corpus/handwritten-card-list-table.html`
  - `scripts/test-export.py` 新增 corpus parse smoke / fixture coverage / structural eval gate
  - `scripts/rigorous-eval.py` 新增 `collect_eval_summary()`，并支持 `--golden` / `--sandbox` / `--skip-visual`

验证结果：

- `python3 -m py_compile scripts/test-export.py scripts/rigorous-eval.py` 通过
- `python3 scripts/test-export.py` 通过
- 手写 fixture 自举导出后的 structured eval 为 0 问题：
  - overflow = 0
  - overlap = 0
  - element gaps = 0
  - card containment = 0
  - color diffs = 0
  - total actionable = 0

## 下一步

1. 先做 `flow_box` 最小承载升级，不先追单页提分
2. 再把独立能力级 fixture 补齐到 grouped inline / `presentation_rows` / `flow_box` 三组
3. 再进入 grouped inline / `presentation_rows` 的实现

---

## Session 29 Continued：Phase 2 实现结果

本轮已经把方案里的 3 条主线接进代码：

1. `flow_box` 迁移契约
   - 新增 `_mark_flow_box_descendants()`
   - descendants 统一 `_in_flow_box=True`
   - 同时清空 `_card_group`
   - `layout_slide_elements()` 禁止这些元素回到旧 `card_group` 路径

2. `inline_fragments v2 grouped mode`
   - `extract_inline_fragments()` 新增 `badge/link/icon`
   - grouped inline 增加 `grouped=True` / `groupAlign`
   - grouped inline 参与内容宽度测量
   - `build_text_element()` 的 `preferContentWidth` 也覆盖 grouped inline

3. `presentation_rows`
   - 新增 `_classify_table_ir()`
   - 展示型 row 结构与真实数据表实现分流
   - 当前渲染仍走 table renderer 的稳态路径

新增测试：

- `test_extract_inline_fragments_grouped_badge_and_link()`
- `test_measure_flow_box_marks_descendants_in_flow_box()`
- `test_build_table_element_classifies_presentation_rows()`
- `test_build_table_element_keeps_real_data_tables()`

验证：

- `python3 -m py_compile scripts/export-sandbox-pptx.py scripts/test-export.py scripts/rigorous-eval.py` 通过
- `python3 scripts/test-export.py` 通过
- `python3 scripts/export-sandbox-pptx.py demo/blue-sky-zh.html output.pptx` 通过
- `python3 scripts/rigorous-eval.py` 结果：
  - `overflow = 0`
  - `overlap = 0`
  - `element gaps = 8`
  - `card containment = 0`
  - `total actionable = 8`

当前页分：

- Slide 1 `9.6`
- Slide 2 `9.7`
- Slide 3 `6.9`
- Slide 4 `8.0`
- Slide 5 `10.0`
- Slide 6 `7.5`
- Slide 7 `7.7`
- Slide 8 `7.9`
- Slide 9 `8.5`
- Slide 10 `7.5`

当前总体 `8.3/10`。

需要明确记录：

- 这是一次“能力建设优先”的实现，不是继续堆 deck-specific patch
- 通用能力已经落地，但 generalized 分支当前视觉分比 Session 28 best state `8.4/10` 低 `0.1`
- 主要回归在 Slide 7；Slide 4 小幅提升；Slide 8 基本持平

下一轮最值的方向不是再扩功能面，而是：

1. 先把 Slide 7 拉回 `8.2+`
2. 保留 `presentation_rows` IR，不急着扩专用 renderer
3. 再决定是否拆分 `kbd-heavy rows` 与 `label/value rows` 两条渲染路线

---

## Session 29 Continued：Phase 2.5 收敛结果

本轮继续优化后，generalized 分支已经从 `8.3/10` 抬到 `8.5/10`。

这次没有新增功能面，而是做了 3 条通用收敛修复：

1. `flow_box` 内容顶部 padding 回写
   - `measure_flow_box()` 现在会把真实内容按 `pad_t` 下推
   - 避免 layer/info card 的文本贴住上边缘

2. `border-left: 4px` accent card 冗余边框抑制
   - `flow_box` bg shape 清空 border 样式
   - `export_shape_background()` 在 accent-bar 模式下不再导出 top/right/bottom 的冗余边框 shape

3. centered grouped inline width 收敛
   - 对 `code + link` 的 centered grouped inline 行，不再极端 shrink-wrap
   - 改为按稳定的 centered block width 对齐

验证结果：

- `python3 -m py_compile scripts/export-sandbox-pptx.py scripts/test-export.py scripts/rigorous-eval.py` 通过
- `python3 scripts/test-export.py` 通过
- `python3 scripts/export-sandbox-pptx.py demo/blue-sky-zh.html output.pptx` 通过
- `python3 scripts/rigorous-eval.py`
  - `overflow = 0`
  - `overlap = 0`
  - `element gaps = 2`
  - `card containment = 0`
  - `total actionable = 2`

当前页分：

- Slide 1 `9.6`
- Slide 2 `9.7`
- Slide 3 `7.3`
- Slide 4 `8.0`
- Slide 5 `10.0`
- Slide 6 `7.1`
- Slide 7 `8.4`
- Slide 8 `8.4`
- Slide 9 `9.2`
- Slide 10 `7.5`

收益最明显的是：

- Slide 7 `7.7 → 8.4`
- Slide 8 `7.9 → 8.4`
- Slide 9 `8.5 → 9.2`
- Slide 3 `6.9 → 7.3`

当前剩余问题已经非常集中：

- `total actionable = 2`
- 全部集中在 Slide 10 closing command row 的文本组织
- golden 的 command row 是三段 paragraph 文本框，而当前 exporter 还是单段 grouped inline 文本框

结论：

- 这版已经证明通用能力增强可以直接转化成更高分，而不需要退回 deck-specific patch
- 下一步最值的是专门做 `closing command row` 的 grouped inline paragraph model

---

## Session 29 Continued：Phase 2.7 命令行 inline overlay + baseline 对齐

这轮继续沿着“程序能力”推进，而不是回到单页补丁。

新增的两条通用规则：

1. `flex-row baseline alignment`
   - `build_grid_children()` 对 plain flex row + `align-items: baseline` 增加基线估算
   - `_estimate_group_baseline_in()` 用首个文本行盒估算 baseline，再做 cross-axis offset
   - 直接收益：Slide 4 顶部 `按内容类型自动匹配` 胶囊从 `y=2.271` 收敛到 `y=2.347`，更接近 golden `2.465`

2. `single-line mixed inline command row`
   - `inline_fragments_to_segments()` / `segments_to_lines()` 现在保留 fragment 级 `fontFamily` / `letterSpacing`
   - `_fragment_style_snapshot()` 同步补齐这两项，code/monospace 风格不会在 segment 层丢失
   - `export_text_element()` 新增 `_layout_single_line_fragments()` / `_export_inline_box_overlay()`
   - 规则最终收窄为：只对“带 `code/kbd` 且同时带 link 的单行 mixed inline 行”导出真实 inline overlay
   - 这样 Slide 10 的 command row 进入 exporter 一等能力，而 Slide 3/6 的普通正文 inline 片段不会误升格成额外 shape

本轮也记录一次已回退的失败尝试：

- 第一版 inline overlay 把 Slide 3/6 的正文 code/kbd 一起转成额外 shape
- 虽然 Slide 10 overlay 生效，但引入了不必要的 shape 数回归
- 已回退到 command/CTA row 专用规则

本轮验证：

- `python3 -m py_compile scripts/export-sandbox-pptx.py scripts/test-export.py scripts/rigorous-eval.py` 通过
- `python3 scripts/test-export.py` 通过
- `python3 scripts/export-sandbox-pptx.py demo/blue-sky-zh.html output.pptx` 通过
- `python3 scripts/rigorous-eval.py`
  - `overflow = 0`
  - `overlap = 0`
  - `element gaps = 2`
  - `card containment = 0`
  - `color differences = 0`
  - `total actionable = 2`

当前页分：

- Slide 1 `9.2`
- Slide 2 `9.7`
- Slide 3 `7.6`
- Slide 4 `7.3`
- Slide 5 `10.0`
- Slide 6 `8.0`
- Slide 7 `8.1`
- Slide 8 `8.4`
- Slide 9 `9.7`
- Slide 10 `7.9`

当前状态的结论：

- generalized 分支当前仍是 `8.6/10`
- 结构问题已经非常集中：`overflow/overlap/containment/color diff = 0`
- 剩余 gap 依旧主要是 Slide 10 command row 的 paragraph 组织差异，而不是布局结构错误

---

## Session 29 Continued：Phase 2.8 mixed-script heading buffer + PPT-safe font stack

这轮继续沿着“程序能力”推进，而不是回到单页补丁。

新增的三条通用规则：

1. `mixed-script explicit-break display heading`
   - `build_text_element()` 对 `h1/h2/h3 + 显式换行 + centered + 大字号` 增加 wrap guard
   - 不再只看整段 CJK 宽度，而是按“最长 authored line + safety margin”预留宽度
   - 对同时包含 CJK 和 Latin 的标题，再补一个 `mixed_script_guard`
   - 直接收益：Slide 1 主标题文本框从 `4.667"` 轻微放大到 `4.700"`

2. `PPT-safe font stack resolution`
   - `map_font()` 不再机械按 CSS stack 的第一个平台字体命中
   - 当 stack 同时包含平台字体和稳定 Office-safe 中文字体时，优先选后者
   - 直接收益：Slide 1 标题、KPI 和命令行 run 现在都导出为 `Microsoft YaHei`

3. `inline box overlay follows row height`
   - `_layout_single_line_fragments()` 对 `code/kbd` overlay 不再死卡 `0.18"` 下限
   - 行内胶囊背景至少跟随整行 row height
   - 直接收益：Slide 10 的 code bg 从 `h=0.180"` 提升到 `h=0.213"`

本轮验证：

- `python3 -m py_compile scripts/export-sandbox-pptx.py scripts/test-export.py scripts/rigorous-eval.py` 通过
- `python3 scripts/test-export.py` 通过
- `python3 scripts/export-sandbox-pptx.py demo/blue-sky-zh.html output.pptx` 通过
- `python3 scripts/rigorous-eval.py`
  - `overflow = 0`
  - `overlap = 0`
  - `element gaps = 2`
  - `card containment = 0`
  - `color differences = 0`
  - `total actionable = 2`

当前页分：

- Slide 1 `9.2`
- Slide 2 `9.7`
- Slide 3 `7.9`
- Slide 4 `7.3`
- Slide 5 `10.0`
- Slide 6 `8.2`
- Slide 7 `8.3`
- Slide 8 `8.4`
- Slide 9 `9.7`
- Slide 10 `7.9`

当前状态的结论：

- generalized 分支当前 best state 更新为 `8.7/10`
- Slide 1 的主标题字体和行宽已经切到更稳的跨机器输出形态
- 剩余 actionable 仍然只集中在 Slide 10 closing command row 的 paragraph 组织差异

---

## Session 29 Continued：Phase 2.9 宽正文单行回退 + margin-aware block flow

这轮的目标是把 Slide 3 / 4 里还在反复出现的两类偏差，收敛成导出器底层规则，而不是继续做点对点 patch。

新增的四条通用能力：

1. `wide prose single-line fallback`
   - `build_text_element()` 对宽正文段落的 adjusted-fit 判定允许轻微负 overflow
   - 修复“调整后已经能放下，但仍被保持成 2 行”的逻辑错误
   - 直接效果：Slide 3 `.layer` 卡片正文高度从 `0.498"` 收敛到 `0.249"` 左右

2. `margin-aware block flow`
   - 新增 `_flow_gap_in()`
   - block flow 间距不再固定吃默认 gap，而是优先使用 `margin-bottom / margin-top` 的 collapsed 结果
   - 直接效果：Slide 3 / 4 标题区、divider、card 之间的垂直节奏更接近 golden

3. `group flow height measurement`
   - 新增 `_iter_group_flow_items()` / `_measure_group_flow_height()`
   - `build_grid_children()` 对带 card bg 的 group 不再只按顶层 text sum 估高
   - nested container、paired inline、margin gap 一起进入真实高度测量
   - 直接效果：Slide 4 四列 preset card 的高度、底部留白和内部 block 节奏明显收敛

4. `IR 保留 marginTop`
   - `build_shape_element()` / `build_text_element()` 现在都会保留 `marginTop`
   - 让 divider / 段落的上边距能够传递到后续 layout 阶段，而不是在 IR 层丢掉

新增测试：

- `test_build_text_element_wide_prose_adjusts_back_to_single_line()`
- `test_flow_gap_prefers_collapsed_margins_over_default_gap()`
- `test_layout_slide_elements_uses_next_margin_top_for_container_gap()`
- `test_build_elements_preserve_margin_top_metadata()`

本轮验证：

- `python3 -m py_compile scripts/export-sandbox-pptx.py scripts/test-export.py scripts/rigorous-eval.py` 通过
- `python3 scripts/test-export.py` 通过
- `python3 scripts/export-sandbox-pptx.py demo/blue-sky-zh.html output.pptx` 通过
- `python3 scripts/rigorous-eval.py`
  - `overflow = 0`
  - `overlap = 0`
  - `element gaps = 2`
  - `card containment = 0`
  - `color differences = 0`
  - `total actionable = 2`

当前页分：

- Slide 1 `9.2`
- Slide 2 `9.9`
- Slide 3 `9.7`
- Slide 4 `8.9`
- Slide 5 `10.0`
- Slide 6 `8.8`
- Slide 7 `8.5`
- Slide 8 `8.3`
- Slide 9 `9.9`
- Slide 10 `7.7`

当前状态的结论：

- generalized 分支当前 best state 更新为 `9.1/10`
- Slide 3 的主问题已经从“正文被误判成双行”消失
- Slide 4 还没过 `9.5`，但已经从 `7.3` 抬到 `8.9`
- 当前残余低分重新集中在：
  - Slide 4：`pill baseline` + `glass card width model`
  - Slide 10：closing command row 的 paragraph 组织

---

## Session 29 Continued：Phase 2.10 absolute Pt line-height + accent-card base/overlay + safer group sync

这轮继续按“程序整体性补能力”的方向推进，但结果也说明了一点：更稳的通用语义修复，不一定会让当前这份 deck 的分数继续单调上升。

新增并保留下来的通用修复有 6 条：

1. `numeric CSS line-height -> absolute Pt`
   - `apply_para_format(p, s, font_size_pt)` 不再把纯数字 `line-height` 原样喂给 PowerPoint
   - 现在会按 `Pt(font_size_pt * multiple)` 显式换算
   - 这是为了让段落 leading 更接近浏览器 / native PPT 的实际视觉，而不是依赖 PowerPoint 自己的二次解释

2. `explicit-break display heading uses TEXT_TO_FIT_SHAPE`
   - `export_text_element()` 对显式换行的大标题改成：
     - `tf.word_wrap = False`
     - `tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE`
   - 目标是降低 authored line 在不同 Office 环境里再次错误拆行的概率

3. `accent card` 改成 `rounded accent base + inset main card`
   - `measure_flow_box()` 不再额外生成 `_is_border_left` 子 shape
   - accent 信息保留在 bg shape 上，由 `export_shape_background()` 统一渲染
   - 对 `border-left: 4px+` 的圆角卡片，先画完整 rounded accent base，再叠加 inset rounded 主卡片
   - 直接修复：Slide 3 / 6 / 7 的大胶囊左上角不再被独立细条切坏

4. `card_group content-bottom sync`
   - `layout_slide_elements()` 新增按内容底部扩高背景的同步逻辑
   - centered / shrink-wrap card 的内部内容如果在 layout 阶段继续下推，背景 shape 会跟着扩高
   - 这让卡片底边不再停留在初始自然高度

5. `centered divider anchor`
   - 对 centered shrink-wrap 标题后的短 divider，x 可以继承上一标题的左锚点
   - 这比 generic center 更接近 native closing layout 的组织方式

6. `centered inline overlay pillify + inline inset guard`
   - `_export_inline_box_overlay()` 支持 `_pillify`
   - 居中的 `code/kbd + link` grouped row 现在能导出 pill 风格的 code bg
   - `_attach_pair_box_insets()` 对 `inline-block` / `inline-flex` 提前返回，避免单行 pill 双重 padding

本轮也明确记录了一条失败尝试，并已回退：

- `grid-group actual-bottom bg-height backfill`
  - 思路：统一按 grid/group 子元素真实最底部回写背景高度
  - 结果：会把整个 deck 从 `9.0+` 直接拉回 `8.8/10`
  - 结论：这条规则过于激进，不能作为 exporter 的通用默认值
  - 当前代码里已经完全回退，不在最终结果中

新增/更新的回归测试：

- `test_export_text_element_preserves_explicit_break_headings()`
  - 期望显式换行标题走 `TEXT_TO_FIT_SHAPE`
- `test_measure_flow_box_marks_descendants_in_flow_box()`
  - 额外断言不再生成独立 `_is_border_left` 子条，而是把 `borderLeft` 保留在 bg shape
- `test_card_group_layout_expands_bg_height_to_content_bottom()`
  - 验证 centered shrink-wrap card 的背景能随真实内容底部扩高

本轮验证：

- `python3 -m py_compile scripts/export-sandbox-pptx.py scripts/test-export.py scripts/rigorous-eval.py` 通过
- `python3 scripts/test-export.py` 通过
- `python3 scripts/export-sandbox-pptx.py demo/blue-sky-zh.html output.pptx` 通过
- `python3 scripts/rigorous-eval.py`
  - `overflow = 0`
  - `overlap = 0`
  - `element gaps = 2`
  - `card containment = 0`
  - `color differences = 0`
  - `total actionable = 2`

当前页分：

- Slide 1 `9.2`
- Slide 2 `9.5`
- Slide 3 `9.5`
- Slide 4 `8.9`
- Slide 5 `10.0`
- Slide 6 `8.7`
- Slide 7 `8.4`
- Slide 8 `8.2`
- Slide 9 `9.7`
- Slide 10 `7.7`

当前结论：

- generalized 分支的**当前已验证状态**是 `9.0/10`
- 这版把 line-height、accent-card 形状语义、card-group 高度同步收进了更稳的通用逻辑
- 但仍未达到“每页 9.5+”
- 当前低分主要集中在：
  - Slide 4：四张白卡高度模型 + pill baseline
  - Slide 6 / 7：accent card 右侧内容宽度和垂直节奏
  - Slide 10：closing command row 的 paragraph 组织
