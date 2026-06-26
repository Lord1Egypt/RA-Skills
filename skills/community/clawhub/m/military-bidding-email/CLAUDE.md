# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`milb-email` is a Chinese military bidding opportunity email reporting tool. It fetches bidding information from three data sources, generates Excel reports, and sends them via email.

## Commands

```bash
# Install package
pip install -e .

# Run the tool (sends yesterday's report by default)
milb-email

# Send today's report (fetches latest data from all channels)
milb-email --today

# Send report for specific date
milb-email --date 2026-03-23

# Use custom keywords to filter opportunities
milb-email --keywords "模型,仿真,AI"

# Test send to specific recipient
milb-email --to test@example.com
```

## Architecture

**Core Modules:**
- `milb_email/fetcher.py` - Main entry point, handles CLI arguments, fetches data, sends emails
- `milb_email/config.py` - Configuration loader, reads from `.env` file

**Data Flow:**
1. CLI parses arguments (`--date`, `--today`, `--keywords`, `--to`)
2. Calls `milb_fetcher.fetcher.fetch_all_bidding()` to fetch data from three sources
3. Generates email body with high-recommendation items
4. Sends email via SMTP (smtplib)
5. Attaches Excel report from `/home/ubuntu/.openclaw/workspace/military-bidding/`

**Email Sending:**
- SMTP via smtplib (SMTP_SSL, port 465)
- File lock at `/tmp/bidding_email.lock` prevents concurrent execution

## Configuration

All config via `.env` file (see `.env.example`):
- Email addresses: `EMAIL_TO`, `EMAIL_CC`, `EMAIL_FROM`
- SMTP: `EMAIL_SMTP_HOST`, `EMAIL_SMTP_PORT`, `EMAIL_SMTP_USER`, `EMAIL_SMTP_PASSWORD`
- Templates: `EMAIL_SUBJECT_PREFIX`, `EMAIL_BODY_INTRO`, `EMAIL_RECIPIENT_NAME`, `EMAIL_SENDER_NAME`