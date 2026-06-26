[简体中文](./README_zh-CN.md) | **English**

# Macro News Signal

> **OpenClaw Skill** — Install at [https://clawhub.ai/zhelincheng/macro-news-signal](https://clawhub.ai/zhelincheng/macro-news-signal)

---

## Overview

Macro News Signal converts fragmented global financial news and macroeconomic indicators into **structured, actionable investment decision support data** through automated collection, deep parsing, sentiment analysis, and multi-dimensional aggregation.

## Demo

![Skill Result](./screenshot/result.png)

---

## Workflow

```
┌─────────────┐    ┌──────────────────┐    ┌───────────────┐
│ News Request │ -> │ Source Identify  │ -> │Automated Collect│
└─────────────┘    └──────────────────┘    └───────────────┘
                                                      │
                                                      v
┌─────────────┐    ┌──────────────────┐    ┌───────────────┐
│Aggregation  │ <- │ Signal Generation│ <- │Parsing & NLP  │
└─────────────┘    └──────────────────┘    └───────────────┘
```

---

## Step 1: Source Identification

Identify appropriate news sources based on request:

| Asset Class    | Main Sources                    | Type     |
|----------------|---------------------------------|----------|
| Equities       | 10JQKA, Bloomberg, CNBC        | RSS      |
| Fixed Income   | Fed Speeches, Indices, BoE      | RSS/API  |
| Commodities    | EIA, OPEC, Metals Bulletin      | Web      |
| Forex          | Central Banks, MNI              | Web      |
| General Macro  | WSJ, FT, Economist, Zaobao     | RSS      |

---

## Step 2: Collection

Use appropriate methods based on source type:

- **RSS Feeds**: See `references/news_apis.md`
- **Web Pages**: Prioritize agent-browser skill if available for dynamic access; otherwise use default scraping method
- **APIs**: See `references/news_apis.md`

Example curl request from `references/news_apis.md`:

```bash
curl 'url' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'accept-language: zh-CN,zh;q=0.9' \
  -H 'cache-control: no-cache' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
```

---

## Step 3: Parsing & Analysis

This stage uses NLP to extract core variables from unstructured text:

### 1. Named Entity Recognition (NER)
Automatically identify specific assets (e.g., `$NAS100$), economic indicators (e.g., `$CPI$, `$TIPS`), and key persons or geographic regions.

### 2. Sentiment Polarity
| Type                  | Description                                              |
|-----------------------|----------------------------------------------------------|
| Hawkish/Dovish        | Quantify policy bias for central bank communications     |
| Bullish/Bearish       | Calculate text sentiment score $S$ based on financial dictionaries |

### 3. Forecast Comparison
When news involves economic data releases, automatically compare "actual" vs "expected" values and calculate deviation.

---

## Step 4: Signal Generation

Transform parsed analysis into quantified investment logic:

| Signal Type          | Description                                                                  |
|----------------------|------------------------------------------------------------------------------|
| **Impact Level**     | Flash (instantaneous volatility), Secondary (minor impact), Trend-Setting (major trend) |
| **Indicator Relevance** | Calculate mapping intensity to specific assets (e.g., gold vs 10Y TIPS yield divergence) |
| **Logic Validation** | Detect divergence signals such as "bullish exhaustion" or "overheated sentiment" |

---

## Step 5: Aggregation

Aggregate analysis results to generate structured reports:

- **Time Window**: Daily summary, weekly in-depth review
- **Core Themes**: Inflation, GDP, Employment, Central Bank Dynamics, Geopolitics
- **Region**: United States, China, European Union, Emerging Markets
- **Asset Class Recommendations**:

| Recommendation | Condition                                           |
|----------------|-----------------------------------------------------|
| *Buy*          | Strong bullish signal with reasonable sentiment     |
| *Hold*         | Neutral signal or data vacuum period               |
| *Sell*         | Structural bearish or extremely overheated sentiment |

---

## Resources

### references/

| File            | Content                                      |
|-----------------|----------------------------------------------|
| `news_apis.md`  | News API documentation and endpoints         |
| `output_format.md`| Output format              |

---

## License

MIT-0 License — This project is released into the public domain under the MIT-0 license with no rights reserved.
