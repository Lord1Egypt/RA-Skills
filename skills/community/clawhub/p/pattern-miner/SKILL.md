# Pattern Miner

Discover patterns in your own data files with local analysis.

## Overview

Pattern Miner helps you identify recurring patterns, associations, and anomalies in your own data files. All processing happens locally on your machine.

## Features

- **Pattern Recognition**: Identify recurring themes in your data
- **Association Discovery**: Find items that frequently occur together
- **Anomaly Detection**: Spot unusual patterns that deviate from norms
- **Local Processing**: All analysis runs on your device, no data upload

## When to Use

- Analyzing your own structured data files (CSV, JSON)
- Finding patterns in task lists or notes
- Identifying trends in personal datasets
- Discovering associations in your own records

## Usage

### Basic Analysis

```bash
# Analyze a JSON file
python3 scripts/analyze.py ~/data/my-tasks.json
```

### Requirements

```bash
pip install numpy scikit-learn pandas
```

## Scripts

- `scripts/analyze.py` - Analyze JSON files for patterns

### Configuration

Create a config file at `~/.pattern-miner/config.json`:

```json
{
  "minConfidence": 0.6,
  "minFrequency": 3,
  "analysisTypes": ["cluster", "association"]
}
```

## Input Formats

Supported file formats:
- JSON (array of objects)
- CSV (with headers)
- JSONL (one JSON object per line)

## Output

Analysis results include:
- Discovered patterns with confidence scores
- Association rules with support metrics
- Anomaly flags for unusual items
- Exportable reports (JSON, CSV)

## Privacy & Security

✅ **Your data stays on your device**
- No external API calls
- No data uploaded to cloud services
- No access to system files or shell history
- Only reads files you explicitly specify

## Technical Information

| Attribute | Value |
|-----------|-------|
| **Skill ID** | pattern-miner |
| **Version** | 2.0.1 |
| **Author** | harrylabsj |
| **License** | MIT-0 |

## Requirements

- Python 3.8+
- numpy, scikit-learn, pandas (for analysis)

## Limitations

- Only analyzes files you explicitly provide
- Does not access system logs or shell history
- Does not read OpenClaw session data
- Requires structured data files (JSON/CSV)
