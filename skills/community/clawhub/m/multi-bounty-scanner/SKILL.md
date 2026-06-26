# Multi-Platform Bounty Scanner

## Overview

Automatically scan 50+ bug bounty and OSS bounty platforms for new opportunities. Save hours of manual searching.

## When to use

Use this skill when:
- You want to find new bounty opportunities across multiple platforms
- You need to automate daily bounty scanning
- You want to filter bounties by tech stack, reward, or difficulty
- You're tired of manually checking 50+ websites

## Installation

```bash
clawhub install multi-bounty-scanner
```

Or manually:

```bash
cd ~/.openclaw/workspace/skills/multi-bounty-scanner
chmod +x scanner.js
npm link
```

## Usage

### Basic scan

```bash
bounty-scan
```

### Filter by tech stack

```bash
bounty-scan --tech javascript,python,rust
```

### Filter by minimum reward

```bash
bounty-scan --min-reward 100
```

### Export to JSON

```bash
bounty-scan --output bounties.json
```

### OpenClaw integration

Add to cron for daily automated scanning:

```bash
openclaw cron add \
  --name "Daily Bounty Scan" \
  --every 24h \
  --session isolated \
  --message "Run: cd ~/.openclaw/workspace/skills/multi-bounty-scanner && node scanner.js"
```

## Configuration

Create `~/.bounty-scanner/config.json`:

```json
{
  "filters": {
    "techStack": ["javascript", "python", "rust"],
    "minReward": 50,
    "platforms": ["github", "code4rena", "immunefi"]
  }
}
```

## Supported Platforms

Currently implemented:
- ✅ GitHub (with bounty label)

Coming soon:
- Code4rena
- Immunefi
- HackerOne
- Bugcrowd
- Intigriti
- Algora.io
- And 40+ more

## Output

The scanner tracks seen bounties and only shows new ones. Results include:
- Title
- Platform
- Reward amount
- Tech stack
- URL
- Description

## Requirements

- Node.js 18+
- GitHub CLI (`gh`) for GitHub scanning

## Pricing

- **Free**: GitHub scanning only
- **Pro ($5/month)**: All 50+ platforms (coming soon)

## Support

Issues: https://github.com/your-repo/issues

## License

MIT
