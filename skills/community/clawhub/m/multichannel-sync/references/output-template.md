# Multichannel Sync Plan — Output Template

## 1. Executive Summary

**Business:** [Company name and description]
**Active channels:** [List all sales channels with monthly volume]
**Anchor channel:** [Primary channel driving pricing and inventory decisions]
**Total SKU count:** [Number of active SKUs across all channels]
**Primary sync challenge:** [One-sentence description of the biggest pain point]
**Plan version:** [Date]

---

## 2. Channel Architecture Map

### Channel Inventory

| Channel | Platform | Monthly Orders | AOV | Revenue Share | Fulfillment Method | Current Sync Method | Sync Frequency |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

### Integration Stack

| System | Role | Channels Connected | API Status |
|---|---|---|---|
| | | | |

### Pain Point Inventory

| Issue | Frequency | Impact | Affected Channels |
|---|---|---|---|
| | | | |

---

## 3. Inventory Synchronization Model

### Pool Structure
- **Model type:** [Single pool / Split pool / Hybrid]
- **Source of truth:** [System name]
- **Rationale:** [Why this model was chosen]

### Buffer Calculations

| SKU / Category | Daily Velocity | Lead Time | Base Buffer | Channel Risk Multiplier | Final Buffer | Low-Stock Threshold |
|---|---|---|---|---|---|---|
| | | | | | | |

### Sync Frequency Assignments

| SKU Tier | Sync Frequency | Trigger | Channels |
|---|---|---|---|
| High velocity / Hero SKUs | Real-time (< 5 min) | | |
| Standard SKUs | Near-time (15-30 min) | | |
| Slow-moving / Long-tail | Batch (hourly+) | | |

### Low-Stock Throttling Rules

| Total Stock Level | Action | Channels Affected |
|---|---|---|
| < [X] units | Pause [channel] listing | |
| < [Y] units | Pause [channels] listings | |
| < [Z] units | Pause all except [anchor channel] | |

---

## 4. Pricing Architecture

### Anchor Pricing Model

| Channel | Relationship to Anchor | Allowed Differential | Notes |
|---|---|---|---|
| [Anchor channel] | Anchor price | — | |
| | | | |

### Parity Compliance Matrix

| Channel A | Channel B | Monitoring Direction | Parity Rule | Violation Consequence |
|---|---|---|---|---|
| | | | | |

### Promotion Pricing Rules

| Promotion Type | Allowed Channels | Pricing Method | Parity Impact | Required Actions |
|---|---|---|---|---|
| Flash sale | | | | |
| Coupon / code | | | | |
| Bundle discount | | | | |
| Clearance | | | | |

### Per-Channel Margin Analysis

| SKU / Category | Channel | List Price | Fees | Shipping | Returns | Net Margin |
|---|---|---|---|---|---|---|
| | | | | | | |

---

## 5. Listing Content Strategy

### Field-Level Content Mapping

| Field | [Channel 1] | [Channel 2] | [Channel 3] | Sync Rule |
|---|---|---|---|---|
| Product title | | | | Adapted |
| Bullet points | | | | Adapted |
| Description | | | | Adapted |
| Images | | | | Adapted |
| Price | | | | Rule-based |
| UPC/EAN | | | | Identical |
| Weight/Dimensions | | | | Identical |

### Content Update Propagation

| Field Type | Source of Truth | Auto-Sync Channels | Manual Update Channels | Review Required |
|---|---|---|---|---|
| | | | | |

---

## 6. Promotion Coordination Playbook

### Pre-Launch Checklist (48-72 hours before)
- [ ] Inventory covers projected demand + buffer across all channels
- [ ] Pricing parity implications reviewed and mitigated
- [ ] Promotion inventory reserved in sync system
- [ ] Channel notifications sent where required
- [ ] Promotional content staged per channel
- [ ] Low-stock auto-pause rules configured for non-promotion channels

### During Promotion
- [ ] Real-time inventory monitoring active (alerts at 25%, 10%, 5%)
- [ ] Parity alert dashboard monitored
- [ ] Channel velocity tracked for buffer reallocation

### Post-Promotion
- [ ] Actual vs. projected demand reconciled per channel
- [ ] Standard pricing restored within [X] hours
- [ ] Promotional content removed from all channels
- [ ] Oversells and parity violations documented
- [ ] Buffer calculations updated with actual data

---

## 7. Exception Handling Playbooks

### Oversell Response (< 1 hour SLA)
1. Identify affected channel(s) and order(s)
2. Check fulfillable inventory across all locations
3. If fulfillable: [expedite procedure]
4. If not fulfillable: [cancellation and compensation procedure]
5. Root cause: [sync delay / buffer error / manual error]
6. Prevention: [buffer adjustment / frequency increase]

### Price Parity Violation Response (< 4 hours)
1. Identify triggering channel and cause
2. Correct offending price immediately
3. Submit marketplace appeal if needed
4. Update compliance matrix
5. Review promotion cascade rules

### Listing Suspension Response (< 24 hours)
1. Identify suspension reason
2. Assess cross-channel impact
3. Prepare platform-specific appeal
4. Monitor sales impact on other channels
5. Update compliance checklist

---

## 8. Monitoring and Reconciliation

### Dashboard Metrics

| Metric | Target | Alert Threshold | Check Frequency |
|---|---|---|---|
| Inventory drift | 0 units | > 5 units | Real-time |
| Sync latency | < 5 min | > 30 min | Real-time |
| Oversell rate | 0% | Any occurrence | Daily |
| Parity violations | 0 | Any occurrence | Daily |
| Listing accuracy | 100% | < 95% | Weekly |

### Reconciliation Schedule
- **Real-time:** Automated inventory drift detection and sync latency monitoring
- **Daily:** Detailed inventory reconciliation across all channels
- **Weekly:** Buffer adequacy review, sync failure analysis, channel performance comparison
- **Monthly:** Full sync health report with oversell rate, parity compliance, and manual intervention count
