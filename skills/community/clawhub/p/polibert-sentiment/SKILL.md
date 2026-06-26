---
name: polibert-sentiment
slug: polibert-sentiment
version: 1.0.0
homepage: https://github.com/GU-DataLab/PoliBERTweet
description: Political sentiment analysis using PoliBERTweet - a RoBERTa model pre-trained on 83M political tweets. Analyzes support, opposition, and stance toward political figures and events. Integrates with Reddit data for real-time political sentiment tracking.
changelog: |
  v1.0.0 - Initial release with PoliBERTweet integration, Reddit data support, and sentiment analysis pipeline
metadata:
  requires:
    python: ">=3.9"
    packages:
      - transformers>=4.18.0
      - torch>=1.10.2
      - praw>=7.8.1
    bins: []
  sources:
    - reddit
    - twitter
    - political_news
  authors:
    - name: AI Assistant
    - name: Georgetown University DataLab (PoliBERTweet model)
  license: MIT
---

# PoliBERT Sentiment Analysis

Political sentiment analysis skill powered by **PoliBERTweet** - a transformer model trained on 83 million political tweets (Georgetown University, LREC 2022).

## Overview

This skill provides political sentiment analysis capabilities using a specialized NLP model trained on political content. It can analyze sentiment toward political candidates, issues, and events from various data sources including Reddit, local files, or direct text input.

## Features

- **Sentiment Classification**: Support / Oppose / Neutral toward political targets
- **Stance Detection**: Issue-specific stance analysis (e.g., pro/anti immigration)
- **Entity Targeting**: Analyze sentiment toward specific politicians
- **Confidence Scoring**: Probability scores for each classification
- **Reddit Data Integration**: Auto-fetch political discussions from Reddit (free, read-only)
- **Batch Processing**: Analyze multiple texts from files or stdin
- **JSON Output**: Machine-readable results for integration with other tools

## When to Use

Use this skill when you need to:
- Analyze public sentiment toward political candidates or figures
- Track political opinion trends on social media
- Complement prediction market data with social sentiment
- Monitor political discourse around specific issues
- Aggregate opinions from Reddit political communities

## Model Information

- **Model**: PoliBERTweet
- **Architecture**: RoBERTa (Robustly Optimized BERT)
- **Training Data**: 83 million political tweets (2016-2020 US elections)
- **HuggingFace Hub**: `kornosk/polibertweet-political-twitter-roberta-mlm`
- **Model Size**: ~500MB
- **Academic Paper**: [LREC 2022](https://aclanthology.org/2022.lrec-1.801)
- **Institution**: Georgetown University DataLab

## Installation

### Prerequisites

```bash
# Python 3.9 or higher
python --version

# Install core dependencies
pip install transformers>=4.18.0 torch>=1.10.2

# Optional: Reddit data fetching
pip install praw>=7.8.1
```

### First Run

On first execution, the model will be automatically downloaded from HuggingFace Hub (~500MB):

```bash
python polibert_sentiment.py --text "Test"
```

## Data Sources

| Source | Method | Cost | Data Quality | Use Case |
|--------|--------|------|:------------:|:---------|
| **Reddit** | `--reddit` | Free | High | Real-time political discussions |
| **Local File** | `--file` | - | User-dependent | Batch analysis of collected data |
| **Stdin** | `--stdin` | - | User-dependent | Pipeline integration |
| **Direct Text** | `--text` | - | User-dependent | Quick testing and single analysis |

### Reddit Data

**Default Subreddits**: r/politics, r/Conservative, r/democrats, r/Republican, r/PoliticalDiscussion

**Note**: Reddit data fetching uses read-only mode (no API credentials required). Rate limits apply.

## Usage Examples

### 1. Single Text Analysis

```bash
python polibert_sentiment.py --text "J.D. Vance is the future of the Republican party"
```

**Output**:
```
Text: J.D. Vance is the future of the Republican party
Sentiment: SUPPORT (78.3% confidence)
```

### 2. Reddit Sentiment Analysis

```bash
# Analyze J.D. Vance sentiment from Reddit
python polibert_sentiment.py --candidate "J.D. Vance" --reddit --limit 50

# Analyze specific query
python polibert_sentiment.py --query "2028 election" --reddit --limit 100

# Custom subreddits
python polibert_sentiment.py --query "climate policy" --reddit --subreddits politics,environment
```

### 3. Batch File Analysis

```bash
# File with one text per line
python polibert_sentiment.py --candidate "Trump" --file tweets.txt
```

### 4. JSON Output (for integration)

```bash
python polibert_sentiment.py --candidate "Biden" --reddit --json
```

**Output**:
```json
{
  "candidate": "Biden",
  "total_analyzed": 47,
  "sentiment_breakdown": {
    "support": {"count": 15, "percentage": 31.9},
    "oppose": {"count": 22, "percentage": 46.8},
    "neutral": {"count": 10, "percentage": 21.3}
  },
  "net_sentiment": -14.9,
  "average_confidence": 72.4
}
```

## Integration with Other Skills

### With Polymarket

```
Polymarket (market odds)  →  PoliBERT (social sentiment)  →  Prediction synthesis
     18.6% (Vance)                    35% Support                      Combined signal
```

### With Prediction Skill

Use PoliBERT sentiment as an input factor in the BRACE forecasting framework:
- Base rate: Historical election patterns
- Sentiment: Social media trends (via PoliBERT)
- Market: Prediction market odds (via Polymarket)

### Example Workflow

```bash
# 1. Get market data
python polymarket.py search "presidential election winner 2028" --json

# 2. Get social sentiment
python polibert_sentiment.py --candidate "J.D. Vance" --reddit --limit 100 --json

# 3. Synthesize in prediction framework
# (Use prediction skill to combine signals)
```

## Output Format

### Human-Readable Output

```
📊 Sentiment Analysis: J.D. Vance
Source: Reddit | Total analyzed: 47

Support: 31.9% (15)
Oppose: 46.8% (22)
Neutral: 21.3% (10)

Net Sentiment: -14.9%
Avg Confidence: 72.4%
```

### JSON Output Structure

```json
{
  "candidate": "string",
  "total_analyzed": "integer",
  "sentiment_breakdown": {
    "support": {"count": "integer", "percentage": "float"},
    "oppose": {"count": "integer", "percentage": "float"},
    "neutral": {"count": "integer", "percentage": "float"}
  },
  "average_confidence": "float",
  "net_sentiment": "float",
  "sample_results": [
    {"text": "string", "sentiment": "string", "confidence": "float"}
  ]
}
```

## Limitations and Considerations

### Model Limitations

1. **Training Data**: Model trained on 2016-2020 tweets, may not capture 2024-2028 linguistic patterns
2. **Context Sensitivity**: May miss sarcasm, irony, or cultural references
3. **Temporal Drift**: Political language evolves; model accuracy may degrade over time
4. **Confidence Calibration**: Confidence scores are model outputs, not calibrated probabilities

### Data Limitations

1. **Reddit Sample Bias**: Reddit users skew younger, more educated, more liberal than general population
2. **Selection Bias**: Active Reddit users are not representative voters
3. **Timing**: Social sentiment can shift rapidly; snapshot may not represent election day mood
4. **Volume**: Low-liquidity markets may have few social media discussions

### Best Practices

- Use as **one input among many**, not sole prediction basis
- Combine with prediction markets, polling data, economic indicators
- Track sentiment **trends over time**, not single snapshots
- Adjust for platform demographics (Reddit ≠ Twitter ≠ general population)

## Citation

If you use this skill or PoliBERTweet model in research, please cite:

```bibtex
@inproceedings{kawintiranon2022polibertweet,
  title={{P}oli{BERT}weet: A Pre-trained Language Model for Analyzing Political Content on {T}witter},
  author={Kawintiranon, Kornraphop and Singh, Lisa},
  booktitle={Proceedings of the Language Resources and Evaluation Conference (LREC)},
  year={2022},
  pages={7360--7367},
  publisher={European Language Resources Association}
}
```

## License

- **Skill Code**: MIT License
- **PoliBERTweet Model**: Subject to HuggingFace Hub and original paper terms

## Feedback and Contributions

- Report issues: Create GitHub issue
- Model questions: See [PoliBERTweet repository](https://github.com/GU-DataLab/PoliBERTweet)

## Related Skills

- `polymarket-unified` - Prediction market data for political forecasting
- `prediction` - BRACE framework for calibrated forecasting
- `ai-model-team` - Multi-model prediction system for financial markets

## Version History

- **v1.0.0** (2026-04-17): Initial release
  - PoliBERTweet model integration
  - Reddit data source support
  - Sentiment analysis pipeline
  - JSON and human-readable output formats
  - Batch processing capabilities
