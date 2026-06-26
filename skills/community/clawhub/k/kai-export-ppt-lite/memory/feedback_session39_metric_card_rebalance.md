# Session 39：data-story KPI 卡不能只放大数字，还要同步收紧 card height / slot gap

## 1. 背景

继续优化 `demo/data-story-zh.html` 时，`P2 / P4 / P7 / P8` 的 KPI 卡暴露出同一类问题：

- 数字偏小，视觉冲击不够
- 卡片整体偏高，和 source HTML 相比显得“更钝、更笨”
- 即使 `sync-slide-creator-contracts.py` 里已经把 `metric_max_height_ratio` 调大，如果 vendored contract 没同步，运行时仍然吃不到新参数

## 2. 根因

这轮确认了两个层面的根因：

### A. contract drift：只改同步脚本，不改 vendored contract，导出器不会自动变好

`scripts/sync-slide-creator-contracts.py` 里：

- `data-story.metric_card.metric_max_height_ratio`
  已经从 `0.62` 提到 `0.80`

但运行时实际读的是：

- `contracts/slide_creator/presets/data-story.json`

如果这个 vendored contract 还是旧值，exporter 仍会按 `0.62` 继续压缩 KPI 数字。

### B. 只放大数字不够，KPI 卡的“光学比例”还需要一起收紧

在 `metric_card` 里，光学结果不只是 `metric_max_height_ratio` 决定的，还受两项共同影响：

1. `minimum_height_in`
2. `gaps.after_metric / gaps.after_label`

如果只把数字放大：

- 数字会更大
- 但 card 仍保留旧的保守最小高度和较大的内部空隙
- 最终视觉上仍然会显得卡片过高、节奏偏散

## 3. 修复

### 3.1 同步 vendored contract

把 `contracts/slide_creator/presets/data-story.json` 的：

- `metric_max_height_ratio: 0.62 -> 0.80`

与同步脚本里的定义重新对齐。

### 3.2 一起收紧 KPI 卡光学几何

在 `scripts/sync-slide-creator-contracts.py` 和 vendored contract 里，对 `data-story.metric_card` 同时做了 3 个收紧：

- `minimum_height_in: 1.22 -> 1.10`
- `gaps.after_metric: 0.08 -> 0.05`
- `gaps.after_label: 0.06 -> 0.05`

这条规则的目标不是“把卡压扁”，而是让：

- 数字更大
- 标签更贴近数字
- 整卡更接近 source HTML 的短促 KPI 节奏

## 4. 验证

### 4.1 测试

- `python3 scripts/test-export.py` 通过

并同步更新了断言：

- `test_data_story_metric_cards_limit_metric_share_of_card_height()`
  - 允许比例从 `0.63` 放宽到 `0.81`

### 4.2 导出实体验证

- `python3 scripts/export-sandbox-pptx.py demo/data-story-zh.html demo/data-story-output.pptx` 通过

直接核当前 PPTX 实体：

- `P2`
  - `73% / 12+ / 3`：`55.9pt -> 72.0pt`
- `P4`
  - `0 / 100% / <1s`：`39.0pt -> 42.0pt`
- `P4` 底部 KPI row card height：
  - `1.22" -> 1.1869"`

## 5. 一个重要边界

这轮 `compare-html-ppt-visual.py` 仍然存在不稳定现象：

- 旧输出目录会写完结果但进程不及时退出
- 新输出目录有时甚至在较长等待后仍未 materialize

所以这轮不能伪造“fresh visual score 已上升”，只能确认：

- 实体几何和字号已经按预期变化
- 最新完整完成的 `summary.json` 仍停留在上一轮

## 6. 不要再犯

1. `sync-slide-creator-contracts.py` 改了，不等于运行时已经吃到；如果没同步 vendored contract，exporter 不会变。
2. KPI 卡的视觉优化不能只看“数字够不够大”，必须同时看：
   - `metric_max_height_ratio`
   - `minimum_height_in`
   - `gaps`
3. 当 compare 链不稳定时，要先核：
   - PPTX 实体 run size
   - container/card 实体高度
   - contract 文件实际值
   再判断这轮是不是没生效。
