# 牛牛量化技能

## 技能描述

专业的股票量化交易技能，提供股票数据分析、策略回测、智能选股、交易信号等功能。

## 功能列表

### 1. 股票数据查询
- 实时股价查询
- K 线数据获取
- 财务数据分析
- 技术指标计算

### 2. 量化策略
- 均线策略
- MACD 策略
- KDJ 策略
- 布林带策略
- 自定义策略

### 3. 智能选股
- 技术面选股
- 基本面选股
- 资金流选股
- 热点题材选股

### 4. 交易信号
- 买入信号
- 卖出信号
- 持仓建议
- 风险提示

## 使用方式

### 命令行调用
```bash
# 查询股票信息
nn-quant stock 600519

# 运行策略回测
nn-quant backtest --strategy ma --stock 600519

# 智能选股
nn-quant select --type technical

# 获取交易信号
nn-quant signal 600519
```

### API 调用
```python
import requests

# 查询股票
response = requests.get('http://localhost:5000/api/stock/600519')

# 运行策略
response = requests.post('http://localhost:5000/api/strategy/run', json={
    'strategy': 'ma',
    'stock': '600519'
})

# 智能选股
response = requests.get('http://localhost:5000/api/select/technical')
```

## 配置说明

### 环境变量
```bash
export NN_QUANT_API_KEY=your_api_key
export NN_QUANT_DATA_SOURCE=tushare
export NN_QUANT_CACHE_DIR=~/.nn-quant/cache
```

### 配置文件
```yaml
# ~/.nn-quant/config.yaml
data_source: tushare
api_key: your_api_key
cache_enabled: true
log_level: INFO
```

## 依赖安装

```bash
pip install niuniu-quant
pip install tushare
pip install pandas
pip install ta-lib
```

## 示例

### 查询贵州茅台
```bash
nn-quant stock 600519
```

输出：
```
贵州茅台 (600519)
当前价格：1750.00 元
涨跌幅：+2.5%
成交量：123456 手
成交额：21.6 亿
52 周最高：1900.00
52 周最低：1500.00
```

### 均线策略回测
```bash
nn-quant backtest --strategy ma --stock 600519 --days 250
```

输出：
```
策略：均线策略
股票：贵州茅台 (600519)
回测周期：250 天
初始资金：100000
最终收益：125000
收益率：25%
最大回撤：-8.5%
夏普比率：1.85
```

## 风险提示

⚠️ 量化交易有风险，投资需谨慎！

- 历史业绩不代表未来收益
- 策略可能失效
- 市场风险不可控
- 请合理配置资金

## 技术支持

- 文档：https://niuniu-quant.readthedocs.io
- 问题反馈：https://github.com/niuniu-quant/issues
- 交流群：QQ 群 123456789

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基础股票查询
- 支持均线策略
- 支持智能选股

### v1.1.0
- 新增 MACD 策略
- 新增 KDJ 策略
- 优化选股算法
- 提升回测速度
