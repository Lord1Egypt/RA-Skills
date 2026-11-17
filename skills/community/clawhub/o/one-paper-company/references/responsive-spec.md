# 响应式断点 + 滚动跟随规范

> 本文档定义 one-paper-company 周期复盘形态的响应式和滚动跟随铁律。

## 响应式断点（铁律）

| 断点 | 行为 |
|---|---|
| `≥ 1181px` | 横屏默认：左 44% 文字 / 右 56% 图表 |
| `961-1180px` | 中等屏幕：左 38% 文字 / 右 62% 图表（小笔记本/iPad 竖屏）|
| `≤ 960px` | 竖屏单列：vizcol 顶部 sticky 54vh / step 下方滚动 |
| `≤ 560px` | 小屏：信号卡单列 |
| `@media print` | 打印 PDF：所有 vp 展开，sticky 失效 |

## 滚动跟随（与原始素材 1:1 对齐）

- IntersectionObserver `rootMargin: -38% 0px -52% 0px`（激活区视口 38%~48%，中部偏上 10%）
- 文字滚到视口中部时图表才切换，避免"跟随不同步"
- `.steps::after` 60vh tail spacer，确保 s9/s10 能滚到激活区
- resize 防抖 200ms + orientationchange 三次 resize（0/300/800ms）

## 配色策略（铁律）

**固定不变**（中性色，跨公司通用）：
```
--bg:#f7f5f0 --panel:#fffdf9 --ink:#20242b --ink2:#3a414c --muted:#717a86
--line:#e4e0d6 --soft:#efede6
--navy:#24425e --blue:#2c7be5 --red:#c0392b --up:#c0392b --down:#2e9e5b --gold:#b98a1d
```

**按公司替换**（仅这两个）：
- `--green`：品牌色（默认 `#76b900`）
- `--green-d`：深一档（默认 `#5a9200`）

**替换点**：kicker / step-tag bar / hair / selection / ECharts green 系列（净利柱/dcrev线/雷达now/LED/pixel字）

**品牌色识别优先级**：用户指定 > WebSearch logo 主色 > 默认 #76b900

## K 线对数轴范围算法

原页 0.02~400 是英伟达专属。通用算法：

```python
def calc_kline_yrange(prices):
    pmin, pmax = min(prices), max(prices)
    down_ticks = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50]
    up_ticks = [50, 100, 200, 400, 800, 1600, 3200]
    ymin = max([t for t in down_ticks if t <= pmin * 0.7] + [down_ticks[0]])
    ymax = min([t for t in up_ticks if t >= pmax * 1.2] + [up_ticks[-1]])
    return (ymin, ymax)
```

`build_html.py` 已实现：若 `data.kline.yMin` 缺失，自动从 `pre+closes+candles` 全价格算。
