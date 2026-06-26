---
name: csv-stats-analyzer
description: Analyzes any CSV file and returns row count, column names, and basic statistics for numeric columns.
user-invocable: true
metadata:
  emoji: 📊
  requires:
    bins: ["uv"]
---

## Usage

Invoke with: `/csv-stats-analyzer <path-to-csv-file>`

Example: `/csv-stats-analyzer ./sales.csv`

## Features

- Shows total rows and columns
- Lists all column names
- Calculates min, max, and average for every numeric column

## Rules

- The CSV must exist and be readable.
- Use the helper script at {baseDir}/analyzer.py
- Run it with: uv run --with pandas {baseDir}/analyzer.py [csv-path]
- Return the output in a clean, readable format with emojis.
- Never modify the original CSV file.
