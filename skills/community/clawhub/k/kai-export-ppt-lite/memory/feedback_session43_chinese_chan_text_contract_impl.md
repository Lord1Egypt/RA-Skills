# Session 43：Chinese Chan 排版契约真正接入导出器

日期：2026-04-24

## 结论

Session 42 只完成了方案，没有真正让 `Chinese Chan` 的 typography / line-break contract 进入渲染链。

本轮实现后，真正落地的是：

1. `scripts/sync-slide-creator-contracts.py` 现在会同步 `Chinese Chan` contract
2. contract 正式包含：
   - `typography`
   - `line_break_contract`
3. exporter 新增 `resolve_text_contract()` 运行时消费路径
4. `map_font()` 支持 mixed-script serif stack：
   - Latin glyph 用 serif-safe Latin face
   - CJK glyph 用 serif-safe CJK face
5. authored `<br>` 不再只是“heading 特判”，而是可由 contract 驱动
6. `prefer_preserve` 已真正进入 render 前控制逻辑

## 本轮最重要的新经验

### 1. `preserve` 和 `prefer_preserve` 不是一回事

`Chinese Chan` 的核心标题 `kai-slide-creator` 没有显式 `<br>`，但浏览器会在作者给定的宽度里自然换行。

因此：

- `preserve` 适合“已有 `<br>`，必须保住”
- `prefer_preserve` 适合“没有 `<br>`，但必须优先保住 authored width rhythm，而不是 shrink-fit 压成一行”

如果只实现 `preserve`，就会出现：

- contract 存在
- 字体也更接近了
- 但标题仍被 exporter 压成一行小字

### 2. render 前 text contract 必须直接改变 `TextFrame` 行为

本轮新增的真正有效分支是：

- `preferWrapToPreserveSize=True`
- 导出时：
  - `tf.word_wrap = True`
  - `tf.auto_size = SHAPE_TO_FIT_TEXT`

而不是继续走：

- `wrap = none`
- `TEXT_TO_FIT_SHAPE`

这条规则让 `Chinese Chan` 的封面标题重新回到“按 600px authored 宽度自然折成两行”的路径。

### 3. 字体 fidelity 不能只看逻辑，要看 PPTX XML

这轮再次确认：

- `python-pptx` 回读对象不可靠
- 真正要看的是 `ppt/slides/slideN.xml`

本轮已核到：

- Slide 1 标题：`wrap="square"` + `spAutoFit`
- 中英 serif 混排：
  - `latin = Baskerville`
  - `ea = Songti SC`

也就是说：

- contract 已进入写盘实体
- 不是只停留在 Python 逻辑里

### 4. 自动视觉分对“白底 + 黑字 + 节奏差异”不够敏感

`Chinese Chan` 这类 deck 的大面积留白会掩盖 typography / line-break 差异。

本轮即使实体行为改变了：

- visual compare 仍然可能维持在 `9.68`

所以这类 preset 的验证口径必须是双轨：

1. montage / diff
2. PPTX XML / text-frame 行为

不能只看 `overall_score`

### 5. 本机 `soffice` 是坏 wrapper，compare 实际落回了粗糙 preview

这轮额外确认了一条很容易误导人的环境问题：

- `which soffice` 返回 `/opt/homebrew/bin/soffice`
- 但它实际指向不存在的：
  - `/Applications/LibreOffice.app/Contents/MacOS/soffice`

结果是：

1. `compare-html-ppt-visual.py` 尝试用 `soffice` 转 PDF
2. 转换失败
3. 脚本静默退回 `_render_ppt_slides_preview()`
4. 这个 preview 只会：
   - 画背景矩形
   - 用固定小字体绘制 `shape.text`
   - 不理解真实的 wrap / auto-size / font metrics

所以当前 `Chinese Chan` 的：

- `overall = 9.68`
- `P1 = 9.8`

只能看成“fallback preview 分数”，不能等价于真实 Office 渲染分。

本轮的正确口径是：

1. `summary.json` 只作参考
2. typography / break 是否真的生效，要以：
   - PPTX XML
   - `wrap / auto_size`
   - contract-driven export branch
   为准

## 本轮代码结果

涉及文件：

- `scripts/export-sandbox-pptx.py`
- `scripts/sync-slide-creator-contracts.py`
- `scripts/test-export.py`
- `contracts/slide_creator/manifest.json`
- `contracts/slide_creator/presets/chinese-chan.json`

新增能力：

1. `_resolve_text_contract()` 产出：
   - `preserveAuthoredBreaks`
   - `preferWrapToPreserveSize`
   - `shrinkForbidden`
2. `build_text_element()` 把 text contract 元数据写入 IR
3. `export_text_element()` 新增 contract 分支：
   - `preserveAuthoredBreaks -> wrap none + SHAPE_TO_FIT_TEXT`
   - `preferWrapToPreserveSize -> wrap true + SHAPE_TO_FIT_TEXT`
4. `sync-slide-creator-contracts.py` 新增 `Chinese Chan`
5. `line_break_contract.break_policy['.zen-title'] = 'prefer_preserve'`

## 测试与验证

通过：

- `python3 -m py_compile scripts/export-sandbox-pptx.py scripts/test-export.py scripts/sync-slide-creator-contracts.py`
- `python3 scripts/test-export.py`
- `python3 scripts/sync-slide-creator-contracts.py`
- `python3 scripts/export-sandbox-pptx.py demo/chinese-chan-zh.html demo/chinese-chan-output.pptx`
- `python3 scripts/compare-html-ppt-visual.py demo/chinese-chan-zh.html demo/chinese-chan-output.pptx --outdir demo/chinese-chan-visual-compare-r4`
- `python3 scripts/rigorous-eval.py --sandbox demo/chinese-chan-output.pptx --golden demo/chinese-chan-output.pptx --skip-visual`

当前可用视觉分：

- `overall = 9.68/10`
- `P1 9.8`
- `P2 9.5`
- `P3 9.5`
- `P4 9.8`
- `P5 9.8`
- `P6 9.5`
- `P7 9.8`
- `P8 9.7`

结构检查：

- `overflow = 0`
- `overlap = 0`
- `element gaps = 0`
- `card containment = 0`
- `total actionable = 0`

## 后续注意事项

1. 新 preset 不能再只同步 layout contract，必须同步 typography + line-break contract
2. 对留白型 serif preset，visual score 不能作为唯一真相源
3. 任何“显得像小字压一行”的问题，先检查：
   - `breakPolicy`
   - `preferWrapToPreserveSize`
   - slide XML 里的 `wrap` / `spAutoFit`
4. 如果 source 是 authored width rhythm，不要第一反应 shrink-fit
5. 如果 compare 结果和 PPTX XML 明显冲突，先查 `soffice` 是否真的可用，不要默认当前 `summary.json` 代表了真实 Office 渲染
