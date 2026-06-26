---
name: gold-price-query
description: Gold price query tool supporting CNY (RMB/gram) and USD (USD/oz) currency options for real-time spot gold price lookup.
---

# Gold Price Query

Real-time gold spot price lookup supporting CNY (RMB/gram) and USD (USD/oz) currency options.

## Quick Start

Run the script to query gold prices:

```bash
# Query USD price (default)
python gold_price.py USD

# Query CNY price
python gold_price.py CNY
```

## Output Format

Returns JSON data containing:

```json
{
  "success": true,
  "data": {
    "名称": "现货黄金",
    "单位": "美元/盎司",
    "开盘价": "2350.00",
    "当前价": "2355.50",
    "最高价": "2360.00",
    "最低价": "2345.00",
    "买价": "2355.00",
    "卖价": "2356.00",
    "涨跌额": "5.50",
    "涨跌幅": "0.23%",
    "成交量": "500000",
    "更新时间": "2024-04-12 10:30:00"
  },
  "timestamp": 1712899200000
}
```

## Currency Parameters

| Parameter | Description | Unit |
|-----------|-------------|------|
| CNY | RMB denominated | RMB/gram |
| USD | USD denominated (default) | USD/oz |

## Notes

- Requires network access to API
- API source: jijinhao.com
- Consider setting appropriate request intervals to avoid rate limiting