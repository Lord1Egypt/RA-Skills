---
name: hk-stock-short-selling
name_zh: 港股卖空数据
description: Get Hong Kong stock short selling data (daily and historical) from HKEX and ETNet. 免费获取港股每日和历史卖空数据。
description_zh: 获取港股每日卖空数据和历史卖空数据，数据来自港交所和ETNet。
---

# 港股卖空数据 HK Stock Short Selling

获取港股每日卖空数据，数据来自港交所官网 + ETNet（免费公开）。

## 功能 Features

1. **当天卖空数据** - 获取指定股票的当日卖空数据（港交所）
2. **历史数据查询** - 获取个股历史卖空数据（ETNet，可查3个月）
3. **排行榜** - 获取卖空金额/股数排行榜
4. **持仓监控** - 监控持仓股票的卖空情况

## 数据源 Data Source

- **当天数据**: 港交所官网 (https://www.hkex.com.hk/chi/stat/smstat/)
- **历史数据**: ETNet (https://www.etnet.com.hk/)

## 安装 Installation

```bash
pip install requests pandas beautifulsoup4
```

## 使用方法 Usage

### 命令行

```bash
# 获取单只股票当天卖空数据
python3 hk_short_selling.py 2513

# 获取多只股票
python3 hk_short_selling.py 2513 100 700

# 获取当天全部数据
python3 hk_short_selling.py --all

# 获取排行榜
python3 hk_short_selling.py --top 20
```

### 获取历史数据

```python
from hk_short_selling import ETNetHistoricalScraper

scraper = ETNetHistoricalScraper()

# 获取个股历史卖空数据
# 参数: 股票代码(去掉前导0), 获取页数
df = scraper.get_stock_short_selling_history('2513', pages=5)

# 返回字段:
# - date: 交易日期
# - short_volume: 卖空股数
# - short_amount: 卖空金额 (港元)
# - short_pct: 卖空占成交比例 (%)
# - turnover: 股票成交金额
# - avg_5d: 5日平均卖空金额
# - total_short_value: 当日全市场卖空总额
# - pct_of_total: 该股占全市场卖空比例
```

## 数据字段 Fields

| 字段 | 说明 |
|------|------|
| stock_code | 股票代码 (5位) |
| stock_name | 股票名称 |
| short_volume | 卖空股数 |
| short_amount | 卖空金额 (港元) |
| short_pct | 卖空占成交比例 (%) |
| market | 主板/创业板 |
| date | 数据日期 |

## 示例 Examples

```python
from hk_short_selling import HKShortSeller, ETNetHistoricalScraper

# 获取当天数据
seller = HKShortSeller()
df = seller.get_today_data(stock_codes=['2513', '100', '700'])
print(df)

# 获取历史数据
scraper = ETNetHistoricalScraper()
df_hist = scraper.get_stock_short_selling_history('700', pages=3)
print(df_hist)

# 获取排行榜
top10 = seller.get_top(n=10, by='amount')
print(top10)
```

## 注意事项 Notes

1. 当天数据每日更新，通常在收市后晚上可获取
2. 只有当日有卖空交易的股票才会出现
3. 历史数据通过ETNet获取，约3个月历史
