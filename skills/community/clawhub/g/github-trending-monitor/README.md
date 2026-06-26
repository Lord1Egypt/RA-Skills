# GitHub Trending Monitor

Monitor GitHub trending repositories and receive daily notifications via Telegram, Discord, or Email.

## Features

- 🔥 **Real-time Trending**: Fetch latest trending repositories from GitHub
- 🌍 **Multi-language Support**: Filter by programming language
- 📅 **Time Ranges**: Daily, weekly, or monthly trends
- 📱 **Multi-channel Notifications**: Telegram, Discord, Email
- 💰 **Pay-per-use**: 0.001 USDT per API call via SkillPay
- ⏰ **Scheduled Reports**: Daily automated notifications

## Usage

### GET /trending

Fetch current GitHub trending repositories.

**Query Parameters:**
- `language` (optional): Programming language filter (e.g., javascript, python, go)
- `since` (optional): Time range - daily, weekly, or monthly (default: daily)

**Example:**
```bash
curl "http://localhost:3000/trending?language=javascript&since=daily"
```

### POST /notify

Trigger immediate notification with trending repositories.

**Request Body:**
```json
{
  "userId": "user123",
  "transactionId": "tx456",
  "channels": {
    "telegram": { "chatId": "123456789" },
    "discord": true,
    "email": { "to": "user@example.com" }
  },
  "language": "javascript",
  "since": "daily"
}
```

### POST /subscribe

Subscribe to daily trending notifications.

**Request Body:**
```json
{
  "userId": "user123",
  "channels": {
    "telegram": { "chatId": "123456789" },
    "email": { "to": "user@example.com" }
  },
  "preferences": {
    "language": "javascript",
    "since": "daily",
    "schedule": "0 9 * * *"
  }
}
```

### POST /unsubscribe

Cancel subscription.

**Request Body:**
```json
{
  "userId": "user123"
}
```

## Configuration

Create a `.env` file with the following variables:

```env
# SkillPay API Key (Required)
SKILLPAY_API_KEY=sk_e390b52cb259fc4f4aa1489547a48375d72876acdee75de57101d9e0e833fcb7

# Server Port
PORT=3000

# Telegram Bot (Optional)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Discord Webhook (Optional)
DISCORD_WEBHOOK_URL=your_discord_webhook_url

# Email SMTP (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password

# GitHub Token (Optional, for higher rate limits)
GITHUB_TOKEN=your_github_token

# Schedule (Cron format)
SCHEDULE=0 9 * * *
```

## Installation

```bash
npm install
```

## Running

```bash
npm start
```

## Testing

```bash
npm test
```

## Pricing

- **Per-call**: 0.001 USDT
- **Auto-settlement**: Via SkillPay.me

## Tech Stack

- Node.js + Express
- Cheerio (Web scraping)
- GitHub API
- Telegram Bot API
- Discord Webhooks
- Nodemailer (Email)
- node-cron (Scheduling)

## License

MIT
