# Output Templates

## 1. Trackable Market — Initial Snapshot Report

```markdown
# Resolution Tracking Report

**Market:** {event_title}
**Link:** {market_url}
**Generated:** {YYYY-MM-DD HH:MM:SS} UTC
**Resolution Date:** {end_date}
**Time Remaining:** {hours}h

## Resolution Source

| Field | Value |
|-------|-------|
| Source URL | {resolution_url} |
| Metric | {metric_name} |
| Trackability | {Full/Partial/Manual} |
| Data Method | {html_table/embedded_json/api} |

## Current State

### Resolution Data

| Rank | Candidate | Score | CI | Model/Entry |
|------|-----------|-------|----|-------------|
| {rank} | {candidate} | {score} | ±{ci} | {model_name} |
| ... | ... | ... | ... | ... |

### Market Prices

| Candidate | Market Price | Resolution Data Rank |
|-----------|-------------|---------------------|
| {candidate} | {price}% | #{rank} |
| ... | ... | ... |

## Alignment Analysis

**Data Leader:** {leader} (Score: {score})
**Market Leader:** {market_leader} ({price}%)
**Status:** {ALIGNED / MISALIGNED}

## Risk Assessment

| Factor | Assessment |
|--------|-----------|
| Leader Gap | {gap} points |
| CI Overlap | {Yes/No} (leader CI: ±{ci1}, second CI: ±{ci2}) |
| Time to Resolution | {hours}h |
| Market Conviction | {leader_price}% (high/moderate/low certainty) |

## Monitoring Configuration

| Setting | Value |
|---------|-------|
| Check Interval | {interval} min |
| State Directory | {state_dir} |
| Alert Log | {alert_log_path or "Console only"} |
```

## 2. Non-Trackable Market Report

```markdown
# Resolution Tracking Report — Not Trackable

**Market:** {event_title}
**Link:** {market_url}
**Generated:** {YYYY-MM-DD HH:MM:SS} UTC

## Assessment

**Trackability Level:** {Manual/None}

### Reasons

{Numbered list of specific reasons why this market cannot be automatically tracked}

1. {reason_1}
2. {reason_2}

### Resolution Criteria (from description)

> {quoted relevant portion of market description}

## Recommendations

{If Manual:}
- Check {source_url} manually on the following schedule:
  - {schedule based on time to resolution}
- Key data points to look for: {what to check}

{If None:}
- This market has subjective resolution criteria and cannot be reliably tracked.
- Consider monitoring market price movements instead as a proxy.
```

## 3. Monitoring Alert Formats

### Terminal Output Format

```
══════════════════════════════════════════════════════
[{YYYY-MM-DD HH:MM} UTC] Resolution Tracker Started
Market: {event_title}
Source: {resolution_url}
Resolution: {end_date} ({hours}h remaining)
──────────────────────────────────────────────────────
[HH:MM] #{rank} {leader} {score}±{ci} | #{rank} {second} {score}±{ci} | Gap: {gap}
        Market: {leader} {price}% | {second} {price}% | ...
        Status: ALIGNED ✓
──────────────────────────────────────────────────────
[HH:MM] No change. Next check in {interval}min.
[HH:MM] WARNING: {org} score changed {old}→{new}, gap narrowed to {gap}
[HH:MM] CRITICAL: Leader changed! {new_leader} {score} > {old_leader} {score}
══════════════════════════════════════════════════════
```

### Alert Severity Levels

| Level | Color | Trigger Conditions |
|-------|-------|--------------------|
| **CRITICAL** | Red, bold | Leader changed; resolution outcome would flip |
| **WARNING** | Yellow | Gap narrowed; CI overlap; significant score change |
| **ALERT** | Magenta, bold | Market price vs resolution data misalignment |
| **INFO** | Dim/gray | No change; minor updates; status reports |

### JSON Alert Format (for log files)

```json
{
  "type": "CRITICAL",
  "message": "Leader changed! Google 1504 > Anthropic 1502",
  "data": {
    "new_leader": "Google",
    "old_leader": "Anthropic",
    "new_score": 1504,
    "old_score": 1502
  },
  "timestamp": "2026-02-24T12:00:00+00:00"
}
```

## 4. Monitoring Interval Guidelines

| Time to Resolution | Recommended Interval |
|---|---|
| > 7 days | 360 min (6h) |
| 2-7 days | 120 min (2h) |
| 1-2 days | 60 min (1h) |
| < 24 hours | 30 min |
| < 6 hours | 15 min |
