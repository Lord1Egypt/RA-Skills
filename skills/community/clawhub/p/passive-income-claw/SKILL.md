---
name: passive-income-claw
version: 0.1.0
description: |
  Binance passive income AI assistant. Automatically scans Binance earn opportunities,
  pushes matching opportunities based on user preferences, and executes subscriptions
  within authorized limits. Use when user mentions "passive income", "earn", "yield",
  "scan opportunities", "buy earn product", "what opportunities suit me".
  After install, tell the user: "Run /passive-income to get started, or just say 'help me set up passive income'."
user-invocable: true
metadata: '{"openclaw":{"requires":{"env":["BINANCE_API_KEY","BINANCE_API_SECRET"]}}}'
---

# Passive Income Claw

## Tools

This skill includes TypeScript scripts in `{baseDir}/bin/` for all deterministic operations. **Always use these via `node {baseDir}/bin/<script>.ts` instead of doing arithmetic, file parsing, or API calls manually.**

| Script | Purpose |
|--------|---------|
| `bin/earn-api.ts` | Binance Earn API + **账户资产明细查询** (`balance` 命令) |
| `bin/margin-api.ts` | Binance Cross Margin API (借贷、还款、账户状态、利率) |
| `bin/profile.ts` | User profile read/write/daily-reset |
| `bin/auth-check.ts` | 5-step authorization validation |
| `bin/snapshot.ts` | Snapshot diff & update |
| `bin/log.ts` | Execution log append & query |

### Official Binance Skills (use for prices only)

| Skill | 用途 |
|-------|------|
| **Binance Spot** | 行情价格查询、币种换算（**不要用 Spot 查余额，它只返回总额**） |
| **Market Ranking** | 市场热度（扫描时参考） |
| **Trading Signals** | 买卖信号（扫描时参考） |
| **Token Details** | Token 基本信息、价格 |

**查账户资产明细 → `node {baseDir}/bin/earn-api.ts balance`**
**查价格/行情 → Binance Spot skill**
**不要用 Spot skill 查余额 — 它只返回 BTC 总额，没有资产明细。**

All scripts output JSON to stdout. Errors go to stderr with non-zero exit code. All timestamps use UTC.

## Routing

**First use** (`~/passive-income-claw/user-profile.md` does not exist):
→ Read `{baseDir}/setup.md`

**User triggers scan** ("scan", "what's available", "recommend", cron job):
→ Read `{baseDir}/scan.md` — full-path scan: direct earn + borrow-to-earn, all candidates scored and sorted

**User triggers execution** ("buy #1", "execute", "redeem"):
→ Read `{baseDir}/execute.md`

**User asks about borrow-to-earn details** ("how does borrowing work", "explain #4"):
→ Read `{baseDir}/path-analysis.md`

**User wants to update settings** ("change my limit", "switch to auto"):
→ `node {baseDir}/bin/profile.ts dump` → show current → collect changes → `profile.ts set`

**User asks execution history** ("what did you execute"):
→ `node {baseDir}/bin/log.ts recent 20`
→ If no entries: "No executions recorded yet."

**Before all write operations**: run `node {baseDir}/bin/auth-check.ts` first.
