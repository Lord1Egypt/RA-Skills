# Session 41：未知 slide-creator preset 也必须默认过滤 runtime chrome

## 1. 背景

导出 `demo/chinese-chan-zh.html` 后，结构检查是干净的：

- `overflow = 0`
- `overlap = 0`
- `element gaps = 0`
- `card containment = 0`

但逐页截图对比只有 `9.40/10`，最低页集中在：

- `P2 = 9.3`
- `P3 = 9.2`
- `P6 = 9.3`
- `P8 = 9.4`

## 2. 根因

肉眼对比后，低分页存在一个共同异常：

- 顶部多出一条不该出现的深红色横条
- `P8` 多出两个不该出现的小方块

继续查 PPTX 实体和 exporter IR，确认这些都不是正文，而是全局 runtime chrome：

- 红条 = `.progress-bar`
- 小方块 = `.nav-dots`

更关键的是，这个问题不是 `Chinese Chan` 特有的 DOM bug，而是当前 producer-aware 路径的一个缺口：

1. `detect_producer()` 已经能把 `Chinese Chan` 识别为 `slide-creator`
2. 但因为仓库里**没有** `contracts/slide_creator/presets/chinese-chan.json`
3. `SlideCreatorAdapter.collect_hints()` 没拿到 contract
4. 所以 `runtime_chrome_selectors` 没有注入
5. `parse_html_to_slides()` 也就没有执行 `_prune_runtime_chrome()`

结果就是：

- 已知 preset（Blue Sky / Enterprise Dark / Data Story）没问题
- 未 vendored contract 的新 preset 会把共享 runtime chrome 当正文导出来

## 3. 修复

在 `scripts/export-sandbox-pptx.py` 里新增了通用常量：

- `SLIDE_CREATOR_RUNTIME_CHROME_SELECTORS`

内容包括：

- `.progress-bar`
- `.nav-dots`
- `.edit-hotzone`
- `.edit-toggle`
- `#notes-panel`
- `#present-btn`
- `#present-counter`

然后在 `SlideCreatorAdapter.collect_hints()` 里改成：

- 只要识别为 `slide-creator`
- 且当前 hints 里还没有 `chrome_selectors`
- 就先注入这套 shared runtime chrome fallback

也就是说：

- 有 contract 时，继续优先用 contract
- 没 contract 时，也不会把共享 runtime chrome 漏进正文

## 4. 测试

新增测试：

- `test_slide_creator_unknown_preset_still_gets_runtime_chrome_fallback()`

覆盖点：

- `demo/chinese-chan-zh.html`
- `detection.producer == slide-creator`
- `contract is None`
- 但 `hints.chrome_selectors` 仍应包含：
  - `.progress-bar`
  - `.nav-dots`
  - `#present-btn`

验证：

- `python3 scripts/test-export.py`：通过

## 5. 结果

重导出并 fresh 跑逐页截图对比后：

- `P1 = 9.8`
- `P2 = 9.5`
- `P3 = 9.5`
- `P4 = 9.8`
- `P5 = 9.8`
- `P6 = 9.5`
- `P7 = 9.8`
- `P8 = 9.7`
- `overall = 9.68/10`

结构检查仍保持：

- `overflow = 0`
- `overlap = 0`
- `element gaps = 0`
- `card containment = 0`
- `total actionable = 0`

## 6. 不要再犯

1. `slide-creator` 的共享 runtime chrome 不能只靠 vendored preset contract 过滤。
2. 对未知 preset，只要 producer 已识别为 `slide-creator`，就必须有一套 shared chrome fallback。
3. 当某个新 preset 视觉上突然多出顶部条、导航点、小控制块时，先查：
   - producer detection 是否生效
   - contract 是否缺失
   - `chrome_selectors` 是否真的注入到 hints 里
