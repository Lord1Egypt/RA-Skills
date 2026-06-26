---
name: Trigger Order Webhooks, Sync with Google Sheets & Send Alerts via Slack
description: "Automate order routing, fulfillment, and inventory management across channels. Use when the user needs real-time order processing, multi-warehouse routing, or complex fulfillment workflows for e-commerce operations."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["SHOPIFY_API_KEY", "SHOPIFY_API_PASSWORD", "WAREHOUSE_API_TOKEN", "SLACK_WEBHOOK_URL"],
        "bins": ["curl", "node"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "📦"
    }
  }
---

# OrderFlow: Intelligent E-Commerce Order Management

## Overview

OrderFlow is a production-grade order management automation skill that transforms how online businesses handle fulfillment. Unlike basic trigger-based automation, OrderFlow orchestrates complex order workflows across multiple channels, warehouses, and fulfillment partners in real time.

**Why OrderFlow matters:**
- **Multi-channel unification** — Consolidate orders from Shopify, WooCommerce, BigCommerce, and custom APIs into a single intelligent routing system
- **Smart inventory orchestration** — Automatically route orders to optimal fulfillment locations based on stock levels, shipping zones, and carrier rates
- **Workflow customization** — Define complex rules: "If order > $500 AND customer = VIP AND item in warehouse_A, then use expedited shipping and add gift wrap"
- **Real-time visibility** — Integrate with Slack, email, and dashboards to notify teams of order status, bottlenecks, and exceptions
- **Seamless integrations** — Works with Shopify, WooCommerce, 3PL APIs (ShipBob, Flexport), shipping carriers (FedEx, UPS, USPS), and inventory systems

**Key integrations:** Shopify, WooCommerce, Slack, Google Sheets, Twilio SMS, SendGrid, Zapier.

---

## Quick Start

Try these example prompts immediately:

### Example 1: Route High-Value Orders to Priority Warehouse
```
Route all orders over $500 to warehouse_east if inventory available, 
otherwise warehouse_central. Notify #orders-team in Slack when a VIP 
customer order is processed. Log the routing decision to Google Sheets.
```

### Example 2: Auto-Fulfill Based on Inventory Levels
```
Create a workflow: if product_id=SKU123 has stock > 100 in warehouse_west, 
ship from west (2-day delivery). If stock < 100, ship from warehouse_central 
(5-day delivery). Notify customer via email based on selected warehouse.
```

### Example 3: Smart Inventory Sync & Low-Stock Alerts
```
Sync real-time inventory across Shopify, WooCommerce, and internal database 
every 15 minutes. If any product drops below 20 units, send SMS alert to 
inventory manager and create a PO draft in Google Sheets.
```

### Example 4: Complex Multi-Condition Fulfillment Logic
```
IF order source = Shopify AND order value > $1000 AND customer location = California 
AND warehouse_la stock > 0 THEN route to warehouse_la, include gift receipt, 
send priority label via email. Otherwise route to default warehouse and 
auto-generate shipping label via ShipStation.
```

---

## Capabilities

### 1. **Intelligent Order Routing**
- Evaluate orders against 50+ custom conditions (customer tier, order value, destination, product type, inventory levels)
- Automatically route to optimal fulfillment location based on:
  - Stock availability across multiple warehouses
  - Shipping cost optimization
  - Delivery time zone requirements
  - Customer VIP status and preferences
- **Example:** "Route all California orders under $200 to warehouse_la. Route all international orders to warehouse_central (has international contracts). Route B2B orders to warehouse_b2b."

### 2. **Real-Time Inventory Management**
- Sync inventory from multiple sources (Shopify, WooCommerce, Magento, custom REST APIs) every 5-30 minutes
- Automatic stock level reconciliation across channels to prevent overselling
- Set minimum stock thresholds and trigger automated reorder workflows
- Track inventory by warehouse, SKU, and variant level
- **Example:** Configure thresholds—when product hits 15 units, auto-email supplier; when hits 5, escalate to manager.

### 3. **Fulfillment Automation**
- Auto-generate shipping labels for USPS, FedEx, UPS, DHL, and regional carriers
- Select carrier based on weight, destination, delivery speed, and cost optimization
- Batch process orders and send labels directly to fulfillment team or printer
- Integration with ShipStation, Shippo, and direct carrier APIs
- Support for multiple fulfillment scenarios: drop-ship, 3PL, in-house, hybrid

### 4. **Customizable Workflow Engine**
- Build if/then/else workflows with visual rule builder or code
- Chain multiple actions: route → label → notify → log → sync
- Set up approval workflows for high-value or exception orders
- Schedule recurring workflows (daily inventory sync, weekly reporting)
- **Example:** "IF inventory < threshold AND supplier response time > 48 hours THEN escalate to secondary supplier"

### 5. **Exception & Alert Management**
- Auto-detect fulfillment exceptions: insufficient stock, invalid address, payment issues
- Route exceptions to appropriate teams via Slack, email, SMS, or dashboard
- Create escalation rules: unresolved orders trigger manager alert after 4 hours
- Provide detailed exception reports with recommended actions

### 6. **Real-Time Notifications**
- Slack integration with rich message cards showing order status, routing decisions, and inventory alerts
- Email notifications with order summaries, shipping confirmation, tracking links
- SMS alerts for urgent issues (stockouts, delivery failures)
- Webhook integration to push updates to custom dashboards

### 7. **Reporting & Analytics**
- Dashboard showing order fulfillment KPIs: avg fulfillment time, warehouse utilization, carrier performance
- Export reports to Google Sheets, CSV, or Power BI
- Track which routing rules are most effective and expensive
- Identify fulfillment bottlenecks and optimization opportunities

---

## Configuration

### Environment Variables (Required)

```bash
# E-commerce Platform
SHOPIFY_API_KEY=your_key_here
SHOPIFY_API_PASSWORD=your_password_here
SHOPIFY_STORE_URL=yourstore.myshopify.com

# Inventory & Warehouse
WAREHOUSE_API_TOKEN=your_token_here
WAREHOUSE_API_URL=https://warehouse.example.com/api

# Notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
SENDGRID_API_KEY=your_sendgrid_key_here
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token

# Shipping & Fulfillment
SHIPSTATION_API_KEY=your_key
SHIPPO_API_TOKEN=your_token
```

### Workflow Configuration (JSON)

Create an `orderflow-config.json` file in your OrderFlow directory:

```json
{
  "routing_rules": [
    {
      "id": "rule_vip_priority",
      "name": "Route VIP orders to priority warehouse",
      "conditions": {
        "customer_tier": "VIP",
        "order_value": { "gte": 500 }
      },
      "actions": {
        "warehouse": "warehouse_priority",
        "shipping_speed": "expedited",
        "notification": "slack_channel:vip_orders"
      }
    },
    {
      "id": "rule_inventory_fallback",
      "name": "Fallback routing on stock shortage",
      "conditions": {
        "primary_warehouse_stock": { "lt": 1 },
        "product_category": "electronics"
      },
      "actions": {
        "warehouse": "warehouse_fallback",
        "notify_inventory_team": true,
        "log_exception": true
      }
    }
  ],
  "inventory_sync": {
    "enabled": true,
    "interval_minutes": 15,
    "sources": ["shopify", "woocommerce", "custom_api"],
    "low_stock_threshold": 20,
    "critical_stock_threshold": 5
  },
  "fulfillment": {
    "default_carrier": "usps",
    "carrier_selection": "cost_optimized",
    "auto_generate_labels": true,
    "batch_processing": true,
    "batch_size": 50
  },
  "notifications": {
    "slack_enabled": true,
    "email_enabled": true,
    "sms_enabled": true,
    "sms_recipients": ["+1-555-0100"]
  }
}
```

### Setup Instructions

1. **Install OrderFlow CLI:**
   ```bash
   npm install -g orderflow-cli
   orderflow init
   ```

2. **Authenticate integrations:**
   ```bash
   orderflow auth shopify --api-key YOUR_KEY --api-password YOUR_PASSWORD
   orderflow auth warehouse --token YOUR_TOKEN
   orderflow auth slack --webhook YOUR_WEBHOOK_URL
   ```

3. **Deploy configuration:**
   ```bash
   orderflow config:deploy orderflow-config.json
   orderflow workflows:activate
   ```

4. **Test end-to-end:**
   ```bash
   orderflow test --order-id test_12345
   ```

---

## Example Outputs

### Order Routing Decision (Slack Notification)

```
📦 Order Routed Successfully

Order ID: #ORD-2024-087654
Customer: Acme Corp (VIP)
Total: $2,450.00
Items: 12x Widget Pro, 4x ServicePack

🎯 Routing Decision:
├─ Primary Warehouse: warehouse_east
├─ Reason: VIP priority + lowest shipping cost ($45 vs $89)
├─ Stock Check: ✓ In stock (47 units available)
├─ Estimated Delivery: Jan 18-20, 2024
└─ Shipping Label: Generated & queued to printer

💬 Actions Taken:
✓ Label generated (FedEx 2-Day)
✓ Inventory reserved (12x SKU123, 4x SKU456)
✓ Customer notified via email
✓ Fulfillment team alerted in #fulfillment

Confidence: 98% | Route Score: 9.2/10
```

### Inventory Sync Report (Google Sheets)

| Product | SKU | Warehouse A | Warehouse B | Total | Status | Last Sync |
|---------|-----|------------|------------|-------|--------|-----------|
| Widget Pro | SKU123 | 47 | 12 | 59 | ✓ Good | 2024-01-16 10:15 AM |
| ServicePack | SKU456 | 3 | 28 | 31 | ⚠️ Low | 2024-01-16 10:15 AM |
| Premium Bundle | SKU789 | 0 | 8 | 8 | 🔴 Critical | 2024-01-16 10:15 AM |

### Fulfillment Exception Alert (Email)

```
Subject: ⚠️ Fulfillment Exception: Order #ORD-2024-087654

High-Priority Issue Detected

Order #ORD-2024-087654 (Acme Corp, $2,450)
Status: EXCEPTION - Inventory Mismatch
Time Detected: Jan 16, 2024, 10:30 AM

Problem:
• Ordered quantity: 12x Widget Pro
• Available in warehouse_east: 11 units (changed since routing)
• Status: PARTIALLY FULFILLABLE

Recommended Actions:
1. Source 1 unit from warehouse_central (in stock, +$12 shipping)
2. Split shipment: 11 from warehouse_east, 1 from warehouse_central
3. Contact customer & offer 10% discount for split delivery
4. Escalate to Ops Manager if not resolved in 2 hours

Action Required: YES | Severity: Medium | Auto-Escalate In: 1h 45m
```

---

## Tips & Best Practices

### 1. **Master Warehouse Scoring**
Design your routing rules to score warehouses based on multiple factors:
- **Stock availability** (50 points if in stock, -100 if out of stock)
- **Distance/shipping cost** (vary by destination)
- **Speed capability** (50 points if warehouse can meet delivery SLA)
- **Utilization** (penalize over-utilized warehouses)

Use weighted scoring to automatically select the best warehouse, avoiding manual decision-making bottlenecks.

### 2. **Implement Smart Fallback Chains**
Define 3-4 fallback warehouses in priority order. When primary warehouse can't fulfill:
1. Try secondary warehouse
2. If unavailable, try tertiary warehouse
3. If all fail, trigger exception workflow (backorder, split shipment, or external 3PL)

This prevents order rejections and keeps fulfillment flowing.

### 3. **Set Realistic Inventory Thresholds**
- **Reorder threshold:** Trigger PO when stock hits 20% of monthly demand
- **Safety stock:** Keep 10-15% buffer above reorder threshold
- **Critical threshold:** Alert team at 5% of monthly demand
- **Review monthly:** Adjust based on demand variability and supplier lead times

### 4. **Automate Low-Touch Workflows**
Identify orders that don't require human intervention:
- Standard domestic orders under $500 ✓ Auto-route and label
- International orders or exceptions ✓ Route to queue for review
- VIP or complex scenarios ✓ Require approval

Target: 70-80% of orders auto-fulfilled, 20-30% requiring human review.

### 5. **Monitor & Optimize Carrier Performance**
Track per-carrier metrics:
- On-time delivery rate (target: >95%)
- Cost per shipment vs. market average
- Damage/loss rates
- Customer satisfaction rating

Rotate carriers quarterly or use dynamic selection based on real-time performance.

### 6. **Integrate with Your Accounting System**
Export fulfillment costs to your accounting software (QuickBooks, Xero, NetSuite) to calculate true product margins and identify unprofitable order types.

### 7. **Use A/B Testing for Routing Rules**
Test two routing strategies on 10% of orders:
- Strategy A: Cost-optimized routing
- Strategy B: Speed-optimized routing

Measure fulfillment time, shipping cost, and customer satisfaction. Roll out winner to 100% of orders.

---

## Safety & Guardrails

### What OrderFlow Will NOT Do

❌ **Not a fraud detection system.** OrderFlow does not validate payment legitimacy, detect credit card fraud, or flag suspicious accounts. Integrate with third-party fraud tools (Sift, MaxMind) for that.

❌ **Not a customer communication platform.** OrderFlow sends transactional notifications (routing decisions, shipping alerts) but does not handle general customer support, returns/refunds, or dispute resolution. Use Zendesk, Gorgias, or similar for customer service.

❌ **Not a financial forecasting tool.** Reporting shows fulfillment costs and metrics but does not predict demand, manage cash flow, or provide business strategy recommendations.

❌ **Not a compliance or tax system.** Does not calculate sales tax, VAT, duties, or enforce shipping regulations. Integrate with TaxJar or Vertex for tax compliance.

❌ **Not a data migration tool.** Cannot bulk import legacy orders or perform complex data transformations. Use ETL tools (Talend, Stitch) for one-time migrations.

### Limitations & Boundaries

- **Rate limits:** Most carrier APIs limit to 100-500 label requests/minute. Batch processing may add 5-15 second delays during peak volume.
- **Real-time sync latency:** Inventory sync occurs every 5-30 minutes; same-minute sync requires direct API integration (additional setup).
- **Warehouse capacity:** Assumes warehouses don't have space/weight constraints. Add custom capacity checks if needed.
- **International shipping:** Requires additional configuration for customs documentation, international carriers, and duty calculations.
- **Order size:** Tested with up to 10,000 orders/day per instance. Scale horizontally for larger volumes.

### Privacy & Security

- Credentials stored in encrypted environment variables; never logged or transmitted in plain text
- Warehouse location data and inventory levels not shared externally
- Webhook payloads