# 当前工作断点 - HTML→PPTX 优化

## 优化前必做 Preflight（从本轮起强制执行）

每次开始新一轮优化前，先读文档，再动代码；不要直接凭记忆开修。

固定顺序：

1. 先读 `docs/设计与实践文档.md`
2. 再读 `memory/work-checkpoint.md`
3. 再读最近 2-4 份相关的 `memory/feedback_session*.md`
4. 然后才允许开始：
   - 截图对比
   - 根因分析
   - 写测试
   - 改 exporter

本规则要解决的不是“少看一次文档”这种形式问题，而是避免重复犯这几类错：

1. 已经确认过的根因，下轮又按旧假设重复修一遍
2. 已经回退过的失败方案，下轮又重新试一次
3. 看了旧 montage / 旧 summary，就误以为最新导出还存在同样问题
4. 没先核 PPTX 实体几何 / XML，就根据预览或 `python-pptx` 回读对象误判

当前和 `data-story` / pill / wrapper / font 相关的最近必读记录：

- `memory/feedback_session33_data_story_wrapper_layout.md`
- `memory/feedback_session34_pill_pair_packer.md`
- `memory/feedback_session35_block_pill_component_path.md`
- `memory/feedback_session36_latin_pill_font_mapping.md`

执行口径：

1. 优化前先在 commentary 里明确说“先看文档/断点/最近反馈”
2. 如果这轮问题与近期 session 明显相关，先复述上一轮已确认结论，再动代码
3. 任何新经验都必须在收口时补回：
   - `docs/设计与实践文档.md`
   - `memory/work-checkpoint.md`
   - 对应 `memory/feedback_session*.md`

## Session 32：contract sync pipeline 已落地，但质量主提升还在 solver 层

这轮真正完成了 Session 31 里定下来的第一步：

1. 新增 `scripts/sync-slide-creator-contracts.py`
2. 新增 `contracts/slide_creator/manifest.json`
3. 正式补齐 `contracts/slide_creator/presets/data-story.json`
4. 扩充所有 preset contract：
   - `component_selectors`
   - `component_slot_models`
   - `layout_variations`
   - `producer_detection`
   - `observed_component_classes`
5. 修正 `data-story` 装饰层 drift：
   - 真实 demo 是 `.slide::before`
   - 不只是 `body::before`
6. exporter 支持 `var(--grid-line)` + `opacity` 的网格背景解析

当前验证：

- `python3 scripts/test-export.py` 通过
- `python3 scripts/export-sandbox-pptx.py demo/data-story-zh.html demo/data-story-output.pptx` 通过
- `python3 scripts/compare-html-ppt-visual.py ...` 通过

但这轮也明确说明了一个事实：

- contract sync pipeline 已经落地
- `data-story` 仍然只有 `8.88/10`

原因不是“同步没用”，而是：

- 现在只是把上游 contract 成功搬进来了
- 还没有让 `ds-kpi-card / feat-card / install-row / ds-split-layout`
  这些组件真正按 `component_slot_models` 走 solver

当前最正确优先级：

1. `ds-kpi-card` solver
2. `feat-card` solver
3. `install-row` solver
4. `ds-split-layout` solver
5. 再跑 `data-story` 逐页截图对比，把 `2 / 4 / 6 / 7` 拉过 `9.5`

## 当前分数
- Slide 1: 9.2 | Slide 2: 9.5 | Slide 3: 9.5 | Slide 4: 8.9 | Slide 5: 10.0 ✅
- Slide 6: 8.7 | Slide 7: 8.4 | Slide 8: 8.2 | Slide 9: 9.7 | Slide 10: 7.7
- 总体: 9.0/10（当前已验证状态；上一轮 9.1/10 为历史更高分，但已不是当前 generalized 输出）

## Session 31：slide-creator contract/reference 执行缺口已确认

这轮明确确认了一件事：

- Session 30 的 `reference / contract / hints` 路线只落了 **minimal path**
- 真正决定导出质量的 **contract -> component solver -> layout** 还没有接上

已落地：

1. `ExportHints` schema
2. producer detection
3. vendored preset contracts
4. `collect_export_context()` / contract resolve / validate

没落地：

1. `slide-creator` upstream contract sync pipeline
2. upstream version manifest / drift check
3. contract 驱动的 component solver registry
4. `ds-kpi-card / feat-card / install-row / ds-split-layout` 这些组件的正式布局器

这也是为什么即使已经“引用了 slide-creator reference / contract”，`data-story` 这类 deck 的导出仍然只有 `8.88/10`：

- 现在主要只是“认得它是谁”
- 还做不到“按它的组件契约来排版”

当前正确优先级已经切换为：

1. 新增 `scripts/sync-slide-creator-contracts.py`
2. 增加 upstream version manifest
3. 把 contract 真正接到布局器
4. 第一批 component solver：
   - `ds-kpi-card`
   - `feat-card`
   - `install-row`
   - `ds-split-layout`

## Session 42：下一阶段从“组件几何”切到“排版契约”

`Chinese Chan` 的复盘已经把当前真正的短板钉死了：

- reference 明确写了字体与排版节奏
- exporter 目前只同步了布局契约，没有同步排版契约

因此下一阶段的主线，不再是继续按页修，而是补这条 render 前 contract enforcement 主链：

1. 为 `Chinese Chan` 新增 vendored contract
2. 扩 `sync-slide-creator-contracts.py`：
   - `typography`
   - `line_break_contract`
   - `font_features`
3. parse 阶段保留：
   - `source_text_raw`
   - `has_authored_breaks`
4. 新增 `resolve_text_contract()`，供 guard / layout / render / eval 共享
5. 新增 `guard_validate_export.py`
6. 新增 typed eval boundary：
   - `producer_contract`
   - `typography_fidelity`
   - `break_fidelity`
   - `component_integrity`
   - `render_integrity`

### 自评后已经锁死的边界

1. typography contract 不能写成“必须等于某个具体字体名”，而是：
   - `family_mode`
   - `candidate_stack`
   - `safe_fallback_policy`
2. break policy 必须分级：
   - `preserve`
   - `prefer_preserve`
   - `allow_reflow`
3. authored break overflow 的修复顺序必须是：
   - 扩文本框
   - 扩卡片高度
   - 调整组件 gap
   - 最后才是 contract 允许下的 shrink-fit
4. traceability 首轮只做 sidecar JSON，不直接 patch PPTX metadata
5. typed eval 首轮增量接入，不替代现有 visual compare

### 当前最正确下一步

1. 先实现 `Chinese Chan` 的 typography / break contract
2. 再把这套 resolver / guard / eval 跑通
3. 最后才回到 deck 级视觉分确认，不要反过来

## Session 43：Chinese Chan 的 typography / break contract 已实现一轮

本轮不是继续围着页面肉眼调，而是把 Session 42 里定下来的 text contract 真正接进了 exporter：

1. `scripts/sync-slide-creator-contracts.py` 已正式同步 `Chinese Chan`
2. vendored contract 已包含：
   - `typography`
   - `line_break_contract`
3. exporter 运行时已消费：
   - `preserveAuthoredBreaks`
   - `preferWrapToPreserveSize`
   - `shrinkForbidden`
4. `prefer_preserve` 现已落成真实导出行为：
   - `word_wrap = True`
   - `SHAPE_TO_FIT_TEXT`

### 当前口径

- `Chinese Chan overall = 9.68/10`
- `P1 9.8 / P2 9.5 / P3 9.5 / P4 9.8 / P5 9.8 / P6 9.5 / P7 9.8 / P8 9.7`
- `rigorous-eval`：`overflow=0 overlap=0 element_gaps=0 card_containment=0 total_actionable=0`

### 本轮最关键经验

1. `preserve` 和 `prefer_preserve` 不能混用  
   `zen-title` 这种没有显式 `<br>`、但依赖 authored width rhythm 的标题，必须用 `prefer_preserve`

2. 留白型 serif preset 不能只看 visual score  
   自动评分容易被大面积白底掩盖，必须同时看：
   - montage
   - PPTX XML
   - text frame 的 `wrap / auto_size`

3. 验证字体/换行必须看实体，不看推断  
   先看：
   - `ppt/slides/slideN.xml`
   - `wrap="square" / spAutoFit / normAutofit`
   - `latin/ea` typeface
4. 本机 `which soffice` 不等于真的可渲染  
   当前 `/opt/homebrew/bin/soffice` 指向不存在的 LibreOffice.app，因此 `compare-html-ppt-visual.py` 会静默回退到粗糙 preview；留白型 serif preset 不能把这份 `summary.json` 当作真实 Office 渲染分

### 下一步

如果继续拉 `Chinese Chan`：

## Session 45：P8 seal / command fidelity 已收口到通用规则

这轮把 `Chinese Chan P8` 剩余的两个问题收成了可执行规则：

1. `zen-seal` 这类无文字、显式尺寸的 decoration shape 也必须保留 border 契约  
   之前 IR 里只保留了 `backgroundColor/backgroundImage/borderRadius`，导致最终 PPTX 根本没有边框。

2. centered command card 的对齐参照系必须是 authored content column  
   不能错误地按整页中心检查。对 `Chinese Chan`，正确参照是与 `slide8_title` 同一列中心。

3. 纯 border shell 默认不再加 light shadow  
   只有真正带 fill 的 shape 才允许加阴影，更接近 source HTML 的平面边框气质。

当前已验证：

- `python3 scripts/test-export.py` 全绿
- `python3 scripts/export-sandbox-pptx.py demo/chinese-chan-zh.html demo/chinese-chan-output.pptx` 通过
- `python3 scripts/rigorous-eval.py --sandbox demo/chinese-chan-output.pptx --golden demo/chinese-chan-output.pptx --skip-visual`
  - `overflow = 0`
  - `overlap = 0`
  - `element gaps = 0`
  - `card containment = 0`
  - `total actionable = 0`

XML 实体已确认：

- seal：`fill = F5E8E8`, `line = C41E3A`
- command：`algn="ctr"`，并在 authored column 内 shrink-wrap 居中

1. 不再扩 contract 字段
2. 只盯 `P1 / P3 / P8` 的 typography fidelity
3. 优先检查 compare 预览链是否准确反映 PPTX XML，而不是先怀疑 contract 没生效

## Session 30：通用 Exporter + Producer-Aware Hints 方案已收口

本轮没有继续改代码，而是把“通用 HTML 导出”和“已知 producer 增强路径”之间的分层正式定稿：

- 主方案：`docs/session30-exporter-hints-and-contracts-plan.md`
- 自评：`docs/session30-self-adversarial-review.md`
- Claude 评审：`docs/session30-claude-adversarial-review.md`

这轮收口后的硬约束：

1. 运行时不允许跨仓库读取 `slide-creator`
2. `BRIEF.json` 不作为运行时输入
3. `ExportHints` 是可选运行时协议，不是第二套 IR
4. slide 级语义走 HTML 本体：
   - `data-export-role`
   - `data-export-intent`
5. `slide-creator` 只是第一个 `ProducerAdapter`
6. hints / contract 版本策略固定为：
   - `contract_ref`
   - `contract_id`
   - `contract_version`
   - `producer_version_range`
7. `enterprise-dark` 已被明确写入后续 gate 和成功标准

当前最正确的下一步，不是继续修某一页，而是按 Session 30 phase 顺序推进：

1. `Phase 2`
   - `ExportHints` schema
   - producer detection
   - `ProducerAdapter`
   - `slide-creator adapter` minimal path
2. `Phase 3`
   - vendored contracts
   - drift/version checks
3. `Phase 4`
   - generic core 消费 hints
4. `Phase 5`
   - producer-aware corpus + eval gate

## Session 29 Phase 2.10：line-height Pt + accent-card base/overlay + safer card-group sync

本轮新增的是 6 条通用修复，不是按页打补丁：

1. `numeric CSS line-height -> absolute Pt`
   - `apply_para_format()` 把纯数字 `line-height` 显式换成 `Pt(font_size_pt * multiple)`
   - 避免 PowerPoint 再按自己的相对 leading 解释段落

2. `explicit-break heading -> TEXT_TO_FIT_SHAPE`
   - 显式换行的大标题不再强制 `auto_size = NONE`
   - 改成 `word_wrap = False + TEXT_TO_FIT_SHAPE`
   - 目标是降低 authored line 在不同机器上再次错误拆行的概率

3. `accent card` 统一改成 `rounded accent base + inset main card`
   - 不再导出独立 `_is_border_left` 左侧细条
   - Slide 3 / 6 / 7 的大胶囊左上角不再被细条切坏

4. `card_group content-bottom sync`
   - shrink-wrap / centered card 内部内容下推时，背景 shape 会跟随扩高
   - 避免正文压住卡片底边

5. `centered divider` 可锚定上一标题的左坐标
   - 用于 closing layout，不再只按 generic center 摆放短横线

6. `centered command-row overlay` 走 pill 语义
   - code/kbd inline overlay 可按行高导出 pill，而不是普通圆角矩形
   - 同时跳过 `inline-block` / `inline-flex` 的重复 box insets，避免单行 pill 双重 padding

本轮有一条失败尝试已经回退：

- `grid-group actual-bottom bg-height backfill`
  - 统一按实际子元素底部回填所有 grid/group 卡片高度
  - 会把 deck 从 `9.0+` 拉回 `8.8/10`
  - 已完全回退，不在当前结果中

本轮验证：

- `python3 -m py_compile scripts/export-sandbox-pptx.py scripts/test-export.py scripts/rigorous-eval.py`
- `python3 scripts/test-export.py`
- `python3 scripts/export-sandbox-pptx.py demo/blue-sky-zh.html output.pptx`
- `python3 scripts/rigorous-eval.py`

当前结构指标：

- `overflow = 0`
- `overlap = 0`
- `element gaps = 2`
- `card containment = 0`
- `color differences = 0`
- `total actionable = 2`

当前最值得继续攻的点：

1. Slide 10：closing command row 的 paragraph model
2. Slide 4：四张白卡高度模型 + pill baseline
3. Slide 6 / 7：accent card 右侧内容宽度和节奏

## Session 29 Phase 2.7：命令行 inline overlay + baseline alignment 收敛

本轮继续补的是两条程序级能力，不是单页补丁：

1. `flex-row baseline alignment`
   - `build_grid_children()` 对 plain flex row + `align-items: baseline` 增加基线估算
   - 通过 `_estimate_group_baseline_in()` 按首个文本行盒估算 baseline，再做 cross-axis offset
   - 直接收益：Slide 4 顶部 `按内容类型自动匹配` 胶囊不再和标题顶对齐，`y = 2.271 → 2.347`，更接近 golden `2.465`

2. `single-line mixed inline command row`
   - `inline_fragments_to_segments()` / `segments_to_lines()` 现在保留 fragment 级 `fontFamily` / `letterSpacing`
   - `export_text_element()` 新增 `_layout_single_line_fragments()` + `_export_inline_box_overlay()`
   - 对“带 `code/kbd` 且同时带 link 的单行 mixed inline 行”导出真实 inline bg overlay
   - 规则已收窄到 command/CTA row，不再把 Slide 3/6 的正文 inline code/kbd 误导成额外 shape

3. `fragment style snapshot` 补全
   - `_fragment_style_snapshot()` 新增 `fontFamily` / `letterSpacing`
   - 混排 run 的 monospace/code 风格不再在 segment 层丢失

新增/更新的回归覆盖：

- `test_build_grid_children_flex_row_preserves_component_width_and_pairing()`
  - 现在额外断言 baseline 下胶囊会被压到标题下方
- `test_flat_extract_mixed_inline_code_uses_inline_overlays()`
  - 确保 command row 走 text-bound inline overlay，而不是旧的 detached code_bg sibling

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

当前状态要明确两点：

- Slide 10 的 code bg 已经不再靠后定位 hack，而是 exporter 内的真实 inline overlay shape，位置为：
  - bg `x=4.769, y=4.951, w=2.865, h=0.180`
  - text row `x=4.232, y=4.935, w=4.867, h=0.213`
- 但总体视觉分仍停在 `8.6/10`，剩余 gap 依旧集中在 Slide 10 command row 的 paragraph 组织
- generalized 分支现在更像“能力正确但 paragraph model 还没追上 golden”，而不是结构性错误

## Session 29 设计重置（Phase 1-2 已落地）

- 设计文档：`docs/session29-exporter-generalization-plan.md`
- Claude 对抗性评审：`docs/session29-claude-adversarial-review.md`
- 当前 generalized 分支为 `8.5/10`
- Session 28 Phase 3 的视觉 best state `8.4/10` 已被超过
- Phase 1（fixture/corpus + eval gate）和 Phase 2（flow_box / grouped inline / presentation_rows 首轮接线）都已落地

Claude 评审后确认的硬约束：

1. `compound_inline_group` 不能新增成第二套 IR，只能作为 `inline_fragments v2 grouped mode`
2. `presentation_rows` 不能靠“固定两列”判断，要按语义密度分类
3. corpus 不能只用 Blue Sky，至少扩到：
   - `references/blue-sky-starter.html`
   - `demos/blue-sky-zh.html`
   - `demos/slide-creator-intro.html`
   - 手写 HTML fixture
   - `demos/swiss-modern-zh.html`
4. 实施顺序改为：
   - 先补 fixture/corpus + eval 门槛
   - 再做 `flow_box` 最小承载升级
   - 再做 grouped inline
   - 再做 `presentation_rows`
   - 最后退役 hardcode
5. `flow_box` 迁移契约必须显式：
   - 进入 `flow_box` 的子元素统一打 `_in_flow_box=True`
   - 同时清空 `_card_group`
   - layout/render loop 禁止这些元素再回到旧 `card_group` 路径
6. `GOLDEN_FIRST_Y` 的替代锚点固定为 `paddingTop + content_top`，不再按 slide index 偏移

## Session 29 Phase 1：fixture/corpus + eval gate 已落地

本轮实际已完成：

1. 新增手写 corpus fixture：
   - `tests/fixtures/export-corpus/handwritten-card-list-table.html`
   - 覆盖 title/card/list/command-row/presentation-like rows/real data table
2. `scripts/test-export.py` 新增 3 个 gate：
   - `test_export_corpus_parse_smoke()`
   - `test_handwritten_fixture_covers_core_patterns()`
   - `test_handwritten_fixture_structural_eval_gate()`
3. `scripts/rigorous-eval.py` 新增 `collect_eval_summary()`，并支持：
   - `--golden`
   - `--sandbox`
   - `--skip-visual`
4. 当前 corpus 入口已锁为：
   - `demo/blue-sky-zh.html`
   - `demo/slide-creator-intro.html`
   - 手写 fixture
   - `slide-creator/references/blue-sky-starter.html`
   - `slide-creator/demos/swiss-modern-zh.html`

验证结果：

- `python3 -m py_compile scripts/test-export.py scripts/rigorous-eval.py` 通过
- `python3 scripts/test-export.py` 通过
- 手写 fixture 自举导出后的 structured eval 为：
  - `overflow = 0`
  - `overlap = 0`
  - `element gaps = 0`
  - `card containment = 0`
  - `color diffs = 0`
  - `total actionable = 0`

## Session 29 Phase 2：核心能力接线已落地

本轮已完成：

1. `flow_box` 迁移契约
   - descendants 统一 `_in_flow_box=True`
   - 同时清空 `_card_group`
   - layout loop 禁止回到旧 `card_group` 路径
2. `inline_fragments v2 grouped mode`
   - 支持 `badge/link/icon`
   - grouped metadata 已接入 `extract_inline_fragments()`
   - grouped inline 参与内容宽度测量和 `preferContentWidth`
3. `presentation_rows`
   - `_classify_table_ir()` 已分流展示型 row 结构与真实数据表
   - 首轮渲染仍走 table renderer 的稳态路径
4. 新增回归测试：
   - `test_extract_inline_fragments_grouped_badge_and_link()`
   - `test_measure_flow_box_marks_descendants_in_flow_box()`
   - `test_build_table_element_classifies_presentation_rows()`
   - `test_build_table_element_keeps_real_data_tables()`

当前验证结果：

- `python3 -m py_compile scripts/export-sandbox-pptx.py scripts/test-export.py scripts/rigorous-eval.py` 通过
- `python3 scripts/test-export.py` 通过
- `python3 scripts/export-sandbox-pptx.py demo/blue-sky-zh.html output.pptx` 通过
- `python3 scripts/rigorous-eval.py`
  - `overflow = 0`
  - `overlap = 0`
  - `element gaps = 8`
  - `card containment = 0`
  - `total actionable = 8`

结论：

- 结构面继续收敛，当前 generalized 分支视觉分是 `8.5/10`
- 当前 remaining actionable 只剩 2 个，全部集中在 Slide 10 closing command row
- `presentation_rows` 的 IR 分流可以保留，但专用 visual renderer 需要下一轮单独优化

## Session 29 Phase 2.5：通用收敛修复已落地

新增的通用修复：

1. `flow_box` 内容顶部 padding 回写
   - 防止 layer/info card 文本顶到卡片上缘
2. `border-left: 4px` accent card 边框抑制
   - 防止导出 top/right/bottom 冗余边框 shape
3. centered grouped inline width 收敛
   - `code + link` 的 centered command row 不再过度 shrink-wrap

最新 `rigorous-eval`：

- `overflow = 0`
- `overlap = 0`
- `element gaps = 2`
- `card containment = 0`
- `total actionable = 2`

最新页分：

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

## Session 29 Phase 2.6：组件宽度/字体栈收敛已落地

本轮新增的通用修复：

1. `font stack` 顺序尊重 CSS 声明顺序
   - `map_font()` 不再按 `_FONT_MAP` 的字典顺序抢先命中
   - 改为先按 CSS font-family 列表顺序做精确匹配，再做包含匹配
   - 直接效果：Blue Sky 默认中文标题不再错误落到 `Microsoft YaHei`，而会优先使用 `PingFang SC`

2. `letter-spacing` 支持相对单位
   - `_estimate_text_width_px()` / `set_letter_spacing()` 支持 `em` / `rem`
   - 不再把 `0.05em` 这类组件字距当成固定 `16px` 基准

3. `flex-row` 单行组件宽度不再走旧字符启发式
   - `build_grid_children()` 里的 plain flex row 宽度分配，新增 `_measure_preferred_child_width_in()`
   - 对带背景/边框且 `preferContentWidth=True` 的 child，直接复用 `build_text_element()` 的组件测量宽度
   - 直接效果：Slide 4 顶部 pill 不再被压回旧的窄宽度

4. grid/flex 子项的 bg/text pairing 回写到构建阶段
   - `build_grid_children()` 给带背景的 text/leaf container 子项补上 `_pair_with`
   - 形状和文本共享同一组布局锚点
   - 直接效果：胶囊文字不再脱离背景单独堆叠

5. grouped inline badge 增加单行胶囊高度下限
   - `build_text_element()` 把“有背景 + grouped inline”的单行组件视为 `component_like_inline`
   - 保留 `forceSingleLine`
   - 统一使用 capsule-height floor
   - 直接效果：`Blue Sky 当前` 这类 badge group 不再被压到 `0.15"` 的低矮高度

新增测试：

- `test_build_text_element_grouped_inline_badge_keeps_single_line_height()`
- `test_build_grid_children_flex_row_preserves_component_width_and_pairing()`
- `test_map_font_respects_css_stack_order()`

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

当前 best state：

- Slide 1 `9.2`
- Slide 2 `9.7`
- Slide 3 `7.9`
- Slide 4 `7.3`
- Slide 5 `10.0`
- Slide 6 `8.1`
- Slide 7 `8.3`
- Slide 8 `8.4`
- Slide 9 `9.7`
- Slide 10 `7.9`

当前最集中的剩余问题仍然只有一类：

- Slide 10 closing command row 的 paragraph 组织与 golden 不同
- 目前视觉上 code pill 已正确 rounded + behind text
- 但 compare/eval 仍把 golden 的“三段 paragraph 文本框”与当前单段 grouped inline 文本框视为 gap

## 已完成的修复（在 scripts/export-sandbox-pptx.py）
1. code_bg shape 双向搜索定位（line ~2912-2970）
2. step 圆圈 CSS 尺寸修复（line ~1771-1802）+ _use_css_dims 防止 layout 覆盖（line ~2290-2293）
3. **borderLeft info bar 宽度修复（Session 25，3 处）**：
   - `flat_extract` all_inline 路径（line ~1522）：`4px` border-left → `shape_w = max_w_in * 1.15`
   - `layout_slide_elements` paired shape（line ~2779）：同样应用展开宽度
   - post-layout sync pass（line ~2871）：跳过 `4px` border-left shape 的宽度同步
   - 关键：检查 `'4px' in bl` 而非 `not bl.startswith('0px')`，避免误判 `1px solid rgba(...)`
4. **ul.bl 误用 shrink-wrap 修复（Session 26，1 处）**：
   - `flat_extract`（line ~1580）：`child_cw_override` 仅在 `bg_shape` 存在时生效，避免内层 `ul.bl` 把 `li` 宽度收窄到 `2.80"` 并误判成双行
   - 效果：Slide 2 `7.8→9.7`，Slide 9 `7.1→8.5`，Slide 8 `7.9→8.2`
5. **code bg shape 创建（Session 27）**：
   - `flat_extract` 文本叶子路径：`<code>` 作为首个子元素时创建独立 bg shape
   - all_inline 路径：`<code>` 子元素也创建 code bg shape
   - rgba 背景合成：将 rgba 颜色复合到纯色（金色参考使用复合色）
6. **Session 28 Phase 1：`flow_box` 容器基础设施**
   - 新增 `measure_flow_box()`，把带背景的 flex-row card 提升为一等容器
   - 新增 `_shift_container_descendants()` 与递归 `_render_layout_element()`
   - `build_grid_children()` 支持 `flow_box` 子容器高度计算与布局
   - 测试新增：
     - `test_layout_slide_elements_flow_box_advances_current_y_correctly()`
     - `test_measure_flow_box_intrinsic_height_for_layer_card()`
   - 当前结果：视觉总分仍 `8.2/10`，但 `rigorous-eval` 从 `overlap=3` 收敛到 `overlap=2`，`position drift` 的均值明显下降
7. **Session 28 Phase 2：`code/kbd inline_fragments` + table cell fragments**
   - 新增 `extract_inline_fragments()`、`inline_fragments_to_segments()`、fragment 宽高测量 helper
   - `build_text_element()` 改为消费 normalized fragments，修复 `kbd/code/strong` 的 run 语义和 HTML 缩进换行污染
   - `build_table_element()` / `_compute_table_column_widths()` / `export_table_element()` 打通 `cell.fragments`
   - 新增 `compute_inherited_style()`，补齐 table cell 的字体继承；`strong/b` 明确强制 bold
   - 测试门槛已转正：
     - `test_extract_inline_fragments_code_kbd_support()`
     - `test_table_cell_fragments_measure_kbd_sequence()`
   - 当前结构指标：
     - `overflow = 0`
     - `overlap = 0`
     - `card containment = 2`
     - `total actionable = 12`
   - 直接收益：Slide 7 `7.1→8.2`，Slide 6 `7.0→7.5`，Slide 9 维持 `8.5`
8. **Session 28 Phase 3：参考截图对照后的收敛修复**
   - table/card 高度计算改为使用 `table.bounds.height` / 实际 `row.height`，不再用 `len(rows) * 0.264` 的扁平估算
   - `build_text_element()` 为带 `code/kbd/link` 的 centered inline 行打上 `preferContentWidth`
   - `layout_slide_elements()` 对这类行改为按内容宽度收紧，而不是默认拉满 `maxWidth`
   - 新增测试：
     - `test_table_card_height_uses_actual_table_bounds()`
     - `test_centered_inline_command_prefers_content_width()`
   - 当前结构指标：
     - `overflow = 0`
     - `overlap = 0`
     - `card containment = 0`
     - `total actionable = 10`
   - 直接收益：Slide 7 containment 清零；Slide 10 最大 X 漂移 `0.908"→0.729"`，但视觉分仍为 `7.5`

## 下一步优先级
### P3：收敛 Slide 7 回归，同时保留 `presentation_rows` IR
- 已完成，generalized 分支已回到 `8.5/10`

### P4：收敛 Slide 10 closing command row
- 当前仍只剩 2 个 actionable，都在这条命令行
- 已完成的前置收敛：
  - `code/kbd` overlay 跟随整行 row height，不再是 `0.18"` 的窄方块
  - 混合字体栈优先解析为 `Microsoft YaHei`，跨机器字宽更稳
  - mixed-script 显式换行标题已增加 width guard，Slide 1 主标题文本框 `4.667"→4.700"`
- 下一步重点：
  - grouped inline 的 paragraph model
  - `code / separator / link` 的段落组织是否要对齐 golden 的三段式文本框
  - 在不引入 deck-specific hardcode 的前提下抬 Slide 10

### P5：继续补能力级 fixture
- 还缺：
  - `nested_badge_group`
  - `centered_command_with_code_and_link`
  - `flow_box_with_grouped_inline_children`
  - `flow_box_with_presentation_rows_children`

### P6：退役 hardcode
- 优先审视：
  - `GOLDEN_FIRST_Y`
  - 顶层 pill 固定 content width
  - code_bg 纯后定位搜索
- 替代锚点统一为 `paddingTop + content_top`

## 本轮设计文档
- docs/session29-exporter-generalization-plan.md
- docs/session29-claude-adversarial-review.md

## 对抗性评审结论
- Claude 结论：需要先改方案
- 已采纳的关键修改：
  1. `compound_inline_group` 退回为 `inline_fragments` 的 grouped 模式，不新开第二套 IR
  2. `presentation_rows` 改为语义密度分类，不靠固定两列
  3. corpus 扩到 Blue Sky 之外，加入 intro deck、手写 fixture 和非 Blue Sky preset
  4. 实施顺序前移 `flow_box` 最小承载升级
  5. `_in_flow_box=True` / 清空 `_card_group` 成为显式迁移契约
  6. `total actionable` 与 `GOLDEN_FIRST_Y` 替代策略都已在方案中定义

## 关键文件
- scripts/export-sandbox-pptx.py（主导出引擎，~4100 行）
- scripts/test-export.py（回归测试 + corpus gate）
- scripts/rigorous-eval.py（structured eval gate）
- tests/fixtures/export-corpus/handwritten-card-list-table.html（手写 corpus fixture）
- scripts/compare-visual-comprehensive.py（对比工具）
- demo/blue-sky-golden-native.pptx（golden 参考）
- demo/blue-sky-zh.html（输入 HTML）
- docs/设计与实践文档.md（完整设计文档）
- docs/session29-exporter-generalization-plan.md（本轮设计方案）
- docs/session29-claude-adversarial-review.md（Claude 评审）
- 运行：python3 scripts/export-sandbox-pptx.py demo/blue-sky-zh.html output.pptx --no-chrome
- 对比：python3 scripts/compare-visual-comprehensive.py demo/blue-sky-golden-native.pptx output.pptx

## 最新状态（Session 29 Phase 2.9）
- generalized 分支当前 best state：`9.1/10`
- 当前页分：
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
- 结构指标：
  - `overflow = 0`
  - `overlap = 0`
  - `card containment = 0`
  - `color differences = 0`
  - `element gaps = 2`
  - `total actionable = 2`

本轮新增的底层规则：

1. `wide prose single-line fallback`
   - 宽正文段落的 adjusted-fit 判定允许轻微负 overflow
   - 修复了“已经放得下但仍被锁成 2 行”的情况
   - 直接拉升 Slide 3 `.layer` 卡片正文高度与整体节奏

2. `margin-aware block flow`
   - 新增 `_flow_gap_in()`，layout 不再一律追加默认 gap
   - block 间距改为优先使用 `margin-bottom / margin-top` 的 collapsed 结果
   - divider / subtitle / nested container 的节奏更接近 browser/golden

3. `group flow height measurement`
   - 新增 `_iter_group_flow_items()` / `_measure_group_flow_height()`
   - grid/card group 高度计算不再只看顶层 text sum
   - nested container、margin gap、paired inline 文本都进入真实高度测量

4. `marginTop` 元数据打通到 IR
   - `build_shape_element()` / `build_text_element()` 现在都保留 `marginTop`
   - 让后续 block flow gap 计算能拿到 divider / 段落的上边距

新增回归覆盖：

- `test_build_text_element_wide_prose_adjusts_back_to_single_line()`
- `test_flow_gap_prefers_collapsed_margins_over_default_gap()`
- `test_layout_slide_elements_uses_next_margin_top_for_container_gap()`
- `test_build_elements_preserve_margin_top_metadata()`

下一步优先级更新：

- `P4` 仍然是 Slide 10 closing command row
  - 当前 2 个 actionable 仍全部集中在这里
  - 需要继续打 `code / separator / link` 的 paragraph model
- `P5` 改为收敛 Slide 4
  - 剩余问题不再是结构错乱，而是 `pill baseline` 和 `glass card width model`
  - 可以继续沿“margin-aware block flow / component width model”这条通用路径推进

## 最新状态（Session 33: data-story wrapper + compare refresh）

- 本轮不是继续修单页 `x/y`，而是补了一条通用 wrapper 规则：
  - `display:flex|inline-flex + flex-direction:column`
  - 且带 `max-width / text-align:center / align-items:center / auto margins`
  - 不能再在 `flat_extract()` 里被扁平打散
- `data-story` 现在的外层 centered stack 会被保成真实 relative container：
  - Slide 1 hero group
  - Slide 7 install + KPI wrapper
- wrapper packing 阶段的 `maxWidth` 解析也收正了：
  - 不再直接用 `parse_px()`
  - 改为 `_resolve_css_length_with_basis()`
- compare 流程新增一个硬规则：
  - **每次重导出后必须 fresh 跑 `compare-html-ppt-visual.py`**
  - 不能继续盯旧 `montage/summary.json`

### 当前 data-story best state

- 输出：`demo/data-story-output.pptx`
- 对比：`demo/data-story-visual-compare/summary.json`
- 最新逐页分：
  - Slide 1 `9.2`
  - Slide 2 `8.7`
  - Slide 3 `9.0`
  - Slide 4 `8.6`
  - Slide 5 `9.1`
  - Slide 6 `8.7`
  - Slide 7 `8.9`
  - Slide 8 `9.2`
- 当前整体：约 `8.93/10`

### 本轮记录下来的“不要再犯”

1. 不要把带 authored width cap 的 centered column wrapper 打散成顶层散件。
2. 不要在 wrapper packing 里直接用 `parse_px()` 吃 `min()/max()/clamp()/vw`。
3. 不要在旧 compare 截图上继续修布局；必须先 fresh 跑 compare。
4. 当截图和直查 PPTX 不一致时，先核：
   - text box bounds
   - run font size
   - run font family

### 下一步优先级

- `P1`: 继续核定 display heading / hero KPI 在 compare renderer 下的表现，避免被 stale preview 或 autosize 误导
- `P2/P4/P6/P7`: 继续深化 data-story 组件 solver，而不是再拖散点坐标
  - `metric_card`
  - `style_card`
  - `feature_card`
  - `split_layout`

## 最新状态（Session 34: paired pill packer regression fix）

- `data-story` 的 `P1 / P8` 单行胶囊回归已经修掉
- 根因不是 pill builder，而是 centered wrapper packer 把 `_pair_with` 配对元素拆成了两个顺序 block
- `_pack_relative_block_container()` 现在：
  - 会先把同一个 `_pair_with` 的 children 聚成一个 packed item
  - 再按 item 参与纵向 block flow
  - 居中时按 item 居中，不再逐 child 居中
- wrapper `maxWidth` 也在这里一起收正：
  - 继续使用 `_resolve_css_length_with_basis()`
  - 不允许退回 `parse_px()`

### 实体验证

- `python3 -m py_compile scripts/export-sandbox-pptx.py scripts/test-export.py`
- `python3 scripts/test-export.py`
- 当前 `test-export.py` 已重新全绿

### 新增回归测试

- `test_data_story_centered_wrapper_keeps_paired_pills_overlaid()`

它直接验证：

- Slide 1 的 `slide-creator`
- Slide 8 的 `/slide-creator`

在 layout 后 paired shape/text 仍然保持同 `x/y` overlay。

### 当前几何确认

- Slide 1 `slide-creator`
  - `shape == text == {x: 6.0996, y: 2.4484, w: 1.1974, h: 0.2314}`
- Slide 8 `/slide-creator`
  - `shape == text == {x: 5.5465, y: 3.0289, w: 2.3037, h: 0.4888}`

### 本轮不要再犯

1. 单行胶囊错位时，先查 `_pack_relative_block_container()` 是否拆散了 `_pair_with`。
2. centered wrapper 的 packing / centering 必须按“组件组”处理，不要逐 child 处理。
3. compare 刷新异常慢时，先核 PPTX 实体几何，不要先看旧 montage。

### 下一步优先级

- 继续打 `data-story` 的组件 solver，不再回头修 `P1 / P8` 单行胶囊
- 优先：
  - `metric_card`
  - `style_card`
  - `feature_card`
  - `split_layout`

## 最新状态（Session 35: block-level CTA pill rejoins component path）

- Session 34 修掉的是 `_pair_with` 在 centered wrapper packer 里被拆散
- Session 35 继续确认：`data-story` 胶囊“还不对”的剩余根因不是 packer，也不是旧 pill solver 全坏
- 真正的问题是：
  - `blue-sky / enterprise-dark` 的胶囊大多是 `span`
  - `data-story` 的大 CTA pill 是 `div.cta-pill`
  - 旧 pill-like component 检测默认偏向 `INLINE_TAGS`

### 本轮通用修复

- `build_text_element()` 中的 pill-like component 检测已扩展到：
  - visible bg/border
  - leaf text container
  - `display:inline-block / inline-flex / flex`
- 不再要求标签一定属于 `INLINE_TAGS`

### 当前验证

- 新增测试：
  - `test_build_text_element_block_cta_pill_uses_component_layout()`
- 当前 `.cta-pill` 直接核对结果：
  - 修复前：`forceSingleLine=False`, `preferContentWidth=False`
  - 修复后：`forceSingleLine=True`, `preferContentWidth=True`

### 不要再犯

1. 不要把胶囊组件路径默认等同于 `span`。
2. 只要视觉语义和 CSS 语义都像 pill，block tag 也必须进入同一条组件路径。
3. 下次先查这个元素有没有进入：
   - `forceSingleLine`
   - `preferContentWidth`

### 当前下一步

- 继续肉眼对比 `P1 / P8` 胶囊细节是否还存在字体、内边距、圆角等差异
- 之后再回到 `data-story` 主体 solver：
  - `metric_card`
  - `style_card`
  - `feature_card`
  - `split_layout`

## 最新状态（Session 38: heading boost + centered auto-fit grid）

- `data-story` 本轮已经收掉两条容易反复回归的通用问题：
  - display heading 的 boost 现在会同步覆盖 `styles / segments / fragments`
  - centered column wrapper 里的 small auto-fit KPI grid 现在会走 intrinsic shrink-wrap

### 本轮通用修复

- `build_text_element()` 中，当 `_should_apply_display_heading_boost()` 命中时：
  - 不再只改 `styles.fontSize`
  - 会用 `_set_text_element_font_px()` 把 `segments[] / fragments[]` 一并同步
- 新增 `_has_centered_parent_column()`
- `_should_use_intrinsic_auto_fit_grid()` 和 `_should_stack_centered_auto_fit_cards()` 现在都能识别：
  - parent 是 centered flex-column wrapper
  - child count 很小
  - card-like auto-fit grid 应 shrink-wrap，而不是拉满整行

### 当前验证

- `python3 scripts/test-export.py`：通过
- `python3 scripts/export-sandbox-pptx.py demo/data-story-zh.html demo/data-story-output.pptx`：通过

直接核对当前 PPTX 实体：

- `P1` 标题 run size：`70.8pt`
- `P2 / P4 / P6` 的 h2 run size：`39pt`
- `P8` CTA KPI grid：已恢复成 centered single-column stack

### 一个重要验证边界

- `compare-html-ppt-visual.py` 仍然会出现“summary 已写但进程不及时退出”的老问题
- 所以当前要区分：
  - 已经真正落盘的 PPTX 改动
  - 最新完整 compare 的 `summary.json`

### 不要再犯

1. 任何 text size 修复，只改 `styles.fontSize` 是不够的；如果导出 run 来自 `segments`，就必须同步覆盖 `segments / fragments`。
2. centered column wrapper 里的 small auto-fit card grid 不能默认按 full-width grid 处理。
3. compare 卡住时，先核 XML / IR / 文件时间戳，不要立刻相信旧 summary。

### 当前下一步

- 继续看 `data-story` 的低分页：
  - `P2`
  - `P4`
  - `P6`
- 优先方向：
  - `metric_card` 光学高度与数字垂直居中
  - `vertical_card` 标题/正文字重与槽位密度
  - 继续压低“整体看起来比 source 小一号”的问题

## Session 39：metric_card 已做一次完整 rebalance，实体已生效

这轮不是再加新 solver，而是把 `data-story.metric_card` 的 contract 真正收紧到更接近 source HTML 的光学比例。

### 已落地

1. `contracts/slide_creator/presets/data-story.json`
   - `metric_max_height_ratio: 0.62 -> 0.80`
   - `minimum_height_in: 1.22 -> 1.10`
   - `gaps.after_metric: 0.08 -> 0.05`
   - `gaps.after_label: 0.06 -> 0.05`
2. `scripts/sync-slide-creator-contracts.py`
   - 同步更新到同一组值，避免下次 sync 把 vendored contract 覆盖回旧值
3. `scripts/test-export.py`
   - `test_data_story_metric_cards_limit_metric_share_of_card_height()` 的比例断言同步更新

### 当前验证

- `python3 scripts/test-export.py`：通过
- `python3 scripts/export-sandbox-pptx.py demo/data-story-zh.html demo/data-story-output.pptx`：通过

直接核对当前 PPTX 实体：

- `P2`
  - `73% / 12+ / 3`：`72pt`
- `P4`
  - `0 / 100% / <1s`：`42pt`
- `P4` 底部 KPI row card height：`1.1869"`（上一轮是 `1.22"`）

### 一个重要边界

- 这轮实体变化已经确认生效
- 但 `compare-html-ppt-visual.py` 的 fresh 跑法仍不稳定：
  - 老目录 summary 可能停在旧结果
  - 新目录 compare 可能长时间不 materialize
- 所以当前不能把“实体已改善”直接等同于“fresh visual score 已确认抬升”

### 当前最正确下一步

1. 继续补 `data-story` 的低分页：
   - `P2`
   - `P4`
   - `P6`
2. 优先不再只改字号，而是继续收：
   - `metric_card` 左右 padding / text block optical centering
   - `solution_card` 的 compact icon-title-body 节奏
   - `feature_card` 的 card density 与正文槽位

## Session 40：CJK 主字体链已修通，feature-grid local-origin guard 已补

这轮又补了两条通用能力：

### 1. CJK 文本不再只靠 `ea_font`

`map_font()` 现在对 `contains CJK` 的文本直接返回：

- `(ea_font, ea_font)`

也就是：

- `run.font.name`
- `a:ea`
- `a:cs`

都统一到稳定中文字体，不再让中文正文/标题继续挂在 Latin font 上。

当前直接核实体：

- `P2` 的正文标签：`Hiragino Sans GB`
- `P4` 的卡片标题：`Hiragino Sans GB`
- `P6` 的 feature card 标题/正文：`Hiragino Sans GB`

### 2. data-story feature grid 有了 local-origin 回归测试

新增：

- `test_data_story_feature_grid_children_stay_within_local_container_width()`

这条测试先把“feature grid children 必须受 local container 宽度约束”固化下来，避免后续继续调 solver 时把 wrapper children 又打回页级坐标思路。

### 当前验证

- `python3 scripts/test-export.py`：通过
- `python3 scripts/export-sandbox-pptx.py demo/data-story-zh.html demo/data-story-output.pptx`：通过

### 当前边界

- 这轮字体主链已经确认生效
- 但 `P6` 右列 card 几何还有系统性偏差，不能误报“feature grid 已完全修完”
- 当前更像是：
  - 字体问题已收
  - wrapper regression guard 已补
  - 下一步还要继续打 grid/container 最终 x 宽度链

## Session 40：CJK 主字体链已修通，feature-grid local-origin guard 已补

这轮又补了两条通用能力：

### 1. CJK 文本不再只靠 `ea_font`

`map_font()` 现在对 `contains CJK` 的文本直接返回：

- `(ea_font, ea_font)`

也就是：

- `run.font.name`
- `a:ea`
- `a:cs`

都统一到稳定中文字体，不再让中文正文/标题继续挂在 Latin font 上。

当前直接核实体：

- `P2` 的正文标签：`Hiragino Sans GB`
- `P4` 的卡片标题：`Hiragino Sans GB`
- `P6` 的 feature card 标题/正文：`Hiragino Sans GB`

### 2. data-story feature grid 有了 local-origin 回归测试

新增：

- `test_data_story_feature_grid_children_stay_within_local_container_width()`

这条测试先把“feature grid children 必须受 local container 宽度约束”固化下来，避免后续继续调 solver 时把 wrapper children 又打回页级坐标思路。

### 当前验证

- `python3 scripts/test-export.py`：通过
- `python3 scripts/export-sandbox-pptx.py demo/data-story-zh.html demo/data-story-output.pptx`：通过

### 当前边界

- 这轮字体主链已经确认生效
- 但 `P6` 右列 card 几何还有系统性偏差，不能误报“feature grid 已完全修完”
- 当前更像是：
  - 字体问题已收
  - wrapper regression guard 已补
  - 下一步还要继续打 grid/container 最终 x 宽度链

## Session 39：metric_card 已做一次完整 rebalance，实体已生效

这轮不是再加新 solver，而是把 `data-story.metric_card` 的 contract 真正收紧到更接近 source HTML 的光学比例。

### 已落地

1. `contracts/slide_creator/presets/data-story.json`
   - `metric_max_height_ratio: 0.62 -> 0.80`
   - `minimum_height_in: 1.22 -> 1.10`
   - `gaps.after_metric: 0.08 -> 0.05`
   - `gaps.after_label: 0.06 -> 0.05`
2. `scripts/sync-slide-creator-contracts.py`
   - 同步更新到同一组值，避免下次 sync 把 vendored contract 覆盖回旧值
3. `scripts/test-export.py`
   - `test_data_story_metric_cards_limit_metric_share_of_card_height()` 的比例断言同步更新

### 当前验证

- `python3 scripts/test-export.py`：通过
- `python3 scripts/export-sandbox-pptx.py demo/data-story-zh.html demo/data-story-output.pptx`：通过

直接核对当前 PPTX 实体：

- `P2`
  - `73% / 12+ / 3`：`72pt`
- `P4`
  - `0 / 100% / <1s`：`42pt`
- `P4` 底部 KPI row card height：`1.1869"`（上一轮是 `1.22"`）

### 一个重要边界

- 这轮实体变化已经确认生效
- 但 `compare-html-ppt-visual.py` 的 fresh 跑法仍不稳定：
  - 老目录 summary 可能停在旧结果
  - 新目录 compare 可能长时间不 materialize
- 所以当前不能把“实体已改善”直接等同于“fresh visual score 已确认抬升”

### 当前最正确下一步

1. 继续补 `data-story` 的低分页：
   - `P2`
   - `P4`
   - `P6`
2. 优先不再只改字号，而是继续收：
   - `metric_card` 左右 padding / text block optical centering
   - `solution_card` 的 compact icon-title-body 节奏
   - `feature_card` 的 card density 与正文槽位

## 最新状态（Session 36: pure Latin pill font mapping）

- `P1 / P8` 胶囊剩余问题继续收窄后，确认还有一层字体问题：
  - 结构已经对
  - `div.cta-pill` 也已经回到胶囊组件路径
  - 但 pure Latin 文本仍可能被错误映射到 CJK safe font

### 本轮通用修复

- `map_font()` 现在允许基于 `text` 做分流
- pure Latin label：
  - 优先 Latin-safe font（如 `Calibri`）
- 含 CJK 文本：
  - 继续走 `Microsoft YaHei` 这条稳定路径
- `pill_text` 内嵌 shape 文本也补上了统一字体映射

### 当前验证

- 新增测试：
  - `test_map_font_pure_latin_prefers_latin_safe_font_even_in_mixed_stack()`
- `python3 scripts/test-export.py` 继续全绿

### 一个重要验证口径

- 以后不要只看 `python-pptx` 读回的 `run.font.name`
- 这轮已经确认：
  - API 读回值可能误导
  - 最终是否真的写进 PPTX，以 slide XML 为准

### 当前记录下来的规则

1. pure Latin pill / badge / command tag 不能默认跟中文正文共用同一条字体 fallback。
2. 字体验证优先看 XML，不要只看 `python-pptx` 回读对象。

### 下一步

- 如果继续盯 `P1 / P8`，重点不再是结构和组件路径，而是：
  - 最终视觉字形
  - 内边距
  - 细圆角气质
- 之后再回到 `data-story` 主体 solver：
  - `metric_card`
  - `style_card`
  - `feature_card`
  - `split_layout`

## Session 41：Chinese Chan 已达 9.68/10，根因是未知 preset 漏过滤 runtime chrome

这轮新验证了一个泛化问题：

- `demo/chinese-chan-zh.html` 虽然已经被识别成 `slide-creator`
- 但因为没有 vendored `chinese-chan` contract
- 共享 runtime chrome 没被过滤
- `.progress-bar` / `.nav-dots` 被当正文导进了 PPTX

症状很典型：

- `P2 / P3 / P6` 顶部多出红色横条
- `P8` 多出小方块

修复方式不是给 `Chinese Chan` 写特判，而是：

- 只要 producer 已识别为 `slide-creator`
- 即使当前 preset 没有 contract
- 也默认注入 shared runtime chrome selectors

当前结果：

- `P1 = 9.8`
- `P2 = 9.5`
- `P3 = 9.5`
- `P4 = 9.8`
- `P5 = 9.8`
- `P6 = 9.5`
- `P7 = 9.8`
- `P8 = 9.7`
- `overall = 9.68/10`

结构检查：

- `overflow = 0`
- `overlap = 0`
- `element gaps = 0`
- `card containment = 0`
- `total actionable = 0`

下一次遇到新的 `slide-creator` preset，先确认：

1. producer detection 是否生效
2. contract 是否存在
3. 若 contract 缺失，shared chrome fallback 是否仍在工作

## Session 44：Chinese Chan 的换行 fidelity 已补上“保列宽 + XML page-overflow gate”

这轮把用户指出的 `P2 / P3 / P8` 换行问题收敛成一个统一规则：

- 不能只在 render 阶段开 `wrap + spAutoFit`
- 还必须在 IR 阶段保住 authored column width

本轮已经落地：

1. `preferWrapToPreserveSize` 现在会在 `build_text_element()` 里保住 `effective_max_w`
2. `Chinese Chan` 这类 serif/editorial preset 的标题/正文，不再先被 shrink 成 natural text width
3. 新增 roundtrip XML regression：
   - Slide 2 两段正文
   - Slide 3 最后一段正文
   - Slide 8 标题

新的检查口径：

- `wrap="square"`
- `spAutoFit`
- `x + cx <= slide_width`
- `cx >= authored column width threshold`

当前实体确认：

- Slide 2 body 1：`cx = 5080000`
- Slide 2 body 2：`cx = 5080000`
- Slide 3 body 2：`cx = 5080000`
- Slide 8 title：`cx = 5080000`

当前结构检查仍为：

- `overflow = 0`
- `overlap = 0`
- `element gaps = 0`
- `card containment = 0`
- `total actionable = 0`

### 这轮必须记住

1. wrap fidelity 至少有两层：
   - `wrap / auto_size`
   - authored column width
2. “溢出页面”必须直接检查 `x + cx`
3. PPTX XML regression 不要再用跨多个 `<p:sp>` 的单条 regex
