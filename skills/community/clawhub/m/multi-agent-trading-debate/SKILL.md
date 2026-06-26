---
name: multi-agent-trading-debate
description: "Multi-agent trading debate framework for collective market decision-making. Use when a trading signal is detected or a position decision is needed. Triggers on: (1) Cron-triggered decision windows every 8 hours, (2) Significant price movements more than 5pct deviation from entry, (3) Manual request for team analysis, (4) Position review before execution. The debate follows a structured flow: regime detection, analyst reports, bull/bear arguments, judge verdict, execution or hold."
---

# Multi-Agent Trading Debate

A structured multi-agent debate system for financial market decisions. Agents represent distinct roles: regime detection, technical analysis, on-chain data, sentiment, bull perspective, bear perspective, and final judgment.

## Workflow

```
Signal Detected
     ↓
Regime Detection (trend/range/volatility)
     ↓
Analysts Report (technical + onchain + sentiment)
     ↓
Bull/Bear Arguments (independent positions)
     ↓
Trading Judge Verdict (confidence + position size)
     ↓
Execution → Prediction Log → Reflection
```

## Quick Start

1. Send debate batch to Feishu trading group
2. Wait for analyst reports (timeout: 25 minutes)
3. Collect all responses
4. Synthesize verdict with confidence score
5. Execute if signal confirmed, otherwise hold

## Debate Message Format

```markdown
📊 【批次 #[YYYYMMDD-NNN] 自动辩论触发】

🔍 Regime: [REGIME_RESULT]

当前持仓：[DIRECTION] [SIZE] @ [ENTRY] | 当前：[PRICE]
浮亏：-[AMOUNT] USDT

请各位分析师给出独立判断：
- technical-analyst: K线形态分析
- onchain-analyst: 链上大户动向
- sentiment-analyst: 市场情绪短期
- trading-bull: 看多理由（具体点位）
- trading-bear: 看空理由（具体点位）

@trading-judge 最终裁决，截止 [TIME]
```

## Judge Verdict Template

```markdown
📋 【交易裁决 #YYYYMMDD-NNN】

Regime: [REGIME]
Confidence: [0-100]%
Signal: [BUY/SELL/HOLD]
Position: [SIZE] @ [PRICE]

Bull case: [summary]
Bear case: [summary]

Decision: [ACTION] [REASON]
Risk: [RISK_LEVEL]
Next review: [TIME]
```

## Position Sizing

| Confidence | Max Position | Stop Loss |
|-----------|-------------|-----------|
| >80% | 100% | Tight (1.5%) |
| 60-80% | 75% | Standard (3%) |
| 40-60% | 50% | Wide (5%) |
| <40% | 25% or hold | No entry |

## Regime Detection Rules

| Regime | Description | Preferred Strategy |
|--------|-------------|-------------------|
| TRENDING | ADX > 25, clear direction | Momentum follow |
| RANGING | ADX < 20, no clear trend | Mean reversion |
| VOLATILE | High variance, uncertain | Reduced size, wider SL |

## Prediction Log Entry

After each decision, record in `predictions.jsonl`:

```json
{"timestamp":"ISO8601","regime":"TRENDING","signal":"HOLD","confidence":62,"reason":"No clear entry, ranging market","actual_outcome":"pending","pnl":0}
```

## Key Files

- Regime detector: `regime/detector.py` (ADX + trend analysis)
- Position sizer: `risk/position_sizer.py` (Kelly + risk budget)
- Prediction log: `data/predictions.jsonl`
- TCA log: `data/tca_log.jsonl`

## When to Trigger

✅ **Trigger debate:**
- Cron window: 08:00, 12:00, 16:00, 20:00 CST daily
- Price deviation > 5% from entry
- Major news event detected
- Manual request

🚫 **Skip debate (hold current position):**
- Confidence < 40%
- Regime unclear
- Risk/reward < 1.5
