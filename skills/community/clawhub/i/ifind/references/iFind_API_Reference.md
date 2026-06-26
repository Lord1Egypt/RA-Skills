# iFinD API Reference

Skill name: `ifind`

This reference is copied from the user's local `~/iFind_API_Reference.md` and documents the Python wrapper bundled in this skill.

## 目录
1. [类和方法总览](#类和方法总览)
2. [IFindAPI 类](#ifindapi-类)
3. [IFindHistoryData 类](#ifindhistorydata-类)
4. [IFindRealtimeData 类](#ifindrealtimedata-类)
5. [常量定义](#常量定义)
6. [响应格式](#响应格式)
7. [错误码表](#错误码表)

---

## 类和方法总览

### IFindAPI 类
核心API封装类,提供所有数据接口。

| 方法 | 说明 |
|------|------|
| `get_access_token()` | 获取access_token |
| `update_access_token()` | 刷新access_token |
| `get_history_data()` | 获取历史行情 |
| `get_real_time_quotation()` | 获取实时行情 |
| `get_high_frequency()` | 获取高频序列(分钟级) |
| `get_snap_shot()` | 获取日内快照 |
| `get_basic_data()` | 获取基础数据(财务指标) |
| `get_date_sequence()` | 获取日期序列 |
| `get_trade_dates()` | 查询交易日 |
| `get_date_offset()` | 日期偏移计算 |
| `get_thscode()` | 证券代码转换 |
| `smart_stock_picking()` | 智能选股 |
| `get_data_volume()` | 数据量查询 |
| `get_error_message()` | 错误信息查询 |
| `query_report()` | 公告查询 |
| `get_edb_data()` | 经济数据库(EDB) |
| `get_data_pool()` | 专题报表 |
| `portfolio_*()` | 组合管理相关 |

### IFindHistoryData 类
历史行情专用便捷类。

| 方法 | 说明 |
|------|------|
| `get_ohlc()` | 获取OHLC数据 |
| `get_full_quote()` | 获取完整行情 |

### IFindRealtimeData 类
实时行情专用便捷类。

| 方法 | 说明 |
|------|------|
| `get_realtime()` | 获取实时行情 |
| `get_order_book()` | 获取十档委托 |

---

## IFindAPI 类

### 初始化

```python
from risk_parity_strategy.data.ifind_api import IFindAPI, REFRESH_TOKEN

api = IFindAPI(REFRESH_TOKEN)
```

### get_access_token()

获取或刷新access_token。

**返回**: `str` - access_token

```python
token = api.get_access_token()
```

### update_access_token()

强制刷新access_token(会使所有旧token失效)。

**返回**: `str` - 新的access_token

### get_history_data()

获取股票历史行情数据。

**参数**:
- `codes` (str): 股票代码,多个用逗号分隔,如 `"300033.SZ,600000.SH"`
- `startdate` (str): 开始日期,格式 `"YYYY-MM-DD"`
- `enddate` (str): 结束日期,格式 `"YYYY-MM-DD"`
- `indicators` (str): 指标列表,用逗号分隔
- `functionpara` (dict, optional): 函数参数

**返回**: `dict` - API响应

```python
result = api.get_history_data(
    codes="300033.SZ",
    startdate="2024-01-01",
    enddate="2025-03-14",
    indicators="open,high,low,close,volume"
)
```

### get_real_time_quotation()

获取股票实时行情。

**参数**:
- `codes` (str): 股票代码
- `indicators` (str): 指标列表
- `functionpara` (dict, optional): 函数参数

### get_high_frequency()

获取高频序列(分钟级K线)。

### get_snap_shot()

获取日内快照数据。

### get_basic_data()

获取基础数据(财务指标等)。

### get_date_sequence()

获取日期序列数据。

### get_trade_dates()

查询交易日。

### get_date_offset()

计算日期偏移。

### get_thscode()

证券代码/简称转换。

### smart_stock_picking()

智能选股搜索。

### get_data_volume()

查询数据量配额。

### query_report()

公告查询。

---

## IFindHistoryData 类

便捷的历史行情获取类。

### get_ohlc()

获取OHLC数据。

### get_full_quote()

获取完整行情数据。

---

## IFindRealtimeData 类

便捷的实时行情获取类。

### get_realtime()

获取实时行情。

### get_order_book()

获取实时行情(含十档委托)。

---

## 常量定义

### 复权类型 (IFindHistoryData)

```python
NO_ADJUST = "1"
FORWARD_ADJUST = "2"
BACKWARD_ADJUST = "3"
```

### 时间周期 (IFindHistoryData)

```python
DAILY = "D"
WEEKLY = "W"
MONTHLY = "M"
QUARTERLY = "Q"
SEMI_YEARLY = "S"
YEARLY = "Y"
```

---

## 响应格式

API返回JSON格式,结构如下:

```json
{
  "errorcode": 0,
  "errmsg": "Success!",
  "tables": [],
  "datatype": [],
  "dataVol": 10,
  "perf": 25
}
```

---

## 错误码表

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| -1300 | token无效 |
| -1301 | refresh_token无效 |
| -1302 | access_token无效 |
| -4219 | 权限不足 |
| -4400 | 每分钟最多600条请求 |

For full method details, examples, and longer indicator lists, read the original user file if deeper expansion is needed.
