---
name: mx-xuangu
description: Use this skill for Eastmoney MX condition-based stock screening and universe lookup when the user asks to find stocks, listed companies, sector constituents, index constituents, or recommendations based on market/valuation/financial/industry constraints such as PE, ROE, price, growth, volume, industry, board, or concept. Do not use for single-security quote or financial data (use mx-data), news/event research (use mx-search), watchlist actions (use mx-zixuan), or simulated trading operations (use mx-moni).
---

# mx-xuangu

Use `mx_xuangu.py` to convert natural-language screening conditions into Eastmoney MX stock-screening queries and CSV outputs.

## Trigger Boundaries

- Use for "筛选/找出/选出/有哪些股票/成分股/板块内/行业内/满足条件" requests.
- Use for compound filters such as price, PE/PB, ROE, revenue/profit growth, market cap, industry, board, concept, region, dividend, and recent performance.
- Use for constituent lookup of sectors, themes, and indexes.
- Do not use for exact data of one entity; use `mx-data`.
- Do not present screening output as personalized investment advice unless the user explicitly asks for analysis.

## Inputs

- Required: universe or condition. If the universe is missing, default to A-shares only when the user's wording implies China/A-share context; otherwise ask.
- Clarify ambiguous constraints that change the result, such as "低估值", "近期", or "龙头".
- Require `MX_APIKEY`. Optional: set `MX_OUTPUT_DIR`; otherwise output goes to `~/.codex/skills-output/mx_data/output`.

## Workflow

1. Convert the request into one concise natural-language screening query.
2. Keep the query specific: universe + filters + ordering/limit if requested.
3. Run:

```bash
python /Users/lu/.codex/skills/mx-xuangu/mx_xuangu.py --query "市盈率小于20且ROE大于15%的银行股"
```

4. Inspect row count, CSV path, and description file.
5. If raw field interpretation matters, read `references/result-fields.md`.
6. Report the matching count, key filters, top rows, and generated file paths.

## Output Contract

- Show the parsed screening condition and final match count.
- Include a compact table of representative results when the list is long.
- State that results are data-screening candidates, not buy/sell advice.
- Mention if a condition appears too strict or returned zero rows.

## Failure Handling

- Zero rows: suggest relaxing one or two specific constraints.
- Parser failure: rewrite the query with explicit operators and units.
- Too many rows: add ranking, top N, sector, market, or date constraints.
- API/auth/rate-limit errors: report the code and stop.

## Validation

- Use `evals/evals.json` to check that screening prompts trigger this skill and single-security data/news prompts route elsewhere.
