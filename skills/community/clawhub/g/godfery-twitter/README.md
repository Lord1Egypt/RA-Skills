# OpenClaw Twitter 🐦

Twitter/X data and automation for autonomous agents. Powered by SkillBoss API Hub.

## Installation

```bash
export SKILLBOSS_API_KEY="your-key"
```

## Quick Start

```bash
# Get user info
python scripts/twitter_client.py user-info --username elonmusk

# Search tweets
python scripts/twitter_client.py search --query "AI agents"

# Get trends
python scripts/twitter_client.py trends
```

## Features

- **Read Operations**: User info, tweets, search, trends, followers, followings
- **Write Operations**: Post tweets, like, retweet (requires login)

## Get API Key

Sign up at [skillbossai.com](https://skillbossai.com)

## Links

- [ClawHub](https://www.clawhub.com/aisa-one/openclaw-twitter)
- [API Reference](https://aisa.mintlify.app/api-reference/introduction)
