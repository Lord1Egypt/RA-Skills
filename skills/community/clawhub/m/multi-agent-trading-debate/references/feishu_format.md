# Feishu Trading Debate Formats

## Trading Team Group ID
```
oc_e8921bddaed45af1209cb76353d484a8
```

## Agent Roles

| Agent | Feishu ID | Role |
|-------|-----------|------|
| trading-lead | @trading-lead | Coordinator, does not trade |
| trading-risk | @trading-risk | Risk审核 |
| trading-execution | @trading-execution | 执行订单 |
| technical-analyst | @technical-analyst | K线技术分析 |
| onchain-analyst | @onchain-analyst | 链上数据 |
| sentiment-analyst | @sentiment-analyst | 情绪分析 |
| trading-bull | @trading-bull | 看多 |
| trading-bear | @trading-bear | 看空 |
| trading-judge | @trading-judge | 最终裁决 |
| ops-monitor | @ops-monitor | 资金统计 |

## Message Templates

### 1. Debate Trigger
```
📊 【批次 #YYYYMMDD-NNN 自动辩论触发】

⚠️ 当前持仓状态：
- 方向：{DIRECTION}
- 数量：{SIZE} {ASSET}
- 开仓价：{ENTRY} USDT
- 当前价：{CURRENT} USDT
- 浮亏：{PNL} USDT

🔍 Regime检测：{REGIME}（ADX: {ADX}）

请各位分析师给出判断：

@technical-analyst K线形态分析
@onchain-analyst 链上大户动向  
@sentiment-analyst 市场情绪
@trading-bull 看多理由+目标点位
@trading-bear 看空理由+目标点位

截止时间：{TIME}，留给 trading-judge 裁决。
```

### 2. Judge Verdict
```
📋 【交易裁决 #YYYYMMDD-NNN】

Regime: {REGIME}
Confidence: {CONFIDENCE}%
Signal: {SIGNAL}
Position: {SIZE} @ {PRICE}

多空摘要：
🟢 多头：{BULL_SUMMARY}
🔴 空头：{BEAR_SUMMARY}

裁决：{DECISION}
理由：{REASON}
风险等级：{RISK_LEVEL}
止损：{STOP_LOSS}
下一审查：{NEXT_REVIEW}
```

### 3. Execution Command to trading-execution
```
@trading-execution 执行订单：

方向：{SIDE}
数量：{SIZE}
品种：{ASSET}
类型：市价

附注：{NOTES}
```

### 4. Position Update to ops-monitor
```
@ops-monitor 仓位更新：

方向：{DIRECTION}
数量：{SIZE}
开仓价：{ENTRY}
当前价：{CURRENT}
浮盈：{PNL}
执行时间：{EXEC_TIME}
```

## Cron Schedule

| Time (CST) | Batch | Focus |
|-----------|-------|-------|
| 08:00 | #YYYYMMDD-001 | 亚盘开盘 review |
| 12:00 | #YYYYMMDD-002 | 欧美盘前调整 |
| 16:00 | #YYYYMMDD-003 | 欧美盘 review |
| 20:00 | #YYYYMMDD-004 | 美盘核心窗口 |
