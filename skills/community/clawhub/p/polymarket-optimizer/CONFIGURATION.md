# Configuration Guide — Polymarket Optimizer v1.0.0

---

## Prerequisites

- `polymarket-executor` must be running (provides input files)
- Python 3.7+
- Telegram bot (optional — already configured in Wesley)

---

## Step 1: Environment Variables

The optimizer uses the same `.env` as the executor. No additional variables needed.

```bash
# Already in Wesley's .env:
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=1584210176
WORKSPACE=/data/.openclaw/workspace
```

---

## Step 2: Install in Wesley Workspace

```bash
# On VPS as root
docker exec openclaw-yyvg-openclaw-1 bash -c "
mkdir -p /data/.openclaw/workspace/skills/polymarket-optimizer
"

docker cp polymarket_optimizer.py openclaw-yyvg-openclaw-1:/data/.openclaw/workspace/skills/polymarket-optimizer/
docker cp SKILL.md openclaw-yyvg-openclaw-1:/data/.openclaw/workspace/skills/polymarket-optimizer/
```

---

## Step 3: Test Run

```bash
docker exec openclaw-yyvg-openclaw-1 bash -c "
cd /data/.openclaw/workspace/skills/polymarket-optimizer
python3 polymarket_optimizer.py
"
```

If no executor data exists yet, optimizer will report "insufficient data" and exit cleanly. This is normal — run the executor first.

---

## Step 4: Configure Cron Job

Add to OpenClaw's cron configuration:

```
# Polymarket optimizer — every 6 hours
0 */6 * * * docker exec openclaw-yyvg-openclaw-1 python3 /data/.openclaw/workspace/skills/polymarket-optimizer/polymarket_optimizer.py >> /data/.openclaw/workspace/optimizer_cron.log 2>&1
```

---

## Optimizer Parameters (Advanced)

These are hardcoded in `polymarket_optimizer.py` but can be adjusted if needed:

| Parameter | Default | Description |
|---|---|---|
| `WIN_RATE_FLOOR` | 50% | Below this → tighten thresholds |
| `WIN_RATE_TARGET` | 65% | Above this → no change needed |
| `WIN_RATE_EXCELLENT` | 80% | Above this → loosen thresholds |
| `MIN_TRADES_TO_OPTIMIZE` | 5 | Minimum trades before optimizer acts |
| `MAX_THRESHOLD_STEP` | 0.5% | Max threshold change per cycle |
| `MAX_KELLY_STEP` | 5% | Max Kelly fraction change per cycle |
| `MAX_ALLOCATION_STEP` | 10% | Max allocation change per cycle |

Small steps prevent overcorrection — the optimizer is conservative by design.

---

## Monitoring

```bash
# View optimization history
docker exec openclaw-yyvg-openclaw-1 bash -c "
tail -5 /data/.openclaw/workspace/optimizer_log.jsonl | python3 -m json.tool
"

# View current config (what executor will use next run)
docker exec openclaw-yyvg-openclaw-1 bash -c "
cat /data/.openclaw/workspace/learned_config.json | python3 -m json.tool
"

# Count optimization runs
docker exec openclaw-yyvg-openclaw-1 bash -c "
wc -l /data/.openclaw/workspace/optimizer_log.jsonl
"
```

---

## Troubleshooting

**"No metrics file — building from paper trades"**
→ Normal on first run after executor. Optimizer builds metrics from `paper_trades.json`.

**"No paper trades yet"**
→ Executor hasn't traded yet. Let it run for a few scan cycles first.

**"No adjustments needed — config is optimal"**
→ Good! Strategies are performing well within acceptable ranges.

**Telegram not sending**
→ Check `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`.

---

**Version:** 1.0.0 | **Author:** Georges Andronescu (Wesley Armando)
