---
name: Heuristic Phishing Detection
description: Analyzes URLs using heuristic algorithms to detect and identify phishing threats in real time.
---

# Overview

Heuristic Phishing Detection is a security-focused API that analyzes suspicious URLs to identify phishing attacks and malicious links. Using advanced heuristic algorithms, the tool examines URL structure, domain characteristics, and behavioral patterns to determine threat likelihood without relying solely on blocklists.

This API is ideal for security teams, email filtering systems, browser extensions, and web applications that need to protect users from phishing campaigns. It provides fast, accurate risk assessment for URLs encountered in emails, messages, search results, and web content, enabling proactive threat prevention before users interact with malicious sites.

Key capabilities include real-time URL analysis, heuristic-based threat detection, and detailed risk scoring. The tool integrates seamlessly into security workflows, SIEM platforms, and automated incident response systems.

# Usage

## Sample Request

```json
{
  "url": "https://secure-paypal-verify.com/login"
}
```

## Sample Response

```json
{
  "url": "https://secure-paypal-verify.com/login",
  "is_phishing": true,
  "risk_score": 0.92,
  "threat_indicators": [
    "homograph_domain",
    "suspicious_tld",
    "brand_impersonation"
  ],
  "confidence": 0.95,
  "analysis_timestamp": "2024-01-15T10:32:45Z"
}
```

# Endpoints

## POST /check-url

Analyzes a provided URL for phishing characteristics and returns a threat assessment.

**Method:** `POST`

**Path:** `/check-url`

**Description:** Submits a URL for heuristic analysis to determine phishing risk. The API examines domain structure, SSL certificate patterns, content indicators, and known phishing signatures.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `url` | string | Yes | The complete URL to analyze, including protocol (http:// or https://). Maximum 2048 characters. |

### Request Body

```json
{
  "url": "string"
}
```

### Response (200 OK)

**Content-Type:** `application/json`

The response contains phishing detection results with risk indicators:

```json
{
  "url": "string",
  "is_phishing": "boolean",
  "risk_score": "number (0-1)",
  "threat_indicators": ["array of strings"],
  "confidence": "number (0-1)",
  "analysis_timestamp": "string (ISO 8601)"
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `url` | string | Echo of the submitted URL |
| `is_phishing` | boolean | True if phishing detected, false otherwise |
| `risk_score` | number | Numeric risk assessment from 0.0 (safe) to 1.0 (confirmed phishing) |
| `threat_indicators` | array | List of detected threat patterns (e.g., homograph_domain, suspicious_tld, brand_impersonation) |
| `confidence` | number | Confidence level of the analysis from 0.0 to 1.0 |
| `analysis_timestamp` | string | ISO 8601 timestamp of when analysis was performed |

### Response (422 Validation Error)

**Content-Type:** `application/json`

Returned when request validation fails:

```json
{
  "detail": [
    {
      "loc": ["body", "url"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

# Pricing

| Plan | Calls/Day | Calls/Month | Price |
|------|-----------|-------------|-------|
| Free | 5 | 50 | Free |
| Developer | 20 | 500 | $39/mo |
| Professional | 200 | 5,000 | $99/mo |
| Enterprise | 100,000 | 1,000,000 | $299/mo |

# About

ToolWeb.in — 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- 🌐 [toolweb.in](https://toolweb.in)
- 🔌 [portal.toolweb.in](https://portal.toolweb.in)
- 🤖 [hub.toolweb.in](https://hub.toolweb.in)
- 🐾 [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- 🚀 [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- 📺 [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

# References

- **Kong Route:** `https://api.mkkpro.com/security/phishing-detection`
- **API Docs:** `https://api.mkkpro.com:8005/docs`
