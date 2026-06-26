# Global Weather Service

A complete OpenClaw weather skill powered by **Open-Meteo**.

It supports both **one-time global weather queries** and **scheduled weather subscriptions**.

## Highlights

- Global city weather lookup
- Chinese formatted weather bulletin output
- Lifestyle advice based on forecast data
  - clothing
  - exercise
  - cold-risk
  - UV
  - extra travel suggestions
- Scheduled weather push through OpenClaw cron
- Subscription management
  - create
  - list
  - update
  - delete
- Natural subscription modes
  - today
  - tomorrow
  - 7day
- No API key required

## Data source

- [Open-Meteo](https://open-meteo.com/)

## Project structure

```text
global-weather-service/
├─ SKILL.md
├─ README.md
├─ data/
│  ├─ subscriptions.json
│  └─ user_timezones.json
└─ scripts/
   ├─ weather_report.py
   └─ manage_weather_subscription.py
```

## Capabilities

### 1. One-time weather query

Query current or upcoming weather for global cities and format the result into a Chinese bulletin.

Example:

```bash
python scripts/weather_report.py "南京" --days 7
python scripts/weather_report.py "London" --days 1
python scripts/weather_report.py "Dubai" --days 7
```

### 2. Scheduled weather subscription

Create a real OpenClaw cron-backed subscription that pushes weather automatically.

Supported modes:

- `today` → today weather
- `tomorrow` → tomorrow weather
- `7day` → 7-day forecast

Example:

```bash
python scripts/manage_weather_subscription.py add --to "qqbot:c2c:YOUR_ID" --city "南京" --time "每天晚上10点30分" --mode tomorrow
```

### 3. Subscription management

- List subscriptions
- Update subscription city, time, or mode
- Remove subscription by id or name
- Store per-user timezone for correct scheduling

## Example output

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

## Usage

### Query weather

```bash
python scripts/weather_report.py "南京" --days 7
python scripts/weather_report.py "Los Angeles" --days 1
```

### Set timezone

```bash
python scripts/manage_weather_subscription.py set-timezone --to "qqbot:c2c:YOUR_ID" --timezone "Asia/Shanghai"
```

### Create subscription

```bash
python scripts/manage_weather_subscription.py add --to "qqbot:c2c:YOUR_ID" --city "南京" --time "每天早上8点" --mode today
python scripts/manage_weather_subscription.py add --to "qqbot:c2c:YOUR_ID" --city "南京" --time "每天晚上10点30分" --mode tomorrow
python scripts/manage_weather_subscription.py add --to "qqbot:c2c:YOUR_ID" --city "东京" --time "每天早上8点" --mode 7day
```

### List subscriptions

```bash
python scripts/manage_weather_subscription.py list --to "qqbot:c2c:YOUR_ID"
```

### Update subscription

```bash
python scripts/manage_weather_subscription.py update --id "<job-id>" --time "每天晚上9点"
python scripts/manage_weather_subscription.py update --id "<job-id>" --city "伦敦"
python scripts/manage_weather_subscription.py update --id "<job-id>" --mode 7day
```

### Remove subscription

```bash
python scripts/manage_weather_subscription.py remove --id "<job-id>"
python scripts/manage_weather_subscription.py remove --name "天气订阅: 南京 明天天气"
```

## Notes

- This skill is designed for OpenClaw environments.
- Scheduled delivery relies on OpenClaw cron and channel routing.
- For QQ delivery, targets should use the `qqbot:c2c:<id>` form.
- The weather script includes retry logic for transient network failures.
- The subscription manager normalizes QQ targets to reduce delivery mistakes.

## Repository and package

- GitHub: <https://github.com/zykkk-power/global-weather-service>
- ClawHub: `global-weather-service`

## License

If you want to publish this for broader reuse, add a license file that matches your sharing intent.
