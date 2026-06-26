# jqdatasdk 量化开发技能

基于 JoinQuant (聚宽) 官方 jqdatasdk SDK 的量化交易开发技能，帮助开发者使用 Python 进行量化交易策略开发和数据分析。

## 项目概述

本技能提供 jqdatasdk 的完整 API 参考、常用查询示例和二次开发指南，适用于：
- 量化交易策略开发
- 金融数据分析
- 因子研究
- 回测验证

## 参考项目

| 项目 | 路径 | 说明 |
|------|------|------|
| 官方 jqdatasdk | `https://github.com/JoinQuant/jqdatasdk.git` | 官方 Python SDK 源码 |
| 类型定义 | `https://github.com/stairclimber/joinquant_api.git` | 第三方 API 类型定义 |

## 功能特性

- **行情数据**: 日/分钟/K线/Tick/实时数据
- **财务数据**: 财报指标、市值、现金流
- **因子数据**: Alpha因子、风格因子、自定义因子
- **标的信息**: 股票、基金、指数、期货
- **行业概念**: 申万行业、聚宽行业、概念板块
- **资金流向**: 主力资金、超大单、大单等
- **融资融券**: 两融数据、标的列表

## 快速开始

```python
import jqdatasdk as jq

# 认证
jq.auth('username', 'password')

# 获取行情数据
df = jq.get_price('000001.XSHE', start_date='2024-01-01', end_date='2024-12-31')

# 获取指数成分股
stocks = jq.get_index_stocks('000300.XSHG')

# 获取财务数据
from jqdatasdk import finance
q = jq.query(finance.indicator.code, finance.indicator.eps).filter(
    finance.indicator.code == '000001.XSHE'
)
df = jq.get_fundamentals(q, date='2024-12-31')
```

## 目录结构

```
jqdatasdk-skill/
├── SKILL.md           # 技能主文件
├── README.md          # 说明文档
└── references/         # 参考文档目录
    └── api.md         # API详细参考
```

## 主要API分类

### 认证与配置
- `jq.auth()` - 账号认证
- `jq.auth_by_token()` - Token认证
- `jq.is_auth()` - 认证状态
- `jq.set_params()` - 请求参数

### 行情数据
- `get_price()` - 行情数据
- `get_bars()` - K线数据
- `get_ticks()` - Tick数据
- `get_current_tick()` - 实时Tick

### 财务数据
- `get_fundamentals()` - 财务数据查询
- `get_valuation()` - 市值数据
- `get_history_fundamentals()` - 历史财报

### 因子数据
- `get_factor_values()` - 因子值
- `get_all_alpha_101()` - Alpha101因子
- `get_all_alpha_191()` - Alpha191因子

## 安装依赖

```bash
pip install jqdatasdk pandas sqlalchemy
```

## 使用说明

当需要使用 jqdatasdk 进行量化开发时，此技能会自动提供：
1. API 使用指导
2. 查询示例代码
3. 错误处理建议
4. 性能优化建议
5. 二次开发参考

## 注意事项

1. 需要聚宽账号才能使用大部分功能
2. 注意 API 调用频率限制
3. 财务数据有发布延迟
4. 股票代码需使用聚宽标准格式

## 参考资源

- [聚宽官方文档](https://www.joinquant.com/help/api/)
- [财务数据字典](https://www.joinquant.com/data/dict/fundamentals)
- [指数数据](https://www.joinquant.com/indexData)
- [行业分类](https://www.joinquant.com/data/dict/plateData)
