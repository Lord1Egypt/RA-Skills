---
name: Analytics Engine
description: Event tracking, funnel analysis, cohort retention, multi-touch attribution, revenue metrics, and real-time analytics — built for AI agents.
author: MCF Agentic
version: 1.0.0
tags: [analytics, events, funnels, cohorts, attribution, revenue, realtime, tracking]
pricing: x402 (USDC on Base)
gateway: https://gateway.mcfagentic.com
---

# Analytics Engine

Plug your AI agent into a full analytics stack. Track events from any source, build conversion funnels to find where users drop off, create cohorts to measure retention, and run multi-touch attribution to understand what actually drives revenue. Pull MRR, ARR, LTV, and CAC on demand. Stream real-time analytics for live monitoring. Everything an agent needs to measure, analyze, and optimize — without integrating a third-party analytics platform.

## Authentication

All endpoints require x402 payment (USDC on Base L2). Send a request without payment to receive pricing info in the 402 response.

## Endpoints

| Method | Path | Price | Description |
|--------|------|-------|-------------|
| GET | /api/analytics/overview | $0.001 | Analytics overview |
| POST | /api/analytics/events | $0.001 | Track event |
| GET | /api/analytics/events | $0.001 | List events |
| GET | /api/analytics/sessions | $0.001 | List sessions |
| GET | /api/analytics/funnels | $0.001 | List funnels |
| POST | /api/analytics/funnels | $0.01 | Create funnel |
| GET | /api/analytics/funnels/:id/analyze | $0.05 | Funnel drop-off analysis |
| GET | /api/analytics/attribution | $0.05 | Multi-touch attribution |
| GET | /api/analytics/attribution/paths | $0.05 | Attribution paths |
| GET | /api/analytics/cohorts | $0.001 | List cohorts |
| POST | /api/analytics/cohorts | $0.01 | Create cohort |
| GET | /api/analytics/cohorts/:id/analyze | $0.05 | Cohort retention |
| GET | /api/analytics/revenue | $0.01 | Revenue metrics (MRR, ARR, LTV, CAC) |
| GET | /api/analytics/realtime | $0.001 | Real-time analytics |
| POST | /api/analytics/server-events | $0.001 | Server-side event tracking |
