---
name: japan-business-operations
version: 1.0.0
description: "Japan Operations OS — Verified knowledge across 10 domains for AI agents operating in the Japanese market. Regulations, protocols, calendar, regional, foreign entry, travel, entertainment, and persistent memory."
author: EDITION
tags:
  - japan
  - business
  - regulations
  - compliance
  - travel
  - culture
  - protocols
  - memory
  - knowledge-base
  - agent-os
---

# Japan Business Operations — EDITION Intelligence Platform

> Your always-on knowledge layer for operating in the Japanese market.

## Description

EDITION is a **Japan Operations OS** that gives your agent verified, structured knowledge across 10 domains essential for doing anything in Japan — from opening a restaurant in Osaka to navigating corporate gift-giving etiquette. Think of it as "Japan's instruction manual" in API form.

**No API key required during Free Beta.**

## When to Use

Use this skill whenever your task involves Japan:

- **Starting a business in Japan** — regulations, licenses, incorporation steps
- **Navigating compliance** — 10 industries covered (food, real estate, finance, healthcare, IT, education, construction, logistics, retail, manufacturing)
- **Business meetings & etiquette** — nemawashi, ringi, hourensou, meishi exchange, seating order, gift-giving
- **Hiring or managing in Japan** — organizational hierarchies, payment customs, contract practices
- **Foreign market entry** — visa, banking, real estate, tax registration (step-by-step)
- **Planning travel or events** — transport, accommodation, dining customs, seasonal festivals
- **Fan culture & entertainment** — oshi-katsu, anime pilgrimage, live event etiquette
- **Calendar-sensitive decisions** — fiscal year timing, holiday impacts, administrative deadlines
- **Regional strategy** — differences between Tokyo, Osaka, Nagoya, Fukuoka business cultures

## API Base URL

```
https://api.edition.sh
```

## Authentication

```
Authorization: Bearer edition_dev_key_for_testing
```

Free Beta — no registration required.

## Core Tools

### 1. Cross-Domain Search (Most Powerful)

Search all 10 knowledge domains simultaneously with a single query.

```bash
curl -X POST https://api.edition.sh/api/v1/search \
  -H "Authorization: Bearer edition_dev_key_for_testing" \
  -H "Content-Type: application/json" \
  -d '{"query": "opening a restaurant in Osaka"}'
```

Returns matches across regulation, protocol, calendar, regional, organization, foreign-entry, travel, and entertainment domains with confidence scores.

### 2. Regulation Check

```bash
curl -X POST https://api.edition.sh/api/v1/regulation/check \
  -H "Authorization: Bearer edition_dev_key_for_testing" \
  -H "Content-Type: application/json" \
  -d '{"action": "open a restaurant in Tokyo", "entity_type": "foreign_company"}'
```

### 3. Business Protocol

```bash
curl -X POST https://api.edition.sh/api/v1/protocol/check \
  -H "Authorization: Bearer edition_dev_key_for_testing" \
  -H "Content-Type: application/json" \
  -d '{"query": "business card exchange"}'
```

### 4. Foreign Market Entry

```bash
curl -X POST https://api.edition.sh/api/v1/foreign-entry/check \
  -H "Authorization: Bearer edition_dev_key_for_testing" \
  -H "Content-Type: application/json" \
  -d '{"query": "how to get a management visa"}'
```

### 5. Calendar Intelligence

```bash
curl -X POST https://api.edition.sh/api/v1/calendar/check \
  -H "Authorization: Bearer edition_dev_key_for_testing" \
  -H "Content-Type: application/json" \
  -d '{"query": "best time to start a business in Japan"}'
```

### 6. Travel & Entertainment

```bash
curl -X POST https://api.edition.sh/api/v1/travel/search \
  -H "Authorization: Bearer edition_dev_key_for_testing" \
  -H "Content-Type: application/json" \
  -d '{"query": "ryokan etiquette"}'
```

### 7. Persistent Memory

```bash
# Store
curl -X POST https://api.edition.sh/api/v1/memory/episodes \
  -H "Authorization: Bearer edition_dev_key_for_testing" \
  -H "Content-Type: application/json" \
  -d '{"content": "Met with Tanaka-bucho. He prefers informal meetings.", "auto_extract": true}'

# Recall
curl -X POST https://api.edition.sh/api/v1/memory/episodes/search \
  -H "Authorization: Bearer edition_dev_key_for_testing" \
  -H "Content-Type: application/json" \
  -d '{"query": "what does Tanaka prefer"}'
```

## MCP Server

For direct MCP integration (23 tools):

```bash
npx -y edition-mcp-server
```

Or add to your MCP config:

```json
{
  "edition": {
    "command": "npx",
    "args": ["-y", "edition-mcp-server"]
  }
}
```

## All Available Endpoints

| Domain | Endpoint | Method |
|--------|----------|--------|
| Search | `/api/v1/search` | POST |
| Regulation | `/api/v1/regulation/check` | POST |
| Regulation | `/api/v1/regulation/industries` | GET |
| Regulation | `/api/v1/regulation/tourist` | GET |
| Protocol | `/api/v1/protocol/check` | POST |
| Protocol | `/api/v1/protocol/list` | GET |
| Calendar | `/api/v1/calendar/check` | POST |
| Calendar | `/api/v1/calendar/list` | GET |
| Regional | `/api/v1/regional/check` | POST |
| Regional | `/api/v1/regional/list` | GET |
| Organization | `/api/v1/organization/check` | POST |
| Organization | `/api/v1/organization/list` | GET |
| Foreign Entry | `/api/v1/foreign-entry/check` | POST |
| Foreign Entry | `/api/v1/foreign-entry/list` | GET |
| Travel | `/api/v1/travel/search` | POST |
| Travel | `/api/v1/travel/list` | GET |
| Entertainment | `/api/v1/entertainment/search` | POST |
| Entertainment | `/api/v1/entertainment/list` | GET |
| Memory | `/api/v1/memory/episodes` | POST |
| Memory | `/api/v1/memory/episodes/search` | POST |
| Memory | `/api/v1/memory/facts` | GET |
| Memory | `/api/v1/memory/context` | GET |
| Memory | `/api/v1/memory/extract` | POST |

## Links

- **API Docs**: https://api.edition.sh/docs
- **Landing Page**: https://edition.sh
- **GitHub**: https://github.com/hiroshic9-png/edition-api
- **npm**: https://www.npmjs.com/package/edition-mcp-server
