# Logfmt Parser

Converts messy log files from any format into clean, uniform JSON for easier analysis, debugging, and forwarding to log aggregators.

## Usage

```bash
# Convert a log file to JSON
logfmt_parser -i app.log -o structured.json

# Pipe logs through parser with timestamp extraction
cat server.log | logfmt_parser --timestamp | jq '.'

# Parse without keeping original log lines
logfmt_parser -i nginx.log --no-log-field > clean.json
```

## Price

$2.50
