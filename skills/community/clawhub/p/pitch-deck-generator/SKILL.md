---
name: Pitch Deck Outline Generator
description: Generate professional pitch deck outlines using the $1B pitch formula based on startup data and company information.
---

# Overview

The Pitch Deck Outline Generator is a professional presentation platform that leverages proven venture capital investment formulas to create comprehensive, investor-ready pitch deck structures. Designed for founders, startup teams, and pitch coaches, this API transforms raw business data into a structured outline following the $1B pitch deck formula—a methodology proven to attract institutional investment.

This tool automates the cognitive load of organizing complex startup information into a compelling narrative arc. Rather than starting from a blank page, entrepreneurs receive a professionally-structured outline that addresses all critical investor concerns: the problem, solution, market opportunity, business model, traction, competitive advantage, team credentials, and financial ask.

Ideal users include early-stage founders preparing for seed funding, startup accelerator programs, pitch competition participants, and venture capital coaches seeking to standardize pitch preparation workflows.

## Usage

### Sample Request

```json
{
  "startupData": {
    "companyName": "CloudSecure AI",
    "industry": "Cybersecurity",
    "problemStatement": "Enterprises lack real-time threat detection for zero-day vulnerabilities in cloud infrastructure, resulting in millions in breach costs.",
    "solution": "AI-powered threat detection platform that identifies anomalous patterns in cloud activity using machine learning models trained on 500M+ security events.",
    "targetMarket": "Mid-market to enterprise SaaS companies with 500+ employees in AWS, Azure, and GCP environments.",
    "marketSize": "$45B global cloud security market, growing at 18% CAGR through 2030.",
    "businessModel": "SaaS subscription model: $5K-$50K MRR per enterprise customer based on cloud spend and user seats.",
    "traction": "12 paying customers, $180K ARR, 40% MoM growth, partnerships with 3 major managed security service providers.",
    "competition": "CrowdStrike dominates endpoint, but no integrated cloud-native threat detection at our price point. Wiz and Lacework focus on misconfigurations.",
    "fundingAsk": "$2M Series A to expand sales team, build API integrations, and develop advanced ML detection modules.",
    "teamInfo": "CEO: 10-year background in cloud infrastructure at Google. CTO: Former security researcher at Microsoft. Head of Sales: Ex-Gartner analyst covering security.",
    "uniqueValue": "Only cloud-native platform combining real-time behavioral analysis with compliance automation (SOC2, PCI, HIPAA), reducing MTTR from 6 hours to 12 minutes.",
    "timeline": "Q1: Launch API marketplace. Q2: Break $500K ARR. Q3: Expand to APAC. Q4: Achieve FedRAMP compliance.",
    "sessionId": "session-12345",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "sessionId": "session-12345",
  "userId": 42,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Sample Response

```json
{
  "status": "success",
  "pitchDeckOutline": {
    "slideStructure": [
      {
        "slideNumber": 1,
        "title": "Cover Slide",
        "content": "CloudSecure AI - Real-Time Cloud Threat Detection",
        "speakerNotes": "Hook investors with the core value proposition: speed and precision in threat detection."
      },
      {
        "slideNumber": 2,
        "title": "The Problem",
        "content": "Enterprises lack real-time threat detection for zero-day vulnerabilities in cloud infrastructure, resulting in millions in breach costs.",
        "keyPoints": [
          "Average breach detection time: 6+ hours",
          "Cost per breach: $4.45M average",
          "Cloud workloads growing 30% annually"
        ]
      },
      {
        "slideNumber": 3,
        "title": "The Solution",
        "content": "AI-powered threat detection platform with real-time anomaly detection",
        "keyPoints": [
          "ML models trained on 500M+ security events",
          "Automated response workflows",
          "Integrated compliance reporting"
        ]
      },
      {
        "slideNumber": 4,
        "title": "Market Opportunity",
        "content": "$45B cloud security market, 18% CAGR through 2030",
        "addressableMarket": "$8.2B serviceable market (mid-market and enterprise)"
      },
      {
        "slideNumber": 5,
        "title": "Business Model",
        "content": "SaaS subscription: $5K-$50K MRR per enterprise customer",
        "unitEconomics": {
          "acv": "$60K-$600K",
          "paybackPeriod": "9 months"
        }
      },
      {
        "slideNumber": 6,
        "title": "Traction",
        "content": "12 paying customers, $180K ARR, 40% MoM growth",
        "metrics": [
          "3 enterprise pilots closing Q1",
          "3 MSSP partnerships signed"
        ]
      },
      {
        "slideNumber": 7,
        "title": "Competitive Advantage",
        "content": "Only cloud-native platform combining behavioral analysis with compliance automation",
        "differentiation": [
          "MTTR reduced from 6 hours to 12 minutes",
          "Native SOC2, PCI, HIPAA compliance",
          "5x faster detection than competitors"
        ]
      },
      {
        "slideNumber": 8,
        "title": "The Team",
        "content": "Experienced founders with deep security and go-to-market expertise",
        "teamHighlights": [
          "CEO: 10 years cloud infrastructure (Google)",
          "CTO: Security researcher (Microsoft)",
          "Head of Sales: Gartner analyst (security)"
        ]
      },
      {
        "slideNumber": 9,
        "title": "Financials & Ask",
        "content": "$2M Series A investment",
        "useOfFunds": {
          "salesExpansion": "40%",
          "productDevelopment": "35%",
          "operations": "25%"
        }
      },
      {
        "slideNumber": 10,
        "title": "18-Month Roadmap",
        "content": "Clear milestones from Q1 API marketplace to Q4 FedRAMP compliance"
      }
    ],
    "designRecommendations": {
      "primaryColor": "#20002c",
      "secondaryColor": "#cbb4d4",
      "fontRecommendation": "Montserrat (headlines), Open Sans (body)",
      "themeStyle": "Modern, security-focused, professional"
    }
  },
  "generatedAt": "2024-01-15T10:35:22Z"
}
```

## Endpoints

### GET /

**Description:** Root endpoint providing API availability status.

**Response:** Returns JSON object confirming API is running.

---

### GET /health

**Description:** Health check endpoint for monitoring API uptime and service status.

**Response:** Returns JSON object with health status.

---

### POST /api/pitchdeck/generate

**Description:** Generate a comprehensive pitch deck outline based on startup data using the $1B pitch formula.

**Request Body:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `startupData` | StartupData object | Yes | Core startup information including company details, business model, traction, and team info |
| `sessionId` | string | Yes | Unique session identifier for tracking and audit purposes |
| `userId` | integer or null | No | Optional user ID for analytics and personalization |
| `timestamp` | string | Yes | ISO 8601 timestamp of request (e.g., "2024-01-15T10:30:00Z") |

**StartupData Schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `companyName` | string | Yes | Official company name |
| `industry` | string | Yes | Industry vertical (e.g., Cybersecurity, FinTech, HealthTech) |
| `problemStatement` | string | Yes | Clear description of the customer problem being solved |
| `solution` | string | Yes | Explanation of how the product solves the problem |
| `targetMarket` | string | Yes | Description of ideal customer profile and market segment |
| `marketSize` | string | Yes | Total addressable market (TAM) with growth projections |
| `businessModel` | string | Yes | Revenue model and pricing structure |
| `traction` | string | Yes | Current metrics: MRR, ARR, user count, growth rate, partnerships |
| `competition` | string | Yes | Competitive landscape and differentiation factors |
| `fundingAsk` | string | Yes | Amount seeking and use of funds breakdown |
| `teamInfo` | string | Yes | Founder credentials, relevant experience, and advisory board |
| `uniqueValue` | string | Yes | Core value proposition and competitive moat |
| `timeline` | string | Yes | 12-18 month roadmap with key milestones |
| `primaryColor` | string | No | Primary brand color in hex format (default: "#20002c") |
| `secondaryColor` | string | No | Secondary brand color in hex format (default: "#cbb4d4") |
| `sessionId` | string | Yes | Unique session identifier (same as parent request) |
| `timestamp` | string | Yes | ISO 8601 timestamp (same as parent request) |

**Response (200 - Success):**

Returns JSON object with:
- `status`: "success"
- `pitchDeckOutline`: Structured slide-by-slide outline following the $1B pitch formula
- `designRecommendations`: Primary/secondary colors, font suggestions, theme style
- `generatedAt`: Timestamp of outline generation

**Response (422 - Validation Error):**

Returns validation error details indicating which required fields are missing or invalid.

## Pricing

| Plan | Calls/Day | Calls/Month | Price |
|------|-----------|-------------|-------|
| Free | 5 | 50 | Free |
| Developer | 20 | 500 | $39/mo |
| Professional | 200 | 5,000 | $99/mo |
| Enterprise | 100,000 | 1,000,000 | $299/mo |

## About

ToolWeb.in - 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- [toolweb.in](https://toolweb.in)
- [portal.toolweb.in](https://portal.toolweb.in)
- [hub.toolweb.in](https://hub.toolweb.in)
- [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

## References

- **Kong Route:** https://api.mkkpro.com/creative/pitch-deck-generator
- **API Docs:** https://api.mkkpro.com:8076/docs
