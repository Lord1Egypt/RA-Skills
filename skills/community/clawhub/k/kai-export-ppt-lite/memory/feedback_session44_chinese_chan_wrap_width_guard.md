# Session 44：Chinese Chan 换行问题收敛到“列宽 fidelity”，不能只在 render 端开 wrap

日期：2026-04-24

## 结论

这轮 `P2 / P3 / P8` 看起来都是“换行错了”，但根因不是同一层：

1. `P2 / P3`
   - render 端其实已经进入了 `wrap="square" + spAutoFit`
   - 问题核心是：以后必须把“源文件列宽 + 不越界”做成可执行检查，不能只肉眼看
2. `P8`
   - 真正的问题不是字体，也不是 render 分支没生效
   - 而是 `build_text_element()` 在 IR 阶段就把 centered title 文本框按内容宽度 shrink 了
   - 到 export 时即使开了 wrap，也已经失去 authored column width

所以这轮真正修的是：

- `preferWrapToPreserveSize` 不再只影响 render 行为
- 它现在也会保住 authored column width

## 本轮修复

涉及文件：

- `scripts/export-sandbox-pptx.py`
- `scripts/test-export.py`

### 1. build_text_element() 新增“保列宽”规则

新增规则：

- 如果 text contract 已给出 `preferWrapToPreserveSize`
- 且当前文本不是 inline component
- 且存在 `effective_max_w`

则 IR 文本框宽度直接使用 authored 列宽，不再收缩到 natural content width。

这条规则解决的是：

- `Chinese Chan` 的标题/正文已经知道“应该优先 wrap 保节奏”
- 但如果 IR 先把文本框压窄，后面 render 再开 `word_wrap=True` 也晚了

### 2. 新增 roundtrip XML regression test

新增测试：

- `test_chinese_chan_roundtrip_wrap_fidelity_and_no_page_overflow()`

它直接导出 `demo/chinese-chan-zh.html` 到临时 PPTX，然后检查：

1. Slide 2 两段正文：
   - `wrap="square"`
   - `spAutoFit`
   - 文本框右边界不越出页面
   - 文本框宽度维持 authored column width
2. Slide 3 最后一段正文：
   - 同样必须 `wrap + spAutoFit + no overflow`
3. Slide 8 标题：
   - 同样必须保 authored width，不允许缩成小窄框

### 3. XML helper 自己也踩了坑

本轮测试里还确认了一个容易误导人的问题：

- 如果用一个跨 `p:sp` 的大 regex 去找文本框
- 很容易命中错误的 shape block

修正方式：

- 先按 `<p:sp>...</p:sp>` 分块
- 再在 block 内找目标 text
- 最后再读 `off/ext/bodyPr`

以后凡是做 PPTX XML regression，不要再直接用跨 shape 的单条 regex。

## 本轮验证结果

通过：

- `python3 scripts/test-export.py`
- `python3 scripts/export-sandbox-pptx.py demo/chinese-chan-zh.html demo/chinese-chan-output.pptx`
- `python3 scripts/rigorous-eval.py --sandbox demo/chinese-chan-output.pptx --golden demo/chinese-chan-output.pptx --skip-visual`

当前结构检查仍为：

- `overflow = 0`
- `overlap = 0`
- `element gaps = 0`
- `card containment = 0`
- `total actionable = 0`

实体确认：

- Slide 2 两段正文：
  - `wrap="square"`
  - `spAutoFit`
  - `cx = 5080000`
- Slide 3 最后一段正文：
  - `wrap="square"`
  - `spAutoFit`
  - `cx = 5080000`
- Slide 8 标题：
  - 已从窄框恢复成 `cx = 5080000`
  - `wrap="square"`
  - `spAutoFit`

## 记住这轮经验

1. 只在 render 端开 wrap，不足以保证 fidelity。  
   如果 IR 宽度已经 shrink 错了，后面只能“在错误的盒子里正确换行”。

2. “换行 fidelity”至少要检查两件事：
   - `wrap / auto_size`
   - authored column width 是否保住

3. “是否溢出页面”不能只靠肉眼，需要直接检查：
   - `x + cx <= slide_width`

4. 做 XML regression 时，不能用跨多个 `<p:sp>` 的单 regex。
