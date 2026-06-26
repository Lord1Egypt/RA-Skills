# File formats

## Vacancy JSON

Preferred fields:
- source
- source_url
- company
- title
- stack
- seniority
- salary_min
- salary_max
- salary_currency
- gross_or_net
- location
- remote_mode
- employment_type
- summary
- fit_score
- fit_label
- fit_reasons
- red_flags
- status
- raw_text

## Vacancy JSONL

Use JSONL for batch workflows:
- one vacancy per line
- UTF-8
- no trailing commas

## Project markdown files

The current project parsers are intentionally lightweight.
They work best when the templates are kept simple:
- scalar values as `Key: value`
- list values as bullet items under a heading-like key
- avoid complex nested markdown
