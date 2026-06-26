---
name: lorem-gen
description: Generate placeholder text for design mockups, development, and testing. Supports classic Lorem Ipsum, hipster-style, and tech jargon. Output as plain text, HTML, Markdown, or JSON. Use when creating dummy content, filler text, placeholder paragraphs, or sample text for layouts and prototypes.
---

# Lorem Gen

Generate placeholder text via CLI. Supports multiple styles and output formats.

## Quick Start

```bash
# 3 paragraphs of classic Lorem Ipsum
python3 scripts/lorem_gen.py

# 5 sentences
python3 scripts/lorem_gen.py -n 5 -u sentences

# 50 words of hipster-style text
python3 scripts/lorem_gen.py -n 50 -u words -s hipster

# Tech jargon as HTML
python3 scripts/lorem_gen.py -s tech -f html

# JSON output with reproducible seed
python3 scripts/lorem_gen.py -n 2 -f json --seed 42
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-n, --count` | Number of units | 3 |
| `-u, --unit` | `paragraphs`, `sentences`, or `words` | paragraphs |
| `-s, --style` | `lorem`, `hipster`, or `tech` | lorem |
| `-f, --format` | `plain`, `html`, `markdown`, `json` | plain |
| `--no-classic` | Skip "Lorem ipsum dolor sit amet..." opening | off |
| `--seed` | Random seed for reproducible output | none |

## Styles

- **lorem** — Classic Latin placeholder text
- **hipster** — Artisan / wellness / lifestyle vocabulary
- **tech** — DevOps, cloud, and infrastructure jargon

## Notes

- No external dependencies (Python 3 stdlib only)
- First paragraph starts with the classic opening by default (use `--no-classic` to disable)
- Use `--seed` for deterministic output across runs
