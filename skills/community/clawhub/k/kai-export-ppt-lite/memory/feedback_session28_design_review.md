# Session 28: 设计先行 + Claude 对抗性评审

日期：2026-04-21

## 背景

在 `blue-sky-zh.html -> output.pptx` 的最新一轮导出中，整体分数达到 `8.2/10`，但剩余问题已经从“溢出/重叠/缺背景”收敛到“容器结构、复合 inline 行、table cell 富片段”。

结构性指标：

- overflow = 0
- overlap = 0
- card containment = 0

## 本轮决策

在继续写代码之前，先完成：

1. 架构方案文档
2. Claude 对抗性评审
3. 主文档与 checkpoint 记录
4. 先补测试，再改实现

## 核心方案

主文档见：

- `docs/session28-exporter-architecture-plan.md`
- `docs/session28-claude-adversarial-review.md`

本轮确认的主线能力：

- `flow_box`：把 `.layer/.g/.info/.co/.cmd` 这类卡片升级为一等容器
- `inline_fragments`：首轮仅支持 `code/kbd`
- richer table cells：`build_table_element()` / `export_table_element()` 打通 `cell.fragments`

## Claude 评审后采纳的约束

1. `flow_box` 与旧 `_card_group` 必须互斥，切流点在 `flat_extract()`
2. `inline_fragments` 首轮不能一口气覆盖 `link/separator`
3. table cell `fragments` 不能只改测量，不改渲染消费路径
4. 实施顺序必须串行：
   - 先 `.layer -> flow_box`
   - 再 `code/kbd fragments`
   - 最后 `.g + table cell render`

## 当前分数

- Slide 1: 9.6
- Slide 2: 9.7
- Slide 3: 7.0
- Slide 4: 7.8
- Slide 5: 10.0
- Slide 6: 7.0
- Slide 7: 7.1
- Slide 8: 8.2
- Slide 9: 8.5
- Slide 10: 7.5
- Overall: 8.2/10

## 下一步

先把 `flow_box` / `inline_fragments` / `table cell fragments` 的测试骨架补到 `scripts/test-export.py`，再开始迁移实现。

## 实施状态（Phase 1 已落地）

已完成第一条实现线：

- `measure_flow_box()` 已加入导出器
- `.layer` 类带背景 flex-row card 开始走 `flow_box` 容器路径
- 递归 container descendant 位移与递归渲染已接通

验证结果：

- `python3 scripts/test-export.py` 全通过
- 视觉总分仍为 `8.2/10`
- `rigorous-eval` 中 overlap 从 `3` 降到 `2`
- Position drift 的平均 Y 漂移明显下降，但 Slide 7 仍残留 grid + flow_box 的嵌套偏移问题

## 实施状态（Phase 2 已落地）

本轮继续沿着设计方案的第二条线实现：

- 新增 `extract_inline_fragments()`，把 `code/kbd` 升格为一等 inline fragments
- `build_text_element()` 改为消费 normalized fragments，去掉 HTML 缩进换行对导出的污染
- `build_table_element()` / `_compute_table_column_widths()` / `export_table_element()` 打通 `cell.fragments`
- 新增 `compute_inherited_style()`，补齐 table cell 的字号继承
- 明确把 `strong/b` 作为语义粗体，避免 bold 丢失

新增通过的测试：

- `test_extract_inline_fragments_code_kbd_support()`
- `test_table_cell_fragments_measure_kbd_sequence()`

验证结果：

- `python3 scripts/test-export.py` 全通过
- `python3 -m py_compile scripts/export-sandbox-pptx.py scripts/test-export.py scripts/rigorous-eval.py` 全通过
- `python3 scripts/rigorous-eval.py`：
  - overflow = 0
  - overlap = 0
  - card containment = 2
  - total actionable = 12

当前分数：

- Slide 1: 9.6
- Slide 2: 9.7
- Slide 3: 6.9
- Slide 4: 7.9
- Slide 5: 10.0
- Slide 6: 7.5
- Slide 7: 8.2
- Slide 8: 7.9
- Slide 9: 8.5
- Slide 10: 7.5
- Overall: 8.4/10

结论：

- `inline_fragments + table fragments` 这条通用路径是正收益，已经实质抬升 Slide 7/6/9
- 但 `.g + table` 仍停留在“shape + table”的扁平路径，导致 Slide 7 最后一行仍超出 card bottom
- Slide 10 的 closing row 也还没从“单文本框 + code_bg 后定位”升级为真正的 inline layout

## 实施状态（Phase 3 已落地）

这一轮直接参考 `demo/blue-sky-golden/*.png` 截图，不再只看 eval 数字，收敛了两个更通用的偏差来源：

1. **table card 的高度不再按 `len(rows) * 0.264` 粗估**
   - `build_grid_children()` 的 row height 预计算和 item height 计算都改为优先使用 `table.bounds.height`
   - 没有现成 `bounds.height` 时，再回退到真实 `row.height` 求和
   - 结果是 Slide 7 左侧导航 card 不再因为表格内容被低估而短一截

2. **centered inline command row 改为按内容宽度收紧**
   - `build_text_element()` 为带 `code/kbd` 或直接 `<a>` 子元素的行打上 `preferContentWidth`
   - `layout_slide_elements()` 在 center-aligned + maxWidth 场景下，对这类行优先使用 `inlineContentWidth`
   - 避免把 Slide 10 的 closing row 默认拉满整个 `720px` 列宽

新增通过的测试：

- `test_table_card_height_uses_actual_table_bounds()`
- `test_centered_inline_command_prefers_content_width()`

验证结果：

- `python3 -m py_compile scripts/export-sandbox-pptx.py scripts/test-export.py scripts/rigorous-eval.py` 通过
- `python3 scripts/test-export.py` 通过
- `python3 scripts/rigorous-eval.py`：
  - overflow = 0
  - overlap = 0
  - card containment = 0
  - total actionable = 10

当前分数：

- Slide 1: 9.6
- Slide 2: 9.7
- Slide 3: 6.9
- Slide 4: 7.9
- Slide 5: 10.0
- Slide 6: 7.5
- Slide 7: 8.2
- Slide 8: 7.9
- Slide 9: 8.5
- Slide 10: 7.5
- Overall: 8.4/10

结论：

- 这轮视觉分没有继续上升，但 `card containment` 已经从 `2 → 0`
- Slide 10 的最大 X 漂移从 `0.908"` 降到 `0.729"`，说明“居中但不应拉满整栏”的判定方向是对的
- 剩余问题已经继续向“结构相似度”收敛：Slide 4 的 mixed inline badge、Slide 7/8 的 table-like row 结构、Slide 3/6 的 extra shapes

## 失败尝试（已回退）

尝试在 `layout_slide_elements()` 中全局保留背景 shape 的预计算高度下界，想直接兜住 table card。

结果：

- 虽然能放大部分 card 背景，但同时把 stat/info 等其他背景 shape 也一并拉高
- 全局回归明显，导致多页背景高度失真

处理：

- 已当场回退该 patch
- 结论是：这个问题必须通过“特定容器升格”，而不是全局放宽背景 shape 高度
