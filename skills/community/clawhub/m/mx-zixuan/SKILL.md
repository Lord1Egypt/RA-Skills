---
name: mx-zixuan
description: Use this skill for Eastmoney MX self-selected stock watchlist management when the user explicitly asks to query, add, or delete stocks in their personal watchlist/self-select list, using phrases such as 我的自选, 查询自选, 加入自选, 添加到自选, 删除自选, or 从自选移除. Do not use for quote/financial data (use mx-data), news research (use mx-search), screening candidates (use mx-xuangu), or simulated trading (use mx-moni).
---

# mx-zixuan

Use `mx_zixuan.py` to query or mutate the user's Eastmoney self-selected stock list.

## Trigger Boundaries

- Use only for watchlist/self-select operations: query list, add stock, delete stock.
- Treat add/delete as account-mutating actions. Proceed when the user explicitly names the action and stock; ask once when the stock or action is ambiguous.
- Do not use this skill to recommend what should be added unless the user separately asks for screening/analysis.
- Do not use for simulated portfolio holdings; use `mx-moni`.

## Inputs

- Query: no stock required.
- Add/delete: stock name or 6-digit code required. Prefer code when the name may map to multiple securities.
- Require `MX_APIKEY`. Optional: set `MX_OUTPUT_DIR`; otherwise output goes to `~/.codex/skills-output/mx_data/output`.

## Workflow

1. Classify the action: `query`, `add`, or `delete`.
2. For add/delete, verify that the user's instruction is explicit enough to mutate the watchlist.
3. Run one of:

```bash
python /Users/lu/.codex/skills/mx-zixuan/mx_zixuan.py query
python /Users/lu/.codex/skills/mx-zixuan/mx_zixuan.py add "贵州茅台"
python /Users/lu/.codex/skills/mx-zixuan/mx_zixuan.py delete "贵州茅台"
python /Users/lu/.codex/skills/mx-zixuan/mx_zixuan.py "把比亚迪加入自选"
```

4. Report the operation result and generated CSV/JSON path if any.
5. For output field interpretation, read `references/result-fields.md`.

## Output Contract

- Query: summarize total count and show key fields such as code, name, latest price, change, turnover, and volume ratio when returned.
- Add/delete: state whether the operation succeeded and echo the stock/action.
- Do not claim the list changed unless the API response indicates success.

## Failure Handling

- Missing `MX_APIKEY`: stop and ask for configuration.
- Ambiguous stock: ask for code or full name.
- Already exists / not in list: report the API message and suggest querying the list.
- Empty list: say it is empty and mention add flow.
- API/network errors: report the error and do not retry mutating operations automatically.

## Validation

- Use `evals/evals.json` after changing routing, especially to ensure ordinary quote and screening prompts do not trigger watchlist mutation.
