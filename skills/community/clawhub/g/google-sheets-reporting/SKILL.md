---
name: google-sheets-reporting
description: Automated reporting and alerts from Google Sheets data. Daily summaries with auto-detected metrics, configurable threshold alerts, and weekly multi-sheet digest emails. 3 production-ready n8n workflows.
tags: [reporting, google-sheets, alerts, analytics, email, dashboards, automation, n8n]
author: mhmalvi
version: 1.2.0
license: CC BY-NC-SA 4.0
metadata:
  clawdbot:
    emoji: "\U0001F4CA"
    requires:
      n8nCredentials: [google-sheets-oauth2, smtp]
      env: [REPORT_EMAIL, ALERT_THRESHOLDS]
    os: [linux, darwin, win32]
---

# Google Sheets Reporting

Automated reporting and alerting from any Google Sheets data. Get daily summaries, threshold-based alerts, and weekly digest emails without building dashboards.

## Problem

Teams store operational data in Google Sheets but lack automated reporting. Checking sheets manually is tedious, and important changes (threshold violations, trends) go unnoticed until it's too late.

This skill turns any Google Sheet into an automated reporting system with zero code changes.

## What It Does

1. **Daily Summary** — Auto-detects numeric columns, calculates sum/avg/min/max, emails formatted report
2. **Threshold Alerts** — Checks values against configurable min/max thresholds hourly, sends alert emails when violated
3. **Weekly Digest** — Multi-sheet summary every Monday with period-over-period comparison

## Included Workflows

| # | File | Purpose |
|---|------|---------|
| 01 | `01-daily-summary.json` | Daily aggregate statistics email for any sheet |
| 02 | `02-threshold-alerts.json` | Hourly threshold monitoring with alert emails |
| 03 | `03-weekly-digest.json` | Weekly multi-sheet digest email (Monday 9AM) |

## Architecture

```
Daily (once):
    |
    v
Workflow 01: Daily Summary
    +-> Read sheet data
    +-> Auto-detect numeric columns
    +-> Calculate sum, avg, min, max
    +-> Count categories in first text column
    +-> Email formatted report

Hourly:
    |
    v
Workflow 02: Threshold Alerts
    +-> Read sheet data
    +-> Check each value against thresholds
    +-> IF violations found -> email alert
    +-> Thresholds configurable via env variable

Weekly (Monday 9AM):
    |
    v
Workflow 03: Weekly Digest
    +-> Read primary + secondary sheets in parallel
    +-> Summarize both sheets
    +-> Email combined digest
```

## Required n8n Credentials

| Credential Type | Used For | Placeholder in JSON |
|----------------|----------|---------------------|
| Google Sheets OAuth2 | Reading sheet data | `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` |
| SMTP | Sending reports and alerts | `YOUR_SMTP_CREDENTIAL_ID` |

## Configuration Placeholders

| Placeholder | Description |
|-------------|-------------|
| `YOUR_REPORT_SHEET_ID` | Google Sheet ID to monitor |
| `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` | n8n Google Sheets credential ID |
| `YOUR_SMTP_CREDENTIAL_ID` | n8n SMTP credential ID |
| `YOUR_NOTIFICATION_EMAIL` | Email for reports and alerts |

## Environment Variables

```bash
# Required
REPORT_EMAIL=your-email@example.com

# Optional: Threshold configuration (JSON)
ALERT_THRESHOLDS='{"revenue":{"min":100,"max":null,"label":"Revenue"},"error_count":{"min":null,"max":10,"label":"Errors"}}'
```

## Threshold Configuration

Thresholds are configured via the `ALERT_THRESHOLDS` environment variable as JSON:

```json
{
  "column_name": {
    "min": 100,
    "max": null,
    "label": "Display Name"
  }
}
```

- `min` — Alert if value falls below this (set `null` to disable)
- `max` — Alert if value exceeds this (set `null` to disable)
- `label` — Human-readable name for alert emails

## Quick Start

### 1. Prerequisites
- n8n v2.4+ (self-hosted)
- Google Sheets OAuth2 credentials
- SMTP email credentials
- A Google Sheet with data (any structure works)

### 2. Import & Configure
Import all 3 JSON files into n8n. Replace `YOUR_REPORT_SHEET_ID` with your sheet's ID and set credential placeholders.

### 3. Customize Sheet Names
Edit the Google Sheets nodes to match your tab names (default: "Data" and "Sheet2").

### 4. Set Thresholds
Configure `ALERT_THRESHOLDS` env var for your columns, or edit the Code node defaults directly.

### 5. Activate
Activate all 3 workflows. You'll receive your first daily summary within 24 hours.

## Use Cases

1. **Sales teams** — Daily revenue summaries and low-sales alerts from order sheets
2. **Support teams** — Ticket count monitoring with escalation alerts
3. **Marketing** — Campaign performance digests from tracking sheets
4. **Operations** — Inventory level alerts and daily status reports
5. **Finance** — Expense monitoring with budget threshold alerts

## Requirements

- n8n v2.4+ (self-hosted or cloud)
- Google Sheets OAuth2 credentials
- SMTP email credentials
