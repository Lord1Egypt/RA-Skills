# Search Topics Configuration

These are the 6 default Tavily search queries executed each run. Edit to add/remove/translate topics.

## Default Queries

| # | Topic | Query | Notes |
|---|---|---|---|
| 1 | A股行情 | `A股 今日行情 最新` | Core — always run |
| 2 | 港股/恒指 | `港股 恒生指数 今日` | Core — always run |
| 3 | 特朗普动态 | `特朗普 最新动态` | High impact on markets |
| 4 | 军事/地缘政治 | `中国军事 地缘政治 最新` | Risk factor |
| 5 | 美股 | `美股 道指 纳指 标普 最新` | Overnight context |
| 6 | 中国经济政策 | `中国经济政策 最新` | Policy catalyst |

All queries use `time_range=day` for recency.

## Web Fetch Supplements

Run after Tavily for real-time tick data:
- `https://www.cls.cn/telegraph` — 财联社电报（breaking news）
- `https://www.jin10.com/` — 金十数据（macro data releases）

## Adding Topics

Add a row and a corresponding `mcporter call` in Step 3 of SKILL.md:

```bash
mcporter call tavily-remote-mcp.tavily_search query="YOUR QUERY HERE" time_range=day
```

## Removing Topics

Delete or comment the row. Skip the corresponding search in Step 3.
