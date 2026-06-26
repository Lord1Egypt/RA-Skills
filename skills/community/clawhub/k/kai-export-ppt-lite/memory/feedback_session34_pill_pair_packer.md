# Session 34：centered wrapper packer 的 paired pill 回归修复

时间：2026-04-24

## 背景

`demo/data-story-zh.html` 在 Session 33 引入 centered column wrapper packing 后，`Slide 1` 和 `Slide 8` 的单行胶囊出现回归：

- 胶囊背景 shape 还在原位
- 文字被顺序堆到胶囊下面
- 肉眼看起来像“胶囊错位”或“组件本身坏了”

用户明确指出：

- `P1` 和 `P8` 的单行胶囊之前是对的
- 现在与源文件对比已经错了

## 根因

不是 `badge / cta-pill` 组件本身退化，而是通用 `_pack_relative_block_container()` 的打包模型不认识 `_pair_with`。

之前该函数把 children 当作普通 block 顺序重排：

1. 先放 paired bg shape
2. 再放 paired text

于是同一个胶囊被拆成两个独立 block，导致：

- `shape.y = current_y`
- `text.y = current_y + shape.height + gap`

也就是文字掉到胶囊下方。

## 本轮通用修复

对 `_pack_relative_block_container()` 做了 2 个关键修复：

1. `_pair_with` 连续 children 必须先聚合成一个 `packed item`
   - 成组计算 `min_x / min_y / width / height`
   - 组内成员保持原始相对坐标
   - 组与组之间再参与纵向 block flow

2. centered wrapper 不能逐 child 居中，而要逐 `packed item` 居中
   - 否则 pair 内部虽然重合，整体仍可能被二次打散

顺手一起收了另一个旧坑：

3. wrapper packing 阶段的 `maxWidth` 不能直接走 `parse_px()`
   - 改为 `_resolve_css_length_with_basis()`
   - 这样 `min()/max()/vw` authored width 仍然成立

## 验证

代码验证：

- `python3 -m py_compile scripts/export-sandbox-pptx.py scripts/test-export.py`
- `python3 scripts/test-export.py`

当前 `test-export.py` 已重新全绿。

新增回归测试：

- `test_data_story_centered_wrapper_keeps_paired_pills_overlaid()`

它直接验证：

- `Slide 1` 的 `slide-creator`
- `Slide 8` 的 `/slide-creator`

对应的 paired shape/text 在 layout 后仍然保持：

- 同 `x`
- 同 `y`

实体几何核对结果：

- Slide 1 `slide-creator`
  - `shape == text == {x: 6.0996, y: 2.4484, w: 1.1974, h: 0.2314}`
- Slide 8 `/slide-creator`
  - `shape == text == {x: 5.5465, y: 3.0289, w: 2.3037, h: 0.4888}`

结构自检：

- `python3 scripts/rigorous-eval.py --sandbox demo/data-story-output.pptx --golden demo/data-story-output.pptx --skip-visual`
- 结果仍是：
  - `overflow=1`
  - `overlap=0`
  - `element gaps=0`
  - `card containment=0`
  - `total actionable=1`

## 不要再犯

1. 看到胶囊文字掉到背景下方时，先查通用 packer 是否拆散了 `_pair_with`，不要先怀疑 pill builder。
2. centered wrapper 的 block packing，必须按“组件组”而不是“单元素”居中。
3. compare 截图如果刷新异常缓慢，先核 PPTX 实体几何；不要只盯旧 montage。
4. wrapper width contract 继续禁止直接用 `parse_px()` 处理复杂 CSS 长度。

## 当前影响

这轮主要修复的是 `P1 / P8` 的单行胶囊回归，属于通用 centered wrapper 打包稳定性增强。

它不会自动把 `data-story` 整体拉到 `9.5+`，但能避免后续继续在错误结构上优化，防止：

- hero badge
- CTA pill
- 其他 paired inline pill

在后续 solver 优化中反复倒退。
