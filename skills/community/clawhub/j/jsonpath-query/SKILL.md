---
name: jsonpath-query
description: Query JSON data using JSONPath expressions. Use when asked to extract, filter, search, or navigate JSON data. Supports recursive descent, wildcards, array slicing, filter expressions, and union selections. Triggers on "JSONPath", "JSON query", "extract from JSON", "JSON filter", "jq alternative", "json path", "query json".
---

# JSONPath Query Tool

Query JSON data using JSONPath expressions with recursive descent, wildcards, filters, and slicing.

## Query

```bash
# From file
python3 scripts/jsonpath.py query '$.store.book[0].title' -f data.json

# From stdin
cat data.json | python3 scripts/jsonpath.py query '$.store.book[*].author'

# Recursive descent (find all 'name' fields at any depth)
cat data.json | python3 scripts/jsonpath.py query '$..name'

# Array slicing
cat data.json | python3 scripts/jsonpath.py query '$.items[0:5]'

# Filter (price < 10)
cat data.json | python3 scripts/jsonpath.py query '$.store.book[?(@.price < 10)]'

# Wildcard
cat data.json | python3 scripts/jsonpath.py query '$.store.*'

# Count matches
cat data.json | python3 scripts/jsonpath.py query '$.users[*]' --count

# First match only
cat data.json | python3 scripts/jsonpath.py query '$.items[*].id' --first

# Exit 1 if no matches (CI-friendly)
cat data.json | python3 scripts/jsonpath.py query '$.missing' --exit-empty
```

## List Paths

```bash
# Show all available paths in JSON data
cat data.json | python3 scripts/jsonpath.py paths

# Limit depth
cat data.json | python3 scripts/jsonpath.py paths --depth 3
```

## Extract Multiple Values

```bash
# Named extractions
cat data.json | python3 scripts/jsonpath.py extract 'name=$.user.name' 'emails=$.user.emails[*]'
```

## Validate Expression

```bash
python3 scripts/jsonpath.py validate '$.store.book[?(@.price > 10)]'
```

## Output Formats

```bash
python3 scripts/jsonpath.py query '$.items[*]' -f data.json --format json    # default
python3 scripts/jsonpath.py query '$.items[*].id' -f data.json --format lines # one per line
python3 scripts/jsonpath.py query '$.items[*]' -f data.json --format csv      # CSV for objects
```

## JSONPath Syntax

| Expression | Description |
|-----------|-------------|
| `$` | Root object |
| `.key` | Child key |
| `[0]` | Array index |
| `[0:5]` | Array slice (start:end) |
| `[0:10:2]` | Array slice with step |
| `[*]` | All elements |
| `..key` | Recursive descent |
| `[?(@.price<10)]` | Filter expression |
| `['key']` | Bracket notation |
| `[0,1,2]` | Union (multiple indices) |
