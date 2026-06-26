---
description: Event-Driven Analysis Framework - Methodology for analyzing market events and their impact
---

# Event-Driven Analysis Framework

This framework provides methodology for analyzing major events, assessing market impact, identifying beneficiary stocks, and developing investment strategies. Users should provide event and news data for analysis.

## Analysis Steps

### Step 1: Financial Calendar Data Structure

When analyzing calendar events, the following data types are relevant (time span typically 7-40 days):

**Event Types**:
- Earnings calendar: Company earnings releases
- Dividend calendar: Dividend distribution events
- Economic data calendar: Macroeconomic indicators
- IPO calendar: New stock listings

**Required Data Fields**: date, event_type, company/symbol, market, description

### Step 2: News Data Analysis Framework

When analyzing financial news, consider these data sources:

**News Categories**:
- Market-specific news (by country/region)
- Symbol-specific news (company announcements)
- Economic news (policy, macro data)

**Analysis Dimensions**:
- News headline and summary
- Publication time and source
- Related symbols/sectors
- Sentiment indicators

### Step 3: Extract Event Keywords

Extract from calendar events and news data:
- **Company name/symbol**: Directly related stocks
- **Industry keywords**: Used to identify same-industry beneficiary stocks
- **Policy keywords**: Used to expand impact scope
- **Event type**: Earnings beat/policy positive/industry event/breaking news

### Step 4: Beneficiary Stock Identification Framework

**Search Strategy**:
- Use extracted keywords to identify related stocks
- For industry events, analyze same-sector stocks via market leaderboards
- Filter by asset type (stocks), market code, and relevance

**Data Requirements**:
- Stock search results with symbols and descriptions
- Leaderboard data showing gainers/losers by sector
- Market overview data (price, volume, market cap)

### Step 5: Technical Confirmation Analysis

For identified beneficiary stocks (5-10), analyze:

**Quote Data**: Real-time or recent price, volume, change percentage
**Technical Analysis**: RSI, MACD, moving averages, support/resistance levels
**Recommendation Signals**: Buy/Sell/Neutral based on technical indicators

### Step 6: Assess Impact Level

Assess each beneficiary stock:

| Factor | Weight | Assessment Dimension |
|--------|--------|---------------------|
| Event Importance | 30% | Fundamental impact on industry/company |
| Relevance | 25% | Direct correlation between stock and event |
| Timeliness | 20% | Duration of event impact |
| Expectation Gap | 15% | Whether market has fully priced in |
| Certainty | 10% | Certainty of event materialization |

Impact levels:
- **Strong Positive (+3)**: Direct beneficiary, clear earnings improvement
- **Positive (+2)**: Indirect beneficiary, industry prosperity improvement
- **Slight Positive (+1)**: Sentiment positive
- **Neutral (0)**: Limited impact
- **Negative (-1/-2/-3)**: Symmetrical negative impact

### Step 7: Generate Analysis Report

```markdown
# Event-Driven Analysis Report

## Event Overview
- Event: [Event description]
- Time: [Occurrence/expected time]
- Type: [Earnings/Policy/Industry/Breaking]
- Importance: [High/Medium/Low]

## Impact Analysis
- Direct impact: ...
- Indirect impact: ...
- Impact duration: [Short-term/Medium-term/Long-term]

## Beneficiary Stock Analysis

### 1. [Stock Name] (Symbol) - Impact Level: +3
- Relevance: Direct beneficiary, [reason]
- Current price: ¥XX (Change XX%)
- Technical: RSI=XX, TA signal=[Buy/Sell]
- Trading recommendation: ...

### 2. [Stock Name] ...

## Risk Factors
- [Risk 1: Event materialization below expectations]
- [Risk 2: Market has fully priced in]

## Trading Recommendations
- Short-term strategy: ...
- Medium-term strategy: ...
```

## Example

**User**: "Analyze the impact of cloud computing price increases on related companies"

**Analysis Framework**:
1. Review news data about cloud computing price changes
2. Extract news details and key information
3. Search for cloud computing related stocks by keyword
4. Check gainers list to verify market reaction
5. Analyze quotes and technical indicators for identified stocks
6. Assess impact level and generate analysis report

**Note**: This framework describes the analytical methodology. Users should provide relevant market data, news content, and stock information for analysis.
