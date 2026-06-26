---
name: global-weather-service
description: Complete weather system powered by Open-Meteo for global city weather lookup and scheduled weather subscriptions. Use when the user asks to check current or upcoming weather anywhere in the world, wants a formatted Chinese weather bulletin, wants daily fixed-time weather pushes, or needs to list, update, or delete weather subscriptions.
---

# Global Weather Service

Use this skill for both one-time weather queries and cron-backed weather subscriptions.

## Capability split

### 1. One-time weather query

Use this when the user wants weather now, today, tomorrow, or a multi-day forecast.

Command:

```bash
python scripts/weather_report.py "伦敦"
python scripts/weather_report.py "南京" --days 7
```

Return the script output directly when the user wants the standard formatted bulletin.

### 2. Weather subscription

Use this when the user wants automatic pushes such as:
- 每天早上8点推送南京天气
- 以后每天发我伦敦今天天气
- 帮我看看我有哪些天气订阅
- 删除我的天气订阅

Set timezone first when missing:

```bash
python scripts/manage_weather_subscription.py set-timezone --to "<target>" --timezone "Asia/Shanghai"
```

Create subscription:

```bash
python scripts/manage_weather_subscription.py add --to "<target>" --city "南京" --time "每天早上8点" --mode today
python scripts/manage_weather_subscription.py add --to "<target>" --city "伦敦" --time "每天早上8点" --mode tomorrow
python scripts/manage_weather_subscription.py add --to "<target>" --city "东京" --time "每天早上8点" --mode 7day
```

List subscriptions:

```bash
python scripts/manage_weather_subscription.py list --to "<target>"
```

Update subscription:

```bash
python scripts/manage_weather_subscription.py update --id "<job-id>" --time "每天晚上8点"
python scripts/manage_weather_subscription.py update --id "<job-id>" --city "伦敦"
python scripts/manage_weather_subscription.py update --id "<job-id>" --mode 7day
```

Delete subscription:

```bash
python scripts/manage_weather_subscription.py remove --id "<job-id>"
python scripts/manage_weather_subscription.py remove --name "天气订阅: 南京 今天天气"
python scripts/manage_weather_subscription.py remove --name "南京"
```

## Output format for weather reports

Always use this structure unless the user explicitly asks for another format:

```text
#英国伦敦近七日天气
📍 2026年04月28日天气
⛅ 多云 | 温度：22.1/9.8℃

📊 生活指数
🤧 感冒：较易发
🏃 运动：适宜
👔 穿衣：长袖衬衫 / 薄外套 / 早晚加一件针织衫
☀️ 紫外线：较强
❗ 其他建议：昼夜温差明显，白天舒适，早晚偏凉，建议做好基础防晒
```

## Rules

1. Weather data source must be Open-Meteo.
2. Do not promise future pushes without creating a real cron job.
3. If subscription time is missing, ask for a concrete time first.
4. If subscription city is missing, ask which city to subscribe to.
5. If timezone is missing for subscription creation, ask for an IANA timezone explicitly.
6. Support natural subscription modes: `today`, `tomorrow`, `7day`.
7. Allow deletion by subscription id or unique subscription name.
8. When a subscription fires, fetch fresh weather at trigger time.
9. For one-time lookups, do not go through subscription flow.

## Notes

- One-time report script: `scripts/weather_report.py`
- Subscription manager script: `scripts/manage_weather_subscription.py`
- Subscription data: `data/subscriptions.json`
- User timezone data: `data/user_timezones.json`
- Open-Meteo requires no API key.
