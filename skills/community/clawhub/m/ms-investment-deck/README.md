# MS Investment Deck — Morgan Stanley Style PPTX Generator

> Professional investment presentation generator for sell-side/buy-side analysts.

**Author**: WANG DONG JIE | **License**: MIT | **Version**: 1.1.0

## Features

- 23 slide types (27 pages): Cover, Key Takeaways, KPI Blocks, Rating Table, Market Monitor, Financial Charts, Scenario Comparison, WACC Breakdown, Valuation Bridge, Sensitivity Heatmap, and more
- **NEW in v1.1.0:**
  - Dual-Panel Side-by-Side Charts (5 content types: bar/line/metric/table/text)
  - 2x2 Strategic Matrix (four-quadrant framework)
  - Asset Allocation Dot Matrix (BEAT style: --/-/=/+/++)
  - Donut Chart with Center Metric
  - Stacked Bar Chart (horizontal/vertical)
- MS brand styling: navy/gold color scheme, CJK font support
- Chart support: pie charts, bar/line overlays with markers, donut charts, stacked bars
- What's Changed tracking, Shovel Stocks list, Value Chain
- Executive Summary (four-quadrant layout)
- 8 color themes, zh/en/bilingual support

## Quick Start

```python
from ms_investment_deck import make_deck, sample_data

data = sample_data()
output = make_deck(data, "output/deck.pptx", theme="classic", language="zh")
print(f"Generated: {output}")
```

## CLI

```bash
python scripts/run.py -o output/deck.pptx --lang zh --theme classic
```

## Dependencies

- Python >= 3.9
- python-pptx >= 0.6.21

## Links

- [GitHub](https://github.com/yjkj999999/ms-investment-deck)
- [Clawhub](https://clawhub.ai/user/yjkj999999)
