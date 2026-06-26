---
id: 'gumroad-page-gen'
name: 'Gumroad Page Generator'
description: 'Generates Gumroad product page content from a simple spec.'
version: '1.0.0'
author: 'DaVinci'
last_amended_at: null
trigger_patterns: []
pre_conditions:
  git_repo_required: false
  tools_available: []
expected_output_format: 'natural_language'
---

# Gumroad Page Generator

Generates Gumroad product page content from a simple spec.

## Usage

```bash
gumroad-page-gen create \
  --product-name "AI Tax Optimizer" \
  --target-audience "Software Engineers with RSUs" \
  --pain-points "AMT, tax drag, complex tax code" \
  --solution "Optimize your RSU tax strategy with AI." \
  --features "AMT calculator, harvest planner, state tax analysis" \
  --price 49
```
