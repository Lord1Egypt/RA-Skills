---
name: pollen-forecast
description: Daily pollen forecast and allergy alerts for Chinese cities. Use when user asks about pollen levels, allergy season, hay fever, flower pollen, 花粉, 过敏, or wants to set up daily pollen alerts. Supports Beijing, Shanghai, Guangzhou, and other major Chinese cities. Can create automated daily cron reports.
---

# Pollen Forecast 花粉播报

Deliver daily pollen forecasts and allergy alerts for Chinese cities using web search.

## Quick Start

When user asks about pollen:

1. Search for current pollen data using `web_search`
2. Format into a concise daily report
3. Optionally set up daily cron job for automated alerts

## Search Queries

Use these search patterns for best results:

```
{城市}今日花粉浓度预报
{城市}未来三天花粉预测
{城市}花粉过敏季 {月份}
```

## Report Format

Structure the daily report as:

```
🌸 {城市}花粉日报 — {日期}

📊 今日花粉等级：{等级}（{数值}）
🌲 主要花粉种类：{种类列表}
📈 未来3天趋势：{趋势}
🛡️ 出行建议：{建议}
```

### Pollen Level Scale (China Standard)

| Level | Description | Action |
|-------|------------|--------|
| 1级 | 低 | 一般人群无需防护 |
| 2级 | 较低 | 重度过敏者注意 |
| 3级 | 偏高 | 过敏者戴口罩 |
| 4级 | 较高 | N95 + 护目镜 |
| 5级 | 很高 | 尽量室内活动 |

### Key Pollen Calendar (Beijing)

| Tree | Start | Peak | End | Allergenicity |
|------|-------|------|-----|---------------|
| 柏科 (Cypress) | Mar 9 | Mar 30 | Apr 25 | ⚠️ Very High |
| 杨柳科 (Poplar/Willow) | Mar 9 | Mar 26 | Apr 20 | ⚠️ High |
| 榆科 (Elm) | Mar 1 | Mid-Mar | Apr | Medium |
| 松科 (Pine) | Mar 15 | May 11 | Jun 19 | Low |
| 桦木 (Birch) | Apr | Mid-Apr | May | High |

### Protection Mnemonic: 躲戴洗备

| Char | Action |
|------|--------|
| 躲 | Stay indoors during peak hours (10:00-17:00) |
| 戴 | Wear N95 mask + pollen-proof goggles outdoors |
| 洗 | Wash face, rinse nose with saline upon return |
| 备 | Keep nasal spray + antihistamines ready |

## Setting Up Daily Alerts (Cron)

To create automated daily pollen alerts, use `openclaw cron add`:

```bash
openclaw cron add \
  --name "每日花粉播报" \
  --cron "30 8 * * *" \
  --tz "Asia/Shanghai" \
  --exact \
  --session isolated \
  --wake now \
  --announce \
  --channel {channel} \
  --to "{user_target}" \
  --model "openrouter/google/gemini-2.5-flash" \
  --timeout-seconds 120 \
  --message "Search for today's pollen forecast for {city} and deliver a concise daily report following the pollen-forecast skill format."
```

Adjust `--cron`, `--tz`, `--channel`, `--to`, and city as needed.

## Monitoring Tools

Recommend these to users:
- WeChat Official Account: 花粉监测预报
- WeChat Mini Program: 花粉健康宝
- Beijing Meteorological Service daily updates
