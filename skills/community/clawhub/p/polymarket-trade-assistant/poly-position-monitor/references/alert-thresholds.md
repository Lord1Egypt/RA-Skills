# Alert Thresholds Guide

## Price Change Thresholds

All price changes are **relative** (not absolute percentage points).

Formula: `change = (current_price / price_N_min_ago) - 1`

Example: price from 0.50 to 0.515 = +3% relative change.

### Default Thresholds

| Window | Threshold | Alert Level | Rationale |
|--------|-----------|-------------|-----------|
| 5 min  | 3%  | WARNING  | Short-term flash move, may revert |
| 15 min | 15% | WARNING  | Significant momentum shift |
| 60 min | 10% | ALERT    | Sustained directional move |
| 240 min| 20% | CRITICAL | Major repricing event |

### Tuning Guidelines

**More sensitive** (active trader, small markets):
```json
{"5m": 0.02, "15m": 0.05, "60m": 0.07, "240m": 0.15}
```

**Less sensitive** (long-term holder, high-volume markets):
```json
{"5m": 0.05, "15m": 0.20, "60m": 0.15, "240m": 0.30}
```

Prediction markets with low prices (< $0.10) naturally have higher % swings. Consider per-market overrides if needed.

## Volume Thresholds

| Parameter | Default | Description |
|-----------|---------|-------------|
| `volume_spike_ratio` | 2.0 | Alert if current interval volume > 2x rolling average |
| `volume_drop_ratio` | 0.3 | Alert if current interval volume < 30% of rolling average |

Volume comparison uses the previous cycle's `interval_volume_usd` as the baseline. After several cycles, this acts as a rolling comparison.

## Position Change Thresholds

| Parameter | Default | Description |
|-----------|---------|-------------|
| `position_change_pct` | 0.20 | Alert if position size changes by > 20% |
| `min_inflow_usd` | 1000 | Alert on new positions worth > $1,000 |

## Alert Levels

| Level | Color | Telegram | Email | Use Case |
|-------|-------|----------|-------|----------|
| INFO | Dim/gray | No (default) | No | Status updates, minor changes |
| WARNING | Yellow | Yes | No (default) | Moderate anomalies, early signals |
| ALERT | Magenta | Yes | Yes | Significant events requiring attention |
| CRITICAL | Red+Bold | Yes | Yes | Major events, possible resolution impact |

Notification `min_level` is configurable per channel in config.json.
