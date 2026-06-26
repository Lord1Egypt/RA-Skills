---
name: market-chart-renderer
summary: 中国市场行情图表渲染 skill，负责指标计算、ECharts 模板、HTML/PNG 导出
---

# market-chart-renderer

用于把标准化 `bars` 数据渲染成图表。

## 职责边界

负责：

- 指标计算：至少 `MA5/10/20/60`、`MACD`
- ECharts 图表模板
- 标题区（品种名 / 代码 / 周期）
- 主图 K 线 + MA 均线
- 副图默认 `MACD`
- HTML / PNG 导出

不负责：

- AkShare 数据抓取细节
- 品种路由
- 交易所查询逻辑

## 最小入口

直接生成甲醇 `MA0 60m` 图：

```bash
python3 skills/market-chart-renderer/render_ma0_60m.py
```

自定义：

```bash
python3 skills/market-chart-renderer/render_chart.py --symbol MA0 --period 60 --limit 120
```

## 输出位置

默认输出到：

- `output/generated/images/*.html`
- `output/generated/images/*.png`
- `output/generated/images/*.json`

## 依赖关系

- 数据来源：`skills/akshare-futures-options-data/akshare_router_cn.py`
- 渲染方案：ECharts + headless Chrome
