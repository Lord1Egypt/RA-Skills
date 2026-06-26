---
name: kpi-alert-system
description: >
  Business KPI monitoring with threshold-based alerts. Connects to QuickBooks Online, Google Sheets,
  and CSV exports to track AR aging, cash runway, revenue growth, gross margin, and burn rate.
  Fires alerts via Telegram, Slack, or email when thresholds breach. Use when a user wants to set up
  automated financial health monitoring, define alert rules for business metrics, or run a periodic
  KPI check. NOT for real-time stock/crypto monitoring (use defi-position-tracker), ERP systems
  (SAP, Oracle), or dashboards requiring live BI tools (use Power BI or Looker).
version: 1.0.0
updated: 2026-03-15
metadata:
  openclaw:
    requires:
      bins: []
    channels:
      - telegram
      - slack
      - email
---

# KPI Alert System Skill

Automated KPI monitoring with threshold alerts for business financial health. Pulls data from QBO, Google Sheets, or CSV exports, evaluates rules, and fires alerts to Telegram/Slack/email.

---

## Supported KPIs

| KPI | Description | Typical Alert Threshold |
|-----|-------------|------------------------|
| AR Aging (30/60/90+) | Outstanding receivables by age bucket | >$X in 90+ days, or >30% of AR |
| Cash Runway | Months of runway at current burn | <3 months = red, <6 months = yellow |
| Monthly Burn Rate | Net cash outflow per month | >$X/month or >Y% above budget |
| Revenue Growth (MoM/QoQ) | Revenue trend vs prior period | <0% = alert, <5% = warning |
| Gross Margin % | (Revenue - COGS) / Revenue | <X% below target |
| Net Income / Loss | P&L bottom line | Negative for N consecutive months |
| DSO (Days Sales Outstanding) | AR / (Revenue / 30) | >45 days = yellow, >60 = red |
| Current Ratio | Current Assets / Current Liabilities | <1.2 = alert |
| Quick Ratio | (Cash + AR) / Current Liabilities | <1.0 = alert |
| Payroll % of Revenue | Payroll costs as % of top line | >X% = alert |

---

## Setup Steps

### 1. Define Your KPI Config

Create a YAML config file for the client or firm:

```yaml
# kpi-config-clientname.yaml
client: "Acme Corp"
alert_channels:
  - type: telegram
    target: "@irfan_dm"  # or channel ID
  - type: slack
    webhook: "https://hooks.slack.com/services/..."
  - type: email
    to: "imussa@precisionledger.io"

kpis:
  ar_aging_90plus:
    label: "AR 90+ Days"
    source: qbo  # or sheets, csv
    threshold_red: 15000
    threshold_yellow: 8000
    message: "AR aging 90+ days is ${value} — collections action needed"

  cash_runway_months:
    label: "Cash Runway"
    source: qbo
    threshold_red: 3
    threshold_yellow: 6
    direction: below  # alert when BELOW threshold (default: above)
    message: "Cash runway is {value} months — review burn rate immediately"

  revenue_growth_mom:
    label: "MoM Revenue Growth"
    source: sheets
    sheet_id: "1BxiM..."
    tab: "P&L Summary"
    cell_range: "C5"
    threshold_red: -5
    threshold_yellow: 0
    direction: below
    message: "Revenue growth is {value}% MoM — investigate pipeline"

  gross_margin_pct:
    label: "Gross Margin %"
    source: qbo
    threshold_red: 30
    threshold_yellow: 40
    direction: below
    message: "Gross margin at {value}% — below target of 40%"
```

---

### 2. Data Source Integration

#### QuickBooks Online (via QBO Automation skill)
```bash
# Pull P&L summary for current month
qbo report pl --period this-month --format json > /tmp/pl-current.json

# Pull AR aging
qbo report ar-aging --format json > /tmp/ar-aging.json

# Pull balance sheet for liquidity ratios
qbo report balance-sheet --period this-month --format json > /tmp/bs-current.json
```

#### Google Sheets (via gog skill)
```bash
# Read a named range
gog sheets read --id SHEET_ID --range "KPI Dashboard!B2:C20"
```

#### CSV / Excel Export
Place exports at a consistent path and reference in config:
```yaml
source: csv
file: "/tmp/monthly-export-2026-03.csv"
column: "AR_90plus"
row_filter: "Month=March"
```

---

### 3. KPI Evaluation Logic

**Core algorithm (Python pseudocode for reference):**

```python
def evaluate_kpi(config, value):
    direction = config.get("direction", "above")
    
    if direction == "above":
        if value >= config["threshold_red"]:
            return "RED", config["message"].format(value=value)
        elif value >= config["threshold_yellow"]:
            return "YELLOW", config["message"].format(value=value)
    else:  # below
        if value <= config["threshold_red"]:
            return "RED", config["message"].format(value=value)
        elif value <= config["threshold_yellow"]:
            return "YELLOW", config["message"].format(value=value)
    
    return "GREEN", None

def run_kpi_check(config_path):
    config = load_yaml(config_path)
    alerts = []
    
    for kpi_id, kpi_config in config["kpis"].items():
        value = fetch_kpi_value(kpi_config)  # pulls from QBO/Sheets/CSV
        status, message = evaluate_kpi(kpi_config, value)
        
        if status in ["RED", "YELLOW"]:
            alerts.append({
                "kpi": kpi_config["label"],
                "status": status,
                "value": value,
                "message": message
            })
    
    return alerts
```

---

### 4. Alert Formatting

**Telegram message format:**
```
🚨 KPI ALERT — Acme Corp
Date: March 15, 2026

🔴 AR 90+ Days: $18,500
   → Collections action needed immediately

🟡 Gross Margin: 38%
   → Below 40% target — review COGS

✅ Cash Runway: 8.2 months
✅ Revenue Growth: +4.2% MoM

Run by: Sam Ledger / PrecisionLedger
```

**Slack format (with attachments):**
```json
{
  "attachments": [
    {
      "color": "#ff0000",
      "title": "🔴 AR 90+ Days — $18,500",
      "text": "Collections action needed. 90+ day bucket exceeds $15,000 threshold.",
      "footer": "KPI Alert System | PrecisionLedger",
      "ts": 1742076000
    }
  ]
}
```

---

### 5. Scheduling with OpenClaw Cron

**Monthly KPI check (1st of month, 9 AM CST):**
```json
{
  "name": "Monthly KPI Check — Acme Corp",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 1 * *",
    "tz": "America/Chicago"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Run KPI alert check for Acme Corp using kpi-config-acme.yaml. Pull QBO AR aging and P&L, evaluate thresholds, and send alerts to the configured channels."
  },
  "sessionTarget": "isolated",
  "delivery": {
    "mode": "announce"
  }
}
```

**Weekly cash runway check (every Monday, 8 AM CST):**
```json
{
  "name": "Weekly Cash Runway Check",
  "schedule": {
    "kind": "cron",
    "expr": "0 8 * * 1",
    "tz": "America/Chicago"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Check cash runway and burn rate for all active clients. Alert if any client is below 6 months runway."
  },
  "sessionTarget": "isolated"
}
```

---

## Example Prompts

### Setup
> "Set up KPI alerts for my client TechStartup LLC. Alert me on Telegram when AR aging hits 90 days, burn rate exceeds $40k/month, or runway drops below 4 months."

### Manual Check
> "Run a KPI check on Acme Corp right now and tell me which thresholds are breached."

### Threshold Adjustment
> "Update the gross margin alert for TechStartup to yellow at 45% and red at 35%."

### Report Generation
> "Generate a weekly KPI summary for all active clients and post to the #weekly-metrics Telegram channel."

---

## KPI Calculation Reference

### Cash Runway
```
Runway (months) = Current Cash Balance / Average Monthly Burn Rate
Average Monthly Burn = (Cash 3 months ago - Cash today) / 3
```

### Days Sales Outstanding (DSO)
```
DSO = (Accounts Receivable / Revenue) × 30
```

### Burn Rate
```
Net Burn = Total Cash Outflows - Total Cash Inflows (monthly)
Gross Burn = Total Cash Outflows only (monthly)
```

### Current Ratio
```
Current Ratio = Current Assets / Current Liabilities
```

### AR Aging Concentration Risk
```
90+ Day Concentration = AR 90+ days / Total AR × 100
Alert when concentration > 20%
```

---

## Multi-Client Monitoring Pattern

For firms managing multiple clients:

```yaml
# master-kpi-config.yaml
clients:
  - name: "Acme Corp"
    config: "./clients/acme/kpi-config.yaml"
    qbo_realm: "123456789"
  
  - name: "TechStartup LLC"
    config: "./clients/techstartup/kpi-config.yaml"
    qbo_realm: "987654321"
    
  - name: "Retail Co"
    config: "./clients/retailco/kpi-config.yaml"
    data_source: csv
    csv_path: "/data/retailco/monthly-export.csv"
```

Loop pattern:
> "Check KPI thresholds for all clients in master-kpi-config.yaml. Consolidate alerts into one Telegram message grouped by client."

---

## Negative Boundaries — When NOT to Use This Skill

- **Real-time stock/crypto price alerts** → use defi-position-tracker or a dedicated market data feed
- **Live BI dashboards** (charts, drill-downs) → use Power BI, Looker, or Metabase
- **ERP systems** (SAP, Oracle, NetSuite) → requires dedicated API connectors, not this skill
- **Sub-minute alerting** (high-frequency trading signals) → wrong latency class
- **PTIN-regulated tax analysis** → use qbo-to-tax-bridge (Moltlaunch service only)
- **Client-facing automated reports** → requires Irfan approval before sending externally
- **Write operations to QBO** → read-only by default; journal entries need explicit approval

---

## Integration Stack

| Layer | Tool |
|-------|------|
| Data Pull (QBO) | qbo-automation skill |
| Data Pull (Sheets) | gog skill |
| Alerting (Telegram) | message tool (channel=telegram) |
| Scheduling | cron tool |
| Storage | workspace/clients/<name>/kpi-data/ |
| Config Format | YAML (kpi-config-<client>.yaml) |

---

## Alert Severity Guide

| Color | Meaning | Response Time |
|-------|---------|---------------|
| 🔴 RED | Threshold critically breached — action required | Same day |
| 🟡 YELLOW | Warning zone — monitor closely | Within 48 hours |
| ✅ GREEN | Within acceptable range | No action needed |

---

_KPI Alert System — PrecisionLedger Skill v1.0.0_
