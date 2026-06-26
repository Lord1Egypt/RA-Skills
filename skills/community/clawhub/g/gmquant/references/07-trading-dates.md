# 交易日历查询

## get_trading_dates - 查询交易日列表

```python
get_trading_dates(exchange, start_date, end_date, df=False)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| exchange | str | 交易所代码：`'SHSE'`、`'SZSE'`、`'CFFEX'`、`'SHFE'`、`'DCE'`、`'CZCE'` 等 |
| start_date | str | 开始日期 `%Y-%m-%d` |
| end_date | str | 结束日期 `%Y-%m-%d` |
| df | bool | True=DataFrame，False=list[datetime] |

```python
from gm.api import *
set_token('YOUR_TOKEN')

# 获取上交所 2024 年全年交易日
dates = get_trading_dates('SHSE', '2024-01-01', '2024-12-31')
print(f'2024年共 {len(dates)} 个交易日')

# 返回 DataFrame
df = get_trading_dates('SHSE', '2024-01-01', '2024-01-31', df=True)
```

---

## get_previous_trading_date - 查询上一交易日

```python
get_previous_trading_date(exchange, date)
```

```python
prev = get_previous_trading_date('SHSE', '2024-01-15')
print('上一交易日:', prev)  # datetime 对象
```

---

## get_next_trading_date - 查询下一交易日

```python
get_next_trading_date(exchange, date)
```

```python
next_day = get_next_trading_date('SHSE', '2024-01-15')
print('下一交易日:', next_day)
```

---

## 实用场景

### 判断今天是否交易日
```python
from gm.api import *
from datetime import date

set_token('YOUR_TOKEN')
today = str(date.today())
dates = get_trading_dates('SHSE', today, today)
is_trading = len(dates) > 0
print('今天是否交易日:', is_trading)
```

### 获取本月所有交易日
```python
import calendar
from datetime import date

year, month = 2024, 12
_, last_day = calendar.monthrange(year, month)
start = f'{year}-{month:02d}-01'
end = f'{year}-{month:02d}-{last_day}'
dates = get_trading_dates('SHSE', start, end)
print(f'{year}年{month}月共 {len(dates)} 个交易日')
```
