---
name: Marketing Automation
description: Full marketing automation with prospects, campaigns, outreach tracking, solutions catalog, agent conversation logs, and cost tracking — built for AI agents.
author: MCF Agentic
version: 1.0.0
tags: [marketing, campaigns, prospects, outreach, automation, lead-gen, cost-tracking]
pricing: x402 (USDC on Base)
gateway: https://gateway.mcfagentic.com
---

# Marketing Automation

Run your entire marketing operation through API calls. This tool gives AI agents the ability to research and create prospects, launch campaigns, track outreach, manage a solutions catalog, and monitor marketing spend — all programmatically. No dashboards to click through, no manual data entry. Your agent finds a prospect, researches them, slots them into a campaign, and tracks every dollar spent doing it.

## Authentication

All endpoints require x402 payment (USDC on Base L2). Send a request without payment to receive pricing info in the 402 response.

## Endpoints

| Method | Path | Price | Description |
|--------|------|-------|-------------|
| GET | /api/marketing/dashboard | $0.001 | Marketing dashboard stats |
| GET | /api/marketing/prospects | $0.001 | List marketing prospects |
| POST | /api/marketing/prospects | $0.05 | Create and research a prospect |
| GET | /api/marketing/campaigns | $0.001 | List campaigns |
| POST | /api/marketing/campaigns | $0.01 | Create a campaign |
| GET | /api/marketing/outreach | $0.001 | List outreach records |
| GET | /api/marketing/costs | $0.001 | Marketing cost summary |
| GET | /api/marketing/costs/events | $0.001 | Marketing cost event log |
| GET | /api/marketing/solutions | $0.001 | List solutions |
| POST | /api/marketing/solutions | $0.01 | Create a solution |
| GET | /api/marketing/conversations | $0.001 | List agent conversation logs |
