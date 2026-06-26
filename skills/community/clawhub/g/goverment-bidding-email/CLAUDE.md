# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`govb-email` is a Chinese government procurement opportunity email reporting tool. It fetches bidding information from two data sources (北京政采, 湖南政采), generates Excel reports, and sends them via email.

## Commands

```bash
# Install package
pip install -e .

# Run the tool (sends yesterday's report by default)
govb-email

# Send today's report
govb-email --today

# Send report for specific date
govb-email --date 2026-03-23

# Use custom keywords to filter opportunities
govb-email --keywords "模型,仿真,AI"

# Test send to specific recipient
govb-email --to test@example.com
```

## Architecture

**Core Modules:**
- `govb_email/fetcher.py` - Main entry point, handles CLI arguments, fetches data, sends emails
- `govb_email/config.py` - Configuration loader, reads from `.env` file

**Data Flow:**
1. CLI parses arguments (`--date`, `--today`, `--keywords`, `--to`)
2. Calls `govb_fetcher.fetcher.fetch_all_bidding(target_date)` to fetch data from two sources
3. Generates email body with high-recommendation items
4. Sends email via SMTP (smtplib)
5. Attaches Excel report from `~/.openclaw/workspace/govb-bidding/`

**Email Sending:**
- SMTP via smtplib (SMTP_SSL, port 465)
- File lock at `/tmp/govb_bidding_email.lock` prevents concurrent execution

## Configuration

All config via `.env` file (see `.env.example`):
- Email addresses: `EMAIL_TO`, `EMAIL_CC`, `EMAIL_FROM`
- SMTP: `EMAIL_SMTP_HOST`, `EMAIL_SMTP_PORT`, `EMAIL_SMTP_USER`, `EMAIL_SMTP_PASSWORD`
- Templates: `EMAIL_SUBJECT_PREFIX`, `EMAIL_BODY_INTRO`, `EMAIL_RECIPIENT_NAME`, `EMAIL_SENDER_NAME`

Config file search order:
1. `.env` in current working directory
2. `~/.config/govb-email/.env`
