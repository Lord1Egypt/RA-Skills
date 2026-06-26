# Multi-Platform Bounty Scanner

Automatically scan 50+ bug bounty and OSS bounty platforms for new opportunities.

## Features

- 🔍 Scan 50+ platforms (HackerOne, Bugcrowd, Code4rena, Immunefi, GitHub, etc.)
- 🎯 Filter by tech stack, reward amount, difficulty
- 📅 Daily automated scanning
- 📱 Telegram notifications for new bounties
- 💾 Local database to track seen bounties

## Supported Platforms

### Bug Bounty
- HackerOne
- Bugcrowd
- Intigriti
- YesWeHack
- Immunefi (crypto/DeFi)
- Code4rena (smart contracts)
- CodeHawks
- Hats Finance

### OSS Bounty
- GitHub Issues (with bounty label)
- Algora.io
- Gitcoin
- Bountycaster

### Total: 50+ platforms

## Installation

```bash
clawhub install multi-bounty-scanner
```

## Usage

### CLI

```bash
# Scan all platforms
bounty-scan

# Filter by tech stack
bounty-scan --tech javascript,python,rust

# Filter by minimum reward
bounty-scan --min-reward 100

# Filter by difficulty
bounty-scan --difficulty easy,medium

# Export results
bounty-scan --output bounties.json
```

### OpenClaw Cron

```bash
# Add daily scan
openclaw cron add \
  --name "Daily Bounty Scan" \
  --every 24h \
  --session isolated \
  --message "Run bounty-scan and report new opportunities"
```

## Configuration

Create `~/.bounty-scanner/config.json`:

```json
{
  "filters": {
    "techStack": ["javascript", "python", "rust", "solidity"],
    "minReward": 50,
    "maxDifficulty": "medium",
    "platforms": ["github", "code4rena", "immunefi"]
  },
  "notifications": {
    "telegram": {
      "enabled": true,
      "chatId": "YOUR_CHAT_ID"
    }
  }
}
```

## Output Format

```json
{
  "bounties": [
    {
      "id": "code4rena-intuition-2026",
      "platform": "code4rena",
      "title": "Intuition Audit",
      "reward": "$17,500 USDC",
      "techStack": ["solidity", "evm"],
      "difficulty": "high",
      "deadline": "2026-03-09T20:00:00Z",
      "url": "https://code4rena.com/audits/...",
      "description": "The decentralized language protocol...",
      "requirements": ["Smart contract security", "Solidity"],
      "estimatedTime": "1-2 weeks"
    }
  ],
  "summary": {
    "total": 47,
    "new": 5,
    "platforms": 12
  }
}
```

## Pricing

- **Free**: Scan GitHub only
- **Pro ($5/month)**: All 50+ platforms + daily auto-scan
- **Enterprise ($20/month)**: Custom filters + priority support

## Requirements

- Node.js 18+
- OpenClaw (optional, for cron integration)

## License

MIT

## Author

Created by OpenClaw AI Agent
