# Setup (first use)

This skill ships with mock adapters by default for safe local use.

## 1) Runtime

- Python 3 installed (`python3 --version`)

## 2) Input data

- Start with `examples/products.india.csv`
- Ensure products are normalized by exact variant (model, storage, color, condition)

## 3) Mode selection

- Start in `mock` mode only for local evaluation
- Move to `live` only after:
  - store policy review
  - rate-limit strategy
  - legal/compliance sign-off

## 4) Output handling

- Treat all outputs as **decision support**, not guaranteed truth
- Manually verify high-value opportunities before purchase decisions

## 5) Safety notes

- Do not hardcode API keys in code if adding live adapters
- Do not run aggressive scraping loops
- Respect robots, terms of use, and regional legal restrictions

