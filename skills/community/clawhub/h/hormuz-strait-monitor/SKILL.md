---
name: hormuz-strait-monitor
description: "Track shipping transit data through the Strait of Hormuz. Monitors transits, daily throughput, and non-Iranian vessel counts from hormuzstraitmonitor.com and shipxy.com. Alerts when traffic recovery thresholds are met including vessel count recovery, throughput percentage recovery, and non-Iranian vessel exit counts. Use for monitoring Middle East shipping disruption and oil flow recovery."
---

# Hormuz Strait Transit Monitor

Track shipping transit data through the Strait of Hormuz - a critical chokepoint for global oil supply.

## Quick Start

```bash
# Run the monitor
python ~/.openclaw/workspace/skills/hormuz-strait-monitor/scripts/hormuz_monitor.py

# With notification channel
python ~/.openclaw/workspace/skills/hormuz-strait-monitor/scripts/hormuz_monitor.py --channel wecom

# Debug mode (keep browser visible)
python ~/.openclaw/workspace/skills/hormuz-strait-monitor/scripts/hormuz_monitor.py --debug
```

## Data Collected

| Source | Field | Format | Example |
|--------|-------|--------|---------|
| **hormuzstraitmonitor.com** | Transits (24h) | Number of ships | 6 ships |
| | Day Normal | Daily average | 60/day |
| | Daily Throughput | DWT (Deadweight Tonnage) | 500K DWT |
| | Avg Throughput | Average DWT | 10.3M |
| **shipxy.com** | Non-Iranian Vessels | Count from vessel list | 4 vessels |

## Data Sources

| Source | URL | Data Collected |
|--------|-----|----------------|
| **hormuzstraitmonitor.com** | https://hormuzstraitmonitor.com/ | Transits (24h), Daily Throughput, Day Normal, Avg Throughput |
| **shipxy.com** | https://www.shipxy.com/special/hormuz | Non-Iranian vessels exiting strait in 12h |

Both sites require JavaScript rendering - static HTTP fetch will not work.

## Alert Conditions

Alert triggers when **any** condition is met:

| Condition | Threshold | Meaning |
|-----------|-----------|---------|
| **Transits Recovery** | >= 10 vessels | Absolute recovery threshold |
| **Transits Recovery** | >= 20% of day normal | Relative recovery threshold |
| **Throughput Recovery** | >= 20% of avg | Oil flow returning |
| **Non-Iranian Vessels** | >= 10 exiting in 12h | Western/Asian shipping activity |

## Output

Data is appended to CSV: `~/.openclaw/workspace/memory/hormuz-transit-data.csv`

Columns:
- `timestamp` - Collection time
- `transits_24h` - Vessels transited in last 24h
- `daily_throughput` - Current daily oil flow
- `day_normal` - Normal daily transit count
- `avg_throughput` - Average daily throughput
- `non_iranian_vessels` - Non-Iranian vessels exiting in 12h
- `alerts` - Alert messages (if any)

## Configuration

See `references/config.json` for threshold customization.

To enable notifications:
1. Edit `references/config.json`
2. Set `"channel": "wecom"` or other supported channel
3. Or use `--channel` flag at runtime

## Environment Requirements

**Required:**
- Google Chrome (installed at `/usr/bin/google-chrome`)
- Python 3.x
- selenium + webdriver-manager

**Install dependencies:**
```bash
pip install selenium webdriver-manager
```

**Chrome version:** This skill uses Chrome 147+ (headless mode).

## Workflow

1. **Fetch hormuzstraitmonitor.com**
   - Launch headless Chrome
   - Wait for JavaScript rendering (~10s)
   - Parse Transits (24h), Daily Throughput, Day Normal, Avg
   - Use regex patterns for data extraction

2. **Fetch shipxy.com**
   - Navigate to Chinese shipping portal
   - Wait for rendering (~15s)
   - Parse Non-Iranian vessel count (Chinese text patterns)

3. **Record Data**
   - Append to CSV file
   - Include timestamp and all collected values

4. **Check Alerts**
   - Compare current vs previous data
   - Evaluate threshold conditions
   - Generate alert messages

5. **Notify (if configured)**
   - If alerts triggered OR channel configured
   - Send summary via specified channel

## Troubleshooting

**Chrome not found:**
```
ERROR: Chrome binary not found at /usr/bin/google-chrome
```
Solution: Install Google Chrome or update binary path in script.

**Selenium not installed:**
```
ERROR: selenium and webdriver-manager not installed
```
Solution: `pip install selenium webdriver-manager`

**Data not parsed:**
- Check debug screenshots: `~/.openclaw/workspace/memory/hormuzstraitmonitor_debug.png`
- Run with `--debug` to see browser content
- Website structure may have changed - update regex patterns

**Timeout errors:**
- Increase wait time in script (JavaScript-heavy pages)
- Check network connectivity to both sites

## Cron Integration

To monitor regularly, add to heartbeat or cron:

**Heartbeat (HEARTBEAT.md):**
```markdown
- Check Hormuz Strait transit data (every 4h)
```

**Cron job:**
```bash
# Every 4 hours
openclaw cron add --schedule "0 */4 * * *" --name hormuz-monitor \
  --payload '{"kind": "agentTurn", "message": "Run Hormuz Strait monitor skill"}'
```

## Notes

- The Strait of Hormuz handles ~20% of global oil consumption
- During Iran-West tensions, transits may drop significantly
- Recovery signals indicate de-escalation or alternative routing
- Non-Iranian vessel count is key indicator of Western/Asian shipping confidence