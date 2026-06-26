# Gumroad Product Page Generator

Generate high-converting Gumroad product page copy from structured JSON specifications.

## Description

Gumroad Product Page Generator transforms product specifications (features, benefits, pricing, testimonials) into ready-to-publish Gumroad sales page markdown. It includes automatic legal disclaimer injection based on product category (financial, health, general), template-driven copywriting, and compliance-ready output. Designed to accelerate product launch workflows while maintaining legal safety.

## Key Features

- **JSON to markdown conversion** - Transform structured product data into sales page copy
- **Auto disclaimer injection** - Detects product category and adds appropriate legal disclaimers
- **Multiple input modes** - File, inline JSON, or stdin piping
- **Disclaimer type detection** - Financial, investment, health, or general category auto-detection
- **Template library** - Shared disclaimer templates for consistency across products
- **Compliance-ready** - Includes "not financial advice" disclaimers for investment products
- **No manual copy-paste** - Programmatic generation for rapid iteration

## Quick Start

```bash
# Generate page from product JSON file
python3 scripts/generate-page.py product.json --output page.md

# Auto-detect financial disclaimer (recommended)
python3 scripts/generate-page.py product.json

# Force specific disclaimer type
python3 scripts/generate-page.py product.json --disclaimer-type financial

# Skip disclaimer (draft only)
python3 scripts/generate-page.py product.json --no-disclaimer

# Inline JSON
python3 scripts/generate-page.py --json '{"product_name": "Tax Optimizer", "price": 49, ...}'

# Stdin piping
cat product.json | python3 scripts/generate-page.py
```

**Product JSON structure:**
```json
{
  "product_name": "AI Tax Optimizer",
  "price": "$49",
  "tagline": "Maximize deductions using AI",
  "features": ["Feature 1", "Feature 2"],
  "benefits": ["Benefit 1", "Benefit 2"],
  "testimonials": [{"author": "Jane Doe", "quote": "Amazing!"}],
  "category": "financial"
}
```

## Disclaimer Types

- **Financial** - "Not financial, investment, or tax advice. Consult a CPA before decisions."
- **Investment** - Stricter version for investment products
- **Health** - "Not medical advice. Consult a healthcare professional."
- **General** - "Results may vary. Individual results not guaranteed."
- **Auto** (default) - Detects category from product keywords

## What It Does NOT Do

- Does NOT write product features or benefits from scratch (requires structured input)
- Does NOT guarantee regulatory compliance (legal review recommended)
- Does NOT handle design/styling (markdown output only)
- Does NOT upload to Gumroad (manual paste required)
- Does NOT generate product images or graphics

## Requirements

- Python 3.8+
- No external dependencies (standard library only)
- Disclaimer templates file (data/disclaimer-templates.json)

## License

MIT
