---
name: jsonpretty
description: Format, validate, query, flatten, and analyze JSON data. Use when asked to pretty-print JSON, validate JSON syntax, query nested JSON with dot-notation, flatten nested structures, get JSON statistics, or compact JSON output. Reads from files or stdin pipe. Zero dependencies — pure Python.
---

# jsonpretty 📋

JSON swiss army knife — format, validate, query, flatten, stats.

## Commands

```bash
# Pretty-print (from file or stdin)
python3 scripts/jsonpretty.py data.json
echo '{"a":1}' | python3 scripts/jsonpretty.py

# Validate JSON
python3 scripts/jsonpretty.py --validate data.json

# Query with dot-notation
echo '{"user":{"name":"Rogue"}}' | python3 scripts/jsonpretty.py -q "user.name"

# Flatten nested JSON
cat data.json | python3 scripts/jsonpretty.py --flat

# Structure stats (key count, depth, types, size)
python3 scripts/jsonpretty.py --stats data.json

# Compact output (minify)
python3 scripts/jsonpretty.py --compact data.json

# Sort keys
python3 scripts/jsonpretty.py --sort data.json
```

## Features
- Pretty-print with 2-space indent (default)
- JSON validation with error messages
- Dot-notation querying (supports array indices: `key[0].sub`)
- Flatten nested objects to `key.subkey = value` pairs
- Structure statistics: key count, nesting depth, type distribution, byte size
- Compact/minify mode
- Sorted key output
- Reads from file or stdin
