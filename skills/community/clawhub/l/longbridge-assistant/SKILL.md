---
name: longbridge-assistant
description: "长桥证券智能投资助手。自动监控持仓、生成投资组合可视化图表、智能止盈止损提醒。Use when: user asks about 长桥持仓、投资组合分析、止盈止损、股票监控、portfolio analysis、price alerts. Features: 实时获取49+只股票持仓、港股/美股分开可视化、价格触发提醒、投资建议。"
homepage: https://open.longportapp.com
metadata:
  openclaw:
    emoji: "🦞"
    requires:
      bins: ["python3"]
      env: ["LONGBRIDGE_APP_KEY", "LONGBRIDGE_APP_SECRET", "LONGBRIDGE_ACCESS_TOKEN"]
---

# 长桥智能投资助手

自动监控长桥证券持仓，提供智能止盈止损提醒、投资组合分析和可视化图表。

## When to Use

✅ **USE this skill when:**

- "查看我的长桥持仓"
- "投资组合分析"
- "止盈止损提醒"
- "生成持仓图表"
- "监控股票价格"
- "portfolio analysis"
- "price alerts"

## When NOT to Use

❌ **DON'T use this skill when:**

- 其他券商账户（如富途、老虎）
- 实时交易执行（仅监控提醒）
- 技术分析指标（K线、MACD等）
- 历史交易记录查询

## Commands

### 查看持仓

```bash
cd ~/.qclaw/workspace/skills/longbridge-assistant
./run.sh
```

### 配置 API

```bash
./setup.sh
```

### 自定义监控

编辑 `longbridge_skill.py` 中的 `ALERTS` 字典：

```python
ALERTS = {
    'AAPL.US': [
        {'price': 150.0, 'action': 'buy_more', 'msg': '苹果回调至$150，建议加仓'},
        {'price': 200.0, 'action': 'sell_partial', 'msg': '苹果涨至$200，建议减仓'},
    ],
}
```

## Example Output

```
🦞 长桥智能投资助手 v2.0.0

📊 获取持仓及市值信息...
✅ 获取成功，共 49 只持仓
💰 总市值: $1,769,599

📈 生成投资组合图表...
   ✅ 图表已保存: portfolio_chart.png

📋 前10大持仓:
 1. 🟢 小米(1810.HK)     10700股 @ $33.20 = $355,240
 2. 🟢 7226.HK           60000股 @ $3.86  = $231,600
 ...

🔔 价格提醒检查:
   ⚠️  SMCI 当前 $22.15，低于目标 $35

📊 组合分析:
   总持仓: 49 只
   做多: 41 只 ($1,715,764)
   做空: 8 只 ($53,835)
   净值: $1,661,929

   💡 建议: 持仓过于分散，建议集中优质标的
```

## Setup

### 1. 安装依赖

```bash
pip install longbridge matplotlib
```

### 2. 配置 API Token

创建文件 `~/.longbridge/env`：

```bash
export LONGBRIDGE_APP_KEY="你的AppKey"
export LONGBRIDGE_APP_SECRET="你的AppSecret"
export LONGBRIDGE_ACCESS_TOKEN="你的AccessToken"
```

获取方式：https://open.longportapp.com

### 3. 运行

```bash
./run.sh
```

## Features

| 功能 | 说明 |
|------|------|
| 持仓监控 | 自动获取49+只股票 |
| 可视化 | 港股/美股分开饼图 |
| 止盈止损 | 价格触发提醒 |
| 投资建议 | 持仓分析建议 |

## Notes

- 需要长桥 OpenAPI 权限
- API 有调用频率限制
- 仅供参考，不构成投资建议

## Version

v2.0.0 (2026-03-23)
