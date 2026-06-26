---
name: kisa-guideline-hub
version: 1.1.0
description: Automatically collect and publish security guidelines and guides from KISA and Boho (보호나라) to Notion. Use when you need to (1) collect new security guidelines, (2) publish guidelines to Notion, (3) manage PDF downloads from KISA/Boho, or (4) run automated guideline collection. Triggered by "가이드라인 발행", "가이드 수집", "KISA 가이드", "보호나라 가이드", "guideline publisher".
---

# Guideline Publisher

## Overview

Automated system to collect security guidelines from Korean security organizations (KISA, Boho) and publish them to Notion. Unlike regular security news, guidelines are published directly without LLM processing.

## Supported Sources

**KISA (한국인터넷진흥원)**:
- Security guidelines and best practices
- Configuration guides
- Policy documents
- URL: https://인터넷진흥원.한국/2060207

**Boho (보호나라/KRCERT)**:
- Security vulnerability guides
- Incident response guides
- Technical guidelines
- URL: https://www.boho.or.kr
- Includes PDF downloads

## Workflow

### 1. Collect Guidelines

```bash
cd ~/.openclaw/workspace/skills/security-news-module
python3 scripts/publish_guidelines.py --collect
```

This will:
- Run KISA crawler (10 guidelines)
- Run Boho crawler (11 guidelines, PDF downloads)
- Collect PDF files to temp_downloads/ directory
- Store articles in processing queue

### 2. Publish to Notion

```bash
python3 scripts/publish_guidelines.py --publish
```

This will:
- Publish collected guidelines to Notion GUIDE_DATABASE_ID
- Upload PDF files to Notion
- No LLM processing (direct publishing)
- Skip duplicates automatically

### 3. Full Pipeline

```bash
python3 scripts/publish_guidelines.py --full
```

Runs both collection and publishing in sequence.

## Notion Database Configuration

Guidelines are published to a separate Notion database:

**GUIDE_DATABASE_ID**: Set in `.env` as `SECURITY_GUIDE_DATABASE_ID`

If not set, defaults to `SECURITY_NEWS_DATABASE_ID`

**Notion Properties**:
- Title: Guideline name
- Category: "KISA 가이드라인" or "보호나라 가이드라인"
- URL: Original source URL
- Date: Publication date
- Files: PDF attachments (Boho only)

## Key Differences from Security News

**Guidelines**:
- ✅ Direct publishing (no LLM processing)
- ✅ PDF file uploads
- ✅ Separate Notion database
- ✅ KISA + Boho sources

**Security News**:
- ✅ LLM summary + analysis
- ✅ Mermaid diagrams
- ✅ Main Notion database
- ✅ 9 sources (KRCERT, 데일리시큐, etc.)

## Environment Variables

Required in `~/.openclaw/workspace/.env`:

```bash
# Notion
NOTION_API_KEY=ntn_xxx
SECURITY_NEWS_DATABASE_ID=xxx
SECURITY_GUIDE_DATABASE_ID=xxx  # Optional, defaults to SECURITY_NEWS_DATABASE_ID

# GLM API (for security news only)
SECURITY_NEWS_GLM_API_KEY=xxx
```

## File Structure

```
security-news-module/
├── modules/
│   ├── crawlers/
│   │   ├── kisa.py (KISA guidelines)
│   │   └── boho.py (Boho guidelines + PDF)
│   ├── publisher_service.py
│   └── notion_handler.py (PDF upload support)
└── scripts/
    └── publish_guidelines.py (This skill's script)
```

## PDF Downloads

Boho crawler automatically downloads PDF files:

```
temp_downloads_boho/
├── 가이드라인1.pdf
├── 가이드라인2.pdf
└── ...
```

PDFs are uploaded to Notion as file blocks.

## Troubleshooting

**No guidelines collected**:
- Check KISA/Boho websites are accessible
- Verify Notion API key and database ID
- Check network connectivity

**PDF upload fails**:
- Verify Notion API supports file uploads
- Check file size limits (20MB max)
- Ensure temp_downloads/ directory exists

**Duplicate guidelines**:
- Notion Duplicate_check() prevents duplicates
- Based on URL matching
- Safe to run multiple times

## Integration with Security News Module

This skill is integrated into the Security News Module:

```bash
# Run both guidelines and news
python3 security_news_aggregator.py --once

# Guidelines run first (no LLM, fast)
# Then security news (with LLM, slower)
```

## Cron Scheduling

For automated hourly runs:

```bash
# Already configured in LaunchAgent
# com.openclaw.security-news.plist
# Runs every hour automatically
```

## Resources

### scripts/
- `publish_guidelines.py` - Main script for guideline collection and publishing

### references/
- `schema.md` - Notion database schema for guidelines
- `examples.md` - Example guideline publications
