---
name: portfolio-analysis
description: 股票持仓分析系统，用于管理股票投资组合，实时更新价格，分析盈亏，生成报告。使用当用户需要管理股票持仓、查看实时价格、分析盈亏情况、生成投资报告时。
version: 1.0.0
icon: 📊
metadata:
  clawdbot:
    emoji: 📊
    requires:
      bins: ["python"]
    install:
      - id: python-deps
        kind: pip
        packages:
          - requests
          - flask
        label: Install Python dependencies for portfolio analysis
---

# 股票持仓分析 Skill

提供股票投资组合管理、实时价格更新、盈亏分析和报告生成功能。

## 功能说明

本skill提供以下功能：

1. **持仓管理** - 添加、编辑、删除股票持仓记录，支持股票代码、名称、持仓数量、成本价的完整编辑
2. **实时价格更新** - 手动或自动更新持仓价格，支持多数据源，自动更新仅在交易时间执行
3. **盈亏分析** - 计算总市值、总成本、总盈亏、盈亏比例、个股盈亏、仓位占比等
4. **操作记录** - 自动记录所有操作历史，支持查看和追溯
5. **报告生成** - 生成Markdown格式的持仓报告，支持下载导出
6. **股票价格查询** - 查询单只股票的实时价格信息

## 使用方法

### 1. 启动系统

```python
from portfolio_system import PortfolioManager, start_server

# 启动Web服务器
start_server(host='0.0.0.0', port=5000, auto_update=True)
```

### 2. 使用API接口

```python
import requests

# 获取持仓数据
response = requests.get('http://localhost:5000/api/portfolio')
data = response.json()

# 更新价格
response = requests.post('http://localhost:5000/api/portfolio/update')

# 添加持仓
response = requests.post('http://localhost:5000/api/portfolio/add', json={
    'symbol': '600519',
    'name': '贵州茅台',
    'quantity': 100,
    'cost_price': 1800.00
})

# 查询股票价格
response = requests.get('http://localhost:5000/api/stock/price/600519')
```

### 3. 使用PortfolioManager类

```python
from portfolio_system import PortfolioManager

manager = PortfolioManager('portfolio.db')

# 添加持仓
result = manager.add_holding('600519', '贵州茅台', 100, 1800.00)

# 获取持仓数据
portfolio = manager.get_portfolio_data()

# 更新所有价格
result = manager.update_all_prices()

# 生成报告
result = manager.generate_report()
```

## API接口说明

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/portfolio` | GET | 获取持仓数据 |
| `/api/portfolio/update` | POST | 手动更新所有价格 |
| `/api/portfolio/add` | POST | 添加持仓 |
| `/api/portfolio/edit/<symbol>` | PUT | 编辑单个字段 |
| `/api/portfolio/edit-multiple/<symbol>` | PUT | 批量编辑持仓 |
| `/api/portfolio/delete/<symbol>` | DELETE | 删除持仓 |
| `/api/portfolio/logs` | GET | 获取操作记录 |
| `/api/portfolio/report` | GET | 生成持仓报告 |
| `/api/portfolio/export` | GET | 下载报告文件 |
| `/api/stock/price/<symbol>` | GET | 查询单只股票价格 |

## 依赖项

- requests
- flask

安装依赖：
```bash
pip install requests flask
```

## 交易时间

自动更新仅在以下时间段执行：
- 工作日（周一到周五）
- 上午：9:30 - 11:30
- 下午：13:00 - 15:00

## 股票代码格式

- 上海股票：6位数字代码（如 600519）
- 深圳股票：6位数字代码（如 000001）
- 创业板：300开头（如 300750）

## 数据精度

所有价格相关数据支持4位小数精度，包括：
- 成本价
- 当前价
- 盈亏额
- 盈亏百分比

## 颜色标识

- 红色：代表盈利
- 绿色：代表亏损

## 排序功能

持仓列表支持按以下字段排序：
- 股票名称
- 股票代码
- 市值
- 盈亏额
- 盈亏百分比
