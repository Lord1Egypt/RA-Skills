# Meme Risk Radar Skill

A bilingual meme token risk radar for Binance Web3 data. Scan newly launched or fast-rising meme tokens from Meme Rush, enrich with token audit and token info, produce a normalized risk report in Chinese or English, and support SkillPay billing hooks for paid scan and audit calls.

## Version

Current version: **1.0.0**

## Features

- Multi-chain Support: Base, BSC, Ethereum, Solana
- Risk Assessment: Scoring system with multiple risk signals
- Audit Integration: Token security audit from Binance Web3
- Proxy Support: Built-in proxy configuration for restricted networks
- Billing Hooks: Optional SkillPay integration
- Bilingual: Chinese and English output
- Fast Scanning: Real-time meme token discovery
- Structured Output: JSON format for easy integration

## Installation

### Prerequisites

- Python 3.9+
- requests>=2.31.0

### Setup

1. Clone or copy to OpenClaw skills directory
2. Install dependencies: pip install -r requirements.txt
3. Configure environment variables: cp .env.example .env
4. Create global command (optional)

## Usage

### Health Check

meme-risk health

### Scan Meme Tokens

meme-risk scan --chain bsc --stage new --limit 10 --lang zh

### Audit Single Token

meme-risk audit --chain bsc --contract 0x1234... --lang zh

## Configuration

See .env.example for available configuration options.

## Risk Scoring

- 0-25: Low Risk
- 26-50: Medium Risk
- 51-75: High Risk
- 76-100: Critical Risk

## Disclaimer

LOW risk never means safe. This skill is a risk-filtering tool, not an execution tool. The report is a point-in-time snapshot. Do your own research (DYOR) before investing. Most meme tokens eventually go to zero.

## Changelog

See CHANGELOG.md for detailed version history.

## Support

For issues and questions, please use OpenClaw support channels.
