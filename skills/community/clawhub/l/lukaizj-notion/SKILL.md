---
name: Notion Integration
description: Notion integration - Manage pages, databases, and content in Notion
homepage: https://github.com/lukaizj/notion-integration-skill
tags:
  - productivity
  - integration
  - notion
  - database
requires:
  env:
    - NOTION_API_KEY
files:
  - notion.py
---

# Notion Integration

Notion integration skill for OpenClaw. Manage pages, databases, and content in Notion.

## Capabilities

- Create new pages
- Query databases
- Update page content
- Search pages
- Create database entries

## Setup

1. Create an integration at https://www.notion.so/my-integrations
2. Get the Internal Integration Token
3. Share pages/databases with the integration
4. Configure NOTION_API_KEY environment variable

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NOTION_API_KEY` | Yes | Your Notion API Key (secret_xxx) |