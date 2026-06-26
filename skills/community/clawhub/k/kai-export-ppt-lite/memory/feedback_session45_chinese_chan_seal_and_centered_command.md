# Session 45：Chinese Chan P8 的 seal border 和 centered command 需要单独 gate

日期：2026-04-24

## 结论

`Chinese Chan` 的 `P8` 剩余两个问题看起来都像“视觉细节”，但根因分别在不同层：

1. `zen-seal` 小方块没有边框
   - 根因不是 `export_shape_background()` 不会画边框
   - 而是 **无文字 + 显式尺寸** 的 decoration shape 在 IR 构建时只保留了：
     - `backgroundColor`
     - `backgroundImage`
     - `borderRadius`
   - `border / borderLeft / borderRight / borderTop / borderBottom` 全丢了
   - 所以后面 export 阶段根本没有边框可画

2. 底部 command 行看起来“左对齐”
   - 真正要检查的不是“相对整页是否中心”
   - 而是 **相对 authored content column 是否居中**
   - `Chinese Chan` 的 footer command card 本来就在 `slide-content max-width: 600px` 这条内容列里居中，而不是相对 13.33" 全页居中

## 本轮修复

涉及文件：

- `scripts/export-sandbox-pptx.py`
- `scripts/test-export.py`

### 1. decoration shape 也必须保留 border 契约

修复前：

- no-text explicit-size decoration 路径会丢 border 信息

修复后：

- 这类 shape IR 也保留：
  - `border`
  - `borderLeft`
  - `borderRight`
  - `borderTop`
  - `borderBottom`

直接收益：

- `zen-seal` 现在能在最终 PPTX 里保留边框

### 2. 纯 border shell 默认不再加轻阴影

修复前：

- command / seal 这类无填充、只有 border 的壳，也会走 `set_light_shadow()`

修复后：

- 只有真正有 `bg_rgb` 或 `gradient fill` 的 shape 才允许加 light shadow

直接收益：

- `P8` command card 不再带多余阴影
- 这条规则也更接近浏览器里大量“细边框壳”的真实表现

### 3. centered command 的 roundtrip gate 明确改成“相对列中心”

新增/修正的检查：

- `slide8_cmd` 的 textbox：
  - 必须 `algn="ctr"`
  - 必须 shrink-wrap（宽度小于 authored column）
  - 中心点必须接近 `slide8_title` 的中心点

而不是：

- 错误地要求它接近整页 `slide_width / 2`

## XML 实体确认

最新 `demo/chinese-chan-output.pptx` 的 `slide8.xml` 已确认：

1. `zen-seal`
   - `fill = F5E8E8`
   - `line = C41E3A`
   - 无 shadow

2. command card
   - shape/text 共用：
     - `x = 4424172`
     - `cx = 3797808`
   - 文本：
     - `algn="ctr"`
   - 现在是 shrink-wrap 后在 authored column 中心对齐

## 本轮验证

通过：

- `python3 scripts/test-export.py`
- `python3 scripts/export-sandbox-pptx.py demo/chinese-chan-zh.html demo/chinese-chan-output.pptx`
- `python3 scripts/rigorous-eval.py --sandbox demo/chinese-chan-output.pptx --golden demo/chinese-chan-output.pptx --skip-visual`

结构检查：

- `overflow = 0`
- `overlap = 0`
- `element gaps = 0`
- `card containment = 0`
- `total actionable = 0`

## 记住这轮经验

1. decoration shape 不是“简单 shape”，也要保留 border contract。  
   否则会出现“source 有边框，export 根本没有边框”的低级丢失。

2. centered alignment 的 fidelity，必须先明确参照系。  
   `Chinese Chan` 这种 editorial preset，很多元素是相对 `content column` 居中，而不是相对整页居中。

3. 纯 border shell 默认不应带 light shadow。  
   这类壳如果没有 fill，就优先按 browser 的“平面边框框体”处理。
