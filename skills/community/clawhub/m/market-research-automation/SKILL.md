---
name: market-research-automation
description: Market research automation skill. Mine user pain points from social media and analyze competitors. Applicable for market validation before product launch, user needs analysis, and competitor feature comparison.
---

# Market Research Automation

Mine user pain points from social media and analyze competitors. Applicable for market validation before product launch, user needs analysis, and competitor feature comparison.

## Trigger Conditions

- Market research
- Competitor analysis
- market research
- competitor analysis
- User research
- survey generation
- TAM SAM SOM
- Market size estimation

## Core Capabilities

### Capability 1: Market Sizing — TAM/SAM/SOM Three-Layer Model
Estimate the Total Addressable Market (TAM), Serviceable Available Market (SAM), and Serviceable Obtainable Market (SOM) for a target market.

### Capability 2: In-Depth Competitor Analysis — Feature/Pricing/User Review Comparison Matrix
Compare multiple competitors across dimensions such as features, pricing, target users, strengths, and weaknesses.

### Capability 3: Automatic Generation of User Interview Frameworks and Survey Questionnaires
Automatically generate structured user survey questionnaires based on the research topic.

## Usage Workflow

### Scenario 1: Market Sizing Research

```bash
python3 scripts/market_researcher_tool.py research --market 'AI Writing Tools'
```

### Scenario 2: Competitor Analysis

```bash
python3 scripts/market_researcher_tool.py compete --products 'Jasper,Copy.ai,Notion AI'
```

### Scenario 3: Generate Survey Questionnaire

```bash
python3 scripts/market_researcher_tool.py survey --topic 'AI Writing Tools'
```

## Command Details

### `research` - Market Research

**Purpose**: Estimate market size and generate a TAM/SAM/SOM analysis report.

**Parameters**:
- `--market`: Market name (required)
- `--output, -o`: Output file path (optional, defaults to console output)

**Example**:
```bash
python3 scripts/market_researcher_tool.py research --market 'AI Writing Tools' -o report.md
```

### `compete` - Competitor Analysis

**Purpose**: Compare features, pricing, and user reviews of multiple competitors.

**Parameters**:
- `--products`: List of competitors, comma-separated (required)
- `--output, -o`: Output file path (optional)

**Example**:
```bash
python3 scripts/market_researcher_tool.py compete --products 'Jasper,Copy.ai,Notion AI,ChatGPT' -o compete.md
```

### `survey` - Generate Survey Questionnaire

**Purpose**: Automatically generate a structured user survey questionnaire.

**Parameters**:
- `--topic`: Research topic (required)
- `--output, -o`: Output file path (optional)

**Example**:
```bash
python3 scripts/market_researcher_tool.py survey --topic 'AI Writing Tools' -o survey.md
```

## Output Format

### Market Research Report

```markdown
# 📊 Market Research Automation Report

**Generated on**: YYYY-MM-DD HH:MM

## Key Findings
1. [Key Finding 1]
2. [Key Finding 2]
3. [Key Finding 3]

## Market Size Analysis (TAM/SAM/SOM)
| Metric | Value | Description |
|------|------|------|
| TAM | $XXX Billion | Total Addressable Market |
| SAM | $YYY Billion | Serviceable Available Market |
| SOM | $ZZZ Billion | Serviceable Obtainable Market |

## Actionable Recommendations
| Priority | Recommendation | Expected Outcome |
|--------|------|----------|
| 🔴 High | [Specific recommendation] | [Quantified expectation] |
```

### Competitor Analysis Report

```markdown
# 🔍 In-Depth Competitor Analysis Report

## Competitor Comparison Matrix
| Product | Pricing | User Rating | Target User | Key Strengths | Main Weaknesses |

## Competitive Strategy Recommendations
| Priority | Recommendation | Expected Outcome |
```

### User Survey Questionnaire

```markdown
# 📋 User Survey Questionnaire

## Basic Information
**Q1. What is your current job role?**
○ Product Manager ○ Marketing ○ Content Creation ...

## Current Usage
**Q2. How often do you use AI writing tools?**
○ Multiple times daily ○ Once daily ...

## Pain Points and Needs
**Q3. What feature would you most like to see improved in AI writing tools?**
________________________________________
```

## Prerequisites

Install Python dependencies before first use:

```bash
pip install requests beautifulsoup4 pandas
```

## References

- [X/Twitter API](https://developer.x.com/en/docs/x-api) - User discussion data
- [Google Trends](https://www.google.com/trends/) - Search trend analysis
- [Full Market Research Agent Use Case](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/market-research-product-factory.md)

## Notes

- All analysis is based on data obtained by the script; data is not fabricated.
- Missing data fields are marked "Data Unavailable" rather than guessed.
- It is recommended to combine with human judgment; AI analysis is for reference only.
- The current version uses mock data and can be extended to real API calls.