---
name: hk-stock-predictor
description: Analyze Hong Kong listed stocks and produce prediction-ready theses from price action, fundamentals, technicals, southbound flows, AH premium, liquidity, and event catalysts. Use when users ask for 港股, 港股通, 恒生, 港股预测, AH 溢价, 南向资金, or when turning HK stock research into time-bounded forecastable questions.
metadata: {"clawdbot":{"emoji":"📊","os":["darwin","linux","win32"]}}
---

# HK Stock Predictor

Research a Hong Kong listed stock or theme, then turn the analysis into clear, time-bounded predictions.

## Minimal Input

User can provide any of:

```json
{
  "symbol": "00700",
  "horizon": "30d"
}
```

```json
{
  "theme": "南向资金持续流入的恒生科技成分股",
  "horizon": "14d"
}
```

## Agent Normalization

Normalize input before analysis:

- `symbol`: keep the 5-digit HK code when possible, also map to `.HK` form for external data.
- `companyName`: resolve from ticker or user text.
- `horizon`: normalize to one of `5d|14d|30d|90d|event`.
- `benchmark`: default to `HSI` or `HSTECH` for tech-heavy names.
- `predictionType`: choose `direction|range|event|relative-performance`.

## Preferred Data Stack

If these skills are available, use them in this order:

1. `akshare-skill` for broad market and company data.
2. `hk-stock-analysis` for HK-specific analysis framework.
3. `cross-border-flow-tracker` for southbound flow and positioning.
4. `market-overview` for index and sector context.

Fallback sources if the skills are not installed:

- HKEX / HKEXnews
- AAStocks
- ET Net
- AASTOCKS southbound / short selling pages
- public financial data providers with clear source attribution

## Deterministic Workflow

1. Validate the target.
   - Reject symbols that cannot be resolved to a Hong Kong listed security.
   - If the user gives only a theme, narrow to 3-10 HK candidates first.
2. Build market context.
   - Capture `HSI`, `HSCEI`, and `HSTECH` direction.
   - Note sector rotation, overnight macro drivers, and any major policy headline.
3. Gather company facts.
   - Current price, market cap, 52-week range, valuation, earnings date, lot size, daily turnover.
4. Gather HK-specific signals.
   - Southbound net buy/sell trend.
   - Short selling ratio and unusual changes.
   - AH premium or discount if dual-listed.
   - Liquidity warning if turnover is weak or spread is wide.
5. Build the thesis.
   - State `bull`, `base`, and `bear` cases.
   - For each case, list 2-4 drivers and 1-2 invalidation signals.
6. Convert thesis into forecastable statements.
   - Use binary, range, or relative-performance formats.
   - Every statement must be time-bounded and externally resolvable.
7. Rank prediction candidates.
   - Prefer high observability, low ambiguity, and direct catalyst linkage.
   - Avoid questions that require subjective wording such as "表现好不好".
8. Return the analysis and top prediction candidates.

## Prediction Design Rules

Good prediction candidates:

- "Will 00700 close above HK$520 on or before 2026-04-30?"
- "Will 09988 outperform the Hang Seng Tech Index between now and 2026-05-15?"
- "Will 02318 report YoY net profit growth above 10% in the next earnings release?"

Avoid:

- vague targets without dates
- subjective wording
- multi-condition questions that resolve unclearly
- tiny illiquid stocks where resolution may be distorted

## Output

Return one structured object plus a readable summary.

```json
{
  "ok": true,
  "normalizedInput": {
    "symbol": "00700",
    "symbolYahoo": "0700.HK",
    "companyName": "Tencent Holdings",
    "horizon": "30d",
    "benchmark": "HSTECH",
    "predictionType": "direction"
  },
  "marketContext": {
    "indices": [],
    "sectorTone": "",
    "macroDrivers": []
  },
  "evidence": {
    "fundamental": [],
    "technical": [],
    "flow": [],
    "hkSpecific": []
  },
  "scenarioAnalysis": {
    "bull": [],
    "base": [],
    "bear": []
  },
  "predictionCandidates": [
    {
      "title": "",
      "type": "direction|range|event|relative-performance",
      "deadlineIsoUtc": "",
      "resolutionSource": "",
      "confidence": 0,
      "why": []
    }
  ],
  "recommendedPrediction": {
    "title": "",
    "deadlineIsoUtc": "",
    "confidence": 0,
    "keyRisks": []
  },
  "warnings": []
}
```

## Summary Template

```markdown
# [公司名称] ([代码].HK) 港股推演

## 核心判断
- 方向判断:
- 时间窗口:
- 相对基准:

## 关键证据
- 基本面:
- 技术面:
- 资金面:
- 港股特有因子:

## 三种情景
- Bull:
- Base:
- Bear:

## 可预测题目
1. [候选题目 1]
2. [候选题目 2]
3. [候选题目 3]

## 首选题目
- 题目:
- 截止时间:
- 置信度:
- 主要风险:
```

## If The User Wants Gougoubi Conversion

Convert the top prediction candidate into Gougoubi-ready fields:

- `marketName`: use the selected prediction title.
- `deadlineIsoUtc`: use the prediction deadline.
- `rules`: include exact resolution source, timezone, comparison field, and tie handling.
- `tags`: include `hong-kong-stocks`, sector tag, catalyst tag, and horizon tag.

## Boundaries

- Do not claim "all HK stocks" were checked unless the scan actually covered the full universe.
- Do not hide missing data. Surface gaps in `warnings`.
- Do not give investment advice phrased as certainty.
- Prefer liquid names and observable events when generating prediction questions.
