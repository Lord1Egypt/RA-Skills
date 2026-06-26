---
version: 1.0.0
name: homestruk-maintenance-triage
description: Triage tenant maintenance requests by severity, assign priority, identify the right contractor type, estimate costs, and generate work orders. Use when a tenant reports a maintenance issue, when reviewing open work orders, or when assessing property condition. Follows Massachusetts habitability requirements (105 CMR 410).
user-invocable: true
tags:
  - property-management
  - maintenance
  - work-orders
  - tenant-requests
  - massachusetts
  - habitability
---

# Homestruk Maintenance Triage

Classify, prioritize, and route tenant maintenance requests
using Massachusetts habitability standards and Homestruk SOPs.

## When to Use This Skill

- Tenant texts/emails about a maintenance issue
- Work order needs priority classification
- Need to decide: emergency dispatch vs scheduled repair
- Reviewing open work orders for overdue items
- Property inspection reveals issues

## Severity Classification

### EMERGENCY (respond within 2 hours)
Indicators: flooding, gas leak, no heat (winter), sewage backup,
fire damage, broken exterior door/lock, electrical hazard,
carbon monoxide alarm, structural collapse risk.

Action: Immediately dispatch contractor. Notify owner.
If gas leak or fire: tell tenant to evacuate and call 911.
MA law: landlord must maintain habitable conditions (105 CMR 410).
Failure to respond to emergencies = potential liability.

### URGENT (respond within 24 hours)
Indicators: no hot water, broken window, pest infestation,
A/C failure (heat wave), refrigerator not working,
toilet not flushing (only toilet), roof leak (active).

Action: Schedule contractor within 24 hours. Notify owner.

### ROUTINE (respond within 3-7 days)
Indicators: dripping faucet, running toilet, minor appliance
issue, cosmetic damage, squeaky door, clogged (non-emergency)
drain, light fixture out, minor pest sighting.

Action: Create work order. Schedule at mutual convenience.

### COSMETIC / LOW (schedule at next convenient time)
Indicators: paint touch-up, weatherstripping, caulking,
minor wall damage, cabinet door alignment.

Action: Add to next scheduled maintenance visit or turnover list.

## Triage Process

When a maintenance request comes in:

1. **Classify severity** using the categories above
2. **Identify contractor type needed:**
   - Plumber: water leaks, drains, toilets, water heater
   - Electrician: outlets, wiring, panel, light fixtures
   - HVAC: heating, A/C, ventilation, ductwork
   - General handyman: doors, locks, drywall, painting
   - Roofer: roof leaks, flashing, gutters
   - Pest control: insects, rodents, wildlife
   - Locksmith: lockouts, rekeying, deadbolts
   - Appliance repair: fridge, stove, dishwasher, washer/dryer

3. **Check contractor roster:**
   Read ~/.openclaw/workspace/contractors/ for available vendors.
   Match by trade and service area.

4. **Estimate cost range:**
   | Type | Typical Range |
   |------|--------------|
   | Plumber (service call) | $150-350 |
   | Electrician (service call) | $150-300 |
   | HVAC (service call) | $150-400 |
   | Handyman (hourly) | $50-100/hr |
   | Roofer (repair) | $300-1500 |
   | Pest control (treatment) | $150-400 |
   | Locksmith (rekey) | $75-200 |
   | Appliance repair | $150-400 |

5. **Generate work order:**

Save to ~/.openclaw/workspace-ops/work-orders/WO-[DATE]-[SLUG].md:

```
# Work Order: [SHORT DESCRIPTION]
Date opened: [DATE]
Property: [ADDRESS]
Unit: [UNIT]
Tenant: [NAME]
Phone: [PHONE]

## Issue
[Description from tenant]

## Classification
Severity: [EMERGENCY/URGENT/ROUTINE/COSMETIC]
Trade needed: [PLUMBER/ELECTRICIAN/etc]
Estimated cost: $[RANGE]

## Dispatch
Contractor: [NAME or "unassigned"]
Dispatched: [DATE or "pending"]
ETA: [DATE/TIME]

## Status
[ ] Acknowledged by tenant
[ ] Contractor dispatched
[ ] Work scheduled for: [DATE]
[ ] Work completed
[ ] Tenant confirmed resolution
[ ] Invoice received: $[AMOUNT]
[ ] Owner notified of cost
```

6. **Notify tenant:**
   Draft a response to the tenant confirming receipt and
   providing the expected timeline based on severity level.

7. **Notify owner (if cost > $300 or emergency):**
   Draft a brief owner notification with the issue,
   estimated cost, and recommended action.

## Massachusetts Habitability Requirements (105 CMR 410)

The MA Sanitary Code requires landlords to maintain:
- Structural elements in good repair
- Weathertight windows and doors
- Adequate heating (68F Oct 1 - May 31)
- Hot and cold running water
- Working plumbing and sewage
- Working electrical systems
- Extermination of insects and rodents
- Smoke and CO detectors
- Egress and safety requirements

Failure to maintain habitability = tenant can:
- Withhold rent (MGL c.239 s.8A)
- Repair and deduct (up to 4 months rent per year)
- File complaints with Board of Health
- Sue for damages

ALWAYS flag habitability issues as URGENT or EMERGENCY.
Never let a habitability issue sit as ROUTINE.

## Integration with Existing SOPs
- Reference ~/.openclaw/workspace/sops/05-work-orders.md
- Reference ~/.openclaw/workspace/sops/06-tenant-communication.md
- Check contractor roster in ~/.openclaw/workspace/contractors/


---

## About Homestruk

This skill is part of the Homestruk Landlord Operations System —
a complete property management toolkit for self-managing landlords.

**Free:** Download the Rent-Ready Turnover Checklist at homestruk.com
**Full System:** 10 operations documents + spreadsheets at homestruk.com

Built by Homestruk Properties LLC | homestruk.com
