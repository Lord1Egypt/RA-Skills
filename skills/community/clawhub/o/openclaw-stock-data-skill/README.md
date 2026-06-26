# 股票数据 API Skill for OpenClaw

这是一个为 OpenClaw 等 Agent 工具设计的股票数据 Skill，提供了 A 股市场及周边资产的完整数据访问能力。

## 📋 数据分类概览

1. **股票历史数据**  
   - 日 K 线（前复权/不复权）、分钟级历史、日度财务因子、估值、复权因子、历史快照等  
   - 典型函数：`get_daily_data`、`get_history_data`、`get_finance_data`、`get_daily_adj_data`、`get_adj_factor`、`get_stock_snapshot_daily` 等

2. **股票实时数据**  
   - 集合竞价、基础快照、推送快照历史、停牌信息等  
   - 典型函数：`get_call_auction`、`get_basic_snapshot`、`get_stock_snapshot_push_history`、`get_stock_suspension` 等

3. **可转债历史和实时数据**  
   - 可转债日线、分钟级行情、日度指标（纯债价值、转股溢价等）、收盘快照、基础列表等  
   - 典型函数：`get_bond_daily`、`get_bond_history`、`get_bond_indicator_daily`、`get_bond_closing_snapshot`、`get_bond_list` 等

4. **ETF 数据**  
   - ETF 日线与分钟级历史行情  
   - 典型函数：`get_etf_daily`、`get_etf_history`

5. **指数历史数据**  
   - 指数分钟级历史行情（支持多种时间粒度）  
   - 典型函数：`get_index_history`

> 此外还提供 **条件搜索等高级能力**，详见 `stock_api.py` 与 `skill.json`。

## 🚀 快速开始

### 1. 注册账号并开通接口权限

**重要：使用本 Skill 前，必须先注册账号并为需要使用的接口开通对应权限。**

1. 访问 [https://data.diemeng.chat/](https://data.diemeng.chat/)
2. 注册新账号或登录现有账号
3. 在 **个人中心 / 权限或套餐管理** 中，按需开通以下数据大类的访问权限：
   - 股票历史数据（行情、财务、估值等）
   - 股票实时数据（集合竞价、基础快照等）
   - 可转债数据（历史 & 实时）
   - ETF 数据
   - 指数历史数据
4. 在 **API 管理** 中创建并复制您的 **API Key**

> 如果未为某一类接口开通权限，即使配置了 API Key，也会收到 403 或权限不足的错误。

### 2. 在 Skill 页面配置 API Key（推荐）

在 OpenClaw / ClawHub 中启用本 Skill 时：

1. 打开 `openclaw-stock-skill` 的 Skill 配置页面
2. 在参数面板中将从 `data.diemeng.chat` 获取的 **API Key** 填入对应字段（通常是 `apiKey` 或 `STOCK_API_KEY`）
3. 保存后，网关会自动将该值注入到运行环境中（映射为 `STOCK_API_KEY` 环境变量）

这样使用本 Skill 时，无需在本机手动配置环境变量。

### 3. （可选）在本地代码中直接使用 API Key

如果你在自己的 Python 项目中直接使用 `stock_api.py`，可以按以下方式配置：

#### 方式一：环境变量

```bash
# Linux/macOS
export STOCK_API_KEY="your_api_key_here"

# Windows PowerShell
$env:STOCK_API_KEY="your_api_key_here"

# Windows CMD
set STOCK_API_KEY=your_api_key_here
```

#### 方式二：在代码中设置

```python
import os
os.environ["STOCK_API_KEY"] = "your_api_key_here"
```

### 3. 安装依赖

```bash
pip install requests
```

或使用 requirements.txt：

```bash
pip install -r requirements.txt
```

## 📖 使用示例

### 基本使用

```python
from stock_api import get_stock_list, get_daily_data, search_stock_by_name

# 1. 获取股票列表
stocks = get_stock_list(page_size=10)
print(f"共有 {stocks['total']} 只股票")
for stock in stocks['list']:
    print(f"{stock['stock_code']}: {stock['name']}")

# 2. 搜索股票
results = search_stock_by_name("平安")
for stock in results:
    print(f"{stock['stock_code']}: {stock['name']}")

# 3. 获取日K线数据
daily_data = get_daily_data(
    stock_code="600000.SH",
    start_time="2024-01-01",
    end_time="2024-01-31"
)
print(f"共 {daily_data['total']} 条数据")
for record in daily_data['list'][:5]:
    print(f"{record['trade_date']}: 收盘价 {record['close']}")
```

### 获取多只股票数据

```python
from stock_api import get_daily_data

# 同时查询多只股票
data = get_daily_data(
    stock_code=["600000.SH", "000001.SZ", "000002.SZ"],
    start_time="2024-01-01",
    end_time="2024-01-31"
)
```

### 获取历史分时数据（股票分钟级）

```python
from stock_api import get_history_data

# 获取5分钟级别数据
data = get_history_data(
    stock_code="600000.SH",
    level="5min",
    start_time="2024-01-15 09:30:00",
    end_time="2024-01-15 15:00:00"
)
```

### 获取财务数据（股票日度因子）

```python
from stock_api import get_finance_data

# 获取财务指标
finance = get_finance_data(
    stock_code="600000.SH",
    start_time="2024-01-01",
    end_time="2024-01-31"
)

for record in finance['list']:
    print(f"日期: {record['trade_date']}")
    print(f"PE(TTM): {record['pe_ttm']}")
    print(f"PB: {record['pb']}")
    print(f"总市值: {record['total_mv']}")
```

### 获取股票估值（A 股）

```python
from stock_api import get_stock_valuation

# 按PE百分位排序
valuation = get_stock_valuation(
    sort_by="pe_percentile",
    sort_order="asc",
    limit=20
)

for stock in valuation:
    print(f"{stock['stock_code']} - {stock['stock_name']}")
    print(f"  PE(TTM): {stock['pe_ttm']}")
    print(f"  PE百分位: {stock['pe_percentile']}%")
```

### 获取可转债数据

```python
from stock_api import (
    get_bond_daily,
    get_bond_history,
    get_bond_indicator_daily,
)

# 1. 获取可转债日线数据
daily = get_bond_daily(
    stock_code="110031.SH",
    start_time="2024-01-01",
    end_time="2024-01-31",
)

# 2. 获取可转债 5 分钟级历史数据
history = get_bond_history(
    stock_code="110031.SH",
    level="5min",
    start_time="2024-01-02 09:30:00",
    end_time="2024-01-02 15:00:00",
)

# 3. 获取可转债日度指标（纯债价值、转股溢价等）
indicator = get_bond_indicator_daily(
    stock_code="110031.SH",
    start_date="2024-01-01",
    end_date="2024-01-31",
)
```

### 获取 ETF 数据

```python
from stock_api import get_etf_daily, get_etf_history

# 1. 获取 ETF 日线数据
etf_daily = get_etf_daily(
    stock_code="510300.SH",
    start_time="2024-01-01",
    end_time="2024-01-31",
)

# 2. 获取 ETF 5 分钟级历史数据
etf_history = get_etf_history(
    stock_code="510300.SH",
    level="5min",
    start_time="2024-01-02 09:30:00",
    end_time="2024-01-02 15:00:00",
)
```

### 获取指数历史数据

```python
from stock_api import get_index_history

# 获取指数 1 分钟级历史数据
index_history = get_index_history(
    index_code="000300.SH",  # 沪深 300 指数
    level="1min",
    start_time="2024-01-02 09:30:00",
    end_time="2024-01-02 15:00:00",
)
```

## 🔧 API 接口说明

### 股票代码格式

- 上海：`600000.SH`、`688000.SH`
- 深圳：`000001.SZ`、`300000.SZ`
- 北京：`430000.BJ`、`830000.BJ`

### 时间格式

- 日期：`YYYY-MM-DD`，例如 `2024-01-15`
- 日期时间：`YYYY-MM-DD HH:MM:SS`，例如 `2024-01-15 09:30:00`

### 分时级别

- `1min` - 1分钟
- `5min` - 5分钟（默认）
- `15min` - 15分钟
- `30min` - 30分钟
- `60min` - 60分钟

## 📚 完整 API 文档

更多详细的 API 文档请访问：[https://data.diemeng.chat/](https://data.diemeng.chat/)

## ⚠️ 注意事项

1. **API Key 安全**：请妥善保管您的 API Key，不要将其提交到公开代码仓库
2. **请求频率**：请注意 API 的请求频率限制，避免过于频繁的请求
3. **数据范围**：部分接口支持查询全市场数据，但建议使用分页参数控制返回数量
4. **错误处理**：所有函数在出错时会抛出异常，请做好异常处理

## 🐛 常见问题

### Q: 提示 "未找到 API Key"

A: 请确保已设置环境变量 `STOCK_API_KEY`，或访问 [https://data.diemeng.chat/](https://data.diemeng.chat/) 注册并获取 API Key。

### Q: 返回 401 未授权错误

A: 请检查 API Key 是否正确，并确保已在个人中心激活 API 访问权限。

### Q: 返回 403 权限不足

A: 您的账号可能没有访问该接口的权限，请检查您的账号权限设置。

### Q: 如何获取更多数据？

A: 使用 `page` 和 `page_size` 参数进行分页查询，或联系管理员提升账号权限。

## 📝 更新日志

### v1.0.0 (2024-01-XX)
- 初始版本发布
- 支持股票列表、日K线、历史分时、财务数据等核心功能
- 支持股票搜索和估值查询

## 📄 许可证

MIT License

## 🔗 相关链接

- API 文档：[https://data.diemeng.chat/](https://data.diemeng.chat/)
- 注册账号：[https://data.diemeng.chat/](https://data.diemeng.chat/)
- GitHub 仓库：[查看项目源码](https://github.com)（创建仓库后更新此链接）
- GitHub 推送指南：[GITHUB.md](./GITHUB.md)

## 📤 推送到 GitHub

**是的，建议推送到 GitHub！** OpenClaw 有官方的 Skills 生态，你可以：

1. **推送到个人 GitHub 仓库** - 便于版本控制和分享
2. **提交到 OpenClaw Skills 生态** - 让更多用户发现和使用你的 skill
3. **通过 ClawHub 平台发布** - OpenClaw 的官方 Skills 管理平台

详细步骤请查看 [GITHUB.md](./GITHUB.md) 文件。

---

**重要提示**：使用本 Skill 前，请务必访问 [https://data.diemeng.chat/](https://data.diemeng.chat/) 注册并获取 API Key！
