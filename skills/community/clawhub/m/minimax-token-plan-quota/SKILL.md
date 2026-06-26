---
name: minimax-token-plan-quota
description: Check MiniMax Token Plan remaining quota, usage window reset time, and per-model remaining limits, especially for the China mainland Token Plan flow on minimaxi.com. Use when the user asks things like “MiniMax 还有多少额度”, “查一下 minimax 订阅剩余额度”, “看看 Token Plan 还剩多少”, or wants a compact quota table for MiniMax Token Plan.
---

# MiniMax Token Plan Quota

Use this skill to query **MiniMax Token Plan remaining quota**.

## Default behavior

- Default to the **China mainland** endpoint on `www.minimaxi.com`
- Return a compact **table** with:
  - 项目
  - 周期
  - 总额度
  - 剩余额度
  - 重置剩余时间

## Important rule

Interpret the `/coding_plan/remains` response as **remaining quota**, not consumed quota.

The script maps:
- `current_interval_total_count` → 当前周期总额度
- `current_interval_usage_count` → 当前周期剩余额度
- `current_weekly_total_count` → 本周总额度
- `current_weekly_usage_count` → 本周剩余额度

Do not flip those meanings unless MiniMax docs change.

## Secret handling

- Prefer `MINIMAX_API_KEY` from env
- If env is absent, the bundled script will also try `~/.openclaw/.env`
- You may pass `--api-key` for one-off manual runs
- If the user pasted a key in the current conversation, use it transiently for the current task only
- Do **not** store MiniMax API keys in workspace memory, skill files, or long-term notes
- If `~/.openclaw/.env` is missing or lacks `MINIMAX_API_KEY`, guide the user to add:

```bash
mkdir -p ~/.openclaw
printf "MINIMAX_API_KEY=你的key\n" > ~/.openclaw/.env
```

## Commands

### China mainland Token Plan quota

```bash
MINIMAX_API_KEY='...' python3 scripts/check_token_plan_quota.py --region cn
```

Or rely on `~/.openclaw/.env`:

```bash
python3 scripts/check_token_plan_quota.py --region cn
```

### Global endpoint

```bash
MINIMAX_API_KEY='...' python3 scripts/check_token_plan_quota.py --region global
```

### JSON output

```bash
MINIMAX_API_KEY='...' python3 scripts/check_token_plan_quota.py --region cn --json
```

## Output style for user replies

Default to the markdown table only when the user asks for a concise result.

Example:

```markdown
| 项目 | 周期 | 总额度 | 剩余额度 | 重置剩余时间 |
|---|---|---:|---:|---|
| MiniMax-M* | 当前周期 | 1500 | 1500 | 4小时26分钟 |
```

If some models show total quota `0`, explain briefly only when needed:
- 当前套餐未开通
- 或该 key 不包含此能力

## Resource

### `scripts/check_token_plan_quota.py`

Queries the MiniMax Token Plan quota endpoint and prints either:
- a compact markdown table
- or normalized JSON
