# MS Financial Model — Morgan Stanley Style DCF/SOTP Excel Generator

> Investment-grade financial model generator for CGMA/ACCA/CPA/CFA professionals.

**Author**: WANG DONG JIE | **License**: MIT | **Version**: 1.1.0

## Features

- Three-scenario DCF (Bear/Base/Bull) with full CAPM-driven WACC
- SOTP (Sum-of-the-Parts) valuation by business segment
- Sensitivity analysis matrices (WACC x TGR, WACC x Exit Multiple)
- PE Band historical analysis with area chart
- Comparable company analysis (multi-market: US/HK/A-share)
- Operational KPI dashboard
- Stacked Revenue by Segment chart
- Donut Chart for SOTP (DoughnutChart)
- Grouped Scenario Comparison chart (Bear/Base/Bull)
- Dual-Axis Combo chart (Revenue bar + EBITDA Margin line)
- Total: 9 publication-grade openpyxl charts
- 8 color themes, zh/en/bilingual support

## Quick Start

```python
from ms_financial_model import make_financial_model, sample_data

data = sample_data()
output = make_financial_model(data, "output/model.xlsx", theme="classic", language="zh")
print(f"Generated: {output}")
```

## CLI

```bash
python scripts/run.py -o output/model.xlsx --lang zh --theme classic
```

## Output Structure

10+ Sheets: Cover, Bear DCF, Base DCF, Bull DCF, WACC, Sensitivity, SOTP, KPI, PE Band, Comps

## Dependencies

- Python >= 3.9
- openpyxl >= 3.1

## Links

- [GitHub](https://github.com/yjkj999999/ms-financial-model)
- [Clawhub](https://clawhub.ai/user/yjkj999999)
