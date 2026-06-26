# 安装与配置指南

## 1. 获取 Tushare 代理 Token

### 为什么需要代理版？

官方 Tushare 的免费积分有限（200积分），无法使用分钟线等高级接口。
闲鱼可购买代理版 Token（约38元/月），提供15000+积分，覆盖所有需要的接口。

### 购买方式

1. 闲鱼搜索 "tushare 代理" 或 "tushare 积分"
2. 选择15000积分以上的套餐
3. 获取: Token 字符串 + 代理 API 地址

### 验证 Token

```python
import urllib.request
import json

token = "你的token"
api_url = "你的代理地址"

req = {
    "api_name": "daily",
    "token": token,
    "params": {"ts_code": "000001.SZ", "start_date": "20260401", "end_date": "20260430"}
}
data = json.dumps(req).encode("utf-8")
request = urllib.request.Request(api_url, data=data, headers={"Content-Type": "application/json"})
resp = urllib.request.urlopen(request, timeout=10)
result = json.loads(resp.read().decode("utf-8"))
print("OK" if result.get("code") == 0 else "FAIL")
```

## 2. 项目结构

```
institutional_tracker/
├── config.py              # 配置（Token、权重、路径）
├── data_fetcher.py         # Tushare + NeoData 数据采集层
├── signal_engine.py        # 5维信号评分引擎（核心）
├── market_regime.py        # 市场环境判断（11指标）
├── sentiment_aggregator.py # 外部情绪聚合（5源）
├── state_tracker.py        # 状态连续确认
├── main.py                 # 主程序（每日扫描）
├── backtest_v2.py          # 大规模回测
├── data/                   # 数据目录
│   └── daily_scores/       # 每日评分JSON
└── reports/                # 生成的HTML报告
```

## 3. 配置 config.py

```python
# === 必须修改 ===
TUSHARE_TOKEN = "你的token"
TUSHARE_API_URL = "http://你的代理地址"

# === 可选调整 ===
TUSHARE_RATE_LIMIT = 0.6  # 请求间隔（秒），代理版一般0.5即可

# 信号权重（已经过回测优化，不建议大幅修改）
WEIGHTS = {
    "fund_flow": 0.30,
    "volume_price": 0.24,
    "chip_dist": 0.18,
    "north_margin": 0.16,
    "event": 0.12,
}
```

## 4. 修改标的池

在 `main.py` 的 `build_stock_pool()` 中修改 `core_stocks` 列表：

```python
core_stocks = [
    ("你关注的股票名", "代码.交易所", "赛道标签"),
    ("中际旭创", "300308.SZ", "光模块龙头"),
    ...
]
```

注意：代码格式必须是 `XXXXXX.SZ`（深圳）或 `XXXXXX.SH`（上海）。

## 5. 创建目录

```bash
mkdir -p ./institutional_tracker/data/daily_scores
mkdir -p ./institutional_tracker/reports
```

## 6. 运行

```bash
# 首次运行（完整扫描，约5-15分钟）
cd ./institutional_tracker
python3 main.py

# 回测（约30-60分钟，取决于网络速度）
python3 backtest_v2.py
```

## 7. 设置自动化

### WorkBuddy 自动化

在 WorkBuddy 中创建两个自动化任务：

**每日扫描（每个交易日16:35）**：
```
cd ~/institutional_tracker && python3 main.py
```

**每周评估（每周五17:30）**：
```
评估本周 institutional_tracker 产出的信号实际收益，对比基准胜率55.3%。
连续2周低于45%则标记算法失效。
```

### 微信推送

搭配 WorkBuddy 的微信推送功能，将报告摘要自动发送到微信。

## 8. 常见问题

### Q: 可以不用代理版 Tushare 吗？

可以，但功能受限：
- 免费版无法使用分钟线接口 → 日内分析维度缺失
- 免费版限速更严格 → 回测时间翻倍
- 建议至少购买200积分的基础版

### Q: 可以换成其他数据源吗？

可以。只需实现 `data_fetcher.py` 中对应接口返回相同格式的数据即可。
核心是：日线OHLCV、资金流向（超大/大/中/小单）、融资融券、北向资金。

### Q: 为什么只聚焦AI链条？

回测显示：
1. 全行业通用时信号噪音大，胜率下降约3-5%
2. AI链条标的波动大+机构关注度高，资金流信号更明显
3. 聚焦赛道减少了标的池大小，提高了单只分析的数据质量

### Q: 止损为什么是15%而不是8%？

A股日内涨跌停10%，两个交易日就可能触发8%止损。
回测显示15%止损在10日持有期内的最优止损/收益比。
