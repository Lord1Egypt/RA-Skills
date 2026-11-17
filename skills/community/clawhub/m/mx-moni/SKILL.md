---
name: mx-moni
description: Use this skill for Eastmoney MX simulated stock portfolio operations when the user explicitly asks to query mock trading holdings, account balance, orders, historical fills, buy/sell in a simulated account, cancel mock orders, or publish simulated trading experience posts. This skill is only for simulated A-share trading practice and must not be used for real-money trading, investment advice, watchlist actions, stock screening, news research, or quote-only data.
---

# mx-moni

Use `mx_moni.py` for the user's Eastmoney MX simulated portfolio. Operations may mutate a simulated account, so keep routing strict.

## Trigger Boundaries

- Use for simulated portfolio: holdings, funds, orders, historical fills, buy, sell, cancel, one-click cancel, and simulated trading post.
- Proceed with buy/sell/cancel only when the user explicitly states the simulated-trading action and provides required details.
- Do not use for real brokerage trading or real-money instructions.
- Do not use for watchlist operations (`mx-zixuan`), screening candidates (`mx-xuangu`), latest data (`mx-data`), or news/event analysis (`mx-search`).

## Inputs

- Required environment: `MX_APIKEY`.
- Optional environment: `MX_API_URL` defaults to `https://mkapi2.dfcfs.com/finskillshub`; `MX_OUTPUT_DIR` defaults to `~/.codex/skills-output/mx_data/output`.
- Query/holdings/balance/orders: natural-language instruction is enough.
- Buy/sell: stock code, quantity, and either price or market-price wording.
- Cancel: order id or explicit "撤销所有/一键撤单".
- New post: explicit request plus post text; the script prompts for text interactively.

## Workflow

1. Confirm the request is for the simulated portfolio, not real trading.
2. Identify intent: positions, balance, orders, buy, sell, cancel, or newPost.
3. For mutating operations, ensure required inputs are present. Ask before guessing price, quantity, order id, or stock.
4. Run:

```bash
python /Users/lu/.codex/skills/mx-moni/mx_moni.py "我的持仓"
python /Users/lu/.codex/skills/mx-moni/mx_moni.py "市价买入 000001 100 股"
python /Users/lu/.codex/skills/mx-moni/mx_moni.py "撤销所有未成交委托"
```

5. Report the formatted result and generated JSON/TXT paths.
6. For endpoint and payload details, read `references/api.md`.

## Output Contract

- State that results are from a simulated account.
- For holdings/balance, summarize assets, available funds, positions, and P/L when returned.
- For orders/fills, summarize order status and key identifiers.
- For buy/sell/cancel, report API status and do not imply success if the response is missing or failed.

## Failure Handling

- Missing `MX_APIKEY`: stop and ask for configuration.
- No simulated portfolio bound: tell the user to create/bind one in the MX Skills page.
- Missing trade inputs: ask for exact stock code, quantity, and price/market choice.
- API rejection: surface the message and do not retry mutating operations automatically.
- Encoding for new posts: keep UTF-8 JSON and `Content-Type: application/json; charset=UTF-8`.

## Validation

- Use `evals/evals.json` after changing routing or the script.
- Positive tests must include query and mutation prompts; negative tests must include real-trading, watchlist, screening, and quote-only prompts.
