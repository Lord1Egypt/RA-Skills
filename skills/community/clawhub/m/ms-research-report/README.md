# MS Research Report — Morgan Stanley Style DOCX Generator

> Publication-grade equity research report generator for sell-side/buy-side analysts.

**Author**: WANG DONG JIE | **License**: MIT | **Version**: 1.1.0

## Features

- Complete 20-section report structure (Cover to Disclosure)
- Publication-grade matplotlib charts (DPI 300, MS 8-color palette)
- 10 chart types: bar, line, pie, waterfall, stacked_bar, donut, dual_axis, grouped_bar, bubble, event_line
- 2x2 Strategic Matrix framework section
- Exhibit auto-numbering system
- WACC stacked bar chart, Valuation Bridge waterfall
- Sensitivity analysis matrices
- Comparable company analysis
- Thesis in N Charts with KPI cards
- 8 color themes, zh/en/bilingual support
- All charts: DPI 300, MS 8-color palette, publication-grade

## Quick Start

```python
from ms_research_report import make_report

data = { ... }  # your research data
output = make_report(data, "output/report.docx", theme="classic", language="zh")
print(f"Generated: {output}")
```

## CLI

```bash
python scripts/run.py -o output/report.docx --lang zh --theme classic
```

## Dependencies

- Python >= 3.9
- python-docx >= 0.8.11
- matplotlib >= 3.5 (optional, for charts)

## Links

- [GitHub](https://github.com/yjkj999999/ms-research-report)
- [Clawhub](https://clawhub.ai/user/yjkj999999)
