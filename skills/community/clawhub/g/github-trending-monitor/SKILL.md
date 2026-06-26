# GitHub Trending Monitor

Monitor GitHub trending repositories and receive daily notifications.

## Features

- 🔥 Real-time monitoring of GitHub trending repositories
- 🌍 Filter by programming language (JavaScript, Python, Go, Rust, etc.)
- 📅 Time ranges: Daily, weekly, or monthly trends
- 📱 Multi-channel notifications: Telegram, Discord, Email
- ⏰ Scheduled daily reports
- 💰 Pay-per-use: 0.001 USDT per call

## API Endpoints

### GET /trending

Fetch current GitHub trending repositories.

**Query Parameters:**
- `language` (optional): Programming language filter
- `since` (optional): Time range - daily, weekly, monthly

**Example:**
```bash
curl "http://localhost:3000/trending?language=javascript&since=daily"
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "name": "awesome-project",
      "author": "github-user",
      "description": "An awesome project",
      "language": "JavaScript",
      "stars": 1234,
      "forks": 567,
      "todayStars": 89,
      "url": "https://github.com/github-user/awesome-project"
    }
  ]
}
```

### POST /notify

Trigger immediate notification with trending repositories.

**Request:**
```json
{
  "userId": "user123",
  "transactionId": "tx456",
  "channels": {
    "telegram": { "chatId": "123456789" }
  },
  "language": "javascript",
  "since": "daily"
}
```

### POST /subscribe

Subscribe to daily trending notifications.

**Request:**
```json
{
  "userId": "user123",
  "channels": {
    "telegram": { "chatId": "123456789" }
  },
  "preferences": {
    "language": "javascript",
    "since": "daily"
  }
}
```

## Configuration

Required environment variables:
- `SKILLPAY_API_KEY`: SkillPay API key (required)
- `TELEGRAM_BOT_TOKEN`: Telegram bot token (optional)
- `DISCORD_WEBHOOK_URL`: Discord webhook URL (optional)
- `EMAIL_USER/EMAIL_PASS`: SMTP credentials (optional)

## Installation

```bash
npm install
npm start
```

## Pricing

- 0.001 USDT per API call
- Automatic settlement via SkillPay.me

## License

MIT
